"""
Figure 3.3: sampling and quantization.

Redrawn because the original artwork did not do what the figure exists to show.
Quantization rounds every sample to one of a fixed set of levels, so every
stair-step must lie exactly on a level line. In the original, several steps sat
part way between two levels, by as much as half a level in the negative half of
the wave, which is the one thing a quantization figure must not do.

Here the staircase is computed: each sample is rounded to the nearest level by
the code that draws it, so it cannot drift off a line.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figscale import fs, lws, arr

NAVY="#1F3864"; ORANGE="#C55A11"; GREY="#8A93A0"
LEVELS=3                      # levels drawn at -3D .. +3D
NSAMP=17
AMP=3.15                      # peak of the wave, in units of one level

def draw(path):
    fig, ax = plt.subplots(figsize=(12.6, 6.4))
    t=np.linspace(0, 1, 1200)
    y=AMP*np.sin(2*np.pi*t)
    ts=np.linspace(0.02, 0.98, NSAMP)
    ys=AMP*np.sin(2*np.pi*ts)
    q=np.round(ys)                                   # the quantizer itself
    q=np.clip(q, -LEVELS, LEVELS)

    for L in range(-LEVELS, LEVELS+1):
        if L==0: continue
        ax.axhline(L, color="#7C93B4", ls=(0,(5,5)), lw=lws(1.0), zorder=1)
        ax.text(-0.045, L, ("+" if L>0 else "−")+("%dΔ"%abs(L) if abs(L)>1 else "Δ"),
                ha="right", va="center", fontsize=fs(10.0), color=NAVY, zorder=4)
    ax.axhline(0, color=NAVY, lw=lws(1.4), zorder=2)
    ax.text(-0.045, 0, "0", ha="right", va="center", fontsize=fs(10.0),
            color=NAVY, zorder=4)

    ax.plot(t, y, color=GREY, lw=lws(2.6), zorder=2, solid_capstyle="round")

    # the staircase: hold each rounded value until the next sample
    xs=np.concatenate([ts, [1.0]])
    ax.step(xs, np.concatenate([q, [q[-1]]]), where="post", color=NAVY,
            lw=lws(2.0), zorder=3)
    for x0,yv,qv in zip(ts, ys, q):
        ax.plot([x0,x0],[0,yv], color=ORANGE, lw=lws(1.1), zorder=2)
    ax.plot(ts, ys, "o", ms=lws(4.2), color=ORANGE, zorder=5)

    ax.annotate("samples: measuring in time\n(the sampling rate sets how many)",
                xy=(ts[3], ys[3]), xytext=(0.20, 4.35), ha="center", va="bottom",
                fontsize=fs(9.4), color=ORANGE, weight="bold", linespacing=1.4,
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=lws(1.2),
                                mutation_scale=arr(12)), zorder=6)
    k=int(NSAMP*0.62)
    ax.annotate("quantization: rounding the value\nto the nearest level",
                xy=(ts[k]+0.012, q[k]), xytext=(0.70, -4.45), ha="center",
                va="top", fontsize=fs(9.4), color=NAVY, weight="bold",
                linespacing=1.4,
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=lws(1.2),
                                mutation_scale=arr(12)), zorder=6)
    ax.annotate("", xy=(1.045, LEVELS), xytext=(1.045, -LEVELS),
                arrowprops=dict(arrowstyle="<->", color=NAVY, lw=lws(1.3),
                                mutation_scale=arr(11)), zorder=4)
    ax.text(1.062, 0, "dynamic range\n(set by the bit depth)", ha="left",
            va="center", fontsize=fs(9.2), color=NAVY, linespacing=1.4, zorder=4)

    ax.set_xlim(-0.10, 1.30); ax.set_ylim(-5.3, 5.2)
    ax.axis("off")
    fig.tight_layout(pad=0.4)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(path.replace(".png",".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    off=np.abs(q-np.round(q)).max()
    print("largest distance from any step to a level: %.3g levels" % off)

if __name__=="__main__":
    draw("fig3_3.png"); print("wrote fig3_3.png/.pdf")
