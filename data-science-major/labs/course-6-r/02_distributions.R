# =====================================================================
# NOT EXECUTED IN VERIFICATION
#
# R could not be installed in the environment where this repository was
# verified -- the Debian package repositories are blocked by the network
# policy, and R is not available from PyPI or npm. This script is
# DESK-CHECKED ONLY: the syntax has been reviewed by hand, not run.
#
# The numbers quoted in the comments below come from the Python equivalent
# in python/, which WAS executed. So the statistics are machine-checked even
# though the R syntax is not. Run this in RStudio to confirm the syntax.
# =====================================================================
# Experiment 2: Visualise Binomial, Normal and Poisson distributions
# Python equivalent: python/02_distributions.py

# --- BINOMIAL(n = 10, p = 0.3) ---
k <- 0:10
pmf <- dbinom(k, size = 10, prob = 0.3)
barplot(pmf, names.arg = k, col = "#1e7fbf",
        main = "Binomial(10, 0.3)", xlab = "k", ylab = "P(X = k)")

dbinom(3, 10, 0.3)   # 0.266828  -- P(X = 3)
pbinom(3, 10, 0.3)   # 0.649611  -- P(X <= 3)
# mean = np = 3.0 ; variance = np(1-p) = 2.1

# --- POISSON(lambda = 3) ---
k <- 0:10
barplot(dpois(k, lambda = 3), names.arg = k, col = "#059669",
        main = "Poisson(3)", xlab = "k", ylab = "P(X = k)")

dpois(3, 3)   # 0.224042
ppois(3, 3)   # 0.647232
# mean = variance = lambda = 3   <- the Poisson signature

# --- NORMAL(mu = 100, sigma = 15) ---
x <- seq(50, 150, by = 0.5)
plot(x, dnorm(x, mean = 100, sd = 15), type = "l", lwd = 2, col = "#0f4c81",
     main = "Normal(100, 15)", ylab = "density")

pnorm(115, 100, 15)                          # 0.841345
pnorm(115, 100, 15) - pnorm(85, 100, 15)     # 0.682689  <- the 68% rule
pnorm(130, 100, 15) - pnorm(70, 100, 15)     # 0.954500  <- 95%
pnorm(145, 100, 15) - pnorm(55, 100, 15)     # 0.997300  <- 99.7%
qnorm(0.95, 100, 15)                         # 124.67 -- the 95th percentile

# NAMING CONVENTION -- worth memorising, it applies to every distribution:
#   d<name>  density / PMF        dbinom, dnorm, dpois
#   p<name>  cumulative (CDF)     pbinom, pnorm, ppois
#   q<name>  quantile (inverse)   qbinom, qnorm, qpois
#   r<name>  random generation    rbinom, rnorm, rpois
