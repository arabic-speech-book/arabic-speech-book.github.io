from nbbuild import md, code, save, PROVENANCE, PROVENANCE_CODE

cells = [
    md("""## What this notebook does

The three end-to-end ideas of Chapter 5, on examples small enough to check by
hand. No training, no downloads, nothing that takes longer than a second.

1. CTC: enumerate every alignment of a short target, collapse them, and sum their probabilities with the forward recursion.
2. The transducer: walk the emit-or-advance lattice and see why the alignment is monotonic.
3. Beam search with shallow fusion: watch a language-model weight reshape the ranking, and watch too much of it break the transcript.
4. Output units on an Arabic sentence: characters, subwords, morphemes."""),

    code("""NOTEBOOK = 'ch05_end_to_end_arabic_asr.ipynb'

import numpy as np
from itertools import product

BLANK = '-'
print('ready')"""),

    md("""## 1. CTC: alignments and the blank

CTC solves the alignment problem by adding one symbol, the blank, and declaring
that a frame-level labelling collapses to a transcript by two rules: squash runs
of the same symbol, then delete the blanks.

Two consequences follow immediately, and both are exam questions:

- a target with a doubled symbol needs a blank between the two, or they collapse into one;
- many frame labellings give the same transcript, which is why the loss sums over all of them instead of choosing one."""),

    code("""def collapse(labelling):
    out = []
    for sym in labelling:
        if not out or sym != out[-1]:
            out.append(sym)
    return ''.join(s for s in out if s != BLANK)


TARGET, T = 'AB', 4
alphabet = ['A', 'B', BLANK]
valid = [''.join(p) for p in product(alphabet, repeat=T)
         if collapse(p) == TARGET]
print(f'target {TARGET!r} over {T} frames: {len(valid)} valid labellings')
for v in valid:
    print(f'   {v}  ->  {collapse(v)}')

print(f"\\nand the trap: {'AA'!r} needs a blank between the two A's")
for p in ['AA--', 'A-A-', 'AAA-']:
    print(f'   {p}  ->  {collapse(p)!r}')"""),

    md("""### The CTC forward sum

With a toy network output, the probability of the target is the sum over those
labellings. The brute-force sum and the forward recursion must agree, and the
recursion is the one that stays feasible when the transcript is a sentence."""),

    code("""probs = np.array([          # frames x {A, B, blank}
    [0.6, 0.2, 0.2],
    [0.3, 0.4, 0.3],
    [0.2, 0.5, 0.3],
    [0.1, 0.6, 0.3],
])
index = {'A': 0, 'B': 1, BLANK: 2}

brute = sum(np.prod([probs[t, index[s]] for t, s in enumerate(v)])
            for v in valid)

# the recursion, over the target padded with blanks
ext = BLANK + BLANK.join(TARGET) + BLANK
S = len(ext)
alpha = np.zeros((T, S))
alpha[0, 0] = probs[0, index[ext[0]]]
alpha[0, 1] = probs[0, index[ext[1]]]
for t in range(1, T):
    for s in range(S):
        total = alpha[t - 1, s]
        if s > 0:
            total += alpha[t - 1, s - 1]
        if s > 1 and ext[s] != BLANK and ext[s] != ext[s - 2]:
            total += alpha[t - 1, s - 2]
        alpha[t, s] = total * probs[t, index[ext[s]]]
recursion = alpha[T - 1, S - 1] + alpha[T - 1, S - 2]

print(f'padded target: {ext}')
print(f'brute force over {len(valid)} labellings : {brute:.6f}')
print(f'forward recursion                  : {recursion:.6f}')
print(f'CTC loss = -log P                  : {-np.log(recursion):.4f}')"""),

    md("""## 2. The transducer: emit or advance

CTC assumes the outputs are conditionally independent given the audio. The
transducer removes that assumption by adding a prediction network over what has
been emitted so far, and it keeps the alignment monotonic: at every lattice
node the model either emits a token and moves up, or emits blank and moves
right in time. It never goes back.

That is exactly why the transducer is the natural choice for streaming: the
walk below can be run as the audio arrives."""),

    code("""def transducer_walk(emit_probs, target):
    # emit_probs[t][u] = probability of emitting target[u] at frame t
    T_, U = emit_probs.shape
    t = u = 0
    path = []
    while t < T_ - 1 or u < U:
        if u < U and emit_probs[min(t, T_ - 1), u] > 0.5:
            path.append((t, u, f'emit {target[u]!r}'))
            u += 1
        else:
            path.append((t, u, 'blank, advance time'))
            t += 1
        if t >= T_ and u < U:                 # ran out of audio
            path.append((t, u, 'out of frames with tokens left'))
            break
    return path


target = 'ABC'
emit = np.array([
    [0.9, 0.1, 0.0],
    [0.2, 0.8, 0.1],
    [0.1, 0.3, 0.7],
    [0.1, 0.1, 0.6],
])
for t, u, action in transducer_walk(emit, target):
    print(f'  t={t}  u={u}  {action}')
print('\\nTime never decreases and the emitted prefix never shrinks: that is '
      'what monotonic means, and it is what lets the model run online.')"""),

    md("""## 3. Beam search, and what shallow fusion does to it

Beam search keeps the best few prefixes at each step instead of committing to
the single best token. Shallow fusion adds a language-model score to the
acoustic score, weighted by a number you choose.

The weight is not a detail. Too little and the model spells out something no
Arabic speaker would write. Too much and the language model overrules the audio
and writes a fluent sentence that was never spoken. The sweep below shows both
ends."""),

    code("""VOCAB = ['ذهب', 'ذهبت', 'الى', 'المكتبة', 'المدرسة', '</s>']

# a toy acoustic model: per step, a distribution over the vocabulary
acoustic = np.array([
    [0.22, 0.60, 0.05, 0.05, 0.05, 0.03],
    [0.02, 0.02, 0.90, 0.03, 0.02, 0.01],
    [0.01, 0.01, 0.03, 0.45, 0.48, 0.02],
    [0.01, 0.01, 0.01, 0.01, 0.01, 0.95],
])

# a toy bigram language model, trained on text where المكتبة is the common object
LM = {
    ('<s>', 'ذهب'): 0.62, ('<s>', 'ذهبت'): 0.38,
    ('ذهب', 'الى'): 0.9, ('ذهبت', 'الى'): 0.9,
    ('الى', 'المكتبة'): 0.75, ('الى', 'المدرسة'): 0.25,
    ('المكتبة', '</s>'): 1.0, ('المدرسة', '</s>'): 1.0,
}


def lm_score(prev, word):
    return np.log(LM.get((prev, word), 1e-4))


def beam_search(alpha_lm=0.0, beam=3):
    beams = [(0.0, ['<s>'])]
    for t in range(len(acoustic)):
        scored = []
        for score, prefix in beams:
            for i, word in enumerate(VOCAB):
                s = score + np.log(acoustic[t, i] + 1e-12) \\
                    + alpha_lm * lm_score(prefix[-1], word)
                scored.append((s, prefix + [word]))
        beams = sorted(scored, key=lambda x: -x[0])[:beam]
    return beams


for weight in (0.0, 0.5, 1.0, 3.0):
    best_score, best = beam_search(weight)[0]
    print(f'LM weight {weight:>4}:  {" ".join(best[1:])}   '
          f'(score {best_score:.2f})')
print('\\nAt zero the audio decides alone, and it picks the object it barely '
      'preferred. In the middle the language model settles that genuine '
      'ambiguity. At three it has overruled the audio on the verb, which the '
      'audio was not ambiguous about: that is the language model writing the '
      'sentence rather than helping to read it.')"""),

    md("""## 4. Output units for Arabic

The chapter's Arabic-specific question: what should the model emit? Characters
never go out of vocabulary and make long sequences. Words are short sequences
and go out of vocabulary constantly, which for Arabic is not a corner case but
the normal state. Subwords sit in between, and morphemes align with how Arabic
is actually built.

For dialect, there is a further problem the table does not show: there is no
standard spelling, so two annotators write the same spoken word differently and
the model is asked to learn both."""),

    code("""SENTENCE = 'وبكتابهم ذهب الطلاب الى المكتبة'
PROCLITICS = ['وب', 'بال', 'وال', 'ال', 'و', 'ب', 'ل', 'ك']
ENCLITICS = ['هم', 'ها', 'نا', 'ه', 'ك']


def morphemes(word):
    head = []
    for p in PROCLITICS:
        if word.startswith(p) and len(word) - len(p) >= 3:
            head.append(p + '+')
            word = word[len(p):]
    tail = []
    for e in ENCLITICS:
        if word.endswith(e) and len(word) - len(e) >= 3:
            tail.insert(0, '+' + e)
            word = word[:-len(e)]
    return head + [word] + tail


units = {
    'word': SENTENCE.split(),
    'character': list(SENTENCE.replace(' ', '')),
    'morpheme': [m for w in SENTENCE.split() for m in morphemes(w)],
}
for name, toks in units.items():
    print(f'{name:>10}: {len(toks):>3} tokens   {" ".join(toks)}')

print('\\nSpelling variants of one spoken dialect word, all attested:')
for variant in ['وين', 'فين', 'وينه', 'وين هو']:
    print(f'   {variant}')
print('A model with characters as its output unit can produce all of them. '
      'A word-level model has to have seen each one.')"""),

    md(PROVENANCE),
    code(PROVENANCE_CODE),
]

save('ch05_end_to_end_arabic_asr.ipynb', cells,
     'Notebook 5.1  Alignments, blanks, and beams',
     'CTC, the transducer, beam search with shallow fusion, and the choice of '
     'output unit.')
