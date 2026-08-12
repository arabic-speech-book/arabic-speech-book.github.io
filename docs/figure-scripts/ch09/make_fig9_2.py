"""
Figure 9.2: the Arabic front end.

The chapter's opening scene is one spelling with three readings, and this is
that scene drawn. The bare letters على... no: the bare letters are ﻋﻠﻢ, and the
figure shows diacritization choosing between the three words they can spell,
then grapheme-to-phoneme turning the chosen one into phonemes.

Three rules from the book apply here and all three are followed.

  Arabic and Latin never share a text call, because the Arabic face has no
  Latin glyphs and a stray bracket or italic word prints as an empty box. Each
  Arabic word, each transliteration and each gloss is a separate call.

  matplotlib does no mark positioning, so vocalised Arabic is drawn letter by
  letter with arabtext.draw_word, which places each harakat over or under its
  own base letter. The undiacritized form has no marks and is drawn normally.

  No sentences inside the artwork. What the branch means is in the caption.

The three readings and their phoneme strings are the data of this figure and
sit at the top of the script.
"""
from matplotlib.patches import FancyBboxPatch

from bookstyle import (NAVY, ORANGE, GREEN, GREENFILL, WHITE, BOXFILL, GREY,
                       ARF, canvas, box, note, arrow, save, ar)
from figscale import fs, lws
from figfit import must_fit, report
import arabtext

BARE = "علم"
READINGS = [
    ("عِلْم", "ʿilm", "knowledge", "/ʕ i l m/"),
    ("عَلَم", "ʿalam", "flag", "/ʕ a l a m/"),
    ("عَلَّمَ", "ʿallama", "he taught", "/ʕ a l l a m a/"),
]

BW, BH = 2.05, 1.02


def draw(path_out):
    w, h = 12.6, 5.4
    fig, ax = canvas(w, h, (0, w), (0, h))
    fig.canvas.draw()

    x_in, x_dia, x_read, x_g2p, x_out = 1.15, 3.35, 6.45, 9.35, 11.45
    ys = [4.25, 2.90, 1.55]
    ymid = ys[1]

    # ---- the undiacritized input ----------------------------------------
    box(ax, x_in, ymid, BW, BH, fill=BOXFILL, edge=NAVY, lw=1.5, r=0.12)
    ax.text(x_in, ymid + 0.10, ar(BARE), fontproperties=ARF,
            fontsize=fs(15.0), color=NAVY, ha="center", va="center", zorder=5)
    t = note(ax, x_in, ymid - BH / 2 - 0.30, "undiacritized", size=9.2,
             colour=GREY)
    must_fit(fig, t, BW + 0.5, "undiacritized")

    # ---- the diacritization step ----------------------------------------
    box(ax, x_dia, ymid, BW, BH, fill=WHITE, edge=NAVY, lw=1.5, r=0.12)
    t = note(ax, x_dia, ymid, "diacritization", size=10.2, colour=NAVY,
             weight="bold")
    must_fit(fig, t, BW - 0.14, "diacritization")
    t = note(ax, x_dia, ymid - BH / 2 - 0.30, "restore short vowels",
             size=9.2, colour=GREY)
    must_fit(fig, t, BW + 0.95, "restore short vowels")
    arrow(ax, (x_in + BW / 2 + 0.04, ymid), (x_dia - BW / 2 - 0.04, ymid))

    # ---- the three readings, each its own row ---------------------------
    for y, (word, translit, gloss, phones) in zip(ys, READINGS):
        chosen = (y == ymid)
        edge = ORANGE if chosen else GREY
        ax.add_patch(FancyBboxPatch(
            (x_read - 1.30, y - 0.42), 2.60, 0.84,
            boxstyle="round,pad=0.01,rounding_size=0.12",
            facecolor=WHITE, edgecolor=edge, lw=lws(1.5), zorder=3))
        arabtext.draw_word(ax, x_read - 0.62, y - 0.02, word, ARF,
                           fs(13.0), NAVY if chosen else GREY, ha="center",
                           zorder=5)
        t = note(ax, x_read + 0.62, y + 0.14, translit, size=9.2,
                 colour=NAVY if chosen else GREY, style="italic")
        must_fit(fig, t, 1.20, translit)
        t = note(ax, x_read + 0.62, y - 0.20, gloss, size=8.8, colour=GREY)
        must_fit(fig, t, 1.20, gloss)
        arrow(ax, (x_dia + BW / 2 + 0.04, ymid), (x_read - 1.34, y),
              colour=edge if chosen else GREY, lw=1.7 if chosen else 1.2)

    note(ax, x_read, ys[0] + 0.62, "three readings", size=9.6, colour=GREY)

    # ---- grapheme-to-phoneme and the phoneme string ---------------------
    box(ax, x_g2p, ymid, BW, BH, fill=WHITE, edge=NAVY, lw=1.5, r=0.12)
    t = note(ax, x_g2p, ymid, "grapheme-to-\nphoneme", size=10.2, colour=NAVY,
             weight="bold", linespacing=1.45)
    must_fit(fig, t, BW - 0.10, "grapheme-to-")
    arrow(ax, (x_read + 1.34, ymid), (x_g2p - BW / 2 - 0.04, ymid),
          colour=ORANGE, lw=1.7)

    box(ax, x_out, ymid, 1.90, BH, fill=GREENFILL, edge=GREEN, lw=1.5, r=0.12)
    t = note(ax, x_out, ymid, READINGS[1][3], size=9.8, colour=GREEN,
             weight="bold")
    must_fit(fig, t, 1.80, READINGS[1][3])
    arrow(ax, (x_g2p + BW / 2 + 0.04, ymid), (x_out - 0.99, ymid),
          colour=ORANGE, lw=1.7)
    t = note(ax, x_out, ymid - BH / 2 - 0.30, "phonemes", size=9.2,
             colour=GREY)
    must_fit(fig, t, 1.90, "phonemes")

    report()
    save(fig, path_out)


if __name__ == "__main__":
    draw("fig9_2.png")
