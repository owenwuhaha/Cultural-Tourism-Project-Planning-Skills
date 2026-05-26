#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文旅项目总览看板 V2.4
Project Dashboard Generator — Cultural Tourism
================================================

功能说明：
  扫描 F:/owen/hermes/projects/ 目录下的所有已生成文件，
  自动按项目分类聚合，生成统一总览看板HTML。

用法：
  python project-dashboard.py [--dir 扫描目录路径]

依赖：Python 3.7+ (标准库)
输出：F:/owen/hermes/projects/文旅项目总览看板_V2.4.html
（或自定义目录下）
"""

import glob
import os
import re
import webbrowser
from datetime import datetime

VERSION = "2.4"
DEFAULT_DIR = os.path.expandvars(r"F:\owen\hermes\projects")
OUTPUT_DIR = DEFAULT_DIR

# 文件类型识别规则
FILE_PATTERNS = [
    # (后缀, 类别显示名, 图标, 颜色)
    (".md",   "策划方案", "📋", "#2ecc71"),
    (".html", "HTML报告", "🌐", "#4a90d9"),
    (".pdf",  "PDF文档", "📄", "#e74c3c"),
    (".xlsx", "Excel数据", "📊", "#f39c12"),
    (".pptx", "PPT演示", "📽️", "#9b59b6"),
    (".png",  "图片",    "🖼️", "#1abc9c"),
    (".jpg",  "图片",    "🖼️", "#1abc9c"),
    (".jpeg", "图片",    "🖼️", "#1abc9c"),
    (".webp", "图片",    "🖼️", "#1abc9c"),
    (".gif",  "图片",    "🖼️", "#1abc9c"),
    (".svg",  "矢量图",  "🎨", "#e67e22"),
]

# 工具关键词识别（从文件名中提取生成工具）
TOOL_PATTERNS = [
    ("策划方案",    "generate-plan"),
    ("热力图",      "catchment-heatmap"),
    ("功能分区图",  "svg-zoning"),
    ("竞品对标",    "competitive-analysis"),
    ("投资测算",    "investment-calc"),
]


def identify_file_type(filename):
    """根据文件名和后缀识别文件类型"""
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    for suffix, cat, icon, color in FILE_PATTERNS:
        if ext == suffix:
            return cat, icon, color
    return "其他", "📁", "#888"


def identify_tool(filename):
    """从文件名识别生成工具"""
    for tool_name, script_key in TOOL_PATTERNS:
        if tool_name in filename:
            return tool_name
    return None


def extract_project_name(filename):
    """从文件名中提取项目名（取第一个分隔符之前的内容）"""
    name = os.path.splitext(filename)[0]
    # 尝试常见分隔符
    for sep in ["_", "-", "·", "．", "、"]:
        if sep in name:
            parts = name.split(sep)
            # 过滤明显不是项目名的关键词
            for kw in ["策划方案", "热力图", "功能分区图", "竞品对标", "分析", "投资", "测算",
                       "v", "V", "版本"]:
                if kw in parts[-1].lower():
                    return sep.join(parts[:-1])
    return name


def parse_project_from_plan(content):
    """从策划方案Markdown中提取项目名称"""
    # 匹配 Markdown 标题 # 项目名称
    m = re.search(r'^#\s+(.+?)(?:\s*[·\-—]\s*|$)', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None


def scan_directory(target_dir=None):
    """扫描目录，收集所有项目文件"""
    if target_dir is None:
        target_dir = DEFAULT_DIR

    if not os.path.isdir(target_dir):
        return [], f"目录不存在: {target_dir}"

    files = []
    for f in os.listdir(target_dir):
        full_path = os.path.join(target_dir, f)
        if os.path.isfile(full_path):
            stat = os.stat(full_path)
            cat, icon, color = identify_file_type(f)
            tool = identify_tool(f)
            file_size = stat.st_size
            mod_time = datetime.fromtimestamp(stat.st_mtime)
            files.append({
                "name": f,
                "path": full_path,
                "rel_path": f,
                "size": file_size,
                "size_str": format_size(file_size),
                "modified": mod_time,
                "modified_str": mod_time.strftime("%Y-%m-%d %H:%M"),
                "category": cat,
                "icon": icon,
                "color": color,
                "tool": tool,
            })

    # 按修改时间倒序排列
    files.sort(key=lambda x: x["modified"], reverse=True)
    return files, None


def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    else:
        return f"{size_bytes / 1024 / 1024:.1f}MB"


def group_by_project(files):
    """按项目名分组"""
    projects = {}
    for f in files:
        pname = extract_project_name(f["name"])
        if pname not in projects:
            projects[pname] = {"name": pname, "files": [], "count": 0, "total_size": 0, "latest": f["modified"]}
        projects[pname]["files"].append(f)
        projects[pname]["count"] += 1
        projects[pname]["total_size"] += f["size"]
        if f["modified"] > projects[pname]["latest"]:
            projects[pname]["latest"] = f["modified"]

    # 按最新修改时间倒序
    sorted_projects = sorted(projects.values(), key=lambda p: p["latest"], reverse=True)
    return sorted_projects


def group_by_category(files):
    """按类别分组"""
    categories = {}
    for f in files:
        cat = f["category"]
        if cat not in categories:
            categories[cat] = {"name": cat, "icon": f["icon"], "color": f["color"], "files": [], "count": 0}
        categories[cat]["files"].append(f)
        categories[cat]["count"] += 1
    return [v for k, v in sorted(categories.items(), key=lambda x: x[1]["count"], reverse=True)]


def generate_html(files, projects, categories, scan_dir, error_msg=None):
    """生成总览看板HTML"""

    total_files = len(files)
    total_size_str = format_size(sum(f["size"] for f in files))
    projects_count = len(projects)
    categories_count = len(categories)

    # 生成项目卡片
    project_cards = ""
    project_colors = ["#2ecc71", "#4a90d9", "#f39c12", "#e74c3c", "#9b59b6", "#1abc9c", "#e67e22", "#3498db"]
    for i, proj in enumerate(projects):
        files_in_proj = proj["files"]
        color = project_colors[i % len(project_colors)]
        file_list = ""
        for f in files_in_proj:
            file_list += f'''
            <div class="file-item" onclick="window.open('{os.path.abspath(f["path"]).replace(chr(92), "/")}','_blank')">
              <span class="file-icon" style="color:{f["color"]}">{f["icon"]}</span>
              <span class="file-name">{f["name"]}</span>
              <span class="file-meta">
                <span class="file-tool">{f["tool"] or f["category"]}</span>
                <span class="file-size">{f["size_str"]}</span>
                <span class="file-time">{f["modified_str"]}</span>
              </span>
            </div>'''

        proj_size_str = format_size(proj["total_size"])
        project_cards += f'''
        <div class="project-card" style="border-left:4px solid {color};">
          <div class="proj-header" onclick="toggleProj(this)">
            <div class="proj-title">
              <span class="proj-dot" style="background:{color};"></span>
              <span class="proj-name">{proj["name"] or "未分类"}</span>
              <span class="proj-badge">{proj["count"]}个文件</span>
              <span class="proj-size">{proj_size_str}</span>
            </div>
            <span class="toggle-icon">▼</span>
          </div>
          <div class="proj-files">
            {file_list}
          </div>
        </div>'''

    # 统计表格
    cat_rows = ""
    for cat in categories:
        cat_rows += f'''
        <tr>
          <td><span class="stats-icon" style="background:{cat["color"]};">{cat["icon"]}</span> {cat["name"]}</td>
          <td class="num">{cat["count"]}</td>
          <td class="num">{format_size(sum(f["size"] for f in cat["files"]))}</td>
        </tr>'''

    # 工具分布
    tool_counts = {}
    for f in files:
        if f["tool"]:
            tool_counts[f["tool"]] = tool_counts.get(f["tool"], 0) + 1

    tool_rows = ""
    for tool_name, count in sorted(tool_counts.items(), key=lambda x: x[1], reverse=True):
        pct = count / total_files * 100
        tool_rows += f'''
        <tr>
          <td>{tool_name}</td>
          <td class="num">{count}</td>
          <td><div class="bar-wrap"><div class="bar" style="width:{pct:.0f}%;"></div></div></td>
        </tr>'''

    tool_section = ""
    if tool_rows:
        tool_section = f'''<h2 style="margin-top:15px;">🔧 工具分布</h2>
      <div class="info-card" style="padding:0;">
        <table class="stats-table">
          <thead><tr><th>生成工具</th><th class="num">文件数</th><th></th></tr></thead>
          <tbody>{tool_rows}</tbody>
        </table>
      </div>'''

    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>文旅项目总览看板 V{VERSION}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#0f0f23;color:#e0e0e0;font-family:'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;}}
.container{{max-width:1200px;margin:0 auto;padding:20px;}}

/* 头部 */
.header{{text-align:center;padding:30px 0 20px;border-bottom:1px solid #2d2d44;margin-bottom:25px;}}
.header h1{{font-size:28px;color:#f0f0f0;}}
.header .sub{{color:#666;font-size:14px;margin-top:5px;}}

/* 统计卡片 */
.stats-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin-bottom:25px;}}
.stat-card{{background:#1a1a2e;border-radius:10px;padding:18px;border:1px solid #2d2d44;text-align:center;}}
.stat-num{{font-size:32px;font-weight:bold;color:#f0f0f0;}}
.stat-label{{font-size:13px;color:#666;margin-top:3px;}}

/* 双栏 */
.double-col{{display:flex;gap:20px;flex-wrap:wrap;margin-bottom:25px;}}
.col-left{{flex:2;min-width:350px;}}
.col-right{{flex:1;min-width:280px;}}

h2{{font-size:16px;color:#e0e0e0;margin-bottom:12px;border-left:3px solid #f39c12;padding-left:10px;}}

/* 项目卡片 */
.project-card{{background:#1a1a2e;border-radius:8px;margin-bottom:10px;overflow:hidden;border:1px solid #2d2d44;transition:border-color 0.2s;}}
.project-card:hover{{border-color:#3d3d5c;}}
.proj-header{{display:flex;justify-content:space-between;align-items:center;padding:12px 15px;cursor:pointer;user-select:none;}}
.proj-header:hover{{background:#1e1e36;}}
.proj-title{{display:flex;align-items:center;gap:10px;flex-wrap:wrap;}}
.proj-dot{{width:10px;height:10px;border-radius:50%;display:inline-block;flex-shrink:0;}}
.proj-name{{font-weight:bold;font-size:14px;}}
.proj-badge{{background:#1e1e36;color:#888;padding:1px 8px;border-radius:10px;font-size:11px;}}
.proj-size{{color:#555;font-size:12px;}}
.toggle-icon{{color:#555;font-size:12px;transition:transform 0.2s;}}
.proj-files{{padding:0 15px 12px;display:block;}}
.file-item{{display:flex;align-items:center;gap:8px;padding:7px 8px;border-radius:6px;cursor:pointer;transition:background 0.15s;}}
.file-item:hover{{background:#1e1e36;}}
.file-icon{{font-size:16px;width:24px;text-align:center;}}
.file-name{{flex:1;font-size:13px;color:#bbb;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}}
.file-meta{{display:flex;align-items:center;gap:8px;font-size:11px;flex-shrink:0;}}
.file-tool{{background:#1e1e36;color:#888;padding:1px 6px;border-radius:4px;}}
.file-size{{color:#555;}}
.file-time{{color:#444;}}

/* 统计表格 */
.stats-table{{width:100%;border-collapse:collapse;font-size:13px;}}
.stats-table th{{background:#1e1e36;color:#888;padding:8px 10px;text-align:left;border:1px solid #2d2d44;font-weight:normal;}}
.stats-table td{{padding:6px 10px;border:1px solid #2d2d44;color:#aaa;}}
.stats-table .num{{text-align:right;color:#e0e0e0;font-weight:bold;}}
.stats-icon{{display:inline-block;width:22px;height:22px;line-height:22px;text-align:center;border-radius:4px;font-size:12px;margin-right:4px;}}

/* 工具分布条 */
.bar-wrap{{background:#1e1e36;border-radius:4px;height:16px;overflow:hidden;}}
.bar{{height:100%;background:#2ecc71;border-radius:4px;opacity:0.7;}}

/* 侧边信息 */
.info-card{{background:#1a1a2e;border-radius:8px;padding:15px;border:1px solid #2d2d44;margin-bottom:10px;}}
.info-card p{{font-size:13px;color:#888;line-height:1.8;}}
.info-card .label{{color:#666;}}
.info-card .value{{color:#bbb;}}

/* 底部 */
.footer{{margin-top:30px;padding:15px 0;text-align:center;border-top:1px solid #2d2d44;color:#444;font-size:12px;}}

/* 响应式 */
@media(max-width:700px){{
  .stats-grid{{grid-template-columns:repeat(2,1fr);}}
  .file-meta{{flex-wrap:wrap;gap:3px;}}
}}

/* 折叠状态 */
.proj-files.collapsed{{display:none;}}
.toggle-icon.collapsed{{transform:rotate(-90deg);}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🏗️ 文旅项目总览看板</h1>
    <div class="sub">扫描目录：{scan_dir} · 生成时间：{scan_time} · V{VERSION}</div>
  </div>

  <div class="stats-grid">
    <div class="stat-card"><div class="stat-num">{total_files}</div><div class="stat-label">📄 总文件数</div></div>
    <div class="stat-card"><div class="stat-num">{projects_count}</div><div class="stat-label">🏗️ 项目数</div></div>
    <div class="stat-card"><div class="stat-num">{categories_count}</div><div class="stat-label">📂 文件类型</div></div>
    <div class="stat-card"><div class="stat-num">{total_size_str}</div><div class="stat-label">📦 总大小</div></div>
  </div>

  <div class="double-col">
    <div class="col-left">
      <h2>📁 项目分类</h2>
      {project_cards if project_cards else '<div style="color:#666;font-size:13px;padding:20px;text-align:center;">暂无项目文件</div>'}
    </div>
    <div class="col-right">
      <h2>📊 文件类型统计</h2>
      <div class="info-card" style="padding:0;">
        <table class="stats-table">
          <thead><tr><th>类别</th><th class="num">数量</th><th class="num">大小</th></tr></thead>
          <tbody>{cat_rows}</tbody>
        </table>
      </div>

      {tool_section}

      <h2 style="margin-top:15px;">💡 操作提示</h2>
      <div class="info-card">
        <p>
          <span class="label">📂 点击项目名</span> <span class="value">展开/收起文件列表</span><br>
          <span class="label">📄 点击文件</span> <span class="value">在浏览器中打开</span><br>
          <span class="label">🔄 <code>python project-dashboard.py</code></span> <span class="value">重新扫描刷新</span><br>
          <span class="label">📁 扫描目录：</span><span class="value">{scan_dir}</span>
        </p>
      </div>
    </div>
  </div>

  <div class="footer">
    由文旅策划规划助手·项目总览看板自动生成 · V{VERSION} · {scan_time}
  </div>
</div>
<script>
function toggleProj(header){{
  var files = header.nextElementSibling;
  files.classList.toggle('collapsed');
  header.querySelector('.toggle-icon').classList.toggle('collapsed');
}}
</script>
</body>
</html>'''


def main():
    import sys
    scan_dir = DEFAULT_DIR

    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:]):
            if arg == "--dir" and i + 2 < len(sys.argv):
                scan_dir = sys.argv[i + 2]

    files, err = scan_directory(scan_dir)
    if err:
        print(f"❌ {err}")
        return

    if not files:
        print(f"❌ 目录 {scan_dir} 中没有找到文件")
        return

    projects = group_by_project(files)
    categories = group_by_category(files)

    html = generate_html(files, projects, categories, scan_dir)

    output_file = os.path.join(OUTPUT_DIR, f"文旅项目总览看板_v{VERSION}.html")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n{'=' * 55}")
    print(f"  ✅ 文旅项目总览看板已生成：")
    print(f"     {output_file}")
    print(f"  📏 文件大小：{os.path.getsize(output_file):,} 字节")
    print(f"  📊 扫描到 {len(files)} 个文件，{len(projects)} 个项目")
    print(f"{'=' * 55}")

    try:
        webbrowser.open(f"file://{os.path.abspath(output_file)}")
        print("  🌐 已自动打开浏览器预览")
    except Exception:
        print("  请手动打开浏览器查看")


if __name__ == "__main__":
    main()
