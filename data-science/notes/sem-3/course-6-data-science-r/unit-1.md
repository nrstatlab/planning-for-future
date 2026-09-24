# Unit 1 — Introduction to the Data Science Process

**Syllabus topics:** Introduction — definition — data science in various
fields — examples — impact of data science — Data Analytics Life Cycle — data
science toolkit — data scientist — data science team. Exploratory Data Analysis
(EDA). Feature engineering and data transformation.

---

## 1.1 What data science is

### 🎯 The big idea

Data science is the practice of turning data into decisions. It sits where
**statistics**, **computer science** and **domain knowledge** overlap — and it
is the overlap that matters, not any one circle.

### 📖 The story

A hospital notices that some patients readmitted within 30 days cost far more
than others. A statistician alone can find which variables correlate with
readmission. A programmer alone can build a system that scores every patient.
Neither, alone, knows that "discharged on a Friday" matters because weekend
follow-up clinics do not run — that is the doctor's knowledge.

Data science is the discipline that needs all three in the same room, and often
in the same person.

### The three-circle definition

```
        ┌──────────────────────────────────┐
        │          STATISTICS              │
        │   ┌──────────────────────┐       │
        │   │                      │       │
   ─────┼───┤    DATA SCIENCE      ├───────┼─────
        │   │                      │       │
        │   └──────────────────────┘       │
        │  COMPUTER          DOMAIN        │
        │  SCIENCE           KNOWLEDGE     │
        └──────────────────────────────────┘
```

| Missing circle | What you get instead |
|---|---|
| Without **domain knowledge** | Technically correct models answering the wrong question |
| Without **statistics** | Software that reports patterns which are actually noise |
| Without **computer science** | Good analysis that cannot run on real data volumes |

## 1.2 Data science in various fields

| Field | Application |
|---|---|
| **Healthcare** | Disease prediction, medical imaging, drug discovery, readmission risk |
| **Finance** | Credit scoring, fraud detection, algorithmic trading, risk modelling |
| **Retail** | Recommendation engines, demand forecasting, market basket analysis, pricing |
| **Agriculture** | Yield prediction, soil analysis, pest detection, crop insurance |
| **Transport** | Route optimisation, demand prediction, autonomous vehicles |
| **Government** | Census analysis, policy evaluation, resource allocation |
| **Sport** | Player selection, injury prediction, match strategy |
| **Education** | Dropout prediction, adaptive learning, curriculum analytics |

### Examples worth naming in an exam

- **Netflix** — recommendation drives most of what viewers watch
- **Amazon** — "customers who bought this also bought" is market basket analysis,
  which you will implement in Course 8
- **Google Maps** — traffic prediction from aggregated location data
- **UPI fraud detection** — anomaly detection on transaction streams
- **Weather forecasting** — numerical models plus statistical post-processing

## 1.3 Impact of data science

**Positive:** better medical diagnosis; earlier disaster warning; efficient
supply chains; personalised education; scientific discovery at scale.

**Negative, and examinable:** algorithmic bias reproducing historical
discrimination; privacy erosion; filter bubbles; job displacement; opaque
"black box" decisions people cannot appeal.

A complete answer names both. Unit 4 returns to the ethics.

## 1.4 The Data Analytics Life Cycle

**The most examined topic in this unit.** Six phases, and it is **iterative** —
you loop back constantly, you do not march forward once.

```
        ┌────────────────────┐
        │ 1. DISCOVERY       │  frame the problem, assess resources,
        │                    │  form initial hypotheses
        └─────────┬──────────┘
                  ▼
        ┌────────────────────┐
        │ 2. DATA PREPARATION│  collect, clean, transform, load
        │                    │  ← usually 60-80% of the total effort
        └─────────┬──────────┘
                  ▼
        ┌────────────────────┐
        │ 3. MODEL PLANNING  │  explore relationships, select
        │                    │  variables, choose techniques
        └─────────┬──────────┘
                  ▼
        ┌────────────────────┐
        │ 4. MODEL BUILDING  │  train, tune, validate
        └─────────┬──────────┘
                  ▼
        ┌────────────────────┐
        │ 5. COMMUNICATE     │  quantify results, tell the story
        │    RESULTS         │  to stakeholders
        └─────────┬──────────┘
                  ▼
        ┌────────────────────┐
        │ 6. OPERATIONALIZE  │  deploy, monitor, maintain
        └─────────┬──────────┘
                  │
                  └──────────► back to any earlier phase
```

| Phase | Key question | Typical output |
|---|---|---|
| **1. Discovery** | What problem are we solving, and do we have what we need? | Problem statement, hypotheses, resource assessment |
| **2. Data preparation** | Is the data usable? | An analytic sandbox; cleaned, transformed data |
| **3. Model planning** | Which variables and which techniques? | Variable selection, candidate models |
| **4. Model building** | Does it work? | Trained model, validation results |
| **5. Communicate results** | What does it mean to the business? | Findings, visualisations, recommendations |
| **6. Operationalize** | Can it run in production? | Deployed model, monitoring, documentation |

### 💡 Two things about this cycle that carry marks

**Phase 2 is most of the work.** Surveys consistently put data preparation at
60–80% of a project's effort. Students expect the modelling to dominate; it does
not. Saying this in an exam shows you understand real practice rather than the
textbook diagram.

**Phase 6 is where most projects die.** A model that scores well in a notebook
and never reaches production has produced nothing. This is the phase newcomers
underestimate most.

## 1.5 The data science toolkit

| Layer | Tools |
|---|---|
| **Languages** | R, Python, SQL, Scala, Julia |
| **R ecosystem** | RStudio, `tidyverse` (`dplyr`, `tidyr`, `ggplot2`), `caret`, `shiny` |
| **Python ecosystem** | Jupyter, NumPy, Pandas, scikit-learn, matplotlib |
| **Databases** | PostgreSQL, MySQL, MongoDB *(Course 10)*, Cassandra |
| **Big data** | Hadoop, Spark, Hive, Kafka |
| **Visualisation** | ggplot2, Tableau, Power BI *(Course 11)*, Plotly |
| **Version control** | Git, GitHub |
| **Deployment** | Docker, Flask/FastAPI, Shiny, cloud platforms |

**SQL is the one nobody should skip.** You already have it from Course 5, and it
remains the most-requested skill in data science job listings.

## 1.6 The data scientist and the data science team

### Skills of a data scientist

| Category | Skills |
|---|---|
| **Technical** | Programming, statistics, machine learning, databases, data wrangling |
| **Analytical** | Problem framing, critical thinking, experimental design |
| **Communication** | Visualisation, storytelling, writing for non-specialists |
| **Domain** | Understanding of the business the data describes |

### The team — nobody does all of this alone

| Role | Responsibility |
|---|---|
| **Business user / stakeholder** | Owns the problem; uses the results |
| **Project sponsor** | Funds the work; sets priorities |
| **Project manager** | Schedule, scope, delivery |
| **Business intelligence analyst** | Dashboards, reports, domain reporting |
| **Database administrator** | Provisions and manages the data environment |
| **Data engineer** | Builds pipelines; extracts and prepares data at scale |
| **Data scientist** | Modelling, analysis, method selection |

**Data engineer vs data scientist** is a standard two-mark question: the
engineer builds the pipelines that *deliver* data; the scientist builds the
models that *use* it. In most organisations there are several engineers per
scientist, because moving data reliably is harder than it sounds.

## 1.7 Exploratory Data Analysis

### 🎯 The big idea

EDA is looking at your data before modelling it — summarising, plotting and
checking — so that you discover its problems before they silently corrupt your
results.

### 📖 The story

An analyst fits a regression on customer ages and gets a bizarre result. Half an
hour of confusion later, a histogram reveals what a five-second plot would have
shown immediately: several hundred records have age `999`, the system's code for
"not supplied". The model had been faithfully learning from nonsense.

**Every experienced analyst has a story like this. EDA is how you avoid yours.**

### What EDA covers

| Step | Question | R |
|---|---|---|
| **Structure** | What shape and types? | `str(df)`, `dim(df)`, `glimpse(df)` |
| **Summary** | What are the ranges and centres? | `summary(df)` |
| **Missing values** | What is absent, and is it absent at random? | `colSums(is.na(df))` |
| **Distribution** | What shape is each variable? | `hist()`, `boxplot()`, `ggplot`+`geom_histogram` |
| **Outliers** | Are there impossible or extreme values? | `boxplot()`, IQR rule |
| **Relationships** | What moves with what? | `cor()`, `pairs()`, `geom_point` |
| **Categories** | How are groups distributed? | `table()`, `geom_bar` |

### The four questions EDA always answers

1. **What does each variable look like on its own?** (univariate)
2. **How do variables relate to each other?** (bivariate)
3. **What is missing, wrong or impossible?** (quality)
4. **What should I do about it?** (the decision EDA exists to inform)

**Univariate, bivariate and multivariate analysis** are the standard three
categories — know the names.

Your statistical toolkit from Course 4 is exactly what EDA uses: mean, median,
standard deviation, IQR, skewness, correlation, histograms, box plots and
scatter plots. **This unit is Course 4 applied.**

## 1.8 Feature engineering and data transformation

### 🎯 The big idea

Feature engineering is creating better input variables from the ones you have.
It routinely improves a model more than switching algorithms does.

### 📖 The story

You are predicting house prices and have `length` and `width`. A model can
technically learn from both — but `area = length × width` is what actually
drives price, and handing the model that single derived feature will beat any
amount of algorithm tuning on the raw pair.

That is feature engineering: using what you know about the problem to give the
model a better starting point.

### Common techniques

| Technique | What it does | When |
|---|---|---|
| **Scaling / normalisation** | Rescale to [0,1] | Distance-based methods (KNN, K-Means) |
| **Standardisation** | Rescale to mean 0, sd 1 | Regression, PCA, neural networks |
| **Encoding** | Categories → numbers | Any model; one-hot for nominal, ordinal for ranked |
| **Binning / discretisation** | Continuous → categories | Age → age group |
| **Log transform** | Compress a long right tail | Income, population, prices |
| **Derived features** | Combine existing variables | area, ratios, BMI, days-since |
| **Date parts** | Extract components | Day of week, month, is-weekend |
| **Aggregation** | Group-level summaries | Average spend per customer |

> **Min-max normalisation:  x′ = (x − min) / (max − min)** → range [0, 1]
>
> **Standardisation (z-score):  x′ = (x − μ) / σ** → mean 0, sd 1

**Which to use** — a reliable exam question. Normalisation when you need a
bounded range and the distribution is not normal; standardisation when the
method assumes roughly normal data or is sensitive to variance. Distance-based
algorithms need *one or the other*, because otherwise a variable measured in
rupees will overwhelm one measured in years purely through scale.

### Encoding categorical variables

| Method | Produces | Use for |
|---|---|---|
| **Label encoding** | Red=1, Green=2, Blue=3 | **Ordinal** data only |
| **One-hot encoding** | Three 0/1 columns | **Nominal** data |
| **Ordinal encoding** | Low=1, Medium=2, High=3 | Genuinely ordered categories |

**Label-encoding nominal data is a real error**, not a stylistic one: it tells
the model that Blue(3) > Green(2) > Red(1) and that Green is the average of Red
and Blue. Neither is true, and a linear model will act on both.

---

## 📝 Practice problems

### Problem 1

A retail chain wants to predict which customers will stop shopping with them.
Walk through how the Data Analytics Life Cycle applies.

**Solution.**

- **1. Discovery** — Define "stopped shopping" precisely: no purchase in 90
  days? 180? Identify available data (transactions, demographics, support
  contacts). Hypothesis: customers who complain and receive no resolution churn
  more. Assess whether we have enough historical churn examples to learn from.

- **2. Data preparation** — Join transaction, customer and support tables.
  Handle customers with no purchase history. Decide what to do with the
  duplicate accounts one person may hold. Build the analytic sandbox.

- **3. Model planning** — Explore which variables separate churners from
  non-churners: recency, frequency, monetary value, complaint count. Choose
  candidate techniques — logistic regression for interpretability, a decision
  tree for rules the business can act on.

- **4. Model building** — Train on historical data, validate on a held-out
  period. Evaluate with a confusion matrix; note that accuracy alone is
  misleading if only 5% churn.

- **5. Communicate results** — "Customers with an unresolved complaint in the
  last 60 days are four times more likely to churn." That sentence is worth
  more than the model's AUC.

- **6. Operationalize** — Score customers weekly, feed high-risk ones to the
  retention team, monitor whether the model's accuracy decays as behaviour
  changes.

**The loop:** if step 4 shows the model cannot separate the classes, you return
to step 2 or 3 for better features — you do not proceed to step 5 with a bad
model.

### Problem 2

You are given a dataset of student records with `name`, `dob`, `city`,
`marks_out_of_100`, and `annual_family_income`. Suggest five engineered
features and justify each.

**Solution.**

| Feature | Derived from | Why |
|---|---|---|
| `age` | `dob` | The date itself is not comparable across students; age is |
| `age_group` | `age` | Binning can capture non-linear effects a linear model would miss |
| `log_income` | `annual_family_income` | Income is strongly right-skewed; the log makes it usable in a linear model |
| `city_tier` | `city` | Hundreds of city values one-hot encode badly; tier (metro/tier-2/rural) has few levels and more signal |
| `pass_fail` | `marks` | A binary target if the question is classification rather than regression |

Note what is **not** a good feature: `name` label-encoded. Names carry no
ordering, and encoding them invites the model to learn from a meaningless
number — and potentially from caste or religion signals in the name, which is
an ethics failure as well as a statistical one.

### Problem 3

Normalise and standardise the values 10, 20, 30, 40, 50.

**Solution.**

- **Min-max normalisation**, x′ = (x − 10) / (50 − 10) = (x − 10)/40:

| x | 10 | 20 | 30 | 40 | 50 |
|---|---|---|---|---|---|
| x′ | **0.00** | **0.25** | **0.50** | **0.75** | **1.00** |

- **Standardisation**, x′ = (x − μ)/σ. Mean μ = 30. Population sd:
  σ = √[(400+100+0+100+400)/5] = √200 = **14.142**

| x | 10 | 20 | 30 | 40 | 50 |
|---|---|---|---|---|---|
| x′ | **−1.414** | **−0.707** | **0.000** | **0.707** | **1.414** |

*Check:* normalised values span exactly [0, 1]; standardised values have mean 0
and sd 1. Both checks are worth doing in the exam.

---

## Exam questions from this unit

**Two marks**

1. Define data science and name its three constituent areas.
2. List the phases of the Data Analytics Life Cycle.
3. What is EDA, and why is it done before modelling?
4. Distinguish a data engineer from a data scientist.
5. Distinguish normalisation from standardisation.

**Five marks**

1. Explain the Data Analytics Life Cycle with a diagram.
2. Explain feature engineering with five techniques and examples.
3. Explain EDA and the steps it involves.
4. Explain the roles in a data science team.

**Ten marks**

1. Explain the data science process in full, from discovery to
   operationalisation, with a case study.
2. Explain data preprocessing and feature engineering — scaling, encoding,
   binning, transformation — with worked examples.

## Mistakes that cost marks

- Presenting the life cycle as strictly linear — it is **iterative**
- Claiming modelling is the bulk of the work; data preparation is
- Label-encoding nominal categories
- Applying normalisation before splitting into train and test sets, which leaks
  test information into training
- Confusing EDA (understanding data) with modelling (predicting from it)
- Naming only the benefits of data science when asked about its impact
