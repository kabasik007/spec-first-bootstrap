---
name: bootstrap-project
description: Autonomously inspect and onboard a software repository, synthesize the simplest correct architecture, generate concise agent instructions and human development docs, and establish spec-first verification context before non-trivial implementation.
---

# Bootstrap Project

Use this skill when the user references Universal AI Development Bootstrap, asks to initialize/onboard a repository, starts a new application/module/plugin/service, or wants the repository prepared for reliable AI-assisted development.

## Read first

Read the repository's `AUTONOMOUS_BOOTSTRAP.md` and follow it as the operating contract.

## Default behavior

- Inspect repository evidence before asking stack questions.
- Preserve brownfield architecture unless migration is explicitly required.
- Use a modular monolith/internal modules as the default greenfield boundary.
- Do not introduce microservices without concrete deployment/scale/fault/data/team evidence.
- Keep core small; put feature behavior in modules.
- Research official version-matched primary documentation when a material framework fact is uncertain and tools allow it.
- Generate concise `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, and machine-readable `.ai/` context.
- Preserve existing user-authored content outside bootstrap managed blocks.
- Keep instructions retrieval-friendly: one fact/rule per line, exact paths, stable keywords.

## Preferred execution

If this bootstrap repository is available locally:

```bash
python bootstrap.py onboard <target> --intent "<short user intent>"
python bootstrap.py verify <target>
```

If it cannot be executed locally, perform the same phases manually from `AUTONOMOUS_BOOTSTRAP.md`.

## Stop conditions

Do not start implementation when any of these remain materially unresolved:

- target runtime/framework generation affects syntax/API compatibility
- a destructive migration has no rollback/forward plan
- a proposed new service boundary has no concrete operational reason
- product intent is ambiguous enough that different interpretations would produce different user-visible behavior

Otherwise make a best-effort architecture decision from repository evidence and proceed without forcing the user through a setup questionnaire.
