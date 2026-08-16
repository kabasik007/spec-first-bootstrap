# Universal AI Development Bootstrap

A local-first, spec-first bootstrap for preparing **any software repository** for AI-assisted development.

It does not assume PHP, JavaScript, Python, OpenCart, PrestaShop, a browser UI, or a modern stack. It inspects the target repository, records evidence, resolves composable capabilities, maps dependencies and risk boundaries, and generates project-specific AI development context.

> Detect first. Specify behavior. Respect architecture. Change safely. Verify with evidence.

## v1.1: Context Intelligence

v1.1 turns the v1.0 detector/pack foundation into an executable context system:

```text
Target repository
      ↓
Discovery + runtime evidence
      ↓
Capability Pack Resolver
      ↓
Dependency Graph
      ↓
Baseline / core-vs-custom evidence
      ↓
Policy + Knowledge + Project Memory
      ↓
Project-specific .ai/ harness
      ↓
Spec → design → implementation → verification
```

The original spec-first rule is unchanged:

- `AGENTS.md` defines how agents work
- `docs/specs/` defines observable product behavior
- `.ai/ARCHITECTURE.md` and change design define technical structure
- tests / `qa/` / `.ai/verification/` provide verification evidence

## Quick start

Python 3.9+ is required only to run the bootstrap engine. **It does not constrain the target project.**

The target may use PHP 5.x/7.x/8.x, Python, Node, Java, .NET, Go, Rust, legacy frameworks, modern frameworks, or mixed stacks.

```bash
python bootstrap.py detect /path/to/project
python bootstrap.py init /path/to/project
python bootstrap.py verify /path/to/project
```

Windows:

```powershell
python bootstrap.py detect D:\projects\my-app
python bootstrap.py init D:\projects\my-app
python bootstrap.py verify D:\projects\my-app
```

`detect` is read-only.

`init` creates/refreshes the machine-readable `.ai/` context. Existing generated Markdown files are preserved unless `--force` is used; discovery, policy, baseline inventory, knowledge selection and memory observations are refreshed.

## New v1.1 commands

### Compare against an official/upstream/local reference

```bash
python bootstrap.py baseline /path/to/project --reference /path/to/reference
```

This creates a deterministic local diff of added, missing and modified files. It is useful for framework/core/vendor boundary analysis without binding the engine to OpenCart, PrestaShop or any other product.

### Check a guarded action

```bash
python bootstrap.py policy-check /path/to/project read .env
python bootstrap.py policy-check /path/to/project write system/library/foo.php
python bootstrap.py policy-check /path/to/project execute "git reset --hard HEAD~1"
```

Exit codes:

- `0` allow
- `2` deny
- `3` explicit confirmation required

`.ai/policy.json` is machine-readable, but it is not magically an OS sandbox. Agent hosts should call `policy-check` or enforce the same policy mechanically.

### Store a verified project fact

```bash
python bootstrap.py memory-add /path/to/project runtime.production_php 7.4.33 \
  --source "production php -v" --confidence 1
```

Manual facts keep provenance and are not silently overwritten by a later auto-scan.

## Generated target structure

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
│   └── risks.json
├── baseline/
│   ├── inventory.json
│   └── diff.json
├── knowledge/
│   └── index.json
├── memory/
│   └── project-memory.json
├── decisions/
├── changes/
└── verification/
```

Product specs remain separate:

```text
docs/specs/
├── README.md
├── templates/
│   └── feature-spec.md
└── features/
```

## Universal detection

The engine recognizes common evidence for:

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

Unknown stacks still work through generic/catalog capability packs. A framework is never supposed to become a global assumption.

## Runtime compatibility is a target fact

A central rule:

> **Never upgrade syntax merely because the bootstrap engine itself is modern.**

PHP 5.6, PHP 7.4 and PHP 8.x are different target constraints. The same applies to Python, Node, Java, .NET, framework generations, database versions, browser targets and operating systems.

Capability packs contribute compatibility guidance, but exact project evidence wins.

## Executable capability packs

v1.0 selected pack IDs. v1.1 **loads and resolves them**.

A detailed pack can contribute:

- `extends`
- runtime/framework compatibility rules
- project rules
- protected paths
- verification requirements
- curated knowledge IDs
- policy fragments

Example:

```text
base/spec-first
base/architecture
base/change-lifecycle
base/security
languages/php
frameworks/opencart
project-types/extension-platform
verification/extension
verification/web
```

Pack inheritance is recursive and deterministic.

Catalog-only packs remain valid fallback capabilities, so bootstrap does not fail simply because a framework does not yet have a rich manifest. `verify` reports catalog-only packs as warnings so they can be improved incrementally.

See [`packs/README.md`](packs/README.md) and [`schemas/pack.schema.json`](schemas/pack.schema.json).

## Dependency graph

v1.1 reads local dependency manifests and creates:

```text
.ai/discovery/dependency-graph.json
.ai/DEPENDENCIES.md
```

Supported direct dependency evidence includes:

- Composer
- npm/package.json
- requirements.txt
- pyproject.toml
- Cargo
- Go modules
- Maven
- NuGet `.csproj`

It records ecosystem, package, constraint, scope and source manifest.

This is deliberately a **manifest graph**, not a fake “complete architecture graph.” Source/import/call graphs can be layered on later.

## Baseline engine

`init` creates a baseline inventory with SHA-256 hashes and classifications.

Secret-like files are skipped.

Paths can be classified as:

- `project`
- `protected`
- `generated-or-vendor`

A reference comparison identifies:

- added
- missing
- modified
- protected-path changes

The core does **not** automatically download an “official” baseline. The caller must select the correct reference/version explicitly. This prevents accidental comparison of incompatible framework generations and keeps the default workflow local-first.

## Knowledge vs memory

These are intentionally separate.

### Knowledge

`knowledge/catalog.json` contains reusable bootstrap guidance with provenance.

Selected knowledge is written to:

```text
.ai/knowledge/index.json
```

### Memory

`.ai/memory/project-memory.json` contains facts about **this exact project**.

Each fact has:

- value
- confidence
- source/evidence
- `observed_at`
- `last_seen`

Trust project-specific verified evidence over generic knowledge.

Never store secrets in memory.

## Policy and permissions

`.ai/policy.json` can describe:

- `deny_read`
- `deny_write`
- `confirm_write`
- `confirm_commands`

Capability packs can contribute policy fragments.

This gives Codex/Claude/IDE wrappers/CI a stable decision primitive instead of relying only on prose instructions.

The repository does not claim that an instruction file alone can enforce security. Full filesystem/process/database sandboxing belongs to the agent host or runtime.

## Brownfield is first-class

Existing applications are not treated as failed greenfield projects.

Before invasive change, discover:

- languages/runtime constraints
- frameworks/platforms/versions
- direct dependency contracts
- project/system shape
- entry points and commands
- core/vendor/generated boundaries
- existing modifications
- migrations and persistence risks
- integrations/deployment
- tests and QA
- unknowns and conflicts

A baseline/reference diff is especially useful for legacy frameworks, but it is optional and universal.

## Modules, plugins and extensions

Extension development is modeled as a capability, not as an OpenCart-specific special case.

Relevant constraints include:

- host platform/version
- extension type
- install / upgrade / uninstall lifecycle
- events/hooks/services/overrides/modification systems
- permissions
- database changes
- translations/languages
- package layout
- host/runtime compatibility
- core-protection boundaries

OpenCart and PrestaShop are initial detailed packs; the architecture supports other platforms the same way.

## Product specs vs architecture

```text
docs/specs/          WHAT observable behavior must do
.ai/ARCHITECTURE.md  HOW the system is structured/bounded
.ai/changes/...      HOW one non-trivial change will be made
verification/tests   HOW the contract is checked
```

The existing feature spec remains product-level:

- Goal
- Scope
- Non-goals
- User-visible behavior
- Invariants
- Edge cases and failure policy
- Route / state / data implications
- Verification mapping

## Adaptive change lifecycle

```text
L0 trivial      → implementation + focused verification
L1 small fix    → short plan + implementation + verification
L2 feature      → spec + plan + implementation + verification
L3 architecture → spec + design/ADR + plan + tests + verification
L4 critical     → impact + rollback/migration/security + staged verification
```

Do not generate architecture bureaucracy for trivial work.

## Verification is capability-driven

Browser QA remains optional.

v1.1 detailed verification packs currently cover:

- web/browser
- API/backend
- extension/module lifecycle

The model can grow to CLI, desktop, database/migrations, packaging, security, pipelines and performance without changing the core workflow.

## Repository structure

```text
.
├── bootstrap.py
├── engine/
│   ├── discovery.py
│   ├── packs.py
│   ├── dependencies.py
│   ├── baseline.py
│   ├── policy.py
│   ├── knowledge.py
│   ├── memory.py
│   └── harness.py
├── AGENTS.md
├── docs/
│   ├── architecture.md
│   ├── context-intelligence.md
│   └── specs/
├── knowledge/
│   └── catalog.json
├── packs/
├── schemas/
├── templates/
├── prompts/
├── qa/
├── examples/
└── tests/
```

## For coding agents

When this repository is available locally:

```text
Read AGENTS.md and docs/architecture.md.
Run `python bootstrap.py detect <target>`.
Review facts, resolved packs, dependencies, baseline classifications and policy.
Run `python bootstrap.py init <target>`.
For non-trivial work, read the generated project context before changing implementation code.
Call policy-check before guarded actions.
Preserve provenance when adding durable project memory.
```

The prompt pack remains a manual fallback when the engine cannot run.

## Design goals

- universal rather than framework-bound
- greenfield and brownfield
- applications, libraries, services, modules, plugins, extensions, CLIs, desktop tools, workers and pipelines
- local-first
- evidence-driven
- legacy-compatible
- minimal dependency surface
- composable
- machine-readable
- safe without pretending prose is a sandbox
- strict for risky work without becoming bureaucracy for trivial changes

## Architecture details

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/context-intelligence.md`](docs/context-intelligence.md)

## License

MIT
