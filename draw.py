#!/usr/bin/env python3
"""Draw 'The World in One Day' - Tuesday 24 November 2026.
Build-time renderer (PIL). Writes entry.png, 1024x1024, deterministic.
All 36 stories verified against wire reports of 24 Nov 2026 (see STORIES).
Layout is original: masthead, numbers strip, 3 illustrated heroes,
10 illustrated secondaries, dotted world map with numbered pins,
36-story index, DATE CHECK box. Certainty taxonomy: REPORTED / CLAIM / ONGOING.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (25, 25, 25)
NAVY = (22, 48, 94)
NAVY_DK = (16, 34, 66)
RED = (163, 22, 33)
TEAL = (14, 95, 91)
GOLD = (138, 109, 27)
GREY = (90, 90, 90)
LINE = (120, 110, 88)
SEA = (220, 232, 234)
LAND_DOT = (198, 178, 140)

FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_I = lambda s: F("DejaVuSerif.ttf", s)  # no oblique sans on this box; serif reads as editorial note

REGION_COLORS = {
    "EUROPE": (22, 48, 94),
    "MIDDLE EAST": (163, 22, 33),
    "ASIA": (120, 40, 130),
    "AFRICA": (176, 96, 0),
    "AMERICAS": (14, 95, 91),
    "OCEANIA": (0, 110, 150),
    "GLOBAL": (70, 70, 70),
}
CERT_COLORS = {"REPORTED": (34, 120, 50), "CLAIM": (163, 22, 33), "ONGOING": (22, 80, 160)}

# (num, region, place, headline, body, source, certainty)
HEROES = [
    (1, "EUROPE", "MOSCOW / KYIV",
     "Russia says it downed 699 drones",
     "Moscow says air defences intercepted 699 Ukrainian drones overnight, "
     "355 of them aimed at the capital.",
     "RUSSIAN DEFENCE MINISTRY / MEDUZA", "CLAIM"),
    (2, "MIDDLE EAST", "STRAIT OF HORMUZ",
     "Iran's Guards say tankers hit mines",
     "Tehran says three oil tankers hit naval mines in the Strait of Hormuz "
     "and caught fire, then a fourth.",
     "IRNA / REUTERS", "CLAIM"),
    (3, "ASIA", "WASHINGTON / SHENZHEN",
     "Huawei guilty on trade secrets",
     "A US jury convicts Huawei of conspiring to steal trade secrets and bank "
     "fraud, but acquits it of racketeering.",
     "AP / REUTERS", "REPORTED"),
]

SECONDARIES = [
    (4, "ASIA", "SEOUL / TOKYO", "Chip stocks lift Asia",
     "Kospi +7%, Nikkei +3.9%, S&P +4.7%, Nasdaq +6.5% after Nvidia's rally.",
     "REUTERS", "REPORTED", "chart"),
    (5, "MIDDLE EAST", "BAGHDAD", "Baghdad seizes Kurdish oilfields",
     "Kirkuk, Diyala, Salahuddin and Nineveh fields go to the federal Oil Ministry.",
     "REUTERS", "REPORTED", "derrick"),
    (6, "ASIA", "KUALA LUMPUR", "Malaysia to send 6,500 Rohingya back",
     "Anwar: 1,500 go by navy ship on 6-7 Dec and 5,303 by air in December.",
     "AFP", "REPORTED", "ship"),
    (7, "EUROPE", "PARIS", "Sanofi buys Insmed for $41bn",
     "Sanofi agrees $175 a share in cash, the year's biggest biotech deal.",
     "WSJ", "REPORTED", "pill"),
    (8, "MIDDLE EAST", "GAZA", "Strike kills Hamas security chief",
     "An Israeli strike kills Hamas security chief Naeem Abu Nahel and six others.",
     "MEDICS", "REPORTED", "flame"),
    (9, "EUROPE", "BRUSSELS", "NATO vows to defend space",
     "Rutte: NATO will answer reports Russia may deploy a nuclear-armed satellite.",
     "BBC", "REPORTED", "satellite"),
    (10, "EUROPE", "ZAPORIZHZHIA", "Strike kills 2, wounds 40",
     "An overnight attack kills two and wounds about 40, including four children.",
     "REUTERS", "REPORTED", "warn"),
    (11, "AFRICA", "DAKAR", "CAS restores Senegal as AFCON champions",
     "A sports court appeal reinstates Senegal as 2025 Africa Cup winners.",
     "CAS", "REPORTED", "trophy"),
    (12, "OCEANIA", "HONIARA", "Solomons tells China pact will end",
     "Honiara tells Beijing the 2022 pact ends; a new Australia treaty follows.",
     "SYDNEY MORNING HERALD", "REPORTED", "flag"),
    (13, "AMERICAS", "CARTAGENA", "25 held hostage at Cartagena store",
     "Armed men seize a Cartagena supermarket and hold 25 people.",
     "PRESIDENT'S OFFICE", "ONGOING", "store"),
]

# (num, place, headline, source)
ALSO = [
    (14, "Budapest", "Magyar meets Zelensky in Uzhhorod; energy, transport and minority-rights deals", "KYIV INDEPENDENT"),
    (15, "Berlin", "Germany first to access Ukraine's Delta combat system", "KYIV INDEPENDENT"),
    (16, "Washington", "Pentagon delays about 60 Patriot interceptors for Ukraine", "AP"),
    (17, "Kyiv", "Zelensky: US envoys push a peace deal by January; Kyiv will turn to Congress if it fails", "AP"),
    (18, "Moscow", "Putin admits refinery strikes burden Russia; crude runs down 45% since late Oct", "REUTERS"),
    (19, "Seoul", "Russian aircraft enter South Korea's air defence zone", "JCS"),
    (20, "Warsaw", "Russian drone briefly enters Polish airspace; Warsaw summons envoy", "POLISH AUTHORITIES"),
    (21, "The Hague", "Fourteen countries recognise the ICJ's Rohingya genocide ruling", "ICJ"),
    (22, "New York", "Guterres wants a multilateral AI-risk framework within a year", "UN"),
    (23, "Beijing", "China sentences an official to death for spying for a foreign country", "WIRES"),
    (24, "Ituri", "Fighting traps DR Congo Ebola responders near a hospital", "WHO"),
    (25, "Tripoli", "Libya's Haftar visits Turkey for the first time", "WIRES"),
    (26, "Aden", "Houthis 60 km from Aden and ready to attack; Riyadh tower hit, 11 hurt", "AL JAZEERA"),
    (27, "London", "UK sanctions Yemen's Houthis and four senior officials", "WIRES"),
    (28, "Beijing", "China opens Tiangong station to its first foreign astronaut, from Pakistan", "STRAITS TIMES"),
    (29, "Villavicencio", "Car bomb destroys buildings; no confirmed victims", "PRESIDENT'S OFFICE"),
    (30, "Washington", "Trump orders the DOJ to expedite federal death sentences", "AP"),
    (31, "Pennsylvania", "Ninth measles death in an outbreak across 46 counties", "CDC"),
    (32, "Seoul", "South Korea offers up to $375,000 to catch AI cheats in its college exam", "WIRES"),
    (33, "Tehran", "Singer Parastoo Ahmadi given 74 lashes, rights groups say", "HR GROUPS"),
    (34, "Kathmandu", "Nepal quake, magnitude 5.6, shakes the east; no casualties", "NEMRC"),
    (35, "Mexico City", "Mexico to try 'El Chapo Isidro' at home, turning down a US request", "THE HINDU"),
    (36, "Port Moresby", "Bougainville vote begins: PNG parliament opens ratification of the 2019 result", "THE CONVERSATION"),
]

NUMBERS = [
    ("699", "drones Russia says it downed"),
    ("6,500+", "Rohingya Malaysia will return"),
    ("$41BN", "Sanofi's cash deal for Insmed"),
    ("+7%", "Kospi rebound on chip stocks"),
    ("4", "tankers Iran says hit mines"),
    ("25", "hostages held in Cartagena"),
]

# lon/lat for map pins: (num, lon, lat, dx_px, dy_px)
PINS = [
    (1, 37.6, 55.7, 0, 0), (2, 56.5, 27.0, 0, 0), (3, 116.4, 39.9, 0, 0), (4, 127.0, 37.5, 0, 0),
    (5, 44.4, 33.3, 0, 0), (6, 101.7, 3.1, 0, 0), (7, 2.35, 48.85, -9, 0), (8, 34.5, 31.5, 0, 0),
    (9, 13.4, 52.5, 0, 0), (10, 29.0, 48.0, 0, 7), (11, -17.4, 14.7, 0, 0), (12, 160.0, -9.4, 0, 0),
    (13, -75.5, 10.4, 0, 0), (14, 19.0, 47.5, 0, 0), (19, 133.0, 40.0, 13, 0), (21, 4.3, 52.1, 0, -10),
    (22, -74.0, 40.7, 0, 0), (25, 13.2, 32.9, 0, 0), (28, 124.0, 42.0, 13, 6), (36, 147.1, -9.5, 0, 0),
]


def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_wrapped(d, x, y, text, font, fill, max_w, lh):
    for ln in wrap(d, text, font, max_w):
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def badge(d, x, y, text, bg, fg=(255, 255, 255), font=None):
    font = font or SANS_B(9)
    w = d.textlength(text, font=font) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=bg)
    d.text((x + 5, y + 2), text, font=font, fill=fg)
    return w


def draw_scene(d, kind, x, y, w, h):
    """Original vector-style scene per hero kind."""
    if kind == "drones":
        d.rectangle([x, y, x + w, y + h], fill=(18, 32, 63))
        import random
        rnd = random.Random(24)
        for _ in range(46):
            sx = x + rnd.randint(4, w - 4)
            sy = y + rnd.randint(4, h - 24)
            d.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 220, 230))
        # flight paths
        for k in range(3):
            yy = y + 26 + k * 26
            d.line([(x + 8, yy), (x + w - 40, yy - 12)], fill=(200, 60, 60), width=2)
            for t in range(0, 9):
                px = x + 14 + t * 30
                py = yy - int(t * 1.3)
                d.polygon([(px, py - 5), (px + 9, py), (px, py + 5), (px - 9, py)],
                          fill=(235, 235, 240))
                d.line([(px - 12, py - 7), (px + 12, py - 7)], fill=(160, 160, 170), width=1)
                d.line([(px - 12, py + 7), (px + 12, py + 7)], fill=(160, 160, 170), width=1)
        d.text((x + 10, y + h - 46), "699", font=SERIF_B(40), fill=(255, 255, 255))
        d.text((x + 108, y + h - 30), "DRONES DOWNED", font=SANS_B(11), fill=(255, 210, 210))
    elif kind == "hormuz":
        d.rectangle([x, y, x + w, y + h], fill=(188, 214, 226))
        d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(46, 111, 142))
        # sun
        d.ellipse([x + w - 62, y + 10, x + w - 22, y + 50], fill=(255, 214, 120))
        # tanker
        hx, hy = x + 30, y + int(h * 0.52)
        d.rectangle([hx, hy, hx + 190, hy + 26], fill=(30, 30, 34))
        for cx in range(4):
            d.rectangle([hx + 12 + cx * 44, hy - 22, hx + 48 + cx * 44, hy], fill=(150 + cx * 8, 60, 50))
        d.rectangle([hx + 168, hy - 40, hx + 190, hy], fill=(220, 220, 220))
        d.line([(hx - 8, hy + 30), (hx + 60, hy + 30)], fill=(255, 255, 255), width=2)
        d.line([(hx + 120, hy + 34), (hx + 210, hy + 34)], fill=(255, 255, 255), width=2)
        # mines
        for mx, my in [(x + w - 78, y + h - 34), (x + w - 130, y + h - 22), (x + 210, y + h - 28)]:
            for a in range(8):
                import math
                ang = a * math.pi / 4
                d.line([(mx, my), (mx + int(11 * math.cos(ang)), my + int(11 * math.sin(ang)))],
                       fill=(20, 20, 20), width=2)
            d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(20, 20, 20))
        d.text((x + 10, y + 8), "4 TANKERS", font=SANS_B(15), fill=(22, 48, 94))
    else:  # huawei courthouse
        d.rectangle([x, y, x + w, y + h], fill=(232, 224, 204))
        # courthouse
        bx, by = x + 62, y + 34
        d.polygon([(bx, by), (bx + 200, by), (bx + 100, by - 26)], fill=(22, 48, 94))
        for cx in range(4):
            d.rectangle([bx + 14 + cx * 48, by, bx + 30 + cx * 48, by + 62], fill=(240, 238, 230))
        d.rectangle([bx - 8, by + 62, bx + 208, by + 72], fill=(22, 48, 94))
        d.rectangle([bx - 8, by + 72, bx + 208, by + 80], fill=(120, 110, 88))
        # gavel
        d.rectangle([x + w - 96, y + h - 44, x + w - 30, y + h - 26], fill=(120, 72, 32))
        d.line([(x + w - 60, y + h - 30), (x + w - 30, y + h - 8)], fill=(90, 54, 24), width=5)
        # GUILTY stamp
        st = Image.new("RGBA", (150, 44), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        sd.rectangle([2, 2, 147, 41], outline=(163, 22, 33), width=3)
        sd.text((10, 8), "GUILTY", font=SERIF_B(26), fill=(163, 22, 33))
        st = st.rotate(-7, expand=True, resample=Image.BICUBIC)
        d._image.paste(st, (x + 12, y + h - 58), st)


def draw_icon(d, kind, x, y, s, color):
    d.rounded_rectangle([x, y, x + s, y + s], radius=4, fill=color)
    c = (255, 255, 255)
    if kind == "chart":
        d.line([(x + 5, y + s - 7), (x + 12, y + s - 14), (x + 18, y + s - 10), (x + s - 5, y + 6)],
               fill=c, width=2)
        d.polygon([(x + s - 9, y + 6), (x + s - 4, y + 6), (x + s - 6, y + 11)], fill=c)
    elif kind == "derrick":
        d.polygon([(x + s // 2, y + 4), (x + 6, y + s - 5), (x + s - 6, y + s - 5)], outline=c, width=2)
        d.line([(x + s // 2, y + 4), (x + s // 2, y + s - 5)], fill=c, width=2)
    elif kind == "ship":
        d.polygon([(x + 5, y + 14), (x + s - 5, y + 14), (x + s - 9, y + s - 5), (x + 9, y + s - 5)], fill=c)
        d.rectangle([x + 8, y + 6, x + s - 8, y + 13], fill=c)
    elif kind == "pill":
        d.rounded_rectangle([x + 5, y + s // 2 - 5, x + s - 5, y + s // 2 + 5], radius=5, fill=c)
        d.line([(x + s // 2, y + s // 2 - 5), (x + s // 2, y + s // 2 + 5)], fill=(163, 22, 33), width=2)
    elif kind == "flame":
        d.polygon([(x + s // 2, y + 4), (x + s - 6, y + 16), (x + s - 7, y + s - 5),
                   (x + 7, y + s - 5), (x + 6, y + 16)], fill=c)
    elif kind == "satellite":
        d.rectangle([x + s // 2 - 4, y + s // 2 - 4, x + s // 2 + 4, y + s // 2 + 4], fill=c)
        d.rectangle([x + 3, y + s // 2 - 6, x + s // 2 - 6, y + s // 2 + 6], outline=c, width=2)
        d.rectangle([x + s // 2 + 6, y + s // 2 - 6, x + s - 3, y + s // 2 + 6], outline=c, width=2)
    elif kind == "warn":
        d.polygon([(x + s // 2, y + 4), (x + s - 5, y + s - 5), (x + 5, y + s - 5)], outline=c, width=2)
        d.text((x + s // 2 - 2, y + 11), "!", font=SANS_B(11), fill=c)
    elif kind == "trophy":
        d.polygon([(x + 7, y + 5), (x + s - 7, y + 5), (x + s - 10, y + 16), (x + 10, y + 16)], fill=c)
        d.rectangle([x + s // 2 - 2, y + 16, x + s // 2 + 2, y + s - 7], fill=c)
        d.rectangle([x + 8, y + s - 7, x + s - 8, y + s - 4], fill=c)
    elif kind == "flag":
        d.line([(x + 7, y + 5), (x + 7, y + s - 5)], fill=c, width=2)
        d.polygon([(x + 7, y + 5), (x + s - 5, y + 9), (x + 7, y + 14)], fill=c)
    else:  # store
        d.rectangle([x + 5, y + 12, x + s - 5, y + s - 5], outline=c, width=2)
        for i in range(4):
            d.rectangle([x + 5 + i * 6, y + 6, x + 10 + i * 6, y + 12], fill=c)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)

    # --- masthead bar ---
    d.rectangle([8, 8, W - 8, 36], fill=NAVY)
    d.text((16, 14), "THE WORLD IN ONE DAY", font=SANS_B(14), fill=(255, 255, 255))
    mid = "TUESDAY 24 NOVEMBER 2026"
    d.text(((W - d.textlength(mid, font=SANS_B(13))) / 2, 15), mid, font=SANS_B(13),
           fill=(255, 220, 130))
    right = "36 STORIES  ·  7 REGIONS"
    d.text((W - 16 - d.textlength(right, font=SANS_B(13)), 15), right, font=SANS_B(13),
           fill=(255, 255, 255))

    # --- giant date ---
    title = "Tuesday 24 November 2026"
    tf = SERIF_B(56)
    d.text(((W - d.textlength(title, font=tf)) / 2, 42), title, font=tf, fill=INK)
    sub = "36 STORIES, ALL FROM TUESDAY 24 NOV  ·  EUROPE 10  ·  MIDDLE EAST 5  ·  ASIA 8  ·  AFRICA 3  ·  AMERICAS 6  ·  OCEANIA 2  ·  GLOBAL 2"
    sf = SANS_B(12)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 104), sub, font=sf, fill=NAVY)
    tick = "Russia says it downed 699 drones   ◆   Iran's Guards say tankers hit mines   ◆   Malaysia to send 6,500 Rohingya back"
    tif = SANS_I(12)
    d.text(((W - d.textlength(tick, font=tif)) / 2, 122), tick, font=tif, fill=(60, 60, 60))
    d.line([(14, 140), (W - 14, 140)], fill=LINE, width=1)

    # --- numbers strip ---
    x0, y0 = 14, 146
    cw = (W - 28) / 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = x0 + i * cw
        nf = SERIF_B(30)
        d.text((cx + (cw - d.textlength(num, font=nf)) / 2, y0), num, font=nf,
               fill=RED if i in (0, 2) else NAVY)
        text_wrapped(d, cx + 6, y0 + 34, lab, SANS(9), GREY, cw - 12, 11)
        if i:
            d.line([(cx, y0 + 2), (cx, y0 + 52)], fill=LINE, width=1)
    d.line([(14, 204), (W - 14, 204)], fill=LINE, width=1)

    # --- heroes ---
    hy = 212
    hw, gap = 324, 12
    for i, (num, region, place, head, body, src, cert) in enumerate(HEROES):
        x = 14 + i * (hw + gap)
        kind = ["drones", "hormuz", "huawei"][i]
        draw_scene(d, kind, x, hy, hw, 128)
        badge(d, x + hw - 74, hy + 6, cert, CERT_COLORS[cert])
        # tag bar
        ty = hy + 134
        col = REGION_COLORS[region]
        d.rectangle([x, ty, x + hw, ty + 16], fill=col)
        d.text((x + 6, ty + 2), "%s · %s" % (region, place), font=SANS_B(9), fill=(255, 255, 255))
        d.text((x + hw - 20, ty + 2), str(num), font=SANS_B(10), fill=(255, 220, 130))
        y = text_wrapped(d, x, ty + 20, head, SERIF_B(18), INK, hw, 21)
        y = text_wrapped(d, x, y + 2, body, SANS(10.5), (50, 50, 50), hw, 13)
        d.text((x, y + 3), src, font=SANS_B(8), fill=GREY)

    # --- secondaries: 2 rows x 5 ---
    sy = 452
    sw, sh = 196, 90
    for i, (num, region, place, head, body, src, cert, icon) in enumerate(SECONDARIES):
        r, c = divmod(i, 5)
        x = 14 + c * (sw + 2)
        y = sy + r * (sh + 6)
        col = REGION_COLORS[region]
        d.rectangle([x, y, x + sw, y + sh], outline=(200, 192, 170), width=1)
        d.rectangle([x, y, x + sw, y + 3], fill=col)
        draw_icon(d, icon, x + 6, y + 10, 26, col)
        d.text((x + 38, y + 8), "%d · %s" % (num, place), font=SANS_B(8), fill=col)
        badge(d, x + sw - 62, y + 8, cert, CERT_COLORS[cert], font=SANS_B(7))
        yy = text_wrapped(d, x + 38, y + 22, head, SANS_B(10.5), INK, sw - 44, 13)
        text_wrapped(d, x + 6, y + 54, body, SANS(8.5), (50, 50, 50), sw - 12, 11)
        d.text((x + 6, y + sh - 11), src, font=SANS_B(7), fill=GREY)

    # --- dotted world map ---
    my = 640
    d.text((14, my), "WHERE IT HAPPENED", font=SANS_B(11), fill=INK)
    d.text((170, my + 1), "pins carry the story numbers", font=SANS_I(10), fill=GREY)
    mx0, my0, mw, mh = 14, my + 18, 996, 110
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=SEA)
    blobs = [(-100, 45, 55, 22), (-42, 74, 12, 8), (-60, -15, 18, 28), (15, 52, 22, 12),
             (20, 5, 22, 30), (90, 50, 60, 22), (105, 10, 18, 12), (134, -25, 18, 10),
             (-2, 54, 4, 6), (138, 37, 5, 9), (172, -41, 4, 7), (115, -2, 20, 5)]

    def to_xy(lon, lat):
        return (mx0 + (lon + 180) / 370.0 * mw, my0 + (75 - lat) / 135.0 * mh)

    step = 9
    yy = my0 + 4
    while yy < my0 + mh - 2:
        xx = mx0 + 4
        while xx < mx0 + mw - 2:
            lon = (xx - mx0) / mw * 370.0 - 180
            lat = 75 - (yy - my0) / mh * 135.0
            inside = False
            for clon, clat, rx, ry in blobs:
                if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1:
                    inside = True
                    break
            if inside:
                d.ellipse([xx - 1.6, yy - 1.6, xx + 1.6, yy + 1.6], fill=LAND_DOT)
            xx += step
        yy += step
    for num, lon, lat, dx, dy in PINS:
        px, py = to_xy(lon, lat)
        px += dx
        py += dy
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=(255, 255, 255), width=1)
        t = str(num)
        tf2 = SANS_B(7 if num < 10 else 6)
        d.text((px - d.textlength(t, font=tf2) / 2, py - 4), t, font=tf2, fill=(255, 255, 255))

    # --- ALSO list ---
    ay = my0 + mh + 10
    d.text((14, ay), "ALSO ON TUESDAY 24 NOVEMBER", font=SANS_B(11), fill=INK)
    d.text((280, ay + 1), "23 more stories", font=SANS_I(10), fill=GREY)
    d.line([(14, ay + 16), (W - 14, ay + 16)], fill=LINE, width=1)
    ly = ay + 22
    col_w = 492
    for i, (num, place, head, src) in enumerate(ALSO):
        col_i, row = divmod(i, 12)
        x = 14 + col_i * (col_w + 8)
        y = ly + row * 10.5
        d.text((x, y), "%d" % num, font=SANS_B(9), fill=RED)
        d.text((x + 20, y), place, font=SANS_B(9), fill=NAVY)
        hx = x + 20 + d.textlength(place + "  ", font=SANS_B(9))
        sw_ = d.textlength(src, font=SANS_B(7))
        avail = (x + col_w - sw_ - 8) - hx
        hf = SANS(9)
        htext = head
        while htext and d.textlength(htext, font=hf) > avail:
            htext = htext[:-1]
        if htext != head:
            htext = htext.rstrip() + "…"
        d.text((hx, y), htext, font=hf, fill=INK)
        d.text((x + col_w - sw_, y + 1), src, font=SANS_B(7), fill=GREY)
    by = ly + 12 * 10.5 + 6

    # --- DATE CHECK ---
    d.rectangle([14, by, W - 14, by + 56], outline=RED, width=2)
    d.text((22, by + 5), "DATE CHECK", font=SANS_B(11), fill=RED)
    dc = ("Every story on this page happened, or was first reported, on Tuesday 24 November 2026. "
          "Left out because they happened on an earlier day: Mon 23 Nov — Nvidia reinstates Huang; "
          "EU unveils its 22nd Russia sanctions; Zelensky at the NATO assembly; Murmansk governor "
          "arrested. Sun 22 Nov — COP31 ends with no deal; Verstappen wins the Las Vegas GP. "
          "Sat 21 Nov — Banten factory fire. Fri 20 Nov — Kh-101 missiles in Poland. "
          "Hormuz: Iran first told of the mine hits on 24 Nov; its media date the hits 22–23 Nov.")
    text_wrapped(d, 22, by + 20, dc, SANS(9.5), (50, 50, 50), W - 44, 12)

    # --- footer ---
    fy = by + 62
    d.text((14, fy), "Sources: Reuters · AP · AFP · BBC · WSJ · Al Jazeera · UN · WHO · CAS · Meduza · Wires   —   CERTAINTY:  REPORTED = wires confirm  ·  CLAIM = one side's account  ·  ONGOING = still unfolding",
           font=SANS(8.5), fill=GREY)

    out = os.environ.get("ENTRY_OUTPUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
