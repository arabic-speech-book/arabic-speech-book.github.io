"""
Figure 5.2: the RNN-Transducer.

Drawn from the author's specification: an acoustic encoder and a prediction
network over the output history, both feeding a joint network that emits the
next token or a blank, with the emitted token fed back into the prediction
network.
"""
from matplotlib.patches import FancyArrowPatch

from bookstyle import (NAVY, ORANGE, GREY, BOXFILL, canvas, box, title_in,
                       note, arrow, save)
from figscale import fs, lws, arr

ENC = (3.15, 2.45, 4.60, 1.30)
PRD = (9.45, 2.45, 4.90, 1.30)
JNT = (6.30, 4.70, 4.40, 1.30)


def draw(path_out):
    fig, ax = canvas(12.6, 6.8, (0.25, 12.45), (0.05, 7.30))

    for (cx, cy, w, h), title, sub in (
            (ENC, "Encoder", "acoustic, for example a Conformer"),
            (PRD, "Prediction network", "a small language model over the tokens so far"),
            (JNT, "Joint network", "combines this frame with the history")):
        box(ax, cx, cy, w, h, fill=BOXFILL if (cx, cy, w, h) == JNT else "white")
        title_in(ax, cx, cy + 0.22, title, size=11.8)
        note(ax, cx, cy - 0.26, sub, size=9.0)

    # inputs
    for (cx, cy, w, h), label in ((ENC, "speech features"), (PRD, "previous tokens")):
        note(ax, cx, cy - h / 2 - 0.58, label, size=9.6, colour=NAVY)
        arrow(ax, (cx, cy - h / 2 - 0.44), (cx, cy - h / 2 - 0.04), lw=1.8)

    # into the joint network
    arrow(ax, (ENC[0] + 0.95, ENC[1] + ENC[3] / 2 + 0.04),
          (JNT[0] - 1.15, JNT[1] - JNT[3] / 2 - 0.04), lw=1.9)
    arrow(ax, (PRD[0] - 1.20, PRD[1] + PRD[3] / 2 + 0.04),
          (JNT[0] + 1.15, JNT[1] - JNT[3] / 2 - 0.04), lw=1.9)

    # output
    arrow(ax, (JNT[0], JNT[1] + JNT[3] / 2 + 0.04), (JNT[0], 6.28), lw=1.9)
    title_in(ax, JNT[0], 6.60, "P(next token or blank)", size=11.4)

    # the emitted token goes back into the prediction network
    ax.add_patch(FancyArrowPatch((JNT[0] + 1.85, 6.60), (PRD[0] + 1.10, PRD[1] + PRD[3] / 2 + 0.06),
                                 connectionstyle="arc3,rad=-0.42",
                                 arrowstyle="-|>", mutation_scale=arr(14),
                                 lw=lws(1.6), color=ORANGE,
                                 linestyle=(0, (4, 3)), zorder=4))
    note(ax, 12.35, 5.05, "the emitted token\nfeeds the history", size=9.2,
         ha="right", colour=ORANGE, style="italic", linespacing=1.5)

    note(ax, 6.30, 0.92,
         "Monotonic and streaming: at every step the model either emits a "
         "token or advances\none frame, and never moves back in time.",
         size=9.6, colour=NAVY, va="top", linespacing=1.6)

    save(fig, path_out)


if __name__ == "__main__":
    draw("fig5_2.png")
