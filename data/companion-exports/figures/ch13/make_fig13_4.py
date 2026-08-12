"""Figure 13.4: what an average hides.

A grouped bar chart, four dialects and two genders, with the pooled average
drawn across it as a single line. The line is the point of the figure. Every
bar on the right of it is a group the pooled number declares to be fine, and
the Maghrebi bars are nowhere near it.

The numbers are illustrative and the figure says so in a label, because a
reader who takes them for measurements would be taking them for a measurement
of nothing: they are chosen to show the shape of a disparity. The chapter's
real numbers live in the cited work.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report
import matplotlib.patches as mp

# (dialect, women, men) illustrative word error rates
GROUPS = [("MSA", 0.11, 0.10),
          ("Gulf", 0.19, 0.16),
          ("Egyptian", 0.22, 0.18),
          ("Maghrebi", 0.44, 0.33)]
POOLED = sum(v for _, a, b in GROUPS for v in (a, b)) / (2 * len(GROUPS))
TOP = 0.50

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
    w, h = 12.6, 4.95
    fig, ax = canvas(w, h, (0, w), (0, h))

    base, ceiling = 0.95, 4.15
    x0, x1 = 2.20, 11.60
    step = (x1 - x0) / len(GROUPS)
    barw = step * 0.26

    def y_of(v):
        return base + (ceiling - base) * (v / TOP)

    ax.plot([x0 - 0.35, x0 - 0.35], [base, ceiling], color=GREY, lw=lws(1.2),
            zorder=3)
    ax.plot([x0 - 0.35, x1], [base, base], color=GREY, lw=lws(1.2), zorder=3)
    t = note(ax, 0.12, (base + ceiling) / 2, "word error rate", size=9.2,
             colour=GREY, ha="left", va="center")
    must_fit(fig, t, 1.95, "axis")
    inside(fig, t, "axis")

    for i, (name, women, men) in enumerate(GROUPS):
        cx = x0 + step * (i + 0.5)
        for sign, value, colour, fill in ((-1, women, NAVY, BOXFILL),
                                          (1, men, ORANGE, "#FBE7DE")):
            bx = cx + sign * barw * 0.58
            ax.add_patch(mp.Rectangle((bx - barw / 2, base), barw,
                                      y_of(value) - base, facecolor=fill,
                                      edgecolor=colour, lw=lws(1.4), zorder=4))
        t = note(ax, cx, base - 0.32, name, size=9.6, colour=NAVY,
                 weight="bold")
        must_fit(fig, t, step - 0.20, name)
        inside(fig, t, name)

    ax.plot([x0 - 0.35, x1], [y_of(POOLED)] * 2, color=GREEN, lw=lws(1.6),
            linestyle=(0, (5, 3)), zorder=6)
    # on the left, where the bars are short: on the right it lay across the
    # two Maghrebi bars, which are the pair the line exists to indict
    t = note(ax, x0 - 0.25, y_of(POOLED) + 0.28, "the pooled average",
             size=9.2, colour=GREEN, ha="left", va="center")
    must_fit(fig, t, 3.10, "pooled")
    inside(fig, t, "pooled")

    # the legend, two swatches rather than a sentence
    for i, (label, colour, fill) in enumerate((("women", NAVY, BOXFILL),
                                               ("men", ORANGE, "#FBE7DE"))):
        lx = 2.30 + i * 1.90
        ax.add_patch(mp.Rectangle((lx, ceiling + 0.36), 0.30, 0.24,
                                  facecolor=fill, edgecolor=colour,
                                  lw=lws(1.4), zorder=4))
        t = note(ax, lx + 0.42, ceiling + 0.48, label, size=9.2, colour=colour,
                 ha="left", va="center")
        must_fit(fig, t, 1.30, label)
        inside(fig, t, label)

    t = note(ax, x1, ceiling + 0.48, "illustrative numbers", size=9.2,
             colour=GREY, ha="right", va="center")
    must_fit(fig, t, 3.20, "illustrative")
    inside(fig, t, "illustrative")

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig13_4.png")
