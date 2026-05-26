#!/usr/bin/env python3
"""
文旅策划工具箱总控台 — V2.2
Cultural Tourism Project Planning Toolkit — Main Console
交互式总控台，集成多个文旅策划子工具
"""

import os
import sys
import subprocess
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
VERSION = "V2.2"
TOOLS_DIR = Path(__file__).parent.resolve()
PROJECTS_DIR = Path("F:/owen/hermes/projects")

SCRIPTS = [
    ("generate-plan.py",   "📊 自动策划方案"),
    ("investment-calc.py", "📈 投资测算工具"),
    ("catchment-heatmap.py","🌐 客源圈层热力图"),
    ("competitive-analysis.py", "📊 竞品对标分析"),
    ("svg-zoning.py",      "🗺️ SVG功能分区图"),
]

# ── Banner ────────────────────────────────────────────
BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║                                                            ║
║     🏔️  ⛰️  文 旅 策 划 工 具 箱   🏯  🌊                    ║
║     ═══════════════════════════════════════════════════     ║
║                                                            ║
║        ╱╲      ╱╲     ╔═══╗   ╔════╗  ╔══╗  ╔════╗         ║
║       ╱  ╲    ╱  ╲    ║ ║ ║   ║ ╔╗ ║  ║ ║  ║ ╔╗ ║         ║
║      ╱    ╲  ╱    ╲   ║ ║ ║   ║ ╚╝ ║  ║ ║  ║ ╚╝ ║         ║
║     ╱______╲╱______╲  ║ ║ ║   ║ ╔╗ ║  ║ ║  ║ ╔╗ ║         ║
║    ╱        ╲        ╲ ║ ║ ║   ║ ║║ ║  ║ ║  ║ ║║ ║         ║
║   ╱          ╲         ╲╚═╝ ╚═══╝ ║║ ╚══╝  ╚═╝║║ ║         ║
║  ╱            ╲          ╚════════╝╚══════╝   ╚═╝          ║
║                                                            ║
║         文旅策划工具箱总控台 — {ver}                    ║
║                                                            ║
╚══════════════════════════════════════════════════════════════╝
""".format(ver=VERSION)


# ── 工具函数 ──────────────────────────────────────────

def clear_screen():
    """清理控制台屏幕"""
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    """打印 Banner 和版本信息"""
    clear_screen()
    print(BANNER)
    print()


def show_menu():
    """显示主菜单，返回用户选项"""
    print("  ═══════════════════════════════════════════════")
    print("  请选择要启动的工具：")
    print()

    for idx, (script, label) in enumerate(SCRIPTS, 1):
        path = TOOLS_DIR / script
        status = " ✅" if path.exists() else " ⚠️  未找到"
        print(f"    {idx}) {label}{status}")

    print(f"    {len(SCRIPTS) + 1}) 📋 查看已生成文件列表")
    print(f"    {len(SCRIPTS) + 2}) ❌ 退出")
    print()
    print("  ═══════════════════════════════════════════════")

    while True:
        try:
            choice = input("  ⏩ 请输入选项编号: ").strip()
            num = int(choice)
            if 1 <= num <= len(SCRIPTS) + 2:
                return num
            print(f"  ⚠️  请输入 1 ~ {len(SCRIPTS) + 2} 之间的数字。")
        except ValueError:
            print("  ⚠️  请输入有效的数字。")


def run_script(script_name: str):
    """用 subprocess 调用子脚本，等待结束后返回"""
    script_path = TOOLS_DIR / script_name

    if not script_path.exists():
        print(f"\n  ❌ 未找到脚本: {script_name}")
        print(f"  📍 预期路径: {script_path}")
        input("  ⏎ 按 Enter 返回主菜单...")
        return

    print(f"\n  🚀 正在启动: {script_name}")
    print(f"  {'─' * 50}\n")

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(TOOLS_DIR),
        )
        if result.returncode != 0:
            print(f"\n  ⚠️  脚本退出码: {result.returncode}")
    except Exception as e:
        print(f"\n  ❌ 运行脚本时出错: {e}")

    print(f"\n  {script_name} 已结束。")
    input("  ⏎ 按 Enter 返回主菜单...")


def list_projects():
    """列出 F:/owen/hermes/projects/ 下的文件和文件夹"""
    projects_path = PROJECTS_DIR

    if not projects_path.exists():
        print(f"\n  📂 目录不存在: {projects_path}")
        input("  ⏎ 按 Enter 返回主菜单...")
        return

    print(f"\n  📂 已生成文件列表 — {projects_path}")
    print(f"  {'─' * 60}")

    # 按修改时间排序，最新的在前
    items = sorted(
        projects_path.iterdir(),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not items:
        print("  (空目录)")
    else:
        for item in items:
            if item.is_dir():
                print(f"  📁 {item.name}/")
            else:
                size = item.stat().st_size
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size / 1024:.1f} KB"
                else:
                    size_str = f"{size / 1024 / 1024:.1f} MB"
                print(f"  📄 {item.name}  ({size_str})")

    print(f"  {'─' * 60}")
    print(f"  共 {len(items)} 项")
    input("  ⏎ 按 Enter 返回主菜单...")


# ── 主循环 ────────────────────────────────────────────

def main():
    while True:
        print_header()
        choice = show_menu()

        if 1 <= choice <= len(SCRIPTS):
            script_name, _ = SCRIPTS[choice - 1]
            run_script(script_name)
        elif choice == len(SCRIPTS) + 1:
            print_header()
            list_projects()
        elif choice == len(SCRIPTS) + 2:
            print_header()
            print("\n  👋 感谢使用文旅策划工具箱，再见！\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
