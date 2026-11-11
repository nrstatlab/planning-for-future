# -*- coding: utf-8 -*-
"""UGC NET Statistics, Unit III: fifty exam-standard model questions."""
from . import AR, Q, ar, match, st

TITLE = "Sampling Methods and Design of Experiments"
BLURB = ("Simple random, stratified, systematic, cluster, two-stage, double and varying-probability sampling; "
         "ratio and regression estimators; analysis of variance; CRD, RBD and Latin squares; missing plots; "
         "factorial experiments, confounding and balanced incomplete block designs.")

QUESTIONS = [
 Q(r"A population has $N=50$ units and mean square $S^2=\dfrac{1}{N-1}\sum(Y_i-\bar Y)^2=20$. For a simple random "
   r"sample of size $n=10$, the variance of the sample mean under sampling without replacement and with "
   r"replacement is, respectively:",
   ["2.00 and 1.96", "1.60 and 1.96", "1.60 and 2.00", "1.96 and 1.60"], "B",
   r"Without replacement: $V(\bar y)=\left(\dfrac1n-\dfrac1N\right)S^2=(0.1-0.02)(20)=1.60$. With replacement: "
   r"$V(\bar y)=\dfrac{\sigma^2}{n}$, where $\sigma^2=\dfrac{N-1}{N}S^2=19.6$, giving $1.96$. Sampling without "
   r"replacement is always the more precise.", "srs"),

 Q(r"A simple random sample of 4 units is drawn without replacement from a population of 10 units. The "
   r"probability that two specified units are both included in the sample is:",
   [r"$\dfrac25$", r"$\dfrac{4}{25}$", r"$\dfrac{3}{25}$", r"$\dfrac{2}{15}$"], "D",
   r"$\pi_{ij}=\dfrac{n(n-1)}{N(N-1)}=\dfrac{4\cdot3}{10\cdot9}=\dfrac{2}{15}$; equivalently "
   r"$\binom{8}{2}\big/\binom{10}{4}=\dfrac{28}{210}$. $\tfrac25$ is the inclusion probability $n/N$ of one unit, "
   r"and $\tfrac4{25}$ is its square, which would hold only if inclusions were independent.", "srs"),

 Q(r"A proportion $P$ is to be estimated by simple random sampling from $N=1600$ units with margin of error "
   r"$d=0.05$, using the normal deviate $z=2$ and the safest guess $P=0.5$. With $n_0=\dfrac{z^2PQ}{d^2}$ and the "
   r"finite population adjustment $n=\dfrac{n_0}{1+n_0/N}$, the required sample size is:",
   ["320", "400", "267", "356"], "A",
   r"$n_0=\dfrac{4(0.25)}{0.0025}=400$. Since $n_0/N=0.25$ is not negligible, "
   r"$n=\dfrac{400}{1.25}=320$. Taking $P=0.5$ maximises $PQ$ and so gives the largest, safest $n$.", "srs"),

 Q(r"For simple random sampling without replacement, with $s^2=\dfrac{1}{n-1}\sum(y_i-\bar y)^2$, "
   r"$S^2=\dfrac{1}{N-1}\sum(Y_i-\bar Y)^2$ and $\sigma^2=\dfrac{1}{N}\sum(Y_i-\bar Y)^2$, consider the statements:"
   + st(r"$\bar y$ is unbiased for $\bar Y$.", r"$s^2$ is unbiased for $\sigma^2$.", r"$s^2$ is unbiased for $S^2$.",
        r"$V(\bar y)=\dfrac{N-n}{Nn}S^2$.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and IV only", "I, III and IV only", "I, II, III and IV"], "C",
   r"Without replacement $E(s^2)=S^2$, so (III) is true and (II) is false; $s^2$ is unbiased for $\sigma^2$ only in "
   r"sampling <em>with</em> replacement. (I) and (IV) are the basic results of simple random sampling.", "srs"),

 Q(r"A simple random sample of size 3 is drawn with replacement from a population of 5 units. The expected "
   r"number of distinct units in the sample is:",
   ["3", r"$\dfrac{61}{25}$", r"$\dfrac{12}{5}$", r"$\dfrac{64}{25}$"], "B",
   r"A given unit is missed in all $n$ draws with probability $\left(1-\tfrac1N\right)^n$. So the expected number of "
   r"distinct units is $N\left[1-\left(1-\tfrac1N\right)^n\right]=5\left[1-\tfrac{64}{125}\right]=\tfrac{61}{25}=2.44$.", "srs"),

 Q(r"A population consists of the four values 1, 2, 3 and 6. Two units are drawn one after the other by simple "
   r"random sampling without replacement. The covariance between the values obtained on the first and the "
   r"second draw is:",
   [r"$\dfrac76$", r"$-\dfrac{14}{3}$", r"$-\dfrac73$", r"$-\dfrac76$"], "D",
   r"$\operatorname{Cov}(y_1,y_2)=-\dfrac{S^2}{N}$. Here $\bar Y=3$ and $S^2=\dfrac{4+1+0+9}{3}=\dfrac{14}{3}$, so the "
   r"covariance is $-\dfrac{14}{12}=-\dfrac76$. Direct check: $E(y_1y_2)=\dfrac{2(2+3+6+6+12+18)}{12}=\dfrac{47}{6}$ "
   r"and $\dfrac{47}{6}-9=-\dfrac76$.", "srs"),

 Q(r"A population is divided into two strata with $N_1=400$, $S_1=10$ and $N_2=600$, $S_2=20$. Under Neyman "
   r"allocation, a total sample of $n=100$ is divided between the strata as $(n_1,n_2)=$",
   ["(25, 75)", "(40, 60)", "(50, 50)", "(75, 25)"], "A",
   r"Neyman allocation: $n_h\propto N_hS_h$. $N_1S_1=4000$, $N_2S_2=12000$, in the ratio $1:3$, so "
   r"$n_1=25$, $n_2=75$. Proportional allocation would give $(40,60)$.", "strat"),

 Q(r"For a fixed total sample size, let $V_{ran}$, $V_{prop}$ and $V_{opt}$ denote the variances of the estimator "
   r"of the population mean under simple random sampling, stratified sampling with proportional allocation and "
   r"stratified sampling with Neyman allocation. Ignoring terms in $1/N_h$:",
   [r"$V_{opt}\le V_{ran}\le V_{prop}$", r"$V_{prop}\le V_{opt}\le V_{ran}$",
    r"$V_{opt}\le V_{prop}\le V_{ran}$", r"$V_{ran}\le V_{prop}\le V_{opt}$"], "C",
   r"$V_{ran}-V_{prop}\approx\dfrac{1-f}{n}\sum W_h(\bar Y_h-\bar Y)^2\ge0$ and "
   r"$V_{prop}-V_{opt}=\dfrac1n\sum W_h(S_h-\bar S)^2\ge0$, where $\bar S=\sum W_hS_h$. Proportional allocation gains "
   r"from differences between stratum means, Neyman allocation additionally from differences between stratum "
   r"standard deviations.", "strat"),

 Q(r"A population of $N=1000$ units has two strata with weights $W_1=0.4$, $W_2=0.6$ and mean squares "
   r"$S_1^2=100$, $S_2^2=400$. For a stratified sample of $n=100$ with proportional allocation, the variance of "
   r"$\bar y_{st}$ is:",
   ["2.80", "2.28", "0.28", "2.52"], "D",
   r"$V_{prop}(\bar y_{st})=\dfrac{1-f}{n}\sum W_hS_h^2=\dfrac{0.9}{100}(40+240)=2.52$. Omitting the finite "
   r"population correction gives 2.80.", "strat"),

 Q(r"Two strata have $N_1=400$, $S_1=10$, cost per unit $c_1=4$, and $N_2=600$, $S_2=20$, cost per unit $c_2=16$. "
   r"For a linear cost function, the optimum allocation of a sample of $n=100$ is $(n_1,n_2)=$",
   ["(50, 50)", "(40, 60)", "(25, 75)", "(60, 40)"], "B",
   r"Optimum allocation: $n_h\propto\dfrac{N_hS_h}{\sqrt{c_h}}$. $\dfrac{4000}{2}=2000$ and $\dfrac{12000}{4}=3000$, "
   r"in the ratio $2:3$, so $(n_1,n_2)=(40,60)$. Compared with Neyman allocation $(25,75)$, fewer units are taken "
   r"from the stratum where sampling is costly.", "strat"),

 Q(ar("Stratification gives the greatest gain in precision when the stratum means differ widely from one another.",
      r"$V_{ran}-V_{prop}$ is approximately $\dfrac{1-f}{n}\sum W_h(\bar Y_h-\bar Y)^2$."),
   AR, "A",
   r"The gain of proportional stratification over simple random sampling is the between-strata component "
   r"$\sum W_h(\bar Y_h-\bar Y)^2$, which is large exactly when the stratum means are far apart. Both statements are "
   r"true and (R) explains (A): strata should be internally homogeneous and differ from each other.", "strat"),

 Q(r"A population of $N=1000$ units has two strata with weights $W_1=0.4$, $W_2=0.6$ and standard deviations "
   r"$S_1=10$, $S_2=20$. For a stratified sample of $n=100$ with Neyman allocation, the variance of $\bar y_{st}$ is:",
   ["2.56", "2.52", "2.28", "2.80"], "C",
   r"$V_{opt}=\dfrac{(\sum W_hS_h)^2}{n}-\dfrac{\sum W_hS_h^2}{N}=\dfrac{(4+12)^2}{100}-\dfrac{280}{1000}=2.56-0.28=2.28$. "
   r"It is smaller than the 2.52 of proportional allocation by $\dfrac1n\sum W_h(S_h-\bar S)^2=\dfrac{24}{100}$.", "strat"),

 Q(r"For $N=nk$, the variance of the mean of a systematic sample is "
   r"$\dfrac{S^2}{n}\cdot\dfrac{N-1}{N}\left[1+(n-1)\rho\right]$, where $\rho$ is the intraclass correlation between "
   r"units of the same systematic sample. Systematic sampling is more precise than simple random sampling "
   r"without replacement if and only if:",
   [r"$\rho\lt-\dfrac{1}{N-1}$", r"$\rho\gt0$", r"$\rho\lt\dfrac{1}{n-1}$", r"$\rho=1$"], "A",
   r"$V_{ran}=\dfrac{N-n}{Nn}S^2$. $V_{sy}\lt V_{ran}$ means $(N-1)[1+(n-1)\rho]\lt N-n$, i.e. "
   r"$(N-1)(n-1)\rho\lt-(n-1)$, i.e. $\rho\lt-\dfrac1{N-1}$. Systematic samples must be internally heterogeneous.", "sys"),

 Q(r"For a population with a linear trend, $Y_i=\alpha+\beta i$ $(i=1,\dots,N)$, the variances of the estimators "
   r"of the mean under stratified sampling with one unit per stratum ($V_{st}$), systematic sampling ($V_{sy}$) and "
   r"simple random sampling ($V_{ran}$) satisfy:",
   [r"$V_{sy}\le V_{st}\le V_{ran}$", r"$V_{ran}\le V_{sy}\le V_{st}$",
    r"$V_{st}\le V_{ran}\le V_{sy}$", r"$V_{st}\le V_{sy}\le V_{ran}$"], "D",
   r"For a linear trend $V_{st}:V_{sy}:V_{ran}\approx\dfrac1n:1:n$. Systematic sampling removes most of the trend "
   r"but every unit of the sample is in the same position within its stratum; stratified sampling lets these "
   r"positions vary and does better still.", "sys"),

 Q(r"The population $Y_i=i$, $i=1,\dots,12$, is sampled systematically with interval $k=4$ (sample size 3). The "
   r"variance of the systematic sample mean is:",
   ["3.25", "0.75", "1.25", "1.67"], "C",
   r"The four possible samples are $\{1,5,9\},\{2,6,10\},\{3,7,11\},\{4,8,12\}$ with means 5, 6, 7, 8, each with "
   r"probability $\tfrac14$. Their variance about 6.5 is $\dfrac{2.25+0.25+0.25+2.25}{4}=1.25$. A simple random "
   r"sample of 3 would have variance $\left(\tfrac13-\tfrac1{12}\right)13=3.25$.", "sys"),

 Q(r"In simple random sampling, the coefficients of variation of $y$ and of the auxiliary variable $x$ are "
   r"$C_y=0.5$ and $C_x=0.4$. To the first order of approximation the ratio estimator of $\bar Y$ is more "
   r"efficient than the sample mean if the correlation $\rho$ between $x$ and $y$ satisfies:",
   [r"$\rho\gt0.8$", r"$\rho\gt0.4$", r"$\rho\gt0.625$", r"$\rho\gt0.2$"], "B",
   r"$V(\bar y_R)\lt V(\bar y)$ when $C_x^2-2\rho C_xC_y\lt0$, i.e. $\rho\gt\dfrac12\cdot\dfrac{C_x}{C_y}=\dfrac{0.4}{1.0}=0.4$. "
   r"A positive correlation alone is not enough.", "ratio"),

 Q(r"A sample gives $\bar y=22$ and $\bar x=44$; the population mean of $x$ is known to be $\bar X=50$ and the "
   r"sample regression coefficient of $y$ on $x$ is $b=0.6$. The ratio and the linear regression estimates of "
   r"$\bar Y$ are, respectively:",
   ["25.6 and 25", "22 and 25.6", "25 and 23.6", "25 and 25.6"], "D",
   r"Ratio: $\bar y_R=\dfrac{\bar y}{\bar x}\bar X=\dfrac{22}{44}(50)=25$. Regression: "
   r"$\bar y_{lr}=\bar y+b(\bar X-\bar x)=22+0.6(6)=25.6$. Both adjust the sample mean upward because the sample "
   r"mean of $x$ fell below $\bar X$.", "ratio"),

 Q(r"In large samples, if the correlation between $y$ and $x$ is $\rho=0.8$, the efficiency of the linear "
   r"regression estimator of $\bar Y$ relative to the simple random sample mean is about:",
   ["278%", "125%", "156%", "500%"], "A",
   r"$V(\bar y_{lr})\approx\dfrac{1-f}{n}S_y^2(1-\rho^2)$, so the relative efficiency is "
   r"$\dfrac{1}{1-\rho^2}=\dfrac{1}{0.36}=2.78$, i.e. 278%.", "ratio"),

 Q(r"Consider the statements about estimation with an auxiliary variable $x$ in simple random sampling:"
   + st("The ratio estimator is in general biased, the bias being of order $1/n$.",
        r"The ratio estimator is the best linear unbiased estimator when the regression of $y$ on $x$ is a line "
        r"through the origin and the variance of $y$ about it is proportional to $x$.",
        "In large samples the variance of the regression estimator never exceeds that of the ratio estimator.",
        r"The ratio estimator is more efficient than the sample mean whenever $\rho\gt0$.")
   + "Which of the statements are correct?",
   ["I and II only", "I and III only", "I, II and III only", "I, II, III and IV"], "C",
   r"(I), (II) and (III) are standard results; in (III) equality holds when the regression line passes through the "
   r"origin, $\beta=R$. (IV) is false: the condition is $\rho\gt\dfrac{C_x}{2C_y}$, which can fail for a small "
   r"positive $\rho$.", "ratio"),

 Q(r"In a large population $S_y=10$, $S_x=8$, the correlation between $x$ and $y$ is $0.8$ and the ratio "
   r"$R=\bar Y/\bar X=1$. For a simple random sample of $n=36$ (ignore the finite population correction), the "
   r"approximate variance of the ratio estimator of $\bar Y$ is:",
   ["8.11", "1.00", "2.78", "4.56"], "B",
   r"$V(\bar y_R)\approx\dfrac1n\left(S_y^2+R^2S_x^2-2R\rho S_yS_x\right)=\dfrac{100+64-128}{36}=1$. The sample mean "
   r"has variance $\tfrac{100}{36}=2.78$.", "ratio"),

 Q(r"Clusters of $M=10$ elements each are sampled, and the intraclass correlation between elements of the same "
   r"cluster is $\rho=0.1$. Compared with a simple random sample of the same number of elements, the variance of "
   r"the estimated mean is multiplied by about:",
   ["0.9", "1.1", "1.9", "10"], "C",
   r"The design effect of single-stage cluster sampling is $1+(M-1)\rho=1+9(0.1)=1.9$. Even a small positive "
   r"intraclass correlation is costly when clusters are large.", "cluster"),

 Q(ar("For the same number of elements, cluster sampling is usually less precise than simple random sampling.",
      "Elements belonging to the same cluster tend to resemble one another."),
   AR, "A",
   r"Resemblance within clusters means a positive intraclass correlation $\rho$, and the variance is inflated by "
   r"$1+(M-1)\rho\gt1$. Both statements are true and (R) is the reason for (A). Cluster sampling is used because "
   r"it is cheaper and needs no list of elements, not because it is precise.", "cluster"),

 Q(r"In two-stage sampling, $n=10$ first-stage units are selected and $m=5$ second-stage units from each. The "
   r"mean squares between first-stage unit means and within first-stage units are $S_b^2=20$ and $S_w^2=100$. "
   r"Ignoring both sampling fractions, the variance of the sample mean per element is:",
   ["2", "22", "6", "4"], "D",
   r"$V(\bar{\bar y})\approx\dfrac{S_b^2}{n}+\dfrac{S_w^2}{nm}=\dfrac{20}{10}+\dfrac{100}{50}=2+2=4$. Increasing "
   r"$m$ reduces only the second term; the first can be reduced only by taking more first-stage units.", "cluster"),

 Q(r"In double sampling for regression, a first sample of $n'=100$ units gives $\bar x'$ and a subsample of "
   r"$n=20$ gives $y$. With $S_y^2=100$ and $\rho=0.8$, and ignoring finite population corrections, the "
   r"approximate variance of the regression estimator $\bar y+b(\bar x'-\bar x)$ is:",
   ["1.80", "2.44", "5.00", "0.64"], "B",
   r"$V\approx\dfrac{S_y^2(1-\rho^2)}{n}+\dfrac{\rho^2S_y^2}{n'}=\dfrac{36}{20}+\dfrac{64}{100}=1.80+0.64=2.44$. "
   r"The second term is the price of not knowing $\bar X$; the sample mean alone would have variance 5.", "double"),

 Q(r"Two units are selected with replacement with probabilities proportional to size. The selected units have "
   r"$y$-values 20 and 30 and selection probabilities 0.2 and 0.4. The Hansen&ndash;Hurwitz estimate of the "
   r"population total is:",
   ["87.5", "175", "25", "83.3"], "A",
   r"$\hat Y_{HH}=\dfrac1n\sum\dfrac{y_i}{p_i}=\dfrac12\left(\dfrac{20}{0.2}+\dfrac{30}{0.4}\right)=\dfrac{100+75}{2}=87.5$. "
   r"Each $y_i/p_i$ is by itself an unbiased estimate of the total.", "pps"),

 Q(r"A sample of three units drawn without replacement has $y$-values 10, 20, 30 and inclusion probabilities "
   r"0.5, 0.25, 0.5. The Horvitz&ndash;Thompson estimate of the population total is:",
   ["60", "120", "160", "80"], "C",
   r"$\hat Y_{HT}=\sum\dfrac{y_i}{\pi_i}=20+80+60=160$. Each sampled unit represents $1/\pi_i$ units of the "
   r"population.", "pps"),

 Q(r"For a sampling design of fixed size $n$ with inclusion probabilities $\pi_i$ and $\pi_{ij}$, consider the "
   r"statements:"
   + st(r"The Horvitz&ndash;Thompson estimator of the total is unbiased if every $\pi_i\gt0$.",
        "The Yates&ndash;Grundy estimator of its variance can take negative values.",
        r"If $\pi_i$ is exactly proportional to $Y_i$, the Horvitz&ndash;Thompson estimator has zero variance.",
        r"$\sum_{i=1}^{N}\pi_i=n$.")
   + "Which of the statements are correct?",
   ["I and IV only", "I, II and IV only", "I, III and IV only", "I, II, III and IV"], "D",
   r"(I) and (IV) are basic. (II) The Yates&ndash;Grundy estimator is non-negative only if "
   r"$\pi_i\pi_j\ge\pi_{ij}$ for all pairs. (III) If $\pi_i=nY_i/Y$, every $y_i/\pi_i=Y/n$ and the estimator equals "
   r"$Y$ for every sample. All four are true.", "pps"),

 Q(r"Lahiri's method is used to select a unit with probability proportional to size from four units of sizes "
   r"10, 20, 30 and 40, taking $M=40$. The probability that a single trial (a pair of random numbers) results in "
   r"a selection is:",
   [r"$\dfrac14$", r"$\dfrac58$", r"$\dfrac25$", r"$1$"], "B",
   r"A trial picks unit $i$ with probability $\tfrac1N$ and accepts it if a random number between 1 and $M$ does "
   r"not exceed $X_i$. So $P(\text{selection})=\dfrac1N\sum\dfrac{X_i}{M}=\dfrac{\bar X}{M}=\dfrac{25}{40}=\dfrac58$. "
   r"The method needs no cumulative totals.", "pps"),

 Q(r"In a one-way analysis of variance with 4 treatments and 5 observations on each, the between-treatments sum "
   r"of squares is 90 and the total sum of squares is 250. The value of the $F$ statistic is:",
   ["1.78", "9", "3", "0.56"], "C",
   r"Error sum of squares $=250-90=160$ with $20-4=16$ degrees of freedom; treatments have 3. "
   r"$F=\dfrac{90/3}{160/16}=\dfrac{30}{10}=3$, on $(3,16)$ degrees of freedom.", "anova1"),

 Q(r"In a one-way random effects model $y_{ij}=\mu+a_i+e_{ij}$ with 5 observations in each group, the analysis "
   r"of variance gives mean squares 50 between groups and 10 within groups. The estimate of the variance "
   r"component $\sigma_a^2$ is:",
   ["8", "40", "10", "12"], "A",
   r"$E(\text{MS between})=\sigma_e^2+n\sigma_a^2$ and $E(\text{MS within})=\sigma_e^2$. So "
   r"$\hat\sigma_a^2=\dfrac{50-10}{5}=8$.", "anova1"),

 Q(r"Three treatments, each replicated 5 times in a completely randomised design, have totals 20, 30 and 40. "
   r"The sum of squares for the linear contrast with coefficients $(-1,0,1)$ is:",
   ["20", "80", "10", "40"], "D",
   r"$L=-20+0+40=20$ and $SS(L)=\dfrac{L^2}{r\sum c_i^2}=\dfrac{400}{5\cdot2}=40$. The orthogonal quadratic contrast "
   r"$(1,-2,1)$ gives $20-60+40=0$, so the whole treatment sum of squares, 40, is linear.", "anova1"),

 Q(r"In a two-way classification with 3 rows, 4 columns and 2 observations per cell, the degrees of freedom for "
   r"interaction and for error are, respectively:",
   ["6 and 11", "6 and 12", "2 and 12", "3 and 18"], "B",
   r"Interaction: $(3-1)(4-1)=6$. Error: $rc(m-1)=12(1)=12$. Check: total $23=2+3+6+12$.", "anova2"),

 Q(r"Match the principles and devices of experimental design in List I with their main purpose in List II."
   + match(["Replication", "Randomisation", "Local control", "Confounding"],
           ["Reduces the block size in factorial experiments",
            "Provides an estimate of the experimental error",
            "Ensures the validity of the estimate of error and of the tests",
            "Reduces the experimental error by grouping similar units"]),
   ["(a)-(ii), (b)-(iii), (c)-(iv), (d)-(i)", "(a)-(iii), (b)-(ii), (c)-(iv), (d)-(i)",
    "(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)"], "A",
   r"Fisher's three principles: replication gives the estimate of error (and more precision); randomisation makes "
   r"that estimate and the tests based on it valid; local control (blocking) removes known variation from the "
   r"error. Confounding sacrifices unimportant interactions to keep blocks small.", "principles"),

 Q(ar("Local control reduces the experimental error.",
      "Local control increases the number of replications of each treatment."),
   AR, "C",
   r"Blocking groups similar units together, so differences between blocks are removed from the error: (A) is "
   r"true. It does not change the number of replications; that is a separate choice of the experimenter: (R) is "
   r"false.", "principles"),

 Q(r"The error degrees of freedom in the analysis of a $6\times6$ Latin square design are:",
   ["25", "20", "16", "24"], "B",
   r"Total $m^2-1=35$; rows, columns and treatments take $m-1=5$ each. Error $=35-15=20=(m-1)(m-2)$.", "crd"),

 Q(r"For which of the following orders does a Graeco-Latin square (a pair of orthogonal Latin squares) NOT "
   r"exist?",
   ["4", "5", "7", "6"], "D",
   r"A pair of orthogonal Latin squares exists for every order except 2 and 6 (Euler's problem of the 36 "
   r"officers, settled by Tarry). For a prime or prime-power order $m$, such as 4, 5 and 7, there is a complete "
   r"set of $m-1$ mutually orthogonal Latin squares.", "crd"),

 Q(r"A randomised block design with 5 treatments in 4 blocks has block mean square 30 and error mean square 5. "
   r"Its efficiency relative to a completely randomised design is about:",
   ["1.00", "6.00", "1.79", "0.56"], "C",
   r"$E=\dfrac{(r-1)\,MS_B+r(t-1)\,MS_E}{(rt-1)\,MS_E}=\dfrac{3(30)+16(5)}{19(5)}=\dfrac{170}{95}\approx1.79$. "
   r"Blocking has made the experiment about 79% more efficient.", "crd"),

 Q(r"In a randomised block design with 4 blocks the error mean square is 8 on 12 degrees of freedom. Given "
   r"$t_{0.025,12}=2.179$, the critical difference between two treatment means at the 5% level is:",
   ["4.36", "8.72", "3.08", "6.16"], "A",
   r"$CD=t\sqrt{\dfrac{2\,MS_E}{r}}=2.179\sqrt{\dfrac{16}{4}}=2.179\times2=4.36$. Leaving out the factor 2 under the "
   r"root gives 3.08, the half-width for a single mean.", "crd"),

 Q(r"Consider the statements about an $m\times m$ Latin square design:"
   + st("The numbers of rows, columns and treatments are equal.",
        r"A $2\times2$ Latin square leaves no degrees of freedom for error.",
        "The model assumes that rows, columns and treatments do not interact.",
        r"The error degrees of freedom are $(m-1)^2$.")
   + "Which of the statements are correct?",
   ["I and III only", "I, II and III only", "II and IV only", "I, II, III and IV"], "B",
   r"(I) and (III) are part of the definition and model. Error degrees of freedom are $(m-1)(m-2)$, which is 0 for "
   r"$m=2$: (II) is true and (IV) is false; $(m-1)^2$ is the error degrees of freedom of a randomised block "
   r"design with $m$ treatments in $m$ blocks.", "crd"),

 Q(r"In a randomised block design with 5 treatments and 4 blocks one observation is missing. The total of the "
   r"remaining observations in its block is 50, in its treatment 40, and the grand total is 340. The estimate "
   r"of the missing value is:",
   ["2.5", "4", "6", "5"], "D",
   r"$\hat x=\dfrac{rB+tT-G}{(r-1)(t-1)}=\dfrac{4(50)+5(40)-340}{3\cdot4}=\dfrac{60}{12}=5$. The error degrees of "
   r"freedom are then reduced by one, from 12 to 11.", "missing"),

 Q(r"In a $4\times4$ Latin square one observation is missing. The totals of the remaining observations in its "
   r"row, column and treatment are 20, 24 and 22, and the grand total is 120. The estimate of the missing value "
   r"is:",
   ["4", "6", "2", "8"], "A",
   r"$\hat x=\dfrac{m(R+C+T)-2G}{(m-1)(m-2)}=\dfrac{4(66)-240}{3\cdot2}=\dfrac{24}{6}=4$.", "missing"),

 Q(r"A $2^2$ factorial experiment in 5 replicates gives treatment totals $(1)=20$, $a=30$, $b=26$, $ab=44$. The "
   r"main effect of $A$ and its sum of squares are, respectively:",
   ["5.6 and 39.2", "2.8 and 78.4", "2.8 and 39.2", "0.8 and 3.2"], "C",
   r"Contrast $[A]=ab+a-b-(1)=44+30-26-20=28$. Main effect $=\dfrac{[A]}{2r}=\dfrac{28}{10}=2.8$; "
   r"$SS_A=\dfrac{[A]^2}{4r}=\dfrac{784}{20}=39.2$. Option D is the interaction: $[AB]=44+20-30-26=8$, effect "
   r"0.8, sum of squares 3.2.", "fact"),

 Q(r"A $2^3$ factorial experiment is conducted in 3 randomised blocks, each a complete replicate. The error "
   r"degrees of freedom are:",
   ["16", "14", "21", "7"], "B",
   r"Total $24-1=23$; blocks $2$; treatments $7$ (three main effects, three two-factor interactions and one "
   r"three-factor interaction). Error $=23-2-7=14=(r-1)(2^3-1)$.", "fact"),

 Q(r"In a $2^3$ factorial experiment, the treatment combinations that enter the contrast for the interaction "
   r"$ABC$ with a positive sign are:",
   ["$(1), ab, ac, bc$", "$a, b, c$ only", "$ab, ac, bc, abc$", "$a, b, c, abc$"], "D",
   r"$ABC\propto(a-1)(b-1)(c-1)=abc-ab-ac-bc+a+b+c-(1)$. The combinations with an odd number of letters, "
   r"$a,b,c,abc$, are positive; those with an even number, $(1),ab,ac,bc$, are negative.", "fact"),

 Q(r"A $2^3$ factorial experiment is laid out in two blocks of four plots, confounding $ABC$. The principal "
   r"block (the one containing the control) is:",
   ["$(1), ab, ac, bc$", "$(1), a, b, c$", "$a, b, c, abc$", "$(1), a, bc, abc$"], "A",
   r"The principal block holds the combinations having an even number of letters in common with $ABC$: "
   r"$(1),ab,ac,bc$. The other block is $a,b,c,abc$. The difference between block totals is exactly the $ABC$ "
   r"contrast, so $ABC$ cannot be separated from blocks.", "conf"),

 Q(r"A $2^4$ factorial experiment is arranged in four blocks of four plots, confounding $ABC$ and $BCD$. The "
   r"third interaction that is automatically confounded is:",
   ["$AB$", "$BC$", "$AD$", "$ABCD$"], "C",
   r"Four blocks have 3 degrees of freedom, so three effects are confounded: the two chosen and their generalised "
   r"interaction, $ABC\times BCD=AB^2C^2D=AD$ (squares drop out). Choosing $ABCD$ and $ABC$ instead would confound "
   r"the main effect $D$, which is why the generators must be picked with care.", "conf"),

 Q(r"In a $2^3$ experiment in 4 replicates, each in two blocks of four plots, the interactions $ABC$, $AB$, $AC$ "
   r"and $BC$ are confounded in replicates 1, 2, 3 and 4 respectively. Relative to an unconfounded effect, the "
   r"information recovered on each of these interactions is:",
   [r"$\dfrac14$", r"$\dfrac34$", r"$\dfrac12$", r"$1$"], "B",
   r"This is partial confounding: each of the four interactions is confounded in one replicate and estimated "
   r"from the other three, so the relative information is $\tfrac34$. Main effects are estimated from all four "
   r"replicates with full information.", "conf"),

 Q(r"Which of the following sets of parameters $(v,b,r,k,\lambda)$ can NOT be those of a balanced incomplete "
   r"block design?",
   ["(7, 7, 3, 3, 1)", "(9, 12, 4, 3, 1)", "(6, 10, 5, 3, 2)", "(8, 8, 4, 4, 2)"], "D",
   r"A BIBD needs $bk=vr$ and $\lambda(v-1)=r(k-1)$. Option D satisfies $bk=vr=32$ but "
   r"$\lambda(v-1)=14\ne r(k-1)=12$. The other three satisfy both relations and Fisher's inequality $b\ge v$, and "
   r"designs with those parameters exist.", "bibd"),

 Q(r"The efficiency factor of the balanced incomplete block design with $v=b=7$, $r=k=3$, $\lambda=1$, relative "
   r"to a randomised block design with the same number of replications and the same error variance, is:",
   [r"$\dfrac37$", r"$\dfrac23$", r"$\dfrac79$", r"$\dfrac97$"], "C",
   r"$E=\dfrac{\lambda v}{rk}=\dfrac{1\cdot7}{3\cdot3}=\dfrac79$. The variance of the difference between two "
   r"adjusted treatment means is $\dfrac{2k\sigma^2}{\lambda v}$ against $\dfrac{2\sigma^2}{r}$ for complete blocks. "
   r"$E\lt1$ always; the design pays only if the smaller blocks reduce $\sigma^2$ enough.", "bibd"),

 Q(r"Consider the statements about a balanced incomplete block design with parameters $(v,b,r,k,\lambda)$:"
   + st("If $b=v$, then $r=k$.", r"$b\ge v$.", "Every balanced incomplete block design is resolvable.",
        r"If $b=v$, any two blocks have exactly $\lambda$ treatments in common.")
   + "Which of the statements are correct?",
   ["I, II and IV only", "I and II only", "I, II and III only", "I, II, III and IV"], "A",
   r"(I) follows from $bk=vr$. (II) is Fisher's inequality. (IV) is the characteristic property of a symmetric "
   r"BIBD. (III) is false: a resolvable design needs $k$ to divide $v$ and satisfies $b\ge v+r-1$; the design "
   r"$(7,7,3,3,1)$ cannot be resolvable since 3 does not divide 7.", "bibd"),
]
