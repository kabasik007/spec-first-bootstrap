# Roadmap and Blocking Questions

Universal Bootstrap v1.3 separates **bootstrap validity** from **implementation readiness**.

## Why

A coding agent should not repeatedly ask for facts that can be discovered from the repository, but it also should not guess a material compatibility fact just to avoid asking a question.

The workflow is therefore:

```text
discover repository evidence
        ↓
reuse verified project memory
        ↓
research version-matched primary sources when useful
        ↓
material unknown remains?
        ↓
ask the user with options + reason
        ↓
store verified answer
        ↓
regenerate roadmap/context
```

## Blocking vs advisory

A question is blocking when the answer can materially change:

- runtime syntax/API compatibility
- framework/host extension architecture
- template/file format
- package/install layout
- database/migration behavior
- public product behavior
- a high-risk architecture decision

An advisory question can be deferred without making the next implementation step unsafe.

## Generated files

```text
.ai/questions/blocking.json
.ai/planning/roadmap.json
docs/ROADMAP.md
```

## Readiness

`verify.ok=true` means the generated bootstrap context is structurally valid.

`ready_for_implementation=true` means there is no known material setup blocker.

These values are intentionally independent.

## Answers

Use:

```bash
python bootstrap.py answer <target> <question-id> "<value>" --source "<provenance>"
```

The answer is stored in `.ai/memory/project-memory.json` as a manual verified fact.

The bootstrap then regenerates questions and roadmap.

## Roadmap

The default roadmap has nine phases from blocker resolution through handoff. Every phase has:

- objective
- status
- dependencies
- deliverables
- exit gates

The roadmap ends with an explicit definition of done.

Downstream phases remain blocked while setup blockers remain unresolved.

For trivial work, agents may execute only the relevant roadmap slice; the roadmap is a planning model, not a ceremony engine.
