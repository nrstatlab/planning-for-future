# -*- coding: utf-8 -*-
"""UGC NET Statistics, Unit IV: fifty exam-standard model questions."""
from . import AR, Q, ar, match, st

TITLE = "Estimation Theory"
BLURB = ("Unbiasedness, consistency and efficiency; method of moments and maximum likelihood; the "
         "Cram&eacute;r&ndash;Rao bound; sufficiency, completeness and ancillarity; Rao&ndash;Blackwell, "
         "Lehmann&ndash;Scheff&eacute; and Basu; confidence intervals; order statistics and rank correlation.")

QUESTIONS = [
 Q(r"If $X\sim\text{Bin}(n,p)$ with $n\ge2$, an unbiased estimator of $p^2$ is:",
   [r"$\left(\dfrac Xn\right)^2$", r"$\dfrac{X(X-1)}{n(n-1)}$", r"$\dfrac{X^2}{n(n-1)}$", r"$\dfrac{X(n-X)}{n(n-1)}$"], "B",
   r"The second factorial moment of the binomial is $E[X(X-1)]=n(n-1)p^2$, so $\dfrac{X(X-1)}{n(n-1)}$ is unbiased "
   r"for $p^2$. $(X/n)^2$ has expectation $p^2+\dfrac{pq}{n}$, and option D is unbiased for $pq$.", "unbiased"),

 Q(r"Let $X$ be a single observation from the Poisson distribution with mean $\lambda$. The only unbiased "
   r"estimator of $e^{-2\lambda}$ is:",
   [r"$e^{-2X}$", r"$2^{-X}$", r"$e^{-X}$", r"$(-1)^X$"], "D",
   r"$E[(-1)^X]=\sum_x(-1)^x\dfrac{e^{-\lambda}\lambda^x}{x!}=e^{-\lambda}e^{-\lambda}=e^{-2\lambda}$, and by "
   r"completeness of the Poisson family it is the only unbiased estimator. It takes only the values $\pm1$ for a "
   r"quantity lying in $(0,1)$: an unbiased, indeed UMVU, estimator can be absurd.", "unbiased"),

 Q(r"Let $X_1,\dots,X_n$ be a random sample from $N(\mu,\sigma^2)$, both parameters unknown. Among estimators of "
   r"$\sigma^2$ of the form $c\sum(X_i-\bar X)^2$, the mean squared error is least for $c=$",
   [r"$\dfrac1{n+1}$", r"$\dfrac1n$", r"$\dfrac1{n-1}$", r"$\dfrac1{n-2}$"], "A",
   r"With $W=\sum(X_i-\bar X)^2\sim\sigma^2\chi^2_{n-1}$: $E(W)=(n-1)\sigma^2$, $E(W^2)=(n^2-1)\sigma^4$. "
   r"$\text{MSE}(cW)=\sigma^4\left[c^2(n^2-1)-2c(n-1)+1\right]$ is least at $c=\dfrac{1}{n+1}$. The divisor $n-1$ "
   r"gives the unbiased estimator and $n$ the maximum likelihood estimator; neither minimises the MSE.", "unbiased"),

 Q(r"Let $X_1,\dots,X_n$ $(n\gt1)$ be a random sample from the uniform distribution on $(0,\theta)$. Consider the "
   r"statements:"
   + st(r"$2\bar X$ is unbiased for $\theta$.", r"$X_{(n)}$ is unbiased for $\theta$.",
        r"$\dfrac{n+1}{n}X_{(n)}$ is unbiased for $\theta$.",
        r"$\dfrac{n+1}{n}X_{(n)}$ has smaller variance than $2\bar X$.")
   + "Which of the statements are correct?",
   ["I and III only", "I and II only", "I, III and IV only", "I, II, III and IV"], "C",
   r"$E(\bar X)=\tfrac\theta2$: (I) true. $E(X_{(n)})=\dfrac{n}{n+1}\theta$: (II) false and (III) true. "
   r"$V(2\bar X)=\dfrac{\theta^2}{3n}$, while $V\left(\tfrac{n+1}{n}X_{(n)}\right)=\dfrac{\theta^2}{n(n+2)}$, smaller for "
   r"every $n\gt1$ and of order $1/n^2$: (IV) true.", "unbiased"),

 Q(r"For a random sample from the Cauchy distribution with location $\theta$, "
   r"$f(x)=\dfrac{1}{\pi[1+(x-\theta)^2]}$, which of the following is a consistent estimator of $\theta$?",
   ["The sample mean", "The sample median", r"The mid-range $\tfrac12(X_{(1)}+X_{(n)})$", "The first observation $X_1$"], "B",
   r"The mean of $n$ Cauchy observations has the same Cauchy distribution as one observation, so it does not "
   r"settle down; the mid-range is even worse. The sample median is asymptotically normal about $\theta$ with "
   r"variance $\dfrac{1}{4nf(\theta)^2}=\dfrac{\pi^2}{4n}\to0$, hence consistent.", "consist"),

 Q(r"Consider the statements:"
   + st("An unbiased estimator whose variance tends to zero is consistent.",
        "Every consistent estimator is unbiased.",
        r"If $T_n$ is consistent for $\theta$ and $g$ is continuous, then $g(T_n)$ is consistent for $g(\theta)$.",
        "A maximum likelihood estimator is always unbiased.")
   + "Which of the statements are correct?",
   ["I and III only", "I and II only", "I, III and IV only", "II and IV only"], "A",
   r"(I) follows from Chebyshev's inequality and (III) is the invariance of consistency under continuous maps. "
   r"(II) is false: $\tfrac1n\sum(X_i-\bar X)^2$ is consistent but biased for $\sigma^2$. (IV) is false for the same "
   r"example, which is the maximum likelihood estimator in the normal case.", "consist"),

 Q(r"Let $X_{(n)}$ be the largest of $n$ independent observations from the uniform distribution on $(0,\theta)$. "
   r"As $n\to\infty$, the distribution of $n(\theta-X_{(n)})$ converges to:",
   [r"$N(0,\theta^2)$", r"the uniform distribution on $(0,\theta)$", r"the exponential distribution with mean $1/\theta$",
    r"the exponential distribution with mean $\theta$"], "D",
   r"$P\{n(\theta-X_{(n)})\gt t\}=P\left\{X_{(n)}\lt\theta-\tfrac tn\right\}=\left(1-\dfrac{t}{n\theta}\right)^n\to e^{-t/\theta}$. "
   r"So the limit is exponential with mean $\theta$. The rate is $n$, not $\sqrt n$, and the limit is not normal: "
   r"the usual regularity conditions fail because the support depends on $\theta$.", "consist"),

 Q(r"A random sample from a gamma distribution with shape $\alpha$ and scale $\beta$ (mean $\alpha\beta$) has "
   r"sample mean 6 and sample variance 12. The method-of-moments estimates $(\hat\alpha,\hat\beta)$ are:",
   ["(2, 3)", "(6, 1)", "(3, 2)", "(12, 0.5)"], "C",
   r"Mean $\alpha\beta=6$ and variance $\alpha\beta^2=12$ give $\hat\beta=\dfrac{12}{6}=2$ and "
   r"$\hat\alpha=\dfrac{6^2}{12}=3$.", "mom"),

 Q(r"A random sample from the density $f(x;\theta)=\theta x^{\theta-1}$, $0\lt x\lt1$, has mean $\bar x=0.6$. "
   r"The method-of-moments estimate of $\theta$ is:",
   ["1.5", "0.6", "2.5", "0.667"], "A",
   r"$E(X)=\dfrac{\theta}{\theta+1}$. Setting this equal to $\bar x$: $\hat\theta=\dfrac{\bar x}{1-\bar x}=\dfrac{0.6}{0.4}=1.5$. "
   r"The maximum likelihood estimator, $-n/\sum\ln x_i$, is a different function of the sample.", "mom"),

 Q(r"A random sample of size 10 from the density $f(x;\theta)=\theta x^{\theta-1}$, $0\lt x\lt1$, gives "
   r"$\sum\ln x_i=-4$. The maximum likelihood estimate of $\theta$ is:",
   ["0.4", "4", "0.25", "2.5"], "D",
   r"$\ln L=n\ln\theta+(\theta-1)\sum\ln x_i$, so $\dfrac{\partial\ln L}{\partial\theta}=\dfrac n\theta+\sum\ln x_i=0$ gives "
   r"$\hat\theta=-\dfrac{n}{\sum\ln x_i}=\dfrac{10}{4}=2.5$.", "mle"),

 Q(r"For a random sample from the uniform distribution on $(\theta,\theta+1)$, the maximum likelihood "
   r"estimator of $\theta$ is:",
   [r"$X_{(1)}$ only", r"$X_{(n)}-1$ only", r"any value in the interval $\left[X_{(n)}-1,\;X_{(1)}\right]$", r"$\bar X-\tfrac12$ only"], "C",
   r"The likelihood is 1 when $\theta\le X_{(1)}$ and $X_{(n)}\le\theta+1$, and 0 otherwise. It is constant on "
   r"$[X_{(n)}-1,X_{(1)}]$, so every point of this interval maximises it: the maximum likelihood estimator need "
   r"not be unique.", "mle"),

 Q(r"For a random sample of odd size from the double exponential density "
   r"$f(x;\theta)=\tfrac12e^{-|x-\theta|}$, the maximum likelihood estimator of $\theta$ is:",
   ["the sample mean", "the sample median", "the mid-range", "the sample mode"], "B",
   r"$\ln L=-n\ln2-\sum|x_i-\theta|$. Maximising it means minimising $\sum|x_i-\theta|$, which is done by the "
   r"sample median. (For the normal density the same argument with squares gives the mean.)", "mle"),

 Q(r"A random sample of size 10 from $N(\mu,\sigma^2)$ gives $\bar x=20$ and $\sum(x_i-\bar x)^2=90$. The maximum "
   r"likelihood estimate of the 95th percentile $\mu+1.645\,\sigma$ is:",
   ["24.935", "25.202", "34.805", "21.645"], "A",
   r"The maximum likelihood estimates are $\hat\mu=\bar x=20$ and $\hat\sigma^2=\tfrac1n\sum(x_i-\bar x)^2=9$, so "
   r"$\hat\sigma=3$. By the invariance property, the estimate of $\mu+1.645\sigma$ is $20+1.645(3)=24.935$. Using "
   r"the divisor $n-1$ ($s=3.162$) gives 25.202, which is not the maximum likelihood estimate.", "mle"),

 Q(r"For a random sample from $f(x;\mu,\theta)=\dfrac1\theta e^{-(x-\mu)/\theta}$, $x\gt\mu$, with both parameters "
   r"unknown, the maximum likelihood estimators of $\mu$ and $\theta$ are:",
   [r"$\bar X$ and $S$", r"$X_{(1)}$ and $\bar X$", r"$X_{(1)}$ and $\bar X-X_{(1)}$", r"$X_{(n)}$ and $\bar X-X_{(n)}$"], "C",
   r"$L=\theta^{-n}\exp\{-\sum(x_i-\mu)/\theta\}$ for $\mu\le x_{(1)}$. For any $\theta$ it increases with $\mu$, so "
   r"$\hat\mu=X_{(1)}$. Then maximising over $\theta$ gives $\hat\theta=\tfrac1n\sum(X_i-X_{(1)})=\bar X-X_{(1)}$.", "mle"),

 Q(r"Let $\hat\lambda=\bar X$ be the maximum likelihood estimator of the mean of a Poisson distribution from a "
   r"sample of size $n$. The asymptotic variance of the maximum likelihood estimator of $P(X=0)=e^{-\lambda}$ is:",
   [r"$\dfrac{\lambda}{n}$", r"$\dfrac{e^{-2\lambda}}{n}$", r"$\dfrac{e^{-\lambda}(1-e^{-\lambda})}{n}$", r"$\dfrac{\lambda e^{-2\lambda}}{n}$"], "D",
   r"By invariance the estimator is $e^{-\bar X}$, and by the delta method its asymptotic variance is "
   r"$[g'(\lambda)]^2\,\dfrac\lambda n=\dfrac{\lambda e^{-2\lambda}}{n}$. Option C is the variance of the proportion of "
   r"zeros in the sample, a less efficient estimator.", "mle"),

 Q(r"A random sample from $N(\theta,\theta)$, $\theta\gt0$ (mean and variance both equal to $\theta$), has "
   r"$\tfrac1n\sum x_i^2=6$. The maximum likelihood estimate of $\theta$ is:",
   ["6", "2", r"$\sqrt6$", "3"], "B",
   r"$\ln L=-\tfrac n2\ln\theta-\dfrac{\sum x_i^2}{2\theta}+\sum x_i-\dfrac{n\theta}{2}+\text{const}$. Differentiating, "
   r"$\theta^2+\theta-\tfrac1n\sum x_i^2=0$, so $\hat\theta=\dfrac{-1+\sqrt{1+4(6)}}{2}=2$. Note that it depends on "
   r"the data only through $\sum x_i^2$, the sufficient statistic.", "mle"),

 Q(r"For large samples from a normal population, the efficiency of the sample median relative to the sample "
   r"mean as an estimator of $\mu$ is:",
   [r"$\dfrac2\pi$", r"$\dfrac\pi2$", r"$\dfrac12$", r"$\dfrac3\pi$"], "A",
   r"$V(\bar X)=\dfrac{\sigma^2}{n}$ and the asymptotic variance of the median is "
   r"$\dfrac{1}{4nf(\mu)^2}=\dfrac{\pi\sigma^2}{2n}$. The ratio is $\dfrac2\pi\approx0.637$: the median wastes about "
   r"36% of the observations. $\tfrac3\pi$ is the corresponding figure for the Hodges&ndash;Lehmann estimator.", "eff"),

 Q(r"Let $X_1,\dots,X_n$ be a random sample from $N(\theta,1)$. The uniformly minimum variance unbiased "
   r"estimator of $\theta^2$ is:",
   [r"$\bar X^2$", r"$\bar X^2-\dfrac1n$", r"$\dfrac1n\sum X_i^2-1$", r"$\bar X^2+\dfrac1n$"], "B",
   r"$\bar X$ is complete and sufficient, and $E(\bar X^2)=\theta^2+\tfrac1n$. So $\bar X^2-\tfrac1n$ is an unbiased "
   r"function of the complete sufficient statistic, hence the UMVUE by Lehmann&ndash;Scheff&eacute;. Option C is "
   r"also unbiased but is not a function of $\bar X$ alone.", "eff"),

 Q(r"For a random sample of size $n$ from $N(0,\sigma^2)$, the Cram&eacute;r&ndash;Rao lower bound for the "
   r"variance of an unbiased estimator of $\sigma^2$ is:",
   [r"$\dfrac{\sigma^4}{n}$", r"$\dfrac{2\sigma^4}{n-1}$", r"$\dfrac{\sigma^2}{n}$", r"$\dfrac{2\sigma^4}{n}$"], "D",
   r"With $\phi=\sigma^2$: $\ln f=-\tfrac12\ln\phi-\dfrac{x^2}{2\phi}+\text{const}$, and "
   r"$I(\phi)=-E\left[\dfrac{1}{2\phi^2}-\dfrac{x^2}{\phi^3}\right]=\dfrac{1}{2\phi^2}$. The bound is "
   r"$\dfrac{1}{nI}=\dfrac{2\sigma^4}{n}$, attained by $\tfrac1n\sum X_i^2$. $\dfrac{2\sigma^4}{n-1}$ is the variance of "
   r"$S^2$ when the mean is unknown.", "crlb"),

 Q(r"For a random sample of size $n$ from the Bernoulli distribution with parameter $p$, the "
   r"Cram&eacute;r&ndash;Rao lower bound for the variance of an unbiased estimator of $p(1-p)$ is:",
   [r"$\dfrac{(1-2p)^2\,p(1-p)}{n}$", r"$\dfrac{p(1-p)}{n}$", r"$\dfrac{p^2(1-p)^2}{n}$", r"$\dfrac{(1-2p)^2}{n\,p(1-p)}$"], "A",
   r"For $g(p)=p(1-p)$ the bound is $\dfrac{[g'(p)]^2}{nI(p)}$ with $g'(p)=1-2p$ and $I(p)=\dfrac{1}{p(1-p)}$, giving "
   r"$\dfrac{(1-2p)^2p(1-p)}{n}$. At $p=\tfrac12$ the bound is zero, although no estimator has zero variance: the "
   r"bound is not attained.", "crlb"),

 Q(r"For a random sample of size $n$ from the Cauchy density $\dfrac{1}{\pi[1+(x-\theta)^2]}$, the "
   r"Cram&eacute;r&ndash;Rao lower bound for unbiased estimators of $\theta$ is:",
   [r"$\dfrac1n$", r"$\dfrac{\pi^2}{4n}$", r"$\dfrac2n$", r"$\dfrac{1}{2n}$"], "C",
   r"$\dfrac{\partial\ln f}{\partial\theta}=\dfrac{2(x-\theta)}{1+(x-\theta)^2}$, and "
   r"$I(\theta)=\displaystyle\int\frac{4u^2}{(1+u^2)^2}\cdot\frac{du}{\pi(1+u^2)}=\frac12$. The bound is "
   r"$\dfrac{1}{nI}=\dfrac2n$. The sample median has asymptotic variance $\dfrac{\pi^2}{4n}\approx\dfrac{2.47}{n}$, "
   r"so its efficiency is $8/\pi^2\approx81\%$.", "crlb"),

 Q(r"Consider the statements about the Cram&eacute;r&ndash;Rao lower bound for a parametric function "
   r"$g(\theta)$:"
   + st(r"An unbiased estimator $T$ attains the bound if and only if "
        r"$\dfrac{\partial\ln L}{\partial\theta}=A(\theta)\,[T-g(\theta)]$.",
        "The bound can be attained only when the distribution belongs to a one-parameter exponential family.",
        r"For the uniform distribution on $(0,\theta)$ there is an unbiased estimator of $\theta$ with variance "
        r"smaller than $\theta^2/n$.",
        "A uniformly minimum variance unbiased estimator always attains the bound.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "I, III and IV only", "I, II, III and IV"], "B",
   r"(I) is the condition for equality in the Cauchy&ndash;Schwarz inequality, and integrating it gives the "
   r"exponential family form: (II). (III) $\tfrac{n+1}{n}X_{(n)}$ has variance $\dfrac{\theta^2}{n(n+2)}$; the "
   r"regularity conditions fail, so there is no contradiction. (IV) is false: the UMVUE of $e^{-\lambda}$ in the "
   r"Poisson case has variance above the bound.", "crlb"),

 Q(ar(r"For a Poisson sample, the UMVUE $\left(1-\tfrac1n\right)^{\sum X_i}$ of $e^{-\lambda}$ does not attain the "
      r"Cram&eacute;r&ndash;Rao lower bound.",
      r"In the Poisson family the bound is attained only by estimators of linear functions $a\lambda+b$."),
   AR, "A",
   r"$\dfrac{\partial\ln L}{\partial\lambda}=\dfrac n\lambda(\bar X-\lambda)$, so equality holds only for $T=\bar X$ and "
   r"linear functions of it, estimating $a\lambda+b$. $e^{-\lambda}$ is not linear in $\lambda$, so its UMVUE, though "
   r"best among unbiased estimators, has variance $e^{-2\lambda}(e^{\lambda/n}-1)\gt\dfrac{\lambda e^{-2\lambda}}{n}$. "
   r"Both statements are true and (R) explains (A).", "crlb"),

 Q(r"For a random sample from the uniform distribution on $(-\theta,\theta)$, a sufficient statistic for "
   r"$\theta$ is:",
   [r"$\bar X$", r"$X_{(n)}$", r"$X_{(n)}-X_{(1)}$", r"$\max_i|X_i|$"], "D",
   r"$L=(2\theta)^{-n}$ if $-\theta\lt x_{(1)}$ and $x_{(n)}\lt\theta$, i.e. if $\max|x_i|\lt\theta$, and 0 otherwise. "
   r"By the factorisation theorem $\max|X_i|=\max\{-X_{(1)},X_{(n)}\}$ is sufficient. $X_{(n)}$ alone is not, "
   r"because a large negative observation also restricts $\theta$.", "suff"),

 Q(r"For a random sample from the density $f(x;\theta)=\theta(1+x)^{-(\theta+1)}$, $x\gt0$, a sufficient "
   r"statistic for $\theta$ is:",
   [r"$\sum X_i$", r"$\prod X_i$", r"$\sum\ln(1+X_i)$", r"$X_{(n)}$"], "C",
   r"$L=\theta^n\exp\{-(\theta+1)\sum\ln(1+x_i)\}$, which depends on the sample only through "
   r"$\sum\ln(1+x_i)$ (equivalently $\prod(1+x_i)$). It is a one-parameter exponential family, so this statistic "
   r"is also complete.", "suff"),

 Q(r"Consider the statements about sufficiency for a random sample $X_1,\dots,X_n$:"
   + st("The whole sample is a sufficient statistic.",
        "A one-to-one function of a sufficient statistic is sufficient.",
        "Every function of a sufficient statistic is sufficient.",
        "The set of order statistics is sufficient.")
   + "Which of the statements are correct?",
   ["I, II and IV only", "I and II only", "I, II and III only", "I, II, III and IV"], "A",
   r"(I) is trivially true, (II) holds because nothing is lost by a one-to-one map, and (IV) holds because the "
   r"joint density of independent, identically distributed observations is symmetric. (III) is false: a "
   r"constant is a function of any statistic. The correct statement is that any statistic of which a sufficient "
   r"statistic is a function is itself sufficient.", "suff"),

 Q(r"$X_1$ and $X_2$ are independent Poisson variates with the same mean $\lambda$. Then "
   r"$P(X_1=1\mid X_1+X_2=2)$ equals:",
   [r"$\lambda e^{-\lambda}$", r"$\dfrac14$", r"$\dfrac13$", r"$\dfrac12$"], "D",
   r"Given $X_1+X_2=t$, $X_1\sim\text{Bin}\left(t,\tfrac12\right)$, so the probability is $\binom21\left(\tfrac12\right)^2=\tfrac12$. "
   r"It does not involve $\lambda$, which is what the sufficiency of $X_1+X_2$ means.", "suff"),

 Q(r"For a random sample from the uniform distribution on $(0,\theta)$, which of the following statistics is "
   r"ancillary?",
   [r"$X_{(n)}$", r"$X_{(n)}-X_{(1)}$", r"$\dfrac{X_{(1)}}{X_{(n)}}$", r"$\bar X$"], "C",
   r"$\theta$ is a scale parameter: $X_i=\theta U_i$ with $U_i$ uniform on $(0,1)$. Any ratio such as "
   r"$\dfrac{X_{(1)}}{X_{(n)}}=\dfrac{U_{(1)}}{U_{(n)}}$ has a distribution free of $\theta$. The range would be "
   r"ancillary in a location family, not here: its distribution scales with $\theta$.", "minsuff"),

 Q(r"For a random sample of size $n\ge2$ from the uniform distribution on "
   r"$\left(\theta-\tfrac12,\theta+\tfrac12\right)$, the statistic $(X_{(1)},X_{(n)})$ is:",
   ["sufficient and complete", "minimal sufficient but not complete", "complete but not sufficient", "neither sufficient nor complete"], "B",
   r"The likelihood is the indicator of $x_{(n)}-\tfrac12\lt\theta\lt x_{(1)}+\tfrac12$, so $(X_{(1)},X_{(n)})$ is "
   r"minimal sufficient. The range $R=X_{(n)}-X_{(1)}$ is ancillary with $E(R)=\dfrac{n-1}{n+1}$, so "
   r"$R-\dfrac{n-1}{n+1}$ is a non-zero function of the statistic with zero expectation for all $\theta$: not "
   r"complete.", "minsuff"),

 Q(r"Let $X$ be a single observation from $N(0,\sigma^2)$, $\sigma\gt0$. Consider the statements:"
   + st("$X$ is a sufficient statistic.", "$X$ is a complete statistic.", "$X^2$ is a complete sufficient statistic.",
        "$X^2$ is a minimal sufficient statistic.")
   + "Which of the statements are correct?",
   ["I, III and IV only", "I and II only", "II and III only", "I, II, III and IV"], "A",
   r"(I) The sample itself is always sufficient. (II) is false: $E(X)=0$ for every $\sigma$ although $X$ is not "
   r"zero. (III) The family is a one-parameter exponential family in $X^2$, whose natural parameter space contains "
   r"an interval. (IV) A complete sufficient statistic is minimal sufficient.", "complete"),

 Q(ar("A complete sufficient statistic is minimal sufficient.",
      "Every minimal sufficient statistic is complete."),
   AR, "C",
   r"(A) is Bahadur's theorem (when a minimal sufficient statistic exists). (R) is false: for the uniform "
   r"distribution on $(\theta-\tfrac12,\theta+\tfrac12)$, or for the Cauchy location family, the minimal sufficient "
   r"statistic is not complete.", "complete"),

 Q(r"Let $X\sim\text{Bin}(2,p)$ where the parameter space is only $\left\{\tfrac14,\tfrac34\right\}$. Then the "
   r"family of distributions of $X$ is:",
   ["complete, because every binomial family is complete",
    "complete, because $X$ is sufficient",
    "not complete, because $X$ is not sufficient",
    "not complete, because there is a non-zero $g$ with $E_p\,g(X)=0$ for both values of $p$"], "D",
   r"$E_pg(X)=g(0)q^2+2g(1)pq+g(2)p^2=0$ at the two values of $p$ gives two linear equations in three unknowns: "
   r"$9g(0)+6g(1)+g(2)=0$ and $g(0)+6g(1)+9g(2)=0$. A non-zero solution is $g(0)=g(2)=1$, $g(1)=-\tfrac53$. "
   r"Completeness depends on the parameter space: with $p\in(0,1)$ the family is complete.", "complete"),

 Q(r"$X_1,\dots,X_5$ is a random sample from the Poisson distribution with mean $\lambda$, and $\sum x_i=10$. The "
   r"Rao&ndash;Blackwell improvement of the estimator $I(X_1=0)$ of $e^{-\lambda}$ takes the value:",
   ["0.107", "0.135", "0.200", "0.328"], "A",
   r"Given $T=\sum X_i=t$, $X_1\sim\text{Bin}\left(t,\tfrac1n\right)$, so "
   r"$E[I(X_1=0)\mid T=t]=\left(1-\tfrac1n\right)^t=(0.8)^{10}=0.107$. This is the UMVUE of $e^{-\lambda}$. "
   r"The maximum likelihood estimate is $e^{-\bar x}=e^{-2}=0.135$.", "rb"),

 Q(r"$X_1,\dots,X_{10}$ are independent Bernoulli($p$) variates and $T=\sum X_i=4$ is observed. The value of the "
   r"UMVUE of $p^2$, obtained by conditioning $X_1X_2$ on $T$, is:",
   [r"$\dfrac{4}{25}$", r"$\dfrac{2}{15}$", r"$\dfrac{8}{45}$", r"$\dfrac15$"], "B",
   r"$E(X_1X_2\mid T=t)=P(X_1=1,X_2=1\mid T=t)=\dfrac{\binom{n-2}{t-2}}{\binom nt}=\dfrac{t(t-1)}{n(n-1)}=\dfrac{12}{90}=\dfrac{2}{15}$. "
   r"The maximum likelihood estimate is $(0.4)^2=\tfrac4{25}$, which is biased upward.", "rb"),

 Q(r"For a random sample from the uniform distribution on $(0,\theta)$, the UMVUE of $\theta$ is:",
   [r"$2\bar X$", r"$X_{(n)}$", r"$\dfrac{n+2}{n+1}X_{(n)}$", r"$\dfrac{n+1}{n}X_{(n)}$"], "D",
   r"$X_{(n)}$ is complete and sufficient, with $E(X_{(n)})=\dfrac{n}{n+1}\theta$. So $\dfrac{n+1}{n}X_{(n)}$ is an "
   r"unbiased function of it and is the UMVUE by Lehmann&ndash;Scheff&eacute;. $\dfrac{n+2}{n+1}X_{(n)}$ is the "
   r"multiple of $X_{(n)}$ with least mean squared error, but it is biased.", "ls"),

 Q(r"For a random sample of size $n$ from the exponential distribution with mean $\theta$, the UMVUE of "
   r"$\theta^2$ is:",
   [r"$\dfrac{n\bar X^2}{n+1}$", r"$\bar X^2$", r"$\dfrac{(n+1)\bar X^2}{n}$", r"$\dfrac{1}{2n}\sum X_i^2-\bar X^2$"], "A",
   r"$T=\sum X_i$ is complete and sufficient and is gamma with shape $n$: $E(T^2)=n(n+1)\theta^2$. So "
   r"$\dfrac{T^2}{n(n+1)}=\dfrac{n\bar X^2}{n+1}$ is the UMVUE. $\bar X^2$ overestimates $\theta^2$ on average by the "
   r"factor $\tfrac{n+1}{n}$.", "ls"),

 Q(r"For a random sample of size $n\ge2$ from the density $f(x;\lambda)=\lambda e^{-\lambda x}$, $x\gt0$, the "
   r"UMVUE of $\lambda$ is:",
   [r"$\dfrac{1}{\bar X}$", r"$\dfrac{n+1}{\sum X_i}$", r"$\dfrac{n-1}{\sum X_i}$", r"$\dfrac{n}{\sum X_i+1}$"], "C",
   r"$T=\sum X_i$ is complete and sufficient, gamma with shape $n$ and rate $\lambda$, so "
   r"$E\left(\dfrac1T\right)=\dfrac{\lambda}{n-1}$. Hence $\dfrac{n-1}{T}$ is the UMVUE. The maximum likelihood "
   r"estimator $\dfrac1{\bar X}=\dfrac nT$ is biased upward by the factor $\tfrac{n}{n-1}$.", "ls"),

 Q(ar(r"In sampling from $N(\mu,\sigma^2)$, the sample mean $\bar X$ and the sample variance $S^2$ are independent.",
      r"For any fixed $\sigma^2$, $\bar X$ is a complete sufficient statistic for $\mu$ and the distribution of $S^2$ "
      r"does not depend on $\mu$."),
   AR, "A",
   r"This is Basu's theorem: a complete sufficient statistic is independent of every ancillary statistic. For "
   r"fixed $\sigma^2$, $\bar X$ is complete sufficient for $\mu$ and $S^2$ is ancillary (it is unchanged when a "
   r"constant is added to every observation). Since this holds for each $\sigma^2$, the independence holds "
   r"throughout. Both statements are true and (R) is the reason.", "basu"),

 Q(r"$X_1,\dots,X_4$ is a random sample from the exponential distribution with mean $\theta$, and "
   r"$U=\dfrac{X_1}{X_1+X_2+X_3+X_4}$. Then $E(U^2)$ equals:",
   [r"$\dfrac1{16}$", r"$\dfrac1{10}$", r"$\dfrac18$", r"$\dfrac1{20}$"], "B",
   r"$U$ is ancillary (a ratio in a scale family) and $T=\sum X_i$ is complete sufficient, so by Basu's theorem "
   r"they are independent: $E(X_1^2)=E(U^2)E(T^2)$, i.e. $2\theta^2=E(U^2)\cdot n(n+1)\theta^2$. With $n=4$, "
   r"$E(U^2)=\dfrac{2}{20}=\dfrac1{10}$. (Directly, $U\sim\text{Beta}(1,3)$.)", "basu"),

 Q(r"The largest of 4 independent observations from the uniform distribution on $(0,\theta)$ is 8. Using the "
   r"pivot $X_{(n)}/\theta$, the shortest confidence interval for $\theta$ with confidence coefficient "
   r"$\tfrac{15}{16}$ is:",
   ["(8, 12)", "(4, 16)", "(8, 32)", "(8, 16)"], "D",
   r"$P\left(X_{(n)}/\theta\le u\right)=u^n$. The density of the pivot increases on $(0,1)$, so the shortest interval "
   r"uses $\alpha^{1/n}\le X_{(n)}/\theta\le1$, giving $\left(X_{(n)},\;X_{(n)}\alpha^{-1/n}\right)$. With "
   r"$\alpha=\tfrac1{16}$, $n=4$: $\alpha^{-1/4}=2$ and the interval is $(8,16)$.", "pivot"),

 Q(r"A random sample of size 5 from the exponential distribution with mean $\theta$ has $\sum x_i=20$. Given "
   r"$\chi^2_{10;\,0.975}=20.48$ and $\chi^2_{10;\,0.025}=3.25$ (upper-tail areas 0.025 and 0.975), the 95% "
   r"equal-tailed confidence interval for $\theta$ is:",
   ["(1.95, 12.31)", "(0.98, 6.15)", "(3.25, 20.48)", "(2.05, 7.80)"], "A",
   r"$\dfrac{2\sum X_i}{\theta}\sim\chi^2_{2n}=\chi^2_{10}$. So "
   r"$\dfrac{2\sum x_i}{20.48}\lt\theta\lt\dfrac{2\sum x_i}{3.25}$, i.e. $\dfrac{40}{20.48}=1.95$ to "
   r"$\dfrac{40}{3.25}=12.31$. Forgetting the factor 2 gives option B.", "pivot"),

 Q(r"A random sample of size 16 from a normal population gives $\bar x=50$ and $s=8$ (divisor $n-1$). Given "
   r"$t_{0.025,15}=2.131$, the 95% confidence interval for the population mean is:",
   ["(46.08, 53.92)", "(32.95, 67.05)", "(45.74, 54.26)", "(46.50, 53.50)"], "C",
   r"$\bar x\pm t\,\dfrac{s}{\sqrt n}=50\pm2.131\cdot\dfrac{8}{4}=50\pm4.26$, i.e. $(45.74,54.26)$. Using 1.96 in "
   r"place of the $t$ value gives $(46.08,53.92)$, which is too narrow for $n=16$.", "ci"),

 Q(r"A random sample of size 10 from a normal population has $s^2=4$ (divisor $n-1$). Given that the upper 2.5% "
   r"and lower 2.5% points of $\chi^2_9$ are 19.02 and 2.70, the 95% confidence interval for $\sigma^2$ is:",
   ["(2.10, 14.81)", "(1.89, 13.33)", "(0.21, 1.48)", "(1.38, 3.65)"], "B",
   r"$\dfrac{(n-1)s^2}{\sigma^2}\sim\chi^2_9$, so the interval is "
   r"$\left(\dfrac{36}{19.02},\dfrac{36}{2.70}\right)=(1.89,13.33)$. It is not symmetric about $s^2=4$. Option D is the "
   r"interval for $\sigma$, the square roots.", "ci"),

 Q(r"Consider the statements about a confidence interval for a normal mean with known variance:"
   + st("For a given sample, its width increases with the confidence coefficient.",
        "For a given confidence coefficient, its width decreases as the sample size increases.",
        r"Once a 95% interval has been computed from the data, the probability that $\mu$ lies in it is 0.95.",
        "To halve the width, the sample size must be made four times as large.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "II, III and IV only", "I, II and IV only"], "D",
   r"The width is $2z_{\alpha/2}\,\sigma/\sqrt n$: (I), (II) and (IV) follow. (III) is false in the frequentist "
   r"sense: $\mu$ is a fixed constant and the computed interval either contains it or not; 0.95 is the proportion "
   r"of such intervals, over repeated samples, that cover $\mu$.", "ci"),

 Q(r"Match the statistics in List I with their variance-stabilising (or normalising) transformations in List II."
   + match(["Poisson count $X$", r"Binomial proportion $\hat p$", "Sample correlation coefficient $r$",
            "Sample variance $s^2$ from a normal population"],
           [r"$\tanh^{-1}r$", r"$\sqrt X$", r"$\sin^{-1}\sqrt{\hat p}$", r"$\ln s^2$"]),
   ["(a)-(iii), (b)-(ii), (c)-(i), (d)-(iv)", "(a)-(ii), (b)-(iii), (c)-(iv), (d)-(i)",
    "(a)-(ii), (b)-(iii), (c)-(i), (d)-(iv)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)"], "C",
   r"If $V(T)\approx h(\theta)^2/n$, the transformation $g$ with $g'=1/h$ has variance free of $\theta$. Poisson: "
   r"$V(\sqrt X)\approx\tfrac14$. Binomial: $V(\sin^{-1}\sqrt{\hat p})\approx\tfrac1{4n}$. Correlation: Fisher's "
   r"$z=\tanh^{-1}r$ has variance $\approx\tfrac1{n-3}$. Normal variance: $V(\ln s^2)\approx\tfrac{2}{n-1}$.", "large"),

 Q(r"In a random sample of 400 voters, 80 favour a proposal. The large-sample 95% confidence interval for the "
   r"population proportion is:",
   ["(0.161, 0.239)", "(0.180, 0.220)", "(0.167, 0.233)", "(0.151, 0.249)"], "A",
   r"$\hat p=0.2$, standard error $\sqrt{\dfrac{0.2\times0.8}{400}}=0.02$. The interval is "
   r"$0.2\pm1.96(0.02)=(0.161,0.239)$. Option C uses 1.645 (a 90% interval) and option D uses 2.58 (99%).", "large"),

 Q(r"Let $F_n$ be the empirical distribution function of a random sample of size 25 from a continuous "
   r"distribution $F$. At a point $x$ where $F(x)=0.2$, the variance of $F_n(x)$ is:",
   ["0.16", "0.0064", "0.008", "0.032"], "B",
   r"$nF_n(x)$ is the number of observations not exceeding $x$, which is $\text{Bin}(n,F(x))$. So "
   r"$V[F_n(x)]=\dfrac{F(x)[1-F(x)]}{n}=\dfrac{0.2\times0.8}{25}=0.0064$. $F_n(x)$ is unbiased and consistent for "
   r"$F(x)$, uniformly in $x$ by the Glivenko&ndash;Cantelli theorem.", "order"),

 Q(r"The median $M$ of a random sample of size 3 from the uniform distribution on $(0,1)$ satisfies "
   r"$P\left(M\lt\tfrac14\right)=$",
   [r"$\dfrac1{16}$", r"$\dfrac{9}{64}$", r"$\dfrac{5}{32}$", r"$\dfrac14$"], "C",
   r"$M\lt x$ when at least two of the three observations are below $x$: "
   r"$P=3x^2(1-x)+x^3=3x^2-2x^3$. At $x=\tfrac14$: $\tfrac{3}{16}-\tfrac{2}{64}=\tfrac{10}{64}=\tfrac{5}{32}$. "
   r"($M\sim\text{Beta}(2,2)$ with density $6x(1-x)$.)", "order"),

 Q(r"Eight individuals are ranked on two characters, without ties, and the sum of squares of the differences "
   r"of ranks is $\sum d_i^2=42$. Spearman's rank correlation coefficient is:",
   ["0.25", "0.50", "0.75", "0.42"], "B",
   r"$r_s=1-\dfrac{6\sum d_i^2}{n(n^2-1)}=1-\dfrac{6\times42}{8\times63}=1-\dfrac{252}{504}=0.50$.", "rank"),

 Q(r"Five individuals have ranks $1,2,3,4,5$ on $X$ and $2,1,4,3,5$ on $Y$. Kendall's $\tau$ and Spearman's "
   r"$r_s$ are, respectively:",
   ["0.8 and 0.6", "0.6 and 0.9", "0.4 and 0.8", "0.6 and 0.8"], "D",
   r"Of the $\binom52=10$ pairs, two are discordant (individuals 1, 2 and individuals 3, 4), so "
   r"$\tau=\dfrac{8-2}{10}=0.6$. The rank differences are $-1,1,-1,1,0$, $\sum d^2=4$, and "
   r"$r_s=1-\dfrac{24}{120}=0.8$. As usual $|\tau|\lt|r_s|$.", "rank"),
]
