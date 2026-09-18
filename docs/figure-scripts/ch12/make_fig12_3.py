"""Figure 12.4: a healthcare voice interface, drawn around the thing that
decides whether it is safe.

The pipeline across the middle is ordinary and short. What the chapter argues
is that the pipeline is not the system: the system is the pipeline plus a gate
that stops it, and plus the conditions it operates under. So the gate is drawn
on the path, with the two ways out of it, and the governing conditions are
drawn as a band the whole path sits inside rather than as a footnote beside it.

The low-confidence exit is the one a reader should remember, which is why it
leaves the gate downward and lands on a person.

Both exits sit inside the band, which is the point: acting and deferring are
alike governed by the conditions. The band is therefore sized from the boxes
rather than set by hand, so nothing can grow through its edge again, and the
sentence that used to float above the artwork now lives in the caption where
the book keeps its arguments.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report
import matplotlib.patches as mp

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
    w, h = 12.6, 3.80
    fig, ax = canvas(w, h, (0, w), (0, h))
    y = 2.20

    # The band is drawn from the content it governs rather than from two
    # numbers typed in: its top clears the highest box by a margin and its
    # foot leaves room for the four conditions written along the bottom.
    band_bot = 0.20
    band_top = (y + 0.80) + 0.31 + 0.28
    ax.add_patch(mp.FancyBboxPatch((0.30, band_bot), 12.05,
                                   band_top - band_bot,
                                   boxstyle="round,pad=0.02,rounding_size=0.16",
                                   facecolor="#FBFCFE", edgecolor=EDGE_LIGHT,
                                   lw=lws(1.6), zorder=1))
    for i, label in enumerate(["consent", "encryption", "retention limits",
                               "clinical validation"]):
        t = note(ax, 1.70 + i * 3.10, band_bot + 0.32, label, size=9.0,
                 colour=GREY)
        must_fit(fig, t, 2.90, label)
        inside(fig, t, label)

    xs = [1.60, 4.25, 6.90]
    bw, bh = 2.30, 0.78
    cells = [("the patient speaks", BOXFILL, NAVY),
             ("adapted recognizer", WHITE, NAVY),
             ("understanding", WHITE, NAVY)]
    for x, (text, fill, edge) in zip(xs, cells):
        box(ax, x, y, bw, bh, fill=fill, edge=edge, lw=1.4, r=0.12)
        t = note(ax, x, y, text, size=8.8, colour=edge)
        must_fit(fig, t, bw - 0.12, text)
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + bw / 2 + 0.05, y), (b - bw / 2 - 0.05, y), colour=GREY,
              lw=1.5, scale=12)

    # the gate
    gx, gw = 9.30, 1.80
    box(ax, gx, y, gw, 0.96, fill=WHITE, edge=ORANGE, lw=2.0, r=0.12)
    t = note(ax, gx, y + 0.15, "confident?", size=9.8, colour=ORANGE,
             weight="bold")
    must_fit(fig, t, gw - 0.12, "confident?")
    t = note(ax, gx, y - 0.20, "the gate", size=8.6, colour=ORANGE)
    must_fit(fig, t, gw - 0.12, "the gate")
    arrow(ax, (xs[2] + bw / 2 + 0.05, y), (gx - gw / 2 - 0.05, y), colour=GREY,
          lw=1.5, scale=12)

    ox, ow = 11.30, 1.70
    box(ax, ox, y + 0.80, ow, 0.62, fill=GREENFILL, edge=GREEN, lw=1.4,
        r=0.10)
    t = note(ax, ox, y + 0.80, "act", size=9.6, colour=GREEN)
    must_fit(fig, t, ow - 0.16, "act")
    inside(fig, t, "act")
    arrow(ax, (gx + gw / 2 + 0.05, y + 0.22), (ox - ow / 2 - 0.05, y + 0.80),
          colour=GREEN, lw=1.4, scale=11)

    box(ax, ox, y - 1.02, ow, 0.62, fill=WHITE, edge=ORANGE, lw=1.6, r=0.10)
    t = note(ax, ox, y - 1.02, "a person", size=9.6, colour=ORANGE,
             weight="bold")
    must_fit(fig, t, ow - 0.16, "a person")
    inside(fig, t, "a person")
    arrow(ax, (gx + gw / 2 + 0.05, y - 0.22), (ox - ow / 2 - 0.05, y - 1.02),
          colour=ORANGE, lw=1.6, scale=12)

    # every box drawn above sits inside the band, and this is checked rather
    # than trusted, because the last revision put one through the top edge
    for label, cy, hh in (("act", y + 0.80, 0.62),
                          ("a person", y - 1.02, 0.62),
                          ("the gate", y, 0.96),
                          ("the pipeline", y, 0.78)):
        if cy + hh / 2 > band_top - 0.02 or cy - hh / 2 < band_bot + 0.02:
            raise SystemExit(f'the {label} box crosses the band edge')

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig12_4.png")
