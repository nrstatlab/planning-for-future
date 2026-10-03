# -*- coding: utf-8 -*-
"""Data Handling using R: the eight prescribed analyses, on one data set of twenty records.

Built by build_r_practical.py dh_data. Every programme starts from the same customers data
frame (the prelude), so each can be copied and run as it stands.
"""
PAGE = "statistics/data-handling-using-r/practical.html"
TITLE = "Practical — Data Handling using R (STS-108)"
DESC = ("The whole STS-108 workflow on one data set, each analysis set out as Question, Aim, Steps, Programme, "
        "and Execution and Results, with R's own output and plots.")

DATA = '''customers <- data.frame(
  id     = 1:20,
  age    = c(23,45,31,58,27,39,52,34,29,48,36,41,25,55,33,44,30,50,28,38),
  income = c(40,57,37,69,36,38,63,32,35,57,42,49,26,39,48,49,23,57,27,33),
  score  = c(54,55,64,77,69,60,85,57,65,59,64,60,51,57,60,60,55,67,40,56),
  gender = factor(c("M","F","M","F","M","F","M","F","M","F",
                    "M","F","M","F","M","F","M","F","M","F")),
  buy    = c(0,1,0,1,1,0,1,0,0,1,0,0,0,0,1,1,0,1,0,0)
)
customers$grade <- cut(customers$score, breaks = c(-Inf, 57, 65, Inf),
                       labels = c("Low","Med","High"), right = FALSE)
customers$buy <- factor(customers$buy, levels = c(0,1), labels = c("No","Yes"))'''

ESC = lambda t: t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

HEAD = """<div class="wrapper">

  <div class="banner">
    <div class="crumbs"><a href="index.html">Home</a> &raquo; Practical</div>
    <h1>Practical &mdash; Data Handling using R (STS-108)</h1>
    <p>The whole STS-108 workflow on one data set: measurement scales and what each permits, pre-processing in order, six data transformations judged by what they do to the skewness, the full prescribed list of diagrams, model building with 5-fold and leave-one-out cross-validation showing over-fitting measured, the confusion matrix and the ratios from it, the parametric tests in the order they must be run, and five non-parametric tests compared. Each analysis is set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and Results.</p>
  </div>

  <h2>Topics Covered</h2>
  <div class="chips">
    <span class="chip">Measurement Scales</span>
    <span class="chip">Pre-processing</span>
    <span class="chip">Transformations</span>
    <span class="chip">Visualization</span>
    <span class="chip">Cross-Validation</span>
    <span class="chip">Over-fitting</span>
    <span class="chip">Confusion Matrix</span>
    <span class="chip">ROC &amp; AUC</span>
    <span class="chip">Parametric Tests</span>
    <span class="chip">Non-Parametric Tests</span>
    <span class="chip">Statistical Report</span>
  </div>

<details class="toc">
  <summary>On this page</summary>
  <ol>
{toc}
  </ol>
</details>
  <div class="tip">
    <strong>About this course.</strong> STS-108 is a <strong>practical</strong> whose
    stated outcome is a single sentence: <em>&ldquo;Able to carry out the Statistical Analysis and
    writing statistical Report using R for any dataset.&rdquo;</em> It is not a list of programs
    but a workflow, and these pages follow it end to end on one data set of twenty records.
  </div>

  <div class="tip">
    <strong>R itself is not taught here, and neither is most of the statistics.</strong> Both are
    already on this site and are linked, not repeated:
    <ul>
      <li><a href="../computational-statistics-and-r-programming/unit1.html">Computational
      Statistics and R Programming, Unit 1</a> &mdash; the R environment, language basics, data
      types, import and export, missing values, subsetting, merging, the apply family and the
      working directory</li>
      <li><a href="../computational-statistics-and-r-programming/unit2.html">Unit 2</a> &mdash;
      central tendency, variability, quantiles, skewness and kurtosis, the summary functions and
      categorical data</li>
      <li><a href="../computational-statistics-and-r-programming/unit3.html">Unit 3</a> &mdash;
      histograms, boxplots, scatter plots, bar charts, residual plots and saving a plot</li>
      <li><a href="../computational-statistics-and-r-programming/unit4.html">Unit 4</a> &mdash;
      distributions, random sampling, \\(t\\) tests, \\(\\chi^{2}\\) tests, one-way analysis of
      variance, \\(p\\) values, confidence intervals and the Wilcoxon tests</li>
      <li><a href="../computational-statistics-and-r-programming/unit5.html">Unit 5</a> &mdash;
      correlation, simple and multiple regression and residual diagnostics</li>
    </ul>
    <strong>This course begins where those units stop.</strong> Five of its eight prescribed topics
    are not in them at all &mdash; measurement scales and what each permits, data transformations,
    the diagrams beyond the standard four, model building with cross-validation, and the evaluation
    of model performance &mdash; and three of the five non-parametric tests it names are new. Those
    are what is written out below.
  </div>

  <div class="tip">
    <strong>About the numbers.</strong> Every output and plot under Execution and Results was produced by running the
    programme shown, in R {version}. Where R's own convention matters &mdash; type 7 quantiles, the \\(n-1\\) divisor in
    <code>var</code>, the continuity correction in <code>wilcox.test</code> &mdash; it is named.
  </div>

  <h2 id="the-data-set">The Data Set</h2>

  <div class="concept">
    <span class="label">TWENTY RECORDS, SIX VARIABLES</span>
    <p>One data set carries the whole course, so that each stage can be checked against the last.
    <code>grade</code> is derived from <code>score</code> and <code>buy</code> is the outcome the
    classification analysis predicts. Every programme below begins with these lines.</p>
    <pre><code>""" + ESC(DATA) + """</code></pre>
    <p><strong>Note <code>right = FALSE</code>.</strong> R's <code>cut</code> closes intervals on
    the right by default, so <code>breaks = c(-Inf, 57, 65, Inf)</code> without it would put a
    score of exactly 57 in the <em>Low</em> class. Boundary cases are where derived categorical
    variables go wrong, and they go wrong silently.</p>
  </div>

"""

P = []
def add(n, title, question, aim, commands, steps, conclusion, notes=()):
    P.append(dict(n=n, title=title, question=question, aim=aim, commands=commands, steps=steps,
                  notes=list(notes), conclusion=conclusion, prelude=DATA, prelude_title="The data set: twenty records"))

add(1, "Understanding the Data Set",
"""<p>For the <code>customers</code> data, place each variable on its scale of measurement, declare the ordinal
variable so that R refuses the wrong operations, and carry out the pre-processing checks for missing values and
duplicates.</p>""",
"To identify the scale of each variable, which decides the operations that mean anything, and to check the data before any analysis.",
[("<code>str()</code>, <code>sapply(d, class)</code>", "the structure and R's storage class of each column"),
 ("<code>factor(x, levels, ordered = TRUE)</code>", "an ordinal variable: order is kept, arithmetic is refused"),
 ("<code>colSums(is.na(d))</code>, <code>duplicated(key)</code>", "missing values per column; repeated keys")],
[("Inspect the structure, and the counts of each category",
  """<p>R's class is not the scale. "numeric" covers <code>age</code> (ratio) and <code>score</code> (interval);
"factor" covers <code>gender</code> (nominal) and <code>grade</code> (ordinal).</p>
  <table>
    <tr><th>Scale</th><th>Distinguishes</th><th>Legitimate summaries</th><th>Here</th></tr>
    <tr><td>Nominal</td><td>difference only</td><td>counts, mode, \\(\\chi^{2}\\)</td><td><code>gender</code>, <code>buy</code></td></tr>
    <tr><td>Ordinal</td><td>difference and order</td><td>median, quartiles, rank correlation, rank tests</td><td><code>grade</code></td></tr>
    <tr><td>Interval</td><td>order and equal spacing, arbitrary zero</td><td>mean, standard deviation, correlation &mdash; but <em>not</em> ratios</td><td><code>score</code>, treated as interval</td></tr>
    <tr><td>Ratio</td><td>all of the above, plus a true zero</td><td>everything, including the coefficient of variation and the geometric mean</td><td><code>age</code>, <code>income</code></td></tr>
  </table>""",
  'str(customers)\nsapply(customers, class)\ntable(customers$grade); table(customers$gender); table(customers$buy)', {}),
 ("Declare grade ordinal, and see what R then allows",
  """<p>Coding <code>grade</code> 1, 2, 3 and taking a mean produces a number, and the number is meaningless: nothing
says the step from Low to Med equals the step from Med to High. Declared ordered, the median is found by
<code>quantile()</code> and the mean is refused.</p>""",
  'customers$grade <- factor(customers$grade, levels = c("Low","Med","High"), ordered = TRUE)\nquantile(customers$grade, 0.5, type = 1)   # the median of an ordered factor\nmean(customers$grade)', {}),
 ("Pre-processing checks: missing values and duplicates",
  """<p>The checks come in a fixed order: read and inspect; fix types; count missing values and decide (drop,
impute, and by what); identify outliers without deleting them; check duplicates on the key; only then derive and
transform; and split before anything is estimated if a model is to be fitted.</p>""",
  'colSums(is.na(customers))\nsum(duplicated(customers$id))\nsapply(customers, function(v) sum(is.na(v)))    # works for any data frame', {})],
"""<p>The twenty records hold two ratio variables (<code>age</code>, <code>income</code>), one interval
(<code>score</code>), one ordinal (<code>grade</code>: Low 6, Med 9, High 5) and two nominal (<code>gender</code>: 10 and
10; <code>buy</code>: No 12, Yes 8). There are no missing values and no duplicate keys. Declared ordered, <code>grade</code>
has median <em>Med</em>, and R refuses its mean &mdash; it returns <code>NA</code> with a warning &mdash; which is the
right answer to a meaningless question.</p>""",
["<code>mean()</code> of a factor is not an error in R: it returns <code>NA</code> and warns that the argument is not "
 "numeric or logical. The warning is the refusal; a script that ignores warnings will carry the <code>NA</code> on.",
 "<code>median()</code> refuses a factor, even an ordered one, with the error \"need numeric data\". The median of an "
 "ordered factor is <code>quantile(x, 0.5, type = 1)</code> (types 1 and 3 are the quantile rules that pick an observed "
 "value rather than interpolate between two)."])

add(2, "Data Transformations",
"""<p>Apply standardization, min&ndash;max normalization, and the log, square-root and square transformations to
<code>income</code>, judging each by what it does to the skewness; and encode a cyclic variable (month) by its sine
and cosine.</p>""",
"To choose a transformation by what it does to the data, and to see why a cyclic variable needs two columns.",
[("Standardization", "\\((x-\\bar x)/s\\): mean 0, sd 1; for variables on different units in one model or distance"),
 ("Normalization", "\\((x-\\min)/(\\max-\\min)\\): range \\([0,1]\\); for a bounded input"),
 ("Log, square root", "\\(\\ln x\\) (\\(x &gt; 0\\)), \\(\\sqrt x\\) (\\(x \\ge 0\\)): reduce right skew, the root more mildly"),
 ("Square", "\\(x^{2}\\): reduces <em>left</em> skew"),
 ("Sine and cosine", "\\(\\sin(2\\pi x/p)\\), \\(\\cos(2\\pi x/p)\\): a cyclic variable of period \\(p\\), as a <em>pair</em>"),
 ("Skewness", "\\(m_3/m_2^{3/2}\\), the moment definition")],
[("Skewness of income under each transformation", "<p>Judge a transformation by what it does to the skewness, not by habit.</p>",
  'skewness <- function(x) {          # no package: the moment definition\n  m <- mean(x); n <- length(x)\n  (sum((x - m)^3)/n) / (sum((x - m)^2)/n)^1.5\n}\nround(c(raw = skewness(customers$income), log = skewness(log(customers$income)),\n        sqrt = skewness(sqrt(customers$income)), square = skewness(customers$income^2)), 6)', {}),
 ("Standardization and normalization, written out and checked",
  "<p><code>z</code> uses R's <code>sd</code>, which divides by \\(n-1\\); <code>scale()</code> does the same and returns a <em>matrix</em>, not a vector.</p>",
  'z  <- (customers$income - mean(customers$income)) / sd(customers$income)\nmm <- (customers$income - min(customers$income)) /\n      (max(customers$income) - min(customers$income))\nround(c(mean = mean(z), sd = sd(z), min = min(mm), max = max(mm)), 6)\nround(c(z[2], mm[2], z[13], mm[13]), 6)\nisTRUE(all.equal(as.vector(scale(customers$income)), z))', {}),
 ("A cyclic variable: distances between months",
  "<p>Month 1 and month 12 are one month apart, but as numbers eleven. Mapped onto a circle, with both coordinates &mdash; \\(\\sin\\) alone cannot separate month 3 from month 9 &mdash; the distances come right.</p>",
  'cyc <- function(m, period = 12) cbind(s = sin(2*pi*m/period), c = cos(2*pi*m/period))\nd <- function(a, b) sqrt(sum((cyc(a) - cyc(b))^2))\nround(c("1 to 12" = d(1, 12), "1 to 2" = d(1, 2), "1 to 6" = d(1, 6)), 6)', {})],
"""<p><code>income</code> is only mildly right-skewed (0.387). The square root leaves 0.148 and is the best here; the
log over-corrects to &minus;0.108, and squaring makes it worse (0.823). <strong>Reach for the mildest transformation that
does the job</strong>, because every transformation costs interpretability. Standardized income has mean 0 and sd 1;
normalized income runs from 0 to 1. On the circle, month 1 is as close to month 12 as to month 2 (0.518), and month 6
is the farthest (1.932).</p>""",
["Dividing by \\(n\\) instead of \\(n-1\\) gives standardized values about 2.6% larger at \\(n = 20\\). Say which you used."])

add(3, "Descriptive Statistics by Scale",
"""<p>Summarise each variable of <code>customers</code> with the measures its scale permits.</p>""",
"To choose each summary by the variable's scale of measurement, not by whether R will compute it.",
[("<code>summary()</code>, <code>sd()</code>, <code>IQR()</code>", "location and spread of the interval and ratio variables"),
 ("<code>quantile(x)</code>", "quartiles, by R's type 7 rule: interpolating at \\(h = (n-1)p\\)"),
 ("<code>table()</code>", "the only summary a nominal scale allows"),
 ("<code>quantile(g, p, type = 1)</code> of an ordered factor", "the median and quartiles, the summaries an ordinal scale allows")],
[("The interval and ratio variables", "", 'summary(customers[c("age","income","score")])\nround(sapply(customers[c("age","income","score")], sd), 4)\nskewness <- function(x) { m <- mean(x); (mean((x - m)^3)) / (mean((x - m)^2))^1.5 }\nround(sapply(customers[c("age","income","score")], skewness), 4)', {}),
 ("Quartiles, and R's convention", "<p>Nine quantile definitions exist; R's default, type 7, is not the one most textbooks use. State it, or the numbers cannot be reproduced.</p>",
  'quantile(customers$income)\nIQR(customers$age)', {}),
 ("The ordinal and nominal variables", "", 'customers$grade <- factor(customers$grade, ordered = TRUE)\nquantile(customers$grade, c(0.25, 0.5, 0.75), type = 1)\ntable(customers$gender)', {})],
"""<p>Age has mean 38.30 and median 37.0 (sd 10.45); income 42.85 and 39.5 (sd 12.83); score 60.75 and 60.0 (sd 9.44).
All three are mildly right-skewed &mdash; mean above median in every case &mdash; which is what a mean and a median printed
side by side are for. <code>grade</code> has median <em>Med</em>; <code>gender</code> is summarised only by its counts,
10 and 10. The quartiles of <code>grade</code> are Low and Med.</p>""")

VIZ = '''op <- par(mfrow = c(2, 3))
pie(table(customers$grade), main = "Grade")                    # parts of a whole
h <- hist(customers$score, plot = FALSE)
plot(h$mids, h$counts, type = "b", main = "Frequency polygon", xlab = "score", ylab = "frequency")
cf <- cumsum(h$counts)                                          # the ogive
plot(h$breaks[-1], cf, type = "b", main = "Ogive", xlab = "score", ylab = "cumulative frequency")
plot(customers$id, cumsum(customers$income), type = "n",       # area chart
     main = "Cumulative income", xlab = "record", ylab = "total")
polygon(c(1, customers$id, 20), c(0, cumsum(customers$income), 0), col = "grey80")
st <- c(1, 3, 2, 6, 5); en <- c(5, 7, 9, 10, 12)               # Gantt chart
plot(NA, xlim = c(0, 13), ylim = c(0.5, 5.5), yaxt = "n", main = "Gantt", xlab = "week", ylab = "task")
segments(st, 1:5, en, 1:5, lwd = 10, col = "steelblue")
axis(2, at = 1:5, labels = paste("T", 1:5, sep = ""))
M <- cor(customers[c("age","income","score")])                 # heat map of a correlation matrix
image(1:3, 1:3, M, axes = FALSE, main = "Correlation heat map", xlab = "", ylab = "")
axis(1, 1:3, colnames(M)); axis(2, 1:3, colnames(M))
par(op)'''
add(4, "Data Visualization",
"""<p>Draw, from the <code>customers</code> data, the diagrams of the prescribed list that the standard four do not
cover &mdash; pie chart, frequency polygon, ogive, area chart, Gantt chart and heat map &mdash; and give the correlation
matrix the heat map shows.</p>""",
"To draw each prescribed diagram for the kind of data it suits, and to report the numbers a picture only points to.",
[("Histogram, boxplot, scatter, bar", "<code>hist(x)</code>, <code>boxplot(y ~ g)</code>, <code>plot(x, y)</code>, <code>barplot(table(g))</code> (<a href=\"../computational-statistics-and-r-programming/unit3.html\">Unit 3</a>)"),
 ("Pie chart", "<code>pie(table(g))</code>: parts of one whole &mdash; and little else"),
 ("Line plot", "<code>plot(t, y, type = \"l\")</code>: an ordered sequence, usually time"),
 ("Frequency polygon, ogive", "<code>plot(mids, counts, type = \"b\")</code>; <code>plot(breaks, cumsum(counts), type = \"b\")</code>"),
 ("Area chart", "a line plot with the region filled: <code>polygon(...)</code>"),
 ("Gantt chart", "durations against a time axis: <code>segments(start, y, end, y)</code>"),
 ("Heat map, correlation plot", "<code>image(m)</code> or <code>heatmap(m)</code>; <code>pairs(df)</code> with <code>cor(df)</code>")],
[("The six diagrams, in base R", "", VIZ, dict(plot="dh-diagrams.png", size=(900, 620))),
 ("The correlation matrix, as numbers", "<p>A heat map shows where to look; the matrix is what goes in the report.</p>",
  'round(cor(customers[c("age","income","score")]), 6)\nround(cor(customers[c("age","income","score")], method = "spearman"), 6)', {})],
"""<p>The six diagrams are drawn above. Income is correlated 0.78 with age and 0.65 with score; age and score 0.51.
The Spearman correlations are a little lower (0.75, 0.53, 0.41). Two rules matter more than any chart library: a pie
chart with more than four or five slices cannot be read &mdash; use a bar chart; and a correlation matrix printed without
its sample size says nothing &mdash; \\(r = 0.5\\) on twenty records and on two thousand are different findings.</p>""")

CV = '''rmse <- function(y, yhat) sqrt(mean((y - yhat)^2))
cv <- function(d, k, degree = 1) {          # k-fold cross-validation, written out
  fold <- seq_len(nrow(d)) %% k
  sq <- c()
  for (f in unique(fold)) {
    tr <- d[fold != f, ]; te <- d[fold == f, ]
    mdl <- lm(score ~ poly(income, degree, raw = TRUE), data = tr)
    sq <- c(sq, (te$score - predict(mdl, te))^2)
  }
  sqrt(mean(sq))
}
deg <- c(1, 2, 3, 5, 8)
in_sample <- sapply(deg, function(g)
  rmse(customers$score, fitted(lm(score ~ poly(income, g, raw = TRUE), data = customers))))
data.frame(degree = deg, in_sample = round(in_sample, 4),
           cv5   = round(sapply(deg, function(g) cv(customers, 5, g)), 4),
           loocv = round(sapply(deg, function(g) cv(customers, nrow(customers), g)), 4))'''
add(5, "Mathematical Model Building",
"""<p>Model <code>score</code> on <code>income</code>; measure the fit three ways; compare polynomial models of increasing
degree by in-sample, 5-fold and leave-one-out cross-validated error; evaluate a hold-out split; and cross-tabulate
<code>gender</code> against <code>grade</code>.</p>""",
"To fit a model and then measure the gap between its fit to the data in hand and its fit to data it has not seen.",
[("<code>lm(y ~ x)</code>", "the least-squares fit; <code>poly(x, d, raw = TRUE)</code> for a polynomial of degree d"),
 ("RMSE, MAE, \\(\\sigma\\)", "\\(\\sqrt{SSE/n}\\); \\(\\frac1n\\sum|e|\\); \\(\\sqrt{SSE/(n-2)}\\), the residual standard deviation"),
 ("\\(k\\)-fold cross-validation", "fit on \\(k-1\\) folds, predict the held-out fold, pool the errors; \\(k = n\\) is leave-one-out"),
 ("<code>chisq.test(table)</code>, <code>fisher.test(table)</code>", "the test of a cross-tab; Fisher's is exact, for small expected counts")],
[("Fit the straight line and measure it three ways", "<p>Three error measures, three different divisors, three different numbers.</p>",
  'fit <- lm(score ~ income, data = customers)\ncoef(fit)\nround(c(R2 = summary(fit)$r.squared, adjR2 = summary(fit)$adj.r.squared,\n        RMSE = sqrt(mean(resid(fit)^2)), MAE = mean(abs(resid(fit))), sigma = summary(fit)$sigma), 6)', {}),
 ("Over-fitting and under-fitting, measured",
  "<p>The folds are fixed by <code>seq_len(n) %% k</code>, so every degree is scored on exactly the same partition.</p>",
  CV, {}),
 ("A hold-out split, done properly", "<p>The split comes <em>before</em> anything is estimated.</p>",
  'train <- customers[1:14, ]; test <- customers[15:20, ]\nm <- lm(score ~ income, data = train)\ncoef(m)\nround(c(train = rmse(train$score, predict(m, train)), test = rmse(test$score, predict(m, test))), 6)', {}),
 ("Cross-tabs: gender against grade", "", 'tab <- table(customers$gender, customers$grade); tab\nchisq.test(tab)\nchisq.test(tab)$expected\nround(prop.table(tab, 1), 3)\nfisher.test(tab)$p.value', {})],
"""<p>The straight line is \\(\\widehat{score} = 40.15 + 0.481\\,income\\), \\(R^{2} = 0.427\\). The in-sample error falls with
every added degree &mdash; it must &mdash; while the cross-validated error rises from degree 2 and then explodes: by degree 8
the curve passes almost through the points and predicts a held-out point with an error in the hundreds, or thousands,
on a scale whose whole range is 40 to 85. <strong>That divergence is over-fitting</strong>, and a model chosen by in-sample
error alone would have chosen degree 8. <strong>The straight line is the model.</strong> On the hold-out split its error is
7.23 on the data fitted and 6.81 on data never seen. The gender &times; grade table gives \\(\\chi^{2} = 1.87\\) on 2 d.f.
(\\(p = 0.39\\)), but every expected count is below 5 and R warns: the approximation does not hold, and Fisher's exact
test, \\(p = 0.52\\), is the one to quote &mdash; no evidence that grade depends on gender.</p>""",
["The degree-8 errors depend on the arithmetic: a raw polynomial of degree 8 on twenty points is so ill-conditioned "
 "that different software, or a different order of operations, gives different numbers in the hundreds or thousands. "
 "Only their size matters, and every route agrees on that.",
 "Three errors make a cross-validation meaningless: standardizing on the whole data before splitting, so the test "
 "fold's mean leaks into the training set; choosing the model on the test set and reporting the test error as if it "
 "were honest; and a different random partition for each model."])

add(6, "Evaluation of Model Performance",
"""<p>Predict <code>buy</code> from <code>income</code> by logistic regression, classify at a fitted probability of 0.5, and
evaluate the classifier by its confusion matrix, the ratios from it, the no-information rate and the AUC.</p>""",
"To evaluate a classifier quantitatively and qualitatively, and to judge its accuracy against the rate a model-free guess would score.",
[("<code>glm(y ~ x, family = binomial)</code>", "logistic regression; \\(e^{b}\\) is the odds ratio per unit of \\(x\\)"),
 ("Accuracy, precision, recall", "\\((TP+TN)/n\\); \\(TP/(TP+FP)\\); \\(TP/(TP+FN)\\)"),
 ("Specificity, \\(F_1\\)", "\\(TN/(TN+FP)\\); \\(2PR/(P+R)\\)"),
 ("AUC", "\\(P(\\hat p_{\\text{Yes}} &gt; \\hat p_{\\text{No}})\\): the share of (Yes, No) pairs ranked the right way round"),
 ("RMSE, MAE, \\(R^{2}\\), adjusted \\(R^{2}\\)", "for a numeric prediction: RMSE squares, so one large error dominates; adjusted \\(R^{2}\\) can fall, and is the one to compare models with")],
[("Fit the logistic regression", "", 'g <- glm(buy ~ income, data = customers, family = binomial)\ncoef(g)\nexp(coef(g)["income"])            # the odds multiply by this per unit of income\n-coef(g)[1] / coef(g)[2]           # the income at which the fitted probability is 1/2', {}),
 ("The confusion matrix", "", 'p    <- predict(g, type = "response")\npred <- factor(ifelse(p >= 0.5, "Yes", "No"), levels = c("No", "Yes"))\ncm <- table(Predicted = pred, Actual = customers$buy); cm', {}),
 ("The ratios, and the no-information rate", "", 'TP <- cm["Yes","Yes"]; TN <- cm["No","No"]; FP <- cm["Yes","No"]; FN <- cm["No","Yes"]\nprec <- TP/(TP + FP); rec <- TP/(TP + FN)\nround(c(accuracy = (TP + TN)/sum(cm), precision = prec, recall = rec,\n        specificity = TN/(TN + FP), F1 = 2*prec*rec/(prec + rec),\n        no_information = max(table(customers$buy))/nrow(customers)), 6)', {}),
 ("The AUC, by the rank identity", "", 'pos <- p[customers$buy == "Yes"]; neg <- p[customers$buy == "No"]\nmean(outer(pos, neg, function(a, b) (a > b) + 0.5*(a == b)))   # over 8 x 12 = 96 pairs', {})],
"""<p>The odds of buying multiply by 1.28 per unit of income, and the fitted probability passes 1/2 at an income of 45.6.
At that threshold the classifier gets 18 of 20 right: accuracy 0.90, precision and recall 0.875, specificity 0.917,
\\(F_1\\) 0.875, AUC 0.922. <strong>Accuracy on its own is the trap</strong>: predicting <em>No</em> for everyone scores
0.60, the no-information rate, so 0.90 against 0.60 is a real gain &mdash; and the same 0.90 against a base rate of 0.95
would be a failure. Precision and recall move in opposite directions as the threshold moves; AUC does not depend on
it, which is why it is the one to compare models with.</p>""")

add(7, "Parametric Tests",
"""<p>Compare <code>score</code> between men and women by the variance-ratio test and the two-sample \\(t\\) test, in that
order, and analyse <code>score</code> by <code>grade</code> by one-way analysis of variance.</p>""",
"To run the parametric tests in the order they depend on each other, and to recognise a test that cannot fail.",
[("<code>var.test(x, y)</code>", "\\(F = s_1^{2}/s_2^{2}\\) on \\((n_1-1, n_2-1)\\) d.f."),
 ("<code>t.test(x, y, var.equal = TRUE)</code>", "the pooled two-sample \\(t\\), justified only if the variances may be pooled"),
 ("<code>aov(y ~ g)</code>", "one-way analysis of variance")],
[("The two groups", "", 'M <- customers$score[customers$gender == "M"]\nF <- customers$score[customers$gender == "F"]\nM; F\nround(c(mean_M = mean(M), mean_F = mean(F), var_M = var(M), var_F = var(F)), 2)', {}),
 ("1. The variances first, because the next test depends on the answer", "", 'var.test(M, F)', {}),
 ("2. The means", "", 't.test(M, F, var.equal = TRUE)', {}),
 ("3. More than two groups: one-way analysis of variance", "", 'summary(aov(score ~ grade, data = customers))', {})],
"""<p>The variance ratio is 3.32 on (9, 9) d.f., \\(p = 0.088\\): not significant, so pooling is defensible. The pooled
\\(t\\) is &minus;0.023 on 18 d.f., \\(p = 0.98\\): the group means, 60.7 and 60.8, are as close to equal as twenty numbers are
likely to come. What differs is the <em>spread</em> &mdash; variances 144.46 and 43.51 &mdash; which a test of means would have
missed, and which is why the variance test comes first and is reported whatever it says. <strong>The analysis of
variance by grade proves nothing</strong>: \\(F = 19.76\\), \\(p = 0.000037\\), looks decisive and is circular, because
<code>grade</code> was <em>derived</em> from <code>score</code>; testing a variable against a grouping built out of it always
succeeds.</p>""")

NP = '''before <- c(68,72,65,70,74,66,71,69,73,67,75,64)
after  <- c(71,74,64,73,77,69,70,72,76,71,74,68)
d <- after - before; d'''
add(8, "Non-Parametric Tests",
"""<p>Twelve subjects are measured before and after a training programme:</p>
  <table class="left">
    <tr><th>before</th><td>68, 72, 65, 70, 74, 66, 71, 69, 73, 67, 75, 64</td></tr>
    <tr><th>after</th><td>71, 74, 64, 73, 77, 69, 70, 72, 76, 71, 74, 68</td></tr>
  </table>
  <p>Test for a change by the sign test and the Wilcoxon signed-rank test. On <code>customers</code>, compare
  <code>score</code> between men and women by the Mann&ndash;Whitney and median tests, and test the residuals of
  <code>score ~ income</code> for independence by the runs test.</p>""",
"To apply five non-parametric tests and see how much each uses of the data.",
[("Sign test", "paired; only the signs of the differences: <code>binom.test(k, n, 0.5)</code>"),
 ("Wilcoxon signed rank", "paired; signs <em>and</em> ranks of the magnitudes: <code>wilcox.test(x, y, paired = TRUE)</code>"),
 ("Mann&ndash;Whitney \\(U\\)", "two independent groups; ranks of the pooled sample: <code>wilcox.test(x, y)</code>"),
 ("Median test", "two or more groups; only above or below the grand median: \\(\\chi^{2}\\) on the 2 &times; 2 table"),
 ("Runs test", "one ordered sequence; the number of runs of like signs; tests independence")],
[("The differences", "", NP, {}),
 ("Sign test: 9 positive, 3 negative, no ties", "", 'binom.test(sum(d > 0), sum(d != 0), 0.5)$p.value', {}),
 ("Wilcoxon signed rank, using the magnitudes", "", 'wilcox.test(after, before, paired = TRUE, correct = FALSE)', {}),
 ("Mann&ndash;Whitney U on score by gender", "", 'M <- customers$score[customers$gender == "M"]\nF <- customers$score[customers$gender == "F"]\nwilcox.test(M, F, correct = FALSE)', {}),
 ("Mood's median test, on the same two groups", "", 'gm <- median(customers$score); gm\ntab <- table(customers$gender, customers$score > gm); tab\nchisq.test(tab, correct = FALSE)', {}),
 ("Runs test on the signs of the regression residuals", "",
  'r <- resid(lm(score ~ income, data = customers))\ns <- r > 0\nruns <- 1 + sum(s[-1] != s[-length(s)])\nn1 <- sum(s); n0 <- sum(!s)\nmu <- 2*n1*n0/(n1 + n0) + 1\nsg <- sqrt(2*n1*n0*(2*n1*n0 - n1 - n0) / ((n1 + n0)^2 * (n1 + n0 - 1)))\nz <- (runs - mu)/sg\nround(c(runs = runs, positive = n1, negative = n0, expected = mu, sd = sg, z = z, p = 2*pnorm(-abs(z))), 6)', {})],
"""<p><strong>Same data, same hypothesis: the sign test gives \\(p = 0.146\\) and the Wilcoxon \\(p = 0.0086\\).</strong> The
three negative differences are all &minus;1, the smallest magnitude present, while the nine positives run from 2 to 4; the
sign test throws that away and counts 9 against 3, the Wilcoxon keeps it. Using only the signs costs real power. For
score by gender, Mann&ndash;Whitney gives \\(U\\) exactly at its null mean (\\(p = 1\\)), agreeing with the \\(t\\) test of
Practical 7; the median test, which keeps only one bit per value, gives \\(p = 0.16\\). The residuals form 7 runs where
10.9 were expected (\\(p = 0.070\\)): not significant at 5%, but close enough that the straight line should not be
accepted without a plot of residuals against fitted values. The runs test is the one test here with no parametric
counterpart &mdash; it tests independence, which every other test assumes.</p>""",
["With <code>correct = FALSE</code> R uses the normal approximation without a continuity correction; the default "
 "applies one and gives a slightly larger \\(p\\). Ties make R warn that an exact \\(p\\) cannot be computed, and R "
 "also corrects the variance of the statistic for the ties: for the training data \\(W^{+} = 72\\), \\(W^{-} = 6\\) "
 "(\\(72 + 6 = 78 = n(n+1)/2\\)), and the untied textbook standard deviation 12.75 would give \\(p = 0.0096\\), "
 "where R's tie-corrected one gives 0.0086."])

PRACTICALS = P

TAIL = """  <h2 id="writing-the-statistical-report">Writing the Statistical Report</h2>

  <div class="concept">
    <span class="label">THE STRUCTURE THE PAPER ASKS FOR</span>
    <ol>
      <li><strong>Objective.</strong> One sentence: what question the data is being asked.</li>
      <li><strong>The data.</strong> Source, number of records, every variable named with its
      <em>scale</em>, and the period or population it covers.</li>
      <li><strong>Pre-processing.</strong> Missing values found and what was done about them;
      outliers found and whether they were kept; every transformation applied, with its reason.
      <strong>A reader who cannot reproduce your data frame cannot check anything else.</strong></li>
      <li><strong>Descriptive summary.</strong> A table of the summaries permitted by each
      variable's scale, and the two or three diagrams that carry the message.</li>
      <li><strong>Analysis.</strong> Each test with its hypothesis, statistic, degrees of freedom,
      \\(p\\) value and conclusion in words &mdash; in that order, and its assumptions checked
      <em>before</em> it, not after.</li>
      <li><strong>Model, if one was fitted.</strong> The equation, the coefficients with standard
      errors, the fit measures, and the out-of-sample error. <strong>An in-sample \\(R^{2}\\)
      reported alone is not a model evaluation.</strong></li>
      <li><strong>Conclusion and limitations.</strong> What the data supports, and what it does
      not. Twenty records support very little, and saying so is part of the answer.</li>
      <li><strong>The code.</strong> Complete enough to run, with the seed if anything was
      random.</li>
    </ol>
  </div>

  <h2 id="how-marks-are-lost">How Marks Are Lost</h2>

  <div class="tip">
    <span class="label">THE RECURRING ERRORS</span>
    <ul>
      <li><strong>Taking the mean of an ordinal variable.</strong> R will do it if the factor is
      not declared ordered. Declare it, and let R refuse.</li>
      <li><strong>Scaling before splitting.</strong> The test set's mean and standard deviation
      then enter the training set, and the reported error is optimistic by an amount nobody can
      measure.</li>
      <li><strong>Reporting an in-sample \\(R^{2}\\) as if it were a prediction error.</strong>
      Degree 8 in Practical 5 has the best in-sample fit and by far the worst prediction.</li>
      <li><strong>Quoting accuracy without the no-information rate.</strong> \\(0.90\\) is good here
      and would be bad on a data set that is \\(95\\%\\) one class.</li>
      <li><strong>Ignoring R's expected-count warning</strong> on a \\(\\chi^{2}\\) test. Pool the
      classes or use Fisher's exact test.</li>
      <li><strong>Running a pooled \\(t\\) test without testing the variances first</strong>, or
      running it and not reporting the variance test because it came out inconvenient.</li>
      <li><strong>Testing a variable against a grouping derived from it.</strong> The
      \\(F = 19.76\\) of Practical 7 is a worked example of an answer that cannot fail and means nothing.</li>
      <li><strong>Not naming the convention.</strong> Type 7 quantiles, \\(n-1\\) in <code>sd</code>,
      the continuity correction in <code>wilcox.test</code>: each changes the number, and a number
      whose convention is unstated cannot be reproduced.</li>
    </ul>
  </div>

  <h2 id="what-the-practical-record-should-contain">What the Practical Record Should Contain</h2>

  <div class="concept">
    <span class="label">FOR EACH ANALYSIS</span>
    <ol>
      <li><strong>1. Question</strong> &mdash; the variables involved, with their measurement scales, and the
      pre-processing already applied.</li>
      <li><strong>2. Aim</strong> &mdash; in one line.</li>
      <li><strong>3. Steps</strong> &mdash; the method, the assumptions it requires and the check made on each, with the
      R commands used.</li>
      <li><strong>4. Programme</strong> &mdash; the R, complete enough to run.</li>
      <li><strong>5. Execution and Results</strong> &mdash; the output, with the statistic, its degrees of freedom and the
      \\(p\\) value; a second route to the same answer where one exists (the parametric test beside its non-parametric
      counterpart, or the identity \\(W^{+} + W^{-} = n(n+1)/2\\)); and the conclusion in words, with what it does not
      establish.</li>
    </ol>
  </div>

  <div class="page-nav">
    <a href="index.html">&larr; Course Home</a>
    <a href="../index.html">All Statistics courses &rarr;</a>
  </div>

  <footer>Data Handling using R &middot; Statistics</footer>
</div>
"""
