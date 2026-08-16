from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

from .utils import read_json, read_text, rel, walk_files


MANIFEST_NAMES = {
    "composer.json", "package.json", "requirements.txt", "pyproject.toml",
    "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "build.gradle.kts",
}


def _manifest_files(root: Path) -> List[Path]:
    files = walk_files(root)
    manifests = [p for p in files if p.name in MANIFEST_NAMES or p.suffix.lower() == ".csproj"]
    return sorted(manifests, key=lambda p: rel(root, p))


def _component_id(root: Path, manifest: Path) -> str:
    parent = manifest.parent
    if parent == root:
        return "project:root"
    return "component:" + rel(root, parent)


def dependency_graph(root: Path) -> dict:
    nodes: Dict[str, dict] = {
        "project:root": {"id": "project:root", "kind": "project", "name": root.name, "path": "."}
    }
    edges: List[dict] = []
    manifests: List[str] = []
    components: Dict[str, dict] = {}

    def ensure_component(manifest: Path) -> str:
        component_id = _component_id(root, manifest)
        if component_id == "project:root":
            return component_id
        component_path = rel(root, manifest.parent)
        components.setdefault(component_id, {
            "id": component_id,
            "kind": "component",
            "name": manifest.parent.name,
            "path": component_path,
            "manifests": [],
        })
        source = rel(root, manifest)
        if source not in components[component_id]["manifests"]:
            components[component_id]["manifests"].append(source)
        nodes.setdefault(component_id, components[component_id])
        edge = {"from": "project:root", "to": component_id, "scope": "contains", "source": source}
        if edge not in edges:
            edges.append(edge)
        return component_id

    def add(component_id: str, ecosystem: str, name: str, constraint: str = "", scope: str = "runtime", source: str = ""):
        if not name:
            return
        node_id = "{}:{}".format(ecosystem, name)
        nodes.setdefault(node_id, {
            "id": node_id,
            "kind": "dependency",
            "ecosystem": ecosystem,
            "name": name,
            "constraint": constraint or "",
            "sources": [],
        })
        if source and source not in nodes[node_id]["sources"]:
            nodes[node_id]["sources"].append(source)
        edges.append({"from": component_id, "to": node_id, "scope": scope, "source": source})

    for manifest in _manifest_files(root):
        source = rel(root, manifest)
        manifests.append(source)
        component_id = ensure_component(manifest)
        name = manifest.name

        if name == "composer.json":
            obj = read_json(manifest, {})
            for scope, key in [("runtime", "require"), ("development", "require-dev")]:
                for package, version in (obj.get(key) or {}).items():
                    if package == "php" or package.startswith("ext-"):
                        continue
                    add(component_id, "composer", package, str(version), scope, source)
            continue

        if name == "package.json":
            obj = read_json(manifest, {})
            for scope, key in [
                ("runtime", "dependencies"), ("development", "devDependencies"),
                ("peer", "peerDependencies"), ("optional", "optionalDependencies"),
            ]:
                for package, version in (obj.get(key) or {}).items():
                    add(component_id, "npm", package, str(version), scope, source)
            continue

        if name == "requirements.txt":
            for line in read_text(manifest).splitlines():
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("-"):
                    continue
                match = re.match(r"([A-Za-z0-9_.-]+)\s*([<>=!~].*)?$", line)
                if match:
                    add(component_id, "pypi", match.group(1), (match.group(2) or "").strip(), "runtime", source)
            continue

        if name == "pyproject.toml":
            data = read_text(manifest)
            for block in re.findall(r"dependencies\s*=\s*\[(.*?)\]", data, flags=re.S):
                for item in re.findall(r'["\']([^"\']+)["\']', block):
                    match = re.match(r"([A-Za-z0-9_.-]+)\s*(.*)", item)
                    if match:
                        add(component_id, "pypi", match.group(1), match.group(2).strip(), "runtime", source)
            continue

        if name == "Cargo.toml":
            section = None
            for line in read_text(manifest).splitlines():
                stripped = line.strip()
                if stripped.startswith("[") and stripped.endswith("]"):
                    section = stripped.strip("[]")
                    continue
                if section in {"dependencies", "dev-dependencies", "build-dependencies"}:
                    match = re.match(r"([A-Za-z0-9_-]+)\s*=\s*(.+)", stripped)
                    if match:
                        constraint = match.group(2).strip().strip('"')
                        scope = "development" if section == "dev-dependencies" else "runtime"
                        add(component_id, "cargo", match.group(1), constraint, scope, source)
            continue

        if name == "go.mod":
            data = read_text(manifest)
            for package, version in re.findall(r"^\s*([A-Za-z0-9_./-]+)\s+(v[0-9][^\s]*)", data, flags=re.M):
                add(component_id, "go", package, version, "runtime", source)
            continue

        if name == "pom.xml":
            data = read_text(manifest)
            for block in re.findall(r"<dependency>(.*?)</dependency>", data, flags=re.S):
                group = _xml(block, "groupId")
                artifact = _xml(block, "artifactId")
                version = _xml(block, "version")
                scope = _xml(block, "scope") or "runtime"
                if artifact:
                    add(component_id, "maven", "{}:{}".format(group, artifact) if group else artifact, version, scope, source)
            continue

        if manifest.suffix.lower() == ".csproj":
            data = read_text(manifest)
            for package, version in re.findall(r'<PackageReference\s+Include="([^"]+)"(?:\s+Version="([^"]*)")?', data):
                add(component_id, "nuget", package, version, "runtime", source)
            continue

        # Gradle is recognized as a component/build boundary even though this lightweight
        # parser intentionally does not guess dependency expressions from arbitrary DSL code.

    dependency_nodes = [node for node in nodes.values() if node.get("kind") == "dependency"]
    return {
        "schema_version": 2,
        "manifests": sorted(set(manifests)),
        "components": sorted(components.values(), key=lambda item: item["id"]),
        "nodes": sorted(nodes.values(), key=lambda item: item["id"]),
        "edges": edges,
        "summary": {
            "dependency_count": len(dependency_nodes),
            "manifest_count": len(set(manifests)),
            "component_count": len(components),
            "ecosystems": sorted({node.get("ecosystem") for node in dependency_nodes if node.get("ecosystem")}),
        },
    }


def _xml(block: str, tag: str) -> str:
    match = re.search(r"<{}>(.*?)</{}>".format(tag, tag), block, flags=re.S)
    return match.group(1).strip() if match else ""


def render_dependency_md(graph: dict) -> str:
    lines = [
        "# Dependency Graph", "",
        "Generated from local dependency manifests. It is evidence, not a full runtime call graph.", "",
        "- Manifests: {}".format(graph["summary"]["manifest_count"]),
        "- Workspace components: {}".format(graph["summary"].get("component_count", 0)),
        "- Dependencies: {}".format(graph["summary"]["dependency_count"]),
        "- Ecosystems: {}".format(", ".join(graph["summary"]["ecosystems"]) or "none detected"), "",
        "## Workspace components", "",
    ]
    components = graph.get("components", [])
    if components:
        for component in components:
            lines.append("- `{}` — manifests: {}".format(component["path"], ", ".join(component.get("manifests", []))))
    else:
        lines.append("- No nested manifest-defined component detected.")

    lines += ["", "## Direct dependencies", ""]
    count = 0
    for node in graph["nodes"]:
        if node["kind"] != "dependency":
            continue
        count += 1
        constraint = " `{}`".format(node.get("constraint")) if node.get("constraint") else ""
        lines.append("- **{}** `{}`{}".format(node.get("ecosystem"), node["name"], constraint))
    if not count:
        lines.append("- No supported dependency manifest entries detected.")
    return "\n".join(lines) + "\n"
