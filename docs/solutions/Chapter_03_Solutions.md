# Chapter 3 Solutions: Digital Speech Processing

These solutions follow the numbering of the chapter's exercise list. Exercises 1 to 3 have companion notebooks; the numbers quoted below are what those notebooks produced when they were tested.

Notebooks for this chapter: [`Chapter_03_Exercise_01.ipynb`](Chapter_03_Exercise_01.ipynb), [`Chapter_03_Exercise_02.ipynb`](Chapter_03_Exercise_02.ipynb), [`Chapter_03_Exercise_03.ipynb`](Chapter_03_Exercise_03.ipynb).

---

## Exercise 1

**Task.** Generate a 9 kHz sine wave and sample it at 16 kHz with no anti-aliasing filter; plot the spectrogram and report the frequency at which the aliased tone appears. State the minimum sampling rate that would avoid aliasing for content up to 7 kHz, the standard rate you would choose in practice, and where the anti-aliasing cutoff should sit.

**Solution (notebook `Chapter_03_Exercise_01.ipynb`).**

*What the notebook does.* It evaluates sin(2π · 9000 · n / 16000) at the 16 kHz sample instants, which is exactly what an analog-to-digital converter without an anti-aliasing filter does, then plots a spectrogram (512-point Hann, 16 kHz) and finds the peak of the average spectrum.

*Measured result.* The tone appears at **7000 Hz**. The notebook also shows that the 9 kHz samples are numerically identical (up to a sign) to the samples of a true 7 kHz tone, which is why the corruption is irreversible: nothing downstream can tell the two apart.

*The arithmetic.* A 16 kHz rate has a Nyquist limit of 8 kHz. A component at 9 kHz is 1 kHz above the limit and folds back by the same amount: 8 kHz minus 1 kHz = 7 kHz. In general the observed frequency is the distance from the true frequency to the nearest multiple of the sampling rate, |9000 minus 16000| = 7000 Hz.

*Design answers.*

| Question | Answer |
|---|---|
| Minimum sampling rate for content up to 7 kHz | strictly more than 2 × 7 kHz = **14 kHz**; 14 kHz itself is the theoretical boundary and leaves no room for a filter transition band |
| Standard rate in practice | **16 kHz**, the common default for speech recognition (Table 3.1); it keeps the useful band to 8 kHz and matches most pretrained models and corpora |
| Anti-aliasing cutoff | **below the 8 kHz Nyquist limit**: a passband edge near 7 kHz with the stopband fully attenuated by 8 kHz, so that the transition band of a realizable filter fits between the highest wanted frequency and Nyquist. The notebook demonstrates this with an elliptic low-pass (passband 7 kHz, stopband 8 kHz, 60 dB) applied *before* decimation from 192 kHz: the 9 kHz tone disappears instead of folding |

The order matters: the filter must act before the rate is reduced. Resampling an already-aliased recording cannot undo the damage (Common Pitfalls, Section 3.8).

---

## Exercise 2

**Task.** Extract several emphatic /tˤ/ and plain /t/ tokens from an Arabic corpus, measure F2 near the vowel onset and at the midpoint with a formant tracker, plot the two distributions, state which spectrogram view you used to locate the vowel and why, and report the number of tokens, speaker and dialect, tracker settings, median F2 per class and point, and the plot.

**Solution (notebook `Chapter_03_Exercise_02.ipynb`).**

*Data flag.* The minimal-pair clips that the exercise refers to were **not included** in the material supplied for these solutions, and SADA (Kaggle) and Common Voice (Hugging Face) both require a login and licence acceptance, so the notebook could not be tested on real corpus tokens. It therefore has two paths:

* **Path A (real tokens):** upload WAV files plus a `tokens.csv` with vowel boundaries (marked in Praat, Chapter 7 walkthrough, or from the wideband spectrogram the notebook draws). The measurement code is the same as Path B.
* **Path B (synthetic fallback, default):** a source-filter synthesizer generates 12 /tiːn/-like and 12 /tˤiːn/-like tokens whose F2 trajectories follow the values the book reports for the author's recording in Figure 2.4 (about 2580 Hz for the plain token and 1840 Hz for the emphatic token at 30 ms after voicing onset, rising toward a common value over about 60 ms). **This is illustrative data, not speech**; it exists so that the pipeline can be run and checked end to end.

*Which spectrogram view, and why.* The **wideband** view (5 ms window) was used to locate the burst, the first glottal pulse and the vowel edges, because a short window gives sharp time resolution and shows the formant bands as continuous stripes; the **narrowband** view (30 ms window) resolves individual harmonics, which is what you want for pitch but which blurs the onset and hides formants behind harmonic lines (Section 3.4, Figure 3.5). The notebook draws both for one token of each class.

*Tracker settings (report these).* Praat "To Formant (burg)" through `praat-parselmouth`: time step 5 ms, maximum 5 formants, formant ceiling 5000 Hz (adult male; 5500 Hz for a female voice), window 25 ms, pre-emphasis from 50 Hz. F2 was read at **onset** = voicing onset + 30 ms (the point used in Figure 2.4) and at the **vowel midpoint**.

*Report for the run as tested (Path B, synthetic tokens).*

| Item | Value |
|---|---|
| Tokens | 12 plain, 12 emphatic (synthetic; no speaker, no dialect) |
| Median F2 at onset | plain **2613 Hz**, emphatic **1888 Hz** |
| Median F2 at midpoint | plain **2426 Hz**, emphatic **2324 Hz** |
| Plot | box plots with individual tokens overlaid, one panel per measurement point (in the notebook) |

*Interpretation.* The emphatic class shows a much lower F2 at the vowel edge nearest the consonant (a gap of about 700 Hz at onset on these tokens) and the gap has largely closed by the midpoint, which is the "recovery" the book describes: emphasis is something the vowel recovers from rather than carries throughout. On real corpus tokens the numbers will differ by speaker, dialect and vowel, and the two distributions will overlap more; the onset measurement is the one that separates the classes, so a front end must keep enough time and frequency resolution to preserve that transition. When Path A is run on real data, fill the same table and state the speaker and dialect from the corpus metadata.

---

## Exercise 3

**Task.** Build a feature-extraction pipeline that takes raw 16 kHz audio and outputs 40-dimensional log-mel vectors. Give the size after each stage, say where you would continue to obtain 13 MFCCs, compare against a standard toolkit, and state whether the pipeline uses the magnitude or power spectrum and whether the zeroth coefficient is kept.

**Solution (notebook `Chapter_03_Exercise_03.ipynb`).**

*Settings.* Frame 25 ms = 400 samples, zero-padded to a 512-point FFT (Figure 3.7); hop 10 ms = 160 samples; 400-point Hamming window (periodic form, the STFT convention); one-sided **power** spectrum; 40 triangular mel filters from 0 to 8000 Hz, Slaney convention, no filter normalization; natural log with a floor of 1e-10; no pre-emphasis; no centring, first frame at sample 0, last partial frame dropped.

*Size after each stage, for one second of 16 kHz audio.*

| Stage | Operation | Size |
|---|---|---|
| 0 | raw samples | 16,000 |
| 1 | framing: 400-sample frames, hop 160, padded to 512 | 97 × 512 (400 of the 512 samples inside the window) |
| 2 | Hamming window | 97 × 512 |
| 3 | 512-point FFT, one-sided power spectrum (bin spacing 31.25 Hz) | 97 × 257 |
| 4 | 40-filter mel filterbank (matrix 40 × 257) | 97 × 40 |
| 5 | logarithm | **97 × 40 log-mel matrix** |
| 6 | (to obtain MFCCs) DCT-II over the 40 log-mel values, keep 13 | 97 × 13 |
| 7 | (optional) append delta and delta-delta | 97 × 39 |

The frame count depends on the framing convention: 1 + (16000 minus 512)/160 = 97 here; padding the last frame or centring frames (librosa's `center=True`) gives 98 or 101. Table 3.3 asks for this to be reported. The book's "about 100 frames per second" covers all of them.

*Where MFCCs continue.* After Stage 5. The 40 log-mel values of each frame are decorrelated by a type-II DCT and the first 13 coefficients are kept (Stage 6); classical systems then add deltas and cepstral normalization (Stage 7 and Section 3.8).

*Comparison with a standard toolkit.* Against `librosa.feature.melspectrogram` and `librosa.feature.mfcc` with the same settings (`n_fft=512, hop_length=160, win_length=400, window='hamming', center=False, power=2.0, n_mels=40, htk=False, norm=None`, natural log, `dct_type=2, norm='ortho'`), the maximum absolute differences measured in the test run were 2.2 × 10⁻⁴ on the mel energies, 4.7 × 10⁻⁷ on the log-mel values and 2.8 × 10⁻⁶ on the 13 MFCCs, that is, floating-point agreement. Two details had to be matched to get there: the periodic (not symmetric) Hamming window, and the placement of the 400-point window centred inside the 512-point frame. Both are the kind of unstated default that Table 3.3 warns about.

*Statement of choices.* The pipeline uses the **power spectrum** (|X|²), as Kaldi and librosa do; HTK-style pipelines use the magnitude spectrum, which shifts the log values by a factor of two but not their shape. The **zeroth coefficient is kept** (c0 to c12); many classical recipes replace c0 with log energy or drop it, and either choice must be reported. The mel convention is Slaney; an HTK-style toolkit (torchaudio's default) places the filters slightly differently.

---

## Exercise 4

**Task.** A recognizer trained on 16 kHz studio recordings performs poorly on 8 kHz call-centre audio. Give two reasons rooted in this chapter and propose a matched front end and training strategy, including the mel upper frequency, the CMVN scope, and whether to fine-tune on telephone-band data.

**Suggested solution.**

*Two reasons.*

1. **Bandwidth mismatch (Section 3.2, Section 3.9, Figure 3.8).** Telephone audio sampled at 8 kHz contains nothing above 4 kHz, and the classic telephone band is only about 300 to 3400 Hz. The studio-trained model learned to use the 4 to 8 kHz region, where fricative noise, the upper formants and much speaker detail live. On call-centre audio those mel bands are empty or contain only codec noise, so the model sees input it never saw in training. Upsampling 8 kHz audio to 16 kHz does not help: it cannot recreate the missing frequencies, it only produces silent upper bands.
2. **Channel and noise mismatch (Section 3.8).** Handsets, telephone codecs and background noise add persistent spectral colouring and a higher noise floor that studio data lacks. Log-mel features encode this colouring as a constant offset per band, so the whole feature distribution shifts relative to the training distribution; without normalization or matched training data the model is off-distribution before any phonetic decision is made.

*Matched front end.*

* Work at the channel's real bandwidth. Either accept 8 kHz input directly (if the model architecture allows) or resample to 16 kHz for compatibility while **setting the mel upper frequency to 4000 Hz** (3400 Hz if the corpus is strictly telephone-band), so that no filters sit in the empty region; keep 40 filters, which now sit more densely in the useful band.
* Frame 25 ms, hop 10 ms, Hamming or Hann, as before; pre-emphasis is optional and should follow the chosen model.
* **CMVN scope: per recording, or per side of a call** (per speaker-channel), so that each handset's colouring is removed by its own statistics. Global CMVN would leave the handset differences in; per-utterance CMVN on very short turns is unstable. Report the scope.
* Apply SpecAugment and additive noise at realistic SNRs to the training data only.

*Training strategy.* **Yes, fine-tune on telephone-band data**, and preferably build the training set to match deployment: real 8 kHz Gulf call-centre recordings where licensing allows (SAAVB or the LDC Gulf telephone corpus, Table 7.1), plus the studio corpus **band-limited to the telephone band and downsampled** to 8 kHz so that its content is not wasted. If a denoiser or codec will be in the deployment path, run the training audio through it too, so the model learns its artefacts (Section 8.7). Evaluate on held-out call-centre audio, report WER per dialect and per noise condition, and compare the matched system against the studio system on the same test set so the improvement is measured rather than assumed.

---

## Exercise 5

**Task.** You receive 100 hours of transcribed speech from 50 speakers. Design training, development and test splits, state the rule that protects the evaluation, and explain what goes wrong if you split by utterance instead of by speaker. Note how you would balance dialect and gender.

**Suggested solution.**

*The rule.* **Speaker-disjoint splits**: every speaker, with all of his or her recordings and sessions, belongs to exactly one of the three sets (Section 3.10; the recipe box in Section 7.3.4). The test set must contain no speaker, session or source recording that appears in training or development, and the test set is touched only for the final evaluation.

*A concrete design.* With 50 speakers and 2 hours per speaker on average, a reasonable split is 40 speakers for training (about 80 h), 5 speakers for development (about 10 h) and 5 speakers for test (about 10 h). Five speakers is the minimum that gives a usable per-speaker breakdown; if the corpus is more skewed (some speakers with 6 h, others with 15 min), assign by speaker and then check hours, moving whole speakers until the development and test sets each hold roughly 8 to 12 hours. Procedure: group clips by speaker, shuffle the speaker list with a recorded random seed, assign whole speakers to test, then development, then training, and confirm with set-intersection checks that speaker IDs, session IDs and source files do not overlap. If the material is read speech and the goal is to test unseen text, also keep the prompts disjoint. Save and version the split files.

*What goes wrong with an utterance-level split.* Random utterances from the same speaker land in training and test. The model then sees the test speakers' voices, microphones, rooms and, for read speech, often the same sentences during training. Test WER measures recognition of familiar voices and conditions, not generalization to new speakers, so it is optimistically biased, sometimes by a large margin, and the model chosen on such a test set will disappoint in deployment. This is the leakage the chapter warns about, and it is not fixed by making the test set larger.

*Balancing dialect and gender.* Do the balancing at the speaker level, never by moving individual clips. Stratify the speaker list by dialect and by gender before assignment, so that the development and test sets contain enough speakers of each dialect and each gender to report a per-group WER (at least two or three speakers per group per set, more if possible). If a group is small in the corpus, prefer to keep its speakers in development and test so that its performance can at least be measured, and reweight or oversample the remaining speakers of that group in training. Report the composition of every split (hours, speakers, dialects, genders) beside any result, and never report only the pooled WER.

---

### Flags and notes for the companion website

* Exercise 2 depends on minimal-pair clips that were not supplied; the notebook's Path B is a labelled synthetic stand-in and Path A is ready for the real clips or corpus tokens once they are available. Its real-audio path is untested in this release.
* Exercise 3's numbers were measured on a synthetic one-second signal; the notebook accepts an uploaded clip and the size table is unchanged for any one-second 16 kHz input.
