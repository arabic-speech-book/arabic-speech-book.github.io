# مصادر الأشكال

السكربت الذي يرسم كل شكل مرسوم بالكود في الكتاب. الشكل 3.1 من رسم المؤلّفة لا من الكود، فلا سكربت له؛ أما الأشكال 3.2 و3.4 و3.7 فأُعيد رسمها من سكربتات في مراجعة سبتمبر 2026 محفوظة في المخطوطة وغير منشورة هنا. الوحدات المشتركة التي يستوردها كل سكربت في `figure-scripts/shared/` (انظر [`README`](figure-scripts/README.txt)).

```bash
pip install matplotlib numpy scipy pillow arabic_reshaper python-bidi
cd figure-scripts/ch09 && python make_fig9_1.py   # يكتب fig9_1.png و fig9_1.pdf
```


## الفصل 1

| الشكل | الوصف | المصدر |
|---|---|---|
| 1.1 | A timeline of speech processing, from dynamic time warping and HMM-GMM systems through the deep-learning turn to end-to-end and foundation models, with Arabi… | [`ch01/make_figures.py`](figure-scripts/ch01/make_figures.py) |
| 1.2 | How a spoken request becomes an action: the microphone captures the opening scene's dialectal utterance, a front end extracts features, the recognizer produc… | [`ch01/make_figures.py`](figure-scripts/ch01/make_figures.py) |

## الفصل 2

| الشكل | الوصف | المصدر |
|---|---|---|
| 2.1 | The source-filter model of speech. Air from the lungs drives the vocal folds, which chop it into pulses at the rate F0: that is the source. The vocal tract i… | [`ch02/make_fig2_1.py`](figure-scripts/ch02/make_fig2_1.py) |
| 2.2 | The Arabic consonant inventory arranged by place and manner of articulation, with the emphatic, pharyngeal, and uvular consonants highlighted. | [`ch02/make_fig2_2.py`](figure-scripts/ch02/make_fig2_2.py) |
| 2.3 | plots the vowels in the F1-by-F2 space that Section 2.1 introduced. The height of a vowel (how closed the mouth is) runs along F1, and its frontness or backn… | [`ch02/make_fig2_3.py`](figure-scripts/ch02/make_fig2_3.py) |
| 2.4 | Spectrograms of the minimal pair تين (tīn, ‘figs’) and طين (ṭīn, ‘mud’), recorded by the author. The vowel is the same in both, but next to the emphatic the… | [`ch02/make_fig2_4.py`](figure-scripts/ch02/make_fig2_4.py) |
| 2.5 | Positional letter shapes. A fully joining letter takes four shapes (isolated, initial, medial, final), while a non-joining letter such as rāʾ ر has only two,… | [`ch02/make_fig2_5.py`](figure-scripts/ch02/make_fig2_5.py) |
| 2.6 | Root-and-pattern morphology: the root k-t-b interleaved with several patterns to produce a family of related words. The three root circles run right to left,… | [`ch02/make_fig2_6.py`](figure-scripts/ch02/make_fig2_6.py) |
| 2.7 | The major spoken-Arabic dialect groups across the Arab world, each with its own fill and hatch pattern. The boundaries are gradual zones, not sharp lines: ne… | [`ch02/make_fig2_7.py`](figure-scripts/ch02/make_fig2_7.py) |

## الفصل 3

| الشكل | الوصف | المصدر |
|---|---|---|
| 3.1 | places this chapter inside the larger workflow that turns a raw voice recording into a model-ready dataset: record, save, segment, annotate or transcribe, pr… | رسم المؤلّفة — في الكتاب |
| 3.2 | zooms in on the feature-extraction part of that workflow, the sound-to-features path that is the main technical focus of this chapter. | مُعاد رسمه — السكربت في المخطوطة |
| 3.3 | Sampling and quantization. A continuous wave is measured at regular instants (sampling) and each measurement is rounded to the nearest level (quantization),… | [`ch03/make_fig3_3.py`](figure-scripts/ch03/make_fig3_3.py) |
| 3.4 | Short-time analysis: the waveform is split into overlapping frames, each frame is multiplied by a smooth window, and the Fourier transform of each frame give… | مُعاد رسمه — السكربت في المخطوطة |
| 3.5 | Narrowband and wideband spectrograms of the emphatic word طين (ṭīn, ‘mud’) and its plain counterpart تين (tīn, ‘figs’), from the author’s recording used in C… | [`ch03/make_fig3_5.py`](figure-scripts/ch03/make_fig3_5.py) |
| 3.6 | The mel filterbank. Triangular filters are spaced evenly on the perceptual mel scale, which places many narrow filters at low frequencies and fewer wide filt… | [`ch03/make_fig3_6.py`](figure-scripts/ch03/make_fig3_6.py) |
| 3.7 | The Mel-Frequency Cepstral Coefficient (MFCC) pipeline, from optional pre-emphasis through the mel filterbank and logarithm to the Discrete Cosine Transform… | مُعاد رسمه — السكربت في المخطوطة |
| 3.8 | The same recording of تين (tīn, ‘figs’) as captured at 16 kHz, and after passing through a telephone channel: band-limited to 300 to 3400 Hz and resampled to… | [`ch03/make_fig3_8.py`](figure-scripts/ch03/make_fig3_8.py) |

## الفصل 4

| الشكل | الوصف | المصدر |
|---|---|---|
| 4.1 | shows how the four fit together at recognition time: features enter on one side, the decoder searches a space jointly defined by the acoustic model, the lexi… | [`ch04/make_fig4_1.py`](figure-scripts/ch04/make_fig4_1.py) |
| 4.2 | Word Error Rate as a minimum edit distance, on the sentence ذهب الأولاد إلى المدرسة (dhahaba al-awlād ilā al-madrasa, ‘the boys went to the school’) and what… | [`ch04/make_fig4_2.py`](figure-scripts/ch04/make_fig4_2.py) |
| 4.3 | A left-to-right HMM for the word باب (bāb, ‘door’): three states per phone for /b aː b/, self-loops absorbing duration, and a Gaussian-mixture emission distr… | [`ch04/make_fig4_3.py`](figure-scripts/ch04/make_fig4_3.py) |
| 4.4 | The HCLG composition: four transducers, HMM topology (H), context (C), lexicon (L), and language model (G), compose into one searchable decoding graph. | [`ch04/make_fig4_4.py`](figure-scripts/ch04/make_fig4_4.py) |
| 4.5 | GMM-HMM versus DNN-HMM: the HMM states, lexicon, language model, and decoding graph are identical; the Gaussian mixtures that scored each frame are replaced… | [`ch04/make_fig4_5.py`](figure-scripts/ch04/make_fig4_5.py) |
| 4.6 | One Conformer block: a half-step feed-forward layer, multi-head self-attention for global context, a convolution module for local acoustic structure, a secon… | [`ch04/make_fig4_6.py`](figure-scripts/ch04/make_fig4_6.py) |

## الفصل 5

| الشكل | الوصف | المصدر |
|---|---|---|
| 5.1 | What the blank symbol is for, worked through on ممكن (mumkin, ‘possible’), whose first two letters are both mīm. Read each part from the bottom up. In A the… | [`ch05/make_fig5_1.py`](figure-scripts/ch05/make_fig5_1.py) |
| 5.2 | The RNN-Transducer: an acoustic encoder, a prediction network over the output history, and a joint network that combines them to emit the next token or a bla… | [`ch05/make_fig5_2.py`](figure-scripts/ch05/make_fig5_2.py) |
| 5.3 | An attention-based encoder-decoder and its attention heatmap. A healthy alignment forms a roughly diagonal band from encoder frames to output tokens; looping… | [`ch05/make_fig5_3.py`](figure-scripts/ch05/make_fig5_3.py) |
| 5.4 | Hybrid CTC/attention: one shared encoder feeds a CTC head and an attention decoder. Training minimizes a weighted sum of the two losses, and decoding scores… | [`ch05/make_fig5_4.py`](figure-scripts/ch05/make_fig5_4.py) |
| 5.5 | How the language-model fusion weight affects the Word Error Rate (WER). The shape is illustrative rather than measured: too small a weight under-uses the ext… | [`ch05/make_fig5_5.py`](figure-scripts/ch05/make_fig5_5.py) |

## الفصل 6

| الشكل | الوصف | المصدر |
|---|---|---|
| 6.1 | How speech models learn, ordered from most to least hand-labeling. Supervised training uses only labeled pairs; semi-supervised self-training adds pseudo-lab… | [`ch06/make_fig6_1.py`](figure-scripts/ch06/make_fig6_1.py) |
| 6.2 | The wav2vec 2.0 architecture: a convolutional feature encoder, a quantizer that maps the latents to a discrete codebook, and a context Transformer trained to… | [`ch06/make_fig6_2.py`](figure-scripts/ch06/make_fig6_2.py) |
| 6.3 | The HuBERT training loop: cluster speech features into pseudo-labels, mask spans and predict the cluster of the masked frames, then re-cluster from the impro… | [`ch06/make_fig6_3.py`](figure-scripts/ch06/make_fig6_3.py) |
| 6.4 | Layer-wise probing (illustrative). Speaker information tends to peak in early layers, while phonetic information peaks in the middle layers, so the most usef… | [`ch06/make_fig6_4.py`](figure-scripts/ch06/make_fig6_4.py) |
| 6.5 | Parameter-efficient adaptation. The pretrained block stays frozen, shown in grey; the only trainable parts are the two orange inserts, an adapter bottleneck… | [`ch06/make_fig6_5.py`](figure-scripts/ch06/make_fig6_5.py) |
| 6.6 | Per-dialect WER before and after Arabic fine-tuning (illustrative). Every variety improves, yet the pooled average, drawn as the dashed line, sits below thre… | [`ch06/make_fig6_6.py`](figure-scripts/ch06/make_fig6_6.py) |

## الفصل 7

| الشكل | الوصف | المصدر |
|---|---|---|
| 7.1 | places every resource in the catalog on a release timeline, from the early KACST and King Saud University databases to the multidialectal corpora and learner… | [`ch07/make_fig7_1.py`](figure-scripts/ch07/make_fig7_1.py) |
| 7.2 | The data pipeline from recruitment to release. Each box is a step a project has to plan for, and the two that are easiest to underestimate are the ones in th… | [`ch07/make_fig7_2.py`](figure-scripts/ch07/make_fig7_2.py) |
| 7.3 | A Praat annotation view of the word تين, tin, ‘figs’, taken from the recording Chapter 2 uses for Figure 2.4. The waveform and the spectrogram are computed f… | [`ch07/make_fig7_3.py`](figure-scripts/ch07/make_fig7_3.py) |
| 7.4 | Transcribed hours per Arabic variety, drawn to show the shape of the imbalance rather than to be read off: Modern Standard Arabic dominates and the dialects… | [`ch07/make_fig7_4.py`](figure-scripts/ch07/make_fig7_4.py) |

## الفصل 8

| الشكل | الوصف | المصدر |
|---|---|---|
| 8.1 | The major spoken-dialect groups, laid out west to east and south to north on their approximate geography, with a line drawn between every pair whose regions… | [`ch08/make_fig8_1.py`](figure-scripts/ch08/make_fig8_1.py) |
| 8.2 | The dialect identification pipeline. One utterance becomes frame-level features, whether hand-designed or produced by a self-supervised encoder; those frames… | [`ch08/make_fig8_2.py`](figure-scripts/ch08/make_fig8_2.py) |
| 8.3 | Self-supervised speech embeddings projected to two dimensions and marked by dialect. The values are invented, which is why the axes carry no numbers and the… | [`ch08/make_fig8_3.py`](figure-scripts/ch08/make_fig8_3.py) |
| 8.4 | The three speaker tasks side by side. Identification chooses among a closed gallery of enrolled speakers and returns which one. Verification compares one utt… | [`ch08/make_fig8_4.py`](figure-scripts/ch08/make_fig8_4.py) |
| 8.5 | The clustering pipeline for diarization. Silence is removed, the speech is cut into short windows, each window becomes one speaker embedding, and the embeddi… | [`ch08/make_fig8_5.py`](figure-scripts/ch08/make_fig8_5.py) |
| 8.6 | What cleaning the audio cost, on Arabic. Four published word error rates for one fine-tuned model on the Saudi broadcast corpus, with the differences between… | [`ch08/make_fig8_6.py`](figure-scripts/ch08/make_fig8_6.py) |
| 8.7 | Spoken document retrieval, in two phases that run on different schedules. The upper row is indexing: the archive is passed once through a recognizer or a pho… | [`ch08/make_fig8_7.py`](figure-scripts/ch08/make_fig8_7.py) |
| 8.8 | Macro-averaged F1 computed from a confusion matrix, on illustrative counts for four Arabic varieties. Rows are true labels and columns are predicted labels.… | [`ch08/make_fig8_8.py`](figure-scripts/ch08/make_fig8_8.py) |

## الفصل 9

| الشكل | الوصف | المصدر |
|---|---|---|
| 9.1 | The text-to-speech pipeline. The front end normalizes text and produces phonemes; the acoustic model turns phonemes into a mel spectrogram; the vocoder turns… | [`ch09/make_fig9_1.py`](figure-scripts/ch09/make_fig9_1.py) |
| 9.2 | The Arabic front end. The undiacritized form علم has several readings; diacritization selects one, and grapheme-to-phoneme conversion turns it into phonemes. | [`ch09/make_fig9_2.py`](figure-scripts/ch09/make_fig9_2.py) |
| 9.3 | Two neural acoustic models on one skeleton, so that what separates them shows up as a difference in shape. Both take phonemes through an encoder, a middle st… | [`ch09/make_fig9_3.py`](figure-scripts/ch09/make_fig9_3.py) |
| 9.4 | Three ways of getting from a written form to a waveform, drawn on one skeleton so that the difference between them is a difference in shape. Read each row fr… | [`ch09/make_fig9_4.py`](figure-scripts/ch09/make_fig9_4.py) |
| 9.5 | Evaluating synthesis. Listeners rate naturalness on the MOS scale; an automatic recognizer provides an objective intelligibility cross-check via WER. | [`ch09/make_fig9_5.py`](figure-scripts/ch09/make_fig9_5.py) |

## الفصل 10

| الشكل | الوصف | المصدر |
|---|---|---|
| 10.1 | Two speech-translation architectures on one skeleton, so that what separates them shows up as a difference in shape. Both rows begin on the same Arabic audio… | [`ch10/make_fig10_1.py`](figure-scripts/ch10/make_fig10_1.py) |
| 10.2 | What the transcript costs, on one Gulf sentence. أبغى is the Gulf and Najdi word for ‘I want’, and a recognizer trained mostly on Modern Standard Arabic (MSA… | [`ch10/make_fig10_2.py`](figure-scripts/ch10/make_fig10_2.py) |
| 10.3 | A wait-k policy with k = 3, drawn on a time axis rather than a step axis. Source words arrive along the top, one every 0.6 seconds; target words are emitted… | [`ch10/make_fig10_3.py`](figure-scripts/ch10/make_fig10_3.py) |
| 10.4 | What a word-level metric does to a correct Arabic translation. The two sentences mean the same thing and both are correct Arabic; they differ in two places,… | [`ch10/make_fig10_4.py`](figure-scripts/ch10/make_fig10_4.py) |
| 10.5 | The three understanding tasks across two turns of one conversation. The first turn is the sentence this chapter opened on: it carries an intent and two slots… | [`ch10/make_fig10_5.py`](figure-scripts/ch10/make_fig10_5.py) |
| 10.6 | The spoken dialogue loop, with the two stages Arabic changes marked in orange. Speech is recognized, understood as an intent and its slots, tracked as dialog… | [`ch10/make_fig10_6.py`](figure-scripts/ch10/make_fig10_6.py) |

## الفصل 11

| الشكل | الوصف | المصدر |
|---|---|---|
| 11.1 | Every architecture this book has built, and the one this chapter builds. The upper band holds one row per task, each a fixed path from one kind of input, thr… | [`ch11/make_fig11_1.py`](figure-scripts/ch11/make_fig11_1.py) |
| 11.2 | What one Arabic recording becomes on its way to the language model, counted at every stage. The top row is the thirty-second window Whisper is built around;… | [`ch11/make_fig11_2.py`](figure-scripts/ch11/make_fig11_2.py) |
| 11.3 | The three parts, their sizes, and what flows between them: encode the audio, shorten and project what comes out, then generate text. The encoder takes a spec… | [`ch11/make_fig11_3.py`](figure-scripts/ch11/make_fig11_3.py) |
| 11.4 | One instruction-tuning example, and why the format teaches a model to route. A single audio clip branches to three instructions and three different targets.… | [`ch11/make_fig11_4.py`](figure-scripts/ch11/make_fig11_4.py) |
| 11.5 | Speech in and speech out, with a language model in the middle. The row of units drawn beneath the pipeline is the reason the middle box can be a language mod… | [`ch11/make_fig11_5.py`](figure-scripts/ch11/make_fig11_5.py) |
| 11.6 | The speech agent loop. Four stages run clockwise and the loop closes on the next turn. The two marked in orange and green are what separate an agent from a c… | [`ch11/make_fig11_6.py`](figure-scripts/ch11/make_fig11_6.py) |

## الفصل 12

| الشكل | الوصف | المصدر |
|---|---|---|
| 12.1 | The computer-assisted pronunciation training pipeline. The learner reads a text the system already has, which is what makes everything after it possible: wit… | [`ch12/make_fig12_1.py`](figure-scripts/ch12/make_fig12_1.py) |
| 12.2 | Goodness of Pronunciation read off a forced alignment. Each aligned segment gets one bar for how well the audio matches the phone the learner was supposed to… | [`ch12/make_fig12_2.py`](figure-scripts/ch12/make_fig12_2.py) |
| 12.3 | A healthcare voice interface, drawn around the part that decides whether it is safe. The pipeline across the middle is short and ordinary, and it is not the… | [`ch12/make_fig12_3.py`](figure-scripts/ch12/make_fig12_3.py) |

## الفصل 13

| الشكل | الوصف | المصدر |
|---|---|---|
| 13.1 | A threat-and-harm model for an Arabic speech system, drawn in columns rather than as two lists. A threat sits above the system and the safeguard that answers… | [`ch13/make_fig13_1.py`](figure-scripts/ch13/make_fig13_1.py) |
| 13.2 | Voice anonymization, with the measurement attached. The pipeline across the top separates what was said from who said it and puts a different identity back,… | [`ch13/make_fig13_2.py`](figure-scripts/ch13/make_fig13_2.py) |
| 13.3 | Audio watermarking, embedded once and detected later. The top row is what the generator does at the moment the audio is made, which is the only moment the ma… | [`ch13/make_fig13_3.py`](figure-scripts/ch13/make_fig13_3.py) |
| 13.4 | What an average hides. Eight illustrative word error rates, four dialects by two genders, with the pooled average drawn across them as a single line. Every b… | [`ch13/make_fig13_4.py`](figure-scripts/ch13/make_fig13_4.py) |
| 13.5 | A published set of responsible AI principles, with the sections of this chapter that answer each one. The six are Microsoft’s published principles, taken her… | [`ch13/make_fig13_5.py`](figure-scripts/ch13/make_fig13_5.py) |

## الفصل 14

| الشكل | الوصف | المصدر |
|---|---|---|
| 14.1 | The project lifecycle, and the conditions it runs under. Eight stages, read left to right along the top row and then along the bottom: the specification deci… | [`ch14/make_fig14_1.py`](figure-scripts/ch14/make_fig14_1.py) |
| 14.2 | The annotation workflow, with the loop that closes it. Raw audio and the written guideline feed an optional first pass from a recognizer, drawn dashed becaus… | [`ch14/make_fig14_2.py`](figure-scripts/ch14/make_fig14_2.py) |
