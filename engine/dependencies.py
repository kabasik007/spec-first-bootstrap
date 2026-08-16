from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

from .utils import read_json, read_text, rel, walk_files


def dependency_graph(root: Path) -> dict:
    nodes: Dict[str, dict] = {
        "project:root": {"id": "project:root", "kind": "project", "name": root.name}
    }
    edges: List[dict] = []
    manifests: List[str] = []

    def add(ecosystem: str, name: str, constraint: str = "", scope: str = "runtime", source: str = ""):
        if not name:
            return
        node_id = f"{ecosystem}:{name}"
        nodes.setdefault(node_id, {
            "id": node_id, "kind": "dependency", "ecosystem": ecosystem,
            "name": name, "constraint": constraint or "", "sources": [],
        })
        if source and source not in nodes[node_id]["sources"]:
            nodes[node_id]["sources"].append(source)
        edges.append({"from": "project:root", "to": node_id, "scope": scope, "source": source})

    composer = root / "composer.json"
    if composer.exists():
        manifests.append("composer.json")
        obj = read_json(composer, {})
        for scope, key in [("runtime", "require"), ("development", "require-dev")]:
            for name, version in (obj.get(key) or {}).items():
                if name == "php" or name.startswith("ext-"):
                    continue
                add("composer", name, str(version), scope, "composer.json")

    package = root / "package.json"
    if package.exists():
        manifests.append("package.json")
        obj = read_json(package, {})
        for scope, key in [
            ("runtime", "dependencies"), ("development", "devDependencies"),
            ("peer", "peerDependencies"), ("optional", "optionalDependencies"),
        ]:
            for name, version in (obj.get(key) or {}).items():
                add("npm", name, str(version), scope, "package.json")

    requirements = root / "requirements.txt"
    if requirements.exists():
        manifests.append("requirements.txt")
        for line in read_text(requirements).splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            m = re.match(r"([A-Za-z0-9_.-]+)\s*([<>=!~].*)?$", line)
            if m:
                add("pypi", m.group(1), (m.group(2) or "").strip(), "runtime", "requirements.txt")

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        manifests.append("pyproject.toml")
        data = read_text(pyproject)
        for block in re.findall(r"dependencies\s*=\s*\[(.*?)\]", data, flags=re.S):
            for item in re.findall(r'["\']([^"\']+)["\']', block):
                m = re.match(r"([A-Za-z0-9_.-]+)\s*(.*)", item)
                if m:
                    add("pypi", m.group(1), m.group(2).strip(), "runtime", "pyproject.toml")

    cargo = root / "Cargo.toml"
    if cargo.exists():
        manifests.append("Cargo.toml")
        section = None
        for line in read_text(cargo).splitlines():
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                section = stripped.strip("[]")
                continue
            if section in {"dependencies", "dev-dependencies", "build-dependencies"}:
                m = re.match(r"([A-Za-z0-9_-]+)\s*=\s*(.+)", stripped)
                if m:
                    constraint = m.group(2).strip().strip('"')
                    scope = "development" if section == "dev-dependencies" else "runtime"
                    add("cargo", m.group(1), constraint, scope, "Cargo.toml")

    go = root / "go.mod"
    if go.exists():
        manifests.append("go.mod")
        data = read_text(go)
        for name, version in re.findall(r"^\s*([A-Za-z0-9_./-]+)\s+(v[0-9][^\s]*)", data, flags=re.M):
            add("go", name, version, "runtime", "go.mod")

    pom = root / "pom.xml"
    if pom.exists():
        manifests.append("pom.xml")
        data = read_text(pom)
        for block in re.findall(r"<dependency>(.*?)</dependency>", data, flags=re.S):
            group = _xml(block, "groupId")
            artifact = _xml(block, "artifactId")
            version = _xml(block, "version")
            scope = _xml(block, "scope") or "runtime"
            if artifact:
                add("maven", f"{group}:{artifact}" if group else artifact, version, scope, "pom.xml")

    for csproj in root.glob("**/*.csproj"):
        if any(part in {"vendor", "node_modules", ".git", ".ai"} for part in csproj.parts):
            continue
        source = rel(root, csproj)
        manifests.append(source)
        data = read_text(csproj)
        for name, version in re.findall(r'<PackageReference\s+Include="([^"]+)"(?:\s+Version="([^"]*)")?', data):
            add("nuget", name, version, "runtime", source)

    return {
        "schema_version": 1,
        "manifests": sorted(set(manifests)),
        "nodes": sorted(nodes.values(), key=lambda x: x["id"]),
        "edges": edges,
        "summary": {
            "dependency_count": len(nodes) - 1,
            "manifest_count": len(set(manifests)),
            "ecosystems": sorted({n.get("ecosystem") for n in nodes.values() if n.get("ecosystem")}),
        },
    }


def _xml(block: str, tag: str) -> str:
    m = re.search(fr"<{tag}>(.*?)</{tag}>", block, flags=re.S)
    return m.group(1).strip() if m else ""


def render_dependency_md(graph: dict) -> str:
    lines = [
        "# Dependency Graph", "",
        "Generated from local dependency manifests. It is evidence, not a full runtime call graph.", "",
        f"- Manifests: {graph['summary']['manifest_count']}",
        f"- Dependencies: {graph['summary']['dependency_count']}",
        f"- Ecosystems: {', '.join(graph['summary']['ecosystems']) or 'none detected'}", "",
        "## Direct dependencies", "",
    ]
    count = 0
    for node in graph["nodes"]:
        if node["kind"] != "dependency":
            continue
        count += 1
        constraint = f" `{node.get('constraint')}`" if node.get("constraint") else ""
        lines.append(f"- **{node.get('ecosystem')}** `{node['name']}`{constraint}")
    if not count:
        lines.append("- No supported dependency manifest entries detected.")
    return "\n".join(lines) + "\n"
