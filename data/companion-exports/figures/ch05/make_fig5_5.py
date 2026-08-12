"""
Figure 5.5: the effect of the language-model fusion weight.

The curve is illustrative, as the caption says, and the script says so too: the
values are invented to show the shape of the trade-off, not measured. It is
drawn from a smooth function rather than hand-placed points so the minimum and
the two rising arms are consistent with each other, and the y axis is left
unnumbered so no reader can mistake it for a result.
"""
import numpy as np

from bookstyle import NAVY, ORANGE, GREY, canvas, note, title_in, arrow, save
from figscale import fs, lws, arr

# an illustrative shape: a shallow bowl, steeper on the right, where too much
# trust in the language model costs more than too little
WEIGHTS = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
WER = np.array([24.0, 21.4, 19.6, 18.7, 18.4, 18.9, 20.4, 23.2, 27.4])


def draw(path_out):
    fig, ax = canvas(12.6, 6.6, (-0.12, 0.90), (11.0, 31.5))

    ax.plot([0, 0], [15.5, 29.5], color=NAVY, lw=lws(1.4), zorder=3)
    ax.plot([0, 0.86], [15.5, 15.5], color=NAVY, lw=lws(1.4), zorder=3)

    ax.plot(WEIGHTS, WER, color=ORANGE, lw=lws(2.4), zorder=4,
            solid_capstyle="round")
    ax.plot(WEIGHTS, WER, "o", color="white", markeredgecolor=ORANGE,
            markeredgewidth=lws(1.8), markersize=fs(4.6), zorder=5)

    k = int(np.argmin(WER))
    ax.plot([WEIGHTS[k]], [WER[k]], "o", color=ORANGE, markersize=fs(5.0),
            zorder=6)
    ax.plot([WEIGHTS[k], WEIGHTS[k]], [15.5, WER[k]], color=GREY,
            lw=lws(1.0), ls=(0, (3, 3)), zorder=2)
    note(ax, WEIGHTS[k], WER[k] - 1.35, "best weight", size=9.8, colour=ORANGE,
         weight="bold")

    note(ax, 0.43, 13.6,
         "language-model fusion weight, tuned on a development set "
         "(increasing to the right)", size=9.8, colour=NAVY, weight="bold")
    ax.text(-0.085, 22.5, "Word Error Rate (%)", ha="center", va="center",
            fontsize=fs(9.8), color=NAVY, weight="bold", rotation=90)

    note(ax, 0.045, 26.6, "no language model:\nthe text knowledge\nis unused",
         size=9.2, ha="left", colour=GREY, style="italic", linespacing=1.6)
    note(ax, 0.795, 29.3,
         "too much weight: the language model\noverrides the audio and the "
         "decoder writes\nfluent text that was never said",
         size=9.2, ha="right", colour=GREY, style="italic", linespacing=1.6)

    note(ax, 0.43, 12.2,
         "Illustrative shape, not measured values: the axis is deliberately "
         "left unnumbered.",
         size=9.0, colour=GREY, style="italic")

    save(fig, path_out)


if __name__ == "__main__":
    draw("fig5_5.png")
