#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文旅项目自动策划脚本 V2.1
Auto Plan Generator — Cultural Tourism Project Planner
=======================================================

功能说明：
  1. 交互式输入项目参数（地点、面积、地形、类型、客群、预算等）
  2. 自动生成完整八大模块 Markdown 策划方案
  3. 集成 V2.0 知识库数据（十大趋势、康养、5层收入、全时运营等）
  4. 保存到 F:/owen/hermes/projects/ 并同时终端预览

用法：
  python generate-plan.py        # 交互模式
  python generate-plan.py --demo # 演示模式（自动填充示例数据）

依赖：Python 3.7+ (标准库, 无需第三方包)
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# ===== 常量与参考数据 =====

VERSION = "2.1"

OUTPUT_DIR = os.path.expandvars(r"F:\owen\hermes\projects")

PROJECT_TYPES = ["观光型", "度假型", "复合型", "康养型"]
TERRAIN_TYPES = ["平坡地", "阶梯台地", "山地坡地", "滨水滩涂", "混合地形"]
GUEST_TYPES = {
    "Z世代(18-28)": {"price_range": "100-300元", "keywords": "出片、社交、夜经济、国潮", "products": "剧本杀、露营、文创市集"},
    "亲子家庭(30-40)": {"price_range": "200-500元", "keywords": "安全、教育、互动、不累", "products": "无动力乐园、萌宠、研学"},
    "银发康养(55-70)": {"price_range": "150-400元", "keywords": "养生、慢节奏、性价比", "products": "康养民宿、太极拳、农耕体验"},
    "企业团建(25-45)": {"price_range": "300-800元", "keywords": "团队协作、放松、带酒", "products": "户外拓展、篝火晚会、轰趴"},
    "她旅游(25-50女性)": {"price_range": "300-800元", "keywords": "疗愈、美学、仪式感", "products": "旅拍、下午茶、手作体验"},
}
LAND_TYPES = ["集体建设用地", "宅基地", "商业用地", "一般耕地", "未利用地", "混合/不确定"]
PROJECT_MODES = ["新建", "改造提升", "新建+改造混合"]
GRADES = ["经济型", "精品型", "豪华型"]

TREND_TRACKS = [
    ("情绪经济×文旅", "60亿人次情绪逃亡潮"),
    ("银发经济×文旅", "旅居养老万亿市场"),
    ("Z世代×文旅", "个性化/小众/沉浸式"),
    ("她旅游×文旅", "4亿女性撬动10万亿"),
    ("数字文旅×AI", "AI导游/数字孪生"),
    ("低空旅游", "万亿蓝海"),
    ("小而美业态", "村咖300+家=121亿产业"),
    ("夜间经济", "轻资产不夜城"),
    ("研学旅行", "行业标准发布(2025)"),
    ("体育+文旅", "49个户外运动目的地"),
]

FIVE_LAYERS = [
    ("第5层 被动收入", "品牌授权/IP输出/管理输出/数据资产", "80-95%"),
    ("第4层 延伸收入", "文创/课程/内容付费/社群会员", "60-80%"),
    ("第3层 增值收入", "特色餐饮/住宿升级/深度体验/定制服务", "50-70%"),
    ("第2层 基础收入", "门票/停车/基础餐饮/基础住宿", "40-60%"),
    ("第1层 流量收入", "广告/冠名/补贴/招商", "60-90%"),
]

SEASONS = [
    ("春", "花海/采茶/踏青", "赏花节、采茶体验、春游研学"),
    ("夏", "避暑/水上/夜游", "水乐园、漂流、露营夜宿"),
    ("秋", "丰收/观叶/采摘", "果蔬采摘、红叶观赏、丰收节"),
    ("冬", "温泉/年俗/室内", "温泉SPA、年货节、室内场馆"),
]

NIGHT_ECONOMY = [
    ("🌃 夜景", "灯光秀、夜光步道、树上星河"),
    ("🎭 夜演", "实景演艺、篝火晚会、街头艺人"),
    ("🚣 夜游", "游船夜航、夜间漂流"),
    ("🍢 夜市", "美食街、文创市集"),
    ("🏡 夜宿", "帐篷露营、星空民宿"),
]

POLICY_FUNDS = [
    ("乡村振兴补助", "1062亿元(2026提前下达)"),
    ("现代农业产业园", "7000万-1亿/个"),
    ("产业强镇", "500-3000万/个"),
    ("地方专项债", "4.4万亿"),
    ("超长期特别国债", "1.3万亿"),
]

# ===== 交互输入 =====

def input_str(prompt: str, default: str = "") -> str:
    val = input(prompt).strip()
    return val if val else default

def input_float(prompt: str, default: Optional[float] = None) -> float:
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            return float(raw)
        except ValueError:
            print("❌ 请输入有效数字")

def select_option(prompt: str, options: List[str], default_idx: int = 0) -> str:
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
            print(f"请输入 1-{len(options)}")
        except ValueError:
            print("请输入数字")

def select_multi(prompt: str, options: List[str]) -> List[str]:
    print(f"\n{prompt} (可多选，用逗号分隔，如 1,3,5)")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        raw = input("请选择编号: ").strip()
        if not raw:
            return [options[0]]
        try:
            indices = [int(x.strip()) for x in raw.split(",")]
            return [options[i-1] for i in indices if 1 <= i <= len(options)]
        except (ValueError, IndexError):
            print("请输入有效编号，用逗号分隔")

def get_project_info() -> Dict:
    """交互式输入项目信息"""
    print(f"\n{'=' * 55}")
    print(f"  文旅项目自动策划工具 V{VERSION}")
    print(f"  {'=' * 55}")
    print("\n请输入项目基本信息：")

    info = {
        "project_name": input_str("📛 项目名称（如：龙隐山谷）: ", "示例项目"),
        "location": input_str("📍 项目地点（如：四川省成都市都江堰）: ", "示例地点"),
        "area_mu": input_float("📐 规划总面积（亩）: ", 200),
        "terrain": select_option("🏔 地形类型:", TERRAIN_TYPES),
        "project_type": select_option("🎯 项目类型:", PROJECT_TYPES),
        "guests": select_multi("👥 目标客群:", list(GUEST_TYPES.keys())),
        "budget": select_option("💰 预算等级:", GRADES),
        "mode": select_option("🏗 新建还是改造:", PROJECT_MODES),
        "land_type": select_option("🧱 用地性质:", LAND_TYPES),
        "daily_visitors": input_float("📊 预期日均客流（人）: ", 2000),
    }

    # 自动计算年客流
    days_open = 320 if info["project_type"] != "观光型" else 365
    info["annual_visitors"] = int(info["daily_visitors"] * days_open)
    info["area_sqm"] = info["area_mu"] * 666.67
    return info

# ===== 模块生成 =====

def gen_module1(info: Dict) -> str:
    """模块1: 资源禀赋评估"""
    terrain_map = {
        "平坡地": "地势平坦，开发建设成本低，适合大规模布局",
        "阶梯台地": "层次丰富，视野多变，适合立体化景观设计",
        "山地坡地": "自然落差大，景观层次丰富，但建设成本高",
        "滨水滩涂": "水资源丰富，水景观优势突出，需注意防洪",
        "混合地形": "变化丰富，可分区利用不同地形优势",
    }
    terrain_desc = terrain_map.get(info["terrain"], "地形多样")

    # SWOT 模板
    s_list = ["自然资源禀赋突出（山水林田湖）", f"交通区位优势明显（{info['location']}）",
              f"地形类型为{info['terrain']}，开发基础良好"]
    w_list = ["基础设施有待完善", "品牌知名度尚需培育"]
    o_list = ["文旅融合政策持续利好", "周边游/微度假需求增长",
              "银发经济/研学旅行等细分市场崛起"]
    t_list = ["同类项目竞争加剧", "生态保护与开发平衡压力"]

    if info["project_type"] == "康养型":
        s_list.append("生态环境优良，适合康养疗愈")
        o_list.append("康养市场规模达10万亿元，政策红利持续释放")
    if "她旅游" in str(info["guests"]):
        s_list.append("女性消费市场潜力巨大，美学场景基础好")

    swot = f"""### 1.1 五维资源分类

| 资源维度 | 内容描述 | 评级 |
|---------|---------|------|
| 自然资源 | {terrain_desc}，总面积{info['area_mu']:.0f}亩（{info['area_sqm']:.0f}㎡） | ⭐⭐⭐⭐ |
| 区位交通 | 位于{info['location']}，可达性良好 | ⭐⭐⭐⭐ |
| 人文资源 | 需进一步调研当地历史/非遗/民俗资源 | ⭐⭐⭐ |
| 产业资源 | {'已有一定农��/文旅产业基础' if info['mode']=='改造提升' else '待开发阶段'} | ⭐⭐⭐ |
| 政策背景 | 处于文旅/乡村振兴政策覆盖范围（需确认当地细则） | ⭐⭐⭐⭐ |

### 1.2 SWOT 分析矩阵

| 优势(S) | 劣势(W) |
|---------|---------|
| {'；'.join(s_list[:3])} | {'；'.join(w_list)} |
| **机会(O)** | **威胁(T)** |
| {'；'.join(o_list[:3])} | {'；'.join(t_list[:2])} |

### 1.3 资源稀缺性评分

| 评估维度 | 得分(1-5) | 说明 |
|---------|----------|------|
| 资源独特性 | ★★★★☆ | 具备一定的差异化资源条件 |
| 可替代性 | ★★★☆☆ | 区域内有同类项目竞争 |
| 开发难度 | ★★★☆☆ | {info['terrain']}开发成本中等 |
| 市场匹配度 | ★★★★☆ | 目标客群与资源类型匹配度良好 |
"""
    return swot

def gen_module2(info: Dict) -> str:
    """模块2: 市场与客群分析"""
    guests_table = "| 客群类型 | 核心需求 | 典型产品偏好 | 客单价范围 |\n|----------|---------|-------------|-----------|\n"
    for g in info["guests"]:
        if g in GUEST_TYPES:
            d = GUEST_TYPES[g]
            guests_table += f"| {g} | {d['keywords']} | {d['products']} | {d['price_range']} |\n"

    # 趋势匹配
    trend_match = ["| 趋势赛道 | 项目契合度 | 说明 |\n|---------|-----------|------|\n"]
    for name, desc in TREND_TRACKS[:6]:
        score = "⭐⭐⭐⭐⭐" if info["project_type"] == "康养型" and "银发" in name else "⭐⭐⭐⭐"
        trend_match.append(f"| {name} | {score} | {desc} |\n")

    return f"""### 2.1 客源圈层分析

| 圈层 | 距离 | 交通时间 | 客源覆盖目标 | 策略 |
|------|------|---------|-------------|------|
| 核心圈 | 0-50km | 1h内 | 60% | 高频次、轻决策、周末游 |
| 辐射圈 | 50-150km | 1-2h | 25% | 周末/小长假、深度体验 |
| 拓展圈 | 150-300km | 2-3h | 15% | 长假/过夜、强IP吸引 |

### 2.2 目标客群画像

{guests_table}

### 2.3 市场趋势匹配度

{' '.join(trend_match)}

**匹配结论：** 项目契合{'、'.join([t[0] for t in TREND_TRACKS[:3]])}等趋势方向，市场前景良好。
"""

def gen_module3(info: Dict) -> str:
    """模块3: 主题定位与IP策划"""
    themes = []
    if "康养" in info["project_type"]:
        themes.append(f"""### 主题方向1：疗愈山谷 · 身心栖息地
- **核心客群：** 银发康养+她旅游
- **视觉符号：** 竹林、石径、温泉雾气、禅意空间
- **品牌Slogan：** 「{info['location']} · 给自己三天慢生活」
- **二级传播语：** 「离城市[XX]公里，藏了一个能���愈焦虑的疗愈山谷」
- **爆款产品：** 森林冥想、温泉SPA、音钵疗愈、慢病调理""")
        themes.append(f"""### 主题方向2：田园诗·亲子野趣
- **核心客群：** 亲子家庭+企业团建
- **视觉符号：** 稻田、花海、木屋、风车
- **品牌Slogan：** 「把童年还给自然」
- **二级传播语：** 「在{info['location']}，爸妈和孩子一起找回童年的田埂」
- **爆款产品：** 萌宠互动、无动力乐园、农耕体验""")
    else:
        themes.append(f"""### 主题方向1：{info['location']} · {info['project_type'][:2]}秘境
- **核心客群：** {'/'.join(info['guests'][:2])}
- **视觉符号：** 山水、古建、灯笼、烟火
- **品牌Slogan：** 「{info['location']} · 不负好时光」
- **二级传播语：** 「{info['location']}出发1h，邂逅一个会呼吸的{info['project_type'][:2]}天堂」
- **爆款产品：** 沉浸式夜游、文创市集、特色民宿""")
        themes.append(f"""### 主题方向2：国潮新生 · 文化沉浸
- **核心客群：** Z世代+她旅游
- **视觉符号：** 国风服饰、传统纹样、现代装置
- **品牌Slogan：** 「当{info['location']}遇见国潮」
- **爆款产品：** 剧本杀+实景、非遗工坊、国风旅拍""")

    return f"""### 3.1 地缘文化解构

{info['location']}地处{info['terrain']}区域，核心文化关键词可围绕**生态自然、在地民俗、康养疗愈**展开。

### 3.2 备选主题方向

{chr(10).join(themes)}

### 3.3 IP激活方案

| IP层次 | 设计内容 | 实施载体 |
|--------|---------|---------|
| 符号层 | 视觉标识+吉祥物+品牌色彩 | 入口标识、门票、导览系统 |
| 内容层 | 在地故事+传说挖掘 | 文化展示馆、导游词、宣传片 |
| 体验层 | 可参与体验活动 | 工坊、课程、演艺互动 |
| 系统层 | 产品+运营体系 | 会员体系、衍生品、品牌加盟 |
"""

def gen_module4(info: Dict) -> str:
    """模块4: 空间布局与动线规划"""
    layout_map = {
        "平坡地": "环状布局、网格状布局",
        "阶梯台地": "组团式布局、串珠状布局",
        "山地坡地": "组团式布局、散点式布局",
        "滨水滩涂": "带状布局、一衣带水布局",
        "混合地形": "分区差异化布局",
    }
    layout = layout_map.get(info["terrain"], "分区布局")

    capacity = int(info["daily_visitors"] * 2.5)
    parking = max(50, int(info["daily_visitors"] * 0.05 / 2))

    return f"""### 4.1 推荐布局模式

基于{info['terrain']}地形，推荐采用 **{layout}**。

| 功能分区 | 建议占比 | 核心功能 | 主要设施 |
|---------|---------|---------|---------|
| 入口服务区 | 5% | 接待、停车、票务 | 游客中心、停车场、售票处 |
| 核心吸引区 | 20% | 主题广场、演艺、地标 | 演艺剧场、主广场、打卡点 |
| 休闲消费区 | 30% | 餐饮、文创、体验 | 美食街、文创店、手作坊 |
| 住宿配套区 | 25% | 民宿、露营、酒店 | 精品民宿、露营地、树屋 |
| 生态保育区 | 20% | 游览步道、观景 | 环山步道、观景平台 |

### 4.2 游客动线规划

**半日游动线（约3-4h）：**
入口 → 观景平台（拍照15min）→ 核心广场（体验30min）→ 餐饮街（午餐1h）
→ 文创市集（逛30min）→ 体验工坊（活动45min）→ 出口

**一日游动线（约6-8h）：**
入口 → 核心吸引区（活动1h）→ 餐饮街（午餐1h）→ 休闲消费区（逛+体验2h）
→ 住宿区入住 → 夜游/夜演（2h）→ 夜市（1h）

### 4.3 承载力估算

| 指标 | 估算值 | 计算依据 |
|------|-------|---------|
| 瞬时最大承载量 | {info['daily_visitors']:.0f}人 | 核心区面积×人均占地 |
| 日合理承载量 | {capacity}人 | 瞬时的2.5倍 |
| 建议停车位 | {parking}个 | 按{info['daily_visitors']:.0f}人×5%自驾比例÷2周转率 |
| 餐饮接待 | {int(info['daily_visitors']*0.6)}人/餐 | 按60%游客用餐 |
"""

def gen_module5(info: Dict) -> str:
    """模块5: 业态策划与产品矩阵"""
    ratio_map = {
        "观光型": ("40%", "25%", "10%", "25%"),
        "度假型": ("10%", "25%", "40%", "25%"),
        "复合型": ("20%", "25%", "25%", "30%"),
        "康养型": ("5%", "30%", "35%", "30%"),
    }
    ratios = ratio_map.get(info["project_type"], ("20%", "25%", "25%", "30%"))

    night = "\n".join([f"- {e[0]}：{e[1]}" for e in NIGHT_ECONOMY])
    seasons = "\n".join([f"- **{s[0]}**：{s[2]}" for s in SEASONS])

    return f"""### 5.1 业态配比

| 类型 | 门票占比 | 餐饮占比 | 住宿占比 | 二销占比 |
|------|---------|---------|---------|---------|
| {info['project_type']} | {ratios[0]} | {ratios[1]} | {ratios[2]} | {ratios[3]} |

### 5.2 轻资产爆款推荐
- 🏕️ 露营地（50-100万，20-50营位）
- 🐰 萌宠乐园（80-200万，500-2000㎡）
- 🎠 无动力乐园（100-500万）
- 📸 旅拍基地（10-50万，极轻资产）
- 🎭 剧本杀+沉浸式（30-100万）

### 5.3 沉浸式体验四业态
- 沉浸式演艺（实景剧/光影秀）
- 沉浸式夜游（夜光步道/游船）
- 沉浸式研学（自然课堂/非遗工坊）
- 沉浸式消费空间（主题餐饮/文创市集）

### 5.4 夜经济方案

{night}

### 5.5 全时运营策略（四季）

{seasons}
"""

def gen_module6(info: Dict) -> str:
    """模块6: 投资测算与风险评估"""
    cost_map = {
        "经济型": (2000, 350),
        "精品型": (3750, 650),
        "豪华型": (6500, 1150),
    }
    costs = cost_map.get(info["budget"], (3750, 650))
    build_ratio = 0.15
    build_area = info["area_sqm"] * build_ratio

    # 投资估算
    building = build_area * costs[0]
    landscape = info["area_sqm"] * costs[1]
    soft = build_area * 500
    design = (building + landscape) * 0.04
    reserve = (building + landscape + soft + design) * 0.10
    total = building + landscape + soft + design + reserve

    # 收入预测
    spend_map = {"观光型": 150, "度假型": 400, "复合型": 350, "康养型": 500}
    per_capita = spend_map.get(info["project_type"], 300)
    annual_revenue = info["annual_visitors"] * per_capita
    opex = annual_revenue * 0.40
    profit = annual_revenue - opex
    payback = total / profit if profit > 0 else 0

    return f"""### 6.1 投资估算（{info['budget']}）

| 项目 | 金额（万元） | 占比 | 说明 |
|------|------------|------|------|
| 建安工程 | {building/10000:.1f} | {building/total*100:.0f}% | 建设面积{build_area:.0f}㎡ |
| 景观工程 | {landscape/10000:.1f} | {landscape/total*100:.0f}% | 总面积{info['area_sqm']:.0f}㎡ |
| 软装设备 | {soft/10000:.1f} | {soft/total*100:.0f}% | 内部装修+设备采购 |
| 设计费用 | {design/10000:.1f} | {design/total*100:.0f}% | 约4% |
| 预备金 | {reserve/10000:.1f} | {reserve/total*100:.0f}% | 10% |
| **合计** | **{total/10000:.1f}** | **100%** | — |

> ���️ 以上为行业经验估算值，实际需结合当地人工/材料价格。

### 6.2 收入预测

| 指标 | 基准情景 | 乐观情景(+20%) | 悲观情景(-20%) |
|------|---------|---------------|---------------|
| 年客流量 | {info['annual_visitors']}人 | {int(info['annual_visitors']*1.2)}人 | {int(info['annual_visitors']*0.8)}人 |
| 人均消费 | {per_capita}元 | {int(per_capita*1.1)}元 | {int(per_capita*0.9)}元 |
| 年收入 | {annual_revenue/10000:.1f}万 | {annual_revenue*1.2/10000:.1f}万 | {annual_revenue*0.8/10000:.1f}万 |
| 年运营成本 | {opex/10000:.1f}万 | — | — |
| 年净利润 | {profit/10000:.1f}万 | {profit*1.2/10000:.1f}万 | {profit*0.8/10000:.1f}万 |
| 静态回收期 | {payback:.1f}年 | {total/(profit*1.2):.1f}年 | {total/(profit*0.8):.1f}年 |

### 6.3 5层收入结构参考

| 层级 | 收入类型 | 毛利率 | 建议占比目标 |
|------|---------|-------|-------------|
| 第5层 被动收入 | 品牌授权/IP输出/管理输出 | 80-95% | 10-15% |
| 第4层 延伸收入 | 文创/课程/内容付费/社群 | 60-80% | 15-20% |
| 第3层 增值收入 | 特色餐饮/住宿升级/深度体验 | 50-70% | 25-30% |
| 第2层 基础收入 | 门票/停车/基础餐饮 | 40-60% | 30-40% |
| 第1层 流量收入 | 广告/补贴/招商 | 60-90% | 10-15% |

### 6.4 政策资金匹配建议

| 资金通道 | 规模 | 匹配度 |
|---------|------|-------|
| {' | '.join(POLICY_FUNDS[0])} | ⭐⭐⭐⭐⭐ |
| {' | '.join(POLICY_FUNDS[3])} | ⭐⭐⭐⭐ |
| 省级旅游专项资金 | 各地不同 | ⭐⭐⭐⭐ |
"""

def gen_module7(info: Dict) -> str:
    """模块7: 分期开发建议"""
    return f"""### 分期开发建议

| 阶段 | 时间 | 建设内容 | 投资占比 | 目标 |
|------|------|---------|---------|------|
| 一期（启动区） | 0-12个月 | 入口服务区+核心吸引区+基础配套 | 40% | 验证模式、获取现金流 |
| 二期（扩容区） | 12-24个月 | 休闲消费区+住宿配套区 | 35% | 提升客单价、延长停留时间 |
| 三期（完善期） | 24-36个月 | 生态保育区+IP衍生品+线上系统 | 25% | 品牌沉淀、数字资产 |

**冷启动建议：**
- 一期先开公区+核心体验产品试水
- 轻资产启动，优先爆款产品（萌宠/旅拍/露营地）
- 同步推进政策资金申报
"""

def gen_module8(info: Dict) -> str:
    """模块8: 使用引导"""
    return f"""### 后续可选动作

- 🏛️ **出建筑概念方案** — 请描述或上传场地照片/草图，可出单体建筑概念
- 📈 **做3-5年财务模型** — 用 `scripts/investment-calc.py` 做详细测算
- 🗺️ **做HTML项目介绍PPT** — 可用 html-ppt 技能生成
- 📋 **生成标准策划报告（10页版）** — 获取详细策划文本
- 🌐 **查看客源圈层热力图** — 用 `scripts/catchment-heatmap.py` 生成

### 快捷指令
- `/plan` 完整策划  `/swot` SWOT分析  `/calculate` 投资测算  `/report` 生成报告

---

> **生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}
> **工具版本：** V{VERSION}
> **⚠️ 免责声明：** 以上内容为行业经验参考值自动生成，不构成投资决策依据。正式方案需结合当地实际调研和专业机构评估。
"""

# ===== 主流程 =====

def generate_plan(info: Dict) -> str:
    """生成完整方案"""
    timestamp = datetime.now().strftime("%Y年%m月%d日")

    modules = [
        gen_module1(info),
        gen_module2(info),
        gen_module3(info),
        gen_module4(info),
        gen_module5(info),
        gen_module6(info),
        gen_module7(info),
        gen_module8(info),
    ]

    guests_str = "、".join(info["guests"])

    plan = f"""# {info['project_name']} · 文旅项目策划方案

> **项目地点：** {info['location']}
> **项目类型：** {info['project_type']}
> **地形：** {info['terrain']}
> **目标客群：** {guests_str}
> **预算等级：** {info['budget']}
> **建设模式：** {info['mode']}
> **生成日期：** {timestamp}
> **版本：** V{VERSION}

---

## 一、资源禀赋评估

{modules[0]}

---

## 二、市场与客群分析

{modules[1]}

---

## 三、主题定位与IP策划

{modules[2]}

---

## 四、空间布局与动线规划

{modules[3]}

---

## 五、业态策划与产品矩阵

{modules[4]}

---

## 六、投资测算与风险评估

{modules[5]}

---

## 七、分期开发建议

{modules[6]}

---

## 八、使用引导

{modules[7]}
"""
    return plan


def demo_mode():
    """演示模式"""
    info = {
        "project_name": "龙隐山谷康养度假区",
        "location": "四川省成都市都江堰",
        "area_mu": 500,
        "area_sqm": 500 * 666.67,
        "terrain": "山地坡地",
        "project_type": "康养型",
        "guests": ["银发康养(55-70)", "她旅游(25-50女性)", "亲子家庭(30-40)"],
        "budget": "精品型",
        "mode": "新建",
        "land_type": "集体建设用地",
        "daily_visitors": 3000,
        "annual_visitors": 3000 * 320,
    }
    return info


def main():
    args = [a.lower() for a in sys.argv[1:]]
    demo = "--demo" in args

    if demo:
        print("🎯 演示模式 — 使用示例数据")
        info = demo_mode()
    else:
        info = get_project_info()

    print(f"\n{'=' * 55}")
    print(f"  🏗 正在生成策划方案...")
    print(f"{'=' * 55}")

    plan = generate_plan(info)

    # 终端预览（前500字）
    preview = plan[:800]
    print(f"\n{'─' * 55}")
    print(f"  📋 方案预览（前800字）：")
    print(f"{'─' * 55}")
    print(preview)
    print(f"\n...（完整方案共 {len(plan)} 字）")

    # 保存文件
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = os.path.join(OUTPUT_DIR, f"{info['project_name']}_策划方案_v{VERSION}.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(plan)

    print(f"\n{'=' * 55}")
    print(f"  ✅ 方案已保存到：")
    print(f"     {filename}")
    print(f"  📏 总字数：{len(plan)} 字")
    print(f"{'=' * 55}")
    print(f"\n💡 后续操作建议：")
    print(f"  - 运行 investment-calc.py 做详细财务测算")
    print(f"  - 运行 catchment-heatmap.py 生成圈层热力图")
    print(f"  - 如需调整方案，重新运行本脚本修改参数")


if __name__ == "__main__":
    main()
