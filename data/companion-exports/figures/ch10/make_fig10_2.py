"""
Figure 10.2: what a cascade's seam costs, on one Arabic sentence.

The draft's specification asked for a generic diagram with "one highlighted
recognition error in red". A generic error teaches nothing. The book's rule is
that a figure earns its page by carrying a claim, and the claim here is Arabic:
the words a cascade is most likely to mis-hear are the dialectal ones, and a
dialectal mis-hearing does not produce a garbled translation that a reader would
notice. It produces a fluent, confident, wrong one.

The example is one Gulf sentence. أبغى is the Najdi and Gulf word for "I want",
and in Gulf pronunciation the qaf of أبقى is realised as a /g/, so /abɣa/ and
/abga/ differ by very little in the audio and by one letter on the page. A
recognizer trained mostly on Modern Standard Arabic has every reason to prefer
the Modern Standard word. The translation that follows is grammatical English
and says something the speaker did not say: a request has become a statement.

The end-to-end row is drawn beside it because the comparison is the point of
Section 10.1, not because the end-to-end model is safer. It has no transcript
to get wrong and no transcript to check either, which is what the caption says.

The example is illustrative and constructed, not taken from a recognizer's
output on a corpus, and the caption says so.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save, ar, ARF)
from figfit import must_fit, report

BH = 1.05


def card(fig, ax, x, y, w, h, lines, fill=WHITE, edge=NAVY):
    """lines: list of (text, size, colour, is_arabic)."""
    box(ax, x, y, w, h, fill=fill, edge=edge, lw=1.5, r=0.12)
    n = len(lines)
    step = 0.40
    top = y + (n - 1) * step / 2
    for i, (text, size, colour, arabic) in enumerate(lines):
        kw = {"fontproperties": ARF} if arabic else {}
        t = note(ax, x, top - i * step, ar(text) if arabic else text,
                 size=size, colour=colour,
                 weight="normal" if arabic else ("bold" if i == 0
                                                 else "normal"), **kw)
        must_fit(fig, t, w - 0.14, text)


def draw(path_out):
    w, h = 12.6, 5.00
    fig, ax = canvas(w, h, (0, w), (0, h))

    y1, y2 = 3.55, 1.20
    W1, W2, W3 = 3.20, 2.60, 3.85
    xs = [3.35, 6.80, 10.575]

    # ---- the cascade row --------------------------------------------------
    t = note(ax, 0.10, y1 + 0.34, "Cascade", size=10.4, colour=NAVY,
             weight="bold", ha="left", va="center")
    must_fit(fig, t, 1.60, "Cascade")
    t = note(ax, 0.10, y1 - 0.24, "a Gulf word,\nmis-heard", size=9.4,
             colour=GREY, ha="left", va="top", linespacing=1.45)
    must_fit(fig, t, 1.60, "a Gulf word,")

    card(fig, ax, xs[0], y1, W1, 1.30,
         [("أبغى أروح الرياض", 11.0, NAVY, True),
          ("abgha arūḥ ar-riyāḍ", 8.8, GREY, False),
          ("‘I want to go to Riyadh’", 8.8, GREY, False)], fill=BOXFILL)
    card(fig, ax, xs[1], y1, W2, 1.30,
         [("أبقى أروح الرياض", 11.0, ORANGE, True),
          ("abqā arūḥ ar-riyāḍ", 8.8, ORANGE, False),
          ("one letter changed", 8.8, ORANGE, False)],
         edge=ORANGE)
    card(fig, ax, xs[2], y1, W3, 1.30,
         [("“I keep going to Riyadh”", 9.4, ORANGE, False),
          ("fluent English,", 8.8, GREY, False),
          ("and not what was said", 8.8, GREY, False)], edge=ORANGE)

    for a, b, wa, wb in ((xs[0], xs[1], W1, W2), (xs[1], xs[2], W2, W3)):
        arrow(ax, (a + wa / 2 + 0.03, y1), (b - wb / 2 - 0.03, y1))
    t = note(ax, (xs[0] + xs[1]) / 2, y1 + 0.86, "recognizer", size=9.0,
             colour=GREY)
    must_fit(fig, t, 1.60, "recognizer")
    t = note(ax, (xs[1] + xs[2]) / 2, y1 + 0.86, "translator", size=9.0,
             colour=GREY)
    must_fit(fig, t, 1.60, "translator")

    # ---- the end-to-end row -----------------------------------------------
    t = note(ax, 0.10, y2 + 0.34, "End to end", size=10.4, colour=ORANGE,
             weight="bold", ha="left", va="center")
    must_fit(fig, t, 1.60, "End to end")
    t = note(ax, 0.10, y2 - 0.24, "no transcript\neither way", size=9.4,
             colour=GREY, ha="left", va="top", linespacing=1.45)
    must_fit(fig, t, 1.60, "no transcript")

    card(fig, ax, xs[0], y2, W1, 1.30,
         [("أبغى أروح الرياض", 11.0, NAVY, True),
          ("abgha arūḥ ar-riyāḍ", 8.8, GREY, False),
          ("the same audio", 8.8, GREY, False)], fill=BOXFILL)
    box(ax, xs[1], y2, W2, 0.62, fill=WHITE, edge=ORANGE, lw=1.2, r=0.10,
        ls=(0, (4, 3)))
    t = note(ax, xs[1], y2, "no transcript", size=9.1, colour=ORANGE,
             weight="bold")
    must_fit(fig, t, W2 - 0.14, "no transcript")
    card(fig, ax, xs[2], y2, W3, 1.30,
         [("“I want to go to Riyadh”", 9.4, GREEN, False),
          ("or a wrong answer", 8.8, GREY, False),
          ("with nothing to check", 8.8, GREY, False)],
         fill=GREENFILL, edge=GREEN)
    arrow(ax, (xs[0] + W1 / 2 + 0.03, y2), (xs[1] - W2 / 2 - 0.03, y2))
    arrow(ax, (xs[1] + W2 / 2 + 0.03, y2), (xs[2] - W3 / 2 - 0.03, y2))
    t = note(ax, (xs[0] + xs[1]) / 2, y2 + 0.86, "one model", size=9.0,
             colour=GREY)
    must_fit(fig, t, 1.60, "one model")

    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig10_2.png")
