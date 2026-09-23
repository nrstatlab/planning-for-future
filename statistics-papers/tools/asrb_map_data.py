# -*- coding: utf-8 -*-
"""Which page on this site teaches each line of the Agricultural Statistics syllabus.

THE SYLLABUS TEXT IS NOT STORED HERE. Each row names a half-open range of
semicolon-separated items in asrb_syllabus.txt, and asrb_map.py joins that
slice to make the line it prints. So the wording on the finished page is the
document's own wording by construction -- it cannot drift from the source,
because it is never retyped. recheck_asrb.py then proves the same thing from
the other direction, against the PDF.

Ranges are half-open and must be contiguous and in order within a unit;
asrb_map.py asserts both, so a row cannot silently skip an item.

GRADES. deep = a page here works the thing out; brief = it is covered at
exam-summary level; missing = nothing here teaches it. Every "deep" in this
file was checked against the destination page's actual text, not assumed from
its title -- an inflated grade was one of the findings in the go-live report,
and the whole value of a map like this is that its red rows are honest.
"""

# (start, end, destination(s) or None, grade)
UNITS = [
    (1, "Probability and Mathematical Statistics", [
        (0, 1, "../../statistics-major/msc/probability-theory/unit1.html", "deep"),
        (1, 5, "../../statistics-major/theory of probability/unit1_theory of probability.html", "deep"),
        (5, 9, ["../../statistics-major/theory of probability/unit4_theory of probability.html",
                "../../statistics-major/msc/probability-theory/unit2.html"], "deep"),
        (9, 15, ["../../statistics-major/theory of probability/unit2_theory of probability.html",
                 "../../statistics-major/theory of probability/unit3_theory of probability.html"], "deep"),
        (15, 17, "../../statistics-major/msc/probability-theory/unit2.html", "deep"),
        (17, 21, "../../statistics-major/msc/probability-theory/unit4.html", "deep"),
        (21, 22, "../../statistics-major/theoretical discrete distributions/index_theoretical discrete distributions.html", "deep"),
        (22, 24, ["../../statistics-major/theoretical continuous distributions/index_theoretical continuous distributions.html",
                  "../../statistics-major/msc/multivariate-analysis/unit1.html"], "deep"),
        (24, 27, "../../statistics-major/msc/distribution-theory/unit2.html", "deep"),
        (27, 30, "../../statistics-major/msc/distribution-theory/unit3.html", "deep"),
        (30, 31, None, "missing"),
        (31, 33, ["../../statistics-major/statistical methods/unit2_statistical methods.html",
                  "../../statistics-major/statistical methods/unit3_statistical methods.html"], "deep"),
        (33, 37, "../../statistics-major/msc/distribution-theory/unit4.html", "deep"),
    ]),
    (2, "Statistical Inference", [
        (0, 5, "../../statistics-major/msc/estimation-theory/unit1.html", "deep"),
        (5, 6, "../../statistics-major/inferential statistics/unit1_inferential statistics.html", "deep"),
        (6, 7, "../../statistics-major/msc/estimation-theory/unit3.html", "deep"),
        (7, 11, ["../../statistics-major/msc/testing-of-hypotheses/unit1.html",
                 "../../statistics-major/msc/testing-of-hypotheses/unit2.html"], "deep"),
        # Tests about a proportion and about a correlation coefficient are in the
        # large-sample unit, not the small-sample one; the regression coefficient
        # is in Statistical Methods. Pointing this row at unit4 alone was wrong,
        # and the deep-grade check caught it.
        (11, 12, ["../../statistics-major/inferential statistics/unit3_inferential statistics.html",
                  "../../statistics-major/inferential statistics/unit4_inferential statistics.html",
                  "../../statistics-major/statistical methods/unit4_statistical methods.html"], "deep"),
        (12, 14, None, "missing"),
        (14, 15, "../../statistics-major/msc/testing-of-hypotheses/unit3.html", "deep"),
        (15, 16, "../../statistics-major/inferential statistics/unit4_inferential statistics.html", "deep"),
        (16, 17, "../../statistics-major/inferential statistics/unit5_inferential statistics.html", "deep"),
        (17, 19, "../../statistics-major/msc/testing-of-hypotheses/unit4.html", "deep"),
    ]),
    (3, "Multivariate Analysis", [
        (0, 5, "../../statistics-major/msc/multivariate-analysis/unit1.html", "deep"),
        (5, 7, "../../statistics-major/msc/multivariate-analysis/unit2.html", "deep"),
        (7, 12, "../../statistics-major/msc/multivariate-analysis/unit3.html", "deep"),
        (12, 15, "../../statistics-major/msc/multivariate-analysis/unit4.html", "deep"),
        (15, 16, "../../statistics-major/msc/multivariate-analysis/unit4.html", "deep"),
        (16, 18, "../../statistics-major/msc/multivariate-analysis/practical.html", "brief"),
        (18, 19, "../../statistics-major/msc/multivariate-analysis/unit4.html", "deep"),
    ]),
    (4, "Design of Experiments", [
        (0, 2, "../../statistics-major/msc/linear-algebra-and-linear-models/unit4.html", "deep"),
        (2, 3, None, "missing"),
        (3, 5, "../../statistics-major/msc/design-and-analysis-of-experiments/unit1.html", "deep"),
        (5, 9, ["../../statistics-major/design and analysis of experiments/unit1_design and analysis of experiments.html",
                "../../statistics-major/msc/design-and-analysis-of-experiments/unit1.html"], "deep"),
        (9, 11, ["../../statistics-major/design and analysis of experiments/unit2_design and analysis of experiments.html",
                 "../../statistics-major/design and analysis of experiments/unit5_design and analysis of experiments.html"], "deep"),
        (11, 13, None, "missing"),
        (13, 15, "../../statistics-major/msc/design-and-analysis-of-experiments/unit3.html", "deep"),
        (15, 16, "../../statistics-major/msc/design-and-analysis-of-experiments/unit4.html", "deep"),
        (16, 17, "../../statistics-major/statistical analysis of clinical trials/practical.html", "brief"),
        (17, 19, ["../../statistics-major/msc/design-and-analysis-of-experiments/unit2.html",
                  "../../statistics-major/msc/design-and-analysis-of-experiments/unit3.html"], "deep"),
        (19, 21, None, "missing"),
        (21, 22, "../../statistics-major/msc/design-and-analysis-of-experiments/index.html", "brief"),
        (22, 23, "../../statistics-major/msc/design-and-analysis-of-experiments/unit4.html", "deep"),
        (23, 24, "../../statistics-major/msc/design-and-analysis-of-experiments/unit1.html", "deep"),
        (24, 25, "../../statistics-major/sampling techniques/unit1_sampling techniques.html", "brief"),
    ]),
    (5, "Sample Surveys", [
        (0, 5, "../../statistics-major/sampling techniques/unit1_sampling techniques.html", "deep"),
        (5, 6, "../../statistics-major/sampling techniques/unit2_sampling techniques.html", "deep"),
        (6, 7, None, "missing"),
        (7, 9, "../../statistics-major/sampling techniques/unit3_sampling techniques.html", "deep"),
        (9, 11, "../../statistics-major/msc/sampling-theory/unit2.html", "deep"),
        (11, 12, "../../statistics-major/msc/sampling-theory/unit3.html", "deep"),
        (12, 15, ["../../statistics-major/sampling techniques/unit4_sampling techniques.html",
                  "../../statistics-major/msc/sampling-theory/unit4.html"], "deep"),
        (15, 18, "../../statistics-major/msc/sampling-theory/unit1.html", "deep"),
        (18, 20, "../../statistics-major/sampling techniques/unit4_sampling techniques.html", "deep"),
        (20, 23, "../../statistics-major/msc/sampling-theory/unit4.html", "deep"),
    ]),
    (6, "Statistical Genetics", [
        (0, 4, None, "missing"),
        (4, 8, None, "missing"),
        (8, 13, None, "missing"),
        (13, 18, None, "missing"),
        (18, 22, None, "missing"),
        (22, 26, None, "missing"),
        (26, 30, None, "missing"),
        (30, 33, None, "missing"),
        (33, 34, "../../statistics-major/advanced actuarial statistics/unit1_advanced actuarial statistics.html", "brief"),
    ]),
    (7, "Regression Analysis", [
        (0, 2, ["../../statistics-major/statistical methods/unit4_statistical methods.html",
                "../../statistics-major/msc/linear-algebra-and-linear-models/unit4.html"], "deep"),
        (2, 4, "../../statistics-major/msc/design-and-analysis-of-experiments/index.html", "brief"),
        (4, 6, "../../statistics-major/econometrics/unit2_econometrics.html", "brief"),
        (6, 7, None, "missing"),
        (7, 9, "../../data-science-major/machine-learning/unit2_machine-learning.html", "brief"),
        (9, 10, ["../../statistics-major/econometrics/unit3_econometrics.html",
                 "../../statistics-major/econometrics/unit4_econometrics.html",
                 "../../statistics-major/econometrics/unit5_econometrics.html"], "deep"),
        (10, 11, "../../statistics-major/econometrics/unit3_econometrics.html", "deep"),
        (11, 13, "../../statistics-major/applied statistics/unit1_applied statistics.html", "deep"),
        (13, 17, "../../data-science-major/time-series/unit1_time-series.html", "deep"),
        (17, 20, ["../../data-science-major/time-series/unit2_time-series.html",
                  "../../data-science-major/time-series/unit3_time-series.html"], "deep"),
        (20, 22, "../../statistics-major/econometrics/unit2_econometrics.html", "brief"),
        (22, 25, "../../statistics-major/applied statistics ii/unit3_applied statistics ii.html", "deep"),
        (25, 26, None, "missing"),
    ]),
    (8, "Mathematical Methods in Statistics and Optimization Techniques", [
        (0, 3, "../../statistics-major/msc/mathematical-analysis/unit1.html", "deep"),
        (3, 5, None, "missing"),
        (5, 8, "../../statistics-major/computational statistics and r programming/unit2_computational statistics and r programming.html", "brief"),
        (8, 9, None, "missing"),
        (9, 10, "../../statistics-major/msc/linear-algebra-and-linear-models/unit1.html", "deep"),
        (10, 13, "../../statistics-major/msc/linear-algebra-and-linear-models/unit1.html", "brief"),
        (13, 14, "../../statistics-major/msc/distribution-theory/unit3.html", "brief"),
        (14, 16, "../../statistics-major/msc/linear-algebra-and-linear-models/unit2.html", "deep"),
        (16, 17, None, "missing"),
        (17, 20, "../../statistics-major/msc/linear-algebra-and-linear-models/unit1.html", "deep"),
        (20, 22, ["../../statistics-major/msc/linear-algebra-and-linear-models/unit2.html",
                  "../../statistics-major/msc/linear-algebra-and-linear-models/unit3.html"], "deep"),
        (22, 27, "../../statistics-major/operations research/unit1_operations research.html", "brief"),
        (27, 29, ["../../statistics-major/operations research/unit3_operations research.html",
                  "../../statistics-major/operations research/unit5_operations research.html",
                  "../../statistics-major/optimization techniques/unit4_optimization techniques.html"], "deep"),
        (29, 32, None, "missing"),
        (32, 35, None, "missing"),
        (35, 36, "../../data-science-major/artificial-intelligence/unit3_artificial-intelligence.html", "brief"),
        (36, 37, None, "missing"),
        (37, 39, ["../../data-science-major/machine-learning/unit4_machine-learning.html",
                  "../../data-science-major/deep-learning/unit1_deep-learning.html"], "deep"),
        (39, 40, None, "missing"),
        (40, 42, "../../statistics-major/computational statistics and r programming/unit5_computational statistics and r programming.html", "brief"),
        (42, 43, "../../statistics-major/msc/estimation-theory/unit2.html", "deep"),
        (43, 44, "../../statistics-major/computational statistics and r programming/unit5_computational statistics and r programming.html", "brief"),
    ]),
]
