Use https://github.com/kabasik007/spec-first-bootstrap as the bootstrap reference.

This is an existing project. Do not write implementation code yet.

First detect and map the repository. Prefer running:

```bash
python bootstrap.py detect <target>
python bootstrap.py init <target>
```

Then inspect repository evidence and generated `.ai/discovery/` output.

Discover:

- languages and target runtime constraints
- frameworks/platforms and their versions when evidence exists
- project types and system shape
- entry points, routes/APIs, state/data flow
- package/build/test/run commands
- database, migrations, queues, jobs, cron/background workers
- integrations and deployment boundaries
- modules/plugins/extensions and host lifecycle
- framework core/vendor/generated/custom boundaries
- tests, QA and verification surfaces
- security-sensitive and destructive operations

Produce or update:

1. project map
2. architecture/boundary map
3. spec backlog
4. highest-priority first-pass product specs
5. risk zones
6. unknowns/conflicts/assumptions with confidence/evidence

Do not modernize legacy syntax, framework structure, or runtime constraints merely because newer conventions exist. Existing behavior is evidence; verify intent before changing it.
