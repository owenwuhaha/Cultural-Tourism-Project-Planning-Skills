
<p align="center">
  <img src="https://img.shields.io/badge/版本-1.0.0-blue" alt="Version 1.0.0">
  <img src="https://img.shields.io/badge/许可-MIT-green" alt="License MIT">
  <img src="https://img.shields.io/badge/平台-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey" alt="Platforms">
  <img src="https://img.shields.io/badge/适用-Hermes%20Agent-purple" alt="Hermes Agent">
</p>

<h1 align="center">🏔️ 文旅策划规划助手</h1>
<p align="center"><strong>Cultural Tourism Project Planning Skills — Hermes Agent Skill</strong></p>
<p align="center">不是替代规划师，而是帮规划师把写PPT、查数据、画脑图的时间从 <strong>3天压缩到3小时</strong>。</p>

---

## 📖 概述

本技能面向 **文旅策划师、景区规划人员、政府文旅部门、咨询公司**，提供从资源盘点、市场分析、主题策划、业态规划、投资测算到报告生成的全流程辅助。

**设计原则：**
- 🧠 **角色扮演 + 方法论植入 + 思维链** — 以资深规划师的思维框架引导每一步
- ❓ **追问优先于编造** — 信息不足时必须追问，绝不胡编乱造
- 📊 **数据有源** — 所有估算数据标注为"行业参考范围"
- ⚖️ **合规第一** — 不绕过消防、环保、国土等任何合规要求

---

## ✨ 核心功能

| 模块 | 功能 | 输出 |
|------|------|------|
| **1️⃣ 资源禀赋评估** | 五维资源分类 + SWOT矩阵 | 结构化资源清单 |
| **2️⃣ 市场与客群分析** | 半径圈层 / 客群画像 / 趋势捕捉 | 市场规模估算 |
| **3️⃣ 主题定位与IP策划** | 地缘文化解构 + Slogan生成 + 微剧本 | 3-5个主题方向 |
| **4️⃣ 空间布局与动线规划** | 地形适配 + 黄金动线 + 承载力估算 | 功能分区方案 |
| **5️⃣ 业态策划与产品矩阵** | 轻/重资产配比 + 夜经济五件套 | 爆款产品清单 |
| **6️⃣ 投资测算与风险评估** | 投资估算 + 收入预测 + 回收期 + 敏感性分析 | 财务测算表 |
| **7️⃣ 规范报告生成** | 10种行业标准模板 | 结构化策划方案 |

---

## 🚀 快速开始

### 环境要求

- [Hermes Agent](https://hermes-agent.nousresearch.com/) 已安装并运行
- Python 3.8+（仅投资测算脚本需要）

### 安装方式

```bash
# 方式一：通过 Hermes Skills 安装（推荐）
hermes skills install https://github.com/你的用户名/cultural-tourism-planner

# 方式二：手动复制
git clone https://github.com/你的用户名/cultural-tourism-planner.git
hermes skills install ./cultural-tourism-planner
```

### 使用方式

在 Hermes Agent 中直接输入：

```
"帮我做个景区规划"
"分析这个村适合搞旅游吗"
"写个文旅策划方案"
"测算一下投资回报"
"帮我做个SWOT分析"
```

或使用快捷指令：

```
/plan    完整策划
/swot    SWOT分析
/calculate   投资测算
/report    生成报告
```

---

## 📂 项目结构

```
cultural-tourism-planner/
├── SKILL.md                    # 技能主文件（七大模块+追问机制）
├── references/
│   ├── industry-data.md        # 行业标准与投资参考数据
│   └── report-templates.md     # 10种策划报告模板
├── scripts/
│   └── investment_calc.py      # 交互式投资测算工具
├── LICENSE
└── README.md
```

---

## 📊 投资测算工具

交互��命令行工具，三步完成财务测算：

```bash
cd scripts
python investment_calc.py
```

**三阶段流程：**
1. **投资估算** — 输入面积和档次，自动计算建安/景观/软装/设计费用
2. **收入预测** — 输入客流量和消费数据，输出年收入和利润
3. **回收期+敏感性分析** — 计算静态回收期，展示客流±30%的变化影响

> 💡 *测算工具内置行业参考中值，可直接回车使用默认值，快速出数。*

---

## 📝 内置报告模板（10种）

| # | 模板类型 | 适用场景 |
|---|---------|---------|
| 1 | 景区提升规划方案 | 现有景区升级改造 |
| 2 | 乡村振兴旅游策划方案 | 农文旅融合项目 |
| 3 | 度假区项目策划方案 | 综合度假区/主题度假 |
| 4 | 研学基地策划方案 | 教育+旅游融合 |
| 5 | 商业计划书（文旅项目） | 融资/招商 |
| 6 | 可行性研究报告大纲 | 决策/审批/备案 |
| 7 | A级景区创建方案 | 评A/升A |
| 8 | 夜经济项目策划 | 夜间消费打造 |
| 9 | 康养度假项目策划 | 银发/康养经济 |
| 10 | 工业旅游改造方案 | 企业品牌展示 |

---

## ⚙️ 追问机制

当信息不足时，按优先级自动追问（最多3轮/每次不超过3个问题��：

**第一轮（基础）：** 位置？面积？目标客群？
**第二轮（深度）：** 预算？地形？特色资源？
**第三轮（决策）：** 新建/改造？A级/示范点？夜经济？

---

## 🧠 角色设定

> 您是一位拥有10年以上经验的注册文旅规划师，精通《旅游规划通则》(GB/T 18971-2003)，擅长从甲方视角关注投资回报和落地性，参与过50+文旅项目策划。

---

## 🗺️ 版本规划

| 版本 | 计划功能 |
|------|---------|
| **V1.0** ✅ | 基础七大模块 + 报告生成 + 追问机制 |
| **V1.1** 🔜 | 接入地图API，自动生成圈层热力图 |
| **V1.2** 🔜 | 增加竞品案例库（500+已开发文旅项目） |
| **V1.3** 🔜 | 支持多模态（手绘草图→功能分区图） |
| **V2.0** 🔜 | 接入GIS系统，输出可编辑的矢量布局图 |

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/xxx`)
3. 提交修改 (`git commit -m 'feat: 添加xxx功能'`)
4. 推送分支 (`git push origin feature/xxx`)
5. 提交 Pull Request

---

## 📄 许可

[MIT License](LICENSE) © 2026 [疯狂的豇豆](https://www.crazyowen.cn)

---

<p align="center">
  <sub>Made with ❤️ by <a href="https://www.crazyowen.cn">疯狂的豇豆</a></sub>
  <br>
  <sub>文旅策划 · AI赋能 · 轻资产运营</sub>
</p>
