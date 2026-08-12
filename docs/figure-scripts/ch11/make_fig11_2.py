"""Figure 11.2: what one Arabic clip becomes, counted at every stage.

Section 11.2 asserts that a connector has to shorten the audio sequence and
leaves a reader to take the size of the problem on trust. Every number needed
to settle it is fixed by Whisper's own front end and by arithmetic, so the
figure counts instead of asserting.

Two rows, because the second is where the argument lands. Thirty seconds is
the window the model is built around and its numbers look manageable. Ten
minutes is an ordinary recorded meeting, and the same chain leaves seven and a
half thousand positions before a word of the instruction is added, which is
what the section means when it says the language model is overwhelmed.

Only one column is a choice rather than a consequence: keeping one vector in
four is an ordinary connector setting and not a fact about any named system, so
that column is marked illustrative and the caption says so again.

Every count in the figure is computed by the script from the sampling rate, the
hop, the stem stride and the pooling factor. Nothing here is typed in by hand.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

RATE = 16_000          # Whisper resamples all audio to 16 kHz
HOP_MS = 10            # a spectrogram frame every 10 ms
STEM_STRIDE = 2        # the second convolution of the encoder stem
KEEP = 4               # one vector in four, an illustrative connector setting
PROMPT = 12            # word pieces in a short instruction

COLUMNS = [
    ("waveform\nsamples", "at 16 kHz"),
    ("spectrogram\nframes", "one every 10 ms"),
    ("encoder\nvectors", "stem stride of two"),
    ("after the\nconnector", "one in four kept"),
    ("with the\ninstruction", "twelve word pieces"),
]

ROWS = [("thirty seconds", 30.0), ("ten minutes", 600.0)]

BOUNDS = []


def counts(seconds):
    samples = int(seconds * RATE)
    frames = int(seconds * 1000 / HOP_MS)
    vectors = frames // STEM_STRIDE
    kept = vectors // KEEP
    return [samples, frames, vectors, kept, kept + PROMPT]


def inside(fig, artist, what):
    fig.canvas.draw()
    bb = artist.get_window_extent(fig.canvas.get_renderer())
    x0, x1 = bb.x0 / fig.dpi, bb.x1 / fig.dpi
    w_in = fig.get_size_inches()[0]
    if x0 < 0.04 or x1 > w_in - 0.04:
        BOUNDS.append(f'{what}: spans {x0:.2f} to {x1:.2f} in')
    return artist


def draw(path_out):
    w, h = 12.6, 5.20
    fig, ax = canvas(w, h, (0, w), (0, h))

    xs = [2.85, 4.98, 7.11, 9.24, 11.37]
    cw, ch = 1.85, 0.72

    # ---- the column headings ---------------------------------------------
    for x, (head, sub) in zip(xs, COLUMNS):
        t = note(ax, x, 4.66, head, size=9.6, colour=NAVY, weight="bold",
                 linespacing=1.35)
        must_fit(fig, t, 2.00, head)
        inside(fig, t, head)
        t = note(ax, x, 4.20, sub, size=8.8, colour=GREY)
        must_fit(fig, t, 2.00, sub)
        inside(fig, t, sub)

    ax.plot([0.10, 12.50], [4.00, 4.00], color=EDGE_LIGHT, lw=lws(1.4),
            zorder=2)

    # ---- one row per length of audio -------------------------------------
    for row, (label, seconds) in enumerate(ROWS):
        y = 3.20 - row * 1.55
        t = note(ax, 0.10, y, label, size=9.2, colour=NAVY, weight="bold",
                 ha="left", va="center")
        must_fit(fig, t, 1.78, label)
        for i, (x, n) in enumerate(zip(xs, counts(seconds))):
            last_two = i >= 3
            box(ax, x, y, cw, ch,
                fill=GREENFILL if last_two else BOXFILL,
                edge=GREEN if last_two else NAVY, lw=1.5, r=0.12)
            text = f"{n:,}"
            t = note(ax, x, y, text, size=11.4,
                     colour=GREEN if last_two else NAVY, weight="bold")
            must_fit(fig, t, cw - 0.16, text)
        for a, b in zip(xs, xs[1:]):
            arrow(ax, (a + cw / 2 + 0.04, y), (b - cw / 2 - 0.04, y),
                  colour=GREY, lw=1.4, scale=11)

    # the one column that is a setting rather than a consequence
    t = note(ax, xs[3], 0.40, "illustrative", size=8.8, colour=ORANGE)
    must_fit(fig, t, 2.10, "illustrative")
    inside(fig, t, "illustrative")
    ax.plot([xs[3], xs[3]], [0.62, 0.86], color=ORANGE, lw=lws(1.2), zorder=3)

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig11_2.png")
