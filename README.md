# Spec-First Bootstrap for AI-Assisted Projects

## Start here

Open your real project in Codex, Claude Code, or another coding agent and paste
this prompt:

```text
Use https://github.com/potapenko/spec-first-bootstrap as the reference and set up this project for spec-first development.

Read the bootstrap repository first. Add or adapt the needed AGENTS.md, docs/specs, and prompts. Add optional QA only if it fits this project. If this is an existing project, do brownfield discovery and create first-pass specs before changing implementation code.
```

Russian version:

```text
Сходи на https://github.com/potapenko/spec-first-bootstrap и настрой этот проект для spec-first разработки.

Сначала прочитай bootstrap-репозиторий. Добавь или адаптируй инструкции для агента, docs/specs и prompts. QA-слой добавляй только если он подходит проекту. Если проект уже не пустой, сначала разберись в текущем поведении и создай первые спеки; код пока не меняй.
```

That is the normal setup path. You give the agent this repository URL and ask
it to prepare your current project.

## Why this exists

A lot of AI coding failures are not coding failures.
They happen earlier, when product behavior was never made explicit.
This repo gives the agent a simple place to keep that truth before code starts.

**Do not start with code. Start with a spec.**

## What the agent should do

The agent should:

- read this bootstrap repository first
- preserve existing project-specific agent instructions
- add or adapt `AGENTS.md`
- add the `docs/specs/` product-spec layer
- add useful prompts from `prompts/`
- add `qa/` only when a verification layer fits the project
- create a product map, spec backlog, or first-pass specs before implementation
  work starts

This is not just for browser apps. The same model works for web, backend, API,
CLI, data pipelines, internal tools, and other software projects. Browser QA is
optional.

This bootstrap did not come out of theory. It was extracted from several
months of work on four internal projects behind
[`playphrase.me`](https://playphrase.me), then cleaned up into a small public
setup.

If you want the broader context behind this workflow, the main ideas are also
written up in a short article
[here](https://www.patreon.com/posts/spec-first-or-ai-155606468?utm_medium=clipboard_copy&utm_source=copyLink&utm_campaign=postshare_creator&utm_content=join_link).

## What this is for

Use this repository in either of these situations:

- you are starting a new project and want spec-first work from day one
- you already have a working project and want to migrate it to a spec-first
  workflow

Included:

- a minimal public `AGENTS.md`
- a product-spec layer under `docs/specs/`
- a reusable feature spec template
- example specs
- prompt files for greenfield and brownfield adoption
- an optional browser-QA starter pack for web UI projects

## Three layers

Instead of keeping product truth scattered across code and chat history, this
workflow keeps three separate layers:

1. `docs/specs/` - product truth
2. implementation - code that follows the contract
3. `qa/` - verification evidence when the project needs it

The rules are simple:

- context should live in specs, not only in code
- code should implement the contract
- QA should verify the contract when the project needs QA artifacts

## Two common scenarios

### Greenfield project

Use this when the project is new or mostly empty.

The agent should:

- set up the spec-first workflow in the new project
- create the initial product-spec structure
- propose the first specs that should exist before feature code

Reference prompt:

- [`prompts/greenfield-bootstrap.md`](prompts/greenfield-bootstrap.md)

### Brownfield project

Use this when the project already exists and you want to retrofit specs.

The agent should:

- analyze the current codebase
- extract product behavior from code, routes, state, tests, UI flows, and docs
- ask for clarification where product intent is unclear
- generate first-pass specs for the most important product areas

In practice, brownfield migration usually means:

1. map the product
2. build a spec backlog
3. generate first-pass specs
4. review unknowns and conflicts
5. only then start changing code

Reference prompts:

- [`prompts/brownfield-discovery.md`](prompts/brownfield-discovery.md)
- [`prompts/brownfield-interview.md`](prompts/brownfield-interview.md)
- [`prompts/generate-first-specs.md`](prompts/generate-first-specs.md)

## Minimal workflow

Use this workflow for non-trivial work:

1. Clarify the product goal.
2. Create or update a spec.
3. Review behavior, invariants, and edge cases.
4. Implement against the spec.
5. Add or update verification artifacts if the project needs them.

## Optional web QA layer

Browser QA is **optional**.

Use it if your project has a browser UI and you want a lightweight structure
for smoke checks, regression cases, and run reports.

The optional web QA pack assumes Playwright-style real-browser checks.

Do not treat browser QA as mandatory for every project. Many projects are
better served by API verification, CLI verification, integration testing,
operator runbooks, or other project-specific checks.

If you do have a browser UI, this repo includes a compact starter pack under:

- [`qa/web/README.md`](qa/web/README.md)
- [`qa/web/AGENTS.snippet.md`](qa/web/AGENTS.snippet.md)

And a matching prompt:

- [`prompts/optional-web-qa.md`](prompts/optional-web-qa.md)

## Prompt pack

The default setup prompt above is usually enough.

The files under [`prompts/`](prompts/) are follow-up prompts for specific
situations:

- `greenfield-bootstrap.md`
- `brownfield-discovery.md`
- `brownfield-interview.md`
- `generate-first-specs.md`
- `optional-web-qa.md`
- `day-to-day-spec-first.md`

<details>
<summary>Manual install fallback</summary>

Use this only if your agent cannot fetch or inspect the GitHub repository.

Copy these into the target project:

Required:

- `AGENTS.md`
- `docs/`

Recommended:

- `prompts/`

Optional:

- `qa/`

If you copy `qa/`, also add the optional browser-QA routing block from:

- `qa/web/AGENTS.snippet.md`

Without that extra block in the project's `AGENTS.md`, the agent may not load
the QA instructions automatically.

After copying, ask the agent to work from the files already inside the project:

```text
Read AGENTS.md and docs/specs/README.md in this project first.

This is a brownfield project. Generate first-pass specs before changing implementation code.
```

</details>

## Suggested repository structure

```text
.
├── AGENTS.md
├── README.md
├── docs/
│   └── specs/
│       ├── README.md
│       ├── templates/
│       │   └── feature-spec.md
│       └── features/
│           ├── prompt-first-bootstrap.md
│           └── favorites-spec.md
├── examples/
│   └── favorites-spec.md
├── prompts/
│   ├── README.md
│   └── *.md
└── qa/
    ├── README.md
    └── web/
        └── ...
```

## Included files

- `AGENTS.md` - minimal workflow rules for agents
- `docs/specs/README.md` - how the spec layer works
- `docs/specs/templates/feature-spec.md` - reusable template
- `docs/specs/features/prompt-first-bootstrap.md` - onboarding contract for
  this repo
- `docs/specs/features/favorites-spec.md` - example production-style spec
- `examples/favorites-spec.md` - same example in a simpler discovery path
- `prompts/` - ready-to-send prompts for setup and migration
- `qa/web/` - optional browser-QA starter pack for web UI projects

## Copy-paste starting point

The simplest rule to adopt inside a target project's `AGENTS.md` is this:

```md
## Spec-First Rule

Before implementing any non-trivial feature:

1. Clarify the product goal.
2. Create or update a spec under `docs/specs/`.
3. Confirm user-visible behavior, invariants, and edge cases.
4. Only then begin implementation.

`AGENTS.md` is not the source of truth for detailed feature behavior.
Detailed behavior must live in specs.
```

## License

MIT
