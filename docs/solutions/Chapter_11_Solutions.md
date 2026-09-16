# Chapter 11 Solutions: Audio-Language Models (ALM) and Speech Agents

These solutions follow the numbering of the chapter's exercise list. Exercise 2 has a companion notebook.

Notebook for this chapter: [`Chapter_11_Exercise_02.ipynb`](Chapter_11_Exercise_02.ipynb).

---

## Exercise 1

**Task.** Write five structured instruction-tuning records for a single Arabic audio clip (transcribe, identify the dialect, translate into English, recognize the speaker's emotion, answer a question about the content), then explain in two or three sentences how this format teaches one model to select a task based on the instruction.

**Suggested solution.** The clip is the Saudi request of the Chapter 11 opening scene, imagined as a 4-second recording of a woman speaking calmly. The records follow the audio, instruction, target layout of Figure 11.4 (JSON lines, one record per line; the audio field is a path or identifier, never the waveform itself).

```json
{"audio": "clips/sau_0042.wav", "instruction": "اكتب ما قيل في هذا التسجيل كما نُطق.",
 "target": "لخّص لي المكالمة وقل لي إذا كان فيه موعد"}
{"audio": "clips/sau_0042.wav", "instruction": "Which Arabic variety is the speaker using? Answer with one label from: MSA, Egyptian, Gulf, Levantine, Maghrebi.",
 "target": "Gulf"}
{"audio": "clips/sau_0042.wav", "instruction": "Translate the speech into English.",
 "target": "Summarize the call for me and tell me whether there is an appointment."}
{"audio": "clips/sau_0042.wav", "instruction": "ما هي الحالة العاطفية للمتكلمة؟ اختر واحدة: محايد، سعيد، غاضب، حزين.",
 "target": "محايد"}
{"audio": "clips/sau_0042.wav", "instruction": "Answer the question about the recording: what two things does the speaker ask for?",
 "target": "A summary of the call, and whether an appointment was mentioned."}
```

Design notes that make the records usable: the transcription target keeps the dialectal spelling under one convention (CODA-style لخّص, فيه) rather than an MSA rewrite, so that the model learns to transcribe dialect rather than translate it; the dialect and emotion instructions state a closed label set, so that the targets are scorable; the instructions are written in both Arabic and English across the five records, so the model learns that the task is defined by the instruction's meaning and not by its language; and the emotion label is documented as annotator-perceived, not the speaker's self-report (Section 8.5).

*How this teaches task selection.* The five records share the identical audio input, so nothing in the acoustics tells the model which output is expected; the only thing that varies is the instruction, and the loss rewards a different target for each. To reduce the loss the model must therefore condition its output on the instruction, learning an internal mapping from instruction meaning to task, and because the same pattern is repeated across thousands of clips it generalizes to new wordings of the same requests (Section 11.3). This is what turns one encoder-connector-LLM stack into a multitask system, and it is also why evaluation must then probe each task separately: the model may have learned some task-instruction mappings well and others poorly.

---

## Exercise 2

**Task.** Implement a small Python router that classifies a free-text instruction as ASR, speech translation, speech question answering, dialect identification or emotion recognition, using simple English and Arabic keyword rules. Test it on at least eight instructions including dialectal, ambiguous and compound ones. Report the misrouted examples and explain why the keyword rules fail.

**Solution (notebook `Chapter_11_Exercise_02.ipynb`).**

*The router.* Five keyword lists (English plus MSA and dialectal Arabic forms), normalization (lower-case, diacritics removed, alif, ة/ه and ى/ي unified), one point per matching keyword, highest score wins, ties broken by list order, and ASR as the silent default when nothing matches.

*Test set and result (executed).* 16 instructions: 5 plain, 3 dialectal (Gulf and Egyptian), 4 ambiguous, 4 compound. **11 of 16 were routed as expected.** The five misroutes:

| Instruction | Expected | Routed | Why the rules failed |
|---|---|---|---|
| What is the tone of the announcement? | SER | SQA (tie SQA/SER, first wins) | *tone* is an emotion cue in one reading and a content cue in another; *what is the* is a question cue; a tie is broken arbitrarily |
| Where is the speaker from? | ADI | SQA | *where* is listed as a question word; the geographic-origin reading needs world knowledge, not a token |
| شو قال عن الطقس؟ (Levantine: what did he say about the weather?) | SQA | ASR (tie) | شو قال matches the ASR list ("what did he say") although the user wants an answer about content; the same dialect word votes for two tasks |
| اكتب لي ملخص المكالمة (write me a summary of the call) | SQA | ASR (tie) | اكتب 'write' is an ASR cue; ملخص 'summary' should override it, but counts are equal |
| حدد اللهجة ثم ترجم الكلام للإنجليزي (identify the dialect, then translate) | ST | ADI | a compound instruction; the dialect list matched more strings, so the *first* subtask won rather than the final deliverable |

The compound English instruction ("transcribe and then translate") happened to route to ST only because the ST list matched three phrases against one; the outcome depends on list lengths, not on meaning. "Tell me the dialect and whether the speaker sounds angry" has no single right label at all.

*Why keyword rules fail, in general.* (1) **Compound instructions**: rules have no notion of sequence or of which output the user finally wants, and some instructions (the Chapter 11 opening scene: summarize *and* check for an appointment) are two tasks that only a generative response can serve. (2) **Ambiguity of ordinary words**: *tone*, *where ... from*, *what did he say* mean different tasks in different contexts; keywords cannot see intent behind wording. (3) **Dialectal lexical variation**: each dialect has its own question words and verbs (وش / شو / ايش / إيه; منين; زعلان), so every form must be hand-listed and the list is never complete; normalization fixes spelling, not vocabulary. (4) **Collisions across lists**: the same dialect word (شو) sits in two task lists, and substring matching produces false hits (*who* in *whole*). (5) **Negation and scope**: "do not translate, just transcribe" is routed to translation. (6) **A silent default**: unmatched instructions become ASR instead of an explicit "unclear, please rephrase", the same confident-wrong-route problem as in Section 8.11. These are the reasons instruction-tuned audio-language models replace routers with a learned mapping from the whole instruction to the response (Exercise 1), at the price that the learned selection must then be evaluated per task and per dialect.

---

## Exercise 3

**Task.** Using a small worked example, explain how discrete audio tokens allow a language model to generate speech: what the neural audio codec produces, what the language model predicts, and how the codec decoder reconstructs the waveform. State one advantage and one risk of using this approach to generate Arabic speech.

**Suggested solution.** (Section 11.4, Figure 11.5.)

*Worked example.* Take one second of the reply مرحبا، كيف أساعدك؟ (marḥaban, kayfa usāʿiduk, 'hello, how can I help you?') at 16 kHz: 16,000 samples.

1. **What the codec produces.** A neural audio codec such as EnCodec has an encoder that compresses the waveform into a sequence of frames, typically 50 or 75 per second, and a residual vector quantizer that represents each frame by a small stack of integer codes chosen from fixed codebooks (say 8 codebooks of 1,024 entries each). One second of speech becomes about 75 frames × 8 integers = 600 integers instead of 16,000 real-valued samples. The first codebook carries the coarse content (roughly which sound is being made and by what kind of voice); later codebooks add finer acoustic detail. Some systems add a separate stream of *semantic* tokens (from a self-supervised model, HuBERT-style clusters) that capture linguistic content and longer structure, as in AudioLM.

2. **What the language model predicts.** Because the audio is now a sequence of integers from a finite vocabulary, it can be modelled exactly like text: the language model's vocabulary is extended with the audio codes (and possibly the semantic tokens), and the model is trained to predict the next token. Conditioned on a text or phoneme input ("say مرحبا، كيف أساعدك؟"), optionally a short acoustic prompt (a three-second clip that fixes the voice, as in VALL-E), and optionally an incoming speech stream (speech-to-speech), it generates the code sequence frame by frame. VALL-E predicts the first codebook autoregressively (75 steps for our second of audio) and fills in the remaining seven codebooks non-autoregressively; AudioLM generates semantic tokens first and then acoustic tokens conditioned on them.

3. **How the decoder reconstructs the waveform.** The predicted integer stack for each frame is looked up in the codebooks, summed across the residual stages to form the frame's latent vector, and the codec's decoder network (the counterpart of the vocoder in Section 9.5) turns the sequence of latent vectors back into 16,000 samples per second. If semantic tokens were used, an intermediate acoustic-generation model first converts them into acoustic codes. The result is speech in the prompted voice saying the requested words, without an explicit spectrogram stage.

*One advantage for Arabic.* The audio-to-audio route does not require an explicit text pipeline: a speech-to-speech model can respond to a Gulf question in a Gulf voice without transcription, diacritization and G2P, because the incoming audio already contains the spoken vowels and the output tokens encode pronunciation directly (Section 11.4, second decision). Zero-shot voice prompting also makes it possible to produce a consistent, natural dialect voice from a few seconds of speech, which no dialectal TTS corpus currently offers.

*One risk for Arabic.* The same property removes inspectability: there is no diacritized text to check, so a mispronounced or wrong-variety word (an MSA reply to a Gulf question, a mis-geminated word) is produced fluently and can only be caught by listening or by an ASR-based check whose own dialect errors confound the result (Section 11.4 evaluation paragraph). And because a three-second prompt suffices to clone a voice, the approach carries the impersonation and consent risks of Section 9.7 and Chapter 13 in an amplified form; an Arabic assistant should speak in a licensed, consented voice and label its speech as synthetic.

---

## Exercise 4

**Task.** Design a speech-agent loop for "Summarize this recorded Arabic meeting and tell me whether an appointment was proposed or confirmed during the meeting." Describe the perceive, plan, act and respond stages, naming the required model, tool or retrieval method for each, then identify two points at which a dialect-related recognition error would most seriously affect the final answer.

**Suggested solution.** (Section 11.5, Figure 11.6.)

**Perceive.** Input: the user's spoken instruction (Saudi dialect) plus a long meeting recording. Components: an audio-language model or a Whisper-class recognizer for the *instruction* (short, one speaker); for the *meeting*, a long-form pipeline: voice activity detection and segmentation, **speaker diarization** (pyannote-style, Section 8.6) so that turns are attributed, a **dialect-aware ASR** run per segment (a dialect identifier can route segments to a Gulf-adapted recognizer, with a multi-dialect fallback for low-confidence segments, Section 8.11), and timestamps kept for every word. Output of the stage: a speaker-attributed, time-stamped transcript plus the parsed instruction (two sub-goals: summary; appointment status).

**Plan.** The LLM at the core of the agent decomposes the instruction into steps: (1) produce an abstractive summary of the transcript; (2) search the transcript for appointment-related content; (3) decide, for each candidate, whether it was *proposed* or *confirmed*; (4) if a confirmed appointment is found, optionally check it against the calendar; (5) compose the answer in the user's variety. Planning is done by the language model with a tool list and a schema for each tool; a rule such as "always ground claims in transcript spans" is part of the plan.

**Act.** Tools and retrieval: an **Arabic summarization** step (the LLM itself, or a dedicated model such as AraBART, Section 8.10) over the transcript, chunked by topic if long; **retrieval** over the time-stamped transcript, using a dialect-aware query expansion for appointment vocabulary (موعد، نتقابل، الساعة، بكرة، الأسبوع الجاي; MSA and dialectal date and time expressions, Table 10.5) and returning spans with speaker and time; a **temporal-expression normalizer** that resolves "Tuesday at four" relative to the meeting date; a **calendar tool** (read-only) to check whether the slot exists; and a classification prompt that labels each retrieved span as proposal, confirmation, refusal or unrelated, citing the span. Every tool result is kept with its source so that the answer can quote it.

**Respond.** The agent composes a short Arabic answer in the user's dialect: the summary, then a clear verdict ("an appointment was proposed by X for Tuesday at four and confirmed by Y at 12:41" or "an appointment was proposed but not confirmed"), with the supporting quotes and timestamps; if the evidence is ambiguous it says so and offers to play the segment. The text goes through the TTS front end (diacritization or G2P for the chosen voice, Chapter 9) and is spoken back; the next user turn re-enters the loop. Logging of what was retrieved and which tools ran follows the privacy rules of Chapter 13, since a meeting recording is personal data of every participant.

**Two points where a dialect recognition error is most damaging.**

1. **The appointment decision itself.** The verdict rests on a handful of short, dialect-heavy phrases: تمام، خلاص، اتفقنا ('agreed'), ماشي، إن شاء الله (which can be a polite non-commitment), لا خلينا نشوف ('no, let's see'). Misrecognizing a negation particle (ما / مو / مش) or a confirmation word flips "proposed" into "confirmed" or hides the appointment entirely, and the retrieval step will not even surface a span whose key word was transcribed as an MSA near-neighbour. This is the single highest-stakes error in the loop, and it is exactly the kind of substitution an MSA-biased recognizer makes (Chapter 6, Exercise 5).
2. **Dates, times and names.** The value of the answer depends on when and with whom: dialect number words (اثنين / ثنين, عشرة / عشر), day names, relative expressions (بكرة، بعد بكرة، الجاي) and proper names are both hard for the recognizer and unrecoverable by the LLM once wrong, because a plausible date is as fluent as the right one. A recognition error here yields a confident answer with the wrong day, which is worse than no answer (Section 8.11).

Mitigations follow from the analysis: route segments to a dialect-adapted recognizer, pass n-best alternatives for the decision-critical spans, have the agent quote the audio timestamps so the user can verify, and evaluate the whole loop per dialect on real meetings with human judgments, not only the recognizer's WER (Section 11.7).

---

## Exercise 5

**Task.** Design an honest evaluation protocol for an Arabic audio-language model that claims strong ASR and dialect-identification performance: specify the real human-recorded speech data, how transcripts and dialect labels are obtained, how results are reported per dialect, the metrics, and how training-test contamination is investigated. Then explain how five evaluation shortcuts would be detected and prevented: model-generated gold labels, synthesized test audio, shared-pipeline leakage, training-test overlap, and unfair baseline comparisons.

**Suggested solution.** (Sections 11.7 and 11.8, Table 11.3, Table 11.4.)

*Real, human-recorded data.* A test suite, not one set: (a) spontaneous broadcast and conversational speech with dialect labels, from SADA (Saudi varieties, with environment labels) and Casablanca (eight dialects, gender and code-switching annotation), using their official test splits; (b) a read MSA control, FLEURS Arabic or Common Voice Arabic test, to separate register effects from dialect effects; (c) a small **newly recorded** set (a few hundred utterances across the claimed dialects, recorded for this evaluation, speakers consented, never published before the evaluation), which by construction cannot have been seen by any model; (d) noisy and telephone-band conditions represented, since the claim is about real speech. Every clip is human speech; no TTS output is in the test suite.

*Transcripts and dialect labels.* Transcripts produced by trained native transcribers under a published convention (Table 7.3: undiacritized, CODA-style dialect spelling, code-switching in the original script, tags for non-speech), with 10 % double-transcribed and the pairwise CER after normalization reported; dialect labels assigned by at least two native annotators per clip at the country or regional level defined in a stated taxonomy, with Fleiss' kappa reported and disagreements adjudicated or the clip marked "mixed" (Chapter 7, Exercise 3). Nothing in the references is generated by a model, and the provenance of every label is recorded in the data card.

*Reporting per dialect.* For each dialect and each condition (read/spontaneous, clean/noisy): WER and CER with the normalization script attached, dialect-identification accuracy and macro-F1 with the confusion matrix, the number of utterances, speakers and hours in that cell, and confidence intervals or significance tests against the baselines; a macro-average across dialects beside any pooled score; results on the newly recorded set reported separately; and representative failure examples (hallucinations, MSA shifts) with counts, following the OmniASR human-evaluation study's finding that WER explains under half of the variance in comprehensibility.

*Metrics.* ASR: WER and CER (Chapter 4 policy, diacritics removed, one script), plus a human comprehensibility rating on a sample; dialect identification: accuracy, macro-F1, per-class precision and recall, and the confusion matrix (Section 8.11); for instruction following (since the model is an ALM): task success on a fixed-choice set and, for open answers, a named human or model judge whose agreement with Arabic-speaking humans is measured and reported per dialect (Section 11.8.2).

*Investigating contamination.* (1) Exact and near-duplicate search of every test transcript against the model's training corpora where they are disclosed, and against public web text where they are not; (2) speaker and source-programme overlap checks between test sets and the model's known training sets; (3) a behavioural test: compare perplexity or recognition accuracy on the public test sets against the newly recorded set with matched difficulty; a large gap in favour of the public sets is evidence of exposure; (4) a memorization probe: prompt the model with the first half of a public test transcript and see whether it completes the second half; (5) report which of these were possible and label unknown overlap as unknown rather than absent.

*The five shortcuts.*

| Shortcut | How it is detected | How it is prevented |
|---|---|---|
| Model-generated gold labels | Provenance audit of the references: ask who produced each label and how it was verified; statistical signature (suspiciously uniform normalization, MSA-ward transcripts of dialect speech); agreement between the "gold" and a fresh human transcription of a sample | Require human-produced or human-verified references, publish the guideline and the inter-annotator agreement, and forbid using the evaluated model or its family to produce references |
| Synthesized test audio | Listen to a sample; check speaker and channel diversity (TTS is unnaturally clean and uniform); ask for the recording metadata (device, environment, consent); an anti-spoofing detector flags synthetic clips | Test only on real recordings; if synthetic sets are used for controlled probes, report them separately, name the synthesizer, and never let them replace real dialectal speech (Section 11.8.1) |
| Shared-pipeline leakage (the same synthesizer, normalizer or annotation model used for training data and test data) | Compare the model's performance on data produced by the shared pipeline against independently produced data; inspect the pipeline description for shared components | Produce test data with a different pipeline and different voices than the training data; disclose any shared component and test on other voices and real recordings (Section 11.7, item 3) |
| Training-test overlap | Exact and fuzzy transcript matching, speaker and source overlap checks, the behavioural gap between public and freshly recorded sets, memorization probes | Evaluate on a freshly recorded, unpublished set; use official test splits only when their independence from the training data can be confirmed; state confirmed separation versus unknown overlap explicitly (Section 11.8.3) |
| Unfair baseline comparisons | Check that every system received the same audio, the same prompt format and the same normalization and scoring; watch for baselines evaluated only through text output when speech quality is claimed, or for exact-match scoring that penalizes correct paraphrases | Fix one evaluation harness for all systems, publish prompts and scoring code, use matching-rule-aware metrics for open answers, and have an independent party rerun the baselines (Section 11.7, item 5) |

An evaluation that passes these checks can still show a strong model; what it cannot do is make a single impressive average stand in for per-dialect evidence on real speech.

---

### Flags and notes for the companion website

* Exercise 1's records refer to a hypothetical clip; if the website hosts a real Saudi clip with consent, replace the path and re-check the targets against the recording.
* Exercise 2's keyword lists are deliberately small; the notebook's failure table is the teaching point, and a fuller list would only move the failures, not remove them.
