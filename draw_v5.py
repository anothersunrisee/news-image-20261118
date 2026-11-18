#!/usr/bin/env python3
"""v5: dense newspaper front page for news-image-20261118. PIL-drawn, 1024x1024."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 40                      # outer margin
CW = W - 2 * M              # 944 content width

PAPER = (247, 241, 227)     # warm cream
INK = (26, 26, 26)
NAVY = (20, 38, 74)
RED = (193, 39, 45)
GOLD = (217, 164, 65)
TEAL = (31, 122, 109)
BLUE = (46, 95, 163)
GREEN = (62, 122, 58)
PURPLE = (106, 76, 147)
ORANGE = (198, 110, 30)
SLATE = (138, 148, 166)
GRAY = (68, 68, 68)
LIGHT_LINE = (216, 210, 192)
SKY = (215, 227, 238)
WATER = (46, 95, 163)
DARKTEAL = (20, 82, 74)

F = "/usr/share/fonts/truetype/noto/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

F_MAST = font("NotoSerifDisplay-Bold.ttf", 44)
F_KICK = font("NotoSans-Bold.ttf", 14)
F_CLAIM = font("NotoSans-Bold.ttf", 14)
F_SECT = font("NotoSans-Bold.ttf", 13)
F_H1 = font("NotoSans-Bold.ttf", 17)
F_SUB = font("NotoSans-Regular.ttf", 12)
F_CHIP = font("NotoSans-Bold.ttf", 10)
F_MH = font("NotoSans-Bold.ttf", 13)
F_MS = font("NotoSans-Regular.ttf", 11)
F_BR = font("NotoSans-Regular.ttf", 11)
F_BRN = font("NotoSans-Bold.ttf", 11)
F_FOOT = font("NotoSans-Regular.ttf", 11)
F_PIN = font("NotoSans-Bold.ttf", 10)
F_LEG = font("NotoSans-Bold.ttf", 10)
F_MAPL = font("NotoSans-Bold.ttf", 11)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_w(draw, s, f):
    return draw.textlength(s, font=f)

def wrap(draw, s, f, maxw):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def tracked(draw, cx, y, s, f, fill, tr=2):
    widths = [draw.textlength(c, font=f) for c in s]
    total = sum(widths) + tr * (len(s) - 1)
    x = cx - total / 2
    for c, w in zip(s, widths):
        draw.text((x, y), c, font=f, fill=fill)
        x += w + tr

def chip(draw, x, y, label, color):
    tw = draw.textlength(label, font=F_CHIP)
    pad = 7
    bw, bh = tw + 2 * pad, 17
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=3, fill=color)
    draw.text((x + pad, y + 3), label, font=F_CHIP, fill=(255, 255, 255))
    return bw

# ---------------------------------------------------------------- masthead
tracked(d, W // 2, 40, "THE WORLD IN ONE DAY", F_KICK, RED, tr=3)
d.text((W // 2, 56), "Wednesday 18 November 2026", font=F_MAST, fill=NAVY, anchor="ma")
tracked(d, W // 2, 106, "30 STORIES  ·  6 CONTINENTS  ·  ONE DAY", F_CLAIM, NAVY, tr=2)
d.rectangle([M, 128, W - M - 1, 131], fill=NAVY)
d.rectangle([M, 134, W - M - 1, 135], fill=RED)

# ---------------------------------------------------------------- pictograms
def starburst(draw, cx, cy, r_out, r_in, n=8, fill=RED):
    import math
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)

def picto_gulf(x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=NAVY)
    for sx, sy in [(0.12, 0.18), (0.30, 0.10), (0.55, 0.16), (0.90, 0.10)]:
        d.ellipse([x + sx * w - 2, y + sy * h - 2, x + sx * w + 2, y + sy * h + 2], fill=(255, 255, 255))
    # jet silhouette (white)
    d.polygon([(x + 0.08 * w, y + 0.52 * h), (x + 0.60 * w, y + 0.40 * h),
               (x + 0.92 * w, y + 0.46 * h), (x + 0.60 * w, y + 0.54 * h)], fill=(245, 240, 225))
    d.polygon([(x + 0.14 * w, y + 0.50 * h), (x + 0.20 * w, y + 0.28 * h),
               (x + 0.27 * w, y + 0.47 * h)], fill=(245, 240, 225))
    d.polygon([(x + 0.42 * w, y + 0.51 * h), (x + 0.52 * w, y + 0.74 * h),
               (x + 0.58 * w, y + 0.51 * h)], fill=(245, 240, 225))
    # explosion starburst top-right
    starburst(d, x + 0.84 * w, y + 0.22 * h, 20, 9, fill=(232, 90, 40))
    d.ellipse([x + 0.84 * w - 6, y + 0.22 * h - 6, x + 0.84 * w + 6, y + 0.22 * h + 6], fill=GOLD)
    # sea
    d.rectangle([x, y + h - 20, x + w - 1, y + h - 1], fill=TEAL)
    for i in range(6):
        wx = x + 12 + i * 48
        d.arc([wx, y + h - 14, wx + 22, y + h - 2], 180, 360, fill=(255, 255, 255), width=2)

def picto_kerch(x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=SKY)
    # smoke above the gap
    for sx, sy, r in [(0.50, 0.16, 9), (0.55, 0.10, 12), (0.46, 0.08, 7)]:
        d.ellipse([x + sx * w - r, y + sy * h - r, x + sx * w + r, y + sy * h + r], fill=(150, 158, 168))
    # two half-arches
    d.arc([x + 0.01 * w, y + 0.04 * h, x + 0.39 * w, y + 0.52 * h], 180, 360, fill=NAVY, width=4)
    d.arc([x + 0.61 * w, y + 0.04 * h, x + 0.99 * w, y + 0.52 * h], 180, 360, fill=NAVY, width=4)
    # deck: left + right segments, middle span fallen
    dy = y + 0.46 * h
    d.rectangle([x, dy, x + 0.38 * w, dy + 7], fill=NAVY)
    d.rectangle([x + 0.62 * w, dy, x + w, dy + 7], fill=NAVY)
    d.polygon([(x + 0.40 * w, dy + 2), (x + 0.60 * w, dy + 2),
               (x + 0.56 * w, dy + 26), (x + 0.44 * w, dy + 26)], fill=RED)
    # pillars
    d.rectangle([x + 0.13 * w, dy + 7, x + 0.13 * w + 6, y + h - 24], fill=NAVY)
    d.rectangle([x + 0.85 * w, dy + 7, x + 0.85 * w + 6, y + h - 24], fill=NAVY)
    # water
    d.rectangle([x, y + h - 24, x + w - 1, y + h - 1], fill=WATER)
    for i in range(6):
        wx = x + 12 + i * 48
        d.arc([wx, y + h - 16, wx + 22, y + h - 4], 180, 360, fill=(255, 255, 255), width=2)

def picto_shenzhen(x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=DARKTEAL)
    # gold sun
    d.ellipse([x + 0.86 * w - 13, y + 0.10 * h - 13, x + 0.86 * w + 13, y + 0.10 * h + 13], fill=GOLD)
    # small plane silhouette
    px, py = x + 0.30 * w, y + 0.16 * h
    d.polygon([(px - 26, py + 4), (px + 6, py - 2), (px + 30, py + 1), (px + 6, py + 5)], fill=(245, 240, 225))
    d.polygon([(px - 8, py + 3), (px - 2, py - 8), (px + 3, py + 3)], fill=(245, 240, 225))
    d.polygon([(px - 2, py + 4), (px + 2, py + 14), (px + 7, py + 4)], fill=(245, 240, 225))
    # flags: China (left) + USA (right)
    fx, fy = x + 0.30 * w, y + 0.34 * h
    d.rectangle([fx - 2, fy, fx, fy + 44], fill=(255, 255, 255))
    d.rectangle([fx, fy, fx + 52, fy + 32], fill=RED)
    d.ellipse([fx + 7, fy + 6, fx + 15, fy + 14], fill=GOLD)
    for sx, sy in [(24, 6), (30, 10), (30, 16), (24, 20)]:
        d.ellipse([fx + sx, fy + sy, fx + sx + 4, fy + sy + 4], fill=GOLD)
    ux = x + 0.56 * w
    d.rectangle([ux - 2, fy, ux, fy + 44], fill=(255, 255, 255))
    for i in range(7):
        col = RED if i % 2 == 0 else (255, 255, 255)
        d.rectangle([ux, fy + i * 5, ux + 52, fy + i * 5 + 5], fill=col)
    d.rectangle([ux, fy, ux + 22, fy + 18], fill=NAVY)
    for r in range(3):
        for c in range(4):
            d.ellipse([ux + 3 + c * 5, fy + 3 + r * 5, ux + 5 + c * 5, fy + 5 + r * 5], fill=(255, 255, 255))
    # skyline
    base = y + h
    for bx, bw, bh in [(0.02, 0.10, 26), (0.13, 0.08, 38), (0.22, 0.11, 30),
                       (0.68, 0.09, 34), (0.78, 0.10, 24), (0.89, 0.09, 30)]:
        d.rectangle([x + bx * w, base - bh, x + (bx + bw) * w, base], fill=NAVY)
        for wy in range(2):
            d.rectangle([x + (bx + 0.02) * w, base - bh + 6 + wy * 10,
                         x + (bx + 0.04) * w, base - bh + 10 + wy * 10], fill=GOLD)

# ---------------------------------------------------------------- top stories
TOPS = [
    ("MIDDLE EAST", RED, "GULF STRIKES: U.S. JETS HIT IRAN MISSILE SITE",
     "US jets hit an IRGC missile site on Qeshm Island; Iran drones hit US sites in Bahrain and Kuwait.",
     picto_gulf),
    ("EUROPE", BLUE, "KERCH BRIDGE ROAD SPAN COLLAPSES",
     "Strikes on 16–17 Nov bring down a 227 m road arch; first wreckage photos emerge on 18 Nov.",
     picto_kerch),
    ("ASIA", TEAL, "XI GREETS TRUMP AS APEC OPENS IN SHENZHEN",
     "Trump flies in from Manila after meeting Quad leaders; three-way talks with Putin due Thursday.",
     picto_shenzhen),
]
COLW, GUT = 304, 16
TY = 144
for i, (cat, col, head, sub, pic) in enumerate(TOPS):
    cx = M + i * (COLW + GUT)
    pic(cx, TY, COLW, 88)
    chip(d, cx, TY + 96, cat, col)
    lines = wrap(d, head, F_H1, COLW)
    yy = TY + 120
    for ln in lines[:3]:
        d.text((cx, yy), ln, font=F_H1, fill=INK)
        yy += 21
    slines = wrap(d, sub, F_SUB, COLW)
    assert len(slines) <= 2, f"top sub too long: {sub!r} -> {slines}"
    yy = TY + 120 + 3 * 21 + 2
    for ln in slines[:2]:
        d.text((cx, yy), ln, font=F_SUB, fill=GRAY)
        yy += 15

d.rectangle([M, 368, W - M - 1, 369], fill=LIGHT_LINE)

# ---------------------------------------------------------------- medium cards
d.text((M, 376), "AROUND THE WORLD", font=F_SECT, fill=NAVY)
d.rectangle([M + 190, 385, W - M - 1, 386], fill=LIGHT_LINE)
MEDIUMS = [
    ("CYCLONE", ORANGE, "Cyclone Akvan bears down on east India",
     "Severe storm 520 km off Narsapur; landfall due Friday.", "ASIA"),
    ("ISRAEL", RED, "Knesset elects Kahana speaker, 66–52",
     "Vote ends weeks of deadlock in Jerusalem.", "MIDDLE EAST"),
    ("EUROPE", BLUE, "EU proposes €45bn loan for Ukraine",
     "€25bn arms, €20bn budget; repaid only if Russia pays.", "EUROPE"),
    ("GAZA", PURPLE, "Peace board faults Israel and Hamas",
     "Report warns the ceasefire could collapse.", "MIDDLE EAST"),
    ("UKRAINE", BLUE, "Russia fires 141 drones overnight",
     "126 downed by 08:00; two killed, hits at 7 sites.", "EUROPE"),
    ("SUDAN", GREEN, "Amnesty: 37 killed by RSF drone strikes",
     "Nine strikes near El Obeid; probe as war crimes.", "AFRICA"),
    ("SPACE", NAVY, "Voyager 1 reaches one light-day",
     "16.1bn miles out; its signal takes a day to arrive.", "GLOBAL"),
    ("BRITAIN", TEAL, "UK inflation rises to 3.6%",
     "Highest in a year; fourth monthly rise in a row.", "EUROPE"),
]
MCW, MGUT = 227, 12
for row in range(2):
    ry = 404 + row * 102
    for col_i in range(4):
        m = MEDIUMS[row * 4 + col_i]
        mx = M + col_i * (MCW + MGUT)
        chip(d, mx, ry, m[0], m[1])
        lines = wrap(d, m[2], F_MH, MCW)
        yy = ry + 24
        for ln in lines[:2]:
            d.text((mx, yy), ln, font=F_MH, fill=INK)
            yy += 16
        slines = wrap(d, m[3], F_MS, MCW)
        yy = ry + 24 + 2 * 16 + 3
        for ln in slines[:2]:
            d.text((mx, yy), ln, font=F_MS, fill=GRAY)
            yy += 14
    # vertical dividers between columns
    for col_i in range(1, 4):
        vx = M + col_i * (MCW + MGUT) - 6
        d.rectangle([vx, ry + 2, vx, ry + 96], fill=LIGHT_LINE)

d.rectangle([M, 610, W - M - 1, 611], fill=LIGHT_LINE)

# ---------------------------------------------------------------- briefs
d.text((M, 618), "THE BRIEFS — 19 MORE STORIES", font=F_SECT, fill=NAVY)
d.rectangle([M + 268, 627, W - M - 1, 628], fill=LIGHT_LINE)
BRIEFS = [
    "Gold falls below $3,800/oz — first time since Sept.",
    "GTA VI goes on sale worldwide — Take-Two shares +6%.",
    "COP31 draft splits talks — EU rejects fossil text.",
    "Bangladesh garment workers protest — 132 factories shut.",
    "Australia sanctions settler leader Daniella Weiss.",
    "U.S. loses measles elimination status — 5,400+ cases.",
    "DR Congo Ebola cases double — 11,000+ cases.",
    "Dow falls 849 pts; S&P down a 4th straight day.",
    "Anthropic prices IPO — trading starts Thu as ANT.",
    "Estonia border closure fallout — Narva mayor objects.",
    "Trump–Thailand trade deal signed in Manila.",
    "Canada announces C$155m military aid for Ukraine.",
    "Dhoni retires from IPL — mentor from 2027.",
    "Jeffries elected House Democrat leader, 251–11.",
    "Indonesia–China agree $71.8bn partnerships.",
    "Imamoglu given 2 more years + new political ban.",
    "Drone strikes nearly halve Russia's oil refining.",
    "Uganda activist Mugumya charged in military court.",
    "Como hit nine in 9–1 Champions League win at Lens.",
]
BW = 460
for i, b in enumerate(BRIEFS):
    col_i = 0 if i < 10 else 1
    row_i = i if i < 10 else i - 10
    bx = M + col_i * (BW + 24)
    by = 644 + row_i * 13
    d.text((bx, by), f"{i+1}.", font=F_BRN, fill=RED)
    d.text((bx + 22, by), b, font=F_BR, fill=INK)

d.rectangle([M, 782, W - M - 1, 783], fill=LIGHT_LINE)

# ---------------------------------------------------------------- world map (dot-matrix)
d.text((M, 788), "WHERE IT HAPPENED — SCHEMATIC MAP, NOT TO SCALE", font=F_MAPL, fill=NAVY)
MAP = (M, 806, W - M, 944)   # x0, y0, x1, y1
mx0, my0, mx1, my1 = MAP
mw, mh = mx1 - mx0, my1 - my0
LAT_TOP, LAT_BOT = 76.0, -56.0
def proj(lon, lat):
    x = mx0 + (lon + 180.0) / 360.0 * mw
    y = my0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * mh
    return x, y

CONTINENTS = [
    # North America
    [(-168,66),(-140,70),(-125,72),(-110,73),(-95,80),(-85,80),(-75,72),(-65,60),
     (-55,52),(-60,47),(-70,44),(-75,35),(-80,32),(-81,26),(-84,30),(-90,29),
     (-97,26),(-105,20),(-97,16),(-92,15),(-86,13),(-83,9),(-79,9),(-85,11),
     (-90,14),(-95,16),(-105,20),(-110,24),(-114,29),(-120,34),(-125,40),
     (-124,48),(-130,55),(-145,60),(-155,58),(-165,60),(-168,66)],
    # South America
    [(-79,9),(-72,12),(-62,10),(-52,5),(-50,0),(-44,-3),(-35,-8),(-40,-20),
     (-48,-28),(-52,-33),(-58,-38),(-62,-41),(-66,-47),(-70,-52),(-73,-50),
     (-73,-40),(-72,-30),(-70,-18),(-77,-12),(-81,-6),(-80,0),(-79,9)],
    # Africa
    [(-17,15),(-10,30),(-5,35),(0,36),(10,37),(20,32),(30,31),(35,28),(38,22),
     (43,12),(48,11),(51,10),(44,0),(40,-10),(36,-18),(32,-26),(28,-33),
     (20,-35),(16,-28),(12,-18),(9,-1),(9,4),(-8,4),(-13,8),(-17,15)],
    # Eurasia
    [(-10,36),(-9,43),(-2,48),(-5,50),(0,51),(5,53),(8,57),(10,59),(18,56),
     (21,55),(24,59),(28,60),(30,62),(35,66),(40,68),(50,69),(60,69),(70,72),
     (80,73),(90,75),(100,77),(110,74),(120,73),(130,72),(140,72),(150,70),
     (160,70),(170,67),(178,65),(178,62),(170,60),(162,56),(158,52),(150,59),
     (142,55),(140,50),(135,44),(130,42),(127,40),(126,38),(122,38),(120,32),
     (122,28),(118,25),(112,22),(108,18),(105,10),(103,8),(100,6),(97,10),
     (94,16),(92,21),(89,22),(86,20),(80,13),(77,8),(75,12),(72,20),(68,22),
     (62,25),(57,26),(54,26),(50,29),(48,30),(44,29),(40,31),(36,36),(30,36),
     (27,37),(23,36),(19,40),(15,44),(12,44),(8,44),(3,43),(0,40),(-2,37),(-6,36),(-10,36)],
    # Australia
    [(114,-22),(114,-30),(115,-35),(118,-35),(124,-33),(129,-32),(132,-32),
     (135,-35),(138,-35),(140,-38),(145,-38),(150,-37),(153,-32),(153,-27),
     (150,-22),(146,-19),(142,-11),(140,-17),(136,-12),(132,-11),(126,-14),
     (122,-17),(118,-20),(114,-22)],
    # UK
    [(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(1,51),(-3,50)],
    # Japan
    [(130,31),(133,34),(137,35),(140,37),(141,40),(142,43),(144,44),
     (142,41),(140,38),(137,34),(133,33),(130,31)],
]
# project polygons to pixels once
POLYS = [[proj(lon, lat) for lon, lat in poly] for poly in CONTINENTS]

def inside(px, py, poly):
    ins = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            ins = not ins
        j = i
    return ins

d.rectangle([mx0, my0, mx1 - 1, my1 - 1], outline=NAVY, width=1)
STEP = 6
gx = mx0 + 4
while gx < mx1 - 2:
    gy = my0 + 4
    while gy < my1 - 2:
        if any(inside(gx, gy, p) for p in POLYS):
            d.ellipse([gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6], fill=SLATE)
        gy += STEP
    gx += STEP

def pin(lon, lat, num):
    px, py = proj(lon, lat)
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=1)
    d.text((px, py), str(num), font=F_PIN, fill=(255, 255, 255), anchor="mm")

pin(56.3, 26.9, 1)    # Gulf / Qeshm
pin(36.4, 45.3, 2)    # Kerch
pin(114.1, 22.5, 3)   # Shenzhen
pin(82.0, 15.5, 4)    # Cyclone Akvan
# Voyager 1: gold star in the empty South Pacific
import math
sx, sy = proj(-155, -48)
star = []
for i in range(10):
    r = 11 if i % 2 == 0 else 4.5
    a = math.pi * i / 5 - math.pi / 2
    star.append((sx + r * math.cos(a), sy + r * math.sin(a)))
d.polygon(star, fill=GOLD, outline=(255, 255, 255))
d.text((sx, sy - 16), "5", font=F_PIN, fill=GOLD, anchor="mm")

# legend box bottom-right
leg = "1 GULF  ·  2 KERCH  ·  3 SHENZHEN  ·  4 AKVAN  ·  5 VOYAGER 1"
lw = d.textlength(leg, font=F_LEG)
lx0 = mx1 - lw - 16
ly0 = my1 - 20
d.rectangle([lx0, ly0, mx1 - 4, my1 - 4], fill=PAPER, outline=NAVY, width=1)
d.text((lx0 + 8, ly0 + 3), leg, font=F_LEG, fill=NAVY)

# ---------------------------------------------------------------- footer
d.text((W // 2, 956), "Sources: Reuters · AP · AFP · BBC · Al Jazeera  —  Every story above was first reported on Wednesday 18 November 2026.",
       font=F_FOOT, fill=GRAY, anchor="ma")

img.save("/home/hatch/workspace/makefun-test/news-image-entry/entry-v5.png", optimize=True)
print("saved entry-v5.png")
