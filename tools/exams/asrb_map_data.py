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
        (0, 1, "../../statistics/msc/probability-theory/unit1.html", "deep"),
        (1, 5, "../../statistics/bsc/theory-of-probability/unit1.html", "deep"),
        (5, 9, ["../../statistics/bsc/theory-of-probability/unit4.html",
                "../../statistics/msc/probability-theory/unit2.html"], "deep"),
        (9, 15, ["../../statistics/bsc/theory-of-probability/unit2.html",
                 "../../statistics/bsc/theory-of-probability/unit3.html"], "deep"),
        (15, 17, "../../statistics/msc/probability-theory/unit2.html", "deep"),
        (17, 21, "../../statistics/msc/probability-theory/unit4.html", "deep"),
        (21, 22, "../../statistics/bsc/theoretical-discrete-distributions/index.html", "deep"),
        (22, 24, ["../../statistics/bsc/theoretical-continuous-distributions/index.html",
                  "../../statistics/msc/multivariate-analysis/unit1.html"], "deep"),
        (24, 27, "../../statistics/msc/distribution-theory/unit2.html", "deep"),
        (27, 30, "../../statistics/msc/distribution-theory/unit3.html", "deep"),
        (30, 31, None, "missing"),
        (31, 33, ["../../statistics/bsc/statistical-methods/unit2.html",
                  "../../statistics/bsc/statistical-methods/unit3.html"], "deep"),
        (33, 37, "../../statistics/msc/distribution-theory/unit4.html", "deep"),
    ]),
    (2, "Statistical Inference", [
        (0, 5, "../../statistics/msc/estimation-theory/unit1.html", "deep"),
        (5, 6, "../../statistics/bsc/inferential-statistics/unit1.html", "deep"),
        (6, 7, "../../statistics/msc/estimation-theory/unit3.html", "deep"),
        (7, 11, ["../../statistics/msc/testing-of-hypotheses/unit1.html",
                 "../../statistics/msc/testing-of-hypotheses/unit2.html"], "deep"),
        # Tests about a proportion and about a correlation coefficient are in the
        # large-sample unit, not the small-sample one; the regression coefficient
        # is in Statistical Methods. Pointing this row at unit4 alone was wrong,
        # and the deep-grade check caught it.
        (11, 12, ["../../statistics/bsc/inferential-statistics/unit3.html",
                  "../../statistics/bsc/inferential-statistics/unit4.html",
                  "../../statistics/bsc/statistical-methods/unit4.html"], "deep"),
        (12, 14, None, "missing"),
        (14, 15, "../../statistics/msc/testing-of-hypotheses/unit3.html", "deep"),
        (15, 16, "../../statistics/bsc/inferential-statistics/unit4.html", "deep"),
        (16, 17, "../../statistics/bsc/inferential-statistics/unit5.html", "deep"),
        (17, 19, "../../statistics/msc/testing-of-hypotheses/unit4.html", "deep"),
    ]),
    (3, "Multivariate Analysis", [
        (0, 5, "../../statistics/msc/multivariate-analysis/unit1.html", "deep"),
        (5, 7, "../../statistics/msc/multivariate-analysis/unit2.html", "deep"),
        (7, 12, "../../statistics/msc/multivariate-analysis/unit3.html", "deep"),
        (12, 15, "../../statistics/msc/multivariate-analysis/unit4.html", "deep"),
        (15, 16, "../../statistics/msc/multivariate-analysis/unit4.html", "deep"),
        (16, 18, "../../statistics/msc/multivariate-analysis/practical.html", "brief"),
        (18, 19, "../../statistics/msc/multivariate-analysis/unit4.html", "deep"),
    ]),
    (4, "Design of Experiments", [
        (0, 2, "../../statistics/msc/linear-algebra-and-linear-models/unit4.html", "deep"),
        (2, 3, None, "missing"),
        (3, 5, "../../statistics/msc/design-and-analysis-of-experiments/unit1.html", "deep"),
        (5, 9, ["../../statistics/bsc/design-and-analysis-of-experiments/unit1.html",
                "../../statistics/msc/design-and-analysis-of-experiments/unit1.html"], "deep"),
        (9, 11, ["../../statistics/bsc/design-and-analysis-of-experiments/unit2.html",
                 "../../statistics/bsc/design-and-analysis-of-experiments/unit5.html"], "deep"),
        (11, 13, None, "missing"),
        (13, 15, "../../statistics/msc/design-and-analysis-of-experiments/unit3.html", "deep"),
        (15, 16, "../../statistics/msc/design-and-analysis-of-experiments/unit4.html", "deep"),
        (16, 17, "../../statistics/bsc/statistical-analysis-of-clinical-trials/practical.html", "brief"),
        (17, 19, ["../../statistics/msc/design-and-analysis-of-experiments/unit2.html",
                  "../../statistics/msc/design-and-analysis-of-experiments/unit3.html"], "deep"),
        (19, 21, None, "missing"),
        (21, 22, "../../statistics/msc/design-and-analysis-of-experiments/index.html", "brief"),
        (22, 23, "../../statistics/msc/design-and-analysis-of-experiments/unit4.html", "deep"),
        (23, 24, "../../statistics/msc/design-and-analysis-of-experiments/unit1.html", "deep"),
        (24, 25, "../../statistics/bsc/sampling-techniques/unit1.html", "brief"),
    ]),
    (5, "Sample Surveys", [
        (0, 5, "../../statistics/bsc/sampling-techniques/unit1.html", "deep"),
        (5, 6, "../../statistics/bsc/sampling-techniques/unit2.html", "deep"),
        (6, 7, None, "missing"),
        (7, 9, "../../statistics/bsc/sampling-techniques/unit3.html", "deep"),
        (9, 11, "../../statistics/msc/sampling-theory/unit2.html", "deep"),
        (11, 12, "../../statistics/msc/sampling-theory/unit3.html", "deep"),
        (12, 15, ["../../statistics/bsc/sampling-techniques/unit4.html",
                  "../../statistics/msc/sampling-theory/unit4.html"], "deep"),
        (15, 18, "../../statistics/msc/sampling-theory/unit1.html", "deep"),
        (18, 20, "../../statistics/bsc/sampling-techniques/unit4.html", "deep"),
        (20, 23, "../../statistics/msc/sampling-theory/unit4.html", "deep"),
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
        (33, 34, "../../statistics/bsc/advanced-actuarial-statistics/unit1.html", "brief"),
    ]),
    (7, "Regression Analysis", [
        (0, 2, ["../../statistics/bsc/statistical-methods/unit4.html",
                "../../statistics/msc/linear-algebra-and-linear-models/unit4.html"], "deep"),
        (2, 4, "../../statistics/msc/design-and-analysis-of-experiments/index.html", "brief"),
        (4, 6, "../../statistics/bsc/econometrics/unit2.html", "brief"),
        (6, 7, None, "missing"),
        (7, 9, "../../data-science/machine-learning/unit2.html", "brief"),
        (9, 10, ["../../statistics/bsc/econometrics/unit3.html",
                 "../../statistics/bsc/econometrics/unit4.html",
                 "../../statistics/bsc/econometrics/unit5.html"], "deep"),
        (10, 11, "../../statistics/bsc/econometrics/unit3.html", "deep"),
        (11, 13, "../../statistics/bsc/applied-statistics/unit1.html", "deep"),
        (13, 17, "../../data-science/time-series/unit1.html", "deep"),
        (17, 20, ["../../data-science/time-series/unit2.html",
                  "../../data-science/time-series/unit3.html"], "deep"),
        (20, 22, "../../statistics/bsc/econometrics/unit2.html", "brief"),
        (22, 25, "../../statistics/bsc/applied-statistics-ii/unit3.html", "deep"),
        (25, 26, None, "missing"),
    ]),
    (8, "Mathematical Methods in Statistics and Optimization Techniques", [
        (0, 3, "../../statistics/msc/mathematical-analysis/unit1.html", "deep"),
        (3, 5, None, "missing"),
        (5, 8, "../../statistics/bsc/computational-statistics-and-r-programming/unit2.html", "brief"),
        (8, 9, None, "missing"),
        (9, 10, "../../statistics/msc/linear-algebra-and-linear-models/unit1.html", "deep"),
        (10, 13, "../../statistics/msc/linear-algebra-and-linear-models/unit1.html", "brief"),
        (13, 14, "../../statistics/msc/distribution-theory/unit3.html", "brief"),
        (14, 16, "../../statistics/msc/linear-algebra-and-linear-models/unit2.html", "deep"),
        (16, 17, None, "missing"),
        (17, 20, "../../statistics/msc/linear-algebra-and-linear-models/unit1.html", "deep"),
        (20, 22, ["../../statistics/msc/linear-algebra-and-linear-models/unit2.html",
                  "../../statistics/msc/linear-algebra-and-linear-models/unit3.html"], "deep"),
        (22, 27, "../../statistics/bsc/operations-research/unit1.html", "brief"),
        (27, 29, ["../../statistics/bsc/operations-research/unit3.html",
                  "../../statistics/bsc/operations-research/unit5.html",
                  "../../statistics/bsc/optimization-techniques/unit4.html"], "deep"),
        (29, 32, None, "missing"),
        (32, 35, None, "missing"),
        (35, 36, "../../data-science/artificial-intelligence/unit3.html", "brief"),
        (36, 37, None, "missing"),
        (37, 39, ["../../data-science/machine-learning/unit4.html",
                  "../../data-science/deep-learning/unit1.html"], "deep"),
        (39, 40, None, "missing"),
        (40, 42, "../../statistics/bsc/computational-statistics-and-r-programming/unit5.html", "brief"),
        (42, 43, "../../statistics/msc/estimation-theory/unit2.html", "deep"),
        (43, 44, "../../statistics/bsc/computational-statistics-and-r-programming/unit5.html", "brief"),
    ]),
]
