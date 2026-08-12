"""
Figure 11.1: every architecture the book has built, and the one that replaces
the lot of them.

This is the diagram the author asked for in July and deferred until the
audio-language chapter, and Section 11.1 is the only place in the book where it
can be drawn, because it is the first point at which a reader has met all the
pieces. Drawn earlier it would be a preview of things not yet explained; drawn
here it is a summary of things already understood.

The argument is in the shape rather than in a sentence. Every architecture in
the top band is a fixed path: one kind of input, one model, one kind of output,
decided when the system was built. The band below has the same inputs and the
same outputs and one path between them, and what decides which output comes out
is an instruction arriving at run time. Nothing in the lower band can do
anything the upper band could not. What has moved is where the choice is made.

The internal stages of each architecture are deliberately not drawn. They are
the subject of the chapters named on the left, and repeating them here would
turn a map into a diagram of diagrams.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

# (chapter tag, input, model, output)
BUILT = [
    ("Chapters 4 to 6", "Arabic speech", "recognizer", "Arabic text"),
    ("Chapter 8", "Arabic speech", "dialect classifier", "a dialect label"),
    ("Chapter 9", "Arabic text", "synthesizer", "Arabic speech"),
    ("Chapter 10", "Arabic speech", "translation model", "English text"),
    ("Chapter 10", "Arabic speech", "understanding model", "intent and slots"),
]

OUTPUTS = ["Arabic text", "a dialect label", "Arabic speech", "English text",
           "intent and slots"]

CHAIN = ["Arabic speech", "audio encoder", "projector", "language model"]

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
    w, h = 12.6, 7.60
    fig, ax = canvas(w, h, (0, w), (0, h))

    # ---- the band of fixed paths ----------------------------------------
    t = note(ax, 0.10, 7.75, "one model per task", size=10.4, colour=NAVY,
             weight="bold", ha="left", va="center")
    must_fit(fig, t, 6.60, "band one")
    inside(fig, t, "band one")

    cols = [4.20, 7.65, 11.10]
    bw, bh = 2.90, 0.56
    ys = [7.05, 6.40, 5.75, 5.10, 4.45]
    for y, (tag, src, model, out) in zip(ys, BUILT):
        t = note(ax, 0.10, y, tag, size=9.0, colour=GREY, ha="left",
                 va="center")
        must_fit(fig, t, 1.75, tag)
        cells = [(src, BOXFILL, NAVY), (model, WHITE, NAVY),
                 (out, GREENFILL, GREEN)]
        for x, (text, fill, edge) in zip(cols, cells):
            box(ax, x, y, bw, bh, fill=fill, edge=edge, lw=1.3, r=0.10)
            t = note(ax, x, y, text, size=9.6, colour=edge)
            must_fit(fig, t, bw - 0.20, text)
        for a, b in zip(cols, cols[1:]):
            arrow(ax, (a + bw / 2 + 0.04, y), (b - bw / 2 - 0.04, y),
                  colour=GREY, lw=1.4, scale=11)

    ax.plot([0.10, 12.50], [3.97, 3.97], color=EDGE_LIGHT, lw=lws(1.4),
            zorder=2)

    # ---- the band with one path ------------------------------------------
    t = note(ax, 0.10, 3.73, "one model, many tasks", size=10.4, colour=ORANGE,
             weight="bold", ha="left", va="center")
    must_fit(fig, t, 9.10, "band two")
    inside(fig, t, "band two")

    y0 = 2.20
    cw, ch = 2.40, 0.66
    xs = [2.15, 4.85, 7.55, 10.25]
    for x, text in zip(xs, CHAIN):
        first = text == CHAIN[0]
        last = text == CHAIN[-1]
        box(ax, x, y0, cw, ch, fill=BOXFILL if first else WHITE,
            edge=ORANGE if last else NAVY, lw=1.6 if last else 1.3, r=0.10)
        t = note(ax, x, y0, text, size=9.6,
                 colour=ORANGE if last else NAVY,
                 weight="bold" if last else "normal")
        must_fit(fig, t, cw - 0.20, text)
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + cw / 2 + 0.04, y0), (b - cw / 2 - 0.04, y0),
              colour=GREY, lw=1.4, scale=11)

    # the instruction arrives at run time, into the language model
    iy = 3.07
    box(ax, xs[3], iy, cw, ch, fill=WHITE, edge=ORANGE, lw=1.4, r=0.10,
        ls=(0, (4, 3)))
    t = note(ax, xs[3], iy, "the instruction", size=9.6, colour=ORANGE)
    must_fit(fig, t, cw - 0.20, "the instruction")
    arrow(ax, (xs[3], iy - ch / 2 - 0.04), (xs[3], y0 + ch / 2 + 0.04),
          colour=ORANGE, lw=1.6, scale=12)

    # the same five outputs, now chosen rather than built in
    oy, ow = 0.63, 2.28
    ox = [1.42, 3.86, 6.30, 8.74, 11.18]
    for x, text in zip(ox, OUTPUTS):
        box(ax, x, oy, ow, 0.50, fill=GREENFILL, edge=GREEN, lw=1.3, r=0.10)
        t = note(ax, x, oy, text, size=9.4, colour=GREEN)
        must_fit(fig, t, ow - 0.18, text)
        arrow(ax, (xs[3], y0 - ch / 2 - 0.04), (x, oy + 0.25 + 0.04),
              colour=GREY, lw=1.2, scale=10)

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig11_1.png")
