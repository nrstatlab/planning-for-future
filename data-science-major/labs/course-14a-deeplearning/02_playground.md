# Experiment 2 -- TensorFlow Playground and Google Teachable Machine

## *** NOT EXECUTED ***

Both of these are **interactive web applications**. There is no output to
capture and no assertion to run: the whole point of them is that you drag a
slider and watch a decision boundary move. A transcript of that is worthless.

So this file is the **experiment protocol** -- what to set, what to look for,
and what number to write in your record. **It has never been run here**, and
nothing in the notes claims an output for it.

The runnable half is **`01_perceptron_scratch.py`**, which reproduces the two
results Playground exists to show you -- that one linear unit cannot separate
XOR, and that one hidden layer can -- with the arithmetic visible.

---

## Part A -- TensorFlow Playground

<https://playground.tensorflow.org>

The page is a small neural network trained in your browser. Left column
picks the dataset, middle builds the network, right shows the output.

### A1. The result you already proved in `01_perceptron_scratch.py`

| Set | To |
|---|---|
| Dataset | **Exclusive or** (the checkerboard, top-right) |
| Features | `X1` and `X2` **only** -- switch the other five off |
| Hidden layers | **0** |
| Learning rate | 0.03, Activation Tanh, Regularization None |

Press play. Watch the **Test loss** number.

**What to record:** the test loss after 500 epochs, and the shape of the
background. You should see the loss stall near **0.5** and the background
stay a single flat colour split by one straight line.

That is the XOR result. `01_perceptron_scratch.py` prints the same failure as
`accuracy 0.50, converged: NEVER`.

### A2. Now add the hidden layer

Same settings, but set **hidden layers to 1 with 4 neurons**. Press play.

**What to record:** the epoch at which test loss first drops below 0.05, and
the background shape. You should get four coloured quadrants -- the network
has bent the boundary.

**The thing worth staring at:** click each hidden neuron. Each one has learned
*one straight line*. The output layer combines four straight lines into a
curved region. That is the entire idea of a hidden layer, and it is much
clearer here than in any equation.

### A3. The feature-engineering point

Go back to **0 hidden layers**, but now switch on the **X1X2** feature.

Test loss collapses. A linear model on the *product* feature solves XOR
instantly, because `X1X2` is exactly the term that separates it.

**What to record:** test loss with `X1X2` on, 0 hidden layers.

> **This is the most important cell in the whole exercise.** A hidden layer
> is a machine for *discovering* features like `X1X2`. If you already know
> the right feature, you do not need the depth. Deep learning is what you
> reach for when you cannot name the feature yourself.

### A4. Overfitting, visibly

| Set | To |
|---|---|
| Dataset | **Circle** |
| Ratio of training to test data | **10%** |
| Noise | **50** |
| Hidden layers | 4 layers of 8 |

Run to 1000 epochs. **Record training loss and test loss separately.** The
training loss keeps falling; the test loss bottoms out and then *rises*. The
background grows islands of colour around individual noise points.

That gap is overfitting, and `04_deep_network.py` measures the same gap
numerically (`train 1.0000  test 0.9867  gap 0.0133`, then the dropout rows).

### A5. The activation comparison

Dataset **Spiral**, 4 hidden layers of 8, and run each activation:

| Activation | Record test loss at 1000 epochs |
|---|---|
| ReLU | |
| Tanh | |
| Sigmoid | |
| Linear | |

**Linear will fail completely** and it is worth understanding why before you
run it: a stack of linear layers is *itself* a single linear layer, so four
layers of Linear has exactly the power of no hidden layer at all.
`01_perceptron_scratch.py` states the same fact; here you can watch it.

**Sigmoid will train much more slowly than ReLU.** That is the vanishing
gradient, and `01_perceptron_scratch.py` prints the arithmetic behind it --
`0.25^50 = 7.89e-31` in the best case for sigmoid, against `1.0` for ReLU.

---

## Part B -- Google Teachable Machine

<https://teachablemachine.withgoogle.com>

Choose **Image Project → Standard image model**.

### B1. Train it

1. Rename Class 1 to `thumbs_up` and Class 2 to `thumbs_down`.
2. Hold the pose, press and hold **Webcam** to capture. **About 50 images
   per class.** Vary distance and angle while you hold.
3. Press **Train Model**. It takes a few seconds.
4. Test it live in the preview panel.

**What to record:** click **Under the hood** after training and note the
per-class accuracy and the confusion matrix.

### B2. The experiment that teaches something

Add a **third class** with only **5 images**. Retrain.

**What to record:** the accuracy of the 5-image class against the 50-image
classes. It will be markedly worse, and the model will be biased *towards*
the well-represented classes.

That is class imbalance, and it is the single most common reason a student
project reports 95% accuracy and is useless.

### B3. Now break it deliberately

Capture all 50 `thumbs_up` images in front of a window and all 50
`thumbs_down` images in front of a dark wall. Retrain. It will look perfect.

Now swap the backgrounds and test again. **Accuracy collapses.**

The model learned *the background*, not the hand. Record both numbers and
write one sentence on what that implies for any dataset you did not collect
yourself.

> This is the failure mode behind the well-known tank story and behind a
> string of real medical-imaging papers that turned out to be detecting which
> hospital took the scan. It costs five minutes to reproduce and you will
> not forget it.

### B4. Connect it back to the code

Teachable Machine is doing **transfer learning on MobileNet** -- it keeps the
pre-trained convolutional features and trains only a small head on your
images. That is why 50 images is enough and why training takes seconds.

`06_cnn.py` experiment 8 does exactly this mechanism with code you can read:
pre-train on 1,280 shapes, freeze the convolutions, train a new head on 80
noisy images, and measure **0.9125 with transfer against 0.7937 from
scratch**.

---

## What goes in the lab record

| Item | Value |
|---|---|
| A1 XOR, 0 hidden layers, test loss | |
| A2 XOR, 1 hidden layer of 4, epochs to loss < 0.05 | |
| A3 XOR, 0 hidden layers, `X1X2` on, test loss | |
| A4 Circle 50% noise, train loss vs test loss at 1000 epochs | |
| A5 Spiral test loss: ReLU / Tanh / Sigmoid / Linear | |
| B1 two-class accuracy, 50 images each | |
| B2 accuracy of the 5-image class | |
| B3 accuracy before and after swapping backgrounds | |

One paragraph, in your own words: **why did A3 beat A1 without any hidden
layer, and what does that tell you about when depth is worth its cost?**
