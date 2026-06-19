# Notebooks

Every chapter ships with a runnable Jupyter notebook. You can read them right here on the site, run them locally, or open them in Google Colab.

## Running the notebooks

=== "Locally"

    ```bash
    git clone https://github.com/arabic-speech-book/arabic-speech-book.github.io.git
    cd arabic-speech-book.github.io
    pip install -r requirements.txt   # or use the notebooks' own requirements
    jupyter lab docs/notebooks
    ```

=== "Google Colab"

    Open any notebook, then replace `github.com` with `githubtocolab.com` in its URL — Colab will load it directly. (Tip: add a "Open in Colab" badge to each notebook once the repo is public.)

## Chapter notebooks

| # | Notebook | Topic |
|---|----------|-------|
| 1 | [First contact: Arabic ASR](ch01_first_contact_arabic_asr.ipynb) | Transcribe your first Arabic audio |
| 2 | [Arabic phonetics & G2P](ch02_arabic_phonetics_g2p.ipynb) | Grapheme-to-phoneme for Arabic |
| 3 | [Speech features](ch03_speech_features.ipynb) | Spectrograms, MFCCs, filter banks |
| 4 | [Arabic ASR foundations](ch04_arabic_asr_foundations.ipynb) | Acoustic & language modeling |
| 5 | [End-to-end Arabic ASR](ch05_end_to_end_arabic_asr.ipynb) | CTC / seq2seq pipelines |
| 6 | [Arabic foundation models](ch06_arabic_foundation_models.ipynb) | Whisper, wav2vec 2.0, ArTST |
| 7 | [Corpus loader](ch07_corpus_loader.ipynb) | Loading & preparing Arabic corpora |
| 8 | [Enhancement front-end](ch08_enhancement_frontend.ipynb) | Denoising & speech enhancement |
| 9 | [Dialect identification](ch09_dialect_id.ipynb) | Identifying Arabic dialects |
| 10 | [Speaker identification](ch10_speaker_id.ipynb) | Speaker recognition |
| 11 | [Arabic TTS](ch11_arabic_tts.ipynb) | Text-to-speech synthesis |
| 12 | [Speech translation & SLU](ch12_speech_translation_slu.ipynb) | Translation & understanding |
| 13 | [Pronunciation & MDD](ch13_pronunciation_mdd.ipynb) | Mispronunciation detection |
| 14 | [Audio-visual emotion](ch14_av_emotion.ipynb) | Multimodal emotion recognition |
| 15 | [Audio LLM prompting](ch15_audio_llm_prompting.ipynb) | Prompting audio LLMs |
| 16 | [Capstone project](ch16_end_to_end_arabic_project.ipynb) | End-to-end Arabic system |
| 17 | [Fairness, security & audit](ch17_fairness_security_audit.ipynb) | Responsible deployment |

!!! note
    Notebooks render read-only on this site. Use the **download** icon at the top of each notebook page to grab the `.ipynb`.
