"""
Figure 3.8: the same word at 16 kHz and through a telephone channel.

New. Section 3.9 tells a reader to match the front end to the channel, and
Exercise 4 tests it, but nothing in the chapter shows what a channel mismatch
looks like. This figure shows it on the chapter's own example word.

The left column is تين as recorded at 16 kHz. The right column is the same
recording put through a telephone channel: band-limited to 300 to 3400 Hz and
resampled to 8 kHz. Nothing else is changed, so every difference between the
columns is the channel.

The top row is the spectrogram; the bottom row is the average spectrum of the
vowel, which is where the missing band is impossible to miss. A model trained
on the left and given the right sees empty upper filters, and no amount of
resampling puts back what the channel removed.
"""
import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import butter, sosfiltfilt, resample_poly
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figscale import fs, lws, arr

NAVY="#1F3864"; ORANGE="#C55A11"; GREY="#4A5462"
WAVFILE="Ch2_Fig2-4_tin_vs_tiin_16k.wav"
VON=2.002; T0,T1=-0.06,0.26           # the plain word tin, as in Figure 3.5

def spec(x, sr, wlen=96, nfft=1024, hop=16):
    win=np.hanning(wlen); fr=[]
    for k in range(0, len(x)-wlen, hop):
        seg=np.zeros(nfft); seg[:wlen]=x[k:k+wlen]*win
        fr.append(np.abs(np.fft.rfft(seg)))
    return 20*np.log10(np.maximum(np.array(fr).T, 1e-7))

def avg_spectrum(x, sr, nfft=1024):
    win=np.hanning(nfft); acc=np.zeros(nfft//2+1); n=0
    for k in range(0, len(x)-nfft, nfft//2):
        acc+=np.abs(np.fft.rfft(x[k:k+nfft]*win))**2; n+=1
    p=10*np.log10(np.maximum(acc/max(n,1), 1e-12))
    return np.fft.rfftfreq(nfft, 1/sr), p-p.max()

def draw(path):
    sr, raw = wav.read(WAVFILE); raw=raw.astype(float)/32768.0
    seg=raw[int((VON+T0)*sr):int((VON+T1)*sr)]
    sos=butter(6, [300/(sr/2), 3400/(sr/2)], btype="band", output="sos")
    tel=sosfiltfilt(sos, seg)
    tel8=resample_poly(tel, 1, 2)            # 16 kHz -> 8 kHz
    sr8=sr//2

    fig=plt.figure(figsize=(12.6, 7.2))
    gs=fig.add_gridspec(2, 2, height_ratios=[1.35, 1.0], hspace=0.46,
                        wspace=0.16, left=0.075, right=0.978, top=0.925,
                        bottom=0.095)
    cols=[("As recorded: 16 kHz", seg, sr, 8000),
          ("Through a telephone channel: 8 kHz, 300-3400 Hz", tel8, sr8, 8000)]
    for j,(title, x, s_, ymax) in enumerate(cols):
        ax=fig.add_subplot(gs[0,j])
        S=spec(x, s_, wlen=max(16,int(0.006*s_)))
        ax.imshow(S, origin="lower", aspect="auto", cmap="Greys",
                  extent=[T0*1000, T1*1000, 0, s_/2],
                  vmin=S.max()-52, vmax=S.max())
        ax.set_ylim(0, ymax); ax.set_xlim(T0*1000, T1*1000)
        ax.set_title(title, fontsize=fs(10.0), color=NAVY, weight="bold", pad=9)
        ax.set_xlabel("time (ms)", fontsize=fs(9.0))
        if j==0: ax.set_ylabel("frequency (Hz)", fontsize=fs(9.0))
        ax.tick_params(labelsize=fs(8.2))
        if j==1:
            ax.axhspan(4000, ymax, facecolor="white", alpha=0.55, zorder=3)
            ax.axhline(4000, color=ORANGE, lw=lws(1.6), ls=(0,(5,3)), zorder=4)
            ax.text((T0+T1)*500, 6000, "nothing here: the channel\n"
                    "threw this band away", ha="center", va="center",
                    fontsize=fs(9.0), color=ORANGE, weight="bold",
                    linespacing=1.4, zorder=5)

    ax=fig.add_subplot(gs[1,:])
    for (lab, x, s_), style, col in ((("as recorded, 16 kHz", seg, sr), "-", NAVY),
                                     (("telephone, 8 kHz", tel8, sr8), (0,(5,3)), ORANGE)):
        f,p=avg_spectrum(x, s_)
        ax.plot(f, p, linestyle=style, color=col, lw=lws(1.8), label=lab)
    ax.axvline(300, color=GREY, lw=lws(1.0), ls=(0,(2,3)))
    ax.axvline(3400, color=GREY, lw=lws(1.0), ls=(0,(2,3)))
    ax.text(3520, -6, "3400 Hz", ha="left", va="center", fontsize=fs(8.6), color=GREY)
    ax.text(330, -6, "300 Hz", ha="left", va="center", fontsize=fs(8.6), color=GREY)
    ax.set_xlim(0, 8000); ax.set_ylim(-78, 6)
    ax.set_xlabel("frequency (Hz)", fontsize=fs(9.0))
    ax.set_ylabel("relative level (dB)", fontsize=fs(9.0))
    ax.set_title("average spectrum of the same word, both versions overlaid",
                 fontsize=fs(9.6), color=NAVY, pad=8)
    ax.tick_params(labelsize=fs(8.2))
    ax.grid(True, color="#EDF1F7", lw=lws(0.8)); ax.set_axisbelow(True)
    for sp in ("top","right"): ax.spines[sp].set_visible(False)
    leg=ax.legend(loc="upper right", fontsize=fs(8.8), frameon=True, borderpad=0.6)
    leg.get_frame().set_edgecolor("#C8CFD9")
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(path.replace(".png",".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)

if __name__=="__main__":
    draw("fig3_8.png"); print("wrote fig3_8.png/.pdf")
