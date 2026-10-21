"""Mumbai skyline for the scroll journey.

World is 6000 x 1000 units with the horizon at y=790, running west to east:
South Mumbai -> Marine Drive -> Worli -> Sea Link -> Bandra/BKC -> Thane -> Mumbra (AURA) -> Navi Mumbai -> airport.
Each layer is its own <svg> so the browser can pan and fade it without repainting (see main.js).
"""
import math
import random

W, H, HZ = 6000, 1000, 790
_r = random.Random(1966)


def n(v):
    return str(int(round(v)))


def rect(x, y, w, h):
    return f"M{n(x)} {n(y)}h{n(w)}v{n(h)}h{n(-w)}z"


class Layer:
    def __init__(self):
        self.sil = []       # silhouette fill paths
        self.hills = []     # lighter hill fills behind towers
        self.cables = []    # stroked lines (sea link)
        self.warm = []      # lit windows
        self.cool = []
        self.streaks = []   # light reflections on the water
        self.extra = []     # extra raw svg for the lights layer


city = Layer()


def windows(x, w, top, lit=0.34, cool=0.18, bottom=HZ - 8, col=9, row=12, office=False):
    """Scatter lit windows over a building face. Floors switch on in runs so it reads like a real tower."""
    pad = 5
    cols = max(1, int((w - pad * 2 + 3) // col))
    if cols < 1:
        return 0
    x0 = x + (w - (cols * col - 4)) / 2
    count = 0
    y = top + 9
    floor_on = _r.random() < 0.5
    while y < bottom - 6:
        if _r.random() < 0.28:
            floor_on = not floor_on
        p = lit * (1.7 if floor_on else 0.45)
        if office:
            p = lit * (2.2 if floor_on else 0.15)
        for c in range(cols):
            if _r.random() < p:
                target = city.cool if (office or _r.random() < cool) else city.warm
                target.append(rect(x0 + c * col, y, 4, 5))
                count += 1
        y += row
    return count


def streak(x, w, strength):
    """Vertical shimmer of a lit building on the water."""
    for _ in range(max(1, int(strength // 18))):
        sx = x + _r.random() * w
        city.streaks.append(rect(sx, HZ + 6 + _r.random() * 10, 2 + _r.random() * 2, 18 + _r.random() * 60))


def tower(x, w, top, crown="flat", lit=0.34, office=False, light=True):
    d = []
    if crown == "round":
        r = w / 2
        d.append(f"M{n(x)} {HZ}V{n(top + r)}A{n(r)} {n(r)} 0 0 1 {n(x + w)} {n(top + r)}V{HZ}z")
    elif crown == "slant":
        d.append(f"M{n(x)} {HZ}V{n(top + 34)}L{n(x + w)} {n(top)}V{HZ}z")
    elif crown == "taper":  # World One style
        d.append(rect(x, top + 60, w, HZ - top - 60))
        d.append(f"M{n(x + 4)} {n(top + 61)}L{n(x + w * 0.22)} {n(top)}H{n(x + w * 0.78)}L{n(x + w - 4)} {n(top + 61)}z")
        d.append(rect(x + w / 2 - 1.5, top - 34, 3, 35))
    else:
        d.append(rect(x, top, w, HZ - top))
    if crown == "spire":
        d.append(f"M{n(x + w / 2 - 5)} {n(top + 1)}L{n(x + w / 2)} {n(top - 52)}L{n(x + w / 2 + 5)} {n(top + 1)}z")
    elif crown == "antenna":
        d.append(rect(x + w * 0.3, top - 26, 2, 27))
        d.append(rect(x + w * 0.65, top - 16, 2, 17))
    elif crown == "stepped":
        d.append(rect(x + w * 0.12, top - 14, w * 0.76, 15))
        d.append(rect(x + w * 0.3, top - 26, w * 0.4, 13))
    elif crown == "crown":
        d.append(rect(x + w * 0.2, top - 18, w * 0.6, 19))
        d.append(rect(x - 2, top, w + 4, 4))
    elif crown == "deco":  # art-deco Marine Drive row
        d.append(rect(x + w * 0.35, top - 10, w * 0.3, 11))
    city.sil.extend(d)
    if light:
        off = {"round": w / 2, "slant": 34, "taper": 60}.get(crown, 0)
        c = windows(x, w, top + off, lit=lit, office=office)
        streak(x, w, c)


def fabric(x0, x1, lo=736, hi=772):
    """Low continuous city fabric so the skyline never has gaps."""
    x = x0
    while x < x1:
        w = _r.randint(18, 42)
        top = _r.randint(lo, hi)
        city.sil.append(rect(x, top, w + 1, HZ - top))
        if _r.random() < 0.6:
            windows(x, w, top, lit=0.22, col=8, row=10)
        x += w


def cluster(x0, x1, lo, hi, wmin=28, wmax=52, crowns=("flat", "flat", "crown", "stepped", "antenna"), gap=(2, 14), lit=0.34, office=False):
    x = x0
    while x < x1:
        w = _r.randint(wmin, wmax)
        tower(x, w, _r.randint(lo, hi), _r.choice(crowns), lit=lit, office=office)
        x += w + _r.randint(*gap)


def hill(points, layer=None):
    (layer or city).hills.append(points)


def back_row(x0, x1, lo, hi):
    """Hazier towers behind the main skyline for depth; a few lights only."""
    x = x0
    while x < x1:
        w = _r.randint(26, 48)
        top = _r.randint(lo, hi)
        city.hills.append(rect(x, top, w, HZ - top))
        windows(x, w, top, lit=0.12)
        x += w + _r.randint(8, 30)


back_row(980, 1360, 560, 660)
back_row(2140, 2690, 430, 560)
back_row(3660, 4100, 520, 620)
back_row(4280, 4560, 430, 560)
back_row(5030, 5290, 470, 580)


# ---------------------------------------------------------------- South Mumbai
fabric(150, 2700)

# Gateway of India: arch body, four domed turrets, sky visible through the arches
gw = [rect(238, 655, 254, 120), rect(318, 638, 94, 18)]
for tx, tw in ((238, 24), (296, 22), (412, 22), (468, 24)):
    gw.append(rect(tx, 606, tw, 50))
    gw.append(f"M{tx} 606A{tw / 2:.0f} {tw / 2:.0f} 0 0 1 {tx + tw} 606z")
    gw.append(rect(tx + tw / 2 - 1, 586, 2, 10))
gw.append(f"M350 598A15 15 0 0 1 380 598z")
gw.append(rect(350, 598, 30, 41))
gw.append(rect(200, 775, 330, 15))
GATEWAY = " ".join(gw)  # drawn on its own with a mask so the sky shows through the arches
gateway_holes = "M336 775V722Q336 690 365 680Q394 690 394 722V775z M262 775V742Q262 728 273 723Q284 728 284 742V775z M446 775V742Q446 728 457 723Q468 728 468 742V775z"

# Taj Mahal Palace + Taj tower
taj = [rect(540, 662, 340, 128)]
for cx in range(556, 880, 34):
    taj.append(f"M{cx - 6} 662A6 6 0 0 1 {cx + 6} 662z")
taj += [rect(540, 612, 32, 52), "M540 612A16 16 0 0 1 572 612z", rect(555, 588, 2, 10),
        rect(848, 612, 32, 52), "M848 612A16 16 0 0 1 880 612z", rect(863, 588, 2, 10),
        rect(612, 632, 20, 32), "M612 632A10 10 0 0 1 632 632z",
        rect(788, 632, 20, 32), "M788 632A10 10 0 0 1 808 632z",
        rect(676, 606, 68, 58),
        "M680 607C680 566 700 556 710 540C720 556 740 566 740 607z", rect(709, 520, 2, 22)]
city.sil.append(" ".join(taj))
windows(540, 340, 672, lit=0.42, row=14)
streak(540, 340, 120)
tower(905, 80, 572, "stepped", lit=0.45)

# Colaba / Nariman Point
cluster(1000, 1150, 676, 728, 26, 44)
tower(1160, 58, 540, "flat", lit=0.4, office=True)
tower(1226, 84, 506, "antenna", lit=0.42, office=True)
tower(1318, 50, 578, "stepped", lit=0.4, office=True)

# Marine Drive art-deco row (low, rounded) and the Queen's Necklace
x = 1380
while x < 1860:
    w = _r.randint(40, 66)
    tower(x, w, _r.randint(698, 734), "deco", lit=0.48)
    x += w + _r.randint(1, 6)

# Malabar Hill with towers on the ridge
hill("M1810 790C1880 760 1928 700 2000 690C2072 684 2124 722 2160 790z")
for tx, tw, tt, cr in ((1898, 26, 612, "flat"), (1936, 30, 570, "crown"), (1982, 24, 538, "spire"), (2026, 32, 592, "flat"), (2072, 28, 632, "stepped")):
    tower(tx, tw, tt, cr, lit=0.36)

# ---------------------------------------------------------------- Worli & Tardeo supertalls
tower(2188, 46, 388, "round", lit=0.4)    # twin towers
tower(2248, 46, 394, "round", lit=0.4)
cluster(2304, 2410, 520, 620, 30, 44)
tower(2420, 66, 330, "taper", lit=0.38)    # tallest
tower(2504, 44, 372, "spire", lit=0.36)
cluster(2560, 2700, 470, 640, 30, 50, crowns=("flat", "slant", "crown", "stepped"))

# ---------------------------------------------------------------- Bandra-Worli Sea Link
SL0, SL1 = 2700, 3640
deck = [rect(SL0, 757, SL1 - SL0, 9), rect(SL0, 752, SL1 - SL0, 3)]
for px in range(SL0 + 30, SL1, 58):
    deck.append(rect(px, 766, 7, 24))
city.sil.append(" ".join(deck))
for cx in (2955, 3385):
    city.sil.append(f"M{cx - 30} 790L{cx - 7} 590L{cx - 5} 436L{cx + 5} 436L{cx + 7} 590L{cx + 30} 790L{cx + 17} 790L{cx} 646L{cx - 17} 790z")
    for k in range(10):
        my = 452 + k * 13
        reach = 226 - k * 19
        city.cables.append(f"M{cx} {my}L{cx - reach} 754M{cx} {my}L{cx + reach} 754")
    city.extra.append(f'<circle cx="{cx}" cy="434" r="3.2" fill="#ff5a4e"/>')
# deck lamps
for lx in range(SL0 + 6, SL1, 16):
    city.extra.append(f'<circle cx="{lx}" cy="750" r="1.7" fill="#ffd9a0"/>')
    if lx % 48 == 6:
        city.streaks.append(rect(lx - 1, 796, 2.5, 30 + _r.random() * 36))

# ---------------------------------------------------------------- Bandra & BKC
fabric(3640, 4120, 740, 772)
cluster(3650, 3890, 560, 690, 30, 54)
cluster(3900, 4120, 572, 662, 70, 110, crowns=("flat", "stepped", "flat"), gap=(6, 18), lit=0.3, office=True)

# ---------------------------------------------------------------- Thane (after the creek)
fabric(4260, 5330, 742, 774)
hill("M4180 790C4240 730 4300 676 4380 660C4450 648 4520 690 4600 728C4640 748 4660 772 4680 790z")
cluster(4264, 4560, 468, 640, 32, 50, crowns=("flat", "crown", "crown", "stepped", "antenna"))

# ---------------------------------------------------------------- Mumbra & Parsik hill (AURA)
hill("M4520 790C4570 740 4640 640 4720 590C4770 562 4810 566 4860 600C4930 646 5010 708 5120 790z")
cluster(4570, 4770, 612, 704, 30, 46, crowns=("flat", "crown", "stepped"))
tower(4786, 44, 584, "crown", lit=0.5)     # the AURA marker sits above this one
cluster(4846, 5010, 616, 706, 30, 46, crowns=("flat", "crown", "stepped"))
AURA = (4808, 566)

# ---------------------------------------------------------------- Navi Mumbai
cluster(5020, 5300, 512, 650, 34, 56, crowns=("flat", "crown", "stepped", "slant"))

# ---------------------------------------------------------------- Navi Mumbai International Airport
ground = f'<path fill="#060a1c" d="M5290 {HZ}H{W}V{H}H5380C5340 900 5320 820 5290 {HZ}z"/>'
city.sil.append(rect(5366, 590, 12, 200) + " M5350 590L5394 590L5387 560L5357 560z " + rect(5356, 553, 32, 7) + rect(5371, 516, 2, 38))
city.sil.append(rect(5446, 744, 448, 46) +
                " M5420 754C5470 744 5512 716 5566 708C5612 702 5638 716 5675 696C5712 716 5738 702 5784 708C5838 716 5880 744 5930 754z")
# lit terminal glass and lotus-petal roof ribs
city.extra.append('<rect x="5452" y="750" width="436" height="36" fill="url(#glass)"/>')
ribs = []
for k in range(-4, 5):  # lotus petals opening from the entrance
    ex = 5675 + k * 58
    ey = 700 + abs(k) * 9
    ribs.append(f"M5675 786Q{5675 + k * 22} 744 {ex} {ey}")
city.extra.append(f'<path d="{" ".join(ribs)}" fill="none" stroke="#ffd9a0" stroke-width="1.4" opacity=".55"/>')
for lx in range(5440, W, 14):
    city.extra.append(f'<circle cx="{lx}" cy="812" r="1.6" fill="#fff4dc"/><circle cx="{lx + 7}" cy="836" r="1.5" fill="#8fb8ff"/>')
for gx in (5420, 5426, 5432):
    city.extra.append(f'<circle cx="{gx}" cy="824" r="2" fill="#7dffb0"/>')
city.extra.append('<circle cx="5372" cy="514" r="3" fill="#ff5a4e"/>')

# ---------------------------------------------------------------- Queen's Necklace lights (Marine Drive)
necklace = []
for i in range(46):
    t = i / 45
    x = 1370 + t * 500
    y = 798 + 14 * (4 * t * (1 - t))   # promenade curves toward the viewer
    necklace.append(f'<circle cx="{x:.0f}" cy="{y:.1f}" r="5.5" fill="#ffcf8a" opacity=".22"/><circle cx="{x:.0f}" cy="{y:.1f}" r="1.9" fill="#fff0cf"/>')
    if i % 2 == 0:
        city.streaks.append(rect(x - 1, y + 6, 2.5, 26 + _r.random() * 46))
city.extra.append("".join(necklace))
city.sil.append("M1360 802Q1620 830 1880 800V806Q1620 836 1360 808z")


def mid_svg():
    sil = " ".join(city.sil)
    hills = " ".join(city.hills)
    shimmer = "".join(
        f'<path d="M{_r.randint(0, W)} {y}h{_r.randint(60, 260)}" />' for y in range(806, 990, 9) for _ in range(5)
    )
    return f'''<svg class="layer-svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMinYMax meet" aria-hidden="true" focusable="false">
<defs>
<linearGradient id="sil" x1="0" y1="300" x2="0" y2="{HZ}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#1b1d44"/><stop offset="1" stop-color="#0a0e28"/></linearGradient>
<linearGradient id="hillg" x1="0" y1="560" x2="0" y2="{HZ}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#2a2a5a"/><stop offset="1" stop-color="#14173a"/></linearGradient>
<linearGradient id="water" x1="0" y1="{HZ}" x2="0" y2="{H}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#0b1236" stop-opacity=".42"/><stop offset=".35" stop-color="#060b26" stop-opacity=".82"/><stop offset="1" stop-color="#030616" stop-opacity=".97"/></linearGradient>
<linearGradient id="refl" x1="0" y1="{HZ}" x2="0" y2="960" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="arch"><rect x="0" y="0" width="1000" height="1000" fill="#fff"/><path d="{gateway_holes}" fill="#000"/></mask>
<mask id="reflmask"><rect x="0" y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#refl)"/></mask>
</defs>
<rect x="0" y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#water)"/>
<g class="shimmer" stroke="#c9b6ff" stroke-opacity=".10" stroke-width="1.2">{shimmer}</g>
<g mask="url(#reflmask)" opacity=".5"><g transform="matrix(1 0 0 -.62 0 {HZ * 1.62:.1f})"><path fill="url(#hillg)" d="{hills}"/><path fill="#05081c" d="{sil} {GATEWAY}"/></g></g>
{ground}
<path fill="url(#hillg)" d="{hills}"/>
<path fill="url(#sil)" d="{sil}"/>
<path fill="url(#sil)" mask="url(#arch)" d="{GATEWAY}"/>
<path fill="none" stroke="url(#sil)" stroke-width="1.6" d="{" ".join(city.cables)}"/>
</svg>'''


def lights_svg():
    return f'''<svg class="layer-svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMinYMax meet" aria-hidden="true" focusable="false">
<defs>
<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd9a0" stop-opacity=".9"/><stop offset="1" stop-color="#ff9f5a" stop-opacity=".55"/></linearGradient>
<linearGradient id="strk" x1="0" y1="{HZ}" x2="0" y2="900" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ffcf8a" stop-opacity=".55"/><stop offset="1" stop-color="#ffcf8a" stop-opacity="0"/></linearGradient>
</defs>
<path fill="url(#strk)" d="{" ".join(city.streaks)}"/>
<path fill="#ffd9a0" d="{" ".join(city.warm)}"/>
<path fill="#d6e6ff" opacity=".9" d="{" ".join(city.cool)}"/>
{"".join(city.extra)}
</svg>'''


# ---------------------------------------------------------------- far layer (hazy, pans slower)
def far_svg():
    fw = 3800
    far = Layer()
    towers = []
    x = 60
    while x < 2500:
        w = _r.randint(14, 36)
        top = _r.randint(650, 770) if _r.random() < 0.8 else _r.randint(560, 650)
        towers.append(rect(x, top, w, HZ - top))
        x += w + _r.randint(0, 18)
    ridge_back = "M1900 790C2050 700 2180 640 2320 650C2460 660 2560 600 2700 580C2840 562 2960 620 3080 600C3220 576 3360 540 3500 572C3640 604 3720 640 3800 650V790z"
    ridge_front = "M2300 790C2400 740 2520 700 2640 704C2760 708 2860 676 2980 680C3120 684 3240 650 3380 664C3520 678 3660 700 3800 712V790z"
    return f'''<svg class="layer-svg" viewBox="0 0 {fw} {H}" preserveAspectRatio="xMinYMax meet" aria-hidden="true" focusable="false">
<path fill="#3a2f78" fill-opacity=".16" d="{ridge_back}"/>
<path fill="#2b2566" fill-opacity=".24" d="{ridge_front}"/>
<path fill="#221f5c" fill-opacity=".30" d="{" ".join(towers)}"/>
</svg>'''


# ---------------------------------------------------------------- foreground (pans faster)
def palm(x, base, h, lean):
    tx, ty = x + lean, base - h
    trunk = f"M{x - 5} {base}Q{x + lean * 0.3:.0f} {base - h * 0.5:.0f} {tx - 2} {ty}L{tx + 2} {ty}Q{x + lean * 0.3 + 6:.0f} {base - h * 0.5:.0f} {x + 5} {base}z"
    fronds = []
    for ang, ln, droop in ((-160, 96, 40), (-130, 84, 26), (-95, 66, 6), (-60, 84, 22), (-25, 98, 44), (-200, 80, 52), (20, 76, 56)):
        a = math.radians(ang)
        ex, ey = tx + math.cos(a) * ln, ty + math.sin(a) * ln * 0.55 + droop
        mx, my = tx + math.cos(a) * ln * 0.5, ty + math.sin(a) * ln * 0.55 - 14
        fronds.append(f"M{tx} {ty}Q{mx:.0f} {my:.0f} {ex:.0f} {ey:.0f}Q{mx:.0f} {my + 12:.0f} {tx} {ty + 4}z")
    return trunk + " " + " ".join(fronds)


def near_svg():
    nw = 7600
    parts = [palm(1260, 1000, 300, 34), palm(1360, 1000, 360, -26), palm(1450, 1000, 250, 18)]
    # sea wall with tetrapods along the promenade
    wall = ["M0 1000V968"]
    x = 0
    while x < 2600:
        wall.append(f"L{x + 14} {_r.randint(946, 962)}L{x + 28} {_r.randint(960, 970)}")
        x += 28
    wall.append("L2600 1000z")
    parts.append("".join(wall))
    # mangroves on the creek
    for _ in range(40):
        mx = _r.randint(5000, 5700)
        mh = _r.randint(18, 46)
        parts.append(f"M{mx - 16} 1000Q{mx} {1000 - mh * 2} {mx + 16} 1000z")
    # airport approach light stanchions
    for k in range(8):
        ax = 6900 + k * 80
        parts.append(rect(ax, 930 - k * 3, 4, 70 + k * 3) + rect(ax - 18, 928 - k * 3, 40, 3))
    lamps = "".join(f'<circle cx="{6900 + k * 80 + 2}" cy="{924 - k * 3}" r="3" fill="#fff4dc"/>' for k in range(8))
    return f'''<svg class="layer-svg" viewBox="0 0 {nw} {H}" preserveAspectRatio="xMinYMax meet" aria-hidden="true" focusable="false">
<path fill="#04061a" d="{" ".join(parts)}"/>{lamps}
</svg>'''


# world-anchored labels (x, y in world units) for the HTML overlay
LABELS = [
    (365, 560, "Gateway of India"),
    (1620, 668, "Marine Drive"),
    (2453, 270, "Worli"),
    (3170, 410, "Bandra–Worli Sea Link"),
    (4010, 540, "BKC"),
    (4400, 440, "Thane"),
    (5160, 470, "Navi Mumbai"),
    (5670, 650, "Navi Mumbai International Airport"),
]


def mumbra_svg(vb=(4300, 360, 1040, 640)):
    """Static night crop around Mumbra for the AURA art (re-uses the generated city).
    Returns the two SVGs plus CSS that pins the light beam to the AURA tower for this crop."""
    x0, y0, w, h = vb
    box = f'viewBox="{x0} {y0} {w} {h}" preserveAspectRatio="xMidYMax slice"'
    full = f'viewBox="0 0 {W} {H}" preserveAspectRatio="xMinYMax meet"'
    ax, ay = AURA
    s = f"max({100 / w:.5f}cqw, {100 / h:.5f}cqh)"
    beam = f"left:calc(50% + {ax - x0 - w / 2:.0f} * {s});bottom:calc({y0 + h - ay:.0f} * {s})"
    return mid_svg().replace(full, box), lights_svg().replace(full, box), beam
