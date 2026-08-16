# Universal AI Development Bootstrap

A local-first, spec-first, **autonomous repository onboarding and development-planning system** for AI-assisted software development.

It is intentionally not bound to PHP, OpenCart, PrestaShop, Python, Node, microservices, browser apps, or a modern stack.

> Give the agent the repository. Let it inspect reality. Ask only what cannot be discovered safely. Build the roadmap. Then implement.

## Zero-config usage

For a coding agent, this is the primary usage:

```text
Use https://github.com/kabasik007/spec-first-bootstrap
```

That is enough to trigger the default autonomous bootstrap protocol when the agent can read this repository.

The agent should treat the current workspace as the target, inspect it, determine stack/version/architecture, generate concise instructions and human docs, build a phased roadmap, surface only material unresolved questions, and only then begin non-trivial implementation.

You do **not** need to repeatedly describe:

- PHP/Python/Node/etc. version when repository evidence already provides it
- OpenCart/PrestaShop/framework generation when it can be detected
- project type
- folder layout
- build/test commands
- whether it is an app/module/plugin/service
- which documentation files to create
- which architecture style to use
- which roadmap files to create

A short intent is optional and useful:

```text
Use https://github.com/kabasik007/spec-first-bootstrap

We are adding a new module.
```

The bootstrap uses that sentence to scope architecture and planning. It must not invent missing product requirements.

Read [`AUTONOMOUS_BOOTSTRAP.md`](AUTONOMOUS_BOOTSTRAP.md) for the full zero-config contract.

---

## v1.3: Roadmap + Blocking Questions

v1.3 adds a real **readiness gate** between repository discovery and implementation.

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
workspace/component + dependency graph
        |
        v
architecture + standards + baseline + policy
        |
        v
material unknowns?
   no /        \ yes
     /          \
 ready       blocking questions
               |
               v
      ask user with options + reasons
               |
               v
      answer -> verified project memory
               |
               v
        regenerate context
               |
               v
      ready_for_implementation
        |
        v
phased docs/ROADMAP.md
        |
        v
spec/design -> implementation -> verification -> handoff
```

The goal is **not** to ask more questions.

The goal is to ask fewer, better questions only when the repository cannot safely answer them.

---

## Discover first, ask second

The bootstrap does not begin with a setup questionnaire.

It first checks:

- runtime/version constraints
- framework/platform evidence
- dependency manifests
- lock files
- source/layout conventions
- template/view files
- workspace/service boundaries
- project memory from previous confirmed sessions
- baseline/reference evidence when available

Only material unknowns become blockers.

### Example: PHP

If `composer.json` already says:

```json
{
  "require": {
    "php": ">=5.6"
  }
}
```

Bootstrap should not ask which PHP syntax floor to use. The compatibility floor is already evidence.

If PHP is detected but no safe runtime constraint exists, it may ask:

```text
Which PHP runtime must this project remain compatible with?

- PHP 5.6 / legacy 5.x
- PHP 7.x
- PHP 8.0-8.1
- PHP 8.2+
- Other / specify exact version
```

The question includes the reason: syntax and standard-library availability differ materially between generations.

### Example: OpenCart

If repository evidence contains an exact version such as:

```php
define('VERSION', '2.3.0.2');
```

Bootstrap should not ask for the OpenCart generation again.

If the structure looks like OpenCart but no reliable version is available, it may ask:

```text
Which OpenCart version/generation is the target?

- OpenCart 2.3.x
- OpenCart 3.x
- OpenCart 4.x
- Other / specify exact version
```

### Example: TPL vs Twig

If `.tpl` files clearly dominate the affected host/project, bootstrap can treat TPL as repository evidence.

If both `.tpl` and `.twig` are present, or neither is available, it can ask:

```text
Which template/view engine applies to the target component?

- TPL / .tpl
- Twig / .twig
- mixed/custom
- no template/UI work required
```

This is a scoped presentation-layer blocker, not a generic preference survey.

The same principle applies to Python, Node and other runtime/framework questions.

---

## Verified answers are remembered

A confirmed answer becomes project-specific memory with provenance.

CLI example:

```bash
python bootstrap.py answer /path/to/project runtime-php-version 5.6 \
  --source "user confirmed in current conversation"
```

This stores the answer under project memory, then regenerates questions, research context, agent instructions and roadmap.

The next bootstrap should not ask the same question again unless stronger contradictory evidence appears and requires re-evaluation.

Manual verified facts are never silently overwritten by auto-discovery.

---

## Detailed development roadmap

Full onboarding now creates:

```text
docs/ROADMAP.md
.ai/planning/roadmap.json
```

The roadmap is not a generic todo list. It includes:

- current intent
- architecture style
- readiness/blocking state
- blocking questions
- execution principles
- phase dependencies
- deliverables for every phase
- exit gates for every phase
- compatibility checkpoints
- verification strategy
- final definition of done

Default phases:

```text
Phase 0  Resolve compatibility/product blockers
Phase 1  Confirm repository truth and architecture
Phase 2  Define product/change contract
Phase 3  Prepare implementation boundaries
Phase 4  Implement feature modules/domain behavior
Phase 5  Integrate interfaces/host lifecycle/external systems
Phase 6  Data/migrations/backward compatibility
Phase 7  Verification/regression
Phase 8  Documentation/packaging/handoff
```

If blockers exist, downstream phases are marked blocked.

For trivial L0/L1 work, the agent can use only the relevant roadmap slice; the system should not create ceremony for a tiny change.

---

## Readiness semantics

Generated machine context includes:

```json
{
  "ready_for_implementation": false,
  "blocking_questions": 2
}
```

`verify` and implementation readiness are intentionally different concepts.

- `verify.ok=true` means the bootstrap context itself is structurally valid.
- `ready_for_implementation=true` means no known material setup blocker remains.

A repository can therefore be correctly onboarded while still waiting for one important user answer.

---

## Architecture default

The bootstrap does **not** default to microservices.

Greenfield preference:

```text
small stable core
        |
        v
explicit feature modules
        |
        v
interfaces (UI/API/CLI/host adapters)
        |
        v
infrastructure adapters
        |
        v
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

---

## Core rule

Core stays small.

Feature/business behavior belongs in explicit modules.

UI/API/CLI/platform entry points belong at the edge.

Database/filesystem/queues/external APIs belong behind infrastructure adapters.

Avoid turning `core`, `shared`, `common`, or `utils` into catch-all folders.

---

## Workspace-aware architecture

Nested manifests are treated as component evidence.

Example:

```text
services/
├── auth/
│   └── package.json
├── orders/
│   └── composer.json
└── notifications/
    └── pyproject.toml
```

These can be preserved as separate workspace components instead of being flattened into one root dependency list.

The bootstrap does not call them microservices merely because they are under `services/`; it preserves observed boundaries and asks for real deployment evidence before creating new network boundaries.

---

## Human onboarding by default

Full `init` / `onboard` establishes:

```text
AGENTS.md

docs/
├── ARCHITECTURE.md
├── DEVELOPMENT.md
├── ROADMAP.md
└── specs/
    ├── README.md
    └── templates/
        └── feature-spec.md
```

Existing user-authored content is preserved outside bootstrap-managed blocks.

The root `AGENTS.md` remains concise and retrieval-friendly.

Do not generate `.codex`, `.claude`, `.cursor`, or other tool-specific project files by default.

---

## Machine-readable project context

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
│
├── discovery/
│   ├── project-facts.json
│   ├── architecture.json
│   ├── dependency-graph.json
│   ├── packs.json
│   └── risks.json
│
├── questions/
│   └── blocking.json
│
├── planning/
│   └── roadmap.json
│
├── standards/
├── research/
├── baseline/
├── knowledge/
├── memory/
├── decisions/
├── changes/
└── verification/
```

---

## Manual CLI

Python 3.9+ is required only to run the bootstrap engine. It does **not** constrain the target project.

Full onboarding:

```bash
python bootstrap.py onboard /path/to/project --intent "short intent"
python bootstrap.py verify /path/to/project
```

`init` is also full onboarding by default:

```bash
python bootstrap.py init /path/to/project
```

Machine harness only:

```bash
python bootstrap.py init /path/to/project --harness-only
```

Read-only preview including architecture, questions and roadmap:

```bash
python bootstrap.py detect /path/to/project --intent "short intent"
```

Answer a blocker and refresh context:

```bash
python bootstrap.py answer /path/to/project <question-id> "<value>" \
  --source "where this was confirmed"
```

Baseline/reference comparison:

```bash
python bootstrap.py baseline /path/to/project --reference /path/to/reference
```

Policy decision:

```bash
python bootstrap.py policy-check /path/to/project write system/library/foo.php
```

Store another verified project fact:

```bash
python bootstrap.py memory-add /path/to/project runtime.production_php 7.4.33 \
  --source "production php -v" --confidence 1
```

---

## Detection and capability packs

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

Unknown stacks still work through generic/catalog capability packs.

Frameworks are capabilities, not global assumptions.

Runtime compatibility is always a target-project fact.

---

## Spec-first boundary

```text
docs/specs/            WHAT observable behavior must do
docs/ARCHITECTURE.md   HOW the system is structured/bounded
docs/ROADMAP.md        WHEN/IN WHAT ORDER work should happen
.ai/changes/...        HOW one non-trivial change will be made
verification/tests     HOW the contract is proved
```

Do not turn product specs into giant technical design documents.

---

## Research policy

Research is selective.

Use version-matched official/primary sources when:

- framework/version behavior is uncertain
- extension mechanisms materially change architecture
- a current standard/tool capability may have changed

Do not apply the latest documentation to a legacy target without matching version evidence.

If web access is unavailable, leave a material fact unresolved rather than guessing.

A user-confirmed version removes the version-discovery blocker but may still create a version-specific architecture research item.

---

## Project memory and trust order

Project memory stores verified project-specific facts with provenance.

Trust order:

1. explicit current user instruction
2. manually verified project fact
3. exact repository evidence
4. matching version-specific baseline/documentation
5. existing project architecture/specification
6. detected capability pack
7. generic bootstrap guidance

The bootstrap exists to reduce repeated prompting, not to override reality.

---

## Policy/security

Instructions are not a sandbox.

`.ai/policy.json` and `policy-check` provide machine-readable `allow / confirm / deny` decisions.

Secret-like values must never be copied into generated specs, prompts, logs, research findings, memory or baseline output.

Treat production writes, destructive commands, migrations and permission/security changes as high risk.

---

## Repository structure

```text
.
├── bootstrap.py
├── engine/
│   ├── discovery.py
│   ├── architecture.py
│   ├── dependencies.py
│   ├── questions.py
│   ├── roadmap.py
│   ├── standards.py
│   ├── research.py
│   ├── baseline.py
│   ├── packs.py
│   ├── policy.py
│   ├── knowledge.py
│   ├── memory.py
│   ├── onboarding.py
│   └── harness.py
├── AUTONOMOUS_BOOTSTRAP.md
├── AGENTS.md
├── docs/
├── knowledge/
├── packs/
├── schemas/
├── skills/
├── templates/
├── prompts/
├── qa/
└── tests/
```

## Design goals

- zero-config by default
- universal rather than framework-bound
- greenfield and brownfield
- legacy-compatible
- applications, services, modules, plugins, extensions, CLIs, desktop tools and pipelines
- discover-first
- ask-only-when-material
- roadmap-first for non-trivial work
- local-first
- evidence-driven
- provenance-aware
- retrieval-friendly
- machine-readable
- composable capability packs
- small stable core
- no premature microservices
- no God files
- no repeated setup questionnaire

## License

MIT
