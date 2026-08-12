"""
Figure 9.5: the two halves of evaluating synthesis.

Left, the subjective half: a five-point Mean Opinion Score scale, drawn as a
scale rather than described, with its two named endpoints and a mean marked on
it. Right, the objective half: the loop that turns a synthesized utterance back
into text and charges the difference as Word Error Rate.

The point the caption makes, and the picture shows, is that the two halves
measure different things and neither replaces the other, which is why they are
drawn side by side on one baseline rather than in sequence.

The illustrative mean and its interval are marked illustrative inside the
artwork, because a reader must not be able to quote them as a measurement.
"""
from matplotlib.patches import Rectangle

from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save)
from figscale import fs, lws
from figfit import must_fit, report

POINTS = [(1, "bad"), (2, ""), (3, ""), (4, ""), (5, "excellent")]
MEAN, HALFWIDTH = 3.9, 0.25          # illustrative


def draw(path_out):
    w, h = 12.6, 5.0
    fig, ax = canvas(w, h, (0, w), (0, h))

    # ================= left: the scale ===================================
    sx, sy0, sy1 = 2.65, 1.15, 3.95
    ax.plot([sx, sx], [sy0, sy1], color=GREY, lw=lws(1.6), zorder=3)

    def y_of(v):
        return sy0 + (v - 1) / 4 * (sy1 - sy0)

    for v, label in POINTS:
        ax.plot([sx - 0.14, sx + 0.14], [y_of(v)] * 2, color=GREY,
                lw=lws(1.6), zorder=3)
        t = note(ax, sx - 0.44, y_of(v), str(v), size=10.0, colour=NAVY,
                 weight="bold", ha="right")
        must_fit(fig, t, 0.60, str(v))
        if label:
            t = note(ax, sx - 0.76, y_of(v), label, size=9.4, colour=GREY,
                     ha="right")
            must_fit(fig, t, 2.00, label)

    # the mean marked on the scale itself, with its interval
    lo, hi = y_of(MEAN - HALFWIDTH), y_of(MEAN + HALFWIDTH)
    ax.add_patch(Rectangle((sx - 0.30, lo), 0.60, hi - lo, facecolor=BOXFILL,
                           edgecolor=NAVY, lw=lws(1.2), zorder=4))
    ax.plot([sx - 0.34, sx + 0.34], [y_of(MEAN)] * 2, color=NAVY,
            lw=lws(2.2), zorder=5)
    t = note(ax, sx + 0.46, y_of(MEAN) + 0.16, f"mean {MEAN:.1f}", size=9.6,
             colour=NAVY, weight="bold", ha="left")
    must_fit(fig, t, 1.70, "mean 3.9")
    t = note(ax, sx + 0.46, y_of(MEAN) - 0.20, "with its interval", size=9.0,
             colour=GREY, ha="left")
    must_fit(fig, t, 2.00, "with its interval")

    t = note(ax, sx, sy1 + 0.62, "listeners rate naturalness", size=10.4,
             colour=NAVY, weight="bold")
    must_fit(fig, t, 5.00, "listeners rate naturalness")
    note(ax, sx, sy0 - 0.48, "illustrative", size=9.4, colour=GREY,
         style="italic")

    # ================= right: the objective loop =========================
    bx = 9.35
    BW, BH = 2.85, 0.88
    stack = [("synthesized speech", WHITE, NAVY, 3.85),
             ("automatic speech\nrecognizer", WHITE, NAVY, 2.72),
             ("compare with the\ninput text", WHITE, NAVY, 1.59)]
    for title, fill, edge, y in stack:
        box(ax, bx, y, BW, BH, fill=fill, edge=edge, lw=1.5, r=0.12)
        t = note(ax, bx, y, title, size=9.8, colour=edge, weight="bold",
                 linespacing=1.45)
        must_fit(fig, t, BW - 0.12, max(title.split("\n"), key=len))
    for a, b in zip(stack, stack[1:]):
        arrow(ax, (bx, a[3] - BH / 2 - 0.03), (bx, b[3] + BH / 2 + 0.03))

    box(ax, bx, 0.62, BW, 0.72, fill=GREENFILL, edge=GREEN, lw=1.5, r=0.12)
    t = note(ax, bx, 0.62, "Word Error Rate", size=9.8, colour=GREEN,
             weight="bold")
    must_fit(fig, t, BW - 0.12, "Word Error Rate")
    arrow(ax, (bx, 1.59 - BH / 2 - 0.03), (bx, 0.62 + 0.36 + 0.03))

    t = note(ax, bx, sy1 + 0.62, "a recognizer checks intelligibility",
             size=10.4, colour=NAVY, weight="bold")
    must_fit(fig, t, 5.20, "a recognizer checks intelligibility")

    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig9_5.png")
