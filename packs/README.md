# Capability Packs

Packs describe stack-specific knowledge without hard-coding a framework or language into the bootstrap workflow.

The engine detects facts first, then resolves packs such as:

```text
base/spec-first
base/architecture
languages/php
frameworks/opencart
project-types/extension-platform
verification/extension
```

A target can select many packs. A React + FastAPI + PostgreSQL repository is a composition, not one project type.

## Pack rules

- Packs augment universal rules; they do not replace them.
- Language versions are detected target facts, not bootstrap runtime requirements.
- Framework packs should prefer official extension mechanisms and compatibility rules.
- No pack may assume it is the only technology in the repository.
- Unknown stacks must still work through the generic base packs.
- Detection evidence and confidence should be preserved.

## Pack manifest

See `schemas/pack.schema.json`. A pack can provide:

- detection hints
- compatibility notes
- architecture boundaries
- protected paths
- command hints
- verification requirements
- knowledge-source policy

The initial engine resolves pack identifiers even when a detailed pack manifest does not yet exist. This makes the system forward-compatible: adding a richer pack later does not require redesigning the detector.
