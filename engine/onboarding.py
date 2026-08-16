from __future__ import annotations

import json
import shutil
from pathlib import Path

from .architecture import render_human_architecture
from .research import render_research_summary
from .standards import render_development
from .utils import write_json


START = "<!-- universal-bootstrap:start -->"
END = "<!-- universal-bootstrap:end -->"


def _managed_update(path: Path, generated: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    generated = generated.strip() + "\n"
    if not path.exists():
        path.write_text(generated, encoding="utf-8")
        return

    existing = path.read_text(encoding="utf-8", errors="ignore")
    if START in existing and END in existing:
        before, rest = existing.split(START, 1)
        _, after = rest.split(END, 1)
        managed = generated
        if START not in managed or END not in managed:
            managed = START + "\n" + managed + END + "\n"
        path.write_text(before.rstrip() + "\n\n" + managed + after.lstrip(), encoding="utf-8")
        return

    path.write_text(existing.rstrip() + "\n\n" + generated, encoding="utf-8")


def _agent_block(context: dict) -> str:
    architecture = context["architecture"]
    facts = context["facts"]
    components = []
    for item in architecture.get("components", []):
        components.append("- `{}`: {}.".format(item.get("path"), item.get("role")))
    if not components:
        components.append("- No stable component boundary detected yet.")

    compatibility = []
    for name, fact in facts.get("versions", {}).items():
        compatibility.append("- `{}`: `{}`.".format(name, fact.get("value")))
    if not compatibility:
        compatibility.append("- No explicit runtime version constraint detected; verify before using version-specific syntax/APIs.")

    return """# Agent Instructions

<!-- universal-bootstrap:start -->
## Bootstrap contract

- This repository uses Universal AI Development Bootstrap.
- Read `docs/ARCHITECTURE.md` before non-trivial structural work.
- Read `docs/DEVELOPMENT.md` before implementation.
- Read the relevant `docs/specs/` contract before changing observable behavior.
- Read `.ai/RULES.md`, `.ai/policy.json`, and `.ai/memory/project-memory.json` before risky work.
- Treat repository evidence as stronger than generic framework guidance.
- Research official/version-matched primary documentation when a material framework fact is uncertain.
- Do not ask the user to restate stack facts that can be discovered from the repository.
- Ask only when unresolved product intent or a high-risk architecture choice cannot be safely inferred.

## Architecture

- Current style: `{style}`.
- Keep core small and stable.
- Put feature/business logic in explicit modules.
- Keep UI/API/CLI/host adapters at the edge.
- Keep external IO behind infrastructure adapters.
- Do not introduce microservices without a real deployment/scale/fault/data/team boundary.

## Components

{components}

## Compatibility facts

{compatibility}

## Retrieval rules

- Write one rule/fact per bullet or line.
- Include exact paths for path-specific rules.
- Use stable keywords in headings and bullets.
- Keep this root file concise; detailed explanations belong in `docs/` or scoped instruction files.
- Do not bury important compatibility rules in long prose paragraphs.

## Change workflow

- Inspect before planning.
- Update/create a spec for non-trivial behavior changes.
- Create technical design for architectural changes.
- Implement the smallest coherent change.
- Verify using project-native commands and capability-specific checks.
- Update architecture/development docs when boundaries or conventions change.
<!-- universal-bootstrap:end -->
""".format(
        style=architecture.get("style", {}).get("name"),
        components="\n".join(components),
        compatibility="\n".join(compatibility),
    )


def _copy_spec_layer(target: Path, bootstrap_root: Path) -> None:
    source_readme = bootstrap_root / "docs" / "specs" / "README.md"
    source_template = bootstrap_root / "docs" / "specs" / "templates" / "feature-spec.md"
    dest_readme = target / "docs" / "specs" / "README.md"
    dest_template = target / "docs" / "specs" / "templates" / "feature-spec.md"
    dest_readme.parent.mkdir(parents=True, exist_ok=True)
    dest_template.parent.mkdir(parents=True, exist_ok=True)
    if source_readme.exists() and not dest_readme.exists():
        shutil.copyfile(source_readme, dest_readme)
    if source_template.exists() and not dest_template.exists():
        shutil.copyfile(source_template, dest_template)


def apply_onboarding(target: Path, bootstrap_root: Path, context: dict) -> dict:
    ai = target / ".ai"
    docs = target / "docs"

    _managed_update(target / "AGENTS.md", _agent_block(context))
    _managed_update(docs / "ARCHITECTURE.md", render_human_architecture(context["architecture"], context["facts"]))
    _managed_update(docs / "DEVELOPMENT.md", render_development(context["standards"], context["facts"], context["architecture"]))
    _copy_spec_layer(target, bootstrap_root)

    write_json(ai / "discovery" / "architecture.json", context["architecture"])
    write_json(ai / "standards" / "index.json", context["standards"])
    write_json(ai / "research" / "agenda.json", context["research"])

    research_readme = ai / "research" / "README.md"
    research_readme.parent.mkdir(parents=True, exist_ok=True)
    research_readme.write_text(
        "# Research Agenda\n\n"
        "Use official/version-matched primary sources when research is required.\n"
        "Record completed findings in `.ai/research/findings.json`.\n"
        "Do not guess when a material version-specific fact remains unresolved.\n\n"
        + render_research_summary(context["research"]) + "\n",
        encoding="utf-8",
    )

    return {
        "human_docs": ["AGENTS.md", "docs/ARCHITECTURE.md", "docs/DEVELOPMENT.md", "docs/specs/"],
        "architecture_style": context["architecture"]["style"]["name"],
        "research_items": len(context["research"].get("items", [])),
    }
