#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文旅知识库动态查询工具 V2.5
Knowledge Base Query Tool — Cultural Tourism
===============================================

功能说明：
  交互查询 wenlv-wiki 知识库（f:/owen/wenlv-wiki/wiki/），
  支持按维度、关键词、按页面名几种方式浏览知识内容。

用法：
  python knowledge-query.py [--wiki 知识库路径]

依赖：Python 3.7+ (标准库)
知识库目录默认为 f:/owen/wenlv-wiki/wiki/
"""

import glob
import os
import re
import webbrowser
from datetime import datetime

VERSION = "2.5"
DEFAULT_WIKI_DIR = os.path.expandvars(r"F:\owen\wenlv-wiki\wiki")
OUTPUT_DIR = os.path.expandvars(r"F:\owen\hermes\projects")

# 八大维度的颜色和定义
DIMENSIONS = {
    "A": {"name": "政策法规", "icon": "📜", "color": "#e74c3c", "prefixes": ["concept-乡村振兴政策与资金申报", "concept-土地合规", "module-政策资金申报实操手册"]},
    "B": {"name": "策划方法论", "icon": "🧠", "color": "#4a90d9", "prefixes": ["concept-文旅策划方法论", "module-文旅项目策划全流程"]},
    "C": {"name": "规划体系", "icon": "📐", "color": "#2ecc71", "prefixes": ["concept-规划体系"]},
    "D": {"name": "农文旅融合", "icon": "🌾", "color": "#f39c12", "prefixes": ["concept-农文旅深度融合", "concept-乡村产业融合模式"]},
    "E": {"name": "康养疗愈", "icon": "🧘", "color": "#9b59b6", "prefixes": ["concept-康养疗愈旅游"]},
    "F": {"name": "运营升级", "icon": "🚀", "color": "#1abc9c", "prefixes": ["concept-沉浸式文旅与情绪价值", "concept-行业趋势2025-2026"]},
    "G": {"name": "商业模式", "icon": "💼", "color": "#e67e22", "prefixes": ["concept-商业模式设计", "concept-在地文化IP"]},
    "H": {"name": "行业趋势", "icon": "📈", "color": "#3498db", "prefixes": ["concept-行业趋势2025-2026"]},
}

# 页面类型前缀
PAGE_TYPES = {
    "concept": {"icon": "📘", "label": "概念", "color": "#4a90d9"},
    "source":  {"icon": "📄", "label": "来源", "color": "#2ecc71"},
    "module":  {"icon": "🔧", "label": "模块", "color": "#f39c12"},
    "case":    {"icon": "🏗️", "label": "案例", "color": "#e74c3c"},
    "log":     {"icon": "📝", "label": "日志", "color": "#888"},
}


def load_pages(wiki_dir):
    """加载知识库所有页面"""
    if not os.path.isdir(wiki_dir):
        return [], f"知识库目录不存在: {wiki_dir}"

    pages = []
    files = glob.glob(os.path.join(wiki_dir, "*.md"))
    for fpath in files:
        fname = os.path.basename(fpath)
        # 跳过 WIKI.md log.md index.md
        if fname in ("WIKI.md", "log.md", "index.md"):
            continue

        stat = os.stat(fpath)
        # 读取frontmatter
        title = fname
        page_type = "unknown"
        tags = []
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # 尝试解析YAML frontmatter
        fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            fm_raw = fm_match.group(1)
            for line in fm_raw.split("\n"):
                line = line.strip()
                if line.startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip('"').strip("'")
                elif line.startswith("type:"):
                    page_type = line.split(":", 1)[1].strip()
                elif line.startswith("tags:"):
                    # 尝试解析列表格式
                    tag_match = re.findall(r'\[(.*?)\]', line)
                    if tag_match:
                        tags = [t.strip().strip("'\"") for t in tag_match[0].split(",") if t.strip()]

        # 判断维度和分类
        prefix = fname.replace(".md", "")
        dimension_key = None
        for dk, dv in DIMENSIONS.items():
            for p in dv["prefixes"]:
                if prefix == p or prefix.startswith(p.split("-")[0]):
                    dimension_key = dk
                    break
            if dimension_key:
                break

        # 如果是source页，尝试从tags或前缀判断维度
        if not dimension_key:
            # 用关键词匹配
            content_lower = content.lower()
            dim_scores = {}
            for dk, dv in DIMENSIONS.items():
                kw_score = 0
                for kw in dv["name"]:
                    if kw in content_lower:
                        kw_score += 1
                for p in dv["prefixes"]:
                    if p.split("-")[1] in content_lower:
                        kw_score += 2
                dim_scores[dk] = kw_score
            if max(dim_scores.values()) > 0:
                dimension_key = max(dim_scores, key=dim_scores.get)

        # 内容概览（前200字）
        body = fm_match.group(0) if fm_match else ""
        body_end = content[len(body):].strip()
        preview = body_end[:200].replace("\n", " ").strip()
        if len(body_end) > 200:
            preview += "..."

        pt = PAGE_TYPES.get(page_type, {"icon": "📁", "label": page_type, "color": "#888"})

        pages.append({
            "file": fname,
            "path": fpath,
            "title": title,
            "type": page_type,
            "type_icon": pt["icon"],
            "type_label": pt["label"],
            "type_color": pt["color"],
            "size": stat.st_size,
            "size_str": f"{stat.st_size / 1024:.1f}KB",
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "modified_str": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            "preview": preview,
            "tags": tags,
            "dimension": dimension_key,
            "content": content,
        })

    pages.sort(key=lambda p: p["title"])
    return pages, None


def search_pages(pages, keyword):
    """按关键词搜索页面"""
    if not keyword:
        return pages
    kw = keyword.lower()
    results = []
    for p in pages:
        if kw in p["title"].lower() or kw in p["file"].lower():
            results.append(p)
            continue
        if kw in p["preview"].lower():
            results.append(p)
            continue
        if kw in p["content"].lower():
            results.append(p)
            continue
        for tag in p["tags"]:
            if kw in tag.lower():
                results.append(p)
                break
    return results


def filter_by_dimension(pages, dim_key):
    """按维度筛选"""
    if not dim_key:
        return pages
    return [p for p in pages if p["dimension"] == dim_key]


def filter_by_type(pages, page_type):
    """按页面类型筛选"""
    if not page_type:
        return pages
    return [p for p in pages if p["type"] == page_type]


def export_to_html(pages, wiki_dir, query_desc=""):
    """导出查询结果为HTML"""
    # 按维度分组
    dim_groups = {}
    for dk, dv in DIMENSIONS.items():
        dim_groups[dk] = []
    for p in pages:
        dk = p["dimension"] or "other"
        if dk not in dim_groups:
            dim_groups[dk] = []
        dim_groups[dk].append(p)

    # 生成主体
    body = ""
    if query_desc:
        body += f'<div class="query-badge">🔍 查询条件：{query_desc}</div>'

    for dk in sorted(DIMENSIONS.keys()):
        if dk not in dim_groups or not dim_groups[dk]:
            continue
        dv = DIMENSIONS[dk]
        page_list = ""
        for p in dim_groups[dk]:
            page_list += f'''
            <div class="kb-item" onclick="openPage('{os.path.abspath(p["path"]).replace(chr(92), "/")}')">
              <div class="kb-title">
                <span class="kb-icon" style="color:{p["type_color"]}">{p["type_icon"]}</span>
                <span class="kb-name">{p["title"]}</span>
                <span class="kb-badge" style="background:{p["type_color"]}">{p["type_label"]}</span>
              </div>
              <div class="kb-meta">
                <span>{p["size_str"]}</span>
                <span>更新 {p["modified_str"]}</span>
                {f'<span>{" ".join(["#" + t for t in p["tags"][:3]])}</span>' if p["tags"] else ""}
              </div>
              <div class="kb-preview">{p["preview"]}</div>
            </div>'''

        body += f'''
        <div class="dim-section">
          <div class="dim-header" style="border-left:3px solid {dv["color"]};">
            <span class="dim-icon">{dv["icon"]}</span>
            <span class="dim-name">{dv["name"]}</span>
            <span class="dim-count">{len(dim_groups[dk])}页</span>
            <span class="dim-code">[{dk}]</span>
          </div>
          {page_list}
        </div>'''

    # 其他维度
    other = dim_groups.get("other", [])
    if other:
        other_list = ""
        for p in other:
            other_list += f'''
            <div class="kb-item" onclick="openPage('{os.path.abspath(p["path"]).replace(chr(92), "/")}')">
              <div class="kb-title">
                <span class="kb-icon" style="color:{p["type_color"]}">{p["type_icon"]}</span>
                <span class="kb-name">{p["title"]}</span>
                <span class="kb-badge" style="background:{p["type_color"]}">{p["type_label"]}</span>
              </div>
              <div class="kb-preview">{p["preview"]}</div>
            </div>'''
        body += f'''
        <div class="dim-section">
          <div class="dim-header" style="border-left:3px solid #888;">
            <span class="dim-icon">📁</span>
            <span class="dim-name">其他</span>
            <span class="dim-count">{len(other)}页</span>
          </div>
          {other_list}
        </div>'''

    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>文旅知识库查询结果 V{VERSION}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#0f0f23;color:#e0e0e0;font-family:'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;}}
.container{{max-width:1000px;margin:0 auto;padding:20px;}}
.header{{text-align:center;padding:25px 0 15px;border-bottom:1px solid #2d2d44;margin-bottom:20px;}}
.header h1{{font-size:24px;}}
.header .sub{{color:#666;font-size:13px;margin-top:3px;}}
.query-badge{{background:#1a1a2e;border:1px solid #2d2d44;border-radius:6px;padding:8px 12px;margin-bottom:15px;font-size:13px;color:#aaa;}}
.dim-section{{margin-bottom:15px;}}
.dim-header{{display:flex;align-items:center;gap:8px;background:#1a1a2e;padding:10px 12px;border-radius:8px 8px 0 0;border:1px solid #2d2d44;}}
.dim-icon{{font-size:18px;}}
.dim-name{{font-weight:bold;font-size:14px;flex:1;}}
.dim-count{{color:#888;font-size:12px;}}
.dim-code{{color:#444;font-size:11px;}}
.kb-item{{background:#1a1a2e;border-left:1px solid #2d2d44;border-right:1px solid #2d2d44;border-bottom:1px solid #1e1e36;padding:10px 15px;cursor:pointer;transition:background 0.15s;}}
.kb-item:last-of-type{{border-radius:0 0 8px 8px;border-bottom:1px solid #2d2d44;}}
.kb-item:hover{{background:#1e1e36;}}
.kb-title{{display:flex;align-items:center;gap:8px;}}
.kb-icon{{font-size:14px;}}
.kb-name{{font-weight:bold;font-size:13px;flex:1;}}
.kb-badge{{font-size:10px;padding:1px 6px;border-radius:4px;color:#fff;}}
.kb-meta{{display:flex;gap:10px;font-size:11px;color:#555;margin-top:3px;}}
.kb-preview{{font-size:12px;color:#777;margin-top:4px;line-height:1.4;overflow:hidden;text-overflow:ellipsis;}}
.footer{{margin-top:25px;padding:12px 0;text-align:center;border-top:1px solid #2d2d44;color:#444;font-size:12px;}}
.os-link{{display:inline-block;background:#1e1e36;color:#888;padding:3px 10px;border-radius:4px;font-size:12px;margin:2px;text-decoration:none;border:1px solid #2d2d44;}}
.os-link:hover{{background:#2d2d44;color:#ccc;}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📚 文旅知识库查询结果</h1>
    <div class="sub">目录：{wiki_dir} · 共 {len(pages)} 页 · {scan_time} · V{VERSION}</div>
  </div>
  {body}
  <div class="footer">
    由文旅策划规划助手·知识库查询工具自动生成 · V{VERSION} · {scan_time}
  </div>
</div>
<script>
function openPage(url){{window.open(url,'_blank');}}
</script>
</body>
</html>'''


def print_separator(char="=", width=55):
    print(f"\n{char * width}")


def print_header(text):
    print_separator()
    print(f"  {text}")
    print_separator()


def main():
    import sys

    wiki_dir = DEFAULT_WIKI_DIR
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--wiki" and i + 2 < len(sys.argv):
            wiki_dir = sys.argv[i + 2]

    pages, err = load_pages(wiki_dir)
    if err:
        print(f"❌ {err}")
        return

    if not pages:
        print(f"❌ 知识库 {wiki_dir} 中没有找到页面")
        return

    print(f"\n{'=' * 55}")
    print(f"  📚 文旅知识库动态查询工具 V{VERSION}")
    print(f"  目录：{wiki_dir}  · 共 {len(pages)} 个页面")
    print(f"{'=' * 55}")

    while True:
        print()
        print(f"  ┌──────────── 查询方式 ────────────┐")
        print(f"  │ 1) 🔍 按关键词搜索              │")
        print(f"  │ 2) 📂 按维度浏览                │")
        print(f"  │ 3) 📄 按页面类型筛选             │")
        print(f"  │ 4) 📋 浏览全部                  │")
        print(f"  │ 5) 🌐 导出为HTML看板            │")
        print(f"  │ 0) ❌ 退出                     │")
        print(f"  └─────────────────────────────────┘")

        choice = input("  ⏩ 请选择: ").strip()

        if choice == "0":
            print("\n  👋 感谢使用，再见！")
            break

        elif choice == "1":
            keyword = input("  🔍 请输入关键词: ").strip()
            if not keyword:
                continue
            results = search_pages(pages, keyword)
            print(f"\n  📊 找到 {len(results)} 个匹配页面：「{keyword}」")
            for p in results:
                print(f"    {p['type_icon']} {p['title']}  [{p['file']}]  —  {p['preview'][:60]}...")
            print()

            # 询问是否查看详情
            if results:
                sel = input("  输入数字查看详情（0返回）: ").strip()
                if sel.isdigit():
                    idx = int(sel) - 1
                    if 0 <= idx < len(results):
                        show_page_detail(results[idx])

        elif choice == "2":
            print("\n  维度选择：")
            dim_keys = sorted(DIMENSIONS.keys())
            for dk in dim_keys:
                dv = DIMENSIONS[dk]
                count = len([p for p in pages if p["dimension"] == dk])
                print(f"    {dv['icon']} {dv['name']} [{dk}] — {count}页")
            print(f"    📁 其他/未分类 — {len([p for p in pages if not p['dimension']])}页")
            dim_choice = input("\n  请输入维度字母: ").strip().upper()
            if dim_choice == "OTHER" or dim_choice == "O":
                results = [p for p in pages if not p["dimension"]]
            elif dim_choice in DIMENSIONS:
                dv = DIMENSIONS[dim_choice]
                results = filter_by_dimension(pages, dim_choice)
                print(f"\n  {dv['icon']} {dv['name']} 维度 — {len(results)} 页：")
            else:
                print("  ❌ 无效选择")
                continue

            for i, p in enumerate(results, 1):
                print(f"    {i:2d}. {p['type_icon']} {p['title']}  ({p['type_label']})")
            print()

            sel = input("  输入数字查看详情（0返回）: ").strip()
            if sel.isdigit():
                idx = int(sel) - 1
                if 0 <= idx < len(results):
                    show_page_detail(results[idx])

        elif choice == "3":
            print("\n  页面类型：")
            type_list = sorted(PAGE_TYPES.keys())
            for t in type_list:
                pt = PAGE_TYPES[t]
                count = len([p for p in pages if p["type"] == t])
                print(f"    {pt['icon']} {pt['label']} — {count}页")
            type_choice = input("\n  请输入类型: ").strip().lower()
            if type_choice in PAGE_TYPES:
                results = filter_by_type(pages, type_choice)
                pt = PAGE_TYPES[type_choice]
                print(f"\n  {pt['icon']} {pt['label']} — {len(results)} 页：")
            else:
                print("  ❌ 无效选择")
                continue

            for i, p in enumerate(results, 1):
                print(f"    {i:2d}. {p['title']}  ({p['file']})")
            print()

            sel = input("  输入数字查看详情（0返回）: ").strip()
            if sel.isdigit():
                idx = int(sel) - 1
                if 0 <= idx < len(results):
                    show_page_detail(results[idx])

        elif choice == "4":
            results = pages
            print(f"\n  📋 全部页面 — {len(pages)} 页：")
            for dk in sorted(DIMENSIONS.keys()):
                dv = DIMENSIONS[dk]
                dim_pages = [p for p in pages if p["dimension"] == dk]
                if dim_pages:
                    print(f"\n    {dv['icon']} [{dk}] {dv['name']}")
                    for p in dim_pages:
                        print(f"      {p['type_icon']} {p['title']}")

            other = [p for p in pages if not p["dimension"]]
            if other:
                print(f"\n    📁 其他")
                for p in other:
                    print(f"      {p['type_icon']} {p['title']}")

            sel = input("\n  输入页面序号（在全部列表中），或0返回: ").strip()
            if sel.isdigit():
                idx = int(sel) - 1
                if 0 <= idx < len(pages):
                    show_page_detail(pages[idx])

        elif choice == "5":
            # 导出HTML
            keyword = input("  查询关键词（留空=全部）: ").strip()
            if keyword:
                results = search_pages(pages, keyword)
                query_desc = f"关键词「{keyword}」· {len(results)}页"
            else:
                results = pages
                query_desc = f"全量知识库 · {len(results)}页"

            html = export_to_html(results, wiki_dir, query_desc)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            kw_for_file = keyword.replace(" ", "_") if keyword else "全部"
            outfile = os.path.join(OUTPUT_DIR, f"知识库查询_{kw_for_file}_{ts}_v{VERSION}.html")
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            with open(outfile, "w", encoding="utf-8") as f:
                f.write(html)

            print(f"\n  ✅ 已导出：{outfile}")
            print(f"  📏 大小：{os.path.getsize(outfile):,} 字节")
            try:
                webbrowser.open(f"file://{os.path.abspath(outfile)}")
                print("  🌐 已自动打开浏览器预览")
            except Exception:
                pass

        else:
            print("  ❌ 请输入 0-5")


def show_page_detail(page):
    """显示页面详情"""
    print(f"\n{'─' * 55}")
    print(f"  {page['type_icon']} {page['title']}")
    print(f"  📄 {page['file']}  |  {page['size_str']}  |  更新 {page['modified_str']}")
    print(f"  🏷️  {page['type_label']}  |  维��：{page['dimension'] or '未分类'}")
    if page["tags"]:
        print(f"  # {'  #'.join(page['tags'][:5])}")
    print(f"{'─' * 55}")
    # 显示正文前800字
    body = page["content"]
    # 移除frontmatter
    body = re.sub(r'^---.*?\n---\s*', '', body, count=1, flags=re.DOTALL)
    print(f"\n{body[:800].strip()}")
    if len(body) > 800:
        print("  ... (内容较长，仅显示前800字)")
    print(f"\n  📁 {os.path.dirname(os.path.abspath(page['path']))}")
    print()


if __name__ == "__main__":
    main()
