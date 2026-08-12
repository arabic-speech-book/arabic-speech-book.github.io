from nbbuild import md, code, save, PROVENANCE, PROVENANCE_CODE

cells = [
    md("""## What this notebook does

Two things, and the second explains the first.

1. A rule-based grapheme-to-phoneme converter for diacritized Modern Standard
   Arabic: the sun and moon letters, the emphatic consonants, gemination under
   Shadda, Tanwin, and the long vowels. It is evaluated against a small
   hand-labelled set and scored with phone error rate.
2. A look at what emphasis does to the acoustics, on the minimal pair
   طين ṭīn 'mud' against تين tīn 'figs', which is the second-formant lowering
   described in Section 2.4.

The converter is short enough to read in full. That is the point: for
diacritized MSA, most of the mapping really is rules, and knowing which part is
rules tells you exactly which part is not."""),

    code("""NOTEBOOK = 'ch02_arabic_phonetics_g2p.ipynb'

import numpy as np
import matplotlib.pyplot as plt

SR = 16000
print('ready')"""),

    md("""## 1. The phoneme inventory this notebook assumes

Written in a plain ASCII-safe form so it survives a terminal, with the IPA
beside it. The emphatics carry a trailing `+`. Your inventory may differ, and
that is a legitimate choice: state it, because a phone error rate computed
against a different inventory is a different number."""),

    code("""CONSONANTS = {
    'ء': ('?', 'ʔ'), 'ب': ('b', 'b'), 'ت': ('t', 't'), 'ث': ('th', 'θ'),
    'ج': ('j', 'd͡ʒ'), 'ح': ('H', 'ħ'), 'خ': ('x', 'x'), 'د': ('d', 'd'),
    'ذ': ('dh', 'ð'), 'ر': ('r', 'r'), 'ز': ('z', 'z'), 'س': ('s', 's'),
    'ش': ('sh', 'ʃ'), 'ص': ('s+', 'sˤ'), 'ض': ('d+', 'dˤ'),
    'ط': ('t+', 'tˤ'), 'ظ': ('dh+', 'ðˤ'), 'ع': ('3', 'ʕ'),
    'غ': ('gh', 'ɣ'), 'ف': ('f', 'f'), 'ق': ('q', 'q'), 'ك': ('k', 'k'),
    'ل': ('l', 'l'), 'م': ('m', 'm'), 'ن': ('n', 'n'), 'ه': ('h', 'h'),
    'و': ('w', 'w'), 'ي': ('y', 'j'), 'ة': ('t', 't'), 'ى': ('aa', 'aː'),
}
EMPHATIC = {'s+', 'd+', 't+', 'dh+'}
SUN = set('تثدذرزسشصضطظلن')

FATHA, DAMMA, KASRA = '\\u064E', '\\u064F', '\\u0650'
FATHATAN, DAMMATAN, KASRATAN = '\\u064B', '\\u064C', '\\u064D'
SUKUN, SHADDA = '\\u0652', '\\u0651'
SHORT = {FATHA: 'a', DAMMA: 'u', KASRA: 'i'}
TANWIN = {FATHATAN: ('a', 'n'), DAMMATAN: ('u', 'n'), KASRATAN: ('i', 'n')}

print(f'{len(CONSONANTS)} letters, {len(EMPHATIC)} of them emphatic')"""),

    md("""## 2. The converter

Read it once from the top. Every branch corresponds to a paragraph of
Section 2.3 or 2.6:

- the definite article assimilates to a following sun letter and does not to a moon letter;
- Shadda doubles the consonant it sits on, and a doubled consonant is not the same phoneme twice for a listener, but it is for a phone sequence;
- Fatha followed by alef, Damma followed by waw, and Kasra followed by ya are long vowels, not two segments;
- Tanwin is a short vowel and an /n/ that nobody writes."""),

    code("""ALL_MARKS = set(SHORT) | set(TANWIN) | {SUKUN, SHADDA}


def marks_after(word, i):
    \"\"\"The run of diacritics written on the letter at position i.\"\"\"
    j, marks = i + 1, []
    while j < len(word) and word[j] in ALL_MARKS:
        marks.append(word[j])
        j += 1
    return marks, j


def g2p(word):
    \"\"\"Diacritized MSA in, phoneme list out. Rules only, no lexicon.\"\"\"
    out, i = [], 0
    # the definite article: assimilated before a sun letter, kept before a moon
    if word.startswith('ال') and len(word) > 2:
        out += ['a'] if word[2] in SUN else ['a', 'l']
        i = 2
    while i < len(word):
        ch = word[i]
        marks, nxt = marks_after(word, i)
        if ch == 'ا':                     # alef: lengthens a preceding fatha
            if out and out[-1] == 'a':
                out[-1] = 'aa'
            else:
                out.append('aa')
            i = nxt
            continue
        if ch == 'و' and not marks and out and out[-1] == 'u':
            out[-1] = 'uu'               # damma plus waw is one long vowel
            i = nxt
            continue
        if ch == 'ي' and not marks and out and out[-1] == 'i':
            out[-1] = 'ii'               # kasra plus ya is one long vowel
            i = nxt
            continue
        if ch in CONSONANTS:
            sym = CONSONANTS[ch][0]
            out += [sym, sym] if SHADDA in marks else [sym]
            for m in marks:              # the vowel written on the consonant
                if m in SHORT:
                    out.append(SHORT[m])
                elif m in TANWIN:
                    out += list(TANWIN[m])
            i = nxt
            continue
        i = nxt if nxt > i else i + 1    # anything else is skipped
    return out


for w in ['كِتابٌ', 'الشَّمْسُ', 'القَمَرُ', 'طِينٌ', 'تِينٌ', 'مُدَرِّسٌ']:
    print(f'{w:>10}  ->  {" ".join(g2p(w))}')"""),

    md("""## 3. Scoring it

Phone error rate is Word Error Rate with phonemes as the tokens. Same dynamic
program, different unit. The reference below is hand-labelled: ten words, each
transcribed by hand from the inventory above.

A high phone error rate here does not mean the converter is bad. It means the
converter and the hand transcription disagree, and reading the alignment tells
you which of the two you believe."""),

    code("""def edit_distance(ref, hyp):
    n, m = len(ref), len(hyp)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1,
                          d[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1]))
    return d[n][m]


GOLD = [
    ('كِتابٌ',    ['k', 'i', 't', 'aa', 'b', 'u', 'n']),
    ('الشَّمْسُ',  ['a', 'sh', 'sh', 'a', 'm', 's', 'u']),
    ('القَمَرُ',   ['a', 'l', 'q', 'a', 'm', 'a', 'r', 'u']),
    ('طِينٌ',     ['t+', 'ii', 'n', 'u', 'n']),
    ('تِينٌ',     ['t', 'ii', 'n', 'u', 'n']),
    ('مُدَرِّسٌ',   ['m', 'u', 'd', 'a', 'r', 'r', 'i', 's', 'u', 'n']),
    ('صَبْرٌ',     ['s+', 'a', 'b', 'r', 'u', 'n']),
    ('ضَيْفٌ',     ['d+', 'a', 'y', 'f', 'u', 'n']),
    ('عَيْنٌ',     ['3', 'a', 'y', 'n', 'u', 'n']),
    ('خُبْزٌ',     ['x', 'u', 'b', 'z', 'u', 'n']),
]

errors = total = 0
for word, gold in GOLD:
    got = g2p(word)
    e = edit_distance(gold, got)
    errors += e
    total += len(gold)
    flag = '' if e == 0 else f'   <- {e} error(s)'
    print(f'{word:>10}  gold {" ".join(gold):<28} got {" ".join(got)}{flag}')
print(f'\\nphone error rate: {errors / total:.1%}  ({errors}/{total} phones)')"""),

    md("""## 4. What emphasis does to the vowel

The pair طين /tˤiːn/ and تين /tiːn/ differs in one consonant, and the difference
is audible mostly in the vowel beside it: emphasis lowers the second formant.

With no corpus to hand, the cell below builds both syllables with a source
filter model: a buzz at a fixed pitch, passed through two resonators at the
formant frequencies of the vowel. It is synthetic and it is labelled as such.
It shows the geometry of the effect, not a measurement of a speaker.

**Replace it with real audio as soon as you can.** Two clips of a speaker
saying each word, and the same analysis, is the exercise the chapter sets."""),

    code("""def resonator(signal, freq, bandwidth, sr=SR):
    \"\"\"A single two-pole formant filter, applied sample by sample.\"\"\"
    r = np.exp(-np.pi * bandwidth / sr)
    theta = 2 * np.pi * freq / sr
    a1, a2 = 2 * r * np.cos(theta), -r * r
    out = np.zeros_like(signal)
    for n in range(len(signal)):
        out[n] = signal[n]
        if n >= 1:
            out[n] += a1 * out[n - 1]
        if n >= 2:
            out[n] += a2 * out[n - 2]
    return out / (np.max(np.abs(out)) + 1e-9)


def synth_vowel(f1, f2, f0=120, seconds=0.5, sr=SR):
    n = int(seconds * sr)
    period = int(sr / f0)
    source = np.zeros(n)
    source[::period] = 1.0                      # a buzz: one impulse per period
    y = resonator(source, f1, 80)
    y = resonator(y, f2, 100)
    y = resonator(y, 2800, 150)                 # a fixed third formant
    return y


# /iː/ next to a plain consonant, and next to an emphatic one.
plain = synth_vowel(f1=300, f2=2200)
emphatic = synth_vowel(f1=380, f2=1500)

fig, axes = plt.subplots(1, 2, figsize=(11, 3.6), sharey=True)
for ax, sig, name in ((axes[0], plain, 'تين  tīn, plain /t/'),
                      (axes[1], emphatic, 'طين  ṭīn, emphatic /tˤ/')):
    ax.specgram(sig, NFFT=512, Fs=SR, noverlap=384, cmap='magma')
    ax.set_title(name + '  (synthetic)')
    ax.set_xlabel('time (s)')
    ax.set_ylim(0, 4000)
axes[0].set_ylabel('frequency (Hz)')
plt.tight_layout()
plt.show()

print('second formant, plain    : 2200 Hz')
print('second formant, emphatic : 1500 Hz')
print('difference               :  700 Hz lower beside the emphatic consonant')"""),

    md("""## 5. Where the rules stop

Run the converter on undiacritized text and watch it fail. This is not a bug to
fix. It is the reason Chapter 9 spends a whole section on diacritization: the
information the converter needs is simply not written down.

The same three consonants, written without vowels, are several different words.
No rule recovers which one was meant. A model that has read a great deal of
Arabic can guess, and guessing is what the front end of a synthesizer does."""),

    code("""AMBIGUOUS = 'علم'
for reading, gloss in [('عِلْمٌ', 'knowledge'), ('عَلَمٌ', 'a flag'),
                       ('عَلَّمَ', 'he taught'), ('عُلِمَ', 'it was known')]:
    print(f'{reading:>8}  {gloss:<14} {" ".join(g2p(reading))}')
print(f'\\nundiacritized {AMBIGUOUS}: {" ".join(g2p(AMBIGUOUS))}')
print('one written form, four pronunciations, and nothing in the string to '
      'choose between them.')"""),

    md(PROVENANCE),
    code(PROVENANCE_CODE),
]

save('ch02_arabic_phonetics_g2p.ipynb', cells,
     'Notebook 2.1  From letters to sounds',
     'A rule-based Arabic grapheme-to-phoneme converter, and what emphasis '
     'does to a vowel.')
