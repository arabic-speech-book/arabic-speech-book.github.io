"""
Figure 7.2: an approximate release timeline of the resources in Table 7.1.

A timeline, drawn on one axis. The author's artwork measured 2.9 pt at the
smallest ink band, well below Springer's 7 pt floor, and it also omitted five
of the catalog's fifteen resources, including all three King Saud University
collections.

Fifteen markers do not fit on a single axis if each is nudged sideways into a
free lane, which is what an intermediate version tried and what made it
fragile: a label ends up away from the year it belongs to. This one groups by
year instead. Every resource released in the same year hangs from one stem,
stacked, consecutive year groups alternate above and below the axis, and a
group whose first name would touch the group before it starts one lane further
out and grows its stem to reach. A name therefore always sits directly over its
own year, and adding a sixteenth resource means adding a line to ENTRIES.

Every row of Table 7.1 appears here, at the year its reference entry in this
chapter carries. Common Voice Arabic has no single release date, so it is drawn
as a band across the years it has been versioned over.

There is no explanatory text inside the artwork. The corpus names are data
labels; their expansions are in the caption.
"""
from bookstyle import NAVY, ORANGE, GREY, canvas, note, save
from figscale import fs, lws
from figfit import width_in, FAILURES, report
from matplotlib.patches import Rectangle

# year -> the resources released that year, in the catalog's order
ENTRIES = [
    (2003, ["KAPD"]),
    (2008, ["SAAVB"]),
    (2014, ["KSU"]),
    (2016, ["MGB-2", "Arabic Speech Corpus"]),
    (2017, ["MGB-3"]),
    (2019, ["MGB-5"]),
    (2021, ["QASR"]),
    (2023, ["MASC", "Aswat", "FLEURS"]),
    (2022, ["ArabCeleb"]),
    (2024, ["SADA", "Casablanca", "L2-KSU", "ZAEBUC-Spoken"]),
    (2026, ["L2AraSpeech", "Habibi"]),
]

# Resources with no single release date, drawn as a band across the years they
# span: Common Voice by version, and the LDC dialect telephone corpora, which
# were collected over a decade and appear in Table 7.1 as one row.
BANDS = [("LDC dialect telephone", 1997.0, 2007.0),
         ("NEMLAR", 2002.0, 2005.0),
         ("Common Voice Arabic", 2019.0, 2026.5)]
Y0, Y1 = 1996.0, 2027.0
STEM, GAP, STEP = 0.46, 0.24, 0.34


def draw(path_out):
    w, h = 12.6, 7.6
    fig, ax = canvas(w, h, (0, w), (0, h))
    axis_y = 2.75
    x0, x1 = 0.60, w - 0.35

    def X(year):
        return x0 + (year - Y0) / (Y1 - Y0) * (x1 - x0)

    ax.plot([X(Y0), X(Y1)], [axis_y] * 2, color=NAVY, lw=lws(2.0),
            solid_capstyle="butt", zorder=3)
    for yr in range(1997, 2028):
        big = yr % 3 == 1
        ax.plot([X(yr)] * 2, [axis_y - (0.11 if big else 0.06),
                              axis_y + (0.11 if big else 0.06)],
                color=NAVY, lw=lws(1.0), zorder=4)
        if big:
            note(ax, X(yr), axis_y - 0.32, str(yr), size=9.6, colour=GREY)

    def measure(text, size, weight="bold"):
        probe = ax.text(0, -9, text, fontsize=fs(size), weight=weight)
        tw, _ = width_in(fig, probe)
        probe.remove()
        return tw

    def label(text, x, y, size=9.6):
        """Centred, unless that would run past the frame."""
        tw = measure(text, size)
        left, right, ha, ax_ = x - tw / 2, x + tw / 2, "center", x
        if right > w - 0.12:
            right, left, ha, ax_ = w - 0.12, w - 0.12 - tw, "right", w - 0.12
        elif left < 0.12:
            left, right, ha, ax_ = 0.12, 0.12 + tw, "left", 0.12
        note(ax, ax_, y, text, size=size, colour=NAVY, weight="bold", ha=ha)
        return left, right

    def extent(text, x, size=9.6):
        """Where the label would sit, clamped inside the frame."""
        tw = measure(text, size)
        left, right = x - tw / 2, x + tw / 2
        if right > w - 0.12:
            right, left = w - 0.12, w - 0.12 - tw
        elif left < 0.12:
            left, right = 0.12, 0.12 + tw
        return left, right

    # lanes[side] holds the x intervals already used at each lane, so a group
    # whose names would touch the group before it starts one lane further out
    # rather than being nudged sideways off its own year.
    lanes = {True: [], False: []}

    for i, (year, names) in enumerate(ENTRIES):
        x, up = X(year), i % 2 == 0
        s = 1 if up else -1
        # The year label sits one lane beyond the names and has to be
        # tested with them: leaving it out let a 2019 year label land on a
        # 2016 corpus name.
        spans = [extent(n, x) for n in names] + [extent(str(year), x, 9.2)]

        base = 0
        while True:
            rows = lanes[up]
            clash = False
            for k, (l, r) in enumerate(spans):
                if base + k < len(rows):
                    for pl, pr in rows[base + k]:
                        if l < pr + 0.16 and r > pl - 0.16:
                            clash = True
            if not clash:
                break
            base += 1
            if base > 8:
                FAILURES.append(f'no free lane for the {year} group')
                break

        rows = lanes[up]
        while len(rows) < base + len(spans):
            rows.append([])

        ax.plot([x], [axis_y], marker="o", markersize=fs(3.4), color=ORANGE,
                markeredgecolor=NAVY, markeredgewidth=lws(0.7), zorder=6)

        first_y = axis_y + s * (STEM + GAP + 0.16 + base * STEP)
        ax.plot([x, x], [axis_y + s * 0.12, first_y - s * 0.14], color=GREY,
                lw=lws(0.9), zorder=2)

        for k, (name, (l, r)) in enumerate(zip(names, spans)):
            y = first_y + s * k * STEP
            label(name, x, y)
            rows[base + k].append((l, r))

        ytop = first_y + s * len(names) * STEP
        note(ax, x, ytop, str(year), size=9.2, colour=GREY)
        rows[base + len(names)].append(spans[-1])

    for k, (name, a, b) in enumerate(BANDS):
        band_y = axis_y + 2.55 + k * 0.72
        ax.add_patch(Rectangle((X(a), band_y), X(b) - X(a), 0.22,
                               facecolor="#9FB4D2", edgecolor=NAVY,
                               lw=lws(0.9), zorder=4))
        ax.plot([X(a)] * 2, [axis_y + 0.12, band_y], color=GREY, lw=lws(0.9),
                ls=(0, (3, 3)), zorder=2)
        note(ax, X(a), band_y + 0.34, name, size=10.4, colour=NAVY,
             weight="bold", ha="left")

    save(fig, path_out)
    report()


if __name__ == "__main__":
    draw("fig7_2.png")
