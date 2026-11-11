# -*- coding: utf-8 -*-
"""UGC NET Statistics, Unit VII: fifty exam-standard model questions."""
from . import AR, Q, ar, match, st

TITLE = "Time Series"
BLURB = ("Trend and seasonality, autocorrelation and partial autocorrelation, stationarity, linear processes, "
         "MA, AR and ARMA models, Yule&ndash;Walker equations, model identification, forecasting, ARIMA "
         "models and spectral analysis. Throughout, $Z_t$ denotes white noise with mean 0 and variance "
         r"$\sigma^2$.")

QUESTIONS = [
 Q(r"A centred moving average of period 4 is obtained by averaging two successive 4-term moving averages. "
   r"The weights it gives to $y_{t-2},y_{t-1},y_t,y_{t+1},y_{t+2}$ are:",
   [r"$\tfrac15(1,1,1,1,1)$", r"$\tfrac18(1,2,2,2,1)$", r"$\tfrac14(1,1,0,1,1)$", r"$\tfrac1{10}(1,2,4,2,1)$"], "B",
   r"$\tfrac12\left[\tfrac14(y_{t-2}+y_{t-1}+y_t+y_{t+1})+\tfrac14(y_{t-1}+y_t+y_{t+1}+y_{t+2})\right]"
   r"=\tfrac18(y_{t-2}+2y_{t-1}+2y_t+2y_{t+1}+y_{t+2})$. Centring is needed because an even-period average falls "
   r"between two time points.", "intro"),

 Q(r"The values of a series in five successive years are 10, 12, 15, 17 and 21. A straight-line trend is "
   r"fitted by least squares. The trend value for the sixth year is:",
   ["22.7", "23.7", "24.0", "23.1"], "D",
   r"Code the years $t=-2,-1,0,1,2$: $\sum y=75$, $\sum ty=-20-12+0+17+42=27$, $\sum t^2=10$. So "
   r"$a=\bar y=15$, $b=\dfrac{27}{10}=2.7$, and for the sixth year ($t=3$) the trend value is $15+2.7(3)=23.1$.", "intro"),

 Q(r"In a multiplicative model the seasonal indices of the first three quarters are 80, 110 and 120. The "
   r"seasonal index of the fourth quarter is:",
   ["90", "100", "110", "77.5"], "A",
   r"Quarterly seasonal indices average 100, so they add up to 400. The fourth is $400-(80+110+120)=90$. "
   r"(Monthly indices add up to 1200.)", "intro"),

 Q(r"Simple exponential smoothing with constant $\alpha=0.3$ gave the forecast 20 for the current period, in "
   r"which the actual value turned out to be 30. The forecast for the next period is:",
   ["27", "25", "23", "21"], "C",
   r"$F_{t+1}=\alpha y_t+(1-\alpha)F_t=F_t+\alpha(y_t-F_t)=20+0.3(10)=23$. Using weight 0.7 on the actual value "
   r"gives 27.", "intro"),

 Q(r"Applying a moving average to a purely random series produces a smoothed series that shows regular-looking "
   r"oscillations which are not present in the original data. This is called the:",
   ["Gibbs phenomenon", "Slutsky&ndash;Yule effect", "Yule&ndash;Walker effect", "aliasing effect"], "B",
   r"A moving average of uncorrelated terms is autocorrelated (successive averages share terms), and an "
   r"autocorrelated series wanders in waves. Slutsky and Yule showed that such spurious cycles can be created "
   r"by the smoothing itself. Aliasing is the confusion of frequencies caused by sampling at discrete times.", "intro"),

 Q(r"Which of the following pairs $(\rho_1,\rho_2)$ can NOT be the first two autocorrelations of a stationary "
   r"process?",
   ["(0.5, 0.25)", "(0.4, 0)", "($-0.5$, 0.4)", "(0.8, 0.1)"], "D",
   r"The autocorrelation matrix must be non-negative definite. For lags up to 2 this requires "
   r"$\rho_2\ge2\rho_1^2-1$. For $\rho_1=0.8$ the bound is $0.28\gt0.1$, so $(0.8,0.1)$ is impossible: two "
   r"observations each highly correlated with the one between them cannot be nearly uncorrelated. The other "
   r"pairs satisfy the condition.", "acf"),

 Q(r"A stationary process has $\rho_1=0.5$ and $\rho_2=0.4$. Its partial autocorrelation at lag 2 is:",
   ["0.20", "0.40", "0.15", "0.25"], "A",
   r"$\phi_{22}=\dfrac{\rho_2-\rho_1^2}{1-\rho_1^2}=\dfrac{0.40-0.25}{0.75}=0.20$. It is the correlation between "
   r"$X_t$ and $X_{t-2}$ after removing the linear effect of $X_{t-1}$.", "acf"),

 Q(r"For a white-noise series of length $n=100$, the approximate 95% limits within which the sample "
   r"autocorrelations should lie are:",
   [r"$\pm0.100$", r"$\pm0.010$", r"$\pm0.196$", r"$\pm0.020$"], "C",
   r"For white noise the sample autocorrelations are approximately independent $N\left(0,\tfrac1n\right)$, so the "
   r"limits are $\pm\dfrac{1.96}{\sqrt n}=\pm0.196$. About one lag in twenty will fall outside by chance.", "acf"),

 Q(r"Let $X_t=A\cos\omega t+B\sin\omega t$, where $A$ and $B$ are uncorrelated random variables with mean 0 and "
   r"variance $\sigma^2$, and $\omega$ is a constant. The autocovariance function of $\{X_t\}$ is:",
   [r"$\sigma^2$ for $h=0$ and 0 otherwise", r"$\sigma^2\cos\omega h$", r"$\sigma^2\sin\omega h$", r"$\sigma^2e^{-|h|}$"], "B",
   r"$\operatorname{Cov}(X_t,X_{t+h})=\sigma^2[\cos\omega t\cos\omega(t+h)+\sin\omega t\sin\omega(t+h)]=\sigma^2\cos\omega h$. "
   r"It depends only on $h$, so the process is stationary, but the autocovariance never dies out: the process is "
   r"deterministic, completely predictable from two past values.", "acf"),

 Q(r"Match the model in List I with the theoretical behaviour of its ACF and PACF in List II."
   + match(["AR($p$)", "MA($q$)", "ARMA($p,q$)", "White noise"],
           ["ACF tails off; PACF cuts off after lag $p$", "ACF cuts off after lag $q$; PACF tails off",
            "Both ACF and PACF tail off", "Both are zero at all non-zero lags"]),
   ["(a)-(i), (b)-(ii), (c)-(iii), (d)-(iv)", "(a)-(ii), (b)-(i), (c)-(iii), (d)-(iv)",
    "(a)-(i), (b)-(ii), (c)-(iv), (d)-(iii)", "(a)-(iii), (b)-(ii), (c)-(i), (d)-(iv)"], "A",
   r"This duality is the basis of Box&ndash;Jenkins identification: the PACF identifies the order of a pure "
   r"autoregression, the ACF the order of a pure moving average, and when neither cuts off a mixed model is "
   r"indicated.", "acf"),

 Q(r"Consider the processes:"
   + st(r"$X_t=Z_t$", r"$X_t=X_{t-1}+Z_t$, $X_0=0$", r"$X_t=Z_t+0.5Z_{t-1}$", r"$X_t=t+Z_t$")
   + "Which of them are weakly stationary?",
   ["I only", "I, II and III only", "I and III only", "I, III and IV only"], "C",
   r"(I) and (III) have constant mean and autocovariances depending only on the lag (every finite moving "
   r"average of white noise is stationary). (II) is a random walk with $V(X_t)=t\sigma^2$, growing with $t$. "
   r"(IV) has mean $t$, not constant.", "stat"),

 Q(r"Let $Z_t$ be independent $N(0,1)$ variables and $X_t=Z_tZ_{t-1}$. Then $\{X_t\}$ is:",
   ["not stationary", "stationary with $\\rho_1=0.5$", "a sequence of independent random variables",
    "white noise, but its terms are not independent"], "D",
   r"$E(X_t)=0$, $V(X_t)=E(Z_t^2)E(Z_{t-1}^2)=1$ and "
   r"$\operatorname{Cov}(X_t,X_{t-1})=E(Z_t)E(Z_{t-1}^2)E(Z_{t-2})=0$, so the series is uncorrelated with constant "
   r"mean and variance: white noise. But $X_t$ and $X_{t-1}$ share $Z_{t-1}$; for instance $X_t^2$ and "
   r"$X_{t-1}^2$ are correlated. Uncorrelated does not mean independent.", "stat"),

 Q(ar("A strictly stationary process with finite second moments is weakly stationary.",
      "A weakly stationary Gaussian process is strictly stationary."),
   AR, "B",
   r"Both are true. (A): if all joint distributions are invariant under shifts, so are the means and "
   r"covariances, when they exist. (R): a Gaussian process is determined by its means and covariances, so "
   r"invariance of these gives invariance of every joint distribution. (R) is the converse of (A) for Gaussian "
   r"processes, not an explanation of it.", "stat"),

 Q(r"For a stationary AR(1) process with $\phi=0.5$ and variance $\gamma_0$, the variance of the mean of $n$ "
   r"consecutive observations is, for large $n$, approximately $c\,\dfrac{\gamma_0}{n}$, where $c$ is:",
   ["3", "1", "2", "4"], "A",
   r"$nV(\bar X)\to\sum_{h=-\infty}^{\infty}\gamma_h=\gamma_0\left(1+2\sum_{h\ge1}\phi^h\right)=\gamma_0\dfrac{1+\phi}{1-\phi}=3\gamma_0$. "
   r"Positive autocorrelation makes the mean three times as variable as for independent observations; the "
   r"sample is &lsquo;worth&rsquo; only $n/3$ independent values.", "stat"),

 Q(r"The ARMA(1,1) process $X_t=0.5X_{t-1}+Z_t+0.4Z_{t-1}$ is written as $X_t=\sum_{j\ge0}\psi_jZ_{t-j}$ with "
   r"$\psi_0=1$. The values of $\psi_1$ and $\psi_2$ are:",
   ["0.5 and 0.25", "0.9 and 0.81", "0.9 and 0.45", "0.4 and 0.2"], "C",
   r"Equating coefficients in $(1-0.5B)\psi(B)=1+0.4B$: $\psi_1-0.5=0.4$, so $\psi_1=0.9$; and "
   r"$\psi_j=0.5\psi_{j-1}$ for $j\ge2$, so $\psi_2=0.45$. In general $\psi_j=(\phi+\theta)\phi^{j-1}$.", "wold"),

 Q(r"A linear process $X_t=\sum_{j=0}^{\infty}\psi_jZ_{t-j}$ has $\psi_j=(0.5)^j$. Its variance is:",
   [r"$2\sigma^2$", r"$\dfrac43\sigma^2$", r"$\sigma^2$", r"$4\sigma^2$"], "B",
   r"$V(X_t)=\sigma^2\sum\psi_j^2=\sigma^2\sum(0.25)^j=\dfrac{\sigma^2}{1-0.25}=\dfrac43\sigma^2$. This is the AR(1) "
   r"process with $\phi=0.5$ in its moving-average (Wold) form. $2\sigma^2$ is $\sigma^2\sum\psi_j$, not the "
   r"variance.", "wold"),

 Q(r"For the MA(1) process $X_t=Z_t+0.5Z_{t-1}$, the autocorrelation at lag 1 is:",
   ["0.5", "0.25", "0.8", "0.4"], "D",
   r"$\rho_1=\dfrac{\theta}{1+\theta^2}=\dfrac{0.5}{1.25}=0.4$, and $\rho_k=0$ for $k\ge2$.", "ma"),

 Q(r"For an MA(1) process, the largest possible value of $|\rho_1|$ is:",
   ["0.5", "1", "0.25", "0.707"], "A",
   r"$\rho_1=\dfrac{\theta}{1+\theta^2}$ and $1+\theta^2\ge2|\theta|$, so $|\rho_1|\le\tfrac12$, with equality at "
   r"$\theta=\pm1$. A series with lag-one autocorrelation 0.7 and nothing beyond cannot be an MA(1).", "ma"),

 Q(r"The MA(1) processes $X_t=Z_t+2Z_{t-1}$ and $X_t=Z_t+0.5Z_{t-1}$:",
   ["have different autocorrelation functions, and both are invertible",
    "have the same autocorrelation function, and both are invertible",
    "have the same autocorrelation function, and only the second is invertible",
    "have the same autocorrelation function, and only the first is invertible"], "C",
   r"$\dfrac{\theta}{1+\theta^2}$ is unchanged when $\theta$ is replaced by $\dfrac1\theta$: both give $\rho_1=0.4$. "
   r"Invertibility requires $|\theta|\lt1$ (the root of $1+\theta z$ outside the unit circle), which holds only for "
   r"$\theta=0.5$. Invertibility is imposed precisely to make the model unique.", "ma"),

 Q(r"For the MA(2) process $X_t=Z_t+0.5Z_{t-1}+0.5Z_{t-2}$, the autocorrelations $\rho_1$ and $\rho_2$ are:",
   [r"$\dfrac13$ and $\dfrac13$", r"$\dfrac12$ and $\dfrac13$", r"$\dfrac12$ and $\dfrac14$", r"$\dfrac34$ and $\dfrac12$"], "B",
   r"$\gamma_0=\sigma^2(1+\theta_1^2+\theta_2^2)=1.5\sigma^2$, "
   r"$\gamma_1=\sigma^2(\theta_1+\theta_1\theta_2)=0.75\sigma^2$, $\gamma_2=\sigma^2\theta_2=0.5\sigma^2$. So "
   r"$\rho_1=\tfrac12$, $\rho_2=\tfrac13$ and $\rho_k=0$ for $k\ge3$.", "ma"),

 Q(r"The MA(2) process $X_t=Z_t-1.3Z_{t-1}+0.4Z_{t-2}$ is:",
   ["invertible, since the roots of $1-1.3z+0.4z^2=0$ are 1.25 and 2",
    "not invertible, since one coefficient exceeds 1 in absolute value",
    "not invertible, since the roots of $1-1.3z+0.4z^2=0$ are 0.8 and 0.5",
    "not stationary"], "A",
   r"$1-1.3z+0.4z^2=(1-0.8z)(1-0.5z)$, with roots $z=1.25$ and $z=2$, both outside the unit circle: invertible. "
   r"Invertibility is a condition on the roots, not on the size of individual coefficients. Every finite "
   r"moving average is stationary.", "ma"),

 Q(r"For the AR(1) process $X_t=0.8X_{t-1}+Z_t$ with $\sigma^2=1$, the variance of $X_t$ and the "
   r"autocorrelation at lag 3 are:",
   ["5.00 and 0.512", "1.64 and 0.512", "2.78 and 0.640", "2.78 and 0.512"], "D",
   r"$\gamma_0=\dfrac{\sigma^2}{1-\phi^2}=\dfrac{1}{0.36}=2.78$ and $\rho_3=\phi^3=0.512$. "
   r"($5.00=\tfrac{1}{1-\phi}$ is the sum of the $\psi$ weights, not the variance.)", "ar"),

 Q(r"For which of the following values of $(\phi_1,\phi_2)$ is the AR(2) process "
   r"$X_t=\phi_1X_{t-1}+\phi_2X_{t-2}+Z_t$ stationary?",
   ["(1.2, $-0.1$)", "(0.2, 0.9)", "(0.5, 0.3)", "($-0.5$, 0.6)"], "C",
   r"The stationarity region is the triangle $\phi_1+\phi_2\lt1$, $\phi_2-\phi_1\lt1$, $|\phi_2|\lt1$. "
   r"$(0.5,0.3)$ satisfies all three. $(1.2,-0.1)$ and $(0.2,0.9)$ have $\phi_1+\phi_2=1.1$; $(-0.5,0.6)$ has "
   r"$\phi_2-\phi_1=1.1$.", "ar"),

 Q(r"For the stationary AR(2) process $X_t=0.5X_{t-1}+0.3X_{t-2}+Z_t$, the autocorrelations $\rho_1$ and "
   r"$\rho_2$ are approximately:",
   ["0.500 and 0.550", "0.714 and 0.657", "0.714 and 0.510", "0.625 and 0.613"], "B",
   r"The Yule&ndash;Walker equations give $\rho_1=\dfrac{\phi_1}{1-\phi_2}=\dfrac{0.5}{0.7}=0.714$ and "
   r"$\rho_2=\phi_1\rho_1+\phi_2=0.357+0.3=0.657$.", "ar"),

 Q(r"The autocorrelation function of the AR(2) process $X_t=X_{t-1}-0.5X_{t-2}+Z_t$ is:",
   ["a damped sine wave", "a mixture of two decaying exponentials", "zero after lag 2", "constant"], "A",
   r"The process is stationary ($\phi_1+\phi_2=0.5$, $\phi_2-\phi_1=-1.5$, $|\phi_2|\lt1$) and "
   r"$\phi_1^2+4\phi_2=1-2\lt0$, so the roots of the characteristic equation are complex and the autocorrelation "
   r"function is a damped sine wave with damping factor $\sqrt{-\phi_2}=0.707$: the series shows "
   r"pseudo-periodic behaviour.", "ar"),

 Q(r"The mean of the stationary process $X_t=5+0.5X_{t-1}+Z_t$ is:",
   ["5", "2.5", "7.5", "10"], "D",
   r"Taking expectations, $\mu=5+0.5\mu$, so $\mu=\dfrac{5}{1-0.5}=10$. The constant in an autoregression is not "
   r"the mean; it is $\mu(1-\phi)$.", "ar"),

 Q(r"For the AR(2) process $X_t=0.5X_{t-1}+0.3X_{t-2}+Z_t$, the partial autocorrelations at lags 2 and 3 are:",
   ["0.657 and 0.3", "0.3 and 0.15", "0.3 and 0", "0.5 and 0.3"], "C",
   r"For an AR($p$) process the partial autocorrelation at lag $p$ equals $\phi_p$ and is zero beyond it. So "
   r"$\phi_{22}=\phi_2=0.3$ and $\phi_{33}=0$. (At lag 1, $\phi_{11}=\rho_1=0.714$.)", "ar"),

 Q(r"For the ARMA(1,1) process $X_t=0.5X_{t-1}+Z_t+0.4Z_{t-1}$, the autocorrelation at lag 1 is about:",
   ["0.900", "0.692", "0.500", "0.577"], "B",
   r"$\rho_1=\dfrac{(1+\phi\theta)(\phi+\theta)}{1+2\phi\theta+\theta^2}=\dfrac{(1.2)(0.9)}{1+0.4+0.16}=\dfrac{1.08}{1.56}=0.692$. "
   r"After that $\rho_k=\phi\rho_{k-1}$.", "arma"),

 Q(r"The process defined by $X_t-0.5X_{t-1}=Z_t-0.5Z_{t-1}$ is:",
   ["white noise", "an ARMA(1,1) process with $\\rho_1\\ne0$", "non-stationary", "non-invertible"], "A",
   r"The autoregressive and moving-average operators have the common factor $(1-0.5B)$, which cancels, leaving "
   r"$X_t=Z_t$. (The formula gives $\rho_1\propto(1+\phi\theta)(\phi+\theta)=0$.) Such parameter redundancy is why "
   r"an ARMA model is required to have no common factors.", "arma"),

 Q(r"The ARMA(1,1) process $(1-0.5B)X_t=(1+2B)Z_t$ is:",
   ["causal and invertible", "neither causal nor invertible", "invertible but not causal", "causal but not invertible"], "D",
   r"Causality (stationarity) needs the root of $1-0.5z=0$, $z=2$, outside the unit circle: satisfied. "
   r"Invertibility needs the root of $1+2z=0$, $z=-0.5$, outside the unit circle: not satisfied.", "arma"),

 Q(r"For a stationary ARMA(1,1) process with autoregressive parameter $\phi$, the autocorrelations satisfy:",
   [r"$\rho_k=\phi^k$ for all $k\ge1$", r"$\rho_k=0$ for $k\ge2$", r"$\rho_k=\phi\rho_{k-1}$ for $k\ge2$",
    r"$\rho_k=\phi\rho_{k-1}$ for all $k\ge1$"], "C",
   r"Multiply the model by $X_{t-k}$ and take expectations: for $k\ge2$ the moving-average terms are "
   r"uncorrelated with $X_{t-k}$, so $\gamma_k=\phi\gamma_{k-1}$. At $k=1$ the term $\theta Z_{t-1}$ is correlated "
   r"with $X_{t-1}$, so $\rho_1\ne\phi$: the decay starts from $\rho_1$, not from $\rho_0$.", "arma"),

 Q(r"A series has $r_1=0.5$ and $r_2=0.4$. The Yule&ndash;Walker estimates of $(\phi_1,\phi_2)$ for an AR(2) "
   r"model are:",
   ["(0.4, 0.2)", "(0.5, 0.4)", "(0.2, 0.4)", "(0.6, 0.1)"], "A",
   r"Solve $r_1=\phi_1+\phi_2r_1$, $r_2=\phi_1r_1+\phi_2$: "
   r"$\hat\phi_2=\dfrac{r_2-r_1^2}{1-r_1^2}=\dfrac{0.15}{0.75}=0.2$ and "
   r"$\hat\phi_1=\dfrac{r_1(1-r_2)}{1-r_1^2}=\dfrac{0.30}{0.75}=0.4$.", "yw"),

 Q(r"A series has sample variance $c_0=4$ and $r_1=0.5$. For an AR(1) model the Yule&ndash;Walker estimate of "
   r"the white-noise variance is:",
   ["4", "2", "1", "3"], "D",
   r"$\hat\phi=r_1=0.5$ and $\hat\sigma^2=c_0(1-\hat\phi r_1)=4(1-0.25)=3$.", "yw"),

 Q(r"An AR(2) process has $\gamma_0=10$, $\phi_1=0.4$, $\phi_2=0.2$, $\rho_1=0.5$ and $\rho_2=0.4$. The "
   r"white-noise variance $\sigma^2$ is:",
   ["8.0", "7.2", "6.0", "2.8"], "B",
   r"$\sigma^2=\gamma_0(1-\phi_1\rho_1-\phi_2\rho_2)=10(1-0.20-0.08)=7.2$. The fraction of the variance explained by "
   r"the two lagged values is $\phi_1\rho_1+\phi_2\rho_2=0.28$.", "yw"),

 Q(r"For a model with $k$ estimated parameters fitted to $n$ observations, consider the statements:"
   + st(r"$AIC=-2\ln L+2k$.", r"For $n\ge8$, BIC penalises an additional parameter more heavily than AIC.",
        "AIC selects the true order consistently as $n\\to\\infty$.",
        "BIC selects the true order consistently as $n\\to\\infty$.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "I, II and IV only", "I, II, III and IV"], "C",
   r"$BIC=-2\ln L+k\ln n$, and $\ln n\gt2$ for $n\ge8$: (I), (II). BIC is consistent, while AIC has a positive "
   r"probability of choosing too large an order however large $n$ is, so it tends to overfit: (IV) true, "
   r"(III) false.", "order"),

 Q(r"The stages of the Box&ndash;Jenkins approach to time-series modelling, in the correct order, are:",
   ["identification, estimation, diagnostic checking, forecasting",
    "estimation, identification, diagnostic checking, forecasting",
    "identification, diagnostic checking, estimation, forecasting",
    "diagnostic checking, identification, estimation, forecasting"], "A",
   r"A tentative model is identified from the ACF and PACF (after differencing if needed), its parameters are "
   r"estimated, the residuals are checked for whiteness, and only an adequate model is used for forecasting. If "
   r"the check fails, the cycle is repeated.", "order"),

 Q(r"An ARMA(1,1) model is fitted and the Ljung&ndash;Box statistic is computed from the first 20 residual "
   r"autocorrelations. Under the hypothesis that the model is adequate, it is referred to chi-square with "
   r"degrees of freedom:",
   ["20", "18", "19", "17"], "B",
   r"The degrees of freedom are $m-p-q=20-1-1=18$: one is lost for each estimated ARMA parameter. A large value "
   r"of $Q=n(n+2)\sum_{k=1}^{m}\dfrac{r_k^2}{n-k}$ indicates that the residuals are not white noise.", "order"),

 Q(r"The sample ACF of a stationary series is significant at lags 1 and 2 and negligible afterwards, while the "
   r"sample PACF decays gradually. The model suggested is:",
   ["AR(2)", "ARMA(2,2)", "AR(1)", "MA(2)"], "D",
   r"An ACF that cuts off after lag $q$ with a PACF that tails off is the signature of MA($q$); here $q=2$. The "
   r"opposite pattern (PACF cutting off after lag 2) would indicate AR(2).", "order"),

 Q(r"An AR(1) process has mean 10 and $\phi=0.5$, and the last observation is $X_n=12$. The minimum mean "
   r"square error forecast of $X_{n+2}$ is:",
   ["11.0", "10.0", "10.5", "12.0"], "C",
   r"$\hat X_n(h)=\mu+\phi^h(X_n-\mu)=10+0.25(2)=10.5$. The forecasts decay geometrically to the mean: 11, 10.5, "
   r"10.25, ...", "fcst"),

 Q(r"For the AR(1) process with $\phi=0.5$ and $\sigma^2=1$, the variance of the two-step-ahead forecast "
   r"error is:",
   ["1.25", "1.00", "1.33", "1.50"], "A",
   r"$V[e_n(h)]=\sigma^2\sum_{j=0}^{h-1}\psi_j^2=\sigma^2\,\dfrac{1-\phi^{2h}}{1-\phi^2}$. For $h=2$: $1+\phi^2=1.25$. "
   r"As $h\to\infty$ it rises to the process variance $\tfrac43$.", "fcst"),

 Q(r"For the MA(1) process $X_t=Z_t+0.6Z_{t-1}$ with $\sigma^2=1$, the variances of the one-step and two-step "
   r"forecast errors are:",
   ["1 and 1", "1 and 1.36", "1.36 and 1.36", "1 and 1.6"], "B",
   r"One step ahead the forecast is $0.6Z_n$ and the error is $Z_{n+1}$: variance 1. Two or more steps ahead "
   r"the forecast is the mean, and the error is $X_{n+h}$ itself: variance $1+\theta^2=1.36$. An MA($q$) process "
   r"has no forecasting memory beyond $q$ steps.", "fcst"),

 Q(r"For the random walk $X_t=X_{t-1}+Z_t$ with $\sigma=2$, the standard error of the forecast of $X_{n+4}$ made "
   r"at time $n$ is:",
   ["2", "8", "16", "4"], "D",
   r"The forecast is $X_n$ for every lead time, and the error $Z_{n+1}+\cdots+Z_{n+h}$ has variance $h\sigma^2=16$, "
   r"standard error 4. The forecast limits widen as $\sqrt h$ without bound, unlike those of a stationary "
   r"process.", "fcst"),

 Q(r"For the random walk $X_t=Z_1+\cdots+Z_t$, the correlation between $X_4$ and $X_9$ is:",
   [r"$\dfrac23$", r"$\dfrac49$", r"$\dfrac{4}{13}$", r"$\dfrac12$"], "A",
   r"$\operatorname{Cov}(X_s,X_t)=\min(s,t)\,\sigma^2$, so for $s\lt t$, "
   r"$\operatorname{Corr}(X_s,X_t)=\dfrac{s}{\sqrt{st}}=\sqrt{\dfrac st}=\sqrt{\dfrac49}=\dfrac23$. It depends on $s$ "
   r"and $t$ separately, not on $t-s$ alone: the process is not stationary.", "ns"),

 Q(r"The process $X_t=1.5X_{t-1}-0.5X_{t-2}+Z_t$ is:",
   ["a stationary AR(2) process", "ARIMA(0,1,1)", "ARIMA(1,1,0)", "ARIMA(0,2,0)"], "C",
   r"$1-1.5B+0.5B^2=(1-B)(1-0.5B)$. One root is on the unit circle, so the process is not stationary; its first "
   r"difference $W_t=(1-B)X_t$ satisfies $W_t=0.5W_{t-1}+Z_t$, a stationary AR(1). Hence ARIMA(1,1,0).", "ns"),

 Q(r"If white noise $Z_t$ is differenced unnecessarily, the series $W_t=Z_t-Z_{t-1}$ is:",
   ["white noise", "a non-invertible MA(1) process with $\\rho_1=-0.5$", "an AR(1) process with $\\phi=-1$",
    "a random walk"], "B",
   r"$W_t$ is MA(1) with $\theta=-1$: $\rho_1=\dfrac{-1}{2}=-0.5$, and the root of $1-z=0$ lies on the unit circle, "
   r"so it is not invertible. Over-differencing introduces artificial negative autocorrelation and doubles the "
   r"variance.", "ns"),

 Q(r"Consider the statements about the Dickey&ndash;Fuller test:"
   + st("The null hypothesis is that the series has a unit root.",
        r"Under the null hypothesis the test statistic has Student's $t$ distribution.",
        "The augmented test adds lagged differences to allow for serial correlation in the errors.",
        "Rejection of the null hypothesis supports stationarity.")
   + "Which of the statements are correct?",
   ["I and II only", "I and III only", "I, II and IV only", "I, III and IV only"], "D",
   r"The test regresses $\nabla X_t$ on $X_{t-1}$ and tests whether its coefficient is zero (a unit root) "
   r"against the alternative that it is negative (stationarity). Under the null the $t$-ratio does not have a "
   r"$t$ distribution; it has the skewed Dickey&ndash;Fuller distribution with its own critical values: (II) is "
   r"false.", "ns"),

 Q(r"For the MA(1) process $X_t=Z_t+0.5Z_{t-1}$ with spectral density $f(\lambda)$, $-\pi\le\lambda\le\pi$, the "
   r"ratio $f(0)/f(\pi)$ is:",
   ["3", "1", "9", "2.25"], "C",
   r"$f(\lambda)=\dfrac{\sigma^2}{2\pi}\left|1+\theta e^{-i\lambda}\right|^2=\dfrac{\sigma^2}{2\pi}(1+\theta^2+2\theta\cos\lambda)$. "
   r"So $f(0)\propto(1+\theta)^2=2.25$ and $f(\pi)\propto(1-\theta)^2=0.25$: the ratio is 9. With $\theta\gt0$ the "
   r"power is concentrated at low frequencies.", "spec"),

 Q(r"The spectral density of the AR(1) process $X_t=\phi X_{t-1}+Z_t$ with $0\lt\phi\lt1$ is:",
   ["largest at frequency 0 and decreasing on $(0,\\pi)$", "largest at frequency $\\pi$ and increasing on $(0,\\pi)$",
    "constant", "largest at frequency $\\pi/2$"], "A",
   r"$f(\lambda)=\dfrac{\sigma^2}{2\pi(1-2\phi\cos\lambda+\phi^2)}$. For $\phi\gt0$ the denominator is smallest at "
   r"$\lambda=0$, so low frequencies dominate, matching a smooth, slowly wandering series. For $\phi\lt0$ the "
   r"peak is at $\pi$ and the series oscillates rapidly. White noise has a constant spectrum.", "spec"),

 Q(r"With the spectral density defined by "
   r"$f(\lambda)=\dfrac{1}{2\pi}\sum_{h=-\infty}^{\infty}\gamma_he^{-ih\lambda}$, the integral "
   r"$\displaystyle\int_{-\pi}^{\pi}f(\lambda)\,d\lambda$ equals:",
   ["1", r"$\gamma_0$", r"$2\pi\gamma_0$", r"$\sigma^2$"], "B",
   r"$\gamma_h=\displaystyle\int_{-\pi}^{\pi}e^{ih\lambda}f(\lambda)\,d\lambda$, and at $h=0$ this is the variance: the "
   r"spectral density decomposes the variance of the process over frequencies. $f$ is real, even and "
   r"non-negative.", "spec"),

 Q(ar("The periodogram is not a consistent estimator of the spectral density.",
      "The variance of a periodogram ordinate does not tend to zero as the length of the series increases."),
   AR, "A",
   r"The periodogram is asymptotically unbiased, but each ordinate behaves like $f(\lambda)$ times a "
   r"$\tfrac12\chi^2_2$ variable, with variance about $f(\lambda)^2$ however long the series is, and neighbouring "
   r"ordinates are nearly independent. So it never settles down; consistent estimates are obtained by smoothing "
   r"it with a spectral window. Both statements are true and (R) is the reason.", "period"),
]
