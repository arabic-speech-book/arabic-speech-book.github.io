# Glossary

Every term defined across the fourteen chapters, merged into one alphabetical, searchable list — **293 distinct terms**, 337 definitions. Where two chapters define a term differently, both wordings are kept, each tagged with its chapter. Use the search box at the top of the page to jump to a term.


## A

**Abjad**

- *(Ch. 1)* a writing system in which the letters represent the consonants and the long vowels, leaving the short vowels to optional marks. Arabic is written as one, which is why the same string of letters can spell several different words
- *(Ch. 2)* the type of script Arabic uses: the letters written are the consonants and the long vowels, while the short vowels are left to the optional diacritics and in most real text are not written at all

**Acoustic model**

- *(Ch. 4)* the component that says how words sound, scoring how well a candidate’s expected sounds match the observed feature vectors; classically a Hidden Markov Model with Gaussian-mixture emissions, later a deep network
- *(Ch. 9)* the stage that turns a phoneme sequence into a mel spectrogram, fixing what is said, for how long, and at what pitch

**Adapter**

- *(Ch. 6)* a small bottleneck layer inserted into a frozen backbone and trained on its own, so one shared model can serve many Arabic dialects and tasks at a fraction of the cost of retraining it
- *(Ch. 11)* a small trained module placed in front of, or inside, a large frozen model so that the model can be reused without retraining it; in this chapter, usually another word for the connector

**Adversarial example** — a small, often inaudible perturbation added to audio that makes a recognizer produce a transcript the attacker chose. Carlini and Wagner showed targeted attacks that turn any waveform into any transcript a system will report, which is why robustness has to be measured against realistic attacks rather than assumed *(Ch. 13)*

**Agent** — a system that plans, calls a tool or a search, and acts on what comes back, rather than answering from memory alone *(Ch. 11)*

**Aliasing** — the irreversible corruption that follows sampling too slowly, in which a high frequency masquerades as a lower one that was never spoken; an anti-aliasing filter prevents it by removing the too-high frequencies before sampling *(Ch. 3)*

**Alignment** — the organizing problem of this chapter: an utterance has many frames and its transcript few tokens, and the training data never says which frames produced which tokens. Every model family below is a different answer to how to train without that frame-level labeling *(Ch. 5)*

**Anchor** — a deliberately degraded version of a recording, included in a listening test so that the low end of the scale is used *(Ch. 9)*

**Annotation guideline** — the written document that fixes the transcription convention, the diacritization decision, the markup for noise and overlap, the segmentation rule and the metadata fields, before annotation begins. A guideline written first is what makes two annotators agree; a guideline written afterwards is an excuse, and what an agreement check produces is an amendment to it *(Ch. 14)*

**Arabic Dialect Identification** — deciding which Arabic variety a recording is in, a choice among varieties of one language that share a script and much of their vocabulary rather than among separate languages, which is what makes it harder than language identification. It is rarely the end goal in this chapter but a fast first stage that labels the variety so the system can pick the right recognizer, the right language model, or the right human reviewer *(Ch. 8)*

**Articulatory-level feedback** — feedback that names the articulation to correct rather than only the sound that was wrong, telling the learner which part of the vocal tract to engage for a pharyngeal or an emphatic consonant. Arabic mispronunciation work adds it because it is more actionable than a bare error flag and it targets exactly the sounds learners find hardest; where a language model writes the feedback text, that text is fluent and still has to be checked, because fluency is not correctness *(Ch. 12)*

**Attention** — a mechanism that lets every frame look directly at every other frame and decide which ones matter, in one parallel operation, instead of passing information hand to hand along the sequence *(Ch. 4)*

**Attention-based encoder-decoder** — a model whose encoder turns the frames into states and whose decoder emits one token at a time, computing before each token a weight over all encoder states and reading a focused summary of the audio. It conditions each token on all the tokens before it, so it carries a strong internal language model; this is the Listen-Attend-Spell family, and modern versions use the Transformer or Conformer encoders of Chapter 4 *(Ch. 5)*

**Attribution** — asking which system produced a fake rather than only whether the audio is fake, the question a forensic investigation and a misuse investigation both need. Characterization is its companion, asking what kind of manipulation was applied *(Ch. 13)*

**Audio codec** — a system that represents a short slice of sound as a small whole number drawn from a learned set, so that a recording becomes a sequence of integers, called codec tokens *(Ch. 9)*

**Audio watermarking** — embedding an imperceptible, detectable signal in generated speech so it can later be recognized as synthetic and traced to its origin, with modern methods embedding a localized mark that survives common edits and is detected from part of a clip. It only works if generators choose to embed it, an adversary may try to strip it, and a mark proves origin rather than truth *(Ch. 13)*

**Audio-language model**

- *(Ch. 1)* a system built by projecting an audio encoder into a large language model and instruction-tuning the pair, so that it follows spoken instructions rather than only transcribing; the paradigm that opened in 2023, developed in Chapters 6 and 11
- *(Ch. 11)* a large language model with an audio input path attached: an audio encoder, a connector, and the language model itself. Abbreviated ALM throughout this chapter

**Audiovisual recognition** — recognition that reads the moving mouth alongside the audio, useful here because the articulation a learner is told to move is often visible, the lips closing for a bāʾ ب and meeting the teeth for a fāʾ ف and because in a crowded room the camera recovers some of the place-of-articulation information the noise erased. It supplements the scoring rather than replacing it, since the pharyngeals and emphatics of Chapter 2 are made behind the mouth and leave almost nothing on the lips *(Ch. 12)*

**Augmentation** — perturbing the training features so the model sees more variety than the data literally contains. SpecAugment, which masks bands of frequency and spans of time in the log-mel features, is the usual method, and it is applied to the training data only so that evaluation stays comparable *(Ch. 4)*

**Automatic dubbing** — replacing the soundtrack of a video with a translated soundtrack, which is the speech translation of Chapter 10 under two further constraints: the translated line has to fit the time the original occupied and it has to sit under the same room acoustics. A working system controls the length of the translation, aligns its prosody to the source speech, adjusts the duration of the synthesized utterance and restores the background it removed. For Arabic it must also choose a variety, which is a question about the audience rather than about the model *(Ch. 12)*

**Average Lagging** — the latency metric for simultaneous translation, measuring how far on average the output trails an ideal speaker-synchronized output. It is reported beside translation quality so that the two can be traded off honestly, and this chapter asks for it in seconds as well as in steps, because seconds are what a listener waits1 *(Ch. 10)*

**Awzān** — the patterns, traditionally called the forms or measures, that interleave with a root to give a stem, each with a regular meaning, so Form I is the basic verb, Form II is causative or intensive, and Form III often expresses doing something to someone *(Ch. 2)*


## B

**Back end** — the half of a text-to-speech system that turns a pronounceable form into sound; in the classical division, the acoustic model and the vocoder *(Ch. 9)*

**Baum-Welch algorithm** — the training algorithm for a Hidden Markov Model, which adjusts the state transitions and the Gaussian mixtures to fit the data *(Ch. 4)*

**Beam search** — the decoding search that keeps several competing hypotheses rather than committing to one symbol at each step, and the place where an external language-model score is added. The beam width, meaning how many hypotheses are kept, is a tuned and reported setting: too wide is slower for little gain, too narrow causes search errors *(Ch. 5)*

**Beamforming** — combining the signals of a device’s several microphones so that sound arriving from the speaker’s direction adds up while sound from other directions cancels out. It works well against a competing talker at the higher frequencies that carry consonant detail, and much less well at the low frequencies where room noise sits *(Ch. 8)*

**Benchmark** — a fixed dataset with defined training, development, and test splits, against which competing systems can be compared *(Ch. 1)*

**Best-path decoding** — the cheapest way to decode a CTC model, taking the most likely symbol in each frame and collapsing the result; a beam search that sums alignments does better, optionally with an external language model *(Ch. 5)*

**Bias audit** — checking a corpus for skew in dialect, gender, and speaker coverage, and reporting per-dialect results next to the pooled figure, so that thin coverage of a minority variety is visible rather than hidden in an average *(Ch. 7)*

**Bit depth** — the setting that fixes how many levels quantization may round a sample to, with 16-bit audio offering 65,536 levels *(Ch. 3)*

**Blank** — the one extra output symbol CTC adds, meaning ‘emit nothing here’. It lets the model stay silent through the many frames that carry no new token, and it separates a genuine double letter, such as a gemination marked by the Shadda of Chapter 2, from a single token merely held across several frames *(Ch. 5)*

**BLEU** — the standard headline metric for translation quality, counting n-gram overlap with a reference translation and applying a brevity penalty. It is sensitive to tokenization and normalization and correlates only loosely with human judgment, and because the n-grams it counts are word n-grams it marks a correct Arabic translation wrong when a pronoun is attached as a suffix rather than written separately, or a name is spelled with a different alef1 *(Ch. 10)*


## C

**Captioning** — recognition used to put spoken Arabic on the screen, the listening-side service that gives deaf and hard-of-hearing people access to it. Its quality depends on dialect-robust recognition, so it inherits every limitation of the recognizer behind it *(Ch. 12)*

**Cascade** — the modular architecture of both halves of this chapter: a recognizer transcribes the source speech, and a machine-translation model translates that transcript or a text model reads it and returns intents and slots. It reuses strong components, benefits from abundant text parallel data, and can be inspected stage by stage, and it hands every recognition error to the next stage as though it were right1 *(Ch. 10)*

**Cepstral normalization** — subtracting the average of each feature and scaling it to unit variance (CMVN), which removes the roughly constant offset a fixed channel or microphone adds and so reduces slowly varying channel and recording-condition effects. It can also remove speaker-specific cues, so its scope, per utterance, per speaker, or global, must be reported *(Ch. 3)*

**Channel leakage** — the failure in which a dialect was recorded mostly on one channel and the model learns the channel instead of the dialect, so the identifier is really naming the source rather than the variety *(Ch. 8)*

**Character Error Rate** — the same count of substitutions, deletions, and insertions as the Word Error Rate, computed over characters rather than words. It tells a near-miss from a total miss, which matters for a morphologically rich language, but it can over-reward character overlap in words that are morphologically wrong, so the two rates are reported together rather than either replacing the other *(Ch. 1)*

**Character-level score** — a translation score computed over character n-grams rather than word n-grams, called chrF in the tooling of Table 10.6, and the score this chapter asks for beside the word-level one whenever Arabic is the target. Character n-grams degrade gradually where word n-grams fail outright, so a spelling difference that is ordinary in written Arabic costs a little rather than everything1 *(Ch. 10)*

**Child speech** — the speech of children, harder to recognize than adults’ for two reasons at once: shorter vocal tracts shift the acoustics, and pronunciation, grammar and fluency are still developing and highly variable. Adult-trained models degrade badly on it, and the gap is large for Arabic, where an evaluation of a mainstream recognizer on an Arabic children’s set found a word error rate around 0.66 against well under 0.20 on adult Arabic. Children are also a protected group, so their speech demands guardian consent, minimal collection, secure storage and clear limits on use *(Ch. 12)*

**Clinical documentation** — the healthcare use in which a transcript is turned into a structured clinical note by a language model. The published evidence for that middle step runs almost entirely on written or corrected transcripts rather than on what a recognizer actually produced, so the recognition errors of Chapter 4 and the dialectal errors this book has tracked are not in the measurement at all *(Ch. 12)*

**Clipping**

- *(Ch. 3)* the unrecoverable distortion that appears when the recording level is set too high, so the loudest samples hit the top of the scale and the peaks of the wave are flattened. In speech it strikes the high-amplitude portions, often vowels and stressed syllables, and distorts formants and voicing, so setting the level correctly while recording matters more than any later processing
- *(Ch. 7)* the flat-topped distortion produced when the signal exceeds the largest value the converter can represent. It cannot be undone afterwards, which is why levels are set with headroom, peaking near minus 6 dBFS, and why no limiting or automatic gain is applied

**Clitic** — a small grammatical word that attaches directly to a stem, a proclitic at the front (the conjunction wa- ‘and’, the preposition bi- ‘with/by’, the definite article al- ‘the’, the future marker sa-) or an enclitic at the back (object and possessive pronouns). Several can stack on one stem, so a single written token can correspond to a whole English phrase *(Ch. 2)*

**Cocktail-party problem** — two people talking at the same time, which cleaning does not fix because the recording holds two signals and only one of them is wanted; the mixture has to be split into one stream per speaker first *(Ch. 8)*

**CODA** — the conventional orthography proposed for dialectal Arabic, a spelling convention meant to make dialect transcripts consistent where the dialects have no standard spelling of their own; CODA* is its unified extension *(Ch. 2)*

**Code-switching**

- *(Ch. 1)* the alternation between languages, or between Modern Standard Arabic and a dialect, within a single utterance; ordinary conversation for Gulf speakers mixing Arabic and English and for Maghrebi speakers mixing Arabic and French, and treated in Section 8.4
- *(Ch. 2)* mixing two languages inside one sentence, Arabic and English in the Gulf or Arabic and French in the Maghreb, which violates the phonotactic and syntactic regularities that recognizers and language models learn from monolingual data
- *(Ch. 7)* movement between languages or varieties inside a recording, for example between English and Arabic, which a transcription convention has to settle with an explicit rule. ZAEBUC-Spoken is worth reading before writing one, because it annotates the switching rather than normalizing it away
- *(Ch. 8)* mixing languages or registers inside one stretch of speech, English inserted into Arabic in Gulf technical and business settings and French woven through everyday Maghrebi speech. The chapter separates two cases usually discussed as one: switching into English or French crosses a language boundary, where the lexicon and sometimes the script change, while switching between Modern Standard Arabic and a dialect crosses a register boundary inside one language, where the words often stay and the pronunciation and grammar shift under them

**Codebook** — the learned, finite inventory of speech units that quantization maps the continuous latents onto, so that the contrastive choice in wav2vec 2.0 is made over a discrete set rather than an unbounded space *(Ch. 6)*

**Cohen’s kappa** — chance-corrected agreement between two raters on categorical labels such as dialect. Thresholds are task-dependent: a value near 0.6 may be usable for difficult dialect labeling, while simpler labels should reach higher *(Ch. 7)*

**Collapsing** — the two rules that turn a frame-length string of labels into a transcript, first merge runs of the same symbol, then delete the blanks. Many different frame labelings collapse to the same transcript, which is exactly what lets CTC train without a given alignment *(Ch. 5)*

**COMET** — a neural translation metric that compares the output and the reference in a learned multilingual space instead of counting overlap. It tracks human judgments much more closely than BLEU and is now reported alongside or instead of it, though for dialectal or code-switched Arabic it is a useful neural metric and not a substitute for human adequacy and meaning checks1 *(Ch. 10)*

**Command accuracy** — the primary metric of the case study: the proportion of spoken commands the system acts on correctly, measured on speakers it has never heard. It travels with a second metric, the false-accept rate on speech that is not a command, because a wrong action is worse than no action *(Ch. 14)*

**Computer-assisted pronunciation training** — automatic feedback to a learner on how they sound, and the pipeline this chapter builds: the learner reads a text the system already has, the audio is force-aligned to the expected phones, each phone is scored against how a correct production would look, and the scores are turned into feedback the learner can act on. Because the target text is known, alignment is far easier than open recognition, which is what makes reliable phone-level scoring possible *(Ch. 12)*

**Concatenative synthesis** — speech built by joining short recorded units from a database; also called unit selection *(Ch. 9)*

**Conditional independence** — the one structural limitation of CTC: given the audio it treats the output tokens as independent of one another, so it has no built-in sense of which word should follow which. This is the gap an external language model fills (Section 5.6) *(Ch. 5)*

**Conformer** — the encoder this book builds on: a block that keeps the Transformer’s self-attention for global context and adds a convolution module for local acoustic patterns, wrapping both in feed-forward layers, so the model has global reach and local sensitivity at once *(Ch. 4)*

**Confusion matrix** — a table whose rows are true labels and whose columns are predicted labels, and the diagnostic this chapter asks for beside accuracy. Its off-diagonal mass concentrates among neighboring dialects, the signature of the continuum, while a sudden confusion between distant dialects may signal a data or channel artifact rather than a linguistic one *(Ch. 8)*

**Connectionist Temporal Classification** — the simplest answer to alignment: label every frame with either a real token or blank, collapse the result, and define a transcript’s probability as the sum of the probabilities of every frame labeling that collapses to it. Training maximizes that sum, so the model is never told the alignment and learns whichever alignments make the data likely *(Ch. 5)*

**Connector** — the trained piece between the audio encoder and the language model. It does two jobs: it shortens the audio sequence, and it maps the width of each vector into the space the language model reads *(Ch. 11)*

**Contamination** — test material that has already been seen in training, so that a score measures memory rather than ability *(Ch. 11)*

**Continual pretraining** — keeping the self-supervised objective running on a large pool of unlabeled in-domain Arabic audio before any fine-tuning, so a mostly non-Arabic encoder shifts toward Arabic; curated unlabeled corpora such as Aswat exist for exactly this *(Ch. 6)*

**Contrastive objective** — a pretext task that hides part of the signal and asks the model to pick the true continuation, or the true latent for a masked position, out of a set of distractors, the idea behind Contrastive Predictive Coding and wav2vec 2.0 *(Ch. 6)*

**Conventional Orthography for Dialectal Arabic**

- *(Ch. 7)* a principled, consistent way of writing varieties that have no standard orthography, which keeps annotators from spelling the same word three ways. The later unified guidelines, CODA*, carry the same treatment across many dialects and are where a project starting today should begin
- *(Ch. 14)* the spelling convention this chapter adopts so that two annotators write the same spoken dialectal word the same way. Dialectal Arabic has no standard spelling, so the convention is a project decision that has to be made before annotation rather than discovered during it


## D

**Data card** — a short document that records a corpus’s motivation, its composition, how the audio was collected and consent obtained, the annotation convention, the license, the official splits, and the known limitations. Few Arabic speech corpora carry one, so for most resources the answers have to be assembled from the paper, the distributor’s terms, and the files themselves *(Ch. 7)*

**Data minimization** — collecting no more speech than the stated purpose requires, one of the design principles this chapter treats as stable whatever the jurisdiction, beside explicit consent, purpose limitation, encryption, retention limits, access control and deletion rights *(Ch. 12)*

**Data statement** — a written account of what a dataset contains and how it was collected, published alongside it so that a reader can judge what a system trained on it will and will not do. With model cards it is the documentation half of accountability *(Ch. 13)*

**Datasheet** — the one-page record of why a corpus was built, how it was collected and annotated, who the speakers are in aggregate, what the licence permits, what is known to be missing or biased, and how the splits are defined. It is often the most durable output of a project, since it lets a future team judge whether the corpus fits their purpose without downloading a single file *(Ch. 14)*

**Decoder** — the engine that searches the candidate space for the best-scoring transcript, an algorithm rather than a trained model, and the component that makes a search over millions of candidates feasible *(Ch. 4)*

**Decoder-only** — a transformer with no separate encoder and no cross-attention, which continues a sequence one position at a time; the shape of every language model in this chapter *(Ch. 11)*

**Decoding graph** — the single searchable network the decoder walks, built by composing four weighted transducers, each a graph that maps one sequence to another with weights: the HMM topology, the context, the lexicon, and the language model. Recognition then becomes one best-path search with all four knowledge sources applied at once *(Ch. 4)*

**Deep fusion** — folding the external language model into the network itself, the heavier alternative to adding its score during the search *(Ch. 5)*

**Deepfake detection** — deciding whether a recording is genuine, synthetic or replayed, formalized by the ASVspoof challenge series. It is an adversarial problem rather than a solved one: as generative models improve, detectors trained on yesterday’s fakes degrade, so a detector needs fresh data and, for Arabic, data across dialects and across the generators it will actually face *(Ch. 13)*

**Development set** — the split used for tuning and early stopping, which exists so that the test set stays untouched; every decision taken by looking at test scores spends a little of the test set’s value, and it cannot be earned back *(Ch. 7)*

**Diacritization**

- *(Ch. 1)* the writing, or the automatic restoration, of the optional marks (Tashkīl) that carry the short vowels. They are absent from almost all real Arabic text, so the same letters map to different words and pronunciations, which complicates both recognition and synthesis
- *(Ch. 2)* restoring the missing marks to written Arabic, also called vowelization, with accuracy reported as a diacritic error rate. Restoring the vowels inside the word is much easier than restoring the final case endings, which depend on syntax reaching across the whole sentence
- *(Ch. 7)* whether the short vowels are written into a transcript. Most transcripts leave them out, which is easier and matches reading habits, while a fully diacritized transcript costs more and serves synthesis and Qur’anic work
- *(Ch. 9)* restoring the short-vowel marks that Arabic writing usually leaves out, so that a word can be pronounced; Tashkīl

**Diacritized target** — a training transcript written with the full short-vowel diacritics rather than in the far more common undiacritized form. It makes the task harder and the sequences longer but produces vocalized output useful for synthesis and reading, and the metric reported must match the choice *(Ch. 5)*

**Dialect continuum**

- *(Ch. 1)* the way the Arabic dialects shade gradually into one another between neighboring regions while speakers from distant regions may struggle to understand each other, so that Arabic is not one target condition for a speech system but many
- *(Ch. 2)* the geographic and social gradient along which the spoken varieties shade into one another, so neighboring regions generally understand each other easily while speakers from opposite ends may struggle
- *(Ch. 8)* the arrangement in which features change gradually across geography, so that neighboring regions sound alike while distant ones diverge and there is no crisp line between them. It is why an identifier’s errors are not random: a dialect is confused with its neighbors far more often than with distant varieties

**Dialect identification**

- *(Ch. 1)* the task of deciding which variety of Arabic is being spoken, scored by accuracy and macro-averaged F1
- *(Ch. 7)* the task of labeling which variety a recording is in, set across five classes by MGB-3, as a finer 17-way task by MGB-5, and again on common data by the NADI 2025 shared task

**Dialect mixing** — the training-time decision about how varieties are balanced in the data. A recognizer trained on a pooled mixture tends to do well on the dominant variety and poorly on the rest, so under-represented varieties are reweighted or resampled, a dialect tag may be added, and error rates are reported per dialect as well as pooled *(Ch. 4)*

**Dialogue state tracking** — maintaining, across several turns, the accumulated set of intents and slot values that represent what the user wants so far, the backbone of any multi-turn assistant. It is what neither intent detection nor slot filling does, because a later turn may name no intent and merely add a detail to a request already made; scored with joint goal accuracy1 *(Ch. 10)*

**Diarization Error Rate** — the metric for diarization, which adds up three different mistakes over the timeline: false alarm, marking speech where there is silence, missed speech, the reverse, and speaker confusion, giving the right speech to the wrong person. The chapter asks for the three parts separately, and for the collar tolerance, whether overlap was scored at all, and whether the number of speakers was known or estimated, because the headline figure moves with each of those choices *(Ch. 8)*

**Differential privacy** — adding calibrated noise so that what is released cannot be traced back to any one contributor, used beside secure aggregation where federated updates alone would still leak information *(Ch. 13)*

**Diffusion model** — a generator that starts from noise and removes it step by step until the target appears, instead of predicting the target directly *(Ch. 9)*

**Diglossia**

- *(Ch. 1)* the coexistence of two forms of a language used for different purposes; in Arabic, Modern Standard Arabic for news, formal writing, and education, and regional dialects for everyday conversation
- *(Ch. 2)* the coexistence of a formal variety used for writing and formal settings with spoken varieties used for daily life, the classic case being Arabic, where speakers slide along a continuum between the two depending on how formal the situation is
- *(Ch. 8)* the coexistence of Modern Standard Arabic with the regional spoken dialects of Chapter 2, so that a single recording can drift between a dialect and MSA within a few seconds

**Diphone** — a recorded unit running from the middle of one phone to the middle of the next, so that the join falls where the sound is steadiest; the usual unit of concatenative synthesis *(Ch. 9)*

**Disaggregated evaluation** — reporting results per group rather than as one number, per dialect and per gender in this chapter, with the gap between the best and the worst group stated. A single pooled error rate lets a large well-served population hide a small badly-served one, which is the central fairness pitfall of Arabic speech work *(Ch. 13)*

**Discrete audio token** — a whole number standing for a short slice of sound, produced by a neural codec, so that audio becomes a sequence a language model can predict *(Ch. 11)*

**Discrete cosine transform** — the transform applied to the log-mel energies in the MFCC pipeline, which compacts the smooth spectral envelope and decorrelates the band energies so that only the low-order coefficients need be kept *(Ch. 3)*

**Disordered speech** — speech affected by a speech disorder, heterogeneous rather than one condition: dysarthria, apraxia, stuttering, and hearing-related or developmental differences change the acoustics in different ways, so a model validated on one group cannot be assumed to work for another. Mainstream recognizers, trained on typical speech, degrade sharply on it, and evaluation must use the target population or the numbers are meaningless *(Ch. 12)*

**Distillation** — compressing a large, accurate teacher model into a small, fast student that imitates it, trading a little accuracy for speed on phones and other low-power devices, as the Arabic-centric HARNESS models do *(Ch. 6)*

**Distractor** — a competing latent drawn from elsewhere in the utterance or the signal and offered alongside the true one, so that a contrastive model has to identify the correct answer instead of taking a trivial shortcut such as copying the previous frame *(Ch. 6)*

**DNN-HMM hybrid** — the bridge between classical and modern ASR: the HMM, lexicon, language model, and decoder are all kept, and only the Gaussian-mixture emission scorer is replaced by a deep network that outputs a score for every senone at once *(Ch. 4)*

**Dynamic time warping** — the technique that aligns two utterances by stretching and compressing the time axis before comparing them, which let template matching survive the fact that no two utterances share the same duration. It worked for small vocabularies and single speakers and did not scale *(Ch. 1)*

**Dysarthria** — a speech disorder whose atypical articulation, timing and voice quality defeat recognizers built on typical speech. There is no substantial corpus of real Arabic dysarthric speech, so the one peer-reviewed Arabic result augments healthy Arabic speech with transformations learned from English dysarthric data and evaluates largely on speech it generated, which is evidence that the data is missing rather than evidence that the method works for an Arabic speaker with dysarthria *(Ch. 12)*


## E

**Emergent ability** — a skill a model shows on a task it was never explicitly trained for *(Ch. 11)*

**Emphasis spread** — the carrying of the dark, backed coloring of an emphatic consonant onto the sounds around it, so a whole syllable can bear the imprint of one emphatic; its strength and domain vary by dialect, direction, segment type, and distance from the emphatic *(Ch. 2)*

**Emphatic consonant** — a consonant produced with a constriction at the back of the vocal tract. Its acoustic evidence lies less in the consonant than around it, in the lowered second formant of neighboring vowels, so the decisive evidence is smeared across a window of frames that a model must learn to read *(Ch. 1)*

**Emphatic consonants** — the Arabic consonants made with a secondary pharyngealized or velarized constriction, the root of the tongue pulled back toward the pharynx, which lowers the second formant of a neighboring vowel and gives it a dark quality. They contrast with their plain counterparts, so /t/ against /tˤ/ is the difference between tīn ‘figs’ and ṭīn ‘mud’ *(Ch. 2)*

**Encoder-decoder** — the architecture of Section 5.4: an encoder that reads the whole input and a decoder that attends over it while producing the output. Whisper is one, and an audio-language model built on Whisper keeps only its encoder *(Ch. 11)*

**End-to-end model**

- *(Ch. 1)* a single neural network that maps audio directly to text, folding in the separately trained parts of the hybrid system, although practical systems still keep text normalization, tokenization, and language-model fusion around it
- *(Ch. 5)* a single neural network that learns the map from audio to text directly, trained from audio-transcript pairs with no separately built pronunciation lexicon, no grapheme-to-phoneme step, and no separately built alignment. The price of that simplicity is that the model must discover the alignment on its own
- *(Ch. 10)* a single model trained to map source speech directly to the target, English text in the translation half or intents and slots in the understanding half, with no transcript in between. It avoids the lossy hand-off, can be faster, and can use acoustic cues that a transcript discards, at the cost of paired data that is scarce for Arabic and scarcer still for its dialects; its errors are internal, so there is nothing in the middle to inspect1

**End-to-end synthesis** — one network trained from a linguistic form straight to a waveform, with no separate acoustic model or vocoder *(Ch. 9)*

**Energy** — loudness, one of the three quantities a non-autoregressive acoustic model predicts explicitly; it marks emphasis *(Ch. 9)*

**Enhancement objective** — the extension WavLM adds to masked prediction: noise and overlapping speech are mixed in during pretraining and the model must still predict the targets for the clean primary speaker, so the representations learn to ignore interference. That robustness suits real Arabic broadcast, talk-show, and telephone audio *(Ch. 6)*

**Equal Error Rate** — the usual single number for speaker verification, the operating point at which the false accept rate and the false reject rate are equal, where lower is better. A real product rarely runs at it: a bank sets a stricter threshold, accepting more false rejects to push false accepts very low, because letting an impostor into an account costs far more than asking a customer to try again *(Ch. 8)*

**Equal error rate** — the operating point at which a verification system’s false-accept and false-reject rates are equal, used here as the privacy side of an anonymization result: how well an attacker’s speaker recognition still works on the anonymized audio *(Ch. 13)*

**Error propagation** — the structural weakness of the cascade: a word the recognizer got wrong is passed on as if it were correct, and the translation that follows is grammatical, confident, and not what the speaker said. It costs more in Arabic than in most languages, because dialectal recognition is exactly where the errors are and nothing downstream flags them1 *(Ch. 10)*

**Evaluation campaign** — a set of shared tasks run on common data under a fixed condition, with one scoring script, a rule about what may be trained on, and a system description published beside every result. Two systems compared under one campaign’s constraints are comparable; two numbers taken from two papers usually are not, even when both name the same metric, because the tokenization, the normalization and the training data are rarely the same1 *(Ch. 10)*

**Expert human raters** — the qualified people whose judgments a pronunciation, recitation or clinical assessor must be checked against, because an automatic score that disagrees with them is not yet usable. A report has to state the rater pool and their qualifications, the rubric, the population tested and its consent basis, and the agreement between the system and the experts *(Ch. 12)*


## F

**False-accept rate** — how often a system acts on speech that was not addressed to it, measured on an out-of-set script recorded for the purpose. For a command system it matters more than accuracy, because the cost of a wrong action is higher than the cost of no action *(Ch. 14)*

**Federated learning** — training a shared model by sending model updates rather than raw audio to a server, so the speech never leaves the device. It reduces privacy risk without eliminating it, since updates can leak, and for Arabic it has a second use: learning from dialectal speech that users will not upload, without building a central store of sensitive recordings *(Ch. 13)*

**Feed-forward network** — the starting point of the architecture story, a network that scores each frame from a fixed window of neighbors and therefore sees only local context; it cannot use evidence many frames away *(Ch. 4)*

**Fine-tuning** — the second stage of the recipe, in which a pretrained encoder is adapted to recognition with a small labeled set. Full fine-tuning updates every weight and fits best when labeled data and compute are ample, at the cost of a separate full-size model per task; the alternative is to freeze the encoder and train only a light head or a small insert on top *(Ch. 6)*

**Fleiss’ kappa** — the same chance correction as Cohen’s kappa generalized to any number of raters, used where three or more annotators label the same sample, for example with dialect labels *(Ch. 7)*

**Forced alignment**

- *(Ch. 3)* the automatic production of time-aligned labels, which say where each word and phone falls in the audio, using a tool such as the Montreal Forced Aligner. On dialectal Arabic, where pronunciations diverge from MSA and orthography is unstandardized, off-the-shelf aligners frequently fail and the output needs a specialized dialectal model or substantial manual correction
- *(Ch. 7)* giving a model the words that were said so that it works out when each was said, placing the known words, and often the phones, in time against the audio. It is what produces the time-stamped boundaries an annotation tool displays and a trainer consumes, and for dialectal Arabic it still needs correction by hand
- *(Ch. 12)* aligning the audio to a text the system already has, using an acoustic model from Chapter 4, so that every expected phone receives a start and an end time. It is the stage that makes phone-level scoring possible, and it is the alignment of the earlier chapters run under an easier condition, since the words are known in advance
- *(Ch. 14)* computing where each word and phone falls in the audio from a transcript the system already has, which produces time-aligned labels for hundreds of hours without hand-marking boundaries. Its quality depends on the dialect match and the transcript, so the output is spot-checked before it is treated as ground truth

**Forensic voice comparison** — the analysis of recordings for identity, authenticity and origin in support of an investigation. An overconfident match or a missed fake can affect a person’s liberty, so the methods must be calibrated, documented, and validated on the population they are used on rather than on another language *(Ch. 13)*

**Formant**

- *(Ch. 2)* a resonance of the vocal tract, numbered upward from F1. F1 and F2 mainly distinguish vowels, F1 tracking how open the mouth is and F2 how far forward or back the tongue is, which is why an emphatic consonant, pulling the tongue back, shows up as a lowered F2 in the vowel beside it
- *(Ch. 3)* one of the dark horizontal bands of a spectrogram, introduced in Chapter 2 and estimated here from the LPC spectrum. The second formant, written F2, is the one this chapter measures, because it is lowered in a vowel next to an Arabic emphatic consonant

**Formant synthesis** — speech built from rules that drive a set of resonators, with no recordings at all: small, fully controllable, and audibly not a person *(Ch. 9)*

**Forward algorithm** — the algorithm that scores how well an HMM explains a sequence of frames by summing over all the ways the frames could have been aligned to states *(Ch. 4)*

**Foundation model**

- *(Ch. 1)* a model pretrained at large scale on unlabeled or weakly labeled audio, whose representations then transfer to many tasks with little labeled data; heavy on compute, and uneven in its language and dialect coverage
- *(Ch. 6)* a large pretrained speech model that already knows speech in general and is then adapted to a particular job, rather than built from scratch for it; this chapter compares self-supervised, weakly supervised, massively multilingual, and Arabic-centric examples

**Frame** — a short slice of the signal, about 25 milliseconds by long-standing default, brief enough that the sound is roughly steady within it; at 16 kHz that is 400 samples *(Ch. 3)*

**Front end**

- *(Ch. 3)* the processing that turns a recording into the features a model consumes, steps 5 to 8 of Figure 3.1: preprocess, extract features, normalize, and augment
- *(Ch. 9)* the half of a text-to-speech system that turns written text into a pronounceable form: normalization, diacritization and grapheme-to-phoneme conversion

**Frozen** — left unchanged while something else is trained *(Ch. 11)*

**Frozen encoder** — a pretrained network whose weights are held fixed during training, so it keeps what it already learned while only the unfrozen parts adapt. A frozen-encoder probe and a fully fine-tuned model measure different things, so a reported number is interpretable only when the setup is given *(Ch. 6)*

**Full-duplex** — listening and speaking at the same time rather than in turns *(Ch. 11)*

**Fusion weight** — the dial that sets how much the external language-model score counts during decoding. Too little under-uses the text knowledge; too much lets the language model override the audio and ‘hallucinate’ fluent but wrong transcripts. The best value is found on a development set, and like every decoding choice it must be reported *(Ch. 5)*


## G

**Gaussian mixture** — a flexible blend of bell curves used as the emission distribution of an HMM state, able to fit the spread of real acoustic features and so to capture the many ways a phone can be realized by different speakers and contexts *(Ch. 4)*

**Gaussian mixture model** — the component of the statistical era that describes the distribution of acoustic features in each hidden state *(Ch. 1)*

**Gemination** — the doubling of a consonant, contrastive in Arabic and written with the Shadda. Its primary acoustic correlate is a longer hold of the consonant, so a model that represents sounds only by their short-time spectrum can miss the contrast entirely *(Ch. 2)*

**Goodness of Pronunciation** — the classic scoring measure: for each aligned phone the acoustic model estimates how consistent the audio is with the intended phone, and the low scores are flagged. It is interpretable and needs no examples of errors, and it detects without diagnosing, saying that the sound was wrong but not which sound was made instead. Because the scores depend on the model, the phone, the speaker population and the recording condition, thresholds should be calibrated on held-out learner data with expert labels rather than fixed once, which is why it is best treated as a screening score *(Ch. 12)*

**Grapheme-to-phoneme conversion** — turning written letters into the sounds they stand for; for Arabic, largely rule-governed once the diacritics are present *(Ch. 9)*

**Grapheme-to-Phoneme converter** — the component that turns written Arabic into a sequence of phones, so it has to encode the Shadda and the sun-letter behavior of the definite article, everything correct pronunciation needs that the letters do not show *(Ch. 2)*


## H

**Hamza** — the glottal-stop sign, written on different seats depending on context, so one sound appears in several shapes; one of the special letters whose inconsistent use makes text normalization a choice with downstream consequences *(Ch. 2)*

**Hidden Markov model** — the model that represents an utterance as a sequence of hidden states that emit observable sounds; combined with a Gaussian mixture model, a language model, and a pronunciation dictionary, it dominated recognition from the late 1980s into the 2000s *(Ch. 1)*

**Hidden Markov Model** — a small chain of hidden states, read left to right, where each state can repeat before the model advances. The repetition, drawn as a self-loop, is how the model absorbs duration, which is what lets it score frame sequences of unpredictable length *(Ch. 4)*

**Hop** — the step from the start of one frame to the start of the next, 10 milliseconds by default, giving roughly 100 frames per second; at 16 kHz that is 160 samples *(Ch. 3)*

**Hybrid CTC/attention** — one shared encoder feeding two heads, a CTC head and an attention decoder, with training minimizing a weighted sum of the two losses and decoding combining the two scores. The monotonic CTC head keeps the attention from wandering early in training and speeds convergence, while the attention head supplies global context and the strong output language model *(Ch. 5)*


## I

**Idgham** — the Tajwīd rule family of assimilation, written إدغام and heard as two adjacent consonants merging, measurable as the absence of the separate articulation of the first consonant, read from the boundary and energy pattern that a non-merged production would show *(Ch. 12)*

**Imāla** — the raising of long /aː/ toward /eː/ in several varieties, one of the ways the dialects reshape the vowel space that Modern Standard Arabic defines *(Ch. 2)*

**Informed consent** — a record taken before anything else is done, stating the recording, the permitted uses including model training and any redistribution, the retention period, and the right to withdraw, worded to match the law the collection sits under *(Ch. 7)*

**Instruction tuning** — training on examples that pair an input with a natural-language instruction and the target answer, so that the task is chosen when the model is used rather than when it is built *(Ch. 11)*

**Intent accuracy** — the proportion of utterances whose predicted intent label is the reference label, the friendliest of the three understanding scores, since a system can score well on it while filling every slot wrongly1 *(Ch. 10)*

**Intent detection** — classifying what the speaker wants from an utterance, one label per utterance, as a request to book a flight yields the intent book_flight; scored with intent accuracy1 *(Ch. 10)*

**Inter-annotator agreement**

- *(Ch. 7)* how often several annotators labeling the same sample independently agree beyond chance, and the quality check that matters most before a release. State how many annotators labeled how large a sample, which measure was used, the value obtained, and how disagreements were resolved
- *(Ch. 12)* the agreement between two or more qualified raters labeling the same material, computed for example with Cohen’s kappa. It establishes the human ceiling a system should be scored against, rather than scoring it against a single annotator
- *(Ch. 14)* the measured agreement between two annotators transcribing the same sample independently, computed rather than assumed. Disagreements are adjudicated and folded back into the guideline, which is the loop that makes the corpus consistent

**Intonation** — the melody of the pitch across an utterance; in Arabic a statement broadly falls at the end and a yes-or-no question rises (Section 2.10) *(Ch. 9)*

**Iʿrāb** — the case endings on nouns and adjectives and the mood endings on imperfect verbs, almost never written in ordinary text, the second and harder layer of the ambiguity that diacritization has to resolve *(Ch. 2)*


## J

**Joint goal accuracy** — the proportion of turns whose predicted state is right in full, every slot and every value matching the reference state. It is the strictest of the three understanding scores and the one that predicts whether an assistant works, because a single wrong value costs the whole turn1 *(Ch. 10)*

**Joint network** — the part of the RNN-Transducer that combines the encoder’s view of the current frame with the prediction network’s view of the tokens emitted so far and outputs a distribution over the next token or blank *(Ch. 5)*


## K

**Keyword spotting** — watching audio for a small, fixed vocabulary, such as a wake word or a set of voice commands, light enough to run continuously on a device and reported with precision, recall and false-alarm rate *(Ch. 8)*

**Kneser-Ney smoothing** — the standard smoothing method for n-gram models, which backs off on the continuation count, the number of distinct contexts a word follows, rather than on raw frequency; a word that has followed many different words is the safer fallback in a context never seen before *(Ch. 4)*


## L

**Language model** — the component that supplies the second half of the score, the plausibility of a word sequence, and so breaks ties the audio cannot; classically an n-gram model estimated by counting word sequences in a large text corpus *(Ch. 4)*

**Language-model judge** — a strong language model used to score another model’s open-ended answers against a reference; it inherits its own blind spots *(Ch. 11)*

**Leaderboard** — a standing comparison of models on shared test sets, such as the Open Universal Arabic ASR Leaderboard, which makes cross-model comparison fair. Used carelessly it invites overfitting to one test set and rewards a single pooled number that hides dialect variance, so read it as one comparable signal beside your own per-dialect results *(Ch. 7)*

**Leak-free split**

- *(Ch. 3)* training, development, and test sets built so that no speaker appears in more than one of them, and, for read or command speech, so that prompts and recording sessions do not overlap either. Without the rule a model can score well by recognizing familiar voices rather than speech
- *(Ch. 14)* a division into training, development and test sets in which no speaker appears in more than one part, and for read or command speech no prompt or recording session does either. Without it a model is rewarded for recognizing familiar voices and rooms, and the reported number collapses on real users

**Leakage** — overlap between training and evaluation data that lets a system score well for the wrong reason. In speech the speaker is the leak that matters most, because a voice carries so much identity that a model can recognize the speaker instead of the words; a result computed on a leaking split is a measurement of the wrong thing *(Ch. 7)*

**Learned front end** — first layers of a neural network that operate on the raw waveform and discover their own filters instead of computing a fixed pipeline of hand-designed features; the front end of the self-supervised models of Chapter 6 *(Ch. 3)*

**Legitimate variation** — an accent, a dialect or a speech difference that is not a mistake, and the thing a system must not mark as one. Distinguishing it from a genuine error is an accuracy question and an ethical one at once, and for a learner the rate at which correct dialectal or accentual production is flagged, rather than the headline accuracy, is the failure mode that most discourages *(Ch. 12)*

**Length or insertion penalty** — the decoding parameter that biases the search toward longer or shorter output; set too high it buys extra insertions, set too low it buys deletions *(Ch. 5)*

**Log-mel filterbank features** — the logarithm of the mel filterbank band energies, a compact, perceptually grounded summary of the spectrum and a widely used input to many neural ASR and TTS systems. At 16 kHz a 25-millisecond frame of 400 samples becomes about 40 log-mel values, and one second of audio about 100 such vectors instead of 16,000 raw samples *(Ch. 3)*

**Long Short-Term Memory network** — a recurrent network with gates that decide what to keep, forget, and output, so that useful information survives across long spans; the Gated Recurrent Unit is a lighter variant with fewer gates and similar behavior, and both must still be computed frame by frame *(Ch. 4)*

**Looping and deletion** — the characteristic failure modes of attention models, where the decoder repeats a word or skips ahead and drops one, especially on long utterances or noisy audio where the soft alignment loses its way. In an attention heatmap they appear as a broken or scattered band in place of the healthy roughly diagonal one *(Ch. 5)*

**Low-rank adaptation** — freezing the pretrained weights and learning a small, low-rank update to them, two thin matrices whose product is added to a weight matrix, often training well under one percent of the parameters and fitting in modest memory *(Ch. 6)*


## M

**Machine-assisted transcription** — a first pass in which a recognizer proposes text that a human corrects. It reduces the transcription effort substantially when the recognizer is good enough for the variety in question, and not at all when it is not, which for many Arabic dialects is still the case *(Ch. 7)*

**Macro-averaged F1** — the unweighted mean of the per-class F1 scores, so that every dialect counts for exactly as much as every other however many test utterances it has. The chapter asks for it beside accuracy because dialect classes are imbalanced: on the worked matrix of Figure 8.8 a system correct on 85 percent of utterances scores 0.71 *(Ch. 8)*

**Madd** — the Tajwīd rule family of elongation, written مدّ and measurable as vowel duration: the system reads the duration of the long vowel off the alignment and compares it with the length expected for that madd type, flagging a violation when it is too short *(Ch. 12)*

**Masked prediction** — a pretext task that hides spans of audio and asks the model to predict a discrete label for the hidden frames, as HuBERT does, where the labels come from clustering speech features and are refined from the improved model over successive iterations *(Ch. 6)*

**Masking** — the standard method for cleaning noisy audio: move the recording to a time-frequency view, have a network predict for every cell how much of it is speech, a value between 0 and 1, multiply, and transform back. The two targets it is trained against are the ideal binary mask, which keeps a cell only where speech dominates, and the ideal ratio mask, which keeps a graded share *(Ch. 8)*

**Mel filterbank** — a set of triangular filters, typically about forty, spaced evenly on the perceptual mel scale, which re-spaces frequency to match human hearing, finely at low frequencies and coarsely at high ones. The filterbank groups the many frequency bins of a spectrogram into that smaller set of bands by summing the energy in each; implementations differ, for example the HTK and Slaney conventions, so the convention should be reported *(Ch. 3)*

**Mel spectrogram** — a compact picture of which frequencies carry energy at each moment, on a scale spaced the way human hearing is; the usual hand-off between an acoustic model and a vocoder *(Ch. 9)*

**Mel-Frequency Cepstral Coefficients** — the log-mel energies compressed further by a discrete cosine transform, of which only the low-order coefficients are kept, commonly about twelve or thirteen, sometimes with the zeroth coefficient or a log-energy term, and often with the delta and delta-delta coefficients appended to capture dynamics. That decorrelation matched them to the Gaussian-mixture models of classical recognition (Chapter 4), so they are best understood today as a compact classic baseline and a bridge to classical ASR rather than the center of modern systems *(Ch. 3)*

**Minimal pair** — two words that differ in exactly one sound, which is the experiment a pronunciation assessor is really running, since a system that scores the pair correctly has scored the contrast rather than the word. L2AraSpeech is built around 61 of them for that reason *(Ch. 12)*

**Mispronunciation detection and diagnosis** — the neural successor to Goodness of Pronunciation, trained on annotated learner errors so that it both detects a mispronunciation and diagnoses it, naming the wrong sound that was produced. The extra capability is paid for in data, since it needs annotated learner errors and Goodness of Pronunciation needs none *(Ch. 12)*

**Model card** — a short document stating a system’s intended use, its training data and its measured per-group performance, so that users and regulators can judge whether it is fit for a purpose. A blank per-group line usually means the breakdown was never computed *(Ch. 13)*

**Modern Standard Arabic** — the form of Arabic historically rooted in Classical Arabic and used for news, formal writing, and education, but rarely acquired as a home vernacular; the condition most Arabic training data represents, and the reason a broadcast-trained recognizer can fail badly on spontaneous dialect *(Ch. 1)*

**Monotonic alignment** — an alignment that only ever moves forward through the audio, so the model either emits a token or advances one frame and never moves backward in time. CTC and the RNN-Transducer have it by construction, and it is the property that makes low-latency streaming possible *(Ch. 5)*

**Multitask decoding** — the arrangement in Whisper by which special tokens in the decoder tell one network whether to transcribe, translate to English, identify the language, or emit timestamps, so a single model covers several jobs *(Ch. 6)*

**Multitask prompting** — asking one model to do many different tasks by changing the instruction and nothing else *(Ch. 11)*


## N

**N-gram model** — a language model giving the probability of the next word from the previous one or two, estimated by counting word sequences in a text corpus; it needs smoothing, because no corpus contains every valid sequence *(Ch. 4)*

**Neural audio codec** — a model that compresses a waveform into a short sequence of discrete units and reconstructs the sound from them *(Ch. 11)*

**Nyquist limit** — half the sampling rate, the cap on what that rate can represent: to keep frequencies up to some value, sample more than twice that fast *(Ch. 3)*


## O

**Offline translation** — translation that waits for the whole utterance before producing output, the setting in which quality is measured with no latency budget and the foil against which simultaneous translation is defined1 *(Ch. 10)*

**Omni model** — a model that takes speech, text, images and video and can respond in more than one of them *(Ch. 11)*

**On-device recognition** — running recognition on the user’s own phone so the audio never moves, the strongest privacy protection available because it removes the risk rather than managing it. The cost is a smaller model *(Ch. 13)*

**Ontology** — the fixed inventory of intents and slot values a prediction is matched against, held in an ontology or a database. A value leaves the turn in Arabic and enters the state in the form the ontology holds, so everything in between, one orthography for names and one romanization, one numeral system, and a rule about diacritics, is a decision that silently moves slot F1 and joint goal accuracy1 *(Ch. 10)*

**Out-Of-Vocabulary rate** — the share of word forms a system meets that it never saw in training. Templatic morphology drove it high in older word-based Arabic systems, and the sparsity that remains in neural systems is what motivates the subword tokenization discussed in Chapter 4 *(Ch. 1)*

**Output unit** — the token an end-to-end model is trained to emit, a first-class decision for Arabic because it interacts with diacritization and dialect. Characters, subwords, morphemes, and words trade sequence length against vocabulary size, against the need for a tokenizer or a morphological analyzer, and against robustness to unstandardized dialect spelling *(Ch. 5)*


## P

**Parameter-efficient adaptation** — the family of methods, adapters and low-rank adaptation among them, that leave the backbone frozen and train only a small number of new weights, so adaptation needs less labeled data, memory, and time, and one shared backbone serves many dialects *(Ch. 6)*

**Per-dialect evaluation** — reporting error rates separately for each variety, on data that includes spontaneous dialectal speech and not only read benchmarks, because a single pooled Word Error Rate dominated by Modern Standard Arabic can look strong while hiding poor performance on a Gulf or Maghrebi variety *(Ch. 6)*

**Per-group evaluation** — reporting results broken down by population rather than as one figure, so that a system is not declared good while failing the users who need it most. For disordered and child speech the results must come from the target population and never be extrapolated from typical adult speech *(Ch. 12)*

**Personal data** — in Saudi Arabia’s Personal Data Protection Law, any data that would identify a person directly or indirectly, with biometric data listed among the categories treated as sensitive. The law does not name the voice, and it does not have to, since a voice is biometric because it identifies a person *(Ch. 13)*

**Personalization** — adapting a strong recognizer to one speaker with a small amount of that speaker’s own audio, the practical remedy where disordered speech is too scarce to train on. The evidence is a decade deep and carries its own caution: the gains are largest on read phrases and shrink on conversational speech, which is what a person actually needs a recognizer for *(Ch. 12)*

**Phonemic** — carrying meaning: a difference that on its own can change one word into another. Vowel length and gemination are phonemic in Arabic, so a system has to capture them rather than smooth them away *(Ch. 2)*

**Phonotactic modeling** — the first successful approach to spoken dialect identification: run a phone recognizer over the audio, model the statistics of the resulting phone sequences separately for each dialect, and classify a new utterance by which dialect’s phonotactics best explain its phone sequence. It is interpretable and works with modest data, and it is capped by the quality of the phone recognizer *(Ch. 8)*

**Phonotactics** — the restrictions a language places on which sound sequences are allowed, for example that Modern Standard Arabic does not begin a syllable with two consonants. The sequence of sounds alone carries enough information to identify a speaker’s dialect from audio *(Ch. 2)*

**Pre-emphasis** — a simple high-pass step, typically a first-order filter with a coefficient near 0.97, that boosts the high frequencies. It was standard in classical MFCC pipelines and is optional in modern neural front ends *(Ch. 3)*

**Prediction network** — the part of the RNN-Transducer that runs over the tokens emitted so far, in effect a small language model inside the recognizer; it is what removes CTC’s independence assumption while keeping the model left to right *(Ch. 5)*

**Predictive objective** — the third family of pretext task, where the model uses the visible context to predict a hidden or future representation of its own. Predicting several steps ahead, rather than the very next frame, pushes the objective to capture slower-moving phonetic and linguistic structure instead of only local acoustic detail *(Ch. 6)*

**Pretext task** — the invented task solved during pretraining: hide part of the input and train the model to fill in or recognize the missing part, so the data itself is the answer key and no human labels are needed *(Ch. 6)*

**Probing** — the way to ask what a representation actually encodes, introduced in Section 6.5: freeze the pretrained encoder, attach a small classifier to one layer, and train only that classifier to predict a property such as the phone, the speaker, or the dialect. If a light probe can read the property off a layer, the property is encoded there, and doing this layer by layer shows where each kind of information lives *(Ch. 6)*

**Processing artifact** — what an enhancer leaves behind in place of the noise it removed. A recognizer trained on unprocessed audio has never heard these artifacts, so they cost it more than the noise they replaced, which is why a denoising front end raised the Word Error Rate on Saudi broadcast speech instead of lowering it *(Ch. 8)*

**Project specification** — the written statement, fixed before any modeling, of the task, the user and setting, the primary and secondary metrics, and the success criterion. It also decides the shape of the data, since every collection choice should follow from one of its four items rather than from convenience *(Ch. 14)*

**Projector** — the width half of the connector: a feed-forward map from the encoder’s dimension into the language model’s embedding dimension, often a single layer *(Ch. 11)*

**Pronunciation lexicon**

- *(Ch. 2)* the table that maps each word to its sequence of phones, which both classical recognizers (Chapter 4) and synthesizers (Chapter 9) depend on
- *(Ch. 4)* the dictionary that maps each word to its phone sequence, so the acoustic model’s phone scores can be assembled into word scores. For Arabic it is unusually hard to build, because pronunciation depends on the short vowels ordinary text omits, and it must also list dialectal variants

**Prosody**

- *(Ch. 2)* the stress, rhythm, intonation, tempo, and loudness that ride on top of the words. Arabic stress is largely predictable from the shape of the syllables, while intonation varies more across dialects and remains an active research topic
- *(Ch. 9)* the rhythm, stress, pitch melody and loudness that ride on top of the words and carry meaning and emotion

**Provenance** — where evaluation audio and labels came from, and whether they were recorded from speakers or generated by a system *(Ch. 11)*

**Pseudo-label** — a first model’s best-guess transcript for unlabeled audio, used as though it were a real label when the system retrains on labeled and unlabeled data together *(Ch. 6)*


## Q

**Quantization**

- *(Ch. 3)* rounding each sampled measurement to one of a fixed set of levels, which adds a small, constant error heard as a faint hiss and which at 16 bits usually sits below microphone and room noise when the recording level is set properly
- *(Ch. 6)* replacing the continuous latents with entries from a learned, finite codebook of speech units, so the target is a discrete inventory; the ingredient that sharpens the contrastive choice in wav2vec 2.0


## R

**Ranked search** — this chapter’s view of recognition: the system considers many possible transcripts, gives each an acoustic score and a language score, and returns the candidate with the best combination *(Ch. 4)*

**Read speech** — speech produced from a written prompt, as in Common Voice and the learner collections. It is the wrong material for a dialect recognizer, which needs spontaneous speech from many speakers, and its splits must divide the prompts as well as the speakers, or a model can score well by having memorized the sentence *(Ch. 7)*

**Real-time factor** — the hours of human effort needed for one hour of audio, the unit in which annotation is budgeted. Multiply the audio by the factor for each pass and add them up, then add the passes a first plan forgets: the sample a second annotator labels independently so that agreement can be measured, and the adjudication of the cases where the two disagree *(Ch. 7)*

**Recipe** — a condensed route through the project lifecycle for a project type that recurs: a goal, the ingredients, the steps in order, the pitfalls that most often sink it, and a checklist. A recipe changes the ingredients and the failure modes, never the lifecycle, so every recipe still begins with a specification and ends with a reproducibility record *(Ch. 14)*

**Recurrent Neural Network** — a network that carries a hidden state forward from frame to frame, giving it a memory of everything read so far. In practice the signal connecting two distant frames fades during training, so long-range dependencies are hard to learn *(Ch. 4)*

**Reference translation** — the translation a score is computed against, and something dialect changes rather than leaves alone. There is no single correct English for a Tunisian sentence and no single correct dialectal Arabic for an English one, so references must respect dialect and code-switching, and a benchmark built on Modern Standard Arabic will not tell you how a system does on either1 *(Ch. 10)*

**Replay attack** — playing a recording of the target’s voice at a verification system, the cheapest spoof there is, answered by liveness and replay detection rather than by better speaker modelling *(Ch. 13)*

**Reproducibility record** — the living file in the repository that ties any reported number to an exact corpus version, split, configuration, augmentation policy, random seed and scoring script. A result that cannot be reproduced from the repository is not yet a result, and the record is kept as the work happens rather than reconstructed at writing time *(Ch. 14)*

**Rescoring** — the lightest-weight way to use an external language model: the end-to-end model proposes an n-best list or a lattice and the language model re-ranks it afterward *(Ch. 5)*

**Retrieval-augmented generation** — fetching relevant documents when the question is asked and conditioning the answer on them, so that the answer can be traced to a source *(Ch. 11)*

**RNN-Transducer** — the streaming family: an acoustic encoder, a prediction network over the output history, and a joint network that emits the next token or a blank. It keeps a monotonic alignment and an internal language model, at the cost of a heavier training computation and more careful engineering *(Ch. 5)*

**Root-and-pattern morphology** — the templatic axis of Arabic word formation: a root of usually three consonants is interleaved with a pattern of vowels to give a stem, so k-t-b yields kataba ‘he wrote’, kitāb ‘book’, and kātib ‘writer’. The shared root is not a contiguous piece of the written word, which is why subword methods capture it less readily than they capture clitics *(Ch. 2)*

**Routing front end** — the deployed use of a dialect identifier: it labels the variety and the system selects a dialect-specific recognizer. It needs a confidence threshold and a fallback to a robust multidialect or MSA model, because a confident wrong route is worse than a deliberately generic one, and the routing decisions should be logged so that the dialect mix in production can be audited against the taxonomy that was reported *(Ch. 8)*


## S

**Safe failure** — the requirement that a clinical or telehealth system defer to a person when its confidence is low rather than guess a clinical value. The gate that decides this, and the conditions the system runs under, are as much the system as the pipeline is: a low-confidence answer goes to a human rather than into the record, and no autonomous action is taken on a high-risk medication or symptom value *(Ch. 12)*

**Sampling rate**

- *(Ch. 3)* the number of measurements taken per second, written in hertz; 16 kHz is a common default for recognition, telephone speech is usually 8 kHz, and synthesis often uses higher rates for a fuller voice
- *(Ch. 9)* how many amplitude measurements a second the waveform is stored as; 22,050 Hz is a common choice for synthesis

**Scoring normalization** — the text normalization of Chapter 4 applied before a number is computed, and the decision this chapter asks to be recorded with every number. Settle it before annotating, apply the same one to the reference and to the prediction, and state it with the score, because a slot F1 computed under a permissive normalization and one computed under a strict one are not comparable and nothing on the page will say so1 *(Ch. 10)*

**Segment length** — the duration of the clip an identifier is given, and the most durable finding in spoken ADI: accuracy climbs with it, because a few seconds rarely contain enough dialect-bearing cues while twenty seconds usually do. Two published accuracies measured on different duration splits have not really been compared *(Ch. 8)*

**Segmentation** — cutting a recording into short utterances before transcription, with every boundary falling in a silence or pause rather than inside a word and every clip short enough to transcribe and align. It is done by hand on the waveform and spectrogram, by voice activity detection, or by forced alignment *(Ch. 7)*

**Self-supervised learning** — the two-stage recipe of this chapter: pretrain on unlabeled audio with a pretext task that needs no transcripts, then fine-tune on a small labeled set. It is valuable for Arabic because unlabeled audio is plentiful while transcripts, dialectal ones above all, are scarce *(Ch. 6)*

**Semi-supervised learning** — mixing a little labeled data with a large pool of unlabeled audio: a first model trained on the labels produces pseudo-labels for the unlabeled audio and the system retrains on both, a loop known as self-training *(Ch. 6)*

**Senone** — a shared HMM state, produced by clustering acoustically similar context-dependent states so that the number of states stays manageable; it is the unit a hybrid network is trained to score *(Ch. 4)*

**Shadda** — the diacritic that doubles, or geminates, the consonant it sits on. If transcripts drop it, singletons and geminates are merged at the labeling stage, no matter how strong the model that reads them *(Ch. 2)*

**Shallow fusion** — the most common way to bring in an external language model, adding a weighted language-model score to the recognizer’s own score for each candidate during beam search, so the two votes combine at every step *(Ch. 5)*

**Shared task** — an organized competition on a benchmark, which gives a community common data, common metrics, and a reason to publish reproducible results; for Arabic the Multi-Genre Broadcast challenges and the Nuanced Arabic Dialect Identification campaigns play this role *(Ch. 1)*

**Short-time analysis** — the standard move of cutting the signal into short overlapping frames, multiplying each by a window, and analyzing the frequencies in each one. Stacking the per-frame spectra gives the short-time Fourier transform, the workhorse representation of the chapter *(Ch. 3)*

**Sign language recognition** — mapping video of hand shape, movement and facial expression to words, sharing its machinery with lipreading but reading the whole upper body rather than the mouth. Arab sign languages are natural languages with their own lexicons and grammars rather than visual encodings of spoken Arabic, and they differ across countries, so a model has to be evaluated on the variety it serves exactly as a recognizer is evaluated per dialect *(Ch. 12)*

**Simultaneous translation** — translation that must begin producing output while the speaker is still talking, as a human interpreter does. Its core tension is quality against delay: waiting for more input gives better translations but makes the listener wait. For Arabic the speaker is the harder half, since a simultaneous system commits to words before dialectal and code-switched uncertainty has resolved, in exactly the live settings where the stakes are highest1 *(Ch. 10)*

**Slot F1** — the harmonic mean of precision and recall over the predicted slots, a slot counting as correct only when its type and its value both match the reference. It hides the question that decides it, which is when two strings count as the same, so the normalization that produced it has to be stated with the score1 *(Ch. 10)*

**Slot filling** — extracting the arguments that complete an intent, the destination and the date of a flight, from the utterance. In Arabic it is a normalization problem as much as a tagging problem, because a slot counts as filled only when its value matches an entry in an ontology or a database, and the same value can be written several ways without any of them being wrong1 *(Ch. 10)*

**Soft alignment** — the alignment an attention decoder learns, a distribution of weights over all frames rather than a hard path, which lets each output token look wherever it wants across the utterance and buys global context at the cost of being able to wander *(Ch. 5)*

**Source-filter model**

- *(Ch. 2)* the picture of speech production the chapter works from: a source, the buzz of the vocal folds at rate F0 or the noise made by a constriction, is shaped by a filter, the vocal tract, whose resonances are the formants
- *(Ch. 9)* the account of speech as a source, the buzz of the vocal folds or a noise, shaped by a filter, the vocal tract; introduced in Chapter 2

**Speaker anonymization** — altering a recording so that the speaker cannot be recognized while the words and much of the prosody survive, the working answer where a release cannot carry identifiable voices; the VoicePrivacy initiative defines the shared task and the metrics that make such systems comparable *(Ch. 7)*

**Speaker diarization**

- *(Ch. 1)* the task of partitioning a recording into speaker turns, answering neither what was said nor who said it but who spoke when, which is what makes a multi-speaker meeting or a broadcast panel tractable (Section 8.6)
- *(Ch. 8)* deciding who spoke when, partitioning a recording into the stretches belonging to each talker, usually without knowing in advance who they are or even how many. The standard pipeline removes the silence, cuts the speech into short segments, turns each segment into a speaker embedding and clusters the embeddings; its weakness is a segment holding two voices at once, which end-to-end neural diarization avoids by predicting which speakers are active at every moment

**Speaker embedding** — a fixed-length vector meant to carry the voice rather than the words, produced by pooling a neural encoder’s frame outputs, with ECAPA-TDNN the current default architecture. It is the common currency of the three speaker tasks, so a better embedding improves identification, verification and diarization at once *(Ch. 8)*

**Speaker identification** — deciding which of several enrolled people is talking, a one-of-N choice against a closed gallery, which is what a system does when it labels the participants in a recorded meeting; reported with identification accuracy *(Ch. 8)*

**Speaker profiling**

- *(Ch. 1)* also called speaker attribute classification: the prediction of trait labels as recorded in a dataset, such as gender, emotion, or regional dialect, without identifying the individual. Because such labels touch identity, Chapter 13 treats their ethical limits as part of the engineering
- *(Ch. 8)* estimating traits such as gender, age group and emotion from the same embeddings that identify a dialect. These are socially sensitive inferred attributes, so it should be used only with appropriate consent and a clear purpose, and the report should state the consent conditions, the label definitions, inter-annotator agreement, and performance broken down by subgroup

**Speaker verification**

- *(Ch. 1)* the biometric decision whether a voice matches a claimed identity, scored by Equal Error Rate; not to be confused with speaker profiling, which predicts traits and names nobody
- *(Ch. 8)* deciding whether a recording came from one particular claimed person, a yes or no reached by comparing one utterance with one enrolled reference and putting a threshold on the score, which is what a bank does when a customer authorises a transfer by voice; reported with the Equal Error Rate

**Speaker-disjoint split** — a division of the data in which no speaker appears in more than one set, so that a model cannot profit at test time from a voice it heard in training. Where the data allows, the split is made disjoint by prompt, session, and recording condition too, and never made at random over clips cut from long recordings *(Ch. 7)*

**SpecAugment**

- *(Ch. 3)* a training-time augmentation that masks random bands of frequency and random spans of time in the log-mel features, and optionally warps them in time, which makes a model more robust and regularizes it against overfitting. Use it on the training set only, since applying it at test time makes results non-comparable, and report the mask policy
- *(Ch. 14)* the training-time augmentation that masks bands of frequency and spans of time in the input features. It is applied to the training set only, because augmenting the test set changes what the number means

**Spectral leakage** — the smearing of energy across the spectrum caused by the artificial jumps at the ends of a slice chopped abruptly out of the signal, which a window is applied to soften *(Ch. 3)*

**Spectrogram** — a picture of the short-time analysis, with time along the horizontal axis, frequency up the vertical axis, and the energy at each point shown by darkness or color, usually on a decibel scale so quiet detail is visible *(Ch. 3)*

**Speech agent** — the loop of perceive, plan, act and respond, run over a spoken turn *(Ch. 11)*

**Speech command recognition** — the classification of an utterance into one of a small, fixed set of commands, a narrower task than spoken language understanding and one the chapter warns against confusing with it *(Ch. 1)*

**Speech emotion recognition** — predicting an apparent affective state from speech with the now-familiar recipe of a pretrained encoder, pooling, and a small classifier, drawing on Arabic emotional-speech corpora. The overlap that makes neighboring dialects hard to separate also blurs emotion categories, so these labels are subjective and evaluations must report inter-annotator agreement, not only accuracy *(Ch. 8)*

**Speech synthesis markup** — tags carried along with the text that tell a synthesizer how to read a name, a number or a pause; SSML is the W3C Recommendation *(Ch. 9)*

**Speech-language model** — the wider family named in Section 11.1: a language model that takes speech as its input. Every audio-language model is one, and the longer name is used where the family rather than this chapter’s architecture is meant *(Ch. 11)*

**Speech-to-speech** — speech in and speech out, with no written transcript in the middle *(Ch. 11)*

**Spoken dialogue loop** — the cycle a voice assistant closes: speech is recognized and understood, a dialogue manager updates the state and decides what to do, a response is generated, and the synthesis of Chapter 9 speaks it back, after which the loop waits for the next turn. A system answering in Arabic has to decide the diacritization of its own reply before it can pronounce it, so the whole of Section 9.2 sits inside this loop rather than beside it, and any displayed transcript or caption has to render right to left with mixed Arabic and Latin content1 *(Ch. 10)*

**Spoken document retrieval** — searching a large audio collection, such as the decades of broadcast material in Arabic media archives, in two phases that run on different schedules: an indexing phase transcribes or phonetically indexes the archive once, and a querying phase searches that index and ranks the matching documents, which is what makes queries fast. The central design choice is the index unit, because a word-level index cannot match a term the recognizer never produced, while a subword or phonetic index trades precision for the ability to match out-of-vocabulary names and dialectal words *(Ch. 8)*

**Spoken language understanding**

- *(Ch. 1)* the extraction of meaning from spontaneous speech rather than a transcript alone, producing an intent and the parameter values, or slots, that go with it
- *(Ch. 10)* turning speech into structured meaning a machine can act on, resting on three tasks: intent detection, slot filling and dialogue state tracking. It has the same architectural fork as translation, cascade or end-to-end, and the same Arabic difficulty, because users speak to assistants in dialect even when they would write in Modern Standard Arabic1

**Spoken term detection** — the open-vocabulary cousin of keyword spotting: given an arbitrary query term, find every place it occurs in a body of audio, with timestamps. Arabic morphology and unsettled dialectal spelling push it toward indexing smaller units, subwords or phones, and toward expanding every query into its likely forms and spellings *(Ch. 8)*

**Spontaneous speech** — unscripted speech as it is actually produced, in conversation, broadcast, or telephone calls, and what a dialect recognizer needs. Ten hours of it, matched to the target dialect and channel, can be worth more than a thousand hours of MSA broadcast *(Ch. 7)*

**Statistical parametric synthesis** — speech generated by a model that predicts acoustic parameters for a vocoder to render, rather than by joining recordings *(Ch. 9)*

**Streaming** — emitting output while the speaker is still talking, with bounded delay, as a live captioner or a voice assistant needs. The RNN-Transducer is designed for it, CTC supports it when paired with a streaming causal encoder, and pure attention does not, since each token may attend to the end of the utterance *(Ch. 5)*

**Style-shift error** — an error in which the model heard the speech but rendered a dialectal word as its formal Modern Standard Arabic equivalent, semantically close yet wrong under strict scoring. It inflates the error against a dialectal reference and calls for dialect-aware fine-tuning rather than more audio, which is why errors should be separated from acoustic and orthographic ones instead of merged into one rate *(Ch. 6)*

**Subword tokenization** — using a learned inventory of word pieces instead of whole words, so a rare word is spelled from common pieces and nothing is ever out of vocabulary. It is the usual practical choice for Arabic, with the vocabulary size reported as part of the recipe *(Ch. 4)*

**Subword units** — word pieces learned from text with byte-pair encoding or SentencePiece, the common default output unit for Arabic. They balance sequence length against vocabulary size and avoid the out-of-vocabulary problem, which is what makes them safe for dialects that have no standardized orthography *(Ch. 5)*

**Sun letters and moon letters** — the two sets of consonants that decide how the definite article al- is said: before the fourteen sun letters the l assimilates and the following consonant geminates, while before the moon letters the article is pronounced as written. Spelling hides the difference, so a Grapheme-to-Phoneme converter and a synthesizer must both know the sun-letter set *(Ch. 2)*


## T

**Tajwīd**

- *(Ch. 2)* the rules governing recitation of the Qur’an, which fix elongation, assimilation, concealment, clear pronunciation, nasalization, and echo in unusually explicit terms rather than leaving them to the speaker, which makes recitation an unusually well specified target for automatic pronunciation assessment (Chapter 13)
- *(Ch. 12)* the precise system of rules for Quranic recitation, written تجويد and covering articulation, elongation, assimilation and pausing, under which a deviation is an error against an exacting standard rather than a stylistic choice. Its explicitness is an advantage for assessment, because correctness can be defined and measured more sharply than for ordinary speech, and every rule family that belongs in a builder’s taxonomy must end in something the audio can be measured for. Its standing is also why an assessor requires independent expert religious and phonetic validation before educational or religious deployment

**Tashkīl** — the optional diacritics placed above and below the consonants to write the short vowels and a few other marks. In the overwhelming majority of real text they are absent and the reader restores them from context, which is the source of the ambiguity of Section 2.7 *(Ch. 2)*

**Telehealth assistant** — the speech agent of Section 11.5 with the stakes raised: the same loop of perceiving, planning, acting and responding, and the same discipline of retrieving rather than answering from memory and showing where the answer came from. What changes is the cost of a wrong step, which is why the fallback to a person is a design requirement here rather than a refinement *(Ch. 12)*

**Templatic morphology** — the Arabic word-building system in which a root, usually three consonants, is slotted into patterns; with prefixes, suffixes, and attached pronouns and articles, a single root can surface as hundreds of distinct written forms, many of them rare or unseen in training *(Ch. 1)*

**Test set** — the split that is decoded once, at the end. It should be large enough per variety to report a per-dialect result rather than one pooled number, and for a large corpus it is fixed at an absolute size, a few hours, rather than at a percentage *(Ch. 7)*

**Text normalization**

- *(Ch. 1)* the processing applied to text before a score is computed, for example removing or keeping diacritics, unifying the various forms of Alef and Ta-marbuta, or splitting clitics from their hosts. Two papers that normalize differently can report numbers several points apart on identical systems, which is why the normalization script belongs with the result
- *(Ch. 4)* a documented step applied identically to the reference and the hypothesis before scoring, unifying Alef forms, removing Tatweel and short-vowel diacritics, and settling digits and punctuation, so that a correct transcript is not penalized for orthographic variation. These are scoring conventions, not claims of linguistic equivalence, and the script that implements them should be published with the numbers
- *(Ch. 14)* the stated, scripted transformation applied to references and hypotheses before scoring, covering diacritics, Alef and Hamza forms, and punctuation. Two systems that normalize differently are not comparable, so the script travels with the number

**TextGrid** — the annotation file Praat writes, a set of parallel tiers, for example a word tier and a phone tier, whose intervals line up with the audio. It travels with the sound file and is what aligners and trainers read back in *(Ch. 7)*

**Threat-and-harm model** — asking of a system what could go wrong, for whom, and how badly: the assets, the threats against them, and the harms that follow. Its use is that each failure mode calls for a different safeguard, so the model is built before the system rather than after an incident *(Ch. 13)*

**Time-frequency trade-off** — the limit, set by the window length, that sharp time and sharp frequency cannot be had at once. A long window gives the narrowband view, which resolves the individual harmonics of the voice and shows pitch; a short window gives the wideband view, which shows the formants and the striations of individual glottal pulses, so pick the window for the question *(Ch. 3)*

**Tool use** — letting a model call an external function, a search, a database or a calendar, and fold the result into its answer *(Ch. 11)*

**Trait inference** — predicting age, gender, emotion, personality or health from a voice, which the machinery of speaker recognition supports as readily as it supports identification. The prediction is a model output with an error rate rather than something the speaker declared, and consent to be recorded is not consent to be profiled, so a trait that was never disclosed should not be inferred, stored or acted on without a stated purpose and a lawful basis *(Ch. 13)*

**Transcript** — the Arabic text a cascade writes in the middle, and the axis on which the two architectures differ, as Section 9.5 used the same axis for synthesis. Because it is text, a wrong word can be seen in it and corrected before the next stage runs, which is also the moment at which an uncorrected one is handed on as though it were right; an end-to-end model has nothing there, so the same error is possible and invisible1 *(Ch. 10)*

**Transformer** — an architecture built entirely from attention, which reaches distant context in a single step and computes the whole sequence at once, so it trains far faster than a recurrent model; its one weakness for speech is that pure attention has little built-in sense of locality *(Ch. 4)*

**Translation direction** — which way the translation runs, which matters more in Arabic than the metric names suggest. Arabic into English puts the morphology on the input side, where the model absorbs it; English into Arabic puts it on the output side, where the metric has to score it. It is the first of the five questions to put to a benchmark, and a figure reported for Arabic without a direction is not a figure1 *(Ch. 10)*

**Triphone** — a phone modeled in the context of the one before and the one after, which captures how a phone sounds different depending on its neighbors at the cost of multiplying the number of states enormously *(Ch. 4)*


## U

**Unified multilingual model** — one model that performs speech-to-speech, speech-to-text, text-to-speech and text-to-text translation, and recognition, across many languages with Arabic among them. It covers Arabic in both directions and its shared multilingual training transfers some strength to lower-resource varieties, but breadth is not dialectal depth, so it is a strong starting point that must still be evaluated per dialect rather than trusted on its language list; streaming is a separate model released beside it rather than a mode of it1 *(Ch. 10)*

**Utterance embedding** — the single fixed-length vector that stands for a whole utterance, formed by pooling frame-level features and passed to a classifier. The i-vector was the hand-engineered version and a strong pre-deep-learning baseline, though sensitive to channel and recording conditions; modern systems learn the embedding instead, increasingly from a self-supervised encoder pretrained on large amounts of unlabeled audio, which is what lets a dialect classifier do well on Arabic’s scarce dialect labels *(Ch. 8)*


## V

**Viterbi algorithm** — the same left-to-right sweep as the forward algorithm with one change: where the forward algorithm adds the incoming paths, Viterbi keeps only the single best one, so it returns the most likely alignment of frames to states rather than the total *(Ch. 4)*

**Vocal-tract-length perturbation** — an augmentation that warps the frequency axis of adult speech by a small random factor to mimic the shorter vocal tracts of children, used to close part of the adult-to-child mismatch until real child data is available *(Ch. 12)*

**Vocoder**

- *(Ch. 9)* the stage that turns a mel spectrogram into an audible waveform, supplying the fine detail the spectrogram left out. The word is older than this use: it was coined for an analysis and resynthesis device of the 1930s, so a reader meeting it outside this book may meet the earlier meaning
- *(Ch. 11)* the stage that turns a short sequence back into an audible waveform (Section 9.5); in a speech-to-speech model it is what decodes the audio tokens

**Voice activity detection**

- *(Ch. 3)* the step that separates speech from silence and background, what the “trim silence” box of Figure 3.1 stands for. Its failures are asymmetric: a detector tuned for clean speech clips the quiet onsets of fricatives and drops short function words in noisy broadcast audio, and whatever it removes the model never learns from
- *(Ch. 7)* automatic labeling of speech-versus-silence regions, used to segment many hours of audio without hand work, though it needs a manual check on noisy or overlapping material

**Voice anonymization** — transforming speech so that what was said survives while who said it does not, keeping the audio usable for transcription or research. It is a claim about two measurements at once, an attacker’s success and a recognizer’s error rate, and for Arabic the second must include whether dialectal and phonetic content survived rather than words alone *(Ch. 13)*

**Voice biometric** — the use of a voice as an identifier, which is what makes voice authentication convenient and what makes shared audio dangerous. The credential cannot be reissued, so a leak is permanent in a way a password leak is not *(Ch. 13)*

**Voice-output communication aid** — the speaking-side assistive technology, which gives a voice to a person who cannot speak and which the personalized synthesis of Chapter 9 extends to voices that preserve a person’s own vocal identity from past recordings *(Ch. 12)*


## W

**Wait-k** — the simple and influential simultaneous policy that begins translating after k source words and thereafter keeps a fixed lag behind the speaker. It is an intuition borrowed from text translation, since a deployed streaming system commits on audio chunks or detected units rather than on clean word boundaries, and the lag it names in words equals the lag a listener feels in seconds only while the speaker keeps a constant rate1 *(Ch. 10)*

**Waveform** — the sound itself, stored as a long list of amplitude measurements over time *(Ch. 9)*

**Weak supervision** — training on labels that are cheap and noisy rather than careful, such as the imperfect transcripts harvested from the web that train Whisper. It escapes the labeling bottleneck by sheer scale, but the model inherits the biases of those transcripts, including a tilt toward Modern Standard Arabic on dialect *(Ch. 6)*

**Window** — a smooth bell-shaped weighting multiplied into each frame, tapering to near zero at the ends so the edges leak less energy across the spectrum. Hamming and Hann are the usual speech choices, and a plain rectangular window leaks the most *(Ch. 3)*

**Window-level connector** — a connector that reads a fixed window of encoder frames and emits a fixed number of outputs for it, so that the length of the audio stops setting the length of the sequence *(Ch. 11)*

**Word Error Rate**

- *(Ch. 1)* the smallest number of word substitutions, insertions, and deletions needed to turn a recognized text into the reference transcript, divided by the number of words in the reference. Lower is better and the value is not bounded above by one; it is interpretable only alongside the test split, the normalization applied, and whether diacritics were scored
- *(Ch. 14)* the standard recognition metric, and a number that means nothing without the normalization script that produced it. This chapter asks for it per dialect and per condition rather than pooled, because a single average hides exactly the groups a project is most likely to be failing


## Z

**Zero-shot recognition** — transcribing with a pretrained model as it stands, with no fine-tuning on the target data, which is what makes Whisper an unavoidable modern baseline *(Ch. 6)*

**Zero-shot voice cloning** — producing a target speaker’s voice from a few seconds of their speech, with no retraining *(Ch. 9)*

