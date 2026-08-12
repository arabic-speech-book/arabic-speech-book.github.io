"""
Figure 8.6: what cleaning the audio actually cost, on Arabic.

Section 8.7 makes a claim that runs against the instinct of every first
project: a denoiser that makes noisy audio sound better can make a recognizer
read it worse. The claim is not an argument in this book, it is a measurement,
published on the Saudi broadcast corpus this chapter uses elsewhere, and a
reader is entitled to see it rather than be told it.

Four bars, four published word error rates for one fine-tuned model on one
corpus. Every arithmetic difference on the page is computed from those four
numbers rather than typed, so the annotations cannot drift from the bars.

The order of the bars is the order of the argument. Clean audio first, to fix
what good looks like. Then the same model on the noisy portion, which is the
cost of the noise. Then the same noisy audio passed through a denoiser first,
which is worse again. Then the intervention that worked, which was not cleaning
the audio at all but training the model on the condition it would meet.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, save)
from figscale import lws
from figfit import must_fit, report

# Word error rate, percent, one fine-tuned transformer model on SADA.
# The axis label is the one string in this figure longer than a label, and an
# axis label is what section 6 explicitly permits.
LONG_LABELS_ALLOWED = [
    "word error rate on Saudi broadcast speech, percent, lower is better",
]

BARS = [
    ("clean audio", 51.64, NAVY, BOXFILL, ""),
    ("noisy audio", 60.95, NAVY, BOXFILL, "{d:.2f} worse"),
    ("noisy, denoised first", 64.46, ORANGE, "#FBE7DE", "{d:.2f} worse"),
    ("noisy, trained on noise", 58.95, GREEN, GREENFILL, "{d:.2f} better"),
]

X0, X1 = 3.55, 8.60           # where the bars live
SCALE = (X1 - X0) / 70.0      # seventy percent spans the plotting width

BOUNDS = []


def inside(fig, artist, what):
    fig.canvas.draw()
    bb = artist.get_window_extent(fig.canvas.get_renderer())
    x0, x1 = bb.x0 / fig.dpi, bb.x1 / fig.dpi
    w_in = fig.get_size_inches()[0]
    if x0 < 0.04 or x1 > w_in - 0.04:
        BOUNDS.append(f'{what}: spans {x0:.2f} to {x1:.2f} in')
    return artist


def draw(path_out):
    w, h = 12.6, 3.42
    fig, ax = canvas(w, h, (0, w), (0, h))

    ys = [2.77, 2.07, 1.37, 0.67]
    bh = 0.46
    base = BARS[1][1]
    for k, (y, (label, wer, edge, fill, note_fmt)) in enumerate(
            zip(ys, BARS)):
        length = wer * SCALE
        box(ax, X0 + length / 2, y, length, bh, fill=fill, edge=edge, lw=1.5,
            r=0.06)
        t = note(ax, X0 - 0.18, y, label, size=9.6, colour=edge, ha="right",
                 va="center")
        must_fit(fig, t, 3.20, label)
        inside(fig, t, label)
        t = note(ax, X0 + length + 0.16, y, f"{wer:.2f}", size=9.8,
                 colour=edge, weight="bold", ha="left", va="center")
        must_fit(fig, t, 0.90, f"{wer:.2f}")
        inside(fig, t, "value")
        if note_fmt:
            d = abs(wer - (BARS[0][1] if k == 1 else base))
            t = note(ax, 9.35, y, note_fmt.format(d=d), size=9.2, colour=GREY,
                     ha="left", va="center")
            must_fit(fig, t, 1.80, note_fmt)
            inside(fig, t, note_fmt)

    t = note(ax, X0, 3.39, "word error rate on Saudi broadcast speech, "
             "percent, lower is better", size=9.4, colour=GREY, ha="left",
             va="center")
    must_fit(fig, t, 7.60, "axis note")
    inside(fig, t, "axis note")

    ax.plot([X0, X0], [0.35, 3.09], color=EDGE_LIGHT, lw=lws(1.3), zorder=2)
    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig8_6.png")
