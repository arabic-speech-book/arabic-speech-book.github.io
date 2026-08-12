"""Figure 13.5: a published responsible AI framework, against this chapter.

Six principle cards, and under each the sections of this chapter that answer it
in engineering terms. That pairing is the whole figure. A principle is easy to
agree with and hard to act on, and the test of a chapter like this one is
whether every principle it endorses has a measurement, a mechanism or a
document underneath it. Drawn this way, a principle with nothing under it would
be visible immediately, which is a useful thing for a reader to be able to
check.

The principles are Microsoft's published set, named and cited as one widely
used industry framework rather than as the framework. Other bodies name
overlapping sets and the caption says so.

Section numbers are labels, not prose. What each pairing means is in the
caption.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

# (principle, the sections of this chapter that answer it)
PRINCIPLES = [
    ("Fairness", "13.7"),
    ("Reliability\nand safety", "13.5 and 13.6"),
    ("Privacy\nand security", "13.2 and 13.3"),
    ("Transparency", "13.4 and 13.7"),
    ("Accountability", "13.7"),
    ("Inclusiveness", "13.1 and 13.7"),
]

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
    w, h = 12.6, 4.55
    fig, ax = canvas(w, h, (0, w), (0, h))

    left, right = 0.55, 12.05
    cols = 3
    step = (right - left) / cols
    bw, bh = step - 0.45, 1.42
    ys = [3.20, 1.32]

    for i, (name, where) in enumerate(PRINCIPLES):
        cx = left + step * (i % cols + 0.5)
        cy = ys[i // cols]
        # one fill for all six: shading a column would imply a grouping
        # the framework does not have
        box(ax, cx, cy, bw, bh, fill=WHITE, edge=NAVY, lw=1.6, r=0.14)
        t = note(ax, cx, cy + 0.24, name, size=10.4, colour=NAVY,
                 weight="bold")
        must_fit(fig, t, bw - 0.18, name.replace("\n", " "))
        inside(fig, t, name.replace("\n", " "))
        t = note(ax, cx, cy - 0.42, where, size=9.4, colour=GREEN)
        must_fit(fig, t, bw - 0.18, where)
        inside(fig, t, where)

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig13_5.png")
