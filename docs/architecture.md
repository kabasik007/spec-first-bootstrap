# Bootstrap Architecture

## Purpose

Universal AI Development Bootstrap prepares arbitrary software repositories for safer AI-assisted development without binding the workflow to one language, framework, runtime generation or product type.

The design keeps six concerns separate:

```text
product contract       docs/specs/
technical context      .ai/ARCHITECTURE.md + discovery
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
   │    dependency-manifest graph
   │
   ├─ engine/baseline.py
   │    inventory + optional reference diff
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
   └─ engine/harness.py
        orchestration + generated .ai artifacts
```

The engine uses only the Python standard library. Python is the bootstrap runtime, not a constraint on target repositories.

## Evidence first

Detectors record facts with confidence and evidence. Detected facts are hypotheses until project evidence confirms them.

A target can be legacy by design. A modern bootstrap must not force a legacy target onto modern syntax, framework conventions or dependencies.

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

Pack inheritance (`extends`) is resolved before rules, protected paths, verification, knowledge and policy fragments are merged.

Catalog-only packs are allowed so unknown or lightly modeled stacks still bootstrap successfully. Detailed manifests can be added incrementally.

## Local-first baseline

Baseline comparison accepts an explicit local reference tree. The core engine does not automatically fetch upstream releases because version identity is a correctness boundary.

Network-enabled official baseline/document adapters can be added later as explicit capabilities.

## Security model

The bootstrap never claims that Markdown instructions are a security boundary.

`.ai/policy.json` is machine-readable. `policy-check` provides an enforceable decision primitive that external agent hosts can call. Full OS/container sandboxing remains outside this repository.

Secret-like files are skipped by baseline inventory and should never be copied into generated context.

## Compatibility

The CLI preserves v1.0 top-level discovery keys while adding v1.1 context fields.

Generated manifest schema version is `2`.

## Extension points

Future layers can add:

- source/import call graphs
- database/schema graph
- official baseline fetch adapters
- official-document knowledge adapters
- pack signing/version compatibility
- host-level policy enforcement
- IDE/Codex/Claude skill adapters
- incremental discovery cache
- monorepo workspace graphs
