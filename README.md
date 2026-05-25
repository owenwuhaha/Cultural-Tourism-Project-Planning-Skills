<div align="center">

# 🏔️ Cultural Tourism Planner

**文旅策划规划助手 — AI-Powered Planning Assistant**

[![Hermes Skill](https://img.shields.io/badge/Hermes-Skill-8A2BE2)](https://hermes-agent.nousresearch.com)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](./SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Category](https://img.shields.io/badge/category-productivity-orange)](.)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)](.)

> **Cut planning time from 3 days to 3 hours** — AI-powered cultural tourism planning that lets planners focus on creativity, not paperwork.

</div>

---

<div align="center">

[**🇬🇧 English**](#-english) · [**🇨🇳 中文**](#-中文文档)

</div>

---

# 🇬🇧 English

## 📖 Overview

**Cultural Tourism Planner** is a professional AI-powered planning assistant for the cultural tourism industry, built for the Hermes Agent ecosystem.

It simulates a **registered cultural tourism planner with 10+ years of experience**, adhering to China's *Tourism Planning General Code* (GB/T 18971-2003). It approaches every project from the **client/investor's perspective**, focusing on ROI and practical feasibility.

### Core Principles

| Principle | Description |
|-----------|-------------|
| 🎭 **Role-Play + Methodology + CoT** | Guided analysis framework simulating a senior planner's thinking |
| ❓ **Ask Before Fabricate** | Always ask the user when information is insufficient — never make up data |
| 📊 **Data with Sources** | All estimates labeled as "industry reference range" or "rough estimate" |
| 🛡️ **Compliance First** | Never bypass fire safety, environmental, or land-use regulations |

## 🎯 Target Users

| Role | Use Case |
|------|----------|
| 👷 **Tourism Planners** | Rapid framework generation, product mix design, preliminary financial modeling |
| 🗺️ **Scenic Area Operators** | Resource assessment, visitor flow planning, spatial layout, capacity estimation |
| 🏛️ **Government Tourism Departments** | Rural revitalization planning, A-level scenic area certification, feasibility studies |
| 💼 **Consultants** | Market analysis, competitive benchmarking, business plans, financial projections |

## 🧩 Core Modules

| # | Module | Features | Output |
|---|--------|----------|--------|
| 1 | **Resource Assessment** | 5-dimension classification, SWOT matrix, competitive benchmarking, rarity scoring | Structured resource inventory + SWOT analysis |
| 2 | **Market & Audience Analysis** | Radius analysis, persona generation, trend matching, differentiation advice | Personas + market size estimate |
| 3 | **Theme & IP Planning** | Cultural deconstruction, theme direction generation, slogan creation, micro-scripts | 3-5 theme directions + brand slogan |
| 4 | **Spatial Layout & Flow Planning** | Layout mode recommendation, visitor flow simulation, capacity estimation, zone ratio | Functional zones + flow description |
| 5 | **Product Mix Planning** | Asset-light/heavy recommendations, night economy solutions | Product mix table + item list |
| 6 | **Financial Modeling & Risk Assessment** | Investment estimation, revenue forecast, payback period, risk analysis | Financial model + risk report |
| 7 | **Report Generation** | 10 structured templates for different project types | Markdown-format planning document |

### 10 Built-in Report Templates

| # | Report Type |
|---|-------------|
| 1 | 📋 Scenic Area Upgrade Plan |
| 2 | 🌾 Rural Revitalization Tourism Plan |
| 3 | 🏖️ Resort Development Plan |
| 4 | 🎒 Study Base (研学基地) Plan |
| 5 | 💰 Business Plan (Tourism Projects) |
| 6 | 📑 Feasibility Study Report Outline |
| 7 | 🏆 A-Level Scenic Area Certification Plan |
| 8 | 🌃 Night Economy Project Plan |
| 9 | 🏥 Wellness & Healthcare Resort Plan |
| 10 | 🏭 Industrial Tourism Transformation Plan |

## 🚀 How to Trigger

### Intent Recognition

Simply say or type:

```
Create a scenic area plan for me
Analyze if this village is suitable for tourism
Write a cultural tourism planning proposal
Calculate the investment return
```

### Quick Commands

| Command | Function |
|---------|----------|
| `/plan` | Full planning workflow |
| `/swot` | SWOT Analysis |
| `/calculate` | Investment calculation |
| `/report` | Generate report |

### File Upload

Supports: research reports, photos, Excel spreadsheets, CAD sketches — the AI automatically parses the content.

## ⚡ Quick Start

```bash
# Trigger a full planning workflow
/plan

# Or directly describe your project
> I want to plan rural tourism for a 1000-mu lakeside village, 
> 1.5 hours from the provincial capital, with farmland and ancient trees
```

The AI will automatically run through the complete workflow: **Resource Inventory → Market Positioning → Theme Extraction → Spatial Flow → Financial Analysis**.

## 📊 Reference Data

The skill includes extensive industry reference data:

| File | Content |
|------|---------|
| [`references/industry-data.md`](./references/industry-data.md) | Industry standards, investment thresholds, pricing, gross margins, market data, policy trends |
| [`references/report-templates.md`](./references/report-templates.md) | 10 complete planning report templates |
| [`scripts/investment_calc.py`](./scripts/investment_calc.py) | Investment calculation Python script |

## 🗺️ Roadmap

| Version | Features | Status |
|---------|----------|--------|
| V1.0 | 7 core modules + report generation + questioning mechanism | ✅ Complete |
| V1.1 | Map API integration, automatic heatmap generation | 🔜 Planned |
| V1.2 | Competitor case library (500+ projects) | 🔜 Planned |
| V1.3 | Multi-modal support (hand-drawn sketch → functional zoning) | 🔜 Planned |
| V2.0 | GIS integration, editable vector layout output | 🔜 Planned |

---

<div align="right">

[⬆ Back to top](#-) · [🇨🇳 切换到中文](#-中文文档)

</div>

---

# 🇨🇳 中文文档

## 📖 概述

**文旅策划规划助手** 是一个面向文旅行业的专业 AI 辅助技能，为 Hermes Agent 生态系统打造。

它模拟一位拥有 **10年以上经验** 的注册文旅规划师，遵循《旅游规划��则》(GB/T 18971-2003)，从 **甲方视角** 关注投资回报和落地性。

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

| # | 模块 | 功能 | 输出 |
|---|------|------|------|
| 1 | **资源禀赋评估** | 五维分类、SWOT矩阵、竞品对标、稀缺性评分 | 结构化资源清单 + SWOT分析 |
| 2 | **市场与客群分析** | 圈层分析、客群画像、趋势捕捉、差异化建议 | 客群画像 + 市场规模估算 |
| 3 | **主题定位与IP策划** | 文化解构、主题方向、Slogan生成、微剧本 | 3-5个主题方向 + 品牌Slogan |
| 4 | **空间布局与动线规划** | 布局模式、动线模拟、承载力估算、分区比例 | 功能分区 + 动线描述 |
| 5 | **业态策划与产品矩阵** | 业态配比、轻/重资产推荐、夜经济方案 | 业态配比表 + 产品清单 |
| 6 | **投资测算与风险评估** | 投资估算、收入预测、回收期、风险提示 | 财务模型 + 风险报告 |
| 7 | **规范报告生成** | 10种结构化模板，适配不同项目类型 | Markdown格式策划方案 |

### 10种内置报告模板

| # | 报告类型 |
|---|---------|
| 1 | 📋 景区提升规划方案 |
| 2 | 🌾 乡村振兴旅游策划方案 |
| 3 | 🏖️ 度假区策划方案 |
| 4 | 🎒 研学基地策划方案 |
| 5 | 💰 商业计划书（文旅项目） |
| 6 | 📑 可行性研究报告大纲 |
| 7 | 🏆 A级景区创建方案 |
| 8 | 🌃 夜经济项目策划方案 |
| 9 | 🏥 康养度假项目策划方案 |
| 10 | 🏭 工业旅游改造方案 |

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
| `/plan` | 完整策划流程 |
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
> 我想为一个1000亩的滨水村庄做乡村旅游策划，距离省会城市1.5小时车程，有农田和古树资源
```

AI 会自动启动 **资源盘点 → 市场定位 → 主题提炼 → 空间动线 → 投资算账** 的全流程分析。

## 📊 参考数据

| 文件 | 内容 |
|------|------|
| [`references/industry-data.md`](./references/industry-data.md) | 行业标准、投资门槛、客单价、毛利率、市场规模、政策热点 |
| [`references/report-templates.md`](./references/report-templates.md) | 10种策划报告完整模板 |
| [`scripts/investment_calc.py`](./scripts/investment_calc.py) | 投资测算Python脚本 |

## 🗺️ 版本规划

| 版本 | 计划功能 | 状态 |
|------|---------|------|
| V1.0 | 基础七大模块 + 报告生成 + 追问机制 | ✅ 已完成 |
| V1.1 | 接入地图API，自动生成圈层热力图 | 🔜 规划中 |
| V1.2 | 增加竞品案例库（500+已开发文旅项目） | 🔜 规划中 |
| V1.3 | 多模态支持（手绘草图→功能分区图） | 🔜 规划中 |
| V2.0 | 接入GIS系统，输出可编辑的矢量布局图 | 🔜 规划中 |

---

<div align="right">

[⬆ 回到顶部](#-) · [🇬🇧 Switch to English](#-english)

</div>

---

## 📄 License

MIT © 2025 [吴晓 (crazyowen)](https://github.com/crazyowen)

---

<div align="center">

**Built by a practitioner, for practitioners.**  
由一线策划师打造，为一线策划师服务。

[Report Issue](https://github.com/crazyowen/cultural-tourism-planner/issues) · [Request Feature](https://github.com/crazyowen/cultural-tourism-planner/issues)

</div>
