"""
Figure 4.5: GMM-HMM against DNN-HMM.

Redrawn from the author's artwork, whose lettering printed at about 4 pt. The
content is unchanged: two identical stacks with one box different, and the
"posteriors divided by priors" step named inside the neural emission box. The
step is now also explained in the text of Section 4.5, which it was not
before.
"""
import numpy as np
from matplotlib.patches import Circle, Rectangle

from ch4style import (NAVY, ORANGE, GREY, BOXFILL, canvas, box, title_in,
                      note, save)
from figscale import fs, lws

COL = [3.30, 9.60]
BOX_W = 5.70
ROWS = [("Features", 7.55, 0.95),
        ("Emission (acoustic scores)", 5.85, 2.25),
        ("HMM states", 3.95, 0.95),
        ("HCLG graph", 2.70, 0.95),
        ("Text", 1.45, 0.95)]


def bells(ax, cx, cy):
    xs = np.linspace(-1.4, 1.4, 300)
    for shift in (-1.20, -0.40, 0.40, 1.20):
        ys = np.exp(-0.5 * ((xs) / 0.42) ** 2)
        ax.plot(cx + shift + xs * 0.40, cy + ys * 0.34, color=NAVY,
                lw=lws(1.3), zorder=5)


def network(ax, cx, cy):
    layers = []
    for dx, n in ((-0.62, 4), (0.00, 5), (0.62, 3)):
        layers.append([(cx + dx, cy + (i - (n - 1) / 2) * 0.26) for i in range(n)])
    for left, right in zip(layers[:-1], layers[1:]):
        for x0, y0 in left:
            for x1, y1 in right:
                ax.plot([x0, x1], [y0, y1], color="#A9BCD4", lw=lws(0.6),
                        zorder=4)
    for layer in layers:
        for x, y in layer:
            ax.add_patch(Circle((x, y), 0.075, facecolor="white",
                                edgecolor=NAVY, lw=lws(1.0), zorder=5))


def posteriors(ax, cx, cy):
    hs = [0.30, 0.52, 0.20, 0.44, 0.16]
    for i, h in enumerate(hs):
        ax.add_patch(Rectangle((cx + (i - 2) * 0.30 - 0.11, cy - 0.34), 0.22, h,
                               facecolor="#5A7BA8", edgecolor="none", zorder=5))


def draw(path):
    fig, ax = canvas(12.6, 6.6, (0.20, 12.70), (0.32, 8.80))

    title_in(ax, COL[0], 8.45, "GMM-HMM", size=13.0)
    title_in(ax, COL[1], 8.45, "DNN-HMM hybrid", size=13.0)

    for cx in COL:
        for label, cy, h in ROWS:
            emission = label.startswith("Emission")
            box(ax, cx, cy, BOX_W, h,
                fill="#FDF2E9" if emission else "white",
                edge=ORANGE if emission else NAVY, lw=1.7 if emission else 1.5)
            title_in(ax, cx, cy + (h / 2 - 0.28) if emission else cy, label,
                     size=11.2, colour=ORANGE if emission else NAVY)

    # what sits inside the emission box on each side
    bells(ax, COL[0], 5.62)
    note(ax, COL[0], 5.02, "one Gaussian mixture per state", size=9.2)

    network(ax, COL[1] - 1.55, 5.80)
    posteriors(ax, COL[1] + 1.35, 5.80)
    note(ax, COL[1], 5.02, "posteriors ÷ priors  →  scaled likelihoods",
         size=9.2)

    title_in(ax, 6.45, 0.62,
             "Only the emission box differs; the rest of the pipeline is "
             "identical.", size=10.6, colour=ORANGE)

    save(fig, path)


if __name__ == "__main__":
    draw("fig4_5.png")
