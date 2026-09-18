"""
Code-drawn vector figures for Chapter 1 of *Introduction to Arabic Speech Technologies*.

Figure 1.1  Timeline of speech processing with Arabic milestones.
Figure 1.2  How a spoken request becomes an action.

Both figures are drawn deterministically from the data structures below. No
image-generation model is involved. Both are designed to survive grayscale
printing: every distinction carried by colour is also carried by marker shape,
line style, or fill pattern.

Requires: matplotlib, arabic_reshaper, python-bidi, Noto Naskh Arabic.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.font_manager import FontProperties
import arabic_reshaper
from bidi.algorithm import get_display

# ----------------------------------------------------------------------------
# Shared style
# ----------------------------------------------------------------------------
NAVY = "#1F3864"
ORANGE = "#C55A11"
LIGHT = "#EAF0F8"
GREY = "#4D4D4D"

AR_FONT = FontProperties(fname="/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf")

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["svg.fonttype"] = "path"
plt.rcParams["pdf.fonttype"] = 42


def ar(text):
    """Shape and reorder Arabic text for correct rendering in matplotlib."""
    return get_display(arabic_reshaper.reshape(text))


# ============================================================================
# Figure 1.1  Timeline
# ============================================================================
# (date label, event label, track)  track: "general" or "arabic"
# Era spans below match Table 1.2 exactly.
MILESTONES = [
    ("1930s",     "analog vocoder",                    "general"),
    ("1950s",     "isolated-digit\nrecognizers",       "general"),
    ("1970s",     "dynamic time\nwarping",             "general"),
    ("1980s-\n2000s", "HMM-GMM\nsystems",              "general"),
    ("1985",      "real-time spoken\nArabic digit recognizer", "arabic"),
    ("1990",      "doctoral research on\nArabic recognition", "arabic"),
    ("1991",      "Arabic synthesis\nrules at KFUPM",  "arabic"),
    ("2000-2003", "KACST Arabic phonetics\ndatabase and SAAVB", "arabic"),
    ("2002-2011", "DARPA EARS/GALE\nArabic broadcast", "arabic"),
    ("2012",      "deep neural network\nacoustic models", "general"),
    ("2014-\n2020", "end-to-end models\n(CTC, attention, RNN-T)", "general"),
    ("2016",      "MGB-2\nchallenge",                  "arabic"),
    ("2017",      "Transformer;\nMGB-3",               "general"),
    ("2019",      "MGB-5 and\nADI17",                  "arabic"),
    ("2020",      "wav2vec 2.0,\nConformer; first NADI", "general"),
    ("2021",      "HuBERT;\nQASR corpus",              "general"),
    ("2022",      "Whisper",                           "general"),
    ("2023",      "massively multilingual\nmodels; ArTST", "general"),
    ("2024-2025", "audio-language models;\nopen Arabic ASR leaderboards", "arabic"),
]


def figure_1_1(path):
    """Two-band timeline. Splitting the axis keeps the aspect ratio close to 3:2,
    so the figure stays legible at Springer's 6.5-inch text width."""
    bands = [MILESTONES[:10], MILESTONES[10:]]
    fig, axes = plt.subplots(2, 1, figsize=(11.0, 5.9))

    for ax, band in zip(axes, bands):
        n = len(band)
        ax.plot([-0.55, n - 0.45], [0, 0], color=NAVY, lw=2.6, zorder=1,
                solid_capstyle="round")
        for i, (date, label, track) in enumerate(band):
            above = (i % 2 == 0)
            y_stem = 0.40 if above else -0.40
            y_text = 0.52 if above else -0.52
            va = "bottom" if above else "top"
            if track == "arabic":
                colour, marker, fill, edge = ORANGE, "s", ORANGE, ORANGE
            else:
                colour, marker, fill, edge = NAVY, "o", "white", NAVY
            ax.plot([i, i], [0, y_stem], color=colour, lw=1.3, zorder=2)
            ax.scatter([i], [0], marker=marker, s=190, facecolors=fill,
                       edgecolors=edge, linewidths=2.0, zorder=3)
            ax.text(i, y_text, label, ha="center", va=va, fontsize=9.4,
                    color=colour, linespacing=1.35)
            ax.text(i, -0.14 if above else 0.14, date, ha="center",
                    va="top" if above else "bottom", fontsize=9.2,
                    color=GREY, linespacing=1.25)
        ax.set_xlim(-0.9, n - 0.1)
        ax.set_ylim(-1.05, 1.05)
        ax.axis("off")

    # Legend below the lower band, encoded by shape as well as colour
    ax = axes[1]
    ax.scatter([-0.55], [-1.42], marker="o", s=190, facecolors="white",
               edgecolors=NAVY, linewidths=2.0, clip_on=False)
    ax.text(-0.15, -1.42, "general speech technology (open circle)",
            fontsize=10, va="center", color=NAVY)
    ax.scatter([3.55], [-1.42], marker="s", s=190, facecolors=ORANGE,
               edgecolors=ORANGE, linewidths=2.0, clip_on=False)
    ax.text(3.95, -1.42, "Arabic milestone (filled square)",
            fontsize=10, va="center", color=ORANGE)

    fig.subplots_adjust(hspace=0.10, top=0.99, bottom=0.13, left=0.02, right=0.98)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(path.replace(".png", ".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ============================================================================
# Figure 1.2  Spoken request pipeline
# ============================================================================
# Light fills with dark text: legible in print, in grayscale, and on screen.
STAGES = [
    ("1. Microphone /\nspoken request", ""),
    ("2. Front end:\nfeature extraction", "waveform to\nlog-mel features"),
    ("3. Automatic speech\nrecognition (ASR)", "audio to text"),
    ("4. Spoken language\nunderstanding", "intent and slots"),
    ("5. Dialogue manager /\naction", "decide and act"),
    ("6. Text-to-speech\nresponse", ""),
]

# The utterance is the DIALECTAL one from the opening scene of Section 1.1.
UTTERANCE_AR = "وين أقرب محطة بنزين؟"
UTTERANCE_TR = "wēn aqrab maḥaṭṭat banzīn"
UTTERANCE_EN = "where is the nearest gas station?"

BOX_FILL = "#DCE6F4"
BAND_FILL = "#F4F7FC"


def figure_1_2(path):
    fig, ax = plt.subplots(figsize=(13.6, 7.4))

    ax.add_patch(FancyBboxPatch((1.15, 4.3), 12.6, 2.3,
                                boxstyle="round,pad=0.12,rounding_size=0.18",
                                facecolor=BAND_FILL, edgecolor="#C9D6E8",
                                lw=1.0, zorder=0))

    w, h, gap = 1.86, 1.72, 0.24
    x0 = 1.37
    centres = []
    for i, (title, sub) in enumerate(STAGES):
        x = x0 + i * (w + gap)
        centres.append(x + w / 2)
        ax.add_patch(FancyBboxPatch((x, 4.6), w, h,
                                    boxstyle="round,pad=0.06,rounding_size=0.14",
                                    facecolor=BOX_FILL, edgecolor=NAVY,
                                    lw=1.4, zorder=2))
        ty = 4.6 + h * (0.68 if sub else 0.50)
        ax.text(x + w / 2, ty, title, ha="center", va="center",
                fontsize=10.4, color=NAVY, weight="bold",
                linespacing=1.35, zorder=3)
        if sub:
            ax.text(x + w / 2, 4.6 + h * 0.28, sub, ha="center", va="center",
                    fontsize=9.6, color="#2C3E56", linespacing=1.3, zorder=3)
        if i < len(STAGES) - 1:
            ax.annotate("", xy=(x + w + gap - 0.02, 4.6 + h / 2),
                        xytext=(x + w + 0.02, 4.6 + h / 2),
                        arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.6,
                                        mutation_scale=16), zorder=4)

    def bubble(cx, top_y, ar_text, tr_text, en_text, tag, direction):
        """direction 'in': arrow points up into the box (this is what goes in).
           direction 'out': arrow points down out of the box (this is what comes out)."""
        bw, bh = 2.85, 0.74
        bx, by = cx - bw / 2, top_y - bh
        ax.add_patch(FancyBboxPatch((bx, by), bw, bh,
                                    boxstyle="round,pad=0.06,rounding_size=0.14",
                                    facecolor="white", edgecolor=NAVY, lw=1.5, zorder=3))
        ax.text(cx, by + bh / 2, ar(ar_text), ha="center", va="center",
                fontsize=15, fontproperties=AR_FONT, color="#111111", zorder=4)
        ax.text(cx, by - 0.30, tr_text, ha="center", va="center",
                fontsize=9.8, color=GREY, style="italic")
        ax.text(cx, by - 0.60, en_text, ha="center", va="center",
                fontsize=9.8, color=GREY)
        if direction == "in":
            ax.annotate("", xy=(cx, 4.55), xytext=(cx, top_y + 0.05),
                        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.5,
                                        mutation_scale=14), zorder=3)
        else:
            ax.annotate("", xy=(cx, top_y + 0.05), xytext=(cx, 4.55),
                        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.5,
                                        mutation_scale=14), zorder=3)
        ax.text(cx + 0.12, (4.55 + top_y) / 2 + 0.04, tag, ha="left", va="center",
                fontsize=9.4, color=NAVY, weight="bold")

    # What she says goes IN at the microphone; what the recognizer returns comes OUT of box 3.
    bubble(centres[0], 3.98, UTTERANCE_AR, UTTERANCE_TR, UTTERANCE_EN,
           "spoken input", "in")
    bubble(centres[2], 3.98, UTTERANCE_AR, UTTERANCE_TR, UTTERANCE_EN,
           "recognized text", "out")

    # Spoken reply, dashed return path
    ax.add_patch(FancyArrowPatch((centres[5], 4.55), (centres[5], 2.00),
                                 arrowstyle="-", linestyle=(0, (5, 4)),
                                 color=NAVY, lw=1.6, zorder=1))
    ax.add_patch(FancyArrowPatch((centres[5], 2.00), (centres[0] - 0.02, 2.00),
                                 arrowstyle="-", linestyle=(0, (5, 4)),
                                 color=NAVY, lw=1.6, zorder=1))
    ax.add_patch(FancyArrowPatch((centres[0] - 0.02, 2.00), (centres[0] - 0.02, 2.66),
                                 arrowstyle="-|>", linestyle=(0, (5, 4)),
                                 color=NAVY, lw=1.6, mutation_scale=13, zorder=1))
    ax.text((centres[0] + centres[5]) / 2, 2.10, "spoken reply", ha="center",
            va="bottom", fontsize=10, color=NAVY, weight="bold")

    ax.set_xlim(0.15, 14.0)
    ax.set_ylim(1.55, 7.05)
    ax.axis("off")
    fig.tight_layout(pad=0.3)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(path.replace(".png", ".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    figure_1_1("fig1_1.png")
    figure_1_2("fig1_2.png")
    print("wrote fig1_1.png/.pdf and fig1_2.png/.pdf")
