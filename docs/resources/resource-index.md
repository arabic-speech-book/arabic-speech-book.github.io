# Arabic Speech Resource Index

Every corpus, benchmark, model, and toolkit named in the book, in one place. This is the page people link to and the one that goes stale fastest; last checked: **2026-08-12**.

!!! danger "A caution the book insists on"
    A checkpoint is an **untested component** until you test it, and a language list is **not** evidence of dialect coverage.

## Corpora (Table 7.1)

| Name | Scale | Variety | Domain | Access / licence | Main use | Ch. | Last checked |
|------|-------|---------|--------|------------------|----------|-----|--------------|
| **KAPD** | instrumented phonetic database | MSA phonetics | studio / instrumented | KACST | phonetics | 7 | 2026-08-12 |
| **SAAVB** | ~1,033 speakers | MSA, Saudi accent | telephone | KACST | ASR; speaker | 7 | 2026-08-12 |
| **KSU** | ~590 h; 269 speakers | MSA, many nationalities | studio, office, cafeteria | LDC license | ASR; speaker | 7 | 2026-08-12 |
| **L2-KSU** | ~6 h; 80 speakers | MSA, native and learner | read prompts | LDC license | ASR; speaker; learner speech | 7 | 2026-08-12 |
| **L2AraSpeech** | ~44 h; 220 learners | MSA, learner | read, mobile app | IEEE DataPort, non-commercial | pronunciation training | 7 | 2026-08-12 |
| **MGB-2** | > 1,200 h | MSA | broadcast | research use (MGB challenge) | ASR | 7 | 2026-08-12 |
| **MGB-3** | ~16 h + dialect identification | Egyptian (+ 5-way) | web video | research use (MGB challenge) | ASR; dialect identification | 7 | 2026-08-12 |
| **MGB-5** | ~13 h + 17-way identification | Moroccan (+ 17-way) | web video | research use (MGB challenge) | ASR; dialect identification | 7 | 2026-08-12 |
| **QASR** | ~2,000 h | MSA, some dialect | broadcast | CC BY-NC 2.0 | ASR; diarization | 7 | 2026-08-12 |
| **MASC** | ~1,000 h | multi-dialect | found web audio | IEEE DataPort; CC BY 4.0 | ASR | 7 | 2026-08-12 |
| **SADA** | ~668 h | Saudi dialects | broadcast | SDAIA; terms with the release | ASR; dialect identification | 7 | 2026-08-12 |
| **Common Voice Arabic** | release-dependent validated hours | mostly MSA | read prompts | CC0 | ASR | 7 | 2026-08-12 |
| **Casablanca** | 13.6k clips; eval splits only | 8 dialects | mixed | CC BY-NC-ND 4.0 | ASR; dialect identification | 7 | 2026-08-12 |
| **Aswat** | ~732 h, unlabeled | mostly MSA | mixed | terms with the release | pretraining | 7 | 2026-08-12 |
| **FLEURS (Arabic)** | ~12 h per language | MSA | read prompts | CC BY 4.0 | benchmarking | 7 | 2026-08-12 |
| **ArabCeleb** | 1,930 utterances; 100 speakers | mixed | found video | CC BY 4.0; pointers, not audio | speaker identification and verification | 7 | 2026-08-12 |
| **ZAEBUC-Spoken** | ~12 h | MSA, Gulf, Egyptian, English | recorded meetings | terms with the release | code-switching; dialectness | 7 | 2026-08-12 |
| **Habibi benchmark** | ~11,400 utterances | 7 dialects incl. Saudi | derived from the corpora above | Apache-2.0 | speech synthesis benchmarking | 7 | 2026-08-12 |
| **LDC dialect telephone [23, 24, 25, 26]** | 45-50 h each | Egyptian, Gulf, Iraqi, Levantine | telephone | LDC license | ASR; dialect identification | 7 | 2026-08-12 |
| **NEMLAR [27, 28]** | 40 h broadcast; >10 h studio | MSA; Egyptian | broadcast; studio, read | ELRA license, fee | ASR; speech synthesis; phonetics | 7 | 2026-08-12 |
| **Arabic Speech Corpus** | ~1,800 utterances | Levantine (Damascus) | studio, read | CC BY 4.0 | speech synthesis; phone alignment | 7 | 2026-08-12 |

## Models, toolkits & method families

The tables in the other chapters carry no licence column, so those fields are left empty rather than filled with a guess.

| Name | Type | Domain | Main use | Ch. |
|------|------|--------|----------|-----|
| **Read (prompted) speech** | — | — | volunteers read prompts; the prompt is the transcript \| Common Voice Arabic [17] | 3 |
| **Broadcast news and talk** | — | — | harvested from television and radio; lightly supervised transcripts \| MGB-2 [19]; QASR [20] | 3 |
| **Found web audio** | — | — | collected from video platforms, filtered by license \| MASC [21] | 3 |
| **Conversational / telephone** | — | — | calls or fieldwork recorded with consent; verbatim transcription \| dialect corpora catalogued in Chapter 7 | 3 |
| **Special-purpose studio** | — | — | one speaker, controlled; diacritized, aligned text \| ClArTTS [23] | 3 |
| **CTC** | — | — | monotonic, alignment-free \| yes, with a streaming encoder \| none (outputs independent) \| needs an external language model | 5 |
| **RNN-Transducer** | — | — | monotonic, explicit \| yes, designed for streaming \| yes (prediction network) \| heavier to train | 5 |
| **Attention (LAS-style)** | — | — | soft, can be non-monotonic \| not naturally \| yes (decoder) \| looping, deletions, long-form errors | 5 |
| **wav2vec 2.0 / XLS-R** | — | — | contrastive, self-supervised \| XLS-R: ~436k h, 128 languages \| Arabic included; fine-tune per dialect | 6 |
| **HuBERT / WavLM** | — | — | masked prediction; WavLM adds denoising \| tens of thousands of hours, English-centric \| transfers, but gains from Arabic continual pretraining | 6 |
| **Whisper** | — | — | weak supervision (labeled web audio) \| ~680k h, multilingual \| covered; strong MSA, weaker dialect | 6 |
| **MMS** | — | — | self-supervised (wav2vec 2.0) + ASR \| 1,400+ languages pretraining \| Arabic and some varieties | 6 |
| **SeamlessM4T** | — | — | self-supervised backbone + supervised \| ~1M h backbone; ~100 languages \| Arabic for ASR and translation | 6 |
| **Omnilingual ASR** | — | — | self-supervised (7B) + encoder-decoder \| 1,600+ languages \| Arabic covered; extensible to new varieties | 6 |
| **ArTST** | — | — | unified Arabic text and speech \| MSA focus \| Arabic-centric (MSA; dialects emerging) | 6 |
| **Arabic front end (9.2)** | — | — | CAMeL Tools [36], Farasa [37], and published Arabic diacritizer models [3] \| normalization, morphological analysis and restored diacritics | 9 |
| **Grapheme-to-phoneme (9.2)** | — | — | phonemizer [38] with the espeak-ng backend, and rule sets written for Arabic [4] \| letters to phonemes, once the diacritics are there | 9 |
| **Acoustic models (9.4)** | — | — | Coqui TTS, ESPnet [34], NVIDIA NeMo [39] \| Tacotron 2 and FastSpeech 2 recipes, and pretrained checkpoints | 9 |
| **Vocoders and end-to-end (9.5)** | — | — | Coqui TTS, ESPnet [34], NVIDIA NeMo [39] \| HiFi-GAN and VITS, trainable on a single-speaker Arabic corpus | 9 |
| **Zero-shot cloning (9.7)** | — | — | Coqui TTS, and the open speaker-prompted models [16] \| synthesis from a few seconds of a target speaker | 9 |
| **Listening tests (9.8)** | — | — | Label Studio, webMUSHRA [40] \| MOS and MUSHRA-style interfaces, randomization and anchors | 9 |
| **The objective cross-check (9.8)** | — | — | Hugging Face Transformers [41], ESPnet [35] \| an Arabic recognizer to transcribe the output, and WER scoring | 9 |
| **The cascade (10.1)** | — | — | the recognizers of Table 9.4 [1], and a translation model beside them \| an Arabic transcript, then an English sentence, each inspectable | 10 |
| **Unified and end-to-end translation (10.2, 10.4)** | — | — | the released Seamless models [6, 7] \| speech to text and speech to speech in one model, Arabic in both directions | 10 |
| **Simultaneous translation (10.3)** | — | — | SimulEval [24], and the streaming model of the same family [7] \| latency measured the same way twice, and a streaming baseline | 10 |
| **Translation scoring (10.5)** | — | — | sacreBLEU [10], COMET [9] \| a BLEU and a chrF that two papers can compare, and a neural score | 10 |
| **Understanding over speech (10.7, 10.8)** | — | — | ESPnet-SLU [25] \| intent and slot recipes that run on audio rather than on transcripts | 10 |
| **Annotating intents and slots (10.7, 10.9)** | — | — | Label Studio \| an ontology and an interface for labelling spoken commands | 10 |
| **SALMONN** | — | — | encoders + window-level connector to a frozen LLM \| broad skills, some emergent | 11 |
| **Qwen2-Audio** | — | — | audio encoder + LLM, prompt-driven \| voice chat and audio analysis | 11 |
| **AudioPaLM** | — | — | shared text and audio tokens in one LLM \| can speak and listen | 11 |
| **Jais** | — | — | Arabic-centric text LLM \| text only; a backbone for ALMs | 11 |
| **AceGPT** | — | — | localized Arabic text LLM \| text only; culture and values focus | 11 |
| **Qwen2-Audio / Qwen2.5-Omni [7, 17]** | — | — | multilingual audio / omni LLM \| speech in and out; some Arabic | 11 |
| **Fanar 2.0** | — | — | Arabic-centric platform \| speech in and out; bilingual Arabic and English ASR and TTS | 11 |

## Dataset spotlights

??? note "KAPD"
    Dataset Spotlight: the KACST Arabic Phonetics Database (KAPD) [6], [28]Descriptive resources for Arabic phonetics and phonology [6], together with the King Abdulaziz City for Science and Technology (KACST) Arabic Phonetics Database (KAPD), a corpus of more than 46,000 files of articulatory and acoustic measurements from nine experiments with native speakers [28], provide carefully documented sound inventories and example words.Such resources can be converted into a pronunciation lexicon, the table that maps each word to its sequence of phones, which both classical recognizers (Chapter 4) and synthesizers (Chapter 9) depend on.

    The companion notebook for this chapter builds a small lexicon of this kind.

??? note "L2AraSpeech"
    Dataset Spotlight: L2AraSpeech, and the corpora that do not existL2AraSpeech is the corpus the pronunciation half of this chapter can point at: recordings from 220 non-native speakers of varied national and linguistic backgrounds reading 25 sentences and 61 minimal pairs chosen by linguists who teach Arabic to non-native speakers, with 60 of those speakers annotated for pronunciation errors, released through IEEE Dataport in raw, processed and annotated form under a licence for non-commercial research [12].

    The minimal pairs are the part to look at first, because a minimal pair is the experiment this chapter keeps describing: two words that differ in exactly one sound, so a system that scores the pair correctly has scored the contrast rather than the word.

    The other two populations are still waiting.

    For disordered Arabic speech there is no substantial corpus at all, which is why the pee

??? note "SADA"
    Dataset Spotlight: SADA, the Saudi Audio DatasetSADA [19] is a large Saudi Arabic broadcast corpus with multiple dialects, speaker and gender labels, and defined splits, released under the license and access conditions specified in its dataset documentation.It is valuable because it adds spontaneous Gulf-dialect material to a landscape long dominated by MSA broadcast data, which makes it well suited to the dialect-balancing and per-dialect reporting practices above.

    When using it, report the version, the license, the per-dialect hours, the speaker metadata, and the official splits.

??? note "Common Voice Arabic"
    Dataset Spotlight: Common Voice ArabicCommon Voice is a crowd-sourced, openly licensed corpus in which volunteers read sentences aloud and others validate the recordings [13].Its Arabic portion is read rather than spontaneous speech, and its coverage of dialects is uneven, so it is not a complete picture of the language.

    But its permissive license and easy access make it the ideal starting point for the labs in this book: every reader can download it and run experiments without special agreements, provided each lab states the release version, the validated split, and the license alongside its results.

??? note "Casablanca"
    Dataset Spotlight: CasablancaCasablanca [15] is a multidialectal Arabic speech corpus spanning several dialects with transcriptions and annotations for dialect, gender, and code-switching, released under the license and access conditions in its documentation.Because it provides supervised dialectal data across many varieties, it is well suited to training and, especially, to honestly evaluating end-to-end dialect systems.

    Report the version, the license, the per-dialect hours, and the official splits when you use it.

??? note "Aswat"
    Dataset Spotlight: AswatAswat [18] is a curated, manually cleaned corpus of about 732 hours of unlabeled Arabic speech (roughly two-thirds MSA) assembled for self-supervised pretraining.Because it is large and unlabeled, it is well suited to continual pretraining: continue the self-supervised objective on Aswat to move a multilingual encoder toward Arabic before fine-tuning on a small labeled set.

    Report the version and the hours used.

