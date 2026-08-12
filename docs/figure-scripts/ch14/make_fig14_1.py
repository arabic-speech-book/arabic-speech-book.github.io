"""Figure 14.1: the project lifecycle, and the conditions it runs under.

Eight stages, in two rows because eight boxes across a 6.3 inch frame leaves
each label about three quarters of an inch and this book does not print labels
that do not fit. The serpentine is drawn rather than implied: the arrow leaves
the end of the top row, drops, and enters the start of the bottom row, so a
reader never has to guess the reading order.

The band is the part that changed when the book was reordered. In the draft
this figure ended with a dashed arrow out to an ethics chapter that came after
it. Responsible Arabic Speech AI is now Chapter 13 and this is Chapter 14, so
the obligations do not wait at the end of the pipeline: they hold across the
whole of it, and they are drawn as the ground the eight stages stand on.

Which obligation lands on which stage is in the caption. Here they are labels.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report
import matplotlib.patches as mp

TOP = ["the\nspecification", "the data\nplan", "record or\nharvest",
       "annotate"]
BOTTOM = ["align and\nsplit", "a baseline", "evaluate", "the datasheet"]
CONDITIONS = ["consent", "no leakage", "per-group results",
              "documented limits"]

BOUNDS = []


def inside(fig, artist, what):
    fig.canvas.draw()
    bb = artist.get_window_extent(fig.canvas.get_renderer())
    x0, x1 = bb.x0 / fig.dpi, bb.x1 / fig.dpi
    w_in = fig.get_size_inches()[0]
    if x0 < 0.04 or x1 > w_in - 0.04:
        BOUNDS.append(f'{what}: spans {x0:.2f} to {x1:.2f} in')
    return artist


def draw(path_out):
    w, h = 12.6, 4.35
    fig, ax = canvas(w, h, (0, w), (0, h))

    left, right = 0.75, 11.85
    n = 4
    step = (right - left) / n
    bw, bh = step - 0.45, 0.94
    y_top, y_bot = 3.25, 1.55

    band_bot, band_top = 0.30, y_top + bh / 2 + 0.30
    ax.add_patch(mp.FancyBboxPatch(
        (0.30, band_bot), 12.05, band_top - band_bot,
        boxstyle="round,pad=0.02,rounding_size=0.16", facecolor="#FBFCFE",
        edgecolor=EDGE_LIGHT, lw=lws(1.6), zorder=1))

    def row(labels, y, fills):
        xs = []
        for i, (text, (fill, edge)) in enumerate(zip(labels, fills)):
            cx = left + step * (i + 0.5)
            xs.append(cx)
            box(ax, cx, y, bw, bh, fill=fill, edge=edge, lw=1.5, r=0.12)
            t = note(ax, cx, y, text, size=9.4, colour=edge)
            must_fit(fig, t, bw - 0.16, text.replace("\n", " "))
            inside(fig, t, text.replace("\n", " "))
        for a, b in zip(xs, xs[1:]):
            arrow(ax, (a + bw / 2 + 0.06, y), (b - bw / 2 - 0.06, y),
                  colour=ORANGE, lw=1.5, scale=12)
        return xs

    xs_top = row(TOP, y_top, [(BOXFILL, NAVY)] + [(WHITE, NAVY)] * 3)
    xs_bot = row(BOTTOM, y_bot, [(WHITE, NAVY)] * 3 + [(GREENFILL, GREEN)])

    # the turn, drawn rather than implied
    turn = right + 0.28
    arrow(ax, (xs_top[-1] + bw / 2 + 0.06, y_top), (turn, y_top), colour=ORANGE,
          lw=1.5, scale=12)
    arrow(ax, (turn, y_top - 0.10), (turn, (y_top + y_bot) / 2), colour=ORANGE,
          lw=1.5, scale=12)
    ax.plot([turn, left - 0.18], [(y_top + y_bot) / 2] * 2, color=ORANGE,
            lw=lws(1.5), zorder=4)
    ax.plot([left - 0.18, left - 0.18],
            [(y_top + y_bot) / 2, y_bot + 0.10], color=ORANGE, lw=lws(1.5),
            zorder=4)
    arrow(ax, (left - 0.18, y_bot + 0.10),
          (xs_bot[0] - bw / 2 - 0.06, y_bot), colour=ORANGE, lw=1.5, scale=12)

    for i, label in enumerate(CONDITIONS):
        t = note(ax, left + step * (i + 0.5), band_bot + 0.36, label, size=9.2,
                 colour=GREEN)
        must_fit(fig, t, step - 0.20, label)
        inside(fig, t, label)

    # nothing may grow through the band, which is what the last chapter's
    # figure got wrong before it was caught in the proof
    for label, cy in (("top row", y_top), ("bottom row", y_bot)):
        if cy + bh / 2 > band_top - 0.02 or cy - bh / 2 < band_bot + 0.02:
            raise SystemExit(f'the {label} crosses the band edge')

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig14_1.png")
