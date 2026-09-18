# Companion notebooks

*Introduction to Arabic Speech Technologies*, by Hend S. Al-Khalifa.

Twelve notebooks, one per chapter that has one. They are not printed in the
book: the book points here, so that a notebook can be corrected when a library
changes and added to when something new is worth showing.

| Notebook | Chapter | What it does |
| --- | --- | --- |
| `ch01_first_contact_arabic_asr.ipynb` | 1 | Score a recognizer on Arabic, then watch text normalization move the number. MSA against dialect. |
| `ch02_arabic_phonetics_g2p.ipynb` | 2 | A rule-based grapheme-to-phoneme converter for diacritized MSA, scored by phone error rate, and what emphasis does to the second formant. |
| `ch03_speech_features.ipynb` | 3 | Framing, spectrograms, the mel filterbank, MFCCs, SpecAugment and linear prediction, each written out rather than called. Includes the chapter's exercises as code. |
| `ch04_arabic_asr_foundations.ipynb` | 4 | WER and CER with and without normalization, four tokenizations of one sentence, the forward algorithm, and continuation counts. |
| `ch05_end_to_end_arabic_asr.ipynb` | 5 | CTC alignments and the forward sum, a transducer walk, beam search with shallow fusion, and the choice of output unit. |
| `ch06_arabic_foundation_models.ipynb` | 6 | Full fine-tuning against low-rank adaptation: a cost model that runs anywhere, and a real run for a GPU. |
| `ch07_corpus_loader.ipynb` | 7 | Two corpora into one schema, the audit that decides a corpus choice, speaker overlap, and Fleiss' kappa. |
| `ch08_dialect_id.ipynb` | 8 | A dialect classifier on self-supervised embeddings, accuracy against macro F1, the confusion matrix, and a spoken-document search. |
| `ch08_speaker_and_noise.ipynb` | 8 | Equal Error Rate and what lies beyond it, a Diarization Error Rate in three parts, and enhancement measured two ways. |
| `ch09_arabic_tts.ipynb` | 9 | The Arabic text-to-speech front end: normalization, diacritization, grapheme-to-phoneme, and the round-trip intelligibility check. |
| `ch10_speech_translation_slu.ipynb` | 10 | Cascade against direct translation with BLEU and chrF, error attribution across the stages, and an intent-and-slot parser. |
| `ch11_audio_llm_prompting.ipynb` | 11 | Instruction routing, per-task metrics, the per-dialect table, and an audit for the four shortcuts that inflate Arabic scores. |

Chapters 12, 13 and 14 have no notebook. Their work is a project rather than a
computation, and Chapter 14 is itself the worked project.

## Running them

Every notebook runs **end to end with no downloads and no accounts**. Where a
real corpus or a pretrained model is unavailable, a clearly marked fallback
stands in for it and the notebook prints which path it took. Cells that need a
download are marked `OPTIONAL` and are safe to skip.

    pip install -r requirements.txt
    jupyter lab

In Google Colab, open the notebook and run it. The first block of
`requirements.txt` is already installed there.

## Two conventions worth keeping

**The provenance cell.** Every notebook ends with one. It asks for the corpus
and its release version, the licence, the model and its revision, the
normalization applied before scoring, and the date. Fill it in before quoting
any number the notebook produced. It is the same information the chapter's
Reproducibility Note asks for, and it is the difference between a result and a
screenshot.

**Per dialect, always.** Several notebooks compute a pooled figure and then
break it down. The breakdown is the point. A pooled Arabic number is an average
over things that are not the same thing, and it can look good while a whole
variety fails.

## Rebuilding

The notebooks are generated, so that the twelve share one structure and one set
of conventions. `build/` holds the generator: `nbbuild.py` and one
`build_chNN.py` per notebook.

    cd build && python3 build_ch03.py

Edit the builder rather than the notebook if you want a change to survive the
next regeneration.
