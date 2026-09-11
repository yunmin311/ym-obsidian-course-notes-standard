# Skill: Obsidian Course Notes Compiler

Use this skill whenever converting lecture/tutorial/reading/lab material into Obsidian course notes.

## Mission
Create durable, self-contained course notes, not slide summaries or chat-style explanations. Preserve source boundaries, explain mechanisms clearly, and use the right representation for each content type.

## Mandatory behavior
1. Read the complete source before writing.
2. Remove administrative content unless it directly affects learning/assessment or the user asks to keep it.
3. Reorganize by knowledge logic, not slide order.
4. Use continuous prose for first-time explanation; lists only for parallel items/steps; tables for comparable dimensions.
5. Prefer source visuals. Render the PDF/PPT at high resolution and crop only the knowledge-bearing region.
6. If the source visual is unusable and a diagram materially improves comprehension, create a **static SVG** matching the source deck's visual language. Never animate by default.
7. Prefer static SVG over Mermaid for important mechanisms/topologies where visual quality matters. Use Mermaid only for simple structural relations.
8. Use MathJax only for genuine mathematics. Plain directions/states/English terms remain Markdown text.
9. For formulas: establish the problem, show the equation, explain meaning/relationships/conditions, then add an example only when useful.
10. For code: use fenced blocks with language tags. Keep commands and outputs in separate blocks. Explain purpose, key behavior, and relation to the course concept; do not line-comment obvious syntax.
11. Lecture, Tutorial and Lab remain separate documents unless the user explicitly requests merging.
12. All assets use stable relative paths. Final package must remain valid after moving the whole Week/Unit folder.
13. Do not modify `.obsidian/`.
14. Remove AI-hosting language, repetitive summaries, excessive bold, emojis, callout spam, and one-sentence paragraph stacks.
15. Keep visual density moderate: prose interrupted naturally by useful figures/tables/formulas/code, not by decorative blocks.

## Visual decision order
When a visual representation is actually needed: Source crop > embedded source PDF page > static SVG matching deck style > compact table / inline flow > Mermaid.

Do not generate a diagram merely because the section has no image.

## Screenshot crop rule
Keep required labels/legend/axes. Remove slide title when redundant, page number, decorative background and large blank margins. Keep roughly 4–8% breathing room around the useful graphic.

## Static SVG rule
No animation, no hover-required information, no embedded fonts, no `foreignObject` dependency, no unrelated visual theme. Prefer left-to-right layout, centered compact canvas, 1 primary + 1 accent + neutrals inherited from the source deck.

## Source dependency rule
If any delivered Markdown artifact references a file under `sources/`, that referenced source file must be included in the same Delivery ZIP. `sources/` may be omitted only when no delivered note depends on it.

## Delivery
Canonical incremental package:
- Week scheme: `COURSE_CODE_WeekXX_Delivery.zip`
- Unit scheme: `COURSE_CODE_UnitXX_Delivery.zip`

The package contains the updated root `COURSE_STATE.yaml` plus the current `WeekXX/` or `UnitXX/` folder with note `.md`, `assets/`, and optionally `sources/`. A standalone `.md` is preview only when assets are required.

For the full specification, follow the **canonical standard file supplied with this package**. Do not hard-code an older standard filename.


## Ongoing course continuation
When continuing an existing course:
- Read the latest `COURSE_STATE.yaml` before writing.
- Treat accepted prior units as immutable unless the user explicitly requests revision.
- Process only the new Week/Unit by default.
- On first delivery, mark new unit/artifacts as `draft` in `COURSE_STATE.yaml`.
- When the user explicitly accepts a draft, immediately update the artifact/unit to `accepted` and return the updated `COURSE_STATE.yaml`; do not rebuild the Week/Unit ZIP solely for acceptance.
- Deliver `COURSE_CODE_WeekXX_Delivery.zip`; do not resend the full course bundle every week.
- In a new chat, authority order is: Global Standard > Course State > current source materials.
- Use the course Gold Reference to calibrate density and visual style, but never override the Global Standard.
