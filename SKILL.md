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

## Visual QA Gate

每张最终视觉都必须通过：

- **Semantic completeness**：核心对象、公式、坐标、单位、caption、panel 等完整；
- **Technical correctness**：方向、极性、symbol、subscript、模型一致；
- **Visual cleanliness**：无断字、断线、黑边、无关残片；
- **Boundary safety**：四边有合理 breathing room，不贴边；
- **Adaptive sizing**：简单图不无意义放大，复杂图不缩到难读。

不通过就回到对应来源层级修复或升级，不能把半成品交给用户做第一次 QA。

## Source 依赖规则

如果任何已交付 Markdown 引用了 `sources/` 下的文件，被引用的 source file 必须包含在同一个 Delivery ZIP 中。外部视觉必须可追溯，并明确标记为 External Supplement；不要把外部图伪装成教师课件原图。

## 交付

- Week 制：`COURSE_CODE_WeekXX_Delivery.zip`
- Unit 制：`COURSE_CODE_UnitXX_Delivery.zip`

包内包含更新后的根目录 `COURSE_STATE.yaml`，以及当前 `WeekXX/` 或 `UnitXX/` 文件夹（`.md`、`assets/`，以及按依赖需要包含的 `sources/`）。

## 持续课程协同

继续已有课程时：读取最新 Course State；默认只处理新增 Week/Unit；新 artifact 首次交付为 `draft`；accepted artifact 不得静默修改；用户接受后只更新并返回 `COURSE_STATE.yaml`。权威顺序：Global Standard > Course State > 当前原始材料。Gold Reference 只校准当前课程的密度与视觉风格，不能覆盖 Global Standard。
