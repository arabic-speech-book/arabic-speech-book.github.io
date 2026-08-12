"""
Figure 10.3: a wait-k policy on a time axis, not a step axis.

The draft's version drew source and target tokens as two rows of boxes with a
bracket labelled "lag". That is the textbook picture of wait-k and it hides the
thing the chapter's own text says matters: the axis is time. A reader who takes
the token picture literally will report a latency in decoding steps, which is
not a number anyone waiting for a translation can feel.

So the axis is seconds, drawn once and shared by both lanes, and the lag is
marked twice: in words, which is what the policy is defined in, and in seconds,
which is what a listener experiences. The two are only equal when the speaker
speaks at a constant rate, and the caption says so.

The lag drawn is k = 3 at a speaking rate of one word every 0.6 s, so the
policy's three-word lag is 1.8 s. Both numbers are computed from those two
choices rather than typed, so they cannot drift apart.
"""
from bookstyle import (NAVY, ORANGE, GREEN, WHITE, BOXFILL, GREY,
                       canvas, box, note, arrow, save)
from figscale import lws
from figfit import must_fit, report

K = 3
RATE = 0.6              # seconds per source word
N_SRC = 8
N_TGT = N_SRC - K
LAG_S = K * RATE

X0, X1 = 2.20, 12.20    # the time axis, drawn once
T_MAX = (N_SRC - 1) * RATE + 1.0
BW, BH = 0.92, 0.62


def tx(t):
    return X0 + (X1 - X0) * t / T_MAX


def lane(fig, ax, y, n, start_word, colour, fill, prefix):
    xs = []
    for i in range(n):
        t = (start_word + i) * RATE
        x = tx(t)
        xs.append(x)
        box(ax, x, y, BW, BH, fill=fill, edge=colour, lw=1.4, r=0.10)
        lab = f"{prefix}{i + 1}"
        a = note(ax, x, y, lab, size=9.2, colour=colour, weight="bold")
        must_fit(fig, a, BW - 0.10, lab)
    return xs


def draw(path_out):
    w, h = 12.6, 4.30
    fig, ax = canvas(w, h, (0, w), (0, h))
    y_src, y_tgt, y_axis = 3.40, 1.55, 0.72

    t = note(ax, 0.10, y_src, "source", size=10.0, colour=NAVY, weight="bold",
             ha="left", va="center")
    must_fit(fig, t, 1.90, "source")
    t = note(ax, 0.10, y_tgt, "target", size=10.0, colour=ORANGE,
             weight="bold", ha="left", va="center")
    must_fit(fig, t, 1.90, "target")

    src = lane(fig, ax, y_src, N_SRC, 0, NAVY, BOXFILL, "s")
    tgt = lane(fig, ax, y_tgt, N_TGT, K, ORANGE, "#FCEDE3", "t")

    # the time axis, shared
    ax.annotate("", xy=(X1 + 0.30, y_axis), xytext=(X0 - 0.55, y_axis),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=lws(1.3),
                                mutation_scale=13, shrinkA=0, shrinkB=0),
                zorder=3)
    for i in range(0, N_SRC + 1, 2):
        t_s = i * RATE
        x = tx(t_s)
        ax.plot([x, x], [y_axis - 0.10, y_axis + 0.10], color=GREY,
                lw=lws(1.3), zorder=3)
        a = note(ax, x, y_axis - 0.30, f"{t_s:.1f} s", size=8.8, colour=GREY)
        must_fit(fig, a, 1.20, f"{t_s:.1f} s")
    a = note(ax, X1 + 0.34, y_axis + 0.26, "time", size=9.2, colour=GREY,
             ha="right")
    must_fit(fig, a, 1.20, "time")

    # the lag, marked in words and in seconds
    xa, xb = src[K], tgt[0]
    ax.plot([xa, xa], [y_src - BH / 2 - 0.05, y_tgt + BH / 2 + 0.05],
            color=GREY, lw=lws(1.1), ls=(0, (3, 3)), zorder=3)
    ax.plot([xb, xb], [y_src - BH / 2 - 0.05, y_tgt + BH / 2 + 0.05],
            color=GREY, lw=lws(1.1), ls=(0, (3, 3)), zorder=3)
    ymid = (y_src + y_tgt) / 2
    arrow(ax, (tx(0) + 0.02, ymid), (xb - 0.02, ymid), lw=1.5, scale=13)
    label = f"lag: {K} words, {LAG_S:.1f} s at this rate"
    a = note(ax, (tx(0) + xb) / 2, ymid + 0.28, label, size=9.2, colour=ORANGE)
    must_fit(fig, a, xb - tx(0) + 1.60, label)

    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig10_3.png")
