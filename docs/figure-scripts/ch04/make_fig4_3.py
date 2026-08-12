"""
Figure 4.3: a left-to-right HMM for باب (bāb, 'door').

Redrawn from the author's artwork for legibility: her version printed its state
labels at about 3 pt. The content is unchanged, with one correction: the vowel
is written /aː/ with the IPA length mark, as the chapter text writes it, rather
than /a:/ with a colon.
"""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch

from ch4style import (NAVY, ORANGE, GREY, BOXFILL, ARF, canvas, title_in,
                      note, arrow, save, ar)
from figscale import fs, lws, arr

R = 0.40
Y = 2.55
GROUPS = [("/b/", [1.05, 2.35, 3.65]),
          ("/aː/", [5.10, 6.40, 7.70]),
          ("/b/", [9.15, 10.45, 11.75])]


def self_loop(ax, cx, cy):
    """The self-loop: the state can repeat, which is how the model absorbs
    duration."""
    p = FancyArrowPatch((cx - 0.15, cy + R - 0.02), (cx + 0.15, cy + R - 0.02),
                        connectionstyle="arc3,rad=-2.2", arrowstyle="-|>",
                        mutation_scale=arr(11), lw=lws(1.5), color=NAVY,
                        zorder=5)
    ax.add_patch(p)


def gaussian_mixture(ax, cx, cy):
    """Three bell curves standing for the Gaussian mixture at one state."""
    xs = np.linspace(-1.5, 1.5, 400)
    for shift, scale, colour in ((-0.55, 0.42, "#2E75B6"),
                                 (0.00, 0.34, NAVY),
                                 (0.52, 0.46, ORANGE)):
        ys = np.exp(-0.5 * ((xs - shift) / scale) ** 2)
        ax.plot(cx + xs * 0.62, cy + ys * 0.44, color=colour, lw=lws(1.5),
                zorder=4)


def draw(path):
    fig, ax = canvas(12.6, 5.6, (0.30, 12.50), (0.35, 6.25))

    # the word the chain spells
    ax.text(6.40, 5.92, ar("باب"), ha="center", va="center",
            fontproperties=ARF, fontsize=fs(17.0), color=NAVY, zorder=5)
    note(ax, 6.40, 5.48, "bāb ‘door’", size=10.0)

    # the emission distribution above one state
    note(ax, 6.40, 4.98, "Gaussian mixture over the feature space",
         size=9.6, colour=NAVY, weight="bold")
    gaussian_mixture(ax, 6.40, 4.20)
    ax.plot([6.40, 6.40], [4.16, Y + R], color=GREY, lw=lws(1.0), ls=(0, (3, 3)),
            zorder=2)

    xs_all = [x for _, g in GROUPS for x in g]

    # the forward arrows: the model advances one state at a time
    for a, b in zip(xs_all[:-1], xs_all[1:]):
        arrow(ax, (a + R + 0.04, Y), (b - R - 0.10, Y), lw=1.9, scale=15)

    for label, xs in GROUPS:
        for i, x in enumerate(xs):
            ax.add_patch(Circle((x, Y), R, facecolor=BOXFILL, edgecolor=NAVY,
                                lw=lws(1.7), zorder=3))
            title_in(ax, x, Y, f"s{xs_all.index(x) + 1}", size=11.0)
            self_loop(ax, x, Y)
        # the phone this group of states belongs to
        ax.plot([xs[0] - R - 0.10, xs[-1] + R + 0.10], [Y - 1.02] * 2,
                color=GREY, lw=lws(1.2), zorder=2)
        title_in(ax, (xs[0] + xs[-1]) / 2, Y - 1.42, label, size=12.6)

    # the two moves, named
    note(ax, 1.05, Y + 1.22, "stay: one more frame\nin the same state",
         size=9.2, colour=NAVY, ha="center", va="bottom", linespacing=1.4)
    ax.plot([1.05, 1.05], [Y + 1.16, Y + R + 0.34], color=NAVY, lw=lws(1.0),
            ls=(0, (3, 3)), zorder=2)
    note(ax, 3.00, Y - 0.46, "advance", size=9.2, colour=ORANGE,
         style="italic")

    save(fig, path)


if __name__ == "__main__":
    draw("fig4_3.png")
