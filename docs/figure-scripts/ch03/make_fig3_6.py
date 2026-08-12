"""
Figure 3.6: the mel filterbank.

Redrawn because the original artwork drew about 26 triangular filters while
labelling itself "~40 triangular filters", and the chapter text says "typically
about forty". A reader who counts finds a different number from the one the
figure claims.

Here the filters are computed, not drawn by hand: 40 triangles whose edges are
equally spaced on the mel scale between 0 Hz and the 8 kHz Nyquist limit of
16 kHz audio, using the standard formula. The inset plots the same formula, so
the warping shown in the inset is the warping used in the main panel.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figscale import fs, lws

NAVY="#1F3864"; ORANGE="#C55A11"; GREY="#5A6472"
NFILT=40; FMIN=0.0; FMAX=8000.0

def hz2mel(f): return 2595.0*np.log10(1.0+f/700.0)
def mel2hz(m): return 700.0*(10.0**(m/2595.0)-1.0)

def draw(path):
    edges=mel2hz(np.linspace(hz2mel(FMIN), hz2mel(FMAX), NFILT+2))
    fig=plt.figure(figsize=(12.6, 5.6))
    gs=fig.add_gridspec(1, 2, width_ratios=[2.45, 1.0], wspace=0.20,
                        left=0.062, right=0.982, top=0.88, bottom=0.20)
    ax=fig.add_subplot(gs[0,0])
    f=np.linspace(0, FMAX, 6000)
    for i in range(NFILT):
        lo,ct,hi=edges[i], edges[i+1], edges[i+2]
        tri=np.clip(np.minimum((f-lo)/(ct-lo+1e-9), (hi-f)/(hi-ct+1e-9)), 0, None)
        ax.plot(f, tri, color=ORANGE, lw=lws(1.1), zorder=3)
        ax.fill_between(f, 0, tri, color=ORANGE, alpha=0.10, zorder=2)
    ax.set_xlim(0, FMAX); ax.set_ylim(0, 1.02)
    ax.set_xlabel("frequency (Hz)", fontsize=fs(10.0), color=NAVY)
    ax.set_ylabel("filter weight", fontsize=fs(10.0), color=NAVY)
    ax.tick_params(labelsize=fs(8.6))
    for sp in ("top","right"): ax.spines[sp].set_visible(False)
    ax.set_title("mel filterbank: %d triangular filters" % NFILT,
                 fontsize=fs(10.6), color=NAVY, weight="bold", pad=9)
    ax.annotate("many narrow filters\nlow down", xy=(edges[4], 0.985),
                xytext=(1750, 0.70), ha="center", va="center",
                fontsize=fs(9.0), color=GREY, linespacing=1.4,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor="none", alpha=0.88),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=lws(1.1)))
    ax.annotate("few wide filters\nhigh up", xy=(edges[NFILT], 0.985),
                xytext=(6100, 0.66), ha="center", va="center",
                fontsize=fs(9.0), color=GREY, linespacing=1.4,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor="none", alpha=0.88),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=lws(1.1)))

    ins=fig.add_subplot(gs[0,1])
    ff=np.linspace(0, FMAX, 1000)
    ins.plot(ff, hz2mel(ff), color=ORANGE, lw=lws(2.2))
    ins.set_xlim(0, FMAX); ins.set_ylim(0, hz2mel(FMAX)*1.04)
    ins.set_xlabel("frequency (Hz)", fontsize=fs(9.0), color=NAVY)
    ins.set_ylabel("mel", fontsize=fs(9.0), color=NAVY)
    ins.tick_params(labelsize=fs(8.2))
    ins.set_title("the mel scale compresses\nhigh frequencies",
                  fontsize=fs(9.6), color=NAVY, weight="bold",
                  linespacing=1.35, pad=9)
    for sp in ("top","right"): ins.spines[sp].set_visible(False)
    ins.grid(True, color="#EDF1F7", lw=lws(0.8)); ins.set_axisbelow(True)

    fig.text(0.5, 0.045,
             "power spectrum  \u2192  mel filters  \u2192  log  \u2192  log-mel features",
             ha="center", va="center", fontsize=fs(10.0), color=NAVY,
             weight="bold")
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(path.replace(".png",".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("filters drawn: %d, first centre %.0f Hz, last centre %.0f Hz"
          % (NFILT, edges[1], edges[NFILT]))


if __name__=="__main__":
    draw("fig3_6.png"); print("wrote fig3_6.png/.pdf")
