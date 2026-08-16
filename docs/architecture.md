# Bootstrap Architecture

## Purpose

Universal AI Development Bootstrap prepares arbitrary software repositories for reliable AI-assisted development without binding the workflow to one language, framework, runtime generation, architecture fashion or product type.

The default v1.2 experience is autonomous onboarding:

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
agent instructions + human docs + .ai context
        ↓
change-specific spec/design only when needed
```

## Separate truths

Keep these concerns separate:

```text
product contract       docs/specs/
human architecture     docs/ARCHITECTURE.md
human development      docs/DEVELOPMENT.md
machine context        .ai/
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
   │    direct dependency-manifest graph
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
   │    material unknowns + official-source research agenda
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
   │    managed AGENTS/docs/spec-layer generation
   │
   └─ engine/harness.py
        orchestration + generated .ai artifacts
```

The engine uses only the Python standard library. Python is the bootstrap runtime, not a target constraint.

## Autonomous trigger

`AUTONOMOUS_BOOTSTRAP.md` defines the remote-reference protocol.

A coding agent that receives this repository URL in a software-project context should treat it as a request to onboard the current workspace unless the user says otherwise.

This removes repeated setup prompts while keeping discovery evidence-driven.

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

The CLI generates `.ai/research/agenda.json` for material unknowns.

A capable coding agent may then use web/connected tools to resolve version-sensitive architecture facts from official or primary sources.

A research finding should record:

- source
- source version/date
- claim
- affected decision
- confidence

If external research is unavailable, unresolved material facts remain unresolved rather than being guessed.

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

v1.2 preserves the main v1.0/v1.1 discovery surfaces while adding:

- architecture model
- standards index
- research agenda
- human onboarding docs

Generated manifest schema version is `3`.

## Extension points

Future layers can add:

- source/import/call graph
- database/schema graph
- monorepo workspace intelligence
- version-aware official baseline fetch providers
- official documentation providers
- architecture decision scoring from runtime observations
- scoped agent adapters for tools that need them
- incremental discovery cache
- architecture drift checks in CI
