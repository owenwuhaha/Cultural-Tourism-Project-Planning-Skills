#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文旅竞品对标分析工具 V2.3
Competitive Analysis Tool — Cultural Tourism
==============================================

功能说明：
  交互输入项目+竞品信息，生成多维对标分析HTML。
  包含：6维雷达图、竞争力矩阵散点图、综合排名表、SWOT分析、差异化建议

用法：
  python competitive-analysis.py

依赖：Python 3.7+ (标准库)
输出：F:/owen/hermes/projects/{项目名}_竞品对标分析.html
"""

import math
import os
import webbrowser
from datetime import datetime

VERSION = "2.3"
OUTPUT_DIR = os.path.expandvars(r"F:\owen\hermes\projects")

DIMENSIONS = ["资源禀赋", "交通可达性", "产品丰富度", "市场影响力", "投资实力", "运营能力"]

AUDIENCE_TYPES = [
    "亲子和家庭", "年轻潮流", "银发康养", "商务团体", "综合型"
]

COMPETITOR_TYPES = ["景区", "度假区", "小镇", "综合体"]


def input_float(prompt, default=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            return float(raw)
        except ValueError:
            print("❌ 请输入有效数字")


def input_int(prompt, default=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("❌ 请输入有效整数")


def input_str(prompt, default=""):
    val = input(prompt).strip()
    return val if val else default


def select_option(prompt, options, default_idx=0):
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


def input_score(dim_name, ref=""):
    while True:
        raw = input(f"  {dim_name}{ref} [1-10]: ").strip()
        if not raw:
            return 5
        try:
            s = float(raw)
            if 1 <= s <= 10:
                return s
        except ValueError:
            pass
        print("请输入 1-10 之间的数字")


def get_input():
    print(f"\n{'=' * 55}")
    print(f"  📊 竞品对标分析工具 V{VERSION}")
    print(f"{'=' * 55}\n")

    info = {
        "project_name": input_str("📛 项目名称: ", "示例项目"),
        "audience": select_option("🎯 目标客群:", AUDIENCE_TYPES),
    }

    # 竞品数量
    n = input_int("\n📋 竞品数量（2-5个）[3]: ", 3)
    n = max(2, min(5, n))

    # 自己项目评分
    print(f"\n🏠 请输入【{info['project_name']}】各维度评分（参考：1-3薄弱 4-6中等 7-8良好 9-10标杆）：")
    self_scores = {}
    for d in DIMENSIONS:
        self_scores[d] = input_score(d)
    info["self_scores"] = self_scores

    # 竞品
    competitors = []
    for i in range(n):
        print(f"\n{'─' * 40}")
        print(f"  竞品 #{i + 1}")
        print(f"{'─' * 40}")
        c = {
            "name": input_str(f"  📛 名称: ", f"竞品{i+1}"),
            "type": select_option("  🏷️ 类型:", COMPETITOR_TYPES),
            "visitors": input_float("  👥 年客流量（万人）: ", 50),
            "price": input_float("  💰 客单价（元）: ", 150),
            "year": input_int("  📅 开业年份: ", 2020),
        }
        print("  📊 各维度评分：")
        scores = {}
        for d in DIMENSIONS:
            scores[d] = input_score(d, "（7-8=良好参考）")
        c["scores"] = scores
        competitors.append(c)

    info["competitors"] = competitors
    return info


def generate_svg_radar(info):
    """生成6维雷达图SVG"""
    cx, cy, r = 220, 220, 160
    angle_step = 360 / len(DIMENSIONS)

    # 网格
    layers = []
    for layer in [0.2, 0.4, 0.6, 0.8, 1.0]:
        pts = []
        for i, d in enumerate(DIMENSIONS):
            a = math.radians(angle_step * i - 90)
            x = cx + r * layer * math.cos(a)
            y = cy + r * layer * math.sin(a)
            pts.append(f"{x:.1f},{y:.1f}")
        layers.append(
            f'<polygon points="{" ".join(pts)}" fill="none" stroke="#2d2d44" stroke-width="1"/>')
        # 刻度标签
        a0 = math.radians(-90)
        lx = cx + r * layer * math.cos(a0)
        ly = cy + r * layer * math.sin(a0)
        layers.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="#555" font-size="9" text-anchor="end">{(layer*10):.0f}</text>')

    # 维度标签
    dim_labels = []
    for i, d in enumerate(DIMENSIONS):
        a = math.radians(angle_step * i - 90)
        lx = cx + (r + 30) * math.cos(a)
        ly = cy + (r + 30) * math.sin(a)
        anchor = "middle"
        if abs(lx - cx) > 5:
            anchor = "start" if lx > cx else "end"
        dim_labels.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" dominant-baseline="central" fill="#888" font-size="12">{d}</text>')

    # 绘制每个实体的雷达图
    colors = [
        {"fill": "rgba(46,204,113,0.15)", "stroke": "#2ecc71", "label": info["project_name"]},
    ]
    # 竞品颜色
    comp_colors = [
        ("#4a90d9", "rgba(74,144,217,0.12)"),
        ("#e74c3c", "rgba(231,76,60,0.12)"),
        ("#f39c12", "rgba(243,156,18,0.12)"),
        ("#9b59b6", "rgba(155,89,182,0.12)"),
        ("#1abc9c", "rgba(26,188,156,0.12)"),
    ]
    for idx, c in enumerate(info["competitors"]):
        col = comp_colors[idx % len(comp_colors)]
        colors.append({"fill": col[1], "stroke": col[0], "label": c["name"]})

    # 画自己
    all_polygons = []
    for e_idx, entity_list in enumerate([info["self_scores"]] + [c["scores"] for c in info["competitors"]]):
        pts = []
        for i, d in enumerate(DIMENSIONS):
            score = entity_list[d] / 10.0
            a = math.radians(angle_step * i - 90)
            x = cx + r * score * math.cos(a)
            y = cy + r * score * math.sin(a)
            pts.append(f"{x:.1f},{y:.1f}")
        col = colors[e_idx]
        all_polygons.append(
            f'<polygon points="{" ".join(pts)}" fill="{col["fill"]}" stroke="{col["stroke"]}" stroke-width="2"/>')

    # 图例
    legend = []
    for i, col in enumerate(colors):
        y = 30 + i * 25
        legend.append(
            f'<g transform="translate(460, {y})">'
            f'<rect x="0" y="0" width="14" height="14" rx="2" fill="{col["stroke"]}"/>'
            f'<text x="20" y="12" fill="#ccc" font-size="12">{col["label"]}</text>'
            f'</g>')

    return f'''<svg width="740" height="500" viewBox="0 0 740 500" xmlns="http://www.w3.org/2000/svg" style="background:transparent;font-family:'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;">
  <text x="370" y="20" text-anchor="middle" fill="#e0e0e0" font-size="16" font-weight="bold">六维竞争力雷达图</text>
  <g transform="translate(20, 30)">
    {chr(10).join(layers)}
    {chr(10).join(dim_labels)}
    {chr(10).join(all_polygons)}
  </g>
  {chr(10).join(legend)}
</svg>'''


def generate_scatter(info):
    """生成竞争力矩阵SVG"""
    cx, cy, w, h = 60, 330, 500, 240

    def get_x(c):
        return (c["scores"]["资源禀赋"] + c["scores"]["产品丰富度"]) / 2

    def get_y(c):
        return (c["scores"]["市场影响力"] + c["scores"]["运营能力"]) / 2

    # 自己
    self_x = (info["self_scores"]["资源禀赋"] + info["self_scores"]["产品丰富度"]) / 2
    self_y = (info["self_scores"]["市场影响力"] + info["self_scores"]["运营能力"]) / 2

    scale_x = w / 12
    scale_y = h / 12

    dots = []

    # 自己
    px = cx + self_x * scale_x
    py = cy - self_y * scale_y
    dots.append(
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="10" fill="none" stroke="#2ecc71" stroke-width="3"/>'
        f'<text x="{px:.1f}" y="{py + 20:.1f}" text-anchor="middle" fill="#2ecc71" font-size="10">{info["project_name"]}</text>')

    comp_colors_stroke = ["#4a90d9", "#e74c3c", "#f39c12", "#9b59b6", "#1abc9c"]
    for idx, c in enumerate(info["competitors"]):
        x = (c["scores"]["资源禀赋"] + c["scores"]["产品丰富度"]) / 2
        y = (c["scores"]["市场影响力"] + c["scores"]["运营能力"]) / 2
        px = cx + x * scale_x
        py = cy - y * scale_y
        r_size = max(8, min(20, c["visitors"] / 10))
        col = comp_colors_stroke[idx % len(comp_colors_stroke)]
        dots.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r_size:.1f}" fill="none" stroke="{col}" stroke-width="2" opacity="0.8"/>'
            f'<text x="{px:.1f}" y="{py + r_size + 14:.1f}" text-anchor="middle" fill="{col}" font-size="10">{c["name"]}</text>')

    return f'''<svg width="620" height="300" viewBox="0 0 620 300" xmlns="http://www.w3.org/2000/svg" style="background:transparent;font-family:'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;">
  <text x="310" y="20" text-anchor="middle" fill="#e0e0e0" font-size="14" font-weight="bold">竞争力矩阵（气泡大小=客流量）</text>
  <!-- 坐标轴 -->
  <line x1="{cx}" y1="{cy}" x2="{cx + w}" y2="{cy}" stroke="#2d2d44" stroke-width="1"/>
  <line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - h}" stroke="#2d2d44" stroke-width="1"/>
  <!-- 网格线 -->
  <line x1="{cx + w/2}" y1="{cy}" x2="{cx + w/2}" y2="{cy - h}" stroke="#1e1e36" stroke-width="1" stroke-dasharray="3,3"/>
  <line x1="{cx}" y1="{cy - h/2}" x2="{cx + w}" y2="{cy - h/2}" stroke="#1e1e36" stroke-width="1" stroke-dasharray="3,3"/>
  <!-- 象限标签 -->
  <text x="{cx + w - 10}" y="{cy - 10}" text-anchor="end" fill="#444" font-size="11">资源+产品 →</text>
  <text x="{cx + 10}" y="{cy - h + 15}" fill="#444" font-size="11">↑ 市场+运营</text>
  <!-- 象限名 -->
  <text x="{cx + w - 5}" y="{cy - h + 18}" text-anchor="end" fill="#2ecc71" font-size="11" font-weight="bold">领跑者</text>
  <text x="{cx + 5}" y="{cy - h + 18}" fill="#f39c12" font-size="11" font-weight="bold">潜力股</text>
  <text x="{cx + w - 5}" y="{cy - 5}" text-anchor="end" fill="#4a90d9" font-size="11" font-weight="bold">挑战者</text>
  <text x="{cx + 5}" y="{cy - 5}" fill="#e74c3c" font-size="11" font-weight="bold">补课生</text>
  <!-- 数据点 -->
  {chr(10).join(dots)}
</svg>'''


def generate_html(info):
    radar_svg = generate_svg_radar(info)
    scatter_svg = generate_scatter(info)

    # 计算排名表
    rows_data = []
    entities = [{"name": info["project_name"], "scores": info["self_scores"], "is_self": True}] + \
               [{"name": c["name"], "scores": c["scores"], "visitors": c["visitors"], "price": c["price"], "year": c["year"], "type": c["type"], "is_self": False} for c in info["competitors"]]

    for e in entities:
        total = sum(e["scores"].values())
        avg = total / len(DIMENSIONS)
        e["total"] = total
        e["avg"] = avg

    for e in entities:
        row_scores = "".join([f'<td>{e["scores"][d]:.1f}</td>' for d in DIMENSIONS])
        v_str = f'{e["visitors"]}万' if not e.get("is_self") else "-"
        p_str = f'{e["price"]}元' if not e.get("is_self") else "-"
        y_str = str(e.get("year", "")) if not e.get("is_self") else "-"
        t_str = e.get("type", "") if not e.get("is_self") else "-"
        cls = "self-row" if e.get("is_self") else ""
        rows_data.append({
            "html": f'<tr class="{cls}"><td><strong>{e["name"]}</strong></td>{row_scores}<td>{e["total"]:.1f}</td><td>{e["avg"]:.1f}</td><td>{v_str}</td><td>{p_str}</td><td>{t_str}</td><td>{y_str}</td></tr>',
            "total": e["total"],
        })

    # 按总分排序
    sorted_by_total = sorted(rows_data, key=lambda x: x["total"], reverse=True)

    rank_table = '<table class="rank-table"><thead><tr><th>项目名称</th>' + \
        "".join([f'<th>{d}</th>' for d in DIMENSIONS]) + \
        '<th>总分</th><th>均分</th><th>年客流</th><th>客单价</th><th>类型</th><th>开业</th></tr></thead><tbody>'
    rank_table += "".join([r["html"] for r in sorted_by_total])
    rank_table += '</tbody></table>'

    # SWOT分析
    self_scores = info["self_scores"]
    avg_dim_self = {d: self_scores[d] for d in DIMENSIONS}
    # 找对手每个维度的平均分
    avg_dim_comp = {}
    for d in DIMENSIONS:
        vals = [c["scores"][d] for c in info["competitors"]]
        avg_dim_comp[d] = sum(vals) / len(vals)

    strengths = []
    weaknesses = []
    for d in DIMENSIONS:
        diff = avg_dim_self[d] - avg_dim_comp[d]
        if diff >= 1.5:
            strengths.append(f'<li><strong>{d}</strong>：评分 {avg_dim_self[d]:.1f}，高于竞品均值 {diff:.1f} 分，为显著优势</li>')
        elif diff <= -1.5:
            weaknesses.append(f'<li><strong>{d}</strong>：评分 {avg_dim_self[d]:.1f}，低于竞品均值 {abs(diff):.1f} 分，需要重点提升</li>')

    if not strengths:
        strengths.append("<li>各维度相对竞品无明显领先优势，建议聚焦1-2个维度打造差异化</li>")
    if not weaknesses:
        weaknesses.append("<li>各维度与竞品差距不大，但需警惕被全面超越的风险</li>")

    # 机会与威胁
    max_comp_name = max(info["competitors"], key=lambda c: c["scores"]["市场影响力"])["name"]
    min_price_comp = min(info["competitors"], key=lambda c: c["price"])
    opportunities = [
        "<li><strong>消费升级趋势</strong>：客单价普遍在 {}元区间，仍有提升空间，可通过产品升级提高ARPU</li>".format(
            f"{min(c['price'] for c in info['competitors']):.0f}-{max(c['price'] for c in info['competitors']):.0f}"),
        "<li><strong>差异化定位</strong>：目标客群「{}」可与其他竞品形成错位竞争</li>".format(info["audience"]),
        "<li><strong>夜经济/研学/康养</strong>等新兴赛道尚未被充分开发，可率先布局</li>",
    ]
    threats = [
        "<li><strong>竞品升级压力</strong>：{}等头部竞品市场影响力强，可能持续扩大份额</li>".format(max_comp_name),
        "<li><strong>同质化风险</strong>：区域内已有 {} 个竞品，需强化核心IP避免同质���</li>".format(len(info["competitors"])),
        "<li><strong>政策/市场波动</strong>：文旅消费受宏观经济影响大，需控制负债率，保持灵活性</li>",
    ]

    # 差异化建议
    best_dim = max(DIMENSIONS, key=lambda d: avg_dim_self[d] - avg_dim_comp.get(d, 0))
    worst_dim = min(DIMENSIONS, key=lambda d: avg_dim_self[d] - avg_dim_comp.get(d, 0))

    diff_advice = [
        '<li><strong>强化「{}」优势</strong>：评分 {:.1f}，远高于竞品均值 {:.1f}，可围绕此构建核心竞争力。建议加大投入形成壁垒，使之成为项目的代名词。</li>'.format(
            best_dim, avg_dim_self[best_dim], avg_dim_comp.get(best_dim, 0)),
        '<li><strong>补足「{}」短板</strong>：评分 {:.1f}，低于竞品均值 {:.1f}，建议制定专项提升计划。可考虑引入战略合作、专业运营团队或针对性投资。</li>'.format(
            worst_dim, avg_dim_self[worst_dim], avg_dim_comp.get(worst_dim, 0)),
        '<li><strong>客群错位策略</strong>：针对「{}」客群深度开发，在体验设计、服务标准、传播渠道上做精细运营，形成细分市场壁垒。</li>'.format(info["audience"]),
    ]

    sundry_html = ""
    for c in info["competitors"]:
        sundry_html += f'<div class="comp-card"><div class="comp-name"><span class="comp-dot" style="background:#2ecc71;"></span>{c["name"]}</div><div class="comp-info">{c["type"]} · 年客流{c["visitors"]:.0f}万 · 客单价{c["price"]:.0f}元 · 开业{c["year"]}</div></div>'

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{info["project_name"]} · 竞品对标分析 V{VERSION}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#0f0f23;color:#e0e0e0;font-family:'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;}}
.container{{max-width:1200px;margin:0 auto;padding:20px;}}
.header{{text-align:center;padding:30px 0 15px;border-bottom:1px solid #2d2d44;margin-bottom:25px;}}
.header h1{{font-size:26px;}}
.header .sub{{color:#666;font-size:14px;margin-top:5px;}}
h2{{font-size:18px;color:#e0e0e0;margin:25px 0 12px;}}
h2.sec{{border-left:3px solid #f39c12;padding-left:12px;}}
.flex{{display:flex;flex-wrap:wrap;gap:25px;margin-bottom:25px;}}
.card{{background:#1a1a2e;border-radius:10px;padding:20px;border:1px solid #2d2d44;flex:1;min-width:300px;}}
.rank-table{{width:100%;border-collapse:collapse;font-size:13px;}}
.rank-table th{{background:#1e1e36;color:#888;padding:8px 6px;text-align:center;border:1px solid #2d2d44;font-weight:normal;}}
.rank-table td{{padding:6px;text-align:center;border:1px solid #2d2d44;}}
.rank-table .self-row{{background:rgba(46,204,113,0.08);}}
.rank-table .self-row td:first-child{{color:#2ecc71;font-weight:bold;}}
.swot-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:10px 0;}}
.swot-box{{background:#1a1a2e;border-radius:8px;padding:15px;border:1px solid #2d2d44;}}
.swot-box h3{{font-size:14px;margin-bottom:8px;}}
.swot-box ul{{list-style:none;padding:0;}}
.swot-box li{{font-size:13px;color:#aaa;padding:5px 0;border-bottom:1px solid #1e1e36;line-height:1.5;}}
.swot-box li:last-child{{border:none;}}
.swot-s{{border-left:3px solid #2ecc71;}}
.swot-w{{border-left:3px solid #e74c3c;}}
.swot-o{{border-left:3px solid #4a90d9;}}
.swot-t{{border-left:3px solid #f39c12;}}
.advice-box{{background:#1a1a2e;border-radius:8px;padding:15px;border:1px solid #2d2d44;margin:10px 0;}}
.advice-box li{{font-size:13px;color:#aaa;padding:6px 0;line-height:1.5;}}
.footer{{margin-top:30px;padding:15px 0;text-align:center;border-top:1px solid #2d2d44;color:#444;font-size:12px;}}
.tag{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;margin-left:5px;}}
.tag-red{{background:rgba(231,76,60,0.2);color:#e74c3c;}}
.tag-green{{background:rgba(46,204,113,0.2);color:#2ecc71;}}
.tag-blue{{background:rgba(74,144,217,0.2);color:#4a90d9;}}
.comp-card{{background:#1e1e36;border-radius:6px;padding:8px 10px;margin:4px 0;}}
.comp-name{{font-weight:bold;font-size:13px;display:flex;align-items:center;gap:6px;}}
.comp-dot{{width:8px;height:8px;border-radius:50%;display:inline-block;}}
.comp-info{{font-size:11px;color:#666;margin-top:2px;}}
.self-tag{{display:inline-block;background:rgba(46,204,113,0.15);color:#2ecc71;padding:1px 6px;border-radius:3px;font-size:10px;}}
@media(max-width:768px){{.swot-grid{{grid-template-columns:1fr;}}}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📊 {info["project_name"]} · 竞品对标分析</h1>
    <div class="sub">目标客群：{info["audience"]} · 竞品数量：{len(info["competitors"])}个 · V{VERSION}</div>
  </div>

  <div class="flex">
    <div class="card" style="flex:2;min-width:450px;">
      {radar_svg}
    </div>
    <div class="card" style="flex:1;min-width:200px;">
      <h2 style="font-size:14px;margin-bottom:10px;">竞品概览</h2>
      <div style="margin-bottom:8px;"><span class="self-tag">★ 本项目</span> <strong>{info["project_name"]}</strong></div>
      {sundry_html}
      <h2 style="font-size:14px;margin:15px 0 8px;">评分参考</h2>
      <div style="font-size:12px;color:#666;line-height:1.8;">
        1-3分 = 薄弱<br>
        4-6分 = 中等<br>
        7-8分 = 良好<br>
        9-10分 = 标杆
      </div>
    </div>
  </div>

  <h2 class="sec">📈 竞争力矩阵</h2>
  <div class="card">
    {scatter_svg}
  </div>

  <h2 class="sec">🏆 综合排名</h2>
  <div class="card" style="overflow-x:auto;">
    {rank_table}
  </div>

  <h2 class="sec">🔄 SWOT 分析</h2>
  <div class="swot-grid">
    <div class="swot-box swot-s"><h3 style="color:#2ecc71;">💪 优势 (Strengths)</h3><ul>{"".join(strengths)}</ul></div>
    <div class="swot-box swot-w"><h3 style="color:#e74c3c;">🔻 劣势 (Weaknesses)</h3><ul>{"".join(weaknesses)}</ul></div>
    <div class="swot-box swot-o"><h3 style="color:#4a90d9;">🚀 机会 (Opportunities)</h3><ul>{"".join(opportunities)}</ul></div>
    <div class="swot-box swot-t"><h3 style="color:#f39c12;">⚠️ 威胁 (Threats)</h3><ul>{"".join(threats)}</ul></div>
  </div>

  <h2 class="sec">💡 差异化建议</h2>
  <div class="advice-box">
    <ul>{"".join(diff_advice)}</ul>
  </div>

  <div class="footer">
    由文旅策划规划助手·竞品对标分析工具自动生成 · V{VERSION} · {datetime.now().strftime('%Y-%m-%d %H:%M')}<br>
    ⚠️ 所有评分为经验参考值，正式方案需结合实地调研
  </div>
</div>
</body>
</html>'''


def main():
    info = get_input()
    html = generate_html(info)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = os.path.join(OUTPUT_DIR, f"{info['project_name']}_竞品对标分析_v{VERSION}.html")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n{'=' * 55}")
    print(f"  ✅ 竞品对标分析已生成：")
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
