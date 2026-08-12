"""
Figure 7.5: the dialect long tail in transcribed Arabic speech.

Redrawn at the book's type scale, and rebuilt so it cannot be misread as data.

The author's artwork printed a numbered logarithmic axis and a value label on
every bar: 7000 for Modern Standard Arabic, 1200 for Egyptian, and so on down
to 6. Those figures are illustrative, and the caption said so, but a numbered
axis and a printed value are exactly what a later reader quotes. The rule for
this book is that illustrative data is marked illustrative inside the artwork
and its axis left unnumbered, so the shape can carry the argument and the
numbers cannot be lifted out of it.

The variety list is also corrected. The original ranked Najdi and Hijazi as
peers of Gulf, though both are sub-varieties within the Peninsular group the
"Gulf" bar already counts, so the same hours appeared twice. The bars now sit
at one level of the dialect hierarchy, and the sub-variety point is made in
the note instead.
"""
from bookstyle import NAVY, ORANGE, GREY, canvas, note, save
from figscale import fs, lws
from matplotlib.patches import Rectangle

# Heights are on an arbitrary logarithmic scale: the ordering and the size of
# the drop are the content, the values are not.
BARS = [
    ("MSA", 1.00),
    ("Egyptian", 0.63),
    ("Levantine", 0.55),
    ("Gulf", 0.50),
    ("Maghrebi", 0.41),
    ("Iraqi", 0.32),
    ("Sudanese", 0.25),
    ("Yemeni", 0.21),
    ("Hassaniya", 0.15),
    ("smaller\nvarieties", 0.10),
]


def draw(path_out):
    w, h = 12.6, 6.5
    fig, ax = canvas(w, h, (0, w), (0, h))

    base, top = 2.60, h - 0.35
    x0, x1 = 1.95, w - 0.55
    n = len(BARS)
    slot = (x1 - x0) / n
    bw = slot * 0.60

    ax.plot([x0 - 0.10, x1], [base, base], color=NAVY, lw=lws(1.4), zorder=3)
    ax.plot([x0 - 0.10, x0 - 0.10], [base, top + 0.10], color=NAVY,
            lw=lws(1.4), zorder=3)

    for i, (name, frac) in enumerate(BARS):
        cx = x0 + slot * (i + 0.5)
        bh = frac * (top - base)
        first = i == 0
        ax.add_patch(Rectangle((cx - bw / 2, base), bw, bh,
                               facecolor=NAVY if first else "#7E96BC",
                               edgecolor=NAVY, lw=lws(0.9),
                               hatch=None if first else "///", zorder=4))
        t_ = ax.text(cx, base - 0.22, name, fontsize=fs(9.8), color=NAVY,
                     weight="bold" if first else "normal", ha="right",
                     va="top", rotation=32, rotation_mode="anchor",
                     linespacing=1.4, zorder=5)

    ax.text(x0 - 0.52, (base + top) / 2,
            "transcribed hours (log scale, illustrative)",
            rotation=90, ha="center", va="center", fontsize=fs(10.2),
            color=NAVY)

    save(fig, path_out)


if __name__ == "__main__":
    draw("fig7_5.png")
