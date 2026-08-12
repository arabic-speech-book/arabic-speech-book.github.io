"""
Figure 6.3: the HuBERT cluster-mask-predict loop.

Redrawn at the book's type scale. The original arranged the four stages around
a circle, which spent most of a landscape frame on empty middle and left the
lettering at about 4 pt once reduced. The stages run left to right here, with
the return arrow beneath carrying the one thing the circle was there to say:
that the targets are re-derived from the improved model and the loop runs
again.

The first iteration's features are named, because "cluster speech features" is
ambiguous on its own: HuBERT clusters MFCCs on the first pass and the model's
own intermediate-layer features afterwards, which is exactly why the targets
improve.
"""
from bookstyle import (NAVY, ORANGE, GREY, BOXFILL, WHITE, canvas, box,
                       title_in, note, arrow, save)
from figscale import lws, arr

STAGES = [
    ("1  extract features",
     "from unlabeled audio;\nMFCCs on the\nfirst pass"),
    ("2  cluster (k-means)",
     "every frame gets a\ncluster id, a rough\nphonetic label"),
    ("3  mask and predict",
     "a Transformer predicts\nthe cluster id of the\nmasked frames"),
    ("4  re-cluster",
     "using features from\nthe improved model"),
]

BW, GAP, X0 = 2.76, 0.42, 0.28
CY = 4.34
BH = 2.06


def draw(path_out):
    fig, ax = canvas(12.6, 6.2, (0, 12.6), (0, 6.2))

    centres = []
    for i, (head, body) in enumerate(STAGES):
        cx = X0 + BW / 2 + i * (BW + GAP)
        centres.append(cx)
        box(ax, cx, CY, BW, BH, fill=BOXFILL if i != 2 else "#FBEDE2",
            edge=NAVY if i != 2 else ORANGE, lw=1.5, r=0.12)
        title_in(ax, cx, CY + 0.56, head, size=10.0,
                 colour=NAVY if i != 2 else ORANGE)
        note(ax, cx, CY - 0.28, body, size=9.0, colour=NAVY, linespacing=1.65)

    for i in range(3):
        x0 = centres[i] + BW / 2 + 0.04
        arrow(ax, (x0, CY), (x0 + GAP - 0.08, CY), lw=1.9, scale=15)

    # the loop: stage 4 supplies better targets to stage 2
    y_back = 2.44
    xa, xb = centres[3], centres[1]
    ax.plot([xa, xa], [CY - BH / 2, y_back], color=ORANGE, lw=lws(1.8), zorder=2)
    ax.plot([xa, xb], [y_back, y_back], color=ORANGE, lw=lws(1.8), zorder=2)
    ax.annotate("", xy=(xb, CY - BH / 2 - 0.02), xytext=(xb, y_back + 0.16),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=lws(1.8),
                                mutation_scale=arr(15), shrinkA=0, shrinkB=0),
                zorder=4)
    note(ax, (xa + xb) / 2, y_back - 0.34,
         "next iteration: the targets improve as the model does",
         size=9.6, colour=ORANGE, weight="bold")

    note(ax, 0.28, 1.46,
         "This is the masked language model idea of text models applied to "
         "units the model discovers for itself. Because the target is a "
         "discrete\n"
         "cluster identity rather than a choice among distractors, training is "
         "stable and needs none of the contrastive machinery of Figure 6.2.\n"
         "WavLM keeps the same objective and adds noise and overlapping speech "
         "to the input, so the representations learn to ignore interference.",
         size=9.2, ha="left", va="top", colour=NAVY, linespacing=1.7)

    save(fig, path_out)


if __name__ == "__main__":
    draw("fig6_3.png")
