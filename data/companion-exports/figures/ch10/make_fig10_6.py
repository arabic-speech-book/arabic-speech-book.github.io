"""
Figure 10.6: the spoken dialogue loop, with the two stages Arabic changes.

The draft's specification asked for a clockwise loop of six cards and a note in
the middle saying end-to-end understanding can skip stages. That is the diagram
every dialogue textbook prints. Two things make this one the book's:

  The understanding stage is marked, because that is where Arabic slot values
  arrive in forms a string match will miss: an inflected date, a place name with
  more than one accepted spelling, digits in either of two numeral systems.

  The response stage is marked, because the loop closes on the front end of
  Chapter 9. A dialogue system that speaks Arabic back has to diacritize what it
  is about to say, so the whole of Section 9.2 is inside this loop rather than
  beside it.

The end-to-end shortcut is drawn as an arc across the loop from speech to intent
and slots, which is what it is: a chord, not a cycle.

No sentences inside the artwork; the reading is in the caption.
"""
import math

from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

CARDS = [
    ("Arabic\nspeech in", BOXFILL, NAVY, None),
    ("speech\nrecognizer", WHITE, NAVY, None),
    ("intent and\nslots", WHITE, ORANGE,
     "Arabic\nnormalization"),
    ("dialogue\nmanager", WHITE, NAVY, None),
    ("response\ngeneration", WHITE, NAVY, None),
    ("speech\nsynthesis", WHITE, ORANGE,
     "diacritization,\nSection 9.2"),
    ("Arabic\nspeech out", GREENFILL, GREEN, None),
]

BW, BH = 1.46, 0.94
GAP = 0.26


def draw(path_out):
    w, h = 12.6, 4.95
    fig, ax = canvas(w, h, (0, w), (0, h))

    n = len(CARDS)
    span = (0.40, 12.20)
    step = (span[1] - span[0] - BW) / (n - 1)
    xs = [span[0] + BW / 2 + i * step for i in range(n)]
    y = 2.30

    for x, (text, fill, edge, sub) in zip(xs, CARDS):
        box(ax, x, y, BW, BH, fill=fill, edge=edge, lw=1.5, r=0.12)
        t = note(ax, x, y, text, size=8.9, colour=edge, weight="bold",
                 linespacing=1.45)
        must_fit(fig, t, BW - 0.10, max(text.split("\n"), key=len))
        if sub:
            t = note(ax, x, y + BH / 2 + 0.16, sub, size=8.6, colour=ORANGE,
                     va="bottom", linespacing=1.45)
            must_fit(fig, t, 2.60, max(sub.split("\n"), key=len))
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + BW / 2 + 0.03, y), (b - BW / 2 - 0.03, y))

    # the turn: the loop closes back to the start
    top = y + BH / 2 + 1.30
    ax.plot([xs[-1], xs[-1]], [y + BH / 2 + 0.03, top], color=NAVY,
            lw=lws(1.4), zorder=4)
    ax.plot([xs[-1], xs[0]], [top, top], color=NAVY, lw=lws(1.4), zorder=4)
    ax.annotate("", xy=(xs[0], y + BH / 2 + 0.03), xytext=(xs[0], top),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=lws(1.4),
                                mutation_scale=15, shrinkA=0, shrinkB=0),
                zorder=4)
    t = note(ax, (xs[0] + xs[-1]) / 2, top + 0.22, "the next turn", size=9.2,
             colour=NAVY)
    must_fit(fig, t, 3.00, "the next turn")

    # the end-to-end chord, speech straight to intent and slots
    bottom = y - BH / 2 - 0.80
    ax.plot([xs[0], xs[0]], [y - BH / 2 - 0.03, bottom], color=GREY,
            lw=lws(1.3), ls=(0, (4, 3)), zorder=4)
    ax.plot([xs[0], xs[2]], [bottom, bottom], color=GREY, lw=lws(1.3),
            ls=(0, (4, 3)), zorder=4)
    ax.annotate("", xy=(xs[2], y - BH / 2 - 0.03), xytext=(xs[2], bottom),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=lws(1.3),
                                ls=(0, (4, 3)), mutation_scale=14, shrinkA=0,
                                shrinkB=0), zorder=4)
    t = note(ax, (xs[0] + xs[2]) / 2 + 1.05, bottom - 0.26,
             "end-to-end understanding, no transcript", size=9.0, colour=GREY,
             ha="left")
    must_fit(fig, t, 5.20, "end-to-end understanding, no transcript")

    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig10_6.png")
