# Course 14 A — Neural Networks and Deep Learning

**Semester VI**

**This is a Track A course**, paired with
Course 15 A (Natural Language Processing), and it
continues the track you began in Semester V with Machine Learning and
Artificial Intelligence.

---

## The one thing to understand before anything else

**A neural network is not a new idea bolted onto machine learning. It is the
same idea — fit parameters to minimise a loss — with one change: the features
are learned rather than chosen.**

That single change is the whole course, and it is worth being precise about
what it costs and what it buys.

| Course 12 A taught you | This course changes |
|---|---|
| You engineer features, the model fits weights | **The model engineers its own features** |
| A model with 20 parameters and 1,000 rows | A model with 150,000 parameters and 1,000 rows |
| Overfitting is controlled by model choice | Overfitting is controlled by **dropout, early stopping and data** |
| Training is deterministic and fast | Training is stochastic, slow, and **can fail outright** |
| The model is interpretable if you chose it to be | The model is **not interpretable**, and you must design experiments to find out what it learned |

### 🎯 The single most examinable idea

> **A stack of linear layers is one linear layer.** Without a non-linear
> activation between them, `W₃(W₂(W₁x))` is just `Wx` for `W = W₃W₂W₁`.
> **The activation function is the only reason depth means anything.**

The lab proves it twice: a perceptron cannot learn XOR at all
(`01_perceptron_scratch.py` reports accuracy **0.50**, converged **never**),
and one hidden layer with a non-linearity solves it exactly (**1.00**).

### ⚠️ The mistake this course exists to prevent

> Reporting an accuracy without a baseline. **A deep network that gets 94% on
> a task where a linear model gets 91% has bought you three points for
> 59,210 parameters** — that is the actual measurement from experiment 4, and
> it is the kind of number that should change what you build.

Every experiment here reports a baseline next to the headline number.

---

## What runs here

**Ten of the twelve experiments run against real data and real pre-trained
weights.** That is worth stating plainly, because the usual assumption about
a sandboxed environment is the opposite.

| What the syllabus names | What actually ran |
|---|---|
| MNIST (exp. 4) | **the real MNIST**, a stratified 4,000-image subset |
| Fashion-MNIST (exp. 6, 7) | **the real Fashion-MNIST**, a stratified 8,000-image subset |
| IMDb (exp. 9) | **the real IMDb**, 6,000 training reviews, 10,000-word vocabulary |
| MobileNet, VGG (exp. 8, 11) | **the real published ImageNet networks**, with their real trained weights |
| Keras / TensorFlow | **real Keras 3**, on the torch backend — identical API |

### The two that do not run, and why

| Experiment | Why | Where it lives |
|---|---|---|
| **2** — TensorFlow Playground, Teachable Machine | interactive web apps; there is no output to capture | `02_playground.md` — a full experiment protocol with a results table to fill in |
| **12** — Hugging Face deployment | `huggingface.co` is refused at the gateway with a **403** | `12_huggingface_app.md` — the complete app, the traps, and the error analysis that carries the marks |

Both files carry `*** NOT EXECUTED ***` in their header, and
`tools/run_deeplearning_labs.py` asserts that the marker is still there.

### 📖 Why there are generated datasets as well as real ones

Real data tells you the accuracy. **Only a built dataset can tell you whether
the network learned the thing you intended**, and that check is the difference
between a lab report and a demo.

| Built dataset | The question it can answer that real data cannot |
|---|---|
| XOR, four rows | Did it fail because of *this* limitation, provably? |
| 2,000 review sentences, one decisive word each | Fed that word alone, does the model score it correctly? (**positive 0.9998, negative 0.0002**) |
| Four shapes, a known source→target gap | Did transfer help *because* the features moved, or by luck? |

The lab does both, every time, and says which is which.

---

## Course objectives (verbatim)

1. Introduce the fundamental concepts of Artificial Neural Networks and Deep
   Learning, along with their historical and biological inspirations.
2. Provide an in-depth understanding of different neural network architectures
   including Perceptron, DNN, CNN, RNN, and advanced models.
3. Develop hands-on skills to design, train, and evaluate deep learning models
   using popular frameworks such as TensorFlow and Keras.
4. Expose students to applications of deep learning in computer vision, natural
   language processing, and generative modeling.
5. Enable students to critically analyze challenges in deep learning such as
   overfitting, bias, and ethical concerns.

## The five units

| Unit | Topic | Notes | Hardest part |
|---|---|---|---|
| 1 | Foundations: neurons, perceptrons, activations, loss | [unit-1.md](unit-1.md) | why a stack of linear layers is one linear layer |
| 2 | Training: forward/backward propagation, initialisation, optimisers | [unit-2.md](unit-2.md) | the vanishing gradient, as arithmetic rather than a slogan |
| 3 | CNNs: convolution, pooling, LeNet/AlexNet/VGG | [unit-3.md](unit-3.md) | the output-size formula, and where the parameters actually are |
| 4 | RNNs: sequences, LSTM, GRU, text generation | [unit-4.md](unit-4.md) | why the gates fix what they fix |
| 5 | Advanced: transfer learning, attention, transformers, ethics | [unit-5.md](unit-5.md) | attention as a weighted average you can compute by hand |

Plus [lab.md](lab.md) — all twelve experiments with their measured output —
and [practice.md](practice.md) — exam questions with worked solutions.

---

## Also here

- [practice.md](practice.md) — exam questions with worked solutions
- [lab.md](lab.md) — all 12 practicals
- `labs/course-14a-deeplearning/` — the code, and the runner that asserts every figure
  these notes quote
- `data/course-14a-deeplearning/` — **practice datasets**, CSV: `sensor-failures.csv`, `xor.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.
  Also `flowers.csv` in `data/shared/`, which several courses
  analyse so their answers can be compared.

## How this course connects to the rest of the programme

| Course | What it gives you here |
|---|---|
| **Course 3** (Python) | NumPy array thinking; every layer is a matrix multiply |
| **Course 4** (Statistics) | loss functions are likelihoods; cross-entropy is one |
| **Course 9** (Python for Data Analysis) | the train/test discipline this course depends on |
| **Course 12 A** (Machine Learning) | the baselines. **Do not skip them** |
| **Course 13 A** (AI) | search and optimisation; gradient descent is one more optimiser |
| **Course 15 A** (NLP) | takes the RNN and attention material and applies it to language |

---

## Textbooks

- Chollet, *Deep Learning with Python*, 1st edition, Manning, 2018 — written by
  the author of Keras, and the best fit to Units 2–5. A 2nd edition exists
  (2021); the syllabus prescribes the 1st.
- Nielsen, *Neural Networks and Deep Learning*, Determination Press, 2015 —
  **free and legal to read online** at
  [neuralnetworksanddeeplearning.com](http://neuralnetworksanddeeplearning.com).
  The clearest explanation of backpropagation on this syllabus.

**References:** Géron, *Hands-On Machine Learning with Scikit-Learn, Keras and
TensorFlow*, O'Reilly, 2019 · Howard & Gugger, *Practical Deep Learning for
Coders*, 2020, based on the fast.ai course · Shane, *You Look Like a Thing and
I Love You*, Voracious/Hachette, 2019 — the one on Unit 5's ethics, and the
only genuinely funny book on the syllabus.

> ### ⚠️ "Coders(Based" — a lost space
>
> The reference list reads "Practical Deep Learning for **Coders(Based** on the
> fast.ai course)". The title ends at *Coders*; the rest is a parenthetical.
> See review finding **D26**.

## How to study this course

1. **Fix the seed and read the numbers.** Every script here sets one, so the
   figures reproduce on your machine. If yours differ, something differs — that
   is the point of fixing it.
2. **Do experiment 4 before anything else in Unit 2.** The learning-rate table
   is the fastest way to see that a model which "does not work" is usually a
   model that was never going to converge.
3. **Do the arithmetic by hand once.** The output-size formula in Unit 3 and
   the `√d_k` scaling in Unit 5 are two-mark questions you can derive rather
   than memorise — and deriving them is faster than looking them up.
4. **Train something small on your own laptop.** MNIST trains in under a minute
   on a CPU. Waiting for a GPU you do not have is how this course gets
   abandoned in week 9.
5. **Take Unit 5's ethics seriously.** It carries marks, it is the part
   examiners ask about in the viva, and "bias, fairness, privacy, safety,
   explainability" is five separate answers, not one.
6. **Read the failures in these notes.** Zero of eight first-layer kernels came
   out clearly oriented, VGG16 lost to a small CNN trained from scratch, and
   fine-tuning lost to frozen features. Those results are reported rather than
   tidied away, because the tidy version would have taught you something false.

## If you read one thing

**Unit 2**, and specifically the part on what makes training fail. Depth,
width and architecture are choices you can reason about. A learning rate that
is 100× too large produces a model that never learns anything, and the
experiment 4 table shows exactly that — **`lr=10.0` finished at accuracy
0.1000 with the loss having gone *up*.**

Nothing else in the course matters if training does not converge.
