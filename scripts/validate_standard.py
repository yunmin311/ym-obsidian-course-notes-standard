#!/usr/bin/env python3
"""Validate release/version consistency for the course-notes standard repo."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ACTIVE_FILES = [
    "README.md",
    "SKILL.md",
    "SOP_WEEKLY_CONTINUATION.md",
    "HANDOFF_PROMPTS.md",
    "TEMPLATE.md",
    "COURSE_STATE_TEMPLATE.yaml",
]

REQUIRED_STANDARD_MARKERS = [
    "Visual Source Hierarchy",
    "Level 1 — 当前课程原始材料",
    "Level 2 — 可信外部原图",
    "Level 3 — 静态 SVG / 可控重绘",
    "Level 4 — Manual Capture Required",
    "Visual QA Gate",
    "最多两次合理裁切尝试",
    "Adaptive sizing",
    "Pre-delivery Visual Audit",
]


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    version_file = root / "VERSION"
    if not version_file.exists():
        return ["VERSION file is missing"]

    version = version_file.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        return [f"VERSION must be semantic x.y.z, got {version!r}"]

    major, minor, _patch = version.split(".")
    short = f"{major}.{minor}"
    canonical_name = f"Obsidian_Course_Notes_Standard_v{short}.md"
    canonical = root / canonical_name

    if not canonical.exists():
        errors.append(f"canonical standard missing: {canonical_name}")
    else:
        canonical_text = canonical.read_text(encoding="utf-8")
        missing = [marker for marker in REQUIRED_STANDARD_MARKERS if marker not in canonical_text]
        if missing:
            errors.append("canonical standard missing v3 visual markers: " + "; ".join(missing))

    stale_canonicals = [
        path
        for path in sorted(root.glob("Obsidian_Course_Notes_Standard_v*.md"))
        if path.name != canonical_name
    ]
    if stale_canonicals:
        errors.append("stale canonical files present: " + ", ".join(path.name for path in stale_canonicals))

    readme = root / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        if f"v{version}" not in text:
            errors.append(f"README.md does not advertise v{version}")
        if canonical_name not in text:
            errors.append(f"README.md does not reference {canonical_name}")
    else:
        errors.append("README.md is missing")

    state = root / "COURSE_STATE_TEMPLATE.yaml"
    if state.exists():
        text = state.read_text(encoding="utf-8")
        if f'standard_version: "{short}"' not in text:
            errors.append(f"COURSE_STATE_TEMPLATE.yaml must use standard_version {short}")
    else:
        errors.append("COURSE_STATE_TEMPLATE.yaml is missing")

    stale_patterns = [r"\bv2\.1(?:\.0)?\b", r"\bv2\.2(?:\.0)?\b", r'"2\.1"', r'"2\.2"']
    active_paths = [canonical] + [root / name for name in ACTIVE_FILES]
    for path in active_paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in stale_patterns:
            if re.search(pattern, text):
                errors.append(f"stale active version reference {pattern!r} in {path.name}")

    skill = root / "SKILL.md"
    if skill.exists():
        skill_text = skill.read_text(encoding="utf-8")
        for marker in ["可信教材或官方外部原图", "最多两次合理 recrop", "Visual QA Gate"]:
            if marker not in skill_text:
                errors.append(f"SKILL.md missing execution marker: {marker}")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    short = ".".join(version.split(".")[:2])
    print(f"OK: repository is consistent with v{version} (Obsidian_Course_Notes_Standard_v{short}.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
