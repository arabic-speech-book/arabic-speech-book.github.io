# Evaluation and reproducibility checklist

*The Reproducibility Note from every chapter of* **Introduction to Arabic Speech Technologies**, *gathered into one page. Each is what a result of that kind must carry before it can be believed or repeated.*

## Chapter 1: Speech technologies and the Arabic challenge

A WER is only interpretable alongside the exact test split, the text normalization applied, and whether diacritics were scored. Two papers that normalize Arabic text differently, for example by removing or keeping diacritics, by unifying the various forms of Alef and Ta-marbuta, or by splitting clitics such as the definite article and the conjunction from their hosts, can report numbers that differ by several points on identical systems. Nor is a difference in WER automatically a difference in system quality: on a small test set a gap of a point or less may not survive a significance test, and Chapter 4 shows how to run one. Always publish the normalization script with the result.

## Chapter 2: Arabic language and speech fundamentals

Always state the transliteration scheme you use (for example Buckwalter for ASCII contexts or the International Phonetic Alphabet for pronunciation), the phoneme inventory you assume, whether diacritics are kept or stripped, the text-normalization rules applied, and how words are segmented (raw words, morphological tokens, or subword units). A phoneme set, lexicon, or result is only reusable when these choices are documented, because the same Arabic word can be written, vowelled, and split in several ways.

## Chapter 3: Digital speech processing

A feature pipeline is reproducible only if its settings are reported in full: the sampling rate, the frame length and hop, the window type, the transform size, the number of mel filters and their lower and upper frequencies, the mel convention (for example HTK or Slaney), whether the magnitude or power spectrum is used, the logarithm floor, the number of cepstral coefficients, the normalization and its scope, the augmentation policy, and the random seed. Where text is scored, also report the text normalization and the Word Error Rate (WER) or Character Error Rate (CER) convention, including whether diacritics are retained and whether speaker diarization was used.

## Chapter 4: Arabic ASR I

A reproducible Arabic ASR paper should report the evaluation normalization script, the diacritization policy, the tokenizer type and vocabulary size, the acoustic data and splits, the language-model text if one is used, the lexicon or G2P source if one is used, the augmentation policy, the dialect balance, and per-dialect WER or CER.

## Chapter 5: Arabic ASR II

An end-to-end Arabic result is reproducible only if it names the model and its loss (CTC, transducer, attention, or hybrid, with the CTC weight if hybrid), the encoder architecture and whether it is causal or full context, the output unit and its vocabulary size, the diacritization policy for the training text and for the references, the training data with its hours per dialect and its splits, the decoding configuration named in Section 5.6, the external language model and its fusion weight if one was used, the normalization script applied before scoring, and per-dialect WER or CER beside any pooled figure. Two of these decide whether the numbers can be compared at all: the output unit and the diacritization policy, because a system scored on undiacritized text is not being asked the same question as one scored with the short vowels in place.

## Chapter 6: Speech foundation models

A reproducible foundation-model result reports the pretrained checkpoint and its source, whether the encoder was frozen or fine-tuned and which layers, the adaptation method and its trainable-parameter count (for example the LoRA rank), the labeled data and splits, the evaluation sets and their versions, the text normalization, and per-dialect WER or CER alongside any pooled figure.

## Chapter 7: Corpora, annotation and benchmarks

Cite the corpus by name and version, name the exact split files you used, and release your transcription guidelines and inter-annotator agreement alongside the data. State the license and any access restriction, and where text is scored, give the normalization and the per-dialect WER or CER so others can reproduce and compare the result.

## Chapter 8: Dialect identification and spoken language processing

Fix the dialect taxonomy and the per-class counts in every report. Two papers that both say ‘Gulf’ may mean different country sets, and an accuracy figure is meaningless without the class inventory and how many test utterances each class had. State the taxonomy, the counts, the segment-length distribution, and the channel sources, and report macro-F1 next to accuracy.

## Chapter 9: Speech synthesis

Report the front end (diacritizer and grapheme-to-phoneme), the acoustic model and vocoder and their training data, the corpus and its diacritization quality, and the evaluation design: the number and background of listeners, the MOS with its confidence interval, and the objective WER cross-check, broken down per dialect.

## Chapter 10: Speech translation and understanding

Report the architecture (cascade or end-to-end) and every component and its training data, the parallel or labeled corpus and its splits, the text normalization used for scoring, and the metrics: BLEU and a neural metric such as COMET for translation, Average Lagging for streaming, and intent accuracy, slot F1, and joint goal accuracy for understanding, all per dialect.

## Chapter 11: Audio-language models

For an audio-language model, report the audio encoder and language model used and which parts were frozen or trained, the instruction set and tasks, and the exact evaluation data with its provenance (recorded or synthesized, and how labels were obtained). For Arabic, report results per dialect and on real, spontaneous speech, and state any train and test overlap so a claimed capability can be reproduced and trusted.

## Chapter 12: Applications

For assessment and clinical systems, report the rater pool and their qualifications, the scoring rubric, the population tested (with consent basis), the data size per speaker or group, the metric, and the agreement between the system and expert humans. A pronunciation or clinical score without its rater and population details cannot be interpreted or reproduced.

## Chapter 13: Responsible Arabic speech technology

For trust-related work, release the exact evaluation protocol: the threat model and attacker assumptions, the per-dialect and per-gender breakdowns, the data provenance (recorded or synthesized, and license), and for attacks and defenses the precise attack and defense settings. A safety or fairness result that cannot be reproduced cannot be relied on.

## Chapter 14: End-to-end projects

A project is reproducible only if the repository contains the corpus version and split files, the annotation guideline, the feature and training configuration, the augmentation policy and random seed, the text-normalization and Word Error Rate or Character Error Rate (CER) scoring scripts, and the datasheet. State the diacritization convention explicitly, since it changes every count downstream.

