"""
Figure 7.4: a Praat annotation view of a short Arabic utterance.

Built from the author's own recording, the same file Chapter 2 uses for Figure
2.4, so the reader meets one voice, one microphone and one recording level in
both chapters. The token is the plain word تين, tīn, 'figs', cut out of that
recording with a little silence at each end.

  Ch7_Fig7-4_tin_16k.wav        16 kHz, mono, 16-bit PCM
  the token used                1.860 s to 2.400 s of that file

Nothing here is drawn by hand. The waveform is the samples. The spectrogram is
a wideband short-time Fourier transform, 5 ms Hamming window, 1 ms hop, 50 dB
range, which is what Praat shows by default, so the vertical striations are the
glottal pulses of the recording rather than an illustrator's idea of them.

The tier boundaries are placed from the signal and are reproducible from it:

  0.060 s   release of /t/, the burst      root-mean-square energy rises from
                                           the noise floor by two orders of
                                           magnitude within one 10 ms frame
  0.140 s   onset of voicing               zero-crossing rate falls from about
                                           0.45 to below 0.10 while energy rises
  0.388 s   /iː/ to /n/                    energy drops to about a quarter and
                                           the zero-crossing rate settles below
                                           0.06, the nasal murmur
  0.465 s   end of the word

That gives a voice onset time of about 80 ms for the plain /t/, which is the
measurement Chapter 2's Figure 2.4 turns on, so the two figures agree.

The previous artwork drew a pure sine over three flat horizontal bars. It did
not look like speech, it did not look like a spectrogram, and a student opening
Praat for the first time is meant to recognise the picture.
"""
import numpy as np
import scipy.io.wavfile as wav
from matplotlib.patches import Rectangle
from bookstyle import NAVY, ORANGE, GREY, WHITE, ARF, canvas, note, save, ar
from figscale import fs, lws

WAVFILE = "Ch7_Fig7-4_tin_16k.wav"
T0, T1 = 1.860, 2.400                  # the token, in the source recording

# (label, transliteration, end of the interval, in seconds from T0)
PHONES = [("", "", 0.060), ("t", "t", 0.140), ("iː", "ii", 0.388),
          ("n", "n", 0.465), ("", "", T1 - T0)]
WORD_A, WORD_B = 0.060, 0.465
CURSOR = 0.140                         # voicing onset, visible in every panel

WIN_MS, HOP_MS, DB_RANGE, FMAX = 5.0, 1.0, 50.0, 5000.0


def spectrogram(x, sr):
    """Wideband, the way Praat draws it: short window, heavy overlap, dB."""
    n = max(8, int(round(WIN_MS / 1000 * sr)))
    hop = max(1, int(round(HOP_MS / 1000 * sr)))
    nfft = 512
    win = np.hamming(n)
    pre = np.append(x[0], x[1:] - 0.97 * x[:-1])       # pre-emphasis, as Praat
    frames = [pre[i:i + n] * win for i in range(0, len(pre) - n, hop)]
    S = np.abs(np.fft.rfft(np.array(frames), nfft, axis=1)).T
    db = 20 * np.log10(S + 1e-12)
    db -= db.max()
    return np.clip(db, -DB_RANGE, 0.0), np.fft.rfftfreq(nfft, 1 / sr)


def draw(path_out):
    sr, raw = wav.read(WAVFILE)
    x = raw.astype(float) / 32768.0
    seg = x[int(T0 * sr):int(T1 * sr)]
    dur = len(seg) / sr

    w, h = 12.6, 8.1
    fig, ax = canvas(w, h, (0, w), (0, h))
    x0, x1 = 1.85, w - 0.85

    def X(t):
        return x0 + t / dur * (x1 - x0)

    def panel(y, ph, label, fill=WHITE):
        ax.add_patch(Rectangle((x0, y), x1 - x0, ph, facecolor=fill,
                               edgecolor=NAVY, lw=lws(1.2), zorder=2))
        note(ax, x0 - 0.18, y + ph / 2, label, size=10.2, colour=NAVY,
             ha="right", weight="bold")

    # ---- waveform, the samples themselves --------------------------------
    wy, wh = h - 2.45, 1.95
    panel(wy, wh, "waveform")
    t = np.arange(len(seg)) / sr
    peak = np.abs(seg).max()
    ax.plot(X(t), wy + wh / 2 + seg / peak * (wh / 2 - 0.10),
            color=NAVY, lw=lws(0.32), zorder=4)

    # ---- spectrogram, a real short-time Fourier transform -----------------
    sy, sh = wy - 2.25, 1.95
    panel(sy, sh, "spectrogram")
    db, freqs = spectrogram(seg, sr)
    keep = freqs <= FMAX
    ax.imshow(db[keep][::-1], aspect="auto", cmap="Greys",
              extent=(X(0), X(dur), sy, sy + sh),
              vmin=-DB_RANGE, vmax=0.0, zorder=3, interpolation="bilinear")
    for f in (1000, 2000, 3000, 4000):
        note(ax, x1 + 0.10, sy + sh * f / FMAX, f"{f // 1000}k", size=8.4,
             colour=GREY, ha="left")
    note(ax, x1 + 0.10, sy + sh + 0.10, "Hz", size=8.4, colour=GREY, ha="left")

    # ---- the two TextGrid tiers -------------------------------------------
    ty, th_ = sy - 1.32, 1.00
    panel(ty, th_, "words")
    py, ph_ = ty - 1.14, 0.92
    panel(py, ph_, "phones")

    for xv in (WORD_A, WORD_B):
        ax.plot([X(xv)] * 2, [ty, ty + th_], color=NAVY, lw=lws(1.1), zorder=4)
    mid = X((WORD_A + WORD_B) / 2)
    ax.text(mid, ty + th_ * 0.62, ar("تين"), fontproperties=ARF,
            fontsize=fs(13.5), color=NAVY, ha="center", va="center", zorder=5)
    note(ax, mid, ty + th_ * 0.22, "tin  'figs'", size=9.4, colour=GREY,
         style="italic")
    note(ax, (x0 + X(WORD_A)) / 2, ty + th_ / 2, "sil", size=9.0, colour=GREY)
    note(ax, (X(WORD_B) + x1) / 2, ty + th_ / 2, "sil", size=9.0, colour=GREY)

    start = 0.0
    for ipa, tr, end in PHONES:
        if start:
            ax.plot([X(start)] * 2, [py, py + ph_], color=NAVY, lw=lws(1.1),
                    zorder=4)
        cx = X((start + end) / 2)
        note(ax, cx, py + ph_ * 0.58, f"/{ipa}/" if ipa else "sil", size=10.0,
             colour=NAVY if ipa else GREY,
             weight="bold" if ipa else "normal")
        if tr:
            note(ax, cx, py + ph_ * 0.22, tr, size=8.8, colour=GREY,
                 style="italic")
        start = end

    # ---- one cursor through every panel -----------------------------------
    ax.plot([X(CURSOR)] * 2, [py, wy + wh], color=ORANGE, lw=lws(1.3),
            ls=(0, (5, 3)), zorder=6)
    note(ax, X(CURSOR), wy + wh + 0.28,
         "onset of voicing",
         size=10.0, colour=ORANGE, weight="bold")

    for ms in range(0, int(dur * 1000) + 1, 50):
        tv = ms / 1000
        if tv > dur:
            break
        big = ms % 100 == 0
        ax.plot([X(tv)] * 2, [py - (0.13 if big else 0.07), py], color=GREY,
                lw=lws(0.9), zorder=4)
        if big:
            note(ax, X(tv), py - 0.33, f"{ms}", size=8.6, colour=GREY)
    note(ax, x1 + 0.12, py - 0.33, "ms", size=8.6, colour=GREY, ha="left")

    save(fig, path_out)


if __name__ == "__main__":
    draw("fig7_4.png")
