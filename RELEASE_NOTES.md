# Release Notes — Cultural-Tourism-Project-Planning-Skills

## v2.0.0 → v2.6.0 合并发布

---

**中文：**

### 文旅策划规划助手 V2.0 → V2.6 汇总发布

从知识库集成到真实地图圈层热力图，一个工具集从零到8个脚本、14大模块、33页知识库的完整进化。

---

#### V2.0 — 知识库八大维度集成 + 中英文分离
- 集成八大知识库维度：政策法规、策划方法论、规划体系、农文旅融合、康养疗愈、运营升级、商业模式、行业趋势
- README 中英文分离（中文默认，可切换英文）
- references/industry-data.md — 285行行业参考数据（投资/客群/政策/工艺参数）
- references/report-templates.md — 15个结构化文旅策划方案模板
- scripts/investment-calc.py — 投资测算工具（4种模式 x 4种业态 x 5层收入结构）

#### V2.1 — 自动策划脚本 + 圈层热力图
- scripts/generate-plan.py — 自动策划脚本：交互输入项目参数，自动生成结构化HTML方案（含市场分析、定位策略、分区、投资测算）
- scripts/catchment-heatmap.py — 客源圈层热力图SVG版：1h/2h/3h交通圈，按项目类型自动配比

#### V2.2 — 策划工具箱总控台 + SVG分区图
- scripts/planner-toolkit.py — 总控台：统一交互菜单整合所有脚本
- scripts/svg-zoning.py — SVG功能分区图：饼图+图例+承载力估算，暗色文旅主题

#### V2.3 — 竞品对标分析工具
- scripts/competitive-analysis.py — 竞品对标分析（纯Python，零依赖）
  - 6维竞争力雷达图（资源/交通/产品/市场/投资/运营）
  - 竞争力气泡矩阵散点图
  - 自动SWOT分析 + 差异化策略建议
  - 支持2-5个竞品，暗色主题HTML

#### V2.4 — 项目总览看板
- scripts/project-dashboard.py — 自动扫描 projects/ 目录聚合所有报告
  - 统计看板、工具分布条形图、可折叠项目卡片
  - 支持10+文件格式，直接浏览器打开

#### V2.5 — 知识库动态查询
- scripts/knowledge-query.py — 交互浏览wenlv-wiki 33页知识库
  - 关键词搜索、8维度浏览、类型筛选、详情预览
  - 导出暗色主题HTML看板

#### V2.6 — 圈层热力图增强版（真实地图）
- scripts/catchment-heatmap.py 全面重写为V2.6增强版
  - 集成 Leaflet.js + OpenStreetMap 真实地图底图（CartoDB暗色GIS风格）
  - 24个内置中国城市坐标库（一线→景区镇）
  - 信息仪表板升级：项目概要/圈层覆盖/人口估算/运营策略
  - 响应式设计，零安装
- references/industry-data.md — 新增第九章「圈层热力图参考数据」
  - 项目类型x客源圈层渗透配比表
  - 城市等级x人口估算模型
  - 24城市坐标库
  - 圈层运营策略速查

---

**English:**

### Cultural Tourism Planner — V2.0 to V2.6 Consolidated Release

From knowledge base integration to real-map catchment heatmaps — a complete toolset evolved from zero to 8 scripts, 14 modules, and a 33-page knowledge base.

#### V2.0 — Knowledge Base + EN/CN README
- 8 knowledge base dimensions: policy, planning, agri-culture-tourism, wellness, operations, business model, trends
- Bilingual README (Chinese default, English switchable)
- references/industry-data.md — 285 lines industry reference data
- references/report-templates.md — 15 planning templates
- scripts/investment-calc.py — Investment calculator

#### V2.1 — Auto Planning Script + Heatmap
- scripts/generate-plan.py — Interactive input to structured HTML plan
- scripts/catchment-heatmap.py — SVG catchment heatmap with 1h/2h/3h rings

#### V2.2 — Toolkit Dashboard + SVG Zoning
- scripts/planner-toolkit.py — Unified dashboard for all tools
- scripts/svg-zoning.py — SVG zoning map with pie chart, legend, capacity estimation

#### V2.3 — Competitive Analysis
- scripts/competitive-analysis.py — 6D radar chart, bubble matrix, SWOT, differentiation strategy (zero dependencies)

#### V2.4 — Project Dashboard
- scripts/project-dashboard.py — Auto-scan and aggregate all reports, collapsible cards, 10+ format support

#### V2.5 — Knowledge Base Query
- scripts/knowledge-query.py — Interactive browse of 33-page wenlv-wiki, keyword search, dimension browse, HTML export

#### V2.6 — Enhanced Catchment Heatmap (Real Map)
- scripts/catchment-heatmap.py completely rewritten:
  - Leaflet.js + OpenStreetMap real map (CartoDB dark GIS theme)
  - 24 built-in Chinese city coordinates
  - Upgraded info dashboard
  - Responsive, zero install
- references/industry-data.md — New chapter 9: Catchment Heatmap Reference Data
