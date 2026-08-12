"""
Figure 2.5: contextual letter shapes in the Arabic script.

Redrawn for three reasons:

  1. The letter-name column used the IPA symbol ʕ, where Section 1.8 mandates
     ALA-LC romanisation. Names now follow ALA-LC (bāʾ, ʿayn, hāʾ, kāf, sīn)
     and the Arabic name is printed beside each one.
  2. The figure showed shapes in isolation and never showed them inside a word,
     which is where the joining rule actually bites. Part C works two words
     through, one of which breaks the cursive join twice.
  3. Provenance: every glyph is now produced from its Unicode code point by
     arabic_reshaper applying the standard shaping rules, so the figure is
     code-drawn and needs no permission clearance.

Note on kāf. The initial and medial kāf are drawn without the small internal
stroke that the isolated and final forms carry. That is correct Naskh: U+FEDB
and U+FEDC genuinely have that shape, and it is not the Persian keheh, whose
isolated and final forms are the ones that differ from Arabic kāf. The previous
artwork was right on this point.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from figscale import fs, lws, ms, arr
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.font_manager import FontProperties
import arabic_reshaper
from bidi.algorithm import get_display

from arabtext import draw_word

NAVY = "#1F3864"
ORANGE = "#C55A11"
GREY = "#4A5462"
HDR = "#1F3864"
COLHDR = "#DCE6F4"
CELL = "#FFFFFF"
ALT = "#F5F8FD"
EDGE = "#9FB0C6"
NOTE = "#EAF1FA"

ARF = FontProperties(fname="/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf")
ARB = FontProperties(fname="/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf")

TATWEEL = "ـ"


def ar(s):
    return get_display(arabic_reshaper.reshape(s))


# base letter, ALA-LC name, Arabic name
JOINING = [
    ("ب", "bāʾ", "باء"),
    ("ع", "ʿayn", "عين"),
    ("ه", "hāʾ", "هاء"),
    ("ك", "kāf", "كاف"),
    ("س", "sīn", "سين"),
]

NONJOINING = [
    ("ا", "alif", "ألف"),
    ("د", "dāl", "دال"),
    ("ذ", "dhāl", "ذال"),
    ("ر", "rāʾ", "راء"),
    ("ز", "zāy", "زاي"),
    ("و", "wāw", "واو"),
]


def forms(letter):
    """isolated, initial, medial, final, shaped by the standard algorithm."""
    return (ar(letter),
            ar(letter + TATWEEL),
            ar(TATWEEL + letter + TATWEEL),
            ar(TATWEEL + letter))


# ---------------------------------------------------------------- primitives

def band(ax, x, y, w, h, text, fs=13.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=0.10",
                                facecolor=HDR, edgecolor=HDR, lw=lws(0), zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color="white", weight="bold", zorder=3)


def cell(ax, x, y, w, h, fc=CELL, ec=EDGE, lw=lws(0.8)):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, lw=lw,
                           zorder=2))


# ------------------------------------------------------------------- part A

def part_a(ax, x0, y0, w, rowh=0.85):
    cols = [0.30, 0.175, 0.175, 0.175, 0.175]
    heads = ["letter", "isolated", "initial", "medial", "final"]
    xs, acc = [], x0
    for c in cols:
        xs.append(acc)
        acc += c * w
    ws = [c * w for c in cols]

    top = y0
    band(ax, x0, top - 0.9, w, 0.9,
         "PART A   joining letters: four shapes")
    y = top - 0.9 - 0.7
    for k, hd in enumerate(heads):
        cell(ax, xs[k], y, ws[k], 0.7, fc=COLHDR)
        ax.text(xs[k] + ws[k] / 2, y + 0.35, hd, ha="center", va="center",
                fontsize=fs(10.4), color=NAVY, weight="bold", zorder=3)

    for i, (ltr, name, arname) in enumerate(JOINING):
        yy = y - (i + 1) * rowh
        fc = CELL if i % 2 == 0 else ALT
        for k in range(5):
            cell(ax, xs[k], yy, ws[k], rowh, fc=fc)
        ax.text(xs[0] + ws[0] * 0.40, yy + rowh / 2, name, ha="right",
                va="center", fontsize=fs(11.2), color=NAVY, weight="bold", zorder=3)
        ax.text(xs[0] + ws[0] * 0.78, yy + rowh / 2, ar(arname), ha="right",
                va="center", fontsize=fs(13.5), color=GREY,
                fontproperties=ARF, zorder=3)
        for k, g in enumerate(forms(ltr), start=1):
            ax.text(xs[k] + ws[k] / 2, yy + rowh * 0.46, g, ha="center",
                    va="center", fontsize=fs(25), color="#14181E",
                    fontproperties=ARF, zorder=3)
    return y - len(JOINING) * rowh


# ------------------------------------------------------------------- part B

def part_b(ax, x0, y0, w, rowh=0.85):
    cols = [0.34, 0.33, 0.33]
    heads = ["letter", "isolated and initial\n(one shape)",
             "final\n(joins on the right)"]
    xs, acc = [], x0
    for c in cols:
        xs.append(acc)
        acc += c * w
    ws = [c * w for c in cols]

    band(ax, x0, y0 - 0.9, w, 0.9,
         "PART B   non-joining letters: two shapes")
    y = y0 - 0.9 - 0.86
    for k, hd in enumerate(heads):
        cell(ax, xs[k], y, ws[k], 0.86, fc=COLHDR)
        ax.text(xs[k] + ws[k] / 2, y + 0.43, hd, ha="center", va="center",
                fontsize=fs(8.0), color=NAVY, weight="bold", linespacing=1.35,
                zorder=3)

    for i, (ltr, name, arname) in enumerate(NONJOINING):
        yy = y - (i + 1) * rowh
        fc = CELL if i % 2 == 0 else ALT
        for k in range(3):
            cell(ax, xs[k], yy, ws[k], rowh, fc=fc)
        ax.text(xs[0] + ws[0] * 0.44, yy + rowh / 2, name, ha="right",
                va="center", fontsize=fs(11.2), color=NAVY, weight="bold", zorder=3)
        ax.text(xs[0] + ws[0] * 0.82, yy + rowh / 2, ar(arname), ha="right",
                va="center", fontsize=fs(13.5), color=GREY,
                fontproperties=ARF, zorder=3)
        iso, _ini, _med, fin = forms(ltr)
        for k, g in ((1, iso), (2, fin)):
            ax.text(xs[k] + ws[k] / 2, yy + rowh * 0.46, g, ha="center",
                    va="center", fontsize=fs(25), color="#14181E",
                    fontproperties=ARF, zorder=3)
    return y - len(NONJOINING) * rowh


# ------------------------------------------------------------------- part C

# (word, romanisation, gloss, [(shaped form, label, is_break_after)])
EX1 = ("بَعْد", "baʿd", "'after'",
       [("ب" + TATWEEL, "initial"),
        (TATWEEL + "ع" + TATWEEL, "medial"),
        (TATWEEL + "د", "final")])

EX2 = ("بارِد", "bārid", "'cold'",
       [("ب" + TATWEEL, "initial"),
        (TATWEEL + "ا", "final"),
        ("ر", "isolated"),
        ("د", "isolated")])


def example(ax, x0, y0, w, h, ex):
    word, rom, gloss, parts = ex
    cell(ax, x0, y0 - h, w, h, fc=ALT, ec=EDGE, lw=lws(0.8))

    draw_word(ax, x0 + w * 0.20, y0 - h * 0.50, word, ARB, 30, NAVY,
              ha="center", zorder=3)
    ax.text(x0 + w * 0.20, y0 - h * 0.80, f"{rom}   {gloss}", ha="center",
            va="center", fontsize=fs(10.2), color=GREY, zorder=3)

    # the letters, laid out right to left so they match the word above
    n = len(parts)
    zone_x0 = x0 + w * 0.37
    zone_w = w * 0.595
    step = zone_w / n
    ax.annotate("", xy=(zone_x0 + 0.04, y0 - h * 0.15),
                xytext=(zone_x0 + zone_w - 0.04, y0 - h * 0.15),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=lws(1.2),
                                mutation_scale=arr(11)), zorder=4)
    ax.text(zone_x0 + zone_w / 2, y0 - h * 0.13, "read this way",
            ha="center", va="bottom", fontsize=fs(8.2), color=ORANGE,
            weight="bold", zorder=4)

    for i, (raw, label) in enumerate(parts):
        cx = zone_x0 + zone_w - (i + 0.5) * step
        ax.add_patch(FancyBboxPatch((cx - step * 0.40, y0 - h * 0.78),
                                    step * 0.80, h * 0.50,
                                    boxstyle="round,pad=0.02,rounding_size=0.07",
                                    facecolor="white", edgecolor=EDGE, lw=lws(0.8),
                                    zorder=3))
        ax.text(cx, y0 - h * 0.50, ar(raw), ha="center", va="center",
                fontsize=fs(21), color="#14181E", fontproperties=ARF, zorder=4)
        ax.text(cx, y0 - h * 0.88, label, ha="center", va="center",
                fontsize=fs(6.8), color=NAVY, zorder=4)


def part_c(ax, x0, y0, w):
    band(ax, x0, y0 - 0.9, w, 0.9,
         "PART C   the same shapes inside a word")
    y = y0 - 0.9 - 0.18
    h = 2.05
    example(ax, x0, y, w, h, EX1)
    y2 = y - h - 0.22
    example(ax, x0, y2, w, h, EX2)
    return y2 - h


# ---------------------------------------------------------------------- draw

def draw(path):
    W = 14.0
    fig, ax = plt.subplots(figsize=(13.6, 12.4))
    ax.set_xlim(0, W)
    ax.set_ylim(-5.2, 12.85)
    ax.axis("off")
    fig.canvas.draw()

    top = 12.6
    y_a = part_a(ax, 0.0, top, W)

    gap = 0.55
    left_w = W * 0.545
    right_x = left_w + 0.45
    right_w = W - right_x

    y_b = part_b(ax, 0.0, y_a - gap, left_w)
    y_c = part_c(ax, right_x, y_a - gap, right_w)

    note_top = y_c - 0.32
    note_h = 1.95
    ax.add_patch(FancyBboxPatch((right_x, note_top - note_h),
                                right_w, note_h,
                                boxstyle="round,pad=0.05,rounding_size=0.10",
                                facecolor=NOTE, edgecolor="#B9CBE4", lw=lws(0.9),
                                zorder=2))
    ax.text(right_x + right_w / 2, note_top - note_h / 2,
            "A non-joining letter connects only to the\n"
            "letter on its right. It therefore has no\n"
            "medial form, and it breaks the cursive join\n"
            "after itself, as alif and rāʾ do in bārid above.",
            ha="center", va="center", fontsize=fs(8.2), color=NAVY,
            linespacing=1.6, zorder=3)

    ax.set_ylim(min(y_b, note_top - note_h) - 0.25, top + 0.25)
    fig.canvas.draw()
    fig.tight_layout(pad=0.4)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(path.replace(".png", ".pdf"), bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    draw("fig2_5.png")
    print("wrote fig2_5.png/.pdf")
