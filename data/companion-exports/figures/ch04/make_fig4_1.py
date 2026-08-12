"""
Figure 4.1: the classical recognition pipeline.

Redrawn from the author's artwork. The content is hers: three knowledge
sources feeding a decoder, features entering from the left, an Arabic
transcript leaving at the bottom, and the argmax underneath. What changes is
the typography. Her version was drawn 2200 px wide and reproduced at 6.3 in,
which printed its labels at about 4 pt; here the type is pre-scaled so that
nothing prints below 7 pt, and the canvas is cropped to the drawing.
"""
from ch4style import (NAVY, GREEN, BOXFILL, GREENFILL, ARF, canvas, box,
                      title_in, note, arrow, save, ar)
from figscale import fs

TOP = [("Acoustic model", "P(X | W)", 3.55),
       ("Lexicon", "word → phones", 7.00),
       ("Language model", "P(W)", 10.45)]

BOX_W, BOX_H = 3.05, 1.15
Y_TOP = 8.05
Y_DEC = 5.85
Y_OUT = 3.35


def draw(path):
    fig, ax = canvas(12.6, 7.4, (0.15, 12.45), (1.30, 9.05))

    # the three knowledge sources
    for label, sub, cx in TOP:
        box(ax, cx, Y_TOP, BOX_W, BOX_H)
        title_in(ax, cx, Y_TOP + 0.20, label, size=11.6)
        note(ax, cx, Y_TOP - 0.24, sub, size=9.6)
        arrow(ax, (cx, Y_TOP - BOX_H / 2 - 0.04), (cx, Y_DEC + 0.62))

    # features entering from the left
    box(ax, 1.72, Y_DEC, 2.55, 1.15)
    title_in(ax, 1.72, Y_DEC + 0.16, "Features X", size=11.6)
    note(ax, 1.72, Y_DEC - 0.24, "(Chapter 3)", size=9.6, colour=NAVY)
    arrow(ax, (3.02, Y_DEC), (4.05, Y_DEC))

    # the decoder
    box(ax, 8.20, Y_DEC, 8.25, 1.20, fill=BOXFILL)
    title_in(ax, 8.20, Y_DEC, "Decoder: search for the best W", size=12.0)
    arrow(ax, (8.20, Y_DEC - 0.62), (8.20, Y_OUT + 0.88))

    # the transcript that comes out
    box(ax, 8.20, Y_OUT, 8.25, 1.55, fill=GREENFILL, edge=GREEN)
    ax.text(8.20, Y_OUT + 0.42, ar("وصل الوفد إلى عمان"), ha="center",
            va="center", fontproperties=ARF, fontsize=fs(15.0), color=NAVY,
            zorder=5)
    note(ax, 8.20, Y_OUT - 0.14, "wasala al-wafdu ila Amman", size=9.6)
    note(ax, 8.20, Y_OUT - 0.50, "‘the delegation arrived in Amman’", size=9.6)

    # the rule the picture is a drawing of
    title_in(ax, 8.20, 1.98, "W* = argmax P(X | W) · P(W)", size=12.6)
    note(ax, 8.20, 1.58,
         "acoustic model × language model, searched by the decoder",
         size=9.4, style="italic")

    save(fig, path)


if __name__ == "__main__":
    draw("fig4_1.png")
