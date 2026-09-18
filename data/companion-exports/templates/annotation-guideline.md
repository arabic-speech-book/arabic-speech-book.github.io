# Annotation guideline

*Appendix 14.B of* **Introduction to Arabic Speech Technologies** *by Hend S. Al-Khalifa. Copy it, fill it in, and publish it with your data.*

## Decisions to fix before annotation

- Transcription convention (for example Conventional Orthography for Dialectal Arabic) and one agreed spelling per dialectal word.
- **Diacritization:** written, partial, or none, and when.
- Markup for noise, music, overlap, and unintelligible speech.
- Utterance segmentation rule and maximum clip length.
- **Metadata fields:** speaker identifier, gender, sub-dialect, device, distance, sampling rate.
- **Quality control:** sample size for double transcription, the agreement measure, and the adjudication rule.

## Example: the case study’s annotation guideline, decided

- The same checklist as above, with every decision made rather than listed. The value of writing it this way is that an annotator can act on it.
- **Transcription convention:** Conventional Orthography for Dialectal Arabic. One spelling per spoken word, taken from the project word list; if a word is not on the list, the annotator adds it once and the list is the authority afterwards. Write وين, never أين, when the speaker said the dialectal form.
- **Diacritization:** none, on any transcript. The command set is short and unambiguous without vowels, and diacritizing by hand would cost more than it buys here. State this with every error rate, because a system scored on undiacritized text is not answering the same question as one scored with the vowels in place.
- Noise, music, overlap and unintelligible speech: mark inline as [noise], [music], [overlap] and [unk]. A clip with more than two [unk] tokens is rejected rather than transcribed. Television speech in the background is [noise], not a second speaker.
- **Segmentation:** one command per clip, cut at the silence before and after, with 200 ms of padding kept on each side. Maximum clip length 6 seconds; anything longer is a collection error and is sent back.
- **Metadata per clip:** speaker identifier, gender, sub-dialect, device, microphone distance in metres, room identifier, background condition, sampling rate. The room identifier matters as much as the speaker one, because a split that separates speakers but not rooms still leaks.
- **Quality control:** 10 percent of every batch is transcribed independently by a second annotator. Agreement is Cohen’s kappa on the command label and character error rate on the free transcript. A batch below 0.85 kappa is not re-transcribed first; the disagreements are read, the guideline is amended, and only then is the batch redone.

