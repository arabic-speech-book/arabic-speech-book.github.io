# Chapter 5 Solutions: Arabic ASR II, End-to-End Models

These solutions follow the numbering of the chapter's exercise list. Exercises 1 and 5 have companion notebooks; their executed outputs are quoted below.

Notebooks for this chapter: [`Chapter_05_Exercise_01.ipynb`](Chapter_05_Exercise_01.ipynb), [`Chapter_05_Exercise_05.ipynb`](Chapter_05_Exercise_05.ipynb).

---

## Exercise 1

**Task.** Write a short Python function that generates all fifteen valid length-4 CTC frame labelings that collapse to the target 'A B' (blank written as a dash) and prints them. Then extend it to print one invalid length-4 labeling, with what it collapses to and why it fails.

**Solution (notebook `Chapter_05_Exercise_01.ipynb`).**

*Method.* `ctc_collapse(path)` merges consecutive repeats and then drops blanks, exactly the two-step rule of Section 5.2; `valid_paths(target, T)` enumerates all 3⁴ = 81 labelings over {A, B, -} and keeps those that collapse to the target.

*The fifteen valid paths (executed output):*

```
A A A B   A A B B   A A B -   A A - B   A B B B
A B B -   A B - -   A - B B   A - B -   A - - B
- A A B   - A B B   - A B -   - A - B   - - A B
```

*Why fifteen.* Every valid path has the shape `blank* A⁺ blank* B⁺ blank*`, five slots whose lengths sum to 4 with the two token runs at least one long. After reserving one frame for A and one for B, two free frames are distributed over five slots: C(2 + 4, 4) = 15.

*Invalid labelings and why they fail (executed output):*

| Path | Collapses to | Why it fails |
|---|---|---|
| `B A A -` | B A | order is wrong; CTC alignments are monotonic, so the target's tokens must appear in order |
| `A - A B` | A A B | a blank between two identical tokens *prevents* their merger, so this path spells a two-A target |
| `A A - -` | A | the second token was never emitted |
| `A B B B` | A B | (valid) repeated B's merge into one; many paths, one transcript |

The second row is the Arabic point of the exercise: if a geminate consonant is written as a doubled token (Figure 5.1, ممكن), the path *must* contain a blank between the two copies, and the notebook shows that a target 'A A' has no valid path at all with T = 2 frames and only one with T = 3. If gemination is written with a shadda token instead, no blank is needed.

---

## Exercise 2

**Task.** Explain why the RNN-Transducer's alignment is monotonic and why that property is what makes low-latency streaming possible. Contrast it with an attention decoder.

**Suggested solution.**

*Why the alignment is monotonic.* At each step the joint network of an RNN-T (Section 5.3) chooses between emitting a token and emitting a blank. Emitting a token appends to the transcript and feeds the prediction network, but leaves the model at the same encoder frame; emitting a blank appends nothing and moves the model to the *next* encoder frame. There is no third move: the model can never return to an earlier frame or jump ahead. Its path through the (frame, token) grid therefore only goes right (more audio) or up (more tokens), which is what monotonic means. Training sums over all such paths, so the property holds for every alignment the model can represent, not just the one it happens to prefer.

*Why that enables streaming.* Because the decision at frame *t* depends only on the encoder output up to *t* (given a causal or limited-lookahead encoder) and on the tokens already emitted, the recognizer can emit text the moment the evidence for a token has arrived, without waiting for the end of the utterance. The latency is bounded by the encoder's lookahead plus whatever delay the model learned before emitting; it does not grow with utterance length. The prediction network gives it a built-in memory of the output history, so it can be accurate without an external LM in the loop.

*Contrast with an attention decoder.* A LAS-style decoder (Section 5.4) computes, for every output token, a soft weight over *all* encoder positions and reads a weighted summary of the whole utterance. Nothing forces those weights to move left to right, and in standard form the decoder does not start until the entire encoder sequence exists. Two consequences follow. First, it cannot stream without modification (monotonic or chunked attention variants exist but are additions, not the default). Second, because the alignment is free, the decoder can lose its place, re-reading a region (repetitions) or skipping one (deletions), especially in long or noisy audio, which is exactly the failure mode that RNN-T's enforced monotonicity rules out. The price the transducer pays is a more expensive training loss over the frame-by-token lattice and a decoder that cannot look at the future to fix an early mistake. Table 5.1 summarizes the contrast.

---

## Exercise 3

**Task.** Describe in words how shallow fusion changes the score of a candidate during beam search, and explain what happens to the output when the fusion weight is set too high.

**Suggested solution.**

*What shallow fusion does.* During beam search the recognizer extends each partial transcript one token at a time and scores every extension. Without fusion the score is the recognizer's own log-probability of the token given the audio and the tokens so far. With shallow fusion (Section 5.6) a second, external language model, trained on much more text, gives its own log-probability of the same token given the text so far, and the two are added: score = log P_ASR(token) + λ · log P_LM(token), where λ is the fusion weight. Nothing inside either model changes; the combination happens only at decoding time, hypothesis by hypothesis, which is why it is called *shallow*. Candidates that are both acoustically supported and linguistically plausible rise in the beam; candidates the LM finds unlikely (rare spellings, ungrammatical sequences) sink, even if the audio slightly favours them. A length or token-insertion bonus is usually added with it, because the LM term penalizes every extra token and would otherwise favour short outputs (Table 5.2).

*When λ is too high.* The LM's opinion dominates the acoustic evidence. The decoder then produces text that reads fluently but was not said: common words replace rare ones, dialectal words drift toward MSA forms when the LM was trained on MSA news (the recognizer effectively "translates"), names and numbers are replaced by likelier-sounding alternatives, and, because the LM term grows with every emitted token, the output tends to become shorter (deletions) unless the insertion bonus is raised in step. The WER curve in Figure 5.5 falls with a moderate weight and rises again past the optimum; the weight must therefore be chosen on a development set, never on the test set, and reported together with the LM's training text and tokenization.

---

## Exercise 4

**Task.** You are building a streaming Arabic voice assistant and an offline broadcast transcription service. Recommend an architecture (CTC, RNN-Transducer, attention, or hybrid) for each and justify the choice using Table 5.1.

**Suggested solution.**

*Streaming voice assistant: RNN-Transducer with a streaming (causal or limited-lookahead Conformer) encoder.* From Table 5.1 the requirements are streaming and low latency, and the two streaming-capable rows are CTC and RNN-T. CTC's limitation is that it "does not directly condition each prediction on previously emitted tokens", so it relies on an external LM for spelling and word-sequence knowledge, and adding a fused LM to a streaming decoder costs latency and tuning. RNN-T's prediction network "summarizes previously emitted non-blank tokens", giving it an internal model of Arabic token sequences, including clitic stacking and inflected forms, while its monotonic alignment keeps it streaming. Its cost ("training and decoding are more computationally demanding than CTC") is paid once at training time and is acceptable for a product. Attention-based models are ruled out because they are "not naturally" streaming and can repeat or skip. A practical refinement: use a small CTC head jointly during training to stabilize the encoder, and a dialect-aware tokenizer (Exercise 5) so that the assistant's spontaneous, dialectal, code-switched input is not forced into MSA spellings.

*Offline broadcast transcription: hybrid CTC/attention with a full-context Conformer encoder, joint CTC/attention decoding and shallow fusion with a broadcast-domain LM.* Offline means the whole recording is available, so the attention row's limitation about streaming does not apply, and its strength, a decoder that "conditions each prediction on earlier output tokens" while reading global acoustic context, can be used in full. Attention's own limitation, repeating or skipping "especially in long or noisy recordings", is exactly what broadcast audio contains, and the hybrid design answers it: the CTC branch enforces a monotonic alignment during training and penalizes non-monotonic hypotheses during joint decoding (Section 5.5). An external MSA-plus-dialect broadcast LM through shallow fusion adds the large-text knowledge that helps rare names and formal vocabulary. This is also the design ESPnet ships recipes for, which matters for reproducibility. RNN-T would also work offline, but it gives up the attention decoder's global context without gaining anything from its streaming ability.

---

## Exercise 5

**Task.** Choose an output unit for an end-to-end recognizer for (a) MSA broadcast news and (b) spontaneous dialectal speech with no standard spelling, using Table 5.3. Justify each, referring to OOV risk and morphology. Then, using Python with SentencePiece or CAMeL Tools, tokenize وسيكتبونها with each method and compare the actual output tokens.

**Solution (notebook `Chapter_05_Exercise_05.ipynb`).**

*(a) MSA broadcast news: learned subwords* (BPE or unigram, vocabulary of a few thousand, trained on normalized broadcast transcripts). Table 5.3 calls subwords "a practical starting point for both MSA and dialectal ASR" and MSA is their best case: the spelling is standard and consistent, so the pieces a tokenizer learns are stable across the corpus; the morphology that would explode a word vocabulary (clitics, inflection, Table 4.4) is absorbed because frequent clitics and affixes become their own pieces; and full character coverage removes word-level OOVs entirely. Morphological segments are a defensible alternative here, because a good MSA analyzer exists (CAMeL Tools), and they are worth trying when an external LM or linguistically informed error analysis is wanted, but they add an analyzer, a scheme decision and disambiguation to the pipeline. Whole words are ruled out by OOV risk on names and rare inflected forms; characters would work but produce needlessly long sequences when good subword statistics are available.

*(b) Spontaneous dialect with no standard spelling: characters, or a small subword vocabulary with full character coverage* (which behaves close to characters). Table 5.3 lists characters for exactly this case: "data is limited, detailed orthographic output is required, or the vocabulary is highly variable", and "can represent different dialect spellings". With no standard orthography the same word appears in several spellings; a large subword vocabulary would learn several competing pieces for each and generalize poorly, and a morphological analyzer either does not exist for the variety or does not match its spellings (Table 5.3: "dialect coverage is uneven"). Characters keep the inventory small and fixed, so the model sees consistent units even when the spelling varies, and OOV risk is zero. The remaining spelling variation must then be handled by a transcription convention (CODA) applied to training and scoring alike, and by reporting CER beside WER (Section 5.7.2).

*Actual tokenizer outputs (executed).* The word وسيكتبونها does not occur in the SentencePiece training text (2,104 FLEURS Arabic sentences, 38,272 words), so every method below is handling an unseen word.

| Method | Output | Pieces |
|---|---|---|
| CAMeL Tools 1.6.0, MLE disambiguator `calima-msa-r13`, ATB and D3 schemes | و+ س+ يكتبون +ها | 4 |
| CAMeL Tools, BW scheme | و+ س+ ي+ كتب +ون +ها | 6 |
| SentencePiece BPE, vocab 500 and 2000 | ▁و + سي + كت + ب + ون + ها | 6 |
| SentencePiece BPE, vocab 8000 | ▁وسي + كت + ب + ونها | 4 |
| SentencePiece unigram, vocab 500 and 2000 | ▁و + س + ي + ك + ت + ب + ون + ها | 8 |
| SentencePiece unigram, vocab 8000 | ▁وس + يك + ت + ب + ونها | 5 |

The chosen CAMeL analysis was وَسَيَكْتُبُونَها, tag `وَ/PART+سَ/FUT_PART+يَ/IV3MP+كْتُب/IV+ُونَ/IVSUFF_SUBJ:MP_MOOD:I+ها/IVSUFF_DO:3FS`, lemma كَتَب, gloss "will + they write + it". The morphological pieces are the four morphemes of the hand analysis (conjunction, future marker, inflected verb, object pronoun), labelled and stable. The subword pieces are frequent character strings: some coincide with morphemes (a leading و, a trailing ها or ون), but others cut through the root (كت + ب, or وسي joining the conjunction to part of the verb), and the segmentation changes with algorithm and vocabulary size, as the book warns. Both routes avoid an OOV; only the analyzer's route carries linguistic meaning, and only the subword route is available for a variety without an analyzer.

---

### Flags and notes for the companion website

* The SentencePiece models in Exercise 5 are trained on a small public text (FLEURS Arabic transcripts) so that the notebook is self-contained; a broadcast-transcript tokenizer will segment the word differently, which is the point of the exercise.
