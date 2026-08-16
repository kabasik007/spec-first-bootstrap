# Bootstrap Architecture

## Purpose

Universal AI Development Bootstrap prepares arbitrary software repositories for reliable AI-assisted development without binding the workflow to one language, framework, runtime generation, architecture fashion or product type.

The default v1.3 experience is autonomous onboarding with an explicit readiness gate:

```text
repository + optional one-line intent
        ↓
repository evidence
        ↓
context intelligence
        ↓
architecture synthesis
        ↓
standards + research agenda
        ↓
blocking-question synthesis
        ↓
roadmap + phase gates
        ↓
agent instructions + human docs + .ai context
        ↓
resolve blockers / verified memory
        ↓
change-specific spec/design only when needed
        ↓
implementation + verification
```

## Separate truths

Keep these concerns separate:

```text
product contract       docs/specs/
human architecture     docs/ARCHITECTURE.md
human development      docs/DEVELOPMENT.md
human roadmap          docs/ROADMAP.md
machine context        .ai/
blocking questions     .ai/questions/
execution plan         .ai/planning/
change design          .ai/changes/
verification           tests / qa / .ai/verification/
reusable knowledge     .ai/knowledge/
project facts          .ai/memory/
```

## Engine layers

```text
bootstrap.py
   │
   ├─ engine/discovery.py
   │    stack, runtime, framework, commands, risks
   │
   ├─ engine/packs.py
   │    composable capability resolution
   │
   ├─ engine/dependencies.py
   │    workspace-aware direct dependency-manifest graph
   │
   ├─ engine/baseline.py
   │    inventory + explicit reference diff
   │
   ├─ engine/architecture.py
   │    component discovery + simplest-sufficient architecture decision
   │
   ├─ engine/standards.py
   │    project standards + retrieval-friendly documentation rules
   │
   ├─ engine/research.py
   │    material unknowns + version-matched official-source research agenda
   │
   ├─ engine/questions.py
   │    material unresolved facts -> blocking/advisory questions
   │
   ├─ engine/roadmap.py
   │    phased execution plan + dependencies + exit gates + definition of done
   │
   ├─ engine/policy.py
   │    machine-readable guardrails + decision primitive
   │
   ├─ engine/knowledge.py
   │    curated reusable guidance with provenance
   │
   ├─ engine/memory.py
   │    project-specific durable facts with provenance
   │
   ├─ engine/onboarding.py
   │    managed AGENTS/docs/spec/roadmap generation
   │
   └─ engine/harness.py
        orchestration + generated .ai artifacts
```

The engine uses only the Python standard library. Python is the bootstrap runtime, not a target constraint.

## Autonomous trigger

`AUTONOMOUS_BOOTSTRAP.md` defines the remote-reference protocol.

A coding agent that receives this repository URL in a software-project context should treat it as a request to onboard the current workspace unless the user says otherwise.

This removes repeated setup prompts while keeping discovery evidence-driven.

## Question synthesis

Questions are not a first step.

Order:

```text
repository evidence
verified project memory
version-matched primary research when useful
        ↓
material unknown remains?
        ↓
blocking question
```

A question is blocking only when its answer can materially change runtime compatibility, host/framework behavior, file format, package/install layout, data/migration behavior, public behavior, or a high-risk architecture decision.

Examples:

- PHP compatibility floor when no safe project constraint exists
- exact OpenCart/PrestaShop/host generation when extension APIs differ by version
- TPL/Twig/mixed view layer when repository evidence is missing or contradictory
- Python/Node runtime floor when syntax/tooling compatibility cannot be inferred

Questions include:

- stable ID
- category
- project-memory key
- concrete question
- why it matters
- repository evidence
- likely options plus an escape hatch
- scope

Confirmed answers become manual verified memory and are stronger than generic bootstrap guidance.

## Readiness model

Bootstrap validity and implementation readiness are intentionally separate.

```text
verify.ok = generated bootstrap context is structurally valid
ready_for_implementation = no known material setup blocker remains
```

A project can therefore be correctly onboarded while still waiting for a user answer.

`verify` reports blocker IDs as warnings but does not claim the generated context is invalid merely because human input is still required.

## Roadmap model

`engine/roadmap.py` creates a large default roadmap for non-trivial development.

Human form:

```text
docs/ROADMAP.md
```

Machine form:

```text
.ai/planning/roadmap.json
```

Default phases:

```text
Phase 0  Resolve compatibility and product blockers
Phase 1  Confirm repository truth and architecture
Phase 2  Define product/change contract
Phase 3  Prepare implementation boundaries
Phase 4  Implement feature modules/domain behavior
Phase 5  Integrate interfaces/host lifecycle/external systems
Phase 6  Data/migrations/backward compatibility
Phase 7  Verification/regression
Phase 8  Documentation/packaging/handoff
```

Every phase contains:

- objective
- status
- dependencies
- deliverables
- exit gates

The roadmap also contains a final definition of done.

When blockers exist, downstream phases remain blocked.

For low-risk L0/L1 work, the agent may operate on the relevant roadmap slice instead of ceremonially executing every phase.

## Answer loop

`bootstrap.py answer` closes a generated blocker:

```text
question ID + confirmed value + source
        ↓
manual verified memory
        ↓
regenerate context
        ↓
research agenda updates
        ↓
question set updates
        ↓
roadmap/readiness updates
```

The same answer should not be requested again while the verified fact remains applicable.

## Architecture synthesis

### Brownfield

Preserve the current architecture unless the active request explicitly needs a migration.

Existing directories, dependency manifests, extension/platform boundaries and deployment-shaped components are evidence.

### Greenfield

Use the simplest architecture with strong internal boundaries.

Default conceptual shape:

```text
small stable core
        ↓
feature modules
        ↓
interfaces / host adapters
        ↓
infrastructure adapters
        ↓
verification
```

This is a conceptual boundary model, not a requirement that every project use those exact directory names.

### Microservices

Microservices are not the default.

A service/network boundary needs evidence such as:

- independent deployment
- independent scaling
- useful fault isolation
- explicit data ownership
- independent team/operational ownership

Without that evidence, keep the capability as an internal module.

## Core boundary

Core must remain small.

Good core contents:

- stable domain/application contracts
- genuinely cross-cutting primitives
- abstractions required by multiple modules

Bad core growth:

- feature-specific business behavior
- host/framework-specific controllers
- random helpers moved to avoid deciding ownership
- direct external IO that belongs behind adapters

## Human onboarding

Full `init/onboard` creates or updates managed sections in:

- `AGENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/ROADMAP.md`

It also copies the spec-layer README/template when missing.

Existing user-authored content outside bootstrap markers is preserved.

Tool-specific `.codex`, `.claude`, `.cursor`, etc. files are not default output.

## Retrieval model

Generated instructions are optimized for normal text/code search:

- one rule/fact per line
- exact paths where relevant
- stable keywords/headings
- concise root instructions
- detailed context in linked/scoped docs

Hierarchical/scoped instructions should be added only when a subtree genuinely differs.

## Research model

Research is selective.

The CLI generates `.ai/research/agenda.json` for material unknowns and version-sensitive architecture facts.

A capable coding agent may then use web/connected tools to resolve version-sensitive architecture facts from official or primary sources.

A research finding should record:

- source
- source version/date
- claim
- affected decision
- confidence

If external research is unavailable, unresolved material facts remain unresolved rather than being guessed.

Verified user answers are supplied to the research layer so a confirmed framework version replaces the generic version-discovery item with version-specific architecture research where appropriate.

## Evidence first

Detected facts are hypotheses with evidence/confidence.

Trust order:

```text
explicit user instruction
verified project fact
exact repository evidence
matching version-specific baseline/documentation
existing project architecture/spec
capability pack
bootstrap generic guidance
```

A modern bootstrap must not force a legacy target onto modern syntax or framework conventions.

## Capability composition

A target can combine multiple capabilities:

```text
base/security
languages/php
languages/node
frameworks/opencart
frameworks/react
project-types/extension-platform
project-types/web-ui
verification/extension
verification/web
```

Pack inheritance is resolved before rules, compatibility, protected paths, verification, knowledge and policy fragments are merged.

Catalog-only packs remain valid fallbacks so an unknown/lightly-modeled stack still bootstraps.

## Local-first baseline

Baseline comparison accepts an explicit local reference tree.

The core engine does not automatically fetch an upstream/latest release because version identity is a correctness boundary.

Network-enabled official baseline providers may be added later as explicit capabilities.

## Security model

Markdown instructions are not a sandbox.

`.ai/policy.json` is machine-readable and `policy-check` exposes `allow`, `confirm`, or `deny` for external agent hosts.

Full OS/container/database sandboxing remains the responsibility of the execution host.

Secret-like files are skipped by baseline inventory and must never be copied into generated context.

## Compatibility

v1.3 preserves the main v1.0-v1.2 discovery/context surfaces while adding:

- blocking question model
- implementation readiness
- human roadmap
- machine roadmap
- verified-answer refresh workflow

Generated manifest schema version is `4`.

## Extension points

Future layers can add:

- source/import/call graph
- database/schema graph
- more runtime/framework-specific question providers
- deployment/environment fact providers
- version-aware official baseline fetch providers
- official documentation providers
- architecture decision scoring from runtime observations
- scoped agent adapters for tools that need them
- incremental discovery cache
- architecture drift checks in CI
