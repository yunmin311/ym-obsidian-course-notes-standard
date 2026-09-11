# Handoff Prompts

## 同一对话继续

> 按当前项目可访问的 canonical Obsidian Course Notes Standard 和最新 Course State 继续处理这些 WeekXX / UnitXX 材料。只生成本次新增的 Lecture / Tutorial / Lab，不修改已 accepted 的旧 artifact。按 Standard 完成知识重写、PPT 裁图 / 静态 SVG / 表格 / 公式 / 代码等视觉分流，检查全部相对路径；首次交付把新 artifact 标记为 draft，更新 `COURSE_STATE.yaml`，最后输出 `COURSE_CODE_WeekXX_Delivery.zip` 或 `COURSE_CODE_UnitXX_Delivery.zip`。不要重发整个课程总包。

## 新对话继续

> 你现在接手这门课程的持续笔记工作。先完整读取我提供/项目中可访问的 canonical Obsidian Course Notes Standard 和最新 `COURSE_STATE.yaml`；它们分别是全局规范和当前课程状态的权威来源。然后读取本次上传的新课程材料，只处理 `COURSE_STATE.yaml` 中 `next_expected` 对应的新增内容；不要重新设计笔记风格，不要静默修改已经 accepted 的 artifact。首次 Delivery 中新内容保持 draft，完成后更新 `COURSE_STATE.yaml`，输出本周/本单元自包含的 Delivery ZIP。如果当前材料与 Course State 冲突，先指出冲突，不自行融合。

## 用户确认某个 Draft 后

> 用户已经明确接受当前 draft。不要重打 Week/Unit ZIP。立即把最新 `COURSE_STATE.yaml` 中对应 artifact 状态改为 `accepted`；如果本 unit 当前要求的所有 artifacts 都已 accepted，同时把 unit 状态改为 `accepted`；必要时更新 gold_reference。只返回更新后的 `COURSE_STATE.yaml`。
