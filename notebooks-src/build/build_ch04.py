from nbbuild import md, code, save, PROVENANCE, PROVENANCE_CODE

cells = [
    md("""## What this notebook does

Four of the chapter's ideas, made runnable:

1. Word Error Rate and Character Error Rate on Arabic, with and without the normalization of Table 4.2, so the size of that decision is a number rather than a warning.
2. The same sentence tokenized four ways, with the vocabulary each one implies.
3. The forward algorithm on the chapter's toy hidden Markov model, by hand and in code, so the two agree.
4. Kneser-Ney continuation counts on a small corpus, which is where the smoothing intuition lives.

No downloads. Bring your own sentences whenever you like."""),

    code("""NOTEBOOK = 'ch04_arabic_asr_foundations.ipynb'

import unicodedata
from collections import Counter, defaultdict

import numpy as np

print('ready')"""),

    md("""## 1. Scoring, and the normalization that moves it

The normalization below is the one described in Table 4.2: strip the optional
diacritics, unify the alef forms, unify final ya and alef maqsura, unify ta
marbuta with ha, remove tatweel and punctuation.

Every one of those is a decision about what counts as the same word. Together
they can move an Arabic WER by several points without touching the model, which
is why the chapter insists the normalization is reported with the score."""),

    code("""DIACRITICS = set(chr(c) for c in range(0x064B, 0x0653)) | {'\\u0670'}
TATWEEL = '\\u0640'


def normalize(text, diacritics=True, alef=True, ya=True, ta=True,
              punctuation=True):
    text = unicodedata.normalize('NFC', text)
    if diacritics:
        text = ''.join(c for c in text if c not in DIACRITICS)
    text = text.replace(TATWEEL, '')
    if alef:
        for a in 'أإآٱ':
            text = text.replace(a, 'ا')
    if ya:
        text = text.replace('ى', 'ي')
    if ta:
        text = text.replace('ة', 'ه')
    if punctuation:
        for p in '.,!?؟،؛:"()':
            text = text.replace(p, ' ')
    return ' '.join(text.split())


def error_rate(reference, hypothesis, unit='word'):
    ref = reference.split() if unit == 'word' else list(reference.replace(' ', ''))
    hyp = hypothesis.split() if unit == 'word' else list(hypothesis.replace(' ', ''))
    n, m = len(ref), len(hyp)
    d = np.zeros((n + 1, m + 1), dtype=int)
    d[:, 0] = np.arange(n + 1)
    d[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1,
                          d[i - 1, j - 1] + (ref[i - 1] != hyp[j - 1]))
    return d[n, m] / max(1, n)


PAIRS = [
    ('أَعْلَنَتِ الوِزارَةُ عَنْ خِطَّةٍ جَديدَة',
     'اعلنت الوزارة عن خطة جديدة'),
    ('إنَّ المَدينَةَ الكُبْرى قَريبَةٌ',
     'ان المدينه الكبرى قريبة'),
    ('ذَهَبَ إلى المَكْتَبَةِ صَباحاً',
     'ذهب الى المكتبه صباحا'),
]

print(f'{"raw WER":>9} {"norm WER":>9} {"raw CER":>9} {"norm CER":>9}')
for ref, hyp in PAIRS:
    print(f'{error_rate(ref, hyp):9.1%} '
          f'{error_rate(normalize(ref), normalize(hyp)):9.1%} '
          f'{error_rate(ref, hyp, "char"):9.1%} '
          f'{error_rate(normalize(ref), normalize(hyp), "char"):9.1%}')"""),

    md("""### Which switch was worth how much

Turn the options on one at a time. The column that moves most is the decision
your reader most needs told."""),

    code("""SWITCHES = ['diacritics', 'alef', 'ya', 'ta', 'punctuation']
base = np.mean([error_rate(r, h) for r, h in PAIRS])
print(f'no normalization at all      : {base:6.1%}')
opts = {k: False for k in SWITCHES}
for switch in SWITCHES:
    opts[switch] = True
    w = np.mean([error_rate(normalize(r, **opts), normalize(h, **opts))
                 for r, h in PAIRS])
    print(f'+ {switch:<26}: {w:6.1%}')"""),

    md("""## 2. Tokenization, and the vocabulary it implies

Arabic builds words from a root on a pattern and then attaches clitics, so the
number of distinct written words is enormous and most of them are rare. What
you choose as the unit decides how large the vocabulary is, how many tokens a
sentence becomes, and how often the model meets something it has never seen.

Four units, on one sentence: words, characters, subwords learned by byte-pair
encoding, and morphemes stripped by a small clitic rule."""),

    code("""SENTENCE = 'وَبِكِتابِهِمْ ذَهَبَ الطُّلابُ إلى المَكْتَبَةِ'
PLAIN = normalize(SENTENCE)

PROCLITICS = ['وب', 'فب', 'وال', 'فال', 'بال', 'كال', 'لل', 'ال', 'و', 'ف',
              'ب', 'ك', 'ل', 'س']
ENCLITICS = ['هما', 'كما', 'هم', 'هن', 'كم', 'كن', 'ها', 'نا', 'ه', 'ك', 'ي']


def morphemes(word):
    parts = []
    changed = True
    while changed:
        changed = False
        for p in PROCLITICS:
            if word.startswith(p) and len(word) - len(p) >= 3:
                parts.append(p + '+')
                word = word[len(p):]
                changed = True
                break
    tail = []
    changed = True
    while changed:
        changed = False
        for e in ENCLITICS:
            if word.endswith(e) and len(word) - len(e) >= 3:
                tail.insert(0, '+' + e)
                word = word[:-len(e)]
                changed = True
                break
    return parts + [word] + tail


def learn_bpe(corpus, merges=60):
    vocab = Counter(' '.join(w) + ' </w>' for w in corpus.split())
    rules = []
    for _ in range(merges):
        pairs = Counter()
        for word, freq in vocab.items():
            sym = word.split()
            for a, b in zip(sym, sym[1:]):
                pairs[(a, b)] += freq
        if not pairs:
            break
        best = max(pairs, key=pairs.get)
        rules.append(best)
        joined = ' '.join(best)
        vocab = Counter({w.replace(joined, ''.join(best)): f
                         for w, f in vocab.items()})
    return rules


def apply_bpe(word, rules):
    sym = list(word) + ['</w>']
    for a, b in rules:
        i = 0
        while i < len(sym) - 1:
            if sym[i] == a and sym[i + 1] == b:
                sym[i:i + 2] = [a + b]
            else:
                i += 1
    return sym


CORPUS = (PLAIN + ' ' + normalize(
    'ذهب الطلاب الى المكتبة وبكتابهم قرأوا الكتاب والمكتبة كبيرة '
    'وكتب الطالب في الكتاب'))
rules = learn_bpe(CORPUS, merges=18)

units = {
    'word': PLAIN.split(),
    'character': list(PLAIN.replace(' ', '')),
    'subword (BPE)': [s for w in PLAIN.split() for s in apply_bpe(w, rules)],
    'morpheme': [m for w in PLAIN.split() for m in morphemes(w)],
}
print(f'sentence: {PLAIN}\\n')
for name, toks in units.items():
    print(f'{name:>14}: {len(toks):>3} tokens, '
          f'{len(set(toks)):>3} distinct   {" ".join(toks[:12])}'
          f'{" ..." if len(toks) > 12 else ""}')"""),

    md("""## 3. The forward algorithm, by hand and in code

A two-state model, three observations. The forward algorithm sums the
probability of every path that could have produced the sequence, one time step
at a time, which is what makes it linear rather than exponential.

Do it by hand first with the numbers below, then run the cell. If the two
disagree, the hand version is usually right and the indexing is usually wrong."""),

    code("""states = ['s1', 's2']
pi = np.array([0.6, 0.4])                       # initial
A = np.array([[0.7, 0.3],                       # transition
              [0.4, 0.6]])
B = np.array([[0.5, 0.4, 0.1],                  # emission, per observation
              [0.1, 0.3, 0.6]])
obs = [0, 1, 2]

alpha = np.zeros((len(obs), len(states)))
alpha[0] = pi * B[:, obs[0]]
print(f't=0  alpha = {alpha[0].round(4)}')
for t in range(1, len(obs)):
    alpha[t] = (alpha[t - 1] @ A) * B[:, obs[t]]
    print(f't={t}  alpha = {alpha[t].round(4)}')
print(f'\\nP(observations) = {alpha[-1].sum():.6f}')

# the same thing the slow way, to prove the recursion is doing what it claims
from itertools import product
total = sum(
    pi[p[0]] * B[p[0], obs[0]] *
    np.prod([A[p[i], p[i + 1]] * B[p[i + 1], obs[i + 1]]
             for i in range(len(obs) - 1)])
    for p in product(range(len(states)), repeat=len(obs)))
print(f'sum over all {len(states) ** len(obs)} paths = {total:.6f}')"""),

    md("""## 4. Kneser-Ney, and why raw counts mislead

The idea in one sentence: a word that appears in many different contexts
deserves probability in a new context, and a word that appears often but always
after the same word does not.

The classic example is a word that is frequent only because it completes one
fixed expression. Its raw count is high; its continuation count, the number of
distinct words it has followed, is low. Kneser-Ney backs off to the second."""),

    code("""SMALL = normalize('''
ذهب الطالب الى المكتبة
ذهب المعلم الى المدرسة
قرأ الطالب الكتاب في المكتبة
كتب المعلم الدرس على السبورة
الطالب في المكتبة والمعلم في المدرسة
مدينة الرياض كبيرة ومدينة جدة كبيرة
''').split()

unigram = Counter(SMALL)
bigram = Counter(zip(SMALL, SMALL[1:]))
continuation = defaultdict(set)
for a, b in bigram:
    continuation[b].add(a)

print(f'{"word":>10} {"raw count":>10} {"distinct predecessors":>22}')
for word, count in unigram.most_common(8):
    print(f'{word:>10} {count:>10} {len(continuation[word]):>22}')

print('\\nThe ranking by raw count and the ranking by continuation count are '
      'not the same, and the second is the one that predicts what can follow '
      'a word the model has not seen before.')

D = 0.75          # the usual absolute discount
total_bigrams = sum(bigram.values())
p_cont = {w: len(continuation[w]) / len(bigram) for w in unigram}
print('\\ncontinuation probability, the Kneser-Ney lower order term:')
for w in sorted(p_cont, key=p_cont.get, reverse=True)[:6]:
    print(f'  {w:>10}  {p_cont[w]:.4f}')"""),

    md("""## 5. What to report

The chapter's Reproducibility Note asks for nine things. Fill them in from the
run above, and keep the habit: it is cheaper to record them now than to
reconstruct them when a reviewer asks."""),

    code("""REPORT = {
    'normalization script': 'the normalize() above, with which switches on',
    'diacritization policy': 'references undiacritized, hypotheses undiacritized',
    'tokenizer and vocabulary size': f'BPE, {len(rules)} merges',
    'acoustic data and splits': 'fill in',
    'language-model text': 'fill in, or none',
    'lexicon or G2P source': 'fill in, or none',
    'augmentation policy': 'fill in, or none',
    'dialect balance': 'fill in the hours per dialect',
    'per-dialect WER or CER': 'fill in, never only the pooled figure',
}
for k, v in REPORT.items():
    print(f'{k:>30}: {v}')"""),

    md(PROVENANCE),
    code(PROVENANCE_CODE),
]

save('ch04_arabic_asr_foundations.ipynb', cells,
     'Notebook 4.1  From scores to transcripts',
     'Scoring, normalization, tokenization, the forward algorithm, and '
     'continuation counts.')
