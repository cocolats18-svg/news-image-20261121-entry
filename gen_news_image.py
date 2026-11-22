#!/usr/bin/env python3
"""Draw entry.png for news-image-20261121 with Pillow (build-time only).

Slate verified 2026-11-22 against AP / Reuters / NPR reporting of
Saturday 21 November 2026. Every number on the image comes from those
reports; no faces, no leader likenesses, flat vector pictograms only.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.expanduser("~/workspace/bountyhawk/news-image-20261121-entry/entry.png")
W = H = 1024
BG = (247, 243, 232)
NAVY = (15, 42, 68)
INK = (20, 24, 30)
GREY = (70, 75, 85)
RED = (178, 34, 34)
TEAL = (0, 110, 110)
GOLD = (186, 132, 0)
WHITE = (255, 255, 255)
GOLDLT = (255, 214, 90)
LINE = (210, 205, 190)


def font(size, bold=True):
    p = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
         else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(p, size)


def wrap(draw, text, fnt, max_w, x, y, fill, spacing=4):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- masthead ---
d.rectangle([0, 0, W, 150], fill=NAVY)
d.text((36, 18), "THE WORLD IN ONE DAY", font=font(42), fill=WHITE)
d.text((36, 74), "SATURDAY  21  NOVEMBER  2026", font=font(36), fill=GOLDLT)
d.text((36, 122), "World news, summed up in one image", font=font(19, False),
       fill=(200, 215, 230))
# small globe pictogram, top right
cx, cy = 940, 75
d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], outline=GOLDLT, width=4)
d.ellipse([cx - 22, cy - 42, cx + 22, cy + 42], outline=GOLDLT, width=2)
d.line([cx - 42, cy, cx + 42, cy], fill=GOLDLT, width=2)

# --- lead panel: Poland / NATO ---
lx, ly, lw, lh = 36, 168, 952, 216
d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=WHITE,
                    outline=LINE, width=2)
d.rounded_rectangle([lx, ly, lx + lw, ly + 40], radius=16, fill=RED)
d.rectangle([lx, ly + 26, lx + lw, ly + 40], fill=RED)
d.text((lx + 16, ly + 8), "LEAD  •  POLAND  •  NATO", font=font(19), fill=WHITE)
# shield pictogram
sx, sy = lx + 78, ly + 78
d.polygon([(sx, sy), (sx + 52, sy + 14), (sx + 52, sy + 62),
           (sx, sy + 92), (sx - 52, sy + 62), (sx - 52, sy + 14)],
          fill=NAVY, outline=WHITE, width=3)
d.text((sx - 13, sy + 38), "NATO", font=font(15), fill=WHITE)
wrap(d, "Russian missiles land in Poland", font(33), 640, lx + 168, ly + 58, INK)
wrap(d, "NATO chief Rutte in Warsaw: the alliance will defend every inch "
        "of Polish territory. Warsaw calls it a deliberate provocation.",
     font(19, False), 640, lx + 168, ly + 122, GREY)

# --- six panels ---
def card(x, y, w, h, accent, tag, headline, sub):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=WHITE,
                        outline=LINE, width=2)
    d.rounded_rectangle([x, y, x + w, y + 34], radius=14, fill=accent)
    d.rectangle([x, y + 20, x + w, y + 34], fill=accent)
    d.text((x + 14, y + 6), tag, font=font(16), fill=WHITE)
    y2 = wrap(d, headline, font(21), w - 28, x + 14, y + 44, INK)
    wrap(d, sub, font(15, False), w - 28, x + 14, y2 + 6, GREY)


stories = [
    (TEAL, "UKRAINE",
     "Strike hits Zelenskyy's hometown",
     "Kryvyi Rih: 2 killed, 60 hurt in a double-tap missile attack."),
    (RED, "MEXICO",
     "Cartel boss 'El Chapo Isidro' caught",
     "FBI most-wanted fugitive seized in Sinaloa; 11 dead in the raid."),
    (GOLD, "CLIMATE  •  COP31",
     "COP31 talks run into overtime",
     "Antalya draft leaves out fossil fuels; no final deal yet."),
    (NAVY, "BRITAIN  •  EU",
     "UK and EU strike Brexit reset deal",
     "Food trade eased; youth scheme for 100,000; worth £17bn a year."),
    (TEAL, "INDIA  •  CYCLONE",
     "Cyclone Akvan weakens over Odisha",
     "Storm fades to a low after landfall; no deaths reported."),
    (RED, "NIGERIA",
     "Boat capsizes on way to funeral",
     "At least 24 dead in Bayelsa State as rescue goes on."),
]
cw, ch, gap = 304, 186, 20
for i, (accent, tag, head, sub) in enumerate(stories):
    x = 36 + (i % 3) * (cw + gap)
    y = 404 + (i // 3) * (ch + gap)
    card(x, y, cw, ch, accent, tag, head, sub)

# --- bottom strip ---
by = 404 + 2 * ch + gap + 16
d.rounded_rectangle([36, by, 988, by + 96], radius=14, fill=NAVY)
d.text((56, by + 12), "ALSO ON 21 NOVEMBER", font=font(19), fill=GOLDLT)
wrap(d, "Peru quake 6.7 shakes Lima  •  ICJ genocide ruling: sanctions urged "
        "on Myanmar  •  US markets reel from Friday's AI sell-off",
     font(18, False), 900, 56, by + 44, WHITE)
d.text((36, 994), "Events reported on Saturday 21 November 2026  •  One day, one image",
       font=font(15, False), fill=(110, 110, 110))

img.save(OUT, optimize=True)
print("saved", img.size, os.path.getsize(OUT), "bytes")
