#!/usr/bin/env python3
"""Draw the news-image-20261120 entry picture.

A single 1024x1024 PNG summarising the world news of Friday
20 November 2026 as a 3x3 grid of pictogram panels.  Everything is
drawn with PIL primitives only -- no external images, no network --
and the output is fully deterministic (same bytes on every run).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas

W = H = 1024
BG = (11, 19, 43)            # deep navy
WHITE = (255, 255, 255)
AMBER = (255, 197, 61)
INK = (16, 26, 48)           # pictogram / label ink on bright tiles
RED = (217, 4, 41)
ORANGE = (255, 133, 0)
FLAME = (255, 183, 3)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def fit_font(draw, text, max_w, start):
    """Largest bold font (<= start) that keeps text within max_w."""
    size = start
    while size > 10:
        f = font(size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(10)


def centered(draw, cx, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text((cx - w / 2, y), text, font=f, fill=fill)


# ------------------------------------------------------------ pictograms
# Each painter receives the draw context and the pictogram box
# (x, y, w, h) inside its panel and draws in INK unless noted.

def pic_kyiv(d, x, y, w, h):
    """Missile diving over a city skyline."""
    base = y + h
    # skyline
    for bx, bw, bh in ((0, 44, 46), (50, 34, 66), (90, 48, 38),
                       (196, 38, 58), (240, 46, 42)):
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=INK)
    for wx, wy in ((14, base - 34), (64, base - 50), (106, base - 24),
                   (210, base - 42), (256, base - 28)):
        d.rectangle([x + wx, wy, x + wx + 7, wy + 9], fill=AMBER)
    # missile: nose low-left, tail high-right (kept clear of the edges)
    nx, ny = x + 122, y + 76          # nose tip
    tx, ty = x + 214, y + 24          # tail end
    d.line([tx, ty, nx, ny], fill=INK, width=17)
    d.polygon([(nx, ny), (nx + 34, ny - 6), (nx + 12, ny + 22)], fill=INK)
    # fins
    d.polygon([(tx, ty), (tx - 26, ty + 6), (tx - 4, ty + 24)], fill=INK)
    d.polygon([(tx, ty), (tx - 4, ty - 16), (tx + 16, ty + 8)], fill=INK)
    # flame + motion streaks
    d.polygon([(tx + 2, ty - 2), (tx + 30, ty - 18), (tx + 20, ty + 10)],
              fill=ORANGE)
    d.polygon([(tx + 4, ty), (tx + 19, ty - 9), (tx + 14, ty + 7)],
              fill=FLAME)
    for dx, dy in ((40, -20), (54, -4), (32, -34)):
        d.line([tx + dx - 22, ty + dy + 13, tx + dx, ty + dy],
               fill=WHITE, width=5)


def pic_trump_iran(d, x, y, w, h):
    """White House beside a calendar page."""
    base = y + h
    # White House (left)
    hx, hw = x + 6, 158
    d.polygon([(hx - 4, y + 34), (hx + hw / 2, y + 8), (hx + hw + 4, y + 34)],
              fill=INK)
    d.rectangle([hx, y + 36, hx + hw, base], fill=WHITE)
    d.rectangle([hx, y + 36, hx + hw, base], outline=INK, width=4)
    for i in range(4):
        cx = hx + 18 + i * 34
        d.rectangle([cx, y + 46, cx + 10, base - 6], fill=INK)
    d.rectangle([hx + hw / 2 - 9, base - 30, hx + hw / 2 + 9, base], fill=INK)
    # calendar (right)
    cx, cy, cw, ch = x + 182, y + 22, 104, 92
    d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=8,
                        fill=WHITE, outline=INK, width=4)
    d.rectangle([cx, cy, cx + cw, cy + 24], fill=RED)
    for rx in (cx + 22, cx + cw - 22):
        d.line([rx, cy - 8, rx, cy + 10], fill=INK, width=7)
    for r in range(2):
        for c in range(3):
            d.rectangle([cx + 16 + c * 28, cy + 38 + r * 26,
                         cx + 32 + c * 28, cy + 52 + r * 26], fill=INK)
    # big "27" feel: clock hands on the calendar band
    d.ellipse([cx + cw - 34, cy + 30, cx + cw - 8, cy + 56],
              outline=INK, width=4)
    d.line([cx + cw - 21, cy + 43, cx + cw - 21, cy + 34], fill=INK, width=3)
    d.line([cx + cw - 21, cy + 43, cx + cw - 14, cy + 47], fill=INK, width=3)


def pic_anthropic(d, x, y, w, h):
    """Rising chart with an arrow, robot head beside it."""
    base = y + h
    # axes + rising line
    d.line([x + 8, y + 8, x + 8, base], fill=INK, width=5)
    d.line([x + 8, base, x + 150, base], fill=INK, width=5)
    pts = [(x + 16, base - 16), (x + 52, base - 34), (x + 82, base - 28),
           (x + 112, base - 62), (x + 140, base - 84)]
    d.line(pts, fill=INK, width=8, joint="curve")
    d.polygon([(x + 140, base - 84), (x + 118, base - 82), (x + 136, base - 62)],
              fill=INK)
    # robot head (right)
    rx, ry, rw, rh = x + 176, y + 30, 104, 78
    d.line([rx + rw / 2, ry, rx + rw / 2, ry - 16], fill=INK, width=6)
    d.ellipse([rx + rw / 2 - 8, ry - 26, rx + rw / 2 + 8, ry - 10], fill=INK)
    d.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=14,
                        fill=WHITE, outline=INK, width=5)
    for ex in (rx + 26, rx + rw - 38):
        d.ellipse([ex, ry + 24, ex + 14, ry + 38], fill=INK)
    d.line([rx + 30, ry + rh - 20, rx + rw - 30, ry + rh - 20],
           fill=INK, width=5)
    d.rectangle([rx - 10, ry + 28, rx, ry + 52], fill=INK)
    d.rectangle([rx + rw, ry + 28, rx + rw + 10, ry + 52], fill=INK)


def pic_taiwan(d, x, y, w, h):
    """Falling chart stopped by a raised hand."""
    base = y + h
    d.line([x + 8, y + 8, x + 8, base], fill=INK, width=5)
    d.line([x + 8, base, x + 158, base], fill=INK, width=5)
    pts = [(x + 16, y + 22), (x + 52, y + 40), (x + 84, y + 34),
           (x + 116, y + 68), (x + 144, y + 92)]
    d.line(pts, fill=RED, width=8, joint="curve")
    d.polygon([(x + 144, y + 92), (x + 122, y + 88), (x + 138, y + 70)],
              fill=RED)
    # stop hand (right): palm + four fingers + thumb, white on the tile
    hx, hy = x + 192, y + 26
    for i, fh in enumerate((42, 52, 48, 38)):
        fx = hx + i * 22
        d.rounded_rectangle([fx, hy + 54 - fh, fx + 19, hy + 58],
                            radius=8, fill=WHITE, outline=INK, width=4)
    d.rounded_rectangle([hx - 2, hy + 50, hx + 88, base], radius=12,
                        fill=WHITE, outline=INK, width=4)
    d.polygon([(hx - 2, hy + 64), (hx - 24, hy + 80), (hx - 2, hy + 90)],
              fill=WHITE, outline=INK, width=4)


def pic_hormuz(d, x, y, w, h):
    """Tanker at sea, burst at the bow, mine in the water."""
    base = y + h
    sea = base - 18
    # hull + deck gear
    d.polygon([(x + 18, sea - 34), (x + 252, sea - 34), (x + 232, sea),
               (x + 40, sea)], fill=INK)
    d.rectangle([x + 52, sea - 52, x + 168, sea - 34], fill=INK)
    d.rectangle([x + 196, sea - 66, x + 226, sea - 34], fill=INK)
    d.rectangle([x + 204, sea - 78, x + 218, sea - 66], fill=INK)
    # burst at the bow (right)
    cx, cy = x + 258, sea - 44
    for ang in range(0, 360, 45):
        r1, r2 = 8, 26 if ang % 90 == 0 else 19
        d.line([cx + r1 * math.cos(math.radians(ang)),
                cy + r1 * math.sin(math.radians(ang)),
                cx + r2 * math.cos(math.radians(ang)),
                cy + r2 * math.sin(math.radians(ang))], fill=ORANGE, width=6)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=FLAME)
    # mine in the water (left), riding high enough to read clearly
    mx, my = x + 38, sea - 2
    d.ellipse([mx - 14, my - 14, mx + 14, my + 14], fill=INK)
    for ang in range(0, 360, 60):
        d.line([mx, my, mx + 20 * math.cos(math.radians(ang)),
                my + 20 * math.sin(math.radians(ang))], fill=INK, width=4)
    # waves
    for wx in range(0, 290, 48):
        d.arc([x + wx, sea + 2, x + wx + 40, sea + 22], 180, 360,
              fill=INK, width=4)


def pic_cyclone(d, x, y, w, h):
    """Cyclone spiral over two small houses."""
    cx, cy = x + w / 2, y + 46
    pts = []
    for t in range(0, 301):
        ang = t * math.pi / 42.0
        r = 3 + t * 0.16
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.78))
    d.line(pts, fill=INK, width=9, joint="curve")
    base = y + h
    for hx, s in ((x + 58, 1.0), (x + 196, 0.8)):
        hw, hh = 56 * s, 34 * s
        d.rectangle([hx, base - hh, hx + hw, base], fill=INK)
        d.polygon([(hx - 6, base - hh), (hx + hw / 2, base - hh - 22 * s),
                   (hx + hw + 6, base - hh)], fill=INK)
        d.rectangle([hx + hw / 2 - 6, base - 18 * s, hx + hw / 2 + 6, base],
                    fill=AMBER)


def pic_voyager(d, x, y, w, h):
    """Deep-space probe: big dish, body, long boom; stars and the Sun."""
    # stars (dark, so they read on the pale tile)
    for sx, sy in ((16, 14), (58, 40), (30, 84), (252, 16), (272, 60),
                   (238, 96), (120, 10), (196, 30)):
        d.line([x + sx - 6, y + sy, x + sx + 6, y + sy], fill=INK, width=3)
        d.line([x + sx, y + sy - 6, x + sx, y + sy + 6], fill=INK, width=3)
    # Sun, far away (top right)
    sx, sy = x + 252, y + 30
    d.ellipse([sx - 13, sy - 13, sx + 13, sy + 13], fill=FLAME)
    for ang in range(0, 360, 45):
        d.line([sx + 18 * math.cos(math.radians(ang)),
                sy + 18 * math.sin(math.radians(ang)),
                sx + 26 * math.cos(math.radians(ang)),
                sy + 26 * math.sin(math.radians(ang))], fill=FLAME, width=4)
    # dish (left): ellipse + feed mast
    dx, dy = x + 74, y + 62
    d.ellipse([dx - 44, dy - 44, dx + 44, dy + 44], fill=WHITE)
    d.ellipse([dx - 44, dy - 44, dx + 44, dy + 44], outline=INK, width=5)
    d.ellipse([dx - 16, dy - 16, dx + 16, dy + 16], outline=INK, width=4)
    d.line([dx, dy, dx + 52, dy + 6], fill=INK, width=5)
    # bus + boom
    d.rectangle([dx + 48, dy - 12, dx + 84, dy + 18], fill=INK)
    d.line([dx + 84, dy + 2, dx + 168, dy + 40], fill=INK, width=6)
    d.ellipse([dx + 162, dy + 34, dx + 178, dy + 50], fill=INK)
    d.line([dx + 60, dy + 18, dx + 96, dy + 52], fill=INK, width=5)


def pic_gta6(d, x, y, w, h):
    """Game controller in front of a palm tree and skyline."""
    base = y + h
    # skyline silhouette
    for bx, bw, bh in ((0, 34, 40), (206, 40, 52), (252, 36, 36)):
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=INK)
    # palm: curved trunk + fronds + coconuts
    tx = x + 52
    d.line([tx, base, tx + 10, y + 52, tx + 26, y + 30], fill=INK,
           width=11, joint="curve")
    for ang in (180, 215, 250, 290, 325):
        ex = tx + 26 + 44 * math.cos(math.radians(ang))
        ey = y + 30 + 30 * math.sin(math.radians(ang))
        d.line([tx + 26, y + 30, ex, ey], fill=INK, width=7)
    d.ellipse([tx + 16, y + 28, tx + 28, y + 40], fill=INK)
    d.ellipse([tx + 28, y + 32, tx + 40, y + 44], fill=INK)
    # controller body
    cx, cy, cw, ch = x + 96, y + 44, 176, 66
    d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=30,
                        fill=WHITE, outline=INK, width=5)
    # d-pad
    px, py = cx + 36, cy + ch / 2
    d.rectangle([px - 8, py - 20, px + 8, py + 20], fill=INK)
    d.rectangle([px - 20, py - 8, px + 20, py + 8], fill=INK)
    # buttons
    for bx, by, col in ((cx + cw - 42, cy + 22, RED),
                        (cx + cw - 24, cy + 42, INK)):
        d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=col)
    d.line([cx + 78, cy + 16, cx + 98, cy + 16], fill=INK, width=5)


def pic_cricket(d, x, y, w, h):
    """Cricket bat angled across the panel, red ball beside it."""
    # bat blade (long polygon) + handle
    d.polygon([(x + 96, y + h - 4), (x + 122, y + h - 4),
               (x + 176, y + 34), (x + 152, y + 22)], fill=WHITE)
    d.polygon([(x + 96, y + h - 4), (x + 122, y + h - 4),
               (x + 176, y + 34), (x + 152, y + 22)], outline=INK, width=5)
    d.line([x + 164, y + 28, x + 196, y + 2], fill=INK, width=11)
    d.line([x + 104, y + h - 22, x + 158, y + 44], fill=INK, width=3)
    # ball with seam
    bx, by, r = x + 226, y + 74, 30
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=RED)
    d.arc([bx - r + 8, by - r + 5, bx + r - 8, by + r - 5], 100, 260,
          fill=WHITE, width=4)
    d.arc([bx - r + 8, by - r + 5, bx + r - 8, by + r - 5], 280, 80,
          fill=WHITE, width=4)
    # motion ticks
    for dx in (-52, -40):
        d.line([bx + dx - 14, by - 12, bx + dx, by - 12], fill=INK, width=4)
        d.line([bx + dx - 14, by + 8, bx + dx, by + 8], fill=INK, width=4)


# ---------------------------------------------------------------- panels

PANELS = [
    ((255, 197, 61), pic_kyiv,
     ["KYIV HIT BY 4", "BALLISTIC MISSILES"]),
    ((255, 123, 84), pic_trump_iran,
     ["TRUMP: IRAN DECISION", "WAITS TO 2027"]),
    ((138, 201, 38), pic_anthropic,
     ["ANTHROPIC SHARES", "JUMP 17% IN DEBUT"]),
    ((255, 89, 94), pic_taiwan,
     ["TAIWAN CURBS", "SHORT-SELLING AS", "STOCKS SLIDE"]),
    ((76, 201, 240), pic_hormuz,
     ["TANKER HITS MINE", "STRAIT OF HORMUZ"]),
    ((184, 146, 255), pic_cyclone,
     ["CYCLONE AKVAN", "300,000 EVACUATED"]),
    ((144, 224, 239), pic_voyager,
     ["VOYAGER 1 NOW ONE", "LIGHT-DAY FROM EARTH"]),
    ((255, 112, 166), pic_gta6,
     ["GTA 6 SALES PASS", "$1.8 BILLION"]),
    ((167, 201, 87), pic_cricket,
     ["NICHOLLS HITS 113", "NOT OUT vs INDIA"]),
]

MARGIN, GAP = 24, 16
GRID_TOP = 178
PANEL_W = (W - 2 * MARGIN - 2 * GAP) // 3          # 314
PANEL_H = (H - GRID_TOP - MARGIN - 2 * GAP) // 3   # 262
PIC_H = 116


def draw_panel(d, px, py, tile, painter, lines):
    d.rounded_rectangle([px, py, px + PANEL_W, py + PANEL_H], radius=18,
                        fill=tile)
    painter(d, px + 12, py + 10, PANEL_W - 24, PIC_H)
    # label lines, auto-fitted, in the space under the pictogram
    top = py + PIC_H + 22
    avail = py + PANEL_H - 8 - top
    step = avail // len(lines)
    size = min(36, step - 4)
    for i, line in enumerate(lines):
        f = fit_font(d, line, PANEL_W - 20, size)
        tw = d.textlength(line, font=f)
        th = f.size
        ly = top + i * step + (step - th) // 2
        d.text((px + (PANEL_W - tw) / 2, ly), line, font=f, fill=INK)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # header band
    title = "FRIDAY 20 NOVEMBER 2026"
    tf = fit_font(d, title, W - 48, 62)
    centered(d, W / 2, 26, title, tf, WHITE)
    sub = "THE WORLD IN ONE PICTURE"
    sf = fit_font(d, sub, W - 200, 32)
    centered(d, W / 2, 108, sub, sf, AMBER)
    d.rectangle([MARGIN, 156, W - MARGIN, 161], fill=AMBER)

    for idx, (tile, painter, lines) in enumerate(PANELS):
        r, c = divmod(idx, 3)
        px = MARGIN + c * (PANEL_W + GAP)
        py = GRID_TOP + r * (PANEL_H + GAP)
        draw_panel(d, px, py, tile, painter, lines)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
