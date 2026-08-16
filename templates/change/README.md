# Change Lifecycle

Use `.ai/changes/<change-id>/` for non-trivial work.

Recommended artifacts:

```text
proposal.md      why this change exists
spec.md          user-visible/product contract delta
design.md        technical approach and boundaries
tasks.md         implementation slices
verification.md  evidence and checks
result.md        what actually changed
```

Do not require every file for every task.

## Complexity levels

- **L0 — trivial:** implementation + focused verification
- **L1 — small fix:** short plan + implementation + verification
- **L2 — feature:** spec + plan + implementation + verification
- **L3 — architectural:** spec + design/ADR + plan + tests + verification
- **L4 — migration/security/critical:** impact analysis + rollback + migration/security plan + staged verification

The purpose is to scale rigor with risk, not to create paperwork.
