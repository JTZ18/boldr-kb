#!/usr/bin/env python3
"""Normalize copied KB entry filenames to match frontmatter slugs."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: pip install -r requirements.txt") from exc


ROOT = Path(__file__).resolve().parents[1]
KB_ROOT = ROOT / "kb"


def parse_slug(path: Path) -> str | None:
    text = path.read_text()
    if not text.startswith("---\n"):
        return None
    _, frontmatter, _ = text.split("---\n", 2)
    data = yaml.safe_load(frontmatter) or {}
    slug = data.get("slug")
    return slug if isinstance(slug, str) else None


def main() -> int:
    moved = 0
    for path in sorted(KB_ROOT.rglob("*.md")):
        if path.name.startswith("_") or path.name == "index.md":
            continue
        if any(part.startswith("_") for part in path.relative_to(KB_ROOT).parts[:-1]):
            continue
        slug = parse_slug(path)
        if not slug or path.stem == slug:
            continue
        target = path.with_name(f"{slug}.md")
        if target.exists():
            raise SystemExit(f"cannot rename {path}: target exists: {target}")
        path.rename(target)
        print(f"renamed {path.relative_to(ROOT)} -> {target.relative_to(ROOT)}")
        moved += 1
    print(f"normalized_paths={moved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

