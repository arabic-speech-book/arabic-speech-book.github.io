"""
A clustering-based diarization pipeline.

Redrawn at the book's type scale, with the four stages the chapter names and
nothing else. No sentences inside the artwork. The stage that the chapter says
is the weak point, clustering, is drawn in the accent colour so a reader can
find it again when Section 8.6 explains why overlap breaks it.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

CARDS = [("audio", BOXFILL, NAVY),
         ("voice activity\ndetection", WHITE, NAVY),
         ("segment into\nshort\nwindows", WHITE, NAVY),
         ("one speaker\nembedding\nper segment", WHITE, NAVY),
         ("cluster the\nembeddings", WHITE, ORANGE),
         ("who spoke\nwhen", GREENFILL, GREEN)]

BW, BH, PAD = 1.86, 1.30, 0.14


def draw(path_out):
    w, h = 12.6, 2.6
    fig, ax = canvas(w, h, (0, w), (0, h))
    y = h / 2
    gap = (w - 0.6 - len(CARDS) * BW) / (len(CARDS) - 1)
    xs = [0.30 + BW / 2 + i * (BW + gap) for i in range(len(CARDS))]

    for x, (title, fill, edge) in zip(xs, CARDS):
        box(ax, x, y, BW, BH, fill=fill, edge=edge, lw=1.5, r=0.12)
        t = note(ax, x, y, title, size=9.4, colour=edge, weight="bold",
                 linespacing=1.5)
        must_fit(fig, t, BW - PAD, max(title.split("\n"), key=len))
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + BW / 2 + 0.03, y), (b - BW / 2 - 0.03, y))

    report()
    save(fig, path_out)
    print("wrote", path_out)


if __name__ == "__main__":
    draw("fig8_5.png")
