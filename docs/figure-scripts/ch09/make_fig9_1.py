"""
Figure 9.1: the text-to-speech pipeline.

A straight left-to-right chain at the book's type scale. The chapter's whole
structure is this picture: the front end is one card, the back end is two, and
the chapter takes them in that order rather than in the order the delivered
draft used. The two cards that carry information a reader cannot infer from the
title keep a short label beneath them; everything else is in the caption.

No sentences inside the artwork.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save)
from figfit import must_fit, report

CARDS = [("input text", "", BOXFILL, NAVY),
         ("front end", "normalize, diacritize,\ngrapheme-to-phoneme",
          WHITE, NAVY),
         ("acoustic\nmodel", "phonemes to a\nmel spectrogram", WHITE, NAVY),
         ("vocoder", "mel spectrogram\nto a waveform", WHITE, NAVY),
         ("speech\nwaveform", "", GREENFILL, GREEN)]

BW, BH, PAD = 2.24, 1.28, 0.16


def draw(path_out):
    w, h = 12.6, 4.2
    fig, ax = canvas(w, h, (0, w), (0, h))
    y = 2.55

    gap = (w - 0.7 - len(CARDS) * BW) / (len(CARDS) - 1)
    xs = [0.35 + BW / 2 + i * (BW + gap) for i in range(len(CARDS))]

    for x, (title, sub, fill, edge) in zip(xs, CARDS):
        box(ax, x, y, BW, BH, fill=fill, edge=edge, lw=1.5, r=0.12)
        t = note(ax, x, y, title, size=10.4, colour=edge, weight="bold",
                 linespacing=1.5)
        must_fit(fig, t, BW - PAD, max(title.split("\n"), key=len))
        if sub:
            t = note(ax, x, y - BH / 2 - 0.44, sub, size=9.0, colour=GREY,
                     linespacing=1.5)
            must_fit(fig, t, BW + 0.42, max(sub.split("\n"), key=len))
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + BW / 2 + 0.03, y), (b - BW / 2 - 0.03, y))

    # the two halves the chapter is built on, marked as spans rather than said
    for x0, x1, label, colour in ((xs[1] - BW / 2, xs[1] + BW / 2,
                                   "front end", NAVY),
                                  (xs[2] - BW / 2, xs[3] + BW / 2,
                                   "back end", ORANGE)):
        ax.plot([x0, x1], [y + BH / 2 + 0.34] * 2, color=colour, lw=1.9,
                solid_capstyle="butt", zorder=6)
        t = note(ax, (x0 + x1) / 2, y + BH / 2 + 0.58, label, size=10.0,
                 colour=colour, weight="bold", z=6)
        must_fit(fig, t, x1 - x0 + 0.6, label)

    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig9_1.png")
