from nbbuild import md, code, save, PROVENANCE, PROVENANCE_CODE

cells = [
    md("""## What this notebook does

Two corpora, one schema, and the audit that should happen before any of it is
trained on.

1. Load two differently shaped corpora into a common manifest: audio path, transcript, speaker, dialect, gender, duration.
2. Report the statistics that actually drive a corpus choice: total hours, speakers, hours per dialect, hours per gender, and how much of the whole a single speaker accounts for.
3. Find the speaker overlap that would quietly invalidate a split.
4. Compute Fleiss' kappa on a small multi-annotator sample, because an annotation guideline is only as good as the agreement it produces.

It runs on the provided samples with no downloads. Point it at your own
manifests and everything below works unchanged."""),

    code("""NOTEBOOK = 'ch07_corpus_loader.ipynb'

from collections import Counter, defaultdict

import numpy as np

SCHEMA = ['audio', 'transcript', 'speaker', 'dialect', 'gender', 'seconds',
          'corpus']
print('common schema:', ', '.join(SCHEMA))"""),

    md("""## 1. Two corpora, one manifest

Corpora arrive in whatever shape their builders chose: one has a TSV with a
client id and a sentence, another has a JSON with a segment id and a speaker
label, a third has directory names carrying the dialect. The loader's whole job
is to stop that variety from spreading into your code.

Write one adapter per corpus, return the same dictionary, and never let a
corpus-specific field escape the adapter. When the third corpus arrives you
will write a third adapter and change nothing else."""),

    code("""# Corpus A: a crowd-sourced read-speech corpus, TSV-shaped
CORPUS_A = [
    # client_id, path, sentence, gender, accent, duration_ms
    ('c001', 'a/001.mp3', 'ذهب الطالب الى المكتبة', 'male', 'msa', 4200),
    ('c001', 'a/002.mp3', 'الكتاب على الطاولة', 'male', 'msa', 3100),
    ('c002', 'a/003.mp3', 'المدرسة قريبة من البيت', 'female', 'msa', 3800),
    ('c003', 'a/004.mp3', 'وين اقرب محطة بنزين', 'male', 'gulf', 2900),
    ('c004', 'a/005.mp3', 'عايز اروح المطار', 'female', 'egyptian', 2600),
]

# Corpus B: a broadcast corpus, JSON-shaped, with different field names
CORPUS_B = [
    {'seg': 'b-0001', 'wav': 'b/show1.wav', 'text': 'اهلا بكم في نشرة الاخبار',
     'spk': 'SPK_07', 'dialect': 'MSA', 'sex': 'F', 'dur': 5.5},
    {'seg': 'b-0002', 'wav': 'b/show1.wav', 'text': 'نبدأ من العاصمة',
     'spk': 'SPK_07', 'dialect': 'MSA', 'sex': 'F', 'dur': 3.2},
    {'seg': 'b-0003', 'wav': 'b/show2.wav', 'text': 'شنو صار في السوق',
     'spk': 'c003', 'dialect': 'Gulf', 'sex': 'M', 'dur': 4.1},
    {'seg': 'b-0004', 'wav': 'b/show2.wav', 'text': 'بغيت نمشي للدار',
     'spk': 'SPK_09', 'dialect': 'Maghrebi', 'sex': 'M', 'dur': 3.9},
]

GENDER = {'male': 'M', 'female': 'F', 'M': 'M', 'F': 'F'}
DIALECT = {'msa': 'MSA', 'MSA': 'MSA', 'gulf': 'Gulf', 'Gulf': 'Gulf',
           'egyptian': 'Egyptian', 'Maghrebi': 'Maghrebi'}


def load_corpus_a(rows):
    return [{'audio': path, 'transcript': text, 'speaker': f'A:{client}',
             'dialect': DIALECT.get(accent, 'unknown'),
             'gender': GENDER.get(gender, 'unknown'),
             'seconds': ms / 1000.0, 'corpus': 'A'}
            for client, path, text, gender, accent, ms in rows]


def load_corpus_b(rows):
    return [{'audio': r['wav'], 'transcript': r['text'],
             'speaker': f'B:{r["spk"]}',
             'dialect': DIALECT.get(r['dialect'], 'unknown'),
             'gender': GENDER.get(r['sex'], 'unknown'),
             'seconds': float(r['dur']), 'corpus': 'B'}
            for r in rows]


manifest = load_corpus_a(CORPUS_A) + load_corpus_b(CORPUS_B)
print(f'{len(manifest)} utterances in one schema\\n')
for row in manifest[:3]:
    print('  ', row)"""),

    md("""## 2. The audit

Four questions, and a corpus that cannot answer them is not ready to be trained
on:

- how many hours, and how many speakers;
- how are the hours distributed across dialects, and across genders;
- how much of the corpus is one speaker, because a corpus dominated by three voices will teach a model those three voices;
- and is any dialect represented by a single speaker, which makes a per-dialect number a per-speaker number wearing a disguise."""),

    code("""def audit(rows):
    total = sum(r['seconds'] for r in rows)
    speakers = {r['speaker'] for r in rows}
    print(f'total: {total / 3600:.3f} hours across {len(rows)} utterances, '
          f'{len(speakers)} speakers\\n')

    for field in ('dialect', 'gender', 'corpus'):
        by = defaultdict(float)
        spk = defaultdict(set)
        for r in rows:
            by[r[field]] += r['seconds']
            spk[r[field]].add(r['speaker'])
        print(f'  by {field}:')
        for key in sorted(by, key=by.get, reverse=True):
            share = by[key] / total
            warn = '   <- one speaker only' if len(spk[key]) == 1 else ''
            print(f'    {key:<12} {by[key] / 60:6.2f} min  {share:6.1%}  '
                  f'{len(spk[key])} speaker(s){warn}')
        print()

    per_speaker = defaultdict(float)
    for r in rows:
        per_speaker[r['speaker']] += r['seconds']
    top = max(per_speaker, key=per_speaker.get)
    print(f'  largest single speaker: {top} with '
          f'{per_speaker[top] / total:.1%} of the audio')


audit(manifest)"""),

    md("""## 3. The overlap that breaks a split

The rule is one line: no speaker on both sides of a boundary. Two corpora
merged together break it in a way neither breaks alone, because the same person
can appear in both under different identifiers, and nothing in either manifest
says so.

The check below is what you run before you trust any evaluation number. Notice
that it catches a real case in the sample: one speaker id appears in both
corpora."""),

    code("""def overlapping_speakers(rows):
    # the same underlying person may carry different ids: compare the raw id
    raw = defaultdict(set)
    for r in rows:
        corpus, ident = r['speaker'].split(':', 1)
        raw[ident].add(corpus)
    return {ident: sorted(cs) for ident, cs in raw.items() if len(cs) > 1}


shared = overlapping_speakers(manifest)
if shared:
    for ident, corpora in shared.items():
        print(f'  speaker {ident!r} appears in corpora {corpora}')
    print('\\nIf one of those corpora becomes your training set and the other '
          'your test set, the test measures memory of a voice.')
else:
    print('  no shared speaker identifiers')


def person(row):
    # the identity that matters for a split is the person, not the row's
    # corpus-prefixed label: a speaker in two corpora is still one speaker
    return row['speaker'].split(':', 1)[1]


def split_by_speaker(rows, dev=0.2, test=0.2, seed=0):
    speakers = sorted({person(r) for r in rows})
    rng = np.random.default_rng(seed)
    rng.shuffle(speakers)
    n_test = max(1, int(len(speakers) * test))
    n_dev = max(1, int(len(speakers) * dev))
    assign = {}
    for i, s in enumerate(speakers):
        assign[s] = 'test' if i < n_test else \\
                    'dev' if i < n_test + n_dev else 'train'
    out = defaultdict(list)
    for r in rows:
        out[assign[person(r)]].append(r)
    return out


split = split_by_speaker(manifest)
for name in ('train', 'dev', 'test'):
    rows = split[name]
    print(f'\\n{name:>6}: {len(rows)} utterances, '
          f'{sum(r["seconds"] for r in rows) / 60:.1f} min, '
          f'dialects {sorted({r["dialect"] for r in rows})}')
leak = ({person(r) for r in split['train']} &
        ({person(r) for r in split['dev']} | {person(r) for r in split['test']}))
print(f'\\nspeakers on both sides: {len(leak)}')
print('Zero because the split keys on the person rather than on the label. '
      'Key it on the label instead and the shared speaker above lands on both '
      'sides, and nothing in the output would have told you.')"""),

    md("""## 4. Fleiss' kappa

An annotation guideline is a hypothesis: that two people reading it will make
the same decision. Kappa tests that hypothesis, correcting for the agreement
you would expect by chance alone.

Read it as the chapter does. High kappa on an easy label is not evidence the
guideline is good; low kappa on a hard label often means the guideline has not
decided something, and the fix is a better guideline rather than a stricter
annotator."""),

    code("""def fleiss_kappa(table):
    # table[i][j] = how many annotators put item i in category j
    table = np.asarray(table, dtype=float)
    n_items, n_cat = table.shape
    n_annotators = table.sum(axis=1)[0]
    p_i = ((table ** 2).sum(axis=1) - n_annotators) / \\
          (n_annotators * (n_annotators - 1))
    p_bar = p_i.mean()
    p_j = table.sum(axis=0) / (n_items * n_annotators)
    p_e = (p_j ** 2).sum()
    return (p_bar - p_e) / (1 - p_e), p_bar, p_e


# five clips, three annotators, labelling the dialect: MSA, Gulf, Egyptian
LABELS = ['MSA', 'Gulf', 'Egyptian']
EASY = [[3, 0, 0], [0, 3, 0], [0, 0, 3], [3, 0, 0], [0, 3, 0]]
HARD = [[2, 1, 0], [1, 2, 0], [0, 2, 1], [2, 0, 1], [1, 1, 1]]

for name, table in (('clear cases', EASY), ('the continuum', HARD)):
    k, observed, chance = fleiss_kappa(table)
    print(f'{name:<16} kappa {k:6.3f}   observed {observed:.3f}   '
          f'chance {chance:.3f}')

print('\\nThe second table is what the dialect continuum looks like in an '
      'annotation round: neighbouring varieties, three annotators, no '
      'agreement. Before blaming the annotators, ask what the guideline says '
      'to do with a speaker who is between two varieties. If it says nothing, '
      'that is the finding.')"""),

    md("""## 5. The data card

Everything above, in the form the chapter asks a corpus to publish. Fill it in
for whatever you build, and publish it beside the audio."""),

    code("""CARD = {
    'name': 'fill in',
    'version': 'fill in, and change it when the data changes',
    'hours': f'{sum(r["seconds"] for r in manifest) / 3600:.3f}',
    'speakers': len({r['speaker'] for r in manifest}),
    'dialects and hours': 'from the audit above',
    'gender balance': 'from the audit above',
    'collection': 'read, spontaneous, broadcast, telephone',
    'consent': 'what the speakers were told and agreed to',
    'licence': 'the exact licence, and what it forbids',
    'splits': 'speaker-disjoint, and the seed used',
    'known gaps': 'the varieties and conditions it does not cover',
}
for k, v in CARD.items():
    print(f'{k:>20}: {v}')"""),

    md(PROVENANCE),
    code(PROVENANCE_CODE),
]

save('ch07_corpus_loader.ipynb', cells,
     'Notebook 7.1  A unified loader and a data audit',
     'Two corpora into one schema, the statistics that decide a choice, and '
     'the checks that protect an evaluation.')
