"""
Figure 6.6: what a pooled Word Error Rate hides.

Redrawn at the book's type scale. The original grouped bar chart printed at
about 4 to 6 pt and one legend entry sat on top of a data label. Two changes of
substance. The bars are told apart by hatching as well as by colour, so the
comparison survives a greyscale printing, and the pooled average is drawn as a
line across the chart, because the figure exists to make the point that the
pooled number can sit comfortably below three of the four varieties. Without
that line the reader has to imagine it.

The numbers are illustrative and the artwork says so. They are drawn to be
plausible rather than measured: a pooled test set dominated by Modern Standard
Arabic, a modest gain on MSA, and a much larger remaining gap on the dialects.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from bookstyle import NAVY, ORANGE, GREY, save
from figscale import fs, lws

VARIETIES = ["Modern Standard\nArabic", "Gulf", "Egyptian", "Maghrebi"]
BEFORE = [14, 39, 35, 56]
AFTER = [10, 26, 23, 42]
SHARE = [0.70, 0.10, 0.10, 0.10]        # of the pooled test set
POOLED = sum(a * s for a, s in zip(AFTER, SHARE))


def draw(path_out):
    fig = plt.figure(figsize=(12.6, 7.0))
    ax = fig.add_axes([0.075, 0.235, 0.905, 0.715])

    x = range(len(VARIETIES))
    w = 0.34

    b1 = ax.bar([i - w / 2 for i in x], BEFORE, w, facecolor="white",
                edgecolor=NAVY, lw=lws(1.6), hatch="////", zorder=3,
                )
    b2 = ax.bar([i + w / 2 for i in x], AFTER, w, facecolor="#DCE5F2",
                edgecolor=NAVY, lw=lws(1.6), zorder=3)

    for bars in (b1, b2):
        for r in bars:
            ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 1.4,
                    f"{r.get_height():.0f}", ha="center", va="bottom",
                    fontsize=fs(9.4), color=NAVY, weight="bold", zorder=5)

    ax.axhline(POOLED, color=ORANGE, lw=lws(1.8), linestyle=(0, (6, 4)),
               zorder=4)

    ax.set_xticks(list(x))
    ax.set_xticklabels(VARIETIES, fontsize=fs(10.0), color=NAVY,
                       linespacing=1.5)
    ax.set_ylim(0, 66)
    ax.set_yticks([0, 10, 20, 30, 40, 50, 60])
    ax.tick_params(axis="both", labelsize=fs(9.6), colors=NAVY,
                   width=lws(1.2), length=6 * 1.7)
    ax.set_ylabel("Word Error Rate (%), lower is better",
                  fontsize=fs(10.4), color=NAVY, weight="bold",
                  labelpad=8 * 1.7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(NAVY)
        ax.spines[s].set_linewidth(lws(1.4))
    ax.grid(axis="y", color="#E2E7F0", lw=lws(0.9), zorder=0)
    ax.set_axisbelow(True)

    pooled_handle = Line2D([], [], color=ORANGE, lw=lws(1.8),
                           linestyle=(0, (6, 4)))
    handles = [b1, b2, pooled_handle]
    labels = ["before Arabic fine-tuning", "after Arabic fine-tuning",
              f"pooled average after fine-tuning, {POOLED:.0f}%"]
    leg = ax.legend(handles, labels, loc="upper left", fontsize=fs(9.8),
                    frameon=False, handlelength=2.2, borderpad=0.2,
                    labelspacing=0.7)
    for t, c in zip(leg.get_texts(), (NAVY, NAVY, ORANGE)):
        t.set_color(c)
    leg.get_texts()[2].set_weight("bold")

    ax.text(0.985, 0.995, "illustrative numbers, not a measurement",
            transform=ax.transAxes, fontsize=fs(9.4), color=GREY,
            style="italic", ha="right", va="top")

    fig.text(0.075, 0.105,
             "Every variety improves, and because the pooled test set is "
             "mostly MSA the single average sits below three of the four "
             "varieties. Quoting only\nthat average would suggest the model "
             "handles Arabic well, when Maghrebi speech is still "
             "misrecognized four times as often as MSA. Report each\nvariety "
             "separately, on spontaneous speech rather than read benchmarks.",
             fontsize=fs(9.2), color=NAVY, va="top", linespacing=1.7)

    save(fig, path_out)


if __name__ == "__main__":
    draw("fig6_6.png")
    print("pooled after fine-tuning:", round(POOLED, 2))
