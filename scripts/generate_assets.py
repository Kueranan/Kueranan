"""Generate self-contained terminal artwork for the GitHub profile."""

from pathlib import Path
from html import escape
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
WIDTH, HEIGHT = 1280, 480
BG, GREEN, WHITE, MUTED = "#050c09", "#59ff9a", "#e5f7ec", "#8ba99a"


def font_path(env, candidates):
    for candidate in [os.environ.get(env, ""), *candidates]:
        if candidate and Path(candidate).is_file():
            return candidate
    raise RuntimeError(f"No suitable font found. Set {env} to a font file path.")


MONO = font_path("PROFILE_MONO_FONT", [
    "/System/Library/Fonts/Supplemental/Andale Mono.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "C:/Windows/Fonts/consola.ttf",
])
TITLE = font_path("PROFILE_TITLE_FONT", [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
])
fonts = {s: ImageFont.truetype(MONO, s) for s in [12, 14, 16, 18, 20]}
title_font = ImageFont.truetype(TITLE, 78)
surname_font = ImageFont.truetype(TITLE, 41)
rng = random.Random(32)
streams = [(x, rng.randrange(480), rng.randrange(3, 8),
            "".join(rng.choice("01:<>/{}") for _ in range(24)))
           for x in range(850, 1260, 26)]


def frame(index):
    im = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(im)
    for x in range(0, WIDTH, 40):
        d.line((x, 0, x, HEIGHT), fill="#0b1811")
    for y in range(0, HEIGHT, 40):
        d.line((0, y, WIDTH, y), fill="#0b1811")
    for x, offset, speed, chars in streams:
        for j, char in enumerate(chars):
            y = (offset + j * 22 + index * speed) % 550 - 35
            d.text((x, y), char, font=fonts[12], fill="#122b1c" if j % 6 else "#235034")
    d.rounded_rectangle((1, 1, WIDTH-2, HEIGHT-2), radius=18, outline="#245238", width=2)
    d.line((30, 51, 1250, 51), fill="#245238")
    for x, color in [(33, GREEN), (55, "#2c7448"), (77, "#193f2a")]:
        d.ellipse((x, 23, x+9, 32), fill=color)
    d.text((104, 19), "kueranan@github: ~/profile", font=fonts[14], fill=MUTED)
    d.text((1060, 19), "SYSTEM / ONLINE", font=fonts[14], fill=GREEN)
    d.text((48, 80), "CS UNDERGRADUATE  /  CHULALONGKORN UNIVERSITY", font=fonts[16], fill=GREEN)
    d.text((43, 105), "KUERANAN", font=title_font, fill=WHITE)
    d.text((48, 196), "PUANGNINNOI", font=surname_font, fill=GREEN)
    d.text((50, 259), "AI  /  DATA SCIENCE  /  COMPUTER VISION", font=fonts[18], fill=MUTED)

    # Slow network scan keeps the identity legible throughout the animation.
    cx, cy = 1056, 234
    for r in [64, 102, 140]:
        d.ellipse((cx-r, cy-r, cx+r, cy+r), outline="#235b39", width=1)
    d.line((cx-155, cy, cx+155, cy), fill="#173a26")
    d.line((cx, cy-155, cx, cy+155), fill="#173a26")
    phase = index / 80 * math.tau
    nodes = [(cx+math.cos(a)*r, cy+math.sin(a)*r)
             for a, r in [(0.2, 102), (1.1, 140), (2.4, 102), (3.5, 140), (4.5, 102), (5.4, 140)]]
    for i, (x, y) in enumerate(nodes):
        for j in [1, 2]:
            d.line((x, y, *nodes[(i+j) % len(nodes)]), fill="#215235")
        d.line((x, y, cx, cy), fill="#215235")
        d.ellipse((x-4, y-4, x+4, y+4), fill=GREEN)
    angle = math.degrees(phase)-90
    d.arc((cx-140, cy-140, cx+140, cy+140), angle-35, angle, fill=GREEN, width=3)
    px, py = cx+math.cos(phase-math.pi/2)*140, cy+math.sin(phase-math.pi/2)*140
    d.ellipse((px-5, py-5, px+5, py+5), fill=WHITE)
    d.rounded_rectangle((cx-35, cy-26, cx+35, cy+26), radius=10, fill="#0b2014", outline=GREEN)
    d.text((cx, cy), "AI", font=fonts[20], fill=GREEN, anchor="mm")
    d.text((945, 398), "LEARN. BUILD. ITERATE.", font=fonts[14], fill=MUTED)

    d.rounded_rectangle((48, 310, 786, 408), radius=9, fill="#08140d", outline="#245238")
    d.text((67, 326), "$ python train.py --mode explore", font=fonts[18], fill=GREEN)
    messages = ["Preparing data. Finding patterns.", "Training models. Testing ideas."]
    message = messages[index // 40]
    visible = message[:min(len(message), int(index % 40 * 1.5))]
    d.text((67, 365), "> " + visible, font=fonts[18], fill=WHITE)
    if index % 10 < 6:
        x = 67 + d.textlength("> " + visible, font=fonts[18]) + 3
        d.rectangle((x, 366, x+9, 384), fill=GREEN)
    d.line((30, 436, 1250, 436), fill="#245238")
    d.text((48, 450), "PROFILE / 001", font=fonts[12], fill=MUTED)
    d.text((483, 449), "FROM RAW DATA TO WORKING INTELLIGENCE", font=fonts[12], fill=GREEN)
    d.text((1105, 450), "BUILD / LEARN", font=fonts[12], fill=MUTED)
    return im


def badge(filename, label, contact=False):
    width = len(label)*8+45
    fill = "#102b1b" if contact else "#09150e"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="32" viewBox="0 0 {width} 32" role="img" aria-label="{escape(label)}">
<rect x=".5" y=".5" width="{width-1}" height="31" rx="6" fill="{fill}" stroke="#2e6141"/>
<rect x="12" y="13" width="6" height="6" rx="1" fill="#59ff9a"/>
<text x="27" y="21" fill="#c7f7d9" font-family="monospace" font-size="13">{escape(label)}</text>
</svg>'''
    (ASSETS / f"{filename}.svg").write_text(svg + "\n")


def main():
    ASSETS.mkdir(exist_ok=True)
    frames = [frame(i) for i in range(80)]
    # Shared palette prevents color shimmer on stationary text.
    sample = Image.new("RGB", (WIDTH, HEIGHT*4))
    for row, idx in enumerate([0, 20, 40, 60]):
        sample.paste(frames[idx], (0, row*HEIGHT))
    palette = sample.quantize(colors=128)
    indexed = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(ASSETS / "terminal-header.gif", save_all=True,
                    append_images=indexed[1:], duration=100, loop=0,
                    optimize=True, disposal=1)
    frames[30].save(ASSETS / "terminal-header.png", optimize=True)
    for filename, label in [
        ("github", "GITHUB / KUERANAN"), ("kaggle", "KAGGLE / KUERANAN"),
        ("linkedin", "LINKEDIN"), ("email", "LET'S CONNECT"),
        ("python", "Python"), ("java", "Java"), ("scikit-learn", "scikit-learn"),
        ("tensorflow", "TensorFlow"), ("pytorch", "PyTorch"), ("git", "Git / GitHub"),
    ]:
        badge(filename, label, filename in ["github", "kaggle", "linkedin", "email"])
    (ASSETS / "footer.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="140" viewBox="0 0 1280 140" role="img" aria-label="Let's connect — AI, Data Science and Computer Vision">
<rect x="1" y="1" width="1278" height="138" rx="14" fill="#050c09" stroke="#245238" stroke-width="2"/>
<path d="M40 70h200m800 0h200" stroke="#245238"/>
<circle cx="240" cy="70" r="4" fill="#59ff9a"/><circle cx="1040" cy="70" r="4" fill="#59ff9a"/>
<text x="640" y="62" text-anchor="middle" font-family="monospace" font-size="25" fill="#59ff9a">$ let's_connect</text>
<text x="640" y="96" text-anchor="middle" font-family="monospace" font-size="16" fill="#8ba99a">AI / DATA SCIENCE / COMPUTER VISION</text>
</svg>
''')
    print(f"Generated {len(list(ASSETS.iterdir()))} assets in {ASSETS}")
    print(f"Animation: {(ASSETS / 'terminal-header.gif').stat().st_size / 1024:.0f} KiB")


if __name__ == "__main__":
    main()
