# Obsidian Course Notes Standard v2.2

> **Canonical Standard**  
> 适用于所有 Lecture / Tutorial / Reading / Lab / Coding 类课程笔记。  
> 目标不是“总结课件”，而是把原始教学材料重构为 **可长期维护、可复习、可追溯、视觉统一、直接放入 Obsidian 的高质量课程讲义**。  
> 全局 Standard 只定义跨课程共用规则；具体课程的正文密度与视觉基线由该课程 `COURSE_STATE.yaml → gold_reference` 决定。

---

## 0. 总原则

一份合格课程笔记必须同时满足五件事：

1. **知识正确**：不把模型补充、外部常识或推断伪装成课件原意。
2. **讲清机制**：不能只列定义和结论；关键知识要解释“为什么出现、内部怎样工作、结果是什么、与前后概念怎样连接”。
3. **视觉承担信息**：能用原课件好图说明的，不重新画；原图不适合直接用时再做静态 SVG；表格、公式、代码、流程图各自只承担最适合自己的信息。
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

## 2.1 课程根目录

推荐结构：

```text
COURSE_CODE/
├─ README.md
├─ COURSE_STATE.yaml
├─ NOTE_STYLE_SPEC.md        # optional，仅记录课程特有 overrides
├─ Week01/
│  ├─ Lecture 01 - Topic.md
│  ├─ Tutorial 01 - Topic.md
│  ├─ Lab 01 - Topic.md
│  ├─ assets/
│  │  ├─ L01-p34-campus-access.png
│  │  ├─ L01-store-forward.svg
│  │  └─ T01-p08-example.png
│  └─ sources/
│     ├─ Lecture01.pdf
│     └─ Tutorial01.pdf
├─ Week02/
│  └─ ...
└─ ...
```

如果课程不按 Week 组织，可将 `Week01` 替换为 `Unit01` / `Lecture01`，但**同一课程一旦选择后不得混用**。

每个 Unit / Week 必须自包含：移动整个目录后，Markdown、assets、sources 仍然有效。

`COURSE_STATE.yaml` 是课程根目录的必需文件；`NOTE_STYLE_SPEC.md` 仅在该课程存在全局 Standard 之外的课程特例时创建。Global Standard 本身不需要复制进每门课程目录，只要当前项目/工作环境能够稳定访问 canonical standard 即可。

不得创建、覆盖或修改 `.obsidian/`。
**Source dependency hard rule：**如果任何已交付 Markdown 引用了 `sources/` 下的文件，该被引用的 source file 必须包含在同一个 Delivery ZIP 中。只有当所有已交付笔记都不依赖 `sources/` 时，`sources/` 才可以省略。


## 2.2 正式交付

新增一周/单元时，正式交付统一命名为：

- Week 制：`COURSE_CODE_WeekXX_Delivery.zip`
- Unit 制：`COURSE_CODE_UnitXX_Delivery.zip`

用户只需要：

`下载 → 解压 → 整个文件夹内容放进课程根目录`

单独 `.md` 可以额外提供预览，但不能作为唯一正式交付，因为它可能失去图片和 sources。

## 2.3 文件命名

Markdown：

```text
Lecture 01 - Introduction to the Modern Internet.md
Tutorial 01 - Diode Analysis.md
Lab 03 - Socket Programming.md
```

图片 / SVG：

```text
L01-p34-campus-access.png
L01-p45-tunnel-hybrid.png
L01-store-and-forward.svg
T01-p08-load-line-example.png
LAB03-client-server-flow.svg
```

原则：**课程内唯一、可读、可追溯，不使用 UUID。**

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
|因果机制|正文 + 静态 SVG / 原图|短流程|纯 bullet|
|时间/步骤流程|原课件图 / 静态 SVG|编号步骤|动画|
|协议交互|Sequence-style 静态 SVG|横向流程|长文字来回描述|
|概念对比|表格 + 一段解释|双栏 SVG|重复两遍正文|
|公式|MathJax + 解释|源图|截图公式|
|公式推导|MathJax aligned|逐行公式|只给最终式|
|实验/例题|条件 → 判断 → 计算 → 结果解释|表格|只给答案|
|代码|语言代码块 + 必要解释|伪代码|截图代码|
|终端命令|shell / powershell block|inline code|把输出混进命令|
|程序输出|text block|表格|与代码混在同一块|
|算法过程|伪代码 / 静态流程图|代码|长篇 prose|
|数据对比|表格|图表|无理由做饼图|
|趋势/函数关系|原课件图 / 静态 plot|MathJax|纯口述|
|网络拓扑/结构|原课件裁图|静态 SVG|大面积 Mermaid 默认图|
|状态机|原课件图 / 静态 SVG|Mermaid|动画|
|警告/边界条件|短引用或 callout|正文粗体|整页 callout|
|整页 PPT 都有价值|嵌入 PDF page|整页截图|重新抄写整页|

---

# 5. 图片与视觉资产标准

## 5.1 视觉选择优先级

视觉资产严格按以下优先级判断：

### Priority A — 原课件已有好图：直接用

如果 PPT / PDF 的图已经清楚表达知识，**不要重新生成**。高分辨率渲染对应页，然后只裁出真正有价值的区域。

适用：
- 网络拓扑；
- 电路图；
- block diagram；
- 曲线；
- 状态转换；
- 结构示意；
- 教师特制案例图；
- 有教学语义的表格。

### Priority B — 整页上下文都有价值：嵌入原 PDF 页面

```markdown
![[sources/Lecture01.pdf#page=34]]
```

不要为了“保持风格”把整张 slide 截成 PNG。如果整页有价值，PDF page 更清晰、更可追溯。

### Priority C — 原图差，但结构值得画：静态 SVG

只有在以下情况才生成 SVG：

- 原课件没有图；
- 原图太模糊 / 空白过大 / 信息组织很差；
- 需要把散落在多页的机制合成一张结构图；
- 一段 prose 明显不如图直观。

**课程笔记默认禁止动画 SVG。** 动画只在用户明确要求教学动画时作为额外资产提供，不得替代静态主图。

### Priority D — 简单关系不值得做图：表格 / inline flow

例如：

`Client → Request → Server → Response`

如果这已经足够，就不要画一个大图。

---

## 5.2 PPT / PDF 截图裁剪规则

截图裁剪的第一原则不是“尽可能紧”，而是 **语义完整优先（semantic completeness first）**。只有在裁剪后仍能完整理解原图时，才允许进行局部裁图。

### 5.2.1 先判断能不能安全裁

在裁图前，先判断当前图是否依赖周围信息。只要理解这张图还需要下面任意内容，它们就属于图的 **semantic envelope（语义包络）**，不能被裁掉：

- 相邻公式、变量定义、推导步骤；
- 坐标轴、刻度、单位、legend；
- 箭头、极性、电场/电流方向、边界标记；
- panel 编号、左右/上下对照关系；
- 图注、caption、直接解释图的短句；
- worked example 中与图绑定的已知条件、计算关系或结论；
- 电路图、波形图、multi-panel figure 中不可分离的配套信息。

**判断标准：裁完以后，这张图必须在不重新打开原 PPT / PDF 的情况下仍然能被正确理解。** 如果做不到，就说明裁得过头。

### 5.2.2 不同图型使用不同裁剪强度

**可紧裁（tight crop）**：独立结构图、单一网络拓扑、单一 block diagram、主体与标签都集中在一个区域，且外围内容不参与理解。

**默认宽裁（wide crop）**：以下类型优先保留更完整的上下文，不追求极致紧凑：

- math-heavy figure；
- 公式与图形联合出现的页面；
- circuit diagram；
- waveform / timing diagram；
- plotted figure / function graph；
- worked example；
- multi-panel comparison；
- 含大量边界标签、方向标记、单位或图例的技术图。

对于这些内容，宁可多保留一些合理白边，也不能为了“干净”切掉语义。

### 5.2.3 无法安全局部裁切时的 fallback

如果图与周围公式、解释或多个 panel 无法安全分离，按以下顺序处理：

`宽裁 / 半页裁图 → 嵌入原 PDF 页面 → 静态 SVG 重构`

其中：

- **宽裁 / 半页裁图**：保留完整 semantic envelope，只删除明显无关区域；
- **原 PDF 页面**：当整页上下文本身就是教学内容时，直接嵌入 source page；
- **静态 SVG 重构**：仅在原图确实不适合直接使用、且可以不丢失技术含义地重构时使用。

### 5.2.4 可以删除什么

在确认语义完整后，才尽量裁掉：

- 与正文重复且不参与理解的 slide 标题；
- 页码；
- decorative background；
- 与当前知识无关的文字；
- 明显无意义的大面积空白；
- 空的边角和版式占位。

### 5.2.5 必须保留什么

必须保留所有理解所需的：

- 图中标签；
- 图例；
- 箭头与方向；
- 坐标轴、刻度和单位；
- 极性、边界和区域标记；
- panel 标号与比较关系；
- 相关公式、变量定义与必要说明；
- 与图不可分离的上下文。

裁图四周通常保留约 **4–8% 的呼吸边距**；但这只是视觉建议，**不能凌驾于语义完整性**。对公式密集、多 panel、电路、波形和 worked example，允许明显更宽的边距。

截图必须从 PDF/PPT 高分辨率渲染后裁，不从聊天截图二次裁剪。

## 5.3 图片在正文中的位置

图必须放在**第一次真正需要它解释机制的位置**，而不是统一塞到章节尾部。

正确：

```markdown
这一段先说明为什么 access network 需要 edge router。

![Campus Access Path](assets/L01-p34-campus-access.png)

图中 Wi-Fi AP ...
```

不要写：

```markdown
下面是一些相关图片：
...
```

图片前后至少有一句正文建立语境；图后如果图本身不自解释，需要一段解释最关键关系。

## 5.4 图片大小与留白

默认图片应占正文内容宽度的大约 **65–90%**。结构复杂、横向关系多时可以接近全宽；简单图不要无意义撑满页面。

图内部的视觉密度应接近原 PPT，不要把少量信息放进巨大卡片。

---

# 6. 静态 SVG 规范

## 6.1 总风格

SVG 不是另起一套视觉设计，而是**补齐原课件视觉语言**。

如果课件有稳定风格，SVG 应继承：

- 主色；
- accent color；
- neutral background；
- 圆角程度；
- 线条粗细；
- 字号层级；
- 箭头形态；
- node 的视觉重量。

例如 CSI201 的课件是浅背景、深蓝文本、青色与橙色 accent，则补充 SVG 也保持这一风格，不突然变成霓虹、渐变、玻璃、像素风。

如果原课件没有明显风格，则使用中性课程默认：

- 背景：透明或极浅 neutral；
- node：浅色填充 + 细边；
- 文本：深灰/深蓝；
- 主流程：单一主色；
- 仅一个 accent 用于关键节点；
- 禁止阴影堆叠、复杂渐变、拟物效果。

## 6.2 SVG 布局

优先 **横向（left-to-right）**。课程流程通常更适合人的阅读方向，也减少 Obsidian 中向下占屏。

只有以下情况用纵向：
- 因果层级本身强烈从上到下；
- 横向会造成严重拥挤；
- 原课件本来就是纵向结构。

SVG 必须放在一个紧凑画布中，内容居中，不贴左侧，不留巨大空白。节点之间有稳定间距，箭头不能穿过文字。

## 6.3 SVG 文字

- 字体使用系统无衬线栈，不嵌入字体文件；
- 不用过小字体；
- 一张图最多 2–3 个字号层级；
- node 文字尽量 1–2 行；
- 长解释留在正文，不塞进图。

## 6.4 SVG 禁止项

禁止：
- 默认动画；
- moving packet / blinking node / loop animation；
- hover 才显示核心信息；
- 复杂 filter 导致 Obsidian 兼容问题；
- `foreignObject` 作为必要依赖；
- 过度圆角卡片化；
- 颜色数量失控；
- 与 PPT 风格完全不同的“重新设计”。

---

# 7. Mermaid 使用标准

Mermaid 不是默认视觉方案。它适合**简单、结构性强、无需精确视觉风格**的关系，例如 dependency、简单 state graph、项目流程。

优先级：

`在确实需要视觉表达时：原课件裁图 > 原 PDF 页面 > 静态 SVG > 紧凑表格 / inline flow > Mermaid`

对于课程核心机制、网络拓扑、电路、协议 sequence，如果视觉质量重要，优先静态 SVG 或原图。

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

## 10.2 重绘曲线

只有原图不可读或需要把公式关系重新可视化时才重绘。重绘必须：

- 保持数据 / 公式真实；
- 明确标注为“reconstructed / schematic”；
- 不伪造原课件数据点；
- 使用静态 SVG 或高清 PNG；
- 坐标轴、单位、legend 完整；
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

如果代码涉及重要状态流，可以配静态 SVG：

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

如果过程含分支 / loop / multiple states，使用：
- 原课件图；
- 静态 SVG；
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
1 张原课件裁图 / SVG
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
- topology screenshot；
- protocol sequence；
- static flow SVG；
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
- bias / signal flow static SVG。

普通电场方向、PN 区方向等使用 Markdown 文本，不用 LaTeX 画文字。

## 16.3 数学 / 信号与系统

优先：
- 公式；
- derivation；
- function plot；
- waveform；
- transformation table；
- source graph crop。

不要把所有公式都做成截图。

## 16.4 编程 / Lab

优先：
- runnable code；
- terminal commands；
- output；
- architecture / data-flow SVG；
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

### Visual
- [ ] 原 PPT 有好图时是否优先使用？
- [ ] 截图是否裁掉无意义 slide 外壳与大白边？
- [ ] SVG 是否静态、紧凑、风格贴近课件？
- [ ] 是否为了“丰富”而加入无用图？
- [ ] 表格 / 图 / 公式是否真的比 prose 更合适？

### Markdown
- [ ] 相对路径是否全部有效？
- [ ] 图片 / SVG 在 Obsidian 可显示？
- [ ] MathJax 是否稳定？
- [ ] code fence 是否有正确语言？
- [ ] Mermaid 若存在是否可渲染？

### Delivery
- [ ] `.md + assets + sources` 是否自包含？
- [ ] ZIP 解压后是否能直接放入 Vault？
- [ ] 是否避免修改 `.obsidian/`？

---

# 18. 默认工作流程

收到一批新课程材料后：

1. **完整读取材料**：先理解整讲结构，不边读边机械输出。
2. **Source Map**：识别主知识链、公式、例题、好图、必须保留的图表、可删除行政页。
3. **Visual Triage**：对每张候选图判断 `原图裁剪 / PDF page / 静态 SVG / 表格 / 不需要视觉`。
4. **Knowledge Rewrite**：按理解顺序写正文，不按 slide 顺序抄。
5. **Insert Media**：图、表、公式、代码只放在第一次真正需要它的位置。
6. **Density Pass**：删除碎行、重复总结和大段无停顿文字，使密度落在中间区间。
7. **Style Pass**：清理 ChatGPT 主持语、过度粗体、无意义符号。
8. **Technical Validation**：检查相对路径、SVG、图片、MathJax、Mermaid、code fences。
9. **Package**：输出 Week/Unit ZIP；Markdown 可额外作为预览。
10. **Do Not Drift**：后续 Lecture 默认继承本 standard；没有用户确认，不自行改变视觉或结构规范。

---

# 19. 当前已确认的硬规则

以下规则已经通过多门课程的实际笔记迭代确认，默认视为稳定约束：

- 正文是经过重写的课程讲义，不是 PPT 摘要。
- 行政信息默认删除。
- 一个完整思想尽量写完整自然段，不做 bullet dump。
- 密度保持中等：比纯教材稍紧，但不能满屏连续文字。
- 该用表格、图、公式、代码时使用，不追求“全是 prose”。
- **原课件好图优先于任何生成图。**
- 截图优先裁取有效图形区域，不把整张 PPT 大白边塞进笔记。
- 只有原图不适合时才生成 **静态 SVG**。
- SVG 风格继承 PPT；不另造明显不同的视觉语言。
- **课程笔记默认不使用 SVG 动画。**
- Mermaid 不是核心视觉默认方案。
- 公式只承载数学，普通方向/状态/英文术语不用 LaTeX 装饰。
- 代码使用真实 code fence，terminal command 与 output 分离。
- Callout 稀少使用，不做“黄框笔记”。
- 最终交付必须能在 Obsidian 中独立工作并保持链接。
- 一旦某课程的 standard 确认，后续默认复用，除非用户明确修改。

---

# 20. 最小模板

```markdown
# COURSE Lecture X · Topic

[1–2 段建立本讲核心问题和主线。]

## 一、Major Knowledge Block

[连续正文解释现象、原因和机制。]

![必要时使用原课件裁图](assets/LXX-pXX-topic.png)

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

![原图不足时才使用静态 SVG](assets/LXX-mechanism.svg)

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

默认交付包：

```text
COURSE_CODE_WeekXX_Delivery.zip
├─ COURSE_STATE.yaml
└─ WeekXX/
   ├─ Lecture XX - Topic.md
   ├─ Tutorial XX - Topic.md        # 有则生成
   ├─ Lab XX - Topic.md             # 有则生成
   ├─ assets/
   └─ sources/                      # 被笔记引用时必须包含；否则按需生成
```

用户将 ZIP **直接解压到课程根目录**。新的 `COURSE_STATE.yaml` 覆盖旧版本，`WeekXX/` 作为新增目录进入课程。

因此用户每周不需要逐张处理图片，也不需要手动合并 Markdown。

## 21.4 COURSE_STATE.yaml 是跨对话协同核心

`COURSE_STATE.yaml` 是一个极小、可携带的课程状态文件。它不是聊天摘要，而是 Current Project Kernel，只记录会影响后续执行的事实。

必须包含：

```yaml
schema: obsidian-course-state/v1
course_code: COURSE_CODE
standard_version: "2.2"
status: active

structure:
  unit_scheme: week
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

更新规则：
- 新 Week/Unit 首次交付：`ADD completed` 中对应 unit，unit 与新 artifact 初始状态为 `draft`；更新 `current_unit / next_expected / last_delivery`。
- 同一 Week 同时存在 Lecture / Tutorial / Lab 时，每个 artifact 独立记录状态；只有该 unit 当前要求的 artifacts 全部 accepted 后，unit 才标为 `accepted`。
- 用户改变课程特例：`UPDATE course_overrides`。
- 旧规则失效：`DELETE / DEPRECATE`，不保留一长串历史聊天记录。
- 全局规范改变：更新 `standard_version`，不要只写在聊天里。

## 21.5 同一个对话继续时

如果仍在原对话，用户只需要上传新材料并说：

> 按已确认 Standard 和当前 Course State 继续处理 WeekXX。只生成本周新增内容，输出 WeekXX Delivery ZIP，并更新 COURSE_STATE.yaml；不要重发旧周。

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

**Global**：未来所有课程都应该遵守，例如“SVG 默认静态”“PPT 好图优先裁图”。更新本 Standard，版本号从 `2.2 → 2.3`。

Standard 升级后，不自动重写过去所有 Week。旧笔记只有用户明确要求时才迁移。

## 21.10 每周交付 Gate

输出 ZIP 前必须同时通过：

```text
Source completeness
→ Knowledge rewrite complete
→ Visual triage complete
→ Relative links valid
→ Formula / code syntax valid
→ No animation unless explicitly requested
→ No administrative noise unless requested
→ COURSE_STATE.yaml updated
→ WeekXX Delivery ZIP built
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
├─ README.md
├─ Week01/
├─ Week02/
├─ ...
└─ WeekXX/
```

这只是阶段性快照，不取代每周增量 Delivery。


**本文件是全局课程笔记的唯一 Canonical Standard。课程级 `NOTE_STYLE_SPEC.md` / `course_overrides` 只能增加课程特有要求，不能静默覆盖本 Standard 的硬规则；Global Standard 无需复制进每门课程目录。**
