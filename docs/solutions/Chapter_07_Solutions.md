# Chapter 7 Solutions: Arabic Speech Corpora, Annotation, and Benchmarks

These solutions follow the numbering of the chapter's exercise list. Exercises 3 and 4 have companion notebooks.

Notebooks for this chapter: [`Chapter_07_Exercise_03.ipynb`](Chapter_07_Exercise_03.ipynb), [`Chapter_07_Exercise_04.ipynb`](Chapter_07_Exercise_04.ipynb).

---

## Exercise 1

**Task.** Given the goal of a Gulf-dialect voice assistant, select two corpora from Table 7.1 and justify each by domain, dialect and licence. Describe how you would filter the data to isolate the target sub-dialects (for example separating Eastern or Gulf Saudi speech from other Saudi varieties in SADA using its dialect metadata), and define the training, development and test splits.

**Suggested solution.**

*Corpus 1: SADA (about 668 h, predominantly Saudi dialects, television broadcast, CC BY-NC-SA 4.0).* Domain: it is the only large corpus in Table 7.1 with **spontaneous** Saudi speech, and an assistant hears spontaneous speech, not read prompts. Dialect: its metadata labels segments by Saudi variety (Najdi, Hijazi, Khaliji, and others; Section 3.10 and Section 8.6), which is exactly what allows sub-dialect filtering. Licence: CC BY-NC-SA 4.0 permits research and prototyping with attribution and share-alike; it does **not** permit a commercial product, so a commercial assistant would need a separate agreement or its own collection, and this must be stated in the plan.

*Corpus 2: the LDC Gulf Arabic conversational telephone corpus (about 47 h, Gulf dialect, 8 kHz telephone conversations, LDC licence).* Domain: unscripted two-party conversation, the closest match in the catalogue to how people actually address an assistant, and telephone band, which also covers the phone-call channel an assistant may run on. Dialect: labelled Gulf Arabic, so it needs no filtering. Licence: a paid LDC licence; LDC offers commercial licensing for many of its corpora, so, unlike SADA, it may be usable in a product, but the terms for this specific corpus must be confirmed with LDC. Alternatives considered: SAAVB is Saudi-accented but **read MSA**, so it teaches the acoustics of Saudi speakers but not dialectal vocabulary; Casablanca has an Emirati subset but is CC BY-NC-ND (no derivatives, no commercial use) and currently has no training split; Common Voice is CC0 but mostly read MSA.

*Filtering SADA to the target sub-dialects.* Read the segment metadata (dialect, speaker, gender, programme, environment). Keep only segments whose dialect label is in the target set, for example {Khaliji, Eastern Saudi} for a Gulf-coast assistant, or {Najdi, Khaliji} for a Riyadh-plus-Gulf product, and drop segments labelled Hijazi, Southern, Yemeni, Egyptian or Levantine rather than using "all Saudi". Also drop segments labelled as overlapping speech or music-backed if the assistant will run on a near-field microphone, or keep them in a separate robustness test set. Record the exact filter (label values, version of the metadata file) so that the subset is reproducible, and report the resulting hours per label.

*Splits.* Follow the leak-free recipe of Section 7.3.4: group by **speaker** and by **programme** (segments from one programme share channel, studio and topic), shuffle the speaker list with a recorded seed, assign whole speakers to test until it holds about 2 to 3 hours with at least 10 speakers of the target sub-dialects and both genders, then development the same size, then training. Check by set intersection that no speaker or programme crosses a boundary. For the LDC Gulf corpus, assign whole calls (both sides) to one split, roughly 80/10/10 by calls, speakers disjoint. Keep the two corpora's test sets separate so that broadcast and telephone performance can be reported per condition, and publish the split files.

---

## Exercise 2

**Task.** Draft a one-page transcription guideline for Egyptian Arabic spontaneous speech. State your decisions on diacritization, dialect spelling (with one example resolved), code-switching, numbers and non-speech markup.

**Suggested solution (a one-page guideline).**

**Transcription guideline: Egyptian Arabic spontaneous speech, version 1.0**

1. **Scope.** Verbatim transcription of what was said, in the speaker's variety. Do not "correct" dialect to MSA, do not omit repetitions, and do not add words the speaker did not say.
2. **Diacritization.** None. Write undiacritized text. Exception: add a shadda only where it disambiguates a word that is otherwise unreadable in context (rare); never add case endings.
3. **Dialect spelling: follow Egyptian CODA.** Write each dialect word in one conventional form even if pronunciations vary. Spell etymologically where CODA does: ق is written ق although pronounced /ʔ/ (قال, not أال); ج is written ج (جميل); ث and ذ keep their letters even when said as /s/ or /z/. Function words and dialect-specific words take their fixed CODA spelling. *Resolved example:* the demonstrative /kida/ 'like this' is written **كده** (with final ه), not كدا or كدة, following CODA; the negation /miʃ/ is written **مش**; the future prefix is attached, **هيروح** 'he will go'.
4. **Letter forms.** Keep hamza forms as written in standard orthography (أ, إ, آ distinct from ا) where the word has a standard form; keep ة and ى. The evaluation script, not the transcriber, decides what to normalize.
5. **Code-switching.** English or French words are written in **Latin script in their standard spelling** (I sent the email → بعتت الـ email), and tagged inline as `<en>email</en>` when the language must be recoverable. Arabized loanwords that have a conventional Arabic spelling (تليفون, كمبيوتر) are written in Arabic. MSA stretches inside dialect speech are transcribed as said, with no tag; if the project needs register labels, add the utterance-level L0 to L4 dialectness scale of ZAEBUC-Spoken as a separate field.
6. **Numbers.** Write numbers as **words, as spoken** (تلاتة, not 3 or ٣; عشرين جنيه). Dates, times and phone numbers likewise as spoken. Digits are never used in the transcript.
7. **Disfluencies.** Keep fillers (يعني, إيه, أمم), repetitions (أنا أنا رحت) and false starts; mark a cut-off word with a trailing hyphen inside the word token (كتـ-).
8. **Non-speech markup.** One tag per event, in square brackets, in a fixed inventory: `[noise]`, `[music]`, `[laughter]`, `[overlap]` (mark the start of overlapped speech; transcribe the dominant speaker), `[inaudible]` (unrecoverable), `[foreign]` (a language other than Arabic, English or French). No other tags. Tags are removed before WER scoring.
9. **Segmentation.** Segments of 3 to 10 seconds at pauses or turn boundaries; never cut inside a word. One speaker per segment where possible; multi-speaker segments get `[overlap]`.
10. **Quality control.** 10 % of the material is transcribed independently by a second annotator; pairwise CER is computed after the evaluation normalization; recurring disagreements update this guideline and bump its version number, which is stored with every transcript.

---

## Exercise 3

**Task.** Three annotators label 20 clips for dialect from four classes. Compute the inter-annotator agreement with a standard library, provide a small sample of labels, report the score, say what value would indicate usable agreement, and list what a one-page data card must contain.

**Solution (notebook `Chapter_07_Exercise_03.ipynb`).**

*Sample of labels (illustrative, 20 clips, four classes MSA, Egyptian, Gulf, Levantine, three annotators).* The notebook lists all twenty; the disagreements were placed on the pairs Chapter 8 predicts to be hardest, Gulf versus Levantine and MSA versus a dialect in mixed speech. Example rows: clip_06 (Gulf, Levantine, Gulf), clip_14 (MSA, Egyptian, MSA), clip_20 (Gulf, Levantine, Gulf).

*Scores (executed).*

| Measure | Value |
|---|---|
| Fleiss' kappa (statsmodels `fleiss_kappa`, three raters) | **0.687** |
| Raw agreement (all three identical) | 0.65 |
| Cohen's kappa A1 vs A2 / A1 vs A3 / A2 vs A3 (scikit-learn) | 0.733 / 0.797 / 0.533 |

The A1 versus A2 confusion matrix shows the disagreements concentrated in the Gulf/Levantine cells (3 of the 7 disagreements) and MSA/Egyptian (1), which is the pattern to look for.

*What value indicates usable agreement.* There is no universal threshold (Section 7.5.3). By the common Landis and Koch bands, 0.61 to 0.80 is "substantial", so a Fleiss' kappa around **0.6 or higher** on a pilot is usually treated as usable for **training labels** in a four-class dialect task, provided the confusion matrix shows disagreement concentrated on genuinely ambiguous pairs rather than scattered; a **test set** should have every disagreement adjudicated rather than accepted at any kappa. Below about 0.4 the guideline needs revision (class definitions for mixed MSA-dialect speech, or clips too short to carry evidence), not more annotators. Also report the pairwise values: here A2 agrees markedly less with the others (0.53), which points to one annotator's understanding of the Gulf/Levantine boundary rather than to a bad guideline.

*The one-page data card must contain:* purpose and intended and unsuitable uses; composition (clips, total duration, clips and minutes per class, clip-length distribution); source and collection (programme or platform, dates, consent and licence of the source, ethics approval); the label taxonomy with definitions and the rule for mixed and unclear clips; the annotation process (number and background of annotators including their native varieties, guideline version, independent labelling, adjudication rule); agreement (Fleiss' and pairwise kappa, sample size, confusion matrix, how disagreements were resolved); splits (speaker- or programme-disjoint, sizes per class); speaker and demographic metadata (which fields, self-reported or assigned, counts per group); known limitations (imbalance, channel shortcuts, dialects not covered); licence, access conditions, version, contact and maintenance.

---

## Exercise 4

**Task.** Audit a public Arabic corpus for bias: extract its metadata and compute the hours-per-speaker ratio for each dialect and each gender where available, identify the group with the largest deficit, and propose a concrete sampling or reweighting strategy. If the corpus does not expose gender or dialect metadata, state that limitation and audit only the available fields.

**Solution (notebook `Chapter_07_Exercise_04.ipynb`).**

*Data flag.* The official SADA metadata (Kaggle) requires a login, so the notebook wires in three sources with one audit function: (A) the official SADA CSVs, uploaded by the reader (code path present, not executed here); (B) a community-redistributed SADA2022 subset on the Hugging Face Hub, 496 segments (default; executed); (C) the FLEURS Arabic TSVs (executed). Column names are detected by keyword and the notebook prints which of `speaker`, `dialect`, `gender` it found.

*Measured audit, source B (SADA subset, 0.46 h in total; this is a sample, not the corpus).*

| Field | Groups (hours, share) | Largest deficit | Limitation |
|---|---|---|---|
| dialect | Saudi 0.303 h (66 %); Egyptian 0.153 h (34 %) | Egyptian, 0.15 h below Saudi | only two dialect labels in the subset; the full corpus distinguishes Saudi varieties |
| gender | Male 0.355 h (78 %); Female 0.100 h (22 %) | **Female**, 0.26 h below male; within each dialect female speech is about a quarter of the hours | |
| speaker | not available | | **hours per speaker cannot be computed** on this subset; the official CSVs carry a speaker field and the same code computes it |

*Measured audit, source C (FLEURS Arabic, 8.23 h across train, dev and test).* No dialect and no speaker field (stated limitation; FLEURS is MSA read speech). Gender: FEMALE 7.07 h (86 %) versus MALE 1.15 h (14 %), so the largest deficit is **male speech**, 5.9 h below female, and a system evaluated only on FLEURS Arabic is mostly evaluated on female voices.

*Proposed strategy (concrete).* Using the deficit group identified by the audit (female speakers in the SADA subset; male speakers in FLEURS; on the full SADA, whichever sub-dialect by gender cell the per-speaker table flags):

1. **Sampling.** Keep all majority data and draw training batches with temperature sampling over the group, p(group) ∝ hours^0.5, or oversample the deficit group by the factor the notebook prints (3.6 for female speech in the subset; capped at about 4), with speed perturbation and SpecAugment so repeats are not identical.
2. **Reweighting.** Multiply each utterance's loss by the inverse of its group's share of hours, normalized (the notebook's "reweight" column: 1.56 for female, 0.44 for male in the subset), so that every group contributes equally to the gradient.
3. **Evaluation.** Ensure the development and test sets contain enough *speakers* of the deficit group to report its WER, and report the macro-average across groups beside the pooled number.
4. **Collection.** Neither remedy adds acoustic variety; a group with few speakers remains a group with few speakers however it is weighted. The audit's real product is a recording plan that recruits new speakers in the deficit cell, and the plan should be stated in the data card.

---

## Exercise 5

**Task.** Design a consent and licensing plan for a new dialectal collection: state what the consent form must cover, how you would protect speaker privacy, and which licence you would release under and why.

**Suggested solution.**

*Before anything is recorded.* Obtain IRB or research-ethics approval (Section 7.6), confirm the legal basis for processing voice data under the applicable law (in Saudi Arabia the Personal Data Protection Law treats biometric data used for identification as sensitive), and have the ethics or data-protection office review the consent form and the licence together, because the licence cannot promise more than the consent allowed.

*What the consent form must cover.* In plain language, in the participant's own dialect where possible: what is recorded (voice, and any metadata such as region, age band, gender) and for how long a session; the purpose (building a speech corpus for research and technology development); the specific **uses**, named explicitly: training and evaluating speech recognition and dialect identification models, and, as separate opt-in boxes, synthesis or voice-cloning research and commercial use; **who may receive the data** (approved researchers only, or public release); how it will be released (with a coded speaker ID, never the name) and the fact that a public release cannot be fully recalled once downloaded; retention period and storage location; the right to withdraw and its limits (data can be removed from future releases and from the project's servers, but copies already distributed may persist); that the voice may remain recognizable to people who know the speaker even without a name; compensation; and a contact for questions and complaints. Consent to participate and consent to each downstream use are recorded separately, and the signed forms are stored apart from the audio.

*Protecting privacy.* Replace names with speaker codes at ingestion and keep the key in a separate, access-controlled store; collect only the metadata the project needs (region and gender for balancing, an age band rather than a birth date); review transcripts for incidental personal information (names of third parties, phone numbers, addresses) and redact both audio and text with a `[redacted]` tag; drop or restrict any segment where the speaker asks; prohibit re-identification attempts in the data-use agreement; and for material that cannot be released safely offer a restricted-access tier under a data-use agreement, or a speaker-anonymized version evaluated against a speaker-verification attack rather than assumed private (VoicePrivacy). State in the data card that pseudonymization is not anonymization.

*Licence.* For the openly released tier, **CC BY 4.0** if the consent covers commercial use, because the point of a new dialectal collection is to fill the long tail (Section 7.7), and a permissive licence is what lets the widest range of researchers and product teams use it; attribution requirements keep provenance visible. If consent covers research only, **CC BY-NC-SA 4.0** (the SADA choice), which permits research reuse and derivatives while excluding products, and whose share-alike clause keeps derived corpora open. Avoid ND (no derivatives), which blocks the resampling, segmentation and annotation that every downstream project needs (the Casablanca limitation). The restricted tier is released under a signed data-use agreement rather than a public licence. Whatever is chosen, the licence must be identical to what the consent form told participants, it must be attached to every release version, and derived releases must respect it.

---

### Flags and notes for the companion website

* Exercise 4's default data source is an unofficial subset of SADA on the Hugging Face Hub; the audit on the full corpus requires the Kaggle release, and the notebook's Path A is provided for it but was not executed.
* The illustrative annotator labels in Exercise 3 are synthetic and are labelled as such in the notebook.
