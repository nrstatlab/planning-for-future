"""Experiment 5 — Maximum likelihood estimation.

unit-3.md section 3.7 derives the MLE for a coin by hand and claims two things
this script checks numerically:

  * the MLE of a Bernoulli parameter is the sample proportion (7 heads in 10
    gives p-hat = 0.7)
  * least squares IS the MLE for linear regression under normal errors

The second is the connection worth knowing and the one rarely demonstrated.
"""
import numpy as np
from scipy import optimize, stats

from fixtures import STUDY, study_xy


def coin_mle_by_grid_and_by_calculus():
    """Ten flips, seven heads. The hand derivation says p-hat = 0.7."""
    heads, n = 7, 10

    def log_likelihood(p):
        return heads * np.log(p) + (n - heads) * np.log(1 - p)

    grid = np.linspace(0.001, 0.999, 999)
    numeric = grid[np.argmax([log_likelihood(p) for p in grid])]
    analytic = heads / n

    assert round(analytic, 4) == 0.7
    assert abs(numeric - analytic) < 0.002, (numeric, analytic)

    # The likelihood at the MLE beats every alternative -- the definition.
    assert log_likelihood(0.7) > log_likelihood(0.5)
    assert log_likelihood(0.7) > log_likelihood(0.9)

    print(f"  {heads} heads in {n} flips")
    print(f"    analytic MLE  (calculus)   p-hat = {analytic:.4f}")
    print(f"    numeric  MLE  (grid search) p-hat = {numeric:.4f}")
    print(f"    log-likelihood at p=0.5 {log_likelihood(0.5):8.4f}")
    print(f"                   at p=0.7 {log_likelihood(0.7):8.4f}  <- maximum")
    print(f"                   at p=0.9 {log_likelihood(0.9):8.4f}")
    print("       the MLE is the SAMPLE PROPORTION, which is what intuition")
    print("       already suggested -- MLE gives it a principled derivation")


def why_take_logs():
    """Products of many small probabilities underflow. Sums of logs do not."""
    p = 0.5
    n = 2000

    product = p ** n
    log_sum = n * np.log(p)

    assert product == 0.0, "underflowed to EXACTLY zero"
    assert log_sum < -1000 and np.isfinite(log_sum)

    print(f"  0.5 ** {n} as a float  = {product}   <- underflowed to zero")
    print(f"  {n} * ln(0.5)          = {log_sum:.4f}   <- finite and usable")
    print("       a likelihood is a PRODUCT of n probabilities each below 1.")
    print("       Beyond a few hundred observations it is exactly 0.0 in")
    print("       floating point, and every candidate parameter ties at zero.")
    print("       The log is monotonic, so the maximum is unchanged")


def least_squares_is_the_mle_under_normal_errors():
    """unit-3.md's claim, verified: two different derivations, one answer."""
    X, y = study_xy()
    x = X.ravel()

    # (a) Ordinary least squares, in closed form.
    x_bar, y_bar = x.mean(), y.mean()
    ls_slope = ((x - x_bar) * (y - y_bar)).sum() / ((x - x_bar) ** 2).sum()
    ls_intercept = y_bar - ls_slope * x_bar

    # (b) Maximum likelihood, assuming y ~ Normal(b0 + b1 x, sigma).
    def negative_log_likelihood(theta):
        b0, b1, log_sigma = theta
        sigma = np.exp(log_sigma)
        residual = y - (b0 + b1 * x)
        return -np.sum(stats.norm.logpdf(residual, loc=0, scale=sigma))

    fit = optimize.minimize(negative_log_likelihood, x0=[0.0, 1.0, 0.0],
                            method="Nelder-Mead",
                            options={"xatol": 1e-10, "fatol": 1e-10,
                                     "maxiter": 20000, "maxfev": 20000})
    mle_intercept, mle_slope, log_sigma = fit.x

    assert fit.success, fit.message
    assert round(ls_slope, 4) == 4.3030
    assert round(ls_intercept, 4) == 43.0303
    assert abs(mle_slope - ls_slope) < 1e-3, (mle_slope, ls_slope)
    assert abs(mle_intercept - ls_intercept) < 1e-2, (mle_intercept, ls_intercept)

    # And the MLE of sigma is the ROOT MEAN squared residual (divide by n),
    # not the unbiased estimate (divide by n-2).
    residual = y - (ls_intercept + ls_slope * x)
    sigma_mle = np.sqrt((residual ** 2).mean())
    assert abs(np.exp(log_sigma) - sigma_mle) < 1e-2

    print("                     slope    intercept")
    print(f"    least squares  {ls_slope:9.4f}  {ls_intercept:11.4f}")
    print(f"    maximum likelihood {mle_slope:5.4f}  {mle_intercept:11.4f}")
    print(f"    agree to within {abs(mle_slope - ls_slope):.2e} and "
          f"{abs(mle_intercept - ls_intercept):.2e}")
    print(f"    MLE of sigma = RMS residual = {sigma_mle:.4f}")
    print("       TWO DIFFERENT DERIVATIONS, ONE ANSWER. Minimising squared")
    print("       error and maximising likelihood are the same thing when the")
    print("       errors are normal -- which is why least squares is not an")
    print("       arbitrary choice but a consequence of an assumption")


def mle_for_a_normal_mean_and_variance():
    """The other standard derivation: mu-hat is the sample mean."""
    rng = np.random.default_rng(0)
    sample = rng.normal(50, 8, 500)

    mu_hat = sample.mean()
    sigma_hat = np.sqrt(((sample - mu_hat) ** 2).mean())    # divides by n
    sigma_unbiased = sample.std(ddof=1)                     # divides by n-1

    assert abs(mu_hat - 50) < 1.0
    assert sigma_hat < sigma_unbiased, "the MLE of sigma is BIASED downward"
    ratio = sigma_unbiased / sigma_hat
    assert abs(ratio - np.sqrt(500 / 499)) < 1e-12

    print(f"  500 draws from Normal(50, 8):")
    print(f"    mu-hat    (MLE)          {mu_hat:.4f}   = the sample mean")
    print(f"    sigma-hat (MLE, /n)      {sigma_hat:.4f}")
    print(f"    sigma     (unbiased, /n-1) {sigma_unbiased:.4f}")
    print(f"    ratio = sqrt(n/(n-1)) = {ratio:.6f}")
    print("       the MLE of the mean is the sample mean, but the MLE of the")
    print("       VARIANCE divides by n and is biased low. Course 4 divided by")
    print("       n-1 for exactly this reason -- MLE is not automatically")
    print("       unbiased, and knowing that is worth a mark")


def main():
    print("Experiment 5 -- Maximum likelihood estimation")
    coin_mle_by_grid_and_by_calculus()
    why_take_logs()
    least_squares_is_the_mle_under_normal_errors()
    mle_for_a_normal_mean_and_variance()


if __name__ == "__main__":
    main()
