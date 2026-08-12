# About the Book

**Introduction to Arabic Speech Technologies**, by **Hend S. Al-Khalifa**, bridges traditional speech-processing methods with modern AI approaches to address the unique challenges of Arabic — its rich morphology, dialectal variation, and frequent code-switching. It serves researchers, graduate students, and industry practitioners with a unified framework for understanding and building Arabic speech technologies, from classical statistical methods to speech foundation models and audio-language models.

## What makes it different

- **Theory + practice** — each chapter that has a computation ships a runnable [notebook](notebooks/index.md).
- **Arabic-first** — linguistics, datasets, and evaluation are framed around Arabic, not bolted on.
- **Honest evaluation** — results are reported **per dialect**, and the book insists a pooled Arabic number can hide a whole variety failing.
- **Reproducible** — every notebook ends with a *provenance cell* recording the corpus, model revision, normalization, and date behind any number it produces.

## Notebooks by chapter

The notebooks live on this site rather than in the printed pages. Twelve notebooks cover eleven chapters (Chapter 8 has two); Chapters 12, 13, and 14 have none — their work is a project rather than a computation.

| Ch. | Notebook | What it does |
|-----|----------|--------------|
| 1 | [First contact with Arabic ASR](notebooks/ch01_first_contact_arabic_asr.ipynb) | Score a recognizer on Arabic, then watch normalization move the number; MSA vs dialect |
| 2 | [Phonetics & G2P](notebooks/ch02_arabic_phonetics_g2p.ipynb) | Rule-based grapheme-to-phoneme for diacritized MSA, scored by phone error rate; emphasis and the second formant |
| 3 | [Speech features](notebooks/ch03_speech_features.ipynb) | Framing, spectrograms, mel filterbank, MFCCs, SpecAugment, LPC — written out, not called; exercises as code |
| 4 | [Arabic ASR foundations](notebooks/ch04_arabic_asr_foundations.ipynb) | WER/CER with and without normalization, four tokenizations, the forward algorithm, continuation counts |
| 5 | [End-to-end ASR by hand](notebooks/ch05_end_to_end_arabic_asr.ipynb) | CTC alignments and forward sum, a transducer walk, beam search with shallow fusion, output-unit choice |
| 6 | [Foundation models: full vs LoRA](notebooks/ch06_arabic_foundation_models.ipynb) | Full fine-tuning vs low-rank adaptation: a cost model that runs anywhere, plus a real GPU run |
| 7 | [Corpus loader & audit](notebooks/ch07_corpus_loader.ipynb) | Two corpora into one schema, the audit behind a corpus choice, speaker overlap, Fleiss' kappa |
| 8 | [Dialect ID](notebooks/ch08_dialect_id.ipynb) | Dialect classifier on self-supervised embeddings, accuracy vs macro-F1, confusion matrix, spoken-document search |
| 8 | [Speaker & noise](notebooks/ch08_speaker_and_noise.ipynb) | Equal Error Rate and beyond, a three-part Diarization Error Rate, enhancement measured by WER |
| 9 | [Arabic TTS front end](notebooks/ch09_arabic_tts.ipynb) | Normalization, diacritization, G2P, and a round-trip intelligibility check |
| 10 | [Translation & SLU](notebooks/ch10_speech_translation_slu.ipynb) | Cascade vs direct translation with BLEU and chrF, error attribution, an intent-and-slot parser |
| 11 | [Audio-LLM prompting](notebooks/ch11_audio_llm_prompting.ipynb) | Instruction routing, per-task metrics, the per-dialect table, and an audit for four evaluation shortcuts |

## Citing the book

> Al-Khalifa, H. S. *Introduction to Arabic Speech Technologies.* (forthcoming).

*(Update this entry with the final publisher, year, and DOI once available.)*
