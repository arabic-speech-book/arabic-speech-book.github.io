"""Shared drawing helpers for the book's figures.

The chapter's original artwork was drawn about 2200 px wide and reproduced at
6.3 in, which put its lettering at roughly 3 to 6 pt on the printed page. That
is below Springer's 7 pt floor and below the type size used in Chapters 2 and
3. These figures are redrawn at the same design width the earlier chapters
use, with figscale applying the reduction in advance, and with the artwork
cropped to its content so no page height is spent on blank canvas.

The content of each figure is unchanged except where noted in the individual
scripts.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.font_manager import FontProperties

from figscale import fs, lws, arr

NAVY = "#1F3864"
ORANGE = "#C55A11"
GREY = "#5A6472"
GREEN = "#1E7B34"
BOXFILL = "#EAF1FA"
WHITE = "#FFFFFF"
GREENFILL = "#E6F0DC"
EDGE_LIGHT = "#C9D6E8"

ARF = FontProperties(
    fname="/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf")


def canvas(w_in, h_in, xlim, ylim):
    """A figure whose axes fills it edge to edge.

    With matplotlib's default margins the axes is only about three quarters of
    the figure wide, so a box sized in data units comes out a quarter narrower
    than the arithmetic says and long labels overflow. Filling the figure keeps
    the design width honest: one data unit is figure width divided by the x
    range, and nothing else.
    """
    fig = plt.figure(figsize=(w_in, h_in))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def box(ax, cx, cy, w, h, fill=WHITE, edge=NAVY, lw=1.6, r=0.16, z=3, ls="solid"):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad=0.01,rounding_size={r}",
        facecolor=fill, edgecolor=edge, lw=lws(lw), linestyle=ls, zorder=z))


def title_in(ax, cx, cy, text, size=12.0, colour=NAVY, weight="bold", z=5, **kw):
    return ax.text(cx, cy, text, ha="center", va="center", fontsize=fs(size),
                   color=colour, weight=weight, zorder=z, **kw)


def note(ax, x, y, text, size=9.0, colour=GREY, ha="center", va="center",
         style="normal", z=5, **kw):
    return ax.text(x, y, text, ha=ha, va=va, fontsize=fs(size), color=colour,
                   style=style, zorder=z, **kw)


def arrow(ax, p0, p1, colour=ORANGE, lw=1.9, scale=15, z=4, style="-|>"):
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, color=colour, lw=lws(lw),
                                mutation_scale=arr(scale),
                                shrinkA=0, shrinkB=0), zorder=z)


def save(fig, path):
    fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.06,
                facecolor="white")
    fig.savefig(path.replace(".png", ".pdf"), bbox_inches="tight",
                pad_inches=0.06, facecolor="white")
    plt.close(fig)
    print("wrote", path)


# --- Arabic ----------------------------------------------------------------
# matplotlib performs no shaping, so the presentation forms are selected with
# arabic_reshaper and the visual order is produced by the bidi algorithm before
# the string is handed to a single text call. Words without vowel marks need
# nothing more than this; vocalised words are drawn letter by letter instead
# (see arabtext.py).
import arabic_reshaper                                     # noqa: E402
from bidi.algorithm import get_display                     # noqa: E402

_RESHAPER = arabic_reshaper.ArabicReshaper(
    configuration={"delete_harakat": False})


def ar(s):
    """Arabic text laid out for a renderer that does no shaping."""
    return get_display(_RESHAPER.reshape(s))
