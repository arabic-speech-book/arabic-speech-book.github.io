"""
Figure 6.5: parameter-efficient adaptation of a frozen Transformer block.

Redrawn at the book's type scale. The original showed the block with two orange
labels attached to it and left "LoRA, low-rank A·B" to carry the whole
explanation; a reader who did not already know what a low-rank update was
learned nothing from it. Here the two inserts are opened up on the right: the
adapter as a down-projection, a nonlinearity and an up-projection back to the
same width, and LoRA as a pair of thin matrices whose product is added to the
frozen weight. The shared point, that the trainable part is small because it is
narrow, is then visible in both, and the thin matrices are drawn thin.

Two accuracy fixes. The original drew LoRA looping out of and back into the
whole self-attention box; LoRA is applied to individual projection matrices
inside it, usually the query and the value, so the label now says so. And the
adapter was drawn hanging off the feed-forward box with no path through it;
here it is described as sitting in the path, before the residual addition,
which is where an adapter goes.
"""
from bookstyle import (NAVY, ORANGE, GREY, WHITE, canvas, box, title_in, note,
                       arrow, save)
from figscale import lws, arr

FROZEN = "#EDEDED"
FROZEN_EDGE = "#7A7A7A"
FROZEN_TEXT = "#4A4A4A"
PEACH = "#FCF1E8"

BX, BW, RH = 3.05, 4.10, 0.84
ROWS = [("multi-head self-attention", 6.50),
        ("add and norm", 5.26),
        ("feed-forward", 4.02),
        ("add and norm", 2.78)]

PX, PW = 9.15, 6.50          # panel centre and width
PH = 2.20


def draw(path_out):
    fig, ax = canvas(12.6, 8.2, (0, 12.6), (0, 8.2))

    # ---- the frozen block
    note(ax, BX, 7.55, "one Transformer block, weights frozen",
         size=10.0, colour=GREY, weight="bold", style="italic")

    for label, y in ROWS:
        box(ax, BX, y, BW, RH, fill=FROZEN, edge=FROZEN_EDGE, lw=1.5, r=0.10)
        title_in(ax, BX, y, label, size=10.4, colour=FROZEN_TEXT)

    arrow(ax, (BX, 7.24), (BX, 6.96), colour=GREY, lw=1.6, scale=13)
    for i in range(len(ROWS) - 1):
        arrow(ax, (BX, ROWS[i][1] - RH / 2), (BX, ROWS[i + 1][1] + RH / 2 + 0.02),
              colour=GREY, lw=1.6, scale=13)
    arrow(ax, (BX, 2.36), (BX, 2.08), colour=GREY, lw=1.6, scale=13)

    # ---- LoRA
    box(ax, PX, 6.50, PW, PH, fill=PEACH, edge=ORANGE, lw=1.6, r=0.10)
    note(ax, 6.10, 7.22, "LoRA", size=11.0, ha="left", colour=ORANGE,
         weight="bold")
    note(ax, 7.00, 7.22, "a low-rank update added to a frozen weight matrix",
         size=8.0, ha="left", colour=ORANGE)

    box(ax, 6.55, 6.50, 0.92, 0.92, fill=FROZEN, edge=FROZEN_EDGE, lw=1.4,
        r=0.05)
    title_in(ax, 6.55, 6.50, "W", size=10.4, colour=FROZEN_TEXT)
    note(ax, 7.28, 6.50, "+", size=12.0, colour=ORANGE, weight="bold")
    box(ax, 7.72, 6.50, 0.26, 0.92, fill=WHITE, edge=ORANGE, lw=1.4, r=0.04)
    title_in(ax, 7.72, 6.50, "B", size=10.0, colour=ORANGE)
    note(ax, 8.02, 6.50, "·", size=12.0, colour=ORANGE, weight="bold")
    box(ax, 8.55, 6.50, 0.92, 0.26, fill=WHITE, edge=ORANGE, lw=1.4, r=0.04)
    title_in(ax, 8.55, 6.50, "A", size=10.0, colour=ORANGE)

    note(ax, 11.90, 6.50, "trainable:\nusually well under\n1% of the weights",
         size=9.0, ha="right", colour=ORANGE, weight="bold", linespacing=1.6)
    note(ax, PX, 5.82,
         "W is frozen; B and A are thin, of rank r much smaller than d",
         size=8.6, colour=GREY)

    arrow(ax, (BX + BW / 2 + 0.04, 6.50), (PX - PW / 2 - 0.04, 6.50),
          lw=1.6, scale=13)

    # ---- adapter
    box(ax, PX, 4.02, PW, PH, fill=PEACH, edge=ORANGE, lw=1.6, r=0.10)
    note(ax, 6.10, 4.74, "adapter", size=11.0, ha="left", colour=ORANGE,
         weight="bold")
    note(ax, 7.30, 4.74, "a small bottleneck inserted in the frozen path",
         size=8.0, ha="left", colour=ORANGE)

    box(ax, 6.55, 4.02, 1.06, 0.80, fill=WHITE, edge=ORANGE, lw=1.4, r=0.06)
    title_in(ax, 6.55, 4.02, "down", size=9.4, colour=ORANGE)
    arrow(ax, (7.12, 4.02), (7.38, 4.02), lw=1.5, scale=12)
    box(ax, 7.94, 4.02, 1.06, 0.80, fill=WHITE, edge=ORANGE, lw=1.4, r=0.06)
    title_in(ax, 7.94, 4.02, "nonlin.", size=9.4, colour=ORANGE)
    arrow(ax, (8.51, 4.02), (8.77, 4.02), lw=1.5, scale=12)
    box(ax, 9.33, 4.02, 1.06, 0.80, fill=WHITE, edge=ORANGE, lw=1.4, r=0.06)
    title_in(ax, 9.33, 4.02, "up", size=9.4, colour=ORANGE)

    note(ax, 11.90, 4.02, "trainable:\nabout 1 to 5%\nof the weights",
         size=9.0, ha="right", colour=ORANGE, weight="bold", linespacing=1.6)
    note(ax, 7.94, 3.34, "wide in, narrow in the middle, wide out again",
         size=8.6, colour=GREY)

    arrow(ax, (BX + BW / 2 + 0.04, 4.02), (PX - PW / 2 - 0.04, 4.02),
          lw=1.6, scale=13)

    note(ax, 0.28, 1.86,
         "Grey is frozen and orange is trained. Because the backbone never "
         "changes, one shared copy of it can serve many Arabic dialects and "
         "tasks: each\n"
         "dialect needs only its own small set of orange weights, a few "
         "megabytes rather than a few gigabytes, and a dialect with a handful "
         "of labeled hours\n"
         "can be fitted without the overfitting that full fine-tuning would "
         "invite.",
         size=9.2, ha="left", va="top", colour=NAVY, linespacing=1.7)

    save(fig, path_out)


if __name__ == "__main__":
    draw("fig6_5.png")
