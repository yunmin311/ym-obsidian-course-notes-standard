<div align="center">

# Obsidian Course Notes Standard

**A reusable, AI-agnostic workflow for producing consistent, maintainable, source-aware, and Obsidian-ready course notes.**

[![Version](https://img.shields.io/badge/version-v3.1.0-blue.svg)](../../releases/tag/v3.1.0)
[![Status](https://img.shields.io/badge/status-frozen-success.svg)](#versioning)
[![Obsidian](https://img.shields.io/badge/Obsidian-ready-7C3AED.svg)](https://obsidian.md/)
[![Markdown](https://img.shields.io/badge/Markdown-compatible-black.svg)](https://www.markdownguide.org/)
[![AI](https://img.shields.io/badge/AI-agent--agnostic-orange.svg)](#design-principles)

</div>

## Overview

AI can write course notes quickly. The difficult part is keeping them correct, visually reliable, portable, and consistent across weeks, courses, conversations, and different agents.

**Obsidian Course Notes Standard v3.1** treats note generation as a persistent compilation workflow rather than a one-shot prompt. The canonical standard defines global rules; `COURSE_STATE.yaml` stores the current course state; each Week/Unit is delivered as a self-contained package that can be dropped directly into an Obsidian vault.

v3.1 makes the delivery structure and file naming a **mechanically checkable contract**. The naming system has exactly one variable — `structure.unit_scheme` in `COURSE_STATE.yaml` — so it adapts to non-week course organisations without letting names drift.

The 3.0 release was the workflow upgrade driven by real course use: it formalized visual extraction as a source-aware pipeline with explicit escalation and QA instead of relying on ad-hoc screenshot cropping.

```text
Source Materials
      │
      ▼
Canonical Standard + COURSE_STATE.yaml
      │
      ▼
Knowledge Rewrite
      │
      ├─ Visual Need Decision
      │      ↓
      │  Course Source
      │      ↓ if failed
      │  Trusted External Source
      │      ↓ if failed
      │  Low-risk SVG
      │      ↓ if failed
      │  Manual Capture Required
      │
      ▼
Per-Asset QA + Final Visual Audit
      │
      ▼
Draft Week / Unit Delivery
      │
      ▼
Human Review → Accepted State
```

## What v3.1 adds

- **Delivery structure as a hard contract** — the former descriptive section is now a rule set with explicit required/optional/conditional markers and a mechanical validation table.
- **Four-segment naming model with one variable** — `unit_scheme` decides the unit-directory prefix; note files, asset files, and source files are all derived from it.
- **Closed `unit_scheme` enum** — `week` / `lecture` / `module` / `chapter` / `unit` / `custom`, locked once a course starts delivering. No mixing, no free-form prefixes.
- **Real page anchors, no placeholders** — asset names use `{SrcID}-p{NN}-{slug}.{ext}` where `p{NN}` is the genuine source page, or the page segment is omitted entirely for self-made SVG. `p00`-style placeholders are rejected.
- **Course-wide continuous numbering** — note numbers increment per type across the whole course, not per unit, so a later unit continues from the previous one instead of restarting.
- **`sources/` is unconditionally mandatory** — traceability is a property of the structure, not of whether a note happens to link a source file.
- **Course `README.md` is deferred** — unit deliveries never contain it; it is generated once after the whole course is written, and its absence is not a defect.
- **Structure & naming gate** — 11 mechanical checks (U1-U4, N1-N2, A1-A3, S1-S3) added to the pre-delivery gate and the validator.

## What the 3.0 release added

- **Four-level Visual Source Hierarchy** — course source / same-source PDF → trustworthy textbook or official external figure → low-risk SVG → manual capture.
- **Two-attempt escalation** — after two reasonable recrops fail, the agent must stop guessing coordinates and move up the source hierarchy.
- **Visual QA Gate** — semantic completeness, technical correctness, visual cleanliness, boundary safety, and adaptive sizing are mandatory before an asset may enter Markdown.
- **External-source verification** — replacement figures must match the course model, direction, polarity, symbols, axes, and assumptions, and must be clearly attributed.
- **Adaptive image sizing** — small diagrams stay small; wide graphs and multi-panel technical figures may use most of the reading width.
- **Pre-delivery visual audit** — every visual actually referenced by Markdown is re-opened or placed on a contact sheet before the ZIP is built.
- **Version consistency checks** — `VERSION` plus CI validation prevents stale pre-v3 active references from silently surviving a release.

## Quick Start

### 1. Clone the standard

```bash
git clone https://github.com/yunmin311/ym-obsidian-course-notes-standard.git
```

### 2. Create course state

Copy `COURSE_STATE_TEMPLATE.yaml` into the course root as `COURSE_STATE.yaml`, then set the course code, name, `structure.unit_scheme`, current unit, Gold Reference, and any course-specific overrides.

### 3. Give the agent the minimum required context

The agent needs:

```text
Canonical Standard
+ latest COURSE_STATE.yaml
+ new Lecture / Tutorial / Lab / Reading sources
```

For this release, the canonical file is:

```text
Obsidian_Course_Notes_Standard_v3.1.md
```

Supporting prompts are available in `HANDOFF_PROMPTS.md`.

### 4. Review draft delivery

New artifacts are delivered as `draft`. After explicit human acceptance, update the corresponding artifact and unit state to `accepted`; accepted artifacts must not be silently rewritten by later agents.

## Delivery Structure

```text
COURSE_CODE/
├── COURSE_STATE.yaml              # required, filename fixed
├── README.md                      # deferred: generated once the course is complete
├── NOTE_STYLE_SPEC.md             # optional course-specific overrides
├── Week01/                        # prefix comes from structure.unit_scheme
│   ├── Lecture 01 - Topic.md      # numbering continues course-wide per type
│   ├── Tutorial 01 - Topic.md
│   ├── assets/                    # L01-p15-topic.png
│   └── sources/                   # mandatory; CSI201_L01_Topic.pdf
└── Week02/
    └── ...
```

Incremental packages use:

```text
COURSE_CODE_UnitXX_Delivery.zip
```

(`Unit` is a placeholder for the prefix that `unit_scheme` selects: `week`→`Week`, `lecture`→`Lecture`, `module`→`Module`, `chapter`→`Chapter`, `unit`→`Unit`.)

Each unit remains self-contained and portable. `sources/` is mandatory in every unit; if Markdown references a file under `sources/`, that file is additionally a hard delivery dependency.

## Repository Structure

| File | Role |
| --- | --- |
| `VERSION` | Release-version source of truth |
| `Obsidian_Course_Notes_Standard_v3.1.md` | Canonical global specification |
| `SKILL.md` | Compact execution contract for agents |
| `TEMPLATE.md` | Minimum note skeleton |
| `COURSE_STATE_TEMPLATE.yaml` | Persistent course-state template |
| `SOP_WEEKLY_CONTINUATION.md` | Incremental delivery workflow |
| `HANDOFF_PROMPTS.md` | Cross-chat / cross-agent handoff prompts |
| `CHANGELOG.md` | Release history |
| `scripts/validate_standard.py` | Version and repository consistency validator |
| `scripts/check_course_structure.py` | v3.1 delivery-structure and naming checker for a course folder |
| `.github/workflows/validate-standard.yml` | CI validation on pushes and pull requests |

## Design Principles

**Knowledge before formatting.** Notes are reconstructed around concepts, mechanisms, models, and problem-solving logic rather than slide order.

**Prose first.** Continuous explanation is the default teaching medium. Visuals, equations, tables, and code are used when they communicate the current information better.

**Source fidelity.** Primary course material remains the default authority. External figures are supplements, never silently substituted course content.

**Visual correctness before visual abundance.** A technically wrong arrow, polarity, axis, or panel is worse than having no figure. High-risk diagrams must come from a verifiable source rather than speculative reconstruction.

**Persistent state instead of conversational memory.** Course status lives in `COURSE_STATE.yaml`, not in one chat session.

**Stable accepted artifacts.** Human acceptance creates a boundary. Later agents cannot silently rewrite accepted notes.

**One variable, everything else derived.** The naming system is anchored on `structure.unit_scheme`. Changing how a course is organised means changing one enum value, not inventing a new convention.

**Global rules stay global.** Course-specific behavior belongs in `course_overrides` or `NOTE_STYLE_SPEC.md`, not in the canonical standard.

## Visual Source Hierarchy

```text
Level 1  Current course source / same-source PDF
   │     high-resolution extraction + semantic envelope + QA
   ▼
Level 2  Trusted external original figure
   │     textbook / university / OER / vendor / official documentation
   │     semantic-equivalence check + provenance
   ▼
Level 3  Low-risk static SVG
   │     only when structure is simple and every element is verifiable
   ▼
Level 4  Manual Capture Required
         rare, explicit, and never hidden behind a broken substitute
```

Every final asset must pass the Visual QA Gate defined in the canonical standard before delivery.

## Versioning

Current stable baseline:

```text
v3.1.0
```

`VERSION` is the repository source of truth. Supporting execution files intentionally refer to the **canonical standard** rather than hard-coding a versioned filename wherever possible. CI rejects stale active pre-v3 release references.

Course-specific changes do not require a global release. Cross-course systemic changes do.

```text
Course-specific change → course_overrides
Cross-course compatible refinement → 3.x
Breaking workflow / contract change → next major
```

Historical release information is retained in `CHANGELOG.md` and GitHub Releases.

## Validation

Run locally:

```bash
python scripts/validate_standard.py
```

The validator checks canonical filename/version alignment, course-state version alignment, stale active version references, required v3 visual-pipeline markers, and the v3.1 delivery-structure contract (section markers, the closed `unit_scheme` enum, and the presence of `unit_scheme`/`unit_prefix` in the state template).

To check an actual course folder against the delivery rules:

```bash
python scripts/check_course_structure.py /path/to/COURSE_CODE
```

This reports `FAIL` (must fix before delivery) and `WARN` (legacy naming to migrate later) for unit prefixes, note numbering, asset naming, orphan assets/sources, and the mandatory `sources/` directory. `--self-test` proves every rule can actually fire.

---

<div align="center">

**Standardize the workflow. Preserve the state. Verify the visuals. Keep the notes portable.**

</div>
