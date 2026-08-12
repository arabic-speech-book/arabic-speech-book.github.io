"""
Figure 10.4: what a word-level metric does to a correct Arabic translation.

Section 10.5 argues that translating into Arabic puts the morphology on the side
the metric has to score, and that a word n-gram metric punishes an ordinary
spelling variant as though it were an error. That argument is made in prose and
a reader has to take it on trust. Drawn on one sentence with the counts computed
it is not a matter of trust.

The two sentences here mean the same thing and are both correct Arabic. They
differ in two places, and both differences are ordinary in real text: the hamza
is dropped from the alef of إلى, and the Tanwīn is dropped from غدًا. Chapter 4's
normalization folds away exactly these two.

Every number in the figure is counted by the script from the two token
sequences, not typed. The word row falls to no match at all by the fourth
n-gram, which is the order BLEU's usual configuration reaches, so a metric using
it scores this translation at zero. The character row is barely disturbed,
because only two characters of twenty-four changed.
"""
from collections import Counter

from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, save, ar, ARF)
from figscale import lws
from figfit import must_fit, report

REF = "أريد أن أسافر إلى الرياض غدًا"
CAND = "أريد أن أسافر الى الرياض غدا"
GLOSS = "‘I want to travel to Riyadh tomorrow’"

# The Arabic rule requires a gloss beside Arabic text, so this one string is
# longer than a label and is declared rather than removed.
LONG_LABELS_ALLOWED = ["‘I want to travel to Riyadh tomorrow’"]

R, C = REF.split(), CAND.split()
DIFF = [i for i, (a, b) in enumerate(zip(R, C)) if a != b]


def ngrams(t, n):
    return [tuple(t[i:i + n]) for i in range(len(t) - n + 1)]


def matches(a, b, n):
    ca, cb = Counter(ngrams(a, n)), Counter(ngrams(b, n))
    return sum(min(cb[g], ca[g]) for g in cb), len(ngrams(b, n))


def char_matches(n):
    a, b = REF.replace(' ', ''), CAND.replace(' ', '')
    ca = Counter(a[i:i + n] for i in range(len(a) - n + 1))
    cb = Counter(b[i:i + n] for i in range(len(b) - n + 1))
    return sum(min(cb[g], ca[g]) for g in cb), sum(cb.values())


BW, BH = 1.62, 0.72
SPAN = (2.55, 12.10)

# Every label is measured against the box it sits in, but a label centred near
# an edge can satisfy that check and still hang off the page, which is what the
# first render of this figure did on the right. This one checks the figure
# itself.
BOUNDS = []


def inside(fig, artist, what):
    fig.canvas.draw()
    bb = artist.get_window_extent(fig.canvas.get_renderer())
    x0, x1 = bb.x0 / fig.dpi, bb.x1 / fig.dpi
    w_in = fig.get_size_inches()[0]
    if x0 < 0.04 or x1 > w_in - 0.04:
        BOUNDS.append(f'{what}: spans {x0:.2f} to {x1:.2f} in on a '
                      f'{w_in:.2f} in page')
    return artist


def row(fig, ax, y, tokens, mark, colour, tag, sub):
    n = len(tokens)
    gap = 0.20
    bw = (SPAN[1] - SPAN[0] - (n - 1) * gap) / n
    step = (SPAN[1] - SPAN[0] - bw) / (n - 1)
    xs = [SPAN[0] + bw / 2 + i * step for i in range(n)]
    for i, (x, tok) in enumerate(zip(xs, tokens)):
        hot = i in mark
        box(ax, x, y, bw, BH, fill=WHITE if hot else BOXFILL,
            edge=ORANGE if hot else NAVY, lw=1.6 if hot else 1.3, r=0.10)
        t = note(ax, x, y, ar(tok), size=11.4,
                 colour=ORANGE if hot else NAVY, fontproperties=ARF)
        must_fit(fig, t, bw - 0.10, tok)
    t = note(ax, 0.10, y + 0.16, tag, size=10.0, colour=colour, weight="bold",
             ha="left", va="center")
    must_fit(fig, t, 2.30, tag)
    t = note(ax, 0.10, y - 0.20, sub, size=9.0, colour=GREY, ha="left",
             va="center")
    must_fit(fig, t, 2.30, sub)
    return xs, bw


def draw(path_out):
    w, h = 12.6, 4.45
    fig, ax = canvas(w, h, (0, w), (0, h))

    y_ref, y_can = 3.70, 2.50
    row(fig, ax, y_ref, R, [], NAVY, "reference", "a correct translation")
    xs, bw = row(fig, ax, y_can, C, DIFF, ORANGE, "candidate",
                 "another correct one")

    t = note(ax, (SPAN[0] + SPAN[1]) / 2, 4.20, GLOSS, size=9.4, colour=GREY)
    must_fit(fig, t, 6.00, GLOSS)
    inside(fig, t, "gloss")
    for i in DIFF:
        t = note(ax, xs[i], y_can - BH / 2 - 0.26,
                 "hamza dropped" if i == 3 else "Tanwīn dropped",
                 size=8.8, colour=ORANGE)
        must_fit(fig, t, 2.20, "Tanwin dropped")
        inside(fig, t, "dropped-mark note")

    # ---- the two readouts, counted ---------------------------------------
    y0 = 1.20
    t = note(ax, 0.10, y0 + 0.16, "matches", size=10.0, colour=NAVY,
             weight="bold", ha="left", va="center")
    must_fit(fig, t, 2.00, "matches")
    t = note(ax, 0.10, y0 - 0.20, "with the reference", size=9.0, colour=GREY,
             ha="left", va="center")
    must_fit(fig, t, 2.00, "with the reference")

    cols = [3.10, 4.90, 6.70, 8.50, 10.60]
    cw = 1.62
    heads = ["1-gram", "2-gram", "3-gram", "4-gram", "character 6-gram"]
    for x, head in zip(cols, heads):
        t = note(ax, x, y0 + 0.50, head, size=9.2, colour=GREY)
        must_fit(fig, t, 1.95, head)
        inside(fig, t, head)

    word = [matches(R, C, n) for n in (1, 2, 3, 4)]
    chars = char_matches(6)
    for x, (m, total) in zip(cols, word):
        good = m > 0
        box(ax, x, y0, cw, 0.62, fill=WHITE if good else "#FBE7DE",
            edge=NAVY if good else ORANGE, lw=1.5, r=0.10)
        t = note(ax, x, y0, f"{m} of {total}", size=10.6,
                 colour=NAVY if good else ORANGE, weight="bold")
        must_fit(fig, t, 1.60, f"{m} of {total}")
    box(ax, cols[4], y0, cw, 0.62, fill=GREENFILL, edge=GREEN, lw=1.5,
        r=0.10)
    t = note(ax, cols[4], y0, f"{chars[0]} of {chars[1]}", size=10.6,
             colour=GREEN, weight="bold")
    must_fit(fig, t, 1.60, f"{chars[0]} of {chars[1]}")

    ax.plot([cols[0] - cw / 2, cols[3] + cw / 2], [y0 - 0.52, y0 - 0.52],
            color=ORANGE, lw=lws(1.3), zorder=3)
    t = note(ax, (cols[0] + cols[3]) / 2, y0 - 0.78, "word n-grams",
             size=9.2, colour=ORANGE)
    must_fit(fig, t, 2.40, "word n-grams")
    inside(fig, t, "word group label")
    ax.plot([cols[4] - cw / 2, cols[4] + cw / 2], [y0 - 0.52, y0 - 0.52],
            color=GREEN, lw=lws(1.3), zorder=3)
    t = note(ax, cols[4], y0 - 0.78, "character n-grams", size=9.2,
             colour=GREEN)
    must_fit(fig, t, 2.40, "character n-grams")
    inside(fig, t, "character group label")

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig10_4.png")
