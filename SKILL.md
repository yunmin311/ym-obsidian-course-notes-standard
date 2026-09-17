# Skill：Obsidian 课程笔记编译器

当任务是把 Lecture / Tutorial / Reading / Lab 等课程材料整理成 Obsidian 笔记时，使用本 Skill。完整规则以本仓库的 **canonical standard** 为准，本文件只保留执行时必须快速检查的硬约束。

## 目标

生成可长期维护、可独立阅读、可直接放入 Obsidian 的课程讲义，而不是 PPT 摘要或聊天式解释。必须保持来源边界，真正讲清机制，并让视觉、公式、表格、代码各自承担最适合的信息。

## 强制规则

1. 写作前完整读取原始材料与最新 `COURSE_STATE.yaml`。
2. 默认删除行政信息；只有直接影响学习、assessment 或用户明确要求时保留。
3. 按知识逻辑重组，不按 slide 顺序机械抄写。
4. 第一次教学以连续正文为主；列表用于并列项/步骤；表格用于共享比较维度。
5. 只有确认视觉确实比 prose 更适合时，才进入视觉流程。
6. 视觉来源固定为：`课程原图 / 同源 PDF → 可信教材或官方外部原图 → 低风险静态 SVG → Manual Capture Required`。
7. Level 1 必须高分辨率渲染并识别 semantic envelope；公式、axis、unit、legend、caption、arrow、polarity、panel 等只要参与理解就必须完整保留。
8. 同一原图最多两次合理 recrop；仍无法同时做到完整和干净时，停止硬裁并升级 Level 2。
9. 外部图必须做 semantic equivalence check，确认模型、方向、极性、变量和边界条件与当前课程一致，并显式标注来源。
10. SVG 只用于低风险、结构明确、可逐项验证的简单图；PN junction 方向、器件内部机制、复杂电路、I–V curve、精确波形等高风险视觉默认不得自行重绘。
11. 每张视觉资产写入 Markdown 前都必须单独 QA；正式 ZIP 前再做一次全资产 visual audit / contact sheet review。
12. 图片显示尺寸按信息密度与 aspect ratio 自适应，不统一宽度。
13. MathJax 只用于真正的数学；普通方向、状态、英文术语使用正常 Markdown。
14. 公式必须先建立问题，再给公式，并解释关系、条件和实际意义。
15. 代码使用带语言标记的 fenced block；命令与输出分开。
16. Lecture、Tutorial、Lab 默认分开成文，除非用户明确要求合并。
17. 所有 assets 使用稳定相对路径；移动整个 Week/Unit 后链接仍必须有效。
18. 不得创建、覆盖或修改 `.obsidian/`。
19. 删除 AI 主持语、重复总结、过度粗体、emoji、callout spam 和大量单句段落。
20. 正式交付前验证 Markdown 引用、source dependencies、visual assets、MathJax、code fences 和 ZIP 自包含性。

## 交付结构与命名（硬约束）

`COURSE_STATE.yaml → structure.unit_scheme` 是整个命名体系的**唯一变量**，其余三段全靠派生：

| 段 | 模式 |
|---|---|
| 单元目录 | `{UnitPrefix}{NN}`，前缀由 `unit_scheme` 决定：`week→Week`、`lecture→Lecture`、`module→Module`、`chapter→Chapter`、`unit→Unit`、`custom→unit_prefix` |
| 笔记文件 | `{TypeLabel} {NN} - {Title}.md` |
| 资源文件 | `{SrcID}-p{NN}-{slug}.{ext}` |
| 来源文件 | `{COURSE_CODE}_{SrcID}_{Slug}.{ext}` |

21. `unit_scheme` 一旦该课程交付了第一个单元即**锁定**；同类前缀不得混用，序号两位零填充（`Week01` 不是 `Week1`）。
22. TypeLabel / SrcID 映射固定：`Lecture→L`、`Tutorial→T`、`Lab→LAB`、`Recitation→R`。
23. 笔记序号 `{NN}` 在**整门课程内按类型连续递增**，不是单元内递增：Week01 有 Lecture 01 与 02，Week02 就从 Lecture 03 开始。同类型序号不得重复。
24. 资源文件 `{SrcID}` 必须能在**同一单元**找到对应笔记；禁止跨单元引用资源。
25. `p{NN}` 是**原件真实页码**，必填。要么填对，要么整体省略（自制 SVG 用 `L01-store-and-forward.svg`）——**不用 `p00` 或任何占位值**。
26. 顺序编号（`01-campus-access-path.png`）不合规：既无来源标识也无页码。补齐 `sources/` 后一次性重命名并同步引用。
27. **`sources/` 无条件强制存在**，命名为 `{COURSE_CODE}_{SrcID}_{Slug}.{ext}`；每个 `{SrcID}` 都要有对应笔记。
28. **课程 `README.md` 延后**：单元交付不含 README，等整门课内容写完后单独生成一次。缺 README 不算缺陷。
29. 交付包名 `COURSE_CODE_Unit{NN}_Delivery.zip`，包内只有 `COURSE_STATE.yaml` + 单元目录。`assets/` 只放被引用的文件，不放草稿与中间产物。
30. 交付前对课程目录跑一次 `python scripts/check_course_structure.py <course_dir>`；任何 FAIL 必须修掉，`WARN` 必须在交付说明中列出。

## Visual QA Gate

每张最终视觉都必须通过：

- **Semantic completeness**：核心对象、公式、坐标、单位、caption、panel 等完整；
- **Technical correctness**：方向、极性、symbol、subscript、模型一致；
- **Visual cleanliness**：无断字、断线、黑边、无关残片；
- **Boundary safety**：四边有合理 breathing room，不贴边；
- **Adaptive sizing**：简单图不无意义放大，复杂图不缩到难读。

不通过就回到对应来源层级修复或升级，不能把半成品交给用户做第一次 QA。

## Source 依赖规则

`sources/` 无条件强制存在，不是"按需生成"。④ 的命名是 `{COURSE_CODE}_{SrcID}_{Slug}.{ext}`，`{SrcID}` 与 ③ 的 assets 前缀构成 join 关系。

如果任何已交付 Markdown 引用了 `sources/` 下的文件，被引用的 source file 必须包含在同一个 Delivery ZIP 中。外部视觉必须可追溯，并明确标记为 External Supplement；不要把外部图伪装成教师课件原图。

## 交付

包名：`COURSE_CODE_Unit{NN}_Delivery.zip`（`Unit` 为占位符，实际用 `unit_scheme` 对应前缀，如 `CSI201_Week02_Delivery.zip`）。

包内包含更新后的根目录 `COURSE_STATE.yaml`，以及当前单元文件夹（`.md`、`assets/`、`sources/`）。**不含课程 `README.md`。**

## 持续课程协同

继续已有课程时：读取最新 Course State；默认只处理新增 Week/Unit；新 artifact 首次交付为 `draft`；accepted artifact 不得静默修改；用户接受后只更新并返回 `COURSE_STATE.yaml`。权威顺序：Global Standard > Course State > 当前原始材料。Gold Reference 只校准当前课程的密度与视觉风格，不能覆盖 Global Standard。
