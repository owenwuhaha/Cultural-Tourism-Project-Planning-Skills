<div align="center">

# 🏔️ Cultural Tourism Planner

**AI-Powered Cultural Tourism Project Planning Skills**

[![Hermes Skill](https://img.shields.io/badge/Hermes-Skill-8A2BE2)](https://hermes-agent.nousresearch.com)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-ff6b6b)](https://github.com/owenwuhaha/Cultural-Tourism-Project-Planning-Skills)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Ready-9775fa)](https://claude.ai)
[![Codex](https://img.shields.io/badge/Codex-Ready-4ade80)](https://codex.openai.com)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](./SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Category](https://img.shields.io/badge/category-productivity-orange)](.)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)](.)

> **Cut planning time from 3 days to 3 hours** — AI-powered cultural tourism planning that lets planners focus on creativity, not paperwork.

</div>

---

<div align="center">

[**🇬🇧 English**](#-cultural-tourism-planner) · [**🇨🇳 中文**](./README.md)

</div>

---

## 📖 Overview

**Cultural Tourism Planner** is a professional AI-powered planning assistant for the cultural tourism industry, compatible with multiple AI Agent platforms.

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

## 🔌 Multi-Platform Installation

This skill works across multiple AI Agent platforms. Choose the one that fits your workflow:

### 🤖 Hermes Agent

Install as a native Hermes Skill:

```bash
# Install from local directory
hermes skill install /path/to/cultural-tourism-planner

# Install from GitHub
hermes skill install https://github.com/owenwuhaha/Cultural-Tourism-Project-Planning-Skills
```

Once installed, trigger it naturally in conversation (e.g., "Create a scenic area plan for me").

### 🐾 OpenClaw

OpenClaw supports loading SKILL.md-format skill files natively.

**Method 1: Import skill directory**
```bash
# Clone the repo
git clone https://github.com/owenwuhaha/Cultural-Tourism-Project-Planning-Skills.git

# Load via OpenClaw's skill command
openclaw skill load ./Cultural-Tourism-Project-Planning-Skills
```

**Method 2: Manual copy**
Copy `SKILL.md`, `references/`, and `scripts/` into your OpenClaw skill directory.

### 💬 Claude Code (Anthropic)

**Method 1: Project Instructions (Recommended)**

Add the following to your `CLAUDE.md` or project instructions:

```markdown
## Cultural Tourism Planner

You have expertise in cultural tourism planning. Follow these principles:
- Role-play as a senior planner with 10+ years experience
- Ask before fabricating — always question when info is insufficient
- Cite data sources, never fabricate regulated information
- Stay compliant with all regulations

### Required Workflow (internal reasoning order)
1. Resource Inventory → 2. Market Positioning → 3. Theme Extraction → 4. Spatial Flow → 5. Financial Analysis
```

**Method 2: Activate in conversation**

In any Claude Code session, simply say:
> Act as a cultural tourism planner. Follow the 5-step workflow (resources → market → theme → flow → finance) to plan a project for me.

### ✨ Codex (OpenAI)

**Method 1: System Prompt**

Add this to your Codex Instructions or system prompt:

```markdown
You are a registered cultural tourism planner with 10+ years of experience.
Follow this workflow for every project:
1. Resource Inventory — what resources does the site have?
2. Market Positioning — who will visit and why?
3. Theme Extraction — what's the unique story?
4. Spatial Flow — how do visitors move and spend?
5. Financial Analysis — can the client make money?
Ask questions when info is insufficient. Never fabricate data. Stay compliant with regulations.
```

**Method 2: File reference**

Add `references/industry-data.md` as a project context file in your Codex project.

### 📋 Platform Comparison

| Platform | Installation | Recommendation |
|----------|-------------|----------------|
| 🟣 **Hermes Agent** | `hermes skill install` — one command | ⭐ Native |
| 🟠 **OpenClaw** | Import SKILL.md directory | ⭐ Fully Compatible |
| 🟢 **Claude Code** | CLAUDE.md project instructions | ✅ Manual Setup |
| 🔵 **Codex (OpenAI)** | System Prompt configuration | ✅ Manual Setup |

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

## 📄 License

MIT © 2025 [Xiao Wu (crazyowen)](https://github.com/crazyowen)

---

<div align="center">

**Built by a practitioner, for practitioners.**

[Report Issue](https://github.com/owenwuhaha/Cultural-Tourism-Project-Planning-Skills/issues) · [Request Feature](https://github.com/owenwuhaha/Cultural-Tourism-Project-Planning-Skills/issues)

</div>
