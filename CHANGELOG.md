# Changelog

All notable changes to the Obsidian Course Notes Standard are documented here.

## 3.1.0 — 2026-09-17

### Added

- Turned the delivery-structure section from a descriptive recommendation into a **mechanically checkable contract**, with explicit required / conditional / deferred markers and a per-rule validation table (`U1-U4`, `N1-N2`, `A1-A3`, `S1-S3`).
- Introduced the **four-segment naming model** with exactly one variable: `structure.unit_scheme` decides the unit-directory prefix, while note, asset, and source names are derived from it.
- Defined a **closed `unit_scheme` enum** (`week` / `lecture` / `module` / `chapter` / `unit` / `custom`) with a fixed prefix map and a `unit_prefix` escape hatch for `custom`.
- Made **course-wide continuous numbering** explicit: note numbers increment per type across the whole course, not per unit, so a later unit continues instead of restarting at 01.
- Established the **`TypeLabel` → `SrcID` derivation table** (`Lecture→L`, `Tutorial→T`, `Lab→LAB`, `Recitation→R`).
- Added the **Structure & Naming Gate** to the pre-delivery checklist, the Weekly SOP, and `SKILL.md`.

### Changed

- **`sources/` is now unconditionally mandatory** in every unit, instead of being required only when a note links a source file. Traceability is now a property of the structure rather than of incidental references.
- Asset naming tightened to `{SrcID}-p{NN}-{slug}.{ext}` where `p{NN}` must be the **genuine source page**. Placeholder page numbers (including `p00`) are rejected; self-made SVG omits the page segment entirely instead.
- Source files are now named `{COURSE_CODE}_{SrcID}_{Slug}.{ext}` so a file stays self-describing outside its directory, and joined to assets through `{SrcID}`.
- Course `README.md` is **deferred**: unit deliveries never contain it, it is generated once after the whole course is written, and its absence during the course is not a defect.
- Delivery package naming is now uniformly `COURSE_CODE_Unit{NN}_Delivery.zip`, where `Unit` is a placeholder resolved through `unit_scheme`.
- Sequential asset numbering (e.g. `01-campus-access-path.png`) is formally classified as non-compliant; historic units are flagged as `WARN` and migrated together with their `sources/` backfill rather than renamed immediately.

### Repository

- Added `scripts/check_course_structure.py`: a dependency-free checker that validates an actual course folder against the 2.7 rule table, with a `--self-test` mode that proves each rule can really fire. Wired into CI.
- `scripts/validate_standard.py` gained the v3.1 structure gates: required section markers, the closed `unit_scheme` enum, and the `unit_scheme` / `unit_prefix` keys in `COURSE_STATE_TEMPLATE.yaml`.
- Test suite grew from 5 to 8 cases, covering the structure contract, the `unit_scheme` enum, and the state-template naming variables.
- `COURSE_STATE_TEMPLATE.yaml` exposes `unit_prefix` alongside `unit_scheme`.

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
