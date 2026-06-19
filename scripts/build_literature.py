#!/usr/bin/env python3
"""Generate docs/resources/literature.md (+ .ar.md) from data/paper-table.csv.

Run after updating the CSV:

    python scripts/build_literature.py

This keeps the Literature page in sync with the book's reference database.
"""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "paper-table.csv"
OUT_EN = ROOT / "docs" / "resources" / "literature.md"
OUT_AR = ROOT / "docs" / "resources" / "literature.ar.md"


def clean(text: str) -> str:
    """Collapse whitespace and escape pipes so cells don't break the table."""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text).strip()
    return text.replace("|", "\\|")


def best_link(row: dict) -> str:
    for key in ("Paper Link", "PDF Link"):
        url = (row.get(key) or "").strip()
        if url.startswith("http"):
            return url
    doi = (row.get("DOI") or "").strip()
    if doi:
        return f"https://doi.org/{doi}"
    return ""


def title_cell(row: dict) -> str:
    title = clean(row.get("Paper Title") or "Untitled")
    link = best_link(row)
    return f"[{title}]({link})" if link else title


def authors_cell(row: dict) -> str:
    authors = clean(row.get("Author Names") or "")
    names = [a.strip() for a in re.split(r"[\n;]", authors) if a.strip()]
    if not names:
        return "—"
    if len(names) > 2:
        return f"{names[0]} et al."
    return ", ".join(names)


def load_rows():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    # Newest first, then by title
    rows.sort(key=lambda r: ((r.get("Publication Year") or "0"), r.get("Paper Title") or ""),
              reverse=True)
    return rows


def write_page(path: Path, rows, lang: str):
    if lang == "ar":
        header = (
            "# المراجع\n\n"
            "جدول قابل للبحث بأوراق معالجة الكلام العربي، مولَّد من قاعدة مراجع الكتاب. "
            "استخدم مربّع البحث أعلى الصفحة للتصفية حسب العنوان أو المؤلّف أو السنة.\n\n"
            f"**عدد المداخل:** {len(rows)}\n\n"
            "| العنوان | المؤلّفون | السنة | النوع |\n"
            "|---------|-----------|-------|------|\n"
        )
        note = ("\n\n!!! note \"تحديث\"\n"
                "    هذه الصفحة مولَّدة آليًّا. لتحديثها، عدّل `data/paper-table.csv` "
                "ثم شغّل `python scripts/build_literature.py`.\n")
    else:
        header = (
            "# Literature\n\n"
            "A searchable table of papers on Arabic speech processing, generated from the "
            "book's reference database. Use the search box at the top of the page to filter "
            "by title, author, or year.\n\n"
            f"**Entries:** {len(rows)}\n\n"
            "| Title | Authors | Year | Type |\n"
            "|-------|---------|------|------|\n"
        )
        note = ("\n\n!!! note \"Updating\"\n"
                "    This page is auto-generated. To update it, edit `data/paper-table.csv` "
                "then run `python scripts/build_literature.py`.\n")

    lines = [header]
    for row in rows:
        year = clean(row.get("Publication Year") or "—") or "—"
        ptype = clean(row.get("Publication Type") or "—") or "—"
        lines.append(f"| {title_cell(row)} | {authors_cell(row)} | {year} | {ptype} |\n")
    lines.append(note)

    path.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)} ({len(rows)} entries)")


def main():
    rows = load_rows()
    write_page(OUT_EN, rows, "en")
    write_page(OUT_AR, rows, "ar")


if __name__ == "__main__":
    main()
