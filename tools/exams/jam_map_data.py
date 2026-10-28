# -*- coding: utf-8 -*-
"""Which page on this site teaches each line of the IIT JAM Mathematical Statistics (MS) syllabus.

THE SYLLABUS TEXT IS NOT STORED HERE. Each row names a half-open range of lines in
jam_ms_syllabus.txt, and jam_map.py joins that slice to make the line it prints, so
the wording on the page is the document's own. Ranges must be contiguous and in
order within a section; jam_map.py asserts both.

Destinations are paths relative to exams/iit-jam/, optionally with a #section;
jam_map.py checks that every page and every section exists.

GRADES. deep = a page here works the thing out with examples; brief = covered at
exam-summary level; missing = nothing here teaches it. Lines the site lacked when
the map was first drawn (October 2026) were written into the nearest course unit
before the map was published, so the map grades them from those sections.
"""

S = "../../statistics/"
DS, SM = S + "descriptive-statistics/", S + "statistical-methods/"
MA, LA = S + "mathematical-analysis/", S + "linear-algebra-and-linear-models/"
TOP, PT = S + "theory-of-probability/", S + "probability-theory/"
TDD, TCD = S + "theoretical-discrete-distributions/", S + "theoretical-continuous-distributions/"
DT, INF = S + "distribution-theory/", S + "inferential-statistics/"
ET, TH = S + "estimation-theory/", S + "testing-of-hypotheses/"
NET = "../ugc-net/"

# (section, title, [(start, end, destination(s) or None, grade), ...])
SECTIONS = [
    (1, "Sequences and Series of real numbers", [
        (0, 4, [MA + "unit4.html#5-sequences-and-series-of-real-numbers", NET + "unit2.html#seq"], "deep"),
        (4, 5, MA + "unit4.html#5-sequences-and-series-of-real-numbers", "deep"),
        (5, 9, [MA + "unit4.html#5-sequences-and-series-of-real-numbers", NET + "unit2.html#series"], "deep"),
        (9, 12, MA + "unit4.html#5-sequences-and-series-of-real-numbers", "deep"),
        (12, 13, [MA + "unit4.html#5-sequences-and-series-of-real-numbers", NET + "unit2.html#power"], "deep"),
    ]),
    (2, "Differential Calculus of one and two real variables, and Integral Calculus", [
        (0, 3, [MA + "unit1.html#4-limits-and-continuity", NET + "unit2.html#functions"], "deep"),
        (3, 4, [MA + "unit1.html#7-differentiation", NET + "unit2.html#diff"], "deep"),
        (4, 9, MA + "unit1.html#8-calculus-of-one-variable", "deep"),
        (9, 13, [MA + "unit1.html#9-calculus-of-two-variables", NET + "unit2.html#two"], "deep"),
        (13, 14, MA + "unit1.html#8-calculus-of-one-variable", "deep"),
        (14, 17, MA + "unit1.html#9-calculus-of-two-variables", "deep"),
        (17, 18, NET + "unit2.html#riemann", "brief"),
        (18, 20, MA + "unit3.html#3-differentiation-under-the-integral-sign", "deep"),
        (20, 21, NET + "unit2.html#riemann", "brief"),
        (21, 22, [TCD + "unit3.html#1-preliminaries-gamma-function",
                  MA + "unit3.html#5-double-integrals-change-of-variables-and-applications"], "deep"),
        (22, 25, [MA + "unit3.html#5-double-integrals-change-of-variables-and-applications",
                  MA + "unit3.html#4-interchanging-the-order-of-integration"], "deep"),
        (25, 27, MA + "unit3.html#5-double-integrals-change-of-variables-and-applications", "deep"),
    ]),
    (3, "Matrices and Determinants", [
        (0, 5, [NET + "unit2.html#vec", NET + "unit2.html#rank"], "brief"),
        (5, 6, NET + "unit2.html#det", "brief"),
        (6, 7, [LA + "unit1.html#6-special-matrices-determinants-and-rank", NET + "unit2.html#sym"], "deep"),
        (7, 11, [LA + "unit1.html#6-special-matrices-determinants-and-rank", NET + "unit2.html#det"], "deep"),
        (11, 13, NET + "unit2.html#det", "brief"),
        (13, 14, [LA + "unit1.html#6-special-matrices-determinants-and-rank", NET + "unit2.html#rank"], "deep"),
        (14, 15, NET + "unit2.html#rank", "brief"),
        (15, 19, [LA + "unit1.html#5-solving-systems-of-linear-equations",
                  LA + "unit1.html#6-special-matrices-determinants-and-rank"], "deep"),
        (19, 22, [LA + "unit2.html#1-characteristic-roots-and-vectors",
                  LA + "unit2.html#3-the-cayleyhamilton-theorem"], "deep"),
        (22, 23, LA + "unit3.html#1-real-quadratic-forms", "deep"),
    ]),
    (4, "Descriptive Statistics and Probability", [
        (0, 3, [DS + "unit1.html", DS + "unit2.html"], "deep"),
        (3, 4, DS + "unit3.html", "deep"),
        (4, 5, DS + "unit4.html", "deep"),
        (5, 6, DS + "unit5.html", "deep"),
        (6, 7, [SM + "unit2.html", SM + "unit3.html"], "deep"),
        (7, 12, [TOP + "unit1.html#1-basic-concepts", TOP + "unit1.html#5-addition-theorem-of-probability"], "deep"),
        (12, 13, TOP + "unit1.html#geometric-probability", "deep"),
        (13, 14, TOP + "unit1.html#7-booles-inequality", "deep"),
        (14, 17, [TOP + "unit1.html#3-conditional-probability", TOP + "unit1.html#8-bayes-theorem"], "deep"),
    ]),
    (5, "Univariate Distributions", [
        (0, 5, TOP + "unit2.html", "deep"),
        (5, 7, [TOP + "unit4.html", TOP + "unit2.html#6-moments-from-pmf-pdf"], "deep"),
        (7, 8, TOP + "unit5.html#1-moment-generating-function-mgf", "deep"),
        (8, 9, TOP + "unit4.html#7-chebyshevs-inequality", "deep"),
        (9, 10, [TDD + "index.html", TCD + "index.html", DT + "unit1.html"], "deep"),
    ]),
    (6, "Multivariate Distributions", [
        (0, 6, TOP + "unit3.html", "deep"),
        (6, 7, [TOP + "unit3.html#8-transformation-of-two-random-variables-jacobian-method",
                DT + "unit2.html#1-functions-of-random-variables-the-jacobian-rule"], "deep"),
        (7, 9, TOP + "unit4.html#3-covariance-via-expectation", "deep"),
        (9, 11, TOP + "unit5.html#joint-moment-generating-function", "deep"),
        (11, 12, [TOP + "unit4.html", PT + "unit2.html#2-conditional-expectation-and-conditional-variance"], "deep"),
        (12, 13, [TDD + "unit2.html#4-additive-property", TCD + "unit3.html#2-gamma-distribution",
                  TCD + "unit4.html#8-additive-property"], "deep"),
        (13, 14, TDD + "unit1.html#4-multinomial-distribution", "deep"),
        (14, 15, TCD + "unit4.html#13-bivariate-normal-distribution", "deep"),
    ]),
    (7, "Limit Theorems", [
        (0, 1, [TOP + "unit5.html#5-modes-of-convergence", PT + "unit3.html#2-the-implications-between-the-modes"], "deep"),
        (1, 2, [TOP + "unit5.html#6-weak-law-of-large-numbers-wlln", TOP + "unit5.html#8-central-limit-theorem-clt"], "deep"),
    ]),
    (8, "Sampling Distributions", [
        (0, 2, TCD + "unit5.html#2-population-sample-parameter-statistic", "deep"),
        (2, 3, DT + "unit4.html#2-order-statistics", "deep"),
        (3, 4, DT + "unit4.html#smallest-and-largest-order-statistics", "deep"),
        (4, 6, TCD + "unit5.html#3-chi-square-χ²-distribution", "deep"),
        (6, 7, TCD + "unit5.html#4-students-t-distribution", "deep"),
        (7, 9, TCD + "unit5.html#5-f-distribution-snedecors-f", "deep"),
        (9, 10, TCD + "unit5.html#6-relationships-among-sampling-distributions", "deep"),
    ]),
    (9, "Estimation", [
        (0, 1, INF + "unit1.html#21-unbiasedness", "deep"),
        (1, 3, [INF + "unit1.html#24-sufficiency", NET + "unit4.html#suff"], "deep"),
        (3, 4, ET + "unit2.html#1-completeness", "deep"),
        (4, 5, [INF + "unit1.html#22-consistency", INF + "unit1.html#23-efficiency"], "deep"),
        (5, 6, INF + "unit1.html#25-minimum-variance-unbiased-estimator-mvue", "deep"),
        (6, 7, [ET + "unit1.html#5-sufficiency-and-the-raoblackwell-theorem",
                ET + "unit2.html#2-the-lehmannscheffé-theorem"], "deep"),
        (7, 8, [INF + "unit1.html#4-raocramer-inequality", ET + "unit1.html#3-the-cramérrao-inequality"], "deep"),
        (8, 9, INF + "unit1.html#3-methods-of-estimation", "deep"),
        (9, 10, [SM + "unit1.html#2-principle-of-least-squares", SM + "unit4.html#3-two-lines-of-regression"], "deep"),
        (10, 11, INF + "unit1.html#5-confidence-intervals-cis", "deep"),
        (11, 12, [INF + "unit1.html#standard-ci-formulas",
                  INF + "unit1.html#confidence-intervals-for-two-normal-populations-and-the-exponential"], "deep"),
    ]),
    (10, "Testing of Hypotheses", [
        (0, 3, [INF + "unit2.html#1-statistical-hypothesis", INF + "unit2.html#3-two-types-of-errors",
                INF + "unit2.html#4-p-value"], "deep"),
        (3, 6, [INF + "unit2.html#7-neymanpearson-lemma", TH + "unit2.html#1-uniformly-most-powerful-tests"], "deep"),
        (6, 7, [INF + "unit2.html#8-generalized-likelihood-ratio-test-lrt", TH + "unit3.html"], "deep"),
    ]),
    (11, "Nonparametric Methods", [
        (0, 1, INF + "unit5.html#2-one-sample-runs-test-test-for-randomness", "deep"),
        (1, 2, PT + "unit3.html#5-the-glivenkocantelli-lemma", "deep"),
        (2, 3, INF + "unit5.html#9-kolmogorovsmirnov-ks-test", "deep"),
        (3, 4, INF + "unit5.html#3-sign-test", "deep"),
        (4, 5, INF + "unit5.html#6-wilcoxonmannwhitney-u-test", "deep"),
    ]),
    (12, "Stochastic Processes", [
        (0, 1, [NET + "unit9.html#mc", NET + "unit9.html#class", NET + "unit9.html#stat"], "deep"),
        (1, 2, [NET + "unit9.html#poisson", NET + "unit9.html#inter"], "deep"),
    ]),
]
