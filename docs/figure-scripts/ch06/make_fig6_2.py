"""
Figure 6.2: the wav2vec 2.0 architecture.

Redrawn at the book's type scale. Beyond the size, the original left the
contrastive choice implicit: a dashed loop ran from the masked latent down to a
row of unlabeled cells and the reader had to infer what was being chosen
between. Here the candidates are drawn out, one marked as the true unit and
three as distractors, with the arrow running from the context vector at the
masked position to the choice it has to make. That is the whole of the pretext
task, so it is worth showing rather than naming.

The mask sits on the latents, where wav2vec 2.0 puts it, not on the waveform.
"""
from bookstyle import (NAVY, ORANGE, GREY, GREEN, BOXFILL, WHITE, canvas, box,
                       title_in, note, arrow, save)
from figscale import lws, arr

PEACH = "#FBEDE2"
GREENFILL = "#E6F0DC"

Y = 6.30          # the main row
H = 0.72
NL, LX0, LW = 8, 4.30, 0.52
MASK = (3, 4)
QY = 3.55         # the quantizer row


def slots(ax, x0, n, y, w, h, fills, edges, labels=None, size=9.0):
    for i in range(n):
        cx = x0 + w / 2 + i * w
        box(ax, cx, y, w * 0.84, h, fill=fills[i], edge=edges[i], lw=1.3,
            r=0.07)
        if labels and labels[i]:
            note(ax, cx, y, labels[i], size=size, colour=NAVY, weight="bold")


def draw(path_out):
    fig, ax = canvas(12.6, 7.8, (0, 12.6), (0, 7.8))

    # ---- waveform, convolutional encoder
    box(ax, 1.04, Y, 1.52, 1.04, fill=BOXFILL, lw=1.5)
    title_in(ax, 1.04, Y + 0.16, "raw", size=10.4)
    title_in(ax, 1.04, Y - 0.16, "waveform", size=10.4)
    arrow(ax, (1.86, Y), (2.10, Y), lw=1.9, scale=14)

    box(ax, 3.06, Y, 1.84, 1.04, fill=BOXFILL, lw=1.5)
    title_in(ax, 3.06, Y + 0.16, "CNN feature", size=9.8)
    title_in(ax, 3.06, Y - 0.16, "encoder", size=9.8)
    arrow(ax, (4.02, Y), (4.26, Y), lw=1.9, scale=14)

    # ---- latents, with a masked span
    fills, edges = [WHITE] * NL, [NAVY] * NL
    for i in range(MASK[0], MASK[1] + 1):
        fills[i], edges[i] = PEACH, ORANGE
    slots(ax, LX0, NL, Y, LW, H, fills, edges)
    note(ax, LX0 + NL * LW / 2, Y + 0.70,
         "latent features z, one per frame", size=9.4, colour=NAVY,
         weight="bold")
    mx = LX0 + (MASK[0] + (MASK[1] - MASK[0] + 1) / 2) * LW
    note(ax, mx, Y - 0.62, "masked span", size=9.4, colour=ORANGE,
         weight="bold")

    # ---- context Transformer and its output
    arrow(ax, (8.52, Y), (8.74, Y), lw=1.9, scale=14)
    box(ax, 9.75, Y, 1.94, 1.04, fill=BOXFILL, lw=1.5)
    title_in(ax, 9.75, Y + 0.16, "context", size=10.4)
    title_in(ax, 9.75, Y - 0.16, "Transformer", size=10.4)
    arrow(ax, (10.78, Y), (11.00, Y), lw=1.9, scale=14)

    CX0, CWD = 11.04, 0.48
    slots(ax, CX0, 3, Y, CWD, H, [WHITE, PEACH, WHITE], [NAVY, ORANGE, NAVY])
    note(ax, CX0 + 1.5 * CWD, Y + 0.86, "context", size=9.4, colour=NAVY,
         weight="bold")
    note(ax, CX0 + 1.5 * CWD, Y + 0.60, "vectors c", size=9.4, colour=NAVY,
         weight="bold")

    # ---- quantizer branch
    qx = LX0 + 1.5 * LW
    ax.plot([qx, qx], [Y - H / 2, QY + 0.60], color=ORANGE, lw=lws(1.7),
            zorder=2)
    arrow(ax, (qx, QY + 0.64), (qx, QY + 0.46), lw=1.7, scale=13)

    box(ax, qx, QY, 2.62, 0.92, fill=BOXFILL, lw=1.5)
    title_in(ax, qx, QY + 0.14, "quantizer", size=10.2)
    note(ax, qx, QY - 0.18, "learned finite codebook", size=8.8, colour=GREY)
    arrow(ax, (qx + 1.34, QY), (qx + 1.76, QY), lw=1.7, scale=13)

    # ---- the contrastive choice, drawn out
    UX0, UW = qx + 1.82, 0.68
    slots(ax, UX0, 4, QY, UW, 0.72,
          [GREENFILL, WHITE, WHITE, WHITE], [GREEN, GREY, GREY, GREY],
          ["q₁", "q₂", "q₃", "q₄"], size=9.6)
    note(ax, UX0 + 0.5 * UW, QY + 0.62, "true", size=9.0, colour=GREEN,
         weight="bold")
    note(ax, UX0 + 2.5 * UW, QY + 0.62, "distractors", size=9.0, colour=GREY)
    note(ax, UX0 + 2 * UW, QY - 0.66,
         "candidate discrete units q for the masked frame",
         size=9.2, colour=NAVY, weight="bold")

    # the context vector at the masked position has to pick the true unit
    ax.annotate("", xy=(UX0 + 3.5 * UW + 0.42 * UW, QY + 0.22),
                xytext=(CX0 + 1.5 * CWD, Y - H / 2 - 0.06),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=lws(1.6),
                                linestyle=(0, (5, 3)), mutation_scale=arr(13),
                                connectionstyle="arc3,rad=0.30",
                                shrinkA=2, shrinkB=2), zorder=4)

    note(ax, 12.36, 2.24,
         "contrastive loss: from the context vector at the\n"
         "masked position, pick the true unit against the\n"
         "distractors drawn from elsewhere in the utterance",
         size=9.2, ha="right", va="center", colour=GREEN, linespacing=1.7)

    note(ax, 0.28, 1.30,
         "Pretraining needs no transcripts, because the target is the model's "
         "own quantized latent. Only afterwards is\n"
         "a small output layer added and the whole model fine-tuned with the "
         "Connectionist Temporal Classification\n"
         "(CTC) loss of Chapter 5, on whatever labeled Arabic data exists.",
         size=9.2, ha="left", va="top", colour=NAVY, linespacing=1.7)

    save(fig, path_out)


if __name__ == "__main__":
    draw("fig6_2.png")
