import tempfile
import unittest
from pathlib import Path

from scripts.validate_standard import validate


class ValidateStandardTests(unittest.TestCase):
    def make_repo(self) -> Path:
        root = Path(tempfile.mkdtemp())
        (root / "VERSION").write_text("3.0.0\n", encoding="utf-8")
        canonical = root / "Obsidian_Course_Notes_Standard_v3.0.md"
        canonical.write_text(
            "\n".join(
                [
                    "# Obsidian Course Notes Standard v3.0",
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
            ),
            encoding="utf-8",
        )
        (root / "README.md").write_text(
            "v3.0.0\nObsidian_Course_Notes_Standard_v3.0.md\n", encoding="utf-8"
        )
        (root / "COURSE_STATE_TEMPLATE.yaml").write_text(
            'standard_version: "3.0"\n', encoding="utf-8"
        )
        (root / "SKILL.md").write_text(
            "可信教材或官方外部原图\n最多两次合理 recrop\nVisual QA Gate\n",
            encoding="utf-8",
        )
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


if __name__ == "__main__":
    unittest.main()
