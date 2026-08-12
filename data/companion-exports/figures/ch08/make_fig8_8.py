"""
Figure 8.8: computing macro-F1 from a confusion matrix.

The chapter argues that accuracy alone hides a failure on a rare dialect and
that macro-F1 is the number that exposes it. A box of five numbered steps says
so in words. This figure does the arithmetic on a matrix the reader can see,
so the claim can be audited rather than believed.

Everything on the page is computed from CM. Nothing is placed by hand. Change
one count and the highlighted cells, the readout, the bars, the macro-F1 rule
and the accuracy rule all move together.

LEFT, the matrix. Rows are true labels, columns are predicted labels, and the
counts are illustrative, which the panel says inside the artwork. The class
picked out is the rare one, Gulf, because it is the class the two metrics
disagree about. Its diagonal cell is the true positives; the rest of its
column, read downwards, is the false positives; the rest of its row, read
across, is the false negatives. The three are filled differently and hatched
differently so the grouping survives greyscale printing, and each group is
labelled where it sits rather than through a legend.

RIGHT, the consequence. One bar per class, each the class F1 that follows from
the same matrix, with two vertical rules: macro-F1, the unweighted mean of the
four bars, and accuracy, the diagonal over the total. The gap between the two
rules is the whole argument of Section 8.11. Accuracy sits high because the two
large classes dominate the count; macro-F1 sits low because the Gulf bar counts
for exactly as much as the Modern Standard Arabic one.

The counts are chosen to be imbalanced in the way a real Arabic dialect test
set is imbalanced, 500 / 300 / 150 / 50, and the confusions are concentrated
between Levantine and Gulf, which is the adjacency Figure 8.1 draws. They are
not measurements and the panel says so.
"""
import numpy as np
from matplotlib.patches import Rectangle

from bookstyle import NAVY, ORANGE, GREY, GREEN, WHITE, BOXFILL, GREENFILL, \
    canvas, note, save
from figscale import fs, lws
from figfit import must_fit, report

# ---------------------------------------------------------------------------
# The one thing this figure is made of. Rows are true, columns are predicted.
# ---------------------------------------------------------------------------
CLASSES = ["MSA", "Egyptian", "Levantine", "Gulf"]
CM = np.array([[470,  15,  10,   5],
               [ 20, 255,  20,   5],
               [ 10,  15, 105,  20],
               [  4,   3,  25,  18]], dtype=float)
FOCUS = 3                      # the class whose TP, FP and FN are marked

FPFILL = "#FBE6D6"             # a light tint of ORANGE
FNFILL = BOXFILL               # the book's light navy tint


def metrics(cm):
    tp = np.diag(cm)
    fp = cm.sum(axis=0) - tp
    fn = cm.sum(axis=1) - tp
    with np.errstate(divide="ignore", invalid="ignore"):
        prec = np.where(tp + fp > 0, tp / (tp + fp), 0.0)
        rec = np.where(tp + fn > 0, tp / (tp + fn), 0.0)
        f1 = np.where(prec + rec > 0, 2 * prec * rec / (prec + rec), 0.0)
    return tp, fp, fn, prec, rec, f1


def draw(path_out):
    tp, fp, fn, prec, rec, f1 = metrics(CM)
    macro = float(f1.mean())
    acc = float(np.diag(CM).sum() / CM.sum())

    w, h = 12.6, 6.3
    fig, ax = canvas(w, h, (0, w), (0, h))
    n = len(CLASSES)

    # ================= left panel: the matrix ==============================
    cw, chh = 0.86, 0.68
    gx0, gy0 = 2.30, 4.75           # top-left corner of the first cell

    def cx(j):
        return gx0 + (j + 0.5) * cw

    def cy(i):
        return gy0 - (i + 0.5) * chh

    for i in range(n):
        for j in range(n):
            if i == FOCUS and j == FOCUS:
                fill, edge, hatch = GREENFILL, GREEN, None
            elif j == FOCUS:
                fill, edge, hatch = FPFILL, ORANGE, "//"
            elif i == FOCUS:
                fill, edge, hatch = FNFILL, NAVY, "\\\\\\"
            else:
                fill, edge, hatch = WHITE, "#C9D6E8", None
            ax.add_patch(Rectangle(
                (cx(j) - cw / 2, cy(i) - chh / 2), cw, chh,
                facecolor=fill, edgecolor=edge, lw=lws(1.2), hatch=hatch,
                zorder=3))
            strong = (i == FOCUS or j == FOCUS)
            note(ax, cx(j), cy(i), f"{int(CM[i, j])}", size=9.6,
                 colour=NAVY if strong else GREY,
                 weight="bold" if strong else "normal", z=5)

    for j, name in enumerate(CLASSES):
        t = note(ax, cx(j), gy0 + 0.16, name, size=8.8,
                 colour=NAVY if j == FOCUS else GREY,
                 weight="bold" if j == FOCUS else "normal",
                 rotation=28, ha="left", va="bottom", z=5)
        must_fit(fig, t, 1.10, f"column heading {name}")
    note(ax, gx0 + n * cw / 2, gy0 + 0.95, "predicted", size=9.6, colour=NAVY,
         weight="bold", z=5)

    for i, name in enumerate(CLASSES):
        t = note(ax, gx0 - 0.16, cy(i), name, size=8.8,
                 colour=NAVY if i == FOCUS else GREY,
                 weight="bold" if i == FOCUS else "normal", ha="right", z=5)
        must_fit(fig, t, gx0 - 0.40, f"row heading {name}")
    note(ax, gx0 - 1.48, gy0 - n * chh / 2, "true", size=9.6, colour=NAVY,
         weight="bold", rotation=90, z=5)

    # the three groups, each labelled where it sits
    note(ax, cx(FOCUS) + cw / 2 + 0.14, cy(FOCUS), "TP", size=9.8,
         colour=GREEN, weight="bold", ha="left", z=6)
    ax.plot([cx(FOCUS) + cw / 2 + 0.07] * 2,
            [cy(0) + chh / 2, cy(FOCUS - 1) - chh / 2],
            color=ORANGE, lw=lws(1.6), zorder=6)
    note(ax, cx(FOCUS) + cw / 2 + 0.18, (cy(0) + cy(FOCUS - 1)) / 2,
         "FP", size=9.8, colour=ORANGE, weight="bold", ha="left", z=6)
    fn_rule = cy(FOCUS) - chh / 2 - 0.08
    ax.plot([cx(0) - cw / 2, cx(FOCUS - 1) + cw / 2], [fn_rule] * 2,
            color=NAVY, lw=lws(1.6), zorder=6)
    note(ax, (cx(0) + cx(FOCUS - 1)) / 2, fn_rule - 0.26, "FN", size=9.8,
         colour=NAVY, weight="bold", z=6)

    # the readout for the marked class, computed from the same matrix
    k, rx = FOCUS, 0.95
    note(ax, rx, 1.24, CLASSES[k], size=9.6, colour=NAVY, weight="bold",
         ha="left", z=5)
    for dx, (label, colour) in zip(
            (1.05, 2.32, 3.59),
            ((f"TP {int(tp[k])}", GREEN), (f"FP {int(fp[k])}", ORANGE),
             (f"FN {int(fn[k])}", NAVY))):
        t = note(ax, rx + dx, 1.24, label, size=9.6, colour=colour,
                 weight="bold", ha="left", z=5)
        must_fit(fig, t, 1.15, label)
    t = note(ax, rx, 0.72,
             f"precision {prec[k]:.2f}     recall {rec[k]:.2f}     "
             f"F1 {f1[k]:.2f}", size=9.6, colour=GREY, ha="left", z=5)
    must_fit(fig, t, 4.90, "readout line")
    note(ax, gx0 + n * cw, 0.22, "illustrative counts", size=9.8, colour=GREY,
         style="italic", ha="right", z=5)

    # ================= right panel: what it adds up to =====================
    bx0, bw_ = 7.60, 4.05
    btop, bgap = 4.55, 0.80
    for i, name in enumerate(CLASSES):
        y = btop - i * bgap
        colour = ORANGE if i == FOCUS else NAVY
        ax.add_patch(Rectangle((bx0, y - 0.23), bw_ * f1[i], 0.46,
                               facecolor=colour, edgecolor=colour,
                               lw=lws(0.9), zorder=4))
        t = note(ax, bx0 - 0.14, y, name, size=8.8, colour=colour,
                 weight="bold" if i == FOCUS else "normal", ha="right", z=5)
        must_fit(fig, t, 1.30, f"bar label {name}")
        # inside the bar where there is room, outside where there is not
        if f1[i] > 0.45:
            note(ax, bx0 + bw_ * f1[i] - 0.12, y, f"{f1[i]:.2f}", size=9.2,
                 colour=WHITE, weight="bold", ha="right", z=6)
        else:
            note(ax, bx0 + bw_ * f1[i] + 0.12, y, f"{f1[i]:.2f}", size=9.2,
                 colour=colour, weight="bold", ha="left", z=6)

    axis_y = btop - (n - 1) * bgap - 0.55
    ax.plot([bx0, bx0 + bw_], [axis_y] * 2, color=GREY, lw=lws(1.1), zorder=3)
    for v in (0.0, 0.5, 1.0):
        ax.plot([bx0 + bw_ * v] * 2, [axis_y, axis_y - 0.09], color=GREY,
                lw=lws(1.1), zorder=3)
        note(ax, bx0 + bw_ * v, axis_y - 0.28, f"{v:.1f}", size=8.8,
             colour=GREY, z=5)
    note(ax, bx0 + bw_ / 2, axis_y - 0.66, "class F1", size=9.6, colour=GREY,
         z=5)

    # each rule stops at its own label, so no legend is needed
    for value, label, colour, dash, top in (
            (macro, f"macro-F1  {macro:.2f}", GREEN, (0, (5, 3)), 4.98),
            (acc, f"accuracy  {acc:.2f}", GREY, (0, (1.6, 2.2)), 5.42)):
        px = bx0 + bw_ * value
        ax.plot([px, px], [axis_y, top], color=colour, lw=lws(1.6),
                linestyle=dash, zorder=2)
        t = note(ax, px + 0.10, top + 0.19, label, size=9.6, colour=colour,
                 weight="bold", ha="right", z=6)
        must_fit(fig, t, 2.40, label)

    for x, text in ((gx0 + n * cw / 2, "confusion matrix"),
                    (bx0 + bw_ / 2, "per-class F1")):
        t = note(ax, x, 6.05, text, size=10.6, colour=NAVY, weight="bold", z=5)
        must_fit(fig, t, 4.60, text)

    report()
    save(fig, path_out)
    print(f"  accuracy {acc:.4f}   macro-F1 {macro:.4f}")
    for i, name in enumerate(CLASSES):
        print(f"  {name:<10} TP {tp[i]:6.0f}  FP {fp[i]:5.0f}  "
              f"FN {fn[i]:5.0f}  P {prec[i]:.4f}  R {rec[i]:.4f}  "
              f"F1 {f1[i]:.4f}")


if __name__ == "__main__":
    draw("fig8_8.png")
