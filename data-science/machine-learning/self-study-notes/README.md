# Machine Learning — Complete Self-Study Notes

Self-study notes covering **23 machine learning algorithms** across four units,
organised by the kind of supervision signal each one learns from.

**Read them here → [index.html](index.html)**

## Structure

Three levels — a hub, four unit pages, nine topic pages. No build step; every
page is hand-authored HTML.

```
index.html                       Course hub
├── unit1.html                   Supervised Learning
│   ├── unit1-classification.html      Naive Bayes · Logistic Regression · KNN · SVM · Decision Tree
│   └── unit1-regression.html          Linear · Polynomial · Ridge · Lasso · Random Forest
├── unit2.html                   Unsupervised Learning
│   ├── unit2-clustering.html          K-Means · DBSCAN · Hierarchical
│   ├── unit2-association-rules.html   Apriori · FP-Growth
│   └── unit2-anomaly-detection.html   Isolation Forest
├── unit3.html                   Semi-Supervised Learning
│   ├── unit3-inductive.html           Self-Training · Co-Training
│   └── unit3-transductive.html        Label Propagation
├── unit4.html                   Reinforcement Learning
│   ├── unit4-model-free.html          Q-Learning · REINFORCE
│   └── unit4-model-based.html         Dyna-Q · Value Iteration
└── syllabus.html                Scope, prerequisites, and what is not covered
```

## What each algorithm gives you

| Part | What it is for |
|---|---|
| **Definition** | What the method is, in one paragraph |
| **Mathematical foundation** | The objective, the update rule, the derivation — MathJax |
| **How it works** | The intuition, the hyperparameters that matter, the named variants |
| **Assumptions & failure modes** | What it takes for granted, and when it breaks |
| **Worked examples** | Three domains — finance, agriculture, medicine — for every algorithm |
| **Code** | Runnable Python *and* R, in switchable tabs |

Each topic page closes with an **At a Glance** table putting its algorithms side
by side on assumptions and failure modes — the comparison that actually decides
which method to reach for.

## Running the code

Every Python pane is self-contained and simulates its own data — nothing to download.

```bash
pip install numpy pandas scikit-learn mlxtend
```

All 23 Python panes are verified to run end to end against numpy 2.4, pandas 2.x
and scikit-learn 1.9. The R panes use `e1071`, `caret`, `class`, `rpart`,
`randomForest`, `glmnet`, `cluster`, `dbscan` and `arules`, depending on the
algorithm.

## A note on the example figures

The worked examples describe realistic settings, but the code **simulates** its
data, so any accuracy a pane prints is a property of that simulation, not a
published result. Where an example uses a real public dataset — Wisconsin
Diagnostic Breast Cancer, Pima Indians Diabetes — it is named so the figure can
be reproduced.

## Repository layout

```
index.html · unit*.html · syllabus.html   the notes
css/styles.css                            shared stylesheet
js/notes.js                               code tabs and copy button
scripts/check_notes.py                    structural validator
CLAUDE.md                                 authoring guide — read before editing
AUDIT_REPORT.md                           conceptual audit: findings and plan
CHANGELOG.md                              what changed, and when
ml_self_study_notes.html                  redirect stub for old links
```

## Contributing

Read `CLAUDE.md` first — it sets out the six-part algorithm template, the math
and escaping conventions, and what to update when adding an algorithm. Then:

```bash
python scripts/check_notes.py
```

CI additionally validates the HTML, executes every Python pane, and checks links.

## Licence

Not yet chosen — please open an issue if you would like to reuse this material.
