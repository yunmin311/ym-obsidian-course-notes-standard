# Skill：Obsidian 课程笔记编译器

当任务是把 Lecture / Tutorial / Reading / Lab 等课程材料整理成 Obsidian 笔记时，使用本 Skill。

## 目标

生成可长期维护、可独立阅读、可直接放入 Obsidian 的课程讲义，而不是 PPT 摘要或聊天式解释。必须保持来源边界，真正讲清机制，并为不同内容选择合适的表达形式。

## 强制规则

1. 写作前先完整读取原始材料。
2. 默认删除行政信息；只有直接影响学习、assessment 或用户明确要求时保留。
3. 按知识逻辑重组，不按 slide 顺序机械抄写。
4. 第一次教学以连续正文为主；列表只用于并列项/步骤；表格只用于共享比较维度的内容。
5. 原课件有合适视觉时优先使用。PDF/PPT 必须高分辨率渲染后再处理。
6. **裁图必须以语义完整为第一条件。** 如果理解图还依赖相邻公式、变量、坐标、单位、legend、箭头、极性、panel、caption 或解释文字，这些内容必须一起保留。
7. math-heavy、circuit、waveform、plot、worked example、multi-panel figure 默认使用 **wide crop**，不要为了紧凑而过度裁切。
8. 如果无法安全局部裁切，按 `宽裁 / 半页裁图 → 嵌入原 PDF 页面 → 静态 SVG 重构` 处理。
9. 原图不可用且图示确实能明显提升理解时，才生成 **静态 SVG**；SVG 风格必须尽量继承原课件视觉语言，默认禁止动画。
10. 重要机制/拓扑在视觉质量重要时优先静态 SVG；Mermaid 只用于简单结构关系。
11. MathJax 只用于真正的数学。普通方向、状态、英文术语保留为 Markdown 文本。
12. 公式必须先建立问题，再给公式，并解释关系、条件和实际意义；例子只在有帮助时加入。
13. 代码使用带语言标记的 fenced block；命令与输出分开；只解释关键行为及其与课程概念的关系。
14. Lecture、Tutorial、Lab 默认分开成文，除非用户明确要求合并。
15. 所有 assets 使用稳定相对路径；移动整个 Week/Unit 后链接仍必须有效。
16. 不得修改 `.obsidian/`。
17. 删除 AI 主持语、重复总结、过度粗体、emoji、callout spam 和大量单句段落。
18. 视觉密度保持适中：正文由真正有用的图、表、公式、代码自然打断，而不是靠装饰 block 制造层级。

## 视觉决策顺序

**只有在确定需要视觉表达以后**，才按以下顺序选择：

`原课件安全裁图 → 原 PDF 页面 → 贴近课件风格的静态 SVG → 紧凑表格 / inline flow → Mermaid`

不要因为某一节“没有图”就强行生成图。

## 截图裁剪 Gate

裁图前必须检查：

- 裁完以后是否仍能在不打开原 slide 的情况下理解；
- 是否切掉任何公式、变量、axis、unit、legend、arrow、polarity、panel label、caption 或必要说明；
- multi-panel / paired comparison 是否被错误拆开；
- worked example 的条件、关系与图是否仍然完整。

只有全部通过，才允许 tight crop。否则使用 wide crop、半页裁图或 PDF page embed。

## 静态 SVG 规则

禁止默认动画、hover 才显示核心信息、嵌入字体文件、依赖 `foreignObject`、无关视觉主题。优先横向布局、紧凑居中画布，并继承课件的主色、accent 与 neutral。

## Source 依赖规则

如果任何已交付 Markdown 引用了 `sources/` 下的文件，被引用的 source file 必须包含在同一个 Delivery ZIP 中。只有当所有已交付笔记都不依赖 `sources/` 时，`sources/` 才可以省略。

## 交付

增量包命名：

- Week 制：`COURSE_CODE_WeekXX_Delivery.zip`
- Unit 制：`COURSE_CODE_UnitXX_Delivery.zip`

包内包含更新后的根目录 `COURSE_STATE.yaml`，以及当前 `WeekXX/` 或 `UnitXX/` 文件夹（`.md`、`assets/`，以及按依赖需要包含的 `sources/`）。

完整规范以本 package 中的 **canonical standard file** 为准，不要硬编码旧版本文件名。

## 持续课程协同

继续已有课程时：

- 写作前读取最新 `COURSE_STATE.yaml`；
- 已 accepted 的旧 artifact 默认不可静默修改；
- 默认只处理新增 Week / Unit；
- 首次交付时，新 unit / artifact 标记为 `draft`；
- 用户明确接受后，立即把对应状态改为 `accepted`，只返回更新后的 `COURSE_STATE.yaml`，不因为 accept 动作重新打 ZIP；
- 新对话的权威顺序：Global Standard > Course State > 当前原始材料；
- Gold Reference 只用于校准当前课程的密度和视觉风格，不能覆盖 Global Standard。
