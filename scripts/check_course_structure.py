#!/usr/bin/env python3
"""Check a delivered course folder against the v3.1 structure & naming rules.

Implements the rule table in canonical standard section 2.7, so the delivery
structure stops being a matter of interpretation.

    python scripts/check_course_structure.py <course_dir>

Exit 0 = no FAIL (WARNs print but do not block delivery).
Exit 1 = at least one FAIL.

Zero dependencies on purpose: no PyYAML, no pip install, runs anywhere.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

VERSION = "3.1"

UNIT_SCHEME_PREFIX = {
    "week": "Week",
    "lecture": "Lecture",
    "module": "Module",
    "chapter": "Chapter",
    "unit": "Unit",
    "custom": "",  # prefix comes from unit_prefix instead
}
TYPE_TO_SRC = {"Lecture": "L", "Tutorial": "T", "Lab": "LAB", "Recitation": "R"}

UNIT_DIR_RE = re.compile(r"^(?P<prefix>[A-Za-z]+)(?P<num>\d+)$")
NOTE_RE = re.compile(r"^(?P<type>[A-Za-z]+) (?P<num>\d{2,3}) - .+\.md$")

# {SrcID}-p{NN}-{slug}.ext   and   {SrcID}-{slug}.ext (hand-authored SVG, 2.4.1)
ASSET_WITH_PAGE_RE = re.compile(
    r"^(?P<src>L|T|LAB|R)(?P<num>\d{2,3})-p\d{2,3}-[a-z0-9][a-z0-9-]*\.[a-z0-9]+$"
)
ASSET_NO_PAGE_RE = re.compile(
    r"^(?P<src>L|T|LAB|R)(?P<num>\d{2,3})-[a-z0-9][a-z0-9-]*\.[a-z0-9]+$"
)
SEQUENTIAL_RE = re.compile(r"^\d{2,3}-[a-z0-9][a-z0-9-]*\.[a-z0-9]+$")

# Every syntax a note may use to point at an asset. All three appear in real
# deliveries, so all three must be parsed -- a syntax the checker cannot read is
# indistinguishable from "asset never referenced", which silently disables A3.
RE_WIKI_EMBED = re.compile(r"!?\[\[([^\]\n]+?)\]\]")
RE_MD_IMAGE = re.compile(r"!\[[^\]]*\]\(assets/([^)\s]+)")
RE_HTML_IMAGE = re.compile(r"""<img\b[^>]*?\bsrc\s*=\s*["']assets/([^"'\s>]+)""")


def collect_refs(body: str) -> set[str]:
    """Return the bare filenames under assets/ that `body` references.

    Handles, in order:
      1. Obsidian wiki embed  ![[assets/name.png]] / ![[assets/name.png|760]]
      2. Markdown image       ![alt](assets/name.png)
      3. Raw HTML image       <img src="assets/name.png" width="760">

    Form 3 matters: CSI201/Week02, EEE211/Week01 and SOE205/Week02 set a
    per-figure width that Markdown cannot express. An earlier version parsed only
    1 and 2, so `referenced` came back empty for those units and every A3 orphan
    warning was swallowed -- clean output backed by no evidence.
    """
    found: set[str] = set()
    for raw in RE_WIKI_EMBED.findall(body):
        # `|width` and `#heading` are display options, not part of the filename.
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if target.startswith("assets/"):
            found.add(target[len("assets/"):])
    found.update(RE_MD_IMAGE.findall(body))
    found.update(RE_HTML_IMAGE.findall(body))
    return found


def parse_state(course_dir: Path) -> dict[str, str]:
    """Read COURSE_STATE.yaml keys without a YAML dependency.

    Keys may be nested (`structure:` / `current_unit:`), so leading whitespace is
    allowed -- matching only column 0 would miss every nested field.
    """
    text = (course_dir / "COURSE_STATE.yaml").read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for line in text.splitlines():
        m = re.match(r'^\s*([a-z_]+)\s*:\s*["\']?([^"\'#]*?)["\']?\s*$', line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def check(course_dir: Path) -> tuple[list[str], list[str]]:
    fails: list[str] = []
    warns: list[str] = []

    def fail(tag: str, msg: str) -> None:
        fails.append(f"{tag}: {msg}")

    def warn(tag: str, msg: str) -> None:
        warns.append(f"{tag}: {msg}")

    if not course_dir.is_dir():
        return [f"course directory not found: {course_dir}"], []
    if not (course_dir / "COURSE_STATE.yaml").exists():
        return [f"R2: COURSE_STATE.yaml missing in {course_dir}"], []

    f = parse_state(course_dir)
    course_code, scheme = f.get("course_code", ""), f.get("unit_scheme", "")
    prefix = f.get("unit_prefix") or UNIT_SCHEME_PREFIX.get(scheme, None)

    # R1 is intentionally unchecked: README.md is deferred (standard 2.2).
    if course_dir.name != course_code:
        fail("R2", f"dir {course_dir.name!r} != course_code {course_code!r}")
    if prefix is None or (not prefix and scheme != "custom"):
        fail("U3", f"unit_scheme {scheme!r} is not a legal enum value or unit_prefix is unset")
        return fails, warns

    units = sorted(p for p in course_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
    if not units:
        return fails + ["no unit directories found"], warns

    seen_prefixes: set[str] = set()
    type_numbers: dict[str, str] = {}

    for unit in units:
        um = UNIT_DIR_RE.match(unit.name)
        if not um:
            fail("U1", f"unit dir {unit.name!r} does not match {{Prefix}}{{NN}}")
            continue
        if um.group("prefix") != prefix:
            fail("U1", f"unit {unit.name!r} prefix {um.group('prefix')!r} != {prefix!r} (unit_scheme: {scheme})")
        if len(um.group("num")) != 2:
            fail("U4", f"unit {unit.name!r} number must be zero-padded to 2 digits")
        seen_prefixes.add(um.group("prefix"))

        notes = sorted(p for p in unit.iterdir() if p.is_file() and p.suffix == ".md")
        if not notes:
            fail("N1", f"unit {unit.name!r} has no .md file")

        note_srcs: set[str] = set()
        for note in notes:
            nm = NOTE_RE.match(note.name)
            if not nm or nm.group("type") not in TYPE_TO_SRC:
                fail("N2", f"note {unit.name}/{note.name!r} does not match '{{TypeLabel}} {{NN}} - {{Title}}.md'")
                continue
            src = f"{TYPE_TO_SRC[nm.group('type')]}{nm.group('num')}"
            note_srcs.add(src)
            where = f"{unit.name}/{note.name}"
            if src in type_numbers:
                fail("N2", f"{src} used by both {type_numbers[src]!r} and {where!r}")
            else:
                type_numbers[src] = where

        referenced: set[str] = set()
        for note in notes:
            referenced |= collect_refs(note.read_text(encoding="utf-8"))

        assets_dir = unit / "assets"
        for asset in sorted(a for a in assets_dir.iterdir() if a.is_file()) if assets_dir.is_dir() else []:
            am = ASSET_WITH_PAGE_RE.match(asset.name) or ASSET_NO_PAGE_RE.match(asset.name)
            loc = f"{unit.name}/assets/{asset.name}"
            if not am:
                if SEQUENTIAL_RE.match(asset.name):
                    warn("A1", f"{loc!r} uses legacy sequential numbering (needs {{SrcID}}-p{{NN}}-{{slug}})")
                else:
                    fail("A1", f"{loc!r} does not match {{SrcID}}-p{{NN}}-{{slug}}.{{ext}} or {{SrcID}}-{{slug}}.{{ext}}")
            elif f"{am.group('src')}{am.group('num')}" not in note_srcs:
                fail("A2", f"{loc!r} has no matching note ({am.group('src')}{am.group('num')} not in this unit)")
            elif asset.name not in referenced:
                # No `referenced and` guard here: an unreferenced asset is a defect
                # regardless of whether its neighbours happen to be referenced.
                warn("A3", f"{loc!r} is never referenced")

        sources_dir = unit / "sources"
        if not sources_dir.is_dir():
            fail("S1", f"unit {unit.name!r} has no sources/ directory (mandatory)")
            continue
        src_ids = "|".join(TYPE_TO_SRC.values())
        for sf in sorted(p for p in sources_dir.iterdir() if p.is_file()):
            loc = f"{unit.name}/sources/{sf.name}"
            sm = re.match(rf"^{re.escape(course_code)}_(?P<src>{src_ids})(?P<num>\d{{2,3}})_", sf.name)
            if not sm:
                warn("S2", f"{loc!r} does not match {{COURSE_CODE}}_{{SrcID}}_{{Slug}}.ext ({course_code}_L01_Topic.pdf)")
            elif f"{sm.group('src')}{sm.group('num')}" not in note_srcs:
                fail("S3", f"{loc!r} has no matching note ({sm.group('src')}{sm.group('num')})")

    if len(seen_prefixes) > 1:
        fail("U2", "mixed unit prefixes in one course: " + ", ".join(sorted(seen_prefixes)))

    return fails, warns


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    fails, warns = check(Path(sys.argv[1]).resolve())
    for w in warns:
        print(f"WARN: {w}")
    for x in fails:
        print(f"FAIL: {x}")
    if fails:
        print(f"\n{len(fails)} FAIL, {len(warns)} WARN — structure is not compliant")
        return 1
    print(f"\nOK: structure compliant ({len(warns)} WARN)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
