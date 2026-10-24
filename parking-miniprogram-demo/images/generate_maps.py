import xml.etree.ElementTree as ET
from xml.dom import minidom
import math
import os

def create_svg(width, height, view_box=None):
    svg = ET.Element('svg')
    svg.set('xmlns', 'http://www.w3.org/2000/svg')
    svg.set('width', str(width))
    svg.set('height', str(height))
    vb = view_box or f"0 0 {width} {height}"
    svg.set('viewBox', vb)
    svg.set('style', 'background-color:#D6E4F0')
    return svg

def add_rect(parent, x, y, w, h, fill, stroke=None, stroke_w=0, rx=0, ry=0, transform=None, opacity=1.0):
    rect = ET.SubElement(parent, 'rect')
    rect.set('x', str(x))
    rect.set('y', str(y))
    rect.set('width', str(w))
    rect.set('height', str(h))
    rect.set('fill', fill)
    if stroke:
        rect.set('stroke', stroke)
        rect.set('stroke-width', str(stroke_w))
    if rx:
        rect.set('rx', str(rx))
    if ry:
        rect.set('ry', str(ry))
    if transform:
        rect.set('transform', transform)
    if opacity < 1.0:
        rect.set('opacity', str(opacity))
    return rect

def add_polygon(parent, points, fill, stroke=None, stroke_w=0):
    poly = ET.SubElement(parent, 'polygon')
    poly.set('points', ' '.join([f"{p[0]},{p[1]}" for p in points]))
    poly.set('fill', fill)
    if stroke:
        poly.set('stroke', stroke)
        poly.set('stroke-width', str(stroke_w))
    return poly

def add_text(parent, x, y, text, fill, font_size=12, font_weight='normal', text_anchor='middle', transform=None):
    t = ET.SubElement(parent, 'text')
    t.set('x', str(x))
    t.set('y', str(y))
    t.set('fill', fill)
    t.set('font-size', str(font_size))
    t.set('font-weight', font_weight)
    t.set('text-anchor', text_anchor)
    t.set('font-family', 'PingFang SC, Microsoft YaHei, sans-serif')
    if transform:
        t.set('transform', transform)
    t.text = text
    return t

def add_circle(parent, cx, cy, r, fill, stroke=None, stroke_w=0):
    c = ET.SubElement(parent, 'circle')
    c.set('cx', str(cx))
    c.set('cy', str(cy))
    c.set('r', str(r))
    c.set('fill', fill)
    if stroke:
        c.set('stroke', stroke)
        c.set('stroke-width', str(stroke_w))
    return c

def add_path(parent, d, fill='none', stroke=None, stroke_w=1, stroke_linecap='round', stroke_linejoin='round'):
    p = ET.SubElement(parent, 'path')
    p.set('d', d)
    p.set('fill', fill)
    if stroke:
        p.set('stroke', stroke)
        p.set('stroke-width', str(stroke_w))
    p.set('stroke-linecap', stroke_linecap)
    p.set('stroke-linejoin', stroke_linejoin)
    return p

def add_elevator_icon(parent, x, y, size=28, label=None, icon_type='elevator'):
    # Orange square background
    add_rect(parent, x, y, size, size, '#F5A623', rx=4, ry=4)
    # Icon: simplified elevator or escalator
    if icon_type == 'elevator':
        # Box with door lines
        add_rect(parent, x+6, y+5, size-12, size-10, 'none', '#FFFFFF', 2, rx=1)
        add_path(parent, f"M{x+size/2},{y+5} V{y+size-5}", stroke='#FFFFFF', stroke_w=2)
    else:
        # Escalator-ish icon (handrail)
        add_path(parent, f"M{x+7},{y+size-7} L{x+size-7},{y+7}", stroke='#FFFFFF', stroke_w=3)
        add_path(parent, f"M{x+7},{y+7} L{x+7},{y+size-7}", stroke='#FFFFFF', stroke_w=2)
    if label:
        add_text(parent, x+size/2, y+size+14, label, '#333333', font_size=11, font_weight='600')

def draw_parking_row(parent, start_x, start_y, count, direction='vertical', step=34, spot_w=28, spot_h=46, label_prefix='B4-', start_num=1, highlight_id=None):
    spots = []
    for i in range(count):
        num = start_num + i
        label = f"{label_prefix}{num:03d}"
        if direction == 'vertical':
            x = start_x
            y = start_y + i * step
            # Slight perspective: top narrower
            fill = '#E8913A' if highlight_id == label else '#5A8F6A'
            add_rect(parent, x, y, spot_w, spot_h, fill, '#FFFFFF', 0.5)
            add_text(parent, x+spot_w/2, y+spot_h/2+4, label, '#FFFFFF', font_size=9, font_weight='600')
            spots.append({'id': label, 'x': x+spot_w/2, 'y': y+spot_h/2})
        elif direction == 'horizontal':
            x = start_x + i * step
            y = start_y
            fill = '#E8913A' if highlight_id == label else '#5A8F6A'
            add_rect(parent, x, y, spot_h, spot_w, fill, '#FFFFFF', 0.5)
            add_text(parent, x+spot_h/2, y+spot_w/2+4, label, '#FFFFFF', font_size=9, font_weight='600')
            spots.append({'id': label, 'x': x+spot_h/2, 'y': y+spot_w/2})
    return spots

def generate_b4_base(with_route=False):
    W, H = 800, 1000
    svg = create_svg(W, H)
    
    # Background road
    add_rect(svg, 0, 0, W, H, '#4A5568')
    
    # Large building/structure in center-bottom (white)
    add_polygon(svg, [(260, 420), (520, 420), (580, 680), (460, 760), (260, 760)], '#D8DDE5', '#FFFFFF', 1)
    
    # Top-left area: parking rows around B4-162 destination
    # Row 1: B4-159 to B4-164 (vertical, top-left)
    draw_parking_row(svg, 80, 120, 6, 'vertical', step=52, spot_w=36, spot_h=48, label_prefix='B4-', start_num=159, highlight_id='B4-162' if with_route else None)
    
    # Row 2: B4-248, B4-249 (right side vertical)
    draw_parking_row(svg, 680, 120, 2, 'vertical', step=52, spot_w=36, spot_h=48, label_prefix='B4-', start_num=248)
    
    # Row 3: B4-168 to B4-171 (left-middle vertical)
    draw_parking_row(svg, 80, 500, 4, 'vertical', step=52, spot_w=36, spot_h=48, label_prefix='B4-', start_num=168)
    
    # Row 4: B4-239, B4-240 (bottom-middle horizontal)
    draw_parking_row(svg, 320, 860, 2, 'horizontal', step=62, spot_w=30, spot_h=48, label_prefix='B4-', start_num=239)
    
    # 1号电梯厅 near center-right
    add_elevator_icon(svg, 560, 460, 32, '1号电梯厅', 'elevator')
    
    if with_route:
        # Route path (blue arrow line)
        route_d = "M 576 492 L 576 380 L 300 380 L 300 260 L 170 260"
        add_path(svg, route_d, stroke='#4A90E2', stroke_w=18, stroke_linecap='round')
        # Arrow chevrons on the route
        add_path(svg, "M 320 370 L 340 380 L 320 390", stroke='#FFFFFF', stroke_w=3, fill='none')
        add_path(svg, "M 400 370 L 420 380 L 400 390", stroke='#FFFFFF', stroke_w=3, fill='none')
        add_path(svg, "M 300 280 L 290 260 L 310 260", stroke='#FFFFFF', stroke_w=3, fill='none')
        
        # Start marker (green circle with 起)
        add_circle(svg, 576, 500, 16, '#4CAF50', '#FFFFFF', 2)
        add_text(svg, 576, 505, '起', '#FFFFFF', font_size=12, font_weight='bold')
        
        # End marker (red pin)
        pin_x, pin_y = 170, 220
        add_path(svg, f"M{pin_x},{pin_y} C{pin_x-14},{pin_y-18} {pin_x-14},{pin_y-38} {pin_x},{pin_y-38} C{pin_x+14},{pin_y-38} {pin_x+14},{pin_y-18} {pin_x},{pin_y} Z", fill='#E24B4B', stroke='#FFFFFF', stroke_w=2)
        add_circle(svg, pin_x, pin_y-28, 8, '#FFFFFF')
        add_text(svg, pin_x, pin_y-24, '终', '#E24B4B', font_size=9, font_weight='bold')
    
    # Compass
    add_text(svg, 60, 60, 'N', '#E24B4B', font_size=14, font_weight='bold')
    add_text(svg, 60, 78, 'E', '#666666', font_size=10)
    add_text(svg, 44, 70, 'W', '#666666', font_size=10)
    add_text(svg, 52, 70, 'S', '#666666', font_size=10)
    add_path(svg, "M 60 64 L 54 90 L 60 84 L 66 90 Z", fill='#4A90E2')
    
    return svg

def generate_b4():
    return generate_b4_base(with_route=False)

def generate_b4_route():
    return generate_b4_base(with_route=True)

def generate_b1():
    W, H = 800, 1000
    svg = create_svg(W, H)
    add_rect(svg, 0, 0, W, H, '#4A5568')
    
    # Central circular plaza
    add_circle(svg, W/2, H/2-50, 90, '#D8DDE5')
    
    # Parking blocks (green)
    blocks = [
        (60, 120, 180, 60), (300, 120, 180, 60), (540, 120, 200, 60),
        (60, 260, 120, 80), (620, 260, 120, 80),
        (60, 440, 100, 120), (640, 440, 100, 120),
        (60, 640, 120, 80), (620, 640, 120, 80),
        (120, 820, 200, 60), (480, 820, 200, 60),
    ]
    for bx, by, bw, bh in blocks:
        add_rect(svg, bx, by, bw, bh, '#5A8F6A', '#FFFFFF', 1)
        # draw spots inside
        cols = max(1, bw // 36)
        rows = max(1, bh // 50)
        for r in range(rows):
            for c in range(cols):
                sx = bx + c*36 + 2
                sy = by + r*50 + 2
                if sx+32 <= bx+bw and sy+46 <= by+bh:
                    add_rect(svg, sx, sy, 32, 46, '#6BA37C', '#FFFFFF', 0.5)
    
    # Highlight B1-036
    add_rect(svg, 300, 120, 36, 48, '#E8913A', '#FFFFFF', 1)
    add_text(svg, 318, 150, 'B1-036', '#FFFFFF', font_size=9, font_weight='bold')
    add_path(svg, "M 318 180 L 318 210 L 310 200 L 326 200 Z", fill='#4A90E2')
    
    # Elevators
    add_elevator_icon(svg, 160, 220, 32, '2号电梯厅', 'elevator')
    add_elevator_icon(svg, 580, 220, 32, '4号电梯厅', 'escalator')
    add_elevator_icon(svg, 160, 760, 32, '6号电梯厅', 'elevator')
    add_elevator_icon(svg, 420, 540, 32, '5号电梯厅', 'escalator')
    
    # Compass
    add_text(svg, 60, 60, 'N', '#E24B4B', font_size=14, font_weight='bold')
    add_path(svg, "M 60 64 L 54 90 L 60 84 L 66 90 Z", fill='#4A90E2')
    
    return svg

def generate_b3():
    W, H = 800, 1000
    svg = create_svg(W, H)
    add_rect(svg, 0, 0, W, H, '#4A5568')
    
    # Winding road/parking shape
    add_polygon(svg, [(80,80),(720,80),(760,200),(720,400),(760,600),(720,800),(680,920),(120,920),(80,800),(120,600),(80,400),(120,200)], '#5A8F6A')
    
    # Internal roads
    add_polygon(svg, [(200,200),(600,200),(640,320),(600,500),(640,680),(600,800),(200,800),(160,680),(200,500),(160,320)], '#4A5568')
    
    # Elevators
    add_elevator_icon(svg, 240, 240, 32, '3号电梯厅', 'elevator')
    add_elevator_icon(svg, 520, 680, 32, '7号电梯厅', 'escalator')
    
    # Spots labels
    spots = [
        ('B3-101', 140, 140), ('B3-102', 180, 140), ('B3-103', 220, 140),
        ('B3-201', 620, 260), ('B3-202', 660, 260),
        ('B3-301', 140, 860), ('B3-302', 180, 860),
    ]
    for sid, sx, sy in spots:
        add_text(svg, sx, sy, sid, '#FFFFFF', font_size=10, font_weight='600')
    
    # Compass
    add_text(svg, 60, 60, 'N', '#E24B4B', font_size=14, font_weight='bold')
    add_path(svg, "M 60 64 L 54 90 L 60 84 L 66 90 Z", fill='#4A90E2')
    
    return svg

def generate_b5():
    W, H = 800, 1000
    svg = create_svg(W, H)
    add_rect(svg, 0, 0, W, H, '#4A5568')
    
    # Large L-shape parking
    add_polygon(svg, [(60,60),(740,60),(740,420),(420,420),(420,940),(60,940)], '#5A8F6A')
    # Inner road
    add_polygon(svg, [(120,120),(680,120),(680,360),(360,360),(360,880),(120,880)], '#4A5568')
    
    # Elevators
    add_elevator_icon(svg, 200, 200, 32, '1号电梯厅', 'elevator')
    add_elevator_icon(svg, 560, 200, 32, '8号电梯厅', 'escalator')
    add_elevator_icon(svg, 200, 760, 32, '9号电梯厅', 'elevator')
    
    # Spots
    spots = [
        ('B5-001', 100, 100), ('B5-002', 140, 100), ('B5-003', 180, 100),
        ('B5-101', 700, 100), ('B5-102', 700, 140),
        ('B5-201', 100, 900), ('B5-202', 140, 900),
    ]
    for sid, sx, sy in spots:
        add_text(svg, sx, sy, sid, '#FFFFFF', font_size=10, font_weight='600')
    
    # Compass
    add_text(svg, 60, 60, 'N', '#E24B4B', font_size=14, font_weight='bold')
    add_path(svg, "M 60 64 L 54 90 L 60 84 L 66 90 Z", fill='#4A90E2')
    
    return svg

def save_svg(svg, filename):
    rough = ET.tostring(svg, encoding='unicode')
    reparsed = minidom.parseString(rough)
    pretty = reparsed.toprettyxml(indent="  ")
    # Remove empty lines from minidom
    lines = [line for line in pretty.split('\n') if line.strip()]
    xml = '\n'.join(lines)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml)

if __name__ == '__main__':
    out_dir = os.path.dirname(os.path.abspath(__file__))
    save_svg(generate_b1(), os.path.join(out_dir, 'map_b1.svg'))
    save_svg(generate_b3(), os.path.join(out_dir, 'map_b3.svg'))
    save_svg(generate_b4(), os.path.join(out_dir, 'map_b4.svg'))
    save_svg(generate_b4_route(), os.path.join(out_dir, 'map_b4_route.svg'))
    save_svg(generate_b5(), os.path.join(out_dir, 'map_b5.svg'))
    print('SVG maps generated.')
