# human-ui-copy

> 只讲用户收益，不汇报实现。
> 看起来太整齐的时候，故意打破它 —— 但别打破产品，也别过度修正。

> **⚠️ 给使用者：只有 `SKILL.md` 需要放进 agent 的 skills 目录。**
> `references/appendix.md` / `references/` 是给人读的完整资料 —— **不要放进加载目录**，会让 agent 每次加载技能时白读几千 token。`SKILL.md` 里引用了它们，人类需要时再翻即可。

一个给 AI 编程 agent 用的 **skill**：找出并去掉页面里的「AI 味」。

## 它解决什么

**文案层**：模型会把自己的实现约束写进页面。你让它「零后端、不上传」，它会在工具下方加一行 `生成在本地完成 - 内容不出浏览器`。访客不关心你的架构，只关心自己能拿到什么。人类的写法是 `本地处理，秒出结果`。

**结构层**：AI 做的页面**太均匀** —— 每个 section 都是「标题 + 一段话 + 三张卡片」，圆角统一、配色统一，连缺口都统一（没有空态、没有错误态）。人做页面是**偏心**的。

判据一句话：**AI 是均匀的，人是偏心的。**

## 直接粘进 AGENTS.md（不装 skill 也能用）

把下面这段粘进项目的 `AGENTS.md`（或等价的项目指令文件）：

```markdown
## 页面与文案纪律

- 动手前先读现有实现（页面、组件、设计系统），不重复造已经有的东西。
- 结构不套默认模板。三卡片或居中 hero 必须先过四问：数量由内容决定吗？
  每张独立成立吗？是数据驱动还是复制三份？来自组件库吗？
- 文案只讲用户收益，不写实现。「本地处理，秒出结果」可以，
  「内容不出浏览器」不行。
- 不用「·」做间隔。不留 TODO、需求原文、console.log。
- 每个页面至少留一处只有这个项目才会有的细节。打破网格最多一处，且只在装饰层。
- 交付前自检五个状态：空态、加载中、错误、超长输入、离线。
```

（这个片段就是 skill 的最小可用版；完整判据见 [`SKILL.md`](SKILL.md)。）

## 真实案例

[`references/real-audit-static-site.md`](references/real-audit-static-site.md)：一个手写静态站的实地审计 —— 461 个 SVG 里 395 个缺标注，以及为什么"批量补 aria-hidden"这个方案不能直接接受。

## 文件

| 文件 | 用途 |
|---|---|
| [`SKILL.md`](SKILL.md) | 工作清单（给 agent 读的，尽量短） |
| [`references/`](references/) | 详细案例、语言指纹、SSR/SPA、示例报告（按需加载，不是必需品） |
| [`references/appendix.md`](references/appendix.md) | 详细案例、语言指纹、SSR/SPA、过度修正对照、贡献说明 |
| [`references/audit-report.md`](references/audit-report.md) | 一份完整的审计报告样例（输出长什么样） |

`SKILL.md` 只保留判断必需的东西，长案例都在 appendix —— 避免 agent 读技能时 token 压力过大。

## 快速使用

把 `SKILL.md`（以及 `references/appendix.md`）放进你所用 agent 的 **skills 目录**，然后这样触发：

> 使用 human-ui-copy，模式 = `delivery`。输出审计报告：`must` 项逐条 是/否 + 证据；`judgement` 项 0–2 分 + 引用片段 + 依据哪个锚点；结尾给建议清单（`must` 优先）。**不要自动修改 `judgement` 相关内容** —— 只出报告，人来决定。

也可以直接当人工 code review 的清单用，不需要 agent。

## 两种模式与三档环境

| 模式 | 跑什么 |
|---|---|
| `prototype` | 只跑文案层；结构糙一点没关系 |
| `delivery` | 文案 + 结构 + 无障碍 + 多语言，且**每个页面状态**都要跑 |

| 环境 | 标准 |
|---|---|
| 本地 / 测试页 | `judgement` 放宽，只看 `must` |
| 内部后台 / 内部文档 | `judgement` ≤ 1 可接受 |
| 对外客户页 | `judgement` 追求 0 |

## 判断项怎么打分

每条 audit 项标 `must`（可客观核对）或 `judgement`（需人判断，0–2 档）。两个核心 judgement 项：

```
页面太匀   0 有更重的 section + 项目独有细节
           1 各节长短不一，但没有独有细节
           2 每节同形状，整页可换成别家的

文案像人   0 每句都能让访客行动，没有一句解释实现
           1 一两句在描述实现或架构
           2 页面在访客可见处解释自己的技术实现
```

降分歧四招：拿证据；双盲两遍；删除测试（删掉这句对访客有影响吗）；换名测试（换成竞品名还读得通 = 缺少具体性）。

详见 [`references/appendix.md`](references/appendix.md)。

## 适用范围

- **强适用**：工具页、内部工具、文档站、后台、个人项目
- **弱适用 / 不适用**：营销落地页、产品官网、儿童/娱乐产品、已有设计系统的项目 → 只跑文案层

**永远不覆盖项目自己的设计系统。**

## 三种东西不算 AI 味

```
- 组件库自带的结构（数据驱动 + 站内复用）
- 无障碍属性（alt / label / aria-* / focus ring）
- 业务本身就刚好三个功能点
```

完整白名单（含"原型阶段模板布局""营销页惯例""有来源的统计"等八条）在 [`SKILL.md`](SKILL.md#not-ai-flavor-whitelist)。

## 贡献

欢迎 PR：新指纹（附 ❌/✅）；其他语言的同类指纹；真实案例；**把「主观项」客观化的尝试**。

哪些能升级成 `must`、哪些只能是 `judgement`、以及升级方法，见 [appendix#contributing](references/appendix.md#contributing)。

## License

MIT
