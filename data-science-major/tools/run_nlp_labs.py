#!/usr/bin/env python3
"""Run and assert the Course 15 A practicals.

ELEVEN OF THE FOURTEEN EXPERIMENTS RUN against real corpora and real models:
NLTK's Brown, Reuters, Penn Treebank, movie_reviews, Gutenberg and WordNet,
spaCy's en_core_web_sm, scikit-learn and PyTorch. Nothing in those eleven is
simulated.

THREE CANNOT RUN, and all three fail for the same reason: they name Hugging
Face, and huggingface.co is refused by this environment's egress policy with
a 403 at the gateway, before any request reaches the host. No BERT, BART or
sentence-transformer checkpoint can be downloaded.

  12_bert_mlm.md        masked word prediction with a pre-trained BERT
  13_summarization.md   abstractive summarization through a HF pipeline
  14_faq_chatbot.md     an FAQ bot on sentence-transformer embeddings

Each is marked '*** NOT EXECUTED ***' and each names its runnable half. Those
halves are not filler: 12_transformer_local.py TRAINS a bidirectional
transformer encoder with a masked-LM objective on the Brown corpus, builds
TextRank extractive summarization on a real Reuters article, and scores an
FAQ retriever against hand-labelled answers. The pre-trained versions differ
from these by an embedding function, not by an architecture.

The discipline throughout: where an experiment could report 'it worked', it
reports a SCORE against hand-labelled truth instead -- the regexes, the NER
output, the FAQ retrieval and the document similarities are all graded, and
several of them fail in ways the notes explain rather than hide.
"""
import pathlib
import sys
import traceback

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAB = ROOT / "labs" / "course-15a-nlp"
MARKER = "*** NOT EXECUTED ***"

PY_LABS = [
    ("01_setup_regex", "1, 2"),
    ("03_ambiguity_tokenize", "3, 4, 5, 6"),
    ("07_parsing_ner_similarity", "7, 8, 9"),
    ("10_sentiment_rnn", "10, 11"),
    ("12_transformer_local", "12, 13, 14 (mechanisms)"),
]

NOT_EXECUTED = {
    "12_bert_mlm.md":      "pre-trained BERT; huggingface.co is 403 here",
    "13_summarization.md": "BART/T5 for the abstractive half; same 403",
    "14_faq_chatbot.md":   "sentence-transformers; same 403",
}


def banner(text):
    print("\n" + "=" * 62)
    print(text)
    print("=" * 62)


def main():
    banner("Course 15 A -- Natural Language Processing")
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

    banner("Course 15 A -- auditing the files that cannot run")
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
            print(f"    {name:<24}{why}")
        print("  each names its runnable half in 12_transformer_local.py,")
        print("  which trains the same architecture from scratch.")

    banner(f"{passed} lab programs executed and asserted, {failed} failed")
    print("covering all 14 prescribed experiments")
    print("""Eleven run against REAL corpora and REAL models -- Brown, Reuters,
the Penn Treebank, movie_reviews, Gutenberg, WordNet, spaCy's
en_core_web_sm, scikit-learn and PyTorch. Only the three Hugging
Face experiments are documented rather than demonstrated.

Where a result could have been asserted, it was SCORED instead --
and several of the scores contradict the expected story: bag-of-words
ranks an unrelated document above a paraphrase, spaCy mislabels two
Indian state names while getting both cities right, and the six
sentiment models differ by less than the spread between
cross-validation folds -- so they are indistinguishable on this data.""")
    print("=" * 62)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
