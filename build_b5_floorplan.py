#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B5 停车场平面图 SVG 生成器
基于参考图片目视估算比例，生成单个自包含 HTML 文件。
坐标系：viewBox 0 0 1600 1100，1 SVG 单位 ≈ 0.1 m（10 单位 = 1 m）。
"""

import math
from pathlib import Path

# ============== 全局配置 ==============
VIEWBOX_W, VIEWBOX_H = 1600, 1100
SCALE_NOTE = "1 SVG 单位 ≈ 0.1 m（比例由参考图目视估算，供路径规划叠加使用）"

OUTPUT_PATH = Path(r"C:\Users\Su\Desktop\完美假日\output\B5_parking_floor_plan.html")

# 颜色配置（工程平面图风格）
COLORS = {
    "bg": "#F7F9FB",
    "outer_wall": "#2B2B2B",
    "wall_fill": "#EAF0F5",
    "lane": "#4A4A4A",
    "lane_center": "#F5D76E",
    "slot_fill": "#E3EEF7",
    "slot_stroke": "#5A7A96",
    "column": "#7A7A7A",
    "elevator": "#D0E6F7",
    "elevator_stroke": "#3A7CA5",
    "ramp": "#D5D5D5",
    "text": "#1F2937",
    "text_light": "#FFFFFF",
    "arrow": "#5A7A96",
    "scale_bar": "#2B2B2B",
}


def polar_offset(x, y, angle_deg, dist):
    """沿角度方向偏移指定距离。"""
    rad = math.radians(angle_deg)
    return x + dist * math.cos(rad), y + dist * math.sin(rad)


def rect_polygon(cx, cy, w, h, angle_deg=0):
    """返回以 (cx,cy) 为中心、旋转 angle_deg 的矩形四个顶点。"""
    rad = math.radians(angle_deg)
    dx, dy = w / 2, h / 2
    corners = [(-dx, -dy), (dx, -dy), (dx, dy), (-dx, dy)]
    pts = []
    for px, py in corners:
        rx = cx + px * math.cos(rad) - py * math.sin(rad)
        ry = cy + px * math.sin(rad) + py * math.cos(rad)
        pts.append((round(rx, 2), round(ry, 2)))
    return pts


def pts_to_str(points):
    """将 [(x,y),...] 转为 SVG points 字符串。"""
    return " ".join(f"{x},{y}" for x, y in points)


def poly(points, cls, id_=None, fill=None, stroke=None, stroke_width=None):
    """生成 <polygon> 元素。"""
    attrs = f'class="{cls}"'
    if id_:
        attrs += f' id="{id_}"'
    if fill is not None:
        attrs += f' fill="{fill}"'
    if stroke is not None:
        attrs += f' stroke="{stroke}"'
    if stroke_width is not None:
        attrs += f' stroke-width="{stroke_width}"'
    return f"  <polygon {attrs} points='{pts_to_str(points)}' />"


def line(x1, y1, x2, y2, cls, id_=None, stroke=None, stroke_width=None, dash=None, marker_end=None):
    attrs = f'class="{cls}"'
    if id_:
        attrs += f' id="{id_}"'
    if stroke is not None:
        attrs += f' stroke="{stroke}"'
    if stroke_width is not None:
        attrs += f' stroke-width="{stroke_width}"'
    if dash is not None:
        attrs += f' stroke-dasharray="{dash}"'
    if marker_end is not None:
        attrs += f' marker-end="{marker_end}"'
    return f"  <line {attrs} x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' />"


def text(x, y, content, cls, id_=None, anchor="middle", size=12, fill=None, angle=0):
    attrs = f'class="{cls}"'
    if id_:
        attrs += f' id="{id_}"'
    if fill is not None:
        attrs += f' fill="{fill}"'
    transform = ""
    if angle:
        transform = f' transform="rotate({angle} {x} {y})"'
    return f"  <text {attrs} x='{x}' y='{y}' text-anchor='{anchor}' font-size='{size}'{transform}>{content}</text>"


def arrow_path(x, y, angle_deg, length=18, cls="direction-arrow"):
    """生成方向箭头 path。"""
    rad = math.radians(angle_deg)
    x2 = x + length * math.cos(rad)
    y2 = y + length * math.sin(rad)
    # 箭头两翼
    a1 = math.radians(angle_deg + 150)
    a2 = math.radians(angle_deg - 150)
    l = length * 0.35
    xw1 = x2 + l * math.cos(a1)
    yw1 = y2 + l * math.sin(a1)
    xw2 = x2 + l * math.cos(a2)
    yw2 = y2 + l * math.sin(a2)
    d = f"M{x},{y} L{x2},{y2} M{x2},{y2} L{xw1},{yw1} M{x2},{y2} L{xw2},{yw2}"
    return f"  <path class='{cls}' d='{d}' fill='none' stroke='{COLORS['arrow']}' stroke-width='2' stroke-linecap='round' />"


# ============== 几何定义 ==============
# 外层边界（逆时针，基于参考图目视估算）
OUTER_BOUNDARY = [
    (320, 90),    # 左上
    (520, 70),    # 上偏左
    (780, 95),    # 上中
    (1020, 130),  # 上中右
    (1240, 165),  # 右上
    (1380, 195),  # 右上方内凹
    (1440, 240),  # 右上方外凸
    (1460, 420),  # 右中上
    (1450, 620),  # 右中下
    (1390, 760),  # 右下
    (1220, 820),  # 下偏右
    (980, 860),   # 下中右
    (760, 900),   # 下中
    (520, 960),   # 下中左
    (280, 910),   # 左下
    (110, 790),   # 左下外
    (85, 600),    # 左中
    (100, 400),   # 左中上
    (180, 220),   # 左上方
]


def make_lane_polygon(centerline, width):
    """根据中心线（点序列）和宽度生成车道多边形。"""
    if len(centerline) < 2:
        return []
    left = []
    right = []
    half = width / 2
    for i, (x, y) in enumerate(centerline):
        if i == 0:
            dx = centerline[i + 1][0] - x
            dy = centerline[i + 1][1] - y
        elif i == len(centerline) - 1:
            dx = x - centerline[i - 1][0]
            dy = y - centerline[i - 1][1]
        else:
            dx = centerline[i + 1][0] - centerline[i - 1][0]
            dy = centerline[i + 1][1] - centerline[i - 1][1]
        length = math.hypot(dx, dy)
        if length == 0:
            continue
        ux, uy = -dy / length, dx / length
        left.append((round(x + ux * half, 2), round(y + uy * half, 2)))
        right.append((round(x - ux * half, 2), round(y - uy * half, 2)))
    return left + right[::-1]


# 主车道中心线定义（含主干道与连接道）
LANES = [
    # id, centerline_points, width
    ("main-spine", [(520, 940), (700, 760), (900, 560), (1100, 380), (1320, 230)], 60),
    ("left-peripheral", [(180, 820), (250, 620), (320, 420), (390, 220)], 55),
    ("left-connector-n", [(390, 220), (520, 220), (650, 240)], 50),
    ("left-connector-m", [(320, 420), (580, 430), (760, 460)], 50),
    ("left-connector-s", [(250, 620), (520, 640), (760, 680)], 50),
    ("right-top-traverse", [(1020, 130), (1240, 165), (1440, 240)], 55),
    ("right-mid-traverse", [(900, 360), (1100, 380), (1380, 400), (1460, 420)], 55),
    ("right-lower-traverse", [(760, 680), (980, 700), (1220, 720), (1390, 760)], 55),
    ("right-vertical-e", [(1380, 195), (1380, 400), (1390, 760)], 50),
    ("right-vertical-w", [(1220, 165), (1220, 380), (1220, 720)], 50),
    ("central-east-west", [(760, 460), (900, 460), (1100, 380)], 50),
]


def generate_parking_row(start, end, slot_width, slot_depth, count, row_id, angle_offset=0):
    """生成一排停车位（垂直于行车道）。"""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    base_len = math.hypot(dx, dy)
    base_angle = math.degrees(math.atan2(dy, dx))
    perp_angle = base_angle + 90 + angle_offset

    slots = []
    labels = []
    for i in range(count):
        t0 = i / count
        t1 = (i + 1) / count
        x0 = start[0] + dx * t0
        y0 = start[1] + dy * t0
        x1 = start[0] + dx * t1
        y1 = start[1] + dy * t1
        # 槽位多边形：沿车道方向宽 slot_width，垂直深度 slot_depth
        p0 = polar_offset(x0, y0, perp_angle, slot_depth)
        p1 = polar_offset(x1, y1, perp_angle, slot_depth)
        pts = [(x0, y0), (x1, y1), p1, p0]
        slot_id = f"{row_id}-slot-{i+1:02d}"
        slots.append(poly(pts, "parking-slot", id_=slot_id))
        # 编号文字
        mx = (x0 + x1 + p0[0] + p1[0]) / 4
        my = (y0 + y1 + p0[1] + p1[1]) / 4
        labels.append(text(mx, my + 3, f"{row_id.upper()}{i+1:02d}", "slot-label",
                          id_=f"label-{slot_id}", anchor="middle", size=9, fill=COLORS["text"], angle=base_angle))
    return slots, labels


# 停车位排定义：起点、终点、槽宽(单位)、槽深(单位)、数量、行ID
PARKING_ROWS = [
    # 左侧长排（沿 left-peripheral 东侧，垂直向外）
    ((430, 220), (600, 240), 25, 50, 6, "a", -2),
    ((360, 420), (600, 440), 25, 50, 9, "b", -2),
    ((290, 620), (580, 650), 25, 50, 11, "c", -2),
    ((220, 820), (520, 860), 25, 50, 11, "d", -2),
    # 左侧长排另一侧（朝向车道）
    ((460, 270), (630, 290), 25, 50, 6, "e", 0),
    ((390, 470), (630, 490), 25, 50, 9, "f", 0),
    ((320, 670), (610, 700), 25, 50, 11, "g", 0),
    # 左侧上方小块
    ((430, 160), (550, 165), 22, 45, 5, "h", -5),
    # 中央左侧横排
    ((600, 360), (760, 370), 25, 50, 6, "i", -2),
    ((600, 520), (760, 530), 25, 50, 6, "j", -2),
    # 右侧上方停车块
    ((1260, 190), (1380, 210), 25, 50, 4, "k", -5),
    # 右侧中部竖排
    ((1240, 420), (1240, 600), 25, 50, 7, "l", 0),
    ((1380, 420), (1380, 600), 25, 50, 7, "m", 0),
    # 右侧下方停车块
    ((980, 740), (1180, 760), 25, 50, 8, "n", -2),
    ((1240, 760), (1380, 770), 25, 50, 5, "o", -2),
]


# 电梯/扶梯/核心区域定义：中心点、尺寸、旋转角、类型、标签
FACILITIES = [
    {"id": "elevator-1-cargo", "cx": 150, "cy": 580, "w": 70, "h": 90, "angle": -15, "label": "1号货梯", "type": "cargo"},
    {"id": "elevator-2", "cx": 360, "cy": 170, "w": 60, "h": 80, "angle": -10, "label": "2号电梯", "type": "passenger"},
    {"id": "elevator-5", "cx": 480, "cy": 560, "w": 70, "h": 90, "angle": -8, "label": "5号电梯", "type": "passenger"},
    {"id": "elevator-4", "cx": 1160, "cy": 300, "w": 90, "h": 110, "angle": 0, "label": "4号电梯", "type": "passenger"},
    {"id": "escalator-16", "cx": 1280, "cy": 260, "w": 60, "h": 90, "angle": 0, "label": "扶梯16", "type": "escalator"},
    {"id": "escalator-17", "cx": 1300, "cy": 540, "w": 60, "h": 90, "angle": 0, "label": "扶梯17", "type": "escalator"},
]


# 承重柱（小矩形，散布在车道交汇/转角处）
COLUMNS = [
    (420, 260, 12, 18, -10), (510, 300, 12, 18, -10),
    (350, 460, 12, 18, -8), (500, 500, 12, 18, -8),
    (280, 660, 12, 18, -6), (480, 710, 12, 18, -6),
    (720, 620, 14, 20, 0), (720, 500, 14, 20, 0),
    (980, 400, 14, 20, 0), (1100, 380, 14, 20, 0),
    (1220, 380, 14, 20, 0), (1380, 400, 14, 20, 0),
    (1220, 720, 14, 20, 0), (1390, 760, 14, 20, 0),
]


# 出入口坡道区域（左下与右上）
RAMPS = [
    {"id": "ramp-entrance-west", "cx": 140, "cy": 740, "w": 90, "h": 130, "angle": -20, "label": "入口坡道"},
    {"id": "ramp-exit-east", "cx": 1420, "cy": 300, "w": 80, "h": 140, "angle": 5, "label": "出口坡道"},
]


# 方向箭头（沿车道）
ARROWS = [
    (550, 880, 45), (750, 680, 45), (950, 480, 45), (1200, 300, 45),
    (220, 720, -25), (290, 520, -25), (360, 320, -25),
    (850, 380, 0), (1050, 360, 0),
    (1240, 600, 90), (1380, 600, -90),
]


# ============== SVG 组装 ==============
def build_svg():
    lines = []
    lines.append(f'<svg id="floor-plan" viewBox="0 0 {VIEWBOX_W} {VIEWBOX_H}" preserveAspectRatio="xMidYMid meet">')
    lines.append("  <defs>")
    lines.append("    <marker id='arrowhead' markerWidth='8' markerHeight='8' refX='6' refY='3' orient='auto'>")
    lines.append("      <path d='M0,0 L8,3 L0,6 Z' fill='#5A7A96' />")
    lines.append("    </marker>")
    lines.append("  </defs>")

    # 背景
    lines.append(f'  <rect id="canvas-bg" x="0" y="0" width="{VIEWBOX_W}" height="{VIEWBOX_H}" fill="{COLORS["bg"]}" />')

    # 工程网格（轻淡，便于读坐标）
    lines.append('  <g id="grid-lines" opacity="0.18">')
    grid_step = 50
    for gx in range(0, VIEWBOX_W + 1, grid_step):
        lines.append(f'    <line x1="{gx}" y1="0" x2="{gx}" y2="{VIEWBOX_H}" stroke="#94A3B8" stroke-width="0.5" />')
    for gy in range(0, VIEWBOX_H + 1, grid_step):
        lines.append(f'    <line x1="0" y1="{gy}" x2="{VIEWBOX_W}" y2="{gy}" stroke="#94A3B8" stroke-width="0.5" />')
    lines.append("  </g>")

    # 外墙边界
    lines.append(poly(OUTER_BOUNDARY, "outer-wall", id_="outer-boundary",
                     fill=COLORS["wall_fill"], stroke=COLORS["outer_wall"], stroke_width=6))

    # 车道（先绘制填充，再绘制中心虚线）
    lines.append('  <g id="lanes">')
    lane_centerlines = []
    for lane_id, centerline, width in LANES:
        poly_pts = make_lane_polygon(centerline, width)
        if poly_pts:
            lines.append(poly(poly_pts, "lane", id_=f"lane-{lane_id}",
                             fill=COLORS["lane"], stroke=COLORS["outer_wall"], stroke_width=2))
            lane_centerlines.append((lane_id, centerline))
    lines.append("  </g>")

    # 车道中心虚线
    lines.append('  <g id="lane-center-lines">')
    for lane_id, centerline in lane_centerlines:
        for i in range(len(centerline) - 1):
            x1, y1 = centerline[i]
            x2, y2 = centerline[i + 1]
            lines.append(line(x1, y1, x2, y2, "lane-center-line",
                             id_=f"lane-center-{lane_id}-{i}",
                             stroke=COLORS["lane_center"], stroke_width=2, dash="8,8"))
    lines.append("  </g>")

    # 停车位
    lines.append('  <g id="parking-slots">')
    for start, end, sw, sd, count, rid, ang_off in PARKING_ROWS:
        slots, labels = generate_parking_row(start, end, sw, sd, count, rid, ang_off)
        lines.extend(slots)
    lines.append("  </g>")

    # 车位编号图层
    lines.append('  <g id="slot-labels" class="toggle-layer" data-layer="slot-labels">')
    for start, end, sw, sd, count, rid, ang_off in PARKING_ROWS:
        _, labels = generate_parking_row(start, end, sw, sd, count, rid, ang_off)
        lines.extend(labels)
    lines.append("  </g>")

    # 承重柱
    lines.append('  <g id="structural-columns">')
    for i, (cx, cy, w, h, a) in enumerate(COLUMNS):
        pts = rect_polygon(cx, cy, w, h, a)
        lines.append(poly(pts, "column", id_=f"column-{i+1:02d}",
                         fill=COLORS["column"], stroke=COLORS["outer_wall"], stroke_width=1))
    lines.append("  </g>")

    # 电梯/扶梯/核心设施
    lines.append('  <g id="facilities">')
    for f in FACILITIES:
        pts = rect_polygon(f["cx"], f["cy"], f["w"], f["h"], f["angle"])
        lines.append(poly(pts, "facility", id_=f["id"],
                         fill=COLORS["elevator"], stroke=COLORS["elevator_stroke"], stroke_width=2))
    lines.append("  </g>")

    # 坡道
    lines.append('  <g id="ramps">')
    for r in RAMPS:
        pts = rect_polygon(r["cx"], r["cy"], r["w"], r["h"], r["angle"])
        lines.append(poly(pts, "ramp", id_=r["id"],
                         fill=COLORS["ramp"], stroke=COLORS["outer_wall"], stroke_width=2))
    lines.append("  </g>")

    # 标注图层
    lines.append('  <g id="annotations" class="toggle-layer" data-layer="annotations">')
    for f in FACILITIES:
        lines.append(text(f["cx"], f["cy"] + 4, f["label"], "facility-label",
                         id_=f"label-{f['id']}", anchor="middle", size=11, fill=COLORS["text"]))
    for r in RAMPS:
        lines.append(text(r["cx"], r["cy"] + 4, r["label"], "ramp-label",
                         id_=f"label-{r['id']}", anchor="middle", size=10, fill=COLORS["text"]))
    # 楼层标注
    # 右上 P 标识（参考图右上角停车标识）
    lines.append(text(1330, 160, "P", "parking-symbol",
                     anchor="middle", size=48, fill="#9CA3AF"))
    lines.append(text(80, 110, "B5 停车场平面图", "floor-title",
                     anchor="start", size=22, fill=COLORS["text"]))
    lines.append(text(80, 140, SCALE_NOTE, "scale-note",
                     anchor="start", size=11, fill="#5A5A5A"))
    lines.append("  </g>")

    # 方向箭头
    lines.append('  <g id="direction-arrows" class="toggle-layer" data-layer="direction-arrows">')
    for x, y, a in ARROWS:
        lines.append(arrow_path(x, y, a))
    lines.append("  </g>")

    # 比例尺
    lines.append('  <g id="scale-bar">')
    sb_x, sb_y = 80, 1020
    lines.append(line(sb_x, sb_y, sb_x + 100, sb_y, "scale-line",
                     stroke=COLORS["scale_bar"], stroke_width=3))
    lines.append(line(sb_x, sb_y - 5, sb_x, sb_y + 5, "scale-tick",
                     stroke=COLORS["scale_bar"], stroke_width=2))
    lines.append(line(sb_x + 100, sb_y - 5, sb_x + 100, sb_y + 5, "scale-tick",
                     stroke=COLORS["scale_bar"], stroke_width=2))
    lines.append(text(sb_x + 50, sb_y + 20, "10 m", "scale-text",
                     anchor="middle", size=11, fill=COLORS["text"]))
    lines.append("  </g>")

    # 指北针
    lines.append('  <g id="north-arrow">')
    nx, ny = 1500, 80
    lines.append(line(nx, ny + 30, nx, ny - 30, "north-line",
                     stroke=COLORS["scale_bar"], stroke_width=3, marker_end="url(#arrowhead)"))
    lines.append(text(nx + 12, ny, "N", "north-label",
                     anchor="start", size=16, fill=COLORS["text"]))
    lines.append("  </g>")

    lines.append("</svg>")
    return "\n".join(lines)


# ============== HTML 模板 ==============
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>B5 停车场平面图 - 车记得</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { height: 100%; overflow: hidden; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; }
    #app { display: flex; flex-direction: column; height: 100vh; background: #F7F9FB; }
    #toolbar { display: flex; align-items: center; gap: 10px; padding: 10px 16px; background: #fff; border-bottom: 1px solid #E5E7EB; box-shadow: 0 1px 3px rgba(0,0,0,0.04); z-index: 10; }
    #toolbar h1 { font-size: 16px; font-weight: 600; color: #1F2937; margin-right: auto; }
    .btn { padding: 6px 12px; font-size: 13px; border: 1px solid #D1D5DB; border-radius: 6px; background: #fff; color: #374151; cursor: pointer; transition: all 0.15s; user-select: none; }
    .btn:hover { background: #F3F4F6; border-color: #9CA3AF; }
    .btn.active { background: #E0F2FE; border-color: #7DD3FC; color: #0369A1; }
    .btn-group { display: flex; gap: 6px; }
    #canvas-container { flex: 1; position: relative; overflow: hidden; cursor: grab; }
    #canvas-container.grabbing { cursor: grabbing; }
    #floor-plan { display: block; width: 100%; height: 100%; }
    .status { font-size: 12px; color: #6B7280; margin-left: 10px; }

    /* SVG 样式 */
    .outer-wall { fill: #EAF0F5; }
    .lane { fill: #4A4A4A; }
    .lane-center-line { stroke: #F5D76E; opacity: 0.85; }
    .parking-slot { fill: #E3EEF7; stroke: #5A7A96; stroke-width: 1.2; }
    .parking-slot:hover { fill: #BFDBFE; stroke: #2563EB; }
    .slot-label { font-family: "Segoe UI", "PingFang SC", sans-serif; font-weight: 500; pointer-events: none; }
    .column { fill: #7A7A7A; }
    .facility { fill: #D0E6F7; }
    .ramp { fill: #D5D5D5; }
    .facility-label, .ramp-label { font-family: "PingFang SC", "Microsoft YaHei", sans-serif; font-weight: 600; pointer-events: none; }
    .direction-arrow { opacity: 0.7; }
    .scale-text, .north-label, .floor-title, .scale-note { font-family: "PingFang SC", "Microsoft YaHei", sans-serif; pointer-events: none; }

    /* 隐藏图层 */
    .hidden { display: none; }
  </style>
</head>
<body>
  <div id="app">
    <div id="toolbar">
      <h1>B5 停车场平面图</h1>
      <div class="btn-group">
        <button class="btn" id="btn-zoom-in" title="放大">+</button>
        <button class="btn" id="btn-zoom-out" title="缩小">−</button>
        <button class="btn" id="btn-reset" title="复位">复位</button>
      </div>
      <div class="btn-group">
        <button class="btn active" id="btn-toggle-labels" title="显示/隐藏车位编号">车位编号</button>
        <button class="btn active" id="btn-toggle-annotations" title="显示/隐藏标注">标注</button>
        <button class="btn active" id="btn-toggle-arrows" title="显示/隐藏方向箭头">箭头</button>
      </div>
      <span class="status" id="zoom-status">缩放: 100%</span>
    </div>
    <div id="canvas-container">
{svg_content}
    </div>
  </div>

  <script>
    (function() {{
      const container = document.getElementById('canvas-container');
      const svg = document.getElementById('floor-plan');
      const status = document.getElementById('zoom-status');
      let scale = 1;
      let translateX = 0;
      let translateY = 0;
      let isDragging = false;
      let startX = 0;
      let startY = 0;

      function updateTransform() {{
        svg.style.transform = `translate(${{translateX}}px, ${{translateY}}px) scale(${{scale}})`;
        status.textContent = `缩放: ${{(scale * 100).toFixed(0)}}%`;
      }}

      document.getElementById('btn-zoom-in').addEventListener('click', () => {{
        scale = Math.min(scale * 1.2, 8);
        updateTransform();
      }});
      document.getElementById('btn-zoom-out').addEventListener('click', () => {{
        scale = Math.max(scale / 1.2, 0.3);
        updateTransform();
      }});
      document.getElementById('btn-reset').addEventListener('click', () => {{
        scale = 1;
        translateX = 0;
        translateY = 0;
        updateTransform();
      }});

      container.addEventListener('wheel', (e) => {{
        e.preventDefault();
        const delta = e.deltaY > 0 ? 0.9 : 1.1;
        const rect = container.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        const newScale = Math.min(Math.max(scale * delta, 0.3), 8);
        // 以鼠标位置为中心缩放
        translateX = mx - (mx - translateX) * (newScale / scale);
        translateY = my - (my - translateY) * (newScale / scale);
        scale = newScale;
        updateTransform();
      }}, {{ passive: false }});

      container.addEventListener('mousedown', (e) => {{
        if (e.button !== 0) return;
        isDragging = true;
        startX = e.clientX - translateX;
        startY = e.clientY - translateY;
        container.classList.add('grabbing');
      }});
      window.addEventListener('mousemove', (e) => {{
        if (!isDragging) return;
        translateX = e.clientX - startX;
        translateY = e.clientY - startY;
        updateTransform();
      }});
      window.addEventListener('mouseup', () => {{
        isDragging = false;
        container.classList.remove('grabbing');
      }});

      function toggleLayer(btnId, selector) {{
        const btn = document.getElementById(btnId);
        const layers = document.querySelectorAll(selector);
        btn.addEventListener('click', () => {{
          const hidden = btn.classList.toggle('active');
          layers.forEach(el => el.classList.toggle('hidden', !hidden));
        }});
      }}
      toggleLayer('btn-toggle-labels', '#slot-labels');
      toggleLayer('btn-toggle-annotations', '#annotations');
      toggleLayer('btn-toggle-arrows', '#direction-arrows');

      updateTransform();
    }})();
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    svg = build_svg()
    html = HTML_TEMPLATE.replace("{svg_content}", svg)
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"已生成: {OUTPUT_PATH}")
    print(f"文件大小: {len(html):,} 字符")
