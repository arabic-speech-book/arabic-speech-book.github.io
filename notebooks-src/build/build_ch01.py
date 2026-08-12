from nbbuild import md, code, save, PROVENANCE, PROVENANCE_CODE

cells = [
    md("""## What this notebook does

You will run a recognizer on Arabic audio, score it, and then change one thing
that is not the model: the text normalization applied before scoring. The
second number will be different from the first. That gap is the argument of
Section 1.5 and of the whole book, and it is easier to believe once you have
produced it yourself.

Three steps:

1. score a transcript against a reference with Word Error Rate and Character Error Rate, written out in full so nothing is hidden;
2. apply Arabic normalization and score again;
3. compare Modern Standard Arabic against dialect, and write down what you saw."""),

    code("""NOTEBOOK = 'ch01_first_contact_arabic_asr.ipynb'

# OPTIONAL, and only in Colab or a local environment with a GPU:
# !pip install -q transformers torch soundfile datasets

import unicodedata

try:
    import transformers  # noqa: F401
    import torch  # noqa: F401
    HAVE_MODEL = True
except ImportError:
    HAVE_MODEL = False

print('a real recognizer is available' if HAVE_MODEL else
      'no recognizer installed: the notebook will use the recorded outputs '
      'below, which is enough for everything except hearing the audio')"""),

    md("""## 1. Word Error Rate, written out

WER is edit distance at the level of words, divided by the number of words in
the reference. Three kinds of mistake count equally: a word substituted, a word
deleted, a word inserted. The implementation below is the standard dynamic
program. It is short, and reading it once removes the temptation to treat WER
as a black box.

Character Error Rate is the same computation over characters. For Arabic it is
often the fairer of the two, because a single wrong affix on a long word costs
a whole word in WER and only a character or two in CER."""),

    code("""def edit_counts(ref, hyp):
    \"\"\"Levenshtein distance with the three error types counted separately.\"\"\"
    n, m = len(ref), len(hyp)
    # d[i][j] = cheapest way to turn ref[:i] into hyp[:j]
    d = [[(0, 0, 0, 0)] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        d[i][0] = (i, 0, 0, i)          # cost, sub, ins, del
    for j in range(1, m + 1):
        d[0][j] = (j, 0, j, 0)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if ref[i - 1] == hyp[j - 1]:
                d[i][j] = d[i - 1][j - 1]
                continue
            sub = d[i - 1][j - 1]
            ins = d[i][j - 1]
            dele = d[i - 1][j]
            best = min((sub[0] + 1, sub[1] + 1, sub[2], sub[3]),
                       (ins[0] + 1, ins[1], ins[2] + 1, ins[3]),
                       (dele[0] + 1, dele[1], dele[2], dele[3] + 1))
            d[i][j] = best
    cost, sub, ins, dele = d[n][m]
    return {'errors': cost, 'substitutions': sub, 'insertions': ins,
            'deletions': dele, 'reference_length': n}


def wer(reference, hypothesis):
    c = edit_counts(reference.split(), hypothesis.split())
    return c['errors'] / max(1, c['reference_length']), c


def cer(reference, hypothesis):
    c = edit_counts(list(reference.replace(' ', '')),
                    list(hypothesis.replace(' ', '')))
    return c['errors'] / max(1, c['reference_length']), c"""),

    md("""## 2. The clips

Five short utterances: one read Modern Standard Arabic sentence of the kind a
broadcast corpus is full of, and four spoken in dialect. The hypotheses below
are what a multilingual recognizer produced for them. If you have the model
installed, the OPTIONAL cell further down will overwrite these with your own
run, and everything after it is unchanged.

Replace these with your own audio and your own references as soon as you can.
The lesson lands harder on speech you recognise."""),

    code("""CLIPS = [
    {'id': 'msa-1', 'variety': 'MSA',
     'reference': 'أَعْلَنَتِ الوِزارَةُ عَنْ خِطَّةٍ جَديدَةٍ لِلتَّعْليمِ',
     'hypothesis': 'اعلنت الوزارة عن خطة جديدة للتعليم'},
    {'id': 'gulf-1', 'variety': 'Gulf',
     'reference': 'وين أقرب محطة بنزين',
     'hypothesis': 'أين أقرب محطة بنزين'},
    {'id': 'gulf-2', 'variety': 'Gulf',
     'reference': 'أبغى أحجز موعد بكرة الصبح',
     'hypothesis': 'أبقى أحجز موعد بكره الصبح'},
    {'id': 'egyptian-1', 'variety': 'Egyptian',
     'reference': 'عايز أروح المطار دلوقتي',
     'hypothesis': 'عاوز اروح المطار دلوقت'},
    {'id': 'maghrebi-1', 'variety': 'Maghrebi',
     'reference': 'بغيت نمشي للدار دابا',
     'hypothesis': 'بغيت نمشي الدار دبا'},
]

for c in CLIPS:
    w, _ = wer(c['reference'], c['hypothesis'])
    ch, _ = cer(c['reference'], c['hypothesis'])
    print(f"{c['id']:>12}  {c['variety']:>9}   WER {w:6.1%}   CER {ch:6.1%}")"""),

    md("""### OPTIONAL: run a real recognizer

This cell needs a download and a few minutes. It transcribes whatever audio you
put in `AUDIO`, and writes the result back into `CLIPS` so the rest of the
notebook scores your own run. Nothing below depends on it.

Use openly licensed audio. Common Voice Arabic is the usual starting point;
state the release version and the licence in the provenance cell at the end,
because both change."""),

    code("""AUDIO = {}   # {'msa-1': 'path/to/clip.wav', ...}

if HAVE_MODEL and AUDIO:
    from transformers import pipeline
    asr = pipeline('automatic-speech-recognition',
                   model='openai/whisper-small',
                   generate_kwargs={'language': 'arabic'})
    for c in CLIPS:
        path = AUDIO.get(c['id'])
        if path:
            c['hypothesis'] = asr(path)['text'].strip()
            print(f"{c['id']}: {c['hypothesis']}")
else:
    print('skipped: using the recorded hypotheses above')"""),

    md("""## 3. Normalization, the step that moves the number

Arabic writing offers several ways to write the same word. The short vowels are
optional, so most text carries none. Hamza on alef is written or dropped. Final
ya and alef maqsura are interchanged. Ta marbuta and ha are confused at the end
of a word. None of these is a recognition error in any sense a reader cares
about, and all of them cost a full word in WER.

Normalization decides which of these differences to forgive. That is a
judgement, not a preprocessing detail, which is why this book asks for the
normalization to be reported beside every number. Edit the function, rerun, and
watch the same system get better or worse without changing at all."""),

    code("""DIACRITICS = ''.join(chr(c) for c in range(0x064B, 0x0653)) + '\\u0670\\u0640'

def normalize(text, strip_diacritics=True, unify_alef=True,
              unify_ya=True, unify_ta_marbuta=True, drop_punctuation=True):
    text = unicodedata.normalize('NFC', text)
    if strip_diacritics:
        text = ''.join(ch for ch in text if ch not in DIACRITICS)
    if unify_alef:
        for a in 'أإآٱ':
            text = text.replace(a, 'ا')
    if unify_ya:
        text = text.replace('ى', 'ي')
    if unify_ta_marbuta:
        text = text.replace('ة', 'ه')
    if drop_punctuation:
        for p in '.,!?؟،؛:"\\'()':
            text = text.replace(p, ' ')
    return ' '.join(text.split())


print('raw       :', CLIPS[0]['reference'])
print('normalized:', normalize(CLIPS[0]['reference']))"""),

    code("""print(f"{'clip':>12} {'variety':>9} {'WER raw':>9} {'WER norm':>9} "
      f"{'CER raw':>9} {'CER norm':>9}")
rows = []
for c in CLIPS:
    raw_w, _ = wer(c['reference'], c['hypothesis'])
    raw_c, _ = cer(c['reference'], c['hypothesis'])
    nrm_w, _ = wer(normalize(c['reference']), normalize(c['hypothesis']))
    nrm_c, _ = cer(normalize(c['reference']), normalize(c['hypothesis']))
    rows.append((c['variety'], raw_w, nrm_w))
    print(f"{c['id']:>12} {c['variety']:>9} {raw_w:9.1%} {nrm_w:9.1%} "
          f"{raw_c:9.1%} {nrm_c:9.1%}")"""),

    md("""## 4. Modern Standard Arabic against dialect

A pooled average over these five clips is the number a system would report. It
is also the number that hides what happened. Split it."""),

    code("""from collections import defaultdict

by_variety = defaultdict(list)
for variety, raw_w, nrm_w in rows:
    by_variety[variety].append(nrm_w)

pooled = sum(w for _, _, w in rows) / len(rows)
print(f'pooled WER after normalization: {pooled:.1%}\\n')
for variety, values in sorted(by_variety.items()):
    print(f'{variety:>10}: {sum(values) / len(values):6.1%}   '
          f'({len(values)} clip{"s" if len(values) > 1 else ""})')
print('\\nA pooled figure is an average of things that are not the same thing.')"""),

    md("""## 5. Your turn

Answer these in the cell below, in your own words. They are the reflection the
chapter asks for, and they are worth more than the code above.

1. Which error did normalization forgive in each clip? Name the exact character.
2. Which dialect failed worst, and is the failure in the vocabulary, the spelling, or the pronunciation? You can tell them apart by looking at the aligned words.
3. Suppose you report only the pooled WER. Which reader is misled, and about what?
4. Turn one option in `normalize` off and rerun. How many points did that decision move? Would you have thought to report it?"""),

    code("""REFLECTION = '''
1.
2.
3.
4.
'''
print(REFLECTION)"""),

    md(PROVENANCE),
    code(PROVENANCE_CODE),
]

save('ch01_first_contact_arabic_asr.ipynb', cells,
     'Notebook 1.1  First contact with Arabic ASR',
     'Run a recognizer on Arabic, score it, and watch normalization move the '
     'number.')
