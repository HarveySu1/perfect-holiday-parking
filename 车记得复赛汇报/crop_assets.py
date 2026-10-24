# -*- coding: utf-8 -*-
"""Re-crop research screenshots to uniform 3:2 landscape bands."""
from PIL import Image
import os

BASE = r"C:\Users\Su\Desktop\完美假日"
SRC = os.path.join(BASE, "assets", "research-sz-20261014")
DST = os.path.join(BASE, "车记得复赛汇报", "assets")

jobs = [
    # src, dst, y_start_fraction, target_ratio (w/h)
    ("01-qianhai-wxh-ar-nav.jpg", "research_wxh_ar.jpg", 0.050, 1.5),
    ("04-ziyue-pay-only.jpg", "research_zy_pay.jpg", 0.110, 1.5),
    ("05-wxtd-sim-nav.jpg", "research_wxtd_sim.jpg", 0.040, 1.5),
]
for src, dst, y0f, ratio in jobs:
    im = Image.open(os.path.join(SRC, src))
    w, h = im.size
    y0 = int(h * y0f)
    y1 = min(h, y0 + int(round(w / ratio)))
    im.crop((0, y0, w, y1)).save(os.path.join(DST, dst), quality=90)
    print("crop", dst, (w, y1 - y0), "y:", y0, y1, "of", h)

print("DONE")
