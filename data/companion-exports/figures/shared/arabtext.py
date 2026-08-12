"""
Helper for drawing vocalised Arabic in matplotlib figures with per-letter
control of colour and weight.

matplotlib has no OpenType shaping engine: it lays glyphs out by advance width
and applies no mark positioning, so a vocalised Arabic string drawn as one text
object puts every harakat in the wrong place. This module works around that.

  1. arabic_reshaper selects the contextual presentation form of each letter,
     which is what a shaping engine would have chosen.
  2. The reshaped string is split into clusters, each a base letter plus the
     combining marks that belong to it, and the cluster order is reversed so
     that the visual order runs left to right, as matplotlib draws.
  3. Base letters are drawn one at a time at cumulative advance-width offsets.
     Because the presentation forms already carry their joining strokes, the
     result is indistinguishable from drawing the string in one call, but each
     letter can now take its own colour.
  4. Each harakat is drawn separately, centred on its own base letter, above or
     below the baseline according to the mark.

Every glyph therefore comes from the Unicode text and the standard shaping
rules, not from hand-placed artwork.
"""
import unicodedata

import arabic_reshaper
from matplotlib.transforms import offset_copy

_RESHAPER = arabic_reshaper.ArabicReshaper(
    configuration={"delete_harakat": False})

# marks drawn below the base letter; everything else goes above
_BELOW = {"ِ", "ٍ"}          # kasra, kasratan
_MARKS_ABOVE_DY = 0.40                 # in units of fontsize, points
_MARKS_BELOW_DY = -0.36


def clusters(word):
    """[(base_presentation_form, marks, base_letter)] in visual order."""
    shaped = _RESHAPER.reshape(word)
    out = []
    for ch in shaped:
        if unicodedata.combining(ch) and out:
            out[-1][1] += ch
        else:
            base = unicodedata.normalize("NFKD", ch)[0]
            out.append([ch, "", base])
    return [tuple(c) for c in reversed(out)]


def measure(renderer, prop, s):
    if not s:
        return 0.0
    w, _h, _d = renderer.get_text_width_height_descent(s, prop, False)
    return w


def draw_word(ax, x, y, word, prop, fontsize, colour,
              weight_of=None, ha="left", mark_colour=None, zorder=4):
    """Draw `word` with the left edge at data coordinate x (ha='left'),
    centred on x (ha='center') or ending at x (ha='right').

    colour: either a colour string, or a callable base_letter -> colour.
    Returns [(base_letter, x_left, x_right)] in data coordinates, so the caller
    can underline or highlight individual letters.
    """
    fig = ax.figure
    renderer = fig.canvas.get_renderer()
    cl = clusters(word)

    prop = prop.copy()
    prop.set_size(fontsize)

    bases = [c[0] for c in cl]
    widths = [measure(renderer, prop, "".join(bases[:i + 1]))
              - measure(renderer, prop, "".join(bases[:i]))
              for i in range(len(bases))]
    total = measure(renderer, prop, "".join(bases))

    inv = ax.transData.inverted()
    origin_disp = ax.transData.transform((x, y))
    if ha == "center":
        x_disp = origin_disp[0] - total / 2.0
    elif ha == "right":
        x_disp = origin_disp[0] - total
    else:
        x_disp = origin_disp[0]

    def col(base):
        return colour(base) if callable(colour) else colour

    run = 0.0
    spans = []
    for (form, marks, base), w in zip(cl, widths):
        xd = x_disp + run
        xdata, _ = inv.transform((xd, origin_disp[1]))
        xdata_r, _ = inv.transform((xd + w, origin_disp[1]))
        spans.append((base, xdata, xdata_r))
        kw = {}
        if weight_of is not None:
            kw["weight"] = weight_of(base)
        ax.text(xdata, y, form, fontproperties=prop, fontsize=fontsize,
                color=col(base), ha="left", va="baseline", zorder=zorder, **kw)

        if marks:
            xcd, _ = inv.transform((xd + w / 2.0, origin_disp[1]))
            for m in marks:
                dy = (_MARKS_BELOW_DY if m in _BELOW else _MARKS_ABOVE_DY)
                tr = offset_copy(ax.transData, fig=fig,
                                 x=0, y=dy * fontsize, units="points")
                ax.text(xcd, y, m, fontproperties=prop, fontsize=fontsize,
                        color=mark_colour or col(base), ha="center",
                        va="baseline", transform=tr, zorder=zorder + 1)
        run += w
    return spans
