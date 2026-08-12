"""Figure 13.3: watermarking, embedded once and detected later.

Two rows and a turn. The top row is what the generator does, at the moment the
audio is made: the mark goes in there and nowhere else, which is the whole
reason watermarking depends on the generator cooperating. The bottom row is
what a checker does afterwards, on a file that has been through whatever the
internet does to a file, which is why the arrow between the rows is labelled
for the editing rather than drawn as a plain line.

The detector answers one question and the figure draws both answers, because a
reader should see that the no branch exists and means only that no mark was
found. What a missing mark does not prove belongs in the caption.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

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
    w, h = 12.6, 4.90
    fig, ax = canvas(w, h, (0, w), (0, h))
    top, bottom = 3.95, 1.55
    bw, bh = 2.60, 0.86

    xs = [1.75, 4.75, 7.75]
    for cx, text, fill, edge in zip(
            xs, ["generated speech", "embed the mark", "watermarked audio"],
            [BOXFILL, WHITE, GREENFILL], [NAVY, ORANGE, GREEN]):
        box(ax, cx, top, bw, bh, fill=fill, edge=edge, lw=1.5, r=0.12)
        t = note(ax, cx, top, text, size=9.6, colour=edge)
        must_fit(fig, t, bw - 0.16, text)
        inside(fig, t, text)
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + bw / 2 + 0.06, top), (b - bw / 2 - 0.06, top),
              colour=ORANGE, lw=1.5, scale=12)

    # the turn: the file goes out into the world and comes back changed
    turn = 11.75
    arrow(ax, (xs[2] + bw / 2 + 0.06, top), (turn, top), colour=GREY, lw=1.5,
          scale=12)
    arrow(ax, (turn, top - 0.10), (turn, bottom + 0.10), colour=GREY, lw=1.5,
          scale=12)
    t = note(ax, turn - 0.22, (top + bottom) / 2, "shared\nand edited",
             size=9.0, colour=GREY, ha="right")
    must_fit(fig, t, 1.45, "shared and edited")
    inside(fig, t, "shared and edited")

    xs2 = [9.60, 6.70, 3.80]
    for cx, text, fill, edge in zip(
            xs2, ["the audio again", "the detector", "mark found?"],
            [WHITE, WHITE, WHITE], [GREY, NAVY, ORANGE]):
        box(ax, cx, bottom, bw, bh, fill=fill, edge=edge, lw=1.5, r=0.12)
        t = note(ax, cx, bottom, text, size=9.6, colour=edge,
                 weight="bold" if edge == ORANGE else "normal")
        must_fit(fig, t, bw - 0.16, text)
        inside(fig, t, text)
    arrow(ax, (turn, bottom), (xs2[0] + bw / 2 + 0.06, bottom), colour=GREY,
          lw=1.5, scale=12)
    for a, b in zip(xs2, xs2[1:]):
        arrow(ax, (a - bw / 2 - 0.06, bottom), (b + bw / 2 + 0.06, bottom),
              colour=ORANGE, lw=1.5, scale=12)

    # both answers are drawn, because the no branch is the one a reader
    # misreads, and what it does not prove is said in the caption
    for dy, text, colour in ((0.80, "a mark", GREEN), (-0.80, "no mark", GREY)):
        box(ax, 1.05, bottom + dy, 1.60, 0.58, fill=WHITE, edge=colour,
            lw=1.4, r=0.10)
        t = note(ax, 1.05, bottom + dy, text, size=9.2, colour=colour,
                 weight="bold")
        must_fit(fig, t, 1.44, text)
        inside(fig, t, text)
        arrow(ax, (xs2[2] - bw / 2 - 0.06, bottom + dy * 0.26),
              (1.05 + 0.80 + 0.06, bottom + dy), colour=colour, lw=1.4,
              scale=11)

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig13_3.png")
