# -*- coding: utf-8 -*-
"""The CSIR NET map data. Every destination is checked to exist before use."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

SM  = "statistics/"
UGC = "exams/ugc-net/"
DS  = "data-science/"

def P(*a): return a   # (path, short label)

# ---- UNIT 1: Analysis and Linear Algebra ----
UNIT1 = [
 ("Elementary set theory, finite, countable and uncountable sets; real number system as a "
  "complete ordered field, Archimedean property, supremum, infimum",
  [P(UGC+"unit2.html", "UGC NET Unit II §1")], "brief"),
 ("Sequences and series, convergence, limsup, liminf; Bolzano&ndash;Weierstrass, Heine&ndash;Borel",
  [P(SM+"mathematical-analysis/unit1.html", "Mathematical Analysis Unit 1 (Bolzano&ndash;Weierstrass, Heine&ndash;Borel)"),
   P(SM+"mathematical-analysis/unit4.html", "Mathematical Analysis Unit 4 (limsup, liminf, tests of convergence)"),
   P(UGC+"unit2.html", "UGC NET Unit II §2&ndash;3")], "deep"),
 ("Continuity, uniform continuity, differentiability, mean value theorem",
  [P(SM+"mathematical-analysis/unit1.html", "Mathematical Analysis Unit 1 (continuity, differentiation)"),
   P(UGC+"unit2.html", "UGC NET Unit II §5&ndash;6")], "deep"),
 ("Sequences and series of functions, uniform convergence",
  [P(SM+"mathematical-analysis/unit4.html", "Mathematical Analysis Unit 4")], "deep"),
 ("Riemann sums and Riemann integral, improper integrals",
  [P(UGC+"unit2.html", "UGC NET Unit II §7")], "brief"),
 ("Monotonic functions, types of discontinuity",
  [P(UGC+"unit2.html", "UGC NET Unit II §5")], "brief"),
 ("Functions of bounded variation",
  [P(SM+"mathematical-analysis/unit3.html", "Mathematical Analysis Unit 3")], "deep"),
 ("Lebesgue measure, Lebesgue integral",
  [P(SM+"probability-theory/unit1.html", "Probability Theory Unit 1 &mdash; Measure Theory"),
   P(SM+"probability-theory/unit2.html", "Probability Theory Unit 2")], "brief"),
 ("Functions of several variables, directional derivative, partial derivative, derivative as a "
  "linear transformation, inverse and implicit function theorems",
  [P(UGC+"unit2.html", "UGC NET Unit II §8 (partial)")], "brief"),
 ("Metric spaces, compactness, connectedness, normed linear spaces, spaces of continuous functions",
  [P(SM+"mathematical-analysis/unit1.html", "Mathematical Analysis Unit 1"),
   P(SM+"mathematical-analysis/unit4.html", "Mathematical Analysis Unit 4 (Stone&ndash;Weierstrass)")], "brief"),
 ("Vector spaces, subspaces, linear dependence, basis, dimension, algebra of linear transformations",
  [P(UGC+"unit2.html", "UGC NET Unit II §9"),
   P(SM+"linear-algebra-and-linear-models/unit1.html", "Linear Algebra and Linear Models Unit 1")], "brief"),
 ("Algebra of matrices, rank and determinant of matrices, linear equations",
  [P(SM+"linear-algebra-and-linear-models/unit1.html", "Linear Algebra and Linear Models Unit 1"),
   P(UGC+"unit2.html", "UGC NET Unit II §10&ndash;12")], "deep"),
 ("Eigenvalues and eigenvectors, Cayley&ndash;Hamilton theorem",
  [P(SM+"linear-algebra-and-linear-models/unit2.html", "Linear Algebra and Linear Models Unit 2"),
   P(UGC+"unit2.html", "UGC NET Unit II §14&ndash;15")], "deep"),
 ("Matrix representation of linear transformations, change of basis, canonical forms, diagonal "
  "forms, triangular forms, Jordan forms",
  [P(SM+"linear-algebra-and-linear-models/unit2.html", "Linear Algebra and Linear Models Unit 2 (diagonal forms only; no Jordan form)")], "brief"),
 ("Inner product spaces, orthonormal basis",
  [P(UGC+"unit2.html", "UGC NET Unit II §13 (Gram&ndash;Schmidt)")], "brief"),
 ("Quadratic forms, reduction and classification of quadratic forms",
  [P(SM+"linear-algebra-and-linear-models/unit3.html", "Linear Algebra and Linear Models Unit 3"),
   P(UGC+"unit2.html", "UGC NET Unit II §17")], "deep"),
]

# ---- UNIT 4: Statistics ----
UNIT4 = [
 ("Descriptive statistics, exploratory data analysis",
  [P(SM+"descriptive-statistics/index.html", "Descriptive Statistics (5 units)"),
   P(SM+"computational-statistics-and-r-programming/unit2.html", "Descriptive Statistics in R")], "deep"),
 ("Sample space, discrete probability, independent events, Bayes theorem",
  [P(SM+"theory-of-probability/unit1.html", "Theory of Probability Unit 1"),
   P(UGC+"unit1.html", "UGC NET Unit I")], "deep"),
 ("Random variables and distribution functions (univariate and multivariate); expectation and moments",
  [P(SM+"theory-of-probability/unit2.html", "Theory of Probability Unit 2"),
   P(SM+"theory-of-probability/unit4.html", "Mathematical Expectation")], "deep"),
 ("Independent random variables, marginal and conditional distributions",
  [P(SM+"theory-of-probability/unit3.html", "Bivariate Random Variables")], "deep"),
 ("Characteristic functions",
  [P(SM+"probability-theory/unit2.html", "Probability Theory Unit 2 &mdash; the Characteristic Function"),
   P(SM+"theory-of-probability/unit5.html", "Generating Functions, LLN &amp; CLT")], "deep"),
 ("Probability inequalities (Tchebyshef, Markov, Jensen)",
  [P(SM+"theory-of-probability/unit4.html", "Mathematical Expectation (Markov, Chebyshev)"),
   P(SM+"probability-theory/unit2.html", "Probability Theory Unit 2 &mdash; Probability and Moment Inequalities")], "deep"),
 ("Modes of convergence, weak and strong laws of large numbers, Central Limit theorems (i.i.d. case)",
  [P(SM+"probability-theory/unit3.html", "Probability Theory Unit 3 &mdash; Modes of Convergence"),
   P(SM+"probability-theory/unit4.html", "Probability Theory Unit 4 &mdash; Laws of Large Numbers and CLT"),
   P(SM+"theory-of-probability/unit5.html", "Generating Functions, LLN &amp; CLT")], "deep"),
 ("Markov chains with finite and countable state space, classification of states, limiting "
  "behaviour of n-step transition probabilities, stationary distribution, Poisson and "
  "birth-and-death processes",
  [P(UGC+"unit9.html", "UGC NET Unit IX &mdash; Stochastic Processes")], "brief"),
 ("Standard discrete and continuous univariate distributions",
  [P(SM+"theoretical-discrete-distributions/index.html", "Discrete Distributions (5 units)"),
   P(SM+"theoretical-continuous-distributions/index.html", "Continuous Distributions (5 units)")], "deep"),
 ("Sampling distributions, standard errors and asymptotic distributions",
  [P(SM+"theoretical-continuous-distributions/unit5.html", "Standard Normal &amp; Sampling Distributions")], "deep"),
 ("Distribution of order statistics and range",
  [P(SM+"distribution-theory/unit4.html", "Distribution Theory Unit 4 &mdash; Order Statistics and the Sample Range"),
   P(UGC+"unit4.html", "UGC NET Unit IV")], "deep"),
 ("Methods of estimation, properties of estimators, confidence intervals",
  [P(SM+"inferential-statistics/unit1.html", "Inferential Statistics Unit 1")], "deep"),
 ("Tests of hypotheses: most powerful and uniformly most powerful tests, likelihood ratio tests",
  [P(SM+"inferential-statistics/unit2.html", "Inferential Statistics Unit 2"),
   P(SM+"testing-of-hypotheses/unit2.html", "Testing of Hypotheses Unit 2 &mdash; UMP Tests"),
   P(SM+"testing-of-hypotheses/unit3.html", "Testing of Hypotheses Unit 3 &mdash; Likelihood Ratio Tests")], "deep"),
 ("Analysis of discrete data and chi-square test of goodness of fit",
  [P(SM+"inferential-statistics/unit4.html", "Inferential Statistics Unit 4")], "deep"),
 ("Large sample tests",
  [P(SM+"inferential-statistics/unit3.html", "Inferential Statistics Unit 3")], "deep"),
 ("Simple nonparametric tests for one and two sample problems, rank correlation and test for independence",
  [P(SM+"inferential-statistics/unit5.html", "Inferential Statistics Unit 5"),
   P("guides/which-test.html", "Which Statistical Test to Use")], "deep"),
 ("Elementary Bayesian inference",
  [P(SM+"estimation-theory/unit4.html", "Estimation Theory Unit 4 &mdash; Bayes Estimation")], "brief"),
 ("Gauss&ndash;Markov models, estimability of parameters, best linear unbiased estimators, "
  "confidence intervals, tests for linear hypotheses",
  [P(SM+"linear-algebra-and-linear-models/unit4.html", "Linear Models Unit 4 &mdash; Estimability and Gauss&ndash;Markov"),
   P(SM+"econometrics/unit2.html", "Econometrics Unit 2 &mdash; Models and Estimation"),
   P(UGC+"unit6.html", "UGC NET Unit VI")], "deep"),
 ("Analysis of variance and covariance",
  [P(SM+"design-and-analysis-of-experiments/unit1.html", "Design of Experiments Unit 1 &mdash; ANOVA")], "deep"),
 ("Fixed, random and mixed effects models",
  [P(UGC+"unit3.html", "UGC NET Unit III")], "brief"),
 ("Simple and multiple linear regression, elementary regression diagnostics",
  [P(SM+"econometrics/index.html", "Econometrics (5 units)"),
   P(SM+"statistical-methods/unit3.html", "Multiple &amp; Partial Correlation")], "deep"),
 ("Logistic regression",
  [P(UGC+"unit6.html", "UGC NET Unit VI"),
   P(DS+"machine-learning/self-study-notes/unit1-classification.html", "Machine Learning &mdash; Classification")], "brief"),
 ("Multivariate normal distribution, Wishart distribution and their properties; distribution of quadratic forms",
  [P(SM+"multivariate-analysis/unit1.html", "Multivariate Analysis Unit 1 &mdash; Multivariate Normal"),
   P(SM+"multivariate-analysis/unit2.html", "Multivariate Analysis Unit 2 &mdash; Wishart Distribution"),
   P(SM+"distribution-theory/unit4.html", "Distribution Theory Unit 4 &mdash; Quadratic Forms"),
   P(UGC+"unit8.html", "UGC NET Unit VIII &mdash; Multivariate Analysis")], "deep"),
 ("Inference for parameters, partial and multiple correlation coefficients and related tests",
  [P(SM+"multivariate-analysis/unit2.html", "Multivariate Analysis Unit 2 &mdash; Multiple and Partial Correlation"),
   P(SM+"statistical-methods/unit3.html", "Concurrent Deviation, Multiple &amp; Partial Correlation")], "deep"),
 ("Data reduction: principal component analysis, discriminant analysis, cluster analysis, canonical correlation",
  [P(SM+"multivariate-analysis/unit4.html", "Multivariate Analysis Unit 4 &mdash; PCA, Canonical Correlation, Clusters"),
   P(SM+"multivariate-analysis/unit3.html", "Multivariate Analysis Unit 3 &mdash; Discriminant Analysis"),
   P(UGC+"unit8.html", "UGC NET Unit VIII"),
   P(DS+"machine-learning/self-study-notes/unit2-clustering.html", "Machine Learning &mdash; Clustering")], "deep"),
 ("Simple random sampling, stratified sampling and systematic sampling",
  [P(SM+"sampling-techniques/index.html", "Sampling Techniques (5 units)")], "deep"),
 ("Probability proportional to size sampling",
  [P(SM+"sampling-techniques/unit4.html", "Sampling Techniques Unit 4 &mdash; PPS Sampling"),
   P(SM+"sampling-theory/unit1.html", "Sampling Theory Unit 1 &mdash; Hansen&ndash;Hurwitz and Horvitz&ndash;Thompson"),
   P(UGC+"unit3.html", "UGC NET Unit III")], "deep"),
 ("Ratio and regression methods",
  [P(SM+"sampling-theory/unit2.html", "Sampling Theory Unit 2 &mdash; Ratio and Regression Estimators"),
   P(SM+"sampling-techniques/index.html", "Sampling Techniques"),
   P(UGC+"unit3.html", "UGC NET Unit III")], "deep"),
 ("Completely randomized designs, randomized block designs and Latin-square designs",
  [P(SM+"design-and-analysis-of-experiments/index.html", "Design of Experiments (5 units)")], "deep"),
 ("Connectedness and orthogonality of block designs, BIBD",
  [P(SM+"design-and-analysis-of-experiments-advanced/unit3.html", "Design of Experiments (advanced) Unit 3 &mdash; BIBD"),
   P(SM+"design-and-analysis-of-experiments-advanced/unit4.html", "Design of Experiments (advanced) Unit 4 &mdash; PBIBD"),
   P(UGC+"unit3.html", "UGC NET Unit III")], "brief"),
 ("2&#7503; factorial experiments: confounding and construction",
  [P(SM+"design-and-analysis-of-experiments-advanced/unit2.html", "Design of Experiments (advanced) Unit 2 &mdash; 2&#7503; Factorials"),
   P(SM+"design-and-analysis-of-experiments-advanced/unit3.html", "Design of Experiments (advanced) Unit 3 &mdash; Confounding"),
   P(UGC+"unit3.html", "UGC NET Unit III")], "deep"),
 ("Hazard function and failure rates, censoring and life testing",
  [P(SM+"statistical-analysis-of-clinical-trials/unit4.html", "Clinical Trials Unit 4")], "brief"),
 ("Series and parallel systems",
  [P(SM+"distribution-theory/unit4.html", "Distribution Theory Unit 4 &mdash; Applications of Order Statistics")], "brief"),
 ("Linear programming problem, simplex methods, duality",
  [P(SM+"operations-research/index.html", "Operations Research (5 units)")], "deep"),
 ("Elementary queuing and inventory models",
  [P(UGC+"unit9.html", "UGC NET Unit IX (queuing; inventory models not covered)")], "brief"),
 ("Steady-state solutions of Markovian queuing models: M/M/1, M/M/1 with limited waiting space, "
  "M/M/C, M/M/C with limited waiting space, M/G/1",
  [P(UGC+"unit9.html", "UGC NET Unit IX")], "brief"),
]

def check():
    bad = []
    for name, rows in (("Unit 1", UNIT1), ("Unit 4", UNIT4)):
        for text, dests, grade in rows:
            for path, label in dests:
                if not (ROOT / path).is_file():
                    bad.append(f"{name}: {path}")
            if grade == "missing" and dests:
                bad.append(f"{name}: graded missing but has destinations -- {text[:40]}")
            if grade != "missing" and not dests:
                bad.append(f"{name}: graded {grade} but has no destination -- {text[:40]}")
    return bad

if __name__ == "__main__":
    bad = check()
    if bad:
        print("FAILURES:"); [print("  ", b) for b in bad]; sys.exit(1)
    for n, rows in (("Unit 1", UNIT1), ("Unit 4", UNIT4)):
        g = {}
        for _, _, grade in rows: g[grade] = g.get(grade, 0) + 1
        print(f"{n}: {len(rows)} lines  {g}")
    print("all destinations exist")
