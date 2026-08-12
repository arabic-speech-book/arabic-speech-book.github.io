"""
Figure 5.1: what the blank symbol is for, and how the collapse works.

Redrawn after review. The first version was a symbol-by-frame grid with two
marked paths. It was correct but it made the reader assemble the argument
themselves. This version follows the far clearer presentation in Jurafsky and
Martin's Figure 15.12 and 15.13: a horizontal ribbon of rows, read from the
bottom up, in which a run of repeated cells visibly merges into one wide cell.
The failure comes first and the fix second, so the blank is motivated rather
than announced.

The example is chosen to make the blank matter. Jurafsky and Martin use
"dinner", where naive collapsing gives "diner". The Arabic counterpart used
here is ممكن (mumkin, 'possible'), whose first two letters are both م: without
a blank between them the two mīms merge and the output is مكن, a different
string. That is exactly the case Section 5.2 describes when it says the blank
"separates a genuine double letter from a token merely held across frames".

Time runs left to right, as it does in every other figure in the book, so the
Arabic letters appear in the order they are spoken rather than in reading
order. Each cell therefore carries its transliteration underneath, and the
assembled word is shown at the end of the output row.

Arabic and Latin are never drawn in one text call: the Arabic face has no
Latin glyphs, so a stray "=" inside an Arabic string prints as a blank box.
"""
from matplotlib.patches import FancyBboxPatch

from bookstyle import (NAVY, ORANGE, GREY, GREEN, BOXFILL, GREENFILL, ARF,
                       canvas, note, save, ar)
from figscale import fs, lws

NF = 10
X0, CW = 2.75, 0.80
H = 0.78
BLANK = "-"

# frame-by-frame labelings: (symbol, transliteration)
MIM, KAF, NUN = ("م", "m"), ("ك", "k"), ("ن", "n")
BLK = (BLANK, "blank")

NAIVE = [MIM, MIM, MIM, MIM, KAF, KAF, NUN, NUN, NUN, NUN]
WITH_BLANK = [MIM, MIM, BLK, MIM, KAF, KAF, BLK, NUN, NUN, BLK]

PINK = "#FDF2E9"


def runs(seq):
    """Adjacent equal cells, as (start, end, symbol) spans."""
    out = []
    for i, s in enumerate(seq):
        if out and out[-1][2] == s:
            out[-1][1] = i
        else:
            out.append([i, i, s])
    return [tuple(r) for r in out]


def cell(ax, c0, c1, sym, y, fill, edge, ls="solid", translit=True):
    x = X0 + c0 * CW
    w = (c1 - c0 + 1) * CW
    ax.add_patch(FancyBboxPatch((x + 0.02, y - H / 2), w - 0.04, H,
                                boxstyle="round,pad=0.005,rounding_size=0.05",
                                facecolor=fill, edgecolor=edge, lw=lws(1.3),
                                linestyle=ls, zorder=3))
    cx = x + w / 2
    glyph, tr = sym
    if glyph == BLANK:
        note(ax, cx, y + 0.11, BLANK, size=11.5, colour=GREY, weight="bold")
    else:
        ax.text(cx, y + 0.13, ar(glyph), ha="center", va="center",
                fontproperties=ARF, fontsize=fs(12.5), color=NAVY, zorder=5)
    if translit:
        note(ax, cx, y - 0.22, tr, size=7.8, colour=GREY)


def row(ax, y, label, spans, fill, edge, ls="solid"):
    note(ax, X0 - 0.22, y, label, size=9.2, ha="right", colour=NAVY,
         weight="bold")
    for c0, c1, sym in spans:
        cell(ax, c0, c1, sym, y, fill, edge, ls)


def frames_row(ax, y):
    note(ax, X0 - 0.22, y, "frames", size=9.2, ha="right", colour=NAVY,
         weight="bold")
    for i in range(NF):
        x = X0 + i * CW
        ax.add_patch(FancyBboxPatch((x + 0.02, y - 0.24), CW - 0.04, 0.48,
                                    boxstyle="round,pad=0.005,rounding_size=0.05",
                                    facecolor="white", edgecolor="#9FB6D4",
                                    lw=lws(1.0), zorder=3))
        note(ax, x + CW / 2, y, f"t{i + 1}", size=8.2, colour=GREY)


def verdict(ax, y, word, mark, colour):
    note(ax, 11.00, y + 0.10, "=", size=10.5, colour=colour, weight="bold")
    ax.text(11.22, y + 0.12, ar(word), ha="left", va="center",
            fontproperties=ARF, fontsize=fs(12.5), color=colour, zorder=5)
    note(ax, 12.30, y + 0.06, mark, size=12.0, ha="right", colour=colour,
         weight="bold")


def draw(path_out):
    fig, ax = canvas(12.6, 9.6, (0.20, 12.45), (0.55, 10.05))

    # ---- Part A: no blank, and the two mīms merge
    note(ax, 0.30, 9.62, "A.  Without a blank the two mīms run together",
         size=10.4, ha="left", colour=ORANGE, weight="bold")
    row(ax, 8.92, "output", runs(NAIVE), PINK, ORANGE)
    verdict(ax, 8.92, "مكن", "✗", ORANGE)
    row(ax, 8.04, "alignment", [(i, i, s) for i, s in enumerate(NAIVE)],
        BOXFILL, NAVY)
    frames_row(ax, 7.24)
    note(ax, 0.30, 6.66,
         "Merging the repeats leaves a single mīm, so the output is a "
         "different word.",
         size=9.2, ha="left", colour=ORANGE, style="italic")

    # ---- Part B: a blank keeps them apart
    note(ax, 0.30, 5.92, "B.  A blank between them keeps them apart",
         size=10.4, ha="left", colour=GREEN, weight="bold")
    spans_merge = runs(WITH_BLANK)
    spans_noblank = [s for s in spans_merge if s[2] != BLK]

    packed = [(i, i, s) for i, (_, _, s) in enumerate(spans_noblank)]
    row(ax, 5.24, "output", packed, GREENFILL, GREEN)
    verdict(ax, 5.24, "ممكن", "✓", GREEN)
    row(ax, 4.36, "remove blanks", spans_noblank, BOXFILL, NAVY)
    row(ax, 3.48, "merge repeats", spans_merge, BOXFILL, NAVY)
    row(ax, 2.60, "alignment", [(i, i, s) for i, s in enumerate(WITH_BLANK)],
        BOXFILL, NAVY)
    frames_row(ax, 1.80)

    note(ax, 0.30, 1.10,
         "Read each part from the bottom up: the network labels every frame, "
         "then repeats are merged and blanks removed.\n"
         "A dash is the blank, meaning ‘emit nothing here’. Time runs left to "
         "right, so the letters stand in the order they\n"
         "are spoken, not in Arabic reading order; each cell carries its "
         "transliteration and the word is assembled at the end.",
         size=9.0, ha="left", va="top", colour=NAVY, linespacing=1.7)

    save(fig, path_out)


if __name__ == "__main__":
    draw("fig5_1.png")
    print("naive collapse   :", " ".join(s[0] for _, _, s in runs(NAIVE)))
    print("with blank, merge:", " ".join(s[0] for _, _, s in runs(WITH_BLANK)))
    print("after removing blanks:",
          " ".join(s[0] for _, _, s in runs(WITH_BLANK) if s != BLK))
