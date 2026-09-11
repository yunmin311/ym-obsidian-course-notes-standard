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
