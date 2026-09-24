# -*- coding: utf-8 -*-
"""Which page on this site teaches each line of the UGC NET Statistics syllabus.

The source is the UGC NET Bureau's "NET Syllabus, Subject: Statistics, Code
107" (docs/sources/ugc-net-statistics-code-107.pdf), extracted to
ugc_syllabus.txt by pdftext_ugc.py. THE SYLLABUS TEXT IS NOT STORED HERE:
each row names a half-open range of that unit's items, and ugc_map.py joins
the slice to print the line, so the wording on the page is the document's own.

ITEMS are the document's comma-, semicolon-, colon- and full-stop-separated
pieces, split outside parentheses (ugc_map.items()). Ranges must be contiguous
and in order within a unit; ugc_map.py asserts both.

EACH ROW: (start, end, section, courses)

  section  the anchor on the UGC NET unit page that teaches the line, or None
  courses  [(course page, evidence)] -- a full course unit that teaches it,
           with a regular expression that must match that page's text. The
           generator fails the build if it does not, so a course is never
           listed on the strength of its title alone.

THE GRADE IS DERIVED, NOT CHOSEN. Every UGC NET section here is exam-summary
length -- the definition, the result and two worked examples, 60 to 380 words
-- which is exactly what the maps' "brief" means. A line is "deep" when a full
course unit also teaches it (and its evidence is found in that page), "brief"
when only the UGC NET section does, and "not here" when nothing does.
"""

S = "../../statistics/"
D = "../../data-science/"

TOP = S + "theory-of-probability/"
PT = S + "probability-theory/"
DT = S + "distribution-theory/"
MA = S + "mathematical-analysis/"
LA = S + "linear-algebra-and-linear-models/"
SMP = S + "sampling-techniques/"
STH = S + "sampling-theory/"
DAE = S + "design-and-analysis-of-experiments/"
DAA = S + "design-and-analysis-of-experiments-advanced/"
INF = S + "inferential-statistics/"
EST = S + "estimation-theory/"
TOH = S + "testing-of-hypotheses/"
SM = S + "statistical-methods/"
ECO = S + "econometrics/"
MVA = S + "multivariate-analysis/"
CSR = S + "computational-statistics-and-r-programming/"
CSR23 = S + "computational-statistics-and-r-programming-2023/"
TS = D + "time-series/"
ML = D + "machine-learning/"

UNITS = [
    ("I", "Probability and Distributions", [
        (0, 1, "prob", [(TOP + "unit1.html", r"[Aa]xiom")]),
        (1, 4, "cond", [(TOP + "unit1.html", r"Bayes")]),
        (4, 5, "rv", [(TOP + "unit2.html", r"distribution function")]),
        (5, 7, "exp", [(TOP + "unit4.html", r"[Mm]oment"), (TOP + "unit5.html", r"[Mm]oment generating")]),
        (7, 8, "discrete", [(S + "theoretical-discrete-distributions/index.html", r"Poisson"),
                            (S + "theoretical-continuous-distributions/index.html", r"Normal")]),
        (8, 10, "joint", [(TOP + "unit3.html", r"[Mm]arginal")]),
        (10, 11, "cheb", [(TOP + "unit4.html", r"Chebyshev")]),
        (11, 13, "sample", [(DT + "unit3.html", r"[Cc]hi-[Ss]quare"), (DT + "unit2.html", r"Jacobian")]),
        (13, 14, "cf", [(PT + "unit2.html", r"[Cc]haracteristic [Ff]unction")]),
        (14, 15, "conv", [(PT + "unit3.html", r"in probability")]),
        (15, 17, "lln", [(PT + "unit4.html", r"[Cc]entral [Ll]imit")]),
    ]),
    ("II", "Real Analysis and Matrix Algebra", [
        (0, 3, "sets", [(MA + "unit1.html", r"countable")]),
        (3, 8, "seq", [(MA + "unit1.html", r"Cauchy")]),
        (8, 13, "series", []),
        (13, 14, "power", []),
        (14, 20, "functions", [(MA + "unit1.html", r"[Uu]niform(ly)? continu")]),
        (20, 24, "diff", []),
        (24, 26, "riemann", [(MA + "unit2.html", r"Riemann")]),
        (26, 35, "two", []),
        (35, 41, "vec", [(LA + "unit1.html", r"basis")]),
        (41, 44, "rank", [(LA + "unit1.html", r"[Rr]ank")]),
        (44, 46, "det", [(LA + "unit2.html", r"[Dd]eterminant")]),
        (46, 47, "sys", []),
        (47, 48, "gs", [(LA + "unit1.html", r"Gram")]),
        (48, 51, "eig", [(LA + "unit2.html", r"Cayley")]),
        (51, 54, "sym", []),
        (54, 56, "pd", [(LA + "unit3.html", r"[Pp]ositive definite")]),
    ]),
    ("III", "Sampling Methods and Design of Experiments", [
        (0, 2, "srs", [(SMP + "unit2.html", r"without replacement")]),
        (2, 3, "strat", [(SMP + "unit3.html", r"Neyman")]),
        (3, 4, "sys", [(SMP + "unit4.html", r"[Ss]ystematic")]),
        (4, 5, "ratio", [(STH + "unit2.html", r"[Rr]atio estimator")]),
        (5, 6, "cluster", [(STH + "unit3.html", r"[Uu]nequal")]),
        (6, 7, "double", []),
        (7, 8, "pps", [(STH + "unit1.html", r"Horvitz")]),
        (8, 10, "pps", []),
        (10, 12, "anova1", [(DAE + "unit1.html", r"[Tt]wo-way")]),
        (12, 13, "principles", [(DAE + "unit2.html", r"[Rr]eplication")]),
        (13, 16, "crd", [(DAE + "unit2.html", r"Completely"), (DAE + "unit3.html", r"Block"),
                         (DAE + "unit4.html", r"Latin")]),
        (16, 17, "missing", [(DAE + "unit5.html", r"[Mm]issing")]),
        (17, 19, "fact", [(DAA + "unit2.html", r"Yates")]),
        (19, 20, "conf", [(DAA + "unit3.html", r"[Cc]onfounding")]),
        (20, 22, "bibd", []),
        (22, 24, "bibd", [(DAA + "unit3.html", r"[Rr]ecovery of inter-block|inter-block information")]),
    ]),
    ("IV", "Estimation Theory", [
        (0, 2, "unbiased", [(INF + "unit1.html", r"[Uu]nbiased")]),
        (2, 3, "consist", [(INF + "unit1.html", r"[Cc]onsisten")]),
        (3, 4, "mom", [(INF + "unit1.html", r"[Mm]aximum [Ll]ikelihood")]),
        (4, 6, "eff", [(EST + "unit1.html", r"UMVU")]),
        (6, 7, "crlb", [(EST + "unit1.html", r"Cram")]),
        (7, 9, "suff", [(EST + "unit1.html", r"[Ff]actori[sz]ation")]),
        (9, 11, "minsuff", []),
        (11, 12, "complete", [(EST + "unit2.html", r"[Cc]ompleteness")]),
        (12, 13, "rb", [(EST + "unit1.html", r"Rao")]),
        (13, 14, "ls", [(EST + "unit2.html", r"Lehmann")]),
        (14, 15, "basu", []),
        (15, 17, "pivot", [(EST + "unit3.html", r"[Pp]ivot")]),
        (17, 18, "ci", [(EST + "unit3.html", r"[Cc]onfidence [Ii]nterval")]),
        (18, 19, "large", [(INF + "unit3.html", r"[Cc]onfidence")]),
        (19, 21, "order", [(DT + "unit4.html", r"[Oo]rder [Ss]tatistic")]),
        (21, 22, "order", []),
        (22, 23, "rank", [(SM + "unit2.html", r"Spearman")]),
    ]),
    ("V", "Testing of Hypotheses", [
        (0, 2, "basic", [(INF + "unit2.html", r"[Cc]ritical [Rr]egion")]),
        (2, 3, "np", [(TOH + "unit1.html", r"Neyman")]),
        (3, 4, "mlr", [(TOH + "unit2.html", r"[Mm]onotone [Ll]ikelihood")]),
        (4, 6, "ump", [(TOH + "unit2.html", r"[Ii]nvariant")]),
        (6, 8, "lrt", [(TOH + "unit3.html", r"[Ll]ikelihood [Rr]atio")]),
        (8, 10, "sprt", [(TOH + "unit4.html", r"[Aa]verage [Ss]ample [Nn]umber")]),
        (10, 11, "chi2", [(INF + "unit4.html", r"[Gg]oodness of [Ff]it")]),
        (11, 12, "sign", [(INF + "unit5.html", r"[Ss]ign [Tt]est")]),
        (12, 13, "wsr", [(INF + "unit5.html", r"Wilcoxon")]),
        (13, 14, "mw", [(INF + "unit5.html", r"Mann")]),
        (14, 15, "linrank", []),
        (15, 16, "kw", [(INF + "unit5.html", r"Kruskal")]),
    ]),
    ("VI", "Linear Estimation, Regression Analysis and Econometrics", [
        (0, 1, "slr", [(SM + "unit4.html", r"[Rr]egression"), (ECO + "unit2.html", r"[Mm]ultiple")]),
        (1, 3, "gm", [(LA + "unit4.html", r"Gauss")]),
        (3, 4, "hyp", []),
        (4, 7, "anova", [(ML + "unit3.html", r"[Aa]djusted R")]),
        (7, 8, "linhyp", []),
        (8, 9, "gls", [(LA + "unit4.html", r"Aitken")]),
        (9, 10, "dummy", [(ECO + "unit2.html", r"[Dd]ummy")]),
        (10, 11, "multi", [(ECO + "unit4.html", r"[Mm]ulticollinearity")]),
        (11, 12, "het", [(ECO + "unit3.html", r"[Hh]eteroscedasticity")]),
        (12, 14, "auto", [(ECO + "unit5.html", r"Durbin")]),
        (14, 15, "logit", [(ML + "unit3.html", r"[Ll]ogistic regression")]),
        (15, 17, "restr", []),
        (17, 18, "stoch", []),
        (18, 19, "iv", []),
        (19, 21, "sem", [(ECO + "unit5.html", r"identified")]),
        (21, 22, "twosls", [(ECO + "unit5.html", r"2SLS")]),
        (22, 23, "twosls", []),
    ]),
    ("VII", "Time Series", [
        (0, 2, "intro", [(S + "applied-statistics/unit1.html", r"[Tt]rend")]),
        (2, 6, "acf", [(TS + "unit1.html", r"PACF|[Pp]artial autocorrelation")]),
        (6, 8, "stat", []),
        (8, 9, "wold", []),
        (9, 12, "ma", [(TS + "unit2.html", r"[Ii]nvertib")]),
        (12, 13, "yw", []),
        (13, 17, "order", [(TS + "unit2.html", r"AIC")]),
        (17, 20, "ns", [(TS + "unit3.html", r"ARIMA")]),
        (20, 24, "spec", [(TS + "unit5.html", r"[Ff]requency domain")]),
        (24, 25, "period", [(TS + "unit5.html", r"[Pp]eriodogram")]),
    ]),
    ("VIII", "Multivariate Analysis", [
        (0, 1, "mvn", [(MVA + "unit1.html", r"[Mm]ultivariate [Nn]ormal")]),
        (1, 3, "est", [(MVA + "unit1.html", r"[Mm]aximum [Ll]ikelihood")]),
        (3, 4, "wishart", [(MVA + "unit2.html", r"Wishart")]),
        (4, 7, "corr", [(MVA + "unit2.html", r"[Pp]artial")]),
        (7, 8, "hot", [(MVA + "unit3.html", r"Hotelling")]),
        (8, 9, "disc", [(MVA + "unit3.html", r"[Dd]iscriminant")]),
        (9, 10, "pca", [(MVA + "unit4.html", r"[Pp]rincipal [Cc]omponent")]),
        (10, 11, "cca", [(MVA + "unit4.html", r"[Cc]anonical")]),
    ]),
    ("IX", "Stochastic Processes", [
        (0, 2, "mc", []),
        (2, 3, "ck", []),
        (3, 5, "nstep", []),
        (5, 6, "gambler", []),
        (6, 7, "rw", []),
        (7, 9, "poisson", []),
        (9, 10, "bd", []),
        (10, 11, "mm1", []),
    ]),
    ("X", "Indian Statistical System and Research Methodology", [
        (0, 2, "mospi", [(SMP + "unit5.html", r"MoSPI|Ministry of Statistics")]),
        (2, 3, "nsc", [(SMP + "unit5.html", r"National Statistical Commission")]),
        (3, 4, "nso", [(SMP + "unit5.html", r"National Statistic(s|al) Office")]),
        (4, 5, "census", [(SMP + "unit5.html", r"National Sample Survey|NSS")]),
        (5, 11, "statisticians", []),
        (11, 14, "r-basics", [(CSR + "unit1.html", r"[Aa]rithmetic")]),
        (14, 15, "r-funcs", [(CSR + "unit1.html", r"[Mm]atri")]),
        (15, 17, "r-built", [(CSR + "unit1.html", r"is\.na|NA\b")]),
        # Loops are taught only in the 2023 revision of the R course, which is to
        # be retired (statistics/CLAUDE.md); when it goes, ugc_map.py fails on this
        # row rather than silently keeping a dead link.
        (17, 18, "r-control", [(CSR23 + "unit4.html", r"for \(|while \(")]),
        (18, 22, "r-data", [(CSR + "unit1.html", r"rep\(|seq\(")]),
        (22, 25, "r-list", [(CSR + "unit1.html", r"[Ff]actor")]),
        (25, 27, "r-frames", [(CSR + "unit1.html", r"[Dd]ata [Ff]rame")]),
        (27, 28, "r-graph", [(CSR + "unit3.html", r"ggplot|plot\(")]),
        (28, 30, "r-prog", [(CSR + "unit1.html", r"function ?\(")]),
        (30, 31, "latex", []),
    ]),
]
