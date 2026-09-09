#!/usr/bin/env python3
"""Generate the companion reference pages from data/companion-exports/.

Produces (EN + AR) glossary, abbreviations, bibliography, resource index and
figure-source pages, and copies the downloadable assets (BibTeX/RIS/CSV and the
figure scripts) into docs/. Re-run after refreshing the exports:

    python scripts/build_companion.py

Everything is extracted from the manuscript's exports, so the site and the book
cannot drift apart.
"""
import csv
import json
import re
import shutil
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "data" / "companion-exports"
DOCS = ROOT / "docs"
LAST_CHECKED = "2026-08-12"


def clean(text, cell=False):
    if text is None:
        return ""
    text = re.sub(r"\s+", " ", str(text)).strip()
    if cell:
        text = text.replace("|", "\\|")
    return text


def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write(rel, text):
    p = DOCS / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print(f"  wrote docs/{rel}")


def letter_of(term):
    for ch in term:
        if ch.isalpha():
            return ch.upper() if ch.isascii() else "Arabic"
        if ch.isdigit():
            return "0–9"
    return "#"


# --------------------------------------------------------------------------- #
# Glossary
# --------------------------------------------------------------------------- #
def build_glossary():
    rows = load_csv(EXP / "glossary" / "glossary.csv")
    terms = OrderedDict()
    for r in rows:
        term = clean(r["term"])
        terms.setdefault(term, [])
        entry = (clean(r["chapter"]), clean(r["definition"]))
        # merge identical definitions, collecting chapters
        for i, (chs, d) in enumerate(terms[term]):
            if d == entry[1]:
                if entry[0] not in chs.split(", "):
                    terms[term][i] = (chs + ", " + entry[0], d)
                break
        else:
            terms[term].append(entry)

    ordered = sorted(terms.items(), key=lambda kv: kv[0].lower())
    n_terms = len(ordered)
    n_defs = sum(len(v) for v in terms.values())

    def render(intro):
        out = [intro, ""]
        current = None
        for term, defs in ordered:
            lett = letter_of(term)
            if lett != current:
                current = lett
                out.append(f"\n## {lett}\n")
            if len(defs) == 1:
                chs, d = defs[0]
                out.append(f"**{term}** — {d} *(Ch. {chs})*\n")
            else:
                out.append(f"**{term}**\n")
                for chs, d in defs:
                    out.append(f"- *(Ch. {chs})* {d}")
                out.append("")
        return "\n".join(out) + "\n"

    intro_en = (
        f"# Glossary\n\n"
        f"Every term defined across the fourteen chapters, merged into one "
        f"alphabetical, searchable list — **{n_terms} distinct terms**, "
        f"{n_defs} definitions. Where two chapters define a term differently, "
        f"both wordings are kept, each tagged with its chapter. Use the search "
        f"box at the top of the page to jump to a term."
    )
    intro_ar = (
        f"# المسرد\n\n"
        f"كل مصطلح معرَّف عبر الفصول الأربعة عشر، مدموجًا في قائمة أبجدية واحدة "
        f"قابلة للبحث — **{n_terms} مصطلحًا متمايزًا**، و{n_defs} تعريفًا. وحيثما "
        f"عرّف فصلان مصطلحًا تعريفًا مختلفًا، حُفِظت الصياغتان، كلٌّ موسومة بفصلها. "
        f"استخدم مربّع البحث أعلى الصفحة للانتقال إلى مصطلح."
    )
    write("glossary.md", render(intro_en))
    write("glossary.ar.md", render(intro_ar))


# --------------------------------------------------------------------------- #
# Abbreviations
# --------------------------------------------------------------------------- #
def build_abbreviations():
    rows = load_csv(EXP / "abbreviations" / "abbreviations.csv")
    abbr = OrderedDict()
    for r in rows:
        a = clean(r["abbreviation"], cell=True)
        exp = clean(r["expansion"], cell=True)
        # drop stray footnote markers glued to the end (e.g. "...recall1")
        exp = re.sub(r"(?<=[A-Za-z])\d+$", "", exp).strip()
        ch = clean(r["chapter"])
        d = abbr.setdefault(a, {"exp": [], "ch": set()})
        # dedupe expansions case-insensitively, keeping the first casing seen
        if exp and exp.lower() not in {e.lower() for e in d["exp"]}:
            d["exp"].append(exp)
        if ch:
            d["ch"].add(ch)
    ordered = sorted(abbr.items(), key=lambda kv: kv[0].lower())
    n = len(ordered)

    def render(intro):
        out = [intro, "", "| Abbreviation | Expansion | Chapters |",
               "|--------------|-----------|----------|"]
        for a, d in ordered:
            chs = ", ".join(sorted(d["ch"], key=lambda x: int(x) if x.isdigit() else 99))
            out.append(f"| **{a}** | {' / '.join(d['exp'])} | {chs} |")
        return "\n".join(out) + "\n"

    intro_en = (
        f"# Abbreviation Index\n\n"
        f"The **{n} distinct abbreviations** used across the book, alphabetical, "
        f"each with its expansion and the chapters that use it. (An abbreviation "
        f"defined in several chapters — ASR, for instance — is one entry, with "
        f"every chapter listed.)"
    )
    intro_ar = (
        f"# قائمة الاختصارات\n\n"
        f"الاختصارات المتمايزة الـ**{n}** المستخدمة عبر الكتاب، مرتّبة أبجديًّا، "
        f"كلٌّ بتوسعته والفصول التي تستخدمه. (الاختصار المعرَّف في عدّة فصول — "
        f"مثل ASR — مدخل واحد تُدرَج فيه كل الفصول.)"
    )
    write("abbreviations.md", render(intro_en))
    write("abbreviations.ar.md", render(intro_ar))


# --------------------------------------------------------------------------- #
# Bibliography
# --------------------------------------------------------------------------- #
BIB_CHECKED = "2026-09-09"

_ACCENT = re.compile(r"\\['\"^`~=.vHtcdbu]\s*\{?([A-Za-z])\}?")


def _debrace(s):
    if not s:
        return ""
    s = _ACCENT.sub(r"\1", str(s))
    s = (s.replace("{", "").replace("}", "")
           .replace("\\&", "&").replace("\\_", "_").replace("\\%", "%")
           .replace("\\$", "$").replace("\\#", "#").replace("~", " ")
           .replace("\\", ""))
    return clean(s)


_RIS_TYPE = {"article": "JOUR", "inproceedings": "CONF", "incollection": "CHAP",
             "book": "BOOK", "phdthesis": "THES", "mastersthesis": "THES",
             "techreport": "RPRT", "misc": "GEN"}


def _venue(e):
    for f in ("journal", "booktitle", "publisher", "school", "institution",
              "series", "howpublished"):
        if e.get(f):
            return _debrace(e[f])
    return ""


def _authors(e):
    a = _debrace(e.get("author") or e.get("editor") or "")
    return "; ".join(p.strip() for p in re.split(r"\s+and\s+", a) if p.strip())


def _doi(e):
    d = _debrace(e.get("doi", "")).strip()
    return d.replace("https://doi.org/", "").replace("http://doi.org/", "") if d else ""


def _link(e):
    d = _doi(e)
    return f"https://doi.org/{d}" if d else (e.get("url") or "").strip()


def _last_name(e):
    a = _debrace(e.get("author") or e.get("editor") or "")
    if not a:
        return None
    first = re.split(r"\s+and\s+", a)[0].strip()
    return (first.split(",")[0] if "," in first else first.split()[-1]).lower()


def _load_bib():
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    with open(EXP / "bibliography" / "bibliography.bib", encoding="utf-8") as f:
        return bibtexparser.load(f, parser=parser).entries


def _write_ris_bib(entries, path):
    out = []
    for e in entries:
        rec = [f"TY  - {_RIS_TYPE.get(e.get('ENTRYTYPE', 'misc'), 'GEN')}"]
        a = _debrace(e.get("author") or e.get("editor") or "")
        for au in (p.strip() for p in re.split(r"\s+and\s+", a) if p.strip()):
            rec.append(f"AU  - {au}")
        if _debrace(e.get("year", "")):
            rec.append(f"PY  - {_debrace(e['year'])}")
        if _debrace(e.get("title", "")):
            rec.append(f"TI  - {_debrace(e['title'])}")
        venue = _venue(e)
        if venue:
            tag = "BT" if e.get("ENTRYTYPE") in ("inproceedings", "incollection") else "JO"
            rec.append(f"{tag}  - {venue}")
        pages = _debrace(e.get("pages", ""))
        if pages:
            m = re.split(r"[-\u2013]+", pages)
            rec.append(f"SP  - {m[0].strip()}")
            if len(m) > 1 and m[-1].strip():
                rec.append(f"EP  - {m[-1].strip()}")
        if _doi(e):
            rec.append(f"DO  - {_doi(e)}")
        if (e.get("url") or "").strip():
            rec.append(f"UR  - {e['url'].strip()}")
        rec.append("ER  - ")
        out.append("\n".join(rec))
    path.write_text("\n\n".join(out) + "\n", encoding="utf-8")


def _write_csv_bib(entries, path):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "type", "authors", "year", "title", "venue", "doi", "url"])
        for e in entries:
            w.writerow([e.get("ID", ""), e.get("ENTRYTYPE", ""), _authors(e),
                        _debrace(e.get("year", "")), _debrace(e.get("title", "")),
                        _venue(e), _doi(e), (e.get("url") or "").strip()])


def build_bibliography():
    entries = _load_bib()

    dl = DOCS / "bibliography-files"
    dl.mkdir(parents=True, exist_ok=True)
    # publish the validated .bib verbatim (already cleaned of local file paths)
    shutil.copy(EXP / "bibliography" / "bibliography.bib", dl / "bibliography.bib")
    _write_ris_bib(entries, dl / "bibliography.ris")
    _write_csv_bib(entries, dl / "bibliography.csv")

    entries_sorted = sorted(
        entries,
        key=lambda e: (_last_name(e) or _debrace(e.get("title", "")).lower(),
                       _debrace(e.get("year", ""))))
    n = len(entries_sorted)
    n_doi = sum(1 for e in entries if _doi(e))

    def fmt(e):
        authors = _authors(e)
        year = _debrace(e.get("year", ""))
        title = _debrace(e.get("title", ""))
        venue = _venue(e)
        link = _link(e)
        parts = []
        if authors:
            parts.append(authors + (f" ({year})." if year else "."))
        elif year:
            parts.append(f"({year}).")
        if title:
            parts.append(f"*{title}*.")
        if venue:
            parts.append(venue + ".")
        if link:
            parts.append(f"<{link}>")
        return " ".join(parts)

    def render(intro):
        out = [intro, ""]
        for e in entries_sorted:
            out.append(f"1. {fmt(e)}")
        return "\n".join(out) + "\n"

    dto = ("Download: [BibTeX](bibliography-files/bibliography.bib) \u00b7 "
           "[RIS](bibliography-files/bibliography.ris) \u00b7 "
           "[CSV](bibliography-files/bibliography.csv)")
    intro_en = (
        f"# Bibliography\n\n"
        f"The book's complete, validated reference list \u2014 **{n} works**, "
        f"{n_doi} with a DOI, each with a live link. Every record was verified "
        f"against the publisher record.\n\n"
        f"{dto}\n\n"
        f"Use the search box at the top of the page to find an entry. "
        f"*Last checked: {BIB_CHECKED}.*"
    )
    intro_ar = (
        f"# \u062b\u0628\u062a \u0627\u0644\u0645\u0631\u0627\u062c\u0639\n\n"
        f"\u0642\u0627\u0626\u0645\u0629 \u0645\u0631\u0627\u062c\u0639 "
        f"\u0627\u0644\u0643\u062a\u0627\u0628 \u0627\u0644\u0643\u0627\u0645\u0644\u0629 "
        f"\u0627\u0644\u0645\u064f\u062a\u062d\u0642\u064e\u0651\u0642 \u0645\u0646\u0647\u0627 "
        f"\u2014 **{n} \u0639\u0645\u0644\u064b\u0627**\u060c \u0645\u0646\u0647\u0627 "
        f"{n_doi} \u0628\u0645\u0639\u0631\u0651\u0641 DOI\u060c \u0648\u0644\u0643\u0644\u0651 "
        f"\u0631\u0627\u0628\u0637 \u062d\u064a\u0651. \u062a\u064f\u062d\u0642\u0651\u0642 "
        f"\u0645\u0646 \u0643\u0644 \u0633\u062c\u0644 \u0645\u0642\u0627\u0628\u0644 "
        f"\u0633\u062c\u0644 \u0627\u0644\u0646\u0627\u0634\u0631.\n\n"
        f"\u062a\u0646\u0632\u064a\u0644: [BibTeX](bibliography-files/bibliography.bib) \u00b7 "
        f"[RIS](bibliography-files/bibliography.ris) \u00b7 "
        f"[CSV](bibliography-files/bibliography.csv)\n\n"
        f"\u0627\u0633\u062a\u062e\u062f\u0645 \u0645\u0631\u0628\u0651\u0639 "
        f"\u0627\u0644\u0628\u062d\u062b \u0623\u0639\u0644\u0649 \u0627\u0644\u0635\u0641\u062d\u0629 "
        f"\u0644\u0625\u064a\u062c\u0627\u062f \u0645\u062f\u062e\u0644. "
        f"*\u0622\u062e\u0631 \u062a\u062d\u0642\u0651\u0642: {BIB_CHECKED}.*"
    )
    write("bibliography.md", render(intro_en))
    write("bibliography.ar.md", render(intro_ar))


# --------------------------------------------------------------------------- #
# Resource index
# --------------------------------------------------------------------------- #
def build_resource_index():
    items = load_json(EXP / "resource-index" / "resource-index.json")
    corpora = [r for r in items if "7.1" in (r.get("source") or "")]
    others = [r for r in items if "7.1" not in (r.get("source") or "")]
    spotlights = [r for r in items if clean(r.get("spotlight"))]

    def c(v):
        return clean(v, cell=True) or "—"

    def render(lang):
        ar = lang == "ar"
        if ar:
            out = ["# فهرس مصادر الكلام العربي", ""]
            out.append("كل مدوّنة ومقياس ونموذج وأداة ورد في الكتاب، في مكان واحد. "
                       f"هذه هي الصفحة التي يربط بها الناس، وأسرعها تقادمًا؛ آخر تحقّق: **{LAST_CHECKED}**.\n")
            out.append('!!! danger "تحذير يصرّ عليه الكتاب"')
            out.append("    النموذج المُدرَّب **مكوّن غير مُختبَر** حتى تختبره، وقائمة اللغات "
                       "**ليست** دليلًا على تغطية اللهجات.\n")
            out.append("## المدوّنات (Table 7.1)\n")
            out.append("| الاسم | الحجم | النوع | المجال | الوصول/الرخصة | الاستخدام | الفصل | آخر تحقّق |")
            out.append("|-------|------|------|--------|----------------|-----------|-------|-----------|")
        else:
            out = ["# Arabic Speech Resource Index", ""]
            out.append("Every corpus, benchmark, model, and toolkit named in the book, in one place. "
                       f"This is the page people link to and the one that goes stale fastest; last checked: **{LAST_CHECKED}**.\n")
            out.append('!!! danger "A caution the book insists on"')
            out.append("    A checkpoint is an **untested component** until you test it, and a "
                       "language list is **not** evidence of dialect coverage.\n")
            out.append("## Corpora (Table 7.1)\n")
            out.append("| Name | Scale | Variety | Domain | Access / licence | Main use | Ch. | Last checked |")
            out.append("|------|-------|---------|--------|------------------|----------|-----|--------------|")
        for r in corpora:
            out.append(f"| **{c(r.get('name'))}** | {c(r.get('scale'))} | {c(r.get('variety'))} | "
                       f"{c(r.get('domain'))} | {c(r.get('access_licence'))} | {c(r.get('main_use'))} | "
                       f"{c(r.get('chapter'))} | {LAST_CHECKED} |")
        # models & toolkits
        if ar:
            out.append("\n## النماذج والأدوات وعائلات الطرائق\n")
            out.append("جداول الفصول الأخرى لا تحمل عمود رخصة، فتُترَك تلك الحقول فارغة بدل التخمين.\n")
            out.append("| الاسم | النوع | المجال | الاستخدام | الفصل |")
            out.append("|-------|------|--------|-----------|-------|")
        else:
            out.append("\n## Models, toolkits & method families\n")
            out.append("The tables in the other chapters carry no licence column, so those fields "
                       "are left empty rather than filled with a guess.\n")
            out.append("| Name | Type | Domain | Main use | Ch. |")
            out.append("|------|------|--------|----------|-----|")
        for r in others:
            out.append(f"| **{c(r.get('name'))}** | {c(r.get('variety'))} | {c(r.get('domain'))} | "
                       f"{c(r.get('main_use'))} | {c(r.get('chapter'))} |")
        # spotlights
        if spotlights:
            out.append("\n## Dataset spotlights\n" if not ar else "\n## أضواء على المجموعات\n")
            for r in spotlights:
                name = clean(r.get("name"))
                sp = clean(r.get("spotlight"))
                out.append(f'??? note "{name}"')
                for para in re.split(r"(?<=[.。])\s+(?=[A-Z؀-ۿ])", sp):
                    para = clean(para)
                    if para:
                        out.append(f"    {para}\n")
        return "\n".join(out) + "\n"

    write("resources/resource-index.md", render("en"))
    write("resources/resource-index.ar.md", render("ar"))


# --------------------------------------------------------------------------- #
# Figures
# --------------------------------------------------------------------------- #
def build_figures():
    # copy the scripts + shared modules for download/serving
    dst = DOCS / "figure-scripts"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(EXP / "figures", dst)
    # keep the scripts' own README as a downloadable file, not a built page
    readme = dst / "README.md"
    if readme.exists():
        readme.rename(dst / "README.txt")

    rows = load_csv(EXP / "figures" / "figure-index.csv")
    by_ch = defaultdict(list)
    for r in rows:
        by_ch[int(r["chapter"])].append(r)

    def figkey(r):
        parts = re.findall(r"\d+", r["figure"])
        return tuple(int(p) for p in parts) if parts else (0,)

    def render(lang):
        ar = lang == "ar"
        if ar:
            out = ["# مصادر الأشكال", "",
                   "السكربت الذي يرسم كل شكل مرسوم بالكود في الكتاب. أربعة أشكال (3.1 و3.2 و3.4 و3.7) "
                   "من رسم المؤلّفة لا من الكود، فلا سكربت لها. الوحدات المشتركة التي يستوردها كل سكربت في "
                   "`figure-scripts/shared/` (انظر [`README`](figure-scripts/README.txt)).\n",
                   "```bash",
                   "pip install matplotlib numpy scipy pillow arabic_reshaper python-bidi",
                   "cd figure-scripts/ch09 && python make_fig9_1.py   # يكتب fig9_1.png و fig9_1.pdf",
                   "```\n"]
            hdr = "| الشكل | الوصف | المصدر |"
        else:
            out = ["# Figure Sources", "",
                   "The script that draws each code-drawn figure in the book. Four figures "
                   "(3.1, 3.2, 3.4, 3.7) are the author's own artwork rather than code, so no "
                   "script exists for them. The shared modules every script imports live in "
                   "`figure-scripts/shared/` (see the [`README`](figure-scripts/README.txt)).\n",
                   "```bash",
                   "pip install matplotlib numpy scipy pillow arabic_reshaper python-bidi",
                   "cd figure-scripts/ch09 && python make_fig9_1.py   # writes fig9_1.png and fig9_1.pdf",
                   "```\n"]
            hdr = "| Figure | Caption | Source |"
        for ch in sorted(by_ch):
            title = "الفصل" if ar else "Chapter"
            out.append(f"\n## {title} {ch}\n")
            out.append(hdr)
            out.append("|---|---|---|")
            for r in sorted(by_ch[ch], key=figkey):
                cap = clean(r.get("caption"), cell=True)
                if len(cap) > 160:
                    cap = cap[:157].rstrip() + "…"
                if clean(r.get("present")).lower() == "yes":
                    src = f"[`{clean(r['script'])}`](figure-scripts/{clean(r['script'])})"
                else:
                    src = "author artwork — in the book" if not ar else "رسم المؤلّفة — في الكتاب"
                out.append(f"| {clean(r['figure'])} | {cap} | {src} |")
        return "\n".join(out) + "\n"

    write("figures.md", render("en"))
    write("figures.ar.md", render("ar"))


def main():
    print("Building companion pages from data/companion-exports/ …")
    build_glossary()
    build_abbreviations()
    build_bibliography()
    build_resource_index()
    build_figures()
    print("Done.")


if __name__ == "__main__":
    main()
