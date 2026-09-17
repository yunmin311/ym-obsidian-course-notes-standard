import tempfile
import unittest
from pathlib import Path

from scripts.validate_standard import REQUIRED_STRUCTURE_MARKERS, validate

SKILL_MARKERS = "可信教材或官方外部原图\n最多两次合理 recrop\nVisual QA Gate\n"


class ValidateStandardTests(unittest.TestCase):
    def make_repo(self, version: str = "3.0.0") -> Path:
        """Build a minimal repo that is fully consistent with `version`."""
        major, minor = version.split(".")[:2]
        short = f"{major}.{minor}"
        canonical_name = f"Obsidian_Course_Notes_Standard_v{short}.md"

        root = Path(tempfile.mkdtemp())
        (root / "VERSION").write_text(f"{version}\n", encoding="utf-8")
        canonical = root / canonical_name
        canonical.write_text(
            "\n".join(
                [
                    f"# Obsidian Course Notes Standard v{short}",
                    "Visual Source Hierarchy",
                    "Level 1 — 当前课程原始材料",
                    "Level 2 — 可信外部原图",
                    "Level 3 — 静态 SVG / 可控重绘",
                    "Level 4 — Manual Capture Required",
                    "Visual QA Gate",
                    "最多两次合理裁切尝试",
                    "Adaptive sizing",
                    "Pre-delivery Visual Audit",
                    *REQUIRED_STRUCTURE_MARKERS,
                    "`week` `lecture` `module` `chapter` `unit` `custom`",
                ]
            ),
            encoding="utf-8",
        )
        (root / "README.md").write_text(
            f"v{version}\n{canonical_name}\n", encoding="utf-8"
        )
        (root / "COURSE_STATE_TEMPLATE.yaml").write_text(
            f'standard_version: "{short}"\nunit_scheme: week\nunit_prefix: ""\n',
            encoding="utf-8",
        )
        (root / "SKILL.md").write_text(SKILL_MARKERS, encoding="utf-8")
        for name in ["SOP_WEEKLY_CONTINUATION.md", "HANDOFF_PROMPTS.md", "TEMPLATE.md"]:
            (root / name).write_text("canonical standard\n", encoding="utf-8")
        return root

    def test_valid_v3_repository_has_no_errors(self):
        root = self.make_repo()
        self.assertEqual(validate(root), [])

    def test_rejects_stale_canonical_file(self):
        root = self.make_repo()
        (root / "Obsidian_Course_Notes_Standard_v2.2.md").write_text("old", encoding="utf-8")
        errors = validate(root)
        self.assertTrue(any("stale canonical" in error for error in errors))

    def test_rejects_stale_active_version_reference(self):
        root = self.make_repo()
        (root / "SKILL.md").write_text("use v2.2\n", encoding="utf-8")
        errors = validate(root)
        self.assertTrue(any("stale active version" in error for error in errors))

    def test_rejects_missing_visual_pipeline_marker(self):
        root = self.make_repo()
        canonical = root / "Obsidian_Course_Notes_Standard_v3.0.md"
        canonical.write_text(canonical.read_text(encoding="utf-8").replace("Adaptive sizing\n", ""), encoding="utf-8")
        errors = validate(root)
        self.assertTrue(any("missing v3 visual markers" in error for error in errors))

    def test_rejects_version_drift_after_future_upgrade(self):
        """The gate must follow VERSION instead of hardcoding 3.0.

        A repo fully upgraded to 3.1.0 passes even though it still mentions
        older versions inside CHANGELOG.md; the moment an active file is left
        behind on the previous standard version the gate must fail.
        """
        root = self.make_repo("3.1.0")
        # Historical records are allowed to name superseded versions forever.
        (root / "CHANGELOG.md").write_text(
            "## 3.1.0\n\n## 3.0.0\n\n## 2.2.0\n\n## 2.1.0\n", encoding="utf-8"
        )
        self.assertEqual(validate(root), [])

        # SKILL.md was missed during the upgrade and still points at v3.0.
        (root / "SKILL.md").write_text(
            SKILL_MARKERS + "Superseded by v3.1; legacy note retained from v3.0.\n",
            encoding="utf-8",
        )
        errors = validate(root)
        self.assertTrue(any("stale active version" in error for error in errors), errors)
        self.assertTrue(any("v3.0" in error for error in errors), errors)

    def test_rejects_missing_structure_section_marker(self):
        """v3.1 turned the delivery structure into a hard contract.

        Dropping the naming-model section must fail even when every visual
        marker is still intact.
        """
        root = self.make_repo()
        canonical = root / "Obsidian_Course_Notes_Standard_v3.0.md"
        canonical.write_text(
            canonical.read_text(encoding="utf-8").replace("四段派生模型\n", ""),
            encoding="utf-8",
        )
        errors = validate(root)
        self.assertTrue(
            any("missing v3.1 structure markers" in error for error in errors), errors
        )

    def test_rejects_incomplete_unit_scheme_enum(self):
        """The closed unit_scheme enum is what keeps naming from drifting.

        If a legal scheme disappears from the standard, a course organised that
        way has no defined directory prefix and the naming contract is broken.
        """
        root = self.make_repo()
        canonical = root / "Obsidian_Course_Notes_Standard_v3.0.md"
        canonical.write_text(
            canonical.read_text(encoding="utf-8").replace("`chapter`", "CHAPTER_GOES_HERE"),
            encoding="utf-8",
        )
        errors = validate(root)
        self.assertTrue(
            any("does not define unit_scheme `chapter`" in error for error in errors), errors
        )

    def test_rejects_missing_unit_prefix_in_state_template(self):
        """`unit_scheme`/`unit_prefix` are the only naming variables a course sets."""
        root = self.make_repo()
        (root / "COURSE_STATE_TEMPLATE.yaml").write_text(
            'standard_version: "3.0"\nunit_scheme: week\n', encoding="utf-8"
        )
        errors = validate(root)
        self.assertTrue(
            any("must declare unit_prefix:" in error for error in errors), errors
        )


if __name__ == "__main__":
    unittest.main()
