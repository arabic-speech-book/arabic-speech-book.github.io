"""
Figure 3.5: narrowband against wideband spectrograms of طين and تين.

Replaces artwork that was synthesized rather than measured. Three faults made
the replacement necessary:

  1. The two words had identical onsets and offsets, to the millisecond, and
     the voice held one exactly constant pitch. No two real utterances do that.
  2. In the wideband panels the bands labelled F2 were energy minima, not
     maxima: on the color map used, dark meant low energy, so the arrows
     pointed at spectral valleys and called them formants.
  3. The F2 values implied by those bands were about 2000 Hz for the emphatic
     and about 3800 Hz for the plain word. An /iː/ does not have an F2 near
     3800 Hz, and the figure disagreed with Chapter 2, where the same two words
     are measured at 1840 Hz and 2580 Hz.

This version uses the author's own recording of the two words, the same file
Chapter 2 measures, so the two chapters cannot disagree. Both words are shown
over the same time span, aligned on the start of voicing, at the same two
window lengths.

High energy is dark, as in Chapter 2 and as in the printed spectrograms most
readers will meet, so the formants read as dark bands and the figure survives
grayscale printing.
"""
import numpy as np
import scipy.io.wavfile as wav
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from figscale import fs, lws, arr
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch
from arabtext import draw_word

NAVY="#1F3864"; ORANGE="#C55A11"; GREY="#4A5462"
ARB=FontProperties(fname="/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf")
WAVFILE="Ch2_Fig2-4_tin_vs_tiin_16k.wav"

# (Arabic, romanization, gloss, consonant note, voicing onset in the file)
ROWS=[("طِين","ṭīn","'mud'",  "emphatic ط /tˤ/", 3.052),
      ("تِين","tīn","'figs'", "plain ت /t/",     2.002)]
COLS=[("Narrowband (long window, 46 ms)", 736),
      ("Wideband (short window, 4 ms)",    64)]
T0,T1 = -0.05, 0.26
FMAX = 5000

def spec(x, sr, wlen, nfft=2048, hop=16):
    win=np.hanning(wlen); fr=[]
    for k in range(0, len(x)-wlen, hop):
        seg=np.zeros(nfft); seg[:wlen]=x[k:k+wlen]*win
        fr.append(np.abs(np.fft.rfft(seg)))
    return 20*np.log10(np.maximum(np.array(fr).T, 1e-7))

def draw(path):
    sr, raw = wav.read(WAVFILE); raw=raw.astype(float)/32768.0
    fig, axes = plt.subplots(2, 2, figsize=(12.6, 7.9))
    fig.subplots_adjust(left=0.072, right=0.978, top=0.925, bottom=0.085,
                        hspace=0.34, wspace=0.13)
    for i,(ar_w, rom, gloss, cons, von) in enumerate(ROWS):
        seg=raw[int((von+T0)*sr):int((von+T1)*sr)]
        for j,(title, wlen) in enumerate(COLS):
            ax=axes[i][j]
            S=spec(seg, sr, wlen)
            ax.imshow(S, origin="lower", aspect="auto", cmap="Greys",
                      extent=[T0*1000, T1*1000, 0, sr/2],
                      vmin=S.max()-52, vmax=S.max())
            ax.set_ylim(0, FMAX); ax.set_xlim(T0*1000, T1*1000)
            ax.axvline(0, color=NAVY, lw=lws(1.2))
            if i==0: ax.set_title(title, fontsize=fs(10.2), color=NAVY,
                                  weight="bold", pad=9)
            ax.tick_params(labelsize=fs(8.2))
            if j==0: ax.set_ylabel("frequency (Hz)", fontsize=fs(9.0))
            if i==1: ax.set_xlabel("time from the start of voicing (ms)",
                                   fontsize=fs(9.0))
            if j==1:
                f2 = 1840 if i==0 else 2580
                ax.annotate("F2 at 30 ms:\n%d Hz" % f2, xy=(30, f2),
                            xytext=(118, f2+950), ha="left", va="center",
                            fontsize=fs(9.0), color=ORANGE, weight="bold",
                            linespacing=1.4,
                            arrowprops=dict(arrowstyle="-|>", color=ORANGE,
                                            lw=lws(1.5), mutation_scale=arr(12)))
        # word label inside the narrowband panel, as in Figure 2.4
        ax=axes[i][0]
        ax.add_patch(FancyBboxPatch((T0*1000+3, 3250), 124, 1660,
                                    boxstyle="round,pad=0,rounding_size=36",
                                    facecolor="white", edgecolor="#C9D6E8",
                                    lw=lws(0.9), alpha=0.95, zorder=5))
        draw_word(ax, T0*1000+12, 4400, ar_w, ARB, fs(15), NAVY, ha="left",
                  zorder=6)
        ax.text(T0*1000+12, 4230, "%s  %s\n%s" % (rom, gloss, cons),
                ha="left", va="top", fontsize=fs(8.0), color=NAVY,
                linespacing=1.5, zorder=6)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(path.replace(".png",".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)

if __name__=="__main__":
    draw("fig3_5.png"); print("wrote fig3_5.png/.pdf")
