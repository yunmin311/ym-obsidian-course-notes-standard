# Universal Obsidian Course Notes Standard v2.1 — Final Frozen

v2.1 已冻结。后续只有实际课程中出现新的**跨课程共性问题**时才升级 v2.2；单门课程的特殊要求全部进入 `COURSE_STATE.yaml → course_overrides` 或可选 `NOTE_STYLE_SPEC.md`。

核心文件：
- `Obsidian_Course_Notes_Standard_v2.1.md`：全局唯一 Canonical Standard。
- `SKILL.md`：给 Agent 的执行规则；引用“package 中的 canonical standard”，不再硬编码版本文件名。
- `TEMPLATE.md`：单份笔记最小骨架。
- `SOP_WEEKLY_CONTINUATION.md`：每周/每单元持续交付与跨对话协同。
- `COURSE_STATE_TEMPLATE.yaml`：课程状态模板，支持 unit 下多个 artifact 分别 draft / accepted。
- `HANDOFF_PROMPTS.md`：同对话、新对话、用户确认 draft 后的直接交接指令。

课程根目录必须保留 `COURSE_STATE.yaml`。Global Standard 不要求复制进每门课程目录，只要项目环境能够稳定访问即可。

增量交付命名统一：
- `COURSE_CODE_WeekXX_Delivery.zip`
- `COURSE_CODE_UnitXX_Delivery.zip`

新内容首次交付为 draft；用户确认后只更新并返回 `COURSE_STATE.yaml`，不为“accept”动作重新打 ZIP。

## Final freeze clarification

- Visual priority applies **only after deciding that a visual representation is needed**; prose remains the default carrier for first-time teaching.
- Any Markdown reference into `sources/` creates a hard packaging dependency: the referenced source file must be included in that Delivery ZIP.
- No further Global Standard changes are intended until a real cross-course common issue appears; course-specific differences belong in `course_overrides`.
