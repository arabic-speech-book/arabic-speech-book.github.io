"""
Figure 2.7 for Chapter 2 of *Introduction to Arabic Speech Technology*:
the major spoken-Arabic dialect groups.

Drawn deterministically from Natural Earth 1:50m Admin 0 Countries, which is
in the public domain (naturalearthdata.com). No image model is involved and no
third-party map is traced, so the figure needs no permission clearance and is
consistent with the book's declaration that its figures are code-drawn.

Three faults in the previous artwork are fixed:
  1. Six groups were distinguished by pastel fill colour alone, with gradient
     blending, so the figure did not survive grayscale printing. Each group now
     carries a hatch pattern as well as a colour.
  2. Yemen was left uncoloured, and Mauritania with it. Yemeni is now its own
     group and Hassaniya is explicitly folded into Maghrebi rather than
     silently dropped.
  3. The map carried no statement about boundaries. One is now printed on the
     figure and repeated in the caption.

Requires: pyshp, matplotlib, and the Natural Earth 50m admin-0 shapefile.
"""

import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from figscale import fs, lws, ms, arr
from matplotlib.patches import Polygon as MplPolygon, Patch, FancyBboxPatch
import shapefile

SHP = "ne/ne_50m_admin_0_countries"

NAVY = "#1F3864"
CONTEXT_FILL = "#F2F4F7"
CONTEXT_EDGE = "#C8CFD9"
BORDER = "#8A93A0"

# Group -> (member ADMIN names, fill colour, hatch, label, feature from Table 2.8)
GROUPS = [
    ("Maghrebi",
     ["Morocco", "Algeria", "Tunisia", "Libya", "Mauritania", "Western Sahara"],
     "#E5DCF2", "///", "short vowels reduced"),
    ("Egyptian",
     ["Egypt"],
     "#FCEBCB", "...", "jīm pronounced /g/"),
    ("Sudanese",
     ["Sudan"],
     "#F8D6D2", "xxx", "jīm a voiced palatal stop"),
    ("Levantine",
     ["Syria", "Lebanon", "Jordan", "Palestine"],
     "#D8EBD9", "|||", "qāf a glottal stop"),
    ("Iraqi",
     ["Iraq"],
     "#D3E2F5", "\\\\\\", "qāf /g/ in gilit dialects"),
    ("Gulf",
     ["Saudi Arabia", "Kuwait", "Qatar", "Bahrain",
      "United Arab Emirates", "Oman"],
     "#CFE9E4", "---", "qāf pronounced /g/"),
    ("Yemeni",
     ["Yemen"],
     "#EDE3CF", "+++", "qāf /g/ in Ṣanʿānī;\nemphatic ṭ voiced"),
]

# Drawn unfilled, for geographic context only.
CONTEXT = ["Turkey", "Iran", "Israel", "Cyprus", "Chad", "Niger", "Mali",
           "South Sudan", "Ethiopia", "Eritrea", "Djibouti", "Somalia",
           "Somaliland", "Senegal", "Mali", "Burkina Faso", "Nigeria",
           "Greece", "Italy", "Spain", "Portugal", "Malta", "Kenya", "Uganda",
           "Central African Republic", "Cameroon", "Armenia", "Azerbaijan",
           "Georgia", "Turkmenistan", "Afghanistan", "Pakistan", "Gambia",
           "Guinea", "Guinea-Bissau", "Mali", "Nigeria"]

# Country name labels: (name, lon, lat, fontsize)
COUNTRY_LABELS = [
    ("Morocco", -6.5, 31.6, 7.4), ("Algeria", 2.5, 27.5, 7.8),
    ("Tunisia", 9.4, 34.6, 6.8), ("Libya", 17.5, 27.0, 7.8),
    ("Mauritania", -10.5, 20.3, 7.0), ("Egypt", 29.5, 26.5, 8.2),
    ("Sudan", 30.0, 15.5, 8.0), ("Saudi Arabia", 44.5, 23.5, 8.2),
    ("Yemen", 47.0, 15.5, 7.8), ("Oman", 56.5, 21.0, 7.2),
    ("Iraq", 43.5, 33.0, 7.6), ("Syria", 38.3, 35.2, 6.6),
    ("Jordan", 36.6, 31.0, 6.4), ("Lebanon", 31.6, 34.3, 6.2),
    ("Kuwait", 47.9, 29.6, 6.0), ("Qatar", 51.5, 25.4, 6.0),
    ("U.A.E.", 54.6, 23.6, 6.2),
]

# Callouts: (group, text_lon, text_lat, anchor_lon, anchor_lat)
CALLOUTS = [
    ("Maghrebi",  -12.0, 39.6,  0.0, 28.5),
    ("Egyptian",   16.0, 14.5, 29.5, 24.5),
    ("Sudanese",   21.0,  8.0, 30.0, 13.5),
    ("Levantine",  27.0, 41.6, 37.2, 34.6),
    ("Iraqi",      49.5, 41.6, 44.2, 33.2),
    ("Gulf",       55.5, 35.6, 50.0, 24.5),
    ("Yemeni",     55.0,  9.5, 47.0, 14.5),
]

LON = (-18.5, 62.0)
LAT = (6.5, 43.5)


def shapes_by_admin(reader):
    flds = [f[0] for f in reader.fields[1:]]
    i = flds.index("ADMIN")
    out = {}
    for rec, shp in zip(reader.records(), reader.shapes()):
        out.setdefault(rec[i], []).append(shp)
    return out


def visible(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return not (max(xs) < LON[0] or min(xs) > LON[1]
                or max(ys) < LAT[0] or min(ys) > LAT[1])


def draw_country(ax, shapes, **kw):
    for shp in shapes:
        parts = list(shp.parts) + [len(shp.points)]
        for a, b in zip(parts[:-1], parts[1:]):
            ring = shp.points[a:b]
            if len(ring) < 3 or not visible(ring):
                continue
            ax.add_patch(MplPolygon(ring, closed=True, **kw))


def draw(path):
    r = shapefile.Reader(SHP)
    geom = shapes_by_admin(r)

    fig, ax = plt.subplots(figsize=(13.0, 8.3))

    for name in CONTEXT:
        if name in geom:
            draw_country(ax, geom[name], facecolor=CONTEXT_FILL,
                         edgecolor=CONTEXT_EDGE, lw=lws(0.5), zorder=1)

    for label, members, colour, hatch, _feature in GROUPS:
        for name in members:
            if name not in geom:
                print("  ! not found in Natural Earth:", name)
                continue
            draw_country(ax, geom[name], facecolor=colour, edgecolor=BORDER,
                         lw=lws(0.6), hatch=hatch, zorder=2)

    for name, lon, lat, fsz in COUNTRY_LABELS:
        ax.text(lon, lat, name, ha="center", va="center", fontsize=fs(fsz),
                color="#20272F", zorder=5)

    feature_of = {g[0]: g[4] for g in GROUPS}
    for label, tx, ty, ax_, ay in CALLOUTS:
        ax.annotate(
            f"{label}\n{feature_of[label]}",
            xy=(ax_, ay), xytext=(tx, ty),
            ha="center", va="center", fontsize=fs(8.6), color=NAVY,
            linespacing=1.35, zorder=6,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor=NAVY, lw=lws(1.0)),
            arrowprops=dict(arrowstyle="-", color=NAVY, lw=lws(0.9),
                            shrinkA=2, shrinkB=2))

    handles = [Patch(facecolor=c, edgecolor=BORDER, hatch=h, label=lab)
               for lab, _m, c, h, _f in GROUPS]
    handles.append(Patch(facecolor=CONTEXT_FILL, edgecolor=CONTEXT_EDGE,
                         label="not shown as a group here"))
    leg = ax.legend(handles=handles, loc="lower left", ncol=4, frameon=True,
                    fontsize=fs(8.6), handlelength=2.4, handleheight=1.3,
                    borderpad=0.7, columnspacing=1.4,
                    bbox_to_anchor=(0.005, -0.155))
    leg.get_frame().set_edgecolor("#C8CFD9")

    ax.text(0.995, -0.245,
            "Boundaries are gradual dialect zones, not sharp lines.\n"
            "Maghrebi here includes Hassaniya (Mauritania, Western Sahara).\n"
            "Base map: Natural Earth 1:50m, public domain. National boundaries\n"
            "are shown for orientation only and imply no view on legal status.",
            transform=ax.transAxes, ha="right", va="top", fontsize=fs(7.6),
            color="#5A6472", linespacing=1.45)

    ax.set_xlim(*LON)
    ax.set_ylim(*LAT)
    ax.set_aspect(1.0 / math.cos(math.radians(24.0)))
    ax.axis("off")
    fig.tight_layout(pad=0.4)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(path.replace(".png", ".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    plt.rcParams["hatch.linewidth"] = 0.55
    plt.rcParams["hatch.color"] = "#6E7885"
    draw("fig2_7.png")
    print("wrote fig2_7.png/.pdf")
