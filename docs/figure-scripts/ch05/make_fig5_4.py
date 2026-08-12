"""
Figure 5.4: hybrid CTC/attention.

Drawn from the author's specification: one shared encoder feeding a CTC head
and an attention decoder head, with the training loss and the decoding rule
given as label strips rather than typeset equations.
"""
from bookstyle import (NAVY, ORANGE, GREY, BOXFILL, canvas, box, title_in,
                       note, arrow, save)
from figscale import fs, lws

CX = 6.30


def draw(path_out):
    fig, ax = canvas(12.6, 6.4, (0.20, 12.45), (0.05, 7.05))

    # the shared encoder
    box(ax, CX, 1.55, 8.60, 1.10, fill=BOXFILL)
    title_in(ax, CX, 1.72, "Shared encoder (Conformer)", size=12.2)
    note(ax, CX, 1.24, "one set of frame representations, used by both heads",
         size=9.2)
    note(ax, CX, 0.52, "speech features", size=9.6, colour=NAVY)
    arrow(ax, (CX, 0.68), (CX, 0.98), lw=1.8)

    # the two heads
    for cx, title, sub in ((3.30, "CTC head", "monotonic, alignment-free"),
                           (9.30, "Attention decoder head", "soft alignment, global context")):
        box(ax, cx, 4.05, 4.90, 1.10)
        title_in(ax, cx, 4.22, title, size=12.0)
        note(ax, cx, 3.74, sub, size=9.2)
        arrow(ax, (cx, 2.12), (cx, 3.48), lw=1.9)

    # what the two heads are for, as label strips
    box(ax, CX, 5.55, 9.60, 0.72, fill="#FDF2E9", edge=ORANGE, lw=1.4)
    note(ax, CX, 5.55,
         "training loss  =  lambda × CTC loss  +  (1 − lambda) × attention loss",
         size=10.2, colour=ORANGE, weight="bold")
    box(ax, CX, 6.55, 9.60, 0.72, fill="#FDF2E9", edge=ORANGE, lw=1.4)
    note(ax, CX, 6.55, "decoding  =  score every candidate with both heads",
         size=10.2, colour=ORANGE, weight="bold")
    for cx in (3.30, 9.30):
        arrow(ax, (cx, 4.62), (cx, 5.16), lw=1.6, scale=13)

    note(ax, CX, 2.85,
         "The monotonic head keeps the attention head\n"
         "from wandering; the attention head supplies\n"
         "the global context.",
         size=9.2, colour=GREY, style="italic", linespacing=1.6)

    save(fig, path_out)


if __name__ == "__main__":
    draw("fig5_4.png")
