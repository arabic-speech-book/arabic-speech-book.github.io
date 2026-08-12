"""
Figure 2.6: the root-and-pattern system, illustrated with k-t-b.

Redrawn to fix three faults in the previous artwork:

  1. The three root circles ran ك ت ب from left to right. Arabic reads right to
     left, so an Arabic-reading reader took that sequence as b-t-k, while the
     Latin gloss printed under it said k-t-b. The circles now run ب ت ك from
     left to right, which reads k-t-b in Arabic, and each circle carries its
     own Latin letter, so the two notations cannot contradict each other.
  2. Root-consonant highlighting was inconsistent between the five derived
     words: some had all three consonants marked, others only two.
     Highlighting is now derived from the text itself: every letter is checked
     against the root, so no word can be marked differently from another.
  3. The root was distinguished by colour alone. Each root consonant now also
     carries an underline, so the figure survives grayscale printing.

The pattern (wazn) of each derived word is also named, which is what actually
carries the meaning difference, and the figure now says so.

Arabic is drawn letter by letter from the Unicode text through the standard
shaping rules (see arabtext.py), not assembled by hand.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from figscale import fs, lws, ms, arr
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.font_manager import FontProperties

from arabtext import draw_word

NAVY = "#1F3864"
ORANGE = "#C55A11"
GREY = "#5A6472"
BOXFILL = "#FFFFFF"
CIRCLE = "#EAF1FA"
NOTE = "#FDF2E9"

ARF = FontProperties(
    fname="/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf")

ROOT = "كتب"                     # the three root consonants
ROOT_LATIN = {"ك": "k", "ت": "t", "ب": "b"}

# Drawn left to right, so that reading right to left gives k, t, b.
CIRCLE_ORDER = ["ب", "ت", "ك"]

# (Arabic, romanisation, gloss, pattern Arabic, pattern romanisation,
#  box centre x, box centre y, arrow anchor on the root cluster)
WORDS = [
    ("كَتَبَ",   "kataba",  "he wrote",  "فَعَلَ",   "faʿala",  7.00, 9.40),
    ("كِتاب",   "kitāb",   "book",      "فِعال",   "fiʿāl",   2.20, 6.00),
    ("كاتِب",   "kātib",   "writer",    "فاعِل",   "fāʿil",  11.80, 6.00),
    ("مَكتَب",   "maktab",  "office",    "مَفعَل",   "mafʿal",  2.20, 2.20),
    ("مَكتَبة",  "maktaba", "library",   "مَفعَلة",  "mafʿala", 11.80, 2.20),
]

BOX_W, BOX_H = 4.00, 3.00
CX, CY = 7.00, 6.00
R = 0.62
GAP = 1.42


def root_colour(base):
    return ORANGE if base in ROOT else NAVY


def word_box(ax, cx, cy, arabic, rom, gloss, pat_ar, pat_rom):
    ax.add_patch(FancyBboxPatch((cx - BOX_W / 2, cy - BOX_H / 2), BOX_W, BOX_H,
                                boxstyle="round,pad=0.06,rounding_size=0.20",
                                facecolor=BOXFILL, edgecolor=NAVY, lw=lws(1.5),
                                zorder=3))

    y_ar = cy + 0.50
    spans = draw_word(ax, cx, y_ar, arabic, ARF, 30, root_colour,
                      ha="center", zorder=5)
    for base, xl, xr in spans:
        if base in ROOT:
            ax.plot([xl + 0.02, xr - 0.02], [cy + 0.06, cy + 0.06],
                    color=ORANGE, lw=lws(2.4), solid_capstyle="butt", zorder=5)

    ax.text(cx, cy - 0.30, rom, ha="center", va="center",
            fontsize=fs(13.0), color=NAVY, weight="bold", zorder=5)
    ax.text(cx, cy - 0.62, gloss, ha="center", va="center",
            fontsize=fs(11.0), color=GREY, zorder=5)

    # the pattern, which is what carries the meaning difference
    y_pat = cy - 0.96
    ax.text(cx - 0.62, y_pat, "pattern", ha="right", va="center",
            fontsize=fs(9.0), color=GREY, style="italic", zorder=5)
    draw_word(ax, cx - 0.50, y_pat - 0.055, pat_ar, ARF, 15,
              GREY, ha="left", zorder=5)
    ax.text(cx + 1.05, y_pat, pat_rom, ha="left", va="center",
            fontsize=fs(9.6), color=GREY, zorder=5)


def draw(path):
    fig, ax = plt.subplots(figsize=(13.6, 10.9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11.2)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.canvas.draw()

    # ---- the root, laid out so that reading right to left gives k-t-b
    xs = [CX + (i - 1) * GAP for i in range(3)]
    ax.plot([xs[0], xs[2]], [CY, CY], color=NAVY, lw=lws(1.6), zorder=2)
    for x, letter in zip(xs, CIRCLE_ORDER):
        ax.add_patch(Circle((x, CY), R, facecolor=CIRCLE, edgecolor=NAVY,
                            lw=lws(1.6), zorder=3))
        draw_word(ax, x, CY - 0.16, letter, ARF, 27, ORANGE, ha="center",
                  zorder=5)
        ax.text(x, CY - R - 0.30, ROOT_LATIN[letter], ha="center", va="top",
                fontsize=fs(12.0), color=ORANGE, weight="bold", zorder=5)

    ax.annotate("", xy=(xs[0] - 0.72, CY + R + 0.46),
                xytext=(xs[2] + 0.72, CY + R + 0.46),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=lws(1.3),
                                mutation_scale=arr(13)), zorder=4)
    ax.text(CX, CY + R + 0.58, "Arabic reads this way", ha="center",
            va="bottom", fontsize=fs(9.6), color=GREY, weight="bold", zorder=4)

    ax.text(CX, CY - R - 1.02, "root k-t-b:\nthe idea of writing",
            ha="center", va="top", fontsize=fs(11.4), color=NAVY, weight="bold",
            linespacing=1.45, zorder=4)

    # ---- the derived words
    for arabic, rom, gloss, pat_ar, pat_rom, bx, by in WORDS:
        word_box(ax, bx, by, arabic, rom, gloss, pat_ar, pat_rom)
        # arrow from the edge of the root cluster towards the box
        if by > CY and abs(bx - CX) < 0.5:          # straight up
            ax.annotate("", xy=(CX, by - BOX_H / 2 - 0.10),
                        xytext=(CX, CY + R + 1.05),
                        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=lws(1.8),
                                        mutation_scale=arr(15)), zorder=2)
        elif abs(by - CY) < 0.5:                    # straight out to the side
            sx = xs[0] - R - 0.06 if bx < CX else xs[2] + R + 0.06
            tx = bx + (BOX_W / 2 + 0.12) * (1 if bx < CX else -1)
            ax.annotate("", xy=(tx, CY), xytext=(sx, CY),
                        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=lws(1.8),
                                        mutation_scale=arr(15)), zorder=2)
        else:                                        # down and out
            sx = xs[0] - R * 0.7 if bx < CX else xs[2] + R * 0.7
            sy = CY - R * 0.7
            tx = bx + (BOX_W / 2 + 0.12) * (1 if bx < CX else -1)
            ty = by + BOX_H / 2 + 0.05
            ax.annotate("", xy=(tx, ty), xytext=(sx, sy),
                        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=lws(1.8),
                                        mutation_scale=arr(15)), zorder=2)

    # ---- key
    ax.add_patch(FancyBboxPatch((4.72, 0.28), 4.56, 1.82,
                                boxstyle="round,pad=0.06,rounding_size=0.14",
                                facecolor=NOTE, edgecolor=ORANGE, lw=lws(1.1),
                                zorder=3))
    ax.text(7.00, 1.19,
            "Underlined and coloured:\n"
            "the three root consonants.\n"
            "Everything else is the pattern,\n"
            "which carries the meaning.",
            ha="center", va="center", fontsize=fs(8.4), color=NAVY,
            linespacing=1.55, zorder=4)

    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(path.replace(".png", ".pdf"), bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    draw("fig2_6.png")
    print("wrote fig2_6.png/.pdf")
