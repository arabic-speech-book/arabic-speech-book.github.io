# Arabic Speech Datasets

A curated, categorized database of Arabic speech corpora used throughout the book. Use the search box (top of the page) to filter, or browse by task below.

!!! info "How to read this table"
    **Hours** are approximate. **Access** indicates where to obtain the data. Always check each dataset's own **license** before use — many are research-only. This list is a living starting point; see [Contributing](#contributing) to add or correct an entry.

## Automatic Speech Recognition — MSA & broadcast

| Dataset | Variety | Hours | Access | Notes |
|---------|---------|-------|--------|-------|
| **MGB-2** | MSA (broadcast) | ~1,200 | [mgb-challenge.org](http://www.mgb-challenge.org/) | Al Jazeera broadcast news; standard ASR benchmark |
| **QASR** | MSA + dialectal | ~2,000 | [arabicspeech.org](https://arabicspeech.org/qasr/) | Largest transcribed Arabic broadcast corpus; rich metadata |
| **Common Voice (Arabic)** | MSA | growing | [commonvoice.mozilla.org](https://commonvoice.mozilla.org/ar) | Crowd-sourced, CC0; great for quick experiments |
| **Arabic News Speech Corpus** | MSA (news) | ~10+ | [HF: IbrahimSalah](https://hf.co/datasets/IbrahimSalah/The_Arabic_News_speech_Corpus_Dataset) | Syllable-based ASR with Wav2Vec2 |
| **MASC** | MSA + dialects | ~1,000 | [HF: abdusah](https://hf.co/datasets/abdusah/arabic_speech_massive) | Massive Arabic Speech Corpus from YouTube |
| **Aswat** | MSA + varieties | ~732 | See [paper (ArabicNLP 2023)](https://aclanthology.org/2023.arabicnlp-1.10/) | Clean speech for self-supervised pretraining |
| **FLEURS (Arabic)** | MSA | ~12 | [HF: google/fleurs](https://hf.co/datasets/google/fleurs) | Multilingual; good for LID + low-resource ASR |

## ASR — dialectal

| Dataset | Variety | Hours | Access | Notes |
|---------|---------|-------|--------|-------|
| **MGB-3** | Egyptian | ~16 | [mgb-challenge.org](http://www.mgb-challenge.org/) | YouTube; dialectal adaptation challenge |
| **MGB-5** | Moroccan | ~14 | [mgb-challenge.org](http://www.mgb-challenge.org/) | Moroccan dialect ASR + dialect ID |
| **Casablanca** | 8 dialects | varies | See [paper (2024)](https://arxiv.org/abs/2410.04527) | Multidialectal data + models |
| **SADA** | Saudi dialects | ~668 | [Kaggle: SADA](https://www.kaggle.com/datasets/sdaiancc/sada2022) | Saudi Audio Dataset for Arabic (SDAIA) |
| **Egyptian Arabic Speech** | Egyptian | varies | [HF: Yahya-Mohamed](https://hf.co/datasets/Yahya-Mohamed/egyptian-arabic-speech-dataset) | Community dialectal corpus |

## Dialect identification

| Dataset | Coverage | Hours | Access | Notes |
|---------|----------|-------|--------|-------|
| **ADI-17** | 17 country-level dialects | ~3,000 | See [paper (2019)](https://arxiv.org/abs/2005.14601) | Standard dialect-ID benchmark |
| **MGB-3 / MGB-5** | Egyptian / Moroccan | — | [mgb-challenge.org](http://www.mgb-challenge.org/) | Also used for dialect ID |

## Text-to-speech (TTS)

| Dataset | Variety | Hours | Access | Notes |
|---------|---------|-------|--------|-------|
| **Arabic Speech Corpus (Halabi)** | Levantine (Damascene) | ~3.7 | [HF: halabi2016](https://hf.co/datasets/halabi2016/arabic_speech_corpus) | Single-speaker, phonetically annotated; classic TTS corpus |
| **ClArTTS** | Classical Arabic | ~12 | See [paper (2023)](https://arxiv.org/abs/2303.00069) | Single-speaker Classical Arabic TTS |
| **ArabicSpeech / sawtarabi** | MSA | varies | [HF: ArabicSpeech](https://hf.co/datasets/ArabicSpeech/sawtarabi) | Community speech collection |

## Emotion & paralinguistics

| Dataset | Variety | Type | Access | Notes |
|---------|---------|------|--------|-------|
| **KSUEmotions** | MSA / Gulf | Emotional speech | See literature | Multi-emotion acted corpus |
| **EYASE** | Egyptian | Emotional speech | See literature | Egyptian emotion recognition |

## Quranic & religious recitation

| Dataset | Type | Access | Notes |
|---------|------|--------|-------|
| **EveryAyah / Tarteel** | Quranic recitation | [everyayah.com](https://everyayah.com/) | Many reciters; useful for recitation ASR / alignment |

---

## Quick load example

Most Hugging Face datasets load in two lines:

```python
from datasets import load_dataset

ds = load_dataset("halabi2016/arabic_speech_corpus")
print(ds)
```

See [Notebook ch07 — Corpus loader](notebooks/ch07_corpus_loader.ipynb) for a complete loading & preparation walkthrough.

## Contributing

Found a dataset we missed, or a broken link? Open an issue or a pull request on the
[GitHub repository](https://github.com/arabic-speech-book/arabic-speech-book.github.io).
Please include: name, variety/dialect, approximate hours, a stable link, and the license.
