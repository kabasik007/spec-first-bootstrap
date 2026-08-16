# Universal AI Development Bootstrap

A local-first, spec-first, **autonomous repository onboarding system** for AI-assisted software development.

It is intentionally not bound to PHP, OpenCart, PrestaShop, Python, Node, microservices, browser apps, or a modern stack.

> Give the agent the repository. Let it inspect reality. Build the simplest correct architecture. Preserve the rules for the next session.

## Zero-config usage

For a coding agent, this is the primary usage:

```text
Use https://github.com/kabasik007/spec-first-bootstrap
```

That is enough to trigger the default autonomous bootstrap protocol when the agent can read this repository.

The agent should treat the current workspace as the target, inspect it, determine architecture and compatibility, generate concise agent instructions and human development docs, and only then begin non-trivial implementation.

You do **not** need to repeatedly describe:

- PHP/Python/Node/etc. version
- OpenCart/PrestaShop/framework generation
- project type
- folder layout
- build/test commands
- whether it is an app/module/plugin/service
- which documentation files to create
- which architecture style to use

Those are discovered from repository evidence first.

A short intent is optional and useful:

```text
Use https://github.com/kabasik007/spec-first-bootstrap
We are adding a new module.
```

The bootstrap must not invent missing product requirements from that sentence. It uses the intent only to scope architecture/change planning.

Read [`AUTONOMOUS_BOOTSTRAP.md`](AUTONOMOUS_BOOTSTRAP.md) for the full zero-config contract.

## v1.2: Autonomous Bootstrap

v1.2 adds architecture synthesis, standards discovery, research planning and human onboarding on top of the v1.1 Context Intelligence layer.

```text
repository + optional one-line intent
        |
        v
inspect repository evidence
        |
        v
detect runtime/framework/project shape
        |
        v
resolve capability packs + policy + knowledge
        |
        v
map dependencies + baseline/core boundaries
        |
        v
discover development standards
        |
        v
research only material unresolved facts
        |
        v
preserve/choose simplest sufficient architecture
        |
        v
AGENTS.md + docs + machine-readable .ai context
        |
        v
spec/design only when the actual change requires it
        |
        v
implement + verify
```

## Architecture default

The bootstrap does **not** default to microservices.

Greenfield preference:

```text
small stable core
        ↓
explicit feature modules
        ↓
interfaces (UI/API/CLI/host adapters)
        ↓
infrastructure adapters
        ↓
verification
```

A modular monolith/internal module boundary is preferred until a real service boundary exists.

A service split should have a concrete reason:

- independent deployment lifecycle
- independent scaling profile
- useful fault isolation
- explicit data ownership
- independent team/operational ownership

Brownfield projects preserve existing architecture by default.

Legacy code is not treated as failed greenfield code.

## Core rule

Core stays small.

Feature/business behavior belongs in explicit modules.

UI/API/CLI/platform entry points belong at the edge.

Database/filesystem/queues/external APIs belong behind infrastructure adapters.

Avoid turning `core`, `shared`, `common`, or `utils` into catch-all folders.

## Manual CLI

Python 3.9+ is required only to run the bootstrap engine. It does **not** constrain the target project.

Full autonomous onboarding:

```bash
python bootstrap.py onboard /path/to/project --intent "short intent"
python bootstrap.py verify /path/to/project
```

`init` is also full onboarding by default:

```bash
python bootstrap.py init /path/to/project
```

Old v1.1-style machine harness only:

```bash
python bootstrap.py init /path/to/project --harness-only
```

Read-only architecture preview:

```bash
python bootstrap.py detect /path/to/project --intent "short intent"
```

## What full onboarding creates

Human-facing project context:

```text
AGENTS.md

docs/
├── ARCHITECTURE.md
├── DEVELOPMENT.md
└── specs/
    ├── README.md
    └── templates/
        └── feature-spec.md
```

Machine-readable context:

```text
.ai/
├── manifest.yaml
├── PROJECT.md
├── ARCHITECTURE.md
├── DEPENDENCIES.md
├── BASELINE.md
├── COMMANDS.md
├── RULES.md
├── VERIFICATION.md
├── policy.json
├── discovery/
│   ├── project-facts.json
│   ├── packs.json
│   ├── dependency-graph.json
│   ├── architecture.json
│   └── risks.json
├── standards/
│   └── index.json
├── research/
│   ├── agenda.json
│   └── README.md
├── baseline/
├── knowledge/
├── memory/
├── decisions/
├── changes/
└── verification/
```

Existing human content is preserved. Bootstrap-owned sections use managed markers and are updated without replacing unrelated project documentation.

## Human docs are part of the product

The bootstrap does not only generate files for an AI.

`docs/ARCHITECTURE.md` should let a developer answer:

- what the main components are
- where feature logic belongs
- what belongs in core
- where external IO lives
- which boundaries are deployable vs internal
- why the current architecture style was chosen
- when a module is allowed to become a service

`docs/DEVELOPMENT.md` should let a developer answer:

- how to start
- what commands exist
- what lint/format/type/test configuration exists
- what conventions are already present
- how to add a new module/block/service safely
- where exact runtime compatibility facts live

## Retrieval-friendly instructions

Agent instructions are written for retrieval, not as essays.

Default rules:

- one rule/fact per bullet or line
- exact paths for path-specific rules
- stable keywords in headings
- short root `AGENTS.md`
- detailed knowledge in linked/scoped docs
- no important compatibility rule hidden in a long paragraph

Tool-specific `.codex`, `.claude`, `.cursor`, etc. files are **not generated by default**.

The bootstrap uses the cross-agent `AGENTS.md` convention first and adds tool-specific adapters only when they materially improve the active tool.

A standard Agent Skill is also included at [`skills/bootstrap-project/SKILL.md`](skills/bootstrap-project/SKILL.md).

## Research policy

The local CLI does not pretend it can know every framework version convention.

It creates `.ai/research/agenda.json` for material unknowns.

A capable coding agent should use web/connected documentation tools when:

- exact framework/version behavior is uncertain
- official extension architecture affects the design
- a current tool/standard capability may have changed

Source preference:

1. exact repository evidence
2. official version-matched documentation
3. official source/release/tag
4. primary technical standards

Never silently apply current/latest framework documentation to a legacy target.

Research findings should record source, version/date, claim, affected decision and confidence.

## Universal detection

Current language/runtime evidence includes:

- PHP
- Python
- Node / JavaScript / TypeScript
- Go
- Rust
- Java
- .NET

Current framework/platform evidence includes:

- OpenCart
- PrestaShop
- Laravel
- Symfony
- WordPress
- Django
- FastAPI
- Flask
- React
- Vue
- Next.js
- Electron

Unknown stacks still work through generic capability packs and repository evidence.

A framework is a capability, not a bootstrap-wide assumption.

## Runtime compatibility is a project fact

> Never modernize syntax just because the bootstrap engine is modern.

PHP 5.6, PHP 7.4 and PHP 8.x are different valid target constraints.

The same principle applies to Python, Node, Java, .NET, framework generations, database versions, browsers and operating systems.

Verified project evidence wins over generic guidance.

## Context Intelligence from v1.1

v1.2 keeps the full v1.1 layer.

### Capability packs

Packs can contribute:

- inheritance via `extends`
- compatibility rules
- architecture/project rules
- protected paths
- verification requirements
- curated knowledge IDs
- policy fragments

### Dependency graph

Direct dependency evidence currently supports:

- Composer
- npm/package.json
- requirements.txt
- pyproject.toml
- Cargo
- Go modules
- Maven
- NuGet `.csproj`

### Baseline engine

```bash
python bootstrap.py baseline /path/to/project --reference /path/to/reference
```

The engine compares explicit local references and never assumes that the latest upstream framework version matches a legacy target.

### Policy engine

```bash
python bootstrap.py policy-check /path/to/project read .env
python bootstrap.py policy-check /path/to/project write system/library/foo.php
python bootstrap.py policy-check /path/to/project execute "git reset --hard HEAD~1"
```

Decisions:

- `allow`
- `confirm`
- `deny`

Policy is a machine-readable decision primitive, not a claim that Markdown is an OS sandbox.

### Project memory

```bash
python bootstrap.py memory-add /path/to/project runtime.production_php 7.4.33 \
  --source "production php -v" --confidence 1
```

Manual verified facts keep provenance and are not silently overwritten by auto-discovery.

## Change rigor scales with risk

```text
L0 trivial      -> implementation + focused verification
L1 small fix    -> short plan + implementation + verification
L2 feature      -> spec + plan + implementation + verification
L3 architecture -> spec + design/ADR + plan + tests + verification
L4 critical     -> impact + rollback/migration/security + staged verification
```

Do not generate paperwork for trivial work.

Do not regenerate the whole bootstrap context for every small edit.

## Influences and research

v1.2 was informed by primary-source research into:

- GitHub Spec Kit
- OpenSpec
- Agent OS
- BootstrapAgent
- Codex `AGENTS.md` behavior
- Agent Skills specification

The useful ideas and the parts intentionally *not* copied are documented in [`docs/design-research.md`](docs/design-research.md).

## Repository structure

```text
.
├── AUTONOMOUS_BOOTSTRAP.md
├── bootstrap.py
├── engine/
│   ├── discovery.py
│   ├── architecture.py
│   ├── standards.py
│   ├── research.py
│   ├── onboarding.py
│   ├── packs.py
│   ├── dependencies.py
│   ├── baseline.py
│   ├── policy.py
│   ├── knowledge.py
│   ├── memory.py
│   └── harness.py
├── skills/
│   └── bootstrap-project/
│       └── SKILL.md
├── AGENTS.md
├── docs/
├── knowledge/
├── packs/
├── schemas/
├── templates/
├── prompts/
├── qa/
├── examples/
└── tests/
```

## Design goals

- one repository reference should be enough to start
- universal rather than framework-bound
- correct for greenfield and brownfield
- architecture before accidental complexity
- modular by default, microservices only with evidence
- human-readable and agent-readable context
- local-first discovery
- web research only for material/version-sensitive unknowns
- legacy-compatible
- minimal bootstrap dependencies
- machine-readable guardrails
- persistent verified project knowledge
- concise retrieval-friendly instructions
- strict for risky work without bureaucracy for small work

## Documentation

- [`AUTONOMOUS_BOOTSTRAP.md`](AUTONOMOUS_BOOTSTRAP.md)
- [`docs/architecture.md`](docs/architecture.md)
- [`docs/context-intelligence.md`](docs/context-intelligence.md)
- [`docs/design-research.md`](docs/design-research.md)

## License

MIT
