# About the Book

**Introduction to Arabic Speech Technologies**, by **[Prof. Hend S. Al-Khalifa](https://faculty.ksu.edu.sa/ar/hendk)**, bridges traditional speech-processing methods with modern AI approaches to address the unique challenges of Arabic — its rich morphology, dialectal variation, and frequent code-switching. It serves researchers, graduate students, and industry practitioners with a unified framework for understanding and building Arabic speech technologies, from classical statistical methods to speech foundation models and audio-language models.

## What makes it different

- **Theory + practice** — each chapter that has a computation ships a runnable [notebook](notebooks/index.md).
- **Arabic-first** — linguistics, datasets, and evaluation are framed around Arabic, not bolted on.
- **Honest evaluation** — results are reported **per dialect**, and the book insists a pooled Arabic number can hide a whole variety failing.
- **Reproducible** — every notebook ends with a *provenance cell* recording the corpus, model revision, normalization, and date behind any number it produces.

## Notebooks by chapter

The notebooks live on this site rather than in the printed pages. Six notebooks accompany the chapters whose work is a computation; the others are projects rather than computations. Worked coding exercises live under [Exercise Solutions](solutions/index.md).

| Ch. | Notebook | What it implements |
|-----|----------|--------------------|
| 1 | [Word & character error rate](notebooks/ch01_wer_and_cer.ipynb) | Edit-distance alignment, WER and CER, Arabic normalization switches, per-dialect breakdown, bootstrap comparison |
| 2 | [Pronunciation lexicon](notebooks/ch02_pronunciation_lexicon.ipynb) | Letter/diacritic-to-phone mapping, gemination, the definite article, tāʾ marbūṭa, a small lexicon written to file |
| 3 | [Signal to features](notebooks/ch03_signal_to_features.ipynb) | Sampling, framing, the STFT and spectrograms, the mel filterbank, log-mel, MFCCs with deltas, LPC and formants |
| 4 | [HMM forward & Viterbi](notebooks/ch04_hmm_forward_and_viterbi.ipynb) | A two-state, three-frame HMM: forward algorithm, Viterbi, every path enumerated, the log domain |
| 6 | [Self-supervised objectives](notebooks/ch06_self_supervised_objectives.ipynb) | Span masking, InfoNCE, product quantization, masked prediction, layer-wise probing, adapter/LoRA parameter counts |
| 9 | [Diacritization & G2P](notebooks/ch09_diacritization_and_g2p.ipynb) | Undiacritized forms and their readings, grapheme-to-phoneme, diacritic error rate, a two-diacritizer disagreement report |

## Citing the book

> Al-Khalifa, H. S. *Introduction to Arabic Speech Technologies.* (forthcoming).

*(Update this entry with the final publisher, year, and DOI once available.)*
