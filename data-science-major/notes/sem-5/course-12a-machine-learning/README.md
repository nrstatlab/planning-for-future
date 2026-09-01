# Course 12 A — Machine Learning

**Semester V**

**This is a Track A course.** Semester V is Course 11 plus one elective pair:
**12 A + 13 A** (Machine Learning → Artificial Intelligence) or **12 B + 13 B**
(Big Data → Cloud Computing). Taking this means taking
Course 13 A too, and Track A again in
Semester VI.

---

## The one thing to understand before anything else

**Machine learning is not "the model". It is the pipeline, and the model is the
easy part.**

A student's first instinct is to reach for `RandomForestClassifier`. The
accuracy comes out at 0.94, and the exercise feels finished. It is not, because
the questions that decide whether that number means anything have not been
asked: what is the base rate? was the test set really held out? is 94% better
than always predicting the majority class?

| The part that feels like the work | The part that *is* the work |
|---|---|
| Choosing an algorithm | **Framing the problem** — what is being predicted, and for whom |
| Fitting the model | **Preparing the data** — Unit 2, and 70% of the effort |
| Getting a high accuracy | **Knowing whether that accuracy is good** — the base rate |
| Adding features | **Not leaking the target** into them |
| The training score | **The test score**, on data the model has never seen |

**Unit 2 is the most important unit in this course** and the one students skip.
Units 3, 4 and 5 are a catalogue of algorithms, each three lines of
scikit-learn. Unit 2 is what makes any of them mean something.

## Where it sits in the degree

This course is a convergence point — more of the programme meets here than
anywhere else.

| From | You have | Used here |
|---|---|---|
| **Course 4** | Regression, correlation, hypothesis testing, distributions | Unit 3 **is** Course 4's regression, refitted as prediction rather than explanation. §3.1 says exactly what changed |
| **Course 8** | Decision trees (ID3, C4.5, CART), Naive Bayes, k-NN, K-Means, DBSCAN | **Units 4 and 5 repeat these.** §4.1 and §5.1 say which parts are revision, so you do not study them twice |
| **Course 9** | NumPy, pandas, cleaning, feature engineering, matplotlib | Every lab. Unit 2's preprocessing is Course 9 Unit 3 with a purpose |
| **Course 3** | Python, functions, classes | scikit-learn's `fit`/`predict` API |
| **Course 6** | The data science lifecycle, model evaluation, ROC | Unit 2's evaluation section, in Python instead of R |

### ⚠️ The overlap with Course 8 is large, and worth planning around

Course 8 taught decision trees, Naive Bayes, k-NN, K-Means, hierarchical
clustering and DBSCAN **as hand-traced algorithms**. This course teaches the
same six **as tools you fit and evaluate**.

**That difference is the point.** Course 8 asked *how does ID3 choose a split?*
— arithmetic on paper. This course asks *is this tree overfitting, and how
would you know?* Same algorithm, a different question, and both are examined.

If you took Course 8, budget your time on Units 2 and 3, which are new.

## Course objectives (verbatim)

1. Understand fundamental concepts, types, and applications of machine
   learning.
2. Develop, evaluate, and optimize machine learning models through
   preprocessing, training, and feature engineering techniques.
3. Apply supervised and unsupervised learning algorithms to real-world problems
   using appropriate tools and methods.

> **There are only three objectives, and four outcomes.** Every other course in
> the programme has five of each. Nothing appears to be *missing* — the three
> objectives do cover the five units between them — but if an examiner asks for
> "the fourth course objective", the document does not have one. Recorded in
> [SYLLABUS-REVIEW.md](../../../SYLLABUS-REVIEW.md).

## Units

| Unit | Topic | Notes | Difficulty | Weeks |
|:---:|---|---|---|:---:|
| 1 | Introduction to machine learning | [unit-1.md](unit-1.md) | Easy | 2 |
| 2 | Model preparation, evaluation, feature engineering | [unit-2.md](unit-2.md) | **Hard** | 4 |
| 3 | Supervised learning — regression | [unit-3.md](unit-3.md) | Moderate | 3 |
| 4 | Supervised learning — classification | [unit-4.md](unit-4.md) | Moderate | 3 |
| 5 | Unsupervised learning | [unit-5.md](unit-5.md) | Moderate | 3 |

**Unit 2 gets four weeks and deserves them.** It holds preprocessing, model
selection, train/test methodology, every evaluation metric, feature
engineering and PCA. It is three units of material under one heading, and it is
where the marks that separate answers are.

## Also here

- [practice.md](practice.md) — exam questions with worked solutions
- [lab.md](lab.md) — all 12 experiments
- `labs/course-12a-ml/` — code
- `data/course-12a-ml/` — **practice datasets**, CSV: `customer-segments.csv`, `house-prices.csv`, `loan-approval.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.
  Also `flowers.csv` in `data/shared/`, which several courses
  analyse so their answers can be compared.

> **On the lab code.** **Everything in this course runs.** scikit-learn, NumPy,
> pandas and matplotlib are all installed, so all 12 practicals execute and
> every figure in these notes is asserted by
> `tools/run_ml_labs.py`. There is no
> "NOT EXECUTED" file anywhere in this course — unlike Courses 6, 8, 10, 11 and
> 13 B, nothing here needs a tool this environment cannot install.
>
> The labs use `random_state` everywhere, so every number in the notes is
> reproducible on your machine too. If you get a different figure, something
> differs — that is the point of fixing the seed.

## Textbooks

- **Alpaydin, *Introduction to Machine Learning*, 4th ed., MIT Press, 2020** —
  the theory, and the one to read for Units 1 and 2.
- Murthy & Ananthanarayana, *Machine Learning: Theory and Practice*,
  Universities Press.
- Sridhar & Vijayalakshmi, *Machine Learning*, 2nd ed., Oxford — closest to
  this syllabus's ordering.
- Marsland, *Machine Learning: An Algorithmic Perspective*, 2nd ed., CRC, 2014.
- Mitchell, *Machine Learning*, McGraw Hill — old, and still the clearest
  explanation of inductive bias and version spaces.
- **Raschka & Mirjalili, *Python Machine Learning*, 3rd ed., Packt, 2019** —
  the practical one. If you buy one book for the lab, buy this.

**Free:** scikit-learn's own User Guide is unusually good and is what
practitioners actually read.

## How to study this course

1. **Fit a model in the first week.** Load iris, split it, fit a tree, print
   the accuracy. The theory lands better once you have seen the loop.
2. **Then distrust that accuracy.** Compare it against a `DummyClassifier`.
   Unit 2 §2.5 explains why this is not optional, and it is the single habit
   that most improves an answer.
3. **Learn the three-way split cold** — train, validation, test — and why the
   test set is touched once. It is a five-mark question in itself and the
   reason most reported accuracies are wrong.
4. **For every algorithm, learn one sentence on what it assumes.** Naive Bayes
   assumes conditional independence; k-NN assumes distance is meaningful;
   linear regression assumes a linear relationship. The assumption is what the
   exam asks about, and it is what tells you when the algorithm will fail.
5. **Draw the bias–variance picture once, by hand.** Everything in Unit 2 —
   overfitting, regularisation, cross-validation, ensembles — is one trade-off
   seen from different angles.
