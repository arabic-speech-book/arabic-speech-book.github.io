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
def _bib_type(venue):
    low = (venue or "").lower()
    if any(k in low for k in ("proceedings", "conference", "workshop", "lrec",
                              "interspeech", "emnlp", "naacl", "icassp",
                              "symposium", "acl ")):
        return "inproceedings"
    if "arxiv" in low or not low:
        return "misc"
    return "article"


def _bibval(s):
    return (s or "").replace("{", "").replace("}", "").strip()


def write_bibtex(works, path):
    out = []
    for w in works:
        key = _bibval(w.get("bibtex_key")) or "ref"
        et = _bib_type(w.get("venue"))
        lines = [f"@{et}{{{key},"]

        def fld(name, val):
            val = _bibval(val)
            if val:
                lines.append(f"  {name} = {{{val}}},")

        fld("author", w.get("authors"))
        fld("title", w.get("title"))
        fld("year", w.get("year"))
        venue = _bibval(w.get("venue"))
        if venue:
            name = ("booktitle" if et == "inproceedings"
                    else "journal" if et == "article" else "howpublished")
            lines.append(f"  {name} = {{{venue}}},")
        fld("pages", w.get("pages"))
        fld("doi", w.get("doi"))
        fld("url", w.get("url"))
        fld("note", w.get("raw"))
        lines.append("}")
        out.append("\n".join(lines))
    path.write_text("\n\n".join(out) + "\n", encoding="utf-8")


def write_ris(works, path):
    ty = {"inproceedings": "CONF", "article": "JOUR", "misc": "GEN"}
    out = []
    for w in works:
        et = _bib_type(w.get("venue"))
        rec = [f"TY  - {ty[et]}"]
        if clean(w.get("authors")):
            rec.append(f"AU  - {clean(w.get('authors'))}")
        if clean(w.get("year")):
            rec.append(f"PY  - {clean(w.get('year'))}")
        if clean(w.get("title")):
            rec.append(f"TI  - {clean(w.get('title'))}")
        venue = clean(w.get("venue"))
        if venue:
            rec.append(f"{'BT' if et == 'inproceedings' else 'JO'}  - {venue}")
        pages = clean(w.get("pages"))
        if pages:
            m = re.split(r"[-–]", pages)
            rec.append(f"SP  - {m[0].strip()}")
            if len(m) > 1 and m[1].strip():
                rec.append(f"EP  - {m[1].strip()}")
        if clean(w.get("doi")):
            rec.append(f"DO  - {clean(w.get('doi'))}")
        if clean(w.get("url")):
            rec.append(f"UR  - {clean(w.get('url'))}")
        if clean(w.get("raw")):
            rec.append(f"N1  - {clean(w.get('raw'))}")
        rec.append("ER  - ")
        out.append("\n".join(rec))
    path.write_text("\n\n".join(out) + "\n", encoding="utf-8")


def build_bibliography():
    works = load_csv(EXP / "bibliography" / "bibliography.csv")
    for w in works:
        chs = (w.get("chapters") or "").strip()
        w["_chapters"] = [c.strip() for c in re.split(r"[;,]", chs) if c.strip()]

    # regenerate the downloadable BibTeX / RIS / CSV from this same corrected
    # source, so the page and the downloads never disagree
    dl = DOCS / "bibliography-files"
    dl.mkdir(parents=True, exist_ok=True)
    shutil.copy(EXP / "bibliography" / "bibliography.csv", dl / "bibliography.csv")
    write_bibtex(works, dl / "bibliography.bib")
    write_ris(works, dl / "bibliography.ris")

    def sort_key(w):
        a = clean(w.get("authors")) or clean(w.get("title")) or clean(w.get("raw"))
        return (a.lower(), clean(w.get("year")))

    works_sorted = sorted(works, key=sort_key)
    n = len(works_sorted)
    citations = sum(len(w["_chapters"]) for w in works)
    n_low = sum(1 for w in works if w.get("confidence") in ("low", "medium"))

    def fmt(w):
        chs = w.get("_chapters") or []
        chtag = f" *(Ch. {', '.join(chs)})*" if chs else ""
        conf = w.get("confidence", "")
        if conf == "high" and clean(w.get("title")):
            authors = clean(w.get("authors"))
            year = clean(w.get("year"))
            title = clean(w.get("title"))
            venue = clean(w.get("venue"))
            pages = clean(w.get("pages"))
            doi = clean(w.get("doi"))
            url = clean(w.get("url"))
            parts = []
            if authors:
                parts.append(authors + (f" ({year})." if year else "."))
            elif year:
                parts.append(f"({year}).")
            parts.append(f"*{title}*.")
            if venue:
                parts.append(venue + ".")
            if pages:
                parts.append(pages + ".")
            if doi:
                parts.append(f"[https://doi.org/{doi}](https://doi.org/{doi})")
            elif url:
                parts.append(f"[{url}]({url})")
            return " ".join(parts) + chtag
        # medium / low confidence: render the raw string exactly as printed
        raw = clean(w.get("raw"))
        url = clean(w.get("url"))
        if url and url not in raw:
            raw += f" [{url}]({url})"
        return raw + chtag

    def render(intro):
        out = [intro, ""]
        for w in works_sorted:
            out.append(f"1. {fmt(w)}")
        return "\n".join(out) + "\n"

    dto = ("Download: [BibTeX](bibliography-files/bibliography.bib) · "
           "[RIS](bibliography-files/bibliography.ris) · "
           "[CSV](bibliography-files/bibliography.csv)")
    intro_en = (
        f"# Bibliography\n\n"
        f"The book's complete reference list — **{n} distinct works**, cited "
        f"{citations} times across the fourteen chapters. Every record was "
        f"verified against the publisher record. {n_low} entries parsed with "
        f"less than full confidence (mostly undated web resources) and are shown "
        f"exactly as the book prints them.\n\n"
        f"{dto}\n\n"
        f"Each entry is tagged with the chapter(s) that cite it. "
        f"*Last checked: {LAST_CHECKED}.*"
    )
    intro_ar = (
        f"# ثبت المراجع\n\n"
        f"قائمة مراجع الكتاب الكاملة — **{n} عملًا متمايزًا**، مُستشهَدًا بها "
        f"{citations} مرّة عبر الفصول الأربعة عشر. تُحقِّق من كل سجل مقابل سجل "
        f"الناشر. {n_low} مدخلًا "
        f"حُلِّلت بثقة أقل من الكاملة (غالبها موارد وِب غير مؤرَّخة) وتُعرَض كما "
        f"يطبعها الكتاب تمامًا.\n\n"
        f"تنزيل: [BibTeX](bibliography-files/bibliography.bib) · "
        f"[RIS](bibliography-files/bibliography.ris) · "
        f"[CSV](bibliography-files/bibliography.csv)\n\n"
        f"كل مدخل موسوم بالفصل (الفصول) التي تستشهد به. "
        f"*آخر تحقّق: {LAST_CHECKED}.*"
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
