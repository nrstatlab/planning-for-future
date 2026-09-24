# -*- coding: utf-8 -*-
"""The CSIR NET map data. Every destination is checked to exist before use."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

SM  = "statistics-major/"
UGC = "ugc-net-statistics/"
DS  = "data-science-major/"

def P(*a): return a   # (path, short label)

# ---- UNIT 1: Analysis and Linear Algebra ----
UNIT1 = [
 ("Elementary set theory, finite, countable and uncountable sets; real number system as a "
  "complete ordered field, Archimedean property, supremum, infimum",
  [P(UGC+"unit2.html", "UGC NET Unit II §1")], "brief"),
 ("Sequences and series, convergence, limsup, liminf; Bolzano&ndash;Weierstrass, Heine&ndash;Borel",
  [P(UGC+"unit2.html", "UGC NET Unit II §2&ndash;3")], "brief"),
 ("Continuity, uniform continuity, differentiability, mean value theorem",
  [P(UGC+"unit2.html", "UGC NET Unit II §5&ndash;6")], "brief"),
 ("Sequences and series of functions, uniform convergence", [], "missing"),
 ("Riemann sums and Riemann integral, improper integrals",
  [P(UGC+"unit2.html", "UGC NET Unit II §7")], "brief"),
 ("Monotonic functions, types of discontinuity",
  [P(UGC+"unit2.html", "UGC NET Unit II §5")], "brief"),
 ("Functions of bounded variation", [], "missing"),
 ("Lebesgue measure, Lebesgue integral", [], "missing"),
 ("Functions of several variables, directional derivative, partial derivative, derivative as a "
  "linear transformation, inverse and implicit function theorems",
  [P(UGC+"unit2.html", "UGC NET Unit II §8 (partial)")], "brief"),
 ("Metric spaces, compactness, connectedness, normed linear spaces, spaces of continuous functions",
  [], "missing"),
 ("Vector spaces, subspaces, linear dependence, basis, dimension, algebra of linear transformations",
  [], "missing"),
 ("Algebra of matrices, rank and determinant of matrices, linear equations",
  [P(UGC+"unit2.html", "UGC NET Unit II §10&ndash;12")], "deep"),
 ("Eigenvalues and eigenvectors, Cayley&ndash;Hamilton theorem",
  [P(UGC+"unit2.html", "UGC NET Unit II §14&ndash;15")], "deep"),
 ("Matrix representation of linear transformations, change of basis, canonical forms, diagonal "
  "forms, triangular forms, Jordan forms", [], "missing"),
 ("Inner product spaces, orthonormal basis",
  [P(UGC+"unit2.html", "UGC NET Unit II §13 (Gram&ndash;Schmidt)")], "brief"),
 ("Quadratic forms, reduction and classification of quadratic forms",
  [P(UGC+"unit2.html", "UGC NET Unit II §17")], "deep"),
]

# ---- UNIT 4: Statistics ----
UNIT4 = [
 ("Descriptive statistics, exploratory data analysis",
  [P(SM+"descriptive statistics/index_descriptive statistics.html", "Descriptive Statistics (5 units)"),
   P(SM+"computational statistics and r programming/unit2_computational statistics and r programming.html", "Descriptive Statistics in R")], "deep"),
 ("Sample space, discrete probability, independent events, Bayes theorem",
  [P(SM+"theory of probability/unit1_theory of probability.html", "Theory of Probability Unit 1"),
   P(UGC+"unit1.html", "UGC NET Unit I")], "deep"),
 ("Random variables and distribution functions (univariate and multivariate); expectation and moments",
  [P(SM+"theory of probability/unit2_theory of probability.html", "Theory of Probability Unit 2"),
   P(SM+"theory of probability/unit4_theory of probability.html", "Mathematical Expectation")], "deep"),
 ("Independent random variables, marginal and conditional distributions",
  [P(SM+"theory of probability/unit3_theory of probability.html", "Bivariate Random Variables")], "deep"),
 ("Characteristic functions",
  [P(SM+"theory of probability/unit5_theory of probability.html", "Generating Functions, LLN &amp; CLT")], "brief"),
 ("Probability inequalities (Tchebyshef, Markov, Jensen)",
  [P(SM+"theory of probability/unit4_theory of probability.html", "Mathematical Expectation")], "brief"),
 ("Modes of convergence, weak and strong laws of large numbers, Central Limit theorems (i.i.d. case)",
  [P(SM+"theory of probability/unit5_theory of probability.html", "Generating Functions, LLN &amp; CLT")], "brief"),
 ("Markov chains with finite and countable state space, classification of states, limiting "
  "behaviour of n-step transition probabilities, stationary distribution, Poisson and "
  "birth-and-death processes",
  [P(UGC+"unit9.html", "UGC NET Unit IX &mdash; Stochastic Processes")], "brief"),
 ("Standard discrete and continuous univariate distributions",
  [P(SM+"theoretical discrete distributions/index_theoretical discrete distributions.html", "Discrete Distributions (5 units)"),
   P(SM+"theoretical continuous distributions/index_theoretical continuous distributions.html", "Continuous Distributions (5 units)")], "deep"),
 ("Sampling distributions, standard errors and asymptotic distributions",
  [P(SM+"theoretical continuous distributions/unit5_theoretical continuous distributions.html", "Standard Normal &amp; Sampling Distributions")], "deep"),
 ("Distribution of order statistics and range",
  [P(UGC+"unit4.html", "UGC NET Unit IV")], "brief"),
 ("Methods of estimation, properties of estimators, confidence intervals",
  [P(SM+"inferential statistics/unit1_inferential statistics.html", "Inferential Statistics Unit 1")], "deep"),
 ("Tests of hypotheses: most powerful and uniformly most powerful tests, likelihood ratio tests",
  [P(SM+"inferential statistics/unit2_inferential statistics.html", "Inferential Statistics Unit 2")], "deep"),
 ("Analysis of discrete data and chi-square test of goodness of fit",
  [P(SM+"inferential statistics/unit4_inferential statistics.html", "Inferential Statistics Unit 4")], "deep"),
 ("Large sample tests",
  [P(SM+"inferential statistics/unit3_inferential statistics.html", "Inferential Statistics Unit 3")], "deep"),
 ("Simple nonparametric tests for one and two sample problems, rank correlation and test for independence",
  [P(SM+"inferential statistics/unit5_inferential statistics.html", "Inferential Statistics Unit 5"),
   P("which-statistical-test.html", "Which Statistical Test to Use")], "deep"),
 ("Elementary Bayesian inference", [], "missing"),
 ("Gauss&ndash;Markov models, estimability of parameters, best linear unbiased estimators, "
  "confidence intervals, tests for linear hypotheses",
  [P(SM+"econometrics/unit2_econometrics.html", "Econometrics Unit 2 &mdash; Models and Estimation"),
   P(UGC+"unit6.html", "UGC NET Unit VI")], "deep"),
 ("Analysis of variance and covariance",
  [P(SM+"design and analysis of experiments/unit1_design and analysis of experiments.html", "Design of Experiments Unit 1 &mdash; ANOVA")], "deep"),
 ("Fixed, random and mixed effects models",
  [P(UGC+"unit3.html", "UGC NET Unit III")], "brief"),
 ("Simple and multiple linear regression, elementary regression diagnostics",
  [P(SM+"econometrics/index_econometrics.html", "Econometrics (5 units)"),
   P(SM+"statistical methods/unit3_statistical methods.html", "Multiple &amp; Partial Correlation")], "deep"),
 ("Logistic regression",
  [P(UGC+"unit6.html", "UGC NET Unit VI"),
   P(DS+"machine-learning/self-study-notes/unit1-classification.html", "Machine Learning &mdash; Classification")], "brief"),
 ("Multivariate normal distribution, Wishart distribution and their properties; distribution of quadratic forms",
  [P(UGC+"unit8.html", "UGC NET Unit VIII &mdash; Multivariate Analysis")], "brief"),
 ("Inference for parameters, partial and multiple correlation coefficients and related tests",
  [P(SM+"statistical methods/unit3_statistical methods.html", "Concurrent Deviation, Multiple &amp; Partial Correlation")], "deep"),
 ("Data reduction: principal component analysis, discriminant analysis, cluster analysis, canonical correlation",
  [P(UGC+"unit8.html", "UGC NET Unit VIII"),
   P(DS+"machine-learning/self-study-notes/unit2-clustering.html", "Machine Learning &mdash; Clustering")], "brief"),
 ("Simple random sampling, stratified sampling and systematic sampling",
  [P(SM+"sampling techniques/index_sampling techniques.html", "Sampling Techniques (5 units)")], "deep"),
 ("Probability proportional to size sampling",
  [P(SM+"sampling techniques/index_sampling techniques.html", "Sampling Techniques"),
   P(UGC+"unit3.html", "UGC NET Unit III")], "brief"),
 ("Ratio and regression methods",
  [P(SM+"sampling techniques/index_sampling techniques.html", "Sampling Techniques"),
   P(UGC+"unit3.html", "UGC NET Unit III")], "brief"),
 ("Completely randomized designs, randomized block designs and Latin-square designs",
  [P(SM+"design and analysis of experiments/index_design and analysis of experiments.html", "Design of Experiments (5 units)")], "deep"),
 ("Connectedness and orthogonality of block designs, BIBD",
  [P(UGC+"unit3.html", "UGC NET Unit III")], "brief"),
 ("2&#7503; factorial experiments: confounding and construction",
  [P(SM+"design and analysis of experiments/index_design and analysis of experiments.html", "Design of Experiments"),
   P(UGC+"unit3.html", "UGC NET Unit III")], "brief"),
 ("Hazard function and failure rates, censoring and life testing",
  [P(SM+"statistical analysis of clinical trials/unit4.html", "Clinical Trials Unit 4")], "brief"),
 ("Series and parallel systems", [], "missing"),
 ("Linear programming problem, simplex methods, duality",
  [P(SM+"operations research/index_operations research.html", "Operations Research (5 units)")], "deep"),
 ("Elementary queuing and inventory models", [], "missing"),
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
