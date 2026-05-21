# Prompt Pack

Use these prompts as a starting point when you point Codex or Claude Code at
this bootstrap repository.

Default setup prompt:

```text
Use https://github.com/potapenko/spec-first-bootstrap as the reference and set up this project for spec-first development.

Read the bootstrap repository first. Add or adapt the needed AGENTS.md, the docs/specs README and template layer, and prompts. If this is an existing project, do brownfield discovery and create project-specific first-pass specs before changing implementation code.
```

Web UI with browser QA:

```text
Use https://github.com/potapenko/spec-first-bootstrap as the reference and set up this web UI project for spec-first development with the optional browser-QA layer.

Read the bootstrap repository first. Add or adapt the needed AGENTS.md, the docs/specs README and template layer, prompts, and qa/web files. Include the qa/web/AGENTS.snippet.md routing block in AGENTS.md so browser-QA instructions load automatically. If this is an existing project, do brownfield discovery and create project-specific first-pass specs before changing implementation code.
```

The files below are follow-up prompts for specific situations.

Available prompts:

- [`greenfield-bootstrap.md`](greenfield-bootstrap.md)
- [`brownfield-discovery.md`](brownfield-discovery.md)
- [`brownfield-interview.md`](brownfield-interview.md)
- [`generate-first-specs.md`](generate-first-specs.md)
- [`optional-web-qa.md`](optional-web-qa.md)
- [`day-to-day-spec-first.md`](day-to-day-spec-first.md)
