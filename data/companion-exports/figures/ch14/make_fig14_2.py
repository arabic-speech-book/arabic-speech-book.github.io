"""Figure 14.2: the annotation workflow, with the loop that closes it.

Two inputs, a chain of five, and one arrow that goes backwards. The backwards
arrow is the figure's reason for existing. Quality control is not a gate that
passes or fails a batch; what it produces is an amended guideline, and a
project that measures agreement without changing the guideline has paid for the
measurement and kept the disagreement.

The first pass is drawn dashed because it is optional. A recognizer can fill
the transcript in and annotators can correct it, which is much cheaper, and the
chapter says plainly that the correction is the step that must never be
skipped.

The chain is one row rather than two. A serpentine here put the return arrow
across the boxes it was meant to bypass, which is the kind of thing that looks
fine in code and wrong on the page.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

CHAIN = [("a first\npass", "dashed", GREY, WHITE),
         ("human\ncorrection", "solid", NAVY, WHITE),
         ("agreement\ncheck", "solid", NAVY, WHITE),
         ("forced\nalignment", "solid", NAVY, WHITE),
         ("the labeled\ncorpus", "solid", GREEN, GREENFILL)]

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
    w, h = 12.6, 3.05
    fig, ax = canvas(w, h, (0, w), (0, h))
    y = 1.85
    iw = 1.95
    ix = 1.15

    box(ax, ix, y + 0.52, iw, 0.72, fill=BOXFILL, edge=NAVY, lw=1.5, r=0.12)
    t = note(ax, ix, y + 0.52, "raw audio", size=9.4, colour=NAVY)
    must_fit(fig, t, iw - 0.16, "raw audio")
    inside(fig, t, "raw audio")

    box(ax, ix, y - 0.52, iw, 0.72, fill=WHITE, edge=ORANGE, lw=1.6, r=0.12)
    t = note(ax, ix, y - 0.52, "the guideline", size=9.4, colour=ORANGE,
             weight="bold")
    must_fit(fig, t, iw - 0.16, "the guideline")
    inside(fig, t, "the guideline")

    x0, x1 = 2.60, 12.45
    step = (x1 - x0) / len(CHAIN)
    bw, bh = step - 0.26, 0.94
    xs = []
    for i, (text, ls, edge, fill) in enumerate(CHAIN):
        cx = x0 + step * (i + 0.5)
        xs.append(cx)
        box(ax, cx, y, bw, bh, fill=fill, edge=edge, lw=1.5, r=0.12, ls=ls)
        t = note(ax, cx, y, text, size=9.0, colour=edge)
        must_fit(fig, t, bw - 0.14, text.replace("\n", " "))
        inside(fig, t, text.replace("\n", " "))
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + bw / 2 + 0.05, y), (b - bw / 2 - 0.05, y),
              colour=ORANGE, lw=1.4, scale=11)
    for dy in (0.52, -0.52):
        arrow(ax, (ix + iw / 2 + 0.06, y + dy * 0.72),
              (xs[0] - bw / 2 - 0.05, y + dy * 0.16), colour=ORANGE, lw=1.4,
              scale=11)

    t = note(ax, xs[0], y + 0.72, "optional", size=8.8, colour=GREY)
    must_fit(fig, t, 1.50, "optional")
    inside(fig, t, "optional")

    # the loop: what quality control produces is a better guideline
    foot = y - 1.42
    ax.plot([xs[2], xs[2]], [y - bh / 2 - 0.06, foot], color=GREEN,
            lw=lws(1.5), zorder=4)
    ax.plot([xs[2], ix], [foot, foot], color=GREEN, lw=lws(1.5), zorder=4)
    arrow(ax, (ix, foot), (ix, y - 0.52 - 0.36 - 0.06), colour=GREEN, lw=1.5,
          scale=12)
    t = note(ax, (xs[2] + ix) / 2, foot + 0.26, "amend the guideline",
             size=9.0, colour=GREEN)
    must_fit(fig, t, 4.00, "amend")
    inside(fig, t, "amend")

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig14_2.png")
