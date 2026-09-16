# Companion website exports

*Introduction to Arabic Speech Technology*, by Hend S. Al-Khalifa.
Generated 12 August 2026 from the fourteen final chapters.

Everything here is extracted from the manuscript itself rather than retyped, so
the site and the book cannot drift apart. Where a value could not be extracted
with confidence, the file says so in a column rather than guessing.

| Folder | What it holds | Count |
| --- | --- | --- |
| `bibliography/` | the whole bibliography as BibTeX, RIS, CSV and JSON | 275 distinct works, cited 398 times |
| `glossary/` | every defined term with its definition and chapter | 337 entries, 291 distinct terms |
| `abbreviations/` | every abbreviation with its expansion and chapter | 268 entries, 127 distinct abbreviations |
| `resource-index/` | corpora, benchmarks, models and toolkits | 21 corpora with size, variety, domain and licence, plus 35 models and toolkits |
| `figures/` | the script behind each figure, and the shared modules | 70 of 74 figures |
| `templates/` | the Chapter 14 templates, each with its worked example | 4 templates and a checklist |

## Notes that matter for the site

**The counts differ from the ones in the earlier spec, and these are the right
ones.** The book now cites 398 references rather than 395, and carries 127
distinct abbreviations rather than 167. The 167 was a count of table rows across
chapters before the abbreviation lists were completed and deduplicated; 268 rows
now resolve to 127 distinct abbreviations, because a chapter that uses an
abbreviation defines it, so ASR appears in eleven chapters and is one entry.
Use the numbers in the table above.

**Bibliography.** 275 distinct works. 63 are cited in more than one chapter, and
each entry's `keywords` field lists every chapter that cites it, so the site can
offer "references for Chapter 7". Every record carries the entry exactly as the
book prints it, in BibTeX `note` and RIS `N1`. 39 of the 398 chapter entries
parsed with less than full confidence, mostly undated web resources and titles
containing a full stop; their `confidence` column says `medium` or `low` and the
raw string is beside them. **Render `raw` for those rather than the parsed
fields.** `by-chapter.csv` keeps the per-chapter numbering, so a citation marked
[21] in Chapter 9 can be resolved from the site.

**Glossary and abbreviations.** Both are per chapter, because the book defines
terms per chapter and two chapters sometimes define the same term differently,
each for its own use. The `.md` files merge them alphabetically and keep both
wordings where they differ; the `.csv` and `.json` keep them separate. Pick
whichever fits the page you are building.

**Resource index.** The 21 corpora come from the book's master catalogue
(Table 7.1) and carry the six columns the spec asks for: name, scale, variety,
domain, access and licence, and main use. The other 35 rows are models,
toolkits and method families from the tables in Chapters 1, 3, 4, 5, 6, 8, 9, 10
and 11; those tables do not carry a licence column, so those fields are empty
rather than filled with a guess. Where the book has a Dataset Spotlight for a
resource, its full text is in the `spotlight` column.

**Every row of this index needs a date.** The book says so in Chapter 9 and the
website spec repeats it: a licence, a size or a supported-language list is a
page that changes. Add a `last_checked` column when you publish, and put the
model-hub caution on the page: a checkpoint is an untested component until you
test it, and a language list is not evidence of dialect coverage.

**Figures.** 70 of the 74 have their script. Figures 3.1, 3.2, 3.4 and 3.7 are
the author's own artwork rather than code-drawn, so no script exists for them.
`figures/README.md` explains this and also records that Chapter 7's scripts were
renamed after the chapter renumbered its figures.

**Templates.** The spec expected four templates including an "evaluation
report". The book's appendix has a datasheet, an annotation guideline, a consent
form and a tool reference. There is no evaluation-report template, so rather
than invent one I have compiled
`evaluation-and-reproducibility-checklist.md` from the Reproducibility Note of
all fourteen chapters, which is the book's own answer to the same need. Each
template file carries the empty form and then the worked example from the
chapter's Gulf-dialect case study, so a reader sees what a filled one looks like.

## What is still missing, and who has it

- **The audio.** The clips behind the spectrograms, the emphatic and plain minimal pairs, and the dialect samples are in the figure-source archives on the author's machine, not here. A speech book's website should be able to make a sound.
- **The four Chapter 3 figures.** Author artwork; there is nothing to publish but the images themselves, which are in the chapter.
- **Errata and the new-applications page.** Nothing to seed them with yet. Both start empty by design and are promised in print, so they must exist from launch.
