"""
Figure 2.1: the source-filter model.

Second redraw. The first code-drawn version was rejected as hard to read: it
stacked a flat schematic tube, a row of three spectra and a spectrogram into one
frame, so nothing in it was large enough to carry its own explanation, and the
tube did not look like a vocal tract.

This version is built on one idea. The model says a buzz is made in one place
and reshaped in another, and the reshaping is a multiplication of spectra. So
the figure has three columns, one per stage, and each column shows the physical
thing on top and its spectrum directly underneath. Reading across the top gives
the anatomy; reading across the bottom gives source times filter equals output;
reading down a column connects the two. Nothing else is in the frame.

The spectrogram was dropped. Figure 2.4 already shows real spectrograms of real
recordings, so a synthetic one here was both redundant and the least legible
element on the page.

Every curve is computed from one list of three resonances, so the panels cannot
disagree with each other or with the caption.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from figscale import fs, lws, arr
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, FancyArrowPatch

NAVY = "#1F3864"
ORANGE = "#C55A11"
GREY = "#4A5462"
AIR = "#7C93B4"
TISSUE = "#DDE7F5"
WARM = "#FBE3D2"
PANEL = "#F7FAFE"

FORMANTS = [(650, 80), (1600, 100), (2700, 140)]    # (centre Hz, bandwidth Hz)
F0 = 120.0
FMAX = 4000.0


# --------------------------------------------------------------- the acoustics

def filt(f):
    h = np.ones_like(f, dtype=float)
    for fc, bw in FORMANTS:
        h *= (fc ** 2) / np.sqrt((fc ** 2 - f ** 2) ** 2 + (bw * f) ** 2)
    return h


def source(f):
    """Glottal harmonics at multiples of F0 under a falling envelope."""
    env = 1.0 / (1.0 + (f / 300.0) ** 2)
    h = np.zeros_like(f)
    for k in range(1, int(FMAX / F0) + 1):
        h += np.exp(-((f - k * F0) ** 2) / (2 * 16.0 ** 2))
    return env * (0.03 + h)


def db(x):
    return 20 * np.log10(np.maximum(x, 1e-9))


# ----------------------------------------------------------------- the drawing

def _catmull(points, n=24):
    """Resample a control polygon into a smooth curve, numpy only."""
    p = np.asarray(points, dtype=float)
    p = np.vstack([p[0] + (p[0] - p[1]), p, p[-1] + (p[-1] - p[-2])])
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        t = np.linspace(0, 1, n, endpoint=False)[:, None]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                          + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(p[-2][None, :])
    return np.vstack(out)


def band(path, half):
    """A filled band of varying half-width along a path: the vocal tract."""
    p = _catmull(path)
    t = np.linspace(0, 1, len(p))
    w = np.interp(t, np.linspace(0, 1, len(half)), np.asarray(half, float))
    d = np.gradient(p, axis=0)
    d /= np.linalg.norm(d, axis=1)[:, None]
    n = np.column_stack([-d[:, 1], d[:, 0]])
    return np.vstack([p + n * w[:, None], (p - n * w[:, None])[::-1]])


def panel_frame(ax, title, note):
    """Background, title and note in axes coordinates, so they stay put when
    the equal-aspect adjustment expands the data limits."""
    ax.set_axis_off()
    ax.add_patch(FancyBboxPatch((0.012, 0.012), 0.976, 0.976,
                                boxstyle="round,pad=0,rounding_size=0.03",
                                transform=ax.transAxes, facecolor=PANEL,
                                edgecolor="#C9D6E8", lw=lws(1.0), zorder=0))
    ax.text(0.5, 0.955, title, transform=ax.transAxes, ha="center", va="top",
            fontsize=fs(9.6), color=NAVY, weight="bold", zorder=6)
    ax.text(0.5, 0.072, note, transform=ax.transAxes, ha="center", va="center",
            fontsize=fs(8.0), color=GREY, linespacing=1.5, zorder=6)


def draw_source(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.6)
    ax.set_aspect("equal", adjustable="datalim")
    panel_frame(ax, "1.  Source: the vocal folds",
                "The folds chop the airflow into pulses\n"
                "at the rate F0, the pitch.")

    for x0 in (1.90, 5.60):
        ax.add_patch(FancyBboxPatch((x0, 2.45), 2.50, 1.85,
                                    boxstyle="round,pad=0,rounding_size=0.65",
                                    facecolor=TISSUE, edgecolor=NAVY,
                                    lw=lws(1.5), zorder=2))
    ax.text(5.00, 2.28, "lungs", ha="center", va="top", fontsize=fs(9.4),
            color=NAVY, zorder=6)

    ax.add_patch(Rectangle((4.45, 4.30), 1.10, 1.35, facecolor="white",
                           edgecolor=NAVY, lw=lws(1.5), zorder=2))
    ax.annotate("trachea", xy=(4.45, 4.95), xytext=(3.75, 4.95),
                ha="right", va="center", fontsize=fs(9.2), color=NAVY,
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=lws(0.9)),
                zorder=6)

    ax.annotate("", xy=(5.00, 5.55), xytext=(5.00, 4.05),
                arrowprops=dict(arrowstyle="-|>", color=AIR, lw=lws(2.4),
                                mutation_scale=arr(14)), zorder=3)
    ax.text(5.95, 4.95, "air", ha="left", va="center", fontsize=fs(9.2),
            color=AIR, weight="bold", zorder=6)

    ax.add_patch(FancyBboxPatch((4.05, 5.65), 1.90, 1.30,
                                boxstyle="round,pad=0,rounding_size=0.16",
                                facecolor=WARM, edgecolor=ORANGE,
                                lw=lws(2.0), zorder=3))
    for dy in (0.28, -0.28):
        ax.add_patch(FancyBboxPatch((4.28, 6.30 + dy - 0.09), 1.44, 0.18,
                                    boxstyle="round,pad=0,rounding_size=0.09",
                                    facecolor=ORANGE, edgecolor=ORANGE,
                                    lw=0, zorder=4))
    ax.annotate("vocal\nfolds", xy=(6.00, 6.30), xytext=(6.55, 6.30),
                ha="left", va="center", fontsize=fs(9.4), color=ORANGE,
                weight="bold", linespacing=1.35,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=lws(0.9)),
                zorder=6)


def draw_filter(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.6)
    ax.set_aspect("equal", adjustable="datalim")
    panel_frame(ax, "2.  Filter: the vocal tract",
                "The shape of the tube sets its\n"
                "resonances: the formants.")

    path = [(3.30, 2.55), (3.34, 3.35), (3.55, 4.15), (4.05, 4.85),
            (4.85, 5.35), (5.85, 5.62), (6.85, 5.72), (7.75, 5.74)]
    half = [0.30, 0.48, 0.60, 0.62, 0.56, 0.34, 0.56, 0.42]
    ax.add_patch(Polygon(band(path, half), closed=True, facecolor="white",
                         edgecolor=NAVY, lw=lws(1.8), zorder=3))

    ax.annotate("glottis", xy=(3.30, 2.62), xytext=(3.30, 1.95),
                ha="center", va="top", fontsize=fs(9.0), color=NAVY,
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=lws(0.9)),
                zorder=6)
    ax.annotate("pharynx", xy=(3.42, 4.20), xytext=(3.55, 5.40),
                ha="right", va="center", fontsize=fs(9.0), color=NAVY,
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=lws(0.9)),
                zorder=6)
    ax.annotate("the tongue narrows\nthe tube here", xy=(5.85, 5.28),
                xytext=(6.10, 3.30), ha="center", va="center",
                fontsize=fs(9.0), color=ORANGE, weight="bold",
                linespacing=1.35,
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=lws(1.3),
                                mutation_scale=arr(11)), zorder=6)
    ax.annotate("lips", xy=(7.85, 5.74), xytext=(8.35, 4.85),
                ha="left", va="center", fontsize=fs(9.0), color=NAVY,
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=lws(0.9)),
                zorder=6)


def draw_output(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.6)
    ax.set_aspect("equal", adjustable="datalim")
    panel_frame(ax, "3.  Output: speech at the lips",
                "Harmonics near a resonance come out\n"
                "strong; the rest are damped.")

    # the mouth opening
    ax.add_patch(Polygon([(2.45, 6.35), (3.25, 5.90), (3.25, 5.30),
                          (2.45, 4.85)], closed=True, facecolor=NAVY,
                         edgecolor=NAVY, lw=lws(1.0), zorder=4))
    ax.text(2.95, 4.60, "at the lips", ha="center", va="top",
            fontsize=fs(9.0), color=NAVY, zorder=6)

    th = np.linspace(-0.62, 0.62, 90)
    for k, r in enumerate((0.85, 1.40, 1.95, 2.50)):
        ax.plot(3.30 + r * np.cos(th), 5.60 + r * np.sin(th), color=NAVY,
                lw=lws(1.7 - 0.16 * k), alpha=1.0 - 0.13 * k, zorder=3)

    # the signal that actually leaves the lips, from the same three resonances
    t = np.linspace(0, 0.025, 1400)
    fh = np.arange(1, int(FMAX / F0) + 1) * F0
    amp = source(fh) * filt(fh)
    sig = (amp[:, None] * np.sin(2 * np.pi * fh[:, None] * t[None, :])).sum(0)
    sig /= np.abs(sig).max()
    ax.plot(2.30 + 5.6 * t / t[-1], 3.35 + 0.62 * sig, color=NAVY,
            lw=lws(1.2), zorder=4)
    ax.text(5.10, 2.55, "the speech signal", ha="center", va="top",
            fontsize=fs(9.0), color=NAVY, zorder=6)


# ------------------------------------------------------------------ the figure

def spectrum(ax, y, title, mark):
    f = np.linspace(1.0, FMAX, 4000)
    ax.plot(f, db(y) - db(y).max(), color=NAVY, lw=lws(1.5))
    if mark:
        for i, (fc, _b) in enumerate(FORMANTS, start=1):
            ax.axvline(fc, color=ORANGE, ls=(0, (4, 3)), lw=lws(1.1))
            ax.text(fc, 8, f"F{i}", ha="center", va="bottom",
                    fontsize=fs(9.2), color=ORANGE, weight="bold")
    ax.set_xlim(0, FMAX)
    ax.set_ylim(-88, 30)
    ax.set_title(title, fontsize=fs(9.8), color=NAVY, pad=9, linespacing=1.35)
    ax.set_xlabel("frequency (Hz)", fontsize=fs(9.0))
    ax.tick_params(labelsize=fs(8.2))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def draw(path):
    fig = plt.figure(figsize=(12.6, 8.4))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.42, 1.0],
                          hspace=0.46, wspace=0.30,
                          left=0.055, right=0.978, top=0.978, bottom=0.085)

    tops = [fig.add_subplot(gs[0, k]) for k in range(3)]
    draw_source(tops[0])
    draw_filter(tops[1])
    draw_output(tops[2])

    f = np.linspace(1.0, FMAX, 4000)
    src, flt = source(f), filt(f)
    bots = [fig.add_subplot(gs[1, k]) for k in range(3)]
    spectrum(bots[0], src, "source spectrum:\nharmonics of F0", False)
    spectrum(bots[1], flt, "filter response:\nthe formants", True)
    spectrum(bots[2], src * flt,
             "output spectrum:\nharmonics shaped by the formants", True)
    bots[0].set_ylabel("relative amplitude (dB)", fontsize=fs(9.0))

    fig.canvas.draw()

    # air and sound flow across the top row
    for k in range(2):
        a, b = tops[k].get_position(), tops[k + 1].get_position()
        y = a.y0 + (a.y1 - a.y0) * 0.52
        fig.add_artist(FancyArrowPatch((a.x1 + 0.002, y), (b.x0 - 0.002, y),
                                       transform=fig.transFigure,
                                       arrowstyle="-|>",
                                       mutation_scale=arr(16), lw=lws(2.2),
                                       color=AIR, shrinkA=0, shrinkB=0))

    # the arithmetic across the bottom row
    for k, sym in ((0, "×"), (1, "=")):
        a, b = bots[k].get_position(), bots[k + 1].get_position()
        fig.text(a.x1 + 0.30 * (b.x0 - a.x1), (a.y0 + a.y1) / 2, sym,
                 ha="center", va="center", fontsize=fs(17), color=ORANGE,
                 weight="bold")

    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(path.replace(".png", ".pdf"), bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    draw("fig2_1.png")
    print("wrote fig2_1.png/.pdf; F1/F2/F3 =", [fc for fc, _ in FORMANTS])
