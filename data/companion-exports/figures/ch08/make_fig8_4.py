"""
The three speaker tasks, side by side.

Redrawn at the book's type scale. No sentences inside the artwork: each panel
carries its task name, the shape of its input and output, and nothing else. The
comparison the figure exists to make is drawn rather than described, by giving
the three panels the same left-to-right skeleton so that what differs between
them is visible as a difference in shape.
"""
import numpy as np
from matplotlib.patches import Rectangle
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save)
from figscale import fs, lws
from figfit import must_fit, report

PW, PH = 3.95, 4.45
BW, BH = 2.60, 0.68


def draw(path_out):
    w, h = 12.6, 5.4
    fig, ax = canvas(w, h, (0, w), (0, h))
    xs = [0.30 + PW / 2 + i * (PW + 0.28) for i in range(3)]
    ptop = h - 0.30
    pcy = ptop - PH / 2

    for cx, title in zip(xs, ("identification", "verification", "diarization")):
        ax.add_patch(Rectangle((cx - PW / 2, ptop - PH), PW, PH,
                               facecolor="none", edgecolor="#C9D6E8",
                               lw=lws(1.0), zorder=1))
        t = note(ax, cx, ptop - 0.34, title, size=11.0, colour=NAVY,
                 weight="bold")
        must_fit(fig, t, PW - 0.20, title)

    yin, ymid, yout = ptop - 1.15, ptop - 2.42, ptop - 3.90

    def card(cx, y, label, fill=WHITE, edge=NAVY, bw=BW, bh=BH, size=9.6):
        box(ax, cx, y, bw, bh, fill=fill, edge=edge, lw=1.4, r=0.10)
        t = note(ax, cx, y, label, size=size, colour=edge, weight="bold",
                 linespacing=1.45)
        must_fit(fig, t, bw - 0.16, max(label.split("\n"), key=len))

    # ---- 1: one utterance against a closed gallery -----------------------
    cx = xs[0]
    card(cx, yin, "one utterance", BOXFILL)
    gy = ymid + 0.32
    for k in range(3):
        yy = gy - k * 0.38
        box(ax, cx, yy, BW - 0.55, 0.30, fill=WHITE, edge=GREY, lw=1.1, r=0.06)
    note(ax, cx, gy - 1.20, "gallery of N enrolled speakers", size=9.0,
         colour=GREY)
    arrow(ax, (cx, yin - BH / 2 - 0.03), (cx, gy + 0.26))
    card(cx, yout, "which speaker", GREENFILL, GREEN)
    arrow(ax, (cx, gy - 1.44), (cx, yout + BH / 2 + 0.03), colour=GREEN)

    # ---- 2: one utterance against one claim ------------------------------
    cx = xs[1]
    card(cx - 0.82, yin, "one\nutterance", BOXFILL, bw=1.58, bh=0.86, size=9.2)
    card(cx + 0.82, yin, "a claimed\nidentity", BOXFILL, bw=1.58, bh=0.86,
         size=9.2)
    card(cx, ymid, "compare", WHITE, ORANGE, bw=1.90)
    arrow(ax, (cx - 0.82, yin - 0.46), (cx - 0.42, ymid + BH / 2 + 0.03))
    arrow(ax, (cx + 0.82, yin - 0.46), (cx + 0.42, ymid + BH / 2 + 0.03))
    card(cx, yout, "accept or reject", GREENFILL, GREEN)
    arrow(ax, (cx, ymid - BH / 2 - 0.03), (cx, yout + BH / 2 + 0.03),
          colour=GREEN)

    # ---- 3: one recording, a timeline out --------------------------------
    cx = xs[2]
    card(cx, yin, "one recording,\nseveral talkers", BOXFILL, bh=0.86,
         size=9.2)
    tl_x0, tl_x1 = cx - PW / 2 + 0.42, cx + PW / 2 - 0.42
    tl_y = ymid - 0.05
    # who = 0 is the upper row, and the upper row is speaker A
    spans = [(0.00, 0.26, 0), (0.30, 0.58, 1), (0.58, 0.72, 0),
             (0.76, 1.00, 1)]
    for a, b, who in spans:
        x0 = tl_x0 + a * (tl_x1 - tl_x0)
        x1 = tl_x0 + b * (tl_x1 - tl_x0)
        ax.add_patch(Rectangle((x0, tl_y + 0.24 - who * 0.44), x1 - x0, 0.34,
                               facecolor=BOXFILL if who == 0 else "#F6E3D8",
                               edgecolor=NAVY if who == 0 else ORANGE,
                               lw=lws(1.2), zorder=4))
    note(ax, tl_x0 - 0.10, tl_y + 0.41, "A", size=9.6, colour=NAVY,
         weight="bold", ha="right")
    note(ax, tl_x0 - 0.10, tl_y - 0.03, "B", size=9.6, colour=ORANGE,
         weight="bold", ha="right")
    note(ax, cx, tl_y - 0.62, "time", size=9.0, colour=GREY)
    arrow(ax, (cx, yin - 0.49), (cx, tl_y + 0.76))
    card(cx, yout, "who spoke when", GREENFILL, GREEN)
    arrow(ax, (cx, tl_y - 0.84), (cx, yout + BH / 2 + 0.03), colour=GREEN)

    report()
    save(fig, path_out)
    print("wrote", path_out)


if __name__ == "__main__":
    draw("fig8_4.png")
