#!/usr/bin/env python3
"""Validate Boldr KB markdown entries and agent fixtures."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: pip install -r requirements.txt") from exc


ROOT = Path(__file__).resolve().parents[1]
KB_ROOT = ROOT / "kb"
ALLOWED_DOMAINS = {"spec", "pricing", "policy", "faq", "persona"}
ALLOWED_STATUS = {"active", "stale", "draft"}
REQUIRED_FIELDS = {
    "slug",
    "title",
    "domain",
    "themes",
    "sources",
    "last_verified",
    "supersedes",
    "status",
}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_entry(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("malformed YAML frontmatter block")
    data = yaml.safe_load(parts[1]) or {}
    body = parts[2].strip()
    return data, body


def validate_date(value: Any) -> bool:
    if isinstance(value, date):
        return True
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate_agent_fixture(errors: list[str]) -> None:
    fixture = ROOT / "tests" / "fixtures" / "sample_agent_result.json"
    if not fixture.exists():
        errors.append("tests/fixtures/sample_agent_result.json is missing")
        return
    data = json.loads(fixture.read_text())
    if data.get("artifact_type") != "boldr.agent_result":
        errors.append("sample_agent_result.json must use artifact_type=boldr.agent_result")
    validation = data.get("validation")
    if not isinstance(validation, dict) or "status" not in validation:
        errors.append("sample_agent_result.json must include validation.status")


def main() -> int:
    errors: list[str] = []
    active_slugs: dict[str, Path] = {}

    for path in sorted(KB_ROOT.rglob("*.md")):
        if path.name.startswith("_") or path.name == "index.md":
            continue
        if any(part.startswith("_") for part in path.relative_to(KB_ROOT).parts[:-1]):
            continue
        rel = path.relative_to(ROOT)
        try:
            data, body = parse_entry(path)
        except Exception as exc:
            errors.append(f"{rel}: {exc}")
            continue

        missing = REQUIRED_FIELDS - set(data)
        if missing:
            errors.append(f"{rel}: missing required fields {sorted(missing)}")

        slug = data.get("slug")
        if not isinstance(slug, str) or not SLUG_RE.match(slug):
            errors.append(f"{rel}: invalid slug {slug!r}")
        elif path.stem != slug:
            errors.append(f"{rel}: filename stem must match slug {slug!r}")

        domain = data.get("domain")
        if domain not in ALLOWED_DOMAINS:
            errors.append(f"{rel}: invalid domain {domain!r}")

        status = data.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{rel}: invalid status {status!r}")

        for field in ("themes", "sources", "supersedes"):
            if not isinstance(data.get(field), list):
                errors.append(f"{rel}: {field} must be a list")

        if not validate_date(data.get("last_verified")):
            errors.append(f"{rel}: last_verified must be an ISO date")

        if not body:
            errors.append(f"{rel}: body must not be empty")

        if status == "active" and isinstance(slug, str):
            if slug in active_slugs:
                other = active_slugs[slug].relative_to(ROOT)
                errors.append(f"{rel}: duplicate active slug also found at {other}")
            active_slugs[slug] = path

    validate_agent_fixture(errors)

    if errors:
        print("KB validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"KB validation passed: {len(active_slugs)} active entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
