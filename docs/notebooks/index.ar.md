# الدفاتر البرمجية

يأتي كل فصل مصحوبًا بدفتر Jupyter قابل للتشغيل. يمكنك قراءتها هنا على الموقع، أو تشغيلها محليًّا، أو فتحها في Google Colab.

## تشغيل الدفاتر

=== "محليًّا"

    ```bash
    git clone https://github.com/arabic-speech-book/arabic-speech-book.github.io.git
    cd arabic-speech-book.github.io
    pip install -r requirements.txt
    jupyter lab docs/notebooks
    ```

=== "Google Colab"

    افتح أي دفتر ثم استبدل `github.com` بـ `githubtocolab.com` في رابطه — وسيحمّله Colab مباشرةً. (نصيحة: أضِف شارة «Open in Colab» إلى كل دفتر بعد جعل المستودع عامًّا.)

## دفاتر الفصول

| # | الدفتر | الموضوع |
|---|--------|---------|
| 1 | [اللقاء الأول مع التعرّف العربي](ch01_first_contact_arabic_asr.ipynb) | تفريغ أول ملف صوتي عربي |
| 2 | [الصوتيات وتحويل الحرف إلى صوت](ch02_arabic_phonetics_g2p.ipynb) | تحويل الحرف إلى صوت للعربية |
| 3 | [السمات الصوتية](ch03_speech_features.ipynb) | الأطياف ومعاملات MFCC |
| 4 | [أسس التعرّف العربي](ch04_arabic_asr_foundations.ipynb) | النمذجة الصوتية واللغوية |
| 5 | [التعرّف الشامل](ch05_end_to_end_arabic_asr.ipynb) | مسارات CTC وseq2seq |
| 6 | [النماذج الأساسية العربية](ch06_arabic_foundation_models.ipynb) | Whisper وwav2vec 2.0 وArTST |
| 7 | [تحميل المدوّنات](ch07_corpus_loader.ipynb) | تحميل المدوّنات العربية وإعدادها |
| 8 | [واجهة التحسين](ch08_enhancement_frontend.ipynb) | إزالة الضوضاء وتحسين الكلام |
| 9 | [تمييز اللهجات](ch09_dialect_id.ipynb) | تمييز اللهجات العربية |
| 10 | [تمييز المتحدّث](ch10_speaker_id.ipynb) | التعرّف على المتحدّث |
| 11 | [تخليق الكلام العربي](ch11_arabic_tts.ipynb) | تحويل النص إلى كلام |
| 12 | [ترجمة الكلام وفهمه](ch12_speech_translation_slu.ipynb) | الترجمة والفهم |
| 13 | [النطق وكشف الأخطاء](ch13_pronunciation_mdd.ipynb) | كشف الأخطاء النطقية |
| 14 | [المشاعر السمعية البصرية](ch14_av_emotion.ipynb) | تمييز المشاعر متعدّد الوسائط |
| 15 | [توجيه نماذج الصوت الكبيرة](ch15_audio_llm_prompting.ipynb) | توجيه نماذج الصوت اللغوية |
| 16 | [المشروع الختامي](ch16_end_to_end_arabic_project.ipynb) | نظام كلام عربي متكامل |
| 17 | [العدالة والأمان والتدقيق](ch17_fairness_security_audit.ipynb) | النشر المسؤول |

!!! note "ملاحظة"
    تُعرَض الدفاتر للقراءة فقط على الموقع. استخدم أيقونة **التنزيل** أعلى صفحة كل دفتر للحصول على ملف `.ipynb`.
