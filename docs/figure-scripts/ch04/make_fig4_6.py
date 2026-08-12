"""
Figure 4.6: one Conformer block.

Redrawn from the author's artwork, which printed its labels at about 4 pt.
One thing is corrected as well as retypeset. Her version ran a single dashed
line down the left of the stack that touched all five boxes, including the
final layer normalization, which reads as a residual connection around
LayerNorm; a Conformer block has residual connections around its four
modules, and the normalization at the end is not wrapped in one. Each
residual is now drawn as its own arc around its own module, so the picture
says what the architecture does.
"""
from matplotlib.patches import FancyArrowPatch

from ch4style import (NAVY, ORANGE, GREY, BOXFILL, canvas, box, title_in,
                      note, arrow, save)
from figscale import lws, arr

CX = 6.40
BOX_W = 9.00
GAP = 0.45
TOP_EDGE = 7.90

# (label, what it contributes, box height, residual?)
STACK = [("Feed-forward (half-step)", None, 0.85, True),
         ("Multi-head self-attention", "every frame attends to every frame",
          1.15, True),
         ("Convolution module", "local detail: formant slopes and bursts",
          1.15, True),
         ("Feed-forward (half-step)", None, 0.85, True),
         ("Layer normalization", None, 0.85, False)]


def residual(ax, y, h):
    """One skip connection: the module's output is added to its input."""
    x = CX - BOX_W / 2 - 0.02
    ax.add_patch(FancyArrowPatch(
        (x, y + h / 2 + 0.24), (x, y - h / 2 - 0.24),
        connectionstyle="arc3,rad=0.55", arrowstyle="-|>",
        mutation_scale=arr(12), lw=lws(1.4), color=ORANGE,
        linestyle=(0, (4, 3)), zorder=4))


def draw(path):
    fig, ax = canvas(12.6, 8.8, (0.30, 12.50), (-0.15, 8.35))

    ys, edge = [], TOP_EDGE
    for _, _, h, _ in STACK:
        ys.append(edge - h / 2)
        edge -= h + GAP

    note(ax, CX - 0.18, 8.08, "input features", size=10.0, colour=NAVY,
         ha="right")
    arrow(ax, (CX, 8.28), (CX, TOP_EDGE + 0.02), colour=NAVY, lw=1.7)

    for i, (label, side, h, skip) in enumerate(STACK):
        y = ys[i]
        last = i == len(STACK) - 1
        box(ax, CX, y, BOX_W, h, fill="white" if last else BOXFILL)
        title_in(ax, CX, y + (0.20 if side else 0.0), label, size=11.6)
        if side:
            note(ax, CX, y - 0.26, side, size=9.2, style="italic")
        if skip:
            residual(ax, y, h)
        if not last:
            arrow(ax, (CX, y - h / 2 - 0.02),
                  (CX, ys[i + 1] + STACK[i + 1][2] / 2 + 0.02),
                  colour=NAVY, lw=1.7)

    y_last = ys[-1] - STACK[-1][2] / 2
    arrow(ax, (CX, y_last - 0.02), (CX, y_last - 0.40), colour=NAVY, lw=1.7)
    note(ax, CX, y_last - 0.50, "output", size=10.0, colour=NAVY, va="top")

    note(ax, CX, 0.02,
         "The dashed orange arcs are residual connections: each module’s input "
         "is added to its output.\nThe layer normalization at the end is not "
         "wrapped in one.",
         size=9.2, colour=ORANGE, style="italic", va="top", linespacing=1.5)

    save(fig, path)


if __name__ == "__main__":
    draw("fig4_6.png")
