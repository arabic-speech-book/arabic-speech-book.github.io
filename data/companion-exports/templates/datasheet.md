# Corpus datasheet

*Appendix 14.A of* **Introduction to Arabic Speech Technology** *by Hend S. Al-Khalifa. Copy it, fill it in, and publish it with your data.*

## Datasheet fields

- **Motivation:** why the corpus was created, by whom, and for what task.
- **Composition:** hours, clips, speakers, dialects, channel, sampling rate.
- **Collection:** how the audio was recorded or harvested, and the consent obtained.
- **Annotation:** transcription convention, diacritization, tools, and quality control.
- **Licensing and use:** license, redistribution terms, and any no-identification restriction.
- **Splits:** train, development, and test definitions and the leakage policy.
- **Known limitations:** gaps, biases, and uneven dialect or gender coverage.

## Example: the datasheet for the case study, filled in

- The corpus below is the chapter’s worked example, not a released resource. Read it for the shape of the answers rather than for the numbers.
- **Name and version:** Gulf Command Speech, version 1.0, released 2026-03-01. A version is fixed at release and never edited in place.
- **Motivation:** built to train and evaluate a closed-vocabulary spoken-command recognizer for Gulf Arabic in a noisy far-field living room, because no existing corpus carries that command set in that channel. Built by the project team named in the contact field, funded internally.
- **Composition:** 6.4 hours of audio in 5,760 clips from 24 speakers, 12 women and 12 men, aged 19 to 61, all Gulf Arabic with sub-dialect recorded per speaker (14 Najdi, 7 Hijazi, 3 Eastern). 32 commands, each read 6 times per speaker, plus 1,150 out-of-set utterances for measuring false accepts. Recorded at 16 kHz, 16-bit, single channel.
- **Collection:** recorded in three living rooms on two devices, a laptop array and a phone, at 1, 2 and 4 metres, with the television or a fan running in half the sessions. Levels were set below clipping and checked per session. Speakers signed the consent form in Appendix 14.C before recording, and were paid a flat fee.
- **Annotation:** transcribed in the Conventional Orthography for Dialectal Arabic, undiacritized, in Label Studio, against the guideline in the example under Appendix 14.B. Ten percent of clips were transcribed twice; agreement was Cohen’s kappa 0.89 on the command label and character error rate 4.1 percent between annotators on the free transcript. Disagreements were adjudicated by a third annotator and the guideline was amended twice.
- **Licensing and use:** CC BY-NC 4.0. Redistribution of the audio is permitted with attribution for non-commercial research. Any attempt to identify an individual speaker is forbidden by the consent the speakers gave, and that restriction travels with the data.
- **Splits:** speaker-disjoint. 16 speakers train, 4 development, 4 test, with no speaker, room, or device combination shared between test and train. The split is fixed and published as a file of clip identifiers, with the seed recorded, so a later result is comparable with this one.
- **Known limitations:** no Yemeni or Omani speakers, so the corpus is not representative of the Gulf as a whole. Children are not represented. All sessions are indoor and none is on a telephone channel, so a model built on it should not be expected to transfer to 8 kHz call audio. The oldest speaker group is thin: three speakers over 55.
- **Contact:** the maintainer’s address, and the date the datasheet was last checked.

