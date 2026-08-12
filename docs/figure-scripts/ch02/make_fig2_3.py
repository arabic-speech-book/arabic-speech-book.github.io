"""
Figure 2.3: the Arabic vowels in F1-F2 space.

Fixes four faults in the previous artwork:
  1. The vertical axis read "F1 (vowel height): low at bottom, high at top,
     inverted", which cannot all be true at once. Both axes are now labelled
     unambiguously: the quantity, its direction, and the articulatory meaning.
  2. The chart was mirrored relative to the IPA convention (front on the right).
     It now follows the standard orientation, front on the left, so it matches
     every other vowel chart a reader will have seen.
  3. The corners paired short IPA symbols with long transliterations
     (/u/ ū, /i/ ī, /a/ ā). Length now agrees in both notations, and the short
     vowels are plotted as well, so the length contrast is visible.
  4. The bayt/bēt callout pointed at /a/. It now points at /eː/, which is what
     it is about.

Marker shape distinguishes Modern Standard from dialectal vowels, so the figure
survives grayscale printing.

Formant values are representative adult-male values used to place the symbols;
they are illustrative, not measurements from a specific corpus.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from figscale import fs, lws, ms, arr
from matplotlib.patches import FancyBboxPatch
from matplotlib.font_manager import FontProperties
import arabic_reshaper
from bidi.algorithm import get_display

NAVY = "#1F3864"
ORANGE = "#C55A11"
GREY = "#5A6472"
AR = FontProperties(fname="/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf")

# (IPA, transliteration, F1, F2, class)   class: "long" | "short" | "dialect"
VOWELS = [
    ("iː", "ī", 300, 2200, "long"),
    ("uː", "ū", 320,  900, "long"),
    ("aː", "ā", 700, 1400, "long"),
    ("i",  "i", 380, 1900, "short"),
    ("u",  "u", 400, 1050, "short"),
    ("a",  "a", 650, 1500, "short"),
    ("eː", "ē", 450, 1900, "dialect"),
    ("oː", "ō", 470, 1000, "dialect"),
]

STYLE = {
    "long":    dict(marker="o", s=ms(95), facecolor=NAVY,  edgecolor=NAVY,
                    label="Modern Standard, long"),
    "short":   dict(marker="o", s=ms(60), facecolor="white", edgecolor=NAVY,
                    label="Modern Standard, short"),
    "dialect": dict(marker="s", s=ms(90), facecolor=ORANGE, edgecolor=ORANGE,
                    label="added in many dialects"),
}

OFFSET = {"iː": (56, -20), "uː": (-56, -22), "aː": (58, -18),
          "i": (52, -16), "u": (-50, -16), "a": (54, -16),
          "eː": (58, 2), "oː": (58, 2)}


def ar(t):
    return get_display(arabic_reshaper.reshape(t))


def draw(path):
    fig, ax = plt.subplots(figsize=(12.6, 8.6))

    quad = [("iː"), ("uː"), ("aː")]
    pts = {v[0]: (v[3], v[2]) for v in VOWELS}
    tri = [pts["iː"], pts["uː"], pts["aː"], pts["iː"]]
    ax.plot([p[0] for p in tri], [p[1] for p in tri], color="#9FB0C6",
            lw=lws(1.4), ls=(0, (5, 4)), zorder=1)

    seen = set()
    for ipa, tr, f1, f2, cls in VOWELS:
        st = dict(STYLE[cls])
        lab = st.pop("label")
        ax.scatter([f2], [f1], linewidths=lws(1.8), zorder=3,
                   label=lab if lab not in seen else None, **st)
        seen.add(lab)
        dx, dy = OFFSET[ipa]
        ax.annotate(f"/{ipa}/  {tr}", xy=(f2, f1), xytext=(dx, dy),
                    textcoords="offset points", ha="center", va="center",
                    fontsize=fs(12.4), color=ORANGE if cls == "dialect" else NAVY,
                    weight="bold" if cls != "short" else "normal", zorder=4)

    # emphasis lowers F2: with F2 decreasing rightward, that is a move right
    ax.annotate("", xy=(1150, 288), xytext=(2180, 288),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=lws(2.4),
                                mutation_scale=arr(17)), zorder=5)
    ax.text(1665, 278, "emphasis lowers F2: the vowel is pulled back and sounds darker",
            ha="center", va="bottom", fontsize=fs(10.4), color=ORANGE,
            weight="bold", zorder=5)

    # callout anchored to /eː/, which is what it is about
    ax.annotate(
        f"{ar('بَيت')}  bayt  'house'  (Modern Standard)\n"
        f"{ar('بَيت')}  bēt   'house'  (many Levantine varieties)",
        xy=(1900, 462), xytext=(1215, 612), fontsize=fs(8.6), color=NAVY,
        ha="center", va="center", linespacing=1.6, zorder=6,
        fontproperties=None,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FDF2E9",
                  edgecolor=ORANGE, lw=lws(1.3)),
        arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=lws(1.3),
                        mutation_scale=arr(12), connectionstyle="arc3,rad=-0.2"))

    ax.set_xlim(2450, 700)      # F2 decreases to the right: IPA orientation
    ax.set_ylim(830, 245)       # F1 increases downward
    ax.set_xlabel("F2 (Hz), decreasing to the right", fontsize=fs(11), color=NAVY)
    ax.set_ylabel("F1 (Hz), increasing downward", fontsize=fs(11), color=NAVY,
                  labelpad=34)
    ax.tick_params(labelsize=9.4)

    for x, t, ha in ((0.0, "front", "left"), (1.0, "back", "right")):
        ax.text(x, 1.035, t, transform=ax.transAxes, ha=ha, va="bottom",
                fontsize=fs(11), color=GREY, weight="bold")
    for y, t, va in ((1.0, "close (high)", "top"), (0.0, "open (low)", "bottom")):
        ax.text(-0.058, y, t, transform=ax.transAxes, ha="center", va=va,
                fontsize=fs(10.4), color=GREY, weight="bold", rotation=90)

    leg = ax.legend(loc="lower left", fontsize=fs(9.4), frameon=True,
                    borderpad=0.7, labelspacing=0.8, handletextpad=1.0)
    leg.get_frame().set_edgecolor("#C8CFD9")

    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(True, color="#EDF1F7", lw=lws(0.8))
    ax.set_axisbelow(True)

    fig.tight_layout(pad=0.6)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(path.replace(".png", ".pdf"), bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    draw("fig2_3.png")
    print("wrote fig2_3.png/.pdf")
