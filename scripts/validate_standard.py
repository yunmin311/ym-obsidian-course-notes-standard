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

# v3.1 replaced the descriptive delivery-structure section with hard, mechanically
# checkable naming rules. These markers prove the section is present and complete;
# without them a future edit could quietly drop the unit_scheme enum or the
# sources/ mandate while every other gate still passes.
REQUIRED_STRUCTURE_MARKERS = [
    "四段派生模型",
    "unit_scheme",
    "TypeLabel 枚举与 SrcID 派生表",
    "sources 目录规则（强制）",
    "无法确定页码时的处理",
    "结构校验规则",
]

# The closed unit_scheme enum -> directory prefix map (standard 2.4).
UNIT_SCHEME_PREFIX = {
    "week": "Week",
    "lecture": "Lecture",
    "module": "Module",
    "chapter": "Chapter",
    "unit": "Unit",
}

# Tokens that unambiguously mean "the standard's version".
#
# Deliberately NOT a bare `\d+\.\d+` scan: active files legitimately mention
# unrelated versions (tool versions, GitHub Action tags, external citations),
# and a naked number scan would turn every future upgrade into a false alarm.
# These three families are the ones the standard itself uses to refer to its
# own version, so a wrong value in any of them is always a real defect:
#   1. the versioned canonical filename — Obsidian_Course_Notes_Standard_vX.Y.md
#   2. the Course State version key       — standard_version: "X.Y"
#   3. the `v`-prefixed version token     — vX.Y / vX.Y.Z
ACTIVE_VERSION_PATTERNS = (
    r"Obsidian_Course_Notes_Standard_v(?P<ver>\d+\.\d+(?:\.\d+)?)\.md",
    r"standard_version\s*:\s*[\"']?(?P<ver>\d+\.\d+(?:\.\d+)?)",
    r"\bv(?P<ver>\d+\.\d+(?:\.\d+)?)\b",
)

# NOTE: CHANGELOG.md is intentionally absent from ACTIVE_FILES — it is a record
# of superseded versions and must stay free to mention v2.x / v3.0 forever.
# (The historical docs/superpowers/** specs and plans were deleted on 2026-09-17:
# finished work products, referenced by nothing, pure upkeep cost.)


def active_version_tokens(text: str) -> set[str]:
    """Return every version token that refers to the standard itself."""
    tokens: set[str] = set()
    for pattern in ACTIVE_VERSION_PATTERNS:
        tokens.update(match.group("ver") for match in re.finditer(pattern, text))
    return tokens


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
        missing_structure = [
            marker for marker in REQUIRED_STRUCTURE_MARKERS if marker not in canonical_text
        ]
        if missing_structure:
            errors.append(
                "canonical standard missing v3.1 structure markers: "
                + "; ".join(missing_structure)
            )
        # The unit_scheme enum is the single variable of the naming system; if it
        # drifts out of the closed set the whole delivery-structure contract
        # becomes unverifiable, so pin every legal value explicitly.
        for scheme in list(UNIT_SCHEME_PREFIX) + ["custom"]:
            if f"`{scheme}`" not in canonical_text:
                errors.append(f"canonical standard does not define unit_scheme `{scheme}`")

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
        # `unit_scheme` is the only variable of the naming system, so the template
        # must always expose it; `unit_prefix` only matters for the custom scheme.
        for key in ("unit_scheme:", "unit_prefix:"):
            if key not in text:
                errors.append(f"COURSE_STATE_TEMPLATE.yaml must declare {key}")
    else:
        errors.append("COURSE_STATE_TEMPLATE.yaml is missing")

    # Version legitimacy is derived from VERSION, not hardcoded, so the gate
    # keeps working after the next upgrade without touching this file.
    # Only the current full (x.y.z) and short (x.y) forms are legal; anything
    # else — an older release that was left behind, or a newer one referenced
    # before VERSION was bumped — is drift.
    allowed_versions = {short, version}
    active_paths = [canonical] + [root / name for name in ACTIVE_FILES]
    for path in active_paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        stale = sorted(token for token in active_version_tokens(text) if token not in allowed_versions)
        if stale:
            rendered = ", ".join(f"v{token}" for token in stale)
            errors.append(
                f"stale active version reference {rendered} in {path.name} "
                f"(VERSION is {version}; expected v{short} or v{version})"
            )

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
