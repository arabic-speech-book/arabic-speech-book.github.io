# Chapter 1 Solutions: Speech Technologies and the Arabic Challenge

These solutions follow the numbering of the chapter's exercise list. Open-ended items are labelled **Suggested solution** because more than one good answer exists. Numerical items show the calculation. Where a companion notebook is involved, the notebook is named and its measured results are quoted with the exact settings that produced them.

Notebooks for this chapter: [`Chapter_01_Exercise_02.ipynb`](Chapter_01_Exercise_02.ipynb), [`Chapter_01_Exercise_04.ipynb`](Chapter_01_Exercise_04.ipynb).

---

## Exercise 1

**Task.** Select five speech products or services, at least two of them Arabic-capable. For each, tabulate the input, the output, the speech task or tasks from Table 1.1, the likely metric, and one Arabic-specific risk; for any voice assistant, identify the chain of tasks involved.

**Suggested solution.** Any five real products are acceptable; the point is to map each one onto Table 1.1 and to name a risk that is specific to Arabic. The table below uses products that were publicly available when the book was written. Product capabilities change, so verify the Arabic claims on the vendor's current documentation before citing them.

| Product or service | Input | Output | Task(s) from Table 1.1 | Likely metric | One Arabic-specific risk |
|---|---|---|---|---|---|
| Amazon Alexa, Arabic (Khaleeji) voice | Waveform (wake word plus request) | Action and spoken reply | Speech command recognition (wake word), ASR, SLU, TTS | Wake-word accuracy and false-alarm rate; WER; intent accuracy and slot F1; MOS for the reply | **Dialect mismatch**: a Khaleeji-tuned assistant meets Egyptian or Maghrebi users; Table 2.8 shows that even qāf differs (/g/ vs /ʔ/) |
| Apple Siri (Arabic) | Waveform | Action and spoken reply | Speech command recognition, ASR, SLU, TTS; speaker verification for "Hey Siri" personalization | As above plus EER for the voice-match step | **Code-switching**: Gulf users mix English product names and Arabic verbs in one request ("افتح الـ calendar"), which a monolingual lexicon and LM handle badly |
| YouTube automatic captions (Arabic) | Waveform (video soundtrack) | Time-aligned text | ASR (with implicit diarization for turn breaks) | WER and CER, reported per dialect | **Diacritization and normalization**: captions are undiacritized, so عمان (Amman) and عمان (Oman) are indistinguishable, and scoring depends on the normalization policy of Table 4.2 |
| Microsoft Azure Neural TTS, Arabic voices (used by screen readers) | Text | Waveform | TTS | MOS (naturalness), intelligibility via ASR-based WER cross-check | **Diacritization**: the input text is undiacritized, so the front end must guess between عِلْم, عَلَم and عَلَّمَ (Section 1.5.2); a wrong guess changes the meaning for a blind user |
| Zoom translated captions (Arabic to English) | Waveform | Text in another language | ASR then speech translation (cascade); diarization to attribute turns | BLEU or COMET on the translation, WER on the intermediate transcript, latency (Average Lagging) if streaming | **Dialect mismatch propagating through a cascade**: a misrecognized dialect word (Figure 10.2, أبغى heard as أبقى) becomes a fluent but wrong English sentence |

**The voice-assistant chain.** For Alexa or Siri the tasks run in this order (Figure 1.2): (1) wake-word detection, a closed-vocabulary speech command recognition task that runs continuously on the device; (2) optional speaker verification, so that the assistant knows whose calendar to open; (3) ASR, turning the request into text; (4) SLU, extracting the intent (for example `set_alarm`) and the slots (time, day); (5) a dialogue manager that decides and acts; and (6) TTS, which speaks the reply through the Arabic front end of Chapter 9. Each stage has its own metric, and an error in an early stage (a dialectal word misrecognized) propagates to every later one.

---

## Exercise 2

**Task.** Using Table 1.3, compute the WER by hand, reporting S, D, I, and N. Then recompute WER and CER with the companion notebook on its clips, stating the normalization applied and whether diacritics were scored.

**Part A: by hand.** Table 1.3 aligns the five-word reference وين أقرب محطة بنزين هنا with the hypothesis أين أقرب محطة وقود.

| Position | Reference | Hypothesis | Operation |
|---|---|---|---|
| 1 | وين | أين | substitution |
| 2 | أقرب | أقرب | correct |
| 3 | محطة | محطة | correct |
| 4 | بنزين | وقود | substitution |
| 5 | هنا | (none) | deletion |

So **S = 2, D = 1, I = 0, N = 5**, and by Equation 1.1

WER = (S + D + I) / N = (2 + 1 + 0) / 5 = 0.60 = **60 %**.

The CER on the same pair is lower because position 1 is a near miss (one letter differs) while position 4 is a total miss. Counting spaces as characters (the `jiwer` convention) the minimum edit distance is 10 over N = 23 characters, so CER = 43.5 %; ignoring spaces it is 9 edits over 19 letters, CER = 47.4 %. Whichever convention is used must be stated, which is the lesson of the exercise.

**Part B: the notebook on real clips.** The companion clips referred to in the book were **not included** in the material supplied for these solutions, so the notebook uses a stand-in: the first 20 clips of the FLEURS Arabic (`ar_eg`) test split, an openly licensed (CC BY 4.0) read-speech benchmark listed in Table 7.1. The notebook also accepts your own clips plus a reference TSV. When the companion clips become available on the companion website, switch `USE_UPLOAD = True` and load them; the scoring code does not change.

Measured result from the notebook as tested (zero-shot `openai/whisper-small`, `language=ar`, greedy decoding, CPU, 20 clips, N = 411 reference words):

| Normalization policy | WER | S / D / I | CER |
|---|---|---|---|
| `strict`: NFC, punctuation removed, tatweel removed, **diacritics removed**, no letter unification | **22.14 %** | 84 / 5 / 2 | **6.05 %** |
| `lenient`: `strict` plus alif forms unified, ة to ه, ى to ي, Arabic-Indic digits to Western | 21.65 % | 82 / 5 / 2 | 5.92 % |

Diacritics were **not scored** under either policy (they were stripped from both reference and hypothesis), because FLEURS references are only partly diacritized and Whisper output is not. The same normalization function is applied to reference and hypothesis, and the function is printed in the notebook so that the number is reproducible. The half-point gap between the two policies is the share of "errors" that are spelling conventions (hamza on alif, ة versus ه) rather than misrecognitions, exactly the effect the Reproducibility Note warns about. Note also that CER is far below WER: most wrong words differ from the reference in one or two letters (a dropped hamza, a wrong vowel letter), so CER distinguishes near misses from total misses as the chapter says it should.

---

## Exercise 3

**Task.** Explain the difference between speech command recognition and spoken language understanding, and between speaker profiling and speaker verification, naming the dataset and metric each would use from Table 1.1, and one privacy or fairness risk that each task carries.

**Solution.**

*Speech command recognition versus SLU.* Command recognition classifies an utterance into one of a small, fixed set of commands (on, off, up, a wake word). It is a closed-vocabulary classification problem: the output space is the command list. SLU instead extracts meaning from open, spontaneous speech, producing an intent plus slot values ("book a flight from Riyadh to Jeddah tomorrow" gives intent `book_flight`, slots `origin`, `destination`, `date`). SLU is harder because the input vocabulary is open, the slots have open values (any city, any date), and the same intent can be expressed in many ways and many dialects.

| Task | Table 1.1 dataset | Table 1.1 metric | One privacy or fairness risk |
|---|---|---|---|
| Speech command recognition | ArabAlg; AraSpot | Accuracy | **Fairness**: commands are usually recorded in MSA by speakers from one region (Section 8.8 notes the Arabic Speech Commands set uses Syrian speakers), so a Gulf or Maghrebi pronunciation of the same command may be rejected more often; an always-on wake word also raises the privacy question of what audio is buffered before the trigger |
| Spoken language understanding | TARIC-SLU (Tunisian, railway domain) | Intent accuracy, slot F1, SemER | **Privacy**: slot values are personal (names, destinations, dates), and cascaded systems often send the transcript to a cloud LLM (Section 10.8), so retention and access must be documented and consented to |

*Speaker profiling versus speaker verification.* Verification is a biometric decision about identity: does this voice match the claimed enrolled speaker? The output is accept or reject at a threshold. Profiling never identifies the individual; it predicts trait labels as defined by a dataset, such as gender, age group, emotion or regional dialect. They are easy to confuse because both start from a speaker embedding, but their outputs, data and metrics differ.

| Task | Table 1.1 dataset | Table 1.1 metric | One privacy or fairness risk |
|---|---|---|---|
| Speaker verification (biometric) | ArabCeleb (in-the-wild, celebrity) | Equal Error Rate (EER) | **Privacy and security**: the voice template is biometric data (Section 8.6 and Chapter 13); it can be spoofed with cloned speech, and a false accept gives an impostor access to an account |
| Speaker profiling / emotion | SPARTA | Accuracy, F1 | **Fairness and consent**: inferring gender, dialect or emotional state without the speaker's knowledge can be used to discriminate (for example routing or pricing by inferred origin), and the labels themselves are often subjective or culturally dependent |

---

## Exercise 4

**Task.** For the written form علم, list at least three valid diacritizations with transliterations and meanings, and explain why this is a problem for a text-to-speech system. Validate your list with an open-source Arabic morphological analyzer such as CAMeL Tools, report at least four analyses with the vocalized form, the Buckwalter transliteration, the lemma, the part of speech and an English gloss, and say which analyses lead to different pronunciations for a synthesizer.

**Solution.** Hand list (Section 1.5.2 gives the first four):

| Vocalized | Transliteration | IPA | Meaning |
|---|---|---|---|
| عِلْم | ʿilm | /ʕilm/ | knowledge, science |
| عَلَم | ʿalam | /ʕalam/ | flag |
| عَلِمَ | ʿalima | /ʕalima/ | he knew |
| عَلَّمَ | ʿallama | /ʕalːama/ | he taught (Form II, geminate /lː/) |
| عُلِمَ | ʿulima | /ʕulima/ | it was known (passive) |

*Why this is a problem for TTS.* A recognizer can postpone the choice by emitting the undiacritized string, but a synthesizer cannot: it must choose one pronunciation before it speaks. The five readings are five different words with five different sound sequences, so a wrong guess is not a mild mispronunciation but a change of meaning, which for a screen-reader user with no visual context is a serious failure (Chapter 9 opening scene). The choice depends on sentence context, so the front end needs a diacritizer (a morphological analysis plus a language model) rather than a letter-to-sound table.

*Validation with CAMeL Tools (notebook `Chapter_01_Exercise_04.ipynb`, CAMeL Tools 1.6.0, database `calima-msa-r13`).* The analyzer returns 21 analyses for علم. Grouping by lemma and part of speech gives these distinct readings (Buckwalter transliteration from the `bw` field, gloss from the `gloss` field):

| Vocalized form (diac) | Buckwalter | Lemma | POS | English gloss |
|---|---|---|---|---|
| عِلْم | Eilom/NOUN | عِلْم | noun | knowledge; knowing / science; study_of |
| عَلَم | Ealam/NOUN | عَلَم | noun | flag; banner; badge |
| عَلِمَ | Ealim/PV+a/PVSUFF_SUBJ:3MS | عَلِم | verb | know; find_out + he |
| عَلَّمَ | Eal~am/PV+a/PVSUFF_SUBJ:3MS | عَلَّم | verb | teach; instruct + he |
| عُلِمَ | Eulim/PV_PASS+a/PVSUFF_SUBJ:3MS | عَلِم | verb (passive) | be_known; be_found_out + he/it |

The remaining analyses are the two nouns with each of their case endings (عِلْمُ, عِلْمَ, عِلْمِ, عِلْمٌ, عِلْمٍ; likewise for عَلَم), which the notebook prints in full.

*Which analyses change the pronunciation.* The five stems above are five distinct pronunciations, so they all matter to a synthesizer; the geminate in عَلَّمَ additionally requires the duration modelling of Section 2.5. The case-ending analyses (nominative -u, accusative -a, genitive -i, with or without tanwīn) change the pronunciation **only in connected, fully inflected speech**; in the pausal style used at the end of a phrase they are silent, so عِلْمُ, عِلْمَ and عِلْمِ all sound like /ʕilm/. A front end therefore makes two decisions: which stem (always), and whether to voice the ending (depends on phrase position, Table 9.1).

---

## Exercise 5

**Task.** Choose two published Arabic ASR results on MGB-2, QASR, Common Voice Arabic or NADI 2025, and complete a comparison matrix: dataset version, split, domain, dialect, text normalization, diacritization, metric and model. Then state whether a direct comparison is valid, and why.

**Suggested solution.** Both results below are on MGB-2 and both are published; the figures were checked against the cited papers when these solutions were prepared. Readers who pick other results should fill the same matrix from the papers, never from memory.

| Field | Result A: MGB-2 challenge winner (2016) | Result B: Open Universal Arabic ASR Leaderboard (2024/2025) |
|---|---|---|
| Source | Ali et al., "The MGB-2 challenge," SLT 2016 [3]: best participant system, submitted by QCRI | Wang, Alhmoud and Alqurishi, "Open Universal Arabic ASR Leaderboard" [50]; figures taken from Table 1 of the arXiv version (2412.13788); check them against the Interspeech 2025 version and the live leaderboard, which is updated |
| Dataset version | MGB-2 challenge release (Al Jazeera 2005 to 2015, about 1,200 h training) | MGB-2 as packaged by the leaderboard authors |
| Split | Official MGB-2 evaluation set, about 10 h, verbatim transcribed and manually segmented (3 to 10 s), overlap regions marked | MGB-2 test portion used by the leaderboard, reported as 9.6 h and "5 dialects" |
| Domain | Broadcast television (news, interviews, reports) | Same broadcast source |
| Dialect | More than 70 % MSA, remainder Egyptian, Gulf, Levantine, North African | Same material, described as five dialect groups |
| Text normalization | Official scoring through a Global Mapping File (GLM); the paper also reports variants with punctuation and diacritics removed and with alif, yāʾ and tāʾ marbūṭa normalized | Remove all punctuation and diacritics; normalize letters carrying hamza and madda; convert Arabic-Indic digits to Western; Latin letters kept for code-switching |
| Diacritization | Scored on undiacritized text (diacritics removed in the reported variants) | Diacritics removed before scoring |
| Metric | WER; official result **14.7 %** | WER and CER; for `openai/whisper-large-v3`: **16.26 % WER, 7.74 % CER** on the MGB-2 set, the lowest MGB-2 WER in that table (the overall leader by average WER, `nvidia/conformer-ctc-large-ar` with an LM, scores 17.20 % on MGB-2) |
| Model | Supervised hybrid system trained **on the MGB-2 training data** (QCRI's 2016 challenge system) | Whisper-large-v3, **zero-shot**, weakly supervised on 680 k hours of web audio, no MGB-2 fine-tuning |

**Is a direct comparison valid?** No, not as a ranking of the two systems, for four reasons.

1. **Different scoring conventions.** The 2016 official number was computed through the challenge GLM with the NIST scoring pipeline; the leaderboard applies its own normalization script (diacritic removal, hamza and madda unification, digit conversion). Chapter 1's Reproducibility Note says such differences alone can move a WER by several points on identical output.
2. **Possibly different test material.** The official evaluation set is about 10 h with overlapped speech marked separately; the leaderboard reports 9.6 h. Unless the leaderboard's segment list is shown to be the same set with the same treatment of overlap, the denominators differ.
3. **Different training conditions.** Result A is an in-domain supervised system trained on the MGB-2 training set; Result B is zero-shot. A lower WER for A says as much about domain-matched training data as about model quality, and a higher WER for B is a zero-shot number that would very likely drop after fine-tuning.
4. **Nine years apart.** Toolkits, segmentation and even the reference transcripts' handling (lightly supervised versus verbatim) can differ between releases.

What *is* valid: comparing rows **within** the leaderboard table (same test set, same script, same day), and comparing the challenge entrants **within** the 2016 paper. Across the two, the honest statement is that a modern zero-shot foundation model reaches roughly the WER band that the best supervised in-domain system reached in 2016 on this benchmark, under a different normalization, which is an observation, not a ranking.

---

### Flags and notes for the companion website

* The companion notebook clips mentioned in Exercise 2 were not supplied; the notebook uses FLEURS Arabic as a stand-in and accepts uploaded clips. Replace the stand-in when the official clips are published.
* Exercise 5 figures were transcribed from the cited papers; if either paper is revised (the leaderboard is a living resource), re-check the numbers before publishing.
