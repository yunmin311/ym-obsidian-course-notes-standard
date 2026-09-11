# Weekly Continuation SOP

本文件只解决一个问题：**课程每周持续增加材料时，同一对话或不同对话如何稳定协作，并持续输出可直接放进 Obsidian 的 ZIP。**

## Canonical Flow

```text
New Source Arrives
      ↓
Read Global Standard
      ↓
Read COURSE_STATE.yaml
      ↓
Identify Current Week / Material Type
      ↓
Source Map + Visual Triage
      ↓
Write Lecture / Tutorial / Lab
      ↓
Validate Markdown + Assets
      ↓
Update COURSE_STATE.yaml
      ↓
Build COURSE_CODE_WeekXX_Delivery.zip
      ↓
User extracts into course root
```

## Same-chat continuation

用户只需要上传本周材料并说：

> 按当前 Standard 和 Course State 继续 WeekXX。只生成本周新增内容，输出 Delivery ZIP 并更新 COURSE_STATE.yaml，不重发旧周。

Agent 不应重新询问已经固化的写作、视觉、SVG、公式、代码或目录规则。

## New-chat continuation

最稳妥的输入组合：

```text
1. Obsidian_Course_Notes_Standard_v2.1.md
2. 最新 COURSE_STATE.yaml
3. 本周新材料
```

如果 Standard 已经作为项目共享来源稳定可见，则只需要：

```text
COURSE_STATE.yaml + 本周材料
```

新 Agent 必须先读 Standard 和 Course State，再开始写。不能根据聊天习惯自行重造格式。

## Weekly / Unit Delivery ZIP

Week 制统一为 `COURSE_CODE_WeekXX_Delivery.zip`，Unit 制统一为 `COURSE_CODE_UnitXX_Delivery.zip`。

```text
COURSE_CODE_Week02_Delivery.zip
├─ COURSE_STATE.yaml
└─ Week02/
   ├─ Lecture 02 - ....md
   ├─ assets/
   └─ sources/
```

直接解压到课程根目录，允许新的 `COURSE_STATE.yaml` 覆盖旧版本。不要把旧 Week/Unit 每次全部重新打包。

## Source dependency check

If any delivered Markdown references a file under `sources/`, that referenced file must be present in the Delivery ZIP. `sources/` is optional only when no delivered artifact depends on it.

## Acceptance

新 Week/Unit 首次 Delivery 中，对应 unit 和 artifact 状态为 `draft`。正式文件始终使用 canonical 文件名，不通过 `v1/v2/final` 文件名表达状态。

用户明确确认后，Agent 必须立即：
- 将对应 artifact 改为 `accepted`；
- 只有当前要求的所有 artifacts 都 accepted 时，才把 unit 改为 `accepted`；
- 如有需要更新 Gold Reference；
- **单独返回更新后的 `COURSE_STATE.yaml` 即可，不重新打 Delivery ZIP。**

后续对话不得静默修改 accepted artifact；需要改动时先进入 revision，并把该 artifact 重新置为 `draft`。

## What persists across chats

只持久化会影响后续执行的内容：
- standard version；
- folder scheme；
- unit / artifact 的 draft / accepted 状态；
- gold reference；
- course-specific overrides；
- next expected unit；
- last delivery。

不把聊天历史、失败实验和已经废弃的方案塞进 state。
