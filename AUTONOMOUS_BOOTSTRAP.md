# Autonomous Bootstrap Contract

This is the default operating contract when a coding agent is given this repository as a bootstrap reference.

## Zero-config trigger

If the user references:

`https://github.com/kabasik007/spec-first-bootstrap`

while working on a software repository, assume they want the **current workspace autonomously onboarded for development** unless they explicitly say otherwise.

The user does not need to repeat:

- language or runtime
- framework/platform
- repository layout
- project type
- test/build commands
- architecture style
- module/plugin conventions
- agent instruction files to create
- standard documentation files to create

Discover those from repository evidence first.

A one-line product/change intent is useful but optional.

## Default outcome

Before non-trivial implementation work, establish:

1. repository facts and runtime compatibility
2. current or recommended architecture
3. component/module boundaries
4. dependency and command map
5. project standards/conventions
6. protected/core/generated/vendor boundaries
7. verification strategy
8. architecture research agenda for unresolved version-specific facts
9. concise agent instructions
10. human-readable architecture and development documentation

## Default execution

When the bootstrap repository is available locally, prefer:

```bash
python bootstrap.py onboard <target> --intent "<short user intent>"
python bootstrap.py verify <target>
```

`python bootstrap.py init` is also a full autonomous onboarding path by default.

If the bootstrap repository cannot be executed locally, reproduce the same protocol manually from this repository's files. Do not reduce the workflow to copying templates without discovery.

## Phase 1 — Inspect before designing

Read existing project instructions before generating new ones.

Inspect at minimum:

- repository tree and top-level components
- dependency manifests and lock files
- runtime/version constraints
- framework/platform evidence
- entry points
- tests and QA
- build/lint/format/type-check configuration
- database/migration evidence
- background jobs/workers
- external integrations
- deployment/container configuration
- modules/plugins/extensions
- core/vendor/generated areas
- existing architecture/specification documentation

Do not ask the user for facts that can be discovered safely from the repository.

## Phase 2 — Preserve or choose architecture

### Brownfield default

Preserve existing architecture and conventions unless the requested change explicitly requires migration.

Do not reorganize a legacy repository just because a modern pattern exists.

### Greenfield default

Choose the simplest architecture that gives strong internal boundaries.

Default preference:

`small stable core -> feature modules -> interfaces -> infrastructure adapters -> verification`

Use a modular monolith by default when independent services are not justified.

### Microservice gate

Do not introduce a network/service boundary only because the system may become large.

A service split needs a concrete reason such as:

- independent deployment lifecycle
- independent scaling profile
- useful fault isolation
- explicit data ownership
- independent team/operational ownership

If these are not demonstrated, keep the boundary inside the process as a module.

### Core rule

Core must remain small.

Core may contain stable domain/application contracts and genuinely cross-cutting primitives.

Feature-specific behavior belongs in a module, not in core.

Avoid catch-all `core`, `common`, `shared`, or `utils` growth.

## Phase 3 — Research only where it changes the decision

Use web/connected documentation tools when current or version-specific facts materially affect architecture or compatibility.

Prefer:

1. official documentation for the detected version/generation
2. official source repository/release/tag
3. primary standards/specifications

Do not silently apply documentation for the latest version to an older project.

Record research as:

- source
- version/date
- claim
- affected architecture decision
- confidence

If web access is unavailable, mark material facts unresolved instead of guessing.

## Phase 4 — Generate useful context, not paperwork

Default human-facing files:

- `AGENTS.md` — concise agent operating rules
- `docs/ARCHITECTURE.md` — current system/component boundaries
- `docs/DEVELOPMENT.md` — setup, commands, conventions, how to add modules safely
- `docs/specs/` — product behavior contracts when needed

Default machine-facing context lives in `.ai/`.

Do not generate tool-specific `.codex`, `.claude`, `.cursor`, or similar files by default.

Only create tool-specific adapters when they materially improve the active agent/tool.

Preserve existing human content and update only bootstrap-managed blocks.

## Phase 5 — Retrieval-friendly instructions

Agent guidance must be easy to retrieve with normal code/text search.

Rules:

- one rule/fact per bullet or line
- exact paths for path-specific rules
- stable keywords in headings
- short root instruction file
- detailed material in linked/scoped docs
- no important compatibility rule hidden inside long prose

For agents that support hierarchical `AGENTS.md`, use scoped files only when a directory has genuinely different rules. Do not create dozens of redundant instruction files.

## Phase 6 — Change workflow

For each non-trivial request:

1. read current architecture and relevant specs
2. inspect the affected module/component
3. determine whether behavior or architecture changes
4. update/create the minimum required spec/design artifacts
5. implement the smallest coherent change
6. verify using project-native checks
7. update architecture/development docs only when the system truth changed

Do not regenerate the whole project context for every small code edit.

## Unknown intent

If the user says only "bootstrap this project" or only references this repository:

- perform repository onboarding
- document current architecture
- create a spec backlog only when useful
- do not invent product features
- do not start implementing an arbitrary feature

## New feature/module intent

If the user supplies a short intent such as "add a new module" or "build a new application":

- use the intent to name/scope the change
- do not invent domain requirements that the user did not provide
- decide the technical boundary from repository evidence and architecture policy
- create the feature/module inside the existing architecture unless a new boundary is justified

## Trust order

When guidance conflicts, prefer:

1. explicit current user instruction
2. verified project-specific fact
3. exact repository evidence
4. matching version-specific baseline/documentation
5. existing project architecture/specification
6. detected capability pack
7. generic bootstrap guidance

The bootstrap exists to reduce repeated prompting, not to override reality.
