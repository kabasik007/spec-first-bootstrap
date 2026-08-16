Use https://github.com/kabasik007/spec-first-bootstrap as the bootstrap reference.

This is a new or mostly empty project.

Do not choose a framework or architecture merely because the bootstrap has a pack for it. First establish the product requirements and intended deployment/runtime constraints.

Set up a lightweight universal spec-first workflow:

1. define the product goal and primary system type
2. record explicit runtime/platform constraints
3. select only the capability packs that match the chosen stack
4. initialize `.ai/` project, architecture, commands, rules, changes and verification layers
5. create the initial product-spec structure
6. propose the first product areas that require specs before implementation
7. identify architectural decisions that should be recorded separately from product specs
8. recommend the smallest first vertical slice and its verification strategy

Keep the system composable. Do not make one framework, language, database, UI type, or deployment model a global assumption.
