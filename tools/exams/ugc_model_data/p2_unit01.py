# -*- coding: utf-8 -*-
"""UGC NET Statistics, Unit I: fifty exam-standard model questions."""
from . import AR, Q, ar, match, st

TITLE = "Probability and Distributions"
BLURB = ("Events and Bayes' theorem, random variables, moments and generating functions, the standard "
         "distributions, joint distributions, sampling distributions, convergence, laws of large numbers "
         "and the central limit theorem.")

QUESTIONS = [
 Q(r"For two events $A$ and $B$, $P(A)=0.5$, $P(B)=0.6$ and $P(A\cup B)=0.8$. Consider the statements:"
   + st(r"$A$ and $B$ are independent.", r"$P(A^c\cap B^c)=0.2$.", r"$P(A\mid B^c)=0.4$.")
   + "Which of the statements are correct?",
   ["I only", "I and II only", "II and III only", "I, II and III"], "B",
   r"$P(A\cap B)=0.5+0.6-0.8=0.3=P(A)P(B)$, so $A$ and $B$ are independent: (I) is true. "
   r"$P(A^c\cap B^c)=1-P(A\cup B)=0.2$: (II) is true. Since $A$ and $B^c$ are also independent, "
   r"$P(A\mid B^c)=P(A)=0.5$, not $0.4$ (directly: $P(A\cap B^c)/P(B^c)=0.2/0.4$): (III) is false.", "prob"),

 Q(r"Four letters are placed at random into four addressed envelopes, one letter in each. The probability that "
   r"no letter goes into its own envelope is:",
   [r"$\dfrac38$", r"$\dfrac14$", r"$\dfrac13$", r"$\dfrac{5}{12}$"], "A",
   r"The number of derangements of 4 objects is $4!\left(1-\tfrac1{1!}+\tfrac1{2!}-\tfrac1{3!}+\tfrac1{4!}\right)"
   r"=24\left(\tfrac12-\tfrac16+\tfrac1{24}\right)=9$. So the probability is $9/24=3/8$. "
   r"(By inclusion and exclusion, $P(\text{at least one match})=1-\tfrac12+\tfrac16-\tfrac1{24}=\tfrac58$.)", "prob"),

 Q(r"Machines $M_1$, $M_2$ and $M_3$ make 50%, 30% and 20% of a factory's output, and 2%, 3% and 5% of their "
   r"respective outputs are defective. An item drawn at random is found defective. The probability that it was "
   r"made by $M_3$ is:",
   [r"$\dfrac{9}{29}$", r"$\dfrac25$", r"$\dfrac{10}{29}$", r"$\dfrac15$"], "C",
   r"$P(D)=0.5(0.02)+0.3(0.03)+0.2(0.05)=0.010+0.009+0.010=0.029$. By Bayes' theorem "
   r"$P(M_3\mid D)=0.010/0.029=10/29$. Note that $M_1$ has the same posterior, $10/29$, and $M_2$ has $9/29$; "
   r"$1/5$ is only the prior of $M_3$.", "cond"),

 Q(r"A fair die is rolled repeatedly until a six appears. The probability that the first six appears on an "
   r"even-numbered roll is:",
   [r"$\dfrac12$", r"$\dfrac{6}{11}$", r"$\dfrac{5}{12}$", r"$\dfrac{5}{11}$"], "D",
   r"With $p=\tfrac16$, $q=\tfrac56$: $P(\text{even})=qp+q^3p+q^5p+\cdots=\dfrac{qp}{1-q^2}=\dfrac{q}{1+q}"
   r"=\dfrac{5/6}{11/6}=\dfrac{5}{11}$. The odd-numbered rolls have the remaining $6/11$, which is larger "
   r"because the first roll is odd.", "cond"),

 Q(r"Let $\{A_n\}$ be independent events with $P(A_n)=\dfrac1n$ and let $\{B_n\}$ be any events with "
   r"$P(B_n)=\dfrac1{n^2}$. Then $P(A_n\text{ occurs infinitely often})$ and $P(B_n\text{ occurs infinitely often})$ "
   r"are, respectively:",
   ["1 and 0", "0 and 0", "1 and 1", "0 and 1"], "A",
   r"Borel&ndash;Cantelli. $\sum P(B_n)=\sum 1/n^2\lt\infty$, so $P(\limsup B_n)=0$ whatever the dependence. "
   r"$\sum P(A_n)=\sum 1/n=\infty$ and the $A_n$ are independent, so by the second lemma $P(\limsup A_n)=1$. "
   r"Independence is needed only for the second lemma.", "prob"),

 Q(r"A random variable $X$ has distribution function "
   r"$$F(x)=\begin{cases}0,& x\lt 0\\[2pt] \dfrac{x+1}{4},& 0\le x\lt 1\\[4pt] \dfrac34,& 1\le x\lt 2\\[2pt] 1,& x\ge 2.\end{cases}$$ "
   r"Then $P\left(\tfrac12\lt X\le 2\right)$ and $P(X=1)$ are, respectively:",
   [r"$\dfrac58$ and $0$", r"$\dfrac12$ and $\dfrac14$", r"$\dfrac58$ and $\dfrac14$", r"$\dfrac34$ and $\dfrac12$"], "C",
   r"$P(\tfrac12\lt X\le 2)=F(2)-F(\tfrac12)=1-\tfrac38=\tfrac58$. The jump at 1 is "
   r"$P(X=1)=F(1)-F(1^-)=\tfrac34-\tfrac24=\tfrac14$. $X$ is of mixed type: it also has jumps of $\tfrac14$ at 0 "
   r"and at 2, and a density $\tfrac14$ on $(0,1)$.", "rv"),

 Q(r"Let $X$ have density $f(x)=3x^2$, $0\lt x\lt 1$. Then $P\left(X\gt\tfrac12\ \middle|\ X\gt\tfrac14\right)$ equals:",
   [r"$\dfrac78$", r"$\dfrac89$", r"$\dfrac{63}{64}$", r"$\dfrac12$"], "B",
   r"$F(x)=x^3$, so $P(X\gt\tfrac12)=1-\tfrac18=\tfrac78$ and $P(X\gt\tfrac14)=1-\tfrac1{64}=\tfrac{63}{64}$. "
   r"The conditional probability is $\dfrac{7/8}{63/64}=\dfrac{8}{9}$. The other options are the two "
   r"unconditional probabilities.", "rv"),

 Q(r"If $X\sim N(0,4)$, then $E|X|$ equals:",
   [r"$\sqrt{\dfrac{2}{\pi}}$", r"$2$", r"$\dfrac{4}{\sqrt\pi}$", r"$2\sqrt{\dfrac{2}{\pi}}$"], "D",
   r"For $Z\sim N(0,1)$, $E|Z|=2\displaystyle\int_0^\infty z\,\phi(z)\,dz=\sqrt{2/\pi}$. Here $X=2Z$, so "
   r"$E|X|=2\sqrt{2/\pi}\approx 1.596$. In general the mean deviation about the mean of $N(\mu,\sigma^2)$ is "
   r"$\sigma\sqrt{2/\pi}\approx 0.798\,\sigma$.", "exp"),

 Q(r"A random variable $X$ takes the values $1,2,3,\dots$ and satisfies $P(X\ge k)=\dfrac1{k^2}$ for $k=1,2,\dots$ "
   r"Then $E(X)$ is:",
   [r"$\dfrac{\pi^2}{6}$", r"$2$", r"infinite", r"$\dfrac{\pi^2}{6}-1$"], "A",
   r"For a random variable taking positive integer values, $E(X)=\sum_{k\ge1}P(X\ge k)=\sum_{k\ge1}\dfrac1{k^2}"
   r"=\dfrac{\pi^2}{6}$. The mean is finite; it is $E(X^2)=\sum(2k-1)P(X\ge k)$ that diverges, so the variance "
   r"does not exist.", "exp"),

 Q(r"The number of claims $N$ in a year is Poisson with mean 4. The claim amounts $X_1,X_2,\dots$ are independent "
   r"of $N$ and of each other, each with mean 2 and variance 3. The variance of the total claim "
   r"$S=X_1+\cdots+X_N$ is:",
   ["12", "16", "28", "24"], "C",
   r"$\operatorname{Var}(S)=E(N)\operatorname{Var}(X)+\operatorname{Var}(N)[E(X)]^2=4(3)+4(4)=28$. For a Poisson "
   r"count this is $\lambda E(X^2)=4(3+4)$. The options 12 and 16 are the two parts taken separately.", "exp"),

 Q(r"The moment generating function of $X$ is $M(t)=(1-2t)^{-3}$, $t\lt\tfrac12$. Consider the statements:"
   + st(r"$X$ has the chi-square distribution with 6 degrees of freedom.", r"$\operatorname{Var}(X)=12$.",
        r"The mode of $X$ is 4.", r"$E\left(\dfrac1X\right)=\dfrac16$.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "II, III and IV only", "I, II, III and IV"], "B",
   r"$(1-2t)^{-k/2}$ is the MGF of $\chi^2_k$; here $k=6$: (I) true. $\operatorname{Var}=2k=12$: (II) true. "
   r"The mode of $\chi^2_k$ is $k-2=4$: (III) true. $E(1/X)=\dfrac1{k-2}=\dfrac14$, not $\dfrac16$ "
   r"(the reciprocal of the mean is not the mean of the reciprocal): (IV) false.", "mgf"),

 Q(r"If $X$ has moment generating function $M(t)=\left(\dfrac{2}{2-t}\right)^{3}$, $t\lt 2$, then the coefficient of "
   r"skewness $\gamma_1=\mu_3/\mu_2^{3/2}$ of $X$ is:",
   [r"$\dfrac23$", r"$\dfrac{\sqrt3}{2}$", r"$2$", r"$\dfrac{2}{\sqrt3}$"], "D",
   r"$X$ is gamma with shape $\alpha=3$ and rate 2. The cumulant generating function is $-3\ln(1-t/2)$, so "
   r"$\kappa_r=3\,(r-1)!/2^r$: $\kappa_2=\tfrac34$, $\kappa_3=\tfrac34$. Hence "
   r"$\gamma_1=\dfrac{3/4}{(3/4)^{3/2}}=\dfrac{2}{\sqrt3}$. For any gamma, $\gamma_1=2/\sqrt\alpha$ and the excess "
   r"kurtosis is $6/\alpha=2$.", "mgf"),

 Q(r"If $X$ is a Poisson variate with $P(X=1)=P(X=2)$, then $P(X=4)$ equals:",
   [r"$e^{-2}$", r"$\dfrac{4}{3e^{2}}$", r"$\dfrac{2}{3e^{2}}$", r"$\dfrac{1}{3e^{2}}$"], "C",
   r"$\lambda e^{-\lambda}=\tfrac{\lambda^2}{2}e^{-\lambda}$ gives $\lambda=2$. Then "
   r"$P(X=4)=e^{-2}\dfrac{2^4}{4!}=\dfrac{16}{24}e^{-2}=\dfrac{2}{3e^{2}}$. "
   r"($P(X=3)=\tfrac{4}{3}e^{-2}$ is option B.)", "discrete"),

 Q(r"Let $X$ be the number of independent trials needed to get the first success, the probability of success in "
   r"each trial being $\tfrac13$. Then $P(X\gt 5\mid X\gt 2)$ is:",
   [r"$\dfrac{8}{27}$", r"$\dfrac{32}{243}$", r"$\dfrac{4}{9}$", r"$\dfrac{19}{27}$"], "A",
   r"$P(X\gt k)=q^k$ with $q=\tfrac23$. By the lack-of-memory property "
   r"$P(X\gt 5\mid X\gt 2)=P(X\gt 3)=\left(\tfrac23\right)^3=\tfrac{8}{27}$. "
   r"$\tfrac{32}{243}$ is the unconditional $P(X\gt5)$ and $\tfrac{19}{27}$ is $P(X\le 3)$.", "discrete"),

 Q(r"A lot of 20 items contains 8 defectives. A sample of 5 items is drawn without replacement. The variance of "
   r"the number of defectives in the sample is:",
   [r"$\dfrac65$", r"$\dfrac{24}{19}$", r"$\dfrac{15}{19}$", r"$\dfrac{18}{19}$"], "D",
   r"Hypergeometric with $N=20$, $M=8$, $n=5$, $p=M/N=0.4$: "
   r"$\operatorname{Var}=npq\,\dfrac{N-n}{N-1}=5(0.4)(0.6)\dfrac{15}{19}=\dfrac{18}{19}$. "
   r"$\tfrac65$ is the binomial variance, which holds for sampling with replacement.", "discrete"),

 Q(r"The mode(s) of the binomial distribution with $n=9$ and $p=0.4$ is/are:",
   ["4 only", "3 and 4", "3 only", "4 and 5"], "B",
   r"$(n+1)p=10(0.4)=4$ is an integer, so the distribution is bimodal with modes $(n+1)p-1=3$ and $(n+1)p=4$. "
   r"Check: $\dfrac{P(X=4)}{P(X=3)}=\dfrac{n-3}{4}\cdot\dfrac pq=\dfrac64\cdot\dfrac23=1$.", "discrete"),

 Q(r"$X$ and $Y$ are independent Poisson variates with means 2 and 3. The conditional variance of $X$ given "
   r"$X+Y=5$ is:",
   [r"$2$", r"$\dfrac54$", r"$\dfrac65$", r"$1$"], "C",
   r"Given $X+Y=n$, $X$ is binomial with index $n$ and $p=\dfrac{\lambda}{\lambda+\mu}=\dfrac25$. With $n=5$: "
   r"$E(X\mid X+Y=5)=2$ and $\operatorname{Var}(X\mid X+Y=5)=5\cdot\tfrac25\cdot\tfrac35=\tfrac65$. "
   r"Option A is the unconditional variance of $X$.", "discrete"),

 Q(r"The lifetimes of three components are independent exponential variates, each with mean 6 hours. The "
   r"expected time until all three have failed is:",
   ["2 hours", "6 hours", "9 hours", "11 hours"], "D",
   r"With rate $\lambda=\tfrac16$ each, the waiting times between successive failures are exponential with "
   r"rates $3\lambda,2\lambda,\lambda$, so $E(X_{(3)})=\dfrac1\lambda\left(\tfrac13+\tfrac12+1\right)=6\cdot\tfrac{11}{6}=11$. "
   r"2 hours is the expected time to the first failure.", "cont"),

 Q(r"For a normal distribution, the ratio quartile deviation : mean deviation about the mean : standard "
   r"deviation is approximately:",
   ["10 : 12 : 15", "12 : 10 : 15", "2 : 3 : 4", "10 : 15 : 12"], "A",
   r"$\text{Q.D.}=0.6745\,\sigma\approx\tfrac23\sigma$ and $\text{M.D.}=\sigma\sqrt{2/\pi}=0.7979\,\sigma\approx\tfrac45\sigma$. "
   r"So $\text{Q.D.}:\text{M.D.}:\text{S.D.}=\tfrac23:\tfrac45:1=10:12:15$.", "cont"),

 Q(r"Let $X_1$ and $X_2$ be independent standard Cauchy variates. Consider the statements:"
   + st(r"$E(X_1)$ does not exist.", r"$\dfrac{X_1+X_2}{2}$ is a standard Cauchy variate.",
        r"$\dfrac1{X_1}$ is a standard Cauchy variate.", r"$X_1^2$ has the $F$ distribution with $(1,1)$ degrees of freedom.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "II, III and IV only", "I, II, III and IV"], "D",
   r"(I) $\int|x|\,\dfrac{dx}{\pi(1+x^2)}$ diverges. (II) The characteristic function is $e^{-|t|}$, and "
   r"$\left(e^{-|t|/2}\right)^2=e^{-|t|}$. (III) A standard Cauchy is the ratio of two independent $N(0,1)$ "
   r"variates, and the reciprocal of such a ratio is again one. (IV) Standard Cauchy is $t_1$, and "
   r"$t_n^2\sim F(1,n)$. All four are true.", "cont"),

 Q(r"$X$ and $Y$ are independent gamma variates with unit scale and shape parameters 2 and 3. The variance of "
   r"$U=\dfrac{X}{X+Y}$ is:",
   [r"$\dfrac25$", r"$\dfrac1{25}$", r"$\dfrac{6}{25}$", r"$\dfrac15$"], "B",
   r"$U\sim\text{Beta}(2,3)$ (first kind), independently of $X+Y$. "
   r"$\operatorname{Var}(U)=\dfrac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}=\dfrac{6}{25\cdot 6}=\dfrac1{25}$. "
   r"$\tfrac25$ is its mean.", "cont"),

 Q(r"Let $\ln X\sim N(0,1)$. Match the characteristics of $X$ in List I with their values in List II."
   + match(["Mean", "Median", "Mode", "Variance"], [r"$1$", r"$e^{-1}$", r"$e^{1/2}$", r"$e(e-1)$"]),
   ["(a)-(i), (b)-(iii), (c)-(ii), (d)-(iv)", "(a)-(iii), (b)-(ii), (c)-(i), (d)-(iv)",
    "(a)-(iii), (b)-(i), (c)-(ii), (d)-(iv)", "(a)-(iv), (b)-(i), (c)-(ii), (d)-(iii)"], "C",
   r"For the lognormal with parameters $\mu,\sigma^2$: mean $e^{\mu+\sigma^2/2}=e^{1/2}$; median $e^{\mu}=1$; "
   r"mode $e^{\mu-\sigma^2}=e^{-1}$; variance $e^{2\mu+\sigma^2}(e^{\sigma^2}-1)=e(e-1)$. "
   r"Mode $\lt$ median $\lt$ mean, as for any positively skewed distribution of this kind.", "cont"),

 Q(r"The lifetime $T$ of a device has hazard rate $h(t)=2t$, $t\gt 0$. Then $E(T)$ is:",
   [r"$\dfrac{\sqrt\pi}{2}$", r"$\dfrac12$", r"$\sqrt\pi$", r"$1$"], "A",
   r"$S(t)=\exp\left(-\int_0^t 2u\,du\right)=e^{-t^2}$, a Weibull survival function with shape 2. "
   r"$E(T)=\displaystyle\int_0^\infty S(t)\,dt=\int_0^\infty e^{-t^2}dt=\dfrac{\sqrt\pi}{2}$.", "cont"),

 Q(r"$(X,Y)$ has joint density $f(x,y)=2$ for $0\lt x\lt y\lt 1$ and 0 elsewhere. The correlation coefficient "
   r"between $X$ and $Y$ is:",
   [r"$\dfrac13$", r"$\dfrac12$", r"$\dfrac14$", r"$\dfrac1{\sqrt2}$"], "B",
   r"$f_X(x)=2(1-x)$, $f_Y(y)=2y$: $E(X)=\tfrac13$, $E(Y)=\tfrac23$, "
   r"$\operatorname{Var}(X)=\operatorname{Var}(Y)=\tfrac1{18}$. "
   r"$E(XY)=\displaystyle\int_0^1\!\!\int_0^y 2xy\,dx\,dy=\int_0^1 y^3dy=\tfrac14$, so "
   r"$\operatorname{Cov}=\tfrac14-\tfrac29=\tfrac1{36}$ and $\rho=\dfrac{1/36}{1/18}=\dfrac12$.", "joint"),

 Q(r"$(X,Y)$ is bivariate normal with $E(X)=E(Y)=0$, $\operatorname{Var}(X)=1$, $\operatorname{Var}(Y)=4$ and "
   r"correlation $\rho=0.5$. Then $E(Y\mid X=1)$ and $\operatorname{Var}(Y\mid X=1)$ are, respectively:",
   [r"$\dfrac14$ and $3$", r"$1$ and $4$", r"$2$ and $3$", r"$1$ and $3$"], "D",
   r"$E(Y\mid X=x)=\mu_Y+\rho\dfrac{\sigma_Y}{\sigma_X}(x-\mu_X)=0.5\cdot\dfrac21\cdot 1=1$. "
   r"$\operatorname{Var}(Y\mid X=x)=\sigma_Y^2(1-\rho^2)=4(0.75)=3$, which does not depend on $x$.", "joint"),

 Q(r"$(X,Y)$ has joint density $f(x,y)=e^{-y}$ for $0\lt x\lt y\lt\infty$ and 0 elsewhere. Then $P(Y\gt 2X)$ is:",
   [r"$\dfrac13$", r"$\dfrac14$", r"$\dfrac12$", r"$\dfrac23$"], "C",
   r"$P(Y\gt 2X)=\displaystyle\int_0^\infty\!\!\int_{2x}^\infty e^{-y}\,dy\,dx=\int_0^\infty e^{-2x}dx=\dfrac12$. "
   r"Another way: given $Y=y$, $X$ is uniform on $(0,y)$, so $P(X\lt y/2\mid Y=y)=\tfrac12$ for every $y$.", "joint"),

 Q(r"If $\operatorname{Var}(X)=4$, $\operatorname{Var}(Y)=9$ and the correlation between $X$ and $Y$ is $-0.5$, then "
   r"$\operatorname{Var}(2X-Y)$ is:",
   ["37", "13", "19", "25"], "A",
   r"$\operatorname{Cov}(X,Y)=-0.5(2)(3)=-3$. "
   r"$\operatorname{Var}(2X-Y)=4(4)+9-2(2)(-3)=16+9+12=37$. Taking the covariance term with the wrong sign gives "
   r"13; ignoring it gives 25.", "joint"),

 Q(r"$(X_1,X_2,X_3)$ is multinomial with $n=12$ and cell probabilities $\left(\tfrac12,\tfrac13,\tfrac16\right)$. "
   r"The correlation coefficient between $X_1$ and $X_2$ is:",
   [r"$-\dfrac12$", r"$-\dfrac1{\sqrt2}$", r"$-\dfrac13$", r"$-2$"], "B",
   r"$\operatorname{Cov}(X_1,X_2)=-np_1p_2=-2$, $\operatorname{Var}(X_1)=np_1(1-p_1)=3$, "
   r"$\operatorname{Var}(X_2)=np_2(1-p_2)=\tfrac83$. So "
   r"$\rho=\dfrac{-2}{\sqrt{3\cdot 8/3}}=-\dfrac{2}{\sqrt8}=-\dfrac1{\sqrt2}$; in general "
   r"$\rho=-\sqrt{\dfrac{p_1p_2}{(1-p_1)(1-p_2)}}$, free of $n$. $-2$ is the covariance.", "joint"),

 Q(r"A random variable $X$ has mean 10 and variance 4; nothing else is known about its distribution. "
   r"Chebyshev's inequality gives, for $P(4\lt X\lt 16)$, the lower bound:",
   [r"$\dfrac34$", r"$\dfrac59$", r"$\dfrac19$", r"$\dfrac89$"], "D",
   r"$P(|X-10|\lt 6)\ge 1-\dfrac{\sigma^2}{6^2}=1-\dfrac4{36}=\dfrac89$. Here $6=3\sigma$, so this is the "
   r"familiar $1-1/k^2$ with $k=3$; $\tfrac19$ is the upper bound for the complementary event.", "cheb"),

 Q(ar(r"If $X$ has mean 50 and variance 25, then $P(40\lt X\lt 60)\ge 0.75$.",
      r"Chebyshev's inequality holds only for distributions that are symmetric about the mean."),
   AR, "C",
   r"(A) is true: $P(|X-50|\lt 10)\ge 1-\tfrac{25}{100}=0.75$. (R) is false: Chebyshev's inequality needs only a "
   r"finite variance; no symmetry or any other shape is assumed, which is exactly why its bound is often crude.", "cheb"),

 Q(r"Let $S^2=\dfrac1{n-1}\sum_{i=1}^{n}(X_i-\bar X)^2$ for a random sample of size $n=10$ from $N(\mu,\sigma^2)$ "
   r"with $\sigma^2=3$. Then $\operatorname{Var}(S^2)$ is:",
   ["2", "1.8", "6", "0.9"], "A",
   r"$(n-1)S^2/\sigma^2\sim\chi^2_{n-1}$, whose variance is $2(n-1)$. So "
   r"$\operatorname{Var}(S^2)=\dfrac{2\sigma^4}{n-1}=\dfrac{2(9)}{9}=2$. Dividing by $n$ in place of $n-1$ gives 1.8.", "sample"),

 Q(r"Consider the statements:"
   + st(r"If $T\sim t_n$, then $T^2\sim F(1,n)$.", r"If $X\sim F(m,n)$, then $\dfrac1X\sim F(n,m)$.",
        r"The upper 5% point of $F(m,n)$ is the reciprocal of the upper 5% point of $F(n,m)$.",
        r"The mean of $F(m,n)$ is $\dfrac{n}{n-2}$ for $n\gt 2$.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and IV only", "I, III and IV only", "I, II, III and IV"], "B",
   r"(I), (II) and (IV) are standard results; note the mean of $F$ does not involve $m$. (III) is false: from (II), "
   r"$F_{\alpha}(m,n)=\dfrac{1}{F_{1-\alpha}(n,m)}$, so the upper 5% point of $F(m,n)$ is the reciprocal of the "
   r"<em>lower</em> 5% point of $F(n,m)$.", "sample"),

 Q(r"A random sample of size 5 is drawn from the uniform distribution on $(0,1)$. The expected value of the "
   r"sample range is:",
   [r"$\dfrac13$", r"$\dfrac12$", r"$\dfrac23$", r"$\dfrac56$"], "C",
   r"$E(X_{(n)})=\dfrac{n}{n+1}$ and $E(X_{(1)})=\dfrac{1}{n+1}$, so $E(R)=\dfrac{n-1}{n+1}=\dfrac46=\dfrac23$. "
   r"(The range itself is $\text{Beta}(n-1,2)$, whose mean is $\tfrac{n-1}{n+1}$.) $\tfrac56$ is $E(X_{(5)})$.", "sample"),

 Q(r"Let $X_1,X_2,X_3,X_4$ be independent $N(0,1)$ variates. The distribution of "
   r"$\dfrac{X_1-X_2}{\sqrt{X_3^2+X_4^2}}$ is:",
   [r"$N(0,1)$", r"$t$ with 1 degree of freedom", r"$F(1,2)$", r"$t$ with 2 degrees of freedom"], "D",
   r"$Z=\dfrac{X_1-X_2}{\sqrt2}\sim N(0,1)$ and $V=X_3^2+X_4^2\sim\chi^2_2$, independent. "
   r"$\dfrac{Z}{\sqrt{V/2}}=\dfrac{X_1-X_2}{\sqrt{X_3^2+X_4^2}}\sim t_2$. Its square, not the ratio itself, is $F(1,2)$.", "sample"),

 Q(r"$X_1,\dots,X_5$ is a random sample from the exponential distribution with mean $\theta$. The distribution of "
   r"$\dfrac{2}{\theta}\sum_{i=1}^{5}X_i$ is:",
   [r"$\chi^2_5$", r"$\chi^2_{10}$", r"$\chi^2_{20}$", "exponential with mean 2"], "B",
   r"$2X_i/\theta$ is exponential with mean 2, which is $\chi^2_2$. The sum of 5 independent $\chi^2_2$ variates is "
   r"$\chi^2_{10}$. This pivot gives exact confidence intervals for $\theta$.", "sample"),

 Q(r"If $X$ is uniform on $(0,1)$, the distribution of $Y=-2\ln X$ is:",
   [r"$\chi^2$ with 2 degrees of freedom", r"$\chi^2$ with 1 degree of freedom",
    r"exponential with mean $\tfrac12$", r"uniform on $(0,2)$"], "A",
   r"$P(Y\gt y)=P(X\lt e^{-y/2})=e^{-y/2}$, $y\gt 0$: exponential with mean 2, which is the $\chi^2_2$ distribution. "
   r"This is the basis of Fisher's method of combining independent $p$-values.", "trans"),

 Q(r"Let $X$ and $Y$ be independent $N(0,1)$ variates. Match the statistics in List I with their distributions "
   r"in List II."
   + match([r"$X/Y$", r"$X^2+Y^2$", r"$\dfrac{X^2}{X^2+Y^2}$", r"$\dfrac{X+Y}{\sqrt2}$"],
           [r"$N(0,1)$", r"$\text{Beta}\left(\tfrac12,\tfrac12\right)$", "standard Cauchy", "exponential with mean 2"]),
   ["(a)-(iii), (b)-(ii), (c)-(iv), (d)-(i)", "(a)-(i), (b)-(iv), (c)-(ii), (d)-(iii)",
    "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)"], "C",
   r"The ratio of two independent standard normals is standard Cauchy. $X^2+Y^2\sim\chi^2_2$, exponential with "
   r"mean 2. $X^2$ and $Y^2$ are independent $\text{Gamma}(\tfrac12)$ variates (scale 2), so "
   r"$X^2/(X^2+Y^2)\sim\text{Beta}(\tfrac12,\tfrac12)$. A linear combination of normals with variance "
   r"$\tfrac12+\tfrac12=1$ is $N(0,1)$.", "trans"),

 Q(r"If $X$ and $Y$ are independent and each is uniform on $(0,1)$, then $P\left(XY\le\tfrac12\right)$ is:",
   [r"$\dfrac12$", r"$\ln 2$", r"$\dfrac34$", r"$\dfrac{1+\ln 2}{2}$"], "D",
   r"If $x\le\tfrac12$ the event holds for every $y$; if $x\gt\tfrac12$ it needs $y\le\dfrac1{2x}$. So "
   r"$P=\dfrac12+\displaystyle\int_{1/2}^{1}\dfrac{dx}{2x}=\dfrac12+\dfrac12\ln 2\approx 0.847$.", "trans"),

 Q(ar(r"If $X$ has a continuous distribution function $F$, then $F(X)$ is uniformly distributed on $(0,1)$.",
      r"For every random variable $X$ with distribution function $F$, $P\{F(X)\le u\}=u$ for all $u\in(0,1)$."),
   AR, "C",
   r"(A) is the probability integral transformation and is true. (R) is false: if $F$ has jumps, $F(X)$ cannot "
   r"take values inside a jump. For a fair coin ($X=0,1$), $F(X)$ takes only the values $\tfrac12$ and 1, so "
   r"$P\{F(X)\le 0.3\}=0\ne 0.3$. In general only $P\{F(X)\le u\}\le u$ holds.", "trans"),

 Q(r"Which of the following functions is NOT the characteristic function of any random variable?",
   [r"$\cos t$", r"$e^{-|t|}$", r"$\dfrac{1}{1+t^2}$", r"$e^{-t^4}$"], "D",
   r"$\cos t$: $X=\pm1$ with probability $\tfrac12$ each. $e^{-|t|}$: standard Cauchy. $1/(1+t^2)$: Laplace (double "
   r"exponential). If $\phi(t)=e^{-t^4}$ were a characteristic function, $\phi''(0)=0$ would give $E(X^2)=0$, so "
   r"$X=0$ almost surely and $\phi\equiv 1$, a contradiction.", "cf"),

 Q(r"The characteristic function of $X$ is $\phi(t)=\dfrac{\sin t}{t}$ for $t\ne 0$, with $\phi(0)=1$. Then "
   r"$\operatorname{Var}(X)$ is:",
   [r"$1$", r"$\dfrac13$", r"$\dfrac1{12}$", r"$\dfrac12$"], "B",
   r"$\dfrac{\sin t}{t}=\dfrac{e^{it}-e^{-it}}{2it}$ is the characteristic function of the uniform distribution "
   r"on $(-1,1)$, whose variance is $\dfrac{(b-a)^2}{12}=\dfrac4{12}=\dfrac13$. Or expand: "
   r"$\phi(t)=1-\dfrac{t^2}{6}+\cdots$, so $E(X^2)=\tfrac13$ and $E(X)=0$.", "cf"),

 Q(r"Let $\phi$ be the characteristic function of a random variable $X$. Consider the statements:"
   + st(r"$|\phi(t)|\le 1$ for all real $t$.", r"$\phi$ is uniformly continuous on the real line.",
        r"$\phi$ is real-valued if and only if $X$ is symmetric about 0.",
        r"If $\phi_{X+Y}(t)=\phi_X(t)\,\phi_Y(t)$ for all $t$, then $X$ and $Y$ are independent.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and II only", "I, III and IV only", "I, II, III and IV"], "A",
   r"(I), (II) and (III) are standard properties. (IV) is false: independence implies the product rule, but not "
   r"conversely. If $X$ is standard Cauchy and $Y=X$, then $\phi_{X+Y}(t)=\phi_X(2t)=e^{-2|t|}=\phi_X(t)\phi_Y(t)$, "
   r"although $X$ and $Y$ are completely dependent.", "cf"),

 Q(r"$X_1$ and $X_2$ are independent, each with characteristic function $e^{-|t|}$. The characteristic function of "
   r"$2X_1-X_2$ is:",
   [r"$e^{-|t|}$", r"$e^{-2|t|}$", r"$e^{-3|t|}$", r"$e^{-5|t|}$"], "C",
   r"$\phi_{2X_1-X_2}(t)=\phi(2t)\,\phi(-t)=e^{-2|t|}e^{-|t|}=e^{-3|t|}$: Cauchy with scale 3. Scales of Cauchy "
   r"variates add in absolute value ($|2|+|-1|=3$); variances do not exist, so the &lsquo;$4+1=5$&rsquo; rule "
   r"does not apply.", "cf"),

 Q(r"Let $X_1,X_2,\dots$ be independent with $P(X_n=n)=\dfrac1n$ and $P(X_n=0)=1-\dfrac1n$. Consider the statements:"
   + st(r"$X_n\to 0$ in probability.", r"$X_n\to 0$ in mean (in $L^1$).", r"$X_n\to 0$ almost surely.",
        r"$X_n\to 0$ in distribution.")
   + "Which of the statements are correct?",
   ["I only", "I and IV only", "I, II and IV only", "I, III and IV only"], "B",
   r"$P(|X_n|\gt\varepsilon)=\tfrac1n\to0$: (I) true, hence (IV) true. $E|X_n|=1$ for every $n$: (II) false. "
   r"$\sum P(X_n=n)=\infty$ and the $X_n$ are independent, so by the second Borel&ndash;Cantelli lemma $X_n=n$ "
   r"infinitely often with probability 1: (III) false.", "conv"),

 Q(r"Consider the statements about a sequence of random variables $\{X_n\}$:"
   + st(r"Almost sure convergence implies convergence in probability.",
        r"Convergence in probability implies almost sure convergence.",
        r"Convergence in distribution to a constant implies convergence in probability to that constant.",
        r"Convergence in $r$-th mean implies almost sure convergence.")
   + "Which of the statements are correct?",
   ["I and III only", "I and II only", "I, III and IV only", "II and IV only"], "A",
   r"(I) and (III) are true. (II) is false in general (only a subsequence converges almost surely). (IV) is false: "
   r"convergence in $r$-th mean gives convergence in probability by Markov's inequality, not almost sure "
   r"convergence; the &lsquo;sliding hump&rsquo; indicators on $(0,1)$ converge in mean but at no point.", "conv"),

 Q(r"Let $\bar X_n$ be the mean of a random sample of size $n$ from the Poisson distribution with mean 4. "
   r"The limiting distribution of $\sqrt n\left(\sqrt{\bar X_n}-2\right)$ is normal with mean 0 and variance:",
   ["4", "1", r"$\dfrac1{16}$", r"$\dfrac14$"], "D",
   r"By the central limit theorem $\sqrt n(\bar X_n-4)\to N(0,4)$. By the delta method with $g(x)=\sqrt x$, "
   r"$g'(4)=\tfrac14$, the variance is $4\cdot\tfrac1{16}=\tfrac14$. The square root is the variance-stabilising "
   r"transformation for the Poisson: the limit variance is $\tfrac14$ whatever the mean.", "conv"),

 Q(r"Let $X_1,X_2,\dots$ be independent with $P(X_k=k^{\alpha})=P(X_k=-k^{\alpha})=\tfrac12$, $\alpha\gt0$, and "
   r"$S_n=X_1+\cdots+X_n$. Chebyshev's sufficient condition for the weak law of large numbers, "
   r"$\operatorname{Var}(S_n)/n^2\to 0$, is satisfied precisely when:",
   [r"$\alpha\lt 1$", r"$\alpha\lt\dfrac12$", r"$\alpha\le 1$", r"every $\alpha\gt 0$"], "B",
   r"$\operatorname{Var}(X_k)=k^{2\alpha}$, so $\operatorname{Var}(S_n)=\sum_{k=1}^{n}k^{2\alpha}\sim\dfrac{n^{2\alpha+1}}{2\alpha+1}$ "
   r"and $\operatorname{Var}(S_n)/n^2\sim\dfrac{n^{2\alpha-1}}{2\alpha+1}$, which tends to 0 if and only if $\alpha\lt\tfrac12$.", "lln"),

 Q(r"Let $X_1,X_2,\dots$ be independent, each with density $f(x)=\dfrac{2}{x^3}$, $x\gt 1$. As $n\to\infty$, the "
   r"sample mean $\bar X_n$:",
   ["converges almost surely to 2", "does not converge, because the variance is infinite",
    "converges almost surely to 1", r"converges almost surely to $\tfrac32$"], "A",
   r"$E(X)=\displaystyle\int_1^\infty\dfrac{2}{x^2}dx=2$ is finite, and Kolmogorov's strong law for independent, "
   r"identically distributed variables needs only a finite mean. $E(X^2)=\int_1^\infty\tfrac2x\,dx$ diverges, "
   r"but an infinite variance does not prevent the law of large numbers; it is the usual central limit theorem "
   r"that fails here.", "lln"),

 Q(r"$X_1,\dots,X_{48}$ are independent, each uniform on $(0,1)$. Using the central limit theorem, "
   r"$P\left(\sum_{i=1}^{48}X_i\gt 26\right)$ is approximately (given $\Phi(1)=0.8413$, $\Phi(2)=0.9772$):",
   ["0.0228", "0.3085", "0.1587", "0.0668"], "C",
   r"$E(\sum X_i)=48\cdot\tfrac12=24$ and $\operatorname{Var}(\sum X_i)=48\cdot\tfrac1{12}=4$. "
   r"$P(\sum X_i\gt 26)\approx P\left(Z\gt\dfrac{26-24}{2}\right)=1-\Phi(1)=0.1587$.", "clt"),

 Q(r"$\displaystyle\lim_{n\to\infty}e^{-n}\sum_{k=0}^{n}\dfrac{n^k}{k!}$ equals:",
   ["0", "1", r"$\dfrac1e$", r"$\dfrac12$"], "D",
   r"The expression is $P(S_n\le n)$, where $S_n$ is Poisson with mean $n$, the sum of $n$ independent Poisson(1) "
   r"variates. By the central limit theorem "
   r"$P(S_n\le n)=P\left(\dfrac{S_n-n}{\sqrt n}\le 0\right)\to\Phi(0)=\dfrac12$.", "clt"),
]
