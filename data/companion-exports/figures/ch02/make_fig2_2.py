"""
Figure 2.2 for Chapter 2 of *Introduction to Arabic Speech Technologies*:
the Arabic consonant inventory by place and manner.

Redrawn to fix four faults in the previous artwork:
  1. The emphasis mark U+02E4 rendered as a superscript two, so every emphatic
     read as /t2/, /d2/, /s2/, /ð2/. A font carrying the glyph is selected
     explicitly and the result is checked.
  2. /x/ and /ɣ/ were filed under "uvular", contradicting Section 2.3 and
     Table 2.1, which both leave the velar-versus-uvular question open. They
     now straddle the two columns and the legend records the dispute.
  3. The three highlighted groups were distinguished by colour alone. Each now
     has its own line style as well, so the chart survives grayscale printing.
  4. /dʒ/ sat in the "plosive" row. Affricates now have their own row.

Transliterations follow ALA-LC per Section 1.8: ʾ for hamza, ʿ for ʿayn.
Drawn deterministically from the table below; no image model is involved.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import figscale
from figscale import fs, lws, ms, arr

# Nine place-of-articulation columns in a 6.5 in text block cannot carry 7 pt
# type. This table drops to the 6 pt floor that Springer allows for figures.
figscale.configure(scale=1.35, min_pt=6.0)
from matplotlib.patches import FancyBboxPatch
from matplotlib.font_manager import FontProperties, findfont

NAVY = "#1F3864"
HEAD = "#1F3864"
ROW_A = "#EAF1F8"
ROW_B = "#FFFFFF"
GREY = "#5A6472"

EMPH = "#7030A0"
PHAR = "#1E7B34"
UVUL = "#C55A11"

# A font that actually carries U+02E4 and the Arabic block.
IPA_FONT = FontProperties(family="DejaVu Sans")
AR_FONT = FontProperties(fname="/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf")

PLACES = ["bilabial", "labio-\ndental", "dental /\nalveolar", "post-\nalveolar",
          "palatal", "velar", "uvular", "pharyn-\ngeal", "glottal"]
MANNERS = ["plosive", "affricate", "fricative", "nasal", "trill", "approximant"]

# (manner, place, [(ipa, arabic, translit, group)])
# group: None | "emph" | "phar" | "uvul"
CELLS = {
    ("plosive", "bilabial"):        [("b", "ب", "b", None)],
    ("plosive", "dental /\nalveolar"): [("t", "ت", "t", None), ("d", "د", "d", None),
                                        ("tˤ", "ط", "ṭ", "emph"), ("dˤ", "ض", "ḍ", "emph")],
    ("plosive", "velar"):           [("k", "ك", "k", None)],
    ("plosive", "uvular"):          [("q", "ق", "q", "uvul")],
    ("plosive", "glottal"):         [("ʔ", "ء", "ʾ", None)],
    ("affricate", "post-\nalveolar"): [("dʒ", "ج", "j", None)],
    ("fricative", "labio-\ndental"): [("f", "ف", "f", None)],
    ("fricative", "dental /\nalveolar"): [("θ", "ث", "th", None), ("ð", "ذ", "dh", None),
                                          ("s", "س", "s", None), ("z", "ز", "z", None),
                                          ("sˤ", "ص", "ṣ", "emph"), ("ðˤ", "ظ", "ẓ", "emph")],
    ("fricative", "post-\nalveolar"): [("ʃ", "ش", "sh", None)],
    ("fricative", "pharyn-\ngeal"):    [("ħ", "ح", "ḥ", "phar"), ("ʕ", "ع", "ʿ", "phar")],
    ("fricative", "glottal"):       [("h", "ه", "h", None)],
    ("nasal", "bilabial"):          [("m", "م", "m", None)],
    ("nasal", "dental /\nalveolar"): [("n", "ن", "n", None)],
    ("trill", "dental /\nalveolar"): [("r", "ر", "r", None)],
    ("approximant", "dental /\nalveolar"): [("l", "ل", "l", None)],
    ("approximant", "palatal"):     [("j", "ي", "y", None)],
    ("approximant", "bilabial"):    [("w", "و", "w", None)],
}

# /x/ and /ɣ/ straddle velar and uvular: Section 2.3 leaves the question open.
STRADDLE = [("x", "خ", "kh", "uvul"), ("ɣ", "غ", "gh", "uvul")]

GROUP_STYLE = {
    "emph": (EMPH, "solid",  "emphatic (solid outline)"),
    "phar": (PHAR, "dashed", "pharyngeal (dashed outline)"),
    "uvul": (UVUL, "dotted", "uvular (dotted outline)"),
}


def draw(path):
    ncol, nrow = len(PLACES), len(MANNERS)
    colw, rowh = 1.0, 1.0
    labw = 1.55
    heights = {"plosive": 2.35, "affricate": 0.95, "fricative": 3.05,
               "nasal": 0.8, "trill": 0.8, "approximant": 0.8}
    total_h = sum(heights.values())

    fig, ax = plt.subplots(figsize=(13.2, 8.4))

    # column headers
    ax.add_patch(FancyBboxPatch((0, total_h), labw + ncol * colw, 0.72,
                                boxstyle="square,pad=0", facecolor=HEAD,
                                edgecolor="none", zorder=1))
    for j, p in enumerate(PLACES):
        ax.text(labw + j * colw + colw / 2, total_h + 0.36, p, ha="center", va="center",
                fontsize=fs(9.6), color="white", weight="bold", linespacing=1.25, zorder=2)

    y = total_h
    row_y = {}
    for i, m in enumerate(MANNERS):
        h = heights[m]
        y -= h
        row_y[m] = (y, h)
        ax.add_patch(FancyBboxPatch((0, y), labw + ncol * colw, h,
                                    boxstyle="square,pad=0",
                                    facecolor=ROW_A if i % 2 == 0 else ROW_B,
                                    edgecolor="#C9D6E8", lw=lws(0.8), zorder=0))
        ax.text(labw / 2, y + h / 2, m, ha="center", va="center",
                fontsize=fs(9.6), color=NAVY, weight="bold", zorder=2)

    # vertical rules
    for j in range(ncol + 1):
        ax.plot([labw + j * colw] * 2, [0, total_h], color="#C9D6E8", lw=lws(0.8), zorder=1)

    def cell_entries(entries, cx, cy, ch):
        n = len(entries)
        step = min(0.72, (ch - 0.18) / max(n, 1))
        top = cy + ch / 2 + (n - 1) * step / 2
        for k, (ipa, arab, tr, grp) in enumerate(entries):
            yy = top - k * step
            if grp:
                colour, ls, _ = GROUP_STYLE[grp]
                ax.add_patch(FancyBboxPatch((cx - 0.42, yy - step * 0.39), 0.84, step * 0.78,
                                            boxstyle="round,pad=0.02,rounding_size=0.07",
                                            facecolor="none", edgecolor=colour,
                                            lw=lws(1.6), linestyle=ls, zorder=3))
            ax.text(cx - 0.30, yy, f"/{ipa}/", ha="center", va="center",
                    fontsize=fs(10.4), color="#111111", fontproperties=IPA_FONT, zorder=4)
            ax.text(cx + 0.05, yy, arab, ha="center", va="center",
                    fontsize=fs(13), fontproperties=AR_FONT, color="#111111", zorder=4)
            ax.text(cx + 0.33, yy, tr, ha="center", va="center",
                    fontsize=fs(9.6), color=GREY, style="italic", zorder=4)

    for (m, p), entries in CELLS.items():
        j = PLACES.index(p)
        cy, ch = row_y[m]
        cell_entries(entries, labw + j * colw + colw / 2, cy, ch)

    # the straddling pair
    jv, ju = PLACES.index("velar"), PLACES.index("uvular")
    cy, ch = row_y["fricative"]
    cx = labw + (jv + ju + 1) / 2 * colw
    ax.add_patch(FancyBboxPatch((labw + jv * colw + 0.10, cy + 0.10),
                                2 * colw - 0.20, ch - 0.20,
                                boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor="#FDF2E9", edgecolor=UVUL, lw=lws(1.6),
                                linestyle="dotted", zorder=2))
    ax.text(cx, cy + ch - 0.48, "velar or uvular:\ndisputed (Sect. 2.3)",
            ha="center", va="center", fontsize=fs(7.8), color=UVUL,
            style="italic", linespacing=1.4, zorder=4)
    cell_entries(STRADDLE, cx, cy - 0.44, ch - 0.55)

    # empty-cell dashes
    for m in MANNERS:
        for p in PLACES:
            if (m, p) in CELLS:
                continue
            if m == "fricative" and p in ("velar", "uvular"):
                continue
            j = PLACES.index(p)
            cy, ch = row_y[m]
            ax.text(labw + j * colw + colw / 2, cy + ch / 2, "–",
                    ha="center", va="center", fontsize=fs(10), color="#B8C2CF", zorder=2)

    # legend: colour AND line style
    for k, key in enumerate(["emph", "phar", "uvul"]):
        colour, ls, label = GROUP_STYLE[key]
        x0 = 2.4 + k * 3.4
        ax.add_patch(FancyBboxPatch((x0, -0.95), 0.7, 0.34,
                                    boxstyle="round,pad=0.02,rounding_size=0.06",
                                    facecolor="none", edgecolor=colour, lw=lws(1.8),
                                    linestyle=ls, clip_on=False, zorder=3))
        ax.text(x0 + 0.9, -0.78, label, ha="left", va="center",
                fontsize=fs(9.6), color=colour, clip_on=False)

    ax.set_xlim(-0.1, labw + ncol * colw + 0.1)
    ax.set_ylim(-1.25, total_h + 0.9)
    ax.axis("off")
    fig.tight_layout(pad=0.3)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(path.replace(".png", ".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    draw("fig2_2.png")
    print("wrote fig2_2.png/.pdf; IPA font resolved to", findfont(IPA_FONT))
