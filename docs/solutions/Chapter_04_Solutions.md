# Chapter 4 Solutions: Arabic ASR I, Statistical and Deep-Learning Foundations

These solutions follow the numbering of the chapter's exercise list. Exercises 2 and 5 have companion notebooks; their measured outputs are quoted below.

Notebooks for this chapter: [`Chapter_04_Exercise_02.ipynb`](Chapter_04_Exercise_02.ipynb), [`Chapter_04_Exercise_05.ipynb`](Chapter_04_Exercise_05.ipynb).

---

## Exercise 1

**Task.** Explain in your own words why the acoustic score alone cannot reliably decide between عَمّان /ʕammaːn/ 'Amman' and عُمان /ʕumaːn/ 'Oman', and what information the language score adds. Give one carrier sentence that would push the decision each way.

**Suggested solution.**

*Why the acoustic score is not enough.* The two names differ in exactly two cues: the first short vowel (/a/ against /u/) and the length of the /m/ (geminate /mː/ against single /m/). Both cues are fragile in real audio. Short vowels are brief, easily reduced in fast or casual speech, and coloured by the neighbouring pharyngeal /ʕ/; and consonant length is a *duration* cue, which is compressed when speech is fast, masked by noise or reverberation, and blurred by a front end that summarizes each frame independently (Section 2.5). So the acoustic model often returns two candidates with nearly equal scores, or worse, a confident but wrong one. A further problem is representational: if the recognizer outputs undiacritized text, both candidates are spelled عمان, so from the decoder's point of view there is only one written candidate and the acoustic evidence for the vowel has nowhere to go (Section 4.1).

*What the language score adds.* P(W) supplies context: how likely each place name is given the surrounding words. "Stock Exchange in Jordan" makes Amman overwhelmingly likely; "Royal Opera House Muscat" makes Oman overwhelmingly likely. The decoder multiplies the acoustic score by this prior (Figure 4.1), so a small acoustic preference can be overturned by a strong contextual one. For the language score to be usable, the two names must exist as separate candidates, through diacritized output, distinct lexicon entries or distinct internal labels (Section 4.4.2); an undiacritized word-level LM cannot separate them, though a downstream component could still infer the intended place.

*Carrier sentences.*

* Toward Amman: سافرت إلى عمان لزيارة جامعة الأردن (sāfartu ilā ʿammān li-ziyārati jāmiʿati l-urdunn, 'I travelled to Amman to visit the University of Jordan').
* Toward Oman: سافرت إلى عمان لزيارة مسقط (sāfartu ilā ʿumān li-ziyārati masqaṭ, 'I travelled to Oman to visit Muscat').

In both the acoustic material for عمان is the same string of letters; only the following words move the decision.

---

## Exercise 2

**Task.** A recognizer outputs الى المدرسه while the reference is إلى المدرسة. Compute the WER by hand before normalization and after applying the Table 4.2 rules, and state which rules you used. Then write a short Python script that applies your normalization rules to both strings and recomputes the WER. Explain why these are scoring conventions rather than claims that the forms are identical.

**Solution (notebook `Chapter_04_Exercise_02.ipynb`).**

*By hand.*

| Position | Reference | Hypothesis | Literal match? |
|---|---|---|---|
| 1 | إلى | الى | no (hamza below alif absent) |
| 2 | المدرسة | المدرسه | no (ه for ة) |

Before normalization: S = 2, D = 0, I = 0, N = 2, **WER = 2/2 = 100 %**.

Rules used from Table 4.2: **normalize alif forms** (إ to ا) and **normalize tāʾ marbūṭa and hāʾ** (ة to ه, or both to one chosen form). After both, reference and hypothesis are الى المدرسه: S = 0, **WER = 0 %**. The "usually safe" rules (remove diacritics, remove tatweel, normalize punctuation and spacing) change nothing here because neither difference involves them.

*Script output (as executed).*

| Rules applied | Normalized reference | Normalized hypothesis | S | WER |
|---|---|---|---|---|
| none | إلى المدرسة | الى المدرسه | 2 | 100 % |
| remove diacritics, remove tatweel, punctuation and spacing | إلى المدرسة | الى المدرسه | 2 | 100 % |
| normalize alif | الى المدرسة | الى المدرسه | 1 | 50 % |
| normalize alif + normalize ة/ه | الى المدرسه | الى المدرسه | 0 | 0 % |

The notebook's `normalize()` function takes a set of named rules and is applied to both strings, so the report can list exactly which rules produced which number.

*Why these are conventions, not claims of identity.* إلى and الى are one word in two spellings, so merging them is defensible for undiacritized scoring, but the same alif rule also merges words that genuinely differ in hamza. ة and ه are not equivalent in general: المدرسة 'the school' and مدرسه, which can be مُدَرِّسُهُ 'his teacher', are different words with different pronunciations (Section 4.2). A normalization rule states "for the purpose of comparing systems on this benchmark we will not count this difference"; it is a decision about the metric, applied identically to both sides to remove spelling noise, not a linguistic statement that the two forms are the same. Because the choice can move a WER from 100 % to 0 % without changing the recognizer, the rule set and the script must be published with the result.

---

## Exercise 3

**Task.** Using Table 4.4, tokenize a different Arabic sentence of your choice at the word, character and subword levels, give the token counts, and recommend a tokenization for a low-resource dialect recognizer with a justification.

**Suggested solution.** Sentence: الطالبات يدرسن في المكتبة الجديدة (aṭ-ṭālibātu yadrusna fī l-maktabati l-jadīda, 'the female students study in the new library').

| Unit | Tokens | Count | Trade-off |
|---|---|---|---|
| Words | الطالبات · يدرسن · في · المكتبة · الجديدة | 5 | short sequence, but four of the five are inflected or cliticized forms that a word vocabulary must have seen exactly |
| Characters (excluding spaces) | ا ل ط ا ل ب ا ت · ي د ر س ن · ف ي · ا ل م ك ت ب ة · ا ل ج د ي د ة | 29 | no word-level OOV, but a sequence six times longer |
| BPE subwords (illustrative; actual pieces depend on the trained vocabulary) | ال + طالب + ات · يدرس + ن · في · ال + مكتبة · ال + جديد + ة | 11 | learned compromise; frequent clitics and affixes become pieces |
| Morphological segments (CAMeL Tools 1.6.0, `calima-msa-r13`, D3 scheme, actual output) | ال+ طالبات · يدرسن · في · ال+ مكتبة · ال+ جديدة | 8 | linguistically motivated; the D3 scheme separates the article but not inflectional affixes (the ATB scheme returns the 5 words unchanged) |

*Recommendation for a low-resource dialect recognizer.* **Learned subwords (SentencePiece BPE or unigram) with full character coverage, a small vocabulary (roughly 500 to 2,000 pieces), trained on the dialect transcripts after the same normalization used for scoring.** Justification: (1) dialects have no standard spelling and no mature morphological analyzer for most varieties (Table 5.3, "dialect coverage is uneven"), so morpheme units are not available or not reliable; (2) whole words are the worst choice under sparsity, since every spelling variant and clitic combination is a separate rare type; (3) pure characters remove OOVs but make the sequences long and push the burden of learning word structure onto the acoustic model, which hurts most when data is scarce; (4) subwords with character fallback keep the no-OOV guarantee while shortening sequences and letting frequent clitics become units. Keep the vocabulary small because a large BPE vocabulary trained on little text memorizes whole words and degenerates into a word model. Choose the size on the development set and report algorithm, vocabulary size, training text and normalization, as Section 4.8 requires.

---

## Exercise 4

**Task.** You have 80 hours of MSA broadcast speech and 8 hours of Gulf-dialect speech. Describe a training and evaluation plan that avoids a misleadingly high pooled WER, including how you would balance dialects and what you would report per dialect.

**Suggested solution.**

*Why the naive approach misleads.* Pooled by hours, MSA is 91 % of the data; pooled by test words, an MSA-heavy test set makes the overall WER almost entirely an MSA number. A model that has effectively ignored the Gulf data can still post an impressive pooled figure.

*Splits.* Split each corpus separately, speaker-disjoint, and keep the two test sets apart: for example MSA 72 / 4 / 4 hours and Gulf 6 / 1 / 1 hours (train / dev / test). One hour of Gulf test speech is small, so make sure it contains several speakers and report confidence intervals or a significance test (Chapter 4 Reproducibility Note, Chapter 1).

*Balancing during training.* Pool the two training sets but do not let the 12:1 ratio stand. Options, from simple to stronger: (a) **upsample** the Gulf data, repeating it 3 to 4 times per epoch (with SpecAugment and speed perturbation so the repeats are not identical) so that it forms about 25 to 35 % of the batches; (b) **temperature or square-root sampling** over the two dialects when drawing batches; (c) **two-stage training**: train on the pooled data, then fine-tune on Gulf plus a small MSA replay set so that MSA performance does not collapse; (d) if a self-supervised encoder is available, continue pretraining on any unlabeled Gulf audio first (Chapter 6). Tune the mixing ratio on the *Gulf* development set as well as the MSA one, not on the pooled dev set. Make sure the tokenizer and any external language model are trained on text that includes the Gulf transcripts, otherwise the LM will pull dialectal words toward MSA forms (Section 5.6).

*What to report.* For each dialect separately: WER and CER, the number of test hours, speakers and words, and the normalization script used. Also report a **macro-average** (the mean of the two dialect WERs) alongside the pooled WER so that a Gulf deficit is visible. Add an error analysis on the Gulf set that separates acoustic errors, OOV or spelling variation, and MSA-ward substitutions (Section 4.8 and Section 6.5). Finally, compare against two baselines on the same test sets: the MSA-only model and a Gulf-only model, which shows whether pooling helped the dialect or merely diluted it.

---

## Exercise 5

**Task.** Assume a simple clitic-stripping analyzer that removes leading conjunction, article and preposition clitics and trailing pronoun clitics. Segment وللمكتبة into its clitics and stem, explain how this segmentation reduces OOV forms compared with word-level tokenization, and state your assumptions. Then run a specified tokenizer on this exact word and compare its output with your manual segmentation, reporting tool name, version, model and segmentation scheme.

**Solution (notebook `Chapter_04_Exercise_05.ipynb`).**

*Assumptions about the analyzer.* It strips at most one conjunction (و, ف), one preposition (ب, ل, ك) and the article ال from the left, and one pronoun enclitic (ـه, ـها, ـهم, ـك, ـي, ...) from the right. It leaves inflectional affixes (ـة, ـات, ـون) on the stem. It knows the orthographic rule that لِ + الـ is written لل (the alif of the article is dropped after the preposition ل), which a naive search for the literal string ال would miss.

*Manual segmentation.*

| Piece | Type | Gloss |
|---|---|---|
| وَ wa- | conjunction proclitic | and |
| لِ li- | preposition proclitic | for |
| الـ al- | article proclitic (surface: the second ل of لل) | the |
| مَكْتَبَة maktaba | stem | library |
| (none) | pronoun enclitic | |

Result: **و + ل + ال + مكتبة** (4 pieces).

*Why this reduces OOV forms.* A word vocabulary needs a separate entry for every surface string: مكتبة, المكتبة, للمكتبة, وللمكتبة, بالمكتبة, مكتبتها, ومكتبتهم and so on, each individually rare. After stripping, all of them share the unit مكتبة plus a few very frequent clitic tokens, so the number of types falls toward the number of stems, the counts per type rise, and a never-seen combination such as فبمكتبتهم is no longer OOV as long as its stem and clitics were each seen separately.

*Tool run.* CAMeL Tools **1.6.0**, `MLEDisambiguator` pretrained on **`calima-msa-r13`**, `MorphologicalTokenizer` with `split=True`. Executed output:

| Scheme | Output | Pieces | Agreement with manual |
|---|---|---|---|
| `d3tok` (D3) | و+ ل+ ال+ مكتبة | 4 | identical |
| `atbtok` (ATB, Penn Arabic Treebank) | و+ ل+ المكتبة | 3 | article kept on the noun |
| `bwtok` (Buckwalter) | و+ ل+ ال+ مكتب +ة | 5 | also splits the feminine suffix |

The chosen analysis was وَلِلمَكْتَبَة with Buckwalter tag `وَ/CONJ+لِ/PREP+ال/DET+مَكْتَب/NOUN+َة/NSUFF_FEM_SG`, lemma مَكْتَبَة, part of speech noun, gloss "and + to; for + the + library; bookstore + [fem.sg.]". The D3 scheme matches the assumed analyzer exactly; the other two schemes are also correct but draw the clitic/affix line elsewhere, which is why the scheme must be named.

*Optional cross-check with Stanza* (1.14.0, Arabic PADT model, CPU): in sentence context the word was expanded to و (CCONJ) + ل (ADP) + المكتبة (NOUN, lemma مَكتَبَة), the ATB-style three-piece result; in isolation it was returned unsplit. Stanza is a UD tokenizer and tagger, not a full morphological analyzer, and it should be described as such (Section 4.4.3).

---

### Flags and notes for the companion website

* The book's Table 4.4 gives an illustrative BPE segmentation; the solution to Exercise 3 does the same and marks it as illustrative. Readers who want an actual BPE output can train one in `Chapter_05_Exercise_05.ipynb`.
* Stanza's lemma for some verbs (for example يكتبون) was observed to be wrong in the tested version; this is worth mentioning to students as a reason to prefer a dedicated Arabic analyzer for morphology.
