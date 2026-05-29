#!/usr/bin/env python3
"""Print a compact KB inventory for agent planning."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: pip install -r requirements.txt") from exc


ROOT = Path(__file__).resolve().parents[1]
KB_ROOT = ROOT / "kb"


def main() -> int:
    domains: Counter[str] = Counter()
    statuses: Counter[str] = Counter()
    themes: Counter[str] = Counter()

    for path in KB_ROOT.rglob("*.md"):
        if path.name.startswith("_") or path.name == "index.md":
            continue
        if any(part.startswith("_") for part in path.relative_to(KB_ROOT).parts[:-1]):
            continue
        text = path.read_text()
        if not text.startswith("---\n"):
            continue
        _, frontmatter, _ = text.split("---\n", 2)
        data = yaml.safe_load(frontmatter) or {}
        domains[str(data.get("domain", "unknown"))] += 1
        statuses[str(data.get("status", "unknown"))] += 1
        themes.update(str(theme) for theme in data.get("themes", []))

    print("Domains:")
    for key, count in domains.most_common():
        print(f"- {key}: {count}")
    print("\nStatuses:")
    for key, count in statuses.most_common():
        print(f"- {key}: {count}")
    print("\nTop themes:")
    for key, count in themes.most_common(20):
        print(f"- {key}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
