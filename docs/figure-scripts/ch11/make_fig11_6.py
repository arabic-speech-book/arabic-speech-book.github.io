"""
Figure 11.6: the speech agent loop, drawn as a loop.

Four stages and a cycle. The two marked in orange are the ones that make an
agent an agent rather than a chat model with a microphone: it can look something
up, and it can do something. The note in the middle says what those two buy,
and the note beneath says where an Arabic system loses it.
"""
import math
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save)
from figfit import must_fit, report

STAGES = [
    ("perceive", "listening and recognition", NAVY, BOXFILL),
    ("plan", "reasoning over the input", NAVY, WHITE),
    ("act", "retrieval or a tool call", ORANGE, WHITE),
    ("respond", "the spoken reply", GREEN, GREENFILL),
]

def draw(path_out):
    w, h = 12.6, 5.10
    fig, ax = canvas(w, h, (0, w), (0, h))
    cx, cy = 6.30, 2.65
    rx, ry = 3.95, 1.60
    bw, bh = 3.10, 0.94
    pts = [(cx, cy + ry), (cx + rx, cy), (cx, cy - ry), (cx - rx, cy)]
    for (x, y), (title, sub, edge, fill) in zip(pts, STAGES):
        box(ax, x, y, bw, bh, fill=fill, edge=edge, lw=1.6, r=0.12)
        t = note(ax, x, y + 0.17, title, size=10.2, colour=edge, weight="bold")
        must_fit(fig, t, bw - 0.16, title)
        t = note(ax, x, y - 0.19, sub, size=9.0, colour=GREY)
        must_fit(fig, t, bw - 0.16, sub)
    for i in range(4):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % 4]
        dx, dy = x1 - x0, y1 - y0
        n = math.hypot(dx, dy)
        ux, uy = dx / n, dy / n
        pad0 = bw / 2 * 0.62 + 0.10
        pad1 = bw / 2 * 0.62 + 0.10
        arrow(ax, (x0 + ux * pad0, y0 + uy * (bh / 2 + 0.06) if abs(uy) > abs(ux) else y0 + uy * pad0),
              (x1 - ux * pad1, y1 - uy * (bh / 2 + 0.06) if abs(uy) > abs(ux) else y1 - uy * pad1),
              colour=GREY, lw=1.5, scale=12)
    t = note(ax, cx, cy, "one turn", size=9.6, colour=GREY)
    must_fit(fig, t, 2.00, "centre")
    report()
    save(fig, path_out)

if __name__ == "__main__":
    draw("fig11_6.png")
