"""Figure 13.1: a threat-and-harm model for an Arabic speech system.

The specification the draft carried asked for four threats pointing inward at a
central card with a band of safeguards underneath. Drawn that way the reader
gets a list of threats and a list of safeguards and no way to tell which
answers which, and the chapter's actual claim is the pairing: each failure mode
calls for a different safeguard.

So the figure is drawn in columns. A threat sits above the system and the
safeguard that answers it sits below, in the same column, and the arrows say
which direction each is travelling: threats come down at the system, safeguards
come up to meet it. A reader can then read one column and have the whole
argument for that risk.

Every string is a label. What the threats cost, and who they cost it to, is in
the caption.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report
import matplotlib.patches as mp

# Two lines each, because four columns across a 6.3 in frame leave about an
# inch and a quarter of drawn width per card at reproduction size, and a label
# that does not fit its box is the defect this book keeps catching.
COLUMNS = [
    ("spoofing and\ndeepfakes", "detection and\nwatermarking"),
    ("identity\nleakage", "anonymization"),
    ("adversarial\naudio", "robust\nevaluation"),
    ("unfair errors\nby group", "fairness\naudits"),
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
    w, h = 12.6, 5.30
    fig, ax = canvas(w, h, (0, w), (0, h))

    n = len(COLUMNS)
    left, right = 1.62, 12.30
    step = (right - left) / n
    bw = step - 0.34
    y_threat, y_system, y_guard = 4.50, 2.65, 0.80
    bh = 0.94

    # the system, one bar under everything that attacks it
    box(ax, (left + right) / 2, y_system, right - left, 0.86, fill=BOXFILL,
        edge=NAVY, lw=1.8, r=0.14)
    t = note(ax, (left + right) / 2, y_system, "the Arabic speech system",
             size=11.0, colour=NAVY, weight="bold")
    must_fit(fig, t, right - left - 0.4, "system")
    inside(fig, t, "system")

    for i, (threat, guard) in enumerate(COLUMNS):
        cx = left + step * (i + 0.5)

        box(ax, cx, y_threat, bw, bh, fill=WHITE, edge=ORANGE, lw=1.5, r=0.12)
        t = note(ax, cx, y_threat, threat, size=9.2, colour=ORANGE,
                 weight="bold")
        must_fit(fig, t, bw - 0.16, threat.replace("\n", " "))
        inside(fig, t, threat.replace("\n", " "))
        arrow(ax, (cx, y_threat - bh / 2 - 0.06),
              (cx, y_system + 0.43 + 0.06), colour=ORANGE, lw=1.5, scale=12)

        box(ax, cx, y_guard, bw, bh, fill=GREENFILL, edge=GREEN, lw=1.5,
            r=0.12)
        t = note(ax, cx, y_guard, guard, size=9.2, colour=GREEN)
        must_fit(fig, t, bw - 0.16, guard.replace("\n", " "))
        inside(fig, t, guard.replace("\n", " "))
        arrow(ax, (cx, y_guard + bh / 2 + 0.06),
              (cx, y_system - 0.43 - 0.06), colour=GREEN, lw=1.5, scale=12)

    # the two sides, named once each at the edge rather than per box
    for label, cy, colour in (("threats", y_threat, ORANGE),
                              ("safeguards", y_guard, GREEN)):
        t = note(ax, 0.16, cy, label, size=9.0, colour=colour, ha="left",
                 va="center", style="italic")
        must_fit(fig, t, 1.38, label)
        inside(fig, t, label)

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig13_1.png")
