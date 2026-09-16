# Obsidian Course Notes Standard v3.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Upgrade the repository from v2.2.0 to v3.0.0 with a source-aware visual extraction/QA pipeline and automated version-consistency validation.

**Architecture:** Preserve the v2.2 writing/state/delivery contract, replace the visual fallback model with a four-level source hierarchy plus per-asset/final QA, and add repository-level version SOT/CI validation. Work on `release/v3.0.0`, never directly on `main`.

**Tech Stack:** Markdown, YAML, Python 3 standard library, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-16-v3-visual-pipeline-design.md`

## Global Constraints

- Release version: `3.0.0`; course `standard_version`: `3.0`.
- Visual hierarchy: course source / same-source PDF → trusted external source → low-risk SVG → manual capture.
- Maximum two reasonable recrop attempts at Level 1 before escalation.
- Every final visual must pass semantic completeness, technical correctness, visual cleanliness, boundary safety, and adaptive sizing.
- Accepted historical course notes are not automatically migrated.
- Do not modify user `.obsidian/` settings.

---

### Task 1: Upgrade canonical and execution documentation

**Files:** create `Obsidian_Course_Notes_Standard_v3.0.md`; modify `SKILL.md`, `SOP_WEEKLY_CONTINUATION.md`, `HANDOFF_PROMPTS.md`, `TEMPLATE.md`, `COURSE_STATE_TEMPLATE.yaml`; remove v2.2 canonical.

- [x] Preserve all v2.2 non-visual rules unless they conflict with v3.0.
- [x] Add the four-level hierarchy, two-attempt escalation, external semantic-equivalence/provenance rules, SVG risk restrictions, adaptive sizing, per-asset QA, and final visual audit.
- [x] Set `standard_version: "3.0"`.
- [x] Verify no active v2.1/v2.2 references remain.

### Task 2: Upgrade repository release metadata

**Files:** modify `README.md`, `.gitignore`, `.gitattributes`; create `VERSION`, `CHANGELOG.md`.

- [x] Make README describe v3.0 and current canonical filename.
- [x] Add release history without treating historical versions as stale active references.
- [x] Normalize Markdown/YAML/SVG/Python/VERSION to LF.
- [x] Keep release ZIP files ignored.

### Task 3: Add consistency validation

**Files:** create `scripts/validate_standard.py`, `.github/workflows/validate-standard.yml`.

- [x] Add unit tests for valid v3 repo, stale canonical, stale active version, and missing visual marker.
- [x] Verify the tests fail before validator implementation and pass afterward.
- [x] Validate semantic `VERSION` and canonical filename alignment.
- [x] Validate README and Course State version alignment.
- [x] Reject active stale v2.1/v2.2 references.
- [x] Validate required v3 visual-pipeline markers in canonical and SKILL.
- [x] Run `python scripts/validate_standard.py` and require exit 0.

### Task 4: Repository-wide release audit

- [x] Run stale-version grep excluding `CHANGELOG.md` and historical development docs where appropriate.
- [x] Run Markdown relative-link/reference sanity checks for repository-local file references.
- [x] Build `OBSIDIAN_COURSE_NOTES_STANDARD_V3_0_FINAL.zip` from release files and verify archive integrity.
- [x] Compare branch against `main`; confirm only intended files changed.

### Task 5: GitHub delivery

- [x] Create `release/v3.0.0` from `main`.
- [x] Commit the complete v3.0 file set.
- [x] Create PR to `main` with migration summary and verification evidence.
- [ ] Do not merge or publish the release until human review.
