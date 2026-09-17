#!/usr/bin/env python3
"""CI smoke test for scripts/check_course_structure.py.

Builds a tiny course, breaks it one rule at a time, and asserts each rule fires.
Without this a checker can rot into printing OK forever and nobody notices --
green output with no evidence behind it is worse than no checker at all.

Replaces the old `--self-test` flag, which cost ~130 lines of fixture code
embedded in the checker for a rule set this small. Runtime fixtures beat
hand-maintained ones: less code, and they cannot drift from what the checker
actually reads.

    python tests/fixtures/run_course_check.py
"""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from check_course_structure import check  # noqa: E402


def build(root: Path) -> Path:
    """A minimal, fully compliant course: one unit, one note, one asset, one source."""
    c = root / "TST101"
    (c / "Week01" / "assets").mkdir(parents=True)
    (c / "Week01" / "sources").mkdir(parents=True)
    (c / "COURSE_STATE.yaml").write_text(
        'schema: obsidian-course-state/v1\ncourse_code: TST101\n'
        'standard_version: "3.1"\nstructure:\n  unit_scheme: week\n  current_unit: 1\n',
        encoding="utf-8",
    )
    (c / "Week01" / "Lecture 01 - Topic.md").write_text(
        "![[assets/L01-p10-good.png|760]]\n", encoding="utf-8"
    )
    (c / "Week01" / "assets" / "L01-p10-good.png").write_bytes(b"x")
    (c / "Week01" / "sources" / "TST101_L01_Topic.pdf").write_bytes(b"x")
    return c


def tags(course: Path) -> tuple[set[str], set[str]]:
    f, w = check(course)
    split = lambda xs: {s.split(":", 1)[0] for s in xs}  # noqa: E731
    return split(f), split(w)


def main() -> int:
    results: list[tuple[str, bool]] = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        c = build(root)
        f, w = tags(c)
        results.append(("compliant course is silent", not f and not w))

        # Each case: name, mutate, expected tag, expected severity.
        cases = [
            ("A1 fails on illegal asset name",
             lambda: (c / "Week01/assets/BAD.png").write_bytes(b"x"), "A1", "f"),
            ("A1 warns on legacy sequential",
             lambda: (c / "Week01/assets/09-legacy.png").write_bytes(b"x"), "A1", "w"),
            ("A2 fails on asset with no note",
             lambda: (c / "Week01/assets/L77-p01-orphan.png").write_bytes(b"x"), "A2", "f"),
            ("A3 warns on unreferenced asset",
             lambda: (c / "Week01/assets/L01-p99-extra.png").write_bytes(b"x"), "A3", "w"),
            ("S2 warns on malformed source name",
             lambda: (c / "Week01/sources/random.pdf").write_bytes(b"x"), "S2", "w"),
            ("S3 fails on orphan source",
             lambda: (c / "Week01/sources/TST101_L88_Ghost.pdf").write_bytes(b"x"), "S3", "f"),
            ("N1 fails on unit with no note",
             lambda: (c / "Week02").mkdir() or (c / "Week02/sources").mkdir(), "N1", "f"),
        ]
        for name, mutate, tag, sev in cases:
            mutate()
            f, w = tags(c)
            hits = f if sev == "f" else w
            results.append((name, tag in hits))
            # undo: drop anything created by the mutation
            for p in sorted((c / "Week01").rglob("*"), reverse=True):
                if p.name in {"BAD.png", "09-legacy.png", "L77-p01-orphan.png",
                              "L01-p99-extra.png", "random.pdf", "TST101_L88_Ghost.pdf"}:
                    p.unlink()
            shutil.rmtree(c / "Week02", ignore_errors=True)
            f, w = tags(c)
            results.append((f"  ...and silent again after undoing {tag}", not f and not w))

        # S1: sources/ is mandatory.
        s = c / "Week01/sources"
        bak = root / "sources_bak"
        shutil.move(str(s), str(bak))
        f, _ = tags(c)
        results.append(("S1 fails when sources/ is missing", "S1" in f))
        shutil.move(str(bak), str(s))

        # U3: closed enum -- a made-up scheme must be rejected, not ignored.
        st = c / "COURSE_STATE.yaml"
        orig = st.read_text(encoding="utf-8")
        st.write_text(orig.replace("unit_scheme: week", "unit_scheme: fortnightly"), encoding="utf-8")
        f, _ = tags(c)
        results.append(("U3 fails on illegal unit_scheme", "U3" in f))
        st.write_text(orig, encoding="utf-8")

        # R2: course_code must match the directory name.
        st.write_text(orig.replace("course_code: TST101", "course_code: NOPE"), encoding="utf-8")
        f, _ = tags(c)
        results.append(("R2 fails on course_code mismatch", "R2" in f))
        st.write_text(orig, encoding="utf-8")

        # The three reference syntaxes. <img src> is the one that silently
        # disabled A3 for three real units once -- it must register as a ref.
        note = c / "Week01" / "Lecture 01 - Topic.md"
        for label, body, expect_silent in [
            ("wiki embed", "![[assets/L01-p10-good.png|760]]", True),
            ("markdown image", "![x](assets/L01-p10-good.png)", True),
            ("html img", '<img src="assets/L01-p10-good.png" width="760">', True),
        ]:
            note.write_text(body + "\n", encoding="utf-8")
            _, w = tags(c)
            results.append((f"A3 silent when referenced via {label}", "A3" not in w))

    ok = sum(1 for _, v in results if v)
    for name, passed in results:
        print(f"{'PASS' if passed else 'FAIL'}  {name}")
    if ok != len(results):
        print(f"\n{len(results) - ok} check(s) failed")
        return 1
    print(f"\ncourse checker smoke test OK ({len(results)} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
