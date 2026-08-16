from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Set


IGNORED_TOP_LEVEL = {
    ".ai", ".git", ".github", ".idea", ".vscode", "node_modules", "vendor",
    ".venv", "venv", "dist", "build", "coverage", "__pycache__",
}

ROLE_BY_NAME = {
    "src": "application source",
    "app": "application source",
    "core": "shared core/domain contracts",
    "domain": "domain model and business rules",
    "modules": "feature modules/extensions",
    "module": "feature module/extension",
    "plugins": "plugins/extensions",
    "extensions": "extensions",
    "packages": "workspace packages",
    "services": "deployable or logical services",
    "service": "service layer",
    "api": "API/interface layer",
    "backend": "backend application",
    "frontend": "frontend application",
    "web": "web interface",
    "ui": "user interface",
    "admin": "administration surface",
    "catalog": "catalog/public surface",
    "system": "platform/system layer",
    "infrastructure": "infrastructure adapters",
    "infra": "infrastructure adapters",
    "adapters": "external-system adapters",
    "integrations": "external integrations",
    "workers": "background workers",
    "worker": "background worker",
    "jobs": "background jobs",
    "cmd": "CLI/process entry points",
    "cli": "CLI interface",
    "tests": "verification",
    "test": "verification",
}

DEPLOYABLE_NAMES = {"services", "backend", "frontend", "api", "workers", "worker", "web"}


def _top_level_dirs(target: Path) -> List[Path]:
    result = []
    try:
        children = sorted(target.iterdir(), key=lambda item: item.name.lower())
    except OSError:
        return result
    for child in children:
        if child.is_dir() and child.name not in IGNORED_TOP_LEVEL and not child.name.startswith("."):
            result.append(child)
    return result


def _manifest_roots(dependencies: dict) -> Set[str]:
    roots: Set[str] = set()
    for manifest in dependencies.get("manifests", []):
        path = manifest.get("path", "")
        if not path:
            continue
        parts = Path(path).parts
        if len(parts) > 1:
            roots.add(parts[0])
    return roots


def _existing_components(target: Path, dependencies: dict) -> List[dict]:
    manifest_roots = _manifest_roots(dependencies)
    components = []
    for directory in _top_level_dirs(target):
        name = directory.name
        role = ROLE_BY_NAME.get(name.lower())
        if not role and name not in manifest_roots:
            continue
        deployment = "candidate" if name.lower() in DEPLOYABLE_NAMES or name in manifest_roots else "shared"
        components.append({
            "name": name,
            "path": name + "/",
            "role": role or "workspace component",
            "deployment": deployment,
            "source": "repository-evidence",
        })
    return components


def _greenfield_blueprint(project_types: List[str]) -> List[dict]:
    types = set(project_types)
    if "extension-platform" in types:
        names = [
            ("domain", "business rules independent from the host platform"),
            ("application", "use cases and orchestration"),
            ("host-adapter", "host-platform controllers/hooks/events/entry points"),
            ("infrastructure", "database/external-service adapters"),
            ("tests", "unit/integration/host compatibility verification"),
        ]
    elif "desktop" in types:
        names = [
            ("core", "domain/application contracts"),
            ("modules", "feature modules"),
            ("ui", "desktop presentation layer"),
            ("infrastructure", "filesystem/network/platform adapters"),
            ("tests", "verification"),
        ]
    elif "cli-or-service" in types and "web-ui" not in types:
        names = [
            ("core", "domain/application contracts"),
            ("modules", "feature modules"),
            ("interfaces", "CLI/process entry points"),
            ("infrastructure", "external adapters"),
            ("tests", "verification"),
        ]
    else:
        names = [
            ("core", "small stable domain/application contracts"),
            ("modules", "business/feature modules"),
            ("interfaces", "web/API/CLI/UI entry points"),
            ("infrastructure", "database, queues and external adapters"),
            ("tests", "verification"),
        ]
    return [
        {
            "name": name,
            "path": name + "/",
            "role": role,
            "deployment": "shared",
            "source": "recommended-blueprint",
        }
        for name, role in names
    ]


def _architecture_style(facts: dict, components: List[dict]) -> dict:
    types = set(facts.get("project_types", []))
    deployable = [item for item in components if item.get("deployment") == "candidate"]

    if "extension-platform" in types:
        return {
            "name": "host-extension",
            "reason": "A host extension/platform boundary was detected; preserve host lifecycle and keep custom logic isolated from platform core.",
        }
    if len(deployable) >= 2:
        return {
            "name": "multi-component",
            "reason": "Multiple independently shaped top-level components/manifests were detected; preserve those boundaries before considering consolidation or further splitting.",
        }
    if "desktop" in types:
        return {"name": "modular-desktop", "reason": "Desktop lifecycle detected; use feature modules behind a small application core."}
    if "web-ui" in types and "backend" in types:
        return {"name": "modular-web-application", "reason": "Frontend and backend capabilities coexist; keep interface and application/domain boundaries explicit."}
    if "backend" in types:
        return {"name": "modular-backend", "reason": "Backend/service application detected; organize around domain/application modules and adapters."}
    if "cli-or-service" in types:
        return {"name": "modular-service", "reason": "CLI/service entry points detected; keep process interfaces outside reusable application logic."}
    return {
        "name": "modular-monolith",
        "reason": "No evidence requires independently deployed services; start with the simplest architecture that preserves strong module boundaries.",
    }


def synthesize(target: Path, facts: dict, dependencies: dict, intent: str = "") -> dict:
    existing = _existing_components(target, dependencies)
    greenfield = facts.get("scan", {}).get("files_scanned", 0) <= 10
    components = existing if existing else _greenfield_blueprint(facts.get("project_types", []))
    style = _architecture_style(facts, components)

    microservice_evidence = []
    for component in components:
        if component.get("deployment") == "candidate":
            microservice_evidence.append(component.get("path", component.get("name", "")))

    return {
        "schema_version": 1,
        "intent": intent.strip(),
        "mode": "greenfield" if greenfield else "brownfield",
        "style": style,
        "components": components,
        "principles": [
            "Keep core small and stable; do not turn core into a catch-all for feature logic.",
            "Put business capabilities in explicit modules with narrow public contracts.",
            "Keep UI/API/CLI/host entry points at the edge; they call application/module contracts.",
            "Keep database, filesystem, queues and external APIs behind infrastructure adapters.",
            "A module owns its behavior and data rules; cross-module access goes through explicit contracts.",
            "Shared code must be genuinely cross-cutting; avoid generic utils dumping grounds.",
            "Preserve existing boundaries in brownfield projects unless a change explicitly justifies migration.",
            "Prefer a modular monolith over microservices until independent deployment, scaling, fault isolation, data ownership or team ownership requires a service boundary.",
        ],
        "microservices": {
            "default": False,
            "decision": "preserve-existing" if len(microservice_evidence) >= 2 else "not-recommended-by-default",
            "evidence": microservice_evidence,
            "split_only_when": [
                "independent deployment lifecycle is required",
                "independent scaling profile is required",
                "fault isolation is materially valuable",
                "data ownership can be made explicit",
                "team/operational ownership is independent",
            ],
        },
        "unknowns": [
            "Confirm persistence/data ownership before introducing cross-module database access.",
            "Confirm deployment units before introducing network boundaries between modules.",
            "Confirm public/stable contracts before exposing a module to external consumers.",
        ],
        "source": "repository evidence plus universal architecture policy",
    }


def render_human_architecture(model: dict, facts: dict) -> str:
    style = model["style"]
    intent = model.get("intent") or "No explicit product intent was supplied during bootstrap."
    component_lines = []
    for component in model.get("components", []):
        component_lines.append(
            "- `{path}` — {role}; deployment: {deployment}; source: {source}.".format(**component)
        )
    if not component_lines:
        component_lines.append("- No component boundary detected yet.")

    principle_lines = ["- " + item for item in model.get("principles", [])]
    split_lines = ["- " + item for item in model.get("microservices", {}).get("split_only_when", [])]
    unknown_lines = ["- " + item for item in model.get("unknowns", [])]

    return """# Architecture

<!-- universal-bootstrap:start -->
## Bootstrap intent

{intent}

## Current architecture decision

- Style: `{style}`.
- Reason: {reason}
- Mode: `{mode}`.

## Components and boundaries

{components}

## Architecture rules

{principles}

## Microservice rule

- Microservices are not a default architecture.
- Current decision: `{micro_decision}`.
- Split a module into a service only when at least one strong boundary exists and operational cost is justified.
{split_rules}

## Open architecture questions

{unknowns}

## Source of truth

- Product behavior: `docs/specs/`.
- Human architecture: this file.
- Machine-readable architecture: `.ai/discovery/architecture.json`.
- Change-specific technical design: `.ai/changes/<change-id>/design.md`.
<!-- universal-bootstrap:end -->
""".format(
        intent=intent,
        style=style.get("name"),
        reason=style.get("reason"),
        mode=model.get("mode"),
        components="\n".join(component_lines),
        principles="\n".join(principle_lines),
        micro_decision=model.get("microservices", {}).get("decision"),
        split_rules="\n".join(split_lines),
        unknowns="\n".join(unknown_lines),
    )
