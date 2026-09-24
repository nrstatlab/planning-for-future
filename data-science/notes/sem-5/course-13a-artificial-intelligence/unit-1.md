# Unit 1 — Introduction to AI and Intelligent Agents

**Syllabus topics:** Definition and scope of AI; history and evolution of
AI; the Turing Test; applications of AI in the real world. Types of AI — Weak
AI vs Strong AI, Narrow AI vs General AI. Intelligent agents — structure of
agents, rationality, agent types. Environments — deterministic vs stochastic,
static vs dynamic, discrete vs continuous. PEAS representation (performance
measure, environment, actuators, sensors).

---

## 1.1 What AI is, and what "intelligent" is doing in the name

The **definition and scope of AI** is the first thing the syllabus asks for, and it is genuinely contested — which is why the exam answer needs a definition *and* a boundary.

### 🎯 The big idea

**AI is the study of building systems that act rationally** — that do the right
thing given what they know.

The word "intelligent" invites arguments that the field has learned to avoid.
Russell and Norvig's four-way split is the standard way to organise them, and
it is a standard exam question:

| | **Human-centred** | **Rationality-centred** |
|---|---|---|
| **Thought** | Systems that **think like humans** — cognitive modelling | Systems that **think rationally** — logic, the "laws of thought" |
| **Behaviour** | Systems that **act like humans** — the Turing Test | **Systems that act rationally** — the rational agent |

**The bottom-right cell is the one the field actually pursues**, and it is the
definition to give. Reasons worth stating:

- **Acting rationally is measurable.** "Thinking like a human" is not.
- **Rationality is more general than logic.** Sometimes the right action cannot
  be proved correct, and you must act anyway.
- **It does not require consciousness**, which nobody can test for.

### 📖 History — the dates that get asked

| Year | Event |
|---|---|
| 1943 | McCulloch and Pitts model an artificial neuron |
| **1950** | **Turing's "Computing Machinery and Intelligence"** — the Imitation Game |
| **1956** | **The Dartmouth Conference. John McCarthy coins "Artificial Intelligence"** |
| 1957–69 | Early optimism: the Logic Theorist, GPS, perceptrons, ELIZA |
| 1969 | Minsky and Papert's *Perceptrons* — kills neural network funding |
| 1970s | **The first AI winter** — promises unmet, funding cut |
| 1980s | **Expert systems** — MYCIN, XCON. AI's first commercial success |
| late 80s | **The second AI winter** — expert systems proved brittle |
| **1997** | **Deep Blue beats Kasparov** |
| 1990s–2000s | The statistical turn: machine learning, probability, data |
| **2012** | **AlexNet** — deep learning wins ImageNet decisively |
| 2016 | AlphaGo beats Lee Sedol |
| 2017– | Transformers; large language models |

**Two things to say about the winters**, because they are the interesting part:
both followed **over-promising**, and both ended when the field found something
that **actually worked on real problems** — expert systems, then statistical
learning. The pattern is worth a mark.

### 🔢 The Turing Test

**A human interrogator converses by text with a human and a machine. If the
interrogator cannot reliably tell which is which, the machine passes.**

Turing's move was to **replace an unanswerable question** ("can machines
think?") with an operational one.

| Requires the machine to have | Because |
|---|---|
| Natural language processing | To communicate at all |
| Knowledge representation | To store what it knows |
| Automated reasoning | To answer and draw conclusions |
| Machine learning | To adapt and generalise |
| *(Total Turing Test)* computer vision and robotics | To perceive and manipulate objects |

### ⚠️ The criticisms — and give at least two

1. **It tests imitation, not intelligence.** A system can pass by being evasive
   and making deliberate mistakes; ELIZA (1966) fooled people with pattern
   substitution and no understanding at all.
2. **Searle's Chinese Room.** A person following rule-books to manipulate
   Chinese symbols could pass while understanding nothing — so behaviour does
   not establish understanding.
3. **It is anthropocentric.** Aircraft do not flap. Requiring machines to be
   *indistinguishable from humans* is not a useful engineering target.
4. **It is not a research programme.** Nobody builds systems by aiming at it.

**Its value is historical and philosophical**, and saying that is the mature
answer.

---

## 1.2 Types of AI

### 🔢 Two independent classifications, and students conflate them

The first axis is **Narrow AI against General AI** — how *wide* the capability is:

| | **Narrow AI (Weak)** | **General AI (AGI)** | **Super AI** |
|---|---|---|---|
| Scope | **One task** | **Any** intellectual task a human can do | Beyond human, across the board |
| Exists? | **Yes — everything today** | **No** | **No** |
| Examples | Chess engines, spam filters, translation, self-driving | — | — |

That axis is about **capability breadth**. The other is about **claims of
mind**:

| | **Weak AI (hypothesis)** | **Strong AI (hypothesis)** |
|---|---|---|
| Claims | The machine **acts as if** it thinks. A useful tool | The machine **genuinely thinks** and has a mind |
| Is it a claim about | **Behaviour** | **Consciousness** |
| Testable? | Yes | **Not agreed to be** |
| Searle's target | — | **Strong AI** — the Chinese Room argues against exactly this |

### ⚠️ "Weak AI" is used in two different senses, and the exam expects both

- In **Searle's** sense: weak = *simulating* thought, strong = *really*
  thinking. A philosophical distinction.
- In **common usage**: weak = narrow, strong = general. A capability
  distinction.

**Say which sense you are using.** A good answer gives both tables and notes
that the terms overlap confusingly — that observation is itself worth a mark.

---

## 1.3 Applications of AI

| Domain | Application | Technique |
|---|---|---|
| Healthcare | Diagnosis from images; drug discovery; **triage expert systems** | Vision, expert systems |
| Finance | Fraud detection, algorithmic trading, credit scoring | Classification |
| Transport | Self-driving, route planning, traffic control | **Search**, vision, RL |
| Language | Translation, chatbots, summarisation | NLP |
| Games | Chess, Go, poker | **Search + evaluation**, RL |
| Robotics | Manufacturing, surgery, warehouses | Planning, control |
| Agriculture | Yield prediction, disease detection, irrigation | Vision, regression |
| Education | Adaptive tutoring, automated grading | Modelling, NLP |

### 💡 Notice which of these are *this* course

**Route planning, game playing and puzzle solving are search** (Units 2–3).
**Diagnosis and triage are expert systems** (Unit 5). Those are the
applications to name when the question is about *this* course rather than AI in
general.

---

## 1.4 Intelligent agents

Two questions, in order: what *is* an agent, and what is the **structure of agents** — the internal organisation that turns percepts into actions.

### 🎯 The definition

**An agent is anything that perceives its environment through sensors and acts
on it through actuators.**

```
        ┌──────────────────────────────────┐
        │            AGENT                 │
        │   ┌────────────────────────┐     │
   ─────┼──►│  agent function        │     │
 percepts   │  f : percept* → action │     │
        │   └───────────┬────────────┘     │
        │               ▼                  │
        │           actions ───────────────┼─────►
        └──────────────────────────────────┘
                    ENVIRONMENT
```

| Term | Means |
|---|---|
| **Percept** | One input at one instant |
| **Percept sequence** | Everything perceived so far |
| **Agent function** | The mapping from percept sequence to action — abstract |
| **Agent program** | The **implementation** of that function — concrete, finite |
| **Actuator** | What the agent acts with |

⚠️ **The agent function is the specification; the agent program is the code.**
The function is a mathematical object, potentially an infinite table; the
program is what you actually write. That distinction is a two-mark question.

### 🔢 Rationality

> **A rational agent selects, for each percept sequence, the action expected to
> maximise its performance measure, given the evidence provided by the percept
> sequence and whatever built-in knowledge it has.**

Four things it depends on, and the definition names all four:

1. The **performance measure**
2. The agent's **prior knowledge** of the environment
3. The **actions** available
4. The **percept sequence** to date

### ⚠️ Rational is not omniscient, and this is examined

| | Means |
|---|---|
| **Omniscient** | Knows the *actual* outcome. **Impossible** |
| **Rational** | Maximises *expected* performance, given what is knowable |

**Crossing a road after looking both ways is rational even if a cargo door
falls from a passing aeroplane and kills you.** Rationality is about the
decision, not the outcome — and that example is worth using, because it makes
the point instantly.

Two related ideas:

- **Information gathering** — doing something to improve your percepts (looking
  before crossing) is rational.
- **Learning** — a rational agent should improve from experience, rather than
  relying only on built-in knowledge. An agent that cannot is said to lack
  **autonomy**.

### 🔢 The five agent types — a guaranteed exam question

| Type | Decides from | Keeps state? | Handles |
|---|---|---|---|
| **Simple reflex** | The **current percept only** — condition–action rules | **No** | Fully observable environments only |
| **Model-based reflex** | Percept **+ internal state** of how the world evolves | **Yes** | **Partial observability** |
| **Goal-based** | State **+ a goal** — needs search or planning | Yes | Choosing between actions toward a goal |
| **Utility-based** | State + a **utility function** over outcomes | Yes | **Conflicting goals**, and degrees of success |
| **Learning** | Any of the above, **plus improvement from experience** | Yes | Unknown environments |

### 💡 The progression, and why each step was needed

- **Simple reflex** fails the moment the right action depends on something not
  currently visible. A vacuum agent that cannot see the other square loops for
  ever.
- **Model-based** fixes that by remembering — an internal model of how the
  world evolves and how actions affect it.
- **Goal-based** is needed because knowing the state does not say what to *do*.
  This is where **search** enters, and where Units 2 and 3 live.
- **Utility-based** is needed because goals are binary — reached or not — and
  real problems have **trade-offs**: fastest route versus safest versus
  cheapest. A utility function makes them comparable.
- **Learning** is needed because you cannot programme every situation in
  advance.

### 🔢 The learning agent's four components

| Component | Does |
|---|---|
| **Learning element** | Makes improvements |
| **Performance element** | Selects actions — this is "the agent" in the earlier sense |
| **Critic** | Reports how well the agent is doing against a **fixed standard** |
| **Problem generator** | Suggests **exploratory** actions — deliberately suboptimal, to learn something |

**The problem generator is the one people forget**, and it is the interesting
one: without deliberate exploration the agent only ever refines what it already
does. That is the exploration–exploitation trade-off of Course 12 A §1.3,
arriving from the other direction.

---

## 1.5 PEAS

### 🔢 The specification every agent design starts with

| Letter | Stands for | Answers |
|---|---|---|
| **P** | **Performance measure** | What counts as doing well? |
| **E** | **Environment** | What is it operating in? |
| **A** | **Actuators** | What can it do? |
| **S** | **Sensors** | What can it perceive? |

### 🔢 Worked examples — learn two properly

**An automated taxi driver:**

| | |
|---|---|
| **P** | Safety, legality, speed, comfort, fuel economy, profit |
| **E** | Roads, other traffic, pedestrians, weather, signs, passengers |
| **A** | Steering, accelerator, brake, indicators, horn, display |
| **S** | Cameras, LIDAR, GPS, speedometer, accelerometer, engine sensors |

**A medical diagnosis expert system:**

| | |
|---|---|
| **P** | Correct diagnosis, patient health, cost, time to diagnosis |
| **E** | Patient, hospital staff, test facilities |
| **A** | Questions, test requests, diagnoses, treatment recommendations |
| **S** | Typed symptoms, test results, patient history |

### ⚠️ The performance measure is the hard part, and the exam knows it

**Design it for what you want in the environment, not for how you think the
agent should behave.**

The standard example: reward a vacuum agent for the amount of dirt collected,
and a rational agent will **dump the dirt out and collect it again**. It is
maximising exactly what you asked for. Reward *a clean floor* instead.

**This is the alignment problem in miniature**, and it connects to Unit 5's AI
ethics. Worth stating.

---

## 1.6 Environment properties

### 🔢 The seven dimensions

| Dimension | | | Example of the harder case |
|---|---|---|---|
| **Observability** | **Fully** — sensors give the complete state | **Partially** — some state hidden | Poker: you cannot see other hands |
| **Determinism** | **Deterministic** — next state fixed by current state and action | **Stochastic** — probabilistic | Driving: a tyre may burst |
| **Episodic vs sequential** | **Episodic** — each decision independent | **Sequential** — actions have long-term consequences | Chess: an early move decides the endgame |
| **Static vs dynamic** | **Static** — unchanged while you deliberate | **Dynamic** — changes while you think | Driving: traffic does not wait |
| **Discrete vs continuous** | **Discrete** — finite states and actions | **Continuous** | Steering angle, speed |
| **Single vs multi-agent** | **Single** | **Multi** — competitive or cooperative | Chess (competitive), driving (both) |
| **Known vs unknown** | The **rules** are known | The rules must be learned | A new game |

### ⚠️ Two distinctions that get confused

- **Known ≠ observable.** *Known* is about whether **you** understand the
  rules; *observable* is about whether **the sensors** show the state. A new
  board game with everything visible is **fully observable but unknown**; solitaire
  played by an expert is **known but partially observable**.
- **Deterministic ≠ certain to succeed.** *Stochastic* means genuinely
  probabilistic outcomes. An environment that is deterministic but partially
  observable can *look* stochastic from inside — and Russell and Norvig call
  that **nondeterministic** rather than stochastic.

### 🔢 The classification table

| Environment | Observable | Deterministic | Episodic | Static | Discrete | Agents |
|---|---|---|---|---|---|---|
| **Crossword** | Fully | Deterministic | Sequential | Static | Discrete | Single |
| **Chess with a clock** | Fully | Deterministic | Sequential | **Semi** | Discrete | **Multi** |
| **Poker** | **Partially** | **Stochastic** | Sequential | Static | Discrete | **Multi** |
| **Taxi driving** | **Partially** | **Stochastic** | Sequential | **Dynamic** | **Continuous** | **Multi** |
| Medical diagnosis | Partially | Stochastic | Sequential | Dynamic | Continuous | Single |
| Image classification | Fully | Deterministic | **Episodic** | Semi | Continuous | Single |

**Taxi driving is the hardest case on every dimension**, which is why it is the
standard example — and why it is still not solved.

### 💡 Why this classification matters, rather than being taxonomy

**It tells you which algorithms are even applicable.**

- Fully observable, deterministic, discrete, static → **the search of Units 2
  and 3 works directly**.
- Partially observable → you need **belief states** or a model.
- Stochastic → you need **probability** (Unit 5) and expected utility.
- Multi-agent → you need **game-theoretic search** — minimax, alpha–beta.

**Say that in the exam.** The table alone is description; the consequence is
the answer.

---

## Practice problems

### Problem 1

What is the Turing Test? Explain its structure, what it requires, and the main
criticisms. *(10 marks)*

**Solution.**

**The setup:** a human interrogator converses **by text** with two respondents,
one human and one machine. If the interrogator cannot reliably tell which is
which, the machine passes. Turing proposed it in **1950** to replace the
unanswerable "can machines think?" with an operational question.

**What passing requires:** natural language processing, knowledge
representation, automated reasoning and machine learning — plus, in the
**Total** Turing Test, computer vision and robotics.

**The criticisms, and give at least three:**

1. **It tests imitation, not intelligence.** ELIZA (1966) fooled people with
   pattern substitution and no understanding.
2. **Searle's Chinese Room:** a person following rule-books to manipulate
   Chinese symbols could pass while understanding nothing, so behaviour does
   not establish understanding.
3. **It is anthropocentric.** Aircraft do not flap; requiring
   indistinguishability from humans is not a useful engineering target.
4. **It is not a research programme.** No serious system is built by aiming at
   it.

**Conclude maturely:** its value is historical and philosophical. The field
pursues **acting rationally** instead, because that is measurable, more general
than logic, and does not require consciousness.

### Problem 2

Explain the five types of intelligent agent, and why each was needed.
*(10 marks)*

**Solution.**

Give the table — simple reflex, model-based reflex, goal-based, utility-based,
learning — with what each decides from and whether it keeps internal state.

**Then the progression, which is the part that earns the marks:**

- **Simple reflex** acts on the current percept alone via condition–action
  rules. It fails the moment the right action depends on something not
  currently visible — a vacuum agent that cannot see the other square loops
  for ever.
- **Model-based** fixes that with an internal state plus a model of how the
  world evolves and how actions affect it. It handles **partial
  observability**.
- **Goal-based** is needed because knowing the state does not say what to do.
  **This is where search enters**, and it is Units 2 and 3.
- **Utility-based** is needed because goals are binary while real problems have
  trade-offs — fastest against safest against cheapest. A utility function
  makes outcomes comparable.
- **Learning** is needed because you cannot programme every situation in
  advance.

Finish with the learning agent's four components — **learning element,
performance element, critic, problem generator** — and note that the problem
generator deliberately suggests *suboptimal* exploratory actions, because
without exploration the agent only refines what it already does.

### Problem 3

What is PEAS? Give the PEAS description of an automated taxi. Why is the
performance measure the hard part? *(10 marks)*

**Solution.**

**PEAS** specifies an agent's task environment: **Performance measure,
Environment, Actuators, Sensors**.

Give the taxi table in full — P: safety, legality, speed, comfort, fuel
economy, profit; E: roads, traffic, pedestrians, weather, signs, passengers;
A: steering, accelerator, brake, indicators, horn, display; S: cameras, LIDAR,
GPS, speedometer, engine sensors.

**Then classify the environment** and note it is the hardest case on every
dimension: partially observable, stochastic, sequential, **dynamic**,
**continuous**, multi-agent.

**Why the performance measure is hard:** design it for **what you want in the
environment**, not for how you think the agent should behave. Reward a vacuum
agent for dirt collected and a rational agent will **dump the dirt out and
collect it again** — it is maximising exactly what you asked for. Reward *a
clean floor* instead.

**That is the alignment problem in miniature**, and it links to Unit 5's ethics
material. Note too that the taxi's own measures conflict — speed against
safety against comfort — which is precisely why a taxi needs a **utility-based**
agent rather than a goal-based one.

---

## Exam questions from this unit

**Two marks**

1. Who coined the term "Artificial Intelligence", and when?
2. What is the difference between an agent function and an agent program?
3. Define a rational agent.
4. What does PEAS stand for?
5. Give one example of a partially observable environment.
6. What is the difference between narrow and general AI?
7. What does the problem generator do in a learning agent?

**Five marks**

1. Explain the four approaches to defining AI.
2. Explain the Turing Test and two criticisms of it.
3. Distinguish weak AI from strong AI, and narrow from general.
4. Explain the properties of task environments with examples.
5. Explain rationality, and why a rational agent is not omniscient.
6. Give the PEAS description of a medical diagnosis system.

**Ten marks**

1. Explain the Turing Test, what it requires and its criticisms.
2. Explain the five agent types and why each was needed.
3. Explain PEAS with a worked example, and why the performance measure is hard.
4. Classify six environments across all seven dimensions, and explain what the
   classification implies for algorithm choice.

---

## Mistakes that cost marks

- **Confusing weak/strong with narrow/general.** They are different axes, and
  "weak AI" has two established meanings. Say which you mean.
- **Saying a rational agent always succeeds.** It maximises **expected**
  performance. Looking both ways is rational even if you are still hit.
- **Giving four agent types.** There are five; the learning agent is usually
  the one dropped.
- **PEAS with a vague performance measure.** "Drive well" earns nothing;
  "safety, legality, speed, comfort, fuel economy, profit" earns the mark.
- **Confusing "known" with "observable".** Known is about the rules; observable
  is about the sensors.
- **Listing environment properties with no consequence.** The table is
  description; *which algorithms become applicable* is the answer.
- **Dating the Turing Test to the Dartmouth Conference.** Turing 1950;
  Dartmouth 1956.
