# Boldr KB

This repository is the agent-first system of record for Boldr knowledge-base
operations.

Agents must follow [AGENTS.md](AGENTS.md), use the repo-local skills under
`.agents/skills`, and run validation before returning results.

## Validation

```bash
python scripts/render_index.py --check
python scripts/validate_kb.py
```

## Layout

- `kb/` - active and stale KB entries.
- `gap-log/` - gap records imported from the control-plane repo.
- `briefs/` - generated brief artifacts.
- `external-intel/` - external sentiment and market-intel artifacts.
- `schemas/` - machine-readable output schemas.
- `scripts/` - validation and inspection tools.

