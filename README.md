<div align="center">

# 🏔️ 文旅策划规划助手

**Cultural Tourism Project Planning Skills**

[![Hermes Skill](https://img.shields.io/badge/Hermes-Skill-8A2BE2)](https://hermes-agent.nousresearch.com)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-ff6b6b)](https://github.com/owenwuhaha/Cultural-Tourism-Project-Planning-Skills)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Ready-9775fa)](https://claude.ai)
[![Codex](https://img.shields.io/badge/Codex-Ready-4ade80)](https://codex.openai.com)
[![Version](https://img.shields.io/badge/version-2.1.0-blue)](./SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Category](https://img.shields.io/badge/category-productivity-orange)](.)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)](.)

> **把策划时间从3天压缩到3小时** — 面向一线文旅策划师的 AI 辅助工具，让规划师专注于创意，而非文书。

</div>

---

<div align="center">

[**🇨🇳 中文**](#-文旅策划规划助手) · [**🇬🇧 English**](./README.en.md)

</div>

---

## 📖 概述

**文旅策划规划助手** 是一个面向文旅行业的专业 AI 辅助技能，支持在多个 AI Agent 平台上运行。

它模拟一位拥有 **10年以上经验** 的注册文旅规划师，遵循《旅游规划通则》(GB/T 18971-2003)，从 **甲方视角** 关注投资回报和落地性。

**V2.2 新增亮点：**

| 新增内容 | 说明 |
|---------|------|
| 🗺️ **SVG功能分区图生成器** [`svg-zoning.py`](./scripts/svg-zoning.py) | 交互输入项目参数，自动生成带饼图、图例、功能描述和承载力估算的暗色主题 HTML 分区图 |
| 🎛️ **策划工具箱总控台** [`planner-toolkit.py`](./scripts/planner-toolkit.py) | 整合所有脚本的统一交互菜单，一键启动任意工具，查看已生成文件 |
| 🚀 **自动策划脚本** [`generate-plan.py`](./scripts/generate-plan.py) | 交互输入项目参数，自动输出八大模块完整 Markdown 策划方案，一键保存到本地 |
| 🌐 **圈层热力图生成器** [`catchment-heatmap.py`](./scripts/catchment-heatmap.py) | 基于项目类型自动生成客源圈层热力图（独立 HTML，含33城市人口数据，深色主题） |
| 📋 **15种报告模板** | 新增商业模式设计、沉浸式情绪价值设计、政策资金申报、土地合规检查清单、康养度假升级版 |
| 📊 **行业数据增强** | 新增十大趋势赛道、她旅游客群画像、5层收入结构数据、全时运营策略、康养市场数据 |

### 核心原则

| 原则 | 说明 |
|------|------|
| 🎭 **角色扮演 + 方法论植入 + 思维链** | 以资深规划师的思维框架引导每一步分析 |
| ❓ **追问优先于编造** | 信息不足时追问用户，绝不胡编乱造 |
| 📊 **数据有源** | 所有估算数据标注为"行业参考范围"或"粗略估算" |
| 🛡️ **合规第一** | 不绕过消防、环保、国土等任何合规要求 |

## 🎯 适用人群

| 角色 | 用途 |
|------|------|
| 👷 **文旅策划师** | 快速生成策划框架、产品组合方案、投资测算初稿 |
| 🗺️ **景区规划人员** | 资源评估、动线规划、空间布局、承载力测算 |
| 🏛️ **政府文旅部门** | 乡村振兴旅游策划、A级景区创建方案、可行性研究 |
| 💼 **咨询公司顾问** | 市场分析、竞品对标、商业计划书、财务测算 |

## 🧩 核心功能模块

| # | 模块 | 说明 |
|---|------|------|
| 1 | **资源禀赋评估** | 五维分类、SWOT矩阵、竞品对标、资源稀缺性评分 |
| 2 | **市场与客群分析** | 圈层分析、客群画像、十大趋势赛道匹配 |
| 3 | **主题定位与IP策划** | 文化解构、在地文化IP激活方法论、故事线 |
| 4 | **空间布局与动线规划** | 布局模式、五层规划体系、七线管控提醒 |
| 5 | **业态策划与产品矩阵** | 业态配比、夜经济五件套、全时运营策略 |
| 6 | **投资测算与风险评估** | 投资估算、三情景收入预测、回收期分析 |
| 7 | **规范报告生成** | 15种结构化模板，学术化转译功能 |
| 8 | **商业模式设计** | 5层收入结构模型、全生命周期盈利策略 |
| 9 | **沉浸式文旅与情绪价值** | 文旅3.0进化模型、六大情绪赛道、五感设计 |
| 10 | **农文旅融合模式** | 四大发展形态、六大融合模式速查 |
| 11 | **康养疗愈旅游** | 五大融合模式、百万亿市场分析 |
| 12 | **政策资金申报** | 八大资金通道、申报流程、六大红线 |
| 13 | **土地合规指引** | 地类速查、四大陷阱、三条合规路径 |
| 14 | **策划方法论验证工具箱** | 策划vs规划区别、三轻三真原则、三大验证清单 |

### 15种内置报告模板

| # | 报告类型 | 版本 |
|---|---------|------|
| 1 | 📋 景区提升规划方案 | V1.0 |
| 2 | 🌾 乡村振兴旅游策划方案 | V1.0 |
| 3 | 🏖️ 度假区申报方案 | V1.0 |
| 4 | 🎒 研学基地策划方案 | V1.0 |
| 5 | 💰 文旅商业计划书 | V1.0 |
| 6 | 📑 可行性研究报告 | V1.0 |
| 7 | 🏆 A级景区创建方案 | V1.0 |
| 8 | 🌃 夜经济项目策划方案 | V1.0 |
| 9 | 🏥 康养度假项目方案 | V1.0 |
| 10 | 🏭 工业旅游改造方案 | V1.0 |
| 11 | 🏗️ **商业模式设计方案** | **V2.0 新增** |
| 12 | 🎭 **沉浸式文旅·情绪价值设计** | **V2.0 新增** |
| 13 | 💸 **政策资金申报方案** | **V2.0 新增** |
| 14 | 🧱 **土地合规检查清单** | **V2.0 新增** |
| 15 | 🌿 **康养度假升级方案** | **V2.0 新增** |

## 🚀 触发方式

### 意图识别

直接说或输入：

```
帮我做个景区规划
分析这个村适合搞旅游吗
写个文旅策划方案
测算一下投资回报
```

### 快捷指令

| 指令 | 功能 |
|------|------|
| `/plan` | 完整策划流程（14大模块） |
| `/swot` | SWOT 分析 |
| `/calculate` | 投资测算 |
| `/report` | 生成报告 |

### 文件上传

支持上传：调研报告、照片、Excel数据表、CAD简图等，AI自动解析内容。

## ⚡ 快速开始

```bash
# 触发一个完整的文旅策划流程
/plan

# 或者直接输入需求
> 我想为一个1000亩的滨水村庄做乡村旅游策划，
> 距离省会城市1.5小时车程，有农田和古树资源
```

AI 会自动启动 **资源盘点 → 市场定位 → 主题提炼 → 空间动线 → 投资算账** 的全流程分析。

## 🔌 多平台安装与使用

本技能支持以下 AI Agent 平台，您可根据自身环境选择使用方式：

### 🤖 Hermes Agent

将本仓库安装为 Hermes Skill：

```bash
# 从本地目录安装
hermes skill install /path/to/cultural-tourism-planner

# 从 GitHub 安装
hermes skill install https://github.com/owenwuhaha/Cultural-Tourism-Project-Planning-Skills
```

安装后，在对话中直接输入需求即可触发（如"帮我做个景区规划"）。

### 🐾 OpenClaw

OpenClaw 支持加载 SKILL.md 格式的技能文件。

**方法一：导入技能目录**
```bash
git clone https://github.com/owenwuhaha/Cultural-Tourism-Project-Planning-Skills.git
openclaw skill load ./Cultural-Tourism-Project-Planning-Skills
```

**方法二：手动复制**
将 `SKILL.md` 及 `references/`、`scripts/` 目录复制到 OpenClaw 的技能目录下即可。

### 💬 Claude Code (Anthropic)

**方法一：Project Instructions（推荐）**

将项目中的提示词模板添加到 Claude Code 的项目指令中。在 `CLAUDE.md` 或项目设置中添加：

```markdown
## 文旅策划助手

你拥有文旅策划规划的专业能力，遵循以下原则：
- 角色扮演一位10年以上经验注册文旅规划师
- 追问优先于编造，信息不足时必须追问
- 数据有源，禁止编造法定红线信息
- 合规第一

### 工作流程（内部必须按此顺序思考）
1. 资源盘点 → 2. 市场定位 → 3. 主题提炼 → 4. 空间动线 → 5. 投资算账
```

**方法二：对话中直接激活**

在 Claude Code 会话中输入：
> 请以文旅策划规划师身份，按五步工作流（资源-市场-主题-动线-投资）帮我策划一个项目

### ✨ Codex (OpenAI)

**方法一：System Prompt**

在 Codex 的 Instructions 或 system prompt 中添加：

```markdown
You are a registered cultural tourism planner with 10+ years of experience.
Follow this workflow for every project:
1. Resource Inventory — what resources does the site have?
2. Market Positioning — who will visit and why?
3. Theme Extraction — what's the unique story?
4. Spatial Flow — how do visitors move and spend?
5. Financial Analysis — can the client make money?
Ask questions when info is insufficient. Never fabricate data. Stay compliant.
```

**方法二：文件引用**

将 `references/industry-data.md` 作为项目上下文文件添加到 Codex 项目中。

### 📋 平台对比

| 平台 | 安装方式 | 推荐程度 |
|------|---------|---------|
| 🟣 **Hermes Agent** | `hermes skill install` 一键安装 | ⭐ 原生支持 |
| 🟠 **OpenClaw** | 导入 SKILL.md 目录 | ⭐ 完全兼容 |
| 🟢 **Claude Code** | CLAUDE.md 项目指令 | ✅ 手动配置 |
| 🔵 **Codex (OpenAI)** | System Prompt 设定 | ✅ 手动配置 |

## 🛠️ 配套工具脚本

本仓库提供了5个可直接运行的 Python 工具脚本：

| 脚本 | 版本 | 功能描述 | 用法 |
|------|------|---------|------|
| [`scripts/planner-toolkit.py`](./scripts/planner-toolkit.py) | V2.2 🆕 | **策划工具箱总控台** — 整合所有脚本的统一交互菜单 | `python planner-toolkit.py` |
| [`scripts/svg-zoning.py`](./scripts/svg-zoning.py) | V2.2 🆕 | **SVG功能分区图生成** — 自动生成带饼图的暗色主题 HTML 分区图 | `python svg-zoning.py` |
| [`scripts/generate-plan.py`](./scripts/generate-plan.py) | V2.1 | **自动策划脚本** — 交互输入项目参数，自动生成八大模块完整 Markdown 策划方案 | `python generate-plan.py` |
| [`scripts/catchment-heatmap.py`](./scripts/catchment-heatmap.py) | V2.1 | **圈层热力图生成** — 生成独立 HTML 客源圈层热力图（含33城市人口数据） | `python catchment-heatmap.py` |
| [`scripts/investment-calc.py`](./scripts/investment-calc.py) | V2.0 | **投资测算工具** — 三情景预测、5层收入模型、敏感性分析 | `python investment-calc.py` |

> 📝 所有脚本为纯 Python 标准库实现，无需安装第三方依赖，直接运行即可。

## 📊 参考数据

| 文件 | 内容 |
|------|------|
| [`references/industry-data.md`](./references/industry-data.md) | 行业标准、投资门槛、客单价、毛利率、市场规模、十大趋势、5层收入、康养数据 |
| [`references/report-templates.md`](./references/report-templates.md) | 15种策划报告完整模板（含V2.0新增商业模式/沉浸式/政策申报/土地合规/康养升级） |

## 📂 仓库文件结构

```
Cultural-Tourism-Project-Planning-Skills/
├── SKILL.md                       # 技能定义（14大模块 V2.2）
├── README.md                      # 中文默认README（默认呈现中文版）
├── README.en.md                   # 英文版README（通过切换链接访问）
├── references/                    # 行业数据 + 报告模板
│   ├── industry-data.md           # 行业标准与参考数据（284行）
│   └── report-templates.md        # 15种策划报告模板（975行）
└── scripts/                       # 可运行工具脚本
    ├── planner-toolkit.py           # 策划工具箱总控台（V2.2 新增）
    ├── svg-zoning.py                # SVG功能分区图生成（V2.2 新增）
    ├── generate-plan.py             # 自动策划脚本（V2.1）
    ├── catchment-heatmap.py         # 圈层热力图生成（V2.1）
    └── investment-calc.py           # 投资测算工具（V2.0）
```

## 🗺️ 版本规划

| 版本 | 计划功能 | 状态 |
|------|---------|------|
| V1.0 | 14大模块 + 引导模式 + 追问优化 + 方案后续产出 | ✅ 已完成 |
| V2.0 | 知识库八大维度集成 + README中英文分离 + 15种模板 + 行业数据增强 | ✅ 已完成 |
| **V2.1** | **自动策划脚本 + 圈层热力图生成工具** | ✅ **已完成** |
| **V2.2** | **策划工具箱总控台 + SVG功能分区图生成器** | ✅ **已完成** |
| V2.3 | 接入地图API，自动生成圈层热力图（增强版 + 真实地图） | 🔜 规划中 |
| V2.4 | 知识库动态查询（按需加载wenlv-wiki） | 🔜 规划中 |
| V2.5 | 自动出SVG功能分区图（增强版 + 3D视图） | 🔜 规划中 |
| V3.0 | GIS系统集成，输出可编辑矢量布局图 | 🔜 规划中 |

## 📄 License

MIT © 2025 [吴晓 (crazyowen)](https://github.com/crazyowen)

---

<div align="center">

**由一线策划师打造，为一线策划师服务。**

[报告问题](https://github.com/owenwuhaha/Cultural-Tourism-Project-Planning-Skills/issues) · [功能建议](https://github.com/owenwuhaha/Cultural-Tourism-Project-Planning-Skills/issues)

</div>
