"""
Type and rule sizes for figures that will be reproduced at about half their
design width.

The chapter places its figures in a 6.5 in text column. The generator scripts
draw at roughly 13 in wide, so everything on the page is reduced by about a
half: a 9 pt label in the script prints at about 4.5 pt, which is below what
Springer accepts and below what the author's own artwork used (her labels
measure about 7 to 8.5 pt at final size).

These helpers apply the reduction in advance. fs() scales a point size and
refuses to return anything that would print below 7 pt; lws() does the same for
rule widths against a 0.7 pt floor, which is Springer's minimum.
"""

REPRO = 0.5          # printed width divided by design width
MIN_PT = 7.0         # smallest lettering we are willing to print
MIN_RULE_PT = 0.7    # Springer's minimum rule width

SCALE = 1.7


def configure(scale=None, min_pt=None):
    """Override the defaults for one figure.

    Dense figures, such as a nine-column IPA table, cannot carry 7 pt type at
    final size without the columns colliding. Those may drop to the 6 pt floor
    that Springer allows, but they have to say so by calling this.
    """
    global SCALE, MIN_PT
    if scale is not None:
        SCALE = scale
    if min_pt is not None:
        MIN_PT = min_pt


def fs(v):
    """Scale a font size, with a floor set by MIN_PT at final size."""
    return max(v * SCALE, MIN_PT / REPRO)


def lws(v):
    """Scale a rule width, with a floor set by MIN_RULE_PT at final size."""
    return max(v * SCALE, MIN_RULE_PT / REPRO)


def ms(v):
    """Scale a scatter marker area (which goes as the square of a length)."""
    return v * SCALE ** 2


def arr(v):
    """Scale an arrowhead mutation_scale."""
    return v * SCALE
