import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 227)
INK = (20, 33, 61)
NAVY = (15, 30, 61)
RED = (193, 39, 45)
GOLD = (217, 164, 65)
TEAL = (14, 124, 123)
SKY = (127, 179, 213)
WHITE = (255, 255, 255)
BD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
RG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

LEAD_HEAD = "Trump, Xi and Putin hold first three-way meeting in Shenzhen"
LEAD_SUM = ("At the APEC summit the three leaders released a joint \u201cpeace "
            "declaration\u201d on nuclear arms control and global security.")
STORIES = [
    ("JUSTICE", INK, "scales",
     "ICJ rules Myanmar sought to destroy the Rohingya",
     "Court: military likely intended to destroy a substantial part of the minority."),
    ("WEATHER", TEAL, "spiral",
     "Cyclone Akvan bears down on Odisha",
     "Landfall expected 20 Nov; schools closed, evacuations under way."),
    ("CULTURE", GOLD, "star",
     "Van Gogh sells for a record $190.4 million",
     "Record auction price after a dispute over its Nazi-era history."),
    ("SPACE", SKY, "rocket",
     "Voyager 1 hits one light-day from Earth",
     "First human-made object that far out; a signal now takes 24 hours."),
    ("AMERICAS", NAVY, "handshake",
     "U.S. and Venezuela sign military deal",
     "Agreement to restore cooperation, under a year after Maduro's ouster."),
]
TICKER1 = "Fiji declares disaster over drought"
TICKER2 = "UN: North Korea expanding enrichment"
TICKER3 = "Also that day: Anthropic valued at $1.5 trillion; Musk: \u201cI'm not MAGA.\u201d"
FOOTER = "All stories first reported 20 November 2026"
DATE = "FRIDAY 20 NOVEMBER 2026"


def font(bold, size):
    return ImageFont.truetype(BD if bold else RG, int(size))


def text_w(d, s, f):
    return int(d.textlength(s, font=f))


def wrap_text(d, text, f, max_width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if text_w(d, trial, f) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            while text_w(d, w, f) > max_width and len(w) > 1:
                cut = len(w) - 1
                while text_w(d, w[:cut], f) > max_width:
                    cut -= 1
                lines.append(w[:cut])
                w = w[cut:]
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, xy, lines, f, fill, leading):
    x, y = int(xy[0]), int(xy[1])
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += int(leading)
    return y


def draw_centered(d, cx, y, lines, f, fill, leading):
    for ln in lines:
        d.text((int(cx - text_w(d, ln, f) / 2), int(y)), ln, font=f, fill=fill)
        y += int(leading)
    return y


def rect(d, box, fill, outline=None, width=1):
    d.rectangle([int(box[0]), int(box[1]), int(box[2]), int(box[3])],
                fill=fill, outline=outline, width=int(width))


def line(d, p1, p2, width, fill):
    d.line([int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1])], fill=fill, width=int(width))


def chip(d, x, y, w, label, col):
    f = font(True, 16)
    cw = min(int(w), text_w(d, label, f) + 20)
    ch = 28
    d.rounded_rectangle([int(x), int(y), int(x) + cw, int(y) + ch], radius=8, fill=col)
    d.text((int(x) + 10, int(y) + 5), label, font=f, fill=WHITE)
    return int(y) + ch


def draw_star(d, cx, cy, r, col):
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else int(r * 0.45)
        pts.append((int(cx + rr * math.cos(ang)), int(cy + rr * math.sin(ang))))
    d.polygon(pts, fill=col)


def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY)
    d.arc([cx - int(r * 0.6), cy - r, cx + int(r * 0.6), cy + r], 0, 360, fill=GOLD, width=2)
    d.arc([cx - r, cy - int(r * 0.5), cx + r, cy + int(r * 0.5)], 0, 360, fill=GOLD, width=1)
    for ly in (-1, 0, 1):
        yy = cy + ly * int(r * 0.45)
        w = int((r * 0.9) * (1 - abs(ly) * 0.45))
        d.line([cx - w, yy, cx + w, yy], fill=SKY, width=1)
    for (px, py) in [(cx - 12, cy - 20), (cx + 14, cy - 4), (cx - 2, cy + 18)]:
        if (px - cx) ** 2 + (py - cy) ** 2 <= (r - 6) ** 2:
            d.polygon([(px, py - 6), (px + 8, py - 2), (px + 4, py + 8), (px - 6, py + 4)], fill=TEAL)
    for (sx, sy) in [(cx - r - 14, cy - r), (cx + r + 12, cy + r - 8), (cx + r, cy - r - 12)]:
        draw_star(d, sx, sy, 6, GOLD)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)


def draw_icon(d, cx, cy, r, kind):
    bg = {"globe": TEAL, "scales": INK, "spiral": GOLD, "star": RED,
          "rocket": SKY, "handshake": NAVY}.get(kind, INK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=bg, outline=PAPER, width=2)
    w = 3
    if kind == "globe":
        d.ellipse([cx - int(r * 0.55), cy - r, cx + int(r * 0.55), cy + r], outline=WHITE, width=2)
    elif kind == "scales":
        d.line([cx, cy - r, cx, cy + int(r * 0.6)], fill=WHITE, width=w)
        d.line([cx - int(r * 0.65), cy - int(r * 0.35), cx + int(r * 0.65), cy - int(r * 0.35)], fill=WHITE, width=w)
        d.polygon([(cx - int(r * 0.65), cy - int(r * 0.3)), (cx - int(r * 0.45), cy + int(r * 0.15)), (cx - int(r * 0.85), cy + int(r * 0.15))], fill=WHITE)
        d.polygon([(cx + int(r * 0.65), cy - int(r * 0.3)), (cx + int(r * 0.45), cy + int(r * 0.15)), (cx + int(r * 0.85), cy + int(r * 0.15))], fill=WHITE)
    elif kind == "spiral":
        for k, rr in enumerate([int(r * 0.7), int(r * 0.4), int(r * 0.15)]):
            d.arc([cx - rr, cy - rr, cx + rr, cy + rr], int(k * 60), int(k * 60) + 300, fill=WHITE, width=2)
    elif kind == "star":
        draw_star(d, cx, cy, int(r * 0.7), WHITE)
    elif kind == "rocket":
        d.polygon([(cx, cy - int(r * 0.8)), (cx - int(r * 0.35), cy + int(r * 0.4)), (cx + int(r * 0.35), cy + int(r * 0.4))], fill=WHITE)
        d.polygon([(cx - int(r * 0.35), cy + int(r * 0.1)), (cx - int(r * 0.7), cy + int(r * 0.8)), (cx - int(r * 0.25), cy + int(r * 0.5))], fill=WHITE)
        d.ellipse([cx - 5, cy - 4, cx + 5, cy + 6], fill=NAVY)
    elif kind == "handshake":
        d.arc([cx - int(r * 0.8), cy - int(r * 0.5), cx + int(r * 0.8), cy + int(r * 0.5)], 180, 360, fill=WHITE, width=w)
        d.arc([cx - int(r * 0.8), cy - int(r * 0.5), cx + int(r * 0.8), cy + int(r * 0.5)], 0, 180, fill=NAVY, width=w)


def new_canvas():
    img = Image.new("RGB", (W, H), PAPER)
    return img, ImageDraw.Draw(img)


def story_card(d, x, y, w, h, label, col, kind, headline, summary):
    rect(d, (x, y, x + w, y + h), WHITE, outline=NAVY, width=1)
    chip(d, x + 12, y + 12, w - 24, label, col)
    hf = font(True, 20)
    hl = wrap_text(d, headline, hf, w - 24)[:2]
    draw_wrapped(d, (x + 12, y + 50), hl, hf, INK, 26)
    sf = font(False, 14)
    sl = wrap_text(d, summary, sf, w - 24)[:2]
    draw_wrapped(d, (x + 12, y + 108), sl, sf, INK, 19)
    draw_icon(d, x + w - 34, y + 30, 18, kind)


def draw_variant1():
    img, d = new_canvas()
    rect(d, (0, 0, W, 64), NAVY)
    d.text((24, 17), "THE WORLD IN ONE IMAGE", font=font(True, 30), fill=GOLD)
    df = font(True, 24)
    d.text((W - 24 - text_w(d, DATE, df), 20), DATE, font=df, fill=WHITE)
    draw_globe(d, 512, 285, 140)
    hf = font(True, 40)
    hl = wrap_text(d, LEAD_HEAD, hf, 960)[:2]
    draw_centered(d, 512, 445, hl, hf, INK, 50)
    sf = font(False, 18)
    sl = wrap_text(d, LEAD_SUM, sf, 900)[:2]
    draw_centered(d, 512, 552, sl, sf, INK, 24)
    line(d, (132, 606), (892, 606), 3, RED)
    cards = STORIES + [("TICKER", NAVY, "globe", "Also that day",
                        TICKER1 + "  ///  " + TICKER2)]
    for i, (label, col, kind, head, summ) in enumerate(cards):
        cx = 16 + (i % 3) * 332
        cy = 620 + (i // 3) * 178
        story_card(d, cx, cy, 320, 168, label, col, kind, head, summ)
    rect(d, (0, 972, W, H), NAVY)
    ff = font(False, 15)
    d.text((int((W - text_w(d, FOOTER, ff)) / 2), 990), FOOTER, font=ff, fill=GOLD)
    return img


def draw_variant2():
    img, d = new_canvas()
    rect(d, (0, 0, 600, H), NAVY)
    d.text((28, 28), DATE, font=font(True, 24), fill=GOLD)
    draw_globe(d, 300, 270, 155)
    line(d, (28, 452), (572, 452), 3, GOLD)
    hf = font(True, 38)
    hl = wrap_text(d, LEAD_HEAD, hf, 544)[:3]
    draw_wrapped(d, (28, 472), hl, hf, WHITE, 46)
    sf = font(False, 17)
    sl = wrap_text(d, LEAD_SUM, sf, 544)[:4]
    draw_wrapped(d, (28, 622), sl, sf, WHITE, 23)
    for i, (label, col, kind, head, summ) in enumerate(STORIES):
        x, y = 616, 16 + i * 180
        rect(d, (x, y, x + 392, y + 168), WHITE, outline=NAVY, width=1)
        chip(d, x + 12, y + 12, 240, label, col)
        draw_icon(d, x + 392 - 32, y + 32, 18, kind)
        hf2 = font(True, 19)
        hl2 = wrap_text(d, head, hf2, 368)[:2]
        draw_wrapped(d, (x + 12, y + 50), hl2, hf2, INK, 25)
        sf2 = font(False, 13)
        sl2 = wrap_text(d, summ, sf2, 368)[:2]
        draw_wrapped(d, (x + 12, y + 106), sl2, sf2, INK, 18)
    rect(d, (0, 936, W, H), NAVY)
    tf = font(True, 16)
    d.text((16, 950), "TICKER", font=tf, fill=GOLD)
    rf = font(False, 15)
    tx = 16 + text_w(d, "TICKER", tf) + 14
    d.text((tx, 950), TICKER1, font=rf, fill=WHITE)
    tx += text_w(d, TICKER1, rf) + 14
    d.text((tx, 950), "///", font=tf, fill=GOLD)
    tx += text_w(d, "///", tf) + 14
    d.text((tx, 950), TICKER2, font=rf, fill=WHITE)
    d.text((16, 978), TICKER3, font=font(False, 14), fill=WHITE)
    ff = font(False, 13)
    d.text((int((W - text_w(d, FOOTER, ff)) / 2), 1002), FOOTER, font=ff, fill=GOLD)
    return img


def draw_variant3():
    img, d = new_canvas()
    tf = font(True, 54)
    d.text((int((W - text_w(d, "WORLD", tf)) / 2), 18), "WORLD", font=tf, fill=NAVY)
    df = font(True, 22)
    d.text((int((W - text_w(d, DATE, df)) / 2), 84), DATE, font=df, fill=GOLD)
    line(d, (112, 122), (912, 122), 3, RED)
    rect(d, (16, 138, 1008, 352), WHITE, outline=NAVY, width=1)
    for j, col in enumerate((RED, GOLD, NAVY)):
        rect(d, (28 + j * 98, 154, 28 + j * 98 + 86, 336), col)
    hf = font(True, 36)
    hl = wrap_text(d, LEAD_HEAD, hf, 660)[:2]
    draw_wrapped(d, (330, 158), hl, hf, INK, 44)
    sf = font(False, 18)
    sl = wrap_text(d, LEAD_SUM, sf, 660)[:3]
    draw_wrapped(d, (330, 256), sl, sf, INK, 24)
    for i, (label, col, kind, head, summ) in enumerate(STORIES):
        x = 16 + (i % 3) * 336
        y = 368 + (i // 3) * 264
        rect(d, (x, y, x + 320, y + 252), WHITE, outline=NAVY, width=1)
        rect(d, (x, y, x + 320, y + 6), col)
        nf = font(True, 28)
        d.text((x + 12, y + 16), "%02d" % (i + 1), font=nf, fill=GOLD)
        chip(d, x + 12, y + 54, 200, label, col)
        hf2 = font(True, 21)
        hl2 = wrap_text(d, head, hf2, 296)[:2]
        draw_wrapped(d, (x + 12, y + 94), hl2, hf2, INK, 27)
        sf2 = font(False, 15)
        sl2 = wrap_text(d, summ, sf2, 296)[:2]
        draw_wrapped(d, (x + 12, y + 154), sl2, sf2, INK, 20)
        draw_icon(d, x + 320 - 34, y + 252 - 34, 20, kind)
    x = 16 + 2 * 336
    y = 368 + 264
    rect(d, (x, y, x + 320, y + 252), NAVY)
    tf2 = font(True, 16)
    d.text((x + 12, y + 16), "TICKER", font=tf2, fill=GOLD)
    rf = font(False, 15)
    tl = wrap_text(d, TICKER1 + ". " + TICKER2 + ".", rf, 296)[:3]
    draw_wrapped(d, (x + 12, y + 52), tl, rf, WHITE, 21)
    tl2 = wrap_text(d, TICKER3, rf, 296)[:3]
    draw_wrapped(d, (x + 12, y + 140), tl2, rf, WHITE, 21)
    ff = font(False, 14)
    d.text((int((W - text_w(d, FOOTER, ff)) / 2), 1000), FOOTER, font=ff, fill=GOLD)
    return img


def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else "1"
    fn = globals().get("draw_variant" + variant)
    if fn is None:
        raise SystemExit("unknown variant " + variant)
    img = fn()
    out = "out_%s.png" % variant
    img.save(out)
    print("wrote %s 1024x1024 bytes %d" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()
