# Chapter 10 Solutions: Speech Translation and Spoken Language Understanding

These solutions follow the numbering of the chapter's exercise list. Exercises 2, 3 and 4 have companion notebooks.

Notebooks for this chapter: [`Chapter_10_Exercise_02.ipynb`](Chapter_10_Exercise_02.ipynb), [`Chapter_10_Exercise_03.ipynb`](Chapter_10_Exercise_03.ipynb), [`Chapter_10_Exercise_04.ipynb`](Chapter_10_Exercise_04.ipynb).

---

## Exercise 1

**Task.** Draw the cascade and end-to-end speech-translation architectures for Arabic-to-English, and explain, with a concrete dialectal example, how a single recognition error in the cascade produces a wrong translation.

**Suggested solution.** (Section 10.1, Figure 10.1, Figure 10.2.) The two architectures, drawn as text diagrams:

```
CASCADE
  Arabic speech ──► [ASR: Arabic recognizer] ──► Arabic transcript ──► [MT: Arabic-to-English] ──► English text
                     (Whisper, a Conformer,          (inspectable,             (a text translation
                      an Arabic-adapted model)        correctable)              model)

END-TO-END (DIRECT)
  Arabic speech ──► [speech encoder ──► translation decoder] ──► English text
                     (one jointly trained model; no explicit Arabic transcript at inference)
```

The cascade exposes the transcript between the two boxes; the direct model does not. A speech-to-speech version adds a TTS box after the English text in the cascade, or a speech decoder in the direct model.

*A concrete dialectal error.* Figure 10.2's example, worked through. A Gulf speaker says أبغى أحجز رحلة بكرة (abghā aḥjiz riḥla bukra, 'I want to book a flight tomorrow'). An MSA-biased recognizer does not know the dialect verb أبغى (Table 2.7) and substitutes the nearest form it does know: أبقى (abqā, 'I stay'), one letter away (غ for ق, itself a plausible acoustic confusion because both are back consonants). The transcript is now أبقى أحجز رحلة بكرة, which is grammatical enough for the translation model to render fluently: "I'll stay and book a flight tomorrow", or, if it also re-reads بكرة as MSA بُكرة, something even further from the intent. The English is fluent, so nothing downstream signals a problem; the wrong word was chosen with confidence at the first stage and the second stage had no access to the audio that would have contradicted it. A direct model, given the audio, has no transcript to get wrong in this way, but it can still make the same lexical error internally, and then there is no intermediate representation to inspect (Table 10.1).

---

## Exercise 2

**Task.** Explain the quality-latency trade-off in simultaneous translation and the wait-k policy, then write a Python script that simulates wait-k with k = 3 for an Arabic transcript arriving one word per second, emit the English tokens with the fixed lag, and compute the Average Lagging. Explain what your value reflects.

**Solution (notebook `Chapter_10_Exercise_02.ipynb`).**

*Trade-off and policy.* A simultaneous system alternates between reading source words and writing target words. Waiting longer gives more context and better translations; writing earlier reduces delay but commits before the meaning is clear (verbs at the end of a clause, negation, a place name still to come). Wait-k fixes the compromise in advance: read k source words, then alternate write and read so the output stays k words behind the input (Section 10.3).

*Simulation.* Source: احجز رحلة إلى الرياض غدا صباحا من فضلك (8 words, one per second); a monotone English gloss with one token per source word (the notebook simulates the schedule, not a translation model). Under wait-k, target token j is written after g(j) = min(j + k minus 1, S) source words. With k = 3: nothing for 3 seconds, then "book" at t = 3 s, "a flight" at 4 s, "to" at 5 s, "Riyadh" at 6 s, "tomorrow" at 7 s, "morning" at 8 s, and the last two tokens at 8 s once the source has ended.

*Average Lagging.* AL = (1/τ) Σ_{j=1..τ} [ g(j) minus (j minus 1)/(T/S) ], where τ is the first target token written after the whole source was read. Executed: S = 8, T = 8, τ = 6, per-token lags all 3.0, **AL = 3.00 source words = 3.00 seconds** at one word per second. Sweeping k gives AL = 1, 2, 3, 5, 8 for k = 1, 2, 3, 5, 8.

*What the value reflects.* AL measures how far behind an idealized in-step policy the system's *schedule* runs, in source words (here also seconds): on average each English token appeared when three more Arabic words had been read than the ideal policy needed. It says nothing about translation quality, so it must be reported next to BLEU, chrF or COMET (Table 10.4). Its value depends on three declared choices: whether computation time is included (this simulation is non-computation-aware), how the audio is segmented into units (here an idealized one word per second), and the target-to-source length ratio, which for Arabic-to-English is above 1 because English uses more tokens (Table 4.4), so the ideal policy is credited with writing faster and the measured AL on real output drops below k. k = 1 gives the lowest latency with almost no right context; k = S is offline translation.

---

## Exercise 3

**Task.** Using TARIC-SLU or a small licensed set of task-oriented Arabic speech commands, annotate 20 utterances in Label Studio with an intent-and-slot ontology, export the JSON, compute a baseline inter-annotator agreement, and state which metric you would use for intent detection, slot filling and dialogue state tracking. If you use SADA, first verify that the utterances suit the ontology.

**Solution (notebook `Chapter_10_Exercise_03.ipynb`).**

*Data.* TARIC-SLU is distributed from the authors' site behind a download form (CC BY-NC 4.0), so the notebook uses **Speech-MASSIVE** (`FBK-MT/Speech-MASSIVE`, Arabic `ar-SA` training split of 115 human recordings, CC BY-NC-SA 4.0), the licensed command set the book itself names in Section 10.9; its Arabic text carries Gulf features (حقي, بكرة, ايش, شف لي). SADA was deliberately not used: its segments are broadcast conversation, not requests to a system, and the notebook's suitability check (gold intent in the ontology and at least one slot or a clear command) is the test one would apply to it.

*Ontology and selection.* 10 intents (transport_ticket, transport_taxi, transport_query, transport_traffic, calendar_set, calendar_query, alarm_set, alarm_query, weather_query, datetime_query) and 8 slot types (place_name, date, time, transport_type, event_name, timeofday, general_frequency, time_zone). 20 utterances whose gold intent is in the set were selected, and all 20 passed the suitability check.

*Label Studio project.* The notebook writes `slu_tasks.json` (audio path, transcript, id) and `slu_config.xml` (an `Audio`, a `Labels` block for slot spans over the transcript, a `Choices` block for the intent with an `other` option), and `parse_export()` reads the standard Label Studio export back into (intent, {slot: value}) per utterance.

*Agreement (executed).* Annotator A = the corpus gold labels restricted to the ontology; annotator B = a **simulated** second annotation (the gold with one transport intent confusion, two date/timeofday slot confusions and one dropped slot), labelled as such and to be replaced by a real export. Intent: raw agreement 0.95, **Cohen's kappa 0.943**. Slots: pairwise **F1 0.93** (P 0.95, R 0.91) on exact (type, value) matches with A as the reference. With real annotators the kappa will be lower and the disagreements will cluster on date versus timeofday and on which words belong to a place-name span, which is where the guideline should be tightened.

*Metrics.* Intent detection: **intent accuracy** (Eq. 10.1), with macro-F1 added when the intent set is imbalanced. Slot filling: **slot F1** over (type, value) pairs (Eq. 10.2), stating whether values are compared as raw spans or after normalization (Table 10.5: الرياض versus Riyadh, غدا versus غدًا, ٢ versus 2) and whether partial overlap counts. Dialogue state tracking: **joint goal accuracy** (Eq. 10.3), where one wrong, missing or extra value fails the whole turn, reported beside per-slot accuracy. For the agreement study itself, Cohen's kappa for the categorical intent and pairwise slot F1 with a stated reference direction and normalization, both with the sample size and ontology version.

---

## Exercise 4

**Task.** Design a cascaded SLU pipeline: transcribe 10 dialectal audio files, then use a zero-shot LLM prompt to act as a flight-booking assistant returning a fixed JSON schema. Report the invalid-JSON rate, missing-slot rate and wrong-slot-value rate against the ground truth, discuss whether failures come from recognition errors or prompt design, and compare the LLM cascade with an end-to-end approach when labeled dialect data is limited.

**Solution (notebook `Chapter_10_Exercise_04.ipynb`).**

*Pipeline.* Ten human-recorded Arabic travel requests from Speech-MASSIVE `ar-SA` (8 transport-domain utterances plus 2 out-of-domain controls) with gold intents and slots mapped to the assistant's schema (`book_ticket`, `book_taxi`, `transport_info`, `other`; slots `destination`, `date`, `time`, `transport_type`). Stage 1: Whisper (`openai/whisper-small` in the test run) transcribes each file. Stage 2: a fixed system prompt instructs an open instruction-tuned LLM (`Qwen/Qwen2.5-1.5B-Instruct` in the test run) to return only a JSON object in the stated schema, copying slot values verbatim in Arabic and using null for absent slots. The LLM is run twice: on the **ASR transcript** (the real cascade) and on the **gold transcript** (an oracle that isolates prompt and model failures from recognition failures).

*Metrics.* Invalid-JSON rate (outputs that do not parse into an object with the required keys); missing-slot rate over the gold slots (null or omitted); wrong-slot-value rate over the gold slots the model did fill, after a stated normalization (diacritics and punctuation removed, alif, ة/ه and ى/ي unified, the definite article ignored); and intent accuracy.

*Measured result in the test run* (10 utterances; the numbers are specific to these two models and will change with others):

| Measure | LLM on the ASR transcript (the cascade) | LLM on the gold transcript (oracle) |
|---|---|---|
| Invalid-JSON rate | 10 % (1 of 10: an empty `{}` for an out-of-domain utterance) | 0 % |
| Intent accuracy | 50 % | 50 % |
| Missing-slot rate (of 10 gold slots) | 20 % | 10 % |
| Wrong-slot-value rate (of the gold slots that were filled) | 50 % | 33 % |
| Whisper-small WER on the 10 utterances | 40.0 % (14 substitutions, no deletions or insertions) | |

Reading the side-by-side output: on the ASR transcript, قطار 'train' was heard as كوستور and كتار, so a `book_ticket` request became `other` and a train became a taxi (recognition errors); on the gold transcript the LLM still labelled three `transport_info` and `book_ticket` requests as `book_taxi`, wrote `"taxi"` and `"Taxi"` in Latin letters although the prompt asked for verbatim Arabic, and invented an `origin` key (prompt and model failures). One caveat on the ground truth: MASSIVE marks both places in الرجعة رحلة الخبر إلى الرياض with the same `place_name` label, so the mapping to `destination` is a convention of this notebook (first place name) and the LLM's choice of الرياض as destination is defensible; slot definitions of this kind must be written down before scoring (Table 10.5).

*Recognition errors or prompt design?* The two columns separate the causes. Whatever is wrong on the gold transcript is the prompt's or the LLM's fault: invalid JSON (prose around the object, a code fence, a wrong key), an intent outside the inventory, slot values translated into English or MSA despite the instruction, or dialect time words (بكرة, الليلة) not recognized as dates and times. The additional errors that appear only on the ASR transcript are the cascade's propagation of recognition errors (Figure 10.2): a misheard place name becomes a wrong `destination`, a dropped time phrase becomes a missing `time`. Each cause has a different remedy: dialect-adapted recognition or n-best hypotheses for the first, a stricter prompt, schema-constrained decoding or a JSON repair step for the second, and a normalization and grounding stage after extraction (Table 10.5) for value mismatches that are not really errors.

*LLM cascade versus end-to-end SLU with little labeled dialect data.* The cascade needs no labeled dialect data for the understanding stage (zero-shot), adapts to a new schema by editing the prompt, and keeps a transcript that makes every failure inspectable and attributable; its weaknesses are that recognition errors pass through unchanged, that nothing guarantees the output format unless it is enforced, that transcripts may leave the device to an LLM service (Section 10.8), and that its ceiling is set by dialect ASR quality and by the LLM's knowledge of dialect vocabulary. End-to-end SLU maps speech directly to intents and slots, can exploit acoustic cues a transcript loses, runs on device and fixes the output format by construction, but it needs hundreds to thousands of labeled dialect utterances per domain (Speech-MASSIVE Arabic offers 115 training recordings), and its errors are harder to attribute. With scarce dialect labels the cascade is the pragmatic choice, and its main weakness, dialect recognition, is exactly where Chapter 6's adaptation methods apply without any SLU labels; once a few thousand labeled dialect utterances exist, the end-to-end model should be compared on the same test set with intent accuracy, slot F1 and joint goal accuracy, per dialect.

---

## Exercise 5

**Task.** Design an evaluation for an Arabic speech-translation system that will face dialectal and code-switched input. Specify the test data and its dialect coverage, the automatic metrics and the human evaluation, the latency metric if it is streaming, and how you would report results per dialect.

**Suggested solution.** (Sections 10.5 and 10.6, Table 10.2, Table 10.4.)

*Test data and dialect coverage.* A suite rather than one set, with Arabic as the **source** and English as the target, each part with speaker-disjoint official splits and a stated version: (a) MSA read speech, CoVoST 2 Arabic-to-English test, as a control for register; (b) spontaneous dialectal speech with human English references: the IWSLT dialectal speech-translation data (Tunisian and North Levantine to English) and, for Gulf and Egyptian, newly commissioned English translations of segments from SADA and Casablanca; (c) code-switched speech: TEDxTN (Tunisian Arabic, French and English) and ZAEBUC-Spoken (Arabic and English meetings), whose transcripts mark the switches; (d) a noisy and telephone-band subset. Every clip is real speech; every English reference is human-produced by translators who understand the dialect and instructed to preserve the meaning of dialectal expressions; the audio-transcript alignment is checked on a sample (the IWSLT 2026 metrics study found a third of samples with audio-text mismatches, Section 10.5). Coverage is documented per dialect: hours, speakers, share of code-switched utterances, recording condition.

*Automatic metrics.* **SacreBLEU with its signature** (tokenization, case, smoothing) as the standard word-level score; **chrF** beside it, because it gives partial credit for morphology and spelling variation and is the right complement whenever Arabic is involved; **COMET** with the exact checkpoint named, understood as a learned metric whose reliability on dialectal and code-switched input has not been established; and, because it is a cascade or a direct model facing dialect, the **WER of any intermediate transcript** per dialect, so that translation errors can be attributed to recognition where a transcript exists. One normalization procedure for all systems, published with the scores.

*Human evaluation.* Direct assessment of **adequacy** (meaning preserved) and **fluency** on a stratified sample per dialect, by bilingual raters who are native speakers of the dialect, with the source audio available to them (not only the transcript), at least two raters per item and inter-rater agreement reported; targeted checks on code-switched utterances (was the English span kept, was the French span translated, were names preserved) and on dialect-specific expressions (a list of idioms and function words that MSA-trained systems mistranslate, Figure 10.2). For a speech-to-speech system, add MOS naturalness and ASR-BLEU on the spoken output (Section 11.4).

*Latency, if streaming.* **Average Lagging** (Exercise 2) as the primary latency metric, reported together with the quality metrics on the same test set, with the computation-aware and non-computation-aware versions both given, the segmentation of the audio stated (manual sentence segmentation versus continuous long-form), and the policy's k or its learned equivalent; a latency-quality curve over several operating points rather than a single number.

*Reporting per dialect.* One row per dialect and per condition (read/spontaneous, clean/noisy, monolingual/code-switched): BLEU with signature, chrF, COMET, intermediate WER, AL if streaming, human adequacy and fluency with agreement, and the number of utterances and speakers; a macro-average across dialects next to any pooled score; the same systems, references, normalization and scoring code for every row; and an error analysis on the dialect rows that separates recognition errors, mistranslated dialect lexemes, and code-switch handling. Nothing measured on MSA read speech is presented as evidence about dialectal or code-switched performance.

---

### Flags and notes for the companion website

* Exercises 3 and 4 use Speech-MASSIVE Arabic (CC BY-NC-SA 4.0) as the licensed command set; TARIC-SLU can be substituted once downloaded from the authors' site, with the notebook's loader adapted to its format.
* Exercise 4's rates depend on the recognizer and the LLM; the notebook prints the model names beside the numbers so that any republication states them.
