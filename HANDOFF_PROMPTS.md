# Handoff Prompts

## 同一对话继续

> 按当前项目可访问的 canonical Obsidian Course Notes Standard 和最新 Course State 继续处理这些新材料（按 `unit_scheme` 决定的前缀命名单元目录）。只生成本次新增的 Lecture / Tutorial / Lab，不修改已 accepted 的旧 artifact。先完整读取材料并建立 Source Map；视觉只在确实需要时加入，并严格执行 `课程原图 / 同源 PDF → 可信教材或官方外部原图 → 低风险 SVG → Manual Capture Required`。每张最终视觉必须过 semantic completeness、technical correctness、visual cleanliness、boundary safety、adaptive sizing 五项 Gate；同一原图最多两次合理 recrop，仍失败就升级来源层级。资源文件命名 `{SrcID}-p{NN}-{slug}.{ext}`（页码必须是真实页码，不留占位值）；`sources/` 无条件强制存在，命名 `{COURSE_CODE}_{SrcID}_{Slug}.{ext}`。正式交付前对 Markdown 实际引用的全部视觉资产做 final audit，并过一遍 Structure & Naming Gate。更新 `COURSE_STATE.yaml`，输出 `COURSE_CODE_Unit{NN}_Delivery.zip`，不要重发整个课程总包，也不要生成课程 `README.md`。

## 新对话继续

> 你现在接手这门课程的持续笔记工作。先完整读取我提供/项目中可访问的 canonical Obsidian Course Notes Standard 和最新 `COURSE_STATE.yaml`；它们分别是全局规范和当前课程状态的权威来源。`COURSE_STATE.yaml → structure.unit_scheme` 是整个交付命名体系的唯一变量，单元目录前缀必须与它一致且锁定。再读取本次上传的新课程材料，只处理 `next_expected` 对应的新增内容，不重新设计笔记风格，不静默修改 accepted artifact。视觉处理必须自行完成来源分级、裁图 QA 和最终 contact-sheet / per-asset audit；不要把明显残缺图交给用户做第一次 QA。首次 Delivery 中新内容保持 draft，完成后更新 `COURSE_STATE.yaml` 并输出本单元自包含 ZIP（含 `sources/`，不含 `README.md`）。如果材料与 Course State 冲突，先指出冲突，不自行融合。

## 用户确认某个 Draft 后

> 用户已经明确接受当前 draft。不要重打 Week/Unit ZIP。立即把最新 `COURSE_STATE.yaml` 中对应 artifact 状态改为 `accepted`；如果本 unit 当前要求的所有 artifacts 都已 accepted，同时把 unit 状态改为 `accepted`；必要时更新 gold_reference。只返回更新后的 `COURSE_STATE.yaml`。
