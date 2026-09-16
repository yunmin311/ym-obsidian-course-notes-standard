# Weekly Continuation SOP

本 SOP 规定课程每周/每单元持续增加材料时的稳定交付流程。完整写作与视觉规则以当前 canonical standard 为准。

## Canonical Flow

```text
New Source Arrives
      ↓
Read Canonical Standard + COURSE_STATE.yaml
      ↓
Source Map + Knowledge Structure
      ↓
Visual Need Decision
      ↓
Level 1 Source Extraction
      ↓
Per-Asset Visual QA
      ↓
Escalate if needed: External Source → Low-risk SVG → Manual Capture
      ↓
Write Lecture / Tutorial / Lab
      ↓
Technical Validation + Final Visual Audit
      ↓
Update COURSE_STATE.yaml
      ↓
Build COURSE_CODE_WeekXX_Delivery.zip
```

## Same-chat continuation

用户只需要上传本周材料并说：

> 按当前 Standard 和 Course State 继续 WeekXX。只生成本周新增内容，输出 Delivery ZIP 并更新 COURSE_STATE.yaml，不重发旧周。

Agent 不应重新询问已经固化的写作、视觉、公式、代码或目录规则。

## New-chat continuation

最稳妥的输入组合：

```text
1. 当前 canonical Obsidian Course Notes Standard
2. 最新 COURSE_STATE.yaml
3. 本周新材料
```

如果 Standard 已经作为项目共享来源稳定可见，只需要 `COURSE_STATE.yaml + 本周材料`。新 Agent 必须先读 Standard 和 Course State，不能根据聊天习惯自行重造格式。

## Visual Pipeline

对每一个真正需要视觉表达的位置：

1. **Level 1：课程原图 / 同源 PDF**。高分辨率渲染，识别 semantic envelope，再裁图；每张图立即过 Visual QA Gate。
2. **最多两次 recrop**。两次仍无法同时做到完整、干净、边界安全，就停止硬裁。
3. **Level 2：可信外部原图**。优先教材/出版社、大学课程、OER、官方技术资料；必须验证模型、方向、极性、符号和边界条件一致，并记录来源。
4. **Level 3：低风险 SVG**。仅限结构明确、可逐项验证的简单图；复杂电路、器件内部机制、精确曲线等默认不重绘。
5. **Level 4：Manual Capture Required**。前三层都失败且该视觉不可替代时才使用，明确标注页码、对象和必须保留内容。
6. **Final Visual Audit**。正式 ZIP 前汇总 Markdown 实际引用的全部视觉资产，逐张打开或生成 contact sheet，全部通过后才交付。

## Weekly / Unit Delivery ZIP

Week 制：`COURSE_CODE_WeekXX_Delivery.zip`；Unit 制：`COURSE_CODE_UnitXX_Delivery.zip`。

```text
COURSE_CODE_Week02_Delivery.zip
├─ COURSE_STATE.yaml
└─ Week02/
   ├─ Lecture 02 - ....md
   ├─ assets/
   └─ sources/
```

直接解压到课程根目录，允许新的 `COURSE_STATE.yaml` 覆盖旧版本。不要把旧 Week/Unit 每次全部重新打包。

## Source dependencies

Markdown 只要直接引用 `sources/` 中某个文件，该文件就必须进入同一个 Delivery ZIP。外部视觉必须有来源记录；许可不明确的受版权限制图片不要直接重新打包分发。

## Acceptance

新 Week/Unit 首次 Delivery 中，对应 unit 和 artifact 状态为 `draft`。正式文件始终使用 canonical 文件名，不通过 `v1/v2/final` 文件名表达状态。

用户明确确认后：将对应 artifact 改为 `accepted`；当前要求的所有 artifacts 都 accepted 后再把 unit 改为 `accepted`；必要时更新 Gold Reference；只返回更新后的 `COURSE_STATE.yaml`，不重新打 Delivery ZIP。

后续对话不得静默修改 accepted artifact；需要改动时先进入 revision，并把该 artifact 重新置为 `draft`。
