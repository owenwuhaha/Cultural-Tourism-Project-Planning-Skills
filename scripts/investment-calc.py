#!/usr/bin/env python3
"""
文旅项目投资测算工具 (V2.0)
============================
文化��游规划项目投资测算工具，支持：

V2.0 新增功能：
  - 三情景预测（乐观/基准/悲观）
  - 5层收入结构模型分析
  - 模块化评估输出（资源/市场/IP/空间/业态/投资）
  - 全时运营参考（四季策略）
  - 政策资金通道匹配建议

用法:
    python investment-calc.py

注意：所有数据为行业经验参考值，实际投资需结合当地实际情况。
"""

import json
import sys
import math
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

# V2.0 新增：不同区域客流量波动系数（用于三情景）
VISITOR_VOLATILITY = {
    "一线城市周边": {"optimistic": 1.30, "base": 1.00, "pessimistic": 0.70},
    "二线城市周边": {"optimistic": 1.25, "base": 1.00, "pessimistic": 0.65},
    "三线城市周边": {"optimistic": 1.20, "base": 1.00, "pessimistic": 0.60},
    "县城/乡镇": {"optimistic": 1.15, "base": 1.00, "pessimistic": 0.50},
}

# V2.0 新增：5层收入结构参考占比
REVENUE_LAYER_RATIOS = {
    "观光型": {"ticket": 0.40, "f&b": 0.25, "secondary": 0.25, "lodging": 0.10},
    "度假型": {"ticket": 0.10, "f&b": 0.25, "secondary": 0.25, "lodging": 0.40},
    "复合型": {"ticket": 0.20, "f&b": 0.25, "secondary": 0.30, "lodging": 0.25},
    "康养型": {"ticket": 0.05, "f&b": 0.30, "secondary": 0.30, "lodging": 0.35},
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


def calc_investment() -> Dict:
    """阶段1: 投资估算"""
    print("\n" + "=" * 55)
    print("  📊 第一阶段：投资估算")
    print("=" * 55)

    area_mu = input_float("规划总面积（亩）: ")
    area_sqm = area_mu * 666.67  # 1亩≈666.67㎡

    grade = select_option("项目档次:", ["经济型", "精品型", "豪华型"])
    project_type = select_option("项目类型:", ["观光型", "度假型", "复合型", "康养型"])

    # V2.0 新增：区域选择（用于三情景）
    region = select_option("项目所在区域:", list(VISITOR_VOLATILITY.keys()))

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
    total_mid = (total_low + total_high) / 2

    print(f"\n{'─' * 50}")
    print(f"  【投资估算结果】[{grade}] [{project_type}] [{region}]")
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
        "build_area": build_area,
        "grade": grade,
        "project_type": project_type,
        "region": region,
        "total_low": total_low,
        "total_high": total_high,
        "total_mid": total_mid,
    }


def calc_revenue(project_info: Dict) -> Dict:
    """阶段2: 收入预测（V2.0 新增三情景输入）"""
    print("\n" + "=" * 55)
    print("  💰 第二阶段：收入预测")
    print("=" * 55)

    project_type = project_info["project_type"]
    spend = PER_CAPITA_SPEND[project_type]

    # 年客流量（基准情景）
    annual_visitors = input_float("预估年客流量（万人次，基准情景）: ") * 10000

    # 门票均价
    if "ticket" in spend:
        ticket_price = input_float("门票均价（元/人，默认按行业参考中值）: ",
                                    default=(spend["ticket"][0] + spend["ticket"][1]) / 2)
    else:
        ticket_price = 0

    # 餐饮
    fb_price = input_float("人均餐饮消费（元，默认按参考中值）: ",
                            default=(spend["f&b"][0] + spend["f&b"][1]) / 2)

    # 二消
    sec_price = input_float("人均二次消费（元，默认按参考中值）: ",
                             default=(spend["secondary"][0] + spend["secondary"][1]) / 2)

    # 住宿
    if "lodging" in spend:
        lodging_price = input_float("人均住宿消费（元/晚，默认按参考中值）: ",
                                     default=(spend["lodging"][0] + spend["lodging"][1]) / 2)
        lodging_nights = input_float("住宿率（入住人次占总客流比例，如0.3表示30%）: ", default=0.30)
    else:
        lodging_price = 0
        lodging_nights = 0

    per_capita = ticket_price + fb_price + sec_price + (lodging_price * lodging_nights)
    annual_revenue = annual_visitors * per_capita
    annual_opex = annual_revenue * OPEX_RATIO
    annual_profit = annual_revenue - annual_opex

    print(f"\n{'─' * 50}")
    print(f"  【收入预测结果（基准情景）】")
    print(f"  预估年客流：{annual_visitors/10000:.1f}万人次")
    print(f"  综合人均消费：{per_capita:.1f}元/人")
    print(f"  ────")
    print(f"  年收入合计：{annual_revenue/10000:.1f}万")
    print(f"  年运营成本（{OPEX_RATIO*100:.0f}%）：{annual_opex/10000:.1f}万")
    print(f"  年净利润：{annual_profit/10000:.1f}万")
    print(f"{'─' * 50}")

    return {
        "annual_visitors": annual_visitors,
        "ticket_price": ticket_price,
        "fb_price": fb_price,
        "sec_price": sec_price,
        "lodging_price": lodging_price,
        "lodging_nights": lodging_nights,
        "per_capita": per_capita,
        "annual_revenue": annual_revenue,
        "annual_opex": annual_opex,
        "annual_profit": annual_profit,
    }


def calc_payback(project_info: Dict, revenue_info: Dict):
    """阶段3: 回收期 + V2.0 三情景预测 + 5层收入分析"""
    print("\n" + "=" * 55)
    print("  ⏱ 第三阶段：回报分析与三情景预测")
    print("=" * 55)

    total_invest = project_info["total_mid"]
    annual_profit = revenue_info["annual_profit"]

    if annual_profit <= 0:
        print("\n  ❌ 净利润为负，项目无法回本。请检查成本或客流数据。")
        return

    # 基准情景回收期
    payback = total_invest / annual_profit

    print(f"\n{'─' * 50}")
    print(f"  【基准情景回收期】")
    print(f"  总投资（中值）：{total_invest/10000:.1f}万")
    print(f"  年净利润：{annual_profit/10000:.1f}万")
    print(f"  ⏱ 静态回收期：{payback:.1f}年")
    print(f"{'─' * 50}")

    # ===== V2.0 新增：三情景预测 =====
    region = project_info["region"]
    volatility = VISITOR_VOLATILITY[region]

    print(f"\n  📈 三情景预测（{region}区域波动系数）：")
    print(f"  {'情景':>8} | {'系数':>6} | {'年客流(万)':>10} | {'年收入(万)':>10} | {'年利润(万)':>10} | {'回收期(年)':>10}")
    print(f"  {'─' * 62}")

    scenarios = [
        ("😄 乐观", volatility["optimistic"]),
        ("😐 基准", volatility["base"]),
        ("😰 悲观", volatility["pessimistic"]),
    ]

    scenario_results = []
    for label, factor in scenarios:
        adj_visitors = revenue_info["annual_visitors"] * factor
        adj_revenue = adj_visitors * revenue_info["per_capita"]
        adj_opex = adj_revenue * OPEX_RATIO
        adj_profit = adj_revenue - adj_opex
        adj_payback = total_invest / adj_profit if adj_profit > 0 else float('inf')

        profit_str = f"{adj_profit/10000:.0f}" if adj_profit > 0 else "亏损"
        payback_str = f"{adj_payback:.1f}" if adj_payback != float('inf') else "∞"

        print(f"  {label:>8} | {factor:>+5.0%} | {adj_visitors/10000:>8.1f} | {adj_revenue/10000:>8.1f} | {profit_str:>10} | {payback_str:>10}")

        scenario_results.append({
            "label": label.strip(),
            "factor": factor,
            "visitors": adj_visitors,
            "revenue": adj_revenue,
            "profit": adj_profit,
            "payback": adj_payback,
        })

    # 风险提示
    pessimistic = scenario_results[2]
    if pessimistic["payback"] != float('inf') and pessimistic["payback"] > 8:
        print(f"\n  ⚠️ 悲观情景回收期达{pessimistic['payback']:.1f}年，风险偏高。建议：")
        print("     - 降低总投资规模")
        print("     - 提升产品差异化降低客流波动")
        print("     - 寻求政策补贴对冲风险")
    elif pessimistic["payback"] == float('inf'):
        print(f"\n  ⚠️ 悲观情景下项目亏损，需重新评估可行性！")

    # ===== V2.0 新增：5层收入结构分析 =====
    project_type = project_info["project_type"]
    layers = REVENUE_LAYER_RATIOS[project_type]

    print(f"\n{'─' * 50}")
    print(f"  🏗 5层收入结构分析（{project_type}类型参考）")
    print(f"{'─' * 50}")

    base_revenue = revenue_info["annual_revenue"]
    ticket_ratio = layers["ticket"]
    fb_ratio = layers["f&b"]
    sec_ratio = layers["secondary"]
    lodging_ratio = layers["lodging"]

    print(f"  {'层级':>14} | {'年收入(万)':>10} | {'占比':>6} | {'建议占比':>8}")
    print(f"  {'─' * 44}")
    print(f"  第1层 流量收入(广告/补贴) | {base_revenue/10000*ticket_ratio*0.3:>8.1f} | {ticket_ratio*0.3*100:>5.0f}% | 10-15%")
    print(f"  第2层 基础收入(门票)       | {base_revenue/10000*ticket_ratio*0.7:>8.1f} | {ticket_ratio*0.7*100:>5.0f}% | 30-40%")
    print(f"  第3层 增值收入(餐饮/体验)  | {base_revenue/10000*(fb_ratio+sec_ratio):>8.1f} | {(fb_ratio+sec_ratio)*100:>5.0f}% | 25-30%")
    print(f"  第4层 延伸收入(住宿/课程)  | {base_revenue/10000*lodging_ratio:>8.1f} | {lodging_ratio*100:>5.0f}% | 15-20%")
    print(f"  第5层 被动收入(IP/授权)    | {base_revenue/10000*0.10:>8.1f} | {'10':>5}% | 10-15%")

    # 健康度检查
    print(f"\n  【收入结构健康度检查】")
    ticket_layer_ratio = ticket_ratio * 0.7  # 门票部分
    ticket_ok = ticket_layer_ratio < 0.30
    composite_ok = (fb_ratio + sec_ratio + lodging_ratio) > 0.50
    print(f"  ✅ 门票占比{ticket_layer_ratio*100:.0f}% {'<30% ✓' if ticket_ok else '>30% ✗ 建议提升二消占比'}")
    print(f"  {'✅' if composite_ok else '❌'} 综合消费占比{(fb_ratio+sec_ratio+lodging_ratio)*100:.0f}% {'>50% ✓' if composite_ok else '<50% ✗ 建议增加住宿/体验产品'}")

    # ===== 敏感性分析 =====
    print(f"\n{'─' * 50}")
    print(f"  📊 敏感性分析（客流量变化对回收期的影响）：")
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

    # V2.0 新增：淡旺季客单价对比
    print(f"\n{'─' * 50}")
    print(f"  🗓 淡旺季运营参考")
    print(f"{'─' * 50}")
    peak_price = revenue_info["per_capita"] * 1.2
    off_price = revenue_info["per_capita"] * 0.7
    print(f"  旺季（节假日）：人均消费约 {peak_price:.0f} 元（基准+20%）")
    print(f"  淡季（工作日）：人均消费约 {off_price:.0f} 元（基准-30%）")
    print(f"  建议：工作日针对银发/自由职业者推出特惠套餐")
    print(f"  建议：提前预售锁定淡季客流")

    return scenario_results


def show_risk_notes():
    """风险提示"""
    print(f"\n{'=' * 55}")
    print("  ⚠️ 风险提示与免责声明")
    print("=" * 55)
    print("""
  1. 以上数据基于行业经验参考值，实际投资需结合以下因素：
     - 当地建材价格、人工成本（地区差异可达30-50%）
     - 土地成本（差异极大，需单独核算）
     - 政策补贴和税收优惠

  2. 客流量预测是最大变量，三情景已给出乐观/基准/悲观参考
     - 建议以悲观情景作为投资决策底线

  3. 后期运营能力决定实际收入
     - 初期运营成本可能高于40%（新项目通常为50-60%）

  4. 合规红线必查（V2.0 新增检查清单）：
     □ 是否涉及永久基本农田
     □ 是否在生态保护红线内
     □ 是否涉及自然保护区
     □ 是否涉及文物保护单位
     □ 是否涉及林地使用指标

  5. V2.0 新增政策资金参考：
     - 乡村振兴补助：1062亿元（2026提前下达）
     - 地方专项债：4.4万亿（收益覆盖≥1.3倍）
     - 超长期特别国债：1.3万亿（20-50年期限）
     - 现代农业产业园：7000万-1亿/个

  ⚠️ 本工具仅供初步测算参考，不构成投资建议。
     正式决策请委托专业机构完成可行性研究。
""")


def show_module_checklist():
    """V2.0 新增：模块化评估清单"""
    print("\n" + "=" * 55)
    print("  📋 模块化评估清单（V2.0）")
    print("=" * 55)
    print("""
  在完成投资测算后，建议按以下模块依次评估：

  【模块1】资源禀赋评估
    - 自然资源（山水林田湖）评级
    - 人文资源（历史/非遗/建筑）评级
    - 区位交通评级

  【模块2】市场与客群分析
    - 客源地圈层分析（1h/2h/3h）
    - 目标客群画像匹配
    - 十大趋势赛道契合度

  【模块3】主题定位与IP策划
    - 品牌Slogan体系（主Slogan+二级传播语）
    - 在地文化IP激活方案
    - 差异化竞争力陈述

  【模块4】空间布局与动线规划
    - 功能分区比例
    - 承载力估算
    - 全时运营策略（春夏秋冬）

  【模块5】业态策划与产品矩阵
    - 轻资产爆款组合
    - 沉浸式体验四业态评估
    - 夜经济方案

  【模块6】商业模式设计
    - 5层收入结构健康度
    - 全生命周期盈利策略
    - 盈利模型验证

  【模块7】投资测算（本工具）
    - ✅ 已完成
""")


def main():
    print("""
╔═══════════════════════════════════════════════╗
║    文旅项目投资测算工具 v2.0                  ║
║    Cultural Tourism Investment Calc V2.0      ║
║                                               ║
║    新增：三情景预测 | 5层收入模型 | 模块评估     ║
╚═══════════════════════════════════════════════╝
    """)

    print("本工具将引导您完成3个测算阶段：")
    print("  阶段1: 📊 投资估算（基于面积和档次）")
    print("  阶段2: 💰 收入预测（基于客流量和消费）")
    print("  阶段3: ⏱ 三情景预测 + 5层收入 + 敏感性分析")
    print("  (输入过程中可按 Ctrl+C 随时退出)")
    print("  (V2.0 新增：三情景预测基于区域波动系数)")

    try:
        project_info = calc_investment()
        revenue_info = calc_revenue(project_info)
        calc_payback(project_info, revenue_info)
        show_module_checklist()
        show_risk_notes()

        save = input("\n是否保存测算结果到文件？(y/n): ")
        if save.lower() == 'y':
            workload = {
                "项目信息": {
                    "面积": f"{project_info['area_mu']:.1f}亩",
                    "档次": project_info['grade'],
                    "类型": project_info['project_type'],
                    "区域": project_info['region'],
                    "总投资范围": f"{project_info['total_low']/10000:.1f}万 ~ {project_info['total_high']/10000:.1f}万",
                    "总投资中值": f"{project_info['total_mid']/10000:.1f}万",
                },
                "收入预测（基准情景）": {
                    "年客流": f"{revenue_info['annual_visitors']/10000:.1f}万人次",
                    "人均消费": f"{revenue_info['per_capita']:.1f}元",
                    "年收入": f"{revenue_info['annual_revenue']/10000:.1f}万",
                    "年运营成本": f"{revenue_info['annual_opex']/10000:.1f}万",
                    "年净利润": f"{revenue_info['annual_profit']/10000:.1f}万",
                },
                "工具版本": "V2.0",
                "三情景预测说明": "详细三情景对比已在终端输出，建议复制保存",
            }
            filename = f"文旅测算报告_{project_info['area_mu']:.0f}亩_{project_info['grade']}_v2.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(workload, f, ensure_ascii=False, indent=2)
            print(f"  ✅ 已保存到 {filename}")
        else:
            print("  测算完成，未保存。")

    except KeyboardInterrupt:
        print("\n\n⏹ 已退出测算工具。")
        sys.exit(0)


if __name__ == "__main__":
    main()
