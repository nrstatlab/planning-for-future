# Unit 4 — Cloud Platforms for Data Science and ML

**Syllabus topics:** Machine learning in the cloud: benefits and
limitations. Cloud-based ML services: AIaaS, GPUaaS. Managed ML platforms:
overview and advantages. Cloud ML platforms: AWS SageMaker, Azure ML Studio,
Google Cloud AutoML.

---

## 4.1 Machine learning in the cloud — what changes, and what does not

### 🎯 The table to lead with

| | **Your laptop** | **A managed platform** |
|---|---|---|
| **The algorithm** | scikit-learn | **scikit-learn — identical** |
| Data source | a local file | `s3://`, or a feature store |
| Hardware | what you own | **chosen per job, per hour** |
| Training time | hours on CPU | minutes on GPU, *if it helps* |
| Experiment tracking | a notebook cell | logged automatically |
| The artefact | a file you might lose | **versioned in object storage** |
| Deployment | you build a server | **one API call** |
| Cost | sunk | **per second, and visible** |

### 💡 The first row is the point

**The cloud does not make your model better.** It makes training
**reproducible**, deployment **routine** and cost **visible**.

Measured, in
`11_train_and_automl.py`:

| Model | Accuracy | F1 | AUC |
|---|---:|---:|---:|
| `DummyClassifier` | **0.8433** | 0.0000 | 0.5000 |
| GradientBoosting | 0.9467 | 0.8095 | 0.9029 |

**Quote the dummy first, always.** 94.67% sounds excellent until you see that
predicting "never churns" scores 84.33%. The real gain is **10.3 percentage
points**, and it is the **F1 of 0.8095 against 0.0000** that shows the model
found anything at all.

**This is Course 12 A's argument, and it does not stop being true because the
model trained on somebody else's computer.**

---

## 4.2 Benefits, honestly weighed

| Benefit | The mechanism | The catch |
|---|---|---|
| **Elastic capacity** | rent what the job needs, for its duration | **only helps if the algorithm uses it** |
| **No infrastructure work** | no drivers, no CUDA versions, no cluster | you inherit the platform's opinions |
| **Reproducibility** | jobs are declarative and logged | only if you actually use jobs |
| **Collaboration** | shared notebooks, shared data, shared artefacts | governance becomes mandatory |
| **Deployment in one call** | `estimator.deploy()` | **the endpoint bills until deleted** |
| **Pre-trained services** | vision, speech, translation APIs | a black box you cannot audit |
| **Cost per experiment visible** | per-second billing, tagged | *also* a bill for careless work |

### 🔢 The catch that is measured

For the same ten-minute training job:

| Instance | $/hour | 10 min |
|---|---:|---:|
| t3.medium | 0.0416 | 0.0069 |
| **m5.xlarge** | 0.1920 | **0.0320** |
| c5.4xlarge | 0.6800 | 0.1133 |
| p3.2xlarge (1 GPU) | 3.0600 | 0.5100 |
| **p4d.24xlarge (8 GPU)** | **32.7726** | **5.4621** |

**The 8-GPU box costs 171× the general-purpose one**, and gradient boosting on
tabular data **has no GPU code path**. It would run at exactly the same speed.

> **"Which instance?" is answered by the algorithm, not by ambition.**

GPUs earn their price on **dense matrix multiplication** — deep learning.
Tree ensembles, linear models and pandas feature engineering do not use them.

---

## 4.3 Limitations

| Limitation | Why it bites |
|---|---|
| **Cost is variable and easy to lose track of** | an endpoint bills whether or not it is called |
| **Lock-in** | a SageMaker pipeline does not run on Vertex |
| **Data must move to it** | egress, latency, and sometimes law |
| **Regulatory constraints** | residency, and who may hold identifiable data |
| **Black-box pre-trained services** | you cannot audit, tune or explain them |
| **Version pinning** | the platform's framework versions, not yours |
| **Debugging is remote** | a failed job is a log file, not a breakpoint |

### ⚠️ The one that costs real money

**A training job ends and stops billing. An endpoint runs until you delete
it**, at hourly rates, whether or not anything calls it.

**An `ml.m5.large` endpoint is about $70/month, called or not.**

Every "surprise cloud bill" story is a resource nobody switched off. **Set a
budget alarm on day one**, before creating anything else.

### ⚠️ And the one that costs credibility

**Nothing about the cloud fixes the data.** A wrong target, a leaked feature,
an unexamined base rate or a drifted distribution is exactly as wrong on
eight GPUs. The `DummyClassifier` at 84.33% is unmoved by hardware.

---

## 4.4 AIaaS and GPUaaS

The syllabus names these as if they were new layers. **They are not**, and
saying so is worth the mark:

| Term | What it actually is |
|---|---|
| **AIaaS** | **SaaS for a model** — an API that returns a prediction |
| **GPUaaS** | **IaaS for a GPU** — a rented machine that happens to have one |
| **MLaaS / managed ML** | **PaaS for the ML lifecycle** |

### AIaaS — pre-trained services

| Service | AWS | Azure | GCP |
|---|---|---|---|
| Vision | Rekognition | Computer Vision | Vision AI |
| Speech → text | Transcribe | Speech Service | Speech-to-Text |
| Text → speech | Polly | Speech Service | Text-to-Speech |
| Translation | Translate | Translator | Translation AI |
| Text analysis | Comprehend | Language Service | Natural Language AI |
| Document extraction | Textract | Form Recognizer | Document AI |

### 🎯 When AIaaS is right, and when it is not

**Right** when the task is **generic** — reading text from an invoice,
transcribing English, detecting a face. You will not beat a model trained on
billions of examples with your afternoon and your dataset.

**Wrong** when:

- the task is **specific to your domain** — the general model has never seen
  your vocabulary, your forms, your defect types
- you must **explain** a decision to a regulator
- the data may not leave your environment
- you need the model to **stop changing** — the provider updates it, and your
  downstream thresholds shift underneath you

**That last one is underrated.** A pre-trained API is a dependency that
silently changes behaviour, and nothing in your test suite will tell you when.

### GPUaaS — and the honest version

**Renting a GPU is renting an instance.** The interesting content is *which
one and why*:

| Family | For | Note |
|---|---|---|
| p4d, p5 | large-model **training** | A100/H100; very expensive |
| p3 | training | V100; older, cheaper |
| g5, g4dn | **inference**, small training | cheaper per prediction |
| inf1/inf2, TPU | inference at scale | vendor silicon, framework limits |

**And the two questions before renting any of them:**

1. **Does the algorithm have a GPU code path?** If not, the answer is no.
2. **Is the GPU actually busy?** A GPU at 15% utilisation because the data
   loader is the bottleneck is a CPU problem you are paying GPU rates to
   ignore.

---

## 4.5 Managed ML platforms

### 📖 What "managed" covers

A managed platform provides the whole lifecycle as services:

```
  data  →  prepare  →  train  →  tune  →  register  →  deploy  →  monitor
            │           │        │         │            │          │
         Data Wrangler  Training HPO    Model      Endpoint   Model
         / Glue         Jobs           Registry              Monitor
```

**The value is not any one box; it is that they are joined**, versioned, and
logged. An experiment six months old can be re-run from its record.

### The three platforms, compared

| | **AWS SageMaker** | **Azure ML** | **Google Vertex AI** |
|---|---|---|---|
| Notebook | Studio | Studio notebooks | Workbench |
| Training | Training Jobs, BYO container | Command jobs | Custom Training |
| AutoML | **Autopilot** | Automated ML | **AutoML Tables** |
| Tuning | Automatic Model Tuning | Sweep jobs | Vizier |
| Registry | Model Registry | Model Registry | Model Registry |
| Endpoint | real-time, serverless, **batch transform** | managed endpoints | Prediction |
| Pipelines | SageMaker Pipelines | Azure ML Pipelines | Vertex Pipelines |
| Monitoring | **Model Monitor** | Data Drift monitors | Model Monitoring |
| Notable | the widest feature set | best Microsoft-estate fit | **best AutoML, BigQuery integration** |

### 🎯 Learn the row, not the column

**All three have every one of these**, and an exam answer that names the
capability and gives one vendor's term is worth more than a memorised AWS
product list. The syllabus's own outcome asks you to *apply cloud-based
platforms*, not to recite one.

### The pieces worth knowing by name

| Piece | What it solves |
|---|---|
| **Model registry** | which model is in production, trained on what, by whom |
| **Feature store** | one definition of a feature, served to training **and** serving |
| **Experiment tracking** | which hyperparameters produced which metric |
| **Pipelines** | the DAG, so a retrain is one command |
| **Model monitor** | the distribution has drifted and nothing errored |

**The feature store is the one that prevents a real, silent failure:**
training/serving skew, where a feature is computed one way in the batch job
and another way at request time. The model then sees a distribution it never
trained on, and every infrastructure metric stays green.

---

## 4.6 AutoML

### 🔢 What it actually does, run for real

Five candidates, 5-fold cross-validation on ROC AUC, **25 real fits**:

| Rank | Model | CV AUC | std |
|---:|---|---:|---:|
| 1 | RandomForest(100) | **0.9334** | 0.0210 |
| 2 | GradientBoosting | **0.9288** | 0.0196 |
| 3 | DecisionTree(depth=None) | 0.8213 | 0.0425 |
| 4 | LogisticRegression | 0.8154 | 0.0606 |
| 5 | DecisionTree(depth=3) | 0.8025 | 0.0364 |

**The leaderboard is the whole of AutoML.** It fits many models,
cross-validates each, and ranks them. **There is no intelligence in it — it is
a search**, and its value is that it is exhaustive where a human would be lazy.

### ⚠️ And read the top of it carefully

**0.9334 against 0.9288 is a gap of 0.0047, with standard deviations of
0.0210 and 0.0196. The difference is inside the noise.**

Declaring a winner here is not supported by the data, and **"AutoML picked X"
is not a reason to prefer X**. If two models are indistinguishable, choose on
something else: inference cost, interpretability, training time.

### 🔢 What the search costs

One fit on this 1,200-row dataset takes 0.127 s — too small to cost anything.
**Scale it to a realistic four minutes per fit:**

| Search | Fits | Compute | m5.xlarge |
|---|---:|---:|---:|
| this search | 25 | 1.7 h | $0.32 |
| a modest managed search | 250 | 16.7 h | $3.20 |
| **a full AutoML run** | **2,000** | **133.3 h** | **$25.60** |

**AutoML's compute is a straight multiple of one fit** — $25.60 against
$0.0128, exactly 2,000×, because that is all it is. **And managed AutoML
services charge a premium on top of the compute.**

### 🎯 What AutoML does not do

- decide what the **target variable** should be
- notice that your target **leaks** the answer
- tell you the **base rate** matters more than the algorithm
- know that last year's data no longer describes this year
- choose a **threshold** that fits the business cost of an error
- **explain** a prediction to a regulator
- notice the model is **unfair** to a protected group

**Every one of those is the actual job.** AutoML automates the part a
competent person does in an afternoon and leaves untouched the parts that take
weeks and cause the failures.

> **Say that when asked to evaluate AutoML — and say it before saying it is
> useful, which it is.**

### 💡 The one genuinely valuable output

Autopilot generates a **candidate-definition notebook** and a
**data-exploration notebook**. **Read them.** They show the feature
engineering the search chose, which is the part you would otherwise never see
and could not defend to anyone.

---

## Practice problems

**1. A team reports "our model is 97% accurate in the cloud". What do you ask
next?**

**Three questions, in order:**

1. **What is the base rate?** 97% on a 3%-positive problem is what
   `DummyClassifier` scores by predicting "no" every time — measured here at
   **84.33% accuracy and 0.0000 F1** on a 15%-positive problem.
2. **What is the F1 or recall on the positive class?** Accuracy on an
   imbalanced problem tells you almost nothing.
3. **Was the test set held out before any preprocessing?** Scaling or
   imputing on the full dataset leaks the test distribution into training.

**And "in the cloud" is irrelevant to all three.** The infrastructure has no
bearing on whether the evaluation is sound, and mentioning it suggests the
speaker thinks it does.

**2. When would you use a pre-trained AIaaS API instead of training your own
model?**

**When the task is generic and your data is not special.** Extracting text
from a scanned invoice, transcribing English speech, detecting whether an
image contains a face — a model trained on billions of examples will beat what
you can build, and the API costs cents per call.

**Train your own when:**

- the domain is **specific** — your defect types, your forms, your vocabulary
- you must **explain** the decision, or audit it
- the data may not leave your environment
- the behaviour must be **stable** — the provider updates the model, and your
  thresholds move underneath you

**The decision rule:** *would a knowledgeable stranger do this task well
without knowing your business?* If yes, use the API.

**3. Your AutoML run returns a model with AUC 0.91 and your hand-built one
scores 0.89. Do you switch?**

**Not on those numbers alone.** Ask:

1. **What is the variance?** In the measured run, standard deviations were
   0.0196 and 0.0210 — a 0.02 gap is comfortably inside one standard
   deviation, so the models are not distinguishable.
2. **Is it the same test set, the same folds, the same preprocessing?** If
   AutoML did its own feature engineering, you are comparing two pipelines,
   not two models.
3. **What does the AutoML model cost to serve, and can you explain it?** A
   stacked ensemble of forty models scoring 0.02 higher is often a worse
   choice than one gradient booster.

**And if the gap is real and large**, the useful question is *what did it
find that I missed?* — read the candidate-definition notebook. The feature
engineering is usually the answer, and you can adopt it in your own pipeline.

**4. Explain the difference between AIaaS, GPUaaS and a managed ML platform,
with an example of when each is right.**

| | Is | Right when |
|---|---|---|
| **AIaaS** | **SaaS for a model** — an API returning a prediction | transcribing customer calls: generic, well-solved |
| **GPUaaS** | **IaaS for a GPU** — a rented machine | fine-tuning a vision model on your own images |
| **Managed ML** | **PaaS for the lifecycle** | a churn model that must be retrained monthly, versioned and monitored |

**The axis is the same as Unit 1's:** how much of the stack the provider
manages. AIaaS manages everything including the model; GPUaaS manages only the
hardware; managed ML sits between, handling the lifecycle while you supply the
algorithm and the data.

**5. Your training job runs on a p3.2xlarge and the GPU shows 12%
utilisation. What is wrong and what does it cost you?**

**The GPU is not the bottleneck — the data pipeline is.** The GPU is idle 88%
of the time waiting for batches.

**Usual causes:** single-threaded data loading, decoding images on the CPU,
reading small files one at a time from object storage, or a batch size too
small to fill the device.

**What it costs:** you are paying $3.06/hour for a machine doing $0.19/hour of
work — and the fix is almost always CPU-side: more data-loader workers,
prefetching, larger batches, pre-decoded data in a format like TFRecord or
WebDataset, or reading larger files.

**The general point:** *rent the resource that is the bottleneck.* Paying GPU
rates to run a CPU-bound pipeline is the most common way to waste money on a
managed ML platform.

---

## Exam questions from this unit

**Two marks**

1. What does the cloud change about a machine-learning algorithm?
2. Expand AIaaS and GPUaaS, and say what each really is.
3. Name three managed ML platforms.
4. What is a model registry for?
5. What is a feature store for?
6. What does AutoML actually do?
7. Name two things AutoML cannot do.
8. Why does a training job stop billing and an endpoint not?

**Five marks**

1. Explain the benefits of ML in the cloud, and the catch attached to each.
2. Explain the limitations of cloud ML platforms.
3. Explain AIaaS with examples, and when it is the wrong choice.
4. Compare SageMaker, Azure ML and Vertex AI by capability.
5. Explain what AutoML does, what it costs, and what it leaves undone.

**Ten marks**

1. Explain cloud-based ML services in full — AIaaS, GPUaaS and managed
   platforms — with the benefits, the limitations, and worked cost figures.
2. Evaluate AutoML for a business that wants to build a churn model. What
   will it do, what will it not do, and what would you recommend?

---

## Mistakes that cost marks

- **Saying the cloud makes models more accurate.** It makes training
  reproducible, deployment routine and cost visible.
- **Quoting accuracy without the base rate.** 84.33% for a dummy.
- **Treating AIaaS and GPUaaS as new service models.** They are SaaS and IaaS
  for particular things.
- **Recommending GPUs for tabular machine learning.** 171× the price, same
  speed.
- **Presenting an AutoML leaderboard's winner as the best model** without
  checking whether the gap exceeds the variance.
- **Forgetting that an endpoint bills when idle.**
- **Naming only AWS products** when asked about cloud ML platforms.
- **Ignoring training/serving skew.** It is the failure with no error
  message, and the feature store exists for it.
