# Notebooks

Twelve notebooks, one per chapter that has one. They are not printed in the book: the book points here, so a notebook can be corrected when a library changes and added to when something new is worth showing.

!!! success "Every notebook runs end to end with no downloads and no accounts"
    Where a real corpus or pretrained model is unavailable, a clearly marked **fallback** stands in for it, and the notebook prints which path it took. Cells that need a download are marked `OPTIONAL` and are safe to skip.

## The notebooks

| Ch. | Notebook | What it does |
|-----|----------|--------------|
| 1 | [First contact with Arabic ASR](ch01_first_contact_arabic_asr.ipynb) | Score a recognizer on Arabic, then watch text normalization move the number. MSA against dialect. |
| 2 | [Phonetics & G2P](ch02_arabic_phonetics_g2p.ipynb) | A rule-based grapheme-to-phoneme converter for diacritized MSA, scored by phone error rate, and what emphasis does to the second formant. |
| 3 | [Speech features](ch03_speech_features.ipynb) | Framing, spectrograms, the mel filterbank, MFCCs, SpecAugment and linear prediction, each written out rather than called. Includes the chapter's exercises as code. |
| 4 | [Arabic ASR foundations](ch04_arabic_asr_foundations.ipynb) | WER and CER with and without normalization, four tokenizations of one sentence, the forward algorithm, and continuation counts. |
| 5 | [End-to-end ASR](ch05_end_to_end_arabic_asr.ipynb) | CTC alignments and the forward sum, a transducer walk, beam search with shallow fusion, and the choice of output unit. |
| 6 | [Foundation models: full vs LoRA](ch06_arabic_foundation_models.ipynb) | Full fine-tuning against low-rank adaptation: a cost model that runs anywhere, and a real run for a GPU. |
| 7 | [Corpus loader](ch07_corpus_loader.ipynb) | Two corpora into one schema, the audit that decides a corpus choice, speaker overlap, and Fleiss' kappa. |
| 8 | [Dialect ID](ch08_dialect_id.ipynb) | A dialect classifier on self-supervised embeddings, accuracy against macro-F1, the confusion matrix, and a spoken-document search. |
| 8 | [Speaker & noise](ch08_speaker_and_noise.ipynb) | Equal Error Rate and what lies beyond it, a Diarization Error Rate in three parts, and enhancement measured two ways. |
| 9 | [Arabic TTS](ch09_arabic_tts.ipynb) | The Arabic text-to-speech front end: normalization, diacritization, grapheme-to-phoneme, and the round-trip intelligibility check. |
| 10 | [Translation & SLU](ch10_speech_translation_slu.ipynb) | Cascade against direct translation with BLEU and chrF, error attribution across the stages, and an intent-and-slot parser. |
| 11 | [Audio-LLM prompting](ch11_audio_llm_prompting.ipynb) | Instruction routing, per-task metrics, the per-dialect table, and an audit for the four shortcuts that inflate Arabic scores. |

Chapters 12, 13, and 14 have no notebook — their work is a project rather than a computation, and Chapter 14 is itself the worked project.

## Running them

=== "Locally"

    ```bash
    pip install -r requirements.txt
    jupyter lab
    ```

    The [pinned requirements file](requirements.txt) is small: the first block is all twelve notebooks need to run end to end. The second block (torch, transformers, datasets, …) is only for the `OPTIONAL` cells and is commented out — uncomment what you need.

=== "Google Colab"

    Every notebook page has an **"Open in Colab"** badge at the top — one click opens it in Colab. Colab can only load notebooks from a **public** GitHub repository, so the badge goes live once this site is published. While the repository is private, use the **download** icon on the notebook page, then in Colab choose **File → Upload notebook**.

    Once it is open, the first block of `requirements.txt` is already installed in Colab. For an `OPTIONAL` cell, run the pip line printed at the top of the notebook that needs it.

## Two conventions worth keeping

!!! abstract "The provenance cell"
    Every notebook ends with one. It asks for the corpus and its release version, the licence, the model and its revision, the normalization applied before scoring, and the date. Fill it in before quoting any number the notebook produced — it is the difference between a result and a screenshot.

!!! abstract "Per dialect, always"
    Several notebooks compute a pooled figure and then break it down. **The breakdown is the point.** A pooled Arabic number is an average over things that are not the same thing, and it can look good while a whole variety fails.

## Rebuilding

The notebooks are *generated*, so the twelve share one structure and one set of conventions. The generator (`nbbuild.py` and one `build_chNN.py` per notebook) lives in the repository's `notebooks-src/build/` folder. Edit the builder rather than the notebook if you want a change to survive the next regeneration.
