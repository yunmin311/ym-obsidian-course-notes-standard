<div align="center">

# Obsidian Course Notes Standard

**A reusable, AI-agnostic workflow for producing consistent, maintainable, and Obsidian-ready course notes.**

Turn raw lectures, tutorials, labs, readings, and PDFs into structured course notes through a persistent standard, course state, incremental delivery, and human review.

[![Version](https://img.shields.io/badge/version-v2.1.0-blue.svg)](../../releases/tag/v2.1.0)
[![Status](https://img.shields.io/badge/status-frozen-success.svg)](#versioning)
[![Obsidian](https://img.shields.io/badge/Obsidian-ready-7C3AED.svg)](https://obsidian.md/)
[![Markdown](https://img.shields.io/badge/Markdown-compatible-black.svg)](https://www.markdownguide.org/)
[![AI](https://img.shields.io/badge/AI-agent--agnostic-orange.svg)](#design-principles)

</div>

---

## Overview

AI can generate course notes quickly, but maintaining them across weeks, courses, conversations, and different AI agents is much harder.

Common problems include inconsistent formatting, slide-by-slide transcription, lost source relationships, duplicated content, silent rewriting of previously accepted notes, and new agents having no knowledge of the current course state.

**Obsidian Course Notes Standard** treats course-note generation as a persistent workflow rather than a one-shot prompt.

```text
Source Materials
      │
      ▼
Canonical Standard
      +
COURSE_STATE.yaml
      │
      ▼
   AI Agent
      │
      ▼
Draft Week / Unit Delivery
      │
      ▼
 Human Review
   │       │
revise   accept
           │
           ▼
    Persistent Course State
```

The result is a note system that remains stable even when the model, conversation, machine, or AI application changes.

## Core Model

The workflow separates global rules from course-specific state:

```text
Global Standard
│
├── Writing and knowledge rules
├── Visual / formula / code rules
├── File and packaging rules
└── Agent execution contract

Course State
│
├── Current unit
├── Completed artifacts
├── draft / accepted status
├── Course-specific overrides
└── Next expected work

Source Materials
│
├── Lecture
├── Tutorial
├── Lab
└── Reading

            ↓

Incremental Obsidian Delivery
```

The Global Standard remains stable across courses. Differences belonging to a specific course are stored in its state instead of modifying the global rules.

## Features

- **AI-agent agnostic** — designed to work across different models, applications, conversations, and machines.
- **Stateful workflow** — `COURSE_STATE.yaml` preserves progress, accepted artifacts, overrides, and the next expected unit.
- **Incremental delivery** — generate only the new Week / Unit instead of rebuilding the full course.
- **Human-controlled acceptance** — new artifacts start as `draft`; accepted notes are protected from silent modification.
- **Knowledge-first writing** — notes are reorganized around concepts and mechanisms rather than copied slide-by-slide.
- **Source-aware generation** — course sources, external supplements, and model inference remain distinguishable.
- **Obsidian-ready output** — relative links, Markdown, MathJax, images, SVGs, code, and packaged assets remain portable.
- **Portable handoff** — another AI can continue the course using the same Standard and Course State.

## Quick Start

### 1. Get the Standard

Download the latest release or clone the repository:

```bash
git clone https://github.com/yunmin311/ym-obsidian-course-notes-standard.git
```

### 2. Create the Course State

Copy:

```text
COURSE_STATE_TEMPLATE.yaml
```

into your course root as:

```text
COURSE_STATE.yaml
```

Then set the course code, course name, current unit, and any course-specific overrides.

### 3. Give the Agent the Required Context

The agent should have access to:

```text
Obsidian_Course_Notes_Standard_v2.1.md
SKILL.md
COURSE_STATE.yaml
```

Then provide the current Lecture / Tutorial / Lab / Reading materials.

### 4. Run the Workflow

Use the appropriate handoff prompt from:

```text
HANDOFF_PROMPTS.md
```

The agent reads the Standard, current Course State, and new source materials, then produces only the required new artifacts.

### 5. Review the Draft

New content is delivered as:

```text
draft
```

After explicit human acceptance, the corresponding artifact is changed to:

```text
accepted
```

Accepted artifacts must not be silently rewritten by later agents.

## Delivery Structure

A typical course can look like:

```text
COURSE_CODE/
├── README.md
├── COURSE_STATE.yaml
├── NOTE_STYLE_SPEC.md
│
├── Week01/
│   ├── Lecture 01 - Topic.md
│   ├── Tutorial 01 - Topic.md
│   ├── Lab 01 - Topic.md
│   │
│   ├── assets/
│   │   ├── L01-example.png
│   │   └── L01-process.svg
│   │
│   └── sources/
│       ├── Lecture01.pdf
│       └── Tutorial01.pdf
│
└── Week02/
    └── ...
```

Each Week / Unit is designed to remain self-contained and portable.

Incremental delivery packages use:

```text
COURSE_CODE_WeekXX_Delivery.zip
```

or:

```text
COURSE_CODE_UnitXX_Delivery.zip
```

## Repository Structure

| File | Role |
| --- | --- |
| `Obsidian_Course_Notes_Standard_v2.1.md` | Canonical global specification |
| `SKILL.md` | Execution contract for AI agents |
| `TEMPLATE.md` | Minimum note structure |
| `COURSE_STATE_TEMPLATE.yaml` | Persistent course-state template |
| `SOP_WEEKLY_CONTINUATION.md` | Incremental delivery workflow |
| `HANDOFF_PROMPTS.md` | Cross-conversation and cross-agent handoff prompts |

The canonical Standard defines **what must remain consistent**.

`SKILL.md` defines **how an AI agent should execute it**.

`COURSE_STATE.yaml` defines **where a specific course currently is**.

## Design Principles

### Knowledge before formatting

The goal is not to reproduce slides. Source material is reconstructed around the actual knowledge structure of the lecture.

### Prose first

Continuous explanation is the default teaching medium. Tables, equations, diagrams, screenshots, SVGs, and code are used only when they communicate the information more effectively.

### Stable accepted artifacts

Human acceptance creates a boundary. Once an artifact becomes `accepted`, future agents cannot silently rewrite it.

### Explicit state instead of conversational memory

Important workflow state lives in files rather than relying on one model's memory or one conversation history.

### Global rules stay global

The canonical Standard only contains rules that should apply across courses.

Course-specific requirements belong in:

```text
COURSE_STATE.yaml → course_overrides
```

or, when necessary:

```text
NOTE_STYLE_SPEC.md
```

### Source dependencies remain portable

If a delivered Markdown document references a file inside `sources/`, that source file becomes part of the delivery dependency and must be packaged with it.

## Agent Handoff

A new AI agent does not need the previous conversation history.

It only needs:

```text
Canonical Standard
       +
Latest COURSE_STATE.yaml
       +
New Source Materials
```

From these, it can determine what has already been completed, which artifacts are accepted, what is still draft, what course-specific rules apply, and what should be generated next.

This makes the workflow portable between agents without turning conversation history into the source of truth.

## Versioning

The current stable baseline is:

```text
v2.1.0
```

`v2.1` is frozen.

A new Global Standard version should only be created when actual course usage reveals a **cross-course common problem**.

A requirement that affects only one course does not justify a new global version.

```text
Course-specific change
        ↓
course_overrides

Cross-course systemic change
        ↓
new Standard version
```

This keeps the global contract stable while allowing individual courses to evolve independently.

## Project Status

**v2.1.0 — Frozen baseline**

The current version is intended for real course-note production.

Future revisions will be driven by problems discovered through actual course usage rather than speculative expansion.

---

<div align="center">

**Standardize the workflow, preserve the state, keep the notes portable.**

</div>
