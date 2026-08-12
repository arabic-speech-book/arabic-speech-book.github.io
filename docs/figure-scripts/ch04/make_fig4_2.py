"""
Figure 4.2: Word Error Rate as a minimum edit distance.

Redrawn twice. First because every row and column label in the original
artwork sat one cell out of place: the numbers in the grid were right and the
marked path was right, but the first row and column of an edit-distance matrix
belong to the empty prefix, and the original gave that row the label of the
first reference word, so a reader would have read the alignment one word out.

Then again, after review, for two things a reader asked for and the figure did
not answer:

  * the example was given only in transliteration, so the Arabic it stands for
    was invisible. Each word now carries its Arabic script, and both sentences
    are glossed underneath.
  * nothing said what the numbers in the cells were. A line under the grid now
    says what a cell holds, what the two ε lines count, and which cell is the
    answer.

The matrix and the backtrace are computed from the two word sequences, so the
numbers, the path, the labels and the alignment strip cannot disagree with one
another.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figscale
from figscale import fs, lws
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch
from matplotlib.font_manager import FontProperties

import arabic_reshaper
from bidi.algorithm import get_display

NAVY = "#1F3864"; ORANGE = "#C55A11"; GREY = "#5A6472"; GREEN = "#1E7B34"
CELL = "#EAF1FA"; ALT = "#FFFFFF"; PATH_FILL = "#FDF2E9"

ARF = FontProperties(
    fname="/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf")
_RESHAPER = arabic_reshaper.ArabicReshaper(
    configuration={"delete_harakat": False})


def ar(s):
    """Arabic laid out for a renderer that does no shaping of its own."""
    return get_display(_RESHAPER.reshape(s))


# (transliteration, Arabic) in the order each sentence is spoken
REF = [("dhahaba", "ذهب"), ("al-awlād", "الأولاد"),
       ("ilā", "إلى"), ("al-madrasa", "المدرسة")]
HYP = [("dhahaba", "ذهب"), ("al-awlād", "الأولاد"),
       ("al-madrasa", "المدرسة"), ("fawran", "فورا")]

# All the Arabic here is undiacritized, as a real reference transcript is, so
# the adverb is written فورا rather than فورًا.
REF_GLOSS = "‘the boys went to the school’"
HYP_GLOSS = "‘the boys the school immediately’"

DASH = "—"


def edit_matrix(ref, hyp):
    n, m = len(ref), len(hyp)
    D = np.zeros((n + 1, m + 1), dtype=int)
    D[:, 0] = np.arange(n + 1); D[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sub = D[i - 1, j - 1] + (0 if ref[i - 1] == hyp[j - 1] else 1)
            D[i, j] = min(sub, D[i - 1, j] + 1, D[i, j - 1] + 1)
    return D


def backtrace(D, ref, hyp):
    i, j = len(ref), len(hyp); path = [(i, j)]; ops = []
    # Two alignments can share the minimum cost. Prefer a genuine match, then a
    # deletion or insertion, and only then a substitution, so the path names
    # what actually happened rather than calling a dropped word a substitution.
    while i > 0 or j > 0:
        if i > 0 and j > 0 and ref[i - 1] == hyp[j - 1] and D[i, j] == D[i - 1, j - 1]:
            ops.append("correct"); i, j = i - 1, j - 1
        elif i > 0 and D[i, j] == D[i - 1, j] + 1:
            ops.append("deletion"); i = i - 1
        elif j > 0 and D[i, j] == D[i, j - 1] + 1:
            ops.append("insertion"); j = j - 1
        else:
            ops.append("substitution"); i, j = i - 1, j - 1
        path.append((i, j))
    return path[::-1], ops[::-1]


def alignment(path, ops, ref, hyp):
    """Read the backtrace back as aligned reference and hypothesis columns."""
    cols = []
    for (a, b), (c, d), op in zip(path[:-1], path[1:], ops):
        r = ref[c - 1] if c > a else None
        h = hyp[d - 1] if d > b else None
        cols.append((r, h, op))
    return cols


def fit(ax, x, y, s, size, max_data_w, **kw):
    """Place text, shrinking it if it would run past its cell.

    The words differ in length by a factor of three ("ilā" against
    "al-madrasa"), so one point size either wastes the short cells or overflows
    the long ones. This measures the drawn text and reduces the size until it
    fits, but never below the 7 pt floor at final print size.
    """
    floor = figscale.MIN_PT / figscale.REPRO
    t = ax.text(x, y, s, fontsize=size, **kw)
    fig = ax.figure
    fig.canvas.draw()
    have = t.get_window_extent(fig.canvas.get_renderer()).width
    want = abs(ax.transData.transform((max_data_w, 0))[0]
               - ax.transData.transform((0, 0))[0])
    if have > want:
        t.set_fontsize(max(floor, size * want / have))
    return t


def draw_matrix(ax, D, path):
    n, m = len(REF), len(HYP)
    on_path = {(i, j) for i, j in path}
    for i in range(n + 1):
        for j in range(m + 1):
            face = PATH_FILL if (i, j) in on_path else (CELL if (i + j) % 2 == 0 else ALT)
            ax.add_patch(Rectangle((j, -i), 1, -1, facecolor=face,
                                   edgecolor="#C9D6E8", lw=lws(0.9)))
            ax.text(j + 0.5, -i - 0.5, str(D[i, j]), ha="center", va="center",
                    fontsize=fs(11.5), color=GREY)
    for i, j in path:
        ax.add_patch(Rectangle((j, -i), 1, -1, facecolor="none",
                               edgecolor=ORANGE, lw=lws(2.0), zorder=4))
    # the answer
    ax.add_patch(Rectangle((m, -n), 1, -1, facecolor="none", edgecolor=ORANGE,
                           lw=lws(3.4), zorder=6))

    for j, l in enumerate(["ε"] + [w for w, _ in HYP]):
        fit(ax, j + 0.5, 0.20, l, fs(10.0), 0.94, ha="center", va="bottom",
            color=NAVY, weight="bold")
    for i, l in enumerate(["ε"] + [w for w, _ in REF]):
        ax.text(-0.16, -i - 0.5, l, ha="right", va="center", fontsize=fs(10.0),
                color=NAVY, weight="bold")
    ax.text((m + 1) / 2, 0.92, "hypothesis (what the recognizer wrote)",
            ha="center", va="bottom", fontsize=fs(10.4), color=NAVY, weight="bold")
    ax.text(-1.85, -(n + 1) / 2, "reference\n(what was said)", ha="center",
            va="center", fontsize=fs(10.4), color=NAVY, weight="bold",
            rotation=90, linespacing=1.4)

    for (a, b), (c, d) in zip(path[:-1], path[1:]):
        ax.add_artist(FancyArrowPatch((b + 0.5, -a - 0.5), (d + 0.5, -c - 0.5),
                      arrowstyle="-|>", mutation_scale=fs(9.0), lw=lws(1.8),
                      color=ORANGE, zorder=5, shrinkA=13, shrinkB=13))

    ax.set_xlim(-2.35, m + 1.05)
    ax.set_ylim(-(n + 1) - 1.55, 1.5)
    ax.axis("off")

    # what the numbers are
    ax.text((m + 1) / 2 - 0.42, -(n + 1) - 0.28,
            "Each cell holds the fewest word changes needed so far.\n"
            "Along the ε row the reference is still empty, so every step right "
            "adds a word;\n"
            "down the ε column the hypothesis is empty, so every step down "
            "drops one.\n"
            "The ringed cell at the end is the total: 2 changes.",
            ha="center", va="top", fontsize=fs(8.8), color=NAVY,
            linespacing=1.6)


def draw_strip(ax, cols):
    """The alignment read off the marked path, with each step named."""
    Y_REF, Y_HYP, Y_OP = 2.62, 1.44, 0.62
    BH = 1.00
    for label, y in (("reference", Y_REF), ("hypothesis", Y_HYP),
                     ("operation", Y_OP)):
        ax.text(-0.16, y, label, ha="right", va="center", fontsize=fs(9.4),
                color=NAVY, weight="bold")

    for k, (r, h, op) in enumerate(cols):
        err = op != "correct"
        edge = ORANGE if err else GREEN
        style = "dashed" if err else "solid"
        fill = PATH_FILL if err else "#FFFFFF"
        for y, word in ((Y_REF, r), (Y_HYP, h)):
            ax.add_patch(FancyBboxPatch((k + 0.06, y - BH / 2), 0.88, BH,
                                        boxstyle="round,pad=0.01,rounding_size=0.06",
                                        facecolor=fill, edgecolor=edge,
                                        lw=lws(1.4), linestyle=style))
            if word is None:
                ax.text(k + 0.5, y, DASH, ha="center", va="center",
                        fontsize=fs(10.0), color=GREY)
            else:
                translit, arabic = word
                ax.text(k + 0.5, y + 0.21, ar(arabic), ha="center", va="center",
                        fontproperties=ARF, fontsize=fs(11.0), color=NAVY)
                fit(ax, k + 0.5, y - 0.24, translit, fs(8.4), 0.80,
                    ha="center", va="center", color=GREY)
        ax.text(k + 0.5, Y_OP, op, ha="center", va="center", fontsize=fs(8.6),
                color=edge, weight="bold")

    ax.text(-0.16, 0.06, "meaning", ha="right", va="center",
            fontsize=fs(9.4), color=NAVY, weight="bold")
    ax.text(0.06, 0.20, "reference:  " + REF_GLOSS + "\n"
            "hypothesis: " + HYP_GLOSS,
            ha="left", va="top", fontsize=fs(9.0), color=GREY,
            linespacing=1.6)

    ax.set_xlim(-2.35, len(HYP) + 1.05)
    ax.set_ylim(-1.15, 3.30)
    ax.axis("off")


def draw(path_out):
    ref = [w for w, _ in REF]
    hyp = [w for w, _ in HYP]
    D = edit_matrix(ref, hyp)
    path, ops = backtrace(D, ref, hyp)
    cols = alignment(path, ops, REF, HYP)

    fig = plt.figure(figsize=(12.4, 11.6))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 0.72], hspace=0.05,
                          left=0.005, right=0.995, top=0.98, bottom=0.02)
    draw_matrix(fig.add_subplot(gs[0]), D, path)
    ax2 = fig.add_subplot(gs[1])
    draw_strip(ax2, cols)

    S = ops.count("substitution"); Dl = ops.count("deletion"); I = ops.count("insertion")
    ax2.text((len(HYP) + 1) / 2 - 0.35, -0.60,
             "WER = (S + D + I) / N = (%d + %d + %d) / %d = %.0f%%"
             % (S, Dl, I, len(REF), 100 * (S + Dl + I) / len(REF)),
             ha="center", va="center", fontsize=fs(11.5), color=NAVY,
             weight="bold")

    fig.savefig(path_out, dpi=300, bbox_inches="tight", pad_inches=0.05,
                facecolor="white")
    fig.savefig(path_out.replace(".png", ".pdf"), bbox_inches="tight",
                pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("ops:", ops, " S=%d D=%d I=%d N=%d WER=%.0f%%"
          % (S, Dl, I, len(REF), 100 * (S + Dl + I) / len(REF)))
    for r, h, op in cols:
        print(f'    {(r or ("—", "—"))[0]:12s} {(h or ("—", "—"))[0]:12s} {op}')


if __name__ == "__main__":
    draw("fig4_2.png")
    print("wrote fig4_2.png/.pdf")
