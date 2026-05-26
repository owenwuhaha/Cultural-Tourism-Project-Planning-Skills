#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客源圈层热力图生成工具
Catchment Area Heatmap Generator — V2.1

适用场景：文旅策划 / 景区规划 / 可行性研究
功能说明：
  1. 交互输入：城市名、项目类型、预期日均客流
  2. 自动生成独立 HTML 文件（深色墨绿暗金主题），内联 SVG 绘制
  3. 三个同心圆代表 1h/2h/3h 交通圈，标注客源覆盖目标与人口估算
  4. 按项目类型自动调整客源覆盖配比
  5. 中文页面、响应式布局、可离线浏览器直接打开

依赖：Python 3.7+ (标准库, 无需第三方包)
运行：python catchment-heatmap.py
输出：F:/owen/hermes/projects/{项目名}_热力图.html

参考：
  - SKILL.md 模块4（空间布局与动线规划）
  - references/industry-data.md（场地工艺参数）
"""

import os
import re
import webbrowser
from pathlib import Path

# ── 版本信息 ──────────────────────────────────────────────────
VERSION = "V2.1"

# ── 项目类型客源覆盖配比 ──────────────────────────────────────
CATCHMENT_RATIOS = {
    "观光型": {"1h": 0.60, "2h": 0.30, "3h": 0.10,
              "desc_1h": "高频短途，依靠自然流量和门票性价比",
              "desc_2h": "周末出行主力，需要一定的旅游吸引力",
              "desc_3h": "偶发出行，需强IP或节庆活动驱动"},
    "度假型": {"1h": 0.30, "2h": 0.40, "3h": 0.30,
              "desc_1h": "日常近距离度假客群，复购率高",
              "desc_2h": "周末度假主力，住宿+体验消费充足",
              "desc_3h": "中远程度假客，需独特住宿与内容吸引"},
    "复合型": {"1h": 0.40, "2h": 0.35, "3h": 0.25,
              "desc_1h": "高频基础客流，观光+轻体验",
              "desc_2h": "含住宿的中距离客群，消费力强",
              "desc_3h": "品牌辐射客群，靠口碑与IP拉动"},
    "康养型": {"1h": 0.20, "2h": 0.30, "3h": 0.50,
              "desc_1h": "近程康养日常体验客",
              "desc_2h": "周末/短期康养旅居客",
              "desc_3h": "远距离康养核心客群，长停留高消费"}
}

# ── 城市人口估算数据（万人） ─────────────────────────────────
# 基于中国城市统计年鉴与行业经验值的圈层人口估算参考
# 单位为万人次 — 实际为吸附范围内常住人口估算
CITY_POPULATION_ESTIMATE = {
    # 一线/超一线
    "北京":  {"1h": 2800, "2h": 4500, "3h": 6800},
    "上海":  {"1h": 2600, "2h": 4200, "3h": 8000},
    "广州":  {"1h": 2000, "2h": 3800, "3h": 6500},
    "深圳":  {"1h": 1800, "2h": 3500, "3h": 6000},
    # 新一线
    "成都":  {"1h": 2100, "2h": 3800, "3h": 5500},
    "重庆":  {"1h": 2500, "2h": 4200, "3h": 5800},
    "杭州":  {"1h": 1300, "2h": 2500, "3h": 4500},
    "武汉":  {"1h": 1400, "2h": 2800, "3h": 4200},
    "西安":  {"1h": 1300, "2h": 2400, "3h": 4000},
    "南京":  {"1h": 1100, "2h": 2200, "3h": 3800},
    "长沙":  {"1h": 1000, "2h": 2000, "3h": 3500},
    "郑州":  {"1h": 1300, "2h": 2500, "3h": 4000},
    "苏州":  {"1h": 1300, "2h": 2000, "3h": 3500},
    "天津":  {"1h": 1600, "2h": 3000, "3h": 4500},
    "青岛":  {"1h": 1100, "2h": 2000, "3h": 3200},
    "合肥":  {"1h": 1000, "2h": 1800, "3h": 3000},
    "昆明":  {"1h": 1000, "2h": 1800, "3h": 3000},
    "沈阳":  {"1h": 1200, "2h": 2200, "3h": 3500},
    "大连":  {"1h": 900,  "2h": 1800, "3h": 3000},
    "宁波":  {"1h": 1000, "2h": 1800, "3h": 3000},
    "厦门":  {"1h": 700,  "2h": 1400, "3h": 2600},
    "福州":  {"1h": 900,  "2h": 1800, "3h": 3000},
    "济南":  {"1h": 1100, "2h": 2000, "3h": 3400},
    "哈尔滨": {"1h": 1100, "2h": 2000, "3h": 3200},
    "贵阳":  {"1h": 800,  "2h": 1600, "3h": 2800},
    "南宁":  {"1h": 900,  "2h": 1700, "3h": 2800},
    "南昌":  {"1h": 800,  "2h": 1600, "3h": 2800},
    "太原":  {"1h": 800,  "2h": 1500, "3h": 2600},
    "石家庄": {"1h": 1100, "2h": 2000, "3h": 3500},
    "长春":  {"1h": 900,  "2h": 1700, "3h": 2800},
    "兰州":  {"1h": 600,  "2h": 1200, "3h": 2200},
    "乌鲁木齐": {"1h": 500, "2h": 1000, "3h": 1800},
    "海口":  {"1h": 400,  "2h": 800,  "3h": 1500},
    "三亚":  {"1h": 250,  "2h": 500,  "3h": 1000},
}


def estimate_population(city_name: str) -> dict:
    """根据城市名估算圈层人口，未匹配则用通用算法"""
    # 精确匹配
    for key, val in CITY_POPULATION_ESTIMATE.items():
        if key in city_name or city_name in key:
            return val

    # 按城市级别通用估算（不在白名单中的城市）
    # 一般地级市估算
    return {"1h": 500, "2h": 1000, "3h": 1800}


def get_user_input() -> dict:
    """获取用户交互输入"""
    print(f"\n{'='*60}")
    print(f"  客源圈层热力图生成工具  {VERSION}")
    print(f"  文旅策划规划助手 · 行业参考版")
    print(f"{'='*60}\n")

    city = input("📍 请输入项目所在城市名：").strip()
    while not city:
        city = input("   城市名不能为空，请重新输入：").strip()

    print("\n📋 项目类型：")
    types = list(CATCHMENT_RATIOS.keys())
    for i, t in enumerate(types, 1):
        print(f"   {i}. {t}")
    type_choice = input("\n   请选择（输入序号 1-4，默认 3 复合型）：").strip()

    if type_choice in ("1",):
        project_type = "观光型"
    elif type_choice in ("2",):
        project_type = "度假型"
    elif type_choice in ("4",):
        project_type = "康养型"
    else:
        project_type = "复合型"

    daily_input = input(f"\n📊 预期日均客流量（人次，如 3000，默认 3000）：").strip()
    try:
        daily_visitors = int(daily_input)
        if daily_visitors <= 0:
            daily_visitors = 3000
    except ValueError:
        daily_visitors = 3000

    project_name = input(f"\n🏷️  项目名称（用于文件命名，如 黄山度假区）：").strip()
    if not project_name:
        project_name = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', city)
        if not project_name:
            project_name = "文旅项目"

    print(f"\n{'='*60}")
    print(f"  城市：{city}")
    print(f"  类型：{project_type}")
    print(f"  日均客流：{daily_visitors:,} 人次")
    print(f"  项目名：{project_name}")
    print(f"{'='*60}\n")

    return {
        "city": city,
        "project_type": project_type,
        "daily_visitors": daily_visitors,
        "project_name": project_name,
    }


def build_html(data: dict) -> str:
    """构建完整的HTML内容"""
    city = data["city"]
    ptype = data["project_type"]
    pname = data["project_name"]
    daily = data["daily_visitors"]
    ratios = CATCHMENT_RATIOS[ptype]
    pop = estimate_population(city)

    # 圈层值计算
    annual_visitors = daily * 365

    circles = []
    for i, (key, label, radius, ratio_key) in enumerate([
        ("1h", "1小时交通圈", 120, "1h"),
        ("2h", "2小时交通圈", 85, "2h"),
        ("3h", "3小时交通圈", 50, "3h"),
    ]):
        ratio = ratios[ratio_key]
        target_visitors = int(annual_visitors * ratio)
        pop_est = pop[ratio_key]
        circles.append({
            "key": key,
            "label": label,
            "radius": radius,
            "ratio": ratio,
            "target_visitors": target_visitors,
            "pop_est": pop_est,
            "desc": ratios.get(f"desc_{ratio_key}", ""),
            "color_outer": f"rgba(212, 175, 55, {0.15 + i * 0.10})",
            "color_inner": f"rgba(212, 175, 55, {0.35 - i * 0.08})",
            "stroke": f"rgba(212, 175, 55, {0.5 - i * 0.12})",
        })

    # 方案建议文字
    suggestions = []
    suggestions.append(f"📍 {city} · {ptype}项目 · 日均客流{daily:,}人次")
    suggestions.append("")
    suggestions.append("▎客源圈层策略建议")
    for c in circles:
        suggestions.append(f"  ● {c['label']}：覆盖目标 {c['ratio']*100:.0f}%（年约{c['target_visitors']:,}人次）")
        suggestions.append(f"    圈内人口估算 ≈ {c['pop_est']}万 · {c['desc']}")
    suggestions.append("")
    suggestions.append("▎营销重点")
    suggestions.append(f"  1h圈 → 重点营销 · 高频复购 · 社群运营")
    suggestions.append(f"  2h圈 → 精准投放 · 周末套餐 · KOL种草")
    suggestions.append(f"  3h圈 → 需强IP吸引 · 节庆活动 · 住宿套餐")
    if ptype == "康养型":
        suggestions.append("\n  💡 康养型项目：远距离客群占比最高，建议配套康养旅居产品")
    elif ptype == "观光型":
        suggestions.append("\n  💡 观光型项目：1h圈为核心，建议强化重游率与口碑传播")
    elif ptype == "度假型":
        suggestions.append("\n  💡 度假型项目：2-3h圈为重点，住宿+体验产品需充足")
    elif ptype == "复合型":
        suggestions.append("\n  💡 复合型项目：均衡覆盖，各圈层需差异化产品策略")

    suggestion_text = "\n".join(suggestions)

    # 构建SVG圈层
    svg_circles = ""
    svg_labels = ""
    svg_center_x = 250
    svg_center_y = 250

    for i, c in enumerate(circles):
        r = c["radius"]
        # 外圈描边
        svg_circles += f"""
    <circle cx="{svg_center_x}" cy="{svg_center_y}" r="{r}"
            fill="none" stroke="{c['stroke']}" stroke-width="2"
            opacity="0.8"/>"""
        # 径向渐变填充
        svg_circles += f"""
    <defs>
      <radialGradient id="grad_{c['key']}" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="{c['color_inner']}"/>
        <stop offset="100%" stop-color="{c['color_outer']}"/>
      </radialGradient>
    </defs>
    <circle cx="{svg_center_x}" cy="{svg_center_y}" r="{r}"
            fill="url(#grad_{c['key']})" opacity="0.6"/>"""

        # 标注文字位置
        angle = -60 + i * 35
        import math
        rad = math.radians(angle)
        lx = svg_center_x + r * 0.65 * math.cos(rad)
        ly = svg_center_y + r * 0.65 * math.sin(rad)

        svg_labels += f"""
    <text x="{lx}" y="{ly - 12}" text-anchor="middle" fill="#D4AF37" font-size="14" font-weight="bold">{c['label']}</text>
    <text x="{lx}" y="{ly + 6}" text-anchor="middle" fill="#A0A0A0" font-size="11">占比 {c['ratio']*100:.0f}%</text>
    <text x="{lx}" y="{ly + 22}" text-anchor="middle" fill="#B0B0B0" font-size="10">年{c['target_visitors']:,}人次</text>"""

    # 中心标注
    svg_labels += f"""
    <text x="{svg_center_x}" y="{svg_center_y - 8}" text-anchor="middle" fill="#F0E6D3" font-size="13" font-weight="bold">{city}</text>
    <text x="{svg_center_x}" y="{svg_center_y + 12}" text-anchor="middle" fill="#D4AF37" font-size="11">{ptype}</text>"""

    # 图例
    legend_items = ""
    for c in circles:
        legend_items += f"""
    <div class="legend-item">
      <span class="legend-dot" style="background:{c['stroke'].replace('0.5','0.8').replace('0.38','0.8').replace('0.26','0.8')};"></span>
      <span>{c['label']} &mdash; {c['ratio']*100:.0f}%覆盖 · 圈内约{c['pop_est']}万人</span>
    </div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{pname} · 客源圈层热力图 {VERSION}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
    background: #0D1B0E;
    color: #E8E0D4;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .container {{
    max-width: 1000px;
    width: 100%;
    padding: 30px 20px;
  }}
  .header {{
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(212, 175, 55, 0.3);
  }}
  .header h1 {{
    font-size: 26px;
    color: #D4AF37;
    letter-spacing: 4px;
    margin-bottom: 6px;
  }}
  .header .subtitle {{
    font-size: 14px;
    color: #8A9B6E;
  }}
  .header .version {{
    display: inline-block;
    margin-top: 8px;
    padding: 2px 12px;
    border: 1px solid #D4AF37;
    border-radius: 12px;
    font-size: 11px;
    color: #D4AF37;
  }}
  .main-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
  }}
  @media (max-width: 720px) {{
    .main-grid {{
      grid-template-columns: 1fr;
    }}
  }}
  .map-card {{
    background: linear-gradient(145deg, #0F2410, #162818);
    border: 1px solid rgba(212, 175, 55, 0.25);
    border-radius: 16px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .map-card svg {{
    max-width: 100%;
    height: auto;
  }}
  .info-panel {{
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .info-card {{
    background: linear-gradient(145deg, #0F2410, #162818);
    border: 1px solid rgba(212, 175, 55, 0.25);
    border-radius: 12px;
    padding: 18px;
  }}
  .info-card h3 {{
    font-size: 14px;
    color: #D4AF37;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(212, 175, 55, 0.2);
    letter-spacing: 2px;
  }}
  .stat-row {{
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    font-size: 13px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
  }}
  .stat-row:last-child {{ border: none; }}
  .stat-label {{ color: #A0A0A0; }}
  .stat-value {{ color: #F0E6D3; font-weight: bold; }}
  .stat-value.gold {{ color: #D4AF37; }}
  .legend {{ margin-top: 12px; }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: #B0B0B0;
    padding: 4px 0;
  }}
  .legend-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
  }}
  .suggestions {{
    background: linear-gradient(145deg, #0F2410, #162818);
    border: 1px solid rgba(212, 175, 55, 0.25);
    border-radius: 12px;
    padding: 18px;
    margin-top: 30px;
    white-space: pre-wrap;
    font-size: 13px;
    line-height: 1.7;
    color: #C8C0B4;
  }}
  .suggestions strong {{ color: #D4AF37; }}
  .footer {{
    text-align: center;
    margin-top: 30px;
    padding-top: 16px;
    border-top: 1px solid rgba(212, 175, 55, 0.15);
    font-size: 11px;
    color: #5A6B4E;
  }}
  .tag {{
    display: inline-block;
    background: rgba(212, 175, 55, 0.12);
    color: #D4AF37;
    padding: 2px 10px;
    border-radius: 10px;
    font-size: 11px;
    margin-right: 4px;
  }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🏔️ 客源圈层热力图</h1>
    <div class="subtitle">{pname} · 基于行业经验估算 · 仅供参考</div>
    <span class="version">{VERSION}</span>
  </div>

  <div class="main-grid">
    <div class="map-card">
      <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
        {svg_circles}
        {svg_labels}
      </svg>
      <div class="legend">
        {legend_items}
      </div>
    </div>

    <div class="info-panel">
      <div class="info-card">
        <h3>📋 项目概要</h3>
        <div class="stat-row"><span class="stat-label">城市</span><span class="stat-value">{city}</span></div>
        <div class="stat-row"><span class="stat-label">项目类型</span><span class="stat-value gold">{ptype}</span></div>
        <div class="stat-row"><span class="stat-label">日均客流</span><span class="stat-value">{daily:,} 人次</span></div>
        <div class="stat-row"><span class="stat-label">年客流估算</span><span class="stat-value">{annual_visitors:,} 人次</span></div>
      </div>

      <div class="info-card">
        <h3>🎯 圈层覆盖目标</h3>
"""
    for c in circles:
        html += f"""        <div class="stat-row">
          <span class="stat-label"><span class="tag">{c['label'][:2]}</span>{c['label']}</span>
          <span class="stat-value gold">{c['ratio']*100:.0f}%</span>
        </div>
        <div class="stat-row" style="font-size:12px; color:#808080; padding-left:32px;">
          年约{c['target_visitors']:,}人次 · 圈内人口≈{c['pop_est']}万
        </div>
"""

    html += """      </div>

      <div class="info-card">
        <h3>📊 圈层人口估算</h3>
"""
    for c in circles:
        html += f"""        <div class="stat-row">
          <span class="stat-label">{c['label']}</span>
          <span class="stat-value">≈{c['pop_est']}万人</span>
        </div>
"""
    html += """        <div style="margin-top:8px; font-size:11px; color:#6A7B5E;">* 基于城市等级与行业经验估算</div>
      </div>
    </div>
  </div>

  <div class="suggestions">""" + suggestion_text + """</div>

  <div class="footer">
    生成工具 V2.1 · 文旅策划规划助手 · 数据为行业经验估算值，请结合当地实际调研
  </div>
</div>
</body>
</html>"""

    return html


def save_html(html: str, project_name: str) -> str:
    """保存HTML文件到项目目录"""
    project_dir = Path("F:/owen/hermes/projects")
    project_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{project_name}_热力图.html"
    filepath = project_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    return str(filepath)


def main():
    print(f"🏔️  客源圈层热力图生成工具  {VERSION}")
    print("=" * 60)

    data = get_user_input()
    html = build_html(data)
    filepath = save_html(html, data["project_name"])

    print(f"\n✅ 热力图已生成！")
    print(f"📄 文件路径：{filepath}")
    print(f"💡 可用浏览器直接打开查看\n")

    try:
        webbrowser.open(f"file:///{filepath}")
        print("🌐 已自动打开浏览器...")
    except Exception:
        pass

    print("=" * 60)
    print(f"提示：若自动打开失败，请手动用浏览器打开上述文件。")

    return filepath


if __name__ == "__main__":
    main()
