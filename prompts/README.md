# Prompt Pack

Use these prompts as a starting point when you point Codex or Claude Code at
this bootstrap repository.

Default setup prompt:

```text
Use https://github.com/potapenko/spec-first-bootstrap as the reference and set up this project for spec-first development.

Read the bootstrap repository first. Add or adapt the needed AGENTS.md, docs/specs, and prompts. Add optional QA only if it fits this project. If this is an existing project, do brownfield discovery and create first-pass specs before changing implementation code.
```

Russian version:

```text
Сходи на https://github.com/potapenko/spec-first-bootstrap и настрой этот проект для spec-first разработки.

Сначала прочитай bootstrap-репозиторий. Добавь или адаптируй инструкции для агента, docs/specs и prompts. QA-слой добавляй только если он подходит проекту. Если проект уже не пустой, сначала разберись в текущем поведении и создай первые спеки; код пока не меняй.
```

The files below are follow-up prompts for specific situations.

Available prompts:

- [`greenfield-bootstrap.md`](greenfield-bootstrap.md)
- [`brownfield-discovery.md`](brownfield-discovery.md)
- [`brownfield-interview.md`](brownfield-interview.md)
- [`generate-first-specs.md`](generate-first-specs.md)
- [`optional-web-qa.md`](optional-web-qa.md)
- [`day-to-day-spec-first.md`](day-to-day-spec-first.md)
