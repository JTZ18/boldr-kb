---
name: kb-traversal
description: Use when answering or evaluating a customer question against the Boldr KB
---

# KB Traversal

Use this skill to decide whether the KB already answers a question.

## Steps

1. Read `kb/index.md`.
2. Pick the smallest set of likely relevant entries.
3. Read full entries before deciding.
4. Return cited pages and a clear answerability decision.

## Decision Rules

- `can_answer_fully=true` only when the KB directly supports the answer.
- If the KB is partial, report the missing info instead of guessing.
- Prefer active entries. Use stale entries only as context and label them stale.
- Cite file paths for every factual basis.

## Output Notes

Include:

- `pages_read`
- `can_answer_fully`
- `draft_reply` when answerable
- `missing_info` when not answerable
- `themes_detected`
- `persona_hints`

