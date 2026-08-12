"""
Figure 7.3: the data pipeline from recruitment to licensed release.

Redrawn at the book's type scale. The author's artwork passed the type floor
but carried two problems the redraw fixes.

* "QC + agreement" used an abbreviation the artwork never expanded. Every stage
  is now named in full, as the first use of a term inside a figure must be.
* The nine stages ran left to right and then right to left, so the reader met
  "license and release" at the far left of the second row, against the reading
  direction. The stages now run left to right on both rows, with a return path
  beneath the first row, so the eye always travels the same way.

Every label is measured against its box with figfit rather than estimated.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL,
                       canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

ROW1 = ["recruit speakers,\nobtain consent",
        "record or\nharvest audio",
        "segment into\nutterances",
        "transcribe under\nthe convention\nsheet",
        "quality control\nand annotator\nagreement"]
ROW2 = ["align transcript\nto audio",
        "define leak-free\nsplits",
        "write the\ndata card",
        "license and\nrelease"]

BW, BH, PAD = 2.32, 1.24, 0.14


def draw(path_out):
    w, h = 12.6, 5.5
    fig, ax = canvas(w, h, (0, w), (0, h))

    gap = (w - 0.4 - 5 * BW) / 4
    xs1 = [0.20 + BW / 2 + i * (BW + gap) for i in range(5)]
    y1 = h - 1.28

    for x, label in zip(xs1, ROW1):
        box(ax, x, y1, BW, BH, fill=BOXFILL, edge=NAVY, lw=1.5, r=0.12)
        t = note(ax, x, y1, label, size=9.4, colour=NAVY, weight="bold",
                 linespacing=1.5)
        must_fit(fig, t, BW - PAD, label.split("\n")[0])
    for a, b in zip(xs1, xs1[1:]):
        arrow(ax, (a + BW / 2 + 0.02, y1), (b - BW / 2 - 0.02, y1))

    gap2 = 0.62
    span = 4 * BW + 3 * gap2
    xs2 = [(w - span) / 2 + BW / 2 + i * (BW + gap2) for i in range(4)]
    y2 = 1.05

    for i, (x, label) in enumerate(zip(xs2, ROW2)):
        last = i == len(ROW2) - 1
        box(ax, x, y2, BW, BH,
            fill=GREENFILL if last else WHITE,
            edge=GREEN if last else NAVY, lw=1.5, r=0.12)
        t = note(ax, x, y2, label, size=9.4,
                 colour=GREEN if last else NAVY, weight="bold",
                 linespacing=1.5)
        must_fit(fig, t, BW - PAD, label.split("\n")[0])
    for a, b in zip(xs2, xs2[1:]):
        arrow(ax, (a + BW / 2 + 0.02, y2), (b - BW / 2 - 0.02, y2))

    mid = (y1 - BH / 2 + y2 + BH / 2) / 2
    ax.plot([xs1[-1], xs1[-1]], [y1 - BH / 2 - 0.02, mid], color=ORANGE,
            lw=lws(1.9), zorder=4, solid_capstyle="butt")
    ax.plot([xs1[-1], xs2[0]], [mid, mid], color=ORANGE, lw=lws(1.9),
            zorder=4, solid_capstyle="butt")
    arrow(ax, (xs2[0], mid), (xs2[0], y2 + BH / 2 + 0.02))

    save(fig, path_out)
    report()


if __name__ == "__main__":
    draw("fig7_3.png")
