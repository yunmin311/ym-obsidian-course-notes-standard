<div align="center">

# Obsidian Course Notes Standard

**A reusable, AI-agnostic workflow for producing consistent, maintainable, source-aware, and Obsidian-ready course notes.**

[![Version](https://img.shields.io/badge/version-v3.0.0-blue.svg)](../../releases/tag/v3.0.0)
[![Status](https://img.shields.io/badge/status-frozen-success.svg)](#versioning)
[![Obsidian](https://img.shields.io/badge/Obsidian-ready-7C3AED.svg)](https://obsidian.md/)
[![Markdown](https://img.shields.io/badge/Markdown-compatible-black.svg)](https://www.markdownguide.org/)
[![AI](https://img.shields.io/badge/AI-agent--agnostic-orange.svg)](#design-principles)

</div>

## Overview

AI can write course notes quickly. The difficult part is keeping them correct, visually reliable, portable, and consistent across weeks, courses, conversations, and different agents.

**Obsidian Course Notes Standard v3.0** treats note generation as a persistent compilation workflow rather than a one-shot prompt. The canonical standard defines global rules; `COURSE_STATE.yaml` stores the current course state; each Week/Unit is delivered as a self-contained package that can be dropped directly into an Obsidian vault.

v3.0 is a major workflow upgrade driven by real course use. It formalizes visual extraction as a source-aware pipeline with explicit escalation and QA instead of relying on ad-hoc screenshot cropping.

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

## What v3.0 adds

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

Copy `COURSE_STATE_TEMPLATE.yaml` into the course root as `COURSE_STATE.yaml`, then set the course code, name, unit scheme, current unit, Gold Reference, and any course-specific overrides.

### 3. Give the agent the minimum required context

The agent needs:

```text
Canonical Standard
+ latest COURSE_STATE.yaml
+ new Lecture / Tutorial / Lab / Reading sources
```

For this release, the canonical file is:

```text
Obsidian_Course_Notes_Standard_v3.0.md
```

Supporting prompts are available in `HANDOFF_PROMPTS.md`.

### 4. Review draft delivery

New artifacts are delivered as `draft`. After explicit human acceptance, update the corresponding artifact and unit state to `accepted`; accepted artifacts must not be silently rewritten by later agents.

## Delivery Structure

```text
COURSE_CODE/
├── README.md
├── COURSE_STATE.yaml
├── NOTE_STYLE_SPEC.md             # optional course-specific overrides
├── Week01/
│   ├── Lecture 01 - Topic.md
│   ├── Tutorial 01 - Topic.md
│   ├── assets/
│   └── sources/
└── Week02/
    └── ...
```

Incremental packages use:

```text
COURSE_CODE_WeekXX_Delivery.zip
COURSE_CODE_UnitXX_Delivery.zip
```

Each Week/Unit remains self-contained and portable. If Markdown references a file under `sources/`, that file becomes a hard delivery dependency.

## Repository Structure

| File | Role |
| --- | --- |
| `VERSION` | Release-version source of truth |
| `Obsidian_Course_Notes_Standard_v3.0.md` | Canonical global specification |
| `SKILL.md` | Compact execution contract for agents |
| `TEMPLATE.md` | Minimum note skeleton |
| `COURSE_STATE_TEMPLATE.yaml` | Persistent course-state template |
| `SOP_WEEKLY_CONTINUATION.md` | Incremental delivery workflow |
| `HANDOFF_PROMPTS.md` | Cross-chat / cross-agent handoff prompts |
| `CHANGELOG.md` | Release history |
| `scripts/validate_standard.py` | Version and repository consistency validator |
| `.github/workflows/validate-standard.yml` | CI validation on pushes and pull requests |

## Design Principles

**Knowledge before formatting.** Notes are reconstructed around concepts, mechanisms, models, and problem-solving logic rather than slide order.

**Prose first.** Continuous explanation is the default teaching medium. Visuals, equations, tables, and code are used when they communicate the current information better.

**Source fidelity.** Primary course material remains the default authority. External figures are supplements, never silently substituted course content.

**Visual correctness before visual abundance.** A technically wrong arrow, polarity, axis, or panel is worse than having no figure. High-risk diagrams must come from a verifiable source rather than speculative reconstruction.

**Persistent state instead of conversational memory.** Course status lives in `COURSE_STATE.yaml`, not in one chat session.

**Stable accepted artifacts.** Human acceptance creates a boundary. Later agents cannot silently rewrite accepted notes.

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
v3.0.0
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

The validator checks canonical filename/version alignment, course-state version alignment, stale active version references, and required v3 visual-pipeline markers.

---

<div align="center">

**Standardize the workflow. Preserve the state. Verify the visuals. Keep the notes portable.**

</div>
