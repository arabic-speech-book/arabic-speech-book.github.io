from nbbuild import md, code, save, PROVENANCE, PROVENANCE_CODE

cells = [
    md("""## What this notebook does

Both halves of Chapter 10, on a small set that runs offline.

1. **Cascade against direct.** The same five Arabic utterances translated two ways: through a transcript, and end to end. Scored with BLEU and chrF, both implemented here so nothing is hidden. Then the diagnosis the cascade allows and the direct model does not: which translation errors came from the recognizer.
2. **Spoken language understanding.** A small intent-and-slot parser over spoken Arabic commands, scored with intent accuracy and slot F1, and the normalization decision that quietly sets the slot score.

The recorded outputs below stand in for real systems. The OPTIONAL cells show
where a recognizer, a translator and a unified model plug in."""),

    code("""NOTEBOOK = 'ch10_speech_translation_slu.ipynb'

import re
from collections import Counter

import numpy as np

print('ready')"""),

    md("""## 1. BLEU and chrF, written out

BLEU counts matching n-grams of words, with a penalty for output that is too
short. chrF does the same over characters and is the better fit for a
morphologically rich language, because it gives partial credit for a word that
is right except for an affix.

Which way the translation runs decides how much this matters. Into English, the
target is morphologically simple and BLEU behaves. Into Arabic, one wrong
clitic costs a whole word in BLEU and almost nothing in chrF, and the two
metrics can rank two systems differently."""),

    code("""def ngrams(tokens, n):
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def bleu(references, hypotheses, max_n=4):
    clipped = [0] * max_n
    totals = [0] * max_n
    ref_len = hyp_len = 0
    for ref, hyp in zip(references, hypotheses):
        r, h = ref.split(), hyp.split()
        ref_len += len(r)
        hyp_len += len(h)
        for n in range(1, max_n + 1):
            ref_counts, hyp_counts = ngrams(r, n), ngrams(h, n)
            overlap = sum(min(c, ref_counts[g]) for g, c in hyp_counts.items())
            clipped[n - 1] += overlap
            totals[n - 1] += max(0, len(h) - n + 1)
    precisions = [(c / t) if t else 0.0 for c, t in zip(clipped, totals)]
    if min(precisions) == 0:
        return 0.0, precisions
    log_p = sum(np.log(p) for p in precisions) / max_n
    bp = 1.0 if hyp_len > ref_len else np.exp(1 - ref_len / max(1, hyp_len))
    return 100 * bp * np.exp(log_p), precisions


def chrf(references, hypotheses, n=6, beta=2):
    scores = []
    for ref, hyp in zip(references, hypotheses):
        r, h = ref.replace(' ', ''), hyp.replace(' ', '')
        precs, recs = [], []
        for k in range(1, n + 1):
            rc, hc = ngrams(list(r), k), ngrams(list(h), k)
            overlap = sum(min(c, rc[g]) for g, c in hc.items())
            precs.append(overlap / max(1, sum(hc.values())))
            recs.append(overlap / max(1, sum(rc.values())))
        p, rr = np.mean(precs), np.mean(recs)
        scores.append(0.0 if p + rr == 0 else
                      (1 + beta ** 2) * p * rr / (beta ** 2 * p + rr))
    return 100 * float(np.mean(scores))


print('metrics ready')"""),

    md("""## 2. The two architectures on the same audio

Five Arabic utterances. For each: the true transcript, the reference English,
what the cascade produced at each of its two stages, and what a direct model
produced.

Look at the third row before running anything. The recognizer misheard one
word, and the translator then translated the word it was given, faithfully and
wrongly. That is the failure mode a cascade has and a direct model does not:
an error handed on as though it were correct."""),

    code("""ITEMS = [
    {'truth': 'اين اقرب محطة بنزين',
     'reference': 'where is the nearest gas station',
     'asr': 'اين اقرب محطة بنزين',
     'cascade': 'where is the nearest gas station',
     'direct': 'where is the closest petrol station'},
    {'truth': 'اريد حجز موعد غدا صباحا',
     'reference': 'i want to book an appointment tomorrow morning',
     'asr': 'اريد حجز موعد غدا صباحا',
     'cascade': 'i want to book an appointment tomorrow morning',
     'direct': 'i would like an appointment tomorrow morning'},
    {'truth': 'الرحلة تصل الساعة سبعة',
     'reference': 'the flight arrives at seven',
     'asr': 'الرجلة تصل الساعة سبعة',          # one word misheard
     'cascade': 'the trip arrives at seven',
     'direct': 'the flight arrives at seven'},
    {'truth': 'كم سعر التذكرة الى الرياض',
     'reference': 'how much is the ticket to riyadh',
     'asr': 'كم سعر التذكرة الى الرياض',
     'cascade': 'how much is the ticket to riyadh',
     'direct': 'what is the price of the ticket to riyadh'},
    {'truth': 'الطقس حار جدا اليوم',
     'reference': 'the weather is very hot today',
     'asr': 'الطقس حار جدا اليوم',
     'cascade': 'the weather is very hot today',
     'direct': 'it is very hot today'},
]

refs = [i['reference'] for i in ITEMS]
for name in ('cascade', 'direct'):
    hyps = [i[name] for i in ITEMS]
    score, precisions = bleu(refs, hyps)
    print(f'{name:>8}:  BLEU {score:5.1f}   chrF {chrf(refs, hyps):5.1f}   '
          f'n-gram precisions ' +
          ' '.join(f'{p:.2f}' for p in precisions))
print('\\nTwo systems, and which one wins depends on the metric and on five '
      'sentences. Report the test set size beside the score, always.')"""),

    md("""### What the cascade lets you diagnose

The transcript in the middle is the cascade's cost and its gift. Because it
exists, a translation failure can be attributed: the recognizer was wrong, or
the translator was. A direct model gives you a bad translation and no way to
say which half of the problem it is."""),

    code("""def word_errors(truth, heard):
    t, h = truth.split(), heard.split()
    return [(a, b) for a, b in zip(t, h) if a != b] + \\
           ([('<length mismatch>', '')] if len(t) != len(h) else [])


for item in ITEMS:
    errs = word_errors(item['truth'], item['asr'])
    if errs:
        print(f'recognition error: {errs}')
        print(f'  the translator was given : {item["asr"]}')
        print(f'  and produced             : {item["cascade"]}')
        print(f'  the reference was        : {item["reference"]}')
        print('  The translation of the wrong word is correct. The stage to '
              'fix is the recognizer, and only the transcript says so.\\n')
asr_wer = np.mean([len(word_errors(i['truth'], i['asr'])) /
                   len(i['truth'].split()) for i in ITEMS])
print(f'recognition WER over the set: {asr_wer:.1%}')
print('Report it beside the translation score. A cascade result without the '
      'recognition error rate is a result with its cause removed.')"""),

    code("""# OPTIONAL: run real systems. Needs downloads and a few minutes.
RUN_REAL = False

if RUN_REAL:
    from transformers import pipeline

    asr = pipeline('automatic-speech-recognition', model='openai/whisper-small',
                   generate_kwargs={'language': 'arabic'})
    mt = pipeline('translation', model='Helsinki-NLP/opus-mt-ar-en')
    AUDIO = []          # [(path, reference_english), ...]
    for path, reference in AUDIO:
        transcript = asr(path)['text']
        english = mt(transcript)[0]['translation_text']
        print(f'{path}\\n  transcript: {transcript}\\n  cascade: {english}')
else:
    print('skipped: using the recorded outputs above')"""),

    md("""## 3. Spoken language understanding

Intent detection asks what the speaker wants. Slot filling asks with what
arguments. Both are scored simply, and both hide the same Arabic decision: when
are two spellings of a slot value the same value?

`الرياض` and `الریاض` differ in one character. `غدا` and `غداً` differ in a
diacritic. Under one normalization the slot is right; under another it is
wrong. The chapter asks for that decision to be settled before annotation and
reported with the score, and the cell below shows what it is worth."""),

    code("""COMMANDS = [
    ('احجز لي موعد غدا الساعة تسعة',
     {'intent': 'book_appointment', 'date': 'غدا', 'time': 'تسعة'}),
    ('كم سعر التذكرة الى الرياض',
     {'intent': 'ask_price', 'destination': 'الرياض'}),
    ('شغل الاغاني',
     {'intent': 'play_music'}),
    ('الغي الموعد بكرة',
     {'intent': 'cancel_appointment', 'date': 'بكرة'}),
    ('وين اقرب صيدلية',
     {'intent': 'find_place', 'place': 'صيدلية'}),
]

INTENT_RULES = [
    ('book_appointment', ['احجز', 'حجز', 'ابغى موعد']),
    ('cancel_appointment', ['الغي', 'الغاء']),
    ('ask_price', ['كم سعر', 'بكم', 'السعر']),
    ('play_music', ['شغل', 'اسمع']),
    ('find_place', ['وين', 'اين', 'اقرب']),
]
TIME_WORDS = ['واحدة', 'اثنين', 'ثلاثة', 'اربعة', 'خمسة', 'ستة', 'سبعة',
              'ثمانية', 'تسعة', 'عشرة']
DATE_WORDS = ['اليوم', 'غدا', 'بكرة', 'بعد', 'الاحد', 'الاثنين']
PLACE_WORDS = ['صيدلية', 'مستشفى', 'مطعم', 'محطة', 'مكتبة']


def parse(text):
    out = {'intent': 'unknown'}
    for intent, cues in INTENT_RULES:
        if any(cue in text for cue in cues):
            out['intent'] = intent
            break
    words = text.split()
    for w in words:
        if w in DATE_WORDS:
            out['date'] = w
        if w in TIME_WORDS:
            out['time'] = w
        if w in PLACE_WORDS:
            out['place'] = w
        if w.startswith('الري') or w in ('جدة', 'الدمام'):
            out['destination'] = w
    return out


def score(gold_all, pred_all, normalize=lambda s: s):
    correct_intent = 0
    tp = fp = fn = 0
    for gold, pred in zip(gold_all, pred_all):
        correct_intent += gold['intent'] == pred['intent']
        g = {(k, normalize(v)) for k, v in gold.items() if k != 'intent'}
        p = {(k, normalize(v)) for k, v in pred.items() if k != 'intent'}
        tp += len(g & p)
        fp += len(p - g)
        fn += len(g - p)
    precision = tp / max(1, tp + fp)
    recall = tp / max(1, tp + fn)
    f1 = 0 if precision + recall == 0 else \\
        2 * precision * recall / (precision + recall)
    return correct_intent / len(gold_all), f1


gold = [g for _, g in COMMANDS]
pred = [parse(t) for t, _ in COMMANDS]
accuracy, f1 = score(gold, pred)
print(f'intent accuracy : {accuracy:.1%}')
print(f'slot F1         : {f1:.3f}\\n')
for (text, g), p in zip(COMMANDS, pred):
    mark = 'ok ' if g['intent'] == p['intent'] else 'BAD'
    print(f'  {mark} {text}\\n      gold {g}\\n      pred {p}')"""),

    md("""### The normalization that sets the slot score

Same predictions, same references, two normalizations. The score moves. Neither
is wrong; what would be wrong is not saying which one produced the number."""),

    code("""DIACRITICS = set(chr(c) for c in range(0x064B, 0x0653))


def strict(value):
    return value


def lenient(value):
    value = ''.join(c for c in value if c not in DIACRITICS)
    for a in 'أإآ':
        value = value.replace(a, 'ا')
    return value.replace('ة', 'ه').replace('ى', 'ي')


# a prediction that differs from the reference only in spelling
noisy_pred = [dict(p) for p in pred]
if 'destination' in noisy_pred[1]:
    noisy_pred[1]['destination'] = 'الریاض'      # a different ya
if 'date' in noisy_pred[0]:
    noisy_pred[0]['date'] = 'غداً'               # with tanwin

for name, fn in (('strict', strict), ('lenient', lenient)):
    a, f = score(gold, noisy_pred, fn)
    print(f'{name:>8} matching: intent accuracy {a:.1%}, slot F1 {f:.3f}')
print('\\nThe predictions did not change. The definition of "the same value" '
      'did. Settle it in the annotation guideline, apply it to the reference '
      'and the prediction alike, and print it beside the score.')"""),

    md(PROVENANCE),
    code(PROVENANCE_CODE),
]

save('ch10_speech_translation_slu.ipynb', cells,
     'Notebook 10.1  Cascade against direct, and a small understanding parser',
     'BLEU and chrF from scratch, error attribution across the two stages, '
     'and the normalization that sets the slot score.')
