"""Render concise profile sections as animated data-notebook cards."""

from html import escape
from io import BytesIO
import math
import random
import xml.etree.ElementTree as ET

import cairosvg
from PIL import Image, ImageDraw, ImageFont

from generate_assets import ASSETS, ROOT, REGULAR, TITLE, BG, GREEN, WHITE, MUTED

W, N = 1000, 48
BOLD = ImageFont.truetype(TITLE, 24)
SMALL = ImageFont.truetype(REGULAR, 12)
LABEL = ImageFont.truetype(TITLE, 18)
BADGE = ImageFont.truetype(TITLE, 16)
BODY = ImageFont.truetype(REGULAR, 21)

SECTIONS = [
    ("01", "About Me", 168, [
        "Computer Science @ Chulalongkorn University",
        "AI & Data Science internship candidate | B.Sc. 2024–present",
    ]),
    ("02", "Tech Stack & Tools", 472, []),
    ("03", "Selected Work", 208, [
        "KBTG | 14th place in asset price prediction",
        "AIhack 2025 | Probability prediction & AUC optimization",
        "TIA 2023 | Agricultural computer vision · Semi-finalist",
    ]),
    ("04", "Experience", 168, [
        "Data Science Intern | Air Connect Engineering (Thailand)",
        "Research Assistant Intern | Prince of Songkla University",
    ]),
    ("05", "Recognition", 168, [
        "2026 | Google Student Ambassador · Gemini Rising Star",
        "2022 | AI Designer Award · Super AI Engineer Season 3",
    ]),
    ("06", "Beyond the Code", 168, [
        "CS32 core team · Linear Regression workshop TA",
        "Head Treasurer | Science Study Club, Chulalongkorn",
    ]),
]

GROUPS = [
    ("Machine Learning & Data Science", 96,
     [("python", "PYTHON"), ("pytorch", "PYTORCH"),
      ("scikitlearn", "SCIKIT-LEARN"), ("tensorflow", "TENSORFLOW")],
     "Feature engineering · Cross-validation · CNNs · RNNs/LSTMs"),
    ("Development & Tools", 232,
     [("java", "JAVA"), ("git", "GIT"), ("github", "GITHUB"), ("openai", "CODEX")],
     "Object-oriented programming · Pygame · Version control"),
    ("Analytics & Reporting", 368,
     [("excel", "EXCEL"), ("powerbi", "POWER BI")], ""),
]


def icons():
    result = {}
    for path in (ASSETS / "icons").glob("*.svg"):
        root = ET.fromstring(path.read_text())
        root.set("fill", GREEN)
        for el in root.iter():
            if el.get("fill") and el.get("fill") != "none":
                el.set("fill", GREEN)
        data = cairosvg.svg2png(bytestring=ET.tostring(root), output_width=60, output_height=60)
        result[path.stem] = Image.open(BytesIO(data)).convert("RGBA").resize((30, 30), Image.Resampling.LANCZOS)
    return result


ICONS = icons()


def background(index, number, height):
    im = Image.new("RGB", (W, height), BG)
    d = ImageDraw.Draw(im)
    phase = index / N * math.tau
    for x in range(0, W, 32):
        d.line((x, 0, x, height), fill="#0a1911")
    for y in range(0, height, 32):
        d.line((0, y, W, y), fill="#0a1911")
    # Low-contrast curves behind the text, brighter activity at the right edge.
    for curve in range(3):
        points = [(x, height-22-curve*18 - 12*math.sin(x/75 + phase + curve))
                  for x in range(1, W-1, 4)]
        d.line(points, fill=["#0e2418", "#102b1c", "#123220"][curve], width=1)
    if int(number) % 3 == 1:
        # Moving points along a stylized training curve.
        points = [(x, 93 + (height-118)*(1-math.exp(-(x-818)/55)))
                  for x in range(818, 967, 2)]
        d.line(points, fill="#26603d", width=2)
        for offset in [0, 16, 32]:
            pos = (index+offset) % N / N
            x = 818 + pos*148
            y = 93 + (height-118)*(1-math.exp(-(x-818)/55))
            d.ellipse((x-3, y-3, x+3, y+3), fill="#46b976")
    elif int(number) % 3 == 2:
        # Heatmap cells breathe gently; these are decorative, not reported metrics.
        for row in range(4):
            for col in range(6):
                v = (math.sin(phase + row*.8 + col*.6)+1)/2
                x, y = 842+col*19, height-103+row*19
                color = (12+int(8*v), 36+int(47*v), 23+int(19*v))
                d.rounded_rectangle((x, y, x+14, y+14), radius=2, fill=color)
    else:
        # Scatter clusters, reminiscent of a data exploration notebook.
        rng = random.Random(32)
        for j in range(34):
            x = 835 + rng.random()*124
            y = 94 + rng.random()*(height-120)
            y += math.sin(phase+j)*3
            d.ellipse((x-2, y-2, x+2, y+2), fill="#275f3e" if j%4 else "#459e68")
    d.rounded_rectangle((1, 1, W-2, height-2), radius=12, outline="#245238", width=2)
    d.line((30, 72, 970, 72), fill="#1a3a27")
    return im


def skill_badge(im, x, y, key, label):
    d = ImageDraw.Draw(im)
    width = int(d.textlength(label, font=BADGE))+68
    d.rectangle((x, y, x+width, y+44), fill="#123a24", outline="#2b6c43")
    im.paste(ICONS[key], (x+10, y+7), ICONS[key])
    d.text((x+49, y+22), label, font=BADGE, fill=WHITE, anchor="lm")
    return width


def render(index, section):
    number, title, height, lines = section
    im = background(index, number, height)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((30, 26, 77, 56), radius=5, fill="#123a24")
    d.text((53, 41), number, font=ImageFont.truetype(REGULAR, 16), fill=GREEN, anchor="mm")
    d.text((94, 24), title, font=BOLD, fill=WHITE)
    d.text((966, 40), "NOTEBOOK / " + number, font=SMALL, fill=MUTED, anchor="rm")
    for line, y in zip(lines, [91, 127, 163]):
        assert d.textlength(line, font=BODY) < 780, line
        d.text((32, y), line, font=BODY, fill="#d0e6d8")
    if number == "02":
        for title, y, badges, caption in GROUPS:
            d.text((32, y), title, font=LABEL, fill=WHITE)
            x = 32
            for key, label in badges:
                x += skill_badge(im, x, y+35, key, label)+10
            assert x < 820
            if caption:
                d.text((32, y+91), caption, font=ImageFont.truetype(REGULAR, 20), fill="#a9c6b4")
    return im


def save_animation(section):
    frames = [render(i, section) for i in range(N)]
    sample = Image.new("RGB", (W, section[2]*3))
    for row, i in enumerate([0, 16, 32]):
        sample.paste(frames[i], (0, row*section[2]))
    palette = sample.quantize(colors=128)
    indexed = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    name = f"section-{section[0]}"
    indexed[0].save(ASSETS / f"{name}.gif", save_all=True, append_images=indexed[1:],
                    duration=100, loop=0, optimize=True, disposal=1)
    frames[0].save(ASSETS / f"{name}.png", optimize=True)
    print(f"{name}: {(ASSETS / f'{name}.gif').stat().st_size // 1024} KiB")


def readme():
    contacts = [
        ("github", "https://github.com/Kueranan", "GitHub: Kueranan"),
        ("kaggle", "https://www.kaggle.com/kueranan", "Kaggle: kueranan"),
        ("linkedin", "https://www.linkedin.com/in/kueranan-puangninnoi-71858b2a5", "LinkedIn: Kueranan Puangninnoi"),
        ("email", "mailto:guerguer000@gmail.com", "Email: guerguer000@gmail.com"),
    ]
    parts = ['<!-- Generated by scripts/generate_sections.py. Edit its content to regenerate. -->',
             '<p align="center">\n  <img src="assets/terminal-header.gif" width="100%" alt="Kueranan Puangninnoi | AI, Data Science &amp; Computer Vision" />\n</p>',
             '<p align="center">']
    for name, url, label in contacts:
        parts.append(f'  <a href="{url}"><img src="assets/{name}.png" height="32" alt="{label}" /></a>')
    parts.append('</p>\n')
    for number, title, _, lines in SECTIONS:
        text = f'{number} / {title}. ' + '. '.join(lines)
        if number == "02":
            text += '; '.join(', '.join(label for _, label in badges) for _, _, badges, _ in GROUPS) + '. '
            text += 'Feature engineering, cross-validation, CNNs, RNNs/LSTMs, OOP and Pygame.'
        parts.append(f'<p>\n  <img src="assets/section-{number}.gif" width="100%" alt="{escape(text, quote=True)}" />\n</p>\n')
    parts.extend(['<details>', '<summary>Read the plain-text profile</summary>', ''])
    for number, title, _, lines in SECTIONS:
        parts.extend([f'### {number} / {title}', ''])
        if number == "02":
            for group, _, badges, caption in GROUPS:
                parts.append(f'**{group}:** ' + ', '.join(label for _, label in badges) + '.')
                if caption:
                    parts.append(caption + '.')
                parts.append('')
        else:
            parts.extend([line + '.' for line in lines] + [''])
    parts.extend(['</details>', '', '<p align="center"><a href="mailto:guerguer000@gmail.com">Let’s connect</a> · From raw data to working intelligence.</p>', ''])
    (ROOT / 'README.md').write_text('\n'.join(parts))


if __name__ == "__main__":
    for section in SECTIONS:
        save_animation(section)
    readme()
