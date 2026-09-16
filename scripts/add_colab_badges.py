#!/usr/bin/env python3
"""Insert an "Open in Colab" badge near the top of every notebook.

Idempotent: re-running updates the badge in place rather than duplicating it.
Run after refreshing the notebooks from the author's export:

    python scripts/add_colab_badges.py

Note: Colab can only open notebooks from a PUBLIC GitHub repo, so these badges
start working once the repository is made public (see docs/notebooks/index.md).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
# Every folder under docs/ whose notebooks should carry a badge.
NB_DIRS = [DOCS / "notebooks", DOCS / "solutions"]
OWNER_REPO = "arabic-speech-book/arabic-speech-book.github.io"
BRANCH = "main"
MARKER = "colab.research.google.com/github"


def badge_cell(rel_path: str) -> dict:
    url = (f"https://colab.research.google.com/github/{OWNER_REPO}/blob/"
           f"{BRANCH}/docs/{rel_path}")
    src = (f'<a href="{url}" target="_blank" rel="noopener">'
           f'<img src="https://colab.research.google.com/assets/colab-badge.svg" '
           f'alt="Open In Colab"></a>')
    return {"cell_type": "markdown", "metadata": {"tags": ["colab-badge"]},
            "source": [src]}


def main():
    changed = 0
    nb_paths = [p for d in NB_DIRS if d.is_dir() for p in sorted(d.glob("*.ipynb"))]
    for nb_path in nb_paths:
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        cells = nb.get("cells", [])
        cell = badge_cell(nb_path.relative_to(DOCS).as_posix())
        # replace an existing badge cell if present, else insert after the title
        idx = next((i for i, c in enumerate(cells)
                    if MARKER in "".join(c.get("source", []))), None)
        if idx is not None:
            cells[idx] = cell
        else:
            cells.insert(1 if cells else 0, cell)
        nb["cells"] = cells
        nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1),
                           encoding="utf-8")
        changed += 1
    print(f"Badged {changed} notebooks.")


if __name__ == "__main__":
    main()
