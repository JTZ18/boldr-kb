---
name: kb-drafting
description: Use when turning a resolved knowledge gap into a Boldr KB markdown entry
---

# KB Drafting

Use this skill when a human-provided resolution should become a KB entry.

## Steps

1. Read the gap payload and source note.
2. Search `kb/index.md` for existing entries that overlap.
3. If an active entry already covers the fact, update it instead of creating a duplicate.
4. Write or update one markdown entry with valid frontmatter.
5. Run `python scripts/render_index.py`.
6. Run `python scripts/render_index.py --check` and `python scripts/validate_kb.py`.

## Entry Rules

- `slug` must match the filename stem.
- `domain` must be one of `spec`, `pricing`, `policy`, `faq`, `persona`.
- `sources` must include the gap ID and any provided source note.
- If the resolution is incomplete, prefix uncertain body text with `[NEEDS REVIEW]`.
- Do not fabricate operational details, pricing, policies, dates, or product specs.

