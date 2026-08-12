"""
Figure 9.3: two neural acoustic models, on one skeleton.

Both rows carry the same five stations in the same places: phonemes, encoder,
the stage that differs, decoder, mel spectrogram. What separates an
autoregressive model from a parallel one is then visible as a difference in
shape rather than as a difference in wording, which is what the book's rule for
compared panels asks for.

  The top row's third station is attention, and its arrow runs backwards: from
  the mel spectrogram it has just produced, into the decoder. That loop is what
  autoregression is, and drawing where the fed-back frame comes from is the
  point. It is also the mechanism the chapter blames for skipped and repeated
  words, so a figure that leaves attention out cannot explain the failure the
  text attributes to it.

  The bottom row's third station is the variance adaptor, and its arrow runs
  forwards and widens: the duration predictor says how many frames each phoneme
  becomes, and the length regulator expands the sequence before the decoder
  ever runs. That expansion is why the decoder can produce every frame at once,
  and it belongs between the adaptor and the decoder, not under the decoder.

An earlier version of this figure got all three of those wrong: no attention, a
self-loop on the decoder that came from nowhere, and the fan drawn under the
decoder as though the decoder did the expanding. The author said it looked
incorrect and was right, which is the second time that has happened in this book
and the second time the fault was an architectural claim rather than a layout.

No sentences inside the artwork; the reading is in the caption.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

SPAN = (2.18, 12.46)          # both rows start and end here
BH = 1.00

TOP = ["phonemes", "encoder", "attention", "decoder", "mel\nspectrogram"]
BOT = ["phonemes", "encoder", "duration,\npitch, energy", "decoder",
       "mel\nspectrogram"]


def stations(fig, ax, y, cards, tag, colour):
    n = len(cards)
    gap = 0.34
    bw = (SPAN[1] - SPAN[0] - (n - 1) * gap) / n
    step = (SPAN[1] - SPAN[0] - bw) / (n - 1)
    xs = [SPAN[0] + bw / 2 + i * step for i in range(n)]
    for i, (x, title) in enumerate(zip(xs, cards)):
        fill = BOXFILL if i == 0 else (GREENFILL if i == n - 1 else WHITE)
        edge = GREEN if i == n - 1 else NAVY
        box(ax, x, y, bw, BH, fill=fill, edge=edge, lw=1.5, r=0.12)
        t = note(ax, x, y, title, size=9.1, colour=edge, weight="bold",
                 linespacing=1.45)
        must_fit(fig, t, bw - 0.10, max(title.split("\n"), key=len))
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + bw / 2 + 0.03, y), (b - bw / 2 - 0.03, y))
    t = note(ax, 0.10, y + 0.21, tag[0], size=10.4, colour=colour,
             weight="bold", ha="left", va="center")
    must_fit(fig, t, 2.10, tag[0])
    t = note(ax, 0.10, y - 0.23, tag[1], size=9.4, colour=GREY, ha="left",
             va="center")
    must_fit(fig, t, 2.10, tag[1])
    return xs, bw


def draw(path_out):
    w, h = 12.6, 5.9
    fig, ax = canvas(w, h, (0, w), (0, h))
    y1, y2 = 4.55, 2.05

    xs1, bw = stations(fig, ax, y1, TOP, ("Tacotron 2", "autoregressive"),
                       NAVY)
    xs2, _ = stations(fig, ax, y2, BOT, ("FastSpeech 2", "parallel"), ORANGE)

    # ---- the loop that is autoregression: output back into the decoder ---
    dec, mel = xs1[3], xs1[4]
    drop = y1 - BH / 2 - 0.52
    ax.annotate("", xy=(dec, y1 - BH / 2 - 0.03), xytext=(mel, drop),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=lws(1.7),
                                mutation_scale=25, shrinkA=0, shrinkB=0,
                                connectionstyle="angle,angleA=0,angleB=90,"
                                                "rad=8"), zorder=6)
    ax.plot([mel, mel], [y1 - BH / 2 - 0.03, drop], color=ORANGE,
            lw=lws(1.7), zorder=6)
    t = note(ax, (dec + mel) / 2, drop - 0.26, "one frame at a time",
             size=9.2, colour=ORANGE)
    must_fit(fig, t, 2.80, "one frame at a time")

    # ---- the expansion that makes parallel generation possible ----------
    # The length regulator turns one phoneme into several frames, and it runs
    # before the decoder. There is no room for that between two cards, so it is
    # drawn beneath the gap it belongs to, as one bar becoming four, with a
    # stem back to the stage that does it.
    xl, xr = xs2[2], xs2[3]
    mid = (xl + xr) / 2
    yb = y2 - BH / 2 - 0.60
    ax.plot([xl, xl], [y2 - BH / 2 - 0.03, yb], color=ORANGE, lw=lws(1.5),
            zorder=6)
    ax.plot([xl, mid - 0.86], [yb, yb], color=ORANGE, lw=lws(1.5), zorder=6)
    ax.plot([mid - 0.86, mid - 0.86], [yb - 0.16, yb + 0.16], color=ORANGE,
            lw=lws(2.4), zorder=6, solid_capstyle="butt")
    arrow(ax, (mid - 0.68, yb), (mid - 0.26, yb), lw=1.5, scale=13)
    for dx in (-0.06, 0.16, 0.38, 0.60):
        ax.plot([mid + dx, mid + dx], [yb - 0.16, yb + 0.16], color=ORANGE,
                lw=lws(2.4), zorder=6, solid_capstyle="butt")
    t = note(ax, mid - 0.13, yb - 0.44, "one phoneme, several frames",
             size=9.2, colour=ORANGE)
    must_fit(fig, t, 3.60, "one phoneme, several frames")

    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig9_3.png")
