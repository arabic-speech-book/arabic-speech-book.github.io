# Tools & Models

Open-source models, toolkits, and libraries for building Arabic speech systems — grouped by what you need them for.

## Foundation & pretrained models

| Tool | What it does | Arabic? | Link |
|------|--------------|---------|------|
| **Whisper** (OpenAI) | Multilingual ASR + translation | Yes (incl. Arabic) | [github](https://github.com/openai/whisper) · [HF](https://hf.co/openai/whisper-large-v3) |
| **wav2vec 2.0 / XLS-R** | Self-supervised speech representations | Multilingual | [HF: facebook/wav2vec2-xls-r](https://hf.co/facebook/wav2vec2-xls-r-300m) |
| **MMS** (Meta) | ASR/TTS for 1,000+ languages | Yes | [HF: facebook/mms-1b-all](https://hf.co/facebook/mms-1b-all) |
| **ArTST** | Arabic text & speech transformer (ASR/TTS/dialect ID) | Arabic-first | [github: mbzuai-nlp/ArTST](https://github.com/mbzuai-nlp/ArTST) |
| **SeamlessM4T** (Meta) | Speech translation & ASR | Yes | [HF: facebook/seamless-m4t-v2-large](https://hf.co/facebook/seamless-m4t-v2-large) |

## Speech toolkits (training & pipelines)

| Tool | Strength | Link |
|------|----------|------|
| **Hugging Face Transformers** | Easiest path to Whisper/wav2vec2 fine-tuning | [docs](https://huggingface.co/docs/transformers) |
| **SpeechBrain** | All-in-one PyTorch speech toolkit | [speechbrain.github.io](https://speechbrain.github.io/) |
| **ESPnet** | End-to-end ASR/TTS/ST research toolkit | [github](https://github.com/espnet/espnet) |
| **NVIDIA NeMo** | Production-grade ASR/TTS/LLM | [github](https://github.com/NVIDIA/NeMo) |
| **Kaldi** | Classic HMM/DNN ASR (still a strong baseline) | [kaldi-asr.org](https://kaldi-asr.org/) |

## Text-to-speech

| Tool | Strength | Link |
|------|----------|------|
| **Coqui TTS** | Multi-architecture open TTS (VITS, XTTS) | [github](https://github.com/coqui-ai/TTS) |
| **Piper** | Fast local neural TTS | [github](https://github.com/rhasspy/piper) |

## Arabic NLP & linguistic helpers

| Tool | What it does | Link |
|------|--------------|------|
| **CAMeL Tools** | Arabic morphology, dialect ID, diacritization, normalization | [github](https://github.com/CAMeL-Lab/camel_tools) |
| **PyArabic** | Arabic text utilities (diacritics, normalization) | [github](https://github.com/linuxscout/pyarabic) |
| **Farasa** | Segmentation, POS, diacritization | [farasa.qcri.org](https://farasa.qcri.org/) |
| **Mishkal** | Arabic diacritization (tashkeel) | [github](https://github.com/linuxscout/mishkal) |

## Audio & signal processing

| Tool | What it does | Link |
|------|--------------|------|
| **librosa** | Audio analysis, features, spectrograms | [librosa.org](https://librosa.org/) |
| **torchaudio** | PyTorch audio I/O, transforms, models | [docs](https://pytorch.org/audio/) |
| **pydub / FFmpeg** | Format conversion & basic editing | [ffmpeg.org](https://ffmpeg.org/) |

## Evaluation

| Tool | Metric | Link |
|------|--------|------|
| **jiwer** | WER / CER for ASR | [github](https://github.com/jitsi/jiwer) |
| **🤗 Evaluate** | WER, CER, BLEU, and more | [docs](https://huggingface.co/docs/evaluate) |

!!! tip "Arabic-specific evaluation"
    For Arabic ASR, report **CER** alongside WER, and consider normalizing diacritics and orthographic variants (أ/إ/آ → ا, ة/ه, ى/ي) before scoring. The book's evaluation chapter and [ch04](notebooks/ch04_arabic_asr_foundations.ipynb) cover this in detail.
