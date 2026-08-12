"""Figure 12.2: Goodness of Pronunciation read off a forced alignment.

The measure is simple enough to draw exactly, so it is drawn exactly rather
than sketched. A row of aligned segments, one bar per segment for how well the
audio matches the phone the learner was supposed to produce, and a threshold
line. Everything under the line is flagged.

The example is the chapter's own: a learner reading raḥīm who produces the
ordinary hāʾ in place of the pharyngeal ḥāʾ. Every other phone sits high and
that one sits low, which is what the measure is for and also what it cannot do,
since it says the sound was wrong and not which sound was made instead.

The bar heights are illustrative and the figure says so. They are chosen to
show the shape of a flagged phone, not measured from a model.

Each phone carries its Arabic under its transliteration, because the reader
who will use this figure reads the word in Arabic and the transliteration is
the borrowed notation rather than the other way round. The short vowel is
written on a tatweel, which is how a diacritic is shown standing alone.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save, ar, ARF)
from figscale import lws
from figfit import must_fit, report
import matplotlib.patches as mp

# (transliteration, the Arabic it stands for, the illustrative score)
PHONES = [("r", "ر", 0.86), ("a", "ـَ", 0.90), ("ḥ", "ح", 0.24),
          ("ī", "ِي", 0.88), ("m", "م", 0.82)]
THRESHOLD = 0.45
WORD = "رحيم"

# The Arabic rule requires a gloss beside Arabic text, so this string is longer
# than a label and is declared rather than shortened.
LONG_LABELS_ALLOWED = ["raḥīm, ‘merciful’"]

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
    w, h = 12.6, 5.90
    fig, ax = canvas(w, h, (0, w), (0, h))

    x0, x1 = 2.60, 11.90
    n = len(PHONES)
    step = (x1 - x0) / n
    base, top = 2.00, 4.80

    # the score axis
    ax.plot([x0 - 0.30, x0 - 0.30], [base, top], color=GREY, lw=lws(1.2),
            zorder=3)
    t = note(ax, 0.10, (base + top) / 2, "match to the phone", size=9.0,
             colour=GREY, ha="left", va="center")
    must_fit(fig, t, 2.15, "axis")
    inside(fig, t, "axis")

    for i, (phone, arabic, score) in enumerate(PHONES):
        cx = x0 + step * (i + 0.5)
        low = score < THRESHOLD
        colour = ORANGE if low else NAVY
        height = (top - base) * score
        ax.add_patch(mp.Rectangle((cx - step * 0.30, base), step * 0.60,
                                  height, facecolor=GREENFILL if not low
                                  else "#FBE7DE", edgecolor=colour,
                                  lw=lws(1.4), zorder=4))
        t = note(ax, cx, base - 0.30, phone, size=10.6, colour=colour,
                 weight="bold")
        must_fit(fig, t, step - 0.20, phone)
        t = note(ax, cx, base - 0.74, ar(arabic), size=14.5, colour=colour,
                 fontproperties=ARF)
        must_fit(fig, t, step - 0.20, arabic)
        inside(fig, t, arabic)
        if low:
            t = note(ax, cx, base + height + 0.26, "flagged", size=9.0,
                     colour=ORANGE, weight="bold")
            must_fit(fig, t, step, "flagged")

    ax.plot([x0 - 0.30, x1], [base + (top - base) * THRESHOLD] * 2,
            color=ORANGE, lw=lws(1.4), linestyle=(0, (5, 3)), zorder=5)
    t = note(ax, x1 - 0.10, base + (top - base) * THRESHOLD + 0.20,
             "threshold", size=9.0, colour=ORANGE, ha="right", va="center")
    must_fit(fig, t, 1.60, "threshold")
    inside(fig, t, "threshold")

    # the aligned segments the scores are read from
    ax.plot([x0, x1], [base - 1.16, base - 1.16], color=EDGE_LIGHT,
            lw=lws(1.4), zorder=2)
    for i in range(n + 1):
        x = x0 + step * i
        ax.plot([x, x], [base - 1.28, base - 1.04], color=EDGE_LIGHT,
                lw=lws(1.1), zorder=2)
    t = note(ax, (x0 + x1) / 2, base - 1.54, "the forced alignment", size=9.4,
             colour=GREY)
    must_fit(fig, t, 4.00, "alignment")
    inside(fig, t, "alignment")

    # the word being read
    box(ax, 1.30, top + 0.42, 2.10, 0.78, fill=BOXFILL, edge=NAVY, lw=1.4,
        r=0.12)
    t = note(ax, 1.30, top + 0.56, ar(WORD), size=12.4, colour=NAVY,
             fontproperties=ARF)
    must_fit(fig, t, 1.90, "the word")
    t = note(ax, 1.30, top + 0.24, "raḥīm, ‘merciful’", size=8.4, colour=GREY)
    must_fit(fig, t, 2.00, "gloss")
    inside(fig, t, "gloss")

    t = note(ax, 7.30, top + 0.42, "illustrative scores", size=9.0,
             colour=GREY)
    must_fit(fig, t, 3.00, "illustrative")
    inside(fig, t, "illustrative")

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig12_2.png")
