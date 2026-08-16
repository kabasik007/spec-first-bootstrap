# Prompt Pack

Prompts are now a **fallback and follow-up layer**, not the primary bootstrap engine.

Preferred setup:

```text
Read https://github.com/kabasik007/spec-first-bootstrap.
Run its detector against the current project before making assumptions about stack, versions, project type, or architecture.
Then initialize the project-specific harness and inspect the generated `.ai/` discovery files before implementation work.
Preserve existing project-specific instructions and do not change product code during bootstrap setup.
```

When the repository is available locally, use:

```bash
python bootstrap.py detect <target>
python bootstrap.py init <target>
```

Available follow-up prompts:

- [`greenfield-bootstrap.md`](greenfield-bootstrap.md)
- [`brownfield-discovery.md`](brownfield-discovery.md)
- [`brownfield-interview.md`](brownfield-interview.md)
- [`generate-first-specs.md`](generate-first-specs.md)
- [`optional-web-qa.md`](optional-web-qa.md)
- [`day-to-day-spec-first.md`](day-to-day-spec-first.md)

Rules:

- detect before assuming
- do not hard-code framework or language versions
- preserve legacy compatibility when it is intentional
- keep product specs separate from technical architecture
- use browser QA only when the target actually has a browser surface
