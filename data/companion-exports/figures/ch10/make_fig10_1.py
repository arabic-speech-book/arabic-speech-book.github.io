"""
Figure 10.1: the cascade and the end-to-end model, on one skeleton.

The draft drew these as two unrelated rows of boxes, which shows that one has
more boxes than the other and nothing else. What separates them is not the count
of stages, it is what sits between them, and that is the same axis the book uses
in Section 9.5 for synthesis. Drawing it the same way here lets a reader who has
read Chapter 9 recognise the shape before reading a word.

Both rows sit on the same five slots and end on the same card. The middle slot
is the seam, drawn in orange:

  The cascade's seam is an Arabic transcript. It is text. Anyone can read it,
  and a wrong word in it can be found and corrected before the translator ever
  runs. That is the cascade's real advantage, and it is worth more in Arabic
  than in most languages, because dialectal recognition is where the errors are.

  The end-to-end model has no seam. The slot is drawn empty and dashed, because
  there is nothing there to inspect rather than because the figure ran out of
  room. Nothing is written down between the audio and the English.

No sentences inside the artwork; the reading is in the caption.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save)
from figfit import must_fit, report

SPAN = (2.30, 12.46)
SLOTS = 5
GAP = 0.30
BH = 0.95


def geometry():
    bw = (SPAN[1] - SPAN[0] - (SLOTS - 1) * GAP) / SLOTS
    step = (SPAN[1] - SPAN[0] - bw) / (SLOTS - 1)
    return [SPAN[0] + bw / 2 + i * step for i in range(SLOTS)], bw


def tag(fig, ax, y, head, sub, colour):
    t = note(ax, 0.10, y + 0.34, head, size=10.4, colour=colour, weight="bold",
             ha="left", va="center")
    must_fit(fig, t, 2.10, head)
    t = note(ax, 0.10, y - 0.24, sub, size=9.4, colour=GREY, ha="left",
             va="top", linespacing=1.45)
    must_fit(fig, t, 2.10, max(sub.split("\n"), key=len))


def card(fig, ax, x, y, w, text, fill=WHITE, edge=NAVY, size=9.1):
    box(ax, x, y, w, BH, fill=fill, edge=edge, lw=1.5, r=0.12)
    t = note(ax, x, y, text, size=size, colour=edge, weight="bold",
             linespacing=1.45)
    must_fit(fig, t, w - 0.12, max(text.split("\n"), key=len))


def draw(path_out):
    w, h = 12.6, 4.55
    fig, ax = canvas(w, h, (0, w), (0, h))
    xs, bw = geometry()
    y1, y2 = 3.50, 1.20

    tag(fig, ax, y1, "Cascade", "recognize, then\ntranslate", NAVY)
    card(fig, ax, xs[0], y1, bw, "Arabic\nspeech", fill=BOXFILL)
    card(fig, ax, xs[1], y1, bw, "speech\nrecognizer")
    card(fig, ax, xs[2], y1, bw, "Arabic\ntranscript", edge=ORANGE)
    card(fig, ax, xs[3], y1, bw, "machine\ntranslation")
    card(fig, ax, xs[4], y1, bw, "English\ntext", fill=GREENFILL, edge=GREEN)
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + bw / 2 + 0.03, y1), (b - bw / 2 - 0.03, y1))
    t = note(ax, xs[2], y1 - BH / 2 - 0.30, "text you can read, and correct",
             size=9.0, colour=ORANGE)
    must_fit(fig, t, 3.60, "text you can read, and correct")

    tag(fig, ax, y2, "End to end", "one model, no\ntranscript", ORANGE)
    card(fig, ax, xs[0], y2, bw, "Arabic\nspeech", fill=BOXFILL)
    left, right = xs[1] - bw / 2, xs[3] + bw / 2
    card(fig, ax, (left + right) / 2, y2, right - left,
         "one speech-translation model")
    card(fig, ax, xs[4], y2, bw, "English\ntext", fill=GREENFILL, edge=GREEN)
    arrow(ax, (xs[0] + bw / 2 + 0.03, y2), (xs[1] - bw / 2 - 0.03, y2))
    arrow(ax, (right + 0.03, y2), (xs[4] - bw / 2 - 0.03, y2))
    box(ax, xs[2], y2 - BH / 2 - 0.42, bw, 0.34, fill=WHITE, edge=ORANGE,
        lw=1.2, r=0.10, ls=(0, (4, 3)))
    t = note(ax, xs[2], y2 - BH / 2 - 0.80, "nothing written down",
             size=9.0, colour=ORANGE)
    must_fit(fig, t, 3.20, "nothing written down")

    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig10_1.png")
