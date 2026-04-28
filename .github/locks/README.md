# Locks

Use this folder to reserve shared/danger files for a short-lived task.

Common locked files:

- `index.html`
- `data.json`
- `Dockerfile`
- `AGENTS.md`
- `.github/workflows/*`

Lock file example:

```text
Agent: Alpha
File: index.html
Since: 2026-04-28T00:00:00Z
Reason: Projects tab sort/filter UI patch
```

Do not leave stale locks after merge.
