#!/usr/bin/env python3
"""Check a delivered course folder against the v3.1 structure & naming rules.

This validates a COURSE (not the standard repo itself). It implements the rule
table in canonical standard section 2.7 so the delivery structure stops being a
matter of interpretation.

Usage:
    python scripts/check_course_structure.py <course_dir>
    python scripts/check_course_structure.py --self-test

Exit code 0 = no FAIL (WARNs are printed but do not block delivery).
Exit code 1 = at least one FAIL.
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

# The closed unit_scheme enum -> directory prefix map (standard 2.4).
UNIT_SCHEME_PREFIX = {
    "week": "Week",
    "lecture": "Lecture",
    "module": "Module",
    "chapter": "Chapter",
    "unit": "Unit",
}

# TypeLabel -> SrcID derivation table (standard 2.4, section 2).
TYPE_TO_SRC = {
    "Lecture": "L",
    "Tutorial": "T",
    "Lab": "LAB",
    "Recitation": "R",
}

UNIT_DIR_RE = re.compile(r"^(?P<prefix>[A-Za-z]+?)(?P<num>\d+)$")
NOTE_RE = re.compile(
    r"^(?P<type>" + "|".join(TYPE_TO_SRC) + r") (?P<num>\d{2,3}) - (?:.+)\.md$"
)
# {SrcID}-p{NN}-{slug}.{ext}   or   {SrcID}-{slug}.{ext} for self-made SVG.
ASSET_WITH_PAGE_RE = re.compile(
    r"^(?P<src>" + "|".join(TYPE_TO_SRC.values()) + r")(?P<num>\d{2,3})-p\d{2,3}-[a-z0-9][a-z0-9-]*\.[a-z0-9]+$"
)
ASSET_NO_PAGE_RE = re.compile(
    r"^(?P<src>" + "|".join(TYPE_TO_SRC.values()) + r")(?P<num>\d{2,3})-[a-z0-9][a-z0-9-]*\.[a-z0-9]+$"
)
# Legacy sequential naming, e.g. 01-campus-access-path.png (standard 2.4.2).
SEQUENTIAL_RE = re.compile(r"^\d{2,3}-[a-z0-9][a-z0-9-]*\.[a-z0-9]+$")


def parse_state(course_dir: Path) -> tuple[str, str, dict[str, str]]:
    """Return (course_code, unit_prefix, scalar_fields) read without a YAML dep.

    Keys are matched with optional leading indentation so nested keys such as
    `structure.unit_scheme` are read the same way as top-level ones. A tiny
    hand-rolled reader keeps this script dependency-free, which matters because
    it has to run on any machine in CI without installing PyYAML.
    """
    state = course_dir / "COURSE_STATE.yaml"
    text = state.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    for key in ("course_code", "unit_scheme", "unit_prefix", "standard_version"):
        match = re.search(rf"^[ \t]*{key}\s*:\s*(.*)$", text, re.MULTILINE)
        if match:
            fields[key] = match.group(1).strip().strip('"').strip("'")

    scheme = fields.get("unit_scheme", "")
    if scheme == "custom":
        prefix = fields.get("unit_prefix", "")
    else:
        prefix = UNIT_SCHEME_PREFIX.get(scheme, "")
    return fields.get("course_code", ""), prefix, fields


def check(course_dir: Path) -> tuple[list[str], list[str]]:
    fails: list[str] = []
    warns: list[str] = []

    if not course_dir.is_dir():
        return [f"course directory not found: {course_dir}"], []
    if not (course_dir / "COURSE_STATE.yaml").exists():
        return [f"R2: COURSE_STATE.yaml missing in {course_dir}"], []

    course_code, expected_prefix, fields = parse_state(course_dir)
    scheme = fields.get("unit_scheme", "")

    # R1 is intentionally not checked: README.md is deferred (standard 2.2).

    if course_dir.name != course_code:
        fails.append(
            f"course root directory name {course_dir.name!r} != course_code {course_code!r}"
        )
    if not expected_prefix:
        fails.append(
            f"unit_scheme {scheme!r} is not a legal enum value or unit_prefix is unset"
        )
        return fails, warns

    unit_dirs = sorted(p for p in course_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
    if not unit_dirs:
        fails.append("no unit directories found")
        return fails, warns

    seen_prefixes: set[str] = set()
    type_numbers: dict[str, str] = {}

    for unit in unit_dirs:
        match = UNIT_DIR_RE.match(unit.name)
        if not match:
            fails.append(f"U1: unit directory {unit.name!r} does not match {{Prefix}}{{NN}}")
            continue
        prefix, num = match.group("prefix"), match.group("num")
        seen_prefixes.add(prefix)

        if prefix != expected_prefix:
            fails.append(
                f"U1: unit {unit.name!r} prefix {prefix!r} != unit_scheme-derived "
                f"{expected_prefix!r} (unit_scheme: {scheme})"
            )
        if len(num) != 2:
            fails.append(f"U4: unit {unit.name!r} number must be zero-padded to 2 digits")

        notes = sorted(p for p in unit.iterdir() if p.is_file() and p.suffix == ".md")
        if not notes:
            fails.append(f"N1: unit {unit.name!r} has no .md file")

        note_srcs: set[str] = set()
        for note in notes:
            nm = NOTE_RE.match(note.name)
            if not nm:
                fails.append(
                    f"N2: note {unit.name}/{note.name!r} does not match "
                    "'{TypeLabel} {NN} - {Title}.md'"
                )
                continue
            ntype, nnum = nm.group("type"), nm.group("num")
            src = f"{TYPE_TO_SRC[ntype]}{nnum}"
            note_srcs.add(src)
            if src in type_numbers:
                fails.append(
                    f"N2: {src} used by both {type_numbers[src]!r} and "
                    f"{unit.name + '/' + note.name!r}"
                )
            else:
                type_numbers[src] = f"{unit.name}/{note.name}"

        # --- assets -------------------------------------------------------
        assets_dir = unit / "assets"
        referenced: set[str] = set()
        for note in notes:
            body = note.read_text(encoding="utf-8")
            # Obsidian wiki embed: ![[assets/name.png]] or ![[assets/name.png|760]]
            # The trailing `|width` / `#heading` display options are not part of
            # the filename, so they must be stripped before comparing.
            for raw in re.findall(r"!?\[\[([^\]\n]+?)\]\]", body):
                target = raw.split("|", 1)[0].split("#", 1)[0].strip()
                if target.startswith("assets/"):
                    referenced.add(target[len("assets/"):])
            # Markdown image: ![alt](assets/name.png)
            referenced.update(re.findall(r"!\[[^\]]*\]\(assets/([^)\s]+)", body))

        if assets_dir.is_dir():
            for asset in sorted(p for p in assets_dir.iterdir() if p.is_file()):
                if ASSET_WITH_PAGE_RE.match(asset.name) or ASSET_NO_PAGE_RE.match(asset.name):
                    pass
                elif SEQUENTIAL_RE.match(asset.name):
                    warns.append(
                        f"A1: {unit.name}/assets/{asset.name!r} uses legacy sequential "
                        "numbering (needs {SrcID}-p{NN}-{slug}); migrate with the sources/ backfill"
                    )
                else:
                    fails.append(
                        f"A1: {unit.name}/assets/{asset.name!r} does not match "
                        "{SrcID}-p{NN}-{slug}.{ext} or {SrcID}-{slug}.{ext}"
                    )

                am = ASSET_WITH_PAGE_RE.match(asset.name) or ASSET_NO_PAGE_RE.match(asset.name)
                if am:
                    key = f"{am.group('src')}{am.group('num')}"
                    if key not in note_srcs:
                        fails.append(
                            f"A2: {unit.name}/assets/{asset.name!r} has no matching note "
                            f"({key} not in this unit)"
                        )
                    elif referenced and asset.name not in referenced:
                        warns.append(f"A3: {unit.name}/assets/{asset.name!r} is never referenced")
                elif referenced and asset.name not in referenced:
                    warns.append(f"A3: {unit.name}/assets/{asset.name!r} is never referenced")

        # --- sources ------------------------------------------------------
        sources_dir = unit / "sources"
        if not sources_dir.is_dir():
            fails.append(f"S1: unit {unit.name!r} has no sources/ directory (mandatory)")
            continue
        for src_file in sorted(p for p in sources_dir.iterdir() if p.is_file()):
            sm = re.match(
                rf"^{re.escape(course_code)}_(?P<src>"
                + "|".join(TYPE_TO_SRC.values())
                + r")(?P<num>\d{2,3})_",
                src_file.name,
            )
            if not sm:
                warns.append(
                    f"S2: {unit.name}/sources/{src_file.name!r} does not match "
                    f"{{COURSE_CODE}}_{{SrcID}}_{{Slug}}.ext ({course_code}_L01_Topic.pdf)"
                )
                continue
            key = f"{sm.group('src')}{sm.group('num')}"
            if key not in note_srcs:
                fails.append(
                    f"S3: {unit.name}/sources/{src_file.name!r} has no matching note ({key})"
                )

    if len(seen_prefixes) > 1:
        fails.append(
            "U2: mixed unit prefixes in one course: "
            + ", ".join(sorted(seen_prefixes))
            + " (unit_scheme must be a single value)"
        )

    return fails, warns


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        return self_test()
    if len(sys.argv) != 2:
        print(__doc__)
        return 2

    course_dir = Path(sys.argv[1]).resolve()
    fails, warns = check(course_dir)

    for warn in warns:
        print(f"WARN: {warn}")
    for fail in fails:
        print(f"FAIL: {fail}")

    if fails:
        print(f"\n{len(fails)} FAIL, {len(warns)} WARN — structure is not compliant")
        return 1

    print(f"\nOK: structure compliant ({len(warns)} WARN)")
    return 0


def _build_fixture(root: Path, scheme_line: str = "  unit_scheme: week\n") -> Path:
    course = root / "PRB101"
    (course / "Week01" / "assets").mkdir(parents=True)
    (course / "Week01" / "sources").mkdir(parents=True)
    (course / "COURSE_STATE.yaml").write_text(
        "schema: obsidian-course-state/v1\n"
        "course_code: PRB101\n"
        'standard_version: "3.1"\n'
        "structure:\n" + scheme_line + "  current_unit: 1\n",
        encoding="utf-8",
    )
    (course / "Week01" / "Lecture 01 - Test.md").write_text(
        "![[assets/L01-p10-good.png|760]]\n", encoding="utf-8"
    )
    for name in (
        "L01-p10-good.png",        # referenced, correctly named -> silent
        "L01-p11-extra.png",       # has a note but unreferenced  -> A3
        "L09-p10-orphan.png",      # no matching note            -> A2
        "05-sequential-legacy.png",  # legacy sequential naming  -> A1 + A3
    ):
        (course / "Week01" / "assets" / name).write_bytes(b"x")
    for name in ("PRB101_L01_Topic.pdf", "PRB101_L09_Ghost.pdf"):
        (course / "Week01" / "sources" / name).write_bytes(b"x")
    return course


def self_test() -> int:
    """Prove every rule fires. Run in CI so the checker cannot rot silently.

    These fixtures assert the *fail* paths on purpose: a checker that only ever
    passes is worse than no checker, because it launders non-compliant
    deliveries as green.
    """
    checks: list[tuple[str, bool]] = []
    with tempfile.TemporaryDirectory() as tmp:
        course = _build_fixture(Path(tmp))
        fails, warns = check(course)
        joined = "\n".join(fails)

        checks.append(("A2 fires on orphan asset", any("A2:" in f for f in fails)))
        checks.append(("S3 fires on orphan source", any("S3:" in f for f in fails)))
        checks.append(
            ("A1 warns on sequential numbering", any("A1:" in w for w in warns))
        )
        checks.append(
            ("A3 warns on unreferenced asset", any("A3:" in w for w in warns))
        )
        checks.append(
            ("A3 suppressed when asset has no note (A2 owns it)", "L09-p10-orphan" not in "\n".join(w for w in warns if "A3:" in w))
        )
        checks.append(("no U-prefix false positive on legal layout", "U1:" not in joined))

        # unit_scheme drift: a Module-directory course declared as week must FAIL.
        (course / "Module02").mkdir()
        (course / "Module02" / "Lecture 02 - Other.md").write_text("x", encoding="utf-8")
        (course / "Module02" / "sources").mkdir()
        drift_fails, drift_warns = check(course)
        checks.append(
            ("U1/U2 fire on mixed prefixes", any("U1:" in f for f in drift_fails))
        )

        # Missing sources/ is a FAIL, never a warning.
        (course / "Module02" / "sources").rmdir()
        missing_fails, _ = check(course)
        checks.append(
            ("S1 fires when sources/ missing", any("S1:" in f for f in missing_fails))
        )

    failures = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    if failures:
        print(f"\nself-test failed: {len(failures)} check(s)")
        return 1
    print(f"\nself-test OK ({len(checks)} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
