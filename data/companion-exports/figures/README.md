# Figure sources

Every figure in *Introduction to Arabic Speech Technologies* that is drawn by
code, with the script that draws it. One directory per chapter, plus the shared
modules every script imports.

    pip install matplotlib numpy scipy pillow arabic_reshaper python-bidi
    cd ch09 && python3 make_fig9_1.py      # writes fig9_1.png and fig9_1.pdf

A Noto Naskh Arabic face is needed for any figure carrying Arabic script.

`figure-index.csv` lists all 74 figures with the script that draws each one and
the caption it carries in the book, so a page can be generated from it.

## The shared modules

| Module | What it does |
| --- | --- |
| `bookstyle.py` | the palette and the drawing primitives: boxes, notes, arrows, Arabic text |
| `figscale.py` | point sizes and rule widths, scaled for reproduction at about half the design width |
| `figfit.py` | checks that nothing is drawn outside the frame |
| `figlint.py` | enforces the rule that a figure carries labels, not prose |
| `arabtext.py` | draws Arabic with per-letter control |

## Four figures are not here, and this is why

Figures 3.1, 3.2, 3.4 and 3.7 are the author's own artwork rather than
code-drawn, so there is no script for them. They were checked during review and
are correct. Every other figure in the book, 70 of the 74, is produced by the
script beside it.

## One renaming worth knowing about

Chapter 7's scripts were written when the chapter had five figures. The original
Figure 7.1 was dropped and the rest renumbered, so the scripts here have been
renamed to the figure they draw; `figure-index.csv` records the old name of each.
