"""
Figure 10.5: intent, slots and dialogue state across two Arabic turns.

Section 10.7 names three tasks and Table 10.3 sets out what each one maps from
and to, but a table cannot show the one thing that separates dialogue state
tracking from the other two: the state is what survives when the turn is over.
That needs two turns side by side, and the second turn has to be the kind that
carries no intent of its own, because that is the case a single-turn diagram
never reaches.

The utterance in the first turn is the chapter's opening example, so a reader
arrives here already knowing it. The second turn is a fragment, the way people
actually add a detail to a request they have already made. It adds one slot,
names no intent, and the state after it holds everything from both turns.

The Arabic difficulty of Section 10.7 is visible in the artwork rather than
asserted beside it: the values leave the turn in Arabic and enter the state in
the form an ontology holds, and the footnote says what has to happen in
between.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save, ar, ARF)
from figscale import lws
from figfit import must_fit, report

TURNS = [
    {
        "arabic": "احجز رحلة إلى الرياض غدًا",
        "translit": "iḥjiz riḥla ilā ar-riyāḍ ghadan",
        "gloss": "‘book a flight to Riyadh tomorrow’",
        "tag": "turn 1",
        "chips": [("intent", "book_flight", ORANGE, WHITE),
                  ("slot", "destination = Riyadh", NAVY, WHITE),
                  ("slot", "date = tomorrow", NAVY, WHITE)],
        "state": [("book_flight", ORANGE),
                  ("destination = Riyadh", NAVY),
                  ("date = tomorrow", NAVY)],
    },
    {
        "arabic": "بدرجة الأعمال",
        "translit": "bi-darajat al-aʿmāl",
        "gloss": "‘in business class’",
        "tag": "turn 2",
        "chips": [("intent", "book_flight continues", GREY, WHITE),
                  ("slot", "class = business", GREEN, GREENFILL)],
        "state": [("book_flight", ORANGE),
                  ("destination = Riyadh", NAVY),
                  ("date = tomorrow", NAVY),
                  ("class = business", GREEN)],
    },
]

COL1, COL2, COL3 = 2.00, 6.55, 10.85
TW, CW, SW = 3.80, 4.30, 3.20
CHIP_H, LINE_H = 0.46, 0.40

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


def turn_box(fig, ax, y, turn):
    h = 1.34
    box(ax, COL1, y, TW, h, fill=BOXFILL, edge=NAVY, lw=1.5, r=0.12)
    t = note(ax, COL1, y + 0.36, ar(turn["arabic"]), size=12.4, colour=NAVY,
             fontproperties=ARF)
    must_fit(fig, t, TW - 0.20, turn["tag"] + " Arabic")
    t = note(ax, COL1, y + 0.01, turn["translit"], size=8.8, colour=GREY,
             style="italic")
    must_fit(fig, t, TW - 0.20, turn["translit"])
    t = note(ax, COL1, y - 0.32, turn["gloss"], size=8.8, colour=GREY)
    must_fit(fig, t, TW - 0.20, turn["gloss"])
    t = note(ax, COL1 - TW / 2, y + h / 2 + 0.17, turn["tag"], size=9.4,
             colour=NAVY, weight="bold", ha="left", va="center")
    must_fit(fig, t, 1.40, turn["tag"])
    return h


def chips(fig, ax, y, turn):
    n = len(turn["chips"])
    ys = [y + (n - 1) / 2 * (CHIP_H + 0.14) - i * (CHIP_H + 0.14)
          for i in range(n)]
    for cy, (kind, text, edge, fill) in zip(ys, turn["chips"]):
        box(ax, COL2, cy, CW, CHIP_H, fill=fill, edge=edge, lw=1.4, r=0.10)
        t = note(ax, COL2 - CW / 2 + 0.16, cy, kind, size=8.4, colour=GREY,
                 ha="left", va="center")
        must_fit(fig, t, 0.70, kind)
        t = note(ax, COL2 + 0.30, cy, text, size=9.6, colour=edge,
                 weight="bold")
        must_fit(fig, t, CW - 1.10, text)
    return ys


def state_panel(fig, ax, y, turn, mark_last):
    lines = turn["state"]
    h = len(lines) * LINE_H + 0.44
    box(ax, COL3, y, SW, h, fill=WHITE, edge=EDGE_LIGHT, lw=1.4, r=0.12)
    t = note(ax, COL3, y + h / 2 - 0.20, "dialogue state", size=8.6,
             colour=GREY, weight="bold")
    must_fit(fig, t, SW - 0.30, "dialogue state")
    top = y + h / 2 - 0.52
    for i, (text, colour) in enumerate(lines):
        cy = top - i * LINE_H
        fresh = mark_last and i == len(lines) - 1
        if fresh:
            box(ax, COL3, cy, SW - 0.34, LINE_H - 0.06, fill=GREENFILL,
                edge=GREEN, lw=1.2, r=0.08)
        t = note(ax, COL3, cy, text, size=9.4, colour=colour,
                 weight="bold" if fresh else "normal")
        must_fit(fig, t, SW - 0.50, text)
    return h


def draw(path_out):
    w, h = 12.6, 5.90
    fig, ax = canvas(w, h, (0, w), (0, h))

    heads = [(COL1, "the turn"), (COL2, "what understanding produces"),
             (COL3, "the state after the turn")]
    for x, text in heads:
        t = note(ax, x, 5.62, text, size=10.0, colour=NAVY, weight="bold")
        must_fit(fig, t, 4.20, text)
        inside(fig, t, text)

    y1, y2 = 4.20, 1.60
    panel_h = []
    for y, turn, mark in ((y1, TURNS[0], False), (y2, TURNS[1], True)):
        th = turn_box(fig, ax, y, turn)
        cys = chips(fig, ax, y, turn)
        ph = state_panel(fig, ax, y, turn, mark)
        panel_h.append(ph)
        arrow(ax, (COL1 + TW / 2 + 0.05, y), (COL2 - CW / 2 - 0.05, y))
        arrow(ax, (COL2 + CW / 2 + 0.05, y), (COL3 - SW / 2 - 0.05, y))
        del th, cys

    # the state is the one thing that crosses the turn boundary
    top_bottom = y1 - panel_h[0] / 2
    next_top = y2 + panel_h[1] / 2
    arrow(ax, (COL3, top_bottom - 0.04), (COL3, next_top + 0.04), colour=GREEN)
    t = note(ax, COL3 - 0.16, (top_bottom + next_top) / 2, "carried forward",
             size=8.8, colour=GREEN, ha="right")
    must_fit(fig, t, 1.60, "carried forward")
    inside(fig, t, "carried forward")

    if BOUNDS:
        raise SystemExit('a label hangs off the page:\n  ' +
                         '\n  '.join(BOUNDS))
    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig10_5.png")
