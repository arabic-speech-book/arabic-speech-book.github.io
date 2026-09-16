# Chapter 9 Solutions: Speech Synthesis (Text-to-Speech)

These solutions follow the numbering of the chapter's exercise list. Exercises 2 and 4 have companion notebooks.

Notebooks for this chapter: [`Chapter_09_Exercise_02.ipynb`](Chapter_09_Exercise_02.ipynb), [`Chapter_09_Exercise_04.ipynb`](Chapter_09_Exercise_04.ipynb).

---

## Exercise 1

**Task.** Describe the stages of the text-to-speech pipeline and what each contributes, and explain why the Arabic front end carries more weight than an English one.

**Suggested solution.** (Sections 9.1, 9.2, 9.4, 9.5, Figure 9.1.)

| Stage | What it does | What it contributes |
|---|---|---|
| 1. Text normalization (front end) | expands numbers, dates, currency, abbreviations; handles Latin-script names and code-switched spans | decides *what words* will be spoken; an error here is a wrong word said fluently |
| 2. Diacritization (front end, Arabic) | restores the short vowels, shadda and, where needed, the case endings that the script omits | decides *which word* an ambiguous spelling is (عِلْم / عَلَم / عَلَّمَ) and its vowels |
| 3. Grapheme-to-phoneme conversion (front end) | maps the diacritized text to phonemes, applying sun-letter assimilation, hamzat al-waṣl, gemination, tāʾ marbūṭa and pausal rules, phrase boundaries | the pronounceable form; explicit and inspectable, which is why phoneme input is preferred for Arabic (Section 9.5) |
| 4. Acoustic model (back end) | phonemes (with duration, pitch and energy predictions in FastSpeech 2, or attention in Tacotron 2) to a mel spectrogram | timing, prosody and the acoustic realization of each sound |
| 5. Vocoder (back end) | mel spectrogram to waveform (WaveNet, HiFi-GAN); or jointly with stage 4 in VITS; or codec tokens to waveform in codec language models | the fine detail that makes the voice sound like a recording rather than a buzz |

*Why the Arabic front end carries more weight.* English text tells the synthesizer almost everything it needs: the spelling fixes the word, and a large pronunciation dictionary plus letter-to-sound rules handle the rest, so most quality variation lives in the back end. Arabic text withholds the short vowels, the gemination and the case endings, so the front end must **choose the word** before it can pronounce it; the same letters علم are three or five different words (Exercise 1.4), and only context decides. The mapping from letters to sounds is also less direct than a dictionary: the article is pronounced two ways depending on the next consonant, hamzat al-waṣl disappears inside a phrase, tāʾ marbūṭa is /t/ or /a/ depending on what follows, and numbers inflect for gender and case. A back-end error makes speech sound distorted; a front-end error makes fluent speech say the wrong thing, which for a screen reader is the worse failure (opening scene). The SawtArabi and NVDA studies the chapter cites show the size of the effect: diacritizing the input raised pronunciation scores by more than a point on a five-point scale with the same back end. That is why Chapter 9 treats normalization, diacritization and G2P as the critical path rather than as preprocessing.

---

## Exercise 2

**Task.** Process a short passage of undiacritized Arabic news text through two different open-source diacritizers, convert each output to a phoneme sequence, and write a short comparative analysis of where the two disagree and how those differences would change the synthesized speech.

**Solution (notebook `Chapter_09_Exercise_02.ipynb`).**

*Setup.* Passage: three news-style MSA sentences composed for the exercise (31 words). Diacritizer A: CAMeL Tools 1.6.0 MLE disambiguator over `calima-msa-r13` (full vocalized analysis per word, including case endings). Diacritizer B: Mishkal (open-source rule-and-lexicon diacritizer). The companion G2P notebook was not supplied, so the notebook implements a small rule-based MSA G2P (consonant map, short and long vowels, diphthongs, shadda as gemination, tanwīn, sun-letter assimilation applied by rule, hamzat al-waṣl dropped inside the phrase, tāʾ marbūṭa as /t/ before a vowel and /a/ in pause, pausal deletion of the final short vowel at sentence end). Its self-test gives الشَّمْسُ → /ʔaʃːamsu/, الْقَمَرُ → /ʔalqamaru/, مَدْرَسَةٌ → /madrasatun/ (pausal /madrasa/), عَلَّمَ → /ʕalːama/, بَيْتٌ → /bajtun/.

*Executed result.* The two diacritizers wrote **25 of 31 words differently** (81 %), but most of that is notation: CAMeL omits the fatḥa before alif and the shadda on sun letters after the article and does not mark sukūn on the article's lām, Mishkal writes all of them. After G2P, which applies the pronunciation rules regardless of how they are marked, **13 of 31 words (42 %) have different phoneme strings**: 7 differ only in the final short vowel (case or mood ending) and 6 differ inside the word.

| Word | CAMeL | Mishkal | Phonemes (CAMeL / Mishkal) | Kind of difference and what a listener would hear |
|---|---|---|---|---|
| خطة | خُطَّةٍ | خُطَّةِ | xutˤːatin / xutˤːati | case ending only (indefinite genitive vs definite genitive); in connected speech a different final syllable, in pause identical; Mishkal's reading is wrong after عن with an indefinite noun |
| تشمل | تَشْمَل | تَشْمَلُ | taʃmal / taʃmalu | mood ending: CAMeL omits the indicative -u; audible only in connected speech |
| تدريب | تَدْرِيبِ | تَدْرِيبُ | tadriːbi / tadriːbu | case ending: object of تشمل should be accusative; both are wrong, differently |
| وبناء | وَبِناءَ | وَبِنَاءِ | wabinaːʔa / wabinaːʔi | case ending |
| المدارس | المَدارِسِ | الْمُدَارِسِ | lmadaːrisi / lmudaːrisi | **internal vowel**: Mishkal's /mu-/ is a mispronunciation of 'the schools'; fluent but wrong |
| إن | إِن | إِنّ | ʔin / ʔinː | **gemination**: after قال the particle is إنَّ /ʔinːa/; CAMeL's reading is the conditional 'if', a different word |
| أن | أَنَّ | أَن | ʔanːa / ʔan | **gemination**: before a verb (أن يبدأ) it must be أَنْ; CAMeL's geminate reading is the wrong particle, Mishkal is right |
| عشر | عَشَرَ | عُشُرِ | ʕaʃara / ʕuʃuri | **stem vowels**: 'ten' vs 'a tenth'; a different word |
| ومن | وَمِن | ومِن | wamin / wmin | Mishkal left the conjunction unvowelled; a synthesizer would produce an unpronounceable cluster or guess |
| العام | العامِّ | الْعَامِ | lʕaːmːi / lʕaːmi | **gemination**: CAMeL chose the lemma عامّ 'general' instead of عام 'year'; the geminate /mː/ is audible and the word is wrong |
| التنفيذ, يبدأ, لتطوير | | | | case or mood endings only |

*Comparative analysis.* Neither tool is reliable enough on its own for a synthesizer. Their disagreements fall into the two layers of Section 2.7. The **case- and mood-ending layer** accounts for about half of the phoneme differences; in pausal synthesis (a phrase-final word) these vanish, and in connected synthesis they change one short vowel per word, audibly but without changing the word. Both tools make errors in this layer, which matches the chapter's remark that final endings are the hard part. The **internal layer** is where the synthesized speech changes meaning: a wrong stem vowel (المُدارس), a wrong gemination (إن / إنَّ, أنَّ / أنْ, العامّ / العام) or a wrong lexeme (عُشُر) makes the voice say a different word fluently, exactly the failure the opening scene warns of, and the two tools err on *different* words, so a disagreement between them is a useful flag for human review. CAMeL's MLE model, which picks a whole-word analysis, tends to err on particles and lemma choice; Mishkal, which is rule-driven, tends to err on stem vowels and occasionally leaves a vowel out. The practical conclusions for a front end: run two diacritizers and route disagreements to a lexicon or a human; apply pronunciation rules (sun-letter assimilation, waṣl) in the G2P rather than trusting the diacritizer to mark them; prefer pausal endings at phrase boundaries where the tools are least reliable; and measure both tools against a human-verified reference with a diacritic error rate before choosing one.

---

## Exercise 3

**Task.** Compare autoregressive (Tacotron 2) and non-autoregressive (FastSpeech 2) acoustic models in naturalness, speed and robustness to skipping and repetition, and state which you would choose for a low-latency Arabic assistant and why.

**Suggested solution.** (Section 9.4, Figure 9.3.)

| Aspect | Tacotron 2 (autoregressive) | FastSpeech 2 (non-autoregressive) |
|---|---|---|
| How frames are produced | one mel frame after another, each conditioned on the previous, with soft attention over the encoder | duration, pitch and energy predicted per phoneme; a length regulator expands the sequence and all frames are generated in parallel |
| Naturalness | in its original evaluation close to professionally recorded speech; prosody learned implicitly and often very natural | reported comparable to, and in some comparisons better than, the autoregressive baselines; explicit pitch and energy give control, but naive control does not guarantee natural intonation |
| Speed | slow: generation time grows linearly with the number of frames and cannot be parallelized across time | fast: the whole spectrogram in one pass; latency is dominated by the vocoder and the front end |
| Skipping and repetition | the attention can lose its place, so words are dropped or repeated, more often in long or unusual sentences | explicit durations remove the soft alignment, so skipping and repetition are largely eliminated; remaining errors are wrong durations or pronunciations |
| Data and training | no duration labels needed | needs phoneme durations (from a forced aligner or a teacher model) |

*Choice for a low-latency Arabic assistant: FastSpeech 2 (or a similar duration-based model), with a fast parallel vocoder such as HiFi-GAN.* Three reasons. First, latency: an assistant must start speaking within a few hundred milliseconds of deciding what to say, and parallel spectrogram generation is what makes that possible on a phone or a server under load. Second, reliability: an assistant reads names, numbers, addresses and confirmations, where omitting or repeating a word is worse than a slightly flatter voice (the screen-reader argument of Section 9.4 applies directly), and the duration-based design does not skip or repeat. Third, the Arabic-specific benefits of explicit duration and pitch: the model can be given duration targets that respect gemination and vowel length, both contrastive in Arabic (Section 2.5), and the pitch and energy predictors give a handle on question intonation and emphasis that a Tacotron-style model exposes only indirectly. The condition the book attaches is to verify the choice on the intended variety, front end and device rather than assume it, and to make sure the front end (Exercise 2) feeds it correct phonemes, since a duration-based model will render a mispronunciation just as confidently as a Tacotron.

---

## Exercise 4

**Task.** Design and deploy a hands-on subjective evaluation lab: prepare 20 TTS outputs (10 MSA, 10 dialectal), draft a naturalness annotation scheme, deploy it on a platform such as Label Studio with a MUSHRA-style scale, a hidden reference and low- and mid-quality anchors, define listener instructions and bias-mitigation steps, include an objective WER cross-check, and state how you would report results per dialect with a confidence interval.

**Solution (notebook `Chapter_09_Exercise_04.ipynb`).**

*Stimuli.* Twenty sentences written for the exercise: 10 MSA, 5 Saudi (Najdi) and 5 Egyptian. They were synthesized with `facebook/mms-tts-ara` (VITS, 16 kHz). **Flag:** no openly licensed dialectal Arabic TTS checkpoint with documented provenance and consent could be verified for this release, so the ten dialectal stimuli are dialect *text* read by the MSA voice, which is reported as exactly that condition; the notebook has a slot for a dialect checkpoint.

*Reference and anchors.* Natural recordings serve as the reference: MSA clips from FLEURS Arabic and Saudi and Egyptian clips from a community-redistributed SADA subset (licences to be verified before publication). Because the natural clip is not the same sentence as the stimulus, the design is described as **MUSHRA-like**, as Section 9.8 requires. Anchors follow BS.1534: the reference low-pass filtered at 3.5 kHz (low anchor) and at 7 kHz (mid anchor). The reference is also included hidden among the rated items.

*Annotation scheme.* Attribute: naturalness relative to the reference, 0 to 100 with the bands Bad, Poor, Fair, Good, Excellent; a separate pronunciation question (all words correct / one error / several) with a free-text list of mispronounced words, because naturalness and pronunciation are different attributes; per screen, the open reference plus four hidden items (TTS output, hidden reference, low anchor, mid anchor) in random order. The notebook writes the Label Studio task file and the labelling-interface XML; the exported ratings carry the item kind for analysis while the interface hides it.

*Listener instructions* (quoted in the notebook): headphones in a quiet room; listen fully as often as needed; rate naturalness against the reference from 0 to 100; at least one item should get 100 if it sounds identical to the reference; rate the speech, not the content; note mispronounced words.

*Bias mitigation.* Item order and screen order randomized per listener with a recorded seed; listeners recruited and screened as native speakers of the variety they rate (Saudi screens by Saudi listeners, Egyptian by Egyptian, MSA by any native Arabic speaker), never shown the model identity; attention checks: hidden reference rated at or above 90 and low anchor at or below mid anchor on at least 80 % of screens, else the listener is excluded; a training screen first; at least 15 listeners per item; playback device and environment recorded.

*Objective cross-check.* Whisper-small transcribes each synthesized stimulus and the WER and CER against the intended text are computed after one stated normalization (diacritics and punctuation removed; alif, ة/ه, ى/ي unified). In the test run the values were:

| Variety of the input text | Sentences | N (words) | WER | CER |
|---|---|---|---|---|
| MSA | 10 | 81 | 40.7 % | 11.5 % |
| Saudi | 5 | 34 | 23.5 % | 9.1 % |
| Egyptian | 5 | 30 | 43.3 % | 13.8 % |

(`facebook/mms-tts-ara` synthesis, `openai/whisper-small` recognition, CPU.) The high MSA number is itself informative: the recognizer's transcript of the synthesized MSA (for example أشهد المدينة رتفاعة for تشهد المدينة ارتفاعا) shows that the voice mispronounces or slurs word onsets and case endings, the front-end failure mode of Exercise 2 made audible, and that Whisper-small is a weak judge of it; a listening test would be needed to separate the two. The small samples (5 sentences per dialect) mean these rates carry wide uncertainty and are shown to illustrate the cross-check, not to rank varieties.

These are intelligibility proxies only; they depend on the recognizer and its dialect coverage, and they cannot measure naturalness. The dialectal rows are also affected by the MSA voice's pronunciation of dialect words, which is the point of including them.

*Reporting per dialect with a confidence interval.* For each variety and item kind, average each listener's ratings first (the listener is the unit of replication), then report the mean and a 95 % t-interval (or bootstrap) over listener means, with the number of listeners and screens; report the hidden-reference and anchor rows too, since they validate the test. The notebook demonstrates the computation on **simulated ratings, labelled as such**. The write-up states the MUSHRA-like design, the exact question and scale, listener recruitment and screening, exclusions, playback conditions, the TTS model and version per variety, and the ASR model and normalization behind the WER cross-check. MSA and dialectal screens are never pooled into a single naturalness number.

---

## Exercise 5

**Task.** Plan a Quranic recitation synthesis system: the data needed, the Tajwīd and prosody constraints, how to evaluate correctness with experts, and the religious and ethical considerations. Then conduct a bibliographic audit of three published papers on Quranic or Classical Arabic synthesis: verify each paper's dataset sources and report whether they use a documented open corpus (such as ClArTTS) or proprietary, unvetted audio, and what that implies for reproducibility.

**Suggested solution.**

*Data.* Recordings of qualified reciters (ijāza-holding qurrāʾ), recorded in a studio at 48 kHz or better, in **one declared canonical reading** (for example Ḥafṣ ʿan ʿĀṣim), with explicit, written permission that covers synthesis and, separately, voice cloning; the full Uthmanic text with its recitation marks (pause signs, madd marks, sukūn and shadda conventions) aligned to the audio at verse, word and phone level; annotation of Tajwīd events (madd type and count, idghām, ikhfāʾ, iẓhār, qalqalah, ghunnah) and of pause and continuation choices; and metadata on the reciter, the reading tradition and the recording. The chapter's two public collections show what exists and what is missing: Tadabur (more than 1,400 h, 600+ reciters, CC BY-NC 4.0) is large but multi-reciter and non-commercial, and Tarteel (67 h, crowdsourced, variable quality, CC BY-NC-ND stated in the paper) is recognition data, not synthesis data; neither is a single-speaker studio corpus ready for TTS, so a synthesis project will almost certainly need its own recording with its own consent.

*Tajwīd and prosody constraints.* The synthesizer must treat the rules as hard constraints, not tendencies: madd durations in counts (two, four, six ḥarakāt) become explicit duration targets, which favours a duration-based acoustic model (Exercise 3) with a Tajwīd-aware front end that outputs phone plus length and nasalization features rather than plain phonemes; idghām and ikhfāʾ must be encoded in the G2P as context-dependent assimilation and nasalization across word boundaries; qalqalah requires a release burst on the five letters in sukūn; ghunnah requires controlled nasal duration; pauses may only fall at permitted places and continuation changes the pronunciation of word endings (waṣl and waqf, Table 9.1); and the melodic contour (tartīl style, register, tempo) must stay within the tradition, which argues for a single-reciter voice and against expressive controls that could produce non-canonical melodies. The reading tradition must be fixed and declared, because the same verse differs across qirāʾāt.

*Evaluation with experts.* Naturalness MOS is not sufficient. The primary evaluation is a **rule-by-rule correctness audit** by certified Tajwīd specialists: for each verse, each madd, idghām, ikhfāʾ, qalqalah and ghunnah event is marked correct or incorrect, giving a Tajwīd error rate per rule type and per reciter style, with inter-rater agreement reported (Chapter 7); phonetic checks (measured madd durations against the required counts, nasal duration for ghunnah) complement the listening; ASR-based intelligibility against the verse text; and only then a naturalness and similarity test with native listeners familiar with recitation. Release only if the expert audit finds zero canonical errors on the test verses, and publish the audit.

*Religious and ethical considerations.* The Qurʾān is sacred text; synthesized recitation must never be presented as human recitation or as authoritative, must be labelled as synthetic, and should be developed under the guidance of religious scholars, ideally with a review by a recognized authority before any public use. Cloning a known reciter's voice requires that reciter's explicit permission and a clear statement of permitted uses; using recordings "found online" does not confer it (Section 9.7). The scope should be educational and assistive (a learner hearing a correct rendering, an accessibility use) rather than replacing reciters in worship, and any error is not a mere quality problem but a religious one, which justifies the expert gate above and a mechanism for withdrawal and correction after release.

*Bibliographic audit of three papers* (checked against the papers when these solutions were prepared; readers should re-verify).

| Paper | Data source, as documented | Open and documented? | Implication for reproducibility |
|---|---|---|---|
| Kulkarni, Kulkarni, Shatnawi and Aldarmaki, "ClArTTS: An Open-Source Classical Arabic Text-to-Speech Corpus," Interspeech 2023 | About 12 hours of Classical Arabic from a single male speaker, extracted from a **LibriVox audiobook** (public-domain source), manually transcribed and diacritized; released at the corpus website for research; TTS baselines (Grad-TTS, Glow-TTS in the paper's description) trained on it | **Yes**: a documented open corpus with a stated source and a research licence; the book's Table 1.1 uses it as the reference TTS resource | Fully reproducible: anyone can obtain the same audio and text and train the same baselines; the single speaker and audiobook style limit generalization but not reproducibility. Note that ClArTTS is Classical Arabic prose, not Qurʾānic recitation, so it does not exercise Tajwīd |
| Toyin, Djanibekov, Kulkarni and Aldarmaki, "ArTST: Arabic Text and Speech Transformer," ArabicNLP 2023 | Pretraining on MGB-2 (about 1,000 h of broadcast audio); TTS fine-tuning on **ClArTTS (11.16 h)** and the **Arabic Speech Corpus (3.81 h)**, both open synthesis corpora; MOS evaluation with 15 native listeners; models and code released for research | **Yes**: all TTS data are documented open corpora; MGB-2 is available under challenge research terms | Reproducible with the released checkpoints and the named corpora; the evaluation (15 listeners, MOS) is small and, again, Classical or Modern Standard Arabic rather than recitation |
| Bettayeb and Guerti, "Study to Build a Holy Quran Text-To-Speech System," International Journal on Islamic Applications in Computer Science and Technology, vol. 7, no. 4, 2019 | 772 verse fragments (about 45 minutes) selected from a **39-hour online recording of one reciter (Ayman Rushdi Suwaid, spelled "Aymen Roshdy Sweed" in the paper), downloaded from a recitation website**; concatenative diphone and polyphone synthesis; evaluation by rule-based transcription accuracy on 20 verses and synthesis coverage on 45 verses; no public release of the corpus stated | **No**: proprietary, unvetted audio; the recordings' licence and the reciter's permission for synthesis are not documented, and the derived unit database is not released | Not reproducible: the exact recording version, the segmentation and the unit database cannot be recovered from the paper, and there is no listening test or expert Tajwīd evaluation to compare against; the work also raises the consent question of Section 9.7, since a recognizable reciter's voice is being resynthesized from downloaded audio |

*What the audit implies.* The two papers built on ClArTTS are reproducible because their data are open and documented, but they do not synthesize recitation; the one paper that targets Qurʾānic recitation rests on undocumented, downloaded audio, which is the norm the chapter warns about and the reason a documented, consented Qurʾānic synthesis corpus (single reciter, declared reading, Tajwīd annotations, clear licence) would be the field's most useful contribution. Any new project should publish its data card, its reciter's consent terms and its expert-audit protocol alongside the model.

---

### Flags and notes for the companion website

* Exercise 2's G2P is a stand-in for the book's companion G2P notebook, which was not supplied; if the official notebook is published, the comparison cells can call it instead.
* Exercise 4 could not use an open dialectal TTS voice; the dialectal stimuli are dialect text read by the MSA MMS voice and are labelled as such. The listening test itself was not run; the CI computation is demonstrated on simulated ratings.
* Exercise 5's audit was done against the cited papers' texts; the ClArTTS licence line should be confirmed on the corpus website before publication.
