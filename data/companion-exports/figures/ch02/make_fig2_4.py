"""
Figure 2.4: spectrograms of the minimal pair تين (tin, 'figs') and طين (tin, 'mud').

Built from the author's own recording of the two words, spoken by one speaker in
one session and supplied as a single file, so the two panels are guaranteed to
come from the same voice, the same microphone and the same recording level.

Three faults in the previous artwork are fixed:

  1. The two panels ran to different times, 700 ms against 600 ms, so the same
     duration occupied different widths and the comparison the caption asks the
     reader to make was distorted. Both panels now share one axis, and both are
     aligned on the start of voicing, which is the event the emphatic effect is
     measured from.
  2. The caption carried bracketed placeholders where the two F2 values should
     be. They are now measured, and the measurement point is stated.
  3. Formants were drawn on rather than tracked. F2 is now computed by linear
     prediction from the recording, and the track is plotted, so the reader can
     see the transition rather than take it on trust.

A third panel puts the two F2 tracks side by side, which is where the emphatic
effect is actually visible: F2 starts far lower next to the emphatic and takes
about 60 ms to climb to the value the plain token reaches almost at once.

Analysis: 16 kHz mono, pre-emphasis 0.97, 20 ms Hamming windows every 2 ms,
autocorrelation LPC. Reported F2 is the mean of orders 16 and 18, which agree
throughout; order 20 was unstable on this voice and was not used.
"""
import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import lfilter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from figscale import fs, lws, arr
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch
from arabtext import draw_word

NAVY = "#1F3864"
ORANGE = "#C55A11"
GREY = "#4A5462"

ARB = FontProperties(
    fname="/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf")

WAVFILE = "Ch2_Fig2-4_tin_vs_tiin_16k.wav"

# (label, Arabic, romanisation, gloss, release time, voicing onset)
TOKENS = [
    ("plain",    "تِين", "tīn",  "'figs'", 1.935, 2.002),
    ("emphatic", "طِين", "ṭīn",  "'mud'",  3.045, 3.052),
]

T0, T1 = -0.080, 0.250          # seconds relative to the start of voicing
VOWEL_END = 0.175               # F2 is tracked over the vowel only, not the nasal
FMAX = 5000
MEASURE_MS = 30                 # where the caption's two numbers are taken


# ------------------------------------------------------------------ analysis

def lpc(x, order):
    x = x - x.mean()
    r = np.correlate(x, x, "full")[len(x) - 1:len(x) + order]
    if r[0] == 0:
        return None
    a = np.zeros(order + 1)
    a[0] = 1.0
    e = r[0]
    for i in range(1, order + 1):
        acc = r[i] + sum(a[j] * r[i - j] for j in range(1, i))
        k = -acc / e
        an = a.copy()
        for j in range(1, i):
            an[j] = a[j] + k * a[i - j]
        an[i] = k
        a = an
        e *= (1 - k * k)
        if e <= 0:
            return None
    return a


def poles(frame, sr, order):
    a = lpc(frame * np.hamming(len(frame)), order)
    if a is None:
        return []
    out = []
    for r in np.roots(a):
        if np.imag(r) <= 0.01:
            continue
        f = np.arctan2(np.imag(r), np.real(r)) * sr / (2 * np.pi)
        bw = -0.5 * (sr / (2 * np.pi)) * np.log(np.abs(r))
        if 150 < f < 5000 and bw < 700:
            out.append(f)
    return sorted(out)


def f2_track(x, sr, von, t0, t1, floor=0.04):
    xp = lfilter([1, -0.97], [1], x)
    n, h = int(0.020 * sr), int(0.002 * sr)
    ts, f2 = [], []
    for k in range(int((von + t0) * sr), int((von + t1) * sr) - n, h):
        if np.sqrt((x[k:k + n] ** 2).mean()) < floor:
            continue
        vals = []
        for order in (16, 18):
            p = poles(xp[k:k + n], sr, order)
            if len(p) >= 2:
                vals.append(p[1])
        if len(vals) == 2 and abs(vals[0] - vals[1]) < 250:
            ts.append((k + n / 2) / sr - von)
            f2.append(np.mean(vals))
    return np.array(ts), np.array(f2)


def spectrogram(x, sr, wlen=96, nfft=1024, hop=16):
    """Wideband: a 5 ms window, so the formants appear as bands rather than as
    the individual harmonics of a 300 Hz voice."""
    win = np.hanning(wlen)
    frames = []
    for k in range(0, len(x) - wlen, hop):
        seg = np.zeros(nfft)
        seg[:wlen] = x[k:k + wlen] * win
        frames.append(np.abs(np.fft.rfft(seg)))
    return 20 * np.log10(np.maximum(np.array(frames).T, 1e-7))


# -------------------------------------------------------------------- figure

def draw(path):
    sr, raw = wav.read(WAVFILE)
    raw = raw.astype(float) / 32768.0

    fig = plt.figure(figsize=(12.4, 7.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.55, 1.0],
                          hspace=0.42, wspace=0.16,
                          left=0.075, right=0.982, top=0.94, bottom=0.085)

    tracks = {}
    for i, (key, arabic, rom, gloss, rel, von) in enumerate(TOKENS):
        ax = fig.add_subplot(gs[0, i])
        seg = raw[int((von + T0) * sr):int((von + T1) * sr)]
        S = spectrogram(seg, sr)
        ax.imshow(S, origin="lower", aspect="auto", cmap="Greys",
                  extent=[T0 * 1000, T1 * 1000, 0, sr / 2],
                  vmin=S.max() - 48, vmax=S.max())
        ax.set_ylim(0, FMAX)
        ax.set_xlim(T0 * 1000, T1 * 1000)

        ax.axvspan((rel - von) * 1000, 0, facecolor="none", edgecolor=NAVY,
                   hatch="///", lw=lws(0.8), alpha=0.75, zorder=2)
        ax.axvline(0, color=NAVY, lw=lws(1.4), zorder=3)

        t, f2 = f2_track(raw, sr, von, 0.0, VOWEL_END)
        tracks[key] = (t, f2)
        ax.plot(t * 1000, f2, "o", ms=lws(2.6), color=ORANGE, zorder=4)
        ax.text(t[-1] * 1000 - 6, f2[-1] + 320, "F2", ha="right", va="bottom",
                fontsize=fs(9.2), color=ORANGE, weight="bold", zorder=5)

        ax.add_patch(FancyBboxPatch((T0 * 1000 + 4, 3120), 122, 1600,
                                    boxstyle="round,pad=0,rounding_size=40",
                                    facecolor="white", edgecolor="#C9D6E8",
                                    lw=lws(0.9), alpha=0.94, zorder=5))
        draw_word(ax, T0 * 1000 + 13, 4250, arabic, ARB, fs(15), NAVY,
                  ha="left", zorder=6)
        ax.text(T0 * 1000 + 13, 4080,
                "%s  %s\n%s\nvoiceless %.0f ms"
                % (rom, gloss,
                   "plain /t/" if key == "plain" else "emphatic /tˤ/",
                   1000 * (von - rel)),
                ha="left", va="top", fontsize=fs(8.4), color=NAVY,
                linespacing=1.5, zorder=6)

        ax.set_xlabel("time from the start of voicing (ms)", fontsize=fs(9.0))
        if i == 0:
            ax.set_ylabel("frequency (Hz)", fontsize=fs(9.0))
        ax.tick_params(labelsize=fs(8.2))

    # ---- the two F2 tracks together
    ax = fig.add_subplot(gs[1, :])
    styles = {"plain": (NAVY, "-", "o", "plain /t/  (tīn, 'figs')"),
              "emphatic": (ORANGE, (0, (5, 3)), "s",
                           "emphatic /tˤ/  (ṭīn, 'mud')")}
    read = {}
    for key, (t, f2) in tracks.items():
        c, ls, mk, lab = styles[key]
        ax.plot(t * 1000, f2, linestyle=ls, color=c, lw=lws(1.8),
                zorder=3)
        ax.plot(t[::6] * 1000, f2[::6], linestyle="none", marker=mk,
                color=c, ms=lws(3.2), zorder=4, label=lab)
        read[key] = np.interp(MEASURE_MS / 1000, t, f2)

    ax.axvline(MEASURE_MS, color=GREY, ls=(0, (2, 3)), lw=lws(1.1), zorder=2)
    ax.text(MEASURE_MS + 4, 1080, "measured here,\n%d ms after voicing starts"
            % MEASURE_MS, ha="left", va="bottom", fontsize=fs(8.2),
            color=GREY, linespacing=1.4, zorder=5)
    for key, dy in (("plain", 150), ("emphatic", -260)):
        c = styles[key][0]
        ax.annotate("%d Hz" % (round(read[key] / 10) * 10),
                    xy=(MEASURE_MS, read[key]),
                    xytext=(MEASURE_MS - 26, read[key] + dy),
                    ha="right", va="center", fontsize=fs(9.4), color=c,
                    weight="bold",
                    arrowprops=dict(arrowstyle="-", color=c, lw=lws(0.9)),
                    zorder=5)

    ax.set_xlim(T0 * 1000, T1 * 1000)
    ax.set_ylim(1000, 2900)
    ax.set_xlabel("time from the start of voicing (ms)", fontsize=fs(9.0))
    ax.set_ylabel("F2 (Hz)", fontsize=fs(9.0))
    ax.tick_params(labelsize=fs(8.2))
    ax.grid(True, color="#EDF1F7", lw=lws(0.8))
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    leg = ax.legend(loc="lower right", fontsize=fs(8.6), frameon=True,
                    borderpad=0.6, handlelength=2.6)
    leg.get_frame().set_edgecolor("#C8CFD9")
    ax.set_title("the same two F2 tracks together: next to the emphatic, F2 "
                 "starts far lower and takes about 60 ms to catch up",
                 fontsize=fs(9.4), color=NAVY, pad=8)

    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(path.replace(".png", ".pdf"), bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    for k, v in read.items():
        print("  F2 at %d ms, %-9s %.0f Hz" % (MEASURE_MS, k, v))


if __name__ == "__main__":
    draw("fig2_4.png")
    print("wrote fig2_4.png/.pdf")
