"""
Figure 4.4: the HCLG composition.

Redrawn from the author's artwork. Her version printed its labels at about
3 pt, and the caption line inside each transducer box overlapped the little
state chain drawn beneath it. The content is unchanged apart from that
separation, the composition operator being named rather than left as a small
ring, and the vowel being written /aː/ as the chapter text writes it.
"""
from matplotlib.patches import Circle

from ch4style import (NAVY, ORANGE, GREY, BOXFILL, ARF, canvas, box,
                      title_in, note, arrow, save, ar)
from figscale import fs, lws

BOX_W, BOX_H = 2.60, 2.05
Y_ROW = 6.05
CENTRES = [1.60, 4.75, 7.90, 11.05]
PARTS = [("H", "HMM states → triphones"),
         ("C", "triphones → phones"),
         ("L", "phones → words"),
         ("G", "word n-gram model")]


def mini_chain(ax, cx, cy, n=3, r=0.13, pitch=0.52):
    xs = [cx + (i - (n - 1) / 2) * pitch for i in range(n)]
    ax.plot([xs[0], xs[-1]], [cy, cy], color=GREY, lw=lws(1.1), zorder=3)
    for x in xs:
        ax.add_patch(Circle((x, cy), r, facecolor="white", edgecolor=GREY,
                            lw=lws(1.1), zorder=4))


def draw(path):
    fig, ax = canvas(12.6, 5.9, (0.20, 12.40), (1.05, 7.30))

    for (letter, caption), cx in zip(PARTS, CENTRES):
        box(ax, cx, Y_ROW, BOX_W, BOX_H)
        title_in(ax, cx, Y_ROW + 0.62, letter, size=15.0)
        note(ax, cx, Y_ROW + 0.14, caption, size=8.8, colour=NAVY)
        mini_chain(ax, cx, Y_ROW - 0.50)

    # the composition operator
    for a, b in zip(CENTRES[:-1], CENTRES[1:]):
        ax.text((a + b) / 2, Y_ROW, "∘", ha="center", va="center",
                fontsize=fs(16.0), color=ORANGE, weight="bold", zorder=5)
    note(ax, 3.05, 4.58, "∘ joins two transducers into one", size=9.4,
         colour=ORANGE, style="italic")

    # what L does, on one word
    note(ax, 8.30, 4.58, "/b aː b/  →", size=10.0, colour=NAVY, ha="right")
    ax.text(8.46, 4.60, ar("باب"), ha="left", va="center", fontproperties=ARF,
            fontsize=fs(13.0), color=NAVY, zorder=5)
    note(ax, 8.72, 4.16, "(bāb, ‘door’)", size=9.2)

    # composing the four
    arrow(ax, (6.30, 4.95), (6.30, 3.05), lw=2.2, scale=17)
    note(ax, 6.08, 3.62, "determinize + minimize", size=9.4, ha="right",
         style="italic")

    box(ax, 6.30, 2.05, 6.60, 1.65, fill=BOXFILL)
    title_in(ax, 6.30, 2.32, "HCLG: one static decoding graph", size=12.6)
    note(ax, 6.30, 1.72, "beam search walks it at runtime", size=9.8)

    save(fig, path)


if __name__ == "__main__":
    draw("fig4_4.png")
