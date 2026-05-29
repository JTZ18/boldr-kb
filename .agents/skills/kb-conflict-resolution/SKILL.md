---
name: kb-conflict-resolution
description: Use when comparing Boldr KB entries for contradictions, duplicates, or stale facts
---

# KB Conflict Resolution

Use this skill to make KB consistency changes.

## Steps

1. Inspect `kb/index.md` and the candidate entries.
2. Identify exact contradictory claims with file paths.
3. Choose one canonical active entry when evidence supports it.
4. Mark superseded entries as `status: stale`; never delete them.
5. Add `supersedes` links on the canonical entry when useful.
6. Render and validate the index.

## Rules

- Do not resolve conflicts by inventing new facts.
- If evidence is insufficient, return `needs_review`.
- Preserve old entries for auditability.
- Keep summaries short and cite changed files.

