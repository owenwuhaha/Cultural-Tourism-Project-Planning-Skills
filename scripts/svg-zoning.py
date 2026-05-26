#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG功能分区图生成器 V2.2
SVG Zoning Map Generator — Cultural Tourism Project
=====================================================

功能说明：
  交互输入项目参数，自动生成功能分区饼图HTML文件。
  包含：彩色饼图（5大分区）、图例、面积/占比/设施描述、承载力估算

用法：
  python svg-zoning.py

依赖：Python 3.7+ (标准库, 无第三方依赖)
输出：F:/owen/hermes/projects/{项目名}_功能分区图.html
"""

import math
import os
import webbrowser
from datetime import datetime

VERSION = "2.2"
OUTPUT_DIR = os.path.expandvars(r"F:\owen\hermes\projects")

# 分区颜色配置
ZONE_COLORS = {
    "入口服务区": {"color": "#4a90d9", "desc": "接待、停车、票务"},
    "核心吸引区": {"color": "#e74c3c", "desc": "主题���场、演艺、地标打卡"},
    "休闲消费区": {"color": "#2ecc71", "desc": "餐饮、文创、体验"},
    "住宿配套区": {"color": "#f39c12", "desc": "民宿、露营、酒店"},
    "生态保育区": {"color": "#9b59b6", "desc": "游览步道、观景平台"},
}

ZONE_ORDER = ["入口服务区", "核心吸引区", "休闲消费区", "住宿配套区", "生态保育区"]

DEFAULT_RATIOS = [5, 20, 30, 25, 20]

TERRAIN_TYPES = ["山地坡地", "平坡地", "滨水滩涂", "阶梯台地", "混合地形"]

def input_float(prompt: str, default: float) -> float:
    while True:
        raw = input(prompt).strip()
        if not raw:
            return default
        try:
            return float(raw)
        except ValueError:
            print("❌ 请输入有效数字")

def input_str(prompt: str, default: str = "") -> str:
    val = input(prompt).strip()
    return val if val else default

def select_option(prompt: str, options: list, default_idx: int = 0) -> str:
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        marker = " [默认]" if i == default_idx + 1 else ""
        print(f"  {i}. {opt}{marker}")
    while True:
        raw = input("请选择编号: ").strip()
        if not raw:
            return options[default_idx]
        try:
            idx = int(raw)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        except ValueError:
            print("请输入数字")

def get_input() -> dict:
    print(f"\n{'=' * 55}")
    print(f"  🗺️ 功能分区图生成器 V{VERSION}")
    print(f"{'=' * 55}\n")

    info = {
        "project_name": input_str("📛 项目名称: ", "示例项目"),
        "terrain": select_option("🏔 地形类型:", TERRAIN_TYPES),
        "area_mu": input_float("📐 规划总面积（亩）: ", 200),
    }

    print(f"\n📊 请输入各分区占比（总和应为100%）：\n{'-' * 40}")
    ratios = {}
    total = 0
    for i, zone in enumerate(ZONE_ORDER):
        default = DEFAULT_RATIOS[i]
        remaining = 100 - total
        if i == len(ZONE_ORDER) - 1:
            r = input_float(f"  {zone}（{ZONE_COLORS[zone]['color']}）[{remaining}%]: ", remaining)
        else:
            max_r = min(remaining, default + 15)
            r = input_float(f"  {zone}（{ZONE_COLORS[zone]['color']}）[{default}%]: ", default)
            r = min(r, remaining)
        ratios[zone] = r
        total += r

    # 归一化到100%
    if total != 100:
        factor = 100 / total
        for k in ratios:
            ratios[k] = round(ratios[k] * factor, 1)
        # 修正四舍五入误差
        diff = 100 - sum(ratios.values())
        ratios[ZONE_ORDER[-1]] = round(ratios[ZONE_ORDER[-1]] + diff, 1)

    info["ratios"] = ratios
    info["daily_visitors"] = input_float("\n👥 预期日均客流（人）[2000]: ", 2000)
    return info


def generate_svg(info: dict) -> str:
    """生成SVG饼图"""
    cx, cy, r = 250, 250, 180
    total = sum(info["ratios"].values())
    start_angle = -90  # 从12点方向开始

    paths = []
    labels = []

    for zone in ZONE_ORDER:
        ratio = info["ratios"][zone]
        angle = 360 * ratio / total
        end_angle = start_angle + angle

        # 计算弧路径
        s_rad = math.radians(start_angle)
        e_rad = math.radians(end_angle)

        x1 = cx + r * math.cos(s_rad)
        y1 = cy + r * math.sin(s_rad)
        x2 = cx + r * math.cos(e_rad)
        y2 = cy + r * math.sin(e_rad)

        large_arc = 1 if angle > 180 else 0
        color = ZONE_COLORS[zone]["color"]

        path = f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r},{r} 0 {large_arc},1 {x2:.1f},{y2:.1f} Z" fill="{color}" stroke="#1a1a2e" stroke-width="2"/>'
        paths.append(path)

        # 标签位置（扇形中点）
        mid_angle = math.radians(start_angle + angle / 2)
        label_r = r * 0.65
        lx = cx + label_r * math.cos(mid_angle)
        ly = cy + label_r * math.sin(mid_angle)

        labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="central" fill="#fff" font-size="13" font-weight="bold">{zone[:4]}<tspan x="{lx:.1f}" dy="18">{ratio:.0f}%</tspan></text>')

        start_angle = end_angle

    # 图例
    legend_items = []
    legend_y = 20
    for zone in ZONE_ORDER:
        color = ZONE_COLORS[zone]["color"]
        ratio = info["ratios"][zone]
        desc = ZONE_COLORS[zone]["desc"]
        legend_items.append(
            f'<g transform="translate(520, {legend_y})">'
            f'<rect x="0" y="0" width="16" height="16" rx="3" fill="{color}"/>'
            f'<text x="22" y="13" fill="#e0e0e0" font-size="13" font-weight="bold">{zone}</text>'
            f'<text x="130" y="13" fill="#888" font-size="12">{ratio:.0f}% · {desc}</text>'
            f'</g>'
        )
        legend_y += 28

    # 承载力信息
    dd = int(info["daily_visitors"])
    capacity = dd * 2
    parking = max(50, int(dd * 0.05 / 2))
    area_mu = info["area_mu"]
    area_sqm = area_mu * 666.67

    return f'''
<svg width="800" height="600" viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg" style="background:transparent;font-family:'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;">
  <!-- 标题 -->
  <text x="400" y="30" text-anchor="middle" fill="#e0e0e0" font-size="22" font-weight="bold">{info["project_name"]} · 功能分区图</text>
  <text x="400" y="50" text-anchor="middle" fill="#666" font-size="13">{info["terrain"]} · {area_mu:.0f}亩（{area_sqm:.0f}㎡）</text>

  <!-- 饼图 -->
  <g transform="translate(0, 20)">
    {"".join(paths)}
    {"".join(labels)}
  </g>

  <!-- 中心圆 -->
  <circle cx="250" cy="270" r="55" fill="#1a1a2e" stroke="#2d2d44" stroke-width="2"/>
  <text x="250" y="260" text-anchor="middle" fill="#e0e0e0" font-size="16" font-weight="bold">总面积</text>
  <text x="250" y="280" text-anchor="middle" fill="#f39c12" font-size="18" font-weight="bold">{area_mu:.0f}亩</text>

  <!-- 图例 -->
  <g transform="translate(30, 470)">
    <rect x="0" y="0" width="740" height="110" rx="8" fill="#1e1e36" stroke="#2d2d44" stroke-width="1"/>
    <text x="20" y="25" fill="#888" font-size="12">图例说明</text>
    {chr(10).join([f'<rect x="{20 + i*150}" y="35" width="12" height="12" rx="2" fill="{ZONE_COLORS[z]["color"]}"/><text x="{36 + i*150}" y="46" fill="#ccc" font-size="11">{z}</text>' for i, z in enumerate(ZONE_ORDER)])}
  </g>

  <!-- 承载力 -->
  <g transform="translate(520, 160)">
    <rect x="0" y="0" width="250" height="120" rx="8" fill="#1e1e36" stroke="#2d2d44" stroke-width="1"/>
    <text x="15" y="22" fill="#e0e0e0" font-size="14" font-weight="bold">承载力估算</text>
    <text x="15" y="45" fill="#aaa" font-size="12">瞬时最大承载量</text>
    <text x="200" y="45" text-anchor="end" fill="#4a90d9" font-size="13" font-weight="bold">{dd:,}人</text>
    <text x="15" y="68" fill="#aaa" font-size="12">日合理承载量</text>
    <text x="200" y="68" text-anchor="end" fill="#2ecc71" font-size="13" font-weight="bold">{capacity:,}人</text>
    <text x="15" y="91" fill="#aaa" font-size="12">建议停车位</text>
    <text x="200" y="91" text-anchor="end" fill="#f39c12" font-size="13" font-weight="bold">{parking}个</text>
  </g>

  <!-- 版本 -->
  <text x="755" y="585" text-anchor="end" fill="#444" font-size="11">V{VERSION}</text>
</svg>'''


def generate_html(info: dict, svg_content: str) -> str:
    """生成完整HTML"""
    zones_html = []
    for zone in ZONE_ORDER:
        ratio = info["ratios"][zone]
        color = ZONE_COLORS[zone]["color"]
        desc = ZONE_COLORS[zone]["desc"]
        area_mu = info["area_mu"] * ratio / 100
        zones_html.append(f'''
        <div class="zone-card" style="border-left: 4px solid {color};">
          <div class="zone-header">
            <span class="zone-dot" style="background:{color};"></span>
            <span class="zone-name">{zone}</span>
            <span class="zone-ratio">{ratio:.0f}%</span>
          </div>
          <div class="zone-body">
            <span class="zone-area">{area_mu:.1f}亩</span>
            <span class="zone-desc">{desc}</span>
          </div>
        </div>''')

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{info["project_name"]} · 功能分区图 V{VERSION}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  background:#0f0f23; color:#e0e0e0;
  font-family:'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
  min-height:100vh;
}}
.container {{ max-width:1100px; margin:0 auto; padding:20px; }}
.header {{
  text-align:center; padding:30px 0 10px;
  border-bottom:1px solid #2d2d44; margin-bottom:30px;
}}
.header h1 {{ font-size:28px; color:#f0f0f0; }}
.header .sub {{ color:#666; font-size:14px; margin-top:5px; }}
.grid {{ display:flex; flex-wrap:wrap; gap:30px; }}
.svg-wrap {{
  flex:1; min-width:500px; background:#1a1a2e;
  border-radius:12px; padding:20px;
  border:1px solid #2d2d44;
}}
.svg-wrap svg {{ width:100%; height:auto; display:block; }}
.zones-wrap {{ flex:0 0 320px; }}
.section-title {{ font-size:16px; color:#888; margin-bottom:12px; }}
.zone-card {{
  background:#1a1a2e; border-radius:8px; padding:12px 15px;
  margin-bottom:8px; border:1px solid #2d2d44;
  transition:transform 0.15s;
}}
.zone-card:hover {{ transform:translateX(4px); }}
.zone-header {{ display:flex; align-items:center; gap:8px; }}
.zone-dot {{ width:10px; height:10px; border-radius:50%; display:inline-block; }}
.zone-name {{ font-weight:bold; font-size:14px; flex:1; }}
.zone-ratio {{ color:#f39c12; font-weight:bold; font-size:16px; }}
.zone-body {{ margin-top:6px; display:flex; gap:15px; font-size:13px; color:#888; }}
.zone-area {{ color:#aaa; }}
.zone-desc {{ color:#666; }}
.footer {{
  margin-top:30px; padding:15px 0; text-align:center;
  border-top:1px solid #2d2d44; color:#444; font-size:12px;
}}
@media (max-width:860px) {{
  .svg-wrap {{ min-width:auto; }}
  .grid {{ flex-direction:column; }}
  .zones-wrap {{ flex:auto; }}
}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🗺️ {info["project_name"]}</h1>
    <div class="sub">{info["terrain"]} · {info["area_mu"]:.0f}亩 · 预期日均客流{int(info["daily_visitors"]):,}人</div>
  </div>
  <div class="grid">
    <div class="svg-wrap">
      {svg_content}
    </div>
    <div class="zones-wrap">
      <div class="section-title">📋 分区详情</div>
      {"".join(zones_html)}
      <div class="section-title" style="margin-top:20px;">💡 建议</div>
      <div class="zone-card" style="border-left:4px solid #4a90d9;">
        <div style="font-size:13px;color:#aaa;line-height:1.6;">
          • 核心吸引区+休闲消费区占比 {info["ratios"]["核心吸引区"]+info["ratios"]["休闲消费区"]:.0f}%，是产生主要收入和体验的核心区域<br>
          • 生态保育区占比 {info["ratios"]["生态保育区"]:.0f}%，确保可持续发展<br>
          • 建议按「入口→核心吸引→休闲消费→住宿」动线布局
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    由文旅策划规划助手自动生成 · V{VERSION} · {datetime.now().strftime('%Y-%m-%d %H:%M')}<br>
    ⚠️ 所有数据为行业经验参考值，正式方案需结合当地实际情况
  </div>
</div>
</body>
</html>'''


def main():
    info = get_input()
    svg_content = generate_svg(info)
    html = generate_html(info, svg_content)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = os.path.join(OUTPUT_DIR, f"{info['project_name']}_功能分区图_v{VERSION}.html")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n{'=' * 55}")
    print(f"  ✅ SVG功能分区图已生成：")
    print(f"     {filename}")
    print(f"  📏 文件大小：{os.path.getsize(filename):,} 字节")
    print(f"{'=' * 55}")

    try:
        webbrowser.open(f"file://{os.path.abspath(filename)}")
        print("  🌐 已自动打开浏览器预览")
    except Exception:
        print("  请手动打开浏览器查看")


if __name__ == "__main__":
    main()
