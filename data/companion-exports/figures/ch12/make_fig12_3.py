"""Figure 12.3: the tajwīd rule families, and what each one leaves in the audio.

A taxonomy is only useful to an engineer if every branch ends in something a
system can measure, so each family carries the acoustic quantity a detector
would have to read. That is the whole design of the figure: the left column is
the rule, the right column is the measurement, and a family with no measurable
consequence would have nowhere to sit.

The rule names are given in transliteration with the Arabic beside them,
because a reader who has heard these terms in a class has heard them in Arabic.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save, ar, ARF)
from figscale import lws
from figfit import must_fit, report

FAMILIES = [
    ("madd", "مد", "how long a vowel is held"),
    ("idghām", "إدغام", "one sound absorbed into the next"),
    ("ikhfāʾ", "إخفاء", "a sound hidden, with nasality"),
    ("ghunna", "غنة", "nasal energy, and for how long"),
    ("qalqala", "قلقلة", "the echo on a stopped consonant"),
    ("waqf", "وقف", "where a pause may fall"),
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
    w, h = 12.6, 5.60
    fig, ax = canvas(w, h, (0, w), (0, h))

    t = note(ax, 2.35, 5.20, "the rule", size=10.0, colour=NAVY, weight="bold")
    must_fit(fig, t, 3.60, "head one")
    inside(fig, t, "head one")
    t = note(ax, 8.60, 5.20, "what it leaves in the audio", size=10.0,
             colour=GREEN, weight="bold")
    must_fit(fig, t, 5.40, "head two")
    inside(fig, t, "head two")
    ax.plot([0.30, 12.30], [4.92, 4.92], color=EDGE_LIGHT, lw=lws(1.4),
            zorder=2)

    top, gap = 4.42, 0.74
    for i, (name, arabic, effect) in enumerate(FAMILIES):
        y = top - i * gap
        box(ax, 2.35, y, 3.40, 0.58, fill=BOXFILL, edge=NAVY, lw=1.3, r=0.10)
        t = note(ax, 1.70, y, name, size=9.8, colour=NAVY)
        must_fit(fig, t, 1.90, name)
        t = note(ax, 3.35, y, ar(arabic), size=12.0, colour=NAVY,
                 fontproperties=ARF)
        must_fit(fig, t, 1.10, arabic)
        box(ax, 8.60, y, 5.20, 0.58, fill=GREENFILL, edge=GREEN, lw=1.3,
            r=0.10)
        t = note(ax, 8.60, y, effect, size=9.6, colour=GREEN)
        must_fit(fig, t, 4.90, effect)
        arrow(ax, (2.35 + 1.70 + 0.06, y), (8.60 - 2.60 - 0.06, y),
              colour=GREY, lw=1.3, scale=11)

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig12_3.png")
