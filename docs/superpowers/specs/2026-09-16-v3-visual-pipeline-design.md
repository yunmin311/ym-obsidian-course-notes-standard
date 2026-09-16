# Obsidian Course Notes Standard v3.0 — Visual Pipeline Design

## Purpose

Upgrade the v2.2 course-notes standard to v3.0 after repeated real-course failures showed that semantic-completeness cropping alone was insufficient. The new standard must make visual extraction a source-aware, self-auditing workflow and remove version drift across repository files.

## Scope

v3.0 keeps the existing knowledge-writing, state, delivery, and acceptance model. It changes the global visual execution contract and repository release consistency.

## Visual architecture

Visuals are selected only after prose-first teaching determines that a visual is useful. The source hierarchy is fixed:

1. Current course source or same-source PDF page.
2. Trustworthy external original figure: textbook/publisher, university/OER, vendor, official technical documentation.
3. Low-risk static SVG that can be verified item-by-item.
4. Explicit Manual Capture Required marker.

A Level 1 figure gets at most two reasonable recrop attempts. Continued coordinate guessing after two failures is forbidden.

Every final asset passes five gates before Markdown inclusion: semantic completeness, technical correctness, visual cleanliness, boundary safety, adaptive sizing. A second full audit runs over the actual referenced assets before packaging.

External figures require provenance and semantic-equivalence validation. High-risk visuals—direction/polarity-sensitive mechanisms, complex circuits, precision plots/waveforms—must not be reconstructed speculatively.

## Repository architecture

`VERSION` becomes the release-version source of truth. The canonical file remains versioned (`Obsidian_Course_Notes_Standard_v3.0.md`), while execution helpers refer to the canonical standard generically where possible. A stdlib Python validator and GitHub Actions workflow reject stale active v2.1/v2.2 references, missing canonical files, wrong Course State version, and missing v3 visual-pipeline markers.

## Compatibility

Existing accepted course notes are not automatically rewritten. A course moves to v3.0 by updating `standard_version` when it next adopts the new global standard. Course-specific visual overrides remain in `course_overrides` / `NOTE_STYLE_SPEC.md`.

## Release flow

Development occurs on `release/v3.0.0`, reviewed through a PR into `main`. After merge, create tag/release `v3.0.0` and attach `OBSIDIAN_COURSE_NOTES_STANDARD_V3_0_FINAL.zip`.
