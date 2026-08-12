from nbbuild import md, code, save, PROVENANCE, PROVENANCE_CODE

cells = [
    md("""## What this notebook does

Every representation in Chapter 3, computed here from first principles rather
than called from a library: framing and windowing, the narrowband and wideband
spectrogram, the mel filterbank, log-mel features, MFCCs, SpecAugment, and
linear prediction with formants read off the fitted filter.

Each function is written out so you can put it beside the chapter and match
line to paragraph. A library would be shorter and would teach you nothing about
what the defaults are doing.

The audio is synthetic unless you supply your own. Everything works on either."""),

    code("""NOTEBOOK = 'ch03_speech_features.ipynb'

import numpy as np
import matplotlib.pyplot as plt

SR = 16000
rng = np.random.default_rng(0)

# OPTIONAL: point this at a wav file of your own and everything below uses it.
AUDIO_PATH = None

def synth_syllable(f1, f2, f3=2800, f0=120, seconds=0.6, sr=SR):
    # a source filter model: a buzz through three resonators
    n = int(seconds * sr)
    x = np.zeros(n)
    x[::int(sr / f0)] = 1.0
    for f, bw in ((f1, 80), (f2, 100), (f3, 150)):
        r, th = np.exp(-np.pi * bw / sr), 2 * np.pi * f / sr
        a1, a2 = 2 * r * np.cos(th), -r * r
        y = np.zeros(n)
        for i in range(n):
            y[i] = x[i] + (a1 * y[i - 1] if i else 0) + (a2 * y[i - 2] if i > 1 else 0)
        x = y / (np.abs(y).max() + 1e-9)
    return x * np.hanning(n) ** 0.25


if AUDIO_PATH:
    import soundfile as sf
    audio, SR = sf.read(AUDIO_PATH)
    audio = audio if audio.ndim == 1 else audio.mean(axis=1)
    SOURCE = f'real audio: {AUDIO_PATH}'
else:
    audio = synth_syllable(f1=300, f2=2200)
    SOURCE = 'synthetic /iː/ after a plain consonant'

print(f'{SOURCE}, {len(audio)} samples at {SR} Hz, '
      f'{len(audio) / SR:.2f} seconds')"""),

    md("""## 1. The waveform

Amplitude against time. It shows the loudness envelope and the periodicity, and
almost nothing about which sounds are present. That is why the rest of the
chapter exists."""),

    code("""t = np.arange(len(audio)) / SR
plt.figure(figsize=(11, 2.6))
plt.plot(t, audio, linewidth=0.5)
plt.xlabel('time (s)')
plt.ylabel('amplitude')
plt.title(f'waveform: {SOURCE}')
plt.tight_layout()
plt.show()"""),

    md("""## 2. Framing and windowing

Speech is not stationary, so it is analysed in short overlapping frames. Two
numbers decide everything downstream: the frame length and the hop. The classic
setting is 25 ms with a 10 ms hop, which gives 100 frames a second.

The window tapers each frame to zero at its edges. Without it, the abrupt cut
at the frame boundary is itself a signal, and it appears in the spectrum as
energy that was never in the speech."""),

    code("""def frame(signal, frame_ms=25, hop_ms=10, sr=SR, window='hamming'):
    flen, hop = int(sr * frame_ms / 1000), int(sr * hop_ms / 1000)
    n = 1 + max(0, (len(signal) - flen) // hop)
    idx = np.arange(flen)[None, :] + hop * np.arange(n)[:, None]
    frames = signal[idx]
    if window == 'hamming':
        frames = frames * np.hamming(flen)
    elif window == 'hann':
        frames = frames * np.hanning(flen)
    return frames, flen, hop


frames, flen, hop = frame(audio)
print(f'frame length {flen} samples ({1000 * flen / SR:.0f} ms), '
      f'hop {hop} samples ({1000 * hop / SR:.0f} ms)')
print(f'{len(audio)} samples  ->  {frames.shape[0]} frames of {frames.shape[1]}')
print(f'frame rate: {SR / hop:.0f} frames per second')"""),

    md("""## 3. Narrowband against wideband

The same recording, two window lengths, two different pictures.

A long window (about 45 ms) resolves the harmonics of the voice: the horizontal
stripes are the pitch and its multiples. A short window (about 5 ms) blurs the
harmonics together and resolves the formants instead, and the vertical striping
is the individual glottal pulses.

Neither is more correct. They answer different questions, and the choice of
window length is the question you are asking."""),

    code("""def spectrogram(signal, frame_ms, hop_ms=2.5, sr=SR, nfft=1024):
    frames, _, _ = frame(signal, frame_ms, hop_ms, sr)
    spec = np.abs(np.fft.rfft(frames, n=nfft, axis=1))
    return 20 * np.log10(spec + 1e-10)


fig, axes = plt.subplots(1, 2, figsize=(11, 3.6), sharey=True)
for ax, ms, name in ((axes[0], 45, 'narrowband, 45 ms window'),
                     (axes[1], 5, 'wideband, 5 ms window')):
    S = spectrogram(audio, ms)
    ax.imshow(S.T, origin='lower', aspect='auto', cmap='magma',
              extent=[0, len(audio) / SR, 0, SR / 2])
    ax.set_title(name)
    ax.set_xlabel('time (s)')
    ax.set_ylim(0, 4000)
axes[0].set_ylabel('frequency (Hz)')
plt.tight_layout()
plt.show()"""),

    md("""## 4. The mel filterbank and log-mel features

Human hearing resolves low frequencies finely and high frequencies coarsely.
The mel scale encodes that, and a bank of triangular filters spaced evenly on
it turns a 513-point spectrum into the 40 numbers that most neural speech
systems actually consume.

Two conventions to record, because they differ and both are in use: which mel
formula (the one below is the HTK form), and the low and high edge frequencies.
For 8 kHz telephone audio the upper edge cannot be 8000 Hz, and forgetting that
is one of the pitfalls in the chapter."""),

    code("""def hz_to_mel(hz):
    return 2595.0 * np.log10(1.0 + hz / 700.0)          # HTK convention


def mel_to_hz(mel):
    return 700.0 * (10.0 ** (mel / 2595.0) - 1.0)


def mel_filterbank(n_filters=40, nfft=1024, sr=SR, fmin=20, fmax=None):
    fmax = fmax or sr / 2
    edges = mel_to_hz(np.linspace(hz_to_mel(fmin), hz_to_mel(fmax),
                                  n_filters + 2))
    bins = np.floor((nfft + 1) * edges / sr).astype(int)
    fb = np.zeros((n_filters, nfft // 2 + 1))
    for m in range(1, n_filters + 1):
        left, centre, right = bins[m - 1], bins[m], bins[m + 1]
        for k in range(left, centre):
            fb[m - 1, k] = (k - left) / max(1, centre - left)
        for k in range(centre, right):
            fb[m - 1, k] = (right - k) / max(1, right - centre)
    return fb


NFFT = 1024
fb = mel_filterbank(nfft=NFFT)
frames, _, _ = frame(audio)
power = np.abs(np.fft.rfft(frames, n=NFFT, axis=1)) ** 2
logmel = np.log(power @ fb.T + 1e-10)

fig, axes = plt.subplots(1, 2, figsize=(11, 3.4))
axes[0].plot(np.linspace(0, SR / 2, fb.shape[1]), fb[::4].T, linewidth=0.9)
axes[0].set_title('every fourth mel filter')
axes[0].set_xlabel('frequency (Hz)')
axes[1].imshow(logmel.T, origin='lower', aspect='auto', cmap='magma')
axes[1].set_title(f'log-mel features: {logmel.shape[0]} frames x '
                  f'{logmel.shape[1]}')
axes[1].set_xlabel('frame')
axes[1].set_ylabel('mel filter')
plt.tight_layout()
plt.show()"""),

    md("""## 5. MFCCs

A discrete cosine transform over the log-mel vector decorrelates it and packs
most of the shape into the first dozen coefficients. That mattered when models
assumed diagonal covariance. It matters less now, which is why log-mel is the
usual input to a neural system and MFCC is the classic baseline.

Three things to report, because all three vary between toolkits: how many
coefficients, whether the zeroth is kept, and whether deltas are appended."""),

    code("""def dct2(x, n_out):
    n = x.shape[-1]
    k = np.arange(n_out)[:, None]
    basis = np.cos(np.pi * k * (2 * np.arange(n)[None, :] + 1) / (2 * n))
    return x @ basis.T * np.sqrt(2.0 / n)


mfcc = dct2(logmel, 13)
print(f'log-mel {logmel.shape}  ->  MFCC {mfcc.shape}')
print(f'the zeroth coefficient is overall energy: '
      f'mean {mfcc[:, 0].mean():.2f}')

plt.figure(figsize=(11, 2.8))
plt.imshow(mfcc[:, 1:].T, origin='lower', aspect='auto', cmap='viridis')
plt.title('MFCC 1 to 12 (the zeroth, energy, is not shown)')
plt.xlabel('frame')
plt.ylabel('coefficient')
plt.colorbar()
plt.tight_layout()
plt.show()"""),

    md("""## 6. SpecAugment

Mask a band of frequencies, mask a run of frames, train on that. It is
augmentation applied to the features rather than the waveform, it costs almost
nothing, and it is one of the few tricks that reliably helps when labelled data
is scarce, which is the Arabic case throughout this book.

It belongs in training only. Applying it at evaluation makes the number
incomparable with everybody else's, and that is a pitfall the chapter names."""),

    code("""def spec_augment(features, freq_masks=2, freq_width=8,
                 time_masks=2, time_width=20, rng=rng):
    out = features.copy()
    n_frames, n_bins = out.shape
    for _ in range(freq_masks):
        w = rng.integers(0, freq_width + 1)
        f0 = rng.integers(0, max(1, n_bins - w))
        out[:, f0:f0 + w] = out.mean()
    for _ in range(time_masks):
        w = rng.integers(0, time_width + 1)
        t0 = rng.integers(0, max(1, n_frames - w))
        out[t0:t0 + w, :] = out.mean()
    return out


masked = spec_augment(logmel)
fig, axes = plt.subplots(1, 2, figsize=(11, 3.2), sharey=True)
axes[0].imshow(logmel.T, origin='lower', aspect='auto', cmap='magma')
axes[0].set_title('log-mel')
axes[1].imshow(masked.T, origin='lower', aspect='auto', cmap='magma')
axes[1].set_title('after SpecAugment: two frequency masks, two time masks')
for ax in axes:
    ax.set_xlabel('frame')
plt.tight_layout()
plt.show()"""),

    md("""## 7. Linear prediction, and the emphatic formant

Linear prediction fits an all-pole filter to a frame: the model says each sample
is a weighted sum of the ones before it. The poles of that filter sit at the
resonances of the vocal tract, so reading their angles off the unit circle gives
the formants.

This is the measurement Section 2.4 and Section 3.7 ask for. Below, both
syllables of the minimal pair are analysed the same way, and the second formant
is where they differ."""),

    code("""def lpc(frame_signal, order=16):
    # autocorrelation, then Levinson-Durbin, exactly as in the chapter
    x = frame_signal * np.hamming(len(frame_signal))
    r = np.correlate(x, x, mode='full')[len(x) - 1:len(x) + order]
    a = np.zeros(order + 1)
    a[0], err = 1.0, r[0]
    for i in range(1, order + 1):
        acc = r[i] + sum(a[j] * r[i - j] for j in range(1, i))
        k = -acc / (err + 1e-12)
        a_new = a.copy()
        for j in range(1, i):
            a_new[j] = a[j] + k * a[i - j]
        a_new[i] = k
        a, err = a_new, err * (1 - k * k)
    return a


def formants(frame_signal, sr=SR, order=16, n=3, max_bandwidth=400):
    # the poles of the fitted filter, kept if they look like a resonance
    a = lpc(frame_signal, order)
    keep = []
    for r in np.roots(a):
        if np.imag(r) <= 0.01:
            continue
        f = np.arctan2(np.imag(r), np.real(r)) * sr / (2 * np.pi)
        bandwidth = -0.5 * (sr / np.pi) * np.log(abs(r))
        # a formant is narrow; a wide pole is the spectral tilt, not a resonance
        if 90 < f < sr / 2 and bandwidth < max_bandwidth:
            keep.append(f)
    return sorted(keep)[:n]


pairs = {'تين  tīn, plain /t/': synth_syllable(f1=300, f2=2200),
         'طين  ṭīn, emphatic /tˤ/': synth_syllable(f1=380, f2=1500)}
measured = {}
for name, sig in pairs.items():
    mid = sig[len(sig) // 2 - 200: len(sig) // 2 + 200]
    f = formants(mid)
    measured[name] = f
    print(f'{name:<26} ' + '  '.join(f'F{i+1} {v:6.0f} Hz'
                                     for i, v in enumerate(f)))

names = list(measured)
if len(measured[names[0]]) > 1 and len(measured[names[1]]) > 1:
    drop = measured[names[0]][1] - measured[names[1]][1]
    print(f'\\nsecond formant is {drop:.0f} Hz lower beside the emphatic '
          f'consonant')
print('\\nOn synthetic audio the fit recovers the resonances it was given, '
      'to within a few Hz. On real speech it will not be this tidy: drop the '
      'bandwidth test and watch a spurious pole appear between them.')"""),

    md("""## 8. The chapter's exercises, as code

The workbench for Exercises 1, 3 and 5. Exercises 2 and 4 need your own audio
and your own reasoning; the helpers here do the arithmetic they rest on.

### Exercise 1: aliasing

A 9 kHz tone sampled at 16 kHz with no anti-aliasing filter appears somewhere
else entirely. The rule is that a tone at f above the Nyquist limit folds back
to `sample_rate - f`."""),

    code("""def alias_frequency(tone_hz, sample_rate):
    nyquist = sample_rate / 2
    f = tone_hz % sample_rate
    return f if f <= nyquist else sample_rate - f


TONE, RATE = 9000, 16000
seconds = 0.25
t = np.arange(int(seconds * RATE)) / RATE
tone = np.sin(2 * np.pi * TONE * t)

spec = np.abs(np.fft.rfft(tone * np.hanning(len(tone))))
peak_hz = np.fft.rfftfreq(len(tone), 1 / RATE)[np.argmax(spec)]

print(f'a {TONE} Hz tone sampled at {RATE} Hz')
print(f'  predicted alias: {alias_frequency(TONE, RATE):.0f} Hz')
print(f'  measured peak  : {peak_hz:.0f} Hz')
print(f'  minimum rate that would have avoided it: {2 * TONE} Hz')

plt.figure(figsize=(9, 2.6))
plt.specgram(tone, NFFT=512, Fs=RATE, noverlap=384, cmap='magma')
plt.ylabel('frequency (Hz)')
plt.xlabel('time (s)')
plt.title(f'{TONE} Hz sampled at {RATE} Hz: the tone appears at '
          f'{alias_frequency(TONE, RATE):.0f} Hz')
plt.tight_layout()
plt.show()"""),

    md("""### Exercise 3: the size of everything

One second of 16 kHz audio, from raw samples to a 40-dimensional log-mel
matrix. The point of the table is the compression ratio, and the point of the
ratio is that every stage throws something away on purpose."""),

    code("""def pipeline_sizes(seconds=1.0, sr=16000, frame_ms=25, hop_ms=10,
                   nfft=512, n_mels=40):
    samples = int(seconds * sr)
    n_frames = 1 + (samples - int(sr * frame_ms / 1000)) // int(sr * hop_ms / 1000)
    rows = [
        ('raw samples', samples, 1),
        ('frames', n_frames * int(sr * frame_ms / 1000), n_frames),
        ('magnitude spectra', n_frames * (nfft // 2 + 1), n_frames),
        ('log-mel', n_frames * n_mels, n_frames),
        ('MFCC (13)', n_frames * 13, n_frames),
    ]
    print(f'{"stage":>20} {"numbers":>10} {"per second":>12} {"vs raw":>9}')
    for name, total, _ in rows:
        print(f'{name:>20} {total:>10} {total / seconds:>12.0f} '
              f'{total / samples:>9.3f}')
    print('\\nContinue with log-mel for a neural model. Continue with MFCC '
          'only if something downstream wants decorrelated features.')


pipeline_sizes()"""),

    md("""### Exercise 5: splits that do not leak

One hundred hours, fifty speakers. The rule is that no speaker and no prompt
may appear on both sides of a boundary. Splitting by utterance instead lets the
model recognise the voice rather than the words, and the test number then
measures memory rather than generalisation."""),

    code("""def speaker_disjoint_split(speakers, hours_each, dev=0.1, test=0.1,
                           seed=0):
    order = np.random.default_rng(seed).permutation(len(speakers))
    total = sum(hours_each)
    want_dev, want_test = dev * total, test * total
    split = {'test': [], 'dev': [], 'train': []}
    got_dev = got_test = 0.0
    for i in order:
        if got_test < want_test:
            split['test'].append(speakers[i])
            got_test += hours_each[i]
        elif got_dev < want_dev:
            split['dev'].append(speakers[i])
            got_dev += hours_each[i]
        else:
            split['train'].append(speakers[i])
    return split


speakers = [f'spk{i:02d}' for i in range(50)]
hours = [2.0] * 50
split = speaker_disjoint_split(speakers, hours)
for name, members in split.items():
    print(f'{name:>6}: {len(members):>2} speakers, '
          f'{2.0 * len(members):>5.1f} hours')
overlap = set(split['train']) & (set(split['dev']) | set(split['test']))
print(f'\\nspeakers on both sides of a boundary: {len(overlap)}')
print('If that number is not zero, every result below it is inflated and '
      'there is no way to say by how much.')"""),

    md(PROVENANCE),
    code(PROVENANCE_CODE),
]

save('ch03_speech_features.ipynb', cells,
     'Notebook 3.1  Seeing speech: from waveform to features',
     'Framing, spectrograms, mel filterbanks, MFCCs, SpecAugment and linear '
     'prediction, written out in full.')
