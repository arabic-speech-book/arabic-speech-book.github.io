"""
Figure 6.1: the four ways a speech model can learn, ordered by labeling cost.

Redrawn at the book's type scale. The original printed at roughly 5 to 10 pt
across a 6.3 in column; here everything is drawn at twice final size so the
reduction lands on Springer's 7 pt floor or above.

Two changes of substance beyond the size. The original set the four cards on a
plain row, which left the reader to work out that the ordering meant anything;
the axis beneath now says what the ordering is, and the heading plates are
tinted from full to none so the amount of hand labeling is visible before a
word is read. The "example models" line also names the chapter section where
each family is developed, so the figure doubles as a map of the chapter.
"""
from bookstyle import (NAVY, ORANGE, GREY, WHITE, canvas, box, title_in, note,
                       save)
from figscale import lws, arr

# (heading, learns from, example models, section, plate fill)
COLS = [
    ("Supervised",
     "labeled audio and\ntext pairs only",
     "CTC and attention\nmodels (Chapters 4, 5)",
     "", "#C6D5EC"),
    ("Semi-supervised",
     "a few labels plus\npseudo-labeled audio",
     "self-training with\npseudo-labels",
     "Section 6.1", "#DAE4F3"),
    ("Self-supervised",
     "unlabeled audio and\na pretext task, then\nfine-tuning",
     "wav2vec 2.0, HuBERT,\nWavLM, MMS",
     "Sections 6.2 to 6.4", "#EBF1F9"),
    ("Weak supervision",
     "large amounts of\ncheap, noisy web labels",
     "Whisper",
     "Section 6.6", "#FFFFFF"),
]

CW, GAP, X0 = 2.83, 0.24, 0.32


def draw(path_out):
    fig, ax = canvas(12.6, 6.8, (0, 12.6), (0, 6.8))

    for i, (head, learns, models, sec, fill) in enumerate(COLS):
        cx = X0 + CW / 2 + i * (CW + GAP)

        box(ax, cx, 6.16, CW, 0.72, fill=fill, edge=NAVY, lw=1.5, r=0.10)
        title_in(ax, cx, 6.16, head, size=11.0)

        box(ax, cx, 3.86, CW, 3.76, fill=WHITE, edge=NAVY, lw=1.4, r=0.10)

        note(ax, cx, 5.30, "learns from", size=8.6, colour=ORANGE,
             weight="bold")
        note(ax, cx, 4.72, learns, size=9.0, colour=NAVY, linespacing=1.6)

        ax.plot([cx - CW / 2 + 0.30, cx + CW / 2 - 0.30], [3.98, 3.98],
                color="#C9D6E8", lw=lws(1.1), zorder=4)

        note(ax, cx, 3.64, "example models", size=8.6, colour=ORANGE,
             weight="bold")
        note(ax, cx, 3.02, models, size=9.0, colour=NAVY, linespacing=1.6)
        if sec:
            note(ax, cx, 2.40, sec, size=8.6, colour=GREY, style="italic")

    x_a, x_b = X0 + 0.20, X0 + 4 * CW + 3 * GAP - 0.20
    note(ax, (x_a + x_b) / 2, 1.62, "cost of the human labeling falls",
         size=9.6, colour=ORANGE, weight="bold")
    ax.annotate("", xy=(x_b, 1.22), xytext=(x_a, 1.22),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=lws(2.0),
                                mutation_scale=arr(16), shrinkA=0, shrinkB=0),
                zorder=4)
    note(ax, x_a, 0.86, "every training hour transcribed by hand",
         size=9.2, ha="left", colour=NAVY)
    note(ax, x_b, 0.86, "cheaper, noisier, or no labels at all",
         size=9.2, ha="right", colour=NAVY)

    note(ax, X0, 0.30,
         "The chapter develops the self-supervised family in Sections 6.2 to "
         "6.4 and weak supervision in Section 6.6, because those two do most "
         "for low-resource Arabic.",
         size=9.0, ha="left", colour=GREY, style="italic")

    save(fig, path_out)


if __name__ == "__main__":
    draw("fig6_1.png")
