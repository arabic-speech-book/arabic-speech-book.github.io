"""
Figure 11.4: one instruction-tuning example, and why the format teaches routing.

The draft's specification asked for three stacked rows and a faded stack of
further examples. What makes the format work is not that there are many
examples, it is that the same audio appears with different instructions, so the
model cannot succeed by mapping audio straight to one output. The figure draws
that directly: one audio row, three instruction rows branching from it, and
three different targets.
"""
from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       EDGE_LIGHT, canvas, box, note, arrow, save)
from figfit import must_fit, report

PAIRS = [
    ("transcribe the speech", "the Arabic transcript"),
    ("identify the dialect", "Gulf"),
    ("translate it into English", "the English translation"),
]

def draw(path_out):
    w, h = 12.6, 4.25
    fig, ax = canvas(w, h, (0, w), (0, h))

    box(ax, 1.85, 2.30, 2.90, 1.10, fill=BOXFILL, edge=NAVY, lw=1.5, r=0.12)
    t = note(ax, 1.85, 2.30, "one audio clip", size=10.0, colour=NAVY,
             weight="bold")
    must_fit(fig, t, 2.70, "audio")

    ys = [3.45, 2.30, 1.15]
    for y, (instr, target) in zip(ys, PAIRS):
        box(ax, 6.05, y, 4.00, 0.62, fill=WHITE, edge=ORANGE, lw=1.4, r=0.10)
        t = note(ax, 6.05, y, instr, size=9.8, colour=ORANGE)
        must_fit(fig, t, 3.80, instr)
        box(ax, 10.60, y, 3.20, 0.62, fill=GREENFILL, edge=GREEN, lw=1.4,
            r=0.10)
        t = note(ax, 10.60, y, target, size=9.8, colour=GREEN)
        must_fit(fig, t, 3.00, target)
        arrow(ax, (3.35, 2.30), (4.00, y), colour=GREY, lw=1.3, scale=11)
        arrow(ax, (8.10, y), (8.95, y), colour=GREY, lw=1.3, scale=11)

    t = note(ax, 6.05, 4.20, "the instruction", size=9.4, colour=GREY)
    must_fit(fig, t, 3.00, "instruction head")
    t = note(ax, 10.60, 4.20, "the target answer", size=9.4, colour=GREY)
    must_fit(fig, t, 3.00, "target head")
    report()
    save(fig, path_out)

if __name__ == "__main__":
    draw("fig11_4.png")
