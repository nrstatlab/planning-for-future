# -*- coding: utf-8 -*-
"""UGC NET Statistics, Unit V: fifty exam-standard model questions."""
from . import AR, Q, ar, match, st

TITLE = "Testing of Hypotheses"
BLURB = ("Size, power and p-values; the Neyman&ndash;Pearson lemma; monotone likelihood ratio and UMP tests; "
         "likelihood ratio tests; Wald's sequential probability ratio test; chi-square tests; the sign, "
         "Wilcoxon, Mann&ndash;Whitney, linear rank and Kruskal&ndash;Wallis tests.")

QUESTIONS = [
 Q(r"A single observation $X$ is taken from the uniform distribution on $(0,\theta)$ to test $H_0:\theta=1$ "
   r"against $H_1:\theta=2$, and $H_0$ is rejected if $X\gt0.9$. The size and the power of the test are, "
   r"respectively:",
   ["0.10 and 0.45", "0.10 and 0.55", "0.90 and 0.55", "0.05 and 0.45"], "B",
   r"Size $=P(X\gt0.9\mid\theta=1)=0.1$. Power $=P(X\gt0.9\mid\theta=2)=\dfrac{2-0.9}{2}=0.55$. The probability of a "
   r"type II error is $0.45$, which is option A's second figure.", "basic"),

 Q(r"$\bar X$ is the mean of a random sample of size 9 from $N(\mu,1)$. To test $H_0:\mu=0$ against $H_1:\mu=1$, "
   r"$H_0$ is rejected if $\bar X\gt0.5$. Given $\Phi(1.5)=0.9332$, the probabilities of type I and type II "
   r"errors are, respectively:",
   ["0.0668 and 0.9332", "0.3085 and 0.3085", "0.1336 and 0.0668", "0.0668 and 0.0668"], "D",
   r"Under $H_0$, $\bar X\sim N(0,\tfrac19)$: $\alpha=P(Z\gt1.5)=0.0668$. Under $H_1$, "
   r"$\beta=P(\bar X\le0.5\mid\mu=1)=P(Z\le-1.5)=0.0668$. The cut-off lies midway between the two means, so the "
   r"two errors are equal; the power is $0.9332$.", "basic"),

 Q(r"In a two-sided $z$ test the observed value of the statistic is $z=1.75$. Given $\Phi(1.75)=0.9599$, the "
   r"$p$-value is:",
   ["0.0802", "0.0401", "0.9599", "0.0500"], "A",
   r"$p=2[1-\Phi(1.75)]=2(0.0401)=0.0802$. $H_0$ is not rejected at the 5% level but is rejected at the 10% "
   r"level. $0.0401$ is the $p$-value of the one-sided test.", "basic"),

 Q(r"Consider the statements about a test of a simple $H_0$ against a simple $H_1$ with error probabilities "
   r"$\alpha$ and $\beta$:"
   + st(r"$\alpha+\beta=1$ for every test.",
        r"For a fixed sample size, a critical region with smaller $\alpha$ chosen in the best way has larger $\beta$.",
        r"The power of the test is $1-\beta$.",
        r"The $p$-value is the probability that $H_0$ is true.")
   + "Which of the statements are correct?",
   ["I and III only", "III only", "II and III only", "II, III and IV only"], "C",
   r"(II) and (III) are true: with $n$ fixed the two errors trade off against each other, and power is the "
   r"probability of rejecting a false $H_0$. (I) is false: $\alpha$ and $\beta$ are computed under different "
   r"hypotheses and need not add to 1. (IV) is false: the $p$-value is the probability, under $H_0$, of a result "
   r"at least as extreme as the one observed.", "basic"),

 Q(r"A single observation $X$ is taken from the exponential distribution with mean $\theta$ to test "
   r"$H_0:\theta=1$ against $H_1:\theta=2$, rejecting $H_0$ when $X\gt c$. For size $0.05$, the power of the test "
   r"is about:",
   ["0.050", "0.224", "0.368", "0.950"], "B",
   r"$P(X\gt c\mid\theta=1)=e^{-c}=0.05$ gives $c=\ln20=2.996$. Power "
   r"$=P(X\gt c\mid\theta=2)=e^{-c/2}=\dfrac{1}{\sqrt{20}}=0.224$. One observation gives a poor test.", "basic"),

 Q(r"$X\sim\text{Bin}(3,p)$ is used to test $H_0:p=\tfrac12$ against $H_1:p\gt\tfrac12$. For a test of exact size "
   r"$0.05$ that rejects only when $X=3$, the randomisation probability with which $H_0$ is rejected at $X=3$ is:",
   ["0.40", "0.05", "0.125", "1.00"], "A",
   r"$P(X=3\mid p=\tfrac12)=\tfrac18=0.125\gt0.05$, so always rejecting at $X=3$ gives size 0.125. Rejecting with "
   r"probability $\gamma$ at $X=3$ gives size $0.125\gamma=0.05$, i.e. $\gamma=0.40$. Randomisation is needed "
   r"because a discrete statistic cannot give every size exactly.", "basic"),

 Q(r"$X$ is a Poisson variate with mean $\lambda$. To test $H_0:\lambda=1$ against $H_1:\lambda=2$, $H_0$ is "
   r"rejected if $X\ge3$. The probability of a type II error is:",
   ["0.080", "0.323", "0.920", "0.677"], "D",
   r"$\beta=P(X\le2\mid\lambda=2)=e^{-2}\left(1+2+2\right)=5e^{-2}=0.677$. The size is "
   r"$1-e^{-1}\left(1+1+\tfrac12\right)=0.080$ and the power is $0.323$.", "basic"),

 Q(r"A single observation $X$ has density $f_0(x)=1$ under $H_0$ and $f_1(x)=2x$ under $H_1$, on $0\lt x\lt1$. "
   r"The power of the most powerful test of size $0.1$ is:",
   ["0.10", "0.01", "0.19", "0.81"], "C",
   r"The likelihood ratio $f_1/f_0=2x$ increases with $x$, so the most powerful test rejects for $x\gt c$ with "
   r"$1-c=0.1$, $c=0.9$. Power $=\displaystyle\int_{0.9}^{1}2x\,dx=1-0.81=0.19$. Rejecting for small $x$ "
   r"($x\lt0.1$) would give power only 0.01.", "np"),

 Q(r"$X_1,\dots,X_{10}$ is a random sample from $N(0,\sigma^2)$. Given that the upper 5% point of $\chi^2_{10}$ is "
   r"18.31, the most powerful test of size 0.05 of $H_0:\sigma^2=1$ against $H_1:\sigma^2=4$ rejects $H_0$ when:",
   [r"$\sum X_i^2\gt18.31$", r"$\sum X_i^2\lt18.31$", r"$\sum X_i^2\gt73.24$", r"$|\bar X|\gt0.62$"], "A",
   r"$\dfrac{L_1}{L_0}=4^{-5}\exp\left\{\left(\tfrac12-\tfrac18\right)\sum x_i^2\right\}$ increases with $\sum x_i^2$, so "
   r"the test rejects for large $\sum X_i^2$. Under $H_0$, $\sum X_i^2\sim\chi^2_{10}$, so the cut-off is 18.31. The "
   r"same region is most powerful against every $\sigma^2\gt1$, hence UMP for the one-sided alternative.", "np"),

 Q(r"Consider the statements about the Neyman&ndash;Pearson lemma for a simple $H_0$ against a simple $H_1$:"
   + st(r"A test that rejects $H_0$ when $f_1/f_0\gt k$ is most powerful of its size.",
        r"The power of a most powerful test of size $\alpha$ is at least $\alpha$.",
        r"Every most powerful test of size $\alpha$ has the likelihood-ratio form, except on a set of probability "
        r"zero under both hypotheses.",
        "The power of a most powerful test is always 1.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "I and III only", "I, II, III and IV"], "B",
   r"(I) is the sufficiency part and (III) the necessity part of the lemma. (II) holds because the trivial test "
   r"that rejects with probability $\alpha$ whatever the data has power $\alpha$, and the most powerful test can do "
   r"no worse. (IV) is false: power 1 is reached only when the two distributions do not overlap.", "np"),

 Q(r"A random variable $X$ takes the values 1, 2, 3, 4 with probabilities $0.1,0.2,0.3,0.4$ under $H_0$ and "
   r"$0.4,0.3,0.2,0.1$ under $H_1$. The critical region and the power of the most powerful non-randomised test "
   r"of size $0.3$ are:",
   [r"$\{3\}$ and 0.2", r"$\{1\}$ and 0.4", r"$\{4\}$ and 0.1", r"$\{1,2\}$ and 0.7"], "D",
   r"The likelihood ratios $p_1/p_0$ are $4,\ 1.5,\ 0.67,\ 0.25$ for $x=1,2,3,4$. Take points in decreasing order "
   r"of the ratio until the size is used up: $\{1,2\}$ has size $0.1+0.2=0.3$ and power $0.4+0.3=0.7$. The region "
   r"$\{3\}$ also has size 0.3 but power only 0.2.", "np"),

 Q(ar(r"For testing a simple hypothesis against a simple alternative, the most powerful test of size $\alpha$ has "
      r"power at least $\alpha$.",
      r"The test that rejects $H_0$ with probability $\alpha$ regardless of the data has size $\alpha$ and power "
      r"$\alpha$."),
   AR, "A",
   r"Both are true, and (R) is the proof of (A): the most powerful test is at least as powerful as any other test "
   r"of the same size, in particular the trivial randomised test, whose power is $\alpha$. So a most powerful "
   r"test is unbiased.", "np"),

 Q(r"Which of the following families of distributions does NOT have a monotone likelihood ratio in the sample "
   r"observation $x$?",
   [r"$N(\theta,1)$", r"Poisson with mean $\theta$", r"Cauchy with location $\theta$", r"Uniform on $(0,\theta)$"], "C",
   r"For the Cauchy location family "
   r"$\dfrac{f(x;\theta_2)}{f(x;\theta_1)}=\dfrac{1+(x-\theta_1)^2}{1+(x-\theta_2)^2}\to1$ as $x\to\pm\infty$, so it cannot "
   r"be monotone in $x$. One-parameter exponential families (normal, Poisson) and the uniform $(0,\theta)$ family "
   r"have monotone likelihood ratio.", "mlr"),

 Q(r"For a random sample from $f(x;\theta)=\theta e^{-\theta x}$, $x\gt0$, the UMP test of $H_0:\theta\le\theta_0$ "
   r"against $H_1:\theta\gt\theta_0$ rejects $H_0$ when:",
   [r"$\sum X_i$ is large", r"$\sum X_i$ is small", r"$X_{(n)}$ is large", r"$\prod X_i$ is large"], "B",
   r"For $\theta_2\gt\theta_1$, $\dfrac{L(\theta_2)}{L(\theta_1)}=\left(\dfrac{\theta_2}{\theta_1}\right)^n"
   r"e^{-(\theta_2-\theta_1)\sum x_i}$ is decreasing in $\sum x_i$: the family has monotone likelihood ratio in "
   r"$-\sum x_i$. By the Karlin&ndash;Rubin theorem the UMP test rejects for small $\sum X_i$, as expected since a "
   r"large rate $\theta$ means small observations.", "mlr"),

 Q(r"Consider the statements:"
   + st(r"For a family with monotone likelihood ratio in $T$, a UMP test of $H_0:\theta\le\theta_0$ against "
        r"$H_1:\theta\gt\theta_0$ exists.",
        r"The power function of that test is non-decreasing in $\theta$.",
        r"For $N(\theta,1)$, a UMP test of $H_0:\theta=\theta_0$ against $H_1:\theta\ne\theta_0$ exists.",
        r"For $N(\theta,1)$, a UMP unbiased test of $H_0:\theta=\theta_0$ against $H_1:\theta\ne\theta_0$ exists.")
   + "Which of the statements are correct?",
   ["I, II and IV only", "I and II only", "I, II and III only", "I, II, III and IV"], "A",
   r"(I) and (II) are the Karlin&ndash;Rubin theorem. (III) is false: the tests most powerful against "
   r"$\theta\gt\theta_0$ and against $\theta\lt\theta_0$ use opposite tails, so no single test is best against both. "
   r"(IV) is true: the equal-tailed test is UMP among unbiased tests.", "mlr"),

 Q(r"For which of the following two-sided problems, $H_0:\theta=\theta_0$ against $H_1:\theta\ne\theta_0$, does a "
   r"UMP test exist?",
   [r"$N(\theta,1)$", r"Poisson with mean $\theta$", r"Exponential with mean $\theta$", r"Uniform on $(0,\theta)$"], "D",
   r"For the uniform $(0,\theta)$ family the test that rejects when $X_{(n)}\gt\theta_0$ or "
   r"$X_{(n)}\le\theta_0\alpha^{1/n}$ is UMP against all $\theta\ne\theta_0$; this is the classical exception. In "
   r"one-parameter exponential families (the other three options) no UMP test exists for a two-sided "
   r"alternative.", "ump"),

 Q(r"$\bar X$ is the mean of a sample of size 16 from $N(\theta,1)$. The UMP test of size 0.05 of "
   r"$H_0:\theta\le0$ against $H_1:\theta\gt0$ is used. Given $\Phi(0.355)=0.639$, its power at $\theta=0.5$ is:",
   ["0.361", "0.950", "0.639", "0.500"], "C",
   r"Reject when $\sqrt{16}\,\bar X\gt1.645$. At $\theta=0.5$, $4\bar X\sim N(2,1)$, so the power is "
   r"$P(Z\gt1.645-2)=P(Z\gt-0.355)=\Phi(0.355)=0.639$.", "ump"),

 Q(r"For testing $H_0:\mu=\mu_0$ against $H_1:\mu\gt\mu_0$ with known $\sigma$ at the 5% level "
   r"($z_{0.05}=1.645$), the smallest sample size that gives power at least 0.90 ($z_{0.10}=1.282$) when "
   r"$\mu=\mu_0+0.5\,\sigma$ is:",
   ["43", "35", "22", "69"], "B",
   r"$n\ge\dfrac{(z_\alpha+z_\beta)^2\sigma^2}{\delta^2}=\dfrac{(1.645+1.282)^2}{0.25}=\dfrac{8.567}{0.25}=34.3$, so "
   r"$n=35$. For the two-sided test $1.645$ is replaced by $1.96$, giving 43.", "ump"),

 Q(ar(r"For testing $H_0:\mu=\mu_0$ against $H_1:\mu\ne\mu_0$ in $N(\mu,\sigma^2)$ with $\sigma$ known, the "
      r"equal-tailed $z$ test is uniformly most powerful among unbiased tests.",
      "A uniformly most powerful test exists for this two-sided problem."),
   AR, "C",
   r"(A) is true. (R) is false: the one-sided $z$ tests are each more powerful than the two-sided test on their "
   r"own side, so no test is uniformly most powerful. Those one-sided tests are biased against the other side, "
   r"which is why restricting attention to unbiased tests produces a best test.", "ump"),

 Q(r"Independent samples are drawn from four Poisson populations with means $\lambda_1,\dots,\lambda_4$. For the "
   r"likelihood ratio test of $H_0:\lambda_1=\lambda_2=\lambda_3=\lambda_4$, the large-sample distribution of "
   r"$-2\ln\lambda$ under $H_0$ is chi-square with degrees of freedom:",
   ["3", "4", "1", "7"], "A",
   r"The degrees of freedom equal the number of free parameters in the whole parameter space minus the number "
   r"under $H_0$: $4-1=3$ (Wilks' theorem).", "lrt"),

 Q(r"A sample of size 4 from $N(\mu,1)$ has mean $\bar x=1$. For the likelihood ratio test of $H_0:\mu=0$ "
   r"against $H_1:\mu\ne0$, the value of $-2\ln\lambda$ is:",
   ["1", "2", r"$e^{-2}$", "4"], "D",
   r"$\lambda=\dfrac{L(\mu_0)}{L(\bar x)}=\exp\left\{-\dfrac{n(\bar x-\mu_0)^2}{2}\right\}=e^{-2}$, so "
   r"$-2\ln\lambda=n(\bar x-\mu_0)^2=4=z^2$ with $z=2$. Here $-2\ln\lambda$ is exactly $\chi^2_1$ under $H_0$, and "
   r"the likelihood ratio test is the two-sided $z$ test.", "lrt"),

 Q(r"For a sample of size $n$ from $N(\mu,\sigma^2)$ with $\sigma^2$ unknown, let $t$ be the usual one-sample "
   r"$t$ statistic for $H_0:\mu=\mu_0$. The likelihood ratio $\lambda$ satisfies $\lambda^{2/n}=$",
   [r"$1+\dfrac{t^2}{n-1}$", r"$\left(1+\dfrac{t^2}{n-1}\right)^{-1}$", r"$\left(1+\dfrac{t^2}{n}\right)^{-1}$", r"$e^{-t^2/2}$"], "B",
   r"$\lambda=\left(\dfrac{\hat\sigma^2}{\hat\sigma_0^2}\right)^{n/2}$ with $\hat\sigma^2=\tfrac1n\sum(x_i-\bar x)^2$ and "
   r"$\hat\sigma_0^2=\hat\sigma^2+(\bar x-\mu_0)^2$. Since $t^2=\dfrac{n(n-1)(\bar x-\mu_0)^2}{\sum(x_i-\bar x)^2}$, "
   r"$\lambda^{2/n}=\left(1+\dfrac{t^2}{n-1}\right)^{-1}$. Small $\lambda$ means large $|t|$: the test is the "
   r"two-sided $t$ test.", "lrt"),

 Q(r"A sample of size 5 from the exponential distribution with mean $\theta$ has $\bar x=2$. For "
   r"$H_0:\theta=1$ against $H_1:\theta\ne1$, the likelihood ratio $\lambda$ equals:",
   ["0.0067", "0.0183", "0.2156", "0.5413"], "C",
   r"$L(\theta)=\theta^{-n}e^{-n\bar x/\theta}$, maximised at $\hat\theta=\bar x$. "
   r"$\lambda=\dfrac{L(\theta_0)}{L(\bar x)}=\left(\dfrac{\bar x}{\theta_0}\right)^ne^{-n(\bar x/\theta_0-1)}=2^5e^{-5}=0.2156$.", "lrt"),

 Q(r"Consider the statements about the likelihood ratio "
   r"$\lambda=\dfrac{\sup_{\Theta_0}L}{\sup_{\Theta}L}$:"
   + st(r"$0\le\lambda\le1$.", r"$H_0$ is rejected for small values of $\lambda$.",
        "A likelihood ratio test is always uniformly most powerful.",
        r"Under regularity conditions, $-2\ln\lambda$ is asymptotically chi-square under $H_0$.")
   + "Which of the statements are correct?",
   ["I, II and IV only", "I and II only", "II, III and IV only", "I, II, III and IV"], "A",
   r"(I) holds because $\Theta_0\subseteq\Theta$; (II) because a small $\lambda$ means $H_0$ explains the data much "
   r"worse than the best alternative; (IV) is Wilks' theorem. (III) is false: the likelihood ratio test is a "
   r"general method that often gives good tests but carries no optimality guarantee.", "lrt"),

 Q(r"In Wald's sequential probability ratio test with $\alpha=0.05$ and $\beta=0.10$, the approximate "
   r"boundaries $A$ (reject $H_0$ when the ratio is at least $A$) and $B$ (accept $H_0$ when it is at most $B$) are:",
   ["19 and 0.053", "0.105 and 18", "9.5 and 0.21", "18 and 0.105"], "D",
   r"$A\approx\dfrac{1-\beta}{\alpha}=\dfrac{0.90}{0.05}=18$ and $B\approx\dfrac{\beta}{1-\alpha}=\dfrac{0.10}{0.95}=0.105$. "
   r"Sampling continues while $B\lt\lambda_n\lt A$.", "sprt"),

 Q(r"The SPRT for $H_0:p=\tfrac12$ against $H_1:p=\tfrac34$ on Bernoulli observations continues while the number "
   r"of successes $S_n$ lies between two parallel lines $a_0+sn$ and $a_1+sn$. The common slope $s$ is:",
   ["0.500", "0.631", "0.750", "0.585"], "B",
   r"$\ln\lambda_n=S_n\ln\dfrac{p_1}{p_0}+(n-S_n)\ln\dfrac{q_1}{q_0}$, so "
   r"$s=\dfrac{\ln(q_0/q_1)}{\ln\dfrac{p_1q_0}{p_0q_1}}=\dfrac{\ln2}{\ln3}=0.631$. The slope always lies between $p_0$ "
   r"and $p_1$.", "sprt"),

 Q(r"The SPRT with $\alpha=\beta=0.05$ is used for $H_0:\theta=0$ against $H_1:\theta=1$ on observations from "
   r"$N(\theta,1)$. With $\ln19=2.944$, the approximate expected sample size when $H_0$ is true is:",
   ["2.65", "10.6", "5.30", "11.8"], "C",
   r"$Z=\ln\dfrac{f_1(X)}{f_0(X)}=X-\tfrac12$, so $E_0(Z)=-\tfrac12$. With $\ln A=2.944$, $\ln B=-2.944$: "
   r"$E_0(N)\approx\dfrac{(1-\alpha)\ln B+\alpha\ln A}{E_0(Z)}=\dfrac{-2.797+0.147}{-0.5}=5.30$. The fixed-sample "
   r"test with the same errors needs $n=(1.645+1.645)^2\approx11$.", "sprt"),

 Q(r"Consider the statements about Wald's SPRT for a simple $H_0$ against a simple $H_1$:"
   + st("It terminates with probability one.",
        r"Among all tests with error probabilities not exceeding $\alpha$ and $\beta$, it minimises the expected "
        r"sample size under both $H_0$ and $H_1$.",
        r"With Wald's approximate boundaries, the true error probabilities satisfy $\alpha'+\beta'\le\alpha+\beta$.",
        "The number of observations is fixed before sampling begins.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "II, III and IV only", "I, II, III and IV"], "B",
   r"(I) is Stein's result, (II) the Wald&ndash;Wolfowitz optimality theorem, and (III) follows from "
   r"$\dfrac{\alpha'}{1-\beta'}\le\dfrac1A$ and $\dfrac{\beta'}{1-\alpha'}\le B$. (IV) is false: the sample size is a "
   r"random variable, decided by the data as they come.", "sprt"),

 Q(r"Let $L(\theta)$ be the operating characteristic function (the probability of accepting $H_0$) of the SPRT "
   r"of $H_0:\theta=\theta_0$ against $H_1:\theta=\theta_1$ with strength $(\alpha,\beta)$. Then $L(\theta_0)$ and "
   r"$L(\theta_1)$ are approximately:",
   [r"$1-\alpha$ and $\beta$", r"$\alpha$ and $1-\beta$", r"$1-\alpha$ and $1-\beta$", r"$\alpha$ and $\beta$"], "A",
   r"$L(\theta_0)$ is the probability of accepting a true $H_0$, $1-\alpha$; $L(\theta_1)$ is the probability of "
   r"accepting a false $H_0$, the type II error $\beta$. Wald's formula "
   r"$L(\theta)\approx\dfrac{A^{h}-1}{A^{h}-B^{h}}$ gives these at $h=1$ and $h=-1$.", "sprt"),

 Q(r"A die is thrown 60 times and the faces 1 to 6 appear 8, 9, 10, 13, 12 and 8 times. The value of the "
   r"chi-square statistic for testing that the die is unbiased, and its degrees of freedom, are:",
   ["22 and 5", "2.2 and 6", "0.37 and 5", "2.2 and 5"], "D",
   r"Each expected frequency is 10. $\chi^2=\dfrac{4+1+0+9+4+4}{10}=2.2$ with $6-1=5$ degrees of freedom. The 5% "
   r"point of $\chi^2_5$ is 11.07, so the hypothesis of an unbiased die is not rejected.", "chi2"),

 Q(r"A $2\times2$ table has cell frequencies $a=20$, $b=10$ (first row) and $c=10$, $d=20$ (second row). The "
   r"values of the chi-square statistic for independence without and with Yates' correction are, respectively:",
   ["6.67 and 6.00", "5.40 and 6.67", "6.67 and 5.40", "3.33 and 2.70"], "C",
   r"$\chi^2=\dfrac{N(ad-bc)^2}{(a+b)(c+d)(a+c)(b+d)}=\dfrac{60(300)^2}{30^4}=6.67$. With Yates' correction "
   r"$|ad-bc|$ is reduced by $\tfrac N2=30$: $\dfrac{60(270)^2}{30^4}=5.40$. The correction always reduces the "
   r"statistic.", "chi2"),

 Q(r"A Poisson distribution is fitted to a frequency distribution, its mean being estimated from the data, and "
   r"after pooling small expected frequencies 7 classes remain. The degrees of freedom of the chi-square "
   r"goodness-of-fit statistic are:",
   ["6", "5", "7", "4"], "B",
   r"Degrees of freedom $=$ classes $-1-$ parameters estimated $=7-1-1=5$. One is lost for the condition "
   r"$\sum O=\sum E$ and one for the estimated mean. For a fitted normal distribution two parameters are "
   r"estimated and the figure would be 4.", "chi2"),

 Q(r"Samples from 3 populations are each classified into the same 4 categories. The degrees of freedom of the "
   r"chi-square test of homogeneity of the three populations are:",
   ["6", "12", "11", "9"], "A",
   r"The data form a $3\times4$ table and the test is computed exactly as for independence: "
   r"$(3-1)(4-1)=6$ degrees of freedom.", "chi2"),

 Q(r"A sample of 25 from a normal population has $s^2=36$ (divisor $n-1$). To test $H_0:\sigma^2=25$ against "
   r"$H_1:\sigma^2\gt25$ at the 5% level, given that the upper 5% point of $\chi^2_{24}$ is 36.42, the statistic "
   r"and the decision are:",
   ["36.00; do not reject $H_0$", "34.56; reject $H_0$", "36.00; reject $H_0$", "34.56; do not reject $H_0$"], "D",
   r"$\chi^2=\dfrac{(n-1)s^2}{\sigma_0^2}=\dfrac{24\times36}{25}=34.56$ on 24 degrees of freedom. Since "
   r"$34.56\lt36.42$, $H_0$ is not rejected at the 5% level.", "chi2"),

 Q(r"Consider the statements about the chi-square test of goodness of fit:"
   + st(r"$\sum(O-E)^2/E$ is approximately chi-square when the expected frequencies are large.",
        "One degree of freedom is lost for each parameter efficiently estimated from the grouped data.",
        "The test is two-tailed: very small values of the statistic also lead to rejection of the fitted model.",
        r"The condition $\sum O=\sum E$ accounts for the loss of one degree of freedom.")
   + "Which of the statements are correct?",
   ["I and II only", "I and IV only", "I, II and IV only", "I, II, III and IV"], "C",
   r"(I), (II) and (IV) are the standard conditions. (III) is false: only large values of the statistic, i.e. "
   r"large disagreement between observed and expected frequencies, are evidence against the model, so the test "
   r"uses the upper tail alone.", "chi2"),

 Q(r"In a contingency table with $N=80$ observations the chi-square statistic is 20. Pearson's coefficient of "
   r"contingency is:",
   ["0.200", "0.447", "0.500", "0.250"], "B",
   r"$C=\sqrt{\dfrac{\chi^2}{\chi^2+N}}=\sqrt{\dfrac{20}{100}}=\sqrt{0.2}=0.447$. $C$ is 0 under independence but can "
   r"never reach 1.", "chi2"),

 Q(r"In 10 paired comparisons, 8 differences are positive and 2 are negative. The two-sided $p$-value of the "
   r"sign test is about:",
   ["0.109", "0.055", "0.044", "0.021"], "A",
   r"Under $H_0$ the number of plus signs is $\text{Bin}(10,\tfrac12)$. "
   r"$P(X\ge8)=\dfrac{45+10+1}{1024}=0.0547$, and the two-sided $p$-value is $2(0.0547)=0.109$. The hypothesis of "
   r"no difference is not rejected at the 5% level.", "sign"),

 Q(r"For normal populations, the asymptotic relative efficiency of the sign test with respect to the $t$ test "
   r"is:",
   [r"$\dfrac3\pi$", r"$\dfrac\pi2$", r"$\dfrac12$", r"$\dfrac2\pi$"], "D",
   r"The efficiency of the sign test is $4f(0)^2\sigma^2$, which for the normal density is $\dfrac2\pi\approx0.637$, "
   r"the same as that of the median relative to the mean. $\dfrac3\pi\approx0.955$ is the figure for the Wilcoxon "
   r"signed-rank test.", "sign"),

 Q(r"In a sign test based on 100 non-zero differences, 60 are positive. Without a continuity correction, the "
   r"normal test statistic is:",
   ["1.0", "4.0", "2.0", "2.5"], "C",
   r"Under $H_0$ the number of plus signs has mean $\tfrac n2=50$ and standard deviation $\tfrac{\sqrt n}{2}=5$. "
   r"$z=\dfrac{60-50}{5}=2.0$. With the continuity correction it is $\dfrac{59.5-50}{5}=1.9$.", "sign"),

 Q(r"For the Wilcoxon signed-rank statistic $T^+$ based on $n=10$ differences (no zeros or ties), the mean and "
   r"the variance under $H_0$ are:",
   ["55 and 96.25", "27.5 and 96.25", "27.5 and 192.5", "27.5 and 38.5"], "B",
   r"$E(T^+)=\dfrac{n(n+1)}{4}=\dfrac{110}{4}=27.5$ and "
   r"$V(T^+)=\dfrac{n(n+1)(2n+1)}{24}=\dfrac{10\cdot11\cdot21}{24}=96.25$.", "wsr"),

 Q(r"The differences in six matched pairs are $3,\,-1,\,5,\,-2,\,4,\,6$. The Wilcoxon signed-rank statistic "
   r"$T^+$ (the sum of the ranks of the positive differences) is:",
   ["18", "3", "15", "21"], "A",
   r"The absolute values $1,2,3,4,5,6$ have ranks $1,\dots,6$. The positive differences $3,5,4,6$ have ranks "
   r"$3,5,4,6$, so $T^+=18$; the negative ones give $T^-=1+2=3$, and $T^++T^-=21=\tfrac{n(n+1)}{2}$.", "wsr"),

 Q(r"For $n=4$ differences without ties, the exact null probability $P(T^+\le1)$ of the Wilcoxon signed-rank "
   r"statistic is:",
   [r"$\dfrac1{16}$", r"$\dfrac3{16}$", r"$\dfrac14$", r"$\dfrac18$"], "D",
   r"Under $H_0$ each of the $2^4=16$ assignments of signs to the ranks $1,2,3,4$ is equally likely. "
   r"$T^+=0$ for one assignment (no positive ranks) and $T^+=1$ for one (only rank 1 positive), so "
   r"$P(T^+\le1)=\tfrac2{16}=\tfrac18$.", "wsr"),

 Q(ar("For symmetric populations, the Wilcoxon signed-rank test is generally more powerful than the sign test.",
      "It uses the ranks of the magnitudes of the differences as well as their signs."),
   AR, "A",
   r"The sign test throws away the sizes of the differences; the signed-rank test keeps their order, at the "
   r"price of assuming symmetry. For normal populations the efficiencies relative to the $t$ test are "
   r"$\tfrac3\pi=0.955$ and $\tfrac2\pi=0.637$. Both statements are true and (R) is the reason.", "wsr"),

 Q(r"For the Mann&ndash;Whitney statistic $U$ with sample sizes $m=4$ and $n=5$ (no ties), the mean and the "
   r"variance under $H_0$ are:",
   ["10 and 15", "20 and 16.67", "10 and 16.67", "10 and 33.33"], "C",
   r"$E(U)=\dfrac{mn}{2}=10$ and $V(U)=\dfrac{mn(m+n+1)}{12}=\dfrac{20\times10}{12}=16.67$.", "mw"),

 Q(r"Sample $X$: 1, 4, 6. Sample $Y$: 2, 3, 5, 7. The sum $W$ of the ranks of the $X$ observations in the "
   r"combined sample, and the number $U$ of pairs $(x,y)$ with $x\gt y$, are:",
   ["11 and 7", "11 and 5", "17 and 5", "10 and 6"], "B",
   r"In the combined ordering $1,2,3,4,5,6,7$ the $X$ values have ranks 1, 4, 6, so $W=11$. "
   r"$U=W-\dfrac{m(m+1)}{2}=11-6=5$: directly, 1 exceeds no $y$, 4 exceeds two, 6 exceeds three. The other count, "
   r"pairs with $x\lt y$, is $mn-U=7$.", "mw"),

 Q(r"For two samples of sizes $m=n=3$ from the same continuous distribution, the probability that the "
   r"Mann&ndash;Whitney statistic $U$ equals 0 is:",
   [r"$\dfrac1{10}$", r"$\dfrac16$", r"$\dfrac19$", r"$\dfrac1{20}$"], "D",
   r"Under $H_0$ all $\binom63=20$ ways of choosing which ranks belong to the first sample are equally likely. "
   r"$U=0$ only when the first sample has the ranks $1,2,3$, so the probability is $\tfrac1{20}$. A two-sided test "
   r"with $m=n=3$ therefore cannot reach the 5% level.", "mw"),

 Q(r"Match the population in List I with the asymptotic relative efficiency of the Wilcoxon "
   r"(Mann&ndash;Whitney) test with respect to the $t$ test in List II."
   + match(["Normal", "Uniform", "Double exponential", "Least possible value over all continuous distributions"],
           ["1.5", "0.864", r"$\dfrac3\pi$", "1"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(ii), (b)-(iv), (c)-(i), (d)-(iii)"], "C",
   r"The efficiency is $12\sigma^2\left[\int f^2(x)\,dx\right]^2$: $\tfrac3\pi\approx0.955$ for the normal, 1 for the "
   r"uniform, 1.5 for the double exponential. Hodges and Lehmann showed it is never below $0.864$, so the "
   r"Wilcoxon test loses little at worst and can gain a great deal for heavy-tailed populations.", "mw"),

 Q(r"Which of the following two-sample rank tests is a test for a difference in scale (dispersion) and not in "
   r"location?",
   ["Wilcoxon rank-sum test", "Ansari&ndash;Bradley test", "van der Waerden normal scores test", "Median test"], "B",
   r"A linear rank statistic is $\sum a(R_i)$ over one sample. The Wilcoxon scores $a(i)=i$, the normal scores "
   r"$\Phi^{-1}\left(\tfrac{i}{N+1}\right)$ and the median-test scores are increasing in $i$ and detect shifts in "
   r"location. The Ansari&ndash;Bradley scores (like those of Mood and Siegel&ndash;Tukey) are large in the "
   r"middle and small at both ends, so they detect differences in spread.", "linrank"),

 Q(r"The asymptotic relative efficiency of the normal scores (van der Waerden) test with respect to the "
   r"two-sample $t$ test is:",
   ["never less than 1", r"always equal to $\dfrac3\pi$", "never more than 1", "never less than 0.864 and may be below 1"], "A",
   r"By the Chernoff&ndash;Savage theorem this efficiency is at least 1 for every continuous distribution with "
   r"finite variance, with equality only for the normal. The bound $0.864$ belongs to the Wilcoxon test.", "linrank"),

 Q(r"Three samples of size 3 have the ranks $\{1,2,3\}$, $\{4,5,6\}$ and $\{7,8,9\}$ in the combined sample. The "
   r"Kruskal&ndash;Wallis statistic $H$ is:",
   ["5.6", "6.0", "8.0", "7.2"], "D",
   r"Rank sums are 6, 15, 24. "
   r"$H=\dfrac{12}{N(N+1)}\sum\dfrac{R_i^2}{n_i}-3(N+1)=\dfrac{12}{90}\cdot\dfrac{36+225+576}{3}-30=37.2-30=7.2$. "
   r"This complete separation is the largest value $H$ can take for three samples of 3; it is referred to "
   r"$\chi^2_2$ in large samples.", "kw"),
]
