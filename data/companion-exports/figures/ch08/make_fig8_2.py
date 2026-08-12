"""
Figure 8.2: the dialect identification pipeline.

A straight left-to-right chain, redrawn at the book's type scale. The
illustrator specification put a subtitle under three of the five cards; the two
that carry information a reader cannot infer from the card title are kept as
short labels beneath the boxes, and the rest is in the caption.

No sentences inside the artwork.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

CARDS = [("audio", "one utterance", BOXFILL, NAVY),
         ("features", "log-mel or\nself-supervised", WHITE, NAVY),
         ("utterance\nembedding", "pooled to\none vector", WHITE, NAVY),
         ("dialect\nclassifier", "", WHITE, NAVY),
         ("dialect label\nand confidence", "", GREENFILL, GREEN)]

BW, BH, PAD = 2.26, 1.24, 0.16


def draw(path_out):
    w, h = 12.6, 3.9
    fig, ax = canvas(w, h, (0, w), (0, h))
    y = 2.25

    gap = (w - 0.7 - len(CARDS) * BW) / (len(CARDS) - 1)
    xs = [0.35 + BW / 2 + i * (BW + gap) for i in range(len(CARDS))]

    for x, (title, sub, fill, edge) in zip(xs, CARDS):
        box(ax, x, y, BW, BH, fill=fill, edge=edge, lw=1.5, r=0.12)
        t = note(ax, x, y, title, size=10.0, colour=edge, weight="bold",
                 linespacing=1.5)
        must_fit(fig, t, BW - PAD, max(title.split("\n"), key=len))
        if sub:
            t = note(ax, x, y - BH / 2 - 0.42, sub, size=9.0, colour=GREY,
                     linespacing=1.5)
            must_fit(fig, t, BW + 0.34, max(sub.split("\n"), key=len))
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + BW / 2 + 0.03, y), (b - BW / 2 - 0.03, y))

    report()
    save(fig, path_out)
    print("wrote", path_out)


if __name__ == "__main__":
    draw("fig8_2.png")
