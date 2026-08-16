# Universal AI Development Bootstrap

A local-first, spec-first bootstrap for preparing **any software repository** for AI-assisted development.

It does not assume PHP, JavaScript, Python, OpenCart, PrestaShop, a browser UI, or a modern stack. It inspects the target repository first, records evidence, composes capability packs, and generates project-specific AI development context.

> Detect first. Specify behavior. Respect architecture. Change safely. Verify with evidence.

## What changed

The original project was a lightweight spec-first starter pack. The repository now keeps that useful core and adds an executable bootstrap engine around it.

```text
Target repository
      ↓
Project Detector
      ↓
Project Facts + evidence/confidence
      ↓
Architecture / command / risk discovery
      ↓
Composable Capability Packs
      ↓
Project-specific .ai/ harness
      ↓
Spec → design → implementation → verification
```

The old rule remains important:

- `AGENTS.md` defines how agents work
- `docs/specs/` defines product behavior
- tests / `qa/` / `.ai/verification/` define verification evidence

Technical architecture is now a **separate layer**, not something stuffed into feature specs.

## Quick start

Requires Python 3.9+ only for running the bootstrap engine. **This does not constrain the target project.** The target may use PHP 5.x/7.x/8.x, legacy frameworks, Node, Python, Java, .NET, Go, Rust, or mixed stacks.

From this repository:

```bash
python bootstrap.py detect /path/to/project
python bootstrap.py init /path/to/project
python bootstrap.py verify /path/to/project
```

On Windows:

```powershell
python bootstrap.py detect D:\projects\my-app
python bootstrap.py init D:\projects\my-app
```

`detect` does not modify the target. `init` creates or updates the bootstrap harness under `.ai/`. Existing generated top-level files are preserved unless `--force` is used; discovery facts are refreshed.

## Generated target structure

```text
.ai/
├── manifest.yaml
├── PROJECT.md
├── ARCHITECTURE.md
├── COMMANDS.md
├── RULES.md
├── discovery/
│   ├── project-facts.json
│   └── risks.json
├── changes/
├── verification/
└── memory/
```

The existing product-spec layer remains:

```text
docs/specs/
├── README.md
├── templates/
│   └── feature-spec.md
└── features/
```

## Universal detection

The first engine version can recognize common evidence for:

### Languages / runtimes

- PHP
- Python
- Node / JavaScript / TypeScript
- Go
- Rust
- Java
- .NET

### Frameworks / platforms

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

Unknown stacks still work through generic packs. Detection is intentionally extensible; a framework is never supposed to become a global assumption.

## Runtime compatibility is a target fact

A central rule of this project is:

> **Never upgrade syntax merely because the bootstrap engine itself is modern.**

If a target repository supports PHP 5.6, that compatibility becomes a project constraint. If it supports PHP 7.4 or PHP 8.3, those are different constraints. The same principle applies to Python, Node, Java, .NET, database versions, framework generations, browser targets, and operating systems.

For example, the PHP capability pack explicitly tells the agent to inspect Composer/platform constraints before introducing language syntax.

## Capability packs

Universal behavior comes from composition rather than a giant switch statement.

Example legacy commerce target:

```text
base/spec-first
base/architecture
base/change-lifecycle
languages/php
frameworks/opencart
project-types/web-application
project-types/extension-platform
verification/web
verification/extension
```

Example modern application:

```text
base/spec-first
base/architecture
languages/python
languages/node
frameworks/fastapi
frameworks/react
project-types/backend
project-types/web-ui
project-types/containerized
verification/api
verification/web
```

A repository can select many packs at once.

See [`packs/README.md`](packs/README.md) and [`schemas/pack.schema.json`](schemas/pack.schema.json).

## Brownfield is a first-class mode

Existing applications are not treated as failed greenfield projects.

The bootstrap should discover before recommending change:

- languages and runtime constraints
- frameworks/platforms and versions
- project types and system shape
- commands and build/test entry points
- code and module boundaries
- framework/core/vendor/generated zones
- migrations and persistence risks
- integrations and deployment boundaries
- existing tests and QA
- known unknowns

Discovery output includes evidence and confidence where possible. Agents should verify low-confidence facts before risky changes.

## Modules, plugins, and extensions

Extension development has different constraints from standalone application development.

When an extension platform is detected, the workflow should pay attention to:

- host platform and version
- extension/module type
- lifecycle: install / upgrade / uninstall
- events, hooks, services, overrides, modification systems
- permissions
- database changes
- translations/languages
- package layout
- host compatibility
- core-protection boundaries

OpenCart and PrestaShop are included as initial packs, but they are examples of the architecture — not hard-coded product priorities.

## Product specs vs architecture

Keep these separate:

```text
docs/specs/          WHAT observable behavior must do
.ai/ARCHITECTURE.md  HOW the system is structured / bounded
.ai/changes/...      HOW a particular non-trivial change will be made
verification/tests   HOW the contract is checked
```

The existing feature template remains intentionally product-level:

- Goal
- Scope
- Non-goals
- User-visible behavior
- Invariants
- Edge cases and failure policy
- Route / state / data implications
- Verification mapping

## Adaptive change lifecycle

Not every CSS tweak needs an architecture document.

Use risk-scaled rigor:

```text
L0 trivial      → implementation + focused verification
L1 small fix    → short plan + implementation + verification
L2 feature      → spec + plan + implementation + verification
L3 architecture → spec + design/ADR + plan + tests + verification
L4 critical     → impact + rollback/migration/security + staged verification
```

See [`templates/change/README.md`](templates/change/README.md).

## Verification is not browser-only

The browser QA starter pack remains useful, but it is optional.

The capability model is intended to support verification packs for:

- browser/UI
- API/backend
- CLI
- desktop
- extension/module install/upgrade/uninstall
- database/migrations
- integrations
- packaging
- security
- data pipelines
- performance

Use verification that matches the system.

## Security and risk boundaries

Generated rules include universal safeguards:

- never copy secrets into AI-generated context
- treat framework core/vendor/generated areas as boundaries
- respect target runtime compatibility
- analyze migrations separately
- preserve existing behavior unless the active change intentionally alters it
- prefer extension mechanisms over invasive platform edits

A future policy layer can mechanically enforce filesystem, command, database, and secret permissions; the manifest and pack model are designed to accommodate that without changing the spec-first core.

## Optional future layers

The architecture intentionally leaves room for:

```text
.ai/baseline/   official release / framework baseline comparison
.ai/knowledge/  curated documentation with provenance
.ai/memory/     verified project facts and learned conventions
```

These should be local-first and evidence-based. Network access should be an explicit enhancement for official documentation or official baselines, not a requirement for ordinary discovery.

## Repository structure

```text
.
├── bootstrap.py
├── AGENTS.md
├── docs/
│   ├── architecture.md
│   └── specs/
├── packs/
│   ├── README.md
│   ├── languages/
│   └── frameworks/
├── schemas/
│   └── pack.schema.json
├── templates/
│   └── change/
├── prompts/
├── qa/
├── examples/
└── tests/
```

## For coding agents

If this repository is available locally, prefer running the engine instead of asking the agent to reproduce the bootstrap from memory:

```text
Read this repository's AGENTS.md and docs/architecture.md.
Run `python bootstrap.py detect <target>` first.
Review the detected facts and risks.
Then run `python bootstrap.py init <target>` to generate the target-specific harness.
For brownfield work, inspect the generated discovery output before changing implementation code.
```

If the engine cannot be run, the files under `prompts/` remain a manual fallback.

## Design goals

- universal rather than framework-bound
- useful for greenfield and brownfield
- useful for applications, libraries, services, modules, plugins, extensions, CLIs, desktop tools, workers, and pipelines
- local-first
- evidence-driven
- compatible with legacy projects
- small dependency surface
- composable instead of monolithic
- strict enough for risky work without becoming bureaucracy for trivial changes

## Architecture details

Read [`docs/architecture.md`](docs/architecture.md).

## License

MIT
