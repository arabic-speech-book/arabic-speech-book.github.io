from nbbuild import md, code, save, PROVENANCE, PROVENANCE_CODE

cells = [
    md("""## What this notebook does

Adapt a pretrained multilingual speech encoder to Arabic two ways, full
fine-tuning and low-rank adaptation, and compare them on the four numbers that
decide which you can afford: word error rate, training time, trainable
parameters, and peak memory.

The notebook has two halves and you can run either.

- **The cost model** runs anywhere, in a second, with no downloads. It computes trainable parameters and optimizer memory for both methods from the architecture alone. Most of the difference between the two methods is arithmetic, and the arithmetic is worth seeing before you spend a GPU hour on it.
- **The real run** needs a GPU, a corpus and about an hour. It is written out in full and marked OPTIONAL.

Both halves end in the same place: a per-dialect table, because a pooled Arabic
WER from an adapted model is exactly the number this book keeps warning about."""),

    code("""NOTEBOOK = 'ch06_arabic_foundation_models.ipynb'

import numpy as np

try:
    import torch  # noqa: F401
    HAVE_TORCH = True
except ImportError:
    HAVE_TORCH = False

print('torch available, the OPTIONAL cells can run' if HAVE_TORCH else
      'no torch: the cost model below runs anyway, and it is the part with '
      'the lesson in it')"""),

    md("""## 1. The cost model

A transformer encoder layer has four projection matrices in its attention block
(query, key, value, output), each `d x d`, and a feed-forward block of two
matrices, `d x 4d` and `4d x d`.

Full fine-tuning trains all of them. LoRA freezes them and trains a pair of
small matrices beside each one: `d x r` and `r x d` for a rank `r` that is
typically 8 or 16. The saving is not subtle, and neither is what it does to the
optimizer state, which for Adam is two more numbers per trainable parameter."""),

    code("""def encoder_parameters(layers=24, d=1024, ffn_mult=4):
    attn = 4 * d * d
    ffn = 2 * ffn_mult * d * d
    return layers * (attn + ffn)


def lora_parameters(layers=24, d=1024, rank=16, targets=2):
    # targets: how many of the four attention matrices carry an adapter
    return layers * targets * 2 * d * rank


def report(name, trainable, total, bytes_per_param=4):
    weights = total * bytes_per_param
    grads = trainable * bytes_per_param
    adam = 2 * trainable * bytes_per_param
    gb = (weights + grads + adam) / 1e9
    print(f'{name:<22} trainable {trainable / 1e6:8.2f} M  '
          f'({100 * trainable / total:5.2f} % of {total / 1e6:.0f} M)   '
          f'optimizer footprint {gb:5.2f} GB')


TOTAL = encoder_parameters()
print('a 24-layer encoder with a model dimension of 1024:\\n')
report('full fine-tuning', TOTAL, TOTAL)
for rank in (4, 8, 16, 32):
    report(f'LoRA, rank {rank}', lora_parameters(rank=rank), TOTAL)
print('\\nThe frozen weights still have to be held in memory. What LoRA '
      'removes is the gradient and the optimizer state, which is three '
      'quarters of the bill.')"""),

    md("""### What that buys you in practice

The published pattern, which your own run should either confirm or contradict:
LoRA reaches within a point or so of full fine-tuning on the same data, trains
faster, and fits on a smaller card. When labelled Arabic is scarce it sometimes
does better than full fine-tuning, because there is not enough data to move
three hundred million parameters without overfitting.

Do not take that from this cell. It is a hypothesis to test, and the OPTIONAL
run below is how you test it. Fill the table with your own numbers."""),

    code("""RESULTS = {
    # method: (WER, hours to train, trainable millions, peak GB)
    'full fine-tuning': (None, None, TOTAL / 1e6, None),
    'LoRA rank 16': (None, None, lora_parameters(rank=16) / 1e6, None),
}
print(f'{"method":<20} {"WER":>8} {"hours":>7} {"trainable M":>12} '
      f'{"peak GB":>8}')
for method, (wer, hours, params, gb) in RESULTS.items():
    fmt = lambda v, s: (f'{v:{s}}' if v is not None else '   fill in')
    print(f'{method:<20} {fmt(wer, "8.1%")} {fmt(hours, "7.1f")} '
          f'{params:12.2f} {fmt(gb, "8.1f")}')"""),

    md("""## 2. OPTIONAL: the real run

Needs a GPU, a corpus and roughly an hour. Every choice below is one the
chapter's Reproducibility Note asks you to record, so record it as you go.

Pick a small multilingual encoder as the starting point. Freeze the feature
extractor, put a CTC head on top, and train. Then repeat with adapters instead
of full fine-tuning, changing nothing else, because a comparison in which two
things changed measures neither."""),

    code("""RUN_IT = False          # set True on a machine with a GPU

if RUN_IT and HAVE_TORCH:
    from transformers import (AutoProcessor, AutoModelForCTC,
                              TrainingArguments, Trainer)
    from datasets import load_dataset, Audio

    CHECKPOINT = 'facebook/wav2vec2-xls-r-300m'
    processor = AutoProcessor.from_pretrained(CHECKPOINT)
    model = AutoModelForCTC.from_pretrained(CHECKPOINT, ctc_loss_reduction='mean')
    model.freeze_feature_encoder()

    data = load_dataset('mozilla-foundation/common_voice_17_0', 'ar',
                        split='train[:2%]')
    data = data.cast_column('audio', Audio(sampling_rate=16000))

    args = TrainingArguments(output_dir='out-full', num_train_epochs=2,
                             per_device_train_batch_size=8, fp16=True,
                             learning_rate=3e-4, report_to=[])
    # Trainer(...).train()
    print('full fine-tuning configured')
else:
    print('skipped: this cell needs a GPU and a corpus')"""),

    code("""if RUN_IT and HAVE_TORCH:
    # the same run again, with adapters. Only the adaptation changes.
    from peft import LoraConfig, get_peft_model

    model = AutoModelForCTC.from_pretrained(CHECKPOINT,
                                            ctc_loss_reduction='mean')
    model.freeze_feature_encoder()
    model = get_peft_model(model, LoraConfig(
        r=16, lora_alpha=32, lora_dropout=0.05,
        target_modules=['q_proj', 'v_proj']))
    model.print_trainable_parameters()
else:
    print('skipped')"""),

    md("""## 3. The table that matters

Whatever the pooled number says, the chapter's argument is that an adapted
model has to be read per dialect. A model adapted on mostly Modern Standard
Arabic will post a respectable average and fail a dialect entirely, and the
average will not say so.

Fill in the rows from your own evaluation. The gap column is the one to look
at: it is the distance between the best-served variety and the worst."""),

    code("""PER_DIALECT = {
    # dialect: (hours in the adaptation set, WER full, WER LoRA)
    'MSA': (None, None, None),
    'Gulf': (None, None, None),
    'Egyptian': (None, None, None),
    'Levantine': (None, None, None),
    'Maghrebi': (None, None, None),
}
print(f'{"dialect":<12} {"hours":>7} {"WER full":>10} {"WER LoRA":>10}')
for d, (hours, full, lora) in PER_DIALECT.items():
    row = [f'{v}' if v is not None else 'fill in' for v in (hours, full, lora)]
    print(f'{d:<12} {row[0]:>7} {row[1]:>10} {row[2]:>10}')

print('\\nWhen the rows are filled: report the worst row beside the average, '
      'and report the hours, because a dialect with two hours in the '
      'adaptation set and a bad WER is a data result, not a model result.')"""),

    md(PROVENANCE),
    code(PROVENANCE_CODE),
]

save('ch06_arabic_foundation_models.ipynb', cells,
     'Notebook 6.1  Adapting a speech foundation model to Arabic',
     'Full fine-tuning against low-rank adaptation: what each costs, and what '
     'each is worth per dialect.')
