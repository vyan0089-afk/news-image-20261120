#!/usr/bin/env python3
"""Draw THE TWENTIETH: a one-page newspaper front page summing up
Friday 20 November 2026 world news. 40 stories, all verified as
happened / first reported on 20 Nov 2026. Stdlib + Pillow only.
Run: python3 generate.py  -> writes entry.png (1024x1024, RGB)."""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 222)
PAPER2 = (242, 233, 205)
INK = (26, 26, 26)
RED = (176, 30, 30)
BLUE = (28, 68, 128)
GOLD = (176, 132, 20)
TEAL = (18, 110, 105)
GREEN = (46, 110, 46)
GREY = (110, 105, 90)
LINE = (90, 82, 64)

FDIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FDIR + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

# (num, region, headline, summary, source, label)
# regions: AS Asia, EU Europe, NA North America, ME Middle East, AF Africa,
#          SA South America, GL Global / online
STORIES = [
 (1, "AS", "CYCLONE AKVAN HITS ODISHA",
  "Storm crosses the coast near Gopalpur, winds 70-80 km/h; 300,000+ evacuated to 9,341 shelters.",
  "Reuters; Hindu BusinessLine", ""),
 (2, "EU", "KYIV BRIDGES STRUCK OVERNIGHT",
  "Russia fires 110+ missiles and ~400 drones; three Dnipro bridges hit, 3 killed in Kyiv.",
  "Reuters; CNN", ""),
 (3, "EU", "COP31 DEADLOCK ON CLOSING DAY",
  "Antalya talks enter their final day with no deal; slim draft drops all fossil-fuel wording.",
  "CNN; Reuters", ""),
 (4, "AS", "ASIA'S AI SELL-OFF DEEPENS",
  "Nikkei -4.8%, Taiwan -6.75% in its worst week since 1990, Kospi -5.7%; SoftBank -14.6%.",
  "Reuters; Morningstar", ""),
 (5, "NA", "ANTHROPIC SLIDES ON DAY TWO",
  "Shares fall in early trading, pre-market $90.19, -7.2% on Thursday's $97.17 close.",
  "Finnhub", ""),
 (6, "EU", "POLAND SCRAMBLES JETS",
  "Jets and Patriot defences activated as objects cross Polish airspace in the Ukraine attack.",
  "CNN", ""),
 (7, "ME", "GAZA: NEW DISPLACEMENT",
  "Ground operation around Bureij and Nuseirat drives thousands more from homes as storms flood tents.",
  "Gaza Herald", ""),
 (8, "EU", "BERLIN: ALLIES MEET ON UKRAINE",
  "Coalition of the willing says Europe has a united position for talks; US open to a NATO-style guarantee.",
  "BBC; France 24", ""),
 (9, "NA", "CALIFORNIA PROBES NVIDIA",
  "Attorney general subpoenas Nvidia over whether advanced chips or data reached China.",
  "BBC; CNBC", ""),
 (10, "AF", "DRC EBOLA OUTBREAK PERSISTS",
  "Ebola still spreading six months on, as armed attacks hamper health workers.",
  "UN Geneva", ""),
 (11, "AS", "JAPAN INFLATION KEEPS HIKE ON TRACK",
  "Core prices up 2.2% in October, the year's highest; Bank of Japan rate rise still expected.",
  "Japan Times; CNBC", ""),
 (12, "GL", "MAKE.FUN OPENS TODAY'S CONTEST",
  "This news-image contest opens 00:00 UTC; $250 in USDC locked in escrow at 00:00:40 UTC.",
  "make.fun", ""),
 (13, "AF", "SENEGAL BOAT CAPSIZES",
  "Migrant boat with 50-100 aboard sinks off Yenne; 4 dead, dozens missing.",
  "BBC; Al Jazeera", ""),
 (14, "NA", "HAITI RAID KILLS 34",
  "Forces move to retake Martissant corridor; police say 34 suspected gang members killed.",
  "Al Jazeera; France 24", ""),
]

BRIEFS = [
 (15, "EU", "UK pledges 1,000+ drones for Ukraine in a £260m package.", "UK govt"),
 (16, "EU", "Estonia to close Russia border crossings from December.", "Munich Eye"),
 (17, "EU", "EU to summon Russian envoy over embassy damage in Kyiv.", "Kallas / EU"),
 (18, "NA", "Trump posthumously pardons baseball star Pete Rose.", "BBC"),
 (19, "NA", "US Senate passes energy permitting bill, 62-33.", "CNBC"),
 (20, "NA", "US sanctions Comancheros gang and 'Ndrangheta.", "US Treasury"),
 (21, "NA", "US jobless claims unexpectedly move higher.", "Dow Jones"),
 (22, "AF", "South Africa holds its repo rate at 7.25%.", "Dow Jones"),
 (23, "GL", "Gold falls 4.2% as dollar and yields weigh.", "CNBC"),
 (24, "SA", "Brazil sells $1bn of reserves to curb the dollar.", "MercoPress"),
 (25, "AF", "Sudan drone strike kills 10 at a gold mine.", "AllAfrica"),
 (26, "ME", "Iraq orders Kataib Hezbollah out of Jurf al-Nasr.", "Euronews; DW"),
 (27, "AS", "Pakistan kills 22 militants in north-west raids.", "The Hindu"),
 (28, "AF", "Zimbabwe destroys its 250,000th landmine.", "Africanews"),
 (29, "GL", "UN chief race stalls after eight Council votes.", "Guardian"),
 (30, "ME", "Mosque set on fire in northern Israel.", "Middle East Eye"),
 (31, "NA", "El Nino storm threatens Los Angeles flooding.", "Straits Times"),
 (32, "SA", "Argentina Senate passes disability law, 71-0.", "AppiSToS"),
 (33, "EU", "Spain: students strike, march at noon on 20 Nov.", "CatalunyaInfo"),
 (34, "EU", "Prague protesters demand media independence.", "Munich Eye"),
 (35, "NA", "Actor Stacy Keach dies at 85.", "Munich Eye"),
 (36, "NA", "White House names Kirsten Davies cyber chief.", "France 24"),
 (37, "EU", "UK-EU summit: youth mobility deal expected. [FORECAST]", "BBC"),
 (38, "AS", "India bowls out New Zealand in the day's cricket.", "myKhel"),
 (39, "AS", "Takaichi gets a cool reception at APEC in China.", "CNBC; Yonhap"),
 (40, "EU", "Youth strike in 25+ countries over living costs.", "Straits Times"),
]

REGIONS = [("ASIA", "AS", BLUE), ("EUROPE", "EU", RED), ("N. AMERICA", "NA", TEAL),
           ("MID EAST", "ME", GOLD), ("AFRICA", "AF", GREEN), ("S.AM.", "SA", (120, 70, 130)),
           ("GLOBAL", "GL", GREY)]
REG_COL = {c: col for _, c, col in REGIONS}

def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_illus(d, idx, x, y, w, h, cap=True):
    """Code-drawn vector illustration per story, inside box (x,y,w,h).
    cap=False draws the icon without its caption line (feature rows)."""
    cx, cy = x + w // 2, y + h // 2
    if idx == 1:  # cyclone spiral
        rr = min(w, h) // 2 - 3
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(214, 230, 244))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(160, 190, 220), width=1)
        for r in range(5, rr, 4):
            a0 = r * 0.55
            d.arc([cx - r, cy - r, cx + r, cy + r], math.degrees(a0), math.degrees(a0) + 250,
                  fill=BLUE, width=3)
        d.arc([cx - rr - 2, cy - rr - 2, cx + rr + 2, cy + rr + 2], 20, 160, fill=(140, 175, 210), width=2)
        d.arc([cx - rr - 2, cy - rr - 2, cx + rr + 2, cy + rr + 2], 200, 330, fill=(140, 175, 210), width=2)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
        d.ellipse([cx - 3, cy - 4, cx + 1, cy], fill=(255, 255, 255))
        if cap:
            d.text((x + 4, y + h - 16), "70-80 km/h", font=SANS_B(10), fill=BLUE)
    elif idx == 2:  # bridge + missile
        ar = 14 if cap else 6
        d.line([x + 6, cy + 14, x + w - 6, cy + 14], fill=INK, width=3)
        d.line([x + 6, cy + 17, x + w - 6, cy + 17], fill=(150, 140, 120), width=1)
        for px in (x + w * 0.25, x + w * 0.5, x + w * 0.75):
            d.line([px, cy + 14, px, cy - 8], fill=INK, width=3)
            d.arc([px - ar, cy - 8, px + ar, cy + 14], 180, 360, fill=INK, width=2)
        if cap:
            d.polygon([(x + w * 0.5 - 8, cy - 2), (x + w * 0.5 + 8, cy - 2), (x + w * 0.5, cy + 12)],
                      fill=(255, 170, 40))
            d.polygon([(x + w * 0.5 - 4, cy - 2), (x + w * 0.5 + 4, cy - 2), (x + w * 0.5, cy + 8)],
                      fill=(255, 220, 80))
            for dx in (0, 8, 16):
                d.line([x + 10 + dx, y + 10, x + 18 + dx, y + 16], fill=RED, width=2)
            for wx in (x + 10, x + w // 2, x + w - 28):
                d.arc([wx, cy + 20, wx + 18, cy + 30], 0, 180, fill=BLUE, width=2)
        d.line([x + 8, y + 8, cx + 10, cy - 12], fill=RED, width=3)
        d.polygon([(cx + 10, cy - 12), (cx + 2, cy - 6), (cx + 14, cy - 2)], fill=RED)
        if cap:
            d.text((x + 4, y + h - 16), "3 BRIDGES HIT", font=SANS_B(10), fill=RED)
    elif idx == 3:  # globe + thermometer
        gr = 26 if cap else 14
        gcx = cx if cap else cx - 4
        d.ellipse([gcx - gr, cy - gr - 2, gcx + gr, cy + gr - 2], fill=(205, 230, 240))
        d.ellipse([gcx - gr, cy - gr - 2, gcx + gr, cy + gr - 2], outline=TEAL, width=3)
        d.ellipse([gcx - gr + 4, cy - gr + 6, gcx - 2, cy - 2], fill=(120, 170, 110))
        d.ellipse([gcx + 2, cy, gcx + gr - 4, cy + gr - 6], fill=(120, 170, 110))
        d.line([gcx - gr, cy - 4, gcx + gr, cy - 4], fill=TEAL, width=2)
        d.arc([gcx - gr // 2, cy - gr - 2, gcx + gr // 2, cy + gr - 2], 270, 90, fill=TEAL, width=1)
        if cap:
            d.rectangle([x + w - 18, y + 8, x + w - 10, y + h - 14], fill=(255, 255, 255), outline=RED, width=2)
            d.rectangle([x + w - 16, y + 18, x + w - 12, y + h - 18], fill=RED)
            d.ellipse([x + w - 20, y + h - 26, x + w - 8, y + h - 14], fill=RED)
            for ty in (y + 14, y + 24, y + 34):
                d.line([x + w - 22, ty, x + w - 18, ty], fill=RED, width=1)
            d.text((x + 4, y + h - 16), "NO DEAL YET", font=SANS_B(10), fill=TEAL)
    elif idx == 4:  # falling chart
        for gy in (y + 12, y + 24, y + 36):
            d.line([x + 6, gy, x + w - 8, gy], fill=(220, 212, 190), width=1)
        d.line([x + 6, y + 8, x + 6, y + h - 20], fill=GREY, width=2)
        d.line([x + 6, y + h - 20, x + w - 6, y + h - 20], fill=GREY, width=2)
        pts = [(x + 6, y + 14), (x + w * 0.35, y + 26), (x + w * 0.6, y + 20),
               (x + w * 0.8, y + 44), (x + w - 8, y + h - 22)]
        if cap:
            d.polygon(pts + [(x + w - 8, y + h - 20), (x + 6, y + h - 20)], fill=(250, 215, 210))
        d.line(pts, fill=RED, width=3, joint="curve")
        for px, py in pts[1:-1]:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255), outline=RED, width=2)
        d.polygon([(x + w - 8, y + h - 22), (x + w - 18, y + h - 26), (x + w - 16, y + h - 14)],
                  fill=RED)
        if cap:
            d.text((x + 4, y + h - 16), "NIKKEI -4.8%", font=SANS_B(10), fill=RED)
    elif idx == 5:  # stock arrow down
        bw5 = 12 if cap else 7
        base5 = y + h - 18 if cap else y + h - 6
        bars5 = [(x + 8, base5 - 16, 16), (x + 26, base5 - 26, 26), (x + 44, base5 - 10, 10)] if cap else \
                [(x + 5, base5 - 10, 10), (x + 15, base5 - 16, 16), (x + 25, base5 - 6, 6)]
        for bx, by, bh in bars5:
            d.rectangle([bx, by, bx + bw5, base5], fill=BLUE)
            d.rectangle([bx, by, bx + bw5, by + 4], fill=(110, 160, 210))
        d.line([x + 8, y + 12, x + w - 10, y + h - 30 if cap else y + h - 12], fill=RED, width=3)
        d.polygon([(x + w - 10, y + h - 30 if cap else y + h - 12),
                   (x + w - 24, y + h - 34 if cap else y + h - 16),
                   (x + w - 16, y + h - 16 if cap else y + h - 2)],
                  fill=RED)
        if cap:
            d.ellipse([x + 8, y + 12, x + 14, y + 18], fill=RED)
            d.text((x + 4, y + h - 16), "ANT -7.2% DAY 2", font=SANS_B(10), fill=RED)
    elif idx == 6:  # jet
        if cap:
            d.ellipse([x + 6, y + 4, x + 26, y + 14], fill=(235, 240, 245))
            d.ellipse([x + w - 34, y + 2, x + w - 14, y + 12], fill=(235, 240, 245))
        d.polygon([(x + 8, cy), (x + w - 20, cy - 10), (x + w - 6, cy), (x + w - 20, cy + 10)],
                  fill=GREY)
        d.polygon([(x + 8, cy), (x + w - 20, cy - 10), (x + w - 6, cy), (x + w - 20, cy + 2)],
                  fill=(140, 135, 120))
        d.polygon([(cx - 4, cy - 8), (cx + 8, cy - 22), (cx + 12, cy - 8)], fill=GREY)
        d.polygon([(cx - 4, cy - 8), (cx + 8, cy - 22), (cx + 12, cy - 8)], outline=(90, 85, 70), width=1)
        d.ellipse([x + w - 30, cy - 5, x + w - 20, cy + 3], fill=(180, 220, 240))
        if cap:
            for dx in (0, 14, 28):
                d.line([x + 8 + dx, cy + 16, x + 16 + dx, cy + 16], fill=BLUE, width=2)
            d.line([x + 6, cy + 12, x + w - 8, cy + 12], fill=BLUE, width=2)
            d.text((x + 4, y + h - 16), "AIRSPACE BREACH", font=SANS_B(10), fill=BLUE)
    elif idx == 7:  # tents / displacement
        if cap:
            for i, tx in enumerate((x + 10, x + w // 2 - 8, x + w - 34)):
                d.polygon([(tx, cy + 16), (tx + 12, cy - 10), (tx + 24, cy + 16)],
                          outline=TEAL, width=2, fill=(210, 230, 225))
                d.polygon([(tx + 8, cy + 16), (tx + 12, cy + 4), (tx + 16, cy + 16)],
                          fill=(90, 130, 125))
                d.line([tx + 12, cy - 10, tx + 12, cy - 16], fill=TEAL, width=1)
            for rx, ry in ((x + 20, y + 6), (x + 60, y + 4), (x + 110, y + 6), (x + 170, y + 4), (x + 210, y + 6)):
                d.line([rx, ry, rx - 2, ry + 6], fill=BLUE, width=2)
        else:
            for tx in (x + 3, x + 21):
                d.polygon([(tx, cy + 14), (tx + 8, cy - 6), (tx + 16, cy + 14)],
                          outline=TEAL, width=2, fill=(210, 230, 225))
                d.polygon([(tx + 5, cy + 14), (tx + 8, cy + 4), (tx + 11, cy + 14)],
                          fill=(90, 130, 125))
        d.ellipse([x + w - 30, cy + 20, x + w - 8, cy + 26], fill=(180, 210, 235)) if cap else None
        d.line([x + 6, cy + 22, x + w - 6, cy + 22], fill=BLUE, width=3)
        if cap:
            d.text((x + 4, y + h - 16), "WINTER RAINS", font=SANS_B(10), fill=TEAL)
    elif idx == 8:  # handshake flags
        fb = y + 34 if cap else y + 20
        d.rectangle([x + 8, y + 10 if cap else y + 4, x + w // 2 - 4, fb], fill=BLUE)
        d.rectangle([x + w // 2 + 4, y + 10 if cap else y + 4, x + w - 8, fb], fill=GOLD)
        if cap:
            for sx in range(5):
                d.ellipse([x + 14 + sx * 18, y + 16, x + 18 + sx * 18, y + 20], fill=(255, 220, 90))
        d.line([x + 8, fb, x + w // 2 - 4, fb], fill=(255, 255, 255), width=1)
        d.line([x + w // 2 + 4, fb, x + w - 8, fb], fill=(255, 255, 255), width=1)
        hy = y + h - 24 if cap else cy + 8
        d.polygon([(x + 14, y + 40 if cap else cy + 2), (cx - 6, y + 40 if cap else cy + 2),
                   (cx, hy), (cx - 12, hy)], fill=BLUE)
        d.polygon([(x + w - 14, y + 40 if cap else cy + 2), (cx + 6, y + 40 if cap else cy + 2),
                   (cx, hy), (cx + 12, hy)], fill=GOLD)
        d.ellipse([cx - 12, hy - 6, cx + 12, hy + 6], fill=(255, 235, 210), outline=INK, width=2)
        d.line([cx - 8, hy, cx + 8, hy], fill=INK, width=1)
        if cap:
            d.text((x + 4, y + h - 16), "UNITED POSITION", font=SANS_B(10), fill=INK)
    elif idx == 9:  # chip
        cs = 16 if cap else 12
        d.rectangle([cx - cs, cy - cs, cx + cs, cy + cs], fill=(40, 45, 60), outline=INK, width=3)
        d.rectangle([cx - cs + 3, cy - cs + 3, cx + cs - 3, cy + cs - 3], outline=(110, 120, 150), width=1)
        for i in range(3):
            px = cx - cs + 6 + i * (2 * cs - 12) // 2 if cap else cx - cs + 4 + i * (2 * cs - 8) // 2
            d.line([px, cy - cs - 8, px, cy - cs], fill=INK, width=2)
            d.line([px, cy + cs, px, cy + cs + 8], fill=INK, width=2)
            d.line([cx - cs - 8, cy - cs + 6 + i * (2 * cs - 12) // 2, cx - cs, cy - cs + 6 + i * (2 * cs - 12) // 2], fill=INK, width=2) if cap else None
            d.line([cx + cs, cy - cs + 6 + i * (2 * cs - 12) // 2, cx + cs + 8, cy - cs + 6 + i * (2 * cs - 12) // 2], fill=INK, width=2) if cap else None
        d.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
        d.rectangle([cx - 6, cy - 6, cx + 6, cy - 2], fill=(255, 120, 110))
        if cap:
            d.text((cx - 3, cy + 10), "AI", font=SANS_B(8), fill=(255, 255, 255))
            d.text((x + 4, y + h - 16), "CHIP PROBE", font=SANS_B(10), fill=INK)
    elif idx == 10:  # virus
        vr = 14 if cap else 11
        d.ellipse([cx - vr, cy - vr, cx + vr, cy + vr], fill=(200, 235, 200), outline=GREEN, width=3)
        for a in range(0, 360, 45):
            r = math.radians(a)
            d.line([cx + vr * math.cos(r), cy + vr * math.sin(r),
                    cx + (vr + 8) * math.cos(r), cy + (vr + 8) * math.sin(r)], fill=GREEN, width=2)
            d.ellipse([cx + (vr + 8) * math.cos(r) - 2, cy + (vr + 8) * math.sin(r) - 2,
                       cx + (vr + 8) * math.cos(r) + 2, cy + (vr + 8) * math.sin(r) + 2], fill=GREEN)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=GREEN)
        d.ellipse([cx - 8, cy + 2, cx - 4, cy + 6], fill=(90, 160, 90))
        d.ellipse([cx + 4, cy - 7, cx + 8, cy - 3], fill=(90, 160, 90))
        if cap:
            d.text((x + 4, y + h - 16), "6 MONTHS ON", font=SANS_B(10), fill=GREEN)
    elif idx == 11:  # rising arrow / yen
        if cap:
            for gy in (y + 12, y + 24, y + 36):
                d.line([x + 6, gy, x + w - 8, gy], fill=(220, 212, 190), width=1)
            d.rectangle([x + 14, y + 34, x + 30, y + h - 20], fill=(190, 220, 190))
            d.rectangle([x + 40, y + 26, x + 56, y + h - 20], fill=(150, 200, 150))
            d.rectangle([x + 66, y + 18, x + 82, y + h - 20], fill=(110, 180, 110))
        else:
            d.rectangle([x + 5, y + 24, x + 12, y + h - 6], fill=(150, 200, 150))
            d.rectangle([x + 15, y + 18, x + 22, y + h - 6], fill=(110, 180, 110))
            d.rectangle([x + 25, y + 12, x + 32, y + h - 6], fill=(90, 160, 90))
        d.line([x + 8, y + h - 20 if cap else y + h - 8, x + w - 10, y + 12], fill=RED, width=3)
        d.polygon([(x + w - 10, y + 12), (x + w - 24, y + 12), (x + w - 10, y + 26)], fill=RED)
        if cap:
            d.text((x + 4, y + h - 16), "CPI +2.2%", font=SANS_B(10), fill=RED)
    elif idx == 12:  # make.fun ghost
        gr12 = 20 if cap else 13
        d.ellipse([cx - gr12 - 4, cy - gr12 - 4, cx + gr12 + 4, cy + gr12 + 4], fill=(235, 225, 250))
        d.ellipse([cx - gr12 + 2, cy - gr12 + 2, cx + gr12 - 2, cy + gr12 - 6], fill=(120, 90, 200))
        d.rectangle([cx - gr12 + 2, cy - 2, cx + gr12 - 2, cy + gr12 - 6], fill=(120, 90, 200))
        tw = 12 if cap else 8
        for gx in (cx - gr12 + 2, cx - tw // 2, cx + gr12 - 2 - tw):
            d.polygon([(gx, cy + gr12 - 6), (gx + tw // 2, cy + gr12 + 2), (gx + tw, cy + gr12 - 6)],
                      fill=(120, 90, 200))
        d.ellipse([cx - 10, cy - 10, cx - 4, cy - 2], fill=INK)
        d.ellipse([cx + 4, cy - 10, cx + 10, cy - 2], fill=INK)
        d.ellipse([cx - 8, cy - 8, cx - 6, cy - 6], fill=(255, 255, 255))
        d.ellipse([cx + 6, cy - 8, cx + 8, cy - 6], fill=(255, 255, 255))
        d.arc([cx - 6, cy - 2, cx + 6, cy + 6], 0, 180, fill=INK, width=2)
        if cap:
            d.ellipse([x + w - 30, y + 8, x + w - 12, y + 26], fill=(255, 210, 80), outline=GOLD, width=2)
            d.text((x + w - 23, y + 11), "$", font=SANS_B(11), fill=GOLD, anchor="ma")
            d.text((x + 4, y + h - 16), "$250 ESCROW", font=SANS_B(10), fill=(120, 90, 200))
    elif idx == 13:  # boat + waves
        bw13 = 20 if cap else 13
        d.polygon([(cx - bw13, cy), (cx + bw13, cy), (cx + bw13 - 8, cy + 12), (cx - bw13 + 8, cy + 12)],
                  outline=BLUE, width=2, fill=(190, 215, 240))
        d.line([cx - bw13 + 4, cy + 6, cx + bw13 - 4, cy + 6], fill=BLUE, width=1)
        d.line([cx, cy, cx, cy - 18], fill=INK, width=2)
        d.polygon([(cx, cy - 18), (cx + 14, cy - 6), (cx, cy - 6)], fill=RED)
        d.polygon([(cx, cy - 18), (cx + 7, cy - 6), (cx, cy - 6)], fill=(255, 150, 140))
        d.polygon([(cx, cy - 16), (cx - 10, cy - 6), (cx, cy - 6)], fill=(255, 255, 255), outline=BLUE, width=1)
        for wy in ((cy + 20, cy + 28) if cap else (cy + 16,)):
            d.arc([x + 6, wy - 6, x + w - 6, wy + 6], 0, 180, fill=BLUE, width=2)
        if cap:
            d.text((x + 4, y + h - 16), "4 DEAD, DOZENS LOST", font=SANS_B(9), fill=BLUE)
    else:  # 14 shield / raid
        sh = 20 if cap else 13
        d.polygon([(cx, y + 8 if cap else y + 2), (cx + sh, y + 16 if cap else y + 8),
                   (cx + sh, y + 34 if cap else cy + 6), (cx, y + 52 if cap else y + h - 4),
                   (cx - sh, y + 34 if cap else cy + 6), (cx - sh, y + 16 if cap else y + 8)],
                  fill=(250, 225, 220), outline=RED, width=3)
        d.polygon([(cx, y + 12 if cap else y + 6), (cx + sh - 5, y + 18 if cap else y + 10),
                   (cx + sh - 5, y + 32 if cap else cy + 4), (cx, y + 46 if cap else y + h - 8),
                   (cx - sh + 5, y + 32 if cap else cy + 4), (cx - sh + 5, y + 18 if cap else y + 10)],
                  outline=(200, 120, 110), width=1)
        d.text((cx - 5, cy - 8), "34", font=SANS_B(16 if cap else 11), fill=RED)
        if cap:
            d.text((x + 4, y + h - 16), "CORRIDOR RETAKEN", font=SANS_B(9), fill=RED)

def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 14
    # --- masthead ---
    d.text((W // 2, 8), "THE TWENTIETH", font=SERIF_B(58), fill=INK, anchor="ma")
    d.line([M, 72, W - M, 72], fill=INK, width=2)
    d.text((W // 2, 78), "FRIDAY 20 NOVEMBER 2026  •  THE WORLD IN ONE DAY",
           font=SANS_B(24), fill=RED, anchor="ma")
    d.text((W // 2, 110), "Cyclone Akvan hits India  •  Kyiv's bridges struck overnight  •  COP31 deadlocked  •  Asia's markets tumble",
           font=SERIF(15), fill=INK, anchor="ma")
    # --- region strip (sums to 40) ---
    counts = {}
    for _, r, *_ in STORIES:
        counts[r] = counts.get(r, 0) + 1
    for _, r, *_ in BRIEFS:
        counts[r] = counts.get(r, 0) + 1
    y = 138
    x = M
    total_w = W - 2 * M
    for name, code, col in REGIONS:
        n = counts[code]
        seg = total_w * n // 40
        d.rectangle([x, y, x + seg - 2, y + 22], fill=col)
        d.text((x + seg // 2 - 1, y + 3), f"{name} {n}", font=SANS_B(11),
               fill=(255, 255, 255), anchor="ma")
        x += seg
    d.text((W // 2, y + 26), "",
           font=SANS_B(11), fill=GREY, anchor="ma")
    # --- stat strip: 6 numbers ---
    stats = [("110", "missiles at Ukraine"), ("300,000+", "evacuated in Odisha"),
             ("-4.8%", "Nikkei, Friday"), ("3", "Kyiv bridges hit"),
             ("1,000+", "drones pledged by UK"), ("34", "killed in Haiti raid")]
    y = 168
    bw = (W - 2 * M) // 6
    for i, (num, lab) in enumerate(stats):
        bx = M + i * bw
        d.rectangle([bx + 2, y, bx + bw - 2, y + 34], outline=LINE, width=1, fill=PAPER2)
        d.text((bx + bw // 2, y + 2), num, font=SANS_B(15), fill=RED, anchor="ma")
        d.text((bx + bw // 2, y + 19), lab, font=SANS(10), fill=INK, anchor="ma")
    # --- 4 heroes ---
    y0 = 214
    cw = (W - 2 * M - 3 * 8) // 4
    for i, (num, reg, head, summ, src, lab) in enumerate(STORIES[:4]):
        x = M + i * (cw + 8)
        col = REG_COL[reg]
        d.rectangle([x, y0, x + cw, y0 + 176], outline=LINE, width=1, fill=(255, 252, 240))
        d.rectangle([x, y0, x + cw, y0 + 20], fill=col)
        d.text((x + 6, y0 + 2), f"{num:02d}", font=SANS_B(13), fill=(255, 255, 255))
        d.text((x + cw - 6, y0 + 3), reg, font=SANS_B(11), fill=(255, 255, 255), anchor="ra")
        draw_illus(d, num, x + 4, y0 + 24, cw - 8, 62)
        lines = wrap(d, head, SERIF_B(13), cw - 10)
        yy = y0 + 90
        for ln in lines[:2]:
            d.text((x + 5, yy), ln, font=SERIF_B(13), fill=INK)
            yy += 16
        lines = wrap(d, summ, SANS(11), cw - 10)
        for ln in lines[:3]:
            d.text((x + 5, yy), ln, font=SANS(11), fill=INK)
            yy += 13
        d.text((x + 5, y0 + 176 - 13), f"({src})", font=SANS(9), fill=GREY)
    # --- map band + DATE CHECK ---
    my0 = 398
    d.rectangle([M, my0, 700, my0 + 78], outline=LINE, width=1, fill=(238, 232, 205))
    d.text((M + 6, my0 + 4), "WHERE IT HAPPENED — the 14 drawn stories, numbered", font=SANS_B(11), fill=INK)
    # simplified real coastlines, hand-plotted in the band's coordinate space
    # (vertical relief exaggerated so peninsulas read in this flat band)
    d.polygon([(29, my0 + 26), (54, my0 + 24), (120, my0 + 24), (150, my0 + 26), (165, my0 + 32),
               (180, my0 + 27), (187, my0 + 27), (234, my0 + 30), (247, my0 + 33), (206, my0 + 37),
               (196, my0 + 50), (177, my0 + 41), (170, my0 + 50), (192, my0 + 52), (198, my0 + 52),
               (149, my0 + 45), (137, my0 + 48), (113, my0 + 37), (92, my0 + 29)],
              fill=(215, 205, 170))  # N America (Hudson Bay notch, Florida, Mexico, Baja)
    d.polygon([(244, my0 + 26), (263, my0 + 23), (301, my0 + 24), (282, my0 + 28), (258, my0 + 29)],
              fill=(215, 205, 170))  # Greenland
    d.polygon([(194, my0 + 44), (232, my0 + 42), (238, my0 + 46), (198, my0 + 48)],
              fill=(215, 205, 170))  # Cuba
    d.polygon([(212, my0 + 45), (226, my0 + 45), (224, my0 + 49), (212, my0 + 49)],
              fill=(215, 205, 170))  # Hispaniola (Haiti)
    d.polygon([(202, my0 + 54), (226, my0 + 54), (290, my0 + 57), (257, my0 + 65), (219, my0 + 76),
               (211, my0 + 68), (196, my0 + 57)], fill=(215, 205, 170))  # S America
    d.polygon([(331, my0 + 36), (331, my0 + 35), (344, my0 + 33), (367, my0 + 28), (388, my0 + 22),
               (405, my0 + 25), (405, my0 + 34), (392, my0 + 35), (380, my0 + 34), (366, my0 + 33),
               (342, my0 + 36)], fill=(215, 205, 170))  # Europe
    d.polygon([(340, my0 + 25), (349, my0 + 25), (347, my0 + 32), (339, my0 + 32)],
              fill=(215, 205, 170))  # UK
    d.polygon([(337, my0 + 42), (354, my0 + 41), (409, my0 + 44), (448, my0 + 50), (424, my0 + 54),
               (409, my0 + 65), (386, my0 + 72), (371, my0 + 63), (371, my0 + 56), (324, my0 + 49),
               (316, my0 + 47)], fill=(215, 205, 170))  # Africa
    d.polygon([(409, my0 + 37), (462, my0 + 24), (557, my0 + 22), (671, my0 + 26), (652, my0 + 30),
               (580, my0 + 40), (548, my0 + 49), (544, my0 + 57), (497, my0 + 57), (485, my0 + 45),
               (461, my0 + 53), (453, my0 + 43), (432, my0 + 40)], fill=(215, 205, 170))  # Asia
    d.polygon([(604, my0 + 29), (618, my0 + 33), (616, my0 + 46), (604, my0 + 44)],
              fill=(215, 205, 170))  # Japan
    d.polygon([(538, my0 + 54), (568, my0 + 54), (564, my0 + 58), (540, my0 + 58)],
              fill=(215, 205, 170))  # Indonesia west
    d.polygon([(574, my0 + 55), (602, my0 + 54), (600, my0 + 58), (576, my0 + 58)],
              fill=(215, 205, 170))  # Indonesia east
    d.polygon([(565, my0 + 62), (599, my0 + 66), (633, my0 + 64), (633, my0 + 71), (605, my0 + 70),
               (567, my0 + 67), (563, my0 + 64)], fill=(215, 205, 170))  # Australia
    d.polygon([(676, my0 + 68), (686, my0 + 72), (680, my0 + 76)], fill=(215, 205, 170))  # NZ
    pins = {1: (494, 46), 2: (396, 30), 3: (386, 42), 4: (592, 34), 5: (190, 34),
            6: (374, 30), 7: (404, 43), 8: (358, 30), 9: (102, 38), 10: (363, 55),
            11: (610, 46), 12: (336, 26), 13: (302, 47), 14: (200, 46)}
    for n, (px, py) in pins.items():
        px = M + px
        py = my0 + py
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py - 5), str(n), font=SANS_B(8), fill=(255, 255, 255), anchor="ma")
    # DATE CHECK box
    dx0, dy0 = 710, my0
    d.rectangle([dx0, dy0, W - M, dy0 + 78], outline=RED, width=2, fill=(255, 240, 235))
    d.text((dx0 + 6, dy0 + 3), "DATE CHECK — NOT 20 NOVEMBER", font=SANS_B(11), fill=RED)
    chk = ("19 Nov, NOT today: Shenzhen summit; Anthropic IPO $83 / +17%; ICJ Myanmar ruling; "
           "GTA VI launch; Crimea bridge; Riyadh tower; Fiji drought; US-Venezuela deal. "
           "Not yet happened: any COP31 final deal; Asia closing prices.")
    for j, ln in enumerate(wrap(d, chk, SANS(10), W - M - dx0 - 12)):
        d.text((dx0 + 6, dy0 + 19 + j * 12), ln, font=SANS(10), fill=INK)
    # --- features 05-14: 2 cols x 5 rows ---
    fy = 486
    rh = 46
    fw = (W - 2 * M - 8) // 2
    for i, (num, reg, head, summ, src, lab) in enumerate(STORIES[4:]):
        col_i, row_i = i % 2, i // 2
        x = M + col_i * (fw + 8)
        y = fy + row_i * rh
        col = REG_COL[reg]
        d.rectangle([x, y, x + fw, y + rh - 4], outline=LINE, width=1, fill=(255, 252, 240))
        d.rectangle([x, y, x + 34, y + rh - 4], fill=col)
        d.text((x + 17, y + 4), f"{num:02d}", font=SANS_B(12), fill=(255, 255, 255), anchor="ma")
        d.text((x + 17, y + 22), reg, font=SANS_B(10), fill=(255, 255, 255), anchor="ma")
        d.text((x + 40, y + 2), head, font=SANS_B(12), fill=INK)
        lines = wrap(d, summ + f" ({src})", SANS(11), fw - 90)
        yy = y + 18
        for ln in lines[:2]:
            d.text((x + 40, yy), ln, font=SANS(11), fill=INK)
            yy += 13
        draw_illus(d, num, x + fw - 44, y + 2, 40, 38, cap=False)
    # --- briefs 15-40: 2 cols x 13 rows ---
    by = fy + 5 * rh + 4
    d.text((M, by), "THE REST OF THE DAY — briefs 15-40", font=SANS_B(12), fill=INK)
    by += 16
    brh = 17
    bw2 = (W - 2 * M - 8) // 2
    for i, (num, reg, text, src) in enumerate(BRIEFS):
        col_i, row_i = i % 2, i // 2
        x = M + col_i * (bw2 + 8)
        y = by + row_i * brh
        d.text((x, y), f"{num}.", font=SANS_B(11), fill=REG_COL[reg])
        d.text((x + 24, y), f"{text} ({src})", font=SANS(11), fill=INK)
    # --- footer ---
    fy2 = by + 13 * brh + 4
    d.line([M, fy2, W - M, fy2], fill=LINE, width=1)
    d.text((M, fy2 + 4),
           "Sources: Reuters, CNN, BBC, Morningstar/Dow Jones, Finnhub, Japan Times, CNBC, France 24, "
           "Al Jazeera, UN Geneva, make.fun, and others named per story.",
           font=SANS(9), fill=GREY)
    d.text((M, fy2 + 16),
           "All 40 stories happened or were first reported Friday 20 November 2026. Story 37 is a forecast; "
           "no COP31 final deal had been reached at press time.",
           font=SANS(9), fill=GREY)
    img.save("entry.png", optimize=True)

if __name__ == "__main__":
    main()
    print("wrote entry.png")
