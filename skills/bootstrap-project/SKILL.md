---
name: bootstrap-project
description: Autonomously inspect and onboard a software repository, synthesize the simplest correct architecture, ask only material unresolved compatibility questions, generate a phased development roadmap, and establish concise agent/human context before non-trivial implementation.
---

# Bootstrap Project

Use this skill when the user references Universal AI Development Bootstrap, asks to initialize/onboard a repository, starts a new application/module/plugin/service, or wants the repository prepared for reliable AI-assisted development.

## Read first

Read the repository's `AUTONOMOUS_BOOTSTRAP.md` and follow it as the operating contract.

## Default behavior

- Inspect repository evidence before asking stack questions.
- Reuse verified project memory before asking a question again.
- Ask only material blockers that change runtime compatibility, framework/host behavior, file format, migration/data behavior, packaging, public behavior, or high-risk architecture.
- Batch current blockers when practical.
- Give concrete likely options plus `Other / specify` and explain why each question matters.
- Preserve brownfield architecture unless migration is explicitly required.
- Use a modular monolith/internal modules as the default greenfield boundary.
- Do not introduce microservices without concrete deployment/scale/fault/data/team evidence.
- Keep core small; put feature behavior in modules.
- Research official version-matched primary documentation when a material framework fact is uncertain and tools allow it.
- Generate concise `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, `docs/ROADMAP.md`, and machine-readable `.ai/` context.
- Generate `.ai/questions/blocking.json` and `.ai/planning/roadmap.json`.
- Preserve existing user-authored content outside bootstrap managed blocks.
- Keep instructions retrieval-friendly: one fact/rule per line, exact paths, stable keywords.

## Preferred execution

If this bootstrap repository is available locally:

```bash
python bootstrap.py onboard <target> --intent "<short user intent>"
python bootstrap.py verify <target>
```

If blockers are generated, ask the user and record each confirmed answer:

```bash
python bootstrap.py answer <target> <question-id> "<confirmed value>" \
  --source "user confirmed in current conversation"
```

Then inspect regenerated readiness/roadmap before implementation.

If the bootstrap cannot be executed locally, perform the same phases manually from `AUTONOMOUS_BOOTSTRAP.md`.

## Stop conditions

Do not start risky/non-trivial implementation when `ready_for_implementation=false` or when any of these remain materially unresolved:

- target runtime/framework generation affects syntax/API compatibility
- target host/template technology affects required file format or extension mechanism
- a destructive migration has no rollback/forward plan
- a proposed new service boundary has no concrete operational reason
- product intent is ambiguous enough that different interpretations would produce different user-visible behavior

A valid onboarding can still have blockers. Do not confuse `verify.ok=true` with implementation readiness.
