# Tool reference

*Appendix 14.D of* **Introduction to Arabic Speech Technologies** *by Hend S. Al-Khalifa. Copy it, fill it in, and publish it with your data.*

Praat (praat.org) and ELAN (archive.mpi.nl/tla/elan) for time-aligned phonetic annotation; Label Studio (labelstud.io) for team transcription; the Montreal Forced Aligner (montreal-forced-aligner.readthedocs.io) for alignment; and the Kaldi (kaldi-asr.org), ESPnet (espnet.github.io/espnet), and SpeechBrain (speechbrain.github.io) toolkits for building recognizers and synthesizers.

## Example: the toolchain for the case study, stage by stage

- The same tools as above, placed at the stage that uses them and with the one setting that matters at each.
- **Recording:** any recorder that writes uncompressed audio. Set 16 kHz, 16-bit, one channel, and check the level on the loudest speaker before the session rather than after it.
- **Transcription at volume:** Label Studio, with the command list loaded as the label set. Test the right-to-left rendering and the diacritic input before the team starts, not after the first batch.
- **Time-aligned work:** Praat or ELAN, for the clips that need a phone-level look, and for the spot checks on the aligner.
- **Alignment:** the Montreal Forced Aligner, with a pronunciation dictionary covering the command set. Listen to twenty aligned clips before trusting the rest, because a dialectal word that the dictionary lacks aligns silently and wrongly.
- **Baseline and training:** a small classifier on log-mel features first, then ESPnet or a fine-tuned self-supervised model if the first is not enough. Record the toolkit version with the result: defaults change between releases and move the number.
- **Scoring:** one script, applied to the reference and the hypothesis alike, that prints the normalization it used above the number it produced.

Terminology

The terms this chapter uses without stopping to define them, and the abbreviations it introduces. Entries are alphabetical, so a term can be found without knowing which section introduced it.

## Term

- What it means in this chapter
- Annotation guideline
- the written document that fixes the transcription convention, the diacritization decision, the markup for noise and overlap, the segmentation rule and the metadata fields, before annotation begins. A guideline written first is what makes two annotators agree; a guideline written afterwards is an excuse, and what an agreement check produces is an amendment to it
- Command accuracy
- **the primary metric of the case study:** the proportion of spoken commands the system acts on correctly, measured on speakers it has never heard. It travels with a second metric, the false-accept rate on speech that is not a command, because a wrong action is worse than no action
- Conventional Orthography for Dialectal Arabic
- the spelling convention this chapter adopts so that two annotators write the same spoken dialectal word the same way. Dialectal Arabic has no standard spelling, so the convention is a project decision that has to be made before annotation rather than discovered during it
- Datasheet
- the one-page record of why a corpus was built, how it was collected and annotated, who the speakers are in aggregate, what the licence permits, what is known to be missing or biased, and how the splits are defined. It is often the most durable output of a project, since it lets a future team judge whether the corpus fits their purpose without downloading a single file
- False-accept rate
- how often a system acts on speech that was not addressed to it, measured on an out-of-set script recorded for the purpose. For a command system it matters more than accuracy, because the cost of a wrong action is higher than the cost of no action
- Forced alignment
- computing where each word and phone falls in the audio from a transcript the system already has, which produces time-aligned labels for hundreds of hours without hand-marking boundaries. Its quality depends on the dialect match and the transcript, so the output is spot-checked before it is treated as ground truth
- Inter-annotator agreement
- the measured agreement between two annotators transcribing the same sample independently, computed rather than assumed. Disagreements are adjudicated and folded back into the guideline, which is the loop that makes the corpus consistent
- Leak-free split
- a division into training, development and test sets in which no speaker appears in more than one part, and for read or command speech no prompt or recording session does either. Without it a model is rewarded for recognizing familiar voices and rooms, and the reported number collapses on real users
- Project specification
- the written statement, fixed before any modeling, of the task, the user and setting, the primary and secondary metrics, and the success criterion. It also decides the shape of the data, since every collection choice should follow from one of its four items rather than from convenience
- Recipe
- a condensed route through the project lifecycle for a project type that recurs: a goal, the ingredients, the steps in order, the pitfalls that most often sink it, and a checklist. A recipe changes the ingredients and the failure modes, never the lifecycle, so every recipe still begins with a specification and ends with a reproducibility record
- Reproducibility record
- the living file in the repository that ties any reported number to an exact corpus version, split, configuration, augmentation policy, random seed and scoring script. A result that cannot be reproduced from the repository is not yet a result, and the record is kept as the work happens rather than reconstructed at writing time
- SpecAugment
- the training-time augmentation that masks bands of frequency and spans of time in the input features. It is applied to the training set only, because augmenting the test set changes what the number means
- Text normalization
- the stated, scripted transformation applied to references and hypotheses before scoring, covering diacritics, Alef and Hamza forms, and punctuation. Two systems that normalize differently are not comparable, so the script travels with the number
- Word Error Rate
- the standard recognition metric, and a number that means nothing without the normalization script that produced it. This chapter asks for it per dialect and per condition rather than pooled, because a single average hides exactly the groups a project is most likely to be failing

## Abbreviation

- Spelled out
- ASR
- Automatic Speech Recognition
- CC0
- Creative Commons Zero, a public-domain dedication
- CER
- Character Error Rate
- ClArTTS
- Classical Arabic Text-to-Speech
- CMVN
- Cepstral Mean and Variance Normalization
- CODA
- Conventional Orthography for Dialectal Arabic
- ELAN
- EUDICO Linguistic Annotator, the annotation tool
- G2P
- Grapheme-to-Phoneme conversion
- LLM
- large language model
- MASC
- Massive Arabic Speech Corpus
- MGB
- Multi-Genre Broadcast
- MOS
- Mean Opinion Score
- MSA
- Modern Standard Arabic
- NADI
- Nuanced Arabic Dialect Identification
- QASR
- QCRI Aljazeera Speech Resource
- TTS
- Text-To-Speech
- WER
- Word Error Rate

