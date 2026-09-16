# Chapter 8 Solutions: Dialect Identification and Spoken Language Processing

These solutions follow the numbering of the chapter's exercise list. Exercise 2 has a companion notebook.

Notebook for this chapter: [`Chapter_08_Exercise_02.ipynb`](Chapter_08_Exercise_02.ipynb).

---

## Exercise 1

**Task.** Explain why neighbouring dialects dominate the confusions an Arabic dialect identifier makes. Refer to the dialect continuum and to at least one concrete pair of neighbouring varieties.

**Suggested solution.** Arabic dialects are not discrete boxes but a **continuum** (Sections 2.9 and 8.1): linguistic features change gradually across space, so two varieties spoken in adjacent regions share most of their phonology, vocabulary and grammar and differ only in a few features, whereas varieties at opposite ends of the continuum differ in many. A classifier that works from acoustic and phonotactic evidence (Section 8.2) sees, for a neighbouring pair, two distributions that overlap heavily, with the same consonant realizations, similar vowel systems, shared function words and similar intonation; the few distinguishing cues (a particular lexical item, one vowel shift, a stress pattern) may simply not occur in a short clip. The decision boundary between neighbours therefore runs through dense, mixed territory, and most errors fall on that boundary. Distant pairs are separated by many cues at once, so they are rarely confused.

*Concrete pairs.* **Gulf and Iraqi** (Table 2.8): both realize qāf as /g/, both belong to the same historical Bedouin-influenced group, and southern Iraqi *gilit* dialects shade into Kuwaiti and Eastern Saudi speech with no sharp break, so a Kuwaiti and a Basrawi clip present nearly the same phonotactics. **Levantine and Egyptian urban** speech is another: both turn qāf into a glottal stop, share the /eː/ and /oː/ mid vowels in many words, and share much vocabulary, so short clips are separated mainly by a handful of items (the Egyptian /g/ for jīm, the Levantine future particle) that may be absent. Within one country the effect repeats at a finer scale: Najdi versus Khaliji Saudi speech is far harder than Najdi versus Moroccan.

Two cautions from Section 8.11. First, a confusion pattern is not automatically proof of linguistic similarity: a model may be confusing two *programmes* or two *channels* rather than two dialects, which is why splits must separate speakers and sources. Second, real speech mixes registers and dialects, so some "confusions" between neighbours are clips that genuinely carry features of both, which a single label cannot represent; the taxonomy and the handling of mixed clips must be declared with every result.

---

## Exercise 2

**Task.** Implement the five steps of Section 8.11 on the four-class confusion matrix of Figure 8.8; extract TP, FP and FN per dialect, compute per-class precision and recall and the macro-averaged F1, and check that you recover the reported accuracy and macro-F1. Then raise the rare class from 50 to 500 test utterances holding its error rate fixed, and explain what happens to each of the two numbers and why.

**Solution (notebook `Chapter_08_Exercise_02.ipynb`).**

*The matrix (rows true, columns predicted; MSA, Egyptian, Levantine, Gulf).*

| | pred MSA | pred Egyptian | pred Levantine | pred Gulf | total |
|---|---|---|---|---|---|
| true MSA | 470 | 15 | 10 | 5 | 500 |
| true Egyptian | 20 | 255 | 20 | 5 | 300 |
| true Levantine | 10 | 15 | 105 | 20 | 150 |
| true Gulf | 4 | 3 | 25 | 18 | 50 |

*Five steps per class (executed).*

| Class | TP | FP (rest of column) | FN (rest of row) | Precision | Recall | F1 |
|---|---|---|---|---|---|---|
| MSA | 470 | 34 | 30 | 0.933 | 0.940 | 0.936 |
| Egyptian | 255 | 33 | 45 | 0.885 | 0.850 | 0.867 |
| Levantine | 105 | 55 | 45 | 0.656 | 0.700 | 0.677 |
| Gulf | 18 | 30 | 32 | 0.375 | 0.360 | 0.367 |

Macro-F1 = mean of the unrounded class F1 values = **0.712** (figure: 0.71). Accuracy = (470 + 255 + 105 + 18) / 1000 = 848 / 1000 = **0.848** (figure: 0.85). The highlighted Gulf values in the figure (TP 18, FP 30, FN 32, precision 0.38, recall 0.36, F1 0.37) are all recovered.

*Rare class raised from 50 to 500 with its error rate fixed.* The Gulf row is scaled by ten (40, 30, 250, 180), keeping recall at 36 % and the same spread of misses; the other rows are unchanged.

| | Gulf = 50 | Gulf = 500 |
|---|---|---|
| Accuracy | 0.848 | **0.697** |
| Macro-F1 | 0.712 | **0.658** |
| Gulf P / R / F1 | 0.38 / 0.36 / 0.37 | 0.86 / 0.36 / 0.51 |
| Levantine P / R / F1 | 0.66 / 0.70 / 0.68 | 0.27 / 0.70 / 0.39 |

*What happens and why.* **Accuracy falls by 15 points** because it is support-weighted: a class on which the system is only 36 % correct now makes up 36 % of the test set instead of 5 %, so the pooled count moves toward that class's poor rate, although nothing about the system changed. **Macro-F1 also falls, but through a different mechanism.** The Gulf class's weight is one quarter before and after and its recall is fixed, so its contribution does not shrink; its F1 actually *rises* (0.37 to 0.51) because its 30 false positives are diluted by 180 true positives. What drags macro-F1 down is the **Levantine** column, which now receives 250 misclassified Gulf utterances: Levantine precision collapses from 0.66 to 0.27 and its F1 halves. Macro-F1 is insensitive to how many test utterances a class has, but it is sensitive to where that class's errors land. The lesson of Section 8.11 stands: on the imbalanced set accuracy (0.85) hides the Gulf problem and macro-F1 (0.71) exposes it; on the balanced set both numbers show it, and the confusion matrix shows that the problem is specifically Gulf-to-Levantine confusion, the neighbouring-variety pattern of Exercise 1. Report both numbers, the support of every class, and the matrix.

---

## Exercise 3

**Task.** You are deploying a dialect identifier as a routing front end for a call centre. Describe the confidence threshold and fallback model you would use, justify why a confident wrong route is worse than a generic one, and list the metrics you would monitor in production.

**Suggested solution.**

*Threshold and fallback.* The identifier outputs a dialect label with a probability. First **calibrate** the probability on a held-out development set drawn from real call-centre audio (temperature scaling or isotonic regression), because a softmax score from a network trained on broadcast data is not a probability of being right on telephone speech (Section 8.11). Then choose the threshold τ on that development set by sweeping it and measuring the **final transcription WER of the whole routed system**, not the identifier's accuracy: for each τ, calls above τ go to the dialect-specific recognizer, calls below τ go to the fallback, and the WER of the resulting transcripts is computed per dialect. Pick the τ that minimizes the macro-average WER across dialects, subject to no dialect being worse than the fallback alone. Because identification accuracy rises with duration (ADI17 spotlight, Section 8.3), make the decision only after a minimum amount of speech (say 5 to 8 seconds) and re-evaluate it as the call proceeds; short greetings should never trigger a route. The **fallback** is a single robust **multi-dialect recognizer** trained on all the dialects the centre serves, with an MSA-only model used as fallback only if testing shows it works on the expected dialectal speech (the book's explicit caution). Other fallback options: run two candidate recognizers in parallel and keep the higher-confidence transcript, or ask the caller to choose a language in the IVR.

*Why a confident wrong route is worse than a generic one.* Routing errors are not symmetric. A generic multi-dialect model on a Najdi call gives a moderately degraded transcript, and the degradation is roughly uniform, known in advance, and measurable. A confident misroute sends the Najdi call to, say, the Egyptian recognizer, whose lexicon, language model and tokenizer were tuned away from Najdi: the transcript can be far worse than the generic one, it fails on exactly the dialect-specific words that mattered for the routing decision (the account-balance request of the opening scene), and the failure is *silent*, because the pipeline reports high confidence at every stage and there is no signal that anything went wrong. Routing also amplifies unfairness: the dialects the identifier handles worst (the rare, neighbouring ones of Exercise 1) are the ones most often misrouted, so their callers get the worst transcripts (Section 8.11, "Why It Matters"). An uncertain result that falls back is therefore a bounded, honest error; a confident wrong route is an unbounded, invisible one.

*Metrics to monitor in production.*

* Per-dialect **route rate**, **abstention (fallback) rate** and the **distribution of confidence scores**; a drift in these is the first sign that the call population or the audio channel changed.
* **Identifier accuracy and macro-F1 on a continuously sampled, human-labelled audit set**, with the confusion matrix, so that neighbouring-dialect confusions are visible.
* **Downstream WER (or CER) per routed model and per dialect** on the same audit set, compared with the fallback model on the same calls; the number that justifies the routing at all.
* **Calibration** (expected calibration error or a reliability diagram) of the confidence scores over time.
* **Task outcomes** that do not need transcripts: intent-detection accuracy, call-completion rate, transfers to a human agent, repeat calls, and customer-reported problems, broken down by predicted dialect and by confidence band.
* **Latency** of the identification decision and how much speech it consumed.
* Logging of predicted dialect, confidence, chosen recognizer and later errors under the privacy and retention policy of Chapter 13, with dialect never used for any purpose other than routing.

---

## Exercise 4

**Task.** A Saudi broadcast archive of televised panel debates is to be indexed by speaker. State which of the three speaker tasks each of these needs, and why: (a) labelling every stretch of a debate with the panellist who spoke it; (b) deciding whether a caller to a bank is the account holder; (c) naming which of a station's twelve regular presenters is speaking in a clip. For (a), name the metric you would report, say how you would report its parts, and give two facts about the scoring protocol that must be declared for the number to mean anything.

**Suggested solution.** (Section 8.6, Table 8.3, Figure 8.4.)

| Case | Task | Why |
|---|---|---|
| (a) labelling every stretch of a debate with who spoke it | **Speaker diarization** (who spoke when), followed, if the panellists' names are wanted rather than "Speaker 1, Speaker 2", by closed-set identification against an enrolled gallery of the panellists | The question is about *time*: partition the recording into turns and group them by speaker. Diarization does not need to know the speakers' names and handles an unknown number of them; overlapping speech in a debate is its hardest part |
| (b) is the caller the account holder? | **Speaker verification** | One test utterance, one *claimed* identity, a binary accept/reject decision at a threshold. It is biometric, so it must be paired with spoofing countermeasures and a legal basis (Section 8.6) |
| (c) which of twelve regular presenters is speaking | **Closed-set speaker identification** | One utterance compared against a fixed gallery of N = 12 enrolled speakers, returning the best match; if a guest may be speaking, it becomes open-set identification with a "none of the twelve" option |

*Metric for (a).* The **Diarization Error Rate (DER)**, reported **with its three components stated separately**: missed speech (reference speech not attributed to anyone), false-alarm speech (non-speech labelled as speech) and speaker confusion (speech attributed to the wrong speaker), each as a percentage of total reference speaker time, so that DER = missed + false alarm + confusion. Two systems with the same DER can fail in completely different ways (one misses quiet speakers, the other confuses two similar voices), and only the breakdown shows which. If the names are attached and transcripts are produced, add cpWER for the speaker-attributed transcript.

*Two protocol facts that must be declared* (any two of the following; the book names three):

1. **The collar**: the width of the no-score zone around every reference boundary (typically 0.25 s each side). A wider collar forgives boundary imprecision and lowers DER; results with different collars are not comparable.
2. **Whether overlapping speech was scored or ignored.** Panel debates contain a lot of overlap; ignoring it removes the hardest part of the task and can cut the DER substantially.
3. **Whether the number of speakers was given to the system or estimated.** Telling the system there are five panellists removes a major source of error.

Also declare the reference annotation source (human turn labels with overlap marked, since SADA and MGB-2 were not built as diarization benchmarks) and the scoring tool, so that another team can reproduce the number.

---

## Exercise 5

**Task.** You have 40 hours of noisy Saudi call-centre audio and a recognizer fine-tuned on clean speech. A colleague proposes a neural denoiser in front of it. Using the measured result in Section 8.7, say what you would expect to happen and explain the mechanism, describe the alternative you would try first and how you would build its training data, and state the single measurement that would settle the argument.

**Suggested solution.**

*What to expect.* The SADA experiment in Section 8.7 is the closest measured evidence: an XLS-R model fine-tuned on **clean** SADA had a WER of 51.64 % on the clean test portion and 60.95 % on the noisy portion; **denoising the noisy audio raised the WER to 64.46 %**, while a model fine-tuned on **noisy** SADA reached 58.95 % on the same noisy portion (Figure 8.6). I would therefore expect the denoiser to make the clean-trained recognizer *worse*, or at best not better, on the call-centre audio, even though the processed audio would sound cleaner to a human listener.

*Mechanism.* An enhancement model removes some of the noise but also **introduces artefacts**: it attenuates low-energy speech regions it mistakes for noise (weak consonants, fricative onsets, the very F2 transitions that carry emphasis), smears or suppresses parts of the spectrum, and leaves musical-noise residues. The recognizer was trained on natural clean speech and has never seen these artefacts, so the enhanced audio is, from its point of view, a new and unfamiliar channel. Enhancement errors can be divided into residual noise and newly introduced artefacts, and in the cited experiments the artefacts hurt recognition more than the noise did. Objective quality scores (SI-SDR, STOI, PESQ) can improve while the WER gets worse, because they measure signal similarity or perceived quality, not what the recognizer needs.

*The alternative to try first: noise-matched training.* Fine-tune the recognizer on speech that matches the deployment condition, rather than trying to make the deployment audio match the training condition. Building the training data: (1) take the 40 hours of call-centre audio, transcribe a portion (say 5 to 10 hours) with a careful pass, and use the rest either through pseudo-labelling by the current model with confidence filtering or as unlabeled audio for continued self-supervised pretraining (Chapter 6); (2) augment the existing clean fine-tuning data to look like the call centre: band-limit to the telephone band, downsample to 8 kHz, add noise sampled from **non-speech segments of the real call-centre recordings** at the SNR distribution measured on those calls, and add the handset and codec chain; (3) if a denoiser will nevertheless be part of the product, pass the training data through the same denoiser so that the recognizer learns its artefacts; (4) split speaker-disjoint, with a held-out test set of real, untouched call-centre audio labelled by dialect and by noise level.

*The single measurement that settles it.* **WER (with CER) on the same held-out set of real noisy call-centre calls, reported per dialect and per noise condition, for three systems: the clean-trained recognizer alone, the clean-trained recognizer with the denoiser in front, and the noise-matched recognizer without the denoiser.** Whichever gives the lowest WER on that set wins; no enhancement-quality metric can substitute for it, because the argument is about recognition, not about how the audio sounds.

---

### Flags and notes for the companion website

* Exercise 2's confusion matrix was transcribed from Figure 8.8 in the manuscript (counts 470/15/10/5, 20/255/20/5, 10/15/105/20, 4/3/25/18); the notebook reproduces the figure's accuracy 0.85 and macro-F1 0.71 exactly.
