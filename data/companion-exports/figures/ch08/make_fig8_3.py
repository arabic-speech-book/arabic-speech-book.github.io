"""
Figure 8.3: dialects in embedding space, and where they overlap.

The values are invented, so the axes carry no numbers and the panel says
"illustrative" inside the artwork, which is the one thing the book's figure
rules require to be written on the drawing rather than in the caption.

What is drawn is nonetheless generated rather than hand-placed: each cluster is
a two-dimensional Gaussian with a stated centre and spread, drawn with a fixed
seed, so the degree of overlap between two clusters is a consequence of the
numbers in CLUSTERS and can be changed by editing them. The overlaps follow the
continuum of Figure 8.1: Gulf and Levantine sit close and interpenetrate,
Egyptian touches both, Maghrebi sits apart from Gulf, and Modern Standard
Arabic is the most separable of the five because it is a register rather than a
region.

Clusters are distinguished by marker shape as well as colour and are labelled
directly, so the figure survives greyscale printing. The illustrator
specification asked for a caption strip along the bottom; that is a sentence
inside artwork and it has moved to the caption.
"""
import numpy as np
from bookstyle import NAVY, ORANGE, GREY, GREEN, WHITE, canvas, note, save
from figscale import fs, lws, ms
from figfit import must_fit, report

SEED = 9
N = 46

# name -> (centre x, centre y, spread x, spread y, correlation, marker, colour)
CLUSTERS = [
    ("MSA",       0.20, 0.80, 0.085, 0.075, 0.10, "o", NAVY),
    ("Levantine", 0.56, 0.60, 0.090, 0.080, 0.35, "D", ORANGE),
    ("Gulf",      0.70, 0.52, 0.095, 0.085, 0.30, "s", GREEN),
    ("Egyptian",  0.50, 0.40, 0.100, 0.085, -0.20, "^", GREY),
    ("Maghrebi",  0.20, 0.24, 0.085, 0.080, 0.05, "P", "#7B4FA3"),
]

# where each label sits relative to its centre, to keep it off the points
OFFSET = {"MSA": (-0.02, 0.17), "Levantine": (0.00, 0.18),
          "Gulf": (0.17, -0.02), "Egyptian": (-0.16, -0.10),
          "Maghrebi": (0.00, -0.17)}


def draw(path_out):
    w, h = 12.6, 6.4
    fig, ax = canvas(w, h, (0, w), (0, h))
    rng = np.random.default_rng(SEED)

    x0, y0 = 1.30, 0.95
    pw, ph = w - x0 - 0.60, h - y0 - 0.55

    ax.plot([x0, x0 + pw], [y0] * 2, color=NAVY, lw=lws(1.4), zorder=3)
    ax.plot([x0] * 2, [y0, y0 + ph], color=NAVY, lw=lws(1.4), zorder=3)

    def X(u):
        return x0 + u * pw

    def Y(v):
        return y0 + v * ph

    for name, cx, cy, sx, sy, rho, marker, colour in CLUSTERS:
        cov = [[sx ** 2, rho * sx * sy], [rho * sx * sy, sy ** 2]]
        pts = rng.multivariate_normal([cx, cy], cov, N)
        pts = np.clip(pts, 0.02, 0.98)   # keep every point inside the frame
        ax.scatter(X(pts[:, 0]), Y(pts[:, 1]), s=ms(15), marker=marker,
                   facecolor="none", edgecolor=colour, linewidth=lws(1.15),
                   zorder=4)
        dx, dy = OFFSET[name]
        t = note(ax, X(cx + dx), Y(cy + dy), name, size=10.4, colour=colour,
                 weight="bold", z=6,
                 bbox=dict(boxstyle="round,pad=0.16", facecolor="white",
                           edgecolor="none"))
        must_fit(fig, t, 2.4, name)

    note(ax, x0 + pw / 2, y0 - 0.44, "embedding dimension 1", size=9.4,
         colour=GREY)
    note(ax, x0 - 0.42, y0 + ph / 2, "embedding dimension 2", size=9.4,
         colour=GREY, rotation=90)
    note(ax, x0 + pw - 0.14, y0 + 0.22, "illustrative", size=9.8, colour=GREY,
         ha="right", style="italic")

    report()
    save(fig, path_out)
    print("wrote", path_out)


if __name__ == "__main__":
    draw("fig8_3.png")
