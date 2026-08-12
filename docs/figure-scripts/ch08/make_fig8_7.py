"""
Figure 8.7: spoken document retrieval, indexing once and querying many times.

Two rows, as the illustrator specification asked, with one change. The
specification drew a single arrow from the index down to the search step, which
loses the point of the figure: indexing is done once and offline, querying
happens every time and must be fast. The two rows are therefore labelled with
what distinguishes them, "once, offline" and "per query", as two-word labels
rather than sentences, and the index sits between them because both rows touch
it.

No sentences inside the artwork.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

BW, BH, PAD = 2.55, 1.10, 0.16


def draw(path_out):
    w, h = 12.6, 5.0
    fig, ax = canvas(w, h, (0, w), (0, h))

    ytop, ybot = h - 1.05, 1.05
    ymid = (ytop + ybot) / 2

    top = [("Arabic audio\narchive", BOXFILL, NAVY),
           ("recognizer or\nphonetic indexer", WHITE, NAVY)]
    bot = [("spoken or\ntext query", BOXFILL, NAVY),
           ("search\nthe index", WHITE, NAVY),
           ("ranked\nresults", GREENFILL, GREEN)]

    xs_top = [2.20, 5.15]
    for x, (label, fill, edge) in zip(xs_top, top):
        box(ax, x, ytop, BW, BH, fill=fill, edge=edge, lw=1.5, r=0.12)
        t = note(ax, x, ytop, label, size=9.8, colour=edge, weight="bold",
                 linespacing=1.5)
        must_fit(fig, t, BW - PAD, max(label.split("\n"), key=len))
    arrow(ax, (xs_top[0] + BW / 2 + 0.03, ytop),
          (xs_top[1] - BW / 2 - 0.03, ytop))

    xidx = 8.55
    box(ax, xidx, ymid, BW + 0.30, BH + 0.10, fill=WHITE, edge=ORANGE, lw=1.8,
        r=0.12)
    t = note(ax, xidx, ymid, "searchable\nindex", size=10.2, colour=ORANGE,
             weight="bold", linespacing=1.5)
    must_fit(fig, t, BW + 0.30 - PAD, "searchable")

    arrow(ax, (xs_top[1] + BW / 2 + 0.03, ytop),
          (xidx - BW / 2 - 0.18, ymid + 0.30))

    xs_bot = [2.20, 5.15]
    for x, (label, fill, edge) in zip(xs_bot, bot[:2]):
        box(ax, x, ybot, BW, BH, fill=fill, edge=edge, lw=1.5, r=0.12)
        t = note(ax, x, ybot, label, size=9.8, colour=edge, weight="bold",
                 linespacing=1.5)
        must_fit(fig, t, BW - PAD, max(label.split("\n"), key=len))
    arrow(ax, (xs_bot[0] + BW / 2 + 0.03, ybot),
          (xs_bot[1] - BW / 2 - 0.03, ybot))
    arrow(ax, (xidx - BW / 2 - 0.18, ymid - 0.30),
          (xs_bot[1] + BW / 2 + 0.03, ybot))

    xres = 11.30
    box(ax, xres, ybot, BW - 0.35, BH, fill=GREENFILL, edge=GREEN, lw=1.5,
        r=0.12)
    t = note(ax, xres, ybot, bot[2][0], size=9.8, colour=GREEN, weight="bold",
             linespacing=1.5)
    must_fit(fig, t, BW - 0.35 - PAD, "ranked")
    arrow(ax, (xidx + BW / 2 + 0.18, ymid - 0.20),
          (xres - BW / 2 + 0.32, ybot + BH / 2 + 0.02), colour=GREEN)

    note(ax, 0.22, ytop, "once,\noffline", size=9.4, colour=GREY, ha="left",
         linespacing=1.5)
    note(ax, 0.22, ybot, "per\nquery", size=9.4, colour=GREY, ha="left",
         linespacing=1.5)

    report()
    save(fig, path_out)
    print("wrote", path_out)


if __name__ == "__main__":
    draw("fig8_7.png")
