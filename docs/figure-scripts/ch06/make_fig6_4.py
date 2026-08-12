"""
Figure 6.4: what a frozen representation encodes, layer by layer.

Redrawn at the book's type scale, and with the two things the original chart
did not say made explicit. First, the numbers are illustrative, and the figure
now says so inside the artwork rather than only in the caption, so the shape
cannot be quoted as a measurement. Second, the two curves are told apart by
marker shape and by a label written at the curve, not by colour alone, which is
what a greyscale printing needs.

The shape follows the layer-wise probing literature on self-supervised speech
encoders: speaker and channel detail is strongest in the early layers, phonetic
information peaks around two thirds of the way up, and the top layers drift
toward whatever the pretraining objective rewards. The vertical axis is left
unnumbered for the same reason the curves are marked illustrative.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from bookstyle import NAVY, ORANGE, GREY, save
from figscale import fs, lws, ms

LAYERS = list(range(1, 13))
SPEAKER = [.88, .90, .87, .82, .75, .68, .61, .55, .50, .47, .45, .44]
PHONE = [.42, .48, .56, .65, .74, .82, .88, .90, .86, .79, .72, .68]


def draw(path_out):
    fig = plt.figure(figsize=(12.6, 7.0))
    ax = fig.add_axes([0.075, 0.255, 0.905, 0.705])

    ax.plot(LAYERS, SPEAKER, color=NAVY, lw=lws(2.0), marker="o",
            markersize=ms(4.0) ** 0.5 * 2.2, markerfacecolor="white",
            markeredgewidth=lws(1.6), zorder=4)
    ax.plot(LAYERS, PHONE, color=ORANGE, lw=lws(2.0), marker="s",
            markersize=ms(4.0) ** 0.5 * 2.2, markerfacecolor="white",
            markeredgewidth=lws(1.6), zorder=4)

    ax.annotate("phonetic information\n(squares)", xy=(9.0, .79),
                xytext=(12.5, 1.14), fontsize=fs(10.0), color=ORANGE,
                weight="bold", ha="right", va="top", linespacing=1.6,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=lws(1.2),
                                connectionstyle="arc3,rad=0.25",
                                shrinkA=8, shrinkB=6))
    ax.annotate("speaker information\n(circles)", xy=(11.0, .455),
                xytext=(12.5, .30), fontsize=fs(10.0), color=NAVY,
                weight="bold", ha="right", va="top", linespacing=1.6,
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=lws(1.2),
                                connectionstyle="arc3,rad=-0.25",
                                shrinkA=8, shrinkB=6))

    ax.set_xlim(0.4, 12.7)
    ax.set_ylim(0.10, 1.18)
    ax.set_xticks(LAYERS)
    ax.set_yticks([])
    ax.tick_params(axis="x", labelsize=fs(9.6), colors=NAVY,
                   width=lws(1.2), length=6 * 1.7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(NAVY)
        ax.spines[s].set_linewidth(lws(1.4))

    ax.set_xlabel("encoder layer, shallow to deep", fontsize=fs(10.4),
                  color=NAVY, weight="bold", labelpad=8 * 1.7)
    ax.set_ylabel("probing accuracy", fontsize=fs(10.4), color=NAVY,
                  weight="bold", labelpad=10 * 1.7)

    ax.text(0.55, 1.15, "illustrative shape, not measured values",
            fontsize=fs(9.4), color=GREY, style="italic", ha="left",
            va="top")
    fig.text(0.075, 0.115,
             "A light probe is trained on one frozen layer at a time, and "
             "the higher its accuracy the more readily that layer gives up "
             "the property.\nWhich layer to tap therefore depends on the "
             "task, which is why an Arabic phonetic or dialect probe is worth "
             "running before choosing one.",
             fontsize=fs(9.2), color=NAVY, va="top", linespacing=1.7)

    save(fig, path_out)


if __name__ == "__main__":
    draw("fig6_4.png")
