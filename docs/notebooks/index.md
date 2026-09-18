# Notebooks

The runnable companions the book refers to — one per chapter that has one. Each notebook implements the computations a chapter states in words, so a reader can inspect the exact arithmetic and change it. **The book points here, and nowhere else, for runnable material; no code appears in the chapters themselves.**

!!! success "Runs top to bottom with numpy, scipy and matplotlib only"
    No downloads and no audio files are needed: where a recording is useful the notebook **synthesises** one, and a cell is provided for reading your own WAV file instead. Cells that need extra packages or internet access are marked **Optional** and are commented out.

## The notebooks

| Ch. | Notebook | What it implements | In the book |
|-----|----------|--------------------|-------------|
| 1 | [Word & character error rate](ch01_wer_and_cer.ipynb) | Edit-distance alignment, WER and CER, Arabic normalization switches, per-dialect breakdown, bootstrap comparison | §1.7–1.8; Exercise 2 |
| 2 | [Pronunciation lexicon](ch02_pronunciation_lexicon.ipynb) | Letter/diacritic-to-phone mapping, gemination, the definite article before sun and moon letters, tāʾ marbūṭa in pause and in context, a small lexicon written to file | §2.8 |
| 3 | [Signal to features](ch03_signal_to_features.ipynb) | Sampling & quantization, framing & windowing, the STFT and two spectrogram settings, the mel filterbank, log-mel, the DCT and MFCCs with deltas, linear prediction (Levinson–Durbin) and formants, telephone-band simulation | §3.1, 3.5–3.8 |
| 4 | [HMM forward & Viterbi](ch04_hmm_forward_and_viterbi.ipynb) | A two-state, three-frame HMM: forward algorithm, Viterbi, every path enumerated as a check, the log domain, and a left-to-right model for بَاب | §4.3 |
| 6 | [Self-supervised objectives](ch06_self_supervised_objectives.ipynb) | Span masking, the contrastive InfoNCE objective, product quantization, masked prediction as classification, layer-wise probing, parameter counts for adapters and LoRA | §6.2–6.5 |
| 9 | [Diacritization & G2P](ch09_diacritization_and_g2p.ipynb) | Undiacritized forms and their readings, grapheme-to-phoneme, diacritic error rate with and without the final letter, a disagreement report between two diacritizers, and hooks for CAMeL Tools or Mishkal | §9.2; Exercise 2 |

Chapters 5, 7, 8, 10, and 11 have worked coding exercises in the [Exercise Solutions](../solutions/index.md) rather than a standalone chapter notebook; Chapters 12–14 have neither.

**▶ Open in Google Colab:** [Ch 1](https://colab.research.google.com/github/arabic-speech-book/arabic-speech-book.github.io/blob/main/docs/notebooks/ch01_wer_and_cer.ipynb) · [Ch 2](https://colab.research.google.com/github/arabic-speech-book/arabic-speech-book.github.io/blob/main/docs/notebooks/ch02_pronunciation_lexicon.ipynb) · [Ch 3](https://colab.research.google.com/github/arabic-speech-book/arabic-speech-book.github.io/blob/main/docs/notebooks/ch03_signal_to_features.ipynb) · [Ch 4](https://colab.research.google.com/github/arabic-speech-book/arabic-speech-book.github.io/blob/main/docs/notebooks/ch04_hmm_forward_and_viterbi.ipynb) · [Ch 6](https://colab.research.google.com/github/arabic-speech-book/arabic-speech-book.github.io/blob/main/docs/notebooks/ch06_self_supervised_objectives.ipynb) · [Ch 9](https://colab.research.google.com/github/arabic-speech-book/arabic-speech-book.github.io/blob/main/docs/notebooks/ch09_diacritization_and_g2p.ipynb)

## Running them

=== "Locally"

    ```bash
    pip install -r requirements.txt
    jupyter lab
    ```

    The [pinned requirements file](requirements.txt) needs only `numpy`, `scipy`, and `matplotlib`. The optional block (datasets, soundfile, CAMeL Tools, Mishkal) is commented out — uncomment what an Optional cell needs.

=== "Google Colab"

    Use the **Open in Google Colab** links above to open any notebook directly in Colab (the repository is public, so Colab can load them). Or, from a notebook page, use the **download** icon and, in Colab, choose **File → Upload notebook**.

!!! note "Data"
    No corpus is distributed here. The optional cells point to **Common Voice Arabic** (Chapter 3), downloaded by the reader under its own licence — report the release version and validated-hour count, as Chapter 7 asks.

!!! info "Looking for the earlier set?"
    The larger 12-notebook set from the July/August manuscript revision has been superseded; it is kept for reference under [Earlier drafts](../notebooks-archive/index.md).
