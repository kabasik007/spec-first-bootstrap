#!/usr/bin/env python3
"""Universal AI Development Bootstrap.

Scans a target repository, detects stack/project facts, resolves capability packs,
and generates a project-specific .ai harness without requiring third-party Python packages.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Set

VERSION = "1.0.0"
IGNORE_DIRS = {".git", ".ai", "node_modules", "vendor", ".venv", "venv", "dist", "build", "__pycache__", ".idea", ".vscode"}

LANG_MARKERS = {
    "php": ["composer.json", "*.php"],
    "python": ["pyproject.toml", "requirements.txt", "setup.py", "*.py"],
    "node": ["package.json", "*.js", "*.ts", "*.tsx", "*.jsx"],
    "go": ["go.mod", "*.go"],
    "rust": ["Cargo.toml", "*.rs"],
    "java": ["pom.xml", "build.gradle", "build.gradle.kts", "*.java"],
    "dotnet": ["*.csproj", "*.sln", "*.fsproj"],
}

FRAMEWORK_MARKERS = {
    "opencart": ["system/library/cart.php", "catalog/controller", "admin/controller"],
    "prestashop": ["config/defines.inc.php", "classes/PrestaShopAutoload.php", "modules"],
    "laravel": ["artisan", "bootstrap/app.php"],
    "symfony": ["bin/console", "config/bundles.php"],
    "wordpress": ["wp-config.php", "wp-includes"],
    "django": ["manage.py"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "nextjs": ["next.config.js", "next.config.mjs", "next.config.ts"],
    "react": ["react"],
    "vue": ["vue"],
    "electron": ["electron"],
}

@dataclass
class Fact:
    value: object
    confidence: float
    evidence: List[str]


def walk_files(root: Path, max_files: int = 5000) -> List[Path]:
    out: List[Path] = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
        for name in files:
            out.append(Path(base) / name)
            if len(out) >= max_files:
                return out
    return out


def rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


def text(path: Path, limit: int = 250_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:limit]
    except Exception:
        return ""


def find_by_name(files: Iterable[Path], name: str) -> List[Path]:
    return [p for p in files if p.name == name]


def detect_languages(root: Path, files: List[Path]) -> Dict[str, Fact]:
    names = {p.name for p in files}
    suffixes: Dict[str, int] = {}
    for p in files:
        suffixes[p.suffix.lower()] = suffixes.get(p.suffix.lower(), 0) + 1
    found: Dict[str, Fact] = {}
    checks = {
        "php": ("composer.json" in names or suffixes.get(".php", 0) > 2, ["composer.json", f"php_files={suffixes.get('.php',0)}"]),
        "python": (bool({"pyproject.toml", "requirements.txt", "setup.py"} & names) or suffixes.get(".py", 0) > 2, [f"python_files={suffixes.get('.py',0)}"]),
        "node": ("package.json" in names or sum(suffixes.get(x, 0) for x in [".js", ".ts", ".tsx", ".jsx"]) > 3, ["package.json" if "package.json" in names else "js/ts sources"]),
        "go": ("go.mod" in names or suffixes.get(".go", 0) > 2, ["go.mod" if "go.mod" in names else "go sources"]),
        "rust": ("Cargo.toml" in names or suffixes.get(".rs", 0) > 2, ["Cargo.toml" if "Cargo.toml" in names else "rust sources"]),
        "java": (bool({"pom.xml", "build.gradle", "build.gradle.kts"} & names) or suffixes.get(".java", 0) > 2, ["java build/source markers"]),
        "dotnet": (any(p.suffix in {".csproj", ".fsproj", ".sln"} for p in files), [".NET project files"]),
    }
    for k, (ok, evidence) in checks.items():
        if ok:
            found[k] = Fact(True, 0.95, evidence)
    return found


def detect_versions(root: Path, files: List[Path], languages: Dict[str, Fact]) -> Dict[str, Fact]:
    versions: Dict[str, Fact] = {}
    composer = next(iter(find_by_name(files, "composer.json")), None)
    if composer:
        data = text(composer)
        m = re.search(r'"php"\s*:\s*"([^"]+)"', data)
        if m:
            versions["php_constraint"] = Fact(m.group(1), 0.95, [rel(root, composer)])
    pyproject = next(iter(find_by_name(files, "pyproject.toml")), None)
    if pyproject:
        m = re.search(r'requires-python\s*=\s*["\']([^"\']+)', text(pyproject))
        if m:
            versions["python_constraint"] = Fact(m.group(1), 0.9, [rel(root, pyproject)])
    package = next(iter(find_by_name(files, "package.json")), None)
    if package:
        try:
            obj = json.loads(text(package))
            eng = obj.get("engines", {})
            if eng.get("node"):
                versions["node_constraint"] = Fact(eng["node"], 0.9, [rel(root, package)])
        except Exception:
            pass
    for p in files:
        r = rel(root, p)
        if r.endswith("system/library/cart/user.php") or r.endswith("system/startup.php"):
            data = text(p)
            m = re.search(r"VERSION\s*['\"]?\s*,?\s*['\"]([0-9.]+)", data)
            if m:
                versions["opencart"] = Fact(m.group(1), 0.7, [r])
    return versions


def deps_text(files: List[Path]) -> str:
    chunks = []
    for name in ["composer.json", "package.json", "pyproject.toml", "requirements.txt", "Cargo.toml", "go.mod", "pom.xml"]:
        for p in find_by_name(files, name)[:2]:
            chunks.append(text(p, 80_000).lower())
    return "\n".join(chunks)


def detect_frameworks(root: Path, files: List[Path]) -> Dict[str, Fact]:
    rels = {rel(root, p) for p in files}
    deps = deps_text(files)
    found: Dict[str, Fact] = {}
    def add(name: str, evidence: List[str], conf: float = 0.9):
        found[name] = Fact(True, conf, evidence)
    if {"system/library/cart.php", "catalog/controller", "admin/controller"} & rels or (root / "catalog" / "controller").exists() and (root / "admin" / "controller").exists() and (root / "system").exists(): add("opencart", ["catalog/controller", "admin/controller", "system"], 0.98)
    if (root / "classes" / "PrestaShopAutoload.php").exists() or ((root / "modules").exists() and (root / "config" / "defines.inc.php").exists()): add("prestashop", ["classes/PrestaShopAutoload.php", "modules"], 0.98)
    if (root / "artisan").exists() and (root / "bootstrap" / "app.php").exists(): add("laravel", ["artisan", "bootstrap/app.php"], 0.98)
    if (root / "bin" / "console").exists() and (root / "config" / "bundles.php").exists(): add("symfony", ["bin/console", "config/bundles.php"], 0.98)
    if (root / "wp-includes").exists(): add("wordpress", ["wp-includes"], 0.98)
    if (root / "manage.py").exists() and "django" in deps: add("django", ["manage.py", "dependency: django"])
    for name in ["fastapi", "flask", "react", "vue", "electron"]:
        if name in deps: add(name, [f"dependency: {name}"])
    if any((root / n).exists() for n in ["next.config.js", "next.config.mjs", "next.config.ts"]): add("nextjs", ["next.config.*"], 0.98)
    return found


def detect_project_types(root: Path, files: List[Path], frameworks: Dict[str, Fact]) -> List[str]:
    types: Set[str] = set()
    names = {p.name for p in files}
    if any(k in frameworks for k in ["opencart", "prestashop", "wordpress"]):
        types.add("web-application")
        if (root / "modules").exists() or "opencart" in frameworks:
            types.add("extension-platform")
    if any(k in frameworks for k in ["react", "vue", "nextjs"]): types.add("web-ui")
    if any(k in frameworks for k in ["fastapi", "flask", "django", "laravel", "symfony"]): types.add("backend")
    if "Dockerfile" in names or "docker-compose.yml" in names or "compose.yml" in names: types.add("containerized")
    if any(p.name in {"main.py", "cli.py"} for p in files) or "bin" in {p.parent.name for p in files}: types.add("cli-or-service")
    if "electron" in frameworks: types.add("desktop")
    if not types: types.add("generic-software")
    return sorted(types)


def detect_commands(root: Path, files: List[Path]) -> Dict[str, List[str]]:
    commands: Dict[str, List[str]] = {}
    pkg = next(iter(find_by_name(files, "package.json")), None)
    if pkg:
        try:
            scripts = json.loads(text(pkg)).get("scripts", {})
            for key in ["dev", "start", "test", "lint", "build", "typecheck"]:
                if key in scripts: commands.setdefault(key, []).append(f"npm run {key}")
        except Exception: pass
    if find_by_name(files, "composer.json"): commands.setdefault("install", []).append("composer install")
    if find_by_name(files, "requirements.txt"): commands.setdefault("install", []).append("python -m pip install -r requirements.txt")
    if find_by_name(files, "pyproject.toml"): commands.setdefault("install", []).append("python -m pip install -e .")
    if any(p.name.startswith("pytest") for p in files) or (root / "tests").exists(): commands.setdefault("test", []).append("pytest")
    if (root / "artisan").exists(): commands.setdefault("framework", []).append("php artisan")
    if (root / "bin" / "console").exists(): commands.setdefault("framework", []).append("php bin/console")
    if find_by_name(files, "go.mod"): commands.setdefault("test", []).append("go test ./...")
    if find_by_name(files, "Cargo.toml"): commands.setdefault("test", []).append("cargo test")
    return commands


def detect_risks(root: Path, files: List[Path], frameworks: Dict[str, Fact]) -> List[dict]:
    risks = []
    names = {p.name for p in files}
    if ".env" in names: risks.append({"level":"high","kind":"secrets","evidence":".env present","rule":"Never copy secret values into generated AI files."})
    if "opencart" in frameworks: risks.append({"level":"high","kind":"platform-core","evidence":"OpenCart detected","rule":"Treat core files as protected unless the project explicitly documents core modifications."})
    if "prestashop" in frameworks: risks.append({"level":"high","kind":"platform-core","evidence":"PrestaShop detected","rule":"Prefer modules/overrides/hooks over core edits."})
    if any("migration" in rel(root,p).lower() for p in files): risks.append({"level":"medium","kind":"database-migrations","evidence":"migration files detected","rule":"Require rollback/forward compatibility analysis for schema changes."})
    if any(p.name in {"Dockerfile", "docker-compose.yml", "compose.yml"} for p in files): risks.append({"level":"medium","kind":"runtime-environment","evidence":"container config detected","rule":"Verify runtime commands inside the intended container environment."})
    return risks


def resolve_packs(languages: Dict[str, Fact], frameworks: Dict[str, Fact], types: List[str]) -> List[str]:
    packs = ["base/spec-first", "base/architecture", "base/change-lifecycle"]
    packs += [f"languages/{x}" for x in sorted(languages)]
    packs += [f"frameworks/{x}" for x in sorted(frameworks)]
    packs += [f"project-types/{x}" for x in types]
    if "web-ui" in types or "web-application" in types: packs.append("verification/web")
    if "backend" in types: packs.append("verification/api")
    if "extension-platform" in types: packs.append("verification/extension")
    return sorted(dict.fromkeys(packs))


def discover(root: Path) -> dict:
    files = walk_files(root)
    languages = detect_languages(root, files)
    frameworks = detect_frameworks(root, files)
    versions = detect_versions(root, files, languages)
    types = detect_project_types(root, files, frameworks)
    commands = detect_commands(root, files)
    risks = detect_risks(root, files, frameworks)
    packs = resolve_packs(languages, frameworks, types)
    entry_points = [rel(root,p) for p in files if p.name in {"index.php","main.py","app.py","server.js","main.ts","Program.cs","main.go"}][:30]
    return {
        "bootstrap_version": VERSION,
        "root": str(root.resolve()),
        "languages": {k: asdict(v) for k,v in languages.items()},
        "frameworks": {k: asdict(v) for k,v in frameworks.items()},
        "versions": {k: asdict(v) for k,v in versions.items()},
        "project_types": types,
        "commands": commands,
        "entry_points": entry_points,
        "risks": risks,
        "selected_packs": packs,
        "scan": {"files_scanned": len(files), "truncated": len(files) >= 5000},
    }


def write_json(path: Path, obj: object):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_project_md(facts: dict) -> str:
    langs = ", ".join(facts["languages"].keys()) or "unknown"
    frameworks = ", ".join(facts["frameworks"].keys()) or "none detected"
    types = ", ".join(facts["project_types"])
    return f"""# Project Facts\n\nGenerated by Universal AI Development Bootstrap {VERSION}.\n\n## Detected stack\n\n- Languages: {langs}\n- Frameworks/platforms: {frameworks}\n- Project types: {types}\n\n## Rule\n\nTreat discovery output as evidence, not absolute truth. Preserve confidence and verify low-confidence facts before risky changes.\n"""


def render_architecture_md(facts: dict) -> str:
    eps = "\n".join(f"- `{x}`" for x in facts["entry_points"]) or "- No canonical entry point detected."
    return f"""# Architecture\n\n## System shape\n\nDetected project types: {', '.join(facts['project_types'])}.\n\n## Entry points\n\n{eps}\n\n## Boundaries to discover before architectural changes\n\n- data ownership and persistence\n- public versus internal APIs\n- module/plugin boundaries\n- generated/vendor/core code\n- background jobs and integrations\n- deployment/runtime boundaries\n\n## Architecture rule\n\nDo not put technical architecture inside product feature specs. Keep product contract in `docs/specs/` and technical design here or in `.ai/changes/<id>/design.md`.\n"""


def render_commands_md(facts: dict) -> str:
    lines = ["# Commands", "", "Detected commands are candidates. Verify them before destructive or production use.", ""]
    for kind, cmds in facts["commands"].items():
        lines += [f"## {kind}"] + [f"- `{c}`" for c in cmds] + [""]
    if not facts["commands"]: lines.append("No standard commands detected.")
    return "\n".join(lines) + "\n"


def render_rules_md(facts: dict) -> str:
    risk_lines = "\n".join(f"- **{r['level']} / {r['kind']}**: {r['rule']}" for r in facts["risks"]) or "- No special risk rule detected; normal safe-change rules still apply."
    return f"""# Project Rules\n\n## Universal rules\n\n- Preserve existing behavior unless the active change explicitly alters it.\n- Prefer extension points over invasive core/platform edits.\n- Never copy secrets into specs, prompts, logs, or generated AI context.\n- Match the project's detected runtime compatibility; do not silently introduce newer language syntax.\n- For non-trivial behavior changes, update product specs and verification together.\n- For architectural changes, record design and rollback/migration considerations separately from product specs.\n\n## Detected risk rules\n\n{risk_lines}\n"""


def render_manifest(facts: dict) -> str:
    # JSON is valid YAML 1.2 and avoids an external YAML dependency.
    return json.dumps({
        "schema_version": 1,
        "bootstrap_version": VERSION,
        "mode": "brownfield" if facts["scan"]["files_scanned"] > 10 else "greenfield",
        "selected_packs": facts["selected_packs"],
        "discovery": ".ai/discovery/project-facts.json",
        "architecture": ".ai/ARCHITECTURE.md",
        "commands": ".ai/COMMANDS.md",
        "rules": ".ai/RULES.md"
    }, indent=2) + "\n"


def init(root: Path, force: bool = False):
    facts = discover(root)
    ai = root / ".ai"
    ai.mkdir(parents=True, exist_ok=True)
    outputs = {
        ai / "manifest.yaml": render_manifest(facts),
        ai / "PROJECT.md": render_project_md(facts),
        ai / "ARCHITECTURE.md": render_architecture_md(facts),
        ai / "COMMANDS.md": render_commands_md(facts),
        ai / "RULES.md": render_rules_md(facts),
    }
    for path, content in outputs.items():
        if path.exists() and not force:
            continue
        path.write_text(content, encoding="utf-8")
    write_json(ai / "discovery" / "project-facts.json", facts)
    write_json(ai / "discovery" / "risks.json", facts["risks"])
    (ai / "changes").mkdir(exist_ok=True)
    (ai / "verification").mkdir(exist_ok=True)
    (ai / "memory").mkdir(exist_ok=True)
    print(json.dumps({"status":"ok","generated":str(ai),"selected_packs":facts["selected_packs"]}, indent=2))


def verify(root: Path) -> int:
    required = [root/".ai"/"manifest.yaml", root/".ai"/"PROJECT.md", root/".ai"/"ARCHITECTURE.md", root/".ai"/"RULES.md", root/".ai"/"discovery"/"project-facts.json"]
    missing = [str(p) for p in required if not p.exists()]
    print(json.dumps({"ok": not missing, "missing": missing}, indent=2))
    return 1 if missing else 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="bootstrap", description="Universal AI Development Bootstrap")
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ["detect", "init", "verify"]:
        p = sub.add_parser(name)
        p.add_argument("target", nargs="?", default=".")
        if name == "init": p.add_argument("--force", action="store_true")
    args = parser.parse_args()
    root = Path(args.target).resolve()
    if not root.exists():
        parser.error(f"target does not exist: {root}")
    if args.cmd == "detect":
        print(json.dumps(discover(root), indent=2, ensure_ascii=False)); return 0
    if args.cmd == "init":
        init(root, args.force); return 0
    return verify(root)

if __name__ == "__main__":
    raise SystemExit(main())
