# الدفاتر البرمجية

الدفاتر المرافقة التي يشير إليها الكتاب — دفتر لكل فصل له دفتر. ينفّذ كل دفتر الحسابات التي يصفها الفصل بالكلمات، فيتمكّن القارئ من فحص الحساب الدقيق وتغييره. **يشير الكتاب إلى هنا، ولا مكان سواه، للمواد القابلة للتشغيل؛ ولا يظهر أي كود في الفصول نفسها.**

!!! success "يعمل من أوّله إلى آخره بـ numpy وscipy وmatplotlib فقط"
    لا حاجة إلى أي تنزيل ولا ملفّات صوتية: حيثما كان التسجيل مفيدًا **يُخلِّق** الدفتر واحدًا، مع خلية لقراءة ملفّ WAV خاصّ بك. والخلايا التي تحتاج حزمًا إضافية أو اتصالًا بالإنترنت مُعلَّمة بـ **Optional** ومُعلَّقة.

## الدفاتر

| الفصل | الدفتر | ماذا ينفّذ | في الكتاب |
|-------|--------|-----------|-----------|
| 1 | [معدّل خطأ الكلمة والحرف](ch01_wer_and_cer.ipynb) | محاذاة مسافة التحرير، WER وCER، مفاتيح التطبيع العربي، تفصيل لكل لهجة، مقارنة تمهيدية (bootstrap) | §1.7–1.8؛ تمرين 2 |
| 2 | [معجم النطق](ch02_pronunciation_lexicon.ipynb) | ربط الحرف/الحركة بالصوت، التشديد، لام التعريف قبل الحروف الشمسية والقمرية، التاء المربوطة وقفًا ووصلًا، معجم صغير يُكتب إلى ملف | §2.8 |
| 3 | [من الإشارة إلى السمات](ch03_signal_to_features.ipynb) | المعاينة والتكميم، التأطير والنوافذ، STFT وإعدادا طيف، مرشّح الميل، log-mel، DCT وMFCC مع المشتقّات، التنبؤ الخطّي (Levinson–Durbin) والصيغ، محاكاة نطاق الهاتف | §3.1، 3.5–3.8 |
| 4 | [التقديم وViterbi في HMM](ch04_hmm_forward_and_viterbi.ipynb) | نموذج HMM بحالتين وثلاث إطارات: خوارزمية التقديم، Viterbi، تعداد كل المسارات للتحقّق، المجال اللوغاريتمي، ونموذج يسار-يمين لكلمة بَاب | §4.3 |
| 6 | [أهداف التعلّم الذاتي الإشراف](ch06_self_supervised_objectives.ipynb) | إخفاء المقاطع، هدف InfoNCE التبايني، التكميم الجُدائي، التنبؤ المُقنَّع كتصنيف، السبر حسب الطبقات، عدّ معاملات المحوّلات وLoRA | §6.2–6.5 |
| 9 | [التشكيل وتحويل الحرف إلى صوت](ch09_diacritization_and_g2p.ipynb) | الصور غير المشكّلة وقراءاتها، تحويل الحرف إلى صوت، معدّل خطأ التشكيل بالحرف الأخير وبدونه، تقرير خلاف بين مُشكِّلَين، وخطّافات لـ CAMeL Tools أو Mishkal | §9.2؛ تمرين 2 |

أما الفصول 5 و7 و8 و10 و11 فلها تمارين برمجية محلولة في [حلول التمارين](../solutions/index.md) لا دفتر فصل مستقل؛ والفصول 12–14 لا هذه ولا تلك.

**▶ افتح في Google Colab:** [الفصل 1](https://colab.research.google.com/github/arabic-speech-book/arabic-speech-book.github.io/blob/main/docs/notebooks/ch01_wer_and_cer.ipynb) · [الفصل 2](https://colab.research.google.com/github/arabic-speech-book/arabic-speech-book.github.io/blob/main/docs/notebooks/ch02_pronunciation_lexicon.ipynb) · [الفصل 3](https://colab.research.google.com/github/arabic-speech-book/arabic-speech-book.github.io/blob/main/docs/notebooks/ch03_signal_to_features.ipynb) · [الفصل 4](https://colab.research.google.com/github/arabic-speech-book/arabic-speech-book.github.io/blob/main/docs/notebooks/ch04_hmm_forward_and_viterbi.ipynb) · [الفصل 6](https://colab.research.google.com/github/arabic-speech-book/arabic-speech-book.github.io/blob/main/docs/notebooks/ch06_self_supervised_objectives.ipynb) · [الفصل 9](https://colab.research.google.com/github/arabic-speech-book/arabic-speech-book.github.io/blob/main/docs/notebooks/ch09_diacritization_and_g2p.ipynb)

## تشغيلها

=== "محليًّا"

    ```bash
    pip install -r requirements.txt
    jupyter lab
    ```

    يحتاج [ملف المتطلّبات المثبّت](requirements.txt) إلى `numpy` و`scipy` و`matplotlib` فقط. أما الكتلة الاختيارية (datasets وsoundfile وCAMeL Tools وMishkal) فمُعلَّقة — أزِل التعليق عمّا تحتاجه خلية Optional.

=== "Google Colab"

    استخدم روابط **افتح في Google Colab** أعلاه لفتح أي دفتر مباشرةً في Colab (المستودع عامّ، فيستطيع Colab تحميلها). أو من صفحة الدفتر استخدم أيقونة **التنزيل** ثم اختر في Colab **File → Upload notebook**.

!!! note "البيانات"
    لا تُوزَّع أي مدوّنة هنا. تشير الخلايا الاختيارية إلى **Common Voice Arabic** (الفصل 3)، يُنزّلها القارئ برخصتها — وأبلِغ عن إصدارها وعدد ساعاتها المُتحقَّقة كما يطلب الفصل 7.

!!! info "تبحث عن المجموعة السابقة؟"
    مجموعة الاثني عشر دفترًا من مراجعة المخطوطة (يوليو/أغسطس) استُبدِلت؛ وهي محفوظة للرجوع في [المسودات السابقة](../notebooks-archive/index.md).
