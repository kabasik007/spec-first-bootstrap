from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Tuple

from .architecture import synthesize
from .baseline import compare as baseline_compare
from .baseline import inventory as baseline_inventory
from .baseline import render_baseline_md
from .dependencies import dependency_graph, render_dependency_md
from .discovery import discover
from .knowledge import load_selected
from .memory import add_manual, update_from_discovery
from .onboarding import apply_onboarding
from .packs import PackRegistry
from .policy import build_policy, check as policy_check
from .research import build_agenda
from .standards import discover as discover_standards
from .utils import read_json, write_json


VERSION = "1.2.0"


def build_context(target: Path, bootstrap_root: Path, intent: str = "") -> dict:
    facts = discover(target)
    facts["bootstrap_version"] = VERSION
    registry = PackRegistry(bootstrap_root)
    pack_context = registry.resolve(facts["selected_packs"])
    graph = dependency_graph(target)
    policy = build_policy(pack_context, facts)
    knowledge = load_selected(bootstrap_root, pack_context.get("knowledge_ids", []))
    baseline = baseline_inventory(target, pack_context.get("protected_paths", []))
    architecture = synthesize(target, facts, graph, intent)
    standards = discover_standards(target, facts)
    research = build_agenda(facts, architecture, intent)
    return {
        "facts": facts,
        "packs": pack_context,
        "dependencies": graph,
        "policy": policy,
        "knowledge": knowledge,
        "baseline": baseline,
        "architecture": architecture,
        "standards": standards,
        "research": research,
    }


def init_target(
    target: Path,
    bootstrap_root: Path,
    force: bool = False,
    intent: str = "",
    onboard: bool = True,
) -> dict:
    context = build_context(target, bootstrap_root, intent)
    ai = target / ".ai"
    ai.mkdir(parents=True, exist_ok=True)

    generated = {
        ai / "manifest.yaml": render_manifest(context),
        ai / "PROJECT.md": render_project_md(context),
        ai / "ARCHITECTURE.md": render_architecture_md(context),
        ai / "DEPENDENCIES.md": render_dependency_md(context["dependencies"]),
        ai / "COMMANDS.md": render_commands_md(context["facts"]),
        ai / "RULES.md": render_rules_md(context),
        ai / "VERIFICATION.md": render_verification_md(context),
        ai / "BASELINE.md": render_baseline_md(context["baseline"]),
    }
    for path, content in generated.items():
        if force or not path.exists():
            path.write_text(content, encoding="utf-8")

    write_json(ai / "discovery" / "project-facts.json", context["facts"])
    write_json(ai / "discovery" / "packs.json", context["packs"])
    write_json(ai / "discovery" / "dependency-graph.json", context["dependencies"])
    write_json(ai / "discovery" / "architecture.json", context["architecture"])
    write_json(ai / "discovery" / "risks.json", context["facts"]["risks"])
    write_json(ai / "standards" / "index.json", context["standards"])
    write_json(ai / "research" / "agenda.json", context["research"])
    write_json(ai / "policy.json", context["policy"])
    write_json(ai / "knowledge" / "index.json", context["knowledge"])
    write_json(ai / "baseline" / "inventory.json", context["baseline"])
    update_from_discovery(ai / "memory" / "project-memory.json", context["facts"], context["packs"])

    for folder in ["changes", "verification", "decisions", "research", "standards"]:
        (ai / folder).mkdir(exist_ok=True)

    onboarding = None
    if onboard:
        onboarding = apply_onboarding(target, bootstrap_root, context)

    return {
        "status": "ok",
        "bootstrap_version": VERSION,
        "generated": str(ai),
        "intent": intent.strip(),
        "architecture_style": context["architecture"]["style"]["name"],
        "selected_packs": context["packs"]["resolved_ids"],
        "dependencies": context["dependencies"]["summary"],
        "baseline": context["baseline"]["summary"],
        "knowledge": context["knowledge"]["selected_ids"],
        "onboarding": onboarding,
    }


def onboard_target(target: Path, bootstrap_root: Path, intent: str = "", force: bool = False) -> dict:
    return init_target(target, bootstrap_root, force=force, intent=intent, onboard=True)


def run_baseline(target: Path, bootstrap_root: Path, reference: Optional[Path] = None) -> dict:
    context = build_context(target, bootstrap_root)
    protected = context["packs"].get("protected_paths", [])
    if reference is not None:
        report = baseline_compare(target, reference, protected)
        output = target / ".ai" / "baseline" / "diff.json"
    else:
        report = baseline_inventory(target, protected)
        output = target / ".ai" / "baseline" / "inventory.json"
    write_json(output, report)
    (target / ".ai" / "BASELINE.md").write_text(render_baseline_md(report), encoding="utf-8")
    return report


def verify_target(target: Path, bootstrap_root: Path) -> Tuple[int, dict]:
    ai = target / ".ai"
    required = [
        ai / "manifest.yaml", ai / "PROJECT.md", ai / "ARCHITECTURE.md",
        ai / "DEPENDENCIES.md", ai / "RULES.md", ai / "VERIFICATION.md",
        ai / "policy.json", ai / "discovery" / "project-facts.json",
        ai / "discovery" / "packs.json", ai / "discovery" / "dependency-graph.json",
        ai / "discovery" / "architecture.json", ai / "standards" / "index.json",
        ai / "research" / "agenda.json", ai / "baseline" / "inventory.json",
        ai / "knowledge" / "index.json", ai / "memory" / "project-memory.json",
        target / "AGENTS.md", target / "docs" / "ARCHITECTURE.md",
        target / "docs" / "DEVELOPMENT.md", target / "docs" / "specs" / "README.md",
    ]
    missing = [str(p.relative_to(target)) for p in required if not p.exists()]
    invalid = []
    for path in required:
        if not path.exists() or path.suffix != ".json":
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            invalid.append({"path": str(path.relative_to(target)), "error": str(exc)})

    warnings = []
    facts = read_json(ai / "discovery" / "project-facts.json", {})
    if facts and facts.get("bootstrap_version") != VERSION:
        warnings.append("discovery was generated by bootstrap {}, current is {}".format(facts.get("bootstrap_version"), VERSION))
    packs = read_json(ai / "discovery" / "packs.json", {})
    virtual = [p["id"] for p in packs.get("loaded", []) if p.get("virtual")]
    if virtual:
        warnings.append("catalog-only packs have no detailed manifest: " + ", ".join(virtual))
    research = read_json(ai / "research" / "agenda.json", {})
    unresolved = [item["id"] for item in research.get("items", []) if item.get("status") == "unresolved"]
    if unresolved:
        warnings.append("architecture research remains unresolved: " + ", ".join(unresolved))

    result = {"ok": not missing and not invalid, "missing": missing, "invalid": invalid, "warnings": warnings}
    return (0 if result["ok"] else 1), result


def check_policy_target(target: Path, action: str, subject: str) -> dict:
    policy = read_json(target / ".ai" / "policy.json", {})
    if not policy:
        return {"decision": "deny", "reason": "policy is missing; run init first"}
    return policy_check(policy, action, subject)


def add_memory_target(target: Path, key: str, value: str, source: str, confidence: float) -> dict:
    path = target / ".ai" / "memory" / "project-memory.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return add_manual(path, key, value, source, confidence)


def render_manifest(context: dict) -> str:
    facts = context["facts"]
    value = {
        "schema_version": 3,
        "bootstrap_version": VERSION,
        "mode": context["architecture"]["mode"],
        "architecture_style": context["architecture"]["style"]["name"],
        "selected_packs": context["packs"]["resolved_ids"],
        "artifacts": {
            "facts": ".ai/discovery/project-facts.json",
            "packs": ".ai/discovery/packs.json",
            "dependencies": ".ai/discovery/dependency-graph.json",
            "architecture_model": ".ai/discovery/architecture.json",
            "standards": ".ai/standards/index.json",
            "research": ".ai/research/agenda.json",
            "baseline": ".ai/baseline/inventory.json",
            "policy": ".ai/policy.json",
            "knowledge": ".ai/knowledge/index.json",
            "memory": ".ai/memory/project-memory.json",
            "architecture": ".ai/ARCHITECTURE.md",
            "commands": ".ai/COMMANDS.md",
            "rules": ".ai/RULES.md",
            "verification": ".ai/VERIFICATION.md",
            "human_architecture": "docs/ARCHITECTURE.md",
            "human_development": "docs/DEVELOPMENT.md",
            "agent_instructions": "AGENTS.md",
        },
    }
    return json.dumps(value, indent=2) + "\n"


def render_project_md(context: dict) -> str:
    facts = context["facts"]
    architecture = context["architecture"]
    langs = ", ".join(facts["languages"].keys()) or "unknown"
    frameworks = ", ".join(facts["frameworks"].keys()) or "none detected"
    versions = "\n".join(
        "- {}: `{}` ({:.0%} confidence)".format(name, fact.get("value"), fact.get("confidence", 0))
        for name, fact in facts["versions"].items()
    ) or "- No explicit runtime constraints detected."
    intent = architecture.get("intent") or "not supplied"
    return """# Project Facts

Generated by Universal AI Development Bootstrap {version}.

## Intent

- {intent}

## Detected stack

- Languages: {langs}
- Frameworks/platforms: {frameworks}
- Project types: {types}
- Architecture style: {style}

## Runtime/version evidence

{versions}

## Context artifacts

- Read `ARCHITECTURE.md`, `DEPENDENCIES.md`, `RULES.md`, `VERIFICATION.md`.
- Read `.ai/discovery/architecture.json` for machine-readable component boundaries.
- Read `.ai/research/agenda.json` before relying on uncertain framework/version assumptions.
- Read `.ai/policy.json` and project memory before non-trivial work.

## Evidence rule

- Project-specific verified facts override generic bootstrap guidance.
- Repository evidence overrides generic architecture examples.
- Unresolved version-specific behavior must be researched or left unresolved, not guessed.
""".format(
        version=VERSION,
        intent=intent,
        langs=langs,
        frameworks=frameworks,
        types=", ".join(facts["project_types"]),
        style=architecture["style"]["name"],
        versions=versions,
    )


def render_architecture_md(context: dict) -> str:
    architecture = context["architecture"]
    graph = context["dependencies"]["summary"]
    component_lines = []
    for item in architecture.get("components", []):
        component_lines.append("- `{}` — {}; deployment: {}.".format(item.get("path"), item.get("role"), item.get("deployment")))
    if not component_lines:
        component_lines.append("- No stable component boundary detected yet.")
    principles = ["- " + item for item in architecture.get("principles", [])]
    return """# Architecture Context

## Decision

- Style: `{style}`.
- Mode: `{mode}`.
- Reason: {reason}

## Components

{components}

## Dependency boundary

- Dependency manifests: {manifest_count}.
- Direct dependencies: {dependency_count}.
- Ecosystems: {ecosystems}.

## Architecture policy

{principles}

## Human documentation

- Current human-facing architecture: `docs/ARCHITECTURE.md`.
- Development conventions: `docs/DEVELOPMENT.md`.
- Product behavior: `docs/specs/`.
- Change design: `.ai/changes/<change-id>/design.md`.
""".format(
        style=architecture["style"]["name"],
        mode=architecture["mode"],
        reason=architecture["style"]["reason"],
        components="\n".join(component_lines),
        manifest_count=graph["manifest_count"],
        dependency_count=graph["dependency_count"],
        ecosystems=", ".join(graph["ecosystems"]) or "none detected",
        principles="\n".join(principles),
    )


def render_commands_md(facts: dict) -> str:
    lines = ["# Commands", "", "Detected commands are candidates. Verify environment and policy before production or destructive use.", ""]
    for kind, commands in facts["commands"].items():
        lines += ["## {}".format(kind), ""] + ["- `{}`".format(command) for command in commands] + [""]
    if not facts["commands"]:
        lines.append("No standard commands detected.")
    return "\n".join(lines) + "\n"


def render_rules_md(context: dict) -> str:
    facts = context["facts"]
    packs = context["packs"]
    lines = [
        "# Project Rules", "",
        "## Universal rules", "",
        "- Preserve existing behavior unless the active change explicitly alters it.",
        "- Match detected target runtime compatibility; do not silently introduce newer syntax or APIs.",
        "- Never copy secrets into specs, prompts, logs, memory, baseline output, or generated AI context.",
        "- Product specs describe WHAT; architecture/change design describes HOW.",
        "- Keep core small; keep feature logic in explicit modules with narrow contracts.",
        "- Do not introduce microservices without a real operational/service boundary.",
        "- Use `.ai/policy.json` and `policy-check` before protected/destructive actions.",
        "", "## Capability-pack rules", "",
    ]
    for rule in packs.get("rules", []):
        lines.append("- " + rule)
    if not packs.get("rules"):
        lines.append("- No detailed pack-specific rules loaded.")
    lines += ["", "## Compatibility", ""]
    lines += ["- " + item for item in packs.get("compatibility", [])] or ["- No additional compatibility rule loaded."]
    lines += ["", "## Detected risks", ""]
    lines += ["- **{} / {}**: {}".format(r["level"], r["kind"], r["rule"]) for r in facts["risks"]] or ["- No special risk detected."]
    return "\n".join(lines) + "\n"


def render_verification_md(context: dict) -> str:
    checks = context["packs"].get("verification", [])
    lines = [
        "# Verification Contract", "",
        "Verification is selected by capabilities, not by a hard-coded web-only workflow.", "",
    ]
    lines += ["- " + item for item in checks] or ["- Use project-appropriate focused verification."]
    lines += ["", "For high-risk changes also verify rollback/migration behavior, compatibility boundaries, permissions, and packaging/deployment where applicable."]
    return "\n".join(lines) + "\n"
