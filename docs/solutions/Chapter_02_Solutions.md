# Chapter 2 Solutions: Arabic Language and Speech Fundamentals

These solutions follow the numbering of the chapter's exercise list. Open-ended items are labelled **Suggested solution**. No exercise in this chapter requires code, so there is no companion notebook; readers who want to check the IPA descriptions or the segmentations programmatically can reuse [`Chapter_01_Exercise_04.ipynb`](Chapter_01_Exercise_04.ipynb) (CAMeL Tools analysis) and [`Chapter_05_Exercise_05.ipynb`](Chapter_05_Exercise_05.ipynb) (morphological versus BPE segmentation).

---

## Exercise 1

**Task.** Read these IPA symbols aloud: /q/, /ħ/, /sˤ/, /uː/. For each, give the Arabic letter, the voicing, place and manner (or height and backness for the vowel), and one Arabic example word.

**Solution.** (Sections 2.2 to 2.4, Table 2.1 and Table 2.2.)

| IPA | Arabic letter | Voicing | Place of articulation | Manner (or height and backness) | Example (Arabic, transliteration, gloss) |
|---|---|---|---|---|---|
| /q/ | ق (qāf) | voiceless | uvular (back of the tongue against the uvula, farther back than /k/) | stop (plosive) | قَلب qalb 'heart' |
| /ħ/ | ح (ḥāʾ) | voiceless | pharyngeal (constriction deep in the throat, below the uvula) | fricative | حَجّ ḥajj 'pilgrimage' |
| /sˤ/ | ص (ṣād) | voiceless | alveolar (like /s/) with a secondary pharyngeal constriction, marked by ˤ; this is the "emphatic" or pharyngealized /s/ | fricative | صَيف ṣayf 'summer' (contrast سَيف sayf 'sword') |
| /uː/ | ـُو (ḍamma plus wāw as a vowel letter) | voiced (all Arabic vowels are voiced) | close (high) and back, with rounded lips; the ː mark means it is phonemically long | vowel | نُور nūr 'light' |

Two reminders from the chapter. First, the letter و can also be the consonant /w/, so letters and sounds are not one-to-one. Second, the difference between /q/ and /ħ/ is one of place: /q/ is made at the uvula, /ħ/ lower still, in the pharynx; the chapter asks a phoneme inventory to keep the uvular stop and the pharyngeal fricatives apart.

---

## Exercise 2

**Task.** In your own words, explain the source-filter model and define F0, F1 and F2. Why does the second formant fall in a vowel next to an emphatic consonant? Then connect the model to engineering: which half of the source-filter pair do the recognition features of Chapter 3 mostly capture, and what happens to the other half?

**Suggested solution.**

*The model.* Speech is produced in two stages. The **source** is the air stream chopped into pulses by the vibrating vocal folds (for voiced sounds) or turned into noise by a narrow constriction (for voiceless fricatives). The **filter** is the vocal tract above the larynx: throat, mouth, tongue, lips and nasal passage form an adjustable tube that resonates at some frequencies and damps others. Moving the tongue or lips changes the tube shape, hence the filter, hence the sound. Figure 2.1 draws this as source spectrum times filter response equals output spectrum.

*Definitions.* **F0**, the fundamental frequency, is the rate of vocal-fold vibration; it is heard as pitch and belongs to the source. **F1** and **F2** are the two lowest resonances of the vocal-tract filter, the formants. As a rough guide F1 rises as the mouth opens (low vowels have high F1) and F2 rises as the tongue moves forward (front vowels have high F2). Together F1 and F2 identify a vowel (Figure 2.3).

*Why F2 falls next to an emphatic.* An emphatic consonant such as /tˤ/ is produced with a secondary constriction: the root of the tongue is pulled back toward the pharynx. That backing does not switch off at the consonant boundary; it colours the neighbouring vowel, moving the tongue body back and enlarging the front cavity. A more retracted tongue lowers F2, so the vowel in طين starts with an F2 near 1840 Hz against about 2580 Hz in تين (Figure 2.4) and then climbs back over some tens of milliseconds. The chapter calls this emphasis spread; its strength and reach vary with dialect and context.

*Connection to engineering.* The log-mel filterbank and MFCC features of Chapter 3 summarize the smooth **spectral envelope** of each short frame. That envelope is mainly the **filter**: formant peaks, and therefore vowel identity and the F2 lowering that signals emphasis, are what these features preserve. The **source** is largely, but not entirely, discarded. The mel filterbank smears the fine harmonic structure that carries F0, and the cepstral truncation to 12 or 13 MFCCs removes most of the remaining pitch ripple. Some source information survives: voiced and voiceless frames have different overall spectral tilt and energy, and at low F0 the harmonics are wide enough apart to leave traces in the low mel bands. So the recognizer sees the vocal tract clearly and the larynx faintly, which is why pitch and prosody must be modelled separately when they matter (synthesis, emotion, tone), and why LPC is used as a *diagnostic* tool for the filter (Section 3.7).

---

## Exercise 3

**Task.** Explain how the definite article is pronounced in الشمس ('the sun') versus القمر ('the moon'), state the rule a G2P converter would need, list the fourteen sun letters, and give two further examples of each behaviour.

**Solution.**

*The two pronunciations.* The article is always written الـ, but before a **sun letter** the /l/ of the article assimilates to the following consonant, which is then pronounced as a geminate: الشمس is written al-shams but said ash-shams, [ʔaʃːams], with a long /ʃː/ and no /l/ at all. Before a **moon letter** the /l/ is pronounced as written: القمر is al-qamar, [ʔalqamar]. In writing the assimilation is marked, when diacritics are present, by a shadda on the sun letter (الشَّمس) and by the absence of a sukūn on the lām.

*The rule for a G2P converter.* Given a token beginning with the article ال followed by a consonant C:

* if C is a sun letter, output /ʔa/ (or, in connected speech after a vowel, nothing for the hamzat al-waṣl) followed by **/Cː/** (geminate C) and drop the /l/;
* otherwise output /ʔal/ followed by /C/.

The rule is phonological, not orthographic: the sun letters are exactly the coronal consonants, those made with the tongue tip or blade at or near the teeth and alveolar ridge, which is why /l/ assimilates to them and not to labials, velars, uvulars or pharyngeals.

*The fourteen sun letters* (Section 2.6): ت ث د ذ ر ز س ش ص ض ط ظ ل ن, that is t, th, d, dh, r, z, s, sh, ṣ, ḍ, ṭ, ẓ, l, n. The other fourteen letters (ا ب ج ح خ ع غ ف ق ك م ه و ي) are moon letters.

*Further examples.*

| Behaviour | Written | Pronounced | Gloss |
|---|---|---|---|
| Sun (assimilated) | النور al-nūr | an-nūr [ʔanːuːr] | the light |
| Sun (assimilated) | الطالب al-ṭālib | aṭ-ṭālib [ʔatˤːaːlib] | the student |
| Moon (unassimilated) | الكتاب al-kitāb | al-kitāb [ʔalkitaːb] | the book |
| Moon (unassimilated) | المدرسة al-madrasa | al-madrasa [ʔalmadrasa] | the school |

Note that ج is a moon letter in MSA even though it is pronounced far forward in some dialects, and that the lām of the article assimilates to another lām (اللغة al-lugha is [ʔalːuɣa]), which is why ل is itself counted among the sun letters.

---

## Exercise 4

**Task.** For the written form علم, list at least three valid diacritizations with transliterations and meanings, and say which layer of ambiguity (internal vowels or case ending) each one illustrates; then write one noun with its three case endings to illustrate the final layer explicitly.

**Solution.** Section 2.7 distinguishes two layers: word-internal vowels and gemination, which select the lexeme, and the word-final iʿrāb endings, which mark case (nouns) or mood (verbs).

| Vocalized | Transliteration | Meaning | Layer illustrated |
|---|---|---|---|
| عِلْم | ʿilm | knowledge | word-internal vowels (kasra, sukūn) |
| عَلَم | ʿalam | flag | word-internal vowels (two fatḥas) |
| عَلِمَ | ʿalima | he knew | word-internal vowels (verb reading) |
| عَلَّمَ | ʿallama | he taught | word-internal: the **shadda** (gemination) is also a missing diacritic |
| عِلْمٌ / عِلْمَ / عِلْمِ | ʿilmun / ʿilma / ʿilmi | knowledge (nominative indefinite / accusative definite / genitive definite) | **case ending**: the same lexeme, different syntactic role |

*One noun through its three cases* (Table 2.5 uses الكتاب; here is another):

| Case | Vocalized | Transliteration | Example |
|---|---|---|---|
| Nominative | الْبَيْتُ | al-baytu | الْبَيْتُ كَبِيرٌ 'the house is big' (subject) |
| Accusative | الْبَيْتَ | al-bayta | رَأَيْتُ الْبَيْتَ 'I saw the house' (object) |
| Genitive | الْبَيْتِ | al-bayti | فِي الْبَيْتِ 'in the house' (after a preposition) |

Restoring the internal layer is comparatively easy for a diacritizer because it is a lexical choice; restoring the final layer is hard because it depends on syntax that reaches across the sentence, which is the "robust finding" the chapter reports. In pausal reading the final layer is not pronounced at all, so a synthesizer that speaks pausal MSA can ignore it, while one that speaks fully inflected connected speech cannot.

---

## Exercise 5

**Task.** Segment, in both Arabic script and Latin transliteration, the token وبكتابهم into its clitics and stem, gloss each piece, and explain how clitic stacking raises the OOV rate. Then explain qualitatively how a morphological analyzer and a subword tokenizer such as BPE would each segment the same token and what each representation guarantees; do not claim one exact BPE output.

**Solution.**

*Segmentation* (Table 2.6):

| Piece (Arabic) | Transliteration | Type | Gloss |
|---|---|---|---|
| وَ | wa- | proclitic conjunction | 'and' |
| بِ | bi- | proclitic preposition | 'with, by' |
| كِتَابِ | kitāb-i | stem (noun) plus genitive case ending -i, required after the preposition | 'book' |
| هِمْ | -him | enclitic possessive pronoun (3rd person masculine plural; -hum becomes -him after /i/) | 'their' |

Full form: وَبِكِتَابِهِمْ wa-bi-kitābi-him 'and with their book'.

*Why clitic stacking raises the OOV rate.* A word-based vocabulary must contain each surface string it ever wants to emit. The stem كتاب appears not only bare but with every combination of two proclitics (و، ف، ب، ل، ك، ال ...) and every enclitic pronoun (ـه، ـها، ـهم، ـك، ـي ...), multiplied by the case and number inflections and by the other patterns of the root (Section 2.8). The combinations are productive, so many of them are grammatical yet rare; a fixed vocabulary trained on a finite corpus leaves most of them unseen, and each unseen form is an out-of-vocabulary token that a word-level recognizer can never output. Stacking is what turns one lexeme into hundreds of types.

*How a morphological analyzer segments it.* An analyzer such as CAMeL Tools looks the token up against a lexicon of stems plus tables of legal clitics and affixes, and returns linguistically meaningful pieces with labels: `wa+ bi+ kitAb +him` (in the ATB or D3 schemes, وَ+ بِ+ كِتاب +هِم). It **guarantees** that the pieces are morphemes with a meaning and a part of speech, that the same stem is recovered across all its clitic combinations (so كتاب in وبكتابهم, للكتاب and كتابنا share one unit), and that the analysis is reversible through the tables. Its costs are that it needs an analyzer for the variety (coverage of dialects is uneven), that a token may have several legal analyses so a disambiguator is needed, and that a genuinely unknown stem still fails.

*How BPE segments it.* A BPE tokenizer starts from characters and repeatedly merges the most frequent adjacent pair in its training text until it reaches a target vocabulary size. It then splits وبكتابهم greedily into the longest learned pieces. Depending on the training text, vocabulary size and normalization, the result might be something like و + ب + كتاب + هم, or وب + كتابهم, or a single piece if the whole word was frequent; **no particular output can be promised**, which is why the exercise forbids claiming one. What BPE **guarantees** is coverage: because it can always fall back to single characters (given full character coverage), no word is ever OOV, and frequent clitics tend to become their own pieces so sparsity is reduced in practice. What it does *not* guarantee is that the pieces are morphemes, that the same stem gets the same piece in every context, or that the non-contiguous root (ك-ت-ب inside كتاب) is represented at all. The two representations therefore trade linguistic meaning (analyzer) against universal coverage and data-driven simplicity (BPE), which is exactly the trade-off Table 4.4 and Table 5.3 develop. Notebook `Chapter_05_Exercise_05.ipynb` shows both tools on a related token.

---

## Exercise 6

**Task.** Give one everyday sentence in a dialect you know (or adopt one from Table 2.7 if none), write its MSA equivalent, identify every word that differs, and name one pronunciation feature from Table 2.8 that your dialect shows.

**Suggested solution.** Any dialect is acceptable; the model answer uses Saudi (Najdi) Arabic, the variety of the book's opening scene.

| | Sentence | Transliteration | Gloss |
|---|---|---|---|
| Najdi | أبغى أروح السوق الحين | abghā arūḥ as-sūg al-ḥīn | I want to go to the market now |
| MSA | أُرِيدُ أَنْ أَذْهَبَ إِلَى السُّوقِ الآنَ | urīdu an adhhaba ilā as-sūqi al-āna | I want to go to the market now |

*Words that differ.*

| Najdi | MSA | Nature of the difference |
|---|---|---|
| أبغى abghā | أُرِيدُ urīdu | different lexeme for 'I want' (Table 2.7) |
| (no particle) أروح arūḥ | أَنْ أَذْهَبَ an adhhaba | different verb (رَاحَ vs ذَهَبَ) and the dialect drops the subordinator أَنْ |
| (no preposition) السوق | إِلَى السُّوقِ | dialect omits the preposition after a motion verb; MSA needs إلى and the genitive ending |
| الحين al-ḥīn | الآنَ al-āna | different lexeme for 'now' |

Only السوق 'the market' is shared, and even it differs in pronunciation.

*Pronunciation feature from Table 2.8.* Gulf and Najdi varieties realize qāf as /g/: السوق is [asːuːg], not MSA [asːuːq]. A second feature visible in the same sentence is the loss of the case endings (السوقِ becomes السوق), which is general to the dialects rather than specific to one group.

---

## Exercise 7

**Task.** Levantine Arabic often realizes /q/ ق as /ʔ/ ء. If an ASR system is trained only on MSA phonetics, explain: how this dialectal shift changes the acoustic evidence, how an MSA lexicon represents the word, and what pronunciation-variant modelling would add, for قلب (qalb, 'heart') pronounced /ʔalb/ in Levantine, and say whether an MSA lexicon would map that acoustic signature to the correct written word.

**Solution.**

*1. The acoustic evidence.* /q/ is a voiceless **uvular** stop: a closure at the back of the tongue against the uvula, a burst with energy concentrated fairly low in the spectrum, and formant transitions into the following vowel that show the tongue body pulled back (a lowered F2 onset, similar in direction to emphasis). /ʔ/ is a **glottal** stop: the closure is at the vocal folds, there is no oral constriction, so there is no uvular burst and no backing of the following vowel; the vowel simply starts abruptly from silence, often with a few irregular (creaky) glottal pulses. The acoustic model therefore receives a frame sequence that MSA training data labelled as the beginning of a vowel, or as the hamza in words like أَلَم, not as /q/. The spectral cue that identifies ق in MSA training data is absent.

*2. What an MSA lexicon says.* The pronunciation lexicon (Section 4.4.1) maps the written word قلب to the single phone sequence /q a l b/. There is no entry /ʔ a l b/ for قلب. However, the lexicon may well contain a **different** word with that pronunciation: ألب or the first syllable of ألبان, or the very frequent particle-plus-noun sequences that begin with hamza. So the decoder, forced to explain /ʔalb/ with MSA entries, will either pick a hamza-initial word that exists, misspell the word (ألب), or, if the language model strongly favours قلب in context, pay a large acoustic penalty to keep it.

*3. What pronunciation-variant modelling adds.* Instead of one pronunciation per word, the lexicon lists several with probabilities: قلب : /q a l b/ 0.6, /ʔ a l b/ 0.3, /g a l b/ 0.1 (Egyptian, Levantine and Gulf variants, Table 2.8; the numbers are illustrative and would be estimated from dialect-labelled data). Equivalently, a **rule** maps every ق to the set {q, ʔ, g} in the L transducer of the decoding graph, optionally conditioned on a dialect tag from a dialect identifier (Chapter 8). The acoustic model must also have seen /ʔ/ in these positions, which means dialect-balanced training data (Section 4.8). With the variant present, the decoder can match the glottal-stop frames to the /ʔalb/ path *and still emit the standard spelling قلب*, so the written output is correct although the sound differed from MSA.

*4. Would the MSA-only lexicon map /ʔalb/ to قلب?* In general **no**. The acoustic evidence for the first segment contradicts the only pronunciation listed, so the decoder has no path that is both acoustically plausible and spells قلب. It can only recover the right word if the language model's preference for قلب in context outweighs the acoustic mismatch, which happens for very predictable phrases but not for an isolated or unexpected word. The systematic outcome, seen in real MSA-trained systems on Levantine speech, is a substitution error such as ألب or a deletion, which is why a dialect-aware lexicon or an end-to-end model trained on dialect data (Chapter 5) is needed rather than a larger MSA one.

---

### Flags and notes for the companion website

* Exercises 1 to 7 need no data or code; where a reader wants to verify the segmentation in Exercise 5 with a tool, point them to `Chapter_05_Exercise_05.ipynb`, which runs CAMeL Tools and SentencePiece on the related token وسيكتبونها.
