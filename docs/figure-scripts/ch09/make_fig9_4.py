"""
Figure 9.4: three routes from a linguistic form to a waveform, aligned so that
what separates them is visible as a difference in shape.

Section 9.5 was the one section of the chapter with no figure, and it is the
section carrying the chapter's hardest claim: that removing stages from the
middle of the pipeline buys latency and naturalness and costs inspectability.
That claim is about where the seams are, so it is a claim a diagram can make
and a paragraph cannot.

All three rows sit on the same five slots and end on the same card, a waveform.
The middle slot is the seam, and it is drawn in orange in every row because it
is the thing being compared:

  The two-stage stack hands a mel spectrogram from the acoustic model to the
  vocoder. A spectrogram is a picture. Anyone can look at it, and a wrong
  duration or a missing phoneme is visible in it before a listener hears it.

  An end-to-end network has no seam at all. The slot is drawn empty and dashed,
  because there is nothing there to inspect, not because the figure ran out of
  room.

  A codec model's seam carries discrete audio tokens, which are integers into a
  learned codebook. They exist, they can be counted and stored, and they cannot
  be read.

The third row also starts differently, on text tokens rather than phonemes, and
that is the Arabic point of the section rather than a detail of drawing. A
system built on phonemes is handed the output of Section 9.2 and can be checked
against it. A system built on text tokens is handed undiacritized Arabic, so the
diacritization happens inside the model, where the chapter's front-end argument
has nothing left to hold on to.

No sentences inside the artwork; the reading is in the caption.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save)
from figfit import must_fit, report

SPAN = (2.30, 12.46)          # every row starts and ends here
SLOTS = 5
GAP = 0.30
BH = 0.95


def geometry():
    bw = (SPAN[1] - SPAN[0] - (SLOTS - 1) * GAP) / SLOTS
    step = (SPAN[1] - SPAN[0] - bw) / (SLOTS - 1)
    xs = [SPAN[0] + bw / 2 + i * step for i in range(SLOTS)]
    return xs, bw


def tag(fig, ax, y, head, sub, colour):
    t = note(ax, 0.10, y + 0.34, head, size=10.4, colour=colour, weight="bold",
             ha="left", va="center")
    must_fit(fig, t, 2.10, head)
    t = note(ax, 0.10, y - 0.24, sub, size=9.4, colour=GREY, ha="left",
             va="top", linespacing=1.45)
    must_fit(fig, t, 2.10, max(sub.split("\n"), key=len))


def card(fig, ax, x, y, w, text, fill=WHITE, edge=NAVY, size=9.1, dashed=False):
    box(ax, x, y, w, BH, fill=fill, edge=edge, lw=1.5, r=0.12,
        ls=(0, (4, 3)) if dashed else "solid")
    if text:
        t = note(ax, x, y, text, size=size, colour=edge, weight="bold",
                 linespacing=1.45)
        must_fit(fig, t, w - 0.12, max(text.split("\n"), key=len))


def seam_note(fig, ax, x, y, text):
    t = note(ax, x, y - BH / 2 - 0.30, text, size=9.0, colour=ORANGE)
    must_fit(fig, t, 3.20, text)


def link(ax, a, b, y, bw):
    arrow(ax, (a + bw / 2 + 0.03, y), (b - bw / 2 - 0.03, y))


def draw(path_out):
    w, h = 12.6, 6.45
    fig, ax = canvas(w, h, (0, w), (0, h))
    xs, bw = geometry()
    y1, y2, y3 = 5.55, 3.45, 1.20

    # ---- row 1: the two-stage stack of Sections 9.4 and 9.5 --------------
    tag(fig, ax, y1, "Two stages", "acoustic model,\nthen vocoder", NAVY)
    card(fig, ax, xs[0], y1, bw, "phonemes", fill=BOXFILL)
    card(fig, ax, xs[1], y1, bw, "acoustic\nmodel")
    card(fig, ax, xs[2], y1, bw, "mel\nspectrogram", edge=ORANGE)
    card(fig, ax, xs[3], y1, bw, "vocoder")
    card(fig, ax, xs[4], y1, bw, "waveform", fill=GREENFILL, edge=GREEN)
    for a, b in zip(xs, xs[1:]):
        link(ax, a, b, y1, bw)
    seam_note(fig, ax, xs[2], y1, "a picture you can look at")

    # ---- row 2: one network, and no seam at all --------------------------
    tag(fig, ax, y2, "End to end", "one training\nobjective", ORANGE)
    card(fig, ax, xs[0], y2, bw, "phonemes", fill=BOXFILL)
    wide_l = xs[1] - bw / 2
    wide_r = xs[3] + bw / 2
    card(fig, ax, (wide_l + wide_r) / 2, y2, wide_r - wide_l,
         "one network, phonemes to waveform")
    card(fig, ax, xs[4], y2, bw, "waveform", fill=GREENFILL, edge=GREEN)
    link(ax, xs[0], xs[1], y2, bw)
    arrow(ax, (wide_r + 0.03, y2), (xs[4] - bw / 2 - 0.03, y2))
    # the empty seam, drawn where the other two rows carry theirs
    box(ax, xs[2], y2 - BH / 2 - 0.42, bw, 0.34, fill=WHITE, edge=ORANGE,
        lw=1.2, r=0.10, ls=(0, (4, 3)))
    t = note(ax, xs[2], y2 - BH / 2 - 0.80, "nothing to inspect", size=9.0,
             colour=ORANGE)
    must_fit(fig, t, 3.20, "nothing to inspect")

    # ---- row 3: synthesis as generation ----------------------------------
    tag(fig, ax, y3, "Codec tokens", "synthesis as\ngeneration", GREEN)
    card(fig, ax, xs[0], y3, bw, "text tokens", fill=BOXFILL)
    card(fig, ax, xs[1], y3, bw, "codec model\nor diffusion")
    card(fig, ax, xs[2], y3, bw, "audio\ntokens", edge=ORANGE)
    card(fig, ax, xs[3], y3, bw, "codec\ndecoder")
    card(fig, ax, xs[4], y3, bw, "waveform", fill=GREENFILL, edge=GREEN)
    for a, b in zip(xs, xs[1:]):
        link(ax, a, b, y3, bw)
    seam_note(fig, ax, xs[2], y3, "codes, not human readable")

    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig9_4.png")
