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
7. material blocking questions that repository evidence could not answer
8. a detailed phased development roadmap with gates and definition of done
9. verification strategy
10. architecture research agenda for unresolved version-specific facts
11. concise agent instructions
12. human-readable architecture/development/roadmap documentation

## Default execution

When the bootstrap repository is available locally, prefer:

```bash
python bootstrap.py onboard <target> --intent "<short user intent>"
python bootstrap.py verify <target>
```

`python bootstrap.py init` is also a full autonomous onboarding path by default.

If a generated blocker is answered by the user:

```bash
python bootstrap.py answer <target> <question-id> "<confirmed value>" \
  --source "user confirmed in current conversation"
```

The answer is stored as verified project memory and the context/roadmap is regenerated.

If the bootstrap repository cannot be executed locally, reproduce the same protocol manually from this repository's files. Do not reduce the workflow to copying templates without discovery.

## Phase 1 — Inspect before asking or designing

Read existing project instructions before generating new ones.

Inspect at minimum:

- repository tree and top-level/workspace components
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
- existing verified project memory

Do not ask the user for facts that can be discovered safely from the repository.

## Phase 2 — Resolve only material blocking questions

A setup question is blocking only when the answer can materially change:

- runtime syntax/API compatibility
- framework/host extension architecture
- file/template format
- package/install layout
- database/migration behavior
- public contract or required product behavior
- a high-risk architecture decision

Do not block on preferences that can safely be deferred.

### Ask policy

1. Search repository evidence first.
2. Reuse verified project memory second.
3. Research official/version-matched primary sources when that can answer the question safely.
4. Ask the user only when a material fact is still unresolved.
5. Batch current blocking questions into one concise message when practical.
6. Give concrete likely options plus `Other / specify`.
7. Explain why each answer changes the implementation.
8. Store confirmed answers with provenance.
9. Regenerate questions, research agenda and roadmap.

### Examples

If PHP is detected but no safe compatibility constraint exists, ask something like:

- PHP 5.6 / legacy 5.x
- PHP 7.x
- PHP 8.0-8.1
- PHP 8.2+
- Other / exact version

If an OpenCart-like repository is detected but exact generation is unknown, ask something like:

- OpenCart 2.3.x
- OpenCart 3.x
- OpenCart 4.x
- Other / exact version

If a host extension project has no clear presentation evidence, ask:

- TPL / `.tpl`
- Twig / `.twig`
- mixed/custom view layer
- no template/UI work required

Do not ask these questions when reliable repository evidence already answers them.

## Readiness semantics

Full onboarding writes:

```text
.ai/questions/blocking.json
.ai/planning/roadmap.json
docs/ROADMAP.md
```

`ready_for_implementation=true` means no material setup blocker is currently known.

`ready_for_implementation=false` means onboarding itself may be valid, but risky implementation should wait for the listed questions to be resolved.

`verify` validates the generated context separately from implementation readiness.

## Phase 3 — Preserve or choose architecture

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

## Phase 4 — Build the roadmap before implementation

Generate a roadmap large enough to guide the actual development, but specific enough to be executable.

The default roadmap should contain:

- current intent and architecture style
- readiness/blocking status
- blocking questions
- execution principles
- Phase 0: resolve compatibility/product blockers
- Phase 1: confirm repository truth and architecture
- Phase 2: define product/change contract
- Phase 3: prepare implementation boundaries
- Phase 4: implement feature modules/domain behavior
- Phase 5: integrate interfaces/host lifecycle/external systems
- Phase 6: data/migrations/backward compatibility
- Phase 7: verification/regression
- Phase 8: documentation/packaging/handoff
- deliverables for every phase
- phase dependencies
- exit gates for every phase
- final definition of done

Downstream phases remain `blocked` while setup blockers remain unresolved.

Do not silently skip blocked phase gates.

For trivial L0/L1 work, the active implementation may use only the relevant roadmap slice; do not force ceremonial execution of every phase.

## Phase 5 — Research only where it changes the decision

Use web/connected documentation tools when current or version-specific facts materially affect architecture or compatibility.

Prefer:

1. official documentation for the detected/confirmed version or generation
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

A user-confirmed version should remove the corresponding version-discovery blocker while still allowing version-specific architecture research when needed.

## Phase 6 — Generate useful context, not paperwork

Default human-facing files:

- `AGENTS.md` — concise agent operating rules
- `docs/ARCHITECTURE.md` — current system/component boundaries
- `docs/DEVELOPMENT.md` — setup, commands, conventions, how to add modules safely
- `docs/ROADMAP.md` — phased plan, blockers, gates, definition of done
- `docs/specs/` — product behavior contracts when needed

Default machine-facing context lives in `.ai/`.

Do not generate tool-specific `.codex`, `.claude`, `.cursor`, or similar files by default.

Only create tool-specific adapters when they materially improve the active agent/tool.

Preserve existing human content and update only bootstrap-managed blocks.

## Phase 7 — Retrieval-friendly instructions

Agent guidance must be easy to retrieve with normal code/text search.

Rules:

- one rule/fact per bullet or line
- exact paths for path-specific rules
- stable keywords in headings
- short root instruction file
- detailed material in linked/scoped docs
- no important compatibility rule hidden inside long prose

For agents that support hierarchical `AGENTS.md`, use scoped files only when a directory has genuinely different rules. Do not create dozens of redundant instruction files.

## Phase 8 — Change workflow

For each non-trivial request:

1. read current roadmap, architecture and relevant specs
2. inspect the affected module/component
3. resolve current blocking questions
4. determine whether behavior or architecture changes
5. update/create the minimum required spec/design artifacts
6. implement the smallest coherent change
7. verify using project-native checks
8. update architecture/development/roadmap docs only when system truth/readiness changed

Do not regenerate the whole project context for every small code edit.

## Unknown intent

If the user says only "bootstrap this project" or only references this repository:

- perform repository onboarding
- document current architecture
- generate the development roadmap
- resolve stack/compatibility blockers that matter to future work
- create a spec backlog only when useful
- do not invent product features
- do not start implementing an arbitrary feature

## New feature/module intent

If the user supplies a short intent such as "add a new module" or "build a new application":

- use the intent to name/scope the roadmap/change
- do not invent domain requirements that the user did not provide
- decide the technical boundary from repository evidence and architecture policy
- create the feature/module inside the existing architecture unless a new boundary is justified
- ask product questions only when implementation would otherwise invent observable behavior

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
