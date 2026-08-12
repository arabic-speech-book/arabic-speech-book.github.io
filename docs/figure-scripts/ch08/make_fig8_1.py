"""
Figure 8.1: the Arabic dialect continuum, and where the confusions fall.

The illustrator specification asked for seven labelled nodes with a
double-headed arrow between neighbours, each arrow labelled "most confusable".
Seven copies of the same words is not information, and the reader is left to
take the claim on trust.

This version places the groups on their real geography, west to east and north
to south, and draws an edge only between groups that actually border one
another. Distance on the page is therefore geographic distance, which is the
whole content of the word "continuum": neighbours are close because they are
close.

No sentences inside the artwork. What is left is the group names, the two axis
words that say what the layout means, and the legend distinguishing a shared
border from a distant pair.

The layout is a schematic, not a map, and the caption says so. The positions
are approximate centroids of where each group is spoken, normalised into the
frame; the adjacency list is the set of pairs whose regions share a land
border or a short sea crossing.
"""
import numpy as np
from bookstyle import (NAVY, ORANGE, GREY, WHITE, BOXFILL, canvas, box, note,
                       save)
from figscale import fs, lws, ms
from figfit import must_fit, report

# group -> (west-to-east, south-to-north), schematic, roughly geographic
NODES = {
    "Maghrebi":  (0.06, 0.62),
    "Egyptian":  (0.40, 0.55),
    "Sudanese":  (0.44, 0.16),
    "Levantine": (0.55, 0.88),
    "Iraqi":     (0.85, 0.84),
    "Gulf":      (0.90, 0.50),
    "Yemeni":    (0.72, 0.10),
}

# pairs whose regions share a border or a short sea crossing
EDGES = [("Maghrebi", "Egyptian"), ("Egyptian", "Sudanese"),
         ("Egyptian", "Levantine"), ("Levantine", "Iraqi"),
         ("Iraqi", "Gulf"), ("Gulf", "Yemeni"), ("Yemeni", "Sudanese"),
         ("Sudanese", "Gulf")]

# one distant pair, drawn faint, so the contrast is visible rather than asserted
DISTANT = ("Maghrebi", "Gulf")

BW, BH = 1.88, 0.72


def draw(path_out):
    w, h = 12.6, 6.0
    fig, ax = canvas(w, h, (0, w), (0, h))

    x0, x1 = 1.55, w - 1.35
    y0, y1 = 1.15, h - 1.05

    def P(name):
        fx, fy = NODES[name]
        return x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)

    # the distant pair is drawn as an arc beneath the graph, so it cannot be
    # mistaken for an edge through the groups it passes
    ax.annotate("", xy=P(DISTANT[1]), xytext=P(DISTANT[0]),
                arrowprops=dict(arrowstyle="-", color="#B9C7DC",
                                lw=lws(1.6), linestyle=(0, (6, 4)),
                                connectionstyle="arc3,rad=0.42",
                                shrinkA=40, shrinkB=40), zorder=2)

    for a, b in EDGES:
        (ax_, ay), (bx, by) = P(a), P(b)
        ax.plot([ax_, bx], [ay, by], color=ORANGE, lw=lws(1.9), zorder=3,
                solid_capstyle="round")

    for name in NODES:
        cx, cy = P(name)
        box(ax, cx, cy, BW, BH, fill=BOXFILL, edge=NAVY, lw=1.5, r=0.14, z=5)
        t = note(ax, cx, cy, name, size=10.0, colour=NAVY, weight="bold", z=6)
        must_fit(fig, t, BW - 0.16, name)

    # the two words that say what the layout means
    ax.annotate("", xy=(x1 + 0.62, y0 - 0.72), xytext=(x0 - 0.62, y0 - 0.72),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=lws(1.2),
                                mutation_scale=13, shrinkA=0, shrinkB=0),
                zorder=3)
    note(ax, x0 - 0.62, y0 - 0.94, "west", size=9.4, colour=GREY, ha="left")
    note(ax, x1 + 0.62, y0 - 0.94, "east", size=9.4, colour=GREY, ha="right")

    # legend: a line style each, no sentence
    lx, ly = 0.42, h - 0.34
    ax.plot([lx, lx + 0.62], [ly, ly], color=ORANGE, lw=lws(1.9),
            solid_capstyle="round", zorder=4)
    t = note(ax, lx + 0.74, ly, "shares a border", size=9.4, colour=GREY,
             ha="left")
    must_fit(fig, t, 2.4, "shares a border")
    ax.plot([lx + 3.30, lx + 3.92], [ly, ly], color="#C9D6E8", lw=lws(1.6),
            linestyle=(0, (6, 4)), zorder=4)
    t = note(ax, lx + 4.04, ly, "distant pair", size=9.4, colour=GREY,
             ha="left")
    must_fit(fig, t, 2.4, "distant pair")

    report()
    save(fig, path_out)
    print("wrote", path_out)


if __name__ == "__main__":
    draw("fig8_1.png")
