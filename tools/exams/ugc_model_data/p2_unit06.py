# -*- coding: utf-8 -*-
"""UGC NET Statistics, Unit VI: fifty exam-standard model questions."""
from . import AR, Q, ar, match, st

TITLE = "Linear Estimation, Regression Analysis and Econometrics"
BLURB = ("Simple and multiple regression, the Gauss&ndash;Markov theorem, tests and analysis of variance for "
         "the linear model, generalised least squares, dummy variables, multicollinearity, heteroscedasticity, "
         "autocorrelation, logistic regression, errors in variables, instrumental variables and simultaneous "
         "equations.")

M = lambda rows: r"\begin{pmatrix}" + r"\\".join("&".join(str(x) for x in r) for r in rows) + r"\end{pmatrix}"

QUESTIONS = [
 Q(r"For 10 pairs of observations, $\sum x=50$, $\sum y=100$, $\sum x^2=310$ and $\sum xy=560$. The value of $y$ "
   r"predicted by the least-squares line of $y$ on $x$ at $x=8$ is:",
   ["12", "13", "15", "18"], "B",
   r"$S_{xy}=560-\dfrac{50\times100}{10}=60$ and $S_{xx}=310-\dfrac{50^2}{10}=60$, so $b=1$ and "
   r"$a=\bar y-b\bar x=10-5=5$. At $x=8$: $\hat y=5+8=13$.", "slr"),

 Q(r"The two lines of regression are $3x+2y=26$ and $6x+y=31$. The correlation coefficient between $x$ and "
   r"$y$ is:",
   ["0.5", "$-0.25$", "0.25", "$-0.5$"], "D",
   r"If the first line is $y$ on $x$, $b_{yx}=-\tfrac32$; then the second is $x$ on $y$ with $b_{xy}=-\tfrac16$, and "
   r"$r^2=b_{yx}b_{xy}=\tfrac14$. (The other assignment gives $r^2=\tfrac23\times6=4\gt1$, impossible.) Both "
   r"coefficients are negative, so $r=-0.5$. The lines meet at the means $\bar x=4$, $\bar y=7$.", "slr"),

 Q(r"Let $e_i=y_i-\hat y_i$ be the residuals of a least-squares line $\hat y=a+bx$ fitted with an intercept. "
   r"Consider the statements:"
   + st(r"$\sum e_i=0$.", r"$\sum x_ie_i=0$.", r"$\sum y_ie_i=0$.", r"The line passes through $(\bar x,\bar y)$.")
   + "Which of the statements are correct?",
   ["I, II and IV only", "I and II only", "I, II and III only", "I, II, III and IV"], "A",
   r"(I) and (II) are the two normal equations, and (IV) follows from (I). They give $\sum\hat y_ie_i=0$, but "
   r"$\sum y_ie_i=\sum(\hat y_i+e_i)e_i=\sum e_i^2$, the residual sum of squares, which is zero only for a perfect "
   r"fit: (III) is false.", "slr"),

 Q(r"A sample of 20 pairs gives the correlation coefficient $r=0.6$. The value of the $t$ statistic for testing "
   r"that the slope of the regression line (equivalently, the population correlation) is zero is:",
   ["2.68", "4.50", "3.18", "2.55"], "C",
   r"$t=\dfrac{r\sqrt{n-2}}{\sqrt{1-r^2}}=\dfrac{0.6\sqrt{18}}{0.8}=3.18$ on 18 degrees of freedom. The test of "
   r"$\beta=0$ and the test of $\rho=0$ are the same test.", "slr"),

 Q(r"In a simple linear regression on 20 observations the total sum of squares of $y$ is 100, $r^2=0.64$ and "
   r"$\sum(x_i-\bar x)^2=50$. The standard error of the slope is:",
   ["0.04", "0.20", "0.85", "0.19"], "B",
   r"Residual sum of squares $=(1-r^2)\times100=36$, so $s^2=\dfrac{36}{n-2}=2$. "
   r"$\text{s.e.}(b)=\sqrt{\dfrac{s^2}{S_{xx}}}=\sqrt{\dfrac{2}{50}}=0.20$. ($0.04$ is the variance, not the standard "
   r"error.)", "slr"),

 Q(r"A regression with an intercept and 4 explanatory variables is fitted to 30 observations. If $H=X(X'X)^{-1}X'$ "
   r"is the hat matrix, the traces of $H$ and of $I-H$ are, respectively:",
   ["4 and 26", "5 and 30", "30 and 5", "5 and 25"], "D",
   r"$H$ is symmetric and idempotent, so its trace equals its rank, the number of columns of $X$: $p=5$. "
   r"$\operatorname{tr}(I-H)=n-p=25$, the residual degrees of freedom. Hence $E(e'e)=\sigma^2(n-p)$.", "mlr"),

 Q(r"In the model $y=X\beta+\varepsilon$ with two regressors, $X'X=" + M([[2, 1], [1, 2]]) + r"$ and "
   r"$X'y=" + M([[4], [5]]) + r"$. The least-squares estimate of $\beta$ is:",
   [r"$(1,2)'$", r"$(2,1)'$", r"$(3,6)'$", r"$(2,2.5)'$"], "A",
   r"$(X'X)^{-1}=\dfrac13" + M([[2, -1], [-1, 2]]) + r"$, so $\hat\beta=\dfrac13" + M([[8 - 5], [-4 + 10]]) + r"="
   + M([[1], [2]]) + r"$. Check with the normal equations: $2(1)+2=4$ and $1+2(2)=5$.", "mlr"),

 Q(r"A regression with $p=5$ coefficients (including the intercept) fitted to $n=25$ observations has residual "
   r"sum of squares 80. If the diagonal element of $(X'X)^{-1}$ corresponding to $\hat\beta_j$ is 0.25, the "
   r"standard error of $\hat\beta_j$ is:",
   ["0.25", "0.89", "1.00", "2.00"], "C",
   r"$s^2=\dfrac{SSE}{n-p}=\dfrac{80}{20}=4$. $\widehat{V}(\hat\beta_j)=s^2c_{jj}=4(0.25)=1$, so the standard error is "
   r"1.00. Using the divisor $n$ gives $s^2=3.2$ and 0.89.", "mlr"),

 Q(r"For the least-squares fit of $y=X\beta+\varepsilon$ with $E(\varepsilon)=0$, "
   r"$V(\varepsilon)=\sigma^2I$, $e=y-X\hat\beta$ and $H=X(X'X)^{-1}X'$, consider the statements:"
   + st(r"$X'e=0$.", r"$H^2=H$.", "The residuals sum to zero even when the model has no intercept.",
        r"$\operatorname{Cov}(\hat\beta,e)=0$.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and IV only", "I, II and III only", "I, II, III and IV"], "B",
   r"(I) is the normal equations. (II) $H$ is a projection. (IV) "
   r"$\operatorname{Cov}(\hat\beta,e)=\sigma^2(X'X)^{-1}X'(I-H)=0$. (III) is false: $\sum e_i=0$ holds only when the "
   r"vector of ones lies in the column space of $X$, as it does when there is an intercept.", "mlr"),

 Q(r"A regression with an intercept and $k=4$ explanatory variables fitted to $n=21$ observations has "
   r"$R^2=0.80$. The adjusted $R^2$ is:",
   ["0.75", "0.80", "0.76", "0.84"], "A",
   r"$\bar R^2=1-(1-R^2)\dfrac{n-1}{n-k-1}=1-0.20\times\dfrac{20}{16}=0.75$. $R^2$ never falls when a regressor is "
   r"added; $\bar R^2$ rises only if the added variable's $|t|$ exceeds 1.", "mlr"),

 Q(r"Which of the following is NOT required for the Gauss&ndash;Markov theorem?",
   [r"$E(\varepsilon)=0$", r"$V(\varepsilon)=\sigma^2I$", r"$X$ non-random with full column rank",
    "Normality of the errors"], "D",
   r"The theorem says that under zero mean, homoscedastic and uncorrelated errors and a full-rank non-random "
   r"$X$, least squares is the best linear unbiased estimator. Normality is needed only for exact $t$ and $F$ "
   r"tests and for least squares to coincide with maximum likelihood.", "gm"),

 Q(r"In the one-way model $y_{ij}=\mu+\alpha_i+\varepsilon_{ij}$, $i=1,2,3$, with no side condition on the "
   r"parameters, consider the parametric functions:"
   + st(r"$\alpha_1-\alpha_2$", r"$\mu+\alpha_1$", r"$\alpha_1$", r"$\mu$")
   + "Which of them are estimable?",
   ["I only", "I, II and III only", "I and II only", "I, II, III and IV"], "C",
   r"A linear function is estimable if and only if it is a linear combination of the expectations "
   r"$E(y_{ij})=\mu+\alpha_i$. So $\mu+\alpha_1$ and $(\mu+\alpha_1)-(\mu+\alpha_2)$ are estimable. $\mu$ and "
   r"$\alpha_1$ separately are not: adding a constant to $\mu$ and subtracting it from every $\alpha_i$ leaves the "
   r"distribution of the data unchanged.", "gm"),

 Q(ar("Under the Gauss&ndash;Markov conditions, the least-squares estimator is the best linear unbiased "
      "estimator.",
      "Without assuming normality, the least-squares estimator has the smallest variance among all unbiased "
      "estimators, linear or not."),
   AR, "C",
   r"(A) is the Gauss&ndash;Markov theorem. (R) is false: without normality the optimality is only within the "
   r"class of <em>linear</em> unbiased estimators; for heavy-tailed errors, non-linear estimators can do better. "
   r"With normal errors least squares is best among all unbiased estimators.", "gm"),

 Q(r"In the normal linear model with $p=5$ coefficients fitted to $n=25$ observations, the residual sum of "
   r"squares is 80. The maximum likelihood estimate of $\sigma^2$ is:",
   ["4.0", "3.2", "3.33", "16.0"], "B",
   r"$\hat\sigma^2_{ML}=\dfrac{SSE}{n}=\dfrac{80}{25}=3.2$. It is biased downward: "
   r"$E(\hat\sigma^2_{ML})=\dfrac{n-p}{n}\sigma^2$. The unbiased estimate is $\dfrac{SSE}{n-p}=4.0$.", "mle"),

 Q(r"In the linear model $y=X\beta+\varepsilon$ with $\varepsilon\sim N(0,\sigma^2I)$ and $X$ of full rank $p$, "
   r"consider the statements:"
   + st("The maximum likelihood estimator of $\\beta$ is the least-squares estimator.",
        r"$\hat\beta$ and the residual sum of squares are independent.",
        r"$SSE/\sigma^2$ has the chi-square distribution with $n-p$ degrees of freedom.",
        r"The maximum likelihood estimator of $\sigma^2$ is unbiased.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and III only", "II and III only", "I, II, III and IV"], "A",
   r"Maximising the normal likelihood over $\beta$ is minimising the sum of squares: (I). $\hat\beta$ and $e$ are "
   r"jointly normal and uncorrelated, hence independent: (II). $SSE=\varepsilon'(I-H)\varepsilon$ with $I-H$ "
   r"idempotent of rank $n-p$: (III). (IV) is false: the divisor $n$ gives a biased estimator.", "mle"),

 Q(r"In a regression with 5 coefficients fitted to 25 observations, $\hat\beta_2=2.5$ with standard error 1.0. "
   r"Given $t_{0.025,20}=2.086$, for $H_0:\beta_2=0$ against a two-sided alternative at the 5% level:",
   ["$t=2.5$ on 24 d.f.; do not reject $H_0$", "$t=2.5$ on 20 d.f.; do not reject $H_0$",
    "$t=0.4$ on 20 d.f.; do not reject $H_0$", "$t=2.5$ on 20 d.f.; reject $H_0$"], "D",
   r"$t=\dfrac{\hat\beta_2}{\text{s.e.}}=2.5$ on $n-p=20$ degrees of freedom. Since $2.5\gt2.086$, $H_0$ is "
   r"rejected at the 5% level.", "hyp"),

 Q(r"A regression coefficient is estimated as $\hat\beta=4$ with standard error 0.5 on 16 residual degrees of "
   r"freedom. Given $t_{0.025,16}=2.12$, the 95% confidence interval for $\beta$ is:",
   ["(2.94, 5.06)", "(3.02, 4.98)", "(3.50, 4.50)", "(3.74, 4.26)"], "A",
   r"$\hat\beta\pm t\times\text{s.e.}=4\pm2.12(0.5)=4\pm1.06$, i.e. $(2.94,5.06)$. Using 1.96 gives $(3.02,4.98)$, "
   r"too narrow for 16 degrees of freedom.", "hyp"),

 Q(r"A simple linear regression on $n=10$ observations has $s^2=4$. At $x_0=\bar x$, the estimated variances of "
   r"the fitted mean response and of the error in predicting a new observation are, respectively:",
   ["0.4 and 4.0", "4.0 and 4.4", "0.4 and 4.4", "0.4 and 0.8"], "C",
   r"$\widehat V(\hat y_0)=s^2\left[\dfrac1n+\dfrac{(x_0-\bar x)^2}{S_{xx}}\right]=\dfrac{4}{10}=0.4$. For a new "
   r"observation the variance is $s^2\left[1+\dfrac1n+\dfrac{(x_0-\bar x)^2}{S_{xx}}\right]=4.4$: the prediction "
   r"interval is always wider than the confidence interval for the mean response.", "hyp"),

 Q(r"A regression with an intercept and $k=4$ explanatory variables fitted to $n=25$ observations has "
   r"$R^2=0.6$. The $F$ statistic for the overall significance of the regression is:",
   ["6.0", "7.5", "9.0", "30.0"], "B",
   r"$F=\dfrac{R^2/k}{(1-R^2)/(n-k-1)}=\dfrac{0.6/4}{0.4/20}=\dfrac{0.15}{0.02}=7.5$ on $(4,20)$ degrees of "
   r"freedom.", "anova"),

 Q(r"In a regression of $y$ on 3 explanatory variables (with an intercept) from 20 observations, the total sum "
   r"of squares is 200 and the regression sum of squares is 150. The $F$ statistic is:",
   ["3", "9.5", "50", "16"], "D",
   r"Residual sum of squares $=50$ on $20-4=16$ degrees of freedom: $MSE=3.125$. Regression mean square "
   r"$=\dfrac{150}{3}=50$. $F=\dfrac{50}{3.125}=16$ on $(3,16)$ degrees of freedom; $R^2=0.75$.", "anova"),

 Q(r"Consider the statements about the coefficient of determination of a least-squares regression:"
   + st(r"With an intercept, $R^2$ is the square of the correlation between $y$ and $\hat y$.",
        r"$R^2$ may decrease when an explanatory variable is added.",
        r"The adjusted $R^2$ can be negative.",
        r"Without an intercept, $1-SSE/\sum(y_i-\bar y)^2$ need not lie between 0 and 1.")
   + "Which of the statements are correct?",
   ["I, III and IV only", "I and II only", "I and III only", "I, II, III and IV"], "A",
   r"(I) is the definition of the multiple correlation coefficient. (II) is false: adding a variable cannot "
   r"increase the minimum residual sum of squares, so $R^2$ cannot fall. (III) $\bar R^2\lt0$ when "
   r"$R^2\lt\dfrac{k}{n-1}$. (IV) Without an intercept the decomposition of the sum of squares about the mean "
   r"breaks down, and the quantity can be negative.", "anova"),

 Q(r"A regression has residual sum of squares 40 on 20 degrees of freedom. When two of its explanatory "
   r"variables are dropped, the residual sum of squares becomes 60. The $F$ statistic for testing that the "
   r"coefficients of both dropped variables are zero is:",
   ["10", "1.5", "5", "3"], "C",
   r"$F=\dfrac{(SSE_R-SSE_U)/q}{SSE_U/(n-p)}=\dfrac{(60-40)/2}{40/20}=\dfrac{10}{2}=5$ on $(2,20)$ degrees of "
   r"freedom. This is the extra-sum-of-squares (partial $F$) test.", "anova"),

 Q(r"A model with an intercept and 5 explanatory variables is fitted to 30 observations. The $F$ statistic for "
   r"testing $H_0:\beta_1=\beta_2=\beta_3$ has degrees of freedom:",
   ["(3, 24)", "(2, 24)", "(2, 25)", "(3, 27)"], "B",
   r"$\beta_1=\beta_2=\beta_3$ is two independent linear restrictions ($\beta_1-\beta_2=0$, $\beta_2-\beta_3=0$), so "
   r"$q=2$. The residual degrees of freedom are $n-p=30-6=24$.", "linhyp"),

 Q(r"A regression with 3 coefficients is fitted separately to two groups of 20 observations each, giving "
   r"residual sums of squares that add to 90; the regression fitted to all 40 observations has residual sum of "
   r"squares 120. Chow's $F$ statistic for the equality of the two regressions is about:",
   ["11.33", "2.83", "3.33", "3.78"], "D",
   r"$F=\dfrac{(SSE_P-SSE_1-SSE_2)/k}{(SSE_1+SSE_2)/(n_1+n_2-2k)}=\dfrac{30/3}{90/34}=\dfrac{10}{2.647}=3.78$ on "
   r"$(3,34)$ degrees of freedom.", "linhyp"),

 Q(r"In the model $y_i=\beta x_i+\varepsilon_i$ with uncorrelated errors and "
   r"$V(\varepsilon_i)=\sigma^2x_i^2$ $(x_i\gt0)$, the best linear unbiased estimator of $\beta$ is:",
   [r"$\dfrac1n\sum\dfrac{y_i}{x_i}$", r"$\dfrac{\sum y_i}{\sum x_i}$", r"$\dfrac{\sum x_iy_i}{\sum x_i^2}$",
    r"$\dfrac{\sum y_i/x_i^2}{\sum1/x_i^2}$"], "A",
   r"Dividing by $x_i$ gives $\dfrac{y_i}{x_i}=\beta+\dfrac{\varepsilon_i}{x_i}$ with constant variance, so the "
   r"weighted least-squares estimator is the mean of the ratios. If the variance were proportional to $x_i$ the "
   r"answer would be $\sum y_i/\sum x_i$, and for constant variance $\sum x_iy_i/\sum x_i^2$.", "gls"),

 Q(r"In $y=X\beta+\varepsilon$ suppose $V(\varepsilon)=\sigma^2V$ with $V\ne I$ known. For the ordinary "
   r"least-squares estimator $\hat\beta=(X'X)^{-1}X'y$, consider the statements:"
   + st("It is unbiased.", "It is the best linear unbiased estimator.",
        r"Its covariance matrix is not $\sigma^2(X'X)^{-1}$ in general.",
        "It remains consistent under the usual conditions.")
   + "Which of the statements are correct?",
   ["I and II only", "I and III only", "I, III and IV only", "I, II, III and IV"], "C",
   r"Unbiasedness and consistency need only $E(\varepsilon)=0$ and a well-behaved $X$. The covariance matrix is "
   r"$\sigma^2(X'X)^{-1}X'VX(X'X)^{-1}$, so the usual standard errors are wrong: (III). The best linear unbiased "
   r"estimator is generalised least squares, $(X'V^{-1}X)^{-1}X'V^{-1}y$ (Aitken): (II) is false.", "gls"),

 Q(r"Two independent unbiased measurements $y_1$ and $y_2$ of the same quantity $\mu$ have variances 1 and 4. "
   r"The variance of the best linear unbiased estimator of $\mu$ is:",
   ["1.25", "0.80", "2.50", "1.00"], "B",
   r"Weights inversely proportional to the variances: $\hat\mu=\dfrac{4y_1+y_2}{5}$, with variance "
   r"$\dfrac{1}{1/1+1/4}=0.80$. The simple average has variance $\dfrac{1+4}{4}=1.25$, worse than using $y_1$ "
   r"alone.", "gls"),

 Q(r"A regression with an intercept is to allow for a quarterly seasonal effect. The number of seasonal dummy "
   r"variables that should be included is:",
   ["4", "2", "1", "3"], "D",
   r"With an intercept, a factor with $m$ categories needs $m-1$ dummies; the omitted category is the base. "
   r"Including all 4 would make the dummies add up to the intercept column, exact multicollinearity (the dummy "
   r"variable trap).", "dummy"),

 Q(r"The fitted model is $\hat y=10+2x+3D+1.5\,Dx$, where $D=1$ for group 2 and 0 for group 1. The intercept "
   r"and the slope of the regression line for group 2 are:",
   ["13 and 3.5", "10 and 3.5", "13 and 2", "3 and 1.5"], "A",
   r"Putting $D=1$: $\hat y=(10+3)+(2+1.5)x=13+3.5x$. The coefficient of $D$ is the difference in intercepts and "
   r"that of $Dx$ the difference in slopes between the groups.", "dummy"),

 Q(ar(r"In a regression with an intercept, including a dummy variable for every category of a qualitative "
      r"factor makes $X'X$ singular.",
      "The dummy variables of all the categories add up to the column of ones."),
   AR, "A",
   r"Each observation falls in exactly one category, so the dummies sum to 1 for every observation, which is "
   r"the intercept column. The columns of $X$ are then linearly dependent and $X'X$ cannot be inverted. Both "
   r"statements are true and (R) is the reason.", "dummy"),

 Q(r"When $x_j$ is regressed on the other explanatory variables, the coefficient of determination is "
   r"$R_j^2=0.9$. The variance inflation factor of $\hat\beta_j$ is:",
   ["9", "1.11", "10", "100"], "C",
   r"$VIF_j=\dfrac{1}{1-R_j^2}=\dfrac{1}{0.1}=10$: the variance of $\hat\beta_j$ is ten times what it would be if "
   r"$x_j$ were uncorrelated with the other regressors. A value of 10 or more is the usual warning sign.", "multi"),

 Q(r"Consider the statements about high (but not exact) multicollinearity:"
   + st("The least-squares estimators remain best linear unbiased.",
        "The variances of some least-squares estimators are large.",
        "The least-squares estimators become biased.",
        r"A high $R^2$ may be accompanied by few significant $t$ ratios.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and IV only", "II, III and IV only", "I, II, III and IV"], "B",
   r"Multicollinearity violates none of the Gauss&ndash;Markov conditions, so least squares is still unbiased "
   r"and best: (I) true, (III) false. But &lsquo;best&rsquo; may still be poor: the variances are inflated, "
   r"individual coefficients are imprecise and sensitive to small changes in the data, while the regression as a "
   r"whole fits well: (II), (IV).", "multi"),

 Q(r"The largest and smallest characteristic roots of $X'X$ (in correlation form) are 100 and 0.01. The "
   r"condition number $\sqrt{\lambda_{\max}/\lambda_{\min}}$ is:",
   ["10", "1000", "10000", "100"], "D",
   r"$\sqrt{\dfrac{100}{0.01}}=\sqrt{10^4}=100$. A condition number above about 30 indicates serious "
   r"multicollinearity. Ridge regression, $(X'X+kI)^{-1}X'y$, adds $k$ to every root and so trades a little bias "
   r"for a large reduction in variance.", "multi"),

 Q(r"Match the tests for heteroscedasticity in List I with their basis in List II."
   + match(["Goldfeld&ndash;Quandt", "Breusch&ndash;Pagan", "White", "Glejser"],
           ["Regression of $|e_i|$ on a function of an explanatory variable",
            "Ratio of the residual sums of squares of two sub-samples",
            "Lagrange multiplier test from regressing $e_i^2$ on chosen variables",
            "Regression of $e_i^2$ on the regressors, their squares and cross-products"]),
   ["(a)-(ii), (b)-(iii), (c)-(iv), (d)-(i)", "(a)-(iii), (b)-(ii), (c)-(iv), (d)-(i)",
    "(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)", "(a)-(i), (b)-(iii), (c)-(iv), (d)-(ii)"], "A",
   r"Goldfeld&ndash;Quandt orders the observations, omits the middle ones and compares the two residual sums of "
   r"squares by $F$. Breusch&ndash;Pagan and White are $nR^2$ (chi-square) tests from auxiliary regressions of "
   r"$e^2$; White's needs no assumption about the form. Glejser regresses $|e|$.", "het"),

 Q(r"In a Goldfeld&ndash;Quandt test on 30 observations of a two-parameter regression, the 6 central "
   r"observations are omitted. The residual sums of squares of the two outer groups are 20 and 80. The test "
   r"statistic and its degrees of freedom are:",
   ["4 on (12, 12)", "0.25 on (10, 10)", "4 on (10, 10)", "4 on (14, 14)"], "C",
   r"Each group has $\dfrac{30-6}{2}=12$ observations and $12-2=10$ residual degrees of freedom. "
   r"$F=\dfrac{80/10}{20/10}=4$ on $(10,10)$ degrees of freedom, the larger variance being put in the numerator.", "het"),

 Q(r"In $y_i=\beta_0+\beta_1x_i+\varepsilon_i$ the error variance is proportional to $x_i^2$. Efficient "
   r"estimates are obtained by ordinary least squares applied to:",
   [r"$y_i\sqrt{x_i}$ on $\sqrt{x_i}$ and $x_i\sqrt{x_i}$", r"$\dfrac{y_i}{x_i}$ on $\dfrac{1}{x_i}$, with an intercept",
    r"$\dfrac{y_i}{\sqrt{x_i}}$ on $\dfrac{1}{\sqrt{x_i}}$ and $\sqrt{x_i}$", r"$\ln y_i$ on $\ln x_i$"], "B",
   r"Divide by the standard deviation, proportional to $x_i$: "
   r"$\dfrac{y_i}{x_i}=\beta_0\dfrac{1}{x_i}+\beta_1+\dfrac{\varepsilon_i}{x_i}$, whose error has constant "
   r"variance. Note the roles change: the intercept of the transformed regression estimates $\beta_1$. Option C "
   r"is the transformation for variance proportional to $x_i$.", "het"),

 Q(r"The residuals of a regression have first-order sample autocorrelation $\hat\rho=0.7$. The "
   r"Durbin&ndash;Watson statistic is approximately:",
   ["1.4", "0.3", "2.6", "0.6"], "D",
   r"$d\approx2(1-\hat\rho)=2(0.3)=0.6$. Values near 2 indicate no first-order autocorrelation, values near 0 "
   r"strong positive and near 4 strong negative autocorrelation.", "auto"),

 Q(r"A regression gives the Durbin&ndash;Watson statistic $d=3.0$, with tabulated bounds $d_L=1.2$ and "
   r"$d_U=1.4$. The conclusion is:",
   ["negative autocorrelation is present", "positive autocorrelation is present",
    "there is no autocorrelation", "the test is inconclusive"], "A",
   r"For $d\gt2$ compare $4-d=1.0$ with the bounds. Since $4-d\lt d_L$, i.e. $d\gt4-d_L=2.8$, the hypothesis of no "
   r"autocorrelation is rejected in favour of negative autocorrelation. The test would be inconclusive for "
   r"$2.6\lt d\lt2.8$.", "auto"),

 Q(r"Consider the statements about the Durbin&ndash;Watson test:"
   + st("It is not valid when a lagged dependent variable is among the regressors.",
        "The statistic lies between 0 and 4.",
        "The regression must contain an intercept.",
        r"$d=2$ indicates perfect positive autocorrelation.")
   + "Which of the statements are correct?",
   ["I and II only", "II and III only", "I, II and III only", "I, II, III and IV"], "C",
   r"(I) With a lagged dependent variable $d$ is biased towards 2; Durbin's $h$ test is used. (II) "
   r"$d\approx2(1-\hat\rho)$ with $-1\le\hat\rho\le1$. (III) is a condition for the tabulated bounds. (IV) is "
   r"false: $d=2$ corresponds to $\hat\rho=0$; perfect positive autocorrelation gives $d$ near 0.", "auto"),

 Q(r"The errors of a regression follow $u_t=0.6\,u_{t-1}+\varepsilon_t$, where $\varepsilon_t$ is white noise "
   r"with variance 1.28. The variance of $u_t$ is:",
   ["1.28", "2.00", "3.20", "3.56"], "B",
   r"For a stationary first-order autoregression "
   r"$V(u_t)=\dfrac{\sigma_\varepsilon^2}{1-\rho^2}=\dfrac{1.28}{1-0.36}=2.00$. The Cochrane&ndash;Orcutt "
   r"transformation $y_t-\rho y_{t-1}$ removes the autocorrelation.", "auto"),

 Q(r"A fitted logistic regression is $\ln\dfrac{\hat p}{1-\hat p}=-2+0.5x$. The estimated probability at "
   r"$x=6$ is:",
   ["0.500", "0.269", "0.622", "0.731"], "D",
   r"The logit at $x=6$ is $-2+3=1$, so $\hat p=\dfrac{1}{1+e^{-1}}=0.731$. At $x=4$ the logit is 0 and "
   r"$\hat p=0.5$; $0.269$ is the probability for a logit of $-1$.", "logit"),

 Q(r"In a logistic regression the coefficient of a binary explanatory variable is 0.693. The odds ratio for "
   r"that variable is about:",
   ["2.0", "0.693", "1.5", "0.5"], "A",
   r"The odds ratio is $e^{\beta}=e^{0.693}=2.0$: the odds of the event are doubled when the variable is 1 "
   r"compared with 0, other variables held fixed. The coefficient itself is the log odds ratio.", "logit"),

 Q(r"Consider the statements about models for a binary response:"
   + st("The linear probability model can give fitted probabilities outside $[0,1]$.",
        "The logit model is estimated by maximum likelihood.",
        r"In the logit model the effect of a unit change in $x$ on the probability is the same at all values of $x$.",
        "The errors of the linear probability model are heteroscedastic.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "I, II and IV only", "I, II, III and IV"], "C",
   r"(I) and (IV): in the linear probability model $V(y\mid x)=p(1-p)$ varies with $x$, and nothing keeps "
   r"$x'\beta$ in $[0,1]$. (II) The logit likelihood is maximised numerically (iteratively reweighted least "
   r"squares). (III) is false: $\dfrac{\partial p}{\partial x}=\beta\,p(1-p)$, largest at $p=\tfrac12$ and small "
   r"near 0 and 1.", "logit"),

 Q(r"Let $\hat\beta_R$ be the least-squares estimator of $\beta$ subject to linear restrictions $R\beta=r$ and "
   r"$\hat\beta$ the unrestricted estimator. Which statement is correct?",
   ["The restricted residual sum of squares can be smaller than the unrestricted one",
    "The restricted residual sum of squares is never smaller, and if the restrictions are true "
    r"$\hat\beta_R$ is unbiased with variance no larger than that of $\hat\beta$",
    r"$\hat\beta_R$ is unbiased whether or not the restrictions are true",
    r"$\hat\beta_R$ and $\hat\beta$ always coincide"], "B",
   r"Minimising over a smaller set cannot give a smaller minimum, so $SSE_R\ge SSE_U$. "
   r"$\hat\beta_R=\hat\beta-(X'X)^{-1}R'[R(X'X)^{-1}R']^{-1}(R\hat\beta-r)$; if $R\beta=r$ it is unbiased and "
   r"$V(\hat\beta)-V(\hat\beta_R)$ is non-negative definite. If the restrictions are false it is biased.", "restr"),

 Q(r"The true relation is $y=2x^*+\varepsilon$, but $x^*$ is observed with error as $x=x^*+u$, where "
   r"$V(x^*)=3$, $V(u)=1$ and $u$ is independent of $x^*$ and $\varepsilon$. The least-squares slope of $y$ on $x$ "
   r"converges in probability to:",
   ["2.00", "2.67", "0.50", "1.50"], "D",
   r"$\operatorname{plim}b=\beta\,\dfrac{\sigma_{x^*}^2}{\sigma_{x^*}^2+\sigma_u^2}=2\times\dfrac34=1.50$. Measurement "
   r"error in the regressor biases the slope towards zero (attenuation), and the bias does not disappear in "
   r"large samples.", "stoch"),

 Q(r"In a regression the dependent variable $y$ is measured with a random error that is uncorrelated with the "
   r"regressors, which are measured exactly. Then the least-squares estimator of the slope is:",
   ["unbiased and consistent, but with a larger variance", "biased towards zero", "biased away from zero",
    "inconsistent"], "A",
   r"The measurement error in $y$ simply adds to the disturbance term. The regressors remain uncorrelated with "
   r"the composite error, so least squares stays unbiased and consistent; only the error variance, and hence the "
   r"standard errors, increase. It is error in the <em>regressor</em> that causes inconsistency.", "stoch"),

 Q(r"In $y=\beta x+\varepsilon$ the regressor $x$ is correlated with $\varepsilon$, and $z$ is a valid "
   r"instrument. If the sample covariances are $\operatorname{Cov}(z,y)=6$, $\operatorname{Cov}(z,x)=4$, "
   r"$\operatorname{Cov}(x,y)=10$ and $V(x)=5$, the instrumental variable estimate of $\beta$ is:",
   ["2.0", "0.67", "1.5", "1.2"], "C",
   r"$b_{IV}=\dfrac{\operatorname{Cov}(z,y)}{\operatorname{Cov}(z,x)}=\dfrac64=1.5$. The least-squares estimate "
   r"$\dfrac{10}{5}=2.0$ is inconsistent. A valid instrument must be correlated with $x$ (relevance) and "
   r"uncorrelated with $\varepsilon$ (exogeneity).", "iv"),

 Q(r"A simultaneous equations system has 3 endogenous and 4 exogenous variables. One equation contains 2 "
   r"endogenous variables and 2 exogenous variables. By the order condition this equation is:",
   ["not identified", "over-identified", "exactly identified", "identified only if the system is recursive"], "B",
   r"Order condition: the number of exogenous variables excluded from the equation, $K-k=4-2=2$, must be at "
   r"least the number of included endogenous variables less one, $m-1=1$. Since $2\gt1$ the equation is "
   r"over-identified (provided the rank condition also holds).", "sem"),

 Q(r"In the market model: demand $Q=a_0+a_1P+a_2Y+u$ and supply $Q=b_0+b_1P+v$, where $Q$ and $P$ are "
   r"endogenous and income $Y$ is exogenous:",
   ["both equations are identified", "the demand equation is identified and the supply equation is not",
    "neither equation is identified", "the supply equation is exactly identified and the demand equation is not identified"], "D",
   r"The system has one exogenous variable, $Y$. Supply excludes $Y$: excluded $=1=m-1$, exactly identified. "
   r"Demand excludes nothing: $0\lt1$, not identified. Shifts in income move the demand curve and so trace out "
   r"the supply curve.", "sem"),

 Q(r"In Theil's $k$-class of estimators of a structural equation, the values $k=0$ and $k=1$ give, "
   r"respectively:",
   ["ordinary least squares and two-stage least squares", "two-stage least squares and ordinary least squares",
    "indirect least squares and limited-information maximum likelihood",
    "two-stage least squares and three-stage least squares"], "A",
   r"The $k$-class replaces the endogenous regressors $Y$ by $Y-k\hat V$, where $\hat V$ are the reduced-form "
   r"residuals: $k=0$ leaves them unchanged (ordinary least squares) and $k=1$ uses the fitted values (two-stage "
   r"least squares). Limited-information maximum likelihood is the member with $k$ equal to the smallest root of "
   r"a determinantal equation; the estimator is consistent when $\operatorname{plim}k=1$.", "twosls"),
]
