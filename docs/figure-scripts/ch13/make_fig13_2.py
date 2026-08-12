"""Figure 13.2: voice anonymization, drawn with the measurement attached.

The draft's specification was a four-card pipeline ending in anonymized speech.
Drawn that way the figure says anonymization happened and stops, which is the
one thing the chapter says a reader must not conclude. Anonymization is a claim
about two quantities at once: whether an attacker can still find the speaker,
and whether the words and the dialect survived. Both are measured, and a method
that answers only one of them has not been evaluated.

So the pipeline runs across the middle and the anonymized audio fans out to the
two things that are run on it, the attacker on one side and the recognizer on
the other, each with the quantity it produces. That is the whole protocol in
one picture.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

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
    w, h = 12.6, 4.35
    fig, ax = canvas(w, h, (0, w), (0, h))
    y = 3.55
    bw, bh = 2.45, 0.92

    stages = [
        (1.50, "speech that\nidentifies you", BOXFILL, NAVY),
        (4.30, "split content\nfrom identity", WHITE, NAVY),
        (7.10, "put a different\nidentity back", WHITE, NAVY),
        (9.90, "anonymized\nspeech", GREENFILL, GREEN),
    ]
    for cx, text, fill, edge in stages:
        box(ax, cx, y, bw, bh, fill=fill, edge=edge, lw=1.5, r=0.12)
        t = note(ax, cx, y, text, size=9.4, colour=edge)
        must_fit(fig, t, bw - 0.16, text.replace("\n", " "))
        inside(fig, t, text.replace("\n", " "))
    for a, b in zip([s[0] for s in stages], [s[0] for s in stages][1:]):
        arrow(ax, (a + bw / 2 + 0.06, y), (b - bw / 2 - 0.06, y), colour=ORANGE,
              lw=1.5, scale=12)

    # The two measurements hang below the anonymized audio rather than
    # continuing the row, because they are not the next stage: they are two
    # things run on the same file, and a claim about anonymization is a claim
    # about both of them at once.
    cy = 1.55
    tests = [(8.55, "an attacker", "did it stay hidden", ORANGE),
             (11.25, "a recognizer", "did the words survive", NAVY)]
    for cx, who, asks, colour in tests:
        box(ax, cx, cy, 2.30, 0.70, fill=WHITE, edge=colour, lw=1.5, r=0.10)
        t = note(ax, cx, cy, who, size=9.4, colour=colour, weight="bold")
        must_fit(fig, t, 2.14, who)
        inside(fig, t, who)
        arrow(ax, (9.90 + (cx - 9.90) * 0.22, y - bh / 2 - 0.06),
              (cx, cy + 0.35 + 0.06), colour=colour, lw=1.4, scale=11)
        t = note(ax, cx, cy - 0.62, asks, size=8.8, colour=GREY)
        must_fit(fig, t, 2.60, asks)
        inside(fig, t, asks)

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig13_2.png")
