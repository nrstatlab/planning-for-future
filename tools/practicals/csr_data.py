# -*- coding: utf-8 -*-
"""The seven experiments of Computational Statistics and R Programming (the earlier syllabus).

build_csr_practical.py runs every step's R code, one R session per experiment, and writes
statistics/computational-statistics-and-r-programming/practical.html in the programming
structure: 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and Results.
A step is (heading, explanation HTML, R code, options), as in csr2023_data.py.
"""

E = []
W = "Experiment"

E.append(dict(n=1, word=W, title="Data Import &amp; Preprocessing",
    question="""<p>Import the built-in <code>airquality</code> dataset (153 observations, 6 variables), examine its
structure, count and handle the missing values, and create subsets.</p>""",
    aim="To read a dataset into R, inspect it, deal with missing values (drop or impute), and perform sub-setting.",
    commands=[("<code>data()</code>, <code>str()</code>", "load a built-in dataset; show its structure"),
              ("<code>colSums(is.na(d))</code>", "the number of missing values in each column"),
              ("<code>na.omit(d)</code>", "drops every row with a missing value"),
              ("<code>d$v[is.na(d$v)] &lt;- mean(d$v, na.rm = TRUE)</code>", "replaces the missing values by the mean (mean-imputation)"),
              ("<code>subset(d, condition)</code>", "the rows meeting a condition"),
              ("<code>write.csv(d, file, row.names = FALSE)</code>", "saves a data frame as a CSV file")],
    steps=[("Load the data and inspect its structure", "", 'data(airquality)\nstr(airquality)', {}),
           ("Count the missing values in each column", "", 'colSums(is.na(airquality))', {}),
           ("Drop the rows with any missing value", "", 'clean <- na.omit(airquality)\nnrow(clean)', {}),
           ("Or mean-impute Ozone, keeping every row",
            "<p>A copy, <code>aq</code>, is imputed, so that <code>airquality</code> itself is left as it was loaded.</p>",
            'aq <- airquality\naq$Ozone[is.na(aq$Ozone)] <- mean(aq$Ozone, na.rm = TRUE)\ncolSums(is.na(aq))', {}),
           ("Subset the hot days", "", 'hot <- subset(aq, Temp > 80)\nnrow(hot)', {}),
           ("Save the cleaned file", "", 'write.csv(clean, "airquality_clean.csv", row.names = FALSE)',
            dict(quiet="Nothing is printed: <code>write.csv()</code> writes the file <code>airquality_clean.csv</code> into the working directory.")),
          ],
    notes=[],
    conclusion="""<p>The dataset has 153 rows, with 37 missing values in Ozone and 7 in Solar.R; <code>na.omit</code> leaves
111 complete rows, while mean-imputing Ozone keeps all 153 (Solar.R still has its 7). There are 68 days hotter than
80&deg;F. The cleaned data are saved for later experiments.</p>"""))

E.append(dict(n=2, word=W, title="Descriptive Statistics",
    question="""<p>For <code>iris$Sepal.Length</code> (150 observations), compute the standard descriptive statistics and
the shape measures (skewness, kurtosis), then interpret.</p>""",
    aim="To summarise a numeric variable in R with measures of location, dispersion and shape.",
    commands=[("<code>mean median var sd range IQR</code>", "location and dispersion; <code>var</code> and <code>sd</code> divide by \\(n-1\\)"),
              ("Skewness", "\\(\\sqrt{b_1} = m_3/m_2^{3/2}\\), with \\(m_k = \\frac1n\\sum(x - \\bar x)^{k}\\)"),
              ("Kurtosis", "\\(b_2 = m_4/m_2^{2}\\); 3 for a normal curve")],
    steps=[("Location and dispersion", "", 'data(iris); x <- iris$Sepal.Length\nc(mean = mean(x), median = median(x), var = var(x), sd = sd(x), IQR = IQR(x))\nrange(x)', {}),
           ("Skewness and kurtosis, from the moments",
            "<p>The central moments are computed directly; <code>moments::skewness()</code> and <code>moments::kurtosis()</code> use the same formulas.</p>",
            'm <- function(k) mean((x - mean(x))^k)     # k-th central moment\nc(skewness = m(3) / m(2)^1.5, kurtosis = m(4) / m(2)^2)', {}),
           ("A fuller report (optional)", "<p><code>summary(x)</code> is in base R; the <code>psych</code> package's <code>describe(x)</code> adds more.</p>",
            'summary(x)', {})],
    notes=["The <code>moments</code> package gives <code>skewness()</code> and <code>kurtosis()</code>; where it is not installed, "
           "the two lines above compute the same values from the central moments."],
    conclusion="""<p>Sepal.Length has mean 5.84 cm, median 5.80 and standard deviation 0.83 (variance 0.686, IQR 1.3). It is
mildly right-skewed (skewness 0.31 &gt; 0) and platykurtic (kurtosis 2.43 &lt; 3): slightly flatter than a normal
curve.</p>"""))

E.append(dict(n=3, word=W, title="Frequency Analysis &amp; Chi-Square",
    question="""<p>Cross-classify iris flowers by Species and by whether the petal is "Long" (Petal.Length &gt; 4) or
"Short", and test whether Species and petal category are independent. As a variant, test 120 simulated rolls of a die
for fairness.</p>""",
    aim="To build a contingency table and apply the chi-square test of independence, and a goodness-of-fit test.",
    commands=[("<code>ifelse(cond, a, b)</code>", "makes a categorical variable from a condition"),
              ("<code>table(f1, f2)</code>", "the contingency table of counts"),
              ("<code>chisq.test(tbl)</code>", "\\(\\chi^2 = \\sum (O-E)^2/E\\) on \\((r-1)(c-1)\\) d.f.; on a one-way table, against equal probabilities")],
    steps=[("Make the petal category and the two-way table", "", 'big <- ifelse(iris$Petal.Length > 4, "Long", "Short")\ntbl <- table(iris$Species, big); tbl', {}),
           ("Test independence", "", 'chisq.test(tbl)', {}),
           ("Goodness of fit: 120 simulated rolls of a die", "", 'set.seed(7); rolls <- sample(1:6, 120, replace = TRUE)\ntable(rolls)\nchisq.test(table(rolls))        # expected: 20 of each', {})],
    notes=[],
    conclusion="""<p>\\(\\chi^2 = 105.84\\) on 2 d.f., \\(p &lt; 2.2 \\times 10^{-16}\\): independence is rejected &mdash; petal
category is strongly associated with species (every setosa is "Short", every virginica "Long"). For the die,
\\(\\chi^2 = 1.7\\) on 5 d.f., \\(p = 0.89\\): the simulated rolls are consistent with a fair die.</p>"""))

E.append(dict(n=4, word=W, title="Basic Visualizations &amp; Normality",
    question="""<p>Visualise <code>iris</code> variables with histograms and boxplots, and assess the normality of
Sepal.Length with a Q-Q plot and the Shapiro&ndash;Wilk test.</p>""",
    aim="To produce diagnostic plots and a formal normality test to judge whether a variable is normally distributed.",
    commands=[("<code>hist(x, freq = FALSE)</code>, <code>curve(dnorm(x, m, s), add = TRUE)</code>", "a density histogram with the fitted normal curve over it"),
              ("<code>boxplot(y ~ group)</code>", "one box per group"),
              ("<code>qqnorm(x)</code>, <code>qqline(x)</code>", "the normal Q-Q plot and its reference line"),
              ("<code>shapiro.test(x)</code>", "the Shapiro&ndash;Wilk test of \\(H_0\\): normal")],
    steps=[("Histogram with the normal curve, and boxplots by species", "",
            'par(mfrow = c(1, 2))\nhist(iris$Sepal.Length, breaks = 15, col = "lightblue", freq = FALSE,\n     main = "Histogram of Sepal Length", xlab = "Sepal length (cm)")\ncurve(dnorm(x, mean(iris$Sepal.Length), sd(iris$Sepal.Length)), add = TRUE, col = "red", lwd = 2)\nboxplot(Sepal.Length ~ Species, data = iris, notch = TRUE,\n        col = c("pink", "skyblue", "lightgreen"), main = "Sepal Length by Species")\npar(mfrow = c(1, 1))',
            dict(plot="e4-hist-box.png")),
           ("The Q-Q plot", "", 'qqnorm(iris$Sepal.Length); qqline(iris$Sepal.Length, col = "red", lwd = 2)', dict(plot="e4-qq.png")),
           ("The Shapiro&ndash;Wilk test", "", 'shapiro.test(iris$Sepal.Length)', {})],
    notes=[],
    conclusion="""<p>The histogram is roughly bell-shaped, the boxplots show Sepal.Length rising from setosa to virginica
(with one low virginica value), and the Q-Q points follow the line except in the tails. Shapiro&ndash;Wilk gives
\\(W = 0.976\\), \\(p = 0.0102\\), just below 0.05: normality is borderline &mdash; a caution to consider the
non-parametric tests of Experiment 6.</p>"""))

E.append(dict(n=5, word=W, title="Hypothesis Testing (t-tests &amp; ANOVA)",
    question="""<p>Carry out (a) a one-sample t-test of \\(H_0:\\mu = 50\\) on ten measurements, (b) a two-sample (Welch)
t-test comparing setosa and versicolor Sepal.Length, (c) a paired t-test on the <code>sleep</code> data, and (d) a
one-way ANOVA of Sepal.Length by Species, with Tukey's comparisons.</p>""",
    aim="To perform parametric tests of means (one-sample, two-sample, paired) and ANOVA in R and report the p-values.",
    commands=[("<code>t.test(x, mu = m0)</code>", "one-sample: \\(t = (\\bar x - \\mu_0)/(s/\\sqrt n)\\)"),
              ("<code>t.test(x, y)</code>", "two-sample, Welch (unequal variances) by default"),
              ("<code>t.test(x, y, paired = TRUE)</code>", "paired: a one-sample test on the differences"),
              ("<code>aov(y ~ group)</code>, <code>TukeyHSD()</code>", "one-way ANOVA, \\(F = MS_{between}/MS_{within}\\), and all pairwise comparisons")],
    steps=[("(a) One-sample t-test", "", 'x <- c(48, 52, 49, 53, 51, 47, 55, 50, 49, 52)\nt.test(x, mu = 50)', {}),
           ("(b) Two-sample Welch t-test", "", 'setosa     <- iris$Sepal.Length[iris$Species == "setosa"]\nversicolor <- iris$Sepal.Length[iris$Species == "versicolor"]\nt.test(setosa, versicolor)', {}),
           ("(c) Paired t-test on sleep",
            "<p>The two groups of <code>sleep</code> are the same ten patients, so the test is paired.</p>",
            'data(sleep)\nwith(sleep, t.test(extra[group == 1], extra[group == 2], paired = TRUE))', {}),
           ("(d) One-way ANOVA and Tukey's comparisons", "", 'fit <- aov(Sepal.Length ~ Species, data = iris)\nsummary(fit)\nTukeyHSD(fit)', {})],
    notes=["The paired test is written with two vectors. The formula form "
           "<code>t.test(extra ~ group, data = sleep, paired = TRUE)</code> works in older versions of R but is refused "
           "from R 4.4.0 onwards; the two-vector form works in every version."],
    conclusion="""<p>(a) The ten measurements are consistent with \\(\\mu = 50\\) (\\(t = 0.77\\), \\(p = 0.46\\)). (b) Setosa
and versicolor differ strongly (\\(t = -10.52\\), \\(p &lt; 2.2 \\times 10^{-16}\\)). (c) The drug has a significant paired
effect (\\(t = -4.06\\), 9 d.f., \\(p = 0.0028\\)). (d) The species means differ (\\(F = 119.3\\), \\(p &lt; 2 \\times 10^{-16}\\)),
and Tukey's comparisons show all three pairs different.</p>"""))

E.append(dict(n=6, word=W, title="Non-Parametric Tests",
    question="""<p>Repeat the location comparisons of Experiment 5 without the normality assumption: a one-sample
Wilcoxon signed-rank test, a paired signed-rank test on <code>sleep</code>, and a Wilcoxon rank-sum
(Mann&ndash;Whitney) test for setosa against versicolor; compare the last with its parametric counterpart.</p>""",
    aim="To apply rank-based non-parametric tests and contrast them with the parametric t-tests.",
    commands=[("<code>wilcox.test(x, mu = m0)</code>", "one-sample signed-rank test"),
              ("<code>wilcox.test(x, y, paired = TRUE)</code>", "paired signed-rank test"),
              ("<code>wilcox.test(x, y)</code>", "rank-sum (Mann&ndash;Whitney) test")],
    steps=[("One-sample signed-rank test", "", 'x <- c(48, 52, 49, 53, 51, 47, 55, 50, 49, 52)\nwilcox.test(x, mu = 50)', {}),
           ("Paired signed-rank test on sleep", "", 'with(sleep, wilcox.test(extra[group == 1], extra[group == 2], paired = TRUE))', {}),
           ("Rank-sum test, setosa against versicolor", "", 'setosa     <- iris$Sepal.Length[iris$Species == "setosa"]\nversicolor <- iris$Sepal.Length[iris$Species == "versicolor"]\nwilcox.test(setosa, versicolor)', {}),
           ("The two p-values side by side", "",
            'data.frame(Test = c("Welch t", "Wilcoxon rank-sum"),\n           p = c(t.test(setosa, versicolor)$p.value, suppressWarnings(wilcox.test(setosa, versicolor)$p.value)))', {})],
    notes=["The data contain ties (and, in the one-sample case, a value equal to 50), so R cannot compute exact p-values "
           "and says so in its warnings; it uses the normal approximation with a continuity correction instead."],
    conclusion="""<p>The non-parametric tests agree with the parametric ones: no shift from 50 in the one-sample case
(\\(V = 28.5\\), \\(p = 0.51\\)); a significant paired effect on sleep (\\(p = 0.009\\)); and a strong setosa&ndash;versicolor
difference (\\(W = 168.5\\), \\(p = 8.3 \\times 10^{-14}\\), against Welch's \\(3.7 \\times 10^{-17}\\)). Wilcoxon is preferred
when normality is doubtful, as Experiment 4 flagged.</p>"""))

E.append(dict(n=7, word=W, title="Linear Regression Modeling",
    question="""<p>Using <code>mtcars</code>, model fuel economy (<code>mpg</code>) as a linear function of weight
(<code>wt</code>), check the residuals, and predict mpg for weights 2.5, 3.5 and 4.5 (thousand lb).</p>""",
    aim="To fit a simple linear regression, assess it (R², residual diagnostics) and forecast with prediction intervals.",
    commands=[("<code>lm(y ~ x)</code>, <code>summary(fit)</code>", "fit \\(\\hat y = a + bx\\), \\(b = S_{xy}/S_{xx}\\); coefficients, \\(R^2\\), tests"),
              ("<code>plot(fit)</code>", "the four residual diagnostic plots"),
              ("<code>shapiro.test(resid(fit))</code>", "normality of the residuals"),
              ("<code>predict(fit, newdata, interval = \"prediction\")</code>", "predictions with 95% prediction intervals")],
    steps=[("Fit the model", "", 'data(mtcars); fit <- lm(mpg ~ wt, data = mtcars)\nsummary(fit)', {}),
           ("The scatter with the fitted line", "", 'plot(mtcars$wt, mtcars$mpg, pch = 19, col = "navy",\n     xlab = "Weight (1000 lb)", ylab = "Miles per gallon")\nabline(fit, col = "red", lwd = 2)', dict(plot="e7-fit.png")),
           ("The residual diagnostics", "", 'par(mfrow = c(2, 2)); plot(fit); par(mfrow = c(1, 1))', dict(plot="e7-diagnostics.png", size=(880, 760))),
           ("Normality of the residuals", "", 'shapiro.test(resid(fit))', {}),
           ("Predict at 2.5, 3.5 and 4.5", "", 'predict(fit, data.frame(wt = c(2.5, 3.5, 4.5)), interval = "prediction")', {})],
    notes=[],
    conclusion="""<p>\\(\\widehat{mpg} = 37.285 - 5.344\\,wt\\): each extra 1000 lb lowers fuel economy by about 5.3 mpg. The
model is highly significant (\\(p = 1.29 \\times 10^{-10}\\)) and explains 75.3% of the variation (\\(R^2 = 0.753\\)); the
residuals show no strong departure from normality (Shapiro&ndash;Wilk \\(p = 0.10\\)), though the residuals-against-fitted
plot bends upward at both ends &mdash; a hint that a straight line understates mpg for the lightest and heaviest cars, and
that a curved term in <code>wt</code> is worth trying. Predicted mpg falls from 23.9 at
2.5 to 13.2 at 4.5, each with a 95% prediction interval about &plusmn;6.4 mpg wide.</p>"""))

SYLLABUS = [
    "Data Import and Preprocessing &mdash; import dataset (e.g., iris), handle missing values, basic sub-setting.",
    "Descriptive Statistics Computation &mdash; mean, variance, skewness; interpret results.",
    "Frequency Analysis &mdash; contingency tables and chi-square tests on categorical data.",
    "Basic Visualizations &mdash; histograms and boxplots to assess data normality.",
    "Hypothesis Testing &mdash; t-tests and ANOVA on experimental data, reporting p-values.",
    "Non-Parametric Tests &mdash; Wilcoxon tests; compare with parametric alternatives.",
    "Linear Regression Modeling &mdash; fit a simple linear model, plot residuals, predict new values.",
]

# The decision between the tests, drawn once and placed between Experiments 4 and 5.
DECISION = """  <h2 id="choosing-the-right-test-experiments-3-5-6-7">Choosing the Right Test (Experiments 3, 5, 6, 7)</h2>
  <figure class="figure" style="max-width:860px;">
    <svg viewBox="0 0 820 320" role="img" aria-label="Decision tree for choosing a statistical test">
      <g font-family="Segoe UI, Arial, sans-serif" fill="#334155" font-size="12.5">
        <!-- root -->
        <rect x="300" y="12" width="220" height="34" rx="8" fill="#0f4c81"/>
        <text x="410" y="34" text-anchor="middle" fill="#fff" font-weight="600">What is your question?</text>
        <!-- arrows to level 2 -->
        <g stroke="#94a3b8" stroke-width="1.8" fill="#94a3b8">
          <line x1="345" y1="46" x2="115" y2="84"/><path d="M115,84 l10,-7 -3,10 z"/>
          <line x1="410" y1="46" x2="410" y2="84"/><path d="M410,84 l-5,-9 h10 z"/>
          <line x1="475" y1="46" x2="705" y2="84"/><path d="M705,84 l-10,-7 3,10 z"/>
        </g>
        <!-- level 2 -->
        <rect x="15" y="86" width="200" height="48" rx="8" fill="#e6f1fb" stroke="#0f4c81" stroke-width="1.5"/>
        <text x="115" y="106" text-anchor="middle">Two categorical variables</text>
        <text x="115" y="122" text-anchor="middle">associated?</text>
        <rect x="310" y="86" width="200" height="48" rx="8" fill="#e6f1fb" stroke="#0f4c81" stroke-width="1.5"/>
        <text x="410" y="106" text-anchor="middle">Compare means / medians</text>
        <text x="410" y="122" text-anchor="middle">across groups?</text>
        <rect x="605" y="86" width="200" height="48" rx="8" fill="#e6f1fb" stroke="#0f4c81" stroke-width="1.5"/>
        <text x="705" y="106" text-anchor="middle">Relationship between two</text>
        <text x="705" y="122" text-anchor="middle">numeric variables?</text>
        <!-- middle: normality check -->
        <line x1="410" y1="134" x2="410" y2="168" stroke="#94a3b8" stroke-width="1.8"/>
        <path d="M410,168 l-5,-9 h10 z" fill="#94a3b8"/>
        <rect x="300" y="170" width="220" height="40" rx="8" fill="#fff8e1" stroke="#f59e0b" stroke-width="1.5"/>
        <text x="410" y="187" text-anchor="middle">Normality OK?</text>
        <text x="410" y="202" text-anchor="middle" font-size="11.5">shapiro.test(), Q-Q plot (Exp 4)</text>
        <!-- branches from normality -->
        <g stroke="#94a3b8" stroke-width="1.8" fill="#94a3b8">
          <line x1="355" y1="210" x2="320" y2="246"/><path d="M320,246 l9,-6 -2,10 z"/>
          <line x1="465" y1="210" x2="500" y2="246"/><path d="M500,246 l-9,-6 2,10 z"/>
          <line x1="115" y1="134" x2="115" y2="246"/><path d="M115,246 l-5,-9 h10 z"/>
          <line x1="705" y1="134" x2="705" y2="246"/><path d="M705,246 l-5,-9 h10 z"/>
        </g>
        <text x="325" y="235" font-size="11.5" fill="#059669" font-weight="600">yes</text>
        <text x="482" y="235" font-size="11.5" fill="#dc2626" font-weight="600">no</text>
        <!-- leaves -->
        <rect x="15" y="248" width="200" height="52" rx="8" fill="#ecfdf5" stroke="#059669" stroke-width="1.5"/>
        <text x="115" y="269" text-anchor="middle" font-weight="600">chisq.test(table)</text>
        <text x="115" y="286" text-anchor="middle" font-size="11.5">fisher.test if counts &lt; 5 · Exp 3</text>
        <rect x="240" y="248" width="160" height="52" rx="8" fill="#ecfdf5" stroke="#059669" stroke-width="1.5"/>
        <text x="320" y="269" text-anchor="middle" font-weight="600">t.test() / aov()</text>
        <text x="320" y="286" text-anchor="middle" font-size="11.5">+ TukeyHSD · Exp 5</text>
        <rect x="420" y="248" width="160" height="52" rx="8" fill="#ecfdf5" stroke="#059669" stroke-width="1.5"/>
        <text x="500" y="269" text-anchor="middle" font-weight="600">wilcox.test()</text>
        <text x="500" y="286" text-anchor="middle" font-size="11.5">non-parametric · Exp 6</text>
        <rect x="605" y="248" width="200" height="52" rx="8" fill="#ecfdf5" stroke="#059669" stroke-width="1.5"/>
        <text x="705" y="269" text-anchor="middle" font-weight="600">cor.test(), lm()</text>
        <text x="705" y="286" text-anchor="middle" font-size="11.5">then plot(fit) · Exp 7</text>
      </g>
    </svg>
    <figcaption>The decision every lab report should make explicit: what the question is, whether assumptions hold, and which R function follows. Quote this reasoning in the Interpretation section of your notebook.</figcaption>
  </figure>
"""
