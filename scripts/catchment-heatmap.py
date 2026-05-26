#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客源圈层热力图生成工具 V2.6（增强版）
Catchment Area Heatmap Generator — Enhanced Edition
=====================================================

适用场景：文旅策划 / 景区规划 / 可行性研究
功能说明：
  1. 交互输入：项目名、城市经纬度（或从内置城市数据库选择）、项目类型、日均客流
  2. 自动生成独立 HTML —— 集成 Leaflet.js + OpenStreetMap，在真实地图上绘制3个同心圈
  3. 三个同心圆代表 1h/2h/3h 交通圈，标注客源覆盖目标与人口估算
  4. 集成GIS风格：深色地图底图 + 金色渐变圈层 + 数据仪表板
  5. 纯HTML/JS，无需安装任何库（Leaflet通过CDN加载）

依赖：Python 3.7+ (标准库)
运行：python scripts/catchment-heatmap.py [--demo]
输出：F:/owen/hermes/projects/{项目名}_热力图_v2.6.html
"""

import os
import webbrowser
from pathlib import Path
from datetime import datetime

VERSION = "V2.6"

# ── HTML 模板（使用 %s 占位符，避免 f-string 花括号冲突） ─────
HTML_HEADER = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>%s·客源圈层热力图 %s</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0a0e17;color:#e0e0e0;font-family:'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;}
.container{max-width:1200px;margin:0 auto;padding:20px;}
.header{text-align:center;padding:20px 0 15px;border-bottom:1px solid rgba(255,215,0,0.2);margin-bottom:20px;}
.header h1{font-size:24px;color:#ffd700;letter-spacing:3px;}
.header .sub{color:#888;font-size:13px;margin-top:3px;}
.main-grid{display:grid;grid-template-columns:1.4fr 1fr;gap:20px;}
@media(max-width:800px){.main-grid{grid-template-columns:1fr;}}
#map{height:550px;border-radius:12px;border:1px solid rgba(255,215,0,0.15);}
.info-panel{display:flex;flex-direction:column;gap:12px;}
.info-card{background:#121826;border-radius:10px;padding:15px;border:1px solid #1e2438;}
.info-card h3{font-size:13px;color:#ffd700;margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid rgba(255,215,0,0.12);}
.stat-row{display:flex;justify-content:space-between;padding:5px 0;font-size:13px;border-bottom:1px solid rgba(255,255,255,0.03);}
.stat-row:last-child{border:none;}
.stat-label{color:#888;}
.stat-value{color:#e0e0e0;font-weight:bold;}
.stat-value.gold{color:#ffd700;}
.circle-legend{margin-top:8px;}
.legend-item{display:flex;align-items:center;gap:8px;font-size:12px;color:#aaa;padding:3px 0;}
.legend-dot{width:10px;height:10px;border-radius:50%%;display:inline-block;flex-shrink:0;}
.suggestions{background:#121826;border:1px solid #1e2438;border-radius:10px;padding:15px;margin-top:20px;font-size:13px;line-height:1.7;color:#aaa;white-space:pre-wrap;}
.suggestions strong{color:#ffd700;}
.footer{text-align:center;margin-top:20px;padding:12px 0;border-top:1px solid #1e2438;color:#444;font-size:11px;}
.tag{display:inline-block;background:rgba(255,215,0,0.1);color:#ffd700;padding:1px 8px;border-radius:8px;font-size:10px;margin-right:2px;}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🏔️ 客源圈层热力图</h1>
    <div class="sub">%s · %s · %s · %s · 数据为经验估算值</div>
  </div>

  <div class="main-grid">
    <div>
      <div id="map"></div>
      <div class="circle-legend" style="display:flex;gap:20px;justify-content:center;margin-top:10px;">
        <div class="legend-item"><span class="legend-dot" style="background:rgba(255,215,0,0.3);border:2px solid rgba(255,215,0,0.7);"></span> 1h圈 (%skm, %.0f%%)</div>
        <div class="legend-item"><span class="legend-dot" style="background:rgba(255,165,0,0.2);border:2px solid rgba(255,165,0,0.6);"></span> 2h圈 (%skm, %.0f%%)</div>
        <div class="legend-item"><span class="legend-dot" style="background:rgba(255,100,50,0.15);border:2px solid rgba(255,100,50,0.5);"></span> 3h圈 (%skm, %.0f%%)</div>
      </div>
    </div>

    <div class="info-panel">
      <div class="info-card">
        <h3>📋 项目概要</h3>
        <div class="stat-row"><span class="stat-label">项目名称</span><span class="stat-value">%s</span></div>
        <div class="stat-row"><span class="stat-label">城市</span><span class="stat-value">%s</span></div>
        <div class="stat-row"><span class="stat-label">项目类型</span><span class="stat-value gold">%s</span></div>
        <div class="stat-row"><span class="stat-label">坐标</span><span class="stat-value">%.3f°, %.3f°</span></div>
        <div class="stat-row"><span class="stat-label">日均客流</span><span class="stat-value">%s 人次</span></div>
        <div class="stat-row"><span class="stat-label">年客流估算</span><span class="stat-value">%s 人次</span></div>
      </div>

      <div class="info-card">
        <h3>🎯 圈层覆盖目标</h3>
        %s
      </div>

      <div class="info-card">
        <h3>📊 圈层人口估算</h3>
        %s
        <div style="margin-top:6px;font-size:11px;color:#555;">* 基于城市等级与行业经验估算</div>
      </div>
    </div>
  </div>

  <div class="suggestions">%s</div>

  <div class="footer">
    生成工具 %s · 文旅策划规划助手 · 底图 &copy; OpenStreetMap 贡献者 · 数据为行业经验估算值
  </div>
</div>

<script>
(function(){
var map = L.map('map', {
  center: [%s, %s],
  zoom: 9,
  zoomControl: true
});

// 深色底图 (CartoDB Dark Matter)
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
  subdomains: 'abcd',
  maxZoom: 19
}).addTo(map);

// 中心标记
var marker = L.circleMarker([%s, %s], {
  radius: 8,
  fillColor: '#ffd700',
  color: '#fff',
  weight: 2,
  opacity: 1,
  fillOpacity: 0.8
}).addTo(map);
marker.bindTooltip("<b>%s</b><br>%s", {direction:'top',offset:[0,-10]});

// 三个同心圈
var circles = [
  {radius:%s*1000, color:'rgba(255,215,0,0.7)', fill:'rgba(255,215,0,0.04)', label:'1h · %skm · %.0f%%'},
  {radius:%s*1000, color:'rgba(255,165,0,0.6)', fill:'rgba(255,165,0,0.02)', label:'2h · %skm · %.0f%%'},
  {radius:%s*1000, color:'rgba(255,100,50,0.5)', fill:'rgba(255,100,50,0.01)', label:'3h · %skm · %.0f%%'}
];

circles.forEach(function(c, i){
  var circle = L.circle([%s, %s], {
    radius: c.radius,
    color: c.color,
    fillColor: c.fill,
    fillOpacity: 0.6,
    weight: 2.5,
    opacity: 0.8,
    dashArray: '8,6',
    dashOffset: i * 4
  }).addTo(map);
  circle.bindTooltip(c.label, {direction:'center',className:'circle-label'});
});

// 自适应视图
var maxR = Math.max(%s, %s, %s) * 1000;
var bounds = L.latLng([%s, %s]).toBounds(maxR);
map.fitBounds(bounds, {padding:[30,30]});

})();
</script>
%s
</body>
</html>"""

# ── 内置中国城市坐标数据库（经纬度 + 人口等级） ────────────────────
CITIES = {
    # 一线城市
    "北京": {"lat": 39.9042, "lng": 116.4074, "tier": 1, "pop_desc": "超大城市(2,100万+)"},
    "上海": {"lat": 31.2304, "lng": 121.4737, "tier": 1, "pop_desc": "超大城市(2,400万+)"},
    "广州": {"lat": 23.1291, "lng": 113.2644, "tier": 1, "pop_desc": "超大城市(1,800万+)"},
    "深圳": {"lat": 22.5431, "lng": 114.0579, "tier": 1, "pop_desc": "超大城市(1,700万+)"},
    # 新一线
    "成都": {"lat": 30.5728, "lng": 104.0668, "tier": 2, "pop_desc": "特大城市(2,000万+)"},
    "杭州": {"lat": 30.2741, "lng": 120.1551, "tier": 2, "pop_desc": "特大城市(1,200万+)"},
    "重庆": {"lat": 29.4316, "lng": 106.9123, "tier": 2, "pop_desc": "超大城市(3,200万+)"},
    "武汉": {"lat": 30.5928, "lng": 114.3055, "tier": 2, "pop_desc": "特大城市(1,300��+)"},
    "南京": {"lat": 32.0603, "lng": 118.7969, "tier": 2, "pop_desc": "特大城市(900万+)"},
    "西安": {"lat": 34.3416, "lng": 108.9398, "tier": 2, "pop_desc": "特大城市(1,200万+)"},
    "长沙": {"lat": 28.2282, "lng": 112.9388, "tier": 2, "pop_desc": "特大城市(1,000万+)"},
    # 二线
    "昆明": {"lat": 25.0389, "lng": 102.7183, "tier": 3, "pop_desc": "大城市(800万+)"},
    "大理": {"lat": 25.6065, "lng": 100.2280, "tier": 3, "pop_desc": "中等城市(300万+)"},
    "丽江": {"lat": 26.8721, "lng": 100.2299, "tier": 3, "pop_desc": "中等城市(150万+)"},
    "桂林": {"lat": 25.2736, "lng": 110.2900, "tier": 3, "pop_desc": "中等城市(500万+)"},
    "三亚": {"lat": 18.2528, "lng": 109.5120, "tier": 3, "pop_desc": "中等城市(100万+)"},
    "厦门": {"lat": 24.4798, "lng": 118.0894, "tier": 2, "pop_desc": "特大城市(500万+)"},
    "青岛": {"lat": 36.0671, "lng": 120.3826, "tier": 2, "pop_desc": "特大城市(900万+)"},
    "贵阳": {"lat": 26.6470, "lng": 106.6302, "tier": 3, "pop_desc": "大城市(600万+)"},
    "拉萨": {"lat": 29.6500, "lng": 91.1000, "tier": 3, "pop_desc": "中等城市(90万+)"},
    "哈尔滨": {"lat": 45.8022, "lng": 126.5350, "tier": 2, "pop_desc": "特大城市(900万+)"},
    "乌鲁木齐": {"lat": 43.8256, "lng": 87.6168, "tier": 3, "pop_desc": "大城市(400万+)"},
    "呼和浩特": {"lat": 40.8422, "lng": 111.7499, "tier": 3, "pop_desc": "大城市(300万+)"},
    "敦煌": {"lat": 40.1419, "lng": 94.6619, "tier": 3, "pop_desc": "小城市(20万+)"},
    "九寨沟": {"lat": 33.2621, "lng": 104.2363, "tier": 3, "pop_desc": "景区镇(5万+)"},
}

# ── 项目类型客源覆盖配比 ──────────────────────────────────────
CATCHMENT_RATIOS = {
    "观光型": {"1h": 0.60, "2h": 0.30, "3h": 0.10,
              "radius_km": (50, 150, 300),
              "desc_1h": "高频短途，自然流量为主",
              "desc_2h": "周末出行主力，需要一定吸引力",
              "desc_3h": "偶发出行，需强IP或节庆驱动"},
    "度假型": {"1h": 0.30, "2h": 0.40, "3h": 0.30,
              "radius_km": (30, 120, 250),
              "desc_1h": "日常近距离度假，复购率高",
              "desc_2h": "周末度假主力，住宿+体验消费",
              "desc_3h": "长假/商务出行，高客单价"},
    "综合型": {"1h": 0.45, "2h": 0.35, "3h": 0.20,
              "radius_km": (50, 150, 300),
              "desc_1h": "周边游客+日常休闲",
              "desc_2h": "中距离周末游主力",
              "desc_3h": "远距离吸引+特色活动驱动"},
    "专项型": {"1h": 0.20, "2h": 0.35, "3h": 0.45,
              "radius_km": (30, 100, 200),
              "desc_1h": "本地亲子/研学日常",
              "desc_2h": "区域范围内吸引",
              "desc_3h": "全国目的地型吸引"},
}

# ── 城市圈层人口估算（按城市等级 + 半径） ────────────────────
def estimate_population(tier: int, radius_km: int) -> int:
    """粗糙估算：不同城市等级在对应半径可覆盖人口(万)"""
    density_map = {
        1: {50: 500, 150: 1500, 300: 3000},   # 一线
        2: {50: 300, 150: 1000, 300: 2500},    # 新一线/二线
        3: {50: 100, 150: 500, 300: 1200},     # 三四线
    }
    return density_map.get(tier, density_map[3]).get(radius_km, 500)


def get_user_input():
    """交互输入参数"""
    print(f"\n{'=' * 55}")
    print(f"  🏔️  客源圈层热力图 V{VERSION} 增强版（真实地图）")
    print(f"{'=' * 55}\n")

    data = {}

    data["project_name"] = input("  🏗️  项目名称: ").strip() or "未命名项目"

    print("\n  🌆 选择城市 (输入数字) 或 输入 'c' 自定义坐标:")
    city_names = sorted(CITIES.keys())
    for i, name in enumerate(city_names, 1):
        c = CITIES[name]
        print(f"    {i:2d}. {name} ({c['lat']:.1f}°, {c['lng']:.1f}°) — {c['pop_desc']}")
    print(f"    c. 自定义坐标")

    choice = input("\n  ⏩ 请选择: ").strip()
    if choice.lower() == "c":
        data["city"] = input("    城市名: ").strip() or "自定义"
        data["lat"] = float(input("    纬度 (如 30.57): ").strip() or "30.57")
        data["lng"] = float(input("    经度 (如 104.07): ").strip() or "104.07")
        data["tier"] = 2
    elif choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(city_names):
            name = city_names[idx]
            data["city"] = name
            data["lat"] = CITIES[name]["lat"]
            data["lng"] = CITIES[name]["lng"]
            data["tier"] = CITIES[name]["tier"]
        else:
            data["city"] = "成都"
            data["lat"], data["lng"], data["tier"] = 30.5728, 104.0668, 2
    else:
        data["city"] = "成都"
        data["lat"], data["lng"], data["tier"] = 30.5728, 104.0668, 2

    print(f"\n  📋 项目类型:")
    ptypes = list(CATCHMENT_RATIOS.keys())
    for i, pt in enumerate(ptypes, 1):
        print(f"    {i}. {pt}")
    p_choice = input("  ⏩ 请选择 (1-4, 默认3): ").strip()
    if p_choice.isdigit() and 1 <= int(p_choice) <= len(ptypes):
        data["project_type"] = ptypes[int(p_choice) - 1]
    else:
        data["project_type"] = "综合型"

    daily_str = input(f"\n  👥 预期日均客流 (默认1500): ").strip()
    data["daily_visitors"] = int(daily_str) if daily_str.isdigit() and int(daily_str) > 0 else 1500

    return data


def generate_map_html(data):
    """生成真实地图HTML"""
    pname = data["project_name"]
    city = data["city"]
    lat, lng = data["lat"], data["lng"]
    tier = data["tier"]
    ptype = data["project_type"]
    daily = data["daily_visitors"]

    ratio = CATCHMENT_RATIOS[ptype]
    r1, r2, r3 = ratio["radius_km"]
    annual = daily * 365

    circles_info = [
        {"label": "1h 交通圈", "radius_km": r1, "ratio": ratio["1h"], "desc": ratio["desc_1h"]},
        {"label": "2h 交通圈", "radius_km": r2, "ratio": ratio["2h"], "desc": ratio["desc_2h"]},
        {"label": "3h 交通圈", "radius_km": r3, "ratio": ratio["3h"], "desc": ratio["desc_3h"]},
    ]
    for c in circles_info:
        c["target_visitors"] = int(daily * 365 * c["ratio"])
        c["pop_est"] = estimate_population(tier, c["radius_km"])

    suggestion_parts = []
    suggestion_parts.append(f"💡 **运营��议**")
    suggestion_parts.append(f"")
    suggestion_parts.append(f"• 【1h圈】{ratio['1h']*100:.0f}%客源来自{r1}km内 —— {ratio['desc_1h']}")
    suggestion_parts.append(f"• 【2h圈】{ratio['2h']*100:.0f}%客源来自{r2}km内 —— {ratio['desc_2h']}")
    suggestion_parts.append(f"• 【3h圈】{ratio['3h']*100:.0f}%客源来自{r3}km内 —— {ratio['desc_3h']}")
    suggestion_parts.append(f"")
    suggestion_parts.append(f"📊 **基于{ptype}项目的推荐策略：**")
    suggestion_parts.append(f"• 线上投放聚焦1h圈高频触达，2h圈OTA+社交媒体组合投放")
    suggestion_parts.append(f"• 与3h圈内旅行社/OTA建立合作，通过特色活动+住宿套餐引客")
    suggestion_parts.append(f"• 淡季优先深耕1h圈本地市场，旺季辐射3h圈远程市场")
    suggestion_parts.append(f"• 预期日均客流{daily:,}人次，年客流量约{annual:,}人次")
    suggestion_text = "\n".join(suggestion_parts)

    # 圈层覆盖行（避免嵌套f-string的:,格式问题）
    circle_cover_rows = []
    for c in circles_info:
        tv = c["target_visitors"]
        pe = c["pop_est"]
        lbl = c["label"]
        rto = c["ratio"]*100
        desc = c["desc"]
        circle_cover_rows.append(
            f'''<div class="stat-row"><span class="stat-label"><span class="tag">{lbl[:2]}</span>{lbl}</span><span class="stat-value gold">{rto:.0f}%</span></div><div class="stat-row" style="font-size:12px;color:#666;padding-left:28px;">年约{tv:,}人次 · 圈内人口≈{pe}万 · {desc}</div>'''
        )
    circle_pop_rows = []
    for c in circles_info:
        lbl = c["label"]
        pe = c["pop_est"]
        circle_pop_rows.append(
            f'''<div class="stat-row"><span class="stat-label"><span class="tag">{lbl[:2]}</span>{lbl}</span><span class="stat-value gold">≈{pe}万人</span></div>'''
        )

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    circle_label_css = ("<style>\n.circle-label{background:rgba(10,14,23,0.85);"
                        "color:#ffd700;border:1px solid rgba(255,215,0,0.2);"
                        "font-size:12px;padding:4px 10px;border-radius:6px;box-shadow:none;}\n</style>")

    return (HTML_HEADER % (
        pname, VERSION,                              # 1-2: title
        pname, city, ptype, VERSION,                 # 3-6: subtitle
        r1, ratio["1h"]*100,                        # 7-8: 1h圈
        r2, ratio["2h"]*100,                        # 9-10: 2h圈
        r3, ratio["3h"]*100,                        # 11-12: 3h圈
        pname, city, ptype,                         # 13-15: 项目概要前三
        lat, lng,                                    # 16-17: 坐标
        f"{daily:,}", f"{annual:,}",                 # 18-19: 客流(带逗号)
        "".join(circle_cover_rows),                  # 20: 圈层覆盖
        "".join(circle_pop_rows),                    # 21: 圈层人口
        suggestion_text, VERSION,                    # 22-23: 建议+footer版本
        lat, lng,                                    # 24-25: map center
        lat, lng,                                    # 26-27: marker
        pname, city,                                 # 28-29: tooltip
        r1*1000, r1, ratio["1h"]*100,               # 30-32: circle 1
        r2*1000, r2, ratio["2h"]*100,               # 33-35: circle 2
        r3*1000, r3, ratio["3h"]*100,               # 36-38: circle 3
        lat, lng,                                    # 39-40: forEach
        r1, r2, r3,                                  # 41-43: maxR
        lat, lng,                                    # 44-45: bounds
        circle_label_css                             # 46: style
    ))


def save_html(html: str, project_name: str) -> str:
    project_dir = Path("F:/owen/hermes/projects")
    project_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{project_name}_热力图_v2.6.html"
    filepath = project_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    return str(filepath)


def main():
    import sys

    # --demo 模式
    if "--demo" in sys.argv:
        data = {
            "project_name": "龙隐山谷康养度假区",
            "city": "成都",
            "lat": 30.5728, "lng": 104.0668,
            "tier": 2,
            "project_type": "度假型",
            "daily_visitors": 2000,
        }
    else:
        data = get_user_input()

    html = generate_map_html(data)
    filepath = save_html(html, data["project_name"])

    print(f"\n{'=' * 55}")
    print(f"  ✅ 热力图（增强版）已生成！")
    print(f"  📄 文件：{filepath}")
    print(f"  📏 大小：{os.path.getsize(filepath):,} 字节")
    print(f"  🌐 需要联网加载底图（首次）")
    print(f"{'=' * 55}\n")

    try:
        webbrowser.open(f"file:///{filepath}")
        print("  🌐 已自动打开浏览器...")
    except Exception:
        pass

    return filepath


if __name__ == "__main__":
    main()
