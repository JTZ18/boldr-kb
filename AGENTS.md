# AGENTS.md

This repo is operated by managed agents. Treat these instructions as binding.

## Source Of Truth

- This repository is the system of record for Boldr KB content.
- Read `kb/index.md` before choosing files to inspect.
- Use `.agents/skills/*/SKILL.md` for task-specific operating procedures.

## Git Policy

- Never push directly to `main` except during an explicit approved apply task.
- For normal work, create `agent/{task_type}/{short_id}` from `main`.
- Commit only related KB changes and generated index updates.
- Approved apply tasks may merge the prepared branch directly into `main`.

## Editing Rules

- Never invent facts not present in the task payload, the KB, or cited sources.
- Never delete stale entries; mark `status: stale`.
- Keep `slug` equal to the filename stem.
- Preserve YAML frontmatter fields required by `schemas/kb_entry.schema.json`.
- Add citations in `sources` for every new or changed factual claim.

## Required Checks

Run both commands before final response:

```bash
python scripts/render_index.py --check
python scripts/validate_kb.py
```

If either command fails, stop and report the validation failure.

## Final Artifact

Every completed task must return one JSON object with:

```json
{
  "artifact_type": "boldr.agent_result",
  "task_type": "kb-drafting",
  "status": "succeeded",
  "branch": "agent/kb-drafting/example",
  "commit_sha": "abc123",
  "changed_files": ["kb/faqs/example.md", "kb/index.md"],
  "validation": {"status": "passed", "commands": []},
  "summary": "Short human summary"
}
```

