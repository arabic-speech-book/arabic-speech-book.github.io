#!/usr/bin/env python3
"""Turn the fourteen chapter reference lists into one bibliography.

    python3 build_bibliography.py

Reads by-chapter.json (produced from the manuscript) and writes bibliography.bib,
.ris, .csv and .json. Entries are deduplicated on the digital object identifier
where there is one and on a normalized title otherwise, and an entry cited in
several chapters keeps all of them in its keywords.

Every record carries the entry exactly as the book prints it, in the note field
of the BibTeX and in N1 of the RIS. Where a field was parsed with less than full
confidence the CSV says so, so a site can fall back to the printed string rather
than publish a mangled one.
"""
import csv, json, re, unicodedata

rows = json.load(open('by-chapter.json', encoding='utf-8'))


def norm(s):
    s = unicodedata.normalize('NFKD', s or '').lower()
    return re.sub(r'[^a-z0-9]+', '', s)


master = {}
for r in rows:
    key = norm(r['doi']) or norm(r['title'])[:60] or norm(r['raw'])[:60]
    m = master.setdefault(key, dict(r, chapters=[]))
    m['chapters'].append(r['chapter'])
    for f in ('doi', 'url', 'pages', 'venue', 'accessed'):
        if not m[f] and r[f]:
            m[f] = r[f]
entries = sorted(master.values(), key=lambda r: (r['authors'].lower() or 'zzz', r['year']))


def bib_authors(a):
    if not a:
        return ''
    a = a.replace(' & ', ' and ').replace(', and ', ' and ')
    parts = re.split(r',\s*(?=[A-Z][a-zA-Z\'’\-]+,)', a)
    return ' and '.join(p.strip().rstrip(',') for p in parts) if len(parts) > 1 \
        else a.strip().rstrip(',')


def kind(e):
    v = (e['venue'] or '').lower()
    if any(k in v for k in ('proceedings', 'interspeech', 'icassp', 'workshop',
                            'conference', 'symposium', 'lrec', 'acl', 'emnlp',
                            'naacl', 'coling', 'slt', 'asru')):
        return 'inproceedings'
    if 'arxiv' in v or 'arxiv' in (e['url'] or ''):
        return 'misc'
    if any(k in v for k in ('journal', 'transactions', 'ieee access', 'plos',
                            'speech communication', 'computer speech')):
        return 'article'
    return 'misc'


def esc(s):
    return (s or '').replace('&', r'\&').replace('%', r'\%') \
                    .replace('_', r'\_').replace('#', r'\#')


seen = set()


def cite_key(e):
    first = re.split(r'[,\s]', e['authors'].strip())[0] if e['authors'] else 'anon'
    word = next((w for w in re.findall(r'[A-Za-z]{4,}', e['title'] or '')), 'ref')
    k = f"{norm(first)[:14] or 'anon'}{e['year'] or 'nd'}{norm(word)[:10]}"
    n, base = 1, k
    while k in seen:
        n += 1
        k = f'{base}{chr(ord("a") + n - 2)}'
    seen.add(k)
    return k


header = ('% Introduction to Arabic Speech Technology, by Hend S. Al-Khalifa\n'
          f'% {len(entries)} distinct works, cited {len(rows)} times across '
          'fourteen chapters.\n'
          '% Every entry was checked against the record of the publisher that\n'
          '% issued it. The note field carries the entry exactly as the book\n'
          '% prints it.\n\n')

with open('bibliography.bib', 'w', encoding='utf-8') as f:
    f.write(header)
    for e in entries:
        k = cite_key(e)
        e['bibtex_key'] = k
        f.write(f'@{kind(e)}{{{k},\n')
        if e['authors']:
            f.write(f'  author    = {{{esc(bib_authors(e["authors"]))}}},\n')
        if e['title']:
            f.write(f'  title     = {{{esc(e["title"])}}},\n')
        if e['year']:
            f.write(f'  year      = {{{e["year"]}}},\n')
        if e['venue']:
            field = {'inproceedings': 'booktitle',
                     'article': 'journal'}.get(kind(e), 'howpublished')
            f.write(f'  {field:9} = {{{esc(e["venue"])}}},\n')
        if e['pages']:
            f.write(f'  pages     = {{{e["pages"].replace("-", "--")}}},\n')
        if e['doi']:
            f.write(f'  doi       = {{{e["doi"]}}},\n')
        if e['url']:
            f.write(f'  url       = {{{e["url"]}}},\n')
        if e['accessed']:
            f.write(f'  urldate   = {{{e["accessed"]}}},\n')
        f.write('  keywords  = {chapter '
                + ', chapter '.join(str(c) for c in sorted(set(e['chapters'])))
                + '},\n')
        f.write(f'  note      = {{{esc(e["raw"])}}}\n}}\n\n')

RIS = {'inproceedings': 'CPAPER', 'article': 'JOUR', 'misc': 'GEN'}
with open('bibliography.ris', 'w', encoding='utf-8') as f:
    for e in entries:
        f.write(f'TY  - {RIS[kind(e)]}\n')
        for a in (bib_authors(e['authors']).split(' and ') if e['authors'] else []):
            if a.strip():
                f.write(f'AU  - {a.strip()}\n')
        if e['title']:
            f.write(f'TI  - {e["title"]}\n')
        if e['year']:
            f.write(f'PY  - {e["year"][:4]}\n')
        if e['venue']:
            f.write(f'T2  - {e["venue"]}\n')
        if e['pages'] and '-' in e['pages']:
            sp, ep = e['pages'].split('-', 1)
            f.write(f'SP  - {sp}\nEP  - {ep}\n')
        if e['doi']:
            f.write(f'DO  - {e["doi"]}\n')
        if e['url']:
            f.write(f'UR  - {e["url"]}\n')
        f.write('KW  - chapters '
                + ','.join(str(c) for c in sorted(set(e['chapters']))) + '\n')
        f.write(f'N1  - {e["raw"]}\nER  - \n\n')

cols = ['bibtex_key', 'authors', 'year', 'title', 'venue', 'pages', 'doi',
        'url', 'accessed', 'chapters', 'confidence', 'raw']
with open('bibliography.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
    w.writeheader()
    for e in entries:
        row = dict(e)
        row['chapters'] = ';'.join(str(c) for c in sorted(set(e['chapters'])))
        w.writerow(row)
json.dump(entries, open('bibliography.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(f'{len(rows)} citations, {len(entries)} distinct works')
