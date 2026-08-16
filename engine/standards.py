from __future__ import annotations

from pathlib import Path
from typing import List


STANDARD_MARKERS = {
    ".editorconfig": "EditorConfig formatting rules",
    "phpcs.xml": "PHP_CodeSniffer rules",
    "phpcs.xml.dist": "PHP_CodeSniffer rules",
    "phpstan.neon": "PHPStan static-analysis rules",
    "phpstan.neon.dist": "PHPStan static-analysis rules",
    "eslint.config.js": "ESLint rules",
    "eslint.config.mjs": "ESLint rules",
    "eslint.config.cjs": "ESLint rules",
    ".eslintrc": "ESLint rules",
    ".eslintrc.json": "ESLint rules",
    ".prettierrc": "Prettier formatting rules",
    ".prettierrc.json": "Prettier formatting rules",
    "prettier.config.js": "Prettier formatting rules",
    "ruff.toml": "Ruff lint/format rules",
    ".ruff.toml": "Ruff lint/format rules",
    "mypy.ini": "mypy type-checking rules",
    "pytest.ini": "pytest configuration",
    "tsconfig.json": "TypeScript compiler constraints",
    "Cargo.toml": "Cargo workspace/package conventions",
    "go.mod": "Go module boundary",
    "pom.xml": "Maven build conventions",
    "build.gradle": "Gradle build conventions",
    "build.gradle.kts": "Gradle build conventions",
    "Directory.Build.props": ".NET shared build conventions",
}


def discover(target: Path, facts: dict) -> dict:
    markers = []
    for name, meaning in STANDARD_MARKERS.items():
        matches = list(target.rglob(name))
        for path in matches[:5]:
            try:
                relative = path.relative_to(target).as_posix()
            except ValueError:
                relative = str(path)
            if any(part in {".git", ".ai", "node_modules", "vendor", ".venv", "venv"} for part in path.parts):
                continue
            markers.append({"path": relative, "meaning": meaning})

    commands = []
    for kind, values in facts.get("commands", {}).items():
        for command in values:
            commands.append({"kind": kind, "command": command})

    return {
        "schema_version": 1,
        "markers": markers,
        "commands": commands,
        "retrieval_format": [
            "Write one rule or fact per bullet/line.",
            "Include exact file paths when a rule is path-specific.",
            "Use stable keywords in headings and bullets so text search can retrieve the rule.",
            "Keep root agent instructions short; put detailed guidance in linked/scoped documents.",
            "Do not bury compatibility constraints inside long narrative paragraphs.",
        ],
        "change_rules": [
            "Inspect nearby code before introducing a new pattern.",
            "Prefer existing repository conventions over generic framework advice.",
            "Do not reformat or modernize unrelated code during a focused change.",
            "Add dependencies only when the repository does not already provide the needed capability.",
            "Keep public contracts narrow and document intentional breaking changes.",
        ],
    }


def render_development(standards: dict, facts: dict, architecture: dict) -> str:
    markers = ["- `{}` — {}.".format(item["path"], item["meaning"]) for item in standards.get("markers", [])]
    if not markers:
        markers = ["- No explicit lint/format/type-check configuration detected; mirror nearby code and keep changes minimal."]

    commands = ["- **{}**: `{}`".format(item["kind"], item["command"]) for item in standards.get("commands", [])]
    if not commands:
        commands = ["- No standard command detected; inspect project-native scripts before inventing one."]

    retrieval = ["- " + item for item in standards.get("retrieval_format", [])]
    change_rules = ["- " + item for item in standards.get("change_rules", [])]
    components = ["- `{}` — {}.".format(item.get("path"), item.get("role")) for item in architecture.get("components", [])]
    if not components:
        components = ["- No stable component map exists yet."]

    return """# Development Guide

<!-- universal-bootstrap:start -->
## Start here

- Read `AGENTS.md`.
- Read `docs/ARCHITECTURE.md`.
- Read the relevant `docs/specs/` contract before changing observable behavior.
- Read `.ai/RULES.md` and `.ai/policy.json` before protected or destructive work.
- Prefer repository evidence over generic framework habits.

## Project components

{components}

## Detected development standards

{markers}

## Project-native commands

{commands}

## Code-change rules

{change_rules}

## Retrieval-friendly documentation rules

{retrieval}

## Adding a new module/block/service

- Start as an internal module unless an independent deployment boundary is already justified.
- Give the module one clear responsibility and a narrow public contract.
- Keep host/UI/API adapters outside core business logic.
- Put external IO behind adapters.
- Define data ownership before sharing tables/state across modules.
- Add verification at the boundary that users or other components observe.
- Split into a separate service only for a real deployment/scale/fault/data/team boundary.

## Compatibility

- Languages: {languages}.
- Frameworks/platforms: {frameworks}.
- Exact runtime constraints live in `.ai/PROJECT.md` and `.ai/discovery/project-facts.json`.
<!-- universal-bootstrap:end -->
""".format(
        components="\n".join(components),
        markers="\n".join(markers),
        commands="\n".join(commands),
        change_rules="\n".join(change_rules),
        retrieval="\n".join(retrieval),
        languages=", ".join(facts.get("languages", {}).keys()) or "unknown",
        frameworks=", ".join(facts.get("frameworks", {}).keys()) or "none detected",
    )
