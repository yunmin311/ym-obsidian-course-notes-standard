# Obsidian Course Notes Standard v3.1

> **Canonical Standard**  
> 适用于所有 Lecture / Tutorial / Reading / Lab / Coding 类课程笔记。  
> 目标不是“总结课件”，而是把原始教学材料重构为 **可长期维护、可复习、可追溯、视觉统一、直接放入 Obsidian 的高质量课程讲义**。  
> 全局 Standard 只定义跨课程共用规则；具体课程的正文密度与视觉基线由该课程 `COURSE_STATE.yaml → gold_reference` 决定。  
> **本版（3.1）相对上一版的唯一实质性变更**：把交付结构与文件命名从“示例性描述”升级为 **可机械校验的硬约束**（第 2 节重写），使命名体系既能适配 Week 以外的课程组织方式，又不会随课程漂移。视觉与写作规则未变。

---

## 0. 总原则

一份合格课程笔记必须同时满足五件事：

1. **知识正确**：不把模型补充、外部常识或推断伪装成课件原意。
2. **讲清机制**：不能只列定义和结论；关键知识要解释“为什么出现、内部怎样工作、结果是什么、与前后概念怎样连接”。
3. **视觉有来源层级**：优先保留当前课程原始材料中的高质量视觉；原图无法安全提取时，再检索可信教材、大学课程或官方技术资料中的等价图；SVG 只承担低风险、结构明确的简单图示。任何视觉资产在进入笔记前都必须通过独立 QA。
4. **Obsidian 稳定**：所有链接使用相对路径；Markdown、MathJax、图片和 SVG 在 Obsidian 中可直接渲染；不得依赖本机绝对路径。
5. **密度适中**：正文不能碎成知识卡片，也不能变成连续的大段墙。有当前课程 Gold Reference 时以其密度为校准；没有 Gold Reference 时采用 moderate density：连续解释为主，必要时用表格、图、公式、短流程形成自然视觉停顿。

判断任何格式是否应该出现，只问一个问题：

> **它是否比连续正文更准确、更快地表达当前信息？**

如果答案是否定的，就不用。

---

# 1. 来源边界与知识可信度

## 1.1 来源优先级

每份笔记必须区分以下来源：

**Primary Source**：当前 Lecture / Tutorial / Reading / Lab 原始材料。正文默认只依据这一层。

**Course Supplement**：同课程教材、教师补充材料、官方 handout。只有当原材料明确需要补充或用户要求补充时使用。

**External Supplement**：教材外常识、模型解释、网页资料、其他课程知识。必须显式标为“补充”，不能静默混入老师内容。

**Inference**：根据原材料做出的推断。如果原材料没有足够证据，不得写成确定事实。

Lecture、Tutorial、Lab 默认分开成文。Tutorial 题目不混进 Lecture 正文；Lab 操作步骤不挤进理论 Lecture；Reading 中独有的观点不能自动升格为课程结论。

## 1.2 原材料存在错误或缺失

遇到明显 typo、公式缺项、图文矛盾、术语漂移时：

- 不偷偷纠正；
- 正文保留老师原意；
- 在必要位置标明“课件此处可能有排版/符号问题”；
- 如果给出修正，只能标为补充或校正说明。

## 1.3 行政信息默认删除

Lecture 1 常见的教师邮箱、TA、课程安排、办公室联系方式、分组通知、课堂礼仪等，默认不进入知识笔记。

只有以下内容可以保留：直接影响学习与 assessment 的规则、公式表允许情况、AI 使用限制、考试形式、项目要求、必须掌握的软件/语言。如果用户明确要求“纯知识笔记”，连这些也删除。

---

# 2. 文件与交付结构

本节是**硬约束**，不是建议。第 2.4 与 2.7 节的命名规则必须能机械校验，因此每条规则都给出明确判定条件。

## 2.1 课程根目录

```text
COURSE_CODE/                          # 目录名 = course_code，全大写
├─ COURSE_STATE.yaml                  # [必需]
├─ README.md                          # [延后] 见 2.2
├─ NOTE_STYLE_SPEC.md                 # [可选] 仅课程特例
├─ Unit01/                            # [必需] 至少一个；前缀由 unit_scheme 决定
│  ├─ Lecture 01 - Topic.md           # [必需] 至少一个
│  ├─ Tutorial 01 - Topic.md          # [条件] 该单元有 tutorial 时必需
│  ├─ Lab 01 - Topic.md               # [条件] 该单元有 lab 时必需
│  ├─ assets/                         # [条件必需] 见 2.5
│  └─ sources/                        # [强制] 见 2.6
└─ Unit02/
   └─ ...
```

**必需项判定**：

| 项 | 必需性 | 判定 |
|---|---|---|
| 课程根目录名 | 必需 | 必须等于 `COURSE_STATE.yaml → course_code` |
| `COURSE_STATE.yaml` | 必需 | 必须在课程根，**文件名不可更改** |
| 单元目录 | 必需 | 至少一个；命名见 2.4 |
| 单元内 `.md` | 必需 | 每个单元至少一个；命名见 2.4 |
| `assets/` | 条件必需 | 该单元任一 `.md` 引用了图片 / SVG 时必须存在 |
| `sources/` | **强制** | 无条件必需，见 2.6 |
| `README.md` | 延后 | 见 2.2 |
| `NOTE_STYLE_SPEC.md` | 可选 | 仅当存在 `course_overrides` 时 |

每个单元必须自包含：**单独移动整个单元目录后，Markdown、assets、sources 仍然全部有效。**

不得创建、覆盖或修改 `.obsidian/`。

## 2.2 课程 README 的生成时机（延后）

`README.md` 是课程交付的一部分，但**不在单元增量交付中生成**。

规则：

- 单元交付不含 `README.md`；不要为了“结构完整”提前造一个空壳 README。
- 当该课程**所有计划内容全部写完**（课程结束或用户明确宣告完结）后，才单独生成一次课程 `README.md`。
- 该 README 描述整门课的最终状态，因此必须基于全部已 accepted 的内容来写，而不是基于某一个单元。
- 在课程未完结期间，缺少 `README.md` **不构成结构缺陷**，不得被校验器判为 FAIL。

## 2.3 交付包命名

```text
COURSE_CODE_Unit{NN}_Delivery.zip
```

`Unit{NN}` 中的 `Unit` 为占位符，实际使用由 `unit_scheme` 决定的单元前缀（见 2.4）。

示例：

```text
CSI201_Week02_Delivery.zip
SOE205_Module03_Delivery.zip
EEE211_Lecture05_Delivery.zip
```

用户只需要：

`下载 → 解压 → 整个文件夹内容放进课程根目录`

单独 `.md` 可以额外提供预览，但不能作为唯一正式交付，因为它会失去图片和 sources。

## 2.4 单元目录与文件命名（四段派生模型）

整套命名只有**一个变量**：`COURSE_STATE.yaml → structure.unit_scheme`。其余三段全部从笔记文件名派生。

```text
唯一变量                    派生段
unit_scheme  ──▶  ① 单元目录名
笔记文件名   ──▶  ② 笔记文件 / ③ 资源文件 / ④ 来源文件
```

### 所谓“四段”

| 段 | 模式 | 示例 |
|---|---|---|
| ① 单元目录 | `{UnitPrefix}{NN}` | `Week01` |
| ② 笔记文件 | `{TypeLabel} {NN} - {Title}.md` | `Lecture 01 - Network Performance.md` |
| ③ 资源文件 | `{SrcID}-p{NN}-{slug}.{ext}` | `L01-p15-bandgap.png` |
| ④ 来源文件 | `{COURSE_CODE}_{SrcID}_{Slug}.{ext}` | `CSI201_L01_Network_Performance.pdf` |

### ① 单元目录：唯一变量

`unit_scheme` 取值是**封闭枚举**，不允许自由文本：

| `unit_scheme` | 单元目录前缀 | 适用组织方式 |
|---|---|---|
| `week` | `Week` | 按教学周排课（当前四门课程） |
| `lecture` | `Lecture` | 一讲一目录，无“周”概念 |
| `module` | `Module` | 模块化课程 |
| `chapter` | `Chapter` | 教材章节驱动 |
| `unit` | `Unit` | 通用兜底 |
| `custom` | 由 `structure.unit_prefix` 指定 | 仅在以上都不适用时使用 |

规则：

- 单元目录名 = `{UnitPrefix}` + **两位零填充序号**：`Week01`、`Module03`、`Chapter12`。
- `custom` 必须同时设置 `structure.unit_prefix`，并在 `course_overrides` 中记录原因。
- **同一课程内不得混用前缀。** 一旦该课程交付了第一个单元，`unit_scheme` 即被锁定；后续改变需要显式迁移，不允许悄悄换。
- 不允许出现 `Week1` / `week01` / `WEEK01`：必须是大写开头前缀 + 两位数字。

这样设计的理由：未来出现非 Week 课程时，只需在 `COURSE_STATE.yaml` 改一个枚举值，其余命名规则完全不动；同时因为枚举封闭，命名不会随不同 Agent 的措辞漂移。

### ② 笔记文件

```text
{TypeLabel} {NN} - {Title}.md
```

**TypeLabel 枚举与 SrcID 派生表**（写死，不可扩展）：

| TypeLabel | SrcID | 示例 |
|---|---|---|
| `Lecture` | `L` | `Lecture 03 - ...` → `L03-` |
| `Tutorial` | `T` | `Tutorial 02 - ...` → `T02-` |
| `Lab` | `LAB` | `Lab 01 - ...` → `LAB01-` |
| `Recitation` | `R` | `Recitation 01 - ...` → `R01-` |

**序号规则：`{NN}` 在整门课程内按类型连续递增，不是单元内递增。**

```text
Week01/Lecture 01 - ...md
Week01/Lecture 02 - ...md      ← 同单元可以有两个 Lecture
Week02/Lecture 03 - ...md      ← 跨单元继续数，不回到 01
```

`{NN}` 必须两位零填充。同一课程内，同一 TypeLabel 的序号不得重复。

`{Title}` 使用课件原始标题的自然写法，保留大小写与专有名词，不用连字符替换空格。

### ③ 资源文件（assets）

```text
{SrcID}-p{NN}-{slug}.{ext}
```

| 成分 | 含义 | 规则 |
|---|---|---|
| `{SrcID}` | 来源标识 | 由 ② 派生，如 `L01` / `T01` / `LAB03` |
| `p{NN}` | 原件页码锚点 | **必填**，两位或三位零填充，如 `p08` / `p104` |
| `{slug}` | 内容描述 | 小写英文，连字符分词，不用中文、不用空格、不用大写 |

示例：

```text
L01-p15-bandgap.png
L01-p22-pn-junction.png
T01-p08-load-line.png
LAB03-p04-client-server-flow.svg
```

规则：

- `{SrcID}` 必须能在**同一单元**的笔记文件中找到对应来源；跨单元引用不被接受。
- `p{NN}` 是**原件页码**，用于追溯该图来自哪一页。
- 若同一页导出多张图，用 slug 区分，不重复序号：`L01-p15-bandgap.png` / `L01-p15-bandgap-detail.png`。
- 禁止使用 UUID、哈希、`image1` / `figure2` / `截图` 之类无语义名。

### 2.4.1 无法确定页码时的处理

`p{NN}` 的语义是“**这一页**的原件”，因此**不接受占位值**。不要为了凑格式写 `p00`。

| 情况 | 处理 |
|---|---|
| 有原件 PDF，图是原件截图 | 填真实页码 |
| 有原件 PDF，但图跨页 / 无法定位单页 | 填该图**起始页** |
| 图是自制 SVG（非原件截图） | 省略 `p` 段：`L01-store-and-forward.svg` |

即：**页码段要么是真实页码，要么整体不出现；不允许出现无意义编号。**

> 这一条是 v3.1 相对旧实践的收紧点。旧版曾出现 `L01-store-forward.svg` 这类省略页码的写法，现予以确认合法；但**顺序编号**（如 `01-campus-access-path.png`）不合法，因为它既不含来源标识也不含页码。

### 2.4.2 迁移说明：顺序编号资源

部分历史单元在 `sources/` 缺失时退化使用了顺序编号（`01-xxx.png`、`07-xxx.svg`）。这类文件不满足 ③ 的规则。

处理原则：

- **不强制立即重命名。** 缺少原件 PDF 时无法填出真实页码，强行改写只会产生假页码。
- 在补齐 `sources/` 后**一次性**重命名，并同步更新笔记中的引用。
- 在校验器中被判为 `WARN` 而非 `FAIL`，直到该单元补齐 `sources/`。

## 2.5 assets 目录规则

- `assets/` 只存该单元笔记实际引用的资源。
- 不存放未使用的中间产物、原图副本、contact sheet、草稿版本。
- 引用一律使用相对路径，且必须能从单元目录解析。
- 禁止跨单元引用：需要复用图时，复制进目标单元的 `assets/`。

## 2.6 sources 目录规则（强制）

**`sources/` 无条件必需。** 只要该单元有笔记文件，就必须存在 `sources/`。

理由：`sources/` 是笔记可追溯性的物理基础。③ 的 `p{NN}` 页码锚点只在原件存在时才有意义；没有原件，整个“可追溯”承诺就无法成立。

命名（④ 段）：

```text
{COURSE_CODE}_{SrcID}_{Slug}.{ext}
```

示例：

```text
CSI201_L01_Network_Performance.pdf
CSI201_L02_Protocol_Layers.pdf
EEE211_L01_Semiconductor_Materials.pdf
EEE211_T01_Diode_Circuit_Analysis.pdf
```

规则：

- `{COURSE_CODE}` 与该课程根目录名一致。
- `{SrcID}` 与 ③ 中的来源标识一致，两者构成 join 关系。
- `{Slug}` 取自该笔记的 `{Title}`，下划线分词。
- 保留原件扩展名；不要转码、不要重压缩。

**Source dependency hard rule**：如果任何已交付 Markdown 引用了 `sources/` 下的文件，该文件必须包含在同一个 Delivery ZIP 中。反之，`sources/` 仍必须存在——其中可只放原件本身（原件通常不直接被 `.md` 引用，而是作为 ③ 的提取来源和页码依据）。

## 2.7 结构校验规则

以下规则应能由脚本机械判定，用于 CI 或交付前自检：

| ID | 检查 | 判定 |
|---|---|---|
| U1 | 磁盘上每个单元目录去尾数字后的前缀，必须等于 `unit_scheme` 映射结果 | FAIL：前缀与声明不符 |
| U2 | 同一课程内所有单元目录前缀必须一致 | FAIL：出现两种前缀 |
| U3 | `COURSE_STATE.yaml` 的 `completed[].unit` 与 `next_expected.unit` 前缀必须同 U1 结果 | FAIL：状态与磁盘不一致 |
| U4 | 单元序号必须两位零填充 | FAIL：`Week1` / `week01` |
| N1 | 每个单元目录下必须存在 `.md` 文件 | FAIL：空单元 |
| N2 | `{NN}` 在同一课程的同一 TypeLabel 内不得重复 | FAIL：编号冲突 |
| A1 | `assets/` 下每个文件名必须匹配 `{SrcID}-(p\d{2,3}-)?{slug}\.{ext}` | WARN：顺序编号；FAIL：其他 |
| A2 | `assets/` 中每个 `{SrcID}` 必须能在同单元 `.md` 文件名中找到来源 | FAIL：孤儿资源 |
| A3 | `assets/` 不得存在未被任何 `.md` 引用的文件 | WARN：未使用资源 |
| S1 | 每个单元目录必须存在 `sources/` | FAIL：缺失 |
| S2 | `sources/` 内文件名必须匹配 `{COURSE_CODE}_{SrcID}_{Slug}\.{ext}` | WARN：不合规命名 |
| S3 | `sources/` 中每个 `{SrcID}` 必须有对应的 `{TypeLabel} {NN}` 笔记文件 | FAIL：孤儿来源 |
| R1 | 课程根 `README.md` 缺失 | **不检查**（见 2.2，延后生成） |
| R2 | `COURSE_STATE.yaml` 必须存在于课程根且文件名精确 | FAIL：改名或缺失 |

`WARN` 不阻断交付，但必须在交付说明中指出。

规则的参考实现是 `scripts/check_course_structure.py`，用法：

```bash
python scripts/check_course_structure.py <course_dir>
python scripts/check_course_structure.py --self-test   # 自检，CI 使用
```

该脚本不依赖第三方库，可直接对任意课程目录运行；`--self-test` 会构造夹具逐条验证每条规则**能够真的报错**（只报绿不报红的校验器比没有校验器更危险）。

---

# 3. 正文写作标准

## 3.1 笔记不是 PPT 翻译

禁止逐页写：

```text
Slide 17: ...
Slide 18: ...
Slide 19: ...
```

应先识别整讲的知识主线，再按理解顺序重组。页码只用于图片来源和必要追溯。

例如一讲的真实主线可能是：

`Network → Edge → Access → Core → Packet Switching → Routing`

而不是：

`Page 16 → Page 17 → Page 18 ...`

## 3.2 段落密度

默认一个完整思想写成一个自然段，通常 **3–6 句**。一个重要机制可以连续写 2–4 段，但不要每句话换行。

允许单独成行的内容只有：

- 关键公式；
- 极短的因果链或通信路径；
- 图片；
- 表格；
- 必须强调的一句原课件结论；
- 代码块 / terminal block。

避免两种极端：

**过碎：**

```markdown
Router 收到 packet。

然后查表。

然后转发。
```

**过密：**

连续 20 行正文没有任何视觉停顿。

正确做法是：正文负责教学，表格 / 图 / 公式在自然节点插入，让视觉产生节奏。

## 3.3 标题层级

`#`：一份文档唯一标题。  
`##`：真实的大知识阶段。  
`###`：阶段内部确实需要独立理解的子机制。  
`####`：仅用于长推导、复杂例题或代码模块，默认少用。

禁止“一知识点一标题”。如果一个标题下只有一两句话，通常应并回上一级正文。

标题优先写知识对象，不写主持式标题。例如：

推荐：

```markdown
## Packet Switching
### Store-and-Forward
```

不推荐：

```markdown
## 我们先来看 Packet Switching 到底是什么
### 这里最重要的一点
```

## 3.4 重点如何体现

重点主要靠四种方式体现：

1. 在正文中自然增加解释深度；
2. **粗体**标出真正需要快速定位的术语或结论；
3. 用图 / 表 / 公式承载结构；
4. 必要时用一个短引用块提醒易错点。

不要依靠 emoji、彩色符号、大量 `✅ ⚠️ ❌` 或“核心重点！！”制造重点。

默认每段粗体不超过 1–3 处；整页不能红黄高亮成一片。

## 3.5 AI 口吻清理

删除不推进知识的主持语：

- “这里我们可以看到”
- “真正重要的是”
- “本质上”
- “值得注意的是”
- “简单来说”
- “这告诉我们”
- “接下来我们来看看”
- “总结一下”
- “需要我继续吗”

这些词不是绝对禁词，但如果删掉以后不影响逻辑，就必须删。

---

# 4. 内容类型选择矩阵

不同信息必须使用不同承载方式。默认选择如下：

|内容类型|首选格式|第二选择|避免|
|---|---|---|---|
|概念解释|连续正文|短定义引用|bullet dump|
|并列属性|表格 / 短列表|正文|每项单独标题|
|因果机制|正文 + 原课程图 / 可信外部图|低风险静态 SVG / 短流程|纯 bullet|
|时间/步骤流程|原课程图 / 可信外部图|静态 SVG / 编号步骤|动画|
|协议交互|原课程图 / 官方资料图|Sequence-style 静态 SVG / 横向流程|长文字来回描述|
|概念对比|表格 + 一段解释|双栏 SVG|重复两遍正文|
|公式|MathJax + 解释|源图|截图公式|
|公式推导|MathJax aligned|逐行公式|只给最终式|
|实验/例题|条件 → 判断 → 计算 → 结果解释|表格|只给答案|
|代码|语言代码块 + 必要解释|伪代码|截图代码|
|终端命令|shell / powershell block|inline code|把输出混进命令|
|程序输出|text block|表格|与代码混在同一块|
|算法过程|伪代码 / 静态流程图|代码|长篇 prose|
|数据对比|表格|图表|无理由做饼图|
|趋势/函数关系|原课程图 / 教材或官方 plot|MathJax / verified static plot|纯口述|
|网络拓扑/结构|原课程图 / 官方资料图|低风险静态 SVG|大面积 Mermaid 默认图|
|状态机|原课程图 / 官方资料图|静态 SVG / Mermaid|动画|
|警告/边界条件|短引用或 callout|正文粗体|整页 callout|
|整页 PPT 都有价值|嵌入 PDF page|整页截图|重新抄写整页|

---

# 5. 图片与视觉资产标准

视觉资产不是装饰，也不是“有图就比没图好”。它必须承担正文难以替代的信息，并且在来源、完整性和技术正确性上可追溯。**视觉选择只发生在已经确认“这一处确实需要视觉表达”之后；第一次教学仍以正文为默认载体。**

## 5.1 Visual Source Hierarchy

所有课程统一使用以下四级来源层级。Agent 必须自行判断是否升级，不把明显不合格的候选图交给用户做第一次 QA。

### Level 1 — 当前课程原始材料

第一优先级永远是当前课程的 PPT / PDF / handout / teacher-provided figure。

优先动作：

1. 以高分辨率渲染源页；
2. 识别当前知识点真正需要的 semantic object；
3. 连同必要公式、标签、caption、坐标、箭头、极性和关联 panel 一起裁出；
4. 删除明确无关的 slide 外壳、标题、页码、logo、装饰和无意义空白；
5. 裁完后重新视觉审查，而不是直接写入 Markdown。

同源 PDF page embed 也属于 Level 1。当一个视觉对象无法从整页安全分离，或者“图 + 公式 + caption + 多 panel”本来就是一个完整教学单元时，可直接嵌入 source page，而不是强行切碎。

### Level 2 — 可信外部原图

如果 Level 1 经过 **最多两次合理裁切尝试** 仍不能同时满足“语义完整 + 视觉干净 + 边界安全”，停止继续猜 crop，升级到外部检索。

优先来源：

1. 本课程指定教材、教材配套资源、出版社/作者公开资源；
2. 大学公开课程、官方 handout、OpenCourseWare / OER；
3. 器件厂商、标准组织、官方技术文档；
4. 其他高可信技术资料。

外部图进入笔记前必须做 **semantic equivalence check**：

- 是否讲的是同一个概念和同一种模型；
- 电流、电场、极性、方向、符号约定是否一致；
- 坐标定义、变量、边界条件和近似条件是否一致；
- 是否因为教材版本或领域约定不同而产生潜在歧义。

只要这些条件存在不确定，就不能用“看起来差不多”的外部图替代课程原图。

外部视觉必须显式标注为 **External Supplement** 并记录来源。只有在允许合理再分发的前提下才把图像文件直接打进 `assets/`；如果许可不明确，不应把受版权限制的教材图重新打包分发，可改用链接/引用，或继续升级到 Level 3 / Level 4。

### Level 3 — 静态 SVG / 可控重绘

SVG 的优先级低于可信外部原图。它只适合 **低风险、结构明确、不会因一个箭头或极性画错就改变知识结论** 的图，例如：

- 简单 block diagram；
- 清晰的流程或层级关系；
- 无歧义的 architecture overview；
- 由正文明确数据直接构成的简单示意。

以下高风险内容默认不得为了“有图”而自行重绘：

- PN junction / carrier movement / electric field direction；
- 极性、电流方向、器件内部机制；
- 复杂电路拓扑；
- I–V characteristic、精确坐标图、波形、实验曲线；
- 多 panel 中依赖空间关系的技术图；
- 任何 Agent 无法逐项验证的图。

只有当重绘内容可以逐项对照可靠 source 验证，才允许使用 SVG。

### Level 4 — Manual Capture Required

前三层都无法得到可信视觉、但该图对理解又不可替代时，才允许把该处交给用户人工截图。

这种情况必须极少，并在 draft 中明确标记：

```markdown
> **待补原图：** 请从 Lecture XX p.XX 截取 [具体对象]，需保留 [必须保留的信息]。
```

不能用残缺图、错误 SVG 或无来源替代图掩盖失败。

---

## 5.2 Semantic Envelope：先判断“什么必须一起保留”

截图裁剪的第一原则是 **semantic completeness first**，而不是“尽可能紧”。当前视觉对象的 semantic envelope 包含所有离开后会改变理解的信息，例如：

- 相邻公式、变量定义、推导步骤；
- 坐标轴、刻度、单位、legend；
- 下标、上标、希腊字母、符号说明；
- 箭头、电流方向、电场方向、polarity；
- 区域边界、depletion width、reference line；
- panel 编号与左右/上下比较关系；
- caption、figure title、短说明；
- worked example 的已知条件、约束与结论；
- 与图不可分离的电路、波形、paired comparison。

**裁完后必须能在不重新打开原 slide 的情况下正确理解该图。** 做不到就说明当前 crop 无效。

## 5.3 Crop Strategy

### 5.3.1 Tight crop 只用于真正独立的小对象

可以紧裁的对象：单一 block、独立小结构图、单张 topology、主体和全部标签天然集中在一个区域的图。

即使 tight crop，也不能让文字、箭头、线条、坐标或 caption 贴边。必须保留可见的 breathing room。

### 5.3.2 Wide crop 是技术图的默认策略

以下类型默认使用 wide crop，不追求极致紧凑：

- math-heavy figure；
- circuit diagram；
- waveform / timing diagram；
- function graph / plotted figure；
- worked example；
- multi-panel comparison；
- 公式与图形联合出现的页面；
- 含大量边界标签、方向、单位或 caption 的技术图。

如果两个 panel 在语义上共同解释同一机制，优先裁成一张横向组合图，不为了“图片更小”强行拆开。

### 5.3.3 Boundary Safety

进入 Markdown 前必须检查四边：

- 任何文字行、公式、坐标、曲线、箭头或 circuit wire 都不能被边界截断；
- meaningful foreground 不应紧贴画布边缘；
- 不得留下半截文字、半个 panel、半条坐标轴或一小块无关 slide 残片；
- 不得因为去除黑边而切掉 source content；
- 技术图宁可多留一圈合理白边，也不要贴边。

经验上，最终 crop 应留出与源图视觉密度协调的安全边距。Agent 不应机械使用固定像素值，而应根据原图字号、线宽和 panel 间距判断。

## 5.4 Visual QA Gate

**每一张最终资产都必须在写入 Markdown 前单独过 Gate。** “已经生成文件”不等于“可以使用”。

### Gate A — Semantic completeness

- 主要对象是否完整；
- 公式、变量、axis、unit、legend、caption 是否保全；
- multi-panel 是否被错误拆分；
- 该图脱离原 slide 后是否仍能独立读懂。

### Gate B — Technical correctness

- 电流、电场、箭头、极性是否正确；
- symbol / subscript / superscript 是否正确；
- 外部图是否与本课件模型和约定一致；
- SVG / 重绘是否能逐项对照可靠 source。

### Gate C — Visual cleanliness

- 无黑边、断字、断线；
- 无无关文字残片；
- 无明显失衡空白；
- 不把 slide 标题、logo、页码留进图，除非它们本身有教学意义。

### Gate D — Boundary safety

四边都要留出合理 breathing room；任何接近被切断的元素都视为失败，而不是“勉强能看”。

### Gate E — Adaptive sizing

图片显示大小由 **信息密度、aspect ratio、阅读距离** 决定，而不是统一宽度。

建议范围仅作为默认参考：

- 小型独立示意：约 280–420 px；
- 单个电路 / 单图机制：约 420–620 px；
- 完整 graph / multi-panel / 横向技术图：约 620–820 px；
- 极复杂且必须全宽阅读的图：可接近正文全宽。

同一篇笔记允许不同图片使用不同宽度。简单图不要无意义放大，复杂图也不能为了版面整齐而缩到看不清。

## 5.5 Pre-delivery Visual Audit

正式 ZIP 前，Agent 必须进行一次 **全资产视觉审计**：

1. 汇总本次 Markdown 实际引用的所有视觉资产；
2. 逐张打开或生成 contact sheet；
3. 按 Gate A–E 复查；
4. 任一资产失败时，回到对应来源层级修复或升级；
5. 只有全部引用资产通过后，才允许进入正式 Delivery。

审计必须覆盖 **实际被 Markdown 引用的最终文件**，不能只检查中间候选图。

## 5.6 Source 依赖与来源标注

课程原始材料和外部材料都需要可追溯：

- 当前课程 source file 被 Markdown 直接引用时，必须随 Delivery 打包；
- 外部图必须在正文相邻位置标明来源和“External Supplement”；
- 外部来源 URL / 书名 / 章节应足够让下一位 Agent 或用户重新定位；
- 不把外部图伪装成教师课件原图。

图片文件名应继续保持课程内唯一、可读、可追溯。

---

# 6. 静态 SVG 规范

SVG 是 **Level 3 fallback**，不是原图裁切失败后的默认第一选择。它的目标是补足低风险视觉表达，不是替换已有的可靠技术图。

## 6.1 允许使用 SVG 的条件

只有同时满足以下条件时才使用：

- Level 1 原课程视觉无法安全使用，或原材料本身没有图；
- Level 2 没有找到语义一致、来源可信且适合使用的外部图；
- 图的结构足够简单，Agent 可以逐项验证；
- 重绘不会因为一个方向、极性、坐标或符号错误而改变知识结论。

如果不能逐项验证，停止生成，进入 Level 4。

## 6.2 总风格

SVG 不是另起一套视觉设计，而是尽量继承当前课程已有视觉语言：主色、accent、neutral background、线条粗细、字号层级和箭头形态。如果课件没有稳定风格，使用中性课程默认：透明或极浅背景、深灰/深蓝文字、单一主色、最多一个 accent。

禁止为了“高级感”加入霓虹、复杂渐变、玻璃、拟物、过度阴影或大面积装饰。

## 6.3 布局与文字

优先横向（left-to-right），只有因果层级天然从上到下或横向严重拥挤时使用纵向。

SVG 必须：

- 紧凑居中，不贴边；
- 节点间距稳定，箭头不穿过文字；
- 使用系统无衬线字体，不嵌入字体文件；
- 一张图最多 2–3 个字号层级；
- 长解释留在正文，不塞进图。

## 6.4 技术正确性 Gate

SVG 输出后必须和 source / 公式逐项核对：

- node 是否缺失；
- arrow direction 是否正确；
- polarity / sign / symbol 是否一致；
- label 是否有拼写、下标或单位错误；
- 是否存在 Agent 自行补出的未经 source 支持的信息。

任何一项无法验证，SVG 不得进入正式笔记。

## 6.5 禁止项

禁止：默认动画、moving packet、blinking node、hover 才显示核心信息、复杂 filter、必要依赖 `foreignObject`、过度圆角卡片化、颜色失控，以及用 SVG 重绘高风险技术图来掩盖原图提取失败。

---

# 7. Mermaid 使用标准

Mermaid 不是默认视觉方案。它适合**简单、结构性强、无需精确视觉风格**的关系，例如 dependency、简单 state graph、项目流程。

优先级：

`在确实需要视觉表达时：当前课程原图 / 同源 PDF > 可信外部原图 > 低风险静态 SVG > 紧凑表格 / inline flow > Mermaid > Manual Capture Required`

对于课程核心机制、网络拓扑、电路、协议 sequence，优先使用可验证的课程原图或官方/教材原图；SVG 只用于低风险且可逐项验证的结构。

使用 Mermaid 时：

- 优先 `flowchart LR`；
- 节点控制在 4–8 个；
- 避免巨大纵向树；
- 不在节点里塞长段落；
- 不依赖复杂 theme；
- 必须在 Obsidian Reading View / Live Preview 可渲染。

---

# 8. 表格标准

表格只在**多个对象共享相同比较维度**时使用。

适合：
- Forwarding vs Routing；
- Ethernet / Wi-Fi / FTTH；
- 二极管模型对比；
- protocol fields；
- layer responsibilities。

不适合：
- 第一次解释一个复杂机制；
- 一列只有一个词；
- 强行把 prose 切成表格。

推荐：

|维度|Forwarding|Routing|
|---|---|---|
|范围|当前 router|端到端路径|
|核心问题|下一 hop 去哪里|整条 path 怎样选|
|性质|Local decision|Path selection|

表格之后如存在因果区别，必须继续用正文解释，不让表格替代理解。

---

# 9. 公式与数学推导标准

## 9.1 什么时候使用 MathJax

只有数学对象使用公式。

正确：

```markdown
电场方向：N 区 → P 区
```

错误：

```latex
$$
\mathrm{N\ region}\rightarrow\mathrm{P\ region}
$$
```

Inline math：

```markdown
室温下 $V_T \approx 26\,\text{mV}$。
```

Display math：

```markdown
$$
V_{bi}=V_T\ln\left(\frac{N_aN_d}{n_i^2}\right)
$$
```

普通英文术语不塞进 `\mathrm{}` / `\text{}` 公式里做装饰。

## 9.2 一个公式的完整写法

关键公式通常按以下顺序出现：

**现象 / 问题 → 公式 → 变量 → 公式表达的关系 → 适用条件 → 例子（如果必要）**

不是所有公式都必须机械写六项，但不能只甩最终式。

例如：

二极管正向电流随电压指数变化：

$$
i_D=I_S\left(e^{v_D/(nV_T)}-1\right)
$$

其中 $I_S$ 是反向饱和电流，$n$ 是 ideality factor，$V_T$ 是 thermal voltage。式子最重要的信息不是符号本身，而是 **$v_D$ 的小幅变化可以引起 $i_D$ 的指数级变化**。

## 9.3 推导

长推导使用 `aligned`，每一步只保留真正有意义的变换：

```latex
$$
\begin{aligned}
i_D &= I_S e^{(V_{DQ}+v_d)/V_T} \\
    &= I_{DQ}e^{v_d/V_T} \\
    &\approx I_{DQ}\left(1+\frac{v_d}{V_T}\right)
\end{aligned}
$$
```

推导之后解释：
- 使用了什么近似；
- 近似何时成立；
- 最后得到的量具有什么物理意义。

## 9.4 单位

推荐：

```latex
$5\,\text{k}\Omega$
$26\,\text{mV}$
$1.5\times10^{10}\,\text{cm}^{-3}$
```

变量和单位之间使用适当空格；单位不写成斜体变量。

---

# 10. 图像、曲线、数据图表

## 10.1 原课件曲线

如果原课件已有：
- I–V curve；
- Bode plot；
- delay / throughput graph；
- waveform；
- spectrum；
- timing diagram；

并且可读，优先裁原图。不要为了统一风格重新画，因为坐标、刻度、注释本身就是知识来源。

## 10.2 外部曲线与重绘

原课程曲线不可安全使用时，先进入 Level 2，优先寻找教材、大学课程、厂商或官方资料中的语义等价曲线。只有找不到可靠外部图、且曲线能由明确公式或 source 数据逐项验证时，才允许重绘。

重绘必须：

- 保持数据 / 公式真实；
- 明确标注为“reconstructed / schematic”；
- 不伪造原课件数据点；
- 使用静态 SVG 或高清 PNG；
- 坐标轴、单位、legend 完整；
- 对照公式/source 验证趋势、拐点和方向；
- 风格尽量贴近课件。

---

# 11. 代码块标准

代码在 CS / Network / DSP / Lab 类课程中会成为常见内容，因此必须统一。

## 11.1 原则

代码块只放：
- 需要运行的代码；
- 算法核心；
- API / protocol 示例；
- 最小可复现实验片段。

不要用代码截图，除非课件的 IDE / debugger UI 本身就是讲解对象。

## 11.2 代码格式

必须写语言：

```python
def send_message(sock, payload):
    sock.sendall(payload)
```

Java：

```java
Socket socket = new Socket(host, port);
```

Shell：

```bash
python server.py
```

PowerShell：

```powershell
Get-NetAdapter
```

输出单独写：

```text
Server listening on 127.0.0.1:8000
Client connected
```

**命令和输出不得混在同一个代码块里**，否则复习时无法分辨哪些内容需要输入。

## 11.3 代码讲解

代码讲解默认采用：

**目的 → 关键代码 → 关键行为 → 与课程概念的关系**

不逐行解释显然的语法。

如果代码涉及重要状态流且没有可靠 source figure，可以配低风险静态 SVG：

`Client socket → TCP connection → Server socket`

---

# 12. 算法、伪代码与状态过程

如果重点在“逻辑步骤”而不是语言语法，优先伪代码，不强行用 Python/Java。

```text
receive packet
lookup destination
choose output interface
forward packet
```

如果过程含分支 / loop / multiple states，按顺序使用：
- 当前课程原图 / 官方资料图；
- 可信外部教材或技术图；
- 可逐项验证的低风险静态 SVG；
- 简单 Mermaid。

状态机应明确：
- state；
- trigger / event；
- transition；
- resulting action。

---

# 13. 例题、Tutorial 与计算过程

Lecture 中的 example 是为了解释机制，应直接放在对应知识点附近。

Tutorial 是独立文档，每道题默认结构：

### Problem X

先写**状态判断 / 模型选择**，然后计算。

```markdown
由于二极管正向偏置，采用 constant-voltage model，令 $V_D=0.7\,\text{V}$。
```

再给关键计算：

$$
I_D=\frac{V_S-V_D}{R}
$$

最后解释结果意味着什么。

纯代数变形不要占据大篇幅，但**不能跳过模型判断、边界条件、单位和最终物理意义**。

错题 / 易错点只在确实能改变解题方法时单独提醒。

---

# 14. 定义、提醒、Callout 与引用

## 14.1 定义

短定义可以直接写在正文：

**Store-and-forward** 指 router 完整接收 packet 后，才开始在下一条 link 上发送。

只有原课件一句话本身非常精炼、有记忆价值时使用引用：

> **Packets are the units moved through the network.**

## 14.2 Callout

Callout 只用于：
- 易错点；
- 适用条件；
- source correction；
- 安全 / assessment 限制。

一个大章节默认不超过 1 个。禁止整篇充满黄色/蓝色框。

---

# 15. 视觉节奏标准

目标不是“设计感”，而是**让眼睛知道什么时候该读 prose，什么时候该看结构**。

一段典型高质量章节可以是：

```text
2–3 段解释
↓
1 张经过 QA 的原课程图 / 可信外部图 / 低风险 SVG
↓
1–2 段解释图中的关系
↓
一个小表格或公式
↓
继续正文
```

不要变成：

```text
标题
一句话
标题
两 bullet
大图
标题
一句话
callout
```

也不要变成：

```text
1500 字连续正文
```

视觉元素之间不能连续堆叠。一般不要出现“图片 → 表格 → SVG → 公式”四个 block 中间没有解释文字。

---

# 16. 不同课程类型的适配

## 16.1 网络 / CS

优先：
- verified topology source figure；
- protocol sequence；
- verified source figure / low-risk static flow SVG；
- code blocks；
- comparison tables；
- packet / state diagrams。

例如 CSI201：
`Edge → Access → Core → Interconnection`

## 16.2 电子 / 电路

优先：
- 原课件 circuit diagram；
- I–V / waveform；
- formula + derivation；
- model comparison table；
- verified source figure / low-risk bias-flow SVG。

普通电场方向、PN 区方向等使用 Markdown 文本，不用 LaTeX 画文字。

## 16.3 数学 / 信号与系统

优先：
- 公式；
- derivation；
- function plot；
- waveform；
- transformation table；
- verified source graph crop。

不要把所有公式都做成截图。

## 16.4 编程 / Lab

优先：
- runnable code；
- terminal commands；
- output；
- verified source figure / low-risk architecture SVG；
- screenshot only when UI state matters。

## 16.5 概念 / 理论课程

优先：
- prose；
- compact comparison table；
- timeline / relationship diagram；
- source figures。

不要因为“缺少公式”就硬造视觉元素。

---

# 17. 质量检查 Gate

每次正式交付前必须检查：

### Content
- [ ] 是否覆盖原材料真正重要的知识，而不是只覆盖醒目的标题？
- [ ] 是否把关键机制讲清，而不是只写定义？
- [ ] 是否存在无来源扩展？
- [ ] Lecture / Tutorial / Lab 是否保持边界？

### Writing
- [ ] 是否存在大量一两句短段？
- [ ] 是否出现标题泛滥？
- [ ] 是否有重复总结和 AI 主持语？
- [ ] 重点是否来自内容本身，而不是符号和高亮？

### Visual Source
- [ ] 是否先判断“这里真的需要图”再进入视觉流程？
- [ ] 有课程原图时是否优先使用 Level 1？
- [ ] Level 1 两次仍无法安全提取时，是否停止硬裁并升级 Level 2？
- [ ] 外部图是否完成来源记录和 semantic equivalence check？
- [ ] SVG 是否仅用于低风险、可逐项验证的图？

### Visual Asset QA
- [ ] 每张被 Markdown 实际引用的图是否单独审查？
- [ ] 公式、坐标、刻度、单位、legend、caption、panel、箭头、极性是否完整？
- [ ] 是否存在断字、断线、半截文字、半个 panel、黑边或无关残片？
- [ ] 四边是否有合理安全留白？
- [ ] 图片显示尺寸是否按信息密度自适应，而不是统一宽度？
- [ ] multi-panel / paired figure 是否保持完整比较关系？

### Markdown
- [ ] 相对路径是否全部有效？
- [ ] 图片 / SVG 在 Obsidian 可显示？
- [ ] MathJax 是否稳定？
- [ ] code fence 是否有正确语言？
- [ ] Mermaid 若存在是否可渲染？

### Structure & Naming
- [ ] 课程根目录名是否等于 `course_code`？
- [ ] `COURSE_STATE.yaml` 是否存在且文件名未被改动？
- [ ] 单元目录前缀是否与 `unit_scheme` 声明一致（U1 / U2）？
- [ ] 单元序号是否两位零填充（U4）？
- [ ] 笔记序号是否在课程内按 TypeLabel 连续且无重复（N2）？
- [ ] `assets/` 文件名是否满足 `{SrcID}-(p{NN}-){slug}.{ext}`（A1）？
- [ ] 每个 `{SrcID}` 是否都能在同单元找到对应笔记（A2）？
- [ ] 是否存在未被引用的 `assets/` 文件（A3）？
- [ ] `sources/` 是否存在，且符合 `{COURSE_CODE}_{SrcID}_{Slug}.{ext}`（S1 / S2 / S3）？
- [ ] 是否错误地在单元交付中生成或判定了课程 `README.md`（R1）？

### Delivery
- [ ] `.md + assets + sources` 是否自包含？
- [ ] 外部 visual source 是否有可追溯引用？
- [ ] ZIP 解压后是否能直接放入 Vault？
- [ ] 是否避免修改 `.obsidian/`？
- [ ] 是否完成 final visual contact-sheet / per-asset audit？

---

# 18. 默认工作流程

收到一批新课程材料后：

1. **完整读取材料**：先理解整讲结构，不边读边机械输出。
2. **Source Map**：识别主知识链、公式、例题、好图、必须保留的图表、可删除行政页。
3. **Visual Need Decision**：先判断哪些位置真的需要视觉；不因为某节“没图”而强行加图。
4. **Level 1 Extraction**：优先从当前课程原材料高分辨率提取；识别 semantic envelope，再决定 tight / wide / page embed。
5. **Per-asset QA**：每张 crop 立刻检查完整性、正确性、边界和清洁度。最多两次合理 recrop；仍失败则停止硬裁。
6. **Escalation**：按 `可信外部原图 → 低风险 SVG → Manual Capture Required` 逐级处理，并完成来源/语义一致性验证。
7. **Knowledge Rewrite**：按理解顺序写正文，不按 slide 顺序抄。
8. **Insert Media**：视觉、表格、公式、代码只放在第一次真正需要的位置；显示尺寸按信息密度自适应。
9. **Density + Style Pass**：删除碎行、重复总结、主持语、过度粗体与装饰 block。
10. **Technical Validation**：检查相对路径、图片、SVG、MathJax、Mermaid、code fences 与 source dependencies。
11. **Pre-delivery Visual Audit**：汇总 Markdown 实际引用资产，逐张打开或生成 contact sheet，全部重新过 Gate。
12. **Package**：更新 `COURSE_STATE.yaml`，输出 Week/Unit ZIP；Markdown 可额外作为预览。
13. **Do Not Drift**：后续 Lecture 默认继承本 standard；没有用户确认，不自行改变视觉或结构规范。

---

# 19. 当前已确认的硬规则

以下规则已经通过多门课程的实际笔记迭代确认，默认视为稳定约束：

- 正文是经过重写的课程讲义，不是 PPT 摘要。
- 行政信息默认删除。
- 一个完整思想尽量写完整自然段，不做 bullet dump。
- 密度保持中等：比纯教材稍紧，但不能满屏连续文字。
- 该用表格、图、公式、代码时使用，不追求“全是 prose”。
- **原课程材料中的可靠视觉永远是第一优先级。**
- 截图先识别 semantic envelope，再裁；不允许断公式、断坐标、断 caption、断 panel。
- 同一原图最多进行两次合理 recrop；仍无法同时做到完整和干净时，自动升级，不继续猜坐标。
- **视觉 fallback 固定为：课程原图 / 同源 PDF → 可信教材或官方外部原图 → 低风险静态 SVG → Manual Capture Required。**
- 外部图必须标注来源并完成 semantic equivalence check，不把外部图伪装成老师课件。
- SVG 只承担低风险、结构明确、可逐项验证的图；高风险方向、极性、器件内部机制和复杂曲线默认不自行重绘。
- 每张视觉资产进入 Markdown 前都必须单独 QA；正式 ZIP 前还必须做一次全资产 visual audit。
- 图片尺寸按信息密度与 aspect ratio 自适应，不统一宽度。
- **课程笔记默认不使用 SVG 动画。**
- Mermaid 不是核心视觉默认方案。
- 公式只承载数学，普通方向/状态/英文术语不用 LaTeX 装饰。
- 代码使用真实 code fence，terminal command 与 output 分离。
- Callout 稀少使用，不做“黄框笔记”。
- 最终交付必须能在 Obsidian 中独立工作并保持链接。
- 一旦某课程的 standard 确认，后续默认复用，除非用户明确修改。
- **交付结构与命名是硬约束**：`COURSE_STATE.yaml` 必需且文件名固定；单元目录前缀由 `unit_scheme` 唯一决定，同一课程不得混用；笔记序号在课程内按 TypeLabel 连续；资源文件一律 `{SrcID}-p{NN}-{slug}.{ext}`，页码必须是真实页码或整体省略，不用占位值；**`sources/` 无条件强制存在**。
- **课程 `README.md` 延后生成**：单元交付不含 README；整门课内容写完后单独生成一次。
- 课程结构一旦开始交付即视为锁定；改变 `unit_scheme` 属于显式迁移，不做静默切换。

---

# 20. 最小模板

```markdown
# COURSE Lecture X · Topic

[1–2 段建立本讲核心问题和主线。]

## 一、Major Knowledge Block

[连续正文解释现象、原因和机制。]

![优先使用已通过 QA 的课程原图；失败时按视觉来源层级升级](assets/LXX-pXX-topic.png)

[解释图中真正重要的关系。]

### 1. Sub-mechanism

[正文。]

$$
[仅在真正需要时出现公式]
$$

[解释公式意义、条件和趋势。]

|需要比较时才使用|A|B|
|---|---|---|
|Dimension|...|...|

## 二、Next Major Block

[继续按知识逻辑展开。]

```language
[只有真正需要时出现代码]
```

```text
[程序输出 / 伪代码 / 日志]
```

<!-- 视觉按 Level 1 → Level 2 → Level 3 → Level 4 处理；不要为了填模板强行生成图。 -->

## 三、Integrated Understanding

[最后将前面分开的机制重新放回一个完整系统；不重复逐点总结。]
```

---


# 21. 持续交付与多对话协同 SOP

本节规定课程进入 Week 2、Week 3……以后如何继续，不允许每开一个新对话就重新猜格式，也不要求每周重发整门课程。

## 21.1 三层权威关系

后续任何 Agent / 对话都必须按以下优先级工作：

`Global Standard → Course State → Current Source Materials`

- **Global Standard**：本文件，定义所有课程共用的写作、视觉、公式、代码、图片与交付规则。
- **Course State**：当前课程的小型状态文件 `COURSE_STATE.yaml`，记录已完成到哪里、课程级特例、当前 gold reference 和下一步。
- **Current Source Materials**：本周新上传的 Lecture / Tutorial / Lab / Reading 原始材料。

旧对话内容、模型记忆、口头猜测都不能覆盖这三层。发生冲突时，先按上述优先级解决；无法解决再询问用户。

## 21.2 每周不是“重做课程”，而是增量编译

收到新一周材料后，默认执行 **incremental compilation**：

- 只生成本周新增的 Lecture / Tutorial / Lab；
- 不重写已经 accepted 的旧 Week；
- 不重新打包整个课程；
- 更新一次 `COURSE_STATE.yaml`；
- 输出一个本周 Delivery ZIP。

只有用户明确要求“全量整理 / 重构 / 改旧周 / 打总包”时，才触碰旧内容。

## 21.3 每周正式交付结构

默认交付包（`Unit` 为占位符，实际前缀由 `unit_scheme` 决定，见 2.4）：

```text
COURSE_CODE_Unit{NN}_Delivery.zip
├─ COURSE_STATE.yaml
└─ Unit{NN}/
   ├─ Lecture {NN} - Topic.md
   ├─ Tutorial {NN} - Topic.md      # 有则生成
   ├─ Lab {NN} - Topic.md           # 有则生成
   ├─ assets/                       # 被引用时必需
   └─ sources/                      # 强制必需（2.6）
```

**单元交付包中不包含课程 `README.md`**（见 2.2）；也不包含 `NOTE_STYLE_SPEC.md`。

用户将 ZIP **直接解压到课程根目录**。新的 `COURSE_STATE.yaml` 覆盖旧版本，`Unit{NN}/` 作为新增目录进入课程。

因此用户每周不需要逐张处理图片，也不需要手动合并 Markdown。

## 21.4 COURSE_STATE.yaml 是跨对话协同核心

`COURSE_STATE.yaml` 是一个极小、可携带的课程状态文件。它不是聊天摘要，而是 Current Project Kernel，只记录会影响后续执行的事实。

必须包含：

```yaml
schema: obsidian-course-state/v1
course_code: COURSE_CODE
standard_version: "3.1"
status: active

structure:
  unit_scheme: week          # week | lecture | module | chapter | unit | custom
  unit_prefix: ""            # 仅 unit_scheme: custom 时填写
  current_unit: 1

gold_reference:
  note: "Week01/Lecture 01 - Topic.md"
  visual_baseline: "accepted course note"

completed:
  - unit: Week01
    status: accepted
    artifacts:
      - type: lecture
        file: "Week01/Lecture 01 - Topic.md"
        status: accepted

course_overrides: []

next_expected:
  unit: Week02
  expected_types: [lecture]

last_delivery:
  package: "COURSE_CODE_Week01_Delivery.zip"
  date: "YYYY-MM-DD"
```

`unit_scheme` 是交付结构与命名体系的**唯一变量**（见 2.4）：它决定单元目录前缀，也决定 `completed[].unit` / `next_expected.unit` / `last_delivery.package` 的写法。该字段一旦某课程开始交付即锁定。

更新规则：
- 新 Week/Unit 首次交付：`ADD completed` 中对应 unit，unit 与新 artifact 初始状态为 `draft`；更新 `current_unit / next_expected / last_delivery`。
- 同一 Week 同时存在 Lecture / Tutorial / Lab 时，每个 artifact 独立记录状态；只有该 unit 当前要求的 artifacts 全部 accepted 后，unit 才标为 `accepted`。
- 用户改变课程特例：`UPDATE course_overrides`。
- 旧规则失效：`DELETE / DEPRECATE`，不保留一长串历史聊天记录。
- 全局规范改变：更新 `standard_version`，不要只写在聊天里。

## 21.5 同一个对话继续时

如果仍在原对话，用户只需要上传新材料并说：

> 按已确认 Standard 和当前 Course State 继续处理下一个 Unit（按其 `unit_scheme` 对应的前缀，如 Week03）。只生成新增内容，输出该 Unit 的 Delivery ZIP，并更新 COURSE_STATE.yaml；不要重发旧单元。

Agent 应直接继续，不要求用户重新解释视觉规则、公式规则或打包方式。

## 21.6 新对话继续时

新对话可能不知道旧讨论，所以最小输入是：

1. 当前 Standard（若该项目/环境已经能稳定访问，则不用重复上传）；
2. 最新 `COURSE_STATE.yaml`；
3. 本周新 Lecture / Tutorial / Lab 原材料。

新对话的第一步不是开始写，而是读取 Standard + Course State，确认：
- 当前课程；
- standard version；
- 已完成 Week；
- gold reference；
- course overrides；
- 本次只处理什么。

然后再处理新材料。

推荐直接复制的启动指令见 `HANDOFF_PROMPTS.md`。

## 21.7 Gold Reference

每门课程至少保留一个 **Gold Reference**，即用户已经明确确认“完全没问题”的实际笔记。

Gold Reference 的作用是校准：
- 正文密度；
- 标题粒度；
- PPT 裁图方式；
- SVG 风格；
- 表格频率；
- 留白；
- 重点表达。

Gold Reference 的地位低于 Global Standard，但高于 Agent 自己的写作偏好。

如果课程尚未有 Gold Reference，先按 Global Standard 生成；一旦用户确认某版，将其路径写入 `COURSE_STATE.yaml`。

## 21.8 Draft → Accepted 与回退闭环

每次新 Week/Unit 的 Delivery ZIP 首次生成时，对应 unit / artifact 在 `COURSE_STATE.yaml` 中标记为 `draft`。**正式 Delivery 中始终使用 canonical 文件名，不在文件名后追加 `v1 / v2 / final`**，这样用户确认后无需再次重打 ZIP 或在 Vault 中重命名文件。

如果用户要求修改 draft，Agent 重新生成同一路径的 artifact，并再次输出同名规范的 Delivery ZIP；用户解压后覆盖该 draft 文件即可。必要的实验版只存在于 Agent 工作区，不进入 canonical 课程目录。

当用户明确说“这版可以 / 接受 / 确认”后，状态闭环必须立即完成：

1. 将对应 artifact 的 `status` 从 `draft` 改为 `accepted`；
2. 如果该 unit 当前要求的所有 artifacts 都已 accepted，将 unit 的 `status` 改为 `accepted`；
3. 如该版本成为新的 Gold Reference，同步更新 `gold_reference`；
4. **立即返回更新后的 `COURSE_STATE.yaml` 小文件即可，不需要重新打 Week/Unit ZIP。**

后续 Agent 以最新 state 为准；已经 accepted 的 artifact 默认不可被静默修改。如需修改，必须明确进入 revision，并先把对应 artifact 状态重新标记为 `draft`。

## 21.9 Standard 如何升级

规则变更分两类：

**Course-specific**：只影响某一门课，例如某课程要求每章保留公式索引。写进 `course_overrides`，不升级 Global Standard。

**Global**：未来所有课程都应该遵守，例如“SVG 默认静态”“PPT 好图优先裁图”。更新本 Standard，版本号按语义版本推进；本次 Visual Extraction / QA Pipeline 属于跨课程执行模型变化，因此升级为 `3.0`。后续兼容性小改使用 `3.x`。

Standard 升级后，不自动重写过去所有 Week。旧笔记只有用户明确要求时才迁移。

## 21.10 每周交付 Gate

输出 ZIP 前必须同时通过：

```text
Source completeness
→ Knowledge rewrite complete
→ Visual source hierarchy resolved
→ Per-asset Visual QA passed
→ Final visual audit passed
→ Structure & naming rules pass (2.7: U1-U4, N1-N2, A1-A3, S1-S3)
→ `sources/` present for every unit
→ Relative links valid
→ Formula / code syntax valid
→ No animation unless explicitly requested
→ No administrative noise unless requested
→ COURSE_STATE.yaml updated
→ Unit Delivery ZIP built
```

如果任何一项失败，不应把该 Week 标记为 accepted。

## 21.11 阶段性总包

默认不每周重发完整课程总包。只在以下情况生成：

- 用户明确要求；
- 一个教学阶段结束（如 Midterm / Module Part I）；
- Standard 大版本迁移；
- 需要跨设备备份。

总包形式：

```text
COURSE_CODE_Full_Bundle_YYYY-MM-DD.zip
├─ COURSE_STATE.yaml
├─ README.md                       # 课程完结时才有，见 2.2
├─ Unit01/
├─ Unit02/
├─ ...
└─ Unit{NN}/
```

这只是阶段性快照，不取代每周增量 Delivery。

---

**本文件是全局课程笔记的唯一 Canonical Standard。课程级 `NOTE_STYLE_SPEC.md` / `course_overrides` 只能增加课程特有要求，不能静默覆盖本 Standard 的硬规则；Global Standard 无需复制进每门课程目录。**
