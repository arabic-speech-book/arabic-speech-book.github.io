"""Figure 12.1: the computer-assisted pronunciation training pipeline.

Four stages, left to right, and the one thing that makes the whole arrangement
possible is drawn rather than assumed: the target text is on the page, feeding
the alignment, so the system is never guessing what was meant.

The last card is the one that matters to a learner. A score is not feedback,
so the card carries the three things feedback has to do rather than the bare
word, and all four lines are drawn inside the card with the title clear of the
top edge.

Nothing here explains itself in a sentence. Every string is a label, the notes
that argued a point have gone to the caption, and the rule the whole book
follows is that a figure names things and the caption says what they mean.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

STAGES = [("learner audio", BOXFILL, NAVY),
          ("forced alignment", WHITE, NAVY),
          ("per-phone scoring", WHITE, NAVY),
          ("feedback", GREENFILL, GREEN)]
FEEDBACK = ["locate the sound", "name the error", "say what to fix"]

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
    w, h = 12.6, 3.20
    fig, ax = canvas(w, h, (0, w), (0, h))
    y = 1.45
    xs = [1.55, 4.35, 7.15, 10.35]
    bw, bh = 2.45, 0.80

    # the fourth card is a stack, so it is placed by its edges rather than by
    # a centre: the title sits a clear margin below the top and the three
    # lines below the title, all of them inside the outline
    top4, bot4 = y + 0.60, y - 1.30
    for i, (x, (text, fill, edge)) in enumerate(zip(xs, STAGES)):
        width = 3.30 if i == 3 else bw
        height = (top4 - bot4) if i == 3 else bh
        box(ax, x, ((top4 + bot4) / 2) if i == 3 else y, width, height,
            fill=fill, edge=edge, lw=1.6 if i == 3 else 1.4, r=0.12)
        t = note(ax, x, (top4 - 0.30) if i == 3 else y, text,
                 size=10.2 if i == 3 else 9.8, colour=edge,
                 weight="bold" if i == 3 else "normal")
        must_fit(fig, t, width - 0.20, text)
        if i == 3:
            inside(fig, t, text)
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + bw / 2 + 0.05, y), (b - (3.30 if b == xs[3] else bw) / 2
              - 0.05, y), colour=GREY, lw=1.5, scale=12)

    for i, line in enumerate(FEEDBACK):
        cy = top4 - 0.72 - i * 0.36
        if cy - 0.14 < bot4 + 0.10:
            raise SystemExit(f'{line!r} would sit on the edge of the card')
        t = note(ax, xs[3], cy, line, size=9.2, colour=GREEN)
        must_fit(fig, t, 3.00, line)
        inside(fig, t, line)

    # the target text is what makes the alignment possible
    ty = 2.70
    box(ax, xs[1], ty, 2.90, 0.62, fill=WHITE, edge=ORANGE, lw=1.5, r=0.12,
        ls=(0, (4, 3)))
    t = note(ax, xs[1], ty, "the target text", size=9.6, colour=ORANGE)
    must_fit(fig, t, 2.70, "the target text")
    arrow(ax, (xs[1], ty - 0.35), (xs[1], y + bh / 2 + 0.05), colour=ORANGE,
          lw=1.5, scale=12)
    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig12_1.png")
