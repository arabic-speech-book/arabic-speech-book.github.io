# Chapter 6 Solutions: Speech Foundation Models and Self-Supervised Learning

These solutions follow the numbering of the chapter's exercise list. Exercises 2 and 5 have companion notebooks.

Notebooks for this chapter: [`Chapter_06_Exercise_02.ipynb`](Chapter_06_Exercise_02.ipynb), [`Chapter_06_Exercise_05.ipynb`](Chapter_06_Exercise_05.ipynb).

---

## Exercise 1

**Task.** In two or three sentences each, contrast the wav2vec 2.0, HuBERT and CPC objectives: state what each one hides, what it asks the model to predict, and why that yields useful representations.

**Solution.** (Sections 6.2 to 6.4.)

*wav2vec 2.0.* It hides spans of the convolutional feature sequence by replacing them with a mask vector before the Transformer, while the same unmasked features pass through a learned quantizer that turns them into discrete codebook entries. At each masked position the model must pick the correct quantized target out of a set of distractors sampled from other masked positions in the same utterance (a contrastive task). To succeed, the context network must infer what sound was hidden from its surroundings, so its representations come to encode the phonetic content of speech in a way that generalizes across speakers and channels; the codebook entries end up loosely associated with speech sounds without ever seeing a phoneme label.

*HuBERT.* It also hides spans of the feature sequence, but the targets are discrete pseudo-labels obtained beforehand by k-means clustering of acoustic features (MFCCs in the first round, the model's own hidden representations in later rounds). The model is asked to classify each masked position into the right cluster, a masked-prediction task with a fixed inventory rather than a contrastive choice. Predicting a cluster identity from context forces the model to learn which acoustic units occur where, and re-clustering the model's own representations makes the targets progressively more phone-like, which is why the representations become useful for recognition.

*CPC (Contrastive Predictive Coding).* Nothing is masked; instead the model reads the audio up to the present and must predict the representations of *future* frames several steps ahead, distinguishing the true future from negative samples drawn elsewhere (a contrastive loss, so it belongs to the same family as wav2vec 2.0). Predicting the future from the past rewards representations that capture slowly varying, linguistically informative structure (which sound comes next, the rhythm of the utterance) and discards unpredictable local noise, and the causal formulation makes the learned encoder usable in a streaming setting.

---

## Exercise 2

**Task.** For an encoder with about 300 million parameters, estimate the trainable-parameter count for full fine-tuning versus a LoRA update of rank 8 applied to the attention query and value projections, and give the approximate ratio. Use 2dr trainable parameters per adapted projection and state your assumptions.

**Solution (notebook `Chapter_06_Exercise_02.ipynb`).**

*Assumptions.* A 300 M encoder of the wav2vec 2.0 / HuBERT Large type: 24 Transformer layers, hidden size d = 1024; one query and one value projection per layer, each a square d × d matrix; rank r = 8; biases and the small task head ignored.

*Calculation.*

* Per adapted projection: 2 d r = 2 × 1024 × 8 = **16,384**.
* Per layer (Q and V): 2 × 16,384 = 32,768.
* Over 24 layers: 24 × 32,768 = **786,432 ≈ 0.79 M** trainable parameters.
* Full fine-tuning: **≈ 300,000,000**.
* Ratio: 300 M / 0.786 M ≈ **380 : 1**; LoRA trains about **0.26 %** of the encoder.

*Sensitivity.* The count is linear in rank, in the number of adapted projections and in depth: r = 16 doubles it to 1.57 M (0.52 %); adapting all four attention projections (Q, K, V, output) doubles it again; a Base-type encoder (12 layers, d = 768) with r = 8 on Q and V gives 294,912. The notebook tabulates these. Caveats to state with the number: the frozen backbone must still be loaded, so LoRA saves optimizer and gradient memory rather than activation memory; fewer trainable parameters does not by itself mean less labeled data or shorter training; and LoRA does not match full fine-tuning in every setting (Table 6.2). What the ratio does buy is one shared backbone with a few-megabyte adaptation per Arabic dialect.

---

## Exercise 3

**Task.** Design a probing experiment to test whether a chosen encoder layer encodes phonetic information versus speaker information. Specify the frozen-encoder setup, the probe, the labels and the metric, and say what result would distinguish the two.

**Suggested solution.**

*Frozen-encoder setup.* Take a pretrained encoder (for example XLS-R 300 M or an Arabic model such as ArTST's encoder) and freeze every weight. Run a labeled Arabic corpus through it and store the hidden states of the layer under test, ℓ (and, for context, of every layer). Use a corpus with both phone-level alignments and speaker identities: the Arabic Speech Corpus (Damascene MSA, phoneme boundaries, one speaker) is not enough because it has one speaker; a combination such as Common Voice Arabic with forced alignments from the Montreal Forced Aligner, or SADA with its speaker labels plus alignments, gives both label types on the same audio. Splits must be **speaker-disjoint** for the speaker probe to be meaningful and **speaker-disjoint as well** for the phone probe, so that the phone probe cannot exploit speaker identity.

*Two probes on the same frames.*

1. **Phone probe.** Input: one frame vector from layer ℓ (20 ms). Label: the aligned phone from a small Arabic inventory (about 35 classes, including the emphatic, pharyngeal and uvular consonants and the long/short vowel distinction). Probe: a linear classifier (logistic regression) trained on the frozen features; optionally a one-hidden-layer MLP as a second, more permissive probe, reported separately.
2. **Speaker probe.** Input: the mean-pooled layer-ℓ vectors of an utterance. Label: speaker identity (closed set of, say, 100 speakers, with utterance-level train/test split within each speaker). Probe: the same linear classifier.

*Metric.* Phone probe: frame-level accuracy and, because classes are imbalanced, macro-F1, plus a confusion matrix over the emphatic/plain pairs. Speaker probe: top-1 identification accuracy. Both compared against (a) a chance baseline (majority class) and (b) a baseline probe trained on log-mel features, so that the gain attributable to the encoder is visible. Report accuracy as a function of layer index for both probes (a curve like Figure 6.4).

*What would distinguish the two.* If layer ℓ is a phonetic layer, the phone probe's accuracy at ℓ is high (well above the log-mel baseline) while the speaker probe's accuracy at ℓ is near its minimum across layers, and the confusion matrix keeps emphatic and plain consonants apart. If ℓ is a speaker layer, the reverse: high speaker accuracy, phone accuracy no better than at the raw features. If both are high, the layer is mixed, which is common in shallow layers; the *shape* of the two curves across layers, phone information rising into the middle layers while speaker information peaks early and decays, is the diagnostic. Two controls make the result honest: a probe trained on shuffled labels (should collapse to chance), and a check that the phone probe does not improve when the speaker label is fed to it as an extra input (if it does, the phone probe was leaking speaker information). State that the encoder was frozen and which layer and probe were used, as the Research Habit box requires.

---

## Exercise 4

**Task.** You have 700 hours of unlabeled Arabic audio and 10 hours of labeled dialect audio. Outline a pretrain-then-adapt plan: which pretrained model you would start from, whether you would continually pretrain on the unlabeled audio, and which adaptation method you would use for the 10 labeled hours, with justification.

**Suggested solution.**

*Starting model.* A self-supervised multilingual encoder that already contains Arabic, so that the 700 hours adjust rather than create the representations: XLS-R 300 M (436 k hours, 128 languages including Arabic) is the default choice; MMS's wav2vec 2.0 encoder or an Arabic-centric model (ArTST's encoder, or HArnESS if its checkpoints and evaluation hold up) are alternatives to compare on the same development set. Whisper is the other candidate, but it is a weakly supervised encoder-decoder without a standard self-supervised objective, so 700 hours of *unlabeled* audio cannot be used to continue its pretraining in the same way; it is better kept as the zero-shot baseline to beat.

*Continued pretraining: yes.* The 700 hours are the project's main asset. Continue the model's own self-supervised objective (contrastive with quantization for XLS-R) on the unlabeled dialect audio for a modest number of updates, starting from the released checkpoint rather than from scratch, so that the encoder adapts to the dialect's sounds, the channel and the speaking style (Section 6.8, Table 6.2, "when the original model poorly matches the target language, dialect, speaking style, channel, or acoustic environment"). Hold out a small unlabeled portion to monitor the pretraining loss, and confirm the benefit downstream rather than assume it: the Aswat result is evidence that in-language pretraining data can help, not a guarantee.

*Adaptation on the 10 labeled hours.* Two-stage: **LoRA or adapters first, full fine-tuning only if it wins on the development set.** With ten hours, full fine-tuning of 300 M parameters risks overfitting and forgetting, and it produces a separate 1.2 GB model per dialect; a LoRA update of rank 8 to 16 on the attention projections (well under 1 % of the parameters, Exercise 2) plus a CTC output layer trained on characters or a small subword vocabulary is the safer start, trains in hours on one GPU, and can be stored per dialect on a shared backbone. Use SpecAugment and speed perturbation, split the 10 hours speaker-disjoint (roughly 8 / 1 / 1), and decode with a dialect-text language model through shallow fusion if any dialect text exists. Then run full fine-tuning with a low learning rate and layer-wise learning-rate decay as a comparison; if it beats LoRA on the development set by a margin that survives a significance test, keep it. Whichever wins, report per-dialect WER and CER on real, spontaneous test speech against the zero-shot Whisper baseline and against the same recipe *without* continued pretraining, so that the contribution of the 700 hours is measured (Section 6.9, Reproducibility Note).

---

## Exercise 5

**Task.** Run a hands-on per-dialect error audit: take about five minutes of spontaneous Saudi or Gulf speech (SADA) or Egyptian speech, produce a baseline Whisper transcription, load output and reference into a text annotation tool such as Label Studio, tag each error separating genuine acoustic misrecognitions from MSA translation-style shifts, and report the per-dialect WER and discuss how that single number misrepresents the model's behaviour.

**Solution (notebook `Chapter_06_Exercise_05.ipynb`).**

*Data flag.* The official SADA release requires a Kaggle login and licence acceptance (CC BY-NC-SA 4.0) and MASC requires an IEEE DataPort account, so the notebook uses a community-redistributed SADA2022 subset on the Hugging Face Hub (`SarahUssama/sada-arabic-test-dataset-sample`, 496 segments with dialect, gender, environment and reference-transcript fields; Saudi and Egyptian labels). Verify the licence on the dataset card before use and prefer the official release for anything published. The notebook takes roughly five minutes of Saudi and five minutes of Egyptian segments.

*Pipeline.* (1) Whisper baseline (`openai/whisper-small` on CPU in the test run; `whisper-large-v3` recommended on a GPU); (2) one normalization function applied to both sides (diacritics, tatweel and punctuation removed; alif, ة/ه, ى/ي and digits unified; diacritics not scored); (3) per-dialect and pooled WER with S, D, I and N; (4) word-level alignment with `jiwer`, one row per error, with an **automatic pre-tag** as a hint only: a substitution whose hypothesis word is in the CAMeL Tools MSA lexicon while the reference word is not is flagged "candidate MSA shift", and a substitution differing in at most two letters "candidate spelling variant"; (5) export of a Label Studio task file and labelling interface with the tag set `acoustic`, `msa_shift`, `spelling_variant`, `deletion`, `insertion`, `reference_error`; (6) after the manual pass, a recomputation of the WER with MSA shifts and spelling variants excluded.

*Measured result in the test run* (whisper-small, CPU, subset as described; the manual audit itself is left to the reader, so the "excluding" column below uses the automatic pre-tags and is **not** an audited number):

| Dialect | Segments | Audio | N (ref. words) | S / D / I | WER | Pre-tagged MSA shift / spelling / hallucination | WER excluding the pre-tagged rows |
|---|---|---|---|---|---|---|---|
| Saudi | 91 | 299 s | 687 | 306 / 106 / 30 | **64.3 %** | 27 / 123 / 0 | 42.5 % |
| Egyptian | 62 | 189 s | 490 | 246 / 73 / 14 | **68.0 %** | 24 / 102 / 10 | 40.2 % |
| Pooled | 153 | 488 s | 1,177 | 552 / 179 / 44 | 65.8 % | | |

Settings: `openai/whisper-small`, greedy decoding with `no_repeat_ngram_size=4` and the output length capped to about six tokens per second of audio; segments restricted to those labelled *Clean* in the subset. A first run without the cap and without the environment filter produced a Saudi WER above 200 % driven by 1,110 insertions: Whisper fell into repetition loops on music-backed segments, which is itself an audit finding (the hallucination failure the OmniASR study reports, Section 6.9) and the reason the notebook adds a `hallucination` tag. The "excluding" column is only an upper bound on the effect of non-acoustic errors, because the automatic pre-tags are hints for the annotator and include false positives (يلا rendered as الله is not an MSA shift); the manual pass in Label Studio decides the real split.

*How the single number misrepresents the model.* Three ways, all visible in the alignment table.

1. **WER counts a translation as a mishearing.** When the speaker says وين and the model writes أين, or أبغى becomes أريد, the model has understood the word and rendered it in the register its training data favours; acoustically it did not fail. A WER treats this identically to hearing قلب as كلب. Tagging separates the two, and on dialectal speech the MSA-shift share is typically a large fraction of substitutions, so the "acoustic WER" is materially lower than the headline (the notebook's last table gives the number).
2. **Spelling convention is scored as error.** Dialect words have no fixed spelling; كده versus كدا, or a code-switched English word written in Latin versus Arabic letters, produce substitutions that a stricter or looser normalization would remove. The number depends on the convention as much as on the model.
3. **Pooling hides the gap.** The pooled WER sits close to whichever dialect contributes more words, so a five-minute Saudi sample and a five-minute Egyptian sample can hide a ten-point difference between them; and even within one dialect the score mixes clean studio segments with noisy or music-backed ones (the subset carries an Environment field, which the notebook can group by).

The honest report is therefore per dialect, with the environment stated, the normalization script attached, and the error breakdown by tag; the single WER is the starting point of the audit, not its conclusion.

---

### Flags and notes for the companion website

* Exercise 5 uses an unofficial SADA subset for accessibility; replace with the official release (Kaggle) when the website's data policy allows, and state the licence. The Label Studio step was not executed in testing (it is an interactive application); the exported task and config files follow Label Studio's documented formats.
