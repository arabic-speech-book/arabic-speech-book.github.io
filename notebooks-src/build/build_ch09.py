from nbbuild import md, code, save, PROVENANCE, PROVENANCE_CODE

cells = [
    md("""## What this notebook does

The Arabic front end of a text-to-speech system, which is the half that decides
quality, and then the objective check that closes the loop.

1. Normalize a sentence: numbers into words, symbols spoken, punctuation into pauses.
2. Restore the diacritics, which is the step English does not have and Arabic cannot do without.
3. Convert to phonemes, and see how a different diacritization gives a different pronunciation of the same letters.
4. OPTIONAL: synthesize the sentence and run the result through a recognizer, then score the recognizer's transcript against the text you started from. That round trip is the intelligibility check of Section 9.8.

Everything up to the round trip runs with no downloads."""),

    code("""NOTEBOOK = 'ch09_arabic_tts.ipynb'

import re
import unicodedata

FATHA, DAMMA, KASRA = '\\u064E', '\\u064F', '\\u0650'
SUKUN, SHADDA = '\\u0652', '\\u0651'
TANWIN = {'\\u064B': ('a', 'n'), '\\u064C': ('u', 'n'), '\\u064D': ('i', 'n')}
SHORT = {FATHA: 'a', DAMMA: 'u', KASRA: 'i'}
MARKS = set(SHORT) | set(TANWIN) | {SUKUN, SHADDA}
print('ready')"""),

    md("""## 1. Text normalization

A synthesizer cannot say `2026` or `%`. Something has to decide what those
become, in which dialect, and with which agreement.

Arabic makes this harder than English in one specific way: the number word
agrees with the counted noun in gender, and the noun's case changes with the
number. A full solution needs the noun. The version below handles the cases
that occur constantly and prints what it could not resolve, which is the
honest behaviour for a front end: fail loudly rather than mispronounce."""),

    code("""ONES = ['صفر', 'واحد', 'اثنان', 'ثلاثة', 'أربعة', 'خمسة', 'ستة',
        'سبعة', 'ثمانية', 'تسعة']
TENS = {2: 'عشرون', 3: 'ثلاثون', 4: 'أربعون', 5: 'خمسون', 6: 'ستون',
        7: 'سبعون', 8: 'ثمانون', 9: 'تسعون'}
TEENS = {10: 'عشرة', 11: 'أحد عشر', 12: 'اثنا عشر', 13: 'ثلاثة عشر',
         14: 'أربعة عشر', 15: 'خمسة عشر', 16: 'ستة عشر', 17: 'سبعة عشر',
         18: 'ثمانية عشر', 19: 'تسعة عشر'}


def number_to_words(n):
    n = int(n)
    if n < 10:
        return ONES[n]
    if n < 20:
        return TEENS[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return TENS[tens] if not ones else f'{ONES[ones]} و{TENS[tens]}'
    if n < 1000:
        hundreds, rest = divmod(n, 100)
        head = 'مائة' if hundreds == 1 else f'{ONES[hundreds]}مائة'
        return head if not rest else f'{head} و{number_to_words(rest)}'
    thousands, rest = divmod(n, 1000)
    head = 'ألف' if thousands == 1 else f'{number_to_words(thousands)} آلاف'
    return head if not rest else f'{head} و{number_to_words(rest)}'


SYMBOLS = {'%': 'بالمائة', '&': 'و', '+': 'زائد', '=': 'يساوي'}


def normalize_text(text):
    notes = []
    for symbol, word in SYMBOLS.items():
        if symbol in text:
            text = text.replace(symbol, f' {word} ')
    def swap(match):
        value = match.group(0)
        if len(value) > 6:
            notes.append(f'{value}: too long to speak as a single number, '
                         f'read it digit by digit or supply a rule')
            return ' '.join(number_to_words(d) for d in value)
        return number_to_words(value)
    text = re.sub(r'\\d+', swap, text)
    text = re.sub(r'[.!?]', ' ، ', text)
    return ' '.join(text.split()), notes


for raw in ['وصل 15 طالبا الى المدرسة',
            'ارتفعت النسبة 25% هذا العام',
            'رقم الحساب 4820391']:
    out, notes = normalize_text(raw)
    print(f'  {raw}\\n  -> {out}')
    for n in notes:
        print(f'     note: {n}')
    print()"""),

    md("""## 2. Diacritization, and why it decides everything

Arabic is written without the short vowels. A synthesizer has to put them back
before it can pronounce anything, and the same consonant skeleton often admits
several readings that are all real words.

There is no rule that recovers them. A model trained on diacritized text
guesses, and its guess is the pronunciation your listener hears. The cell below
shows what is at stake: one skeleton, four readings, four different phoneme
sequences, four different meanings."""),

    code("""def marks_after(word, i):
    j, marks = i + 1, []
    while j < len(word) and word[j] in MARKS:
        marks.append(word[j])
        j += 1
    return marks, j


CONSONANTS = {
    'ء': '?', 'ب': 'b', 'ت': 't', 'ث': 'th', 'ج': 'j', 'ح': 'H', 'خ': 'x',
    'د': 'd', 'ذ': 'dh', 'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'sh', 'ص': 's+',
    'ض': 'd+', 'ط': 't+', 'ظ': 'dh+', 'ع': '3', 'غ': 'gh', 'ف': 'f',
    'ق': 'q', 'ك': 'k', 'ل': 'l', 'م': 'm', 'ن': 'n', 'ه': 'h', 'و': 'w',
    'ي': 'y', 'ة': 't', 'ى': 'aa',
}
SUN = set('تثدذرزسشصضطظلن')


def g2p(word):
    out, i = [], 0
    if word.startswith('ال') and len(word) > 2:
        out += ['a'] if word[2] in SUN else ['a', 'l']
        i = 2
    while i < len(word):
        ch = word[i]
        marks, nxt = marks_after(word, i)
        if ch == 'ا':
            if out and out[-1] == 'a':
                out[-1] = 'aa'
            else:
                out.append('aa')
        elif ch == 'و' and not marks and out and out[-1] == 'u':
            out[-1] = 'uu'
        elif ch == 'ي' and not marks and out and out[-1] == 'i':
            out[-1] = 'ii'
        elif ch in CONSONANTS:
            sym = CONSONANTS[ch]
            out += [sym, sym] if SHADDA in marks else [sym]
            for m in marks:
                if m in SHORT:
                    out.append(SHORT[m])
                elif m in TANWIN:
                    out += list(TANWIN[m])
        i = nxt if nxt > i else i + 1
    return out


SKELETON = 'كتب'
READINGS = [('كَتَبَ', 'he wrote'), ('كُتُبٌ', 'books'),
            ('كُتِبَ', 'it was written'), ('كَتَّبَ', 'he made someone write')]
print(f'skeleton: {SKELETON}\\n')
for form, gloss in READINGS:
    print(f'  {form:>8}  {gloss:<24} /{" ".join(g2p(form))}/')
print(f'\\n  undiacritized {SKELETON} gives /{" ".join(g2p(SKELETON))}/, which '
      f'is not a pronunciation at all.')
print('\\nA diacritizer picks one of those four. If it picks wrong, the voice '
      'is fluent, confident and saying a different word, which is the failure '
      'mode a listening test is least likely to catch and a comprehension '
      'test is most likely to.')"""),

    md("""## 3. The whole front end on one sentence

Normalize, diacritize, convert. In a real system the middle step is a model;
here it is a small lexicon, so the notebook runs offline and so you can see
exactly where the guessing happens."""),

    code("""LEXICON = {
    'وصل': 'وَصَلَ', 'خمسة': 'خَمْسَةُ', 'عشر': 'عَشَرَ', 'طالبا': 'طالِباً',
    'الى': 'إلى', 'المدرسة': 'المَدْرَسَةِ', 'صباحا': 'صَباحاً',
}


def diacritize(text):
    out, unknown = [], []
    for word in text.split():
        if word in LEXICON:
            out.append(LEXICON[word])
        else:
            out.append(word)
            if any('\\u0621' <= c <= '\\u064A' for c in word):
                unknown.append(word)
    return ' '.join(out), unknown


RAW = 'وصل 15 طالبا الى المدرسة صباحا'
normalized, notes = normalize_text(RAW)
diacritized, unknown = diacritize(normalized)
phones = [p for w in diacritized.split() for p in g2p(w)]

print(f'raw         : {RAW}')
print(f'normalized  : {normalized}')
print(f'diacritized : {diacritized}')
print(f'phonemes    : /{" ".join(phones)}/')
if unknown:
    print(f'\\nnot in the lexicon, so left undiacritized and therefore '
          f'unpronounceable: {unknown}')
    print('In a real front end these are exactly the words the diacritizer '
          'has to guess, and exactly the words to inspect when the voice '
          'says something odd.')"""),

    md("""## 4. OPTIONAL: the round trip

Synthesize the sentence, recognize the audio, and score the transcript against
the text you started from. It is not a substitute for a listening test, and
Section 9.8 is explicit about that: a recognizer is not a listener, and a
system can be intelligible to one and not the other.

What it is good for is catching the catastrophic case cheaply and repeatably. A
synthesizer that has mispronounced a word because the diacritizer guessed wrong
will produce a transcript that differs from the input in exactly that word, and
you can run the check on a thousand sentences overnight."""),

    code("""RUN_ROUND_TRIP = False

if RUN_ROUND_TRIP:
    from transformers import pipeline, VitsModel, AutoTokenizer
    import torch
    import soundfile as sf

    tts_name = 'facebook/mms-tts-ara'
    tok = AutoTokenizer.from_pretrained(tts_name)
    tts = VitsModel.from_pretrained(tts_name)
    inputs = tok(diacritized, return_tensors='pt')
    with torch.no_grad():
        wav = tts(**inputs).waveform.squeeze().numpy()
    sf.write('/tmp/tts.wav', wav, tts.config.sampling_rate)

    asr = pipeline('automatic-speech-recognition', model='openai/whisper-small',
                   generate_kwargs={'language': 'arabic'})
    heard = asr('/tmp/tts.wav')['text']
    print('said :', normalized)
    print('heard:', heard)
else:
    print('skipped: needs a synthesizer and a recognizer')


def wer(reference, hypothesis):
    ref, hyp = reference.split(), hypothesis.split()
    d = [[0] * (len(hyp) + 1) for _ in range(len(ref) + 1)]
    for i in range(len(ref) + 1):
        d[i][0] = i
    for j in range(len(hyp) + 1):
        d[0][j] = j
    for i in range(1, len(ref) + 1):
        for j in range(1, len(hyp) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1,
                          d[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1]))
    return d[-1][-1] / max(1, len(ref))


print('\\nround-trip WER is computed with wer(normalized, heard). Report it '
      'as an intelligibility cross-check, never as a quality score, and '
      'always beside a listening test with its scale, its listeners and '
      'their dialects.')"""),

    md("""## 5. What a synthesis result has to carry

The chapter asks three questions of every corpus a voice was built on, and they
are worth writing down before the voice is released rather than after."""),

    code("""VOICE_CARD = {
    'who was recorded': 'how many speakers, which variety, and with what consent',
    'diacritization quality': 'automatic or hand-checked, and the error rate if known',
    'licence': 'what the licence permits, including commercial use and voice cloning',
    'front end': 'normalizer, diacritizer and G2P, each with its version',
    'listening test': 'scale, number of listeners, and their dialects',
    'objective check': 'the recognizer used for the round trip, and its revision',
    'per-dialect results': 'never one mean opinion score for all of Arabic',
}
for k, v in VOICE_CARD.items():
    print(f'{k:>24}: {v}')"""),

    md(PROVENANCE),
    code(PROVENANCE_CODE),
]

save('ch09_arabic_tts.ipynb', cells,
     'Notebook 9.1  An Arabic text-to-speech front end',
     'Normalization, diacritization, grapheme-to-phoneme, and the round-trip '
     'intelligibility check.')
