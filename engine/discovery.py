from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Set

from .utils import find_by_name, read_json, read_text, rel, walk_files


@dataclass
class Fact:
    value: object
    confidence: float
    evidence: List[str]


def detect_languages(root: Path, files: List[Path]) -> Dict[str, Fact]:
    names = {p.name for p in files}
    suffixes: Dict[str, int] = {}
    for p in files:
        suffixes[p.suffix.lower()] = suffixes.get(p.suffix.lower(), 0) + 1
    checks = {
        "php": ("composer.json" in names or suffixes.get(".php", 0) > 2, ["composer.json" if "composer.json" in names else f"php_files={suffixes.get('.php', 0)}"]),
        "python": (bool({"pyproject.toml", "requirements.txt", "setup.py"} & names) or suffixes.get(".py", 0) > 2, ["python packaging/source markers"]),
        "node": ("package.json" in names or sum(suffixes.get(x, 0) for x in [".js", ".ts", ".tsx", ".jsx"]) > 3, ["package.json" if "package.json" in names else "js/ts sources"]),
        "go": ("go.mod" in names or suffixes.get(".go", 0) > 2, ["go.mod" if "go.mod" in names else "go sources"]),
        "rust": ("Cargo.toml" in names or suffixes.get(".rs", 0) > 2, ["Cargo.toml" if "Cargo.toml" in names else "rust sources"]),
        "java": (bool({"pom.xml", "build.gradle", "build.gradle.kts"} & names) or suffixes.get(".java", 0) > 2, ["java build/source markers"]),
        "dotnet": (any(p.suffix.lower() in {".csproj", ".fsproj", ".sln"} for p in files), [".NET project files"]),
    }
    return {name: Fact(True, 0.95, evidence) for name, (ok, evidence) in checks.items() if ok}


def detect_versions(root: Path, files: List[Path]) -> Dict[str, Fact]:
    versions: Dict[str, Fact] = {}
    composer = next(iter(find_by_name(files, "composer.json")), None)
    if composer:
        obj = read_json(composer, {})
        constraint = (obj.get("require") or {}).get("php") or (obj.get("config") or {}).get("platform", {}).get("php")
        if constraint:
            versions["php_constraint"] = Fact(str(constraint), 0.98, [rel(root, composer)])
    pyproject = next(iter(find_by_name(files, "pyproject.toml")), None)
    if pyproject:
        m = re.search(r'requires-python\s*=\s*["\']([^"\']+)', read_text(pyproject))
        if m:
            versions["python_constraint"] = Fact(m.group(1), 0.9, [rel(root, pyproject)])
    package = next(iter(find_by_name(files, "package.json")), None)
    if package:
        obj = read_json(package, {})
        node = (obj.get("engines") or {}).get("node")
        if node:
            versions["node_constraint"] = Fact(str(node), 0.95, [rel(root, package)])
    for p in files:
        r = rel(root, p)
        if r.endswith("system/startup.php") or r.endswith("index.php"):
            data = read_text(p, 80_000)
            for pattern in [
                r"define\s*\(\s*['\"]VERSION['\"]\s*,\s*['\"]([0-9.]+)['\"]",
                r"VERSION\s*=\s*['\"]([0-9.]+)['\"]",
            ]:
                m = re.search(pattern, data)
                if m:
                    versions.setdefault("opencart", Fact(m.group(1), 0.78, [r]))
                    break
    return versions


def dependency_text(files: List[Path]) -> str:
    chunks = []
    names = [
        "composer.json", "package.json", "pyproject.toml", "requirements.txt",
        "Cargo.toml", "go.mod", "pom.xml", "*.csproj",
    ]
    for name in names:
        if name.startswith("*"):
            candidates = [p for p in files if p.suffix == ".csproj"]
        else:
            candidates = find_by_name(files, name)
        for p in candidates[:3]:
            chunks.append(read_text(p, 100_000).lower())
    return "\n".join(chunks)


def detect_frameworks(root: Path, files: List[Path]) -> Dict[str, Fact]:
    deps = dependency_text(files)
    found: Dict[str, Fact] = {}

    def add(name: str, evidence: List[str], confidence: float = 0.9):
        found[name] = Fact(True, confidence, evidence)

    if (root / "catalog" / "controller").exists() and (root / "admin" / "controller").exists() and (root / "system").exists():
        add("opencart", ["catalog/controller", "admin/controller", "system"], 0.98)
    if (root / "classes" / "PrestaShopAutoload.php").exists() or ((root / "modules").exists() and (root / "config" / "defines.inc.php").exists()):
        add("prestashop", ["modules", "config/defines.inc.php"], 0.98)
    if (root / "artisan").exists() and (root / "bootstrap" / "app.php").exists():
        add("laravel", ["artisan", "bootstrap/app.php"], 0.98)
    if (root / "bin" / "console").exists() and (root / "config" / "bundles.php").exists():
        add("symfony", ["bin/console", "config/bundles.php"], 0.98)
    if (root / "wp-includes").exists():
        add("wordpress", ["wp-includes"], 0.98)
    if (root / "manage.py").exists() and "django" in deps:
        add("django", ["manage.py", "dependency: django"])
    for name in ["fastapi", "flask", "react", "vue", "electron"]:
        if name in deps:
            add(name, [f"dependency: {name}"])
    if any((root / n).exists() for n in ["next.config.js", "next.config.mjs", "next.config.ts"]):
        add("nextjs", ["next.config.*"], 0.98)
    return found


def detect_project_types(root: Path, files: List[Path], frameworks: Dict[str, Fact]) -> List[str]:
    types: Set[str] = set()
    names = {p.name for p in files}
    if any(k in frameworks for k in ["opencart", "prestashop", "wordpress"]):
        types.add("web-application")
        types.add("extension-platform")
    if any(k in frameworks for k in ["react", "vue", "nextjs"]):
        types.add("web-ui")
    if any(k in frameworks for k in ["fastapi", "flask", "django", "laravel", "symfony"]):
        types.add("backend")
    if {"Dockerfile", "docker-compose.yml", "compose.yml"} & names:
        types.add("containerized")
    if any(p.name in {"main.py", "cli.py", "main.go", "Program.cs"} for p in files):
        types.add("cli-or-service")
    if "electron" in frameworks:
        types.add("desktop")
    if not types:
        types.add("generic-software")
    return sorted(types)


def detect_commands(root: Path, files: List[Path]) -> Dict[str, List[str]]:
    commands: Dict[str, List[str]] = {}
    package = next(iter(find_by_name(files, "package.json")), None)
    if package:
        obj = read_json(package, {})
        for key in ["dev", "start", "test", "lint", "build", "typecheck"]:
            if key in (obj.get("scripts") or {}):
                commands.setdefault(key, []).append(f"npm run {key}")
    if find_by_name(files, "composer.json"):
        commands.setdefault("install", []).append("composer install")
    if find_by_name(files, "requirements.txt"):
        commands.setdefault("install", []).append("python -m pip install -r requirements.txt")
    if find_by_name(files, "pyproject.toml"):
        commands.setdefault("install", []).append("python -m pip install -e .")
    if (root / "tests").exists():
        commands.setdefault("test", []).append("pytest")
    if (root / "artisan").exists():
        commands.setdefault("framework", []).append("php artisan")
    if (root / "bin" / "console").exists():
        commands.setdefault("framework", []).append("php bin/console")
    if find_by_name(files, "go.mod"):
        commands.setdefault("test", []).append("go test ./...")
    if find_by_name(files, "Cargo.toml"):
        commands.setdefault("test", []).append("cargo test")
    if find_by_name(files, "pom.xml"):
        commands.setdefault("test", []).append("mvn test")
    if any(p.name == "gradlew" for p in files):
        commands.setdefault("test", []).append("./gradlew test")
    return commands


def detect_risks(root: Path, files: List[Path], frameworks: Dict[str, Fact]) -> List[dict]:
    names = {p.name for p in files}
    risks: List[dict] = []
    if any(name.startswith(".env") for name in names):
        risks.append({"level": "high", "kind": "secrets", "evidence": ".env-like file present", "rule": "Never copy secret values into generated AI files."})
    if any(k in frameworks for k in ["opencart", "prestashop", "wordpress"]):
        risks.append({"level": "high", "kind": "platform-core", "evidence": "extension platform detected", "rule": "Treat host core as protected until project-specific baseline evidence says otherwise."})
    if any("migration" in rel(root, p).lower() for p in files):
        risks.append({"level": "medium", "kind": "database-migrations", "evidence": "migration files detected", "rule": "Require forward/backward compatibility and rollback analysis."})
    if {"Dockerfile", "docker-compose.yml", "compose.yml"} & names:
        risks.append({"level": "medium", "kind": "runtime-environment", "evidence": "container config detected", "rule": "Verify commands inside the intended runtime boundary."})
    return risks


def resolve_pack_ids(languages: Dict[str, Fact], frameworks: Dict[str, Fact], types: List[str]) -> List[str]:
    packs = ["base/spec-first", "base/architecture", "base/change-lifecycle", "base/security"]
    packs += [f"languages/{x}" for x in sorted(languages)]
    packs += [f"frameworks/{x}" for x in sorted(frameworks)]
    packs += [f"project-types/{x}" for x in types]
    if "web-ui" in types or "web-application" in types:
        packs.append("verification/web")
    if "backend" in types:
        packs.append("verification/api")
    if "extension-platform" in types:
        packs.append("verification/extension")
    return sorted(dict.fromkeys(packs))


def discover(root: Path, max_files: int = 10000) -> dict:
    files = walk_files(root, max_files=max_files)
    languages = detect_languages(root, files)
    frameworks = detect_frameworks(root, files)
    versions = detect_versions(root, files)
    project_types = detect_project_types(root, files, frameworks)
    commands = detect_commands(root, files)
    risks = detect_risks(root, files, frameworks)
    entry_names = {"index.php", "main.py", "app.py", "server.js", "main.ts", "Program.cs", "main.go"}
    return {
        "root": str(root.resolve()),
        "languages": {k: asdict(v) for k, v in languages.items()},
        "frameworks": {k: asdict(v) for k, v in frameworks.items()},
        "versions": {k: asdict(v) for k, v in versions.items()},
        "project_types": project_types,
        "commands": commands,
        "entry_points": [rel(root, p) for p in files if p.name in entry_names][:40],
        "risks": risks,
        "selected_packs": resolve_pack_ids(languages, frameworks, project_types),
        "scan": {"files_scanned": len(files), "truncated": len(files) >= max_files},
    }
