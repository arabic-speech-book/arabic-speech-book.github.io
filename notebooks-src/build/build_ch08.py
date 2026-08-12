from nbbuild import md, code, save, PROVENANCE, PROVENANCE_CODE

# ---------------------------------------------------------------- 8.1 ------
dialect_id = [
    md("""## What this notebook does

A dialect identifier, read honestly, and a spoken-document search demo.

1. Represent each clip as an utterance embedding from a self-supervised encoder, and train a light classifier on top. This is the standard recipe and it is two lines once the embeddings exist.
2. Report accuracy **and** macro-averaged F1, because a corpus with an MSA majority makes accuracy look good for the wrong reason.
3. Read the confusion matrix. The chapter's argument is that neighbouring varieties on the continuum are the hard cases, and the matrix is where that becomes visible rather than assertable.
4. Index a small set of transcribed clips and rank them against a keyword, with a morphological expansion, which is the smallest honest version of spoken document retrieval.

A synthetic fallback generates embeddings with the geometry the chapter
describes, so everything runs with no downloads. Where to plug in real
embeddings is marked."""),

    code("""NOTEBOOK = 'ch08_dialect_id.ipynb'

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, f1_score, confusion_matrix,
                             classification_report)

rng = np.random.default_rng(7)
DIALECTS = ['MSA', 'Gulf', 'Levantine', 'Egyptian', 'Maghrebi']
print('ready')"""),

    md("""## 1. Embeddings

Real embeddings come from a pretrained encoder: mean-pool its hidden states
over time and you have one vector per utterance. The OPTIONAL cell shows the
call.

The fallback below places each dialect at a point in a 64-dimensional space,
and the geography is the lesson: the varieties are laid out along a line, in
the order they sit on the continuum, so neighbours are genuinely close and the
classifier's mistakes will be between neighbours rather than uniform. That is
what the chapter means by a continuum rather than a set of categories."""),

    code("""def synthetic_embeddings(per_class=120, dim=64, spread=1.0):
    # the dialects are placed along a line: neighbours are near, ends are far
    centres = np.zeros((len(DIALECTS), dim))
    for i in range(len(DIALECTS)):
        centres[i, :8] = rng.normal(size=8) * 0.2 + i * 0.9
    X, y = [], []
    for i in range(len(DIALECTS)):
        X.append(centres[i] + rng.normal(scale=spread, size=(per_class, dim)))
        y += [i] * per_class
    return np.vstack(X), np.array(y)


X, y = synthetic_embeddings()
n_train = int(0.7 * len(y))
order = rng.permutation(len(y))
train, test = order[:n_train], order[n_train:]
print(f'{X.shape[0]} utterances, {X.shape[1]} dimensions, '
      f'{len(DIALECTS)} dialects')
print(f'{len(train)} train, {len(test)} test')"""),

    code("""# OPTIONAL: real embeddings from a self-supervised encoder.
REAL_AUDIO = []       # [(path, dialect), ...]

if REAL_AUDIO:
    import torch
    import soundfile as sf
    from transformers import AutoModel, AutoFeatureExtractor

    name = 'facebook/wav2vec2-xls-r-300m'
    fx = AutoFeatureExtractor.from_pretrained(name)
    enc = AutoModel.from_pretrained(name).eval()
    vectors, labels = [], []
    for path, dialect in REAL_AUDIO:
        wav, sr = sf.read(path)
        inputs = fx(wav, sampling_rate=sr, return_tensors='pt')
        with torch.no_grad():
            hidden = enc(**inputs).last_hidden_state
        vectors.append(hidden.mean(dim=1).squeeze().numpy())
        labels.append(DIALECTS.index(dialect))
    X, y = np.array(vectors), np.array(labels)
    print(f'{len(X)} real embeddings')
else:
    print('skipped: using the synthetic embeddings above')"""),

    md("""## 2. The classifier, and two numbers instead of one

Accuracy is the share of clips labelled correctly. On a corpus where most of
the audio is Modern Standard Arabic, a classifier that says MSA to everything
scores well on it.

Macro-averaged F1 gives every dialect the same weight regardless of how much
audio it has, so a variety that fails completely drags it down. The gap between
the two numbers is a measure of how unbalanced the test set is, and reporting
only the first is the pitfall the chapter names."""),

    code("""clf = LogisticRegression(max_iter=2000)
clf.fit(X[train], y[train])
pred = clf.predict(X[test])

print(f'accuracy          : {accuracy_score(y[test], pred):.3f}')
print(f'macro-averaged F1 : {f1_score(y[test], pred, average="macro"):.3f}\\n')
print(classification_report(y[test], pred, target_names=DIALECTS, digits=3))

# the majority-class baseline every claim has to beat
majority = np.bincount(y[train]).argmax()
base = accuracy_score(y[test], np.full_like(y[test], majority))
print(f'a classifier that always says {DIALECTS[majority]}: '
      f'accuracy {base:.3f}, macro F1 '
      f'{f1_score(y[test], np.full_like(y[test], majority), average="macro"):.3f}')"""),

    md("""## 3. The confusion matrix

Read along the rows. A dialect confused with its neighbour on the continuum is
the expected failure and tells you the model has learned something real. A
dialect confused with a distant one usually means a data problem: a mislabelled
speaker, a channel the model is keying on, or a class with too few speakers to
generalise from."""),

    code("""cm = confusion_matrix(y[test], pred, normalize='true')
fig, ax = plt.subplots(figsize=(6.2, 5.2))
im = ax.imshow(cm, cmap='Blues', vmin=0, vmax=1)
ax.set_xticks(range(len(DIALECTS)), DIALECTS, rotation=30, ha='right')
ax.set_yticks(range(len(DIALECTS)), DIALECTS)
ax.set_xlabel('predicted')
ax.set_ylabel('true')
ax.set_title('confusion, normalized by row')
for i in range(len(DIALECTS)):
    for j in range(len(DIALECTS)):
        if cm[i, j] > 0.005:
            ax.text(j, i, f'{cm[i, j]:.2f}', ha='center', va='center',
                    color='white' if cm[i, j] > 0.5 else 'black', fontsize=9)
fig.colorbar(im, ax=ax, shrink=0.8)
plt.tight_layout()
plt.show()

off = [(DIALECTS[i], DIALECTS[j], cm[i, j])
       for i in range(len(DIALECTS)) for j in range(len(DIALECTS)) if i != j]
off.sort(key=lambda x: -x[2])
print('the three largest confusions:')
for a, b, v in off[:3]:
    neighbour = abs(DIALECTS.index(a) - DIALECTS.index(b)) == 1
    print(f'  {a} taken for {b}: {v:.1%}'
          f'{"   (neighbours on the continuum)" if neighbour else ""}')"""),

    md("""## 4. Spoken document search

Once clips are transcribed, finding one is a text problem with an Arabic
complication: the word in the query is rarely written the way it appears in the
transcript. It carries a prefix, or a pronoun is attached, or the dialect
spells it differently.

The expansion below is crude on purpose, so you can see exactly what it does.
The point is the difference between the two result lists."""),

    code("""CLIPS = [
    ('c1', 'وين اقرب محطة بنزين', 'Gulf'),
    ('c2', 'المحطة قريبة من المكتبة', 'MSA'),
    ('c3', 'ذهبت الى محطة القطار صباحا', 'MSA'),
    ('c4', 'محطتنا بعيدة شوي', 'Gulf'),
    ('c5', 'الطقس حار اليوم', 'MSA'),
    ('c6', 'وصلنا للمحطة متأخرين', 'Levantine'),
]
PREFIXES = ['و', 'ف', 'ب', 'ك', 'ل', 'ال', 'وال', 'بال', 'لل', 'فال']
SUFFIXES = ['ها', 'هم', 'نا', 'كم', 'ه', 'ك', 'ي', 'ات', 'ة', 'تنا']


def variants(word):
    out = {word}
    for p in PREFIXES:
        out.add(p + word)
        for s in SUFFIXES:
            out.add(p + word + s)
    for s in SUFFIXES:
        out.add(word + s)
    return out


def search(query, expand=False):
    keys = variants(query) if expand else {query}
    hits = []
    for cid, text, dialect in CLIPS:
        score = sum(1 for w in text.split() if w in keys)
        if score:
            hits.append((score, cid, dialect, text))
    return sorted(hits, reverse=True)


QUERY = 'محطة'
for expand in (False, True):
    print(f'query {QUERY!r}, expansion {"on" if expand else "off"}:')
    hits = search(QUERY, expand)
    for score, cid, dialect, text in hits:
        print(f'   {cid}  [{dialect:<9}] {text}')
    if not hits:
        print('   nothing found')
    print()
print('The expansion reaches the clip written with the definite article and '
      'the one with a preposition fused to it. It still misses محطتنا, where '
      'attaching the possessive turned the ta marbuta into an ordinary ta: '
      'concatenating affixes is not morphology, and this is where a real '
      'system needs an analyser rather than a list. Expansion also lets in '
      'false matches, and both have to be measured.')"""),

    md("""## 5. What to report

Not the accuracy alone. The chapter's Reproducibility Note asks for the dialect
taxonomy and the per-class counts, because two papers that both say Gulf may
not mean the same thing, and a class with two speakers in it is not a class."""),

    code("""counts = np.bincount(y[test], minlength=len(DIALECTS))
print(f'{"dialect":<12} {"test clips":>11} {"speakers":>10}  taxonomy note')
for i, d in enumerate(DIALECTS):
    print(f'{d:<12} {counts[i]:>11} {"fill in":>10}  '
          f'which regions this label covers')
print('\\nAlso report: the encoder and its revision, the layer the embeddings '
      'were taken from, whether the split is speaker-disjoint, and the audio '
      'condition, because a classifier can learn the channel instead of the '
      'dialect and score well doing it.')"""),

    md(PROVENANCE),
    code(PROVENANCE_CODE),
]

save('ch08_dialect_id.ipynb', dialect_id,
     'Notebook 8.1  Dialect identification, read honestly',
     'A classifier on self-supervised embeddings, its confusion matrix, and a '
     'small spoken-document search.')

# ---------------------------------------------------------------- 8.2 ------
speaker_noise = [
    md("""## What this notebook does

Three measurements that the chapter argues are usually reported wrongly.

1. **Speaker verification.** Build genuine and impostor trials from
   speaker-disjoint embeddings, sweep the threshold, and find the Equal Error
   Rate. Then look at what happens away from the equal error point, because no
   deployed system runs there.
2. **Diarization.** Cluster segment embeddings, then compute the Diarization
   Error Rate in its three parts: false alarm, missed speech, and speaker
   confusion. One number hides which of the three is your problem.
3. **Enhancement.** Mix noise into speech, denoise it, and measure the result
   two ways: with a signal-quality score and with the transcript. Section 8.7's
   uncomfortable finding is that these two can disagree, and this is where you
   can watch them disagree.

Synthetic fallbacks throughout, so it runs with no downloads."""),

    code("""NOTEBOOK = 'ch08_speaker_and_noise.ipynb'

import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(11)
SR = 16000
print('ready')"""),

    md("""## 1. Speaker verification and the Equal Error Rate

A verification system compares two utterances and returns a score. Sweep a
threshold across those scores and two errors trade off: the false acceptance
rate falls as the threshold rises, and the false rejection rate climbs. The
Equal Error Rate is the point where they cross.

It is a convenient single number and it describes an operating point almost
nobody uses. A bank does not accept a one in twenty impostor rate; it moves the
threshold until false acceptance is negligible and lives with the rejections."""),

    code("""def speaker_embeddings(n_speakers=40, per_speaker=6, dim=128,
                       within=0.12):
    centres = rng.normal(size=(n_speakers, dim))
    centres /= np.linalg.norm(centres, axis=1, keepdims=True)
    X, ids = [], []
    for s in range(n_speakers):
        noise = rng.normal(scale=within, size=(per_speaker, dim))
        v = centres[s] + noise
        X.append(v / np.linalg.norm(v, axis=1, keepdims=True))
        ids += [s] * per_speaker
    return np.vstack(X), np.array(ids)


# OPTIONAL: replace with a pretrained speaker encoder (for example ECAPA-TDNN)
# from speechbrain.inference import EncoderClassifier
X, spk = speaker_embeddings()

genuine, impostor = [], []
for i in range(len(X)):
    for j in range(i + 1, len(X)):
        score = float(X[i] @ X[j])
        (genuine if spk[i] == spk[j] else impostor).append(score)
genuine, impostor = np.array(genuine), np.array(impostor)
print(f'{len(genuine)} genuine trials, {len(impostor)} impostor trials')"""),

    code("""thresholds = np.linspace(-1, 1, 601)
far = np.array([(impostor >= t).mean() for t in thresholds])
frr = np.array([(genuine < t).mean() for t in thresholds])
k = int(np.argmin(np.abs(far - frr)))
eer = (far[k] + frr[k]) / 2

plt.figure(figsize=(10, 3.4))
plt.subplot(1, 2, 1)
plt.hist(impostor, bins=60, alpha=0.6, label='impostor', density=True)
plt.hist(genuine, bins=60, alpha=0.6, label='genuine', density=True)
plt.axvline(thresholds[k], color='k', linestyle='--', linewidth=1)
plt.legend()
plt.title('trial scores')
plt.subplot(1, 2, 2)
plt.plot(thresholds, far, label='false acceptance')
plt.plot(thresholds, frr, label='false rejection')
plt.axvline(thresholds[k], color='k', linestyle='--', linewidth=1)
plt.legend()
plt.xlabel('threshold')
plt.title(f'EER = {eer:.1%} at threshold {thresholds[k]:.2f}')
plt.tight_layout()
plt.show()

print(f'EER {eer:.2%}\\n')
print('what the same system does at thresholds you might actually deploy:')
for target in (0.01, 0.001):
    idx = int(np.argmin(np.abs(far - target)))
    print(f'  false acceptance {far[idx]:.3%}  ->  '
          f'false rejection {frr[idx]:.1%} at threshold {thresholds[idx]:.2f}')
print('\\nThat second column is what the user experiences, and the EER never '
      'mentions it.')"""),

    md("""## 2. Diarization, in three parts

Who spoke when. The output is a segmentation with speaker labels, and the error
has three separable components:

- **false alarm**: speech marked where there was none;
- **missed speech**: speech that was not marked;
- **speaker confusion**: speech marked, but attributed to the wrong speaker.

They have different causes and different fixes. A DER of 20 percent that is all
confusion is a clustering problem; the same 20 percent that is all missed
speech is a voice-activity problem. Reporting the total alone tells the reader
neither."""),

    code("""# a short two-speaker conversation, in seconds
REFERENCE = [(0.0, 3.2, 'A'), (3.2, 5.0, 'B'), (5.0, 8.4, 'A'),
             (8.4, 11.0, 'B'), (11.0, 12.5, 'A')]
HYPOTHESIS = [(0.2, 3.0, 'S1'), (3.0, 5.4, 'S2'), (5.4, 8.0, 'S1'),
              (8.0, 10.4, 'S1'), (10.4, 12.5, 'S2')]


def frames(segments, step=0.01, end=12.5):
    grid = np.arange(0, end, step)
    labels = np.full(len(grid), '', dtype=object)
    for start, stop, who in segments:
        labels[(grid >= start) & (grid < stop)] = who
    return grid, labels


def der(reference, hypothesis, step=0.01):
    _, ref = frames(reference, step)
    _, hyp = frames(hypothesis, step)
    speech = ref != ''
    total = speech.sum()
    false_alarm = ((ref == '') & (hyp != '')).sum()
    missed = (speech & (hyp == '')).sum()
    # map hypothesis labels to reference labels by best overlap
    mapping = {}
    for h in set(hyp) - {''}:
        counts = {r: ((hyp == h) & (ref == r)).sum() for r in set(ref) - {''}}
        mapping[h] = max(counts, key=counts.get)
    mapped = np.array([mapping.get(h, '') for h in hyp], dtype=object)
    confusion = (speech & (hyp != '') & (mapped != ref)).sum()
    return {'false alarm': false_alarm / total, 'missed': missed / total,
            'confusion': confusion / total,
            'DER': (false_alarm + missed + confusion) / total,
            'mapping': mapping}


result = der(REFERENCE, HYPOTHESIS)
for key in ('false alarm', 'missed', 'confusion', 'DER'):
    print(f'{key:>12}: {result[key]:6.1%}')
print(f'\\nhypothesis speakers mapped to reference: {result["mapping"]}')
print('The largest of the three components is the one to work on. Here it is '
      'the one the total would never have told you about.')"""),

    md("""## 3. Enhancement: the two measurements that disagree

Mix noise into clean speech, denoise it, and score the result twice.

The signal measure below is the scale-invariant signal-to-distortion ratio, one
of the three metrics Section 8.7 names. It is computed against the clean
reference, which is why it can only be measured on simulated mixtures and never
on the field audio a system will actually meet.

The transcript measure is the word error rate of a recognizer reading the
output. Section 8.7 reports a published case where denoising raised SI-SDR and
raised the error rate too. The OPTIONAL cell runs a real recognizer so you can
try to reproduce that on your own audio; without it, this cell shows the signal
side only, and says so."""),

    code("""def si_sdr(reference, estimate):
    # scale invariant: rescaling the estimate cannot change the score
    reference = reference - reference.mean()
    estimate = estimate - estimate.mean()
    alpha = (estimate @ reference) / (reference @ reference + 1e-12)
    target = alpha * reference
    noise = estimate - target
    return 10 * np.log10((target @ target + 1e-12) / (noise @ noise + 1e-12))


def denoise(noisy, frame=512, hop=128, floor=0.1, noise_frames=20):
    # a Wiener gain: the gain per bin is snr / (1 + snr), with a floor so the
    # gain never reaches zero, because a zeroed bin is where musical noise
    # comes from
    window = np.hanning(frame)
    n_frames = 1 + (len(noisy) - frame) // hop
    stft = np.array([np.fft.rfft(noisy[i * hop:i * hop + frame] * window)
                     for i in range(n_frames)])
    magnitude, phase = np.abs(stft), np.angle(stft)
    noise_power = np.mean(magnitude[:noise_frames] ** 2, axis=0)
    snr = np.maximum(magnitude ** 2 - noise_power, 0) / (noise_power + 1e-12)
    cleaned = magnitude * np.maximum(snr / (1 + snr), floor)
    out = np.zeros(len(noisy))
    norm = np.zeros(len(noisy))
    for i in range(n_frames):
        seg = np.fft.irfft(cleaned[i] * np.exp(1j * phase[i]), n=frame)
        out[i * hop:i * hop + frame] += seg * window
        norm[i * hop:i * hop + frame] += window ** 2
    # the floor on the normalizer matters: at the very first and last samples
    # only one tapered window contributes, and dividing by almost nothing
    # produces a spike that dominates every score computed afterwards
    return out / np.maximum(norm, 1e-3)


t = np.arange(int(2.0 * SR)) / SR
speech = np.sin(2 * np.pi * 180 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 3 * t))
speech += 0.3 * np.sin(2 * np.pi * 1400 * t) * (t % 0.25 < 0.12)
speech /= np.abs(speech).max()
# a moment of silence at the front, which is where the noise floor is measured
clean = np.concatenate([np.zeros(int(0.4 * SR)), speech])
inside = slice(1000, len(clean) - 1000)

print(f'{"SNR in":>8} {"SI-SDR noisy":>14} {"SI-SDR denoised":>17} '
      f'{"change":>9}')
for snr_db in (20, 10, 5, 0, -5):
    noise = rng.normal(scale=1.0, size=len(clean))
    scale = np.sqrt((clean @ clean) / (noise @ noise) / 10 ** (snr_db / 10))
    noisy = clean + scale * noise
    denoised = denoise(noisy)[:len(clean)]
    a = si_sdr(clean[inside], noisy[inside])
    b = si_sdr(clean[inside], denoised[inside])
    print(f'{snr_db:>6} dB {a:>13.2f} {b:>17.2f} {b - a:>+9.2f}')

print('\\nThe signal score improves. Whether the transcript does is a '
      'different question, and the only way to answer it is to run a '
      'recognizer over both and compare the word error rates. That is the '
      'comparison Section 8.7 reports, and the one to reproduce on your own '
      'audio in the cell below.')"""),

    code("""RUN_ASR = False        # needs transformers, torch and real Arabic audio

if RUN_ASR:
    from transformers import pipeline
    import soundfile as sf

    asr = pipeline('automatic-speech-recognition', model='openai/whisper-small',
                   generate_kwargs={'language': 'arabic'})
    CLIPS = []          # [(path, reference_transcript), ...]
    for path, reference in CLIPS:
        wav, sr = sf.read(path)
        noise = rng.normal(scale=0.05, size=len(wav))
        noisy = wav + noise
        denoised = denoise(noisy)[:len(wav)]
        for name, signal in (('clean', wav), ('noisy', noisy),
                             ('denoised', denoised)):
            sf.write(f'/tmp/{name}.wav', signal, sr)
            print(name, asr(f'/tmp/{name}.wav')['text'])
    print('Now compute WER for each condition and compare. If denoising '
          'lowered SI-SDR distortion and raised WER, you have reproduced '
          'the finding.')
else:
    print('skipped: needs a recognizer and real audio')"""),

    md(PROVENANCE),
    code(PROVENANCE_CODE),
]

save('ch08_speaker_and_noise.ipynb', speaker_noise,
     'Notebook 8.2  Who is speaking, and whether cleaning the audio helps',
     'Equal Error Rate, a Diarization Error Rate in three parts, and an '
     'enhancement test judged by the transcript.')
