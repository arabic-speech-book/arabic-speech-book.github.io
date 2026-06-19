# الأدوات والنماذج

نماذج وأدوات ومكتبات مفتوحة المصدر لبناء أنظمة الكلام العربي — مصنّفة حسب الغرض.

## النماذج الأساسية والمدرَّبة مسبقًا

| الأداة | الوظيفة | عربية؟ | الرابط |
|--------|---------|--------|--------|
| **Whisper** (OpenAI) | تعرّف وترجمة متعدّدة اللغات | نعم (تشمل العربية) | [github](https://github.com/openai/whisper) · [HF](https://hf.co/openai/whisper-large-v3) |
| **wav2vec 2.0 / XLS-R** | تمثيلات كلام ذاتية الإشراف | متعدّدة اللغات | [HF: facebook/wav2vec2-xls-r](https://hf.co/facebook/wav2vec2-xls-r-300m) |
| **MMS** (Meta) | تعرّف وتخليق لأكثر من 1000 لغة | نعم | [HF: facebook/mms-1b-all](https://hf.co/facebook/mms-1b-all) |
| **ArTST** | محوّل النص والكلام العربي (تعرّف/تخليق/لهجات) | عربية أولًا | [github: mbzuai-nlp/ArTST](https://github.com/mbzuai-nlp/ArTST) |
| **SeamlessM4T** (Meta) | ترجمة الكلام والتعرّف | نعم | [HF: facebook/seamless-m4t-v2-large](https://hf.co/facebook/seamless-m4t-v2-large) |

## أدوات الكلام (التدريب والمسارات)

| الأداة | القوّة | الرابط |
|--------|--------|--------|
| **Hugging Face Transformers** | أسهل طريق لضبط Whisper وwav2vec2 | [docs](https://huggingface.co/docs/transformers) |
| **SpeechBrain** | أداة كلام شاملة على PyTorch | [speechbrain.github.io](https://speechbrain.github.io/) |
| **ESPnet** | أداة بحثية شاملة للتعرّف والتخليق والترجمة | [github](https://github.com/espnet/espnet) |
| **NVIDIA NeMo** | تعرّف وتخليق ونماذج لغوية بمستوى إنتاجي | [github](https://github.com/NVIDIA/NeMo) |
| **Kaldi** | تعرّف كلاسيكي HMM/DNN (أساس قوي) | [kaldi-asr.org](https://kaldi-asr.org/) |

## تخليق الكلام

| الأداة | القوّة | الرابط |
|--------|--------|--------|
| **Coqui TTS** | تخليق مفتوح متعدّد البِنى (VITS وXTTS) | [github](https://github.com/coqui-ai/TTS) |
| **Piper** | تخليق عصبي محلّي سريع | [github](https://github.com/rhasspy/piper) |

## معالجة اللغة العربية والأدوات اللسانية

| الأداة | الوظيفة | الرابط |
|--------|---------|--------|
| **CAMeL Tools** | الصرف العربي، تمييز اللهجات، التشكيل، التطبيع | [github](https://github.com/CAMeL-Lab/camel_tools) |
| **PyArabic** | أدوات نصّ عربي (التشكيل والتطبيع) | [github](https://github.com/linuxscout/pyarabic) |
| **Farasa** | التقطيع ووسم الأقسام والتشكيل | [farasa.qcri.org](https://farasa.qcri.org/) |
| **Mishkal** | تشكيل النص العربي | [github](https://github.com/linuxscout/mishkal) |

## معالجة الصوت والإشارة

| الأداة | الوظيفة | الرابط |
|--------|---------|--------|
| **librosa** | تحليل الصوت والسمات والأطياف | [librosa.org](https://librosa.org/) |
| **torchaudio** | إدخال/إخراج الصوت والتحويلات والنماذج | [docs](https://pytorch.org/audio/) |
| **pydub / FFmpeg** | تحويل الصيغ والتحرير الأساسي | [ffmpeg.org](https://ffmpeg.org/) |

## التقييم

| الأداة | المقياس | الرابط |
|--------|---------|--------|
| **jiwer** | WER / CER للتعرّف | [github](https://github.com/jitsi/jiwer) |
| **🤗 Evaluate** | WER وCER وBLEU وغيرها | [docs](https://huggingface.co/docs/evaluate) |

!!! tip "تقييم خاص بالعربية"
    في تعرّف الكلام العربي، أبلغ عن **CER** إلى جانب WER، وفكّر في تطبيع الحركات والاختلافات الإملائية (أ/إ/آ ← ا، ة/ه، ى/ي) قبل القياس. يغطّي فصل التقييم في الكتاب و[الدفتر ch04](notebooks/ch04_arabic_asr_foundations.ipynb) هذا بالتفصيل.
