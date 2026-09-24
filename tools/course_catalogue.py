#!/usr/bin/env python3
"""The one list of courses, in the order a learner should meet them.

    python3 tools/course_catalogue.py      # print it; exit 1 if it and the tree disagree

The site is for exam preparation, studied course by course: a visitor picks
any course, in any order, for the exam in front of them. There is no degree
programme and no semester. What there is, is an order -- descriptive before
probability, probability before distributions, distributions before
inference -- and this file is the only place it is written down. The menu
(site_nav_model.py), the Statistics and Data Science hubs and the "next
course" links all read it, so reordering a course is a one-line edit here.

LEVEL. Where a topic has two courses, one introductory and one advanced
(Probability, Distributions, Sampling, Design of Experiments), both are kept,
side by side, tagged Foundation or Advanced. The tag describes the material,
not who it was written for. Allied courses (Economics, Financial Accounting)
carry no tag.

A course folder on disk that is not listed here, or one listed twice, makes
main() fail -- so a new course cannot silently fall out of the menu.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

F, A = "Foundation", "Advanced"

# (topic group, [(folder under statistics/, level or None)])
STATISTICS = [
    ("Foundations", [
        ("descriptive-statistics", F),
        ("statistical-methods", F),
        ("mathematical-analysis", A),
        ("linear-algebra-and-linear-models", A),
    ]),
    ("Probability &amp; distributions", [
        ("theory-of-probability", F),
        ("probability-theory", A),
        ("theoretical-discrete-distributions", F),
        ("theoretical-continuous-distributions", F),
        ("distribution-theory", A),
    ]),
    ("Statistical inference", [
        ("inferential-statistics", F),
        ("estimation-theory", A),
        ("testing-of-hypotheses", A),
    ]),
    ("Sampling &amp; design", [
        ("sampling-techniques", F),
        ("sampling-theory", A),
        ("design-and-analysis-of-experiments", F),
        ("design-and-analysis-of-experiments-advanced", A),
    ]),
    ("Models &amp; multivariate", [
        ("econometrics", F),
        ("multivariate-analysis", A),
    ]),
    ("Applied statistics", [
        ("applied-statistics", F),
        ("applied-statistics-ii", F),
        ("statistical-quality-control", F),
        ("operations-research", F),
        ("optimization-techniques", F),
        ("actuarial-statistics", F),
        ("advanced-actuarial-statistics", A),
        ("statistical-analysis-of-clinical-trials", F),
        ("statistical-techniques-for-research-methodology", F),
    ]),
    ("Statistical computing", [
        ("statistical-data-analysis-using-ms-excel", F),
        ("statistical-analysis-using-spss", A),
        ("computational-statistics-and-r-programming", F),
        ("computational-statistics-and-r-programming-2023", F),
        ("data-handling-using-r", A),
        ("statistical-methods-using-python", A),
        ("data-science-using-python", A),
    ]),
    ("Allied courses", [
        ("economics", None),
        ("financial-accounting", None),
    ]),
]

# (topic group, [slug under data-science/])
DATA_SCIENCE = [
    ("Computing foundations", [
        "computer-fundamentals", "problem-solving-c", "python-data-structures",
        "web-technologies",
    ]),
    ("Statistics &amp; analysis", [
        "statistical-foundations", "data-science-r", "python-data-analysis",
        "time-series",
    ]),
    ("Data &amp; platforms", [
        "dbms", "document-database", "big-data", "cloud-computing",
    ]),
    ("Machine learning &amp; AI", [
        "data-mining", "machine-learning", "artificial-intelligence",
        "deep-learning", "nlp",
    ]),
    ("Delivery", [
        "business-intelligence", "mlops",
    ]),
]


# One line per course for its card on the hub: what it covers, in the
# course's own terms. Taken from the cards the hubs carried before the
# catalogue existed; the postgraduate and allied ones shortened from theirs.
BLURB = {
    'descriptive-statistics': 'Mean, Median, Mode, Dispersion, Moments, Skewness, Kurtosis.',
    'theory-of-probability': 'Probability axioms, random variables, expectation, generating functions, CLT.',
    'theoretical-discrete-distributions': 'Bernoulli, Binomial, Poisson, Negative Binomial, Geometric, Hyper-geometric.',
    'theoretical-continuous-distributions': 'Uniform, Exponential, Gamma, Beta, Normal, Sampling distributions (t, F, χ²).',
    'statistical-methods': 'Curve fitting, correlation, regression, attributes.',
    'inferential-statistics': 'Estimation, hypothesis testing, large &amp; small sample tests, non-parametric tests.',
    'sampling-techniques': 'SRS, stratified, systematic, cluster sampling; NSO &amp; NSC.',
    'design-and-analysis-of-experiments': 'ANOVA, CRD, RBD, LSD, missing values, efficiency.',
    'applied-statistics': 'Time series, index numbers, vital statistics, life tables.',
    'statistical-data-analysis-using-ms-excel': 'Excel functions, charts, descriptive stats, regression, hypothesis testing in Excel.',
    'computational-statistics-and-r-programming': 'R basics, descriptive stats, visualization, hypothesis testing, regression in R.',
    'operations-research': 'LPP, graphical &amp; simplex methods, Big-M, Two-phase, duality.',
    'actuarial-statistics': 'Insurance, premium calculation, life tables, life insurance, annuities.',
    'optimization-techniques': 'Transportation, assignment, sequencing, game theory, CPM/PERT.',
    'applied-statistics-ii': 'Growth curves, index numbers, demand analysis, psychological &amp; educational stats.',
    'statistical-quality-control': 'Control charts (variables &amp; attributes), acceptance sampling, single sampling plan.',
    'advanced-actuarial-statistics': 'Future lifetime, mortality laws, life insurance, annuities, premiums &amp; reserves.',
    'statistical-techniques-for-research-methodology': 'Research types, surveys, data collection, questionnaire, report writing &amp; project.',
    'statistical-analysis-of-clinical-trials': 'Phases, sample size, parallel/cross-over designs, surrogate endpoints, meta-analysis.',
    'econometrics': 'Empirical economic analysis, OLS &amp; Gauss–Markov, heteroscedasticity, multicollinearity, autocorrelation.',
    'computational-statistics-and-r-programming-2023': 'Computer basics, Excel data processing &amp; analysis, R programming, data frames, EDA &amp; visualisation.',
    'computer-fundamentals': 'Number systems, memory hierarchy, networks, Word, Excel, pivot tables and dashboards. Ten programs re-compute every spreadsheet figure and every number-system conversion.',
    'problem-solving-c': 'Control flow, arrays, strings, pointers, structures and file handling. 15 runnable programs.',
    'python-data-structures': 'Syntax, collections, files, exceptions, OOP, linked lists, stacks, queues. 18 experiments; 16 run, the two Tkinter programs syntax-checked only.',
    'statistical-foundations': 'Probability, distributions, correlation, regression, estimation and hypothesis testing. Formula sheet included.',
    'dbms': 'Three-schema architecture, ER modelling, normalization to 3NF, SQL joins and PL/SQL. Executable SQL labs.',
    'data-science-r': 'The data science lifecycle, R and RStudio, dplyr and ggplot2, regression and clustering, ARIMA and Shiny. 18 R scripts, 14 with executed Python equivalents.',
    'web-technologies': 'HTML structure and forms, CSS layout and responsive design, JavaScript and the DOM, client-side validation, JSON and jQuery. 16 experiments, 184 assertions under jsdom.',
    'data-mining': 'Data warehousing and OLAP, preprocessing and similarity, Apriori and FP-Growth, ID3 and C4.5, K-Means and DBSCAN. Every hand trace re-executed in scikit-learn.',
    'python-data-analysis': 'NumPy arrays and broadcasting, Pandas Series and DataFrames, cleaning and feature engineering, reshaping and merging, matplotlib, Seaborn and Plotly. All 18 practicals run.',
    'document-database': 'NoSQL and CAP, the BSON document model, CRUD and MQL, embed against reference, aggregation pipelines, indexing and replication. Sixteen of the twenty experiments execute through mongomock; the other four need a real server, and every mongosh script says it was not executed.',
    'business-intelligence': 'BI concepts and the data warehouse, Power BI and Power Query, DAX, Tableau and LOD expressions, dashboard design. Every figure computed, tool click-paths marked not executed.',
    'machine-learning': 'ML paradigms, preprocessing and evaluation, regression, classification and clustering. All 12 practicals run under scikit-learn.',
    'artificial-intelligence': 'Intelligent agents, uninformed and informed search, CSPs, propositional and first-order logic, expert systems. 19 experiments; the Prolog is marked not executed, and five of the Python halves run as real logic programs.',
    'big-data': 'HDFS and YARN, MapReduce, Hive and Pig, ingestion and serialization, HBase, ZooKeeper and Spark. 14 of 17 practicals run, including real Apache Spark, Avro and Parquet.',
    'cloud-computing': 'Service and deployment models, virtualization, cloud storage and warehouses, managed ML, deployment and monitoring. IAM evaluation, a real ETL and a real endpoint, all run locally.',
    'deep-learning': 'Perceptrons and activations, backpropagation, CNNs, RNNs and LSTM, attention and transformers, transfer learning and AI ethics. Ten of twelve experiments run against real MNIST, Fashion-MNIST, IMDb and real ImageNet weights.',
    'nlp': 'Ambiguity and regular expressions, tokenization, stemming and lemmatization, grammars and parsing, named entity recognition, embeddings, classification, RNNs and transformers. Eleven of fourteen experiments run against real NLTK corpora and real spaCy models.',
    'time-series': 'Stationarity, ACF and PACF, ARMA, ARIMA and SARIMA, model selection, prediction intervals, VAR and Granger causality, Kalman filtering and spectral analysis. Every one of the 13 experiments runs.',
    'mlops': 'The data engineering lifecycle, architecture and distributed systems, MLOps fundamentals, deployment and CI/CD, monitoring and governance. Eleven of sixteen experiments run against real MLflow, git, DVC and Flask.',
    'mathematical-analysis': 'Metric spaces, compactness and continuity; the Riemann&ndash;Stieltjes integral; bounded variation and integrals depending on a parameter; sequences and series of functions. Proved rather than asserted.',
    'linear-algebra-and-linear-models': 'Vector spaces, Gram&ndash;Schmidt and generalized inverses; characteristic roots and spectral decomposition; quadratic forms; linear models, estimability, Gauss&ndash;Markov and Aitken.',
    'probability-theory': 'Measure-theoretic probability: sigma-fields, expectation as an integral, modes of convergence, characteristic functions, and the laws of large numbers and CLT proved.',
    'distribution-theory': 'Lognormal, Weibull, Pareto, Laplace and Cauchy; transformed, truncated, mixture and compound distributions; chi-square, t and F; quadratic forms and order statistics.',
    'estimation-theory': 'UMVU estimation, the Cram&eacute;r&ndash;Rao bound, Rao&ndash;Blackwell and Lehmann&ndash;Scheff&eacute;, maximum likelihood, jackknife and bootstrap, interval estimation, and Bayes and minimax rules.',
    'testing-of-hypotheses': 'Randomized tests and the Neyman&ndash;Pearson lemma, UMP tests and Karlin&ndash;Rubin, the likelihood ratio test with Wald and score tests, and the SPRT.',
    'sampling-theory': 'Unequal probability sampling (Hansen&ndash;Hurwitz, Lahiri, Horvitz&ndash;Thompson), the exact bias of ratio and regression estimators, cluster and two-stage sampling, randomized response and small area estimation.',
    'design-and-analysis-of-experiments-advanced': 'Two-way ANOVA with several observations per cell, multiple comparisons, ANCOVA, factorials and Yates&rsquo;s algorithm, confounding, split-plot and incomplete block designs.',
    'multivariate-analysis': 'The multivariate normal, Wishart, Hotelling&rsquo;s T&sup2; and Wilks&rsquo; &Lambda;, discriminant analysis, principal components, canonical correlation, clustering and factor analysis.',
    'statistical-methods-using-python': 'Twelve programs with no statistical package: summary measures, moments, random number generators, distributions fitted and tested, correlation, regression and tests.',
    'data-handling-using-r': 'One data set end to end in R: measurement scales, pre-processing, transformations, diagrams, cross-validation and the confusion matrix.',
    'statistical-analysis-using-spss': 'The prescribed analyses as SPSS procedure: Variable View settings, the syntax for each analysis, model selection, logistic regression and probit.',
    'data-science-using-python': 'One extract&ndash;transform&ndash;load pipeline end to end: five formats parsed, anomalies named, the re module, a normalised schema and its queries.',
    'economics': 'Price determination and market structures, national income and the national accounts, money and banking, public finance, international economics and the Indian economy.',
    'financial-accounting': 'Concepts and conventions, journal and ledger, subsidiary books, bank reconciliation, trial balance and final accounts, depreciation and incomplete records.',
}


def _is_stub(p):
    head = p.read_text(errors="replace")[:2048]
    return 'http-equiv="refresh"' in head and "noindex" in head


def statistics_on_disk():
    """Every statistics/<folder>/ whose index.html is a real page."""
    return sorted(d.name for d in (ROOT / "statistics").iterdir()
                  if d.is_dir() and (d / "index.html").exists()
                  and not _is_stub(d / "index.html"))


def data_science_on_disk():
    """Every Data Science course the generator builds."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_bs", ROOT / "tools" / "data-science" / "build_site.py")
    bs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bs)
    return sorted(c["slug"] for c in bs.COURSES)


def statistics_courses():
    """[(folder, level, group)] in learning order."""
    return [(f, lvl, g) for g, rows in STATISTICS for f, lvl in rows]


def data_science_courses():
    """[(slug, group)] in learning order."""
    return [(s, g) for g, rows in DATA_SCIENCE for s in rows]


def problems():
    out = []
    for name, listed, disk in (
            ("statistics", [f for f, _, _ in statistics_courses()], statistics_on_disk()),
            ("data-science", [s for s, _ in data_science_courses()], data_science_on_disk())):
        seen = set()
        for f in listed:
            if f in seen:
                out.append("%s/%s is listed twice" % (name, f))
            seen.add(f)
        for f in sorted(set(disk) - seen):
            out.append("%s/%s exists but is not in the catalogue" % (name, f))
        for f in sorted(seen - set(disk)):
            out.append("%s/%s is in the catalogue but not on disk" % (name, f))
    for f in [f for f, _, _ in statistics_courses()] + [s for s, _ in data_science_courses()]:
        if f not in BLURB:
            out.append("%s has no BLURB line for its card" % f)
    return out


def main():
    for label, groups in (("Statistics", STATISTICS), ("Data Science", DATA_SCIENCE)):
        print(label)
        for g, rows in groups:
            print("   [%s]" % g)
            for r in rows:
                print("      %-50s %s" % ((r[0], r[1] or "") if isinstance(r, tuple) else (r, "")))
    bad = problems()
    print("\n%d statistics course(s), %d data science course(s), %d problem(s)"
          % (len(statistics_courses()), len(data_science_courses()), len(bad)))
    for b in bad:
        print("   ", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
