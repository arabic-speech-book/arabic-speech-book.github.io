"""
Figure 11.5: speech in, speech out, with a language model in the middle.

The point of the discrete audio token is that it makes generation possible at
all: a language model predicts the next item in a sequence, so audio has to
become a sequence of items before a language model can produce it. The figure
draws the sequence explicitly, as a short row of numbered units between the
tokenizer and the decoder, rather than leaving it as a word on a card.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save)
from figfit import must_fit, report

def draw(path_out):
    w, h = 12.6, 3.20
    fig, ax = canvas(w, h, (0, w), (0, h))
    y = 2.52
    cards = [
        ("Arabic speech in", 2.20, BOXFILL, NAVY),
        ("audio tokenizer", 2.15, WHITE, NAVY),
        ("language model", 2.35, WHITE, ORANGE),
        ("token decoder", 2.05, WHITE, NAVY),
        ("Arabic speech out", 2.30, GREENFILL, GREEN),
    ]
    gap = 0.24
    total = sum(c[1] for c in cards) + gap * (len(cards) - 1)
    x = (w - total) / 2
    centres = []
    for text, cw, fill, edge in cards:
        cx = x + cw / 2
        centres.append((cx, cw))
        box(ax, cx, y, cw, 0.78, fill=fill, edge=edge, lw=1.5, r=0.12)
        t = note(ax, cx, y, text, size=9.6, colour=edge)
        must_fit(fig, t, cw - 0.16, text)
        x += cw + gap
    for (a, aw), (b, bw) in zip(centres, centres[1:]):
        arrow(ax, (a + aw / 2 + 0.05, y), (b - bw / 2 - 0.05, y), colour=GREY,
              lw=1.5, scale=12)

    # what actually travels between the tokenizer and the decoder
    units = ["u7", "u3", "u3", "u9", "u1", "u4"]
    span = (centres[1][0], centres[3][0])
    step = (span[1] - span[0]) / (len(units) - 1)
    for i, u in enumerate(units):
        cx = span[0] + i * step
        box(ax, cx, y - 1.02, 0.62, 0.44, fill=WHITE, edge=GREY, lw=1.1,
            r=0.08)
        t = note(ax, cx, y - 1.02, u, size=8.8, colour=GREY)
        must_fit(fig, t, 0.52, u)
    t = note(ax, (span[0] + span[1]) / 2, y - 1.58, "discrete audio units",
             size=9.4, colour=GREY)
    must_fit(fig, t, 3.20, "units label")
    report()
    save(fig, path_out)

if __name__ == "__main__":
    draw("fig11_5.png")
