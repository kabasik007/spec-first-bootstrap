Using the current project and `.ai/discovery/` as evidence, generate first-pass product specs for the highest-priority product areas.

Use https://github.com/kabasik007/spec-first-bootstrap as the reference.

Each product spec should include:

- Goal
- Scope
- Non-goals
- User-visible behavior
- Invariants
- Edge cases and failure policy
- Route / state / data implications when they are part of the product contract
- Verification mapping
- Unknowns requiring confirmation

Keep product specs short, explicit, and behavior-oriented.

Do **not** turn them into technical design documents. Put implementation architecture, module boundaries, migrations, rollout/rollback, dependency decisions, and internal APIs in `.ai/ARCHITECTURE.md` or the active `.ai/changes/<id>/design.md`.

When existing behavior and desired behavior conflict, record the conflict instead of silently choosing one.
