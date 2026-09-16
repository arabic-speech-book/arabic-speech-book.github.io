"""A very small notebook builder.

Every notebook in this folder is written as a Python list of cells and saved
through here, so that the twelve share one structure, one kernel spec and one
set of front-matter conventions. Writing them by hand as JSON would be
unreadable and would drift; writing them here means a change to the house style
is one edit.

    from nbbuild import md, code, save
    save('ch03_speech_features.ipynb', [md('# ...'), code('import numpy')])

Nothing here is clever. It exists so the notebooks themselves can be.
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def md(text):
    return {'cell_type': 'markdown', 'metadata': {},
            'source': text.rstrip('\n')}


def code(text):
    return {'cell_type': 'code', 'metadata': {}, 'execution_count': None,
            'outputs': [], 'source': text.rstrip('\n')}


HEADER = """*Companion notebook to* **Introduction to Arabic Speech Technology** *by Hend S. Al-Khalifa.*

**How to run.** Open this notebook in Google Colab or run it locally with the
pinned environment in `requirements.txt`. Every notebook in this series runs end
to end with **no downloads and no accounts**: where a real corpus or a
pretrained model is unavailable, a clearly marked fallback stands in for it, and
the notebook says which path it took. Cells that need a download are marked
`OPTIONAL` and are safe to skip.

**On data.** Where you substitute a real corpus, record its release version and
its licence in the provenance cell at the end. A result without them is not
reproducible, which is the habit this book asks for in every chapter."""


def save(name, cells, title, subtitle):
    front = [md(f'# {title}\n\n*{subtitle}*\n\n---\n\n{HEADER}')]
    nb = {
        'cells': front + cells,
        'metadata': {
            'kernelspec': {'display_name': 'Python 3', 'language': 'python',
                           'name': 'python3'},
            'language_info': {'name': 'python', 'version': '3.11'},
            'colab': {'provenance': []},
        },
        'nbformat': 4,
        'nbformat_minor': 5,
    }
    for i, c in enumerate(nb['cells']):
        c['id'] = f'cell-{i:02d}'
    path = os.path.join(OUT, name)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(nb, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print(f'  wrote {name}  ({len(nb["cells"])} cells)')
    return path


PROVENANCE = """## Provenance

Fill this in before you quote any number from this notebook. It is the same
information the chapter's Reproducibility Note asks for, and it is the
difference between a result and a screenshot."""

PROVENANCE_CODE = """PROVENANCE = {
    'notebook': NOTEBOOK,
    'ran_on': 'fill in the date you ran it',
    'data': 'corpus name and release version, or "synthetic fallback"',
    'licence': 'the licence of the data you used',
    'model': 'model name and revision, or "none"',
    'normalization': 'the normalization applied before scoring',
    'hardware': 'CPU or the GPU model',
}
for k, v in PROVENANCE.items():
    print(f'{k:>15}: {v}')"""
