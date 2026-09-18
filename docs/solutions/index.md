# Arabic Speech Technologies: Exercise Solutions

Companion-website solutions for the end-of-chapter exercises of *Arabic Speech Technologies*. Every exercise and subpart in the book's exercise list (Chapters 1 to 11; Chapters 12 to 14 have no exercises) is answered in the chapter's Markdown file, with the original numbering. Every exercise that involves code or computational analysis has one self-contained Google Colab notebook covering all of its coding subparts. Open-ended answers are marked **Suggested solution**; numbers quoted in the solution files were produced by running the notebooks, with the exact models and settings stated.

## How to use the notebooks

Download a notebook and open it in Google Colab (File > Upload notebook). Each notebook begins with the exercise text, installs its own dependencies, downloads or lets you upload the data it needs, and ends with the plots or metrics the exercise asks for. All notebooks run on Colab's free CPU tier; the header of each says when a free T4 GPU is recommended (Whisper transcription of more than a few minutes of audio, or a larger LLM). The notebooks ship with the outputs of a test run so that the expected result is visible before you run anything.

## Data used by the notebooks

The book's companion clips (Chapter 1) and minimal-pair clips (Chapter 3) were not part of the material supplied for these solutions; the affected notebooks use openly licensed stand-ins and accept uploads, and the solution files say so. Openly available sources used: FLEURS Arabic (`google/fleurs`, CC BY 4.0), Speech-MASSIVE Arabic (`FBK-MT/Speech-MASSIVE`, CC BY-NC-SA 4.0), a community-redistributed SADA2022 subset (`SarahUssama/sada-arabic-test-dataset-sample`; verify its licence, SADA itself is CC BY-NC-SA 4.0 via Kaggle), CAMeL Tools with the CALIMA-MSA r13 database, Mishkal, SentencePiece, `facebook/mms-tts-ara` and Whisper checkpoints from the Hugging Face Hub. Illustrative or synthetic data are labelled as such inside each notebook.

## Chapter files

| Chapter | Solutions | Notebooks (one per coding exercise) |
|---|---|---|
| 1. Speech Technologies and the Arabic Challenge | [Chapter_01_Solutions.md](Chapter_01_Solutions.md) | [Ex 2: WER by hand and on real clips](Chapter_01_Exercise_02.ipynb) · [Ex 4: CAMeL Tools analyses of علم](Chapter_01_Exercise_04.ipynb) |
| 2. Arabic Language and Speech Fundamentals | [Chapter_02_Solutions.md](Chapter_02_Solutions.md) | (no coding exercises) |
| 3. Digital Speech Processing | [Chapter_03_Solutions.md](Chapter_03_Solutions.md) | [Ex 1: aliasing](Chapter_03_Exercise_01.ipynb) · [Ex 2: F2 and emphasis](Chapter_03_Exercise_02.ipynb) · [Ex 3: log-mel and MFCC pipeline](Chapter_03_Exercise_03.ipynb) |
| 4. Arabic ASR I | [Chapter_04_Solutions.md](Chapter_04_Solutions.md) | [Ex 2: normalization and WER](Chapter_04_Exercise_02.ipynb) · [Ex 5: clitic segmentation](Chapter_04_Exercise_05.ipynb) |
| 5. Arabic ASR II | [Chapter_05_Solutions.md](Chapter_05_Solutions.md) | [Ex 1: CTC paths](Chapter_05_Exercise_01.ipynb) · [Ex 5: subword vs morphological tokens](Chapter_05_Exercise_05.ipynb) |
| 6. Speech Foundation Models | [Chapter_06_Solutions.md](Chapter_06_Solutions.md) | [Ex 2: LoRA parameter count](Chapter_06_Exercise_02.ipynb) · [Ex 5: per-dialect error audit](Chapter_06_Exercise_05.ipynb) |
| 7. Corpora, Annotation, and Benchmarks | [Chapter_07_Solutions.md](Chapter_07_Solutions.md) | [Ex 3: inter-annotator agreement](Chapter_07_Exercise_03.ipynb) · [Ex 4: corpus bias audit](Chapter_07_Exercise_04.ipynb) |
| 8. Dialect Identification and Spoken Language Processing | [Chapter_08_Solutions.md](Chapter_08_Solutions.md) | [Ex 2: macro-F1 from a confusion matrix](Chapter_08_Exercise_02.ipynb) |
| 9. Speech Synthesis | [Chapter_09_Solutions.md](Chapter_09_Solutions.md) | [Ex 2: two diacritizers and a G2P](Chapter_09_Exercise_02.ipynb) · [Ex 4: MUSHRA-like evaluation lab](Chapter_09_Exercise_04.ipynb) |
| 10. Speech Translation and SLU | [Chapter_10_Solutions.md](Chapter_10_Solutions.md) | [Ex 2: wait-k and Average Lagging](Chapter_10_Exercise_02.ipynb) · [Ex 3: intent and slot annotation](Chapter_10_Exercise_03.ipynb) · [Ex 4: cascaded SLU with an LLM](Chapter_10_Exercise_04.ipynb) |
| 11. Audio-Language Models and Speech Agents | [Chapter_11_Solutions.md](Chapter_11_Solutions.md) | [Ex 2: keyword task router](Chapter_11_Exercise_02.ipynb) |
| 12. Examples of Arabic Speech Applications | no exercises in the book | |
| 13. Responsible Arabic Speech Technology | no exercises in the book | |
| 14. End-to-End Arabic Speech Projects | no exercises in the book | |

## Coverage

57 exercises across Chapters 1 to 11, all solved with their subparts; 20 notebooks, one per exercise that involves coding or computational analysis. A script (`check_coverage.py`, in the build materials) verified that every numbered exercise has a section in its chapter file and that every linked notebook exists.

## Testing status

Every notebook was executed end to end in a CPU-only Linux environment (Python 3.11) before release, with the exceptions listed here and repeated inside the notebooks concerned: Chapter 3 Exercise 2's real-audio path (needs corpus tokens that require registration; the synthetic path was executed); Chapter 4 Exercise 5's optional Stanza cell (executed separately, output quoted); Chapter 7 Exercise 4's official-SADA path (needs a Kaggle login; the two open paths were executed); and the interactive Label Studio steps of Chapters 6, 9 and 10 (the export files were generated and follow Label Studio's formats, but the application itself was not run). No experimental result in these files is invented: every quoted number comes from a test run, a cited paper, or the book.

## Flags for the editors

* Missing resources: companion clips (Ch. 1 Ex. 2), minimal-pair clips (Ch. 3 Ex. 2), companion G2P notebook (Ch. 9 Ex. 2). Stand-ins are used and labelled.
* Access-restricted corpora named in the exercises (SADA via Kaggle, MASC via IEEE DataPort, TARIC-SLU via the authors' form, Common Voice via Hugging Face login) are replaced by open equivalents in the notebooks, with the substitution stated and a code path or instructions for the original.
* No openly licensed dialectal Arabic TTS voice with documented provenance could be verified for Chapter 9 Exercise 4; the dialect stimuli are dialect text read by an MSA voice and are reported as that condition.
