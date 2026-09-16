# Changelog

All notable changes to the Obsidian Course Notes Standard are documented here.

## 3.0.0 — 2026-09-16

### Changed

- Promoted visual handling from a cropping guideline to a four-level **Visual Source Hierarchy**: course source → trustworthy external source → low-risk SVG → manual capture.
- Added a mandatory **Visual QA Gate** covering semantic completeness, technical correctness, visual cleanliness, boundary safety, and adaptive sizing.
- Added the **two-attempt escalation rule**: after two reasonable source recrops fail, agents must stop guessing crop coordinates and move to the next source level.
- Added **semantic equivalence checks** and explicit provenance requirements for external textbook, university, OER, vendor, and official technical figures.
- Restricted SVG reconstruction to low-risk, structurally clear visuals that can be verified item-by-item against reliable sources.
- Added **adaptive image sizing** instead of a single default width.
- Added a mandatory **pre-delivery visual audit** over the actual assets referenced by Markdown.
- Updated Weekly SOP, Skill, Template, Handoff Prompts, and Course State to the v3.0 workflow.

### Repository

- Added `VERSION` as the release-version source of truth.
- Added `scripts/validate_standard.py` and GitHub Actions validation to catch stale version references and missing canonical files before merge.
- Added LF normalization for SVG and Python files.

## 2.2.0 — 2026-09-14

- Made semantic completeness the primary crop rule for formula-heavy, circuit, waveform, plotted, worked-example, and multi-panel figures.

## 2.1.0 — 2026-09-11

- First frozen release of the reusable course-note workflow.
