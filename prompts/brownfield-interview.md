Use https://github.com/kabasik007/spec-first-bootstrap as the bootstrap reference.

This is an existing project with incomplete or unreliable documentation.

First inspect the repository and generated `.ai/discovery/` facts. Identify the main product areas, architecture boundaries, runtime constraints, extension/platform constraints, and places where evidence is weak or contradictory.

Then prepare a structured clarification pass for the user or team focused on:

- intended behavior
- edge cases and failure policy
- business rules and known exceptions
- runtime/platform compatibility requirements
- data ownership, integrations, permissions and lifecycle constraints
- places where current code may not reflect intended product behavior
- places where discovery confidence is low

After that, recommend:

1. which product specs should be created first
2. which technical decisions need design/ADR work separately
3. which risky areas need stronger verification before changes
4. which areas can wait

Do not implement anything yet, and do not silently modernize legacy code while clarifying intent.
