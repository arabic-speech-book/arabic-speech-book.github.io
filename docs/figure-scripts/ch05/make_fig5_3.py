"""
Figure 5.3: an attention-based encoder-decoder and its attention heatmap.

Drawn from the author's specification. The heatmap is generated, not sketched:
each column is a softmax over encoder frames whose peak advances steadily with
the output token, which is what a healthy, roughly monotonic alignment looks
like. Darker means more attention, and the grey scale carries a numeric bar so
the figure survives black-and-white printing.
"""
import numpy as np
from matplotlib.patches import Circle, Rectangle

from bookstyle import (NAVY, ORANGE, GREY, BOXFILL, ARF, canvas, box,
                       title_in, note, arrow, save, ar)
from figscale import fs, lws

TOKENS = ["m", "a", "d", "r", "a", "s", "a"]     # مدرسة, madrasa, 'school'
NFRAMES = 12


def attention():
    """A healthy alignment: each token attends to a band that moves forward."""
    w = np.zeros((len(TOKENS), NFRAMES))
    for i in range(len(TOKENS)):
        centre = (i + 0.5) * (NFRAMES - 1) / len(TOKENS)
        d = np.arange(NFRAMES) - centre
        w[i] = np.exp(-0.5 * (d / 1.15) ** 2)
        w[i] /= w[i].sum()
    return w


def draw(path_out):
    fig, ax = canvas(12.6, 7.0, (0.20, 12.45), (-0.85, 6.60))

    # ---- left: the architecture
    box(ax, 2.55, 2.05, 3.60, 0.90)
    title_in(ax, 2.55, 2.05, "Encoder", size=11.6)
    note(ax, 2.55, 1.28, "speech features", size=9.2, colour=NAVY)
    arrow(ax, (2.55, 1.44), (2.55, 1.56), lw=1.8, scale=13)

    xs = [1.20 + i * 0.55 for i in range(6)]
    for x in xs:
        ax.add_patch(Circle((x, 3.20), 0.20, facecolor=BOXFILL,
                            edgecolor=NAVY, lw=lws(1.3), zorder=3))
    note(ax, 4.65, 3.20, "frame states", size=9.2, ha="left", colour=NAVY)
    arrow(ax, (2.55, 2.52), (2.55, 2.96), lw=1.8, scale=13)

    box(ax, 2.55, 4.35, 3.60, 0.90, fill="#FDF2E9", edge=ORANGE)
    title_in(ax, 2.55, 4.35, "Attention", size=11.6, colour=ORANGE)
    for i, x in enumerate(xs):
        arrow(ax, (x, 3.42), (1.65 + 0.36 * i, 3.88), colour=ORANGE, lw=1.1,
              scale=9)

    box(ax, 2.55, 5.70, 3.60, 0.90)
    title_in(ax, 2.55, 5.70, "Decoder", size=11.6)
    arrow(ax, (2.55, 4.82), (2.55, 5.23), lw=1.8, scale=13)
    note(ax, 4.55, 5.70, "one token\nat a time", size=9.2, ha="left",
         colour=NAVY, linespacing=1.5)

    # ---- right: the attention weights
    W = attention()
    X0, Y0, CW, CH = 7.55, 5.60, 0.375, 0.52
    note(ax, X0, 6.42, "target:", size=9.6, ha="left", colour=NAVY,
         weight="bold")
    ax.text(X0 + 1.02, 6.44, ar("مدرسة"), ha="left", va="center",
            fontproperties=ARF, fontsize=fs(12.0), color=NAVY, zorder=5)
    note(ax, X0 + 2.00, 6.42, "(madrasa, ‘school’)", size=9.4, ha="left")
    note(ax, X0 + NFRAMES * CW / 2, 5.88, "encoder frames (time)", size=9.6,
         colour=NAVY, weight="bold")

    for i in range(len(TOKENS)):
        for j in range(NFRAMES):
            g = 1.0 - 0.88 * W[i, j] / W.max()
            ax.add_patch(Rectangle((X0 + j * CW, Y0 - (i + 1) * CH), CW, CH,
                                   facecolor=(g, g, g), edgecolor="#DCE4EE",
                                   lw=lws(0.5), zorder=3))
        note(ax, X0 - 0.16, Y0 - (i + 0.5) * CH, TOKENS[i], size=9.4,
             ha="right", colour=NAVY, weight="bold")
    ax.text(6.85, Y0 - len(TOKENS) * CH / 2, "output tokens", ha="center",
            va="center", fontsize=fs(9.6), color=NAVY, weight="bold",
            rotation=90)

    # grey-scale key
    ybar = Y0 - len(TOKENS) * CH - 0.58
    for k in range(6):
        g = 1.0 - 0.88 * k / 5
        ax.add_patch(Rectangle((X0 + k * 0.42, ybar), 0.42, 0.26,
                               facecolor=(g, g, g), edgecolor="#DCE4EE",
                               lw=lws(0.5), zorder=3))
    note(ax, X0 - 0.14, ybar + 0.13, "0", size=8.8, ha="right", colour=GREY)
    note(ax, X0 + 6 * 0.42 + 0.14, ybar + 0.13, "max", size=8.8, ha="left",
         colour=GREY)
    note(ax, X0 + NFRAMES * CW / 2, ybar - 0.30, "darker means more attention",
         size=9.0, colour=GREY, style="italic")

    note(ax, 6.30, 0.62,
         "The dark band runs roughly along the diagonal: each token attends "
         "near where the last one\nleft off. Looping and deletions show up as "
         "a broken or scattered band.",
         size=9.4, colour=NAVY, va="top", linespacing=1.6)

    save(fig, path_out)


if __name__ == "__main__":
    draw("fig5_3.png")
