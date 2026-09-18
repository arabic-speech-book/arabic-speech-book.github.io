# Introduction to Arabic Speech Technologies — Companion Website

Source for the bilingual (English / العربية) companion site at
**https://arabic-speech-book.github.io/**.

Built with [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/),
with notebook rendering ([mkdocs-jupyter](https://github.com/danielfrg/mkdocs-jupyter))
and bilingual support ([mkdocs-static-i18n](https://github.com/ultrabug/mkdocs-static-i18n)).

## What's here

- **Notebooks** — one runnable Jupyter notebook per chapter (`docs/notebooks/`).
- **Datasets** — a curated Arabic speech-corpora database (`docs/datasets.md`).
- **Tools** — open-source models, toolkits, libraries (`docs/tools.md`).
- **Resources** — books, surveys, and an auto-generated literature table (`docs/resources/`).

## Local development

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
mkdocs serve                    # live preview at http://127.0.0.1:8000
```

## Editing content

- Each page exists in two files: `page.md` (English) and `page.ar.md` (Arabic).
- Add a new page by creating both files and adding it to the `nav:` in `mkdocs.yml`
  (and a translation under `nav_translations` for the Arabic label).
- The **Literature** page is generated — edit `data/paper-table.csv`, then run:

  ```bash
  python scripts/build_literature.py
  ```

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds the site and
publishes it to GitHub Pages. In the repository settings, set **Pages → Build and
deployment → Source = GitHub Actions** (one-time).

## License

Content © 2026 Hend S. Al-Khalifa. Except where noted, this site's content is
licensed **[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)**
(share and adapt for non-commercial use, with attribution). Notebook code may
also be reused for teaching and research with attribution. See [`LICENSE`](LICENSE).
