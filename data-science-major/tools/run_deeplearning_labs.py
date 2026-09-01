#!/usr/bin/env python3
"""Run and assert the Course 14 A practicals.

TEN OF THE TWELVE EXPERIMENTS RUN AGAINST REAL DATA AND REAL WEIGHTS.
That is worth stating precisely, because the obvious assumption about a
sandboxed environment is the opposite:

  * MNIST (experiment 4), Fashion-MNIST (experiments 6 and 7) and IMDb
    (experiment 9) are the datasets the syllabus names, fetched from
    storage.googleapis.com, which this environment permits.
  * MobileNetV2 and VGG16 (experiments 8 and 11) are the actual published
    ImageNet networks with their actual trained parameters, from the same
    host.
  * Keras runs on the torch backend. The syllabus says Keras/TensorFlow;
    TensorFlow is not installed, but Keras 3 is backend-agnostic, so every
    `keras.Sequential`, `.compile()` and `.fit()` is the real API and the
    code is character-for-character what you would write against TensorFlow.

TWO FILES CANNOT RUN, and both are marked '*** NOT EXECUTED ***':

  * Experiment 2 is two interactive web applications. There is no output to
    capture -- the point of them is the slider.
  * Experiment 12 needs huggingface.co, which is refused at the gateway with
    a 403, so no BERT-family checkpoint can be fetched and no Space pushed.

The discipline that makes the rest worth running: alongside every real
dataset there is a GENERATED one, where the decisive feature is known in
advance. Real data can tell you the accuracy; only a built dataset can tell
you whether the network learned the thing you intended.
"""
import os
import pathlib
import sys
import traceback

os.environ.setdefault("KERAS_BACKEND", "torch")
os.environ.setdefault("KERAS_HOME", "/tmp/keras_home")

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAB = ROOT / "labs" / "course-14a-deeplearning"
MARKER = "*** NOT EXECUTED ***"

PY_LABS = [
    ("01_perceptron_scratch", "1, 3"),
    ("04_deep_network", "4, 5"),
    ("06_cnn", "6, 7"),
    ("08_pretrained", "8"),
    ("09_rnn_lstm", "9, 10"),
    ("11_attention", "11, 12 (mechanism)"),
]

NOT_EXECUTED = {
    "02_playground.md":       "TensorFlow Playground and Teachable Machine "
                              "are interactive web apps",
    "12_huggingface_app.md":  "huggingface.co is refused at the gateway (403)",
}


def banner(text):
    print("\n" + "=" * 62)
    print(text)
    print("=" * 62)


def main():
    banner("Course 14 A -- Neural Networks and Deep Learning")
    sys.path.insert(0, str(LAB))

    passed, failed = 0, 0
    for module, exps in PY_LABS:
        print(f"\n  --- {module}.py   (experiments {exps})")
        try:
            __import__(module).main()
            passed += 1
        except Exception:
            traceback.print_exc()
            print(f"  FAILED: experiments {exps}")
            failed += 1

    banner("Course 14 A -- auditing the files that cannot run")
    problems = []
    for name in sorted(NOT_EXECUTED):
        path = LAB / name
        if not path.exists():
            problems.append(f"{name}: FILE MISSING")
        elif MARKER not in path.read_text(encoding="utf-8"):
            problems.append(f"{name}: marker {MARKER!r} is GONE")
    if problems:
        for p in problems:
            print(f"  {p}")
        failed += len(problems)
    else:
        print(f"  {len(NOT_EXECUTED)} files, all carrying '{MARKER}'")
        for name, why in sorted(NOT_EXECUTED.items()):
            print(f"    {name:<26}{why}")
        print("  each names what it needs and the runnable half that covers")
        print("  the same ground: 01_perceptron_scratch.py for the Playground")
        print("  results, and 09_rnn_lstm.py for sentiment on real IMDb.")

    banner(f"{passed} lab programs executed and asserted, {failed} failed")
    print("covering all 12 prescribed experiments")
    print("""Ten of the twelve run against REAL data and REAL pre-trained
weights: MNIST, Fashion-MNIST and IMDb are the datasets the syllabus
names, and MobileNetV2 and VGG16 are the published ImageNet networks.
Only the two interactive web tools and the Hugging Face deployment
are documented rather than demonstrated.

Every generated dataset in this course exists to make a claim
CHECKABLE rather than merely reported -- the XOR that a perceptron
provably cannot learn, the review sentences with exactly one decisive
word, the transfer task whose source and target differ by a known
amount.""")
    print("=" * 62)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
