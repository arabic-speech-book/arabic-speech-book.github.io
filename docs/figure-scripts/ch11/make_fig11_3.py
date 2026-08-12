"""Figure 11.3: the three parts, their sizes, and what flows between them.

The author specified this one: a left-to-right pipeline of audio encoder,
connector and language model, with each block's input and output named, the
relative sizes carrying the argument, and the representation at every stage
made explicit rather than left to the prose.

Four things the drawing has to do that a row of equal boxes would not:

The sizes are the argument. The connector is the smallest box on the page and
the language model the largest, because the piece that is trained is the piece
that is nearly invisible, and a reader who takes only one thing from Section
11.2 should take that.

The reduction is drawn rather than asserted. Twenty-four thin marks go into the
connector and six wide ones come out, which is the four-to-one of Figure 11.2
made visible at the point where it happens.

Frozen and trained are told apart by more than a word. The two borrowed blocks
are drawn in navy on a pale fill with a dashed edge; the trained one is solid
orange. The dash is the convention this book already uses for a thing that is
held fixed.

Generation is vertical. The tokens leave the language model one at a time down
the right-hand side, because a row of tokens side by side is a picture of a
sequence that already exists, and the point is that it does not.

Every label is a label. What the picture means is in the caption.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

# the reduction drawn between the second and third block
IN_MARKS = 24
OUT_MARKS = 6
TOKENS = ["token 1", "token 2", "token 3"]

BOUNDS = []


def inside(fig, artist, what):
    fig.canvas.draw()
    bb = artist.get_window_extent(fig.canvas.get_renderer())
    x0, x1 = bb.x0 / fig.dpi, bb.x1 / fig.dpi
    w_in = fig.get_size_inches()[0]
    if x0 < 0.04 or x1 > w_in - 0.04:
        BOUNDS.append(f'{what}: spans {x0:.2f} to {x1:.2f} in')
    return artist


def spectrogram(ax, cx, cy, w, h, cols=9, rows=6):
    """A spectrogram as a small block of cells, light where there is energy."""
    cw, ch = w / cols, h / rows
    weights = [0.15, 0.55, 0.85, 0.45, 0.20, 0.70, 0.95, 0.40, 0.25]
    for i in range(cols):
        for j in range(rows):
            v = weights[i] * (1.0 - 0.13 * j)
            v = max(0.05, min(0.92, v))
            ax.add_patch(__import__('matplotlib').patches.Rectangle(
                (cx - w / 2 + i * cw, cy - h / 2 + j * ch), cw, ch,
                facecolor=(1 - v * 0.72, 1 - v * 0.60, 1 - v * 0.30),
                edgecolor='none', zorder=3))
    ax.add_patch(__import__('matplotlib').patches.Rectangle(
        (cx - w / 2, cy - h / 2), w, h, facecolor='none', edgecolor=NAVY,
        lw=lws(1.2), zorder=4))


def marks(ax, x0, x1, cy, n, height, colour, lw=1.1):
    step = (x1 - x0) / n
    for i in range(n):
        x = x0 + step * (i + 0.5)
        ax.plot([x, x], [cy - height / 2, cy + height / 2], color=colour,
                lw=lws(lw), solid_capstyle='butt', zorder=4)


def wide_marks(ax, x0, x1, cy, n, height, colour):
    step = (x1 - x0) / n
    w = step * 0.62
    import matplotlib.patches as mp
    for i in range(n):
        x = x0 + step * (i + 0.5)
        ax.add_patch(mp.Rectangle((x - w / 2, cy - height / 2), w, height,
                                  facecolor=GREENFILL, edgecolor=GREEN,
                                  lw=lws(1.0), zorder=4))


def draw(path_out):
    w, h = 12.6, 5.60
    fig, ax = canvas(w, h, (0, w), (0, h))
    y = 3.55
    strip_label_y = 5.25

    # ---- the representation coming in ------------------------------------
    spectrogram(ax, 0.95, y, 1.25, 1.05)
    t = note(ax, 0.95, y - 0.86, "spectrogram", size=9.4, colour=NAVY)
    must_fit(fig, t, 1.80, "spectrogram")
    inside(fig, t, "spectrogram")

    # ---- block one, the audio encoder ------------------------------------
    e_x, e_w, e_h = 3.15, 2.80, 1.90
    box(ax, e_x, y, e_w, e_h, fill=BOXFILL, edge=NAVY, lw=1.6, r=0.12,
        ls=(0, (5, 3)))
    t = note(ax, e_x, y + 0.30, "Audio Encoder", size=11.4, colour=NAVY,
             weight="bold")
    must_fit(fig, t, e_w - 0.20, "Audio Encoder")
    t = note(ax, e_x, y - 0.22, "one vector every 20 ms", size=8.8,
             colour=NAVY)
    must_fit(fig, t, e_w - 0.14, "one vector every 20 ms")
    t = note(ax, e_x, y - e_h / 2 - 0.30, "borrowed, large, usually frozen",
             size=9.0, colour=GREY)
    must_fit(fig, t, 3.40, "encoder note")
    inside(fig, t, "encoder note")
    arrow(ax, (0.95 + 0.63 + 0.06, y), (e_x - e_w / 2 - 0.06, y), colour=GREY,
          lw=1.5, scale=12)

    # ---- the long sequence it produces -----------------------------------
    a0, a1 = e_x + e_w / 2 + 0.16, 5.90
    marks(ax, a0, a1, y, IN_MARKS, 0.72, NAVY)
    t = note(ax, (a0 + a1) / 2, strip_label_y, "audio vectors", size=9.2,
             colour=NAVY)
    must_fit(fig, t, 1.70, "audio vectors")
    ax.plot([(a0 + a1) / 2, (a0 + a1) / 2], [strip_label_y - 0.22, y + 0.44],
            color=EDGE_LIGHT, lw=lws(1.1), zorder=2)

    # ---- block two, the connector ----------------------------------------
    c_x, c_w, c_h = 6.72, 1.52, 1.06
    box(ax, c_x, y, c_w, c_h, fill=WHITE, edge=ORANGE, lw=2.0, r=0.10)
    t = note(ax, c_x, y, "Connector", size=9.6, colour=ORANGE, weight="bold")
    must_fit(fig, t, c_w - 0.10, "Connector")
    t = note(ax, c_x - 0.32, y - c_h / 2 - 0.58, "smallest, always trained",
             size=9.0, colour=ORANGE, weight="bold")
    must_fit(fig, t, 3.10, "connector note")
    inside(fig, t, "connector note")

    # ---- the short sequence that leaves ----------------------------------
    b0, b1 = c_x + c_w / 2 + 0.16, 8.06
    wide_marks(ax, b0, b1, y, OUT_MARKS, 0.72, GREEN)
    t = note(ax, (b0 + b1) / 2, strip_label_y, "fewer, in the model’s width",
             size=9.2, colour=GREEN)
    must_fit(fig, t, 3.10, "fewer embeddings")
    inside(fig, t, "fewer embeddings")
    ax.plot([(b0 + b1) / 2, (b0 + b1) / 2], [strip_label_y - 0.22, y + 0.44],
            color=EDGE_LIGHT, lw=lws(1.1), zorder=2)

    # ---- block three, the language model ---------------------------------
    m_x, m_w, m_h = 9.55, 2.76, 2.60
    box(ax, m_x, y, m_w, m_h, fill=BOXFILL, edge=NAVY, lw=1.6, r=0.12,
        ls=(0, (5, 3)))
    t = note(ax, m_x, y + 0.46, "Language Model", size=11.0, colour=NAVY,
             weight="bold")
    must_fit(fig, t, m_w - 0.20, "Language Model")
    t = note(ax, m_x, y - 0.12, "text, one token at a time", size=8.4,
             colour=NAVY)
    must_fit(fig, t, m_w - 0.16, "text, one token at a time")
    t = note(ax, m_x, y - m_h / 2 - 0.30, "borrowed, largest, usually frozen",
             size=9.0, colour=GREY)
    must_fit(fig, t, 3.60, "model note")
    inside(fig, t, "model note")

    # ---- the tokens, one at a time ---------------------------------------
    t_x, t_w, t_h = 11.86, 1.10, 0.46
    ys = [y + 0.86, y + 0.14, y - 0.58]
    arrow(ax, (m_x + m_w / 2 + 0.05, y + 0.86), (t_x - t_w / 2 - 0.05, ys[0]),
          colour=GREY, lw=1.4, scale=11)
    for i, (ty, label) in enumerate(zip(ys, TOKENS)):
        box(ax, t_x, ty, t_w, t_h, fill=GREENFILL, edge=GREEN, lw=1.2, r=0.08)
        t = note(ax, t_x, ty, label, size=8.8, colour=GREEN)
        must_fit(fig, t, t_w - 0.10, label)
        inside(fig, t, label)
        if i:
            arrow(ax, (t_x, ys[i - 1] - t_h / 2 - 0.03),
                  (t_x, ty + t_h / 2 + 0.03), colour=GREEN, lw=1.2, scale=10)
    t = note(ax, t_x, ys[2] - 0.46, "and so on", size=8.8, colour=GREY)
    must_fit(fig, t, 1.30, "and so on")
    inside(fig, t, "and so on")

    # ---- the four representations, named on one line ---------------------
    ax.plot([0.30, 12.30], [1.05, 1.05], color=EDGE_LIGHT, lw=lws(1.4),
            zorder=2)
    stages = [(1.20, "spectrogram", NAVY), (4.80, "audio vectors", NAVY),
              (8.40, "fewer embeddings", GREEN), (11.65, "text tokens", GREEN)]
    for x, label, colour in stages:
        t = note(ax, x, 0.60, label, size=9.4, colour=colour)
        must_fit(fig, t, 2.10, label)
        inside(fig, t, label)
    for (x0, _, _), (x1, _, _) in zip(stages, stages[1:]):
        arrow(ax, (x0 + 1.12, 0.60), (x1 - 1.12, 0.60), colour=GREY, lw=1.2,
              scale=10)

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig11_3.png")
