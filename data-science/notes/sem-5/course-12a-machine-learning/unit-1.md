# Unit 1 — Introduction to Machine Learning

**Syllabus topics:** Introduction to machine learning — types of human
learning; what is machine learning?; types of machine learning — supervised,
unsupervised, semi-supervised and reinforcement learning; machine learning
activities; applications of machine learning. Types of data in machine
learning; structure of data.

---

## 1.1 Types of human learning

### 🎯 Why the syllabus starts here

**Machine learning is named after human learning, and the analogy is load
bearing** — each kind of machine learning is modelled on a kind of human
learning, and the mapping is a five-mark question.

| Human learning | How it works | Machine analogue |
|---|---|---|
| **Under expert guidance** | A teacher gives examples *and* the right answers | **Supervised learning** |
| **Guided by knowledge gained from experts** | The expert gave rules once; you apply them to new cases yourself | Supervised learning, then **generalisation** to unseen data |
| **Self-learning** | No teacher. You notice patterns, group things, form categories | **Unsupervised learning** |
| Learning by trial and error | Act, see the consequence, adjust | **Reinforcement learning** |

**A child shown twenty photographs labelled "cat" or "dog" is being supervised.
A child who sorts a box of buttons into piles nobody named is not.** That is
the whole distinction, and it is worth stating in exactly those terms.

---

## 1.2 What is machine learning?

### 🎯 The definition to write

**Mitchell's definition** is the one textbooks use and the one to quote:

> **A computer program is said to learn from experience E with respect to some
> class of tasks T and performance measure P, if its performance at tasks in T,
> as measured by P, improves with experience E.**
> — Tom Mitchell, 1997

Its value is that it forces you to name three things. For spam filtering:

| Symbol | Means | Here |
|---|---|---|
| **T** | The task | Classify an email as spam or not spam |
| **E** | The experience | A corpus of emails already labelled by users |
| **P** | The performance measure | Proportion correctly classified — or, better, precision and recall (Unit 2 §2.6) |

**If you cannot name T, E and P, you do not yet have a machine learning
problem.** That is a genuinely useful test, not just an exam formula.

### 🔢 Machine learning against traditional programming

This contrast is asked nearly every year, and a diagram answers it best.

```
TRADITIONAL PROGRAMMING              MACHINE LEARNING

   data ──┐                             data ──┐
          ├──► program ──► output               ├──► algorithm ──► MODEL
  rules ──┘                          answers ──┘                     │
                                                                     ▼
                                                    new data ──► prediction
```

| | **Traditional programming** | **Machine learning** |
|---|---|---|
| You write | The **rules** | The **objective**, and supply examples |
| The computer produces | The output | **The rules** (the model) |
| Input | Data + rules | Data + **answers** |
| Good for | Problems whose rules you can state | Problems whose rules you **cannot** state |
| Changes when data changes | You rewrite the code | You **retrain** |
| Debuggable by reading | Yes | **Not really** — hence interpretability, Unit 2 §2.4 |

### 💡 When *not* to use machine learning — worth a mark, and usually right

- **The rules are known and stable.** VAT is 18%. Write `price * 0.18`. A model
  would be slower, less accurate, and occasionally wrong.
- **You have very little data.** A model fitted to 40 rows is a guess wearing a
  confidence interval.
- **A mistake is catastrophic and unexplainable.** If you cannot say why the
  model refused the loan, you may not legally be allowed to refuse it.
- **A simple baseline already suffices.** Unit 2 §2.5 insists you measure the
  baseline first, precisely because it often wins.

---

## 1.3 The four types of machine learning

### 🔢 The comparison table

| | **Supervised** | **Unsupervised** | **Semi-supervised** | **Reinforcement** |
|---|---|---|---|---|
| Input | Features **+ labels** | Features **only** | A **few** labels, many without | State, and a **reward** signal |
| Goal | Predict the label | Find structure | Use unlabelled data to improve a supervised model | Learn a **policy** maximising long-run reward |
| Feedback | The correct answer, every time | **None** | Partial | **Delayed** reward, not the correct answer |
| Evaluated by | Accuracy, RMSE against held-out labels | **Hard** — no ground truth | As supervised | Cumulative reward |
| Tasks | Classification, regression | Clustering, dimensionality reduction, association | Classification with scarce labels | Control, sequential decisions |
| Examples | Spam filter, house prices | Customer segments, PCA | Medical images: 100 labelled, 50,000 not | Game playing, robotics, ad bidding |
| In this course | **Units 3 and 4** | **Unit 5** | Mentioned only | Mentioned only |

### 🎯 Supervised learning splits into two

| | **Classification** | **Regression** |
|---|---|---|
| Predicts | A **category** | A **number** |
| Output | Spam / not spam; setosa / versicolor / virginica | 75.3 marks; ₹42 lakh |
| Metrics | Accuracy, precision, recall, F1, AUC | RMSE, MAE, R² |
| Here | **Unit 4** | **Unit 3** |

**The trap:** predicting a **number that is really a category** — a rating of
1–5, a pin code — with regression. And its mirror: binning a genuine quantity
into "high/medium/low" and throwing away information you had. Ask what the
value *means*, not what type it is stored as.

### 💡 Semi-supervised learning, and why it exists

**Labels are expensive; data is cheap.** A radiologist labelling 50,000 scans
is the bottleneck, not the storage.

Semi-supervised methods use the unlabelled majority to learn the *shape* of the
data, then fit a supervised model on the few labels. **Self-training** is the
simplest: train on the labelled data, predict the unlabelled, add the
confident predictions as labels, repeat.

⚠️ **Its failure mode is worth knowing** — if the first model is biased, self
training amplifies the bias by feeding its own mistakes back as truth.

### 💡 Reinforcement learning — the distinction to get right

**RL is not supervised learning with delayed labels.** In supervised learning
you are told the correct answer. In RL you are told **how good the outcome
was**, never what you should have done.

```
   agent ──action──► environment
     ▲                    │
     └── state, reward ◄──┘
```

Key terms: **agent, environment, state, action, reward, policy**. The central
difficulty is the **exploration–exploitation trade-off** — take the known-good
action, or try something that might be better?

This is Course 13 A's territory too; if you are on Track A you will meet
agents and environments again in its Unit 1.

---

## 1.4 Machine learning activities — the pipeline

### 🎯 The big idea

**A machine learning project is a pipeline, and the modelling step is the
smallest part of it.**

```
 1. Problem      2. Data          3. Data          4. Feature
    definition ─►   collection ─►   preparation ─►   engineering
                                                          │
 7. Monitor  ◄── 6. Deployment ◄── 5. Model training ◄─────┘
    and retrain                       and evaluation
```

| Step | What happens | Share of the effort |
|---|---|---|
| 1. **Problem definition** | Name T, E and P. Decide what a useful answer looks like | Small, and decisive |
| 2. Data collection | Gather, and check you are allowed to use it | 10% |
| 3. **Data preparation** | Cleaning, missing values, outliers, encoding, scaling | **~60%** |
| 4. Feature engineering | Construct, transform, select | 15% |
| 5. Model training and evaluation | Fit, tune, compare against a baseline | 10% |
| 6. Deployment | Serve predictions where the decision is made | — |
| 7. **Monitor and retrain** | Watch for **drift**; the world changes | Continuous |

**Steps 3 and 4 are Unit 2**, and they are where the time goes. That is not a
complaint about the field; it is the field.

### ⚠️ Step 7 is the one that is always forgotten

A deployed model **decays**. Customer behaviour changes, a competitor launches,
a pandemic happens — and the relationship the model learned no longer holds.
This is **concept drift**, and the only defence is to keep measuring
performance in production and retrain.

**A model is not a deliverable; it is a running system.** Saying this earns a
mark and is the thing most students never mention.

---

## 1.5 Applications of machine learning

Learn a handful properly rather than listing twenty. The syllabus names four in
Unit 5's case studies, so know those in detail.

| Domain | Application | Type |
|---|---|---|
| **Email** | **Spam filtering** | Classification |
| **Vision** | **Image recognition**, face detection, OCR | Classification |
| **Speech** | **Speech recognition**, voice assistants | Sequence classification |
| **Finance** | **Online fraud detection**, credit scoring | Classification, **heavily imbalanced** |
| Retail | Recommendation, demand forecasting | Association, regression |
| Healthcare | Diagnosis from images, readmission risk | Classification |
| Manufacturing | Predictive maintenance | Classification / survival |
| Transport | Route optimisation, self-driving | RL, vision |
| Agriculture | Yield prediction, disease detection from leaf images | Regression, vision |
| Language | Translation, sentiment, summarisation | Sequence models |

### 💡 Two of these are examinable in detail

**Spam filtering** is the standard Naive Bayes application (Unit 4 §4.4), and
**fraud detection** is the standard *imbalanced data* application (Unit 2
§2.5). Fraud is perhaps 0.1% of transactions, so a model predicting "never
fraud" is **99.9% accurate and completely useless**. Know that example — it is
the cleanest argument for why accuracy is the wrong metric.

---

## 1.6 Types of data in machine learning

### 🔢 By measurement scale — Course 4's scales, reused

| Type | | Example | Operations | Encode as |
|---|---|---|---|---|
| **Qualitative** | **Nominal** | Colour, city, species | =, ≠ | **One-hot** |
| | **Ordinal** | Small/Medium/Large; a 1–5 rating | =, ≠, <, > | **Ordinal integers** |
| **Quantitative** | **Interval** | Temperature in °C, calendar dates | +, − (no meaningful ratio) | Numeric |
| | **Ratio** | Height, income, count — has a **true zero** | +, −, ×, ÷ | Numeric |

### ⚠️ The encoding mistake that this table prevents

**Label-encoding a nominal feature invents an order that is not there.**

Encoding `{Red: 0, Green: 1, Blue: 2}` tells a distance-based model that Red is
closer to Green than to Blue, and that Green is the *average* of Red and Blue.
Both are nonsense, and k-NN, SVM and linear models will act on them.

| Feature | Right encoding | Wrong encoding |
|---|---|---|
| Colour (nominal) | **One-hot** — three 0/1 columns | Label encode 0,1,2 |
| Size S/M/L (ordinal) | **Ordinal** 0,1,2 — the order is real | One-hot, which *discards* the order |
| Pin code (nominal, stored as a number) | Treat as **categorical** | Leave as a number — 500001 is not "less than" 560001 in any useful sense |

**Tree-based models are the exception** — they split on thresholds and are
largely indifferent to an arbitrary integer coding. Everything else is not.

### 🔢 By structure

| Structure | Description | Examples | Handling |
|---|---|---|---|
| **Structured** | Rows and columns, fixed schema | A sales table, sensor readings | Direct — the whole of this course |
| **Semi-structured** | Tags or keys, no fixed schema | JSON, XML, logs | Flatten first — Course 9's `json_normalize` |
| **Unstructured** | No predefined model | Text, images, audio, video | Must be **vectorised** — bag of words, TF-IDF, embeddings |

**Roughly 80% of an organisation's data is unstructured**, and classical
machine learning needs it turned into a feature matrix first. Experiment 15 of
Course 8 did exactly that with TF-IDF.

---

## 1.7 Structure of data

### 🔢 The feature matrix — the shape everything assumes

```
        feature 1  feature 2  ...  feature p        target
row 1 [   x11        x12      ...    x1p     ]  [    y1    ]
row 2 [   x21        x22      ...    x2p     ]  [    y2    ]
  .                                                   .
row n [   xn1        xn2      ...    xnp     ]  [    yn    ]

        X : n x p  (a 2-D array)              y : n  (1-D)
```

| Term | Also called | Is |
|---|---|---|
| **Instance** | Sample, record, observation, row | One thing you are learning about |
| **Feature** | Attribute, variable, predictor, column | One measurement of it |
| **Target** | Label, class, response, dependent variable | What you are predicting |
| **n** | — | Number of instances |
| **p** | — | Number of features |

### ⚠️ scikit-learn's shape rule, which causes half of all first-time errors

**`X` must be 2-D and `y` must be 1-D.** With a single feature you must still
give `X` two dimensions:

```python
X = df[["hours"]]          # 2-D -- CORRECT, note the double brackets
X = df["hours"]            # 1-D -- ValueError: Expected 2D array
X = df["hours"].values.reshape(-1, 1)    # the fix if you already have 1-D
```

The error message is `Expected 2D array, got 1D array instead`, and it is the
first error nearly everyone meets.

### 🔢 Describing the data before modelling

For a dataset of n instances and p features, know these terms:

| Quantity | Meaning | Matters because |
|---|---|---|
| **n / p ratio** | Instances per feature | **p > n** makes most models overfit badly; PCA (Unit 2 §2.10) is one answer |
| **Class balance** | Share of each target class | Decides whether accuracy means anything (§2.5) |
| **Dimensionality** | p | The **curse of dimensionality** — distance becomes meaningless as p grows, which breaks k-NN and clustering |
| **Sparsity** | Share of zero entries | Text data is 99%+ zeros; use sparse matrices or you run out of memory |
| **Missingness** | Share of nulls, and *whether it is random* | Missing-not-at-random is information; see §2.2 |

### 💡 The curse of dimensionality, in one sentence

**As the number of features grows, the volume of the space grows so fast that
your data becomes sparse in it, and every point becomes roughly equidistant
from every other.**

That destroys any method built on distance — k-NN, K-Means, DBSCAN — and it is
the reason dimensionality reduction is in Unit 2 rather than being an optional
extra.

---

## Practice problems

### Problem 1

Define machine learning. Distinguish it from traditional programming, and
explain when *not* to use it. *(10 marks)*

**Solution.**

Give **Mitchell's definition** verbatim, then unpack T, E and P on a concrete
example — spam filtering: T is classifying an email, E is a corpus already
labelled by users, P is the proportion correctly classified. Add that if you
cannot name all three, you do not yet have a machine learning problem.

Draw the contrast diagram: traditional programming takes **data + rules** and
produces output; machine learning takes **data + answers** and produces **the
rules**. Then the comparison table — what you write, what the computer produces,
what happens when the data changes, and whether you can debug it by reading it.

**Then the part most answers omit — when not to use it:**

- The rules are known and stable (VAT is 18%; write the multiplication).
- There is very little data.
- A mistake is catastrophic and must be explainable — you may be legally
  required to say why the loan was refused.
- A simple baseline already suffices, which is why Unit 2 insists you measure
  the baseline first.

### Problem 2

Compare supervised, unsupervised, semi-supervised and reinforcement learning.
*(10 marks)*

**Solution.**

Give the four-column table from §1.3 — input, goal, feedback, how it is
evaluated, typical tasks, and an example each.

Then make the three distinctions that carry the marks:

1. **Supervised vs unsupervised** is simply whether labels exist. A child shown
   photographs labelled cat or dog is supervised; a child sorting buttons into
   unnamed piles is not.
2. **Reinforcement is not supervised learning with delayed labels.** In
   supervised learning you are told the correct answer; in RL you are told only
   **how good the outcome was**, never what you should have done. Name the
   agent/environment/state/action/reward loop and the exploration–exploitation
   trade-off.
3. **Semi-supervised exists because labels are expensive and data is cheap** —
   a radiologist is the bottleneck, not the disk. Describe self-training, and
   note its failure mode: a biased first model amplifies its own bias by
   feeding its mistakes back as truth.

Close by mapping them onto the human learning types of §1.1 — that is what the
syllabus opens with, and few answers connect the two.

### Problem 3

Explain the types of data in machine learning and how each should be encoded.
*(10 marks)*

**Solution.**

**By measurement scale** — nominal, ordinal, interval, ratio — with the
permitted operations and an example each. Note that interval has no meaningful
ratio (20 °C is not twice as hot as 10 °C) while ratio has a true zero.

**Then the encoding rule, which is the examinable half:**

| Feature | Right | Wrong, and why |
|---|---|---|
| Colour (nominal) | **One-hot** | Label encoding 0,1,2 invents an order — it claims Green is the average of Red and Blue |
| Size S/M/L (ordinal) | **Ordinal** 0,1,2 | One-hot **discards** an order that is genuinely there |
| Pin code | Treat as **categorical** | It is stored as a number and is not one |

Add the exception: **tree models split on thresholds and are largely indifferent
to an arbitrary integer coding**; distance-based and linear models are not.

**By structure** — structured, semi-structured, unstructured — with the point
that roughly 80% of real data is unstructured and must be vectorised into a
feature matrix before any of this course's algorithms can touch it.

Finish with the **feature matrix shape**: `X` is n × p and 2-D, `y` is 1-D, and
a single feature still needs double brackets.

---

## Exam questions from this unit

**Two marks**

1. State Mitchell's definition of machine learning.
2. Give one difference between classification and regression.
3. What is semi-supervised learning?
4. Name the components of a reinforcement learning problem.
5. Give one example each of nominal and ordinal data.
6. What is the curse of dimensionality?
7. What shape does scikit-learn expect `X` to be?

**Five marks**

1. Compare machine learning with traditional programming.
2. Explain the types of human learning and their machine analogues.
3. Explain the machine learning pipeline.
4. Explain the types of data in machine learning.
5. Explain the structure of data — instances, features, target, n and p.
6. List five applications of machine learning with the type of each.

**Ten marks**

1. Define machine learning, distinguish it from traditional programming, and
   explain when not to use it.
2. Compare the four types of machine learning.
3. Explain the types of data and how each should be encoded.
4. Explain the machine learning pipeline and where most of the effort goes.

---

## Mistakes that cost marks

- **Defining machine learning as "computers learning like humans".** Give
  Mitchell's T, E and P.
- **Saying reinforcement learning has delayed labels.** It has **rewards**, and
  never the correct answer.
- **Listing applications with no type.** "ML is used in banking" earns nothing;
  "fraud detection — classification, heavily imbalanced" earns the mark.
- **Label-encoding a nominal feature.** It invents an order, and every
  distance-based model believes it.
- **One-hot encoding an ordinal feature.** It throws away real information.
- **Forgetting monitoring and retraining.** A model decays; concept drift is
  the reason.
- **Claiming the modelling step is the bulk of the work.** Data preparation is
  roughly 60% of it.
- **Passing a 1-D array as `X`.** Double brackets, or `reshape(-1, 1)`.
