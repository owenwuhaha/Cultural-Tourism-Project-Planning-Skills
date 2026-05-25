#!/usr/bin/env python3
"""
文旅项目投资测算工具
========================
用法:
    python investment-calc.py

交互式问答界面，输入项目基本参数，
自动输出投资估算、收入预测、回收期分析及敏感性分析。

注意：所有数据为行业经验参考值，实际投资需结合当地实际情况。
"""

import json
import sys
from typing import Dict, List, Tuple


# ========== 行业参考数据 ==========

# 不同档次的单方造价参考（元/㎡）
COST_PER_SQM = {
    "经济型": {"building": (1500, 2500), "landscape": (200, 500), "soft": (500, 1000)},
    "精品型": {"building": (3000, 4500), "landscape": (500, 800), "soft": (1000, 2000)},
    "豪华型": {"building": (5000, 8000), "landscape": (800, 1500), "soft": (2000, 4000)},
}

# 不同项目类型的人均消费参考（元）
PER_CAPITA_SPEND = {
    "观光型": {"ticket": (30, 80), "f&b": (30, 60), "secondary": (20, 50)},
    "度假型": {"ticket": (0, 80), "f&b": (80, 200), "secondary": (50, 150), "lodging": (300, 800)},
    "复合型": {"ticket": (30, 120), "f&b": (50, 100), "secondary": (50, 150), "lodging": (200, 600)},
    "康养型": {"ticket": (0, 50), "f&b": (100, 200), "secondary": (100, 300), "lodging": (400, 1200)},
}

# 运营成本占收入比例参考
OPEX_RATIO = 0.40  # 40-50%

# 建设面积比例（建设面积/总面积）
BUILD_AREA_RATIO = 0.15  # 通常开发建设面积不超过总面积的15-20%


def input_float(prompt: str, default: float = None) -> float:
    """带默认值的数字输入"""
    while True:
        try:
            raw = input(prompt)
            if not raw.strip() and default is not None:
                return default
            return float(raw.strip())
        except ValueError:
            print("❌ 请输入有效数字（如 200、1500万需输入1500）")


def select_option(prompt: str, options: List[str]) -> str:
    """选项选择"""
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        try:
            choice = int(input("请选择编号: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print(f"请选择 1-{len(options)}")
        except ValueError:
            print("请输入数字")


def calc_investment():
    """阶段1: 投资估算"""
    print("\n" + "=" * 55)
    print("  📊 第一阶段：投资估算")
    print("=" * 55)

    area_mu = input_float("规划总面积（亩）: ")
    area_sqm = area_mu * 666.67  # 1亩≈666.67㎡

    grade = select_option("项目档次:", ["经济型", "精品型", "豪华型"])
    project_type = select_option("项目类型:", ["观光型", "度假型", "复合型", "康养型"])

    cost = COST_PER_SQM[grade]
    build_area = area_sqm * BUILD_AREA_RATIO

    # 建安成本
    building_low = build_area * cost["building"][0]
    building_high = build_area * cost["building"][1]

    # 景观成本
    landscape_low = area_sqm * cost["landscape"][0]
    landscape_high = area_sqm * cost["landscape"][1]

    # 软装/设备
    soft_low = build_area * cost["soft"][0]
    soft_high = build_area * cost["soft"][1]

    # 设计费（约3-5%）
    design_low = (building_low + landscape_low) * 0.03
    design_high = (building_high + landscape_high) * 0.05

    # 预备金（10%）
    reserve_low = (building_low + landscape_low + soft_low + design_low) * 0.10
    reserve_high = (building_high + landscape_high + soft_high + design_high) * 0.10

    total_low = building_low + landscape_low + soft_low + design_low + reserve_low
    total_high = building_high + landscape_high + soft_high + design_high + reserve_high

    print(f"\n{'─' * 50}")
    print(f"  【投资估算结果】[{grade}] [{project_type}]")
    print(f"  总面积：{area_mu:.1f}亩（{area_sqm:.0f}㎡）")
    print(f"  建设面积（{BUILD_AREA_RATIO*100:.0f}%）：{build_area:.0f}㎡")
    print(f"{'─' * 50}")
    print(f"  建安工程：{building_low/10000:.1f}万 ~ {building_high/10000:.1f}万")
    print(f"  景观工程：{landscape_low/10000:.1f}万 ~ {landscape_high/10000:.1f}万")
    print(f"  软装设备：{soft_low/10000:.1f}万 ~ {soft_high/10000:.1f}万")
    print(f"  设计费用：{design_low/10000:.1f}万 ~ {design_high/10000:.1f}万")
    print(f"  预备金  ：{reserve_low/10000:.1f}万 ~ {reserve_high/10000:.1f}万")
    print(f"{'─' * 50}")
    print(f"  💰 总投资估算：{total_low/10000:.1f}万 ~ {total_high/10000:.1f}万")
    print(f"  单方造价：{total_low/build_area:.0f} ~ {total_high/build_area:.0f} 元/建设㎡")
    print(f"{'─' * 50}")

    return {
        "area_mu": area_mu,
        "area_sqm": area_sqm,
        "grade": grade,
        "project_type": project_type,
        "total_low": total_low,
        "total_high": total_high,
        "total_mid": (total_low + total_high) / 2,
    }


def calc_revenue(project_info: Dict):
    """阶段2: 收入预测"""
    print("\n" + "=" * 55)
    print("  💰 第二阶段：收入预测")
    print("=" * 55)

    project_type = project_info["project_type"]
    spend = PER_CAPITA_SPEND[project_type]

    # 年客流量
    annual_visitors = input_float("预估年客流量（万人次）: ") * 10000

    # 门票均价
    if "ticket" in spend:
        ticket_price = input_float("门票均价（元/人，默认按行业参考中值）: ", default=(spend["ticket"][0] + spend["ticket"][1]) / 2)
    else:
        ticket_price = 0

    # 餐饮
    fb_price = input_float("人均餐饮消费（元，默认按参考中值）: ", default=(spend["f&b"][0] + spend["f&b"][1]) / 2)

    # 二消
    sec_price = input_float("人均二次消费（元，默认按参考中值）: ", default=(spend["secondary"][0] + spend["secondary"][1]) / 2)

    # 住宿
    if "lodging" in spend:
        lodging_price = input_float("人均住宿消费（元/晚，默认按参考中值）: ", default=(spend["lodging"][0] + spend["lodging"][1]) / 2)
        lodging_nights = input_float("住宿率（入住人次占总客流比例，如0.3表示30%）: ", default=0.30)
    else:
        lodging_price = 0
        lodging_nights = 0

    per_capita = ticket_price + fb_price + sec_price + (lodging_price * lodging_nights)
    annual_revenue = annual_visitors * per_capita
    annual_opex = annual_revenue * OPEX_RATIO
    annual_profit = annual_revenue - annual_opex

    print(f"\n{'─' * 50}")
    print(f"  【收入预测结果】")
    print(f"  预估年客流：{annual_visitors/10000:.1f}万人次")
    print(f"  综合人均消费：{per_capita:.1f}元/人")
    print(f"  ────")
    print(f"  年收入合计：{annual_revenue/10000:.1f}万")
    print(f"  年运营成本（{OPEX_RATIO*100:.0f}%）：{annual_opex/10000:.1f}万")
    print(f"  年净利润：{annual_profit/10000:.1f}万")
    print(f"{'─' * 50}")

    return {
        "annual_visitors": annual_visitors,
        "per_capita": per_capita,
        "annual_revenue": annual_revenue,
        "annual_opex": annual_opex,
        "annual_profit": annual_profit,
    }


def calc_payback(project_info: Dict, revenue_info: Dict):
    """阶段3: 回收期及敏感性分析"""
    print("\n" + "=" * 55)
    print("  ⏱ 第三阶段：回收期与敏感性分析")
    print("=" * 55)

    total_invest = project_info["total_mid"]
    annual_profit = revenue_info["annual_profit"]

    if annual_profit <= 0:
        print("\n  ❌ 净利润为负，项目无法回本。请检查成本或客流数据。")
        return

    payback = total_invest / annual_profit

    print(f"\n{'─' * 50}")
    print(f"  【回收期计算】")
    print(f"  总投资（中值）：{total_invest/10000:.1f}万")
    print(f"  年净利润：{annual_profit/10000:.1f}万")
    print(f"  ⏱ 静态回收期：{payback:.1f}年")
    print(f"{'─' * 50}")

    # 敏感性分析
    print(f"\n  📈 敏感性分析（客流量变化对回收期的影响）：")
    print(f"  {'客流变化':>10} | {'年客流(万)':>10} | {'年利润(万)':>10} | {'回收期(年)':>10}")
    print(f"  {'─' * 46}")
    for change in [-0.30, -0.20, -0.10, 0, 0.10, 0.20, 0.30]:
        adj_visitors = revenue_info["annual_visitors"] * (1 + change)
        adj_revenue = adj_visitors * revenue_info["per_capita"]
        adj_profit = adj_revenue * (1 - OPEX_RATIO)
        adj_payback = total_invest / adj_profit if adj_profit > 0 else float('inf')
        profit_label = f"{adj_profit/10000:.0f}" if adj_profit > 0 else "亏损"
        payback_label = f"{adj_payback:.1f}" if adj_payback != float('inf') else "∞"
        print(f"  {change*100:>+8.0f}% | {adj_visitors/10000:>8.1f} | {profit_label:>10} | {payback_label:>10}")


def show_risk_notes():
    """风险提示"""
    print(f"\n{'=' * 55}")
    print("  ⚠️ 风险提示与免责声明")
    print("=" * 55)
    print("""
  1. 以上数据基于行业经验参考值，实际投资需��合以下因素：
     - 当地建材价格、人工成本（地区差异可达30-50%）
     - 土地成本（差异极大，需单独核算）
     - 政策补贴和税收优惠

  2. 客流量预测是最大变量，建议采用保守估计值
     - 建议按乐观/基准/悲观三种场景分别测算

  3. 后期运营能力决定实际收入
     - 初期运营成本可能高于40%（新项目通常为50-60%）

  4. 合规红线必查：
     □ 是否涉及永久基本农田
     □ 是否在生态保护红线内
     □ 是否涉及自然保护区
     □ 是否涉及文物保护单位
     □ 是否涉及林地使用指标

  ⚠️ 本工具仅供初步测算参考，不构成投资建议。
     正式决策请委托专业机构完成可行性研究。
""")


def main():
    print("""
╔═══════════════════════════════════════════╗
║       文旅项目投资测算工具 v1.0           ║
║      Cultural Tourism Investment Calc     ║
╚═══════════════════════════════════════════╝
    """)

    print("本工具将引导您完成3个测算阶段：")
    print("  阶段1: 📊 投资估算（基于面积和档次）")
    print("  阶段2: 💰 收入预测（基于客流量��消费）")
    print("  阶段3: ⏱ 回收期+敏感性分析")
    print("  (输入过程中可按 Ctrl+C 随时退出)")

    try:
        project_info = calc_investment()
        revenue_info = calc_revenue(project_info)
        calc_payback(project_info, revenue_info)
        show_risk_notes()

        save = input("\n是否保存测算结果到文件？(y/n): ")
        if save.lower() == 'y':
            filename = f"文旅测算报告_{project_info['area_mu']:.0f}亩_{project_info['grade']}.json"
            output = {
                "项目信息": {
                    "面积": f"{project_info['area_mu']:.1f}亩",
                    "档次": project_info['grade'],
                    "类型": project_info['project_type'],
                    "总投资范围": f"{project_info['total_low']/10000:.1f}万 ~ {project_info['total_high']/10000:.1f}万",
                },
                "收入预测": {
                    "年客流": f"{revenue_info['annual_visitors']/10000:.1f}万人次",
                    "人均消��": f"{revenue_info['per_capita']:.1f}元",
                    "年收入": f"{revenue_info['annual_revenue']/10000:.1f}万",
                    "年净利润": f"{revenue_info['annual_profit']/10000:.1f}万",
                },
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print(f"  ✅ 已保存到 {filename}")
        else:
            print("  测算完成，未保存。")

    except KeyboardInterrupt:
        print("\n\n⏹ 已退出测算工具。")
        sys.exit(0)


if __name__ == "__main__":
    main()
