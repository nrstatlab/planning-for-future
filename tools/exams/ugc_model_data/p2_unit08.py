# -*- coding: utf-8 -*-
"""UGC NET Statistics, Unit VIII: fifty exam-standard model questions."""
from . import AR, Q, ar, st

TITLE = "Multivariate Analysis"
BLURB = ("The multivariate normal distribution, estimation of the mean vector and covariance matrix, the "
         "Wishart distribution, partial and multiple correlation, Hotelling's $T^2$, discriminant analysis, "
         "principal components and canonical correlations.")

M = lambda rows: r"\begin{pmatrix}" + r"\\".join("&".join(str(x) for x in r) for r in rows) + r"\end{pmatrix}"
S2 = M([[5, 2], [2, 2]])

QUESTIONS = [
 Q(r"Let $X=(X_1,X_2,X_3)'\sim N_3(\mu,\Sigma)$ with $\Sigma=" + M([[4, 2, 0], [2, 9, 0], [0, 0, 1]]) + r"$. Which "
   r"statement is correct?",
   ["$X_1$ and $X_2$ are independent", "$X_3$ is independent of $(X_1,X_2)$",
    "$X_1,X_2,X_3$ are mutually independent", "$X_1+X_3$ and $X_1$ are independent"], "B",
   r"In a multivariate normal distribution, sub-vectors are independent if and only if their covariance matrix "
   r"is zero. $\operatorname{Cov}(X_3,X_1)=\operatorname{Cov}(X_3,X_2)=0$, so $X_3$ is independent of $(X_1,X_2)$. "
   r"$\operatorname{Cov}(X_1,X_2)=2\ne0$, and $\operatorname{Cov}(X_1+X_3,X_1)=4\ne0$.", "mvn"),

 Q(r"$(X_1,X_2)'$ is bivariate normal with mean $(1,2)'$ and covariance matrix $" + M([[4, 2], [2, 9]]) + r"$. "
   r"The conditional mean and variance of $X_1$ given $X_2=5$ are approximately:",
   ["2.50 and 3.00", "1.67 and 4.00", "2.50 and 3.56", "1.67 and 3.56"], "D",
   r"$E(X_1\mid X_2=x_2)=\mu_1+\dfrac{\sigma_{12}}{\sigma_{22}}(x_2-\mu_2)=1+\dfrac29(3)=1.67$. "
   r"$V(X_1\mid X_2)=\sigma_{11}-\dfrac{\sigma_{12}^2}{\sigma_{22}}=4-\dfrac49=3.56$, the same for every $x_2$.", "mvn"),

 Q(r"If $X\sim N_2\left(" + M([[1], [2]]) + "," + M([[2, 1], [1, 3]]) + r"\right)$, the distribution of $X_1-X_2$ is:",
   [r"$N(-1,3)$", r"$N(-1,5)$", r"$N(-1,7)$", r"$N(3,3)$"], "A",
   r"With $a=(1,-1)'$: $a'\mu=1-2=-1$ and $a'\Sigma a=2+3-2(1)=3$. Every linear combination of a multivariate "
   r"normal vector is univariate normal. Ignoring the covariance gives 5; adding it gives 7.", "mvn"),

 Q(r"If $X\sim N_3(\mu,\Sigma)$ with $\Sigma$ positive definite, the mean and variance of "
   r"$Q=(X-\mu)'\Sigma^{-1}(X-\mu)$ are:",
   ["3 and 3", "1 and 2", "3 and 6", "3 and 9"], "C",
   r"$Z=\Sigma^{-1/2}(X-\mu)\sim N_3(0,I)$ and $Q=Z'Z\sim\chi^2_3$, with mean $p=3$ and variance $2p=6$. This is "
   r"why contours of constant density are ellipsoids and $P(Q\le\chi^2_{p,\alpha})=1-\alpha$.", "mvn"),

 Q(r"$(X_1,X_2)'$ is bivariate normal with unit variances and correlation $\rho$. Then $X_1+X_2$ and "
   r"$X_1-X_2$ are independent:",
   ["only when $\\rho=0$", "for every value of $\\rho$", "only when $\\rho\\gt0$", "for no value of $\\rho$"], "B",
   r"$\operatorname{Cov}(X_1+X_2,X_1-X_2)=V(X_1)-V(X_2)=1-1=0$ whatever $\rho$ is. The two are jointly normal "
   r"(linear functions of a normal vector), so zero covariance implies independence. Equal variances are what "
   r"matter, not $\rho$.", "mvn"),

 Q(r"Consider the statements about a random vector $X$:"
   + st("If $X$ is multivariate normal, every marginal distribution is normal.",
        "If every component of $X$ is normal, then $X$ is multivariate normal.",
        "If $X$ is multivariate normal, components with zero covariance are independent.",
        r"$X$ is multivariate normal if and only if every linear combination $a'X$ is univariate normal.")
   + "Which of the statements are correct?",
   ["I, III and IV only", "I and III only", "I, II and III only", "I, II, III and IV"], "A",
   r"(I), (III) and (IV) are standard; (IV) is often taken as the definition. (II) is false: take $X_1\sim N(0,1)$ "
   r"and $X_2=SX_1$, where $S=\pm1$ with probability $\tfrac12$ independently. Both are $N(0,1)$, but $X_1+X_2$ "
   r"equals 0 with probability $\tfrac12$, so the pair is not bivariate normal.", "mvn"),

 Q(r"For the bivariate normal density with covariance matrix $" + M([[2, 1], [1, 2]]) + r"$, the constant "
   r"multiplying the exponential term is:",
   [r"$\dfrac{1}{2\pi}$", r"$\dfrac{1}{6\pi}$", r"$\dfrac{1}{4\pi}$", r"$\dfrac{1}{2\pi\sqrt3}$"], "D",
   r"The constant is $(2\pi)^{-p/2}|\Sigma|^{-1/2}$ with $p=2$ and $|\Sigma|=4-1=3$: $\dfrac{1}{2\pi\sqrt3}$. "
   r"$|\Sigma|$ is the generalised variance.", "mvn"),

 Q(r"For $\mu=(0,0)'$ and $\Sigma=" + M([[1, 0.5], [0.5, 1]]) + r"$, the squared Mahalanobis distance of the "
   r"point $x=(1,1)'$ from $\mu$ is:",
   ["2.00", "1.00", "1.33", "4.00"], "C",
   r"$\Sigma^{-1}=\dfrac{1}{0.75}" + M([[1, -0.5], [-0.5, 1]]) + r"$, so "
   r"$x'\Sigma^{-1}x=\dfrac{1-0.5-0.5+1}{0.75}=1.33$. It is less than the squared Euclidean distance 2 because "
   r"the point lies along the direction in which the positively correlated variables vary together.", "mvn"),

 Q(r"For a random sample of size $n=10$ from $N_p(\mu,\Sigma)$ with $S=\dfrac{1}{n-1}\sum(X_i-\bar X)(X_i-\bar X)'$, "
   r"the maximum likelihood estimator of $\Sigma$ is:",
   ["$S$", "$0.9\\,S$", "$1.1\\,S$", "$0.81\\,S$"], "B",
   r"$\hat\Sigma=\dfrac1n\sum(X_i-\bar X)(X_i-\bar X)'=\dfrac{n-1}{n}S=0.9S$. It is biased; $S$ is the unbiased "
   r"estimator.", "est"),

 Q(r"For a random sample of size $n$ from $N_p(\mu,\Sigma)$, consider the statements:"
   + st(r"$\bar X\sim N_p\left(\mu,\tfrac1n\Sigma\right)$.", r"$\bar X$ and $S$ are independent.",
        r"$(n-1)S\sim W_p(n-1,\Sigma)$.", r"$S$ is positive definite with probability 1 if and only if $n\gt p$.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "I, III and IV only", "I, II, III and IV"], "D",
   r"(I)&ndash;(III) are the multivariate analogue of the independence of $\bar X$ and $s^2$ in normal samples. "
   r"(IV) $(n-1)S$ is a sum of $n-1$ independent rank-one matrices, so it has full rank $p$ (with probability 1) "
   r"exactly when $n-1\ge p$. All four are true.", "est"),

 Q(r"For a random sample from $N_p(\mu,\Sigma)$ with both parameters unknown, a sufficient statistic is:",
   [r"$(\bar X,S)$", r"$\bar X$ alone", r"$S$ alone", r"$(\bar X,|S|)$"], "A",
   r"The likelihood depends on the data only through $\bar X$ and $\sum(X_i-\bar X)(X_i-\bar X)'=(n-1)S$, so by "
   r"the factorisation theorem $(\bar X,S)$ is sufficient; it is also complete.", "est"),

 Q(r"For a random sample of size $n=5$ from $N_2(\mu,\Sigma)$, the maximum likelihood estimate of the "
   r"generalised variance $|\Sigma|$, in terms of the sample covariance matrix $S$ (divisor $n-1$), is:",
   ["$|S|$", "$0.8\\,|S|$", "$0.64\\,|S|$", "$1.25\\,|S|$"], "C",
   r"By invariance, the estimate is $|\hat\Sigma|=\left|\dfrac{n-1}{n}S\right|=\left(\dfrac{n-1}{n}\right)^p|S|"
   r"=(0.8)^2|S|=0.64|S|$. A scalar multiplying a $p\times p$ matrix comes out of the determinant to the power "
   r"$p$.", "est"),

 Q(r"Three observations on $(X_1,X_2)$ are $(1,2)$, $(3,4)$ and $(5,9)$. The sample covariance $s_{12}$ "
   r"(divisor $n-1$) and the sample correlation coefficient are:",
   ["4.67 and 0.971", "7 and 0.971", "7 and 0.538", "14 and 0.971"], "B",
   r"The means are 3 and 5; the deviations are $(-2,0,2)$ and $(-3,-1,4)$. $s_{12}=\dfrac{6+0+8}{2}=7$, "
   r"$s_{11}=\dfrac82=4$, $s_{22}=\dfrac{26}{2}=13$, and $r=\dfrac{7}{\sqrt{52}}=0.971$. The correlation does not "
   r"depend on the divisor.", "est"),

 Q(r"$\bar X$ is the mean of a random sample of size 25 from $N_2(\mu,\Sigma)$ with $\Sigma$ known. The "
   r"distribution of $25(\bar X-\mu)'\Sigma^{-1}(\bar X-\mu)$ is:",
   [r"$\chi^2_{25}$", r"$F(2,23)$", r"$\chi^2_{24}$", r"$\chi^2_{2}$"], "D",
   r"$\sqrt n(\bar X-\mu)\sim N_p(0,\Sigma)$, so the quadratic form is $\chi^2_p=\chi^2_2$ whatever $n$ is. It "
   r"gives an elliptical confidence region for $\mu$. When $\Sigma$ is replaced by $S$, the statistic becomes "
   r"Hotelling's $T^2$, related to $F(2,23)$.", "sample"),

 Q(ar(r"For a large random sample from any $p$-variate population with finite covariance matrix, "
      r"$n(\bar X-\mu)'S^{-1}(\bar X-\mu)$ is approximately $\chi^2_p$.",
      r"By the multivariate central limit theorem $\sqrt n(\bar X-\mu)$ is approximately $N_p(0,\Sigma)$, and $S$ "
      r"converges in probability to $\Sigma$."),
   AR, "A",
   r"The central limit theorem makes $\sqrt n(\bar X-\mu)$ approximately normal without any assumption of "
   r"normality, and replacing $\Sigma$ by a consistent estimator does not change the limit (Slutsky). So the "
   r"quadratic form is approximately $\chi^2_p$. Both statements are true and (R) is the reason.", "sample"),

 Q(r"$\bar X$ is the mean of a sample of size 7 from a bivariate population with covariance matrix "
   r"$" + M([[2, 1], [1, 3]]) + r"$. The variance of $\bar X_1+\bar X_2$ is:",
   ["0.71", "5", "1", "7"], "C",
   r"With $a=(1,1)'$: $V(a'\bar X)=\dfrac{a'\Sigma a}{n}=\dfrac{2+3+2(1)}{7}=1$.", "sample"),

 Q(r"If $A\sim W_p(10,\Sigma)$ and $\sigma_{11}=2$, the mean and variance of the element $a_{11}$ are:",
   ["20 and 40", "20 and 80", "2 and 8", "10 and 20"], "B",
   r"$\dfrac{a_{11}}{\sigma_{11}}\sim\chi^2_{10}$, so $E(a_{11})=10(2)=20$ and "
   r"$V(a_{11})=2n\sigma_{11}^2=2(10)(4)=80$. In general $E(A)=n\Sigma$.", "wishart"),

 Q(r"Consider the statements about the Wishart distribution:"
   + st(r"If $A_1\sim W_p(n_1,\Sigma)$ and $A_2\sim W_p(n_2,\Sigma)$ are independent, then "
        r"$A_1+A_2\sim W_p(n_1+n_2,\Sigma)$.",
        r"If $A\sim W_p(n,\Sigma)$ and $C$ is a $q\times p$ matrix of rank $q$, then $CAC'\sim W_q(n,C\Sigma C')$.",
        r"If $A\sim W_p(n,\Sigma)$, then $\dfrac{a'Aa}{a'\Sigma a}\sim\chi^2_n$ for every fixed $a\ne0$.",
        r"The sum of two independent Wishart matrices with different $\Sigma$ is again Wishart.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and II only", "I and III only", "I, II, III and IV"], "A",
   r"(I) is the additive property, (II) the transformation property and (III) its special case $q=1$; they "
   r"mirror the properties of chi-square, of which the Wishart is the matrix generalisation. (IV) is false, just "
   r"as $\sigma_1^2\chi^2+\sigma_2^2\chi^2$ is not a multiple of a chi-square.", "wishart"),

 Q(r"If $A\sim W_2(5,\Sigma)$, then $E|A|$ equals:",
   [r"$5|\Sigma|$", r"$25|\Sigma|$", r"$10|\Sigma|$", r"$20|\Sigma|$"], "D",
   r"$\dfrac{|A|}{|\Sigma|}$ is distributed as the product of independent $\chi^2_n,\chi^2_{n-1},\dots,\chi^2_{n-p+1}$ "
   r"variables. So $E|A|=|\Sigma|\,n(n-1)\cdots(n-p+1)=|\Sigma|(5)(4)=20|\Sigma|$.", "wishart"),

 Q(r"If $A\sim W_3(10,\Sigma)$ and $a$ is a fixed non-zero vector, then "
   r"$\dfrac{a'\Sigma^{-1}a}{a'A^{-1}a}$ has the chi-square distribution with degrees of freedom:",
   ["10", "7", "8", "3"], "C",
   r"For the inverse, the degrees of freedom drop to $n-p+1=10-3+1=8$. (Compare $\dfrac{a'Aa}{a'\Sigma a}\sim\chi^2_n$.) "
   r"This result is what gives Hotelling's $T^2$ its $F$ distribution.", "wishart"),

 Q(r"The Wishart distribution $W_p(n,\Sigma)$ with $\Sigma$ positive definite has a density if and only if:",
   [r"$n\gt2p$", r"$n\ge p$", r"$n\ge1$", r"$n\ge p^2$"], "B",
   r"$A=\sum_{i=1}^{n}Z_iZ_i'$ with $Z_i$ independent $N_p(0,\Sigma)$ is non-singular with probability 1 exactly "
   r"when $n\ge p$; for $n\lt p$ it is singular and has no density on the space of positive definite matrices.", "wishart"),

 Q(r"If $r_{12}=0.6$, $r_{13}=0.5$ and $r_{23}=0.4$, the partial correlation coefficient $r_{12.3}$ is about:",
   ["0.504", "0.400", "0.476", "0.600"], "A",
   r"$r_{12.3}=\dfrac{r_{12}-r_{13}r_{23}}{\sqrt{(1-r_{13}^2)(1-r_{23}^2)}}=\dfrac{0.6-0.2}{\sqrt{0.75\times0.84}}=\dfrac{0.4}{0.794}=0.504$.", "corr"),

 Q(r"If $r_{12}=0.6$, $r_{13}=0.5$ and $r_{23}=0.4$, the multiple correlation coefficient $R_{1.23}$ is about:",
   ["0.781", "0.440", "0.600", "0.664"], "D",
   r"$R_{1.23}^2=\dfrac{r_{12}^2+r_{13}^2-2r_{12}r_{13}r_{23}}{1-r_{23}^2}=\dfrac{0.36+0.25-0.24}{0.84}=0.440$, so "
   r"$R_{1.23}=0.664$. It exceeds both $|r_{12}|$ and $|r_{13}|$, as it must; $0.440$ is $R^2$, not $R$.", "corr"),

 Q(r"Consider the statements about the multiple correlation coefficient $R_{1.23}$:"
   + st(r"$R_{1.23}\ge|r_{12}|$ and $R_{1.23}\ge|r_{13}|$.", r"$0\le R_{1.23}\le1$.", r"$R_{1.23}$ can be negative.",
        r"$1-R_{1.23}^2=(1-r_{12}^2)(1-r_{13.2}^2)$.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "I, II and IV only", "II and IV only"], "C",
   r"$R_{1.23}$ is the largest correlation between $X_1$ and any linear function of $X_2,X_3$, so it is at least "
   r"as large as each simple correlation and is never negative: (I), (II) true, (III) false. (IV) is the "
   r"standard identity: the variance left unexplained by $X_2$ is further reduced by the factor $1-r_{13.2}^2$.", "corr"),

 Q(r"From a sample of 28 observations on three normal variables, $r_{12.3}=0.5$. The $t$ statistic for testing "
   r"that the population partial correlation is zero, and its degrees of freedom, are:",
   ["2.94 on 26", "2.89 on 25", "3.06 on 25", "2.89 on 26"], "B",
   r"For a partial correlation with $k$ variables held fixed, $t=\dfrac{r\sqrt{n-2-k}}{\sqrt{1-r^2}}$ on $n-2-k$ "
   r"degrees of freedom. Here $k=1$: $t=\dfrac{0.5\sqrt{25}}{\sqrt{0.75}}=2.89$ on 25 degrees of freedom.", "corr"),

 Q(r"From 23 observations on three normal variables, $R_{1.23}^2=0.5$. The $F$ statistic for testing that the "
   r"population multiple correlation is zero is:",
   ["10", "20", "11", "5"], "A",
   r"With $p-1=2$ explanatory variables, "
   r"$F=\dfrac{R^2/(p-1)}{(1-R^2)/(n-p)}=\dfrac{0.5/2}{0.5/20}=10$ on $(2,20)$ degrees of freedom.", "corr"),

 Q(r"A sample of 28 pairs from a bivariate normal population gives $r=0.6$. The standard error of Fisher's "
   r"$z=\tfrac12\ln\dfrac{1+r}{1-r}$ is:",
   ["0.189", "0.121", "0.160", "0.200"], "D",
   r"$z$ is approximately normal with variance $\dfrac{1}{n-3}=\dfrac1{25}$, so the standard error is 0.200, "
   r"whatever the value of $\rho$. Here $z=0.693$, and the 95% limits $0.693\pm0.392$ transform back to "
   r"$(0.29,0.80)$ for $\rho$.", "corr"),

 Q(r"Let $\Sigma^{-1}=(\sigma^{ij})$ be the inverse of the covariance matrix of $(X_1,\dots,X_p)'$. The partial "
   r"correlation between $X_1$ and $X_2$, given all the other variables, is:",
   [r"$\dfrac{\sigma^{12}}{\sqrt{\sigma^{11}\sigma^{22}}}$", r"$\dfrac{\sigma_{12}}{\sqrt{\sigma_{11}\sigma_{22}}}$",
    r"$-\dfrac{\sigma^{12}}{\sqrt{\sigma^{11}\sigma^{22}}}$", r"$1-\dfrac{1}{\sigma_{11}\sigma^{11}}$"], "C",
   r"The off-diagonal elements of the concentration matrix $\Sigma^{-1}$, scaled and with the sign changed, are "
   r"the partial correlations given the rest. So a zero in $\Sigma^{-1}$ means conditional independence in the "
   r"normal case. Option B is the simple correlation, and option D is $R^2_{1.2\ldots p}$.", "corr"),

 Q(r"A random sample of size $n=20$ from $N_3(\mu,\Sigma)$ is used to test $H_0:\mu=\mu_0$ by Hotelling's "
   r"$T^2=n(\bar X-\mu_0)'S^{-1}(\bar X-\mu_0)$. Under $H_0$:",
   [r"$T^2\sim F(3,17)$", r"$\dfrac{17}{57}T^2\sim F(3,17)$", r"$\dfrac{17}{57}T^2\sim F(3,19)$", r"$T^2\sim\chi^2_3$"], "B",
   r"$\dfrac{n-p}{p(n-1)}T^2\sim F(p,n-p)$. With $n=20$, $p=3$: $\dfrac{17}{3\times19}=\dfrac{17}{57}$ and the "
   r"degrees of freedom are $(3,17)$. $\chi^2_3$ is the limiting distribution for large $n$.", "hot"),

 Q(r"For a sample of size 10 from a bivariate normal population, $\bar x-\mu_0=(1,2)'$ and "
   r"$S=" + M([[2, 0], [0, 4]]) + r"$. The values of Hotelling's $T^2$ and of the corresponding $F$ statistic are:",
   ["15 and 6.67", "15 and 7.50", "1.5 and 0.67", "30 and 13.33"], "A",
   r"$T^2=n(\bar x-\mu_0)'S^{-1}(\bar x-\mu_0)=10\left(\dfrac12+\dfrac44\right)=15$. "
   r"$F=\dfrac{n-p}{p(n-1)}T^2=\dfrac{8}{18}(15)=6.67$ on $(2,8)$ degrees of freedom.", "hot"),

 Q(r"Consider the statements about Hotelling's $T^2$ for testing $H_0:\mu=\mu_0$:"
   + st(r"It is unchanged when the observations are transformed by $X\to CX+d$ with $C$ non-singular (and "
        r"$\mu_0$ correspondingly).",
        r"For $p=1$ it reduces to the square of Student's $t$.",
        r"The likelihood ratio satisfies $\lambda^{2/n}=\left(1+\dfrac{T^2}{n-1}\right)^{-1}$.",
        r"Its null distribution depends on the unknown $\Sigma$.")
   + "Which of the statements are correct?",
   ["I and II only", "II and III only", "I, II, III and IV", "I, II and III only"], "D",
   r"(I)&ndash;(III) are standard: $T^2$ is invariant, generalises $t^2$ and is equivalent to the likelihood "
   r"ratio test. (IV) is false: because of the invariance, the null distribution is the same for every "
   r"$\Sigma$, namely a multiple of $F(p,n-p)$.", "hot"),

 Q(r"Two independent samples of sizes $n_1=n_2=10$ are drawn from trivariate normal populations with a common "
   r"covariance matrix. The $F$ statistic derived from the two-sample Hotelling's $T^2$ has degrees of freedom:",
   ["(3, 18)", "(3, 17)", "(3, 16)", "(2, 17)"], "C",
   r"$\dfrac{n_1+n_2-p-1}{p(n_1+n_2-2)}T^2\sim F(p,\;n_1+n_2-p-1)=F(3,16)$.", "hot"),

 Q(r"Samples of sizes 10 and 15 from two $p$-variate normal populations with a common covariance matrix give "
   r"the Mahalanobis distance $D^2=2$ between the sample mean vectors. The two-sample Hotelling's $T^2$ is:",
   ["50", "12", "6", "25"], "B",
   r"$T^2=\dfrac{n_1n_2}{n_1+n_2}D^2=\dfrac{150}{25}(2)=12$, where $D^2=(\bar x_1-\bar x_2)'S_p^{-1}(\bar x_1-\bar x_2)$ "
   r"with $S_p$ the pooled covariance matrix.", "hot"),

 Q(r"For testing $H_0:\mu=\mu_0$, let $t(a)$ be the one-sample $t$ statistic computed from the linear "
   r"combination $a'X$. Then $\max_{a\ne0}t^2(a)$ equals:",
   [r"Hotelling's $T^2$", r"$\dfrac{T^2}{p}$", r"the largest characteristic root of $S$", r"$\dfrac{n-p}{p(n-1)}T^2$"], "A",
   r"$t^2(a)=\dfrac{n[a'(\bar x-\mu_0)]^2}{a'Sa}$, and by the Cauchy&ndash;Schwarz inequality its maximum over $a$ is "
   r"$n(\bar x-\mu_0)'S^{-1}(\bar x-\mu_0)=T^2$, attained at $a\propto S^{-1}(\bar x-\mu_0)$. This is Roy's "
   r"union&ndash;intersection derivation of $T^2$ and the basis of simultaneous confidence intervals.", "hot"),

 Q(r"Two groups have $\bar x_1-\bar x_2=(2,1)'$ and pooled covariance matrix $S=" + M([[2, 1], [1, 1]]) + r"$. "
   r"The coefficient vector of Fisher's linear discriminant function is proportional to:",
   [r"$(2,1)'$", r"$(0,1)'$", r"$(1,1)'$", r"$(1,0)'$"], "D",
   r"$a=S^{-1}(\bar x_1-\bar x_2)$ with $S^{-1}=" + M([[1, -1], [-1, 2]]) + r"$: $a=(2-1,\,-2+2)'=(1,0)'$. Although "
   r"the groups differ on both variables, the second adds nothing to the separation once the first is used.", "disc"),

 Q(r"Fisher's linear discriminant function for two groups is $y=x_1$, and the group mean vectors are $(4,2)'$ "
   r"and $(2,1)'$. With equal prior probabilities and equal costs, an observation $x=(3.5,0)'$ is allocated to:",
   ["group 1, since $y=3.5$ exceeds the cut-off 3", "group 2, since $y=3.5$ exceeds the cut-off 3",
    "group 2, since $x_2=0$ is nearer to 1 than to 2", "neither group"], "A",
   r"The cut-off is midway between the discriminant scores of the two means: $\tfrac12(4+2)=3$. Since group 1 "
   r"has the larger mean score and $y=3.5\gt3$, the observation goes to group 1. The value of $x_2$ plays no "
   r"part because its coefficient is zero.", "disc"),

 Q(r"Two normal populations with a common covariance matrix have Mahalanobis distance $\Delta^2=4$. With equal "
   r"prior probabilities, the probability of misclassification by the optimal linear rule is "
   r"(given $\Phi(1)=0.8413$):",
   ["0.0228", "0.3085", "0.1587", "0.5000"], "C",
   r"Each error probability is $\Phi\left(-\dfrac\Delta2\right)=\Phi(-1)=0.1587$. The further apart the "
   r"populations, in standard-deviation units, the smaller the error.", "disc"),

 Q(r"Consider the statements about classification into one of two populations:"
   + st("For normal populations with equal covariance matrices the optimal rule is linear.",
        "For normal populations with unequal covariance matrices the optimal rule is quadratic.",
        r"Fisher's discriminant maximises the ratio of between-group to within-group variation of $a'x$.",
        "The linear discriminant function can be used only when the two samples are of equal size.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "I, III and IV only", "I, II, III and IV"], "B",
   r"The log of the ratio of two normal densities is linear in $x$ when the covariance matrices are equal and "
   r"quadratic otherwise: (I), (II). (III) is Fisher's own criterion, which needs no normality. (IV) is false; "
   r"unequal sample sizes only change the pooled covariance matrix, and unequal priors shift the cut-off.", "disc"),

 Q(r"For the two groups with $\bar x_1-\bar x_2=(2,1)'$ and pooled covariance matrix "
   r"$S=" + M([[2, 1], [1, 1]]) + r"$, the Mahalanobis distance $D^2$ between the groups is:",
   ["5", "3", "1", "2"], "D",
   r"$D^2=d'S^{-1}d$ with $S^{-1}d=(1,0)'$, so $D^2=(2,1)(1,0)'=2$. It is also the difference between the two "
   r"mean discriminant scores.", "disc"),

 Q(r"For the covariance matrix $\Sigma=" + S2 + r"$, the proportion of the total variance explained by the "
   r"first principal component is about:",
   ["71.4%", "83.3%", "85.7%", "100%"], "C",
   r"The characteristic equation is $\lambda^2-7\lambda+6=0$, so $\lambda_1=6$, $\lambda_2=1$. The total variance "
   r"is the trace, 7, and the first component explains $\dfrac67=85.7\%$. ($71.4\%$ is the share of $X_1$ alone, "
   r"$\tfrac57$.)", "pca"),

 Q(r"For the covariance matrix $\Sigma=" + S2 + r"$, the first principal component is:",
   [r"$\dfrac{1}{\sqrt5}(2X_1+X_2)$", r"$\dfrac{1}{\sqrt5}(X_1+2X_2)$", r"$\dfrac{1}{\sqrt2}(X_1+X_2)$",
    r"$\dfrac{1}{\sqrt5}(X_1-2X_2)$"], "A",
   r"For $\lambda_1=6$: $(\Sigma-6I)e=0$ gives $-e_1+2e_2=0$, so $e\propto(2,1)'$, normalised by $\sqrt5$. Check: "
   r"$V(2X_1+X_2)/5=\dfrac{20+2+8}{5}=6$. Option D is the second component, with variance 1.", "pca"),

 Q(r"Principal components are extracted from the correlation matrix $" + M([[1, 0.6], [0.6, 1]]) + r"$. The "
   r"first component and the proportion of variance it explains are:",
   [r"$\dfrac{1}{\sqrt2}(Z_1-Z_2)$ and 80%", r"$\dfrac{1}{\sqrt2}(Z_1+Z_2)$ and 80%",
    r"$\dfrac{1}{\sqrt2}(Z_1+Z_2)$ and 60%", r"$Z_1$ and 50%"], "B",
   r"The characteristic roots are $1+\rho=1.6$ and $1-\rho=0.4$, with vectors $(1,1)'/\sqrt2$ and "
   r"$(1,-1)'/\sqrt2$. The first component explains $\dfrac{1.6}{2}=80\%$. For two standardised variables the "
   r"components are always the sum and the difference, whatever $\rho$ is.", "pca"),

 Q(r"Consider the statements about the principal components $Y_i=e_i'X$ of a covariance matrix $\Sigma$ with "
   r"characteristic roots $\lambda_1\ge\cdots\ge\lambda_p$:"
   + st("Different principal components are uncorrelated.",
        r"$\sum V(Y_i)=\operatorname{tr}\Sigma$.",
        "The components are unchanged when the variables are measured in different units.",
        r"$V(Y_i)=\lambda_i$.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "I, II, III and IV", "I, II and IV only"], "D",
   r"(I), (II) and (IV) follow from the spectral decomposition of $\Sigma$. (III) is false: principal components "
   r"are not scale invariant; changing the units changes $\Sigma$ and its vectors, which is why the correlation "
   r"matrix is used when the variables are on different scales.", "pca"),

 Q(r"For $\Sigma=" + S2 + r"$, the correlation between the first principal component $Y_1$ and $X_1$ is about:",
   ["0.894", "0.816", "0.980", "0.447"], "C",
   r"$\operatorname{Corr}(Y_i,X_k)=\dfrac{e_{ik}\sqrt{\lambda_i}}{\sqrt{\sigma_{kk}}}$. With $e_{11}=\dfrac{2}{\sqrt5}$, "
   r"$\lambda_1=6$, $\sigma_{11}=5$: $\dfrac{2\sqrt6}{5}=0.980$. The loading $e_{11}=0.894$ by itself is not the "
   r"correlation.", "pca"),

 Q(r"Four standardised variables all have pairwise correlation 0.5. The proportion of the total variance "
   r"explained by the first principal component is:",
   ["50%", "62.5%", "25%", "87.5%"], "B",
   r"The equicorrelation matrix $(1-\rho)I+\rho J$ has roots $1+(p-1)\rho=2.5$ once and $1-\rho=0.5$ three "
   r"times. The first component, proportional to the sum of the variables, explains $\dfrac{2.5}{4}=62.5\%$.", "pca"),

 Q(r"The characteristic roots of a $5\times5$ correlation matrix are 2.8, 1.2, 0.6, 0.3 and 0.1. By Kaiser's "
   r"rule, the number of components retained and the cumulative proportion of variance they explain are:",
   ["2 and 80%", "3 and 92%", "1 and 56%", "2 and 56%"], "A",
   r"Kaiser's rule keeps components whose roots exceed 1, the average root of a correlation matrix: here two, "
   r"explaining $\dfrac{2.8+1.2}{5}=80\%$. A scree plot would show the same &lsquo;elbow&rsquo; after the second "
   r"root.", "pca"),

 Q(r"A set of 3 variables is related to a set of 5 variables by canonical correlation analysis. The number of "
   r"canonical correlations is:",
   ["5", "8", "15", "3"], "D",
   r"The number of canonical correlations is $\min(p,q)=3$: they are the positive square roots of the non-zero "
   r"characteristic roots of $\Sigma_{11}^{-1}\Sigma_{12}\Sigma_{22}^{-1}\Sigma_{21}$, a $3\times3$ matrix.", "cca"),

 Q(r"When the first set consists of a single variable $X_1$ and the second set of $X_2,\dots,X_p$, the "
   r"canonical correlation is:",
   ["the largest simple correlation of $X_1$ with any $X_j$", "the largest partial correlation",
    r"the multiple correlation coefficient $R_{1.23\ldots p}$", "always 1"], "C",
   r"The canonical correlation is the largest correlation between a linear function of the first set and a "
   r"linear function of the second. With one variable in the first set this is the largest correlation between "
   r"$X_1$ and $b'X^{(2)}$, which is the multiple correlation coefficient.", "cca"),

 Q(r"$X_1$ has unit variance; $(X_2,X_3)$ are uncorrelated with unit variances; and "
   r"$\operatorname{Cov}(X_1,X_2)=0.6$, $\operatorname{Cov}(X_1,X_3)=0.3$. The canonical correlation between "
   r"$\{X_1\}$ and $\{X_2,X_3\}$ is about:",
   ["0.600", "0.671", "0.450", "0.900"], "B",
   r"$\rho^{*2}=\Sigma_{11}^{-1}\Sigma_{12}\Sigma_{22}^{-1}\Sigma_{21}=0.6^2+0.3^2=0.45$, so $\rho^*=0.671$. It is "
   r"the multiple correlation of $X_1$ on $X_2,X_3$ and exceeds the larger simple correlation, 0.6.", "cca"),

 Q(r"Consider the statements about canonical correlation analysis of two sets of variables:"
   + st("Canonical correlations are unchanged by non-singular linear transformations within each set.",
        "Canonical variates of the same set belonging to different pairs are uncorrelated.",
        "The first canonical correlation is at least as large as the absolute value of any simple correlation "
        "between a variable of one set and a variable of the other.",
        "A canonical correlation can be negative.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and II only", "II and III only", "I, II, III and IV"], "A",
   r"(I) holds because the sets of linear combinations are unchanged. (II) is part of the construction: each new "
   r"pair is chosen uncorrelated with the earlier ones. (III) holds because single variables are particular "
   r"linear combinations. (IV) is false: canonical correlations are defined as non-negative square roots; a "
   r"sign can always be absorbed into a canonical variate.", "cca"),
]
