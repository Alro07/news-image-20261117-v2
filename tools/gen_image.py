#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

Run locally (needs Pillow + DejaVu fonts):
    python3 tools/gen_image.py
Writes entry.png next to main.py. The submitted program (main.py, stdlib
only) just copies that committed image to /output/entry.png, so the graded
runs are byte-identical and need no network.

Facts: every story below happened, or was first reported, on Tuesday
17 November 2026 (sources in the footer). Wording stays close to what
was reported; nothing is invented, hyped or shown as fact when it is
only expected (the Shenzhen summit is labelled as planned for Thursday).

Layout (1024x1024): masthead + date, "day in figures" strip, 3 big
illustrated lead stories, 9 illustrated picture stories, a world map
with 13 numbered places, 21 more headlines in three columns, an
"also today" ticker and a sources footer. 40 stories in total,
6 continents represented.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 40)
F_DATE = font("DejaVuSans-Bold.ttf", 46)
F_SUB = font("DejaVuSans-Bold.ttf", 20)
F_FIG_N = font("DejaVuSans-Bold.ttf", 26)
F_FIG_L = font("DejaVuSans.ttf", 13)
F_SEC = font("DejaVuSans-Bold.ttf", 17)
F_TAG = font("DejaVuSans-Bold.ttf", 14)
F_HEAD = font("DejaVuSans-Bold.ttf", 22)
F_BODY = font("DejaVuSans.ttf", 14)
F_CAP = font("DejaVuSans-Bold.ttf", 14)
F_CAP2 = font("DejaVuSans.ttf", 12)
F_GRID_TAG = font("DejaVuSans-Bold.ttf", 13)
F_GRID = font("DejaVuSans.ttf", 14)
F_TICK = font("DejaVuSans-Bold.ttf", 13)
F_MAPLEG = font("DejaVuSans.ttf", 12)
F_FOOT = font("DejaVuSans.ttf", 13)

NAVY = (11, 37, 69)
NAVY_DARK = (8, 28, 53)
GOLD = (201, 162, 39)
GOLD_LIGHT = (217, 180, 91)
PAPER = (247, 243, 234)
CARD = (255, 255, 255)
INK = (20, 33, 61)
BODY_INK = (52, 62, 78)
MUTED = (107, 114, 128)
BORDER = (214, 208, 194)
SEA = (178, 214, 232)
LAND = (232, 222, 190)
LAND_EDGE = (160, 148, 118)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- scenes
# Each scene draws a small recognisable picture into (x, y, w, h).

def scene_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(135, 180, 210))
    d.rectangle([x, y + int(h * 0.68), x + w, y + h], fill=(52, 96, 130))
    d.rectangle([x, y + int(h * 0.55), x + int(w * 0.42), y + int(h * 0.60)],
                fill=(90, 90, 96))
    d.rectangle([x + int(w * 0.58), y + int(h * 0.55), x + w, y + int(h * 0.60)],
                fill=(90, 90, 96))
    # towers
    for tx in (int(w * 0.18), int(w * 0.78)):
        d.rectangle([x + tx - 3, y + int(h * 0.18), x + tx + 3, y + int(h * 0.58)],
                    fill=(70, 70, 76))
    # tilted broken span falling into the strait
    d.polygon([(x + int(w * 0.44), y + int(h * 0.58)),
               (x + int(w * 0.56), y + int(h * 0.60)),
               (x + int(w * 0.53), y + int(h * 0.72)),
               (x + int(w * 0.46), y + int(h * 0.70))], fill=(120, 40, 30))
    d.ellipse([x + int(w * 0.44), y + int(h * 0.10), x + int(w * 0.62),
               y + int(h * 0.30)], fill=(120, 120, 120))
    d.ellipse([x + int(w * 0.48), y + int(h * 0.05), x + int(w * 0.58),
               y + int(h * 0.18)], fill=(150, 150, 150))


def scene_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 120, 90))
    d.rectangle([x, y + int(h * 0.72), x + w, y + h], fill=(120, 90, 60))
    # radar dish
    d.pieslice([x + int(w * 0.10), y + int(h * 0.45), x + int(w * 0.38),
                y + int(h * 0.95)], start=180, end=360, fill=(230, 230, 230))
    d.line([x + int(w * 0.24), y + int(h * 0.70), x + int(w * 0.24),
            y + int(h * 0.98)], fill=(230, 230, 230), width=4)
    # drone
    cx, cy = x + int(w * 0.68), y + int(h * 0.30)
    d.ellipse([cx - 12, cy - 6, cx + 12, cy + 6], fill=(40, 40, 46))
    for dx in (-16, 16):
        d.line([cx + dx - 8, cy - 10, cx + dx + 8, cy - 10], fill=(30, 30, 34),
               width=3)
    d.ellipse([cx - 6, cy + 12, cx + 6, cy + 24], fill=(255, 200, 60))
    d.polygon([(cx - 6, cy + 12), (cx + 6, cy + 12), (cx, cy + 26)],
              fill=(255, 160, 40))


def scene_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 170, 205))
    d.rectangle([x, y + int(h * 0.78), x + w, y + h], fill=(90, 70, 55))
    d.rectangle([x + int(w * 0.15), y + int(h * 0.78), x + int(w * 0.85),
                 y + int(h * 0.86)], fill=(120, 95, 70))
    flags = [((200, 40, 40), None), ((40, 70, 160), None), ((240, 240, 240), None)]
    for i, (col, _) in enumerate(flags):
        px = x + int(w * (0.22 + 0.28 * i))
        d.line([px, y + int(h * 0.14), px, y + int(h * 0.80)], fill=(60, 60, 60),
               width=3)
        d.rectangle([px, y + int(h * 0.14), px + int(w * 0.22), y + int(h * 0.34)],
                    fill=col, outline=(60, 60, 60))
    d.rectangle([x + int(w * 0.22), y + int(h * 0.14), x + int(w * 0.44),
                 y + int(h * 0.34)], fill=(200, 40, 40))
    d.rectangle([x + int(w * 0.50), y + int(h * 0.14), x + int(w * 0.72),
                 y + int(h * 0.34)], fill=(40, 70, 160))
    d.rectangle([x + int(w * 0.50), y + int(h * 0.22), x + int(w * 0.72),
                 y + int(h * 0.26)], fill=(255, 255, 255))
    d.rectangle([x + int(w * 0.78), y + int(h * 0.14), x + int(w * 1.00),
                 y + int(h * 0.34)], fill=(240, 240, 240))
    d.rectangle([x + int(w * 0.78), y + int(h * 0.14), x + int(w * 1.00),
                 y + int(h * 0.20)], fill=(255, 255, 255))
    d.rectangle([x + int(w * 0.78), y + int(h * 0.28), x + int(w * 1.00),
                 y + int(h * 0.34)], fill=(200, 40, 40))


def scene_jet(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 185, 220))
    d.ellipse([x + int(w * 0.72), y + int(h * 0.08), x + int(w * 0.92),
               y + int(h * 0.32)], fill=(255, 220, 120))
    # contrail
    d.line([x, y + int(h * 0.55), x + int(w * 0.55), y + int(h * 0.45)],
           fill=(255, 255, 255), width=3)
    # jet silhouette
    cx, cy = x + int(w * 0.55), y + int(h * 0.45)
    d.polygon([(cx - 34, cy), (cx + 30, cy - 6), (cx + 38, cy), (cx + 30, cy + 6)],
              fill=(50, 55, 65))
    d.polygon([(cx - 6, cy - 4), (cx + 8, cy - 22), (cx + 14, cy - 4)],
              fill=(50, 55, 65))
    d.polygon([(cx - 6, cy + 4), (cx + 8, cy + 20), (cx + 14, cy + 4)],
              fill=(50, 55, 65))


def scene_aid(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 190, 160))
    d.rectangle([x, y + int(h * 0.70), x + w, y + h], fill=(150, 135, 105))
    for i, (bx, by, s) in enumerate([(0.12, 0.42, 0.30), (0.46, 0.42, 0.30),
                                     (0.29, 0.12, 0.30)]):
        px, py, ps = x + int(w * bx), y + int(h * by), int(w * s)
        d.rectangle([px, py, px + ps, py + ps], fill=(196, 150, 90),
                    outline=(120, 85, 40), width=2)
        d.rectangle([px + ps // 2 - 3, py + 6, px + ps // 2 + 3, py + ps - 6],
                    fill=(255, 255, 255))
        d.rectangle([px + 6, py + ps // 2 - 3, px + ps - 6, py + ps // 2 + 3],
                    fill=(255, 255, 255))


def scene_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 160, 140))
    for i in range(4):
        cx = x + int(w * (0.15 + 0.23 * i))
        d.rectangle([cx - 2, y + int(h * 0.18), cx + 2, y + int(h * 0.55)],
                    fill=(240, 240, 235))
        d.rectangle([cx - 10, y + int(h * 0.12), cx + 10, y + int(h * 0.18)],
                    fill=(240, 240, 235))
    d.rectangle([x, y + int(h * 0.55), x + w, y + int(h * 0.62)],
                fill=(120, 100, 75))
    d.rectangle([x + int(w * 0.55), y + int(h * 0.68), x + int(w * 0.85),
                 y + int(h * 0.76)], fill=(110, 75, 40))
    d.line([x + int(w * 0.30), y + int(h * 0.70), x + int(w * 0.80),
            y + int(h * 0.42)], fill=(110, 75, 40), width=7)
    d.rectangle([x + int(w * 0.72), y + int(h * 0.30), x + int(w * 0.92),
                 y + int(h * 0.46)], fill=(90, 60, 30))


def scene_flag(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(190, 170, 130))
    d.rectangle([x, y + int(h * 0.75), x + w, y + h], fill=(140, 110, 70))
    d.line([x + int(w * 0.30), y + int(h * 0.10), x + int(w * 0.30),
            y + int(h * 0.78)], fill=(60, 60, 60), width=3)
    d.polygon([(x + int(w * 0.30), y + int(h * 0.12)),
               (x + int(w * 0.85), y + int(h * 0.22)),
               (x + int(w * 0.30), y + int(h * 0.34))], fill=(180, 40, 35))
    for i in range(3):
        d.polygon([(x + int(w * (0.55 + 0.12 * i)), y + int(h * 0.62)),
                   (x + int(w * (0.62 + 0.12 * i)), y + int(h * 0.62)),
                   (x + int(w * (0.585 + 0.12 * i)), y + int(h * 0.48))],
                  fill=(40, 40, 46))


def scene_parliament(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(180, 195, 215))
    d.rectangle([x, y + int(h * 0.75), x + w, y + h], fill=(120, 125, 110))
    cx = x + w // 2
    d.pieslice([cx - int(w * 0.20), y + int(h * 0.10), cx + int(w * 0.20),
                y + int(h * 0.55)], start=180, end=360, fill=(110, 90, 70))
    d.rectangle([x + int(w * 0.12), y + int(h * 0.45), x + int(w * 0.88),
                 y + int(h * 0.52)], fill=(200, 195, 180))
    for i in range(5):
        px = x + int(w * (0.16 + 0.17 * i))
        d.rectangle([px, y + int(h * 0.52), px + 7, y + int(h * 0.78)],
                    fill=(235, 230, 215))


def scene_football(d, x, y, w, h, shirt=(200, 40, 40)):
    d.rectangle([x, y, x + w, y + h], fill=(60, 150, 80))
    d.line([x, y + int(h * 0.55), x + w, y + int(h * 0.55)], fill=(255, 255, 255),
           width=2)
    d.ellipse([x + int(w * 0.38), y + int(h * 0.30), x + int(w * 0.62),
               y + int(h * 0.72)], outline=(255, 255, 255), width=2)
    # goal
    d.rectangle([x + int(w * 0.68), y + int(h * 0.12), x + int(w * 0.94),
                 y + int(h * 0.38)], outline=(255, 255, 255), width=3)
    # ball
    bx, by = x + int(w * 0.30), y + int(h * 0.68)
    d.ellipse([bx - 11, by - 11, bx + 11, by + 11], fill=(255, 255, 255),
              outline=(40, 40, 40))
    d.polygon([(bx, by - 5), (bx + 5, by - 1), (bx + 3, by + 5), (bx - 3, by + 5),
               (bx - 5, by - 1)], fill=(40, 40, 40))
    # player shirt
    d.polygon([(x + int(w * 0.55), y + int(h * 0.85)),
               (x + int(w * 0.62), y + int(h * 0.55)),
               (x + int(w * 0.72), y + int(h * 0.58)),
               (x + int(w * 0.68), y + int(h * 0.85))], fill=shirt)


def scene_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(35, 45, 70))
    cx, cy, s = x + w // 2, y + h // 2, int(min(w, h) * 0.30)
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(25, 180, 120),
                outline=(180, 255, 220), width=2)
    d.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                fill=(20, 120, 80))
    for i in range(5):
        off = -s + i * (2 * s // 4)
        d.line([cx + off, y + int(h * 0.08), cx + off, cy - s], fill=(200, 200, 200),
               width=2)
        d.line([cx + off, cy + s, cx + off, y + int(h * 0.92)], fill=(200, 200, 200),
               width=2)
        d.line([x + int(w * 0.08), cy + off, cx - s, cy + off],
               fill=(200, 200, 200), width=2)
        d.line([cx + s, cy + off, x + int(w * 0.92), cy + off],
               fill=(200, 200, 200), width=2)


SCENES = {
    "bridge": scene_bridge, "drone": scene_drone, "summit": scene_summit,
    "jet": scene_jet, "aid": scene_aid, "gavel": scene_gavel,
    "flag": scene_flag, "parliament": scene_parliament,
    "chip": scene_chip,
}


def scene_football_blue(d, x, y, w, h):
    scene_football(d, x, y, w, h, shirt=(40, 90, 200))


SCENES["football"] = scene_football
SCENES["football_blue"] = scene_football_blue

# ---------------------------------------------------------------- data

LEAD = [
    ("EUROPE  ·  WAR", (180, 35, 24), "bridge",
     "Kerch Bridge hit again; Kyiv's bridges struck too",
     "A Ukrainian strike collapsed a road span of the Crimea bridge; "
     "Russian missiles hit Kyiv's Dnipro crossings, cutting power."),
    ("MIDDLE EAST", (14, 124, 123), "drone",
     "Iran drones target U.S. base in Bahrain",
     "Drones aimed at a U.S. radar site in Bahrain were intercepted; "
     "no casualties. The U.S. hit Qeshm Island."),
    ("ASIA  ·  DIPLOMACY", (59, 74, 140), "summit",
     "Xi, Trump and Putin to meet Thursday in Shenzhen",
     "China confirms the first three-way summit on the APEC sidelines; "
     "Trump opens his Asia trip with a Quad summit in Manila."),
]

# (scene, caption) — 9 illustrated picture stories
TILES = [
    ("jet", "JAPAN  ·  Jets scrambled over Russian planes"),
    ("aid", "GAZA  ·  West urges Israel to open aid crossings"),
    ("gavel", "FRANCE  ·  Depardieu admits assault charge"),
    ("flag", "YEMEN  ·  Houthis close in on Aden as forces retreat"),
    ("parliament", "MONGOLIA  ·  President resigns amid corruption scandal"),
    ("parliament", "ISRAEL  ·  Knesset elects new speaker"),
    ("football", "USA 2–0 HAITI  ·  Pochettino bows out a winner"),
    ("football_blue", "ARGENTINA 7–0 COSTA RICA  ·  Rout in Cordoba"),
    ("chip", "NVIDIA  ·  Revenue $116bn, up 103%"),
]

# (region, headline) — 21 more stories, 3 columns x 7 rows
GRID = [
    ("EUROPE", "Five EU states plan a Rwanda return hub for rejected asylum seekers"),
    ("EUROPE", "France strike turnout falls to 146,000 in public-sector marches"),
    ("EUROPE", "Moldova says a Russian drone flew over Chisinau"),
    ("EUROPE", "Hoax bomb threats across Europe probed as one group's work"),
    ("MIDEAST", "Gaza: UN warns 1.7m displaced as winter emergency worsens"),
    ("MIDEAST", "Kataib Hezbollah refuses to leave Jurf al-Sakhar stronghold"),
    ("MIDEAST", "Turkiye, Saudi Arabia, Pakistan to hold defence-pact talks"),
    ("ASIA", "U.S. tightens AI chip-export curbs on China via third countries"),
    ("ASIA", "Trump says he may meet Kim Jong Un on his Asia trip"),
    ("ASIA", "COP31 climate talks enter decisive phase in Antalya"),
    ("MIDEAST", "Tankers struck by mines near the Strait of Hormuz"),
    ("AFRICA", "Ivory Coast draw 2–2 with Gambia, stay top of AFCON group"),
    ("AFRICA", "Egypt face Malawi in AFCON qualifier in Lilongwe"),
    ("AFRICA", "WHO validates Eritrea's elimination of trachoma"),
    ("AMERICAS", "Pentagon fails audit for ninth straight year; $4.8tn unverified"),
    ("AMERICAS", "Senate confirms Trump appeals judge 52–46 in lame-duck rush"),
    ("AMERICAS", "Mexico edge Jamaica on away goals; face USA in March"),
    ("AMERICAS", "Protests in Haitian cities back Salvadoran operation"),
    ("OCEANIA", "Australia eases backpacker visa curbs after rural backlash"),
    ("MARKETS", "Stocks slide worldwide: Nasdaq –0.7%, S&P 500 –1%"),
    ("MARKETS", "Bitcoin stalls below $65,000 after sell-off; Brent $92.98"),
]

TICKER = (
    "ALSO TODAY:  Oil falls as U.S. crude stocks rise 5.28m barrels  ·  "
    "Dollar hits 19-month high  ·  Deutsche Bank shares slide 5%  ·  "
    "Anthropic debut looms as AI trade unwinds  ·  Disney, Home Depot report"
)

FOOTER = (
    "Events of Tuesday 17 November 2026, as reported that day  ·  "
    "Sources: Reuters · CNN · Al Jazeera · Arab News · USA Today · Africa CDC · WHO"
)

FIGURES = [
    ("$116bn", "Nvidia Q3 revenue, +103% YoY"),
    ("9th year", "Pentagon fails audit again"),
    ("146,000", "marched in France strike"),
    ("1.7m", "displaced in Gaza, UN warns"),
]

# (lon, lat, label) numbered map places
PLACES = [
    (33.5, 45.3, "Kerch"), (30.5, 50.4, "Kyiv"), (52.5, 24.5, "Bahrain"),
    (114.1, 22.5, "Shenzhen"), (139.7, 35.7, "Tokyo"), (121.0, 14.6, "Manila"),
    (34.5, 31.5, "Gaza"), (2.3, 48.9, "Paris"), (-77.0, 38.9, "Washington"),
    (45.0, 12.8, "Aden"), (106.9, 47.9, "Ulaanbaatar"),
    (-64.2, -31.4, "Cordoba"), (151.2, -33.9, "Sydney"),
]

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-75, 72), (-65, 62), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 26), (-84, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    # South America
    [(-80, 10), (-75, 5), (-80, -5), (-81, -15), (-75, -25), (-70, -35),
     (-65, -45), (-70, -55), (-65, -52), (-55, -35), (-48, -28), (-40, -20),
     (-35, -8), (-45, 0), (-55, 5), (-65, 10), (-75, 10)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 70), (40, 68), (45, 68),
     (50, 69), (40, 66), (35, 60), (30, 55), (28, 45), (23, 40), (19, 42),
     (12, 44), (8, 44), (3, 42), (-2, 37), (-9, 37)],
    # Africa
    [(-17, 15), (-16, 25), (-10, 30), (-5, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (43, 12), (51, 11), (48, 2), (40, -5), (40, -15), (35, -25),
     (28, -33), (20, -35), (15, -28), (12, -18), (13, -10), (9, 4), (-8, 5),
     (-13, 8), (-17, 12)],
    # Asia
    [(30, 36), (35, 36), (40, 40), (45, 40), (50, 42), (55, 45), (60, 45),
     (65, 45), (70, 50), (75, 55), (80, 60), (85, 65), (90, 70), (100, 75),
     (110, 76), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
     (170, 67), (178, 65), (170, 60), (162, 56), (158, 52), (150, 60),
     (142, 55), (140, 45), (135, 43), (130, 38), (127, 35), (122, 32),
     (120, 28), (115, 22), (110, 20), (108, 12), (105, 9), (100, 7),
     (98, 10), (95, 15), (92, 20), (90, 22), (86, 20), (80, 15), (77, 8),
     (75, 15), (72, 20), (68, 23), (62, 25), (58, 25), (55, 26), (52, 28),
     (50, 30), (48, 30), (44, 29), (40, 32), (36, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -23), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20), (114, -21)],
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # graticule
    for gx in range(1, 6):
        lx = x + w * gx / 6
        d.line([lx, y, lx, y + h], fill=(200, 225, 238), width=1)
    for gy in range(1, 4):
        ly = y + h * gy / 4
        d.line([x, ly, x + w, ly], fill=(200, 225, 238), width=1)

    def proj(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (78 - lat) / 136 * h)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for i, (lon, lat, _label) in enumerate(PLACES, start=1):
        px, py = proj(lon, lat)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(180, 35, 24),
                  outline=(255, 255, 255), width=2)
        num = str(i)
        tw = d.textlength(num, font=F_TAG)
        d.text((px - tw / 2, py - 7), num, font=F_TAG, fill=(255, 255, 255))


def section_label(d, x, y, text):
    d.text((x, y), text, font=F_SEC, fill=NAVY)
    d.line([x, y + 22, x + W - 32, y + 22], fill=GOLD, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.rectangle([0, 104, W, 108], fill=GOLD)
    t = "THE WORLD IN ONE DAY"
    tw = d.textlength(t, font=F_MAST)
    d.text(((W - tw) / 2, 8), t, font=F_MAST, fill=(255, 255, 255))
    t = "TUESDAY 17 NOVEMBER 2026"
    tw = d.textlength(t, font=F_DATE)
    d.text(((W - tw) / 2, 52), t, font=F_DATE, fill=GOLD_LIGHT)

    # ---- day in figures ----
    fy, fh = 112, 48
    fw = (W - 32 - 3 * 8) // 4
    for i, (num, label) in enumerate(FIGURES):
        x = 16 + i * (fw + 8)
        d.rounded_rectangle([x, fy, x + fw, fy + fh], radius=6,
                            fill=(255, 255, 255), outline=BORDER, width=1)
        d.text((x + 10, fy + 1), num, font=F_FIG_N, fill=(180, 35, 24))
        for j, ln in enumerate(wrap(d, label, F_FIG_L, fw - 20)[:1]):
            d.text((x + 10, fy + 31), ln, font=F_FIG_L, fill=BODY_INK)

    # ---- lead stories: 3 columns ----
    y0, lh = 168, 244
    margin, gap = 16, 10
    pw = (W - 2 * margin - 2 * gap) // 3
    for i, (tag, colour, scene, headline, body) in enumerate(LEAD):
        x = margin + i * (pw + gap)
        d.rounded_rectangle([x, y0, x + pw, y0 + lh], radius=8, fill=CARD,
                            outline=BORDER, width=1)
        SCENES[scene](d, x + 1, y0 + 1, pw - 2, 88)
        d.rectangle([x, y0 + 88, x + pw, y0 + 90], fill=colour)
        tag_w = d.textlength(tag, font=F_TAG) + 16
        d.rounded_rectangle([x + 10, y0 + 100, x + 10 + tag_w, y0 + 122],
                            radius=5, fill=colour)
        d.text((x + 18, y0 + 104), tag, font=F_TAG, fill=(255, 255, 255))
        ty = y0 + 130
        for ln in wrap(d, headline, F_HEAD, pw - 20)[:2]:
            d.text((x + 10, ty), ln, font=F_HEAD, fill=INK)
            ty += 26
        ty += 2
        for ln in wrap(d, body, F_BODY, pw - 20)[:3]:
            d.text((x + 10, ty), ln, font=F_BODY, fill=BODY_INK)
            ty += 17

    # ---- in pictures: 9 tiles ----
    section_label(d, 16, 420, "IN PICTURES  ·  9 MORE STORIES FROM THE DAY")
    ty0, th = 446, 104
    tw_ = (W - 2 * 16 - 8 * 8) // 9
    for i, (scene, cap) in enumerate(TILES):
        x = 16 + i * (tw_ + 8)
        d.rounded_rectangle([x, ty0, x + tw_, ty0 + th], radius=6, fill=CARD,
                            outline=BORDER, width=1)
        SCENES[scene](d, x + 1, ty0 + 1, tw_ - 2, 52)
        cy = ty0 + 56
        for ln in wrap(d, cap, F_CAP2, tw_ - 8)[:4]:
            d.text((x + 4, cy), ln, font=F_CAP2, fill=INK)
            cy += 13

    # ---- world map ----
    section_label(d, 16, 558, "THE DAY ON THE MAP  ·  13 PLACES, 6 CONTINENTS")
    draw_map(d, 16, 584, W - 32, 124)
    legend = "  ·  ".join(f"{i} {lab}" for i, (_lo, _la, lab) in
                           enumerate(PLACES, start=1))
    lw = d.textlength(legend, font=F_MAPLEG)
    d.text(((W - lw) / 2, 712), legend, font=F_MAPLEG, fill=BODY_INK)

    # ---- more headlines: 3 columns x 7 rows ----
    section_label(d, 16, 730, "MORE FROM THE DAY  ·  21 STORIES")
    gy0 = 756
    gw = (W - 2 * 16 - 2 * 12) // 3
    for i, (region, headline) in enumerate(GRID):
        col, row = i % 3, i // 3
        x = 16 + col * (gw + 12)
        y = gy0 + row * 27
        d.text((x, y), region, font=F_GRID_TAG, fill=(180, 35, 24))
        rw = d.textlength(region, font=F_GRID_TAG)
        lines = wrap(d, headline, F_GRID, gw - rw - 8)
        d.text((x + rw + 8, y + 1), lines[0] if lines else "", font=F_GRID,
               fill=INK)
        if len(lines) > 1:
            d.text((x, y + 14), lines[1], font=F_GRID, fill=INK)

    # ---- ticker + footer ----
    tick_y = 952
    d.rectangle([0, tick_y, W, tick_y + 34], fill=(240, 227, 192))
    d.rectangle([0, tick_y, W, tick_y + 2], fill=GOLD)
    tlines = wrap(d, TICKER, F_TICK, W - 32)
    ty = tick_y + 4
    for ln in tlines[:2]:
        d.text((16, ty), ln, font=F_TICK, fill=NAVY_DARK)
        ty += 14
    fw = d.textlength(FOOTER, font=F_FOOT)
    d.text(((W - fw) / 2, 994), FOOTER, font=F_FOOT, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
