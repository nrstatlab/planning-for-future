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
        (0, 1, "../../statistics/probability-theory/unit1.html", "deep"),
        (1, 5, "../../statistics/theory-of-probability/unit1.html", "deep"),
        (5, 9, ["../../statistics/theory-of-probability/unit4.html",
                "../../statistics/probability-theory/unit2.html"], "deep"),
        (9, 15, ["../../statistics/theory-of-probability/unit2.html",
                 "../../statistics/theory-of-probability/unit3.html"], "deep"),
        (15, 17, "../../statistics/probability-theory/unit2.html", "deep"),
        (17, 21, "../../statistics/probability-theory/unit4.html", "deep"),
        (21, 22, "../../statistics/theoretical-discrete-distributions/index.html", "deep"),
        (22, 24, ["../../statistics/theoretical-continuous-distributions/index.html",
                  "../../statistics/multivariate-analysis/unit1.html"], "deep"),
        (24, 27, "../../statistics/distribution-theory/unit2.html", "deep"),
        (27, 30, "../../statistics/distribution-theory/unit3.html", "deep"),
        (30, 31, None, "missing"),
        (31, 33, ["../../statistics/statistical-methods/unit2.html",
                  "../../statistics/statistical-methods/unit3.html"], "deep"),
        (33, 37, "../../statistics/distribution-theory/unit4.html", "deep"),
    ]),
    (2, "Statistical Inference", [
        (0, 5, "../../statistics/estimation-theory/unit1.html", "deep"),
        (5, 6, "../../statistics/inferential-statistics/unit1.html", "deep"),
        (6, 7, "../../statistics/estimation-theory/unit3.html", "deep"),
        (7, 11, ["../../statistics/testing-of-hypotheses/unit1.html",
                 "../../statistics/testing-of-hypotheses/unit2.html"], "deep"),
        # Tests about a proportion and about a correlation coefficient are in the
        # large-sample unit, not the small-sample one; the regression coefficient
        # is in Statistical Methods. Pointing this row at unit4 alone was wrong,
        # and the deep-grade check caught it.
        (11, 12, ["../../statistics/inferential-statistics/unit3.html",
                  "../../statistics/inferential-statistics/unit4.html",
                  "../../statistics/statistical-methods/unit4.html"], "deep"),
        (12, 14, None, "missing"),
        (14, 15, "../../statistics/testing-of-hypotheses/unit3.html", "deep"),
        (15, 16, "../../statistics/inferential-statistics/unit4.html", "deep"),
        (16, 17, "../../statistics/inferential-statistics/unit5.html", "deep"),
        (17, 19, "../../statistics/testing-of-hypotheses/unit4.html", "deep"),
    ]),
    (3, "Multivariate Analysis", [
        (0, 5, "../../statistics/multivariate-analysis/unit1.html", "deep"),
        (5, 7, "../../statistics/multivariate-analysis/unit2.html", "deep"),
        (7, 12, "../../statistics/multivariate-analysis/unit3.html", "deep"),
        (12, 15, "../../statistics/multivariate-analysis/unit4.html", "deep"),
        (15, 16, "../../statistics/multivariate-analysis/unit4.html", "deep"),
        (16, 18, "../../statistics/multivariate-analysis/practical.html", "brief"),
        (18, 19, "../../statistics/multivariate-analysis/unit4.html", "deep"),
    ]),
    (4, "Design of Experiments", [
        (0, 2, "../../statistics/linear-algebra-and-linear-models/unit4.html", "deep"),
        (2, 3, None, "missing"),
        (3, 5, "../../statistics/design-and-analysis-of-experiments-advanced/unit1.html", "deep"),
        (5, 9, ["../../statistics/design-and-analysis-of-experiments/unit1.html",
                "../../statistics/design-and-analysis-of-experiments-advanced/unit1.html"], "deep"),
        (9, 11, ["../../statistics/design-and-analysis-of-experiments/unit2.html",
                 "../../statistics/design-and-analysis-of-experiments/unit5.html"], "deep"),
        (11, 13, None, "missing"),
        (13, 15, "../../statistics/design-and-analysis-of-experiments-advanced/unit3.html", "deep"),
        (15, 16, "../../statistics/design-and-analysis-of-experiments-advanced/unit4.html", "deep"),
        (16, 17, "../../statistics/statistical-analysis-of-clinical-trials/practical.html", "brief"),
        (17, 19, ["../../statistics/design-and-analysis-of-experiments-advanced/unit2.html",
                  "../../statistics/design-and-analysis-of-experiments-advanced/unit3.html"], "deep"),
        (19, 21, None, "missing"),
        (21, 22, "../../statistics/design-and-analysis-of-experiments-advanced/index.html", "brief"),
        (22, 23, "../../statistics/design-and-analysis-of-experiments-advanced/unit4.html", "deep"),
        (23, 24, "../../statistics/design-and-analysis-of-experiments-advanced/unit1.html", "deep"),
        (24, 25, "../../statistics/sampling-techniques/unit1.html", "brief"),
    ]),
    (5, "Sample Surveys", [
        (0, 5, "../../statistics/sampling-techniques/unit1.html", "deep"),
        (5, 6, "../../statistics/sampling-techniques/unit2.html", "deep"),
        (6, 7, None, "missing"),
        (7, 9, "../../statistics/sampling-techniques/unit3.html", "deep"),
        (9, 11, "../../statistics/sampling-theory/unit2.html", "deep"),
        (11, 12, "../../statistics/sampling-theory/unit3.html", "deep"),
        (12, 15, ["../../statistics/sampling-techniques/unit4.html",
                  "../../statistics/sampling-theory/unit4.html"], "deep"),
        (15, 18, "../../statistics/sampling-theory/unit1.html", "deep"),
        (18, 20, "../../statistics/sampling-techniques/unit4.html", "deep"),
        (20, 23, "../../statistics/sampling-theory/unit4.html", "deep"),
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
        (33, 34, "../../statistics/advanced-actuarial-statistics/unit1.html", "brief"),
    ]),
    (7, "Regression Analysis", [
        (0, 2, ["../../statistics/statistical-methods/unit4.html",
                "../../statistics/linear-algebra-and-linear-models/unit4.html"], "deep"),
        (2, 4, "../../statistics/design-and-analysis-of-experiments-advanced/index.html", "brief"),
        (4, 6, "../../statistics/econometrics/unit2.html", "brief"),
        (6, 7, None, "missing"),
        (7, 9, "../../data-science/machine-learning/unit2.html", "brief"),
        (9, 10, ["../../statistics/econometrics/unit3.html",
                 "../../statistics/econometrics/unit4.html",
                 "../../statistics/econometrics/unit5.html"], "deep"),
        (10, 11, "../../statistics/econometrics/unit3.html", "deep"),
        (11, 13, "../../statistics/applied-statistics/unit1.html", "deep"),
        (13, 17, "../../data-science/time-series/unit1.html", "deep"),
        (17, 20, ["../../data-science/time-series/unit2.html",
                  "../../data-science/time-series/unit3.html"], "deep"),
        (20, 22, "../../statistics/econometrics/unit2.html", "brief"),
        (22, 25, "../../statistics/applied-statistics-ii/unit3.html", "deep"),
        (25, 26, None, "missing"),
    ]),
    (8, "Mathematical Methods in Statistics and Optimization Techniques", [
        (0, 3, "../../statistics/mathematical-analysis/unit1.html", "deep"),
        (3, 5, None, "missing"),
        (5, 8, "../../statistics/computational-statistics-and-r-programming/unit2.html", "brief"),
        (8, 9, None, "missing"),
        (9, 10, "../../statistics/linear-algebra-and-linear-models/unit1.html", "deep"),
        (10, 13, "../../statistics/linear-algebra-and-linear-models/unit1.html", "brief"),
        (13, 14, "../../statistics/distribution-theory/unit3.html", "brief"),
        (14, 16, "../../statistics/linear-algebra-and-linear-models/unit2.html", "deep"),
        (16, 17, None, "missing"),
        (17, 20, "../../statistics/linear-algebra-and-linear-models/unit1.html", "deep"),
        (20, 22, ["../../statistics/linear-algebra-and-linear-models/unit2.html",
                  "../../statistics/linear-algebra-and-linear-models/unit3.html"], "deep"),
        (22, 27, "../../statistics/operations-research/unit1.html", "brief"),
        (27, 29, ["../../statistics/operations-research/unit3.html",
                  "../../statistics/operations-research/unit5.html",
                  "../../statistics/optimization-techniques/unit4.html"], "deep"),
        (29, 32, None, "missing"),
        (32, 35, None, "missing"),
        (35, 36, "../../data-science/artificial-intelligence/unit3.html", "brief"),
        (36, 37, None, "missing"),
        (37, 39, ["../../data-science/machine-learning/unit4.html",
                  "../../data-science/deep-learning/unit1.html"], "deep"),
        (39, 40, None, "missing"),
        (40, 42, "../../statistics/computational-statistics-and-r-programming/unit5.html", "brief"),
        (42, 43, "../../statistics/estimation-theory/unit2.html", "deep"),
        (43, 44, "../../statistics/computational-statistics-and-r-programming/unit5.html", "brief"),
    ]),
]
