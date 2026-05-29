---
name: approval-artifacts
description: Use when finishing a Boldr KB agent task or approved apply task
---

# Approval Artifacts

Use this skill before final response.

## Required Checks

Run:

```bash
python scripts/render_index.py --check
python scripts/validate_kb.py
```

## Final JSON

Return exactly one `boldr.agent_result` JSON object in the final response.

Required fields:

- `artifact_type`
- `task_type`
- `status`
- `branch`
- `commit_sha`
- `changed_files`
- `validation`
- `summary`

If validation failed, set `status` to `failed`, include the errors, and do not
claim the work is complete.

