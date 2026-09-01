#!/usr/bin/env python3
"""Generate the study-material website from the Markdown notes.

House style is adopted from nrstatlab/Statistics-Major: the same
css/styles.css, the same .banner/.crumbs header, .chips topic row,
.unit-card grids, .page-nav footer navigation and MathJax loading, so the
two sites read as one family.

Markdown stays the source of truth. The notes remain readable on github.com
and the verification tooling (tools/verify_all.sh, tools/check_coverage.py)
keeps operating on them; this script only renders them.

Usage:
    pip install markdown
    python3 tools/build_site.py

Writes .html files next to nothing -- into per-course directories at the
repository root, mirroring the Statistics-Major layout:

    index.html                     course hub
    css/styles.css                 shared stylesheet
    <course-slug>/index_<slug>.html
    <course-slug>/unit1_<slug>.html ... unit5_<slug>.html
    <course-slug>/practice_<slug>.html, lab_<slug>.html
    syllabus-review.html, syllabus-map.html, study-plan.html
"""

import html
import pathlib
import re
import sys

try:
    import markdown
except ImportError:
    sys.exit("markdown is required:  pip install markdown")

ROOT = pathlib.Path(__file__).resolve().parent.parent

MATHJAX = ('<script id="MathJax-script" async '
           'src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">'
           '</script>')

MERMAID = """<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  document.querySelectorAll('pre > code.language-mermaid').forEach((code) => {
    const holder = document.createElement('pre');
    holder.className = 'mermaid';
    holder.textContent = code.textContent;
    code.closest('pre').replaceWith(holder);
  });
  mermaid.initialize({ startOnLoad: true, securityLevel: 'strict',
                       flowchart: { useMaxWidth: true }, er: { useMaxWidth: true } });
</script>"""

# --------------------------------------------------------------------------
# Course definitions -- order matches the syllabus, not the filesystem.
# --------------------------------------------------------------------------

COURSES = [
    {
        "slug": "computer-fundamentals",
        "src": "notes/sem-1/course-1-computer-fundamentals",
        "number": 1, "year": "I", "sem": "I",
        "title": "Computer Fundamentals and Office Automation",
        "tagline": "Number systems, computer organization, networking, "
                   "word processing, spreadsheets and dashboards.",
        "blurb": "5 Units + Lab • Number systems, memory hierarchy, networks, "
                 "Word, Excel, pivot tables and dashboards.",
        "units": [
            ("Number Systems, Evolution, Block Diagram and Generations",
             "Binary, octal, hexadecimal and conversions; evolution of computers; "
             "block diagram; five generations."),
            ("Basic Organization and Networking Fundamentals",
             "Functional components, memory hierarchy, types of computers; LAN, WAN, "
             "MAN; star, ring and bus topologies; Internet basics."),
            ("Word Processing and Presentations",
             "Formatting, styles, tables, mail merge; slide design, animations, "
             "transitions; keyboard shortcuts."),
            ("Spreadsheet Basics",
             "Cell referencing, SUM/AVERAGE/IF/COUNT, charts, text functions, "
             "VLOOKUP, HLOOKUP, XLOOKUP, INDEX and MATCH."),
            ("Data Analysis and Visualization",
             "Conditional formatting, pivot tables, data validation, Goal Seek, "
             "Scenario Manager, dashboards, slicers and sparklines."),
        ],
    },
    {
        "slug": "problem-solving-c",
        "src": "notes/sem-1/course-2-problem-solving-c",
        "number": 2, "year": "I", "sem": "I",
        "title": "Problem Solving Using C",
        "tagline": "Structured programming, control flow, arrays, pointers, "
                   "dynamic memory and file handling.",
        "blurb": "5 Units + Lab • Control flow, arrays, strings, pointers, "
                 "structures, unions and file handling. 15 runnable programs.",
        "units": [
            ("Introduction to Computer Programming",
             "Types of software, compiler vs interpreter, algorithms and flowcharts; "
             "C tokens, data types, operators and I/O."),
            ("Control Statements",
             "if, if-else, else-if ladder, switch; while, for, do-while; "
             "break, continue and goto."),
            ("Derived Data Types: Arrays and Strings",
             "One- and two-dimensional arrays, memory representation, row-major "
             "order; strings and string handling functions."),
            ("Pointers, Functions and Storage Classes",
             "Pointers and pointer arithmetic; functions, recursion, call by value "
             "and by address; auto, extern, static and register."),
            ("Dynamic Memory, Structures, Unions and Files",
             "malloc, calloc, realloc, free; structures and unions; "
             "text file operations."),
        ],
    },
    {
        "slug": "python-data-structures",
        "src": "notes/sem-2/course-3-python-data-structures",
        "number": 3, "year": "I", "sem": "II",
        "title": "Python Programming and Data Structures",
        "tagline": "Python fundamentals, collections, file handling, "
                   "object-oriented programming and abstract data structures.",
        "blurb": "5 Units + Lab • Syntax, collections, files, exceptions, OOP, "
                 "linked lists, stacks, queues and Tkinter. 18 runnable programs.",
        "units": [
            ("Basics of Python Programming",
             "Features, programming modes, identifiers, literals, built-in types, "
             "operators and precedence."),
            ("Control Flow, Functions and Modules",
             "if-elif-else, loops, for…else; functions, argument types, scope, "
             "recursion, lambda; modules and namespaces."),
            ("Sequences, Sets and Mapping Types",
             "Strings, lists, tuples, sets and dictionaries; slicing, mutability "
             "and comprehensions."),
            ("File Handling, Exception Handling and OOP",
             "Files and CSV; try-except-else-finally; classes, constructors, "
             "encapsulation, inheritance and overriding."),
            ("Abstract Data Structures and GUI Programming",
             "Linked lists, stacks, queues, priority queues; Tkinter widgets "
             "and event handling."),
        ],
    },
    {
        "slug": "statistical-foundations",
        "src": "notes/sem-2/course-4-statistical-foundations",
        "number": 4, "year": "I", "sem": "II",
        "title": "Statistical Foundations for Data Science",
        "tagline": "Probability, random variables, distributions, regression "
                   "and statistical inference.",
        "blurb": "5 Units + Lab • Probability, distributions, correlation, "
                 "regression, estimation and hypothesis testing. Formula sheet included.",
        "units": [
            ("Fundamentals of Probability and Basic Statistics",
             "Axioms and rules of probability, conditional probability and Bayes' "
             "theorem; central tendency, dispersion, correlation and covariance."),
            ("Random Variables, Expectation and Variance",
             "Discrete and continuous random variables, PMF, PDF and CDF; "
             "expectation, variance, moments and the MGF."),
            ("Probability Distributions",
             "Binomial, Poisson, geometric, negative binomial; uniform, normal, "
             "exponential, gamma; joint distributions and the Central Limit Theorem."),
            ("Correlation and Regression",
             "Bivariate data, Pearson and Spearman correlation; simple linear "
             "regression, ANOVA, residuals and goodness of fit."),
            ("Statistical Inference, Estimation and Hypothesis Testing",
             "Sampling distributions, confidence intervals; z, t, chi-square and "
             "F tests; p-values, Type I and II errors and power."),
        ],
    },
    {
        "slug": "dbms",
        "src": "notes/sem-3/course-5-dbms",
        "number": 5, "year": "II", "sem": "III",
        "title": "Database Management Systems",
        "tagline": "Database design, the relational model, normalization, "
                   "SQL and PL/SQL.",
        "blurb": "5 Units + Lab • Three-schema architecture, ER modelling, "
                 "normalization to 3NF, SQL joins and PL/SQL. Executable SQL labs.",
        "units": [
            ("Overview of Database Management Systems",
             "Data and information, file-based systems and their drawbacks; the "
             "database approach, data models and the three-schema architecture."),
            ("The Entity-Relationship Model",
             "ER building blocks, entity and attribute classification, cardinality; "
             "reducing ER diagrams to tables; the EER model."),
            ("The Relational Model and Normalization",
             "Codd's rules, keys, integrity constraints, relational algebra; "
             "functional dependencies and normal forms to 3NF and BCNF."),
            ("Structured Query Language",
             "DDL, DML and DQL; aggregates, GROUP BY and HAVING; joins, set "
             "operations, subqueries and views."),
            ("PL/SQL and Triggers",
             "Block structure, control structures, cursors and exceptions; "
             "procedures, functions and database triggers."),
        ],
    },
{
        "slug": "data-science-r",
        "src": "notes/sem-3/course-6-data-science-r",
        "number": 6, "year": "II", "sem": "III",
        "title": "Data Science with R",
        "tagline": "The data science process, R programming, wrangling, "
                   "visualisation, modelling and time series.",
        "blurb": "5 Units + Lab \u2022 Data science lifecycle, R programming, "
                 "dplyr/ggplot2, regression, clustering, ARIMA and Shiny.",
        "units": [
            ("Introduction to the Data Science Process",
             "Definition and applications; the Data Analytics Life Cycle; the "
             "toolkit and the team; exploratory data analysis; feature "
             "engineering and data transformation."),
            ("Basics of R Programming",
             "R and RStudio; data types and structures; operators; control "
             "structures and the apply family; functions and packages; "
             "reading CSV, Excel, JSON and XML."),
            ("Data Handling and Visualization in R",
             "The pipe and the five dplyr verbs; tidyr reshaping; missing "
             "data; dates and times; ggplot2 \u2014 grammar of graphics, "
             "geometries, scales, faceting and export."),
            ("Applications and Case Studies",
             "Simple and multiple regression; confusion matrix, precision, "
             "recall, ROC and AUC; K-Means clustering; text mining and "
             "TF-IDF; recommender systems; ethics in data science."),
            ("Advanced Topics",
             "Time series \u2014 decomposition, stationarity, differencing, "
             "ACF/PACF, ARIMA and forecasting; interactive plots with plotly; "
             "building web applications with R Shiny."),
        ],
    },
    {
        "slug": "web-technologies",
        "src": "notes/sem-3/course-7-web-technologies",
        "number": 7, "year": "II", "sem": "III",
        "title": "Web Technologies",
        "tagline": "HTML, CSS, JavaScript, the DOM, JSON and jQuery \u2014 "
                   "the only course where you build something you can see.",
        "blurb": "5 Units + Lab \u2022 HTML structure and forms, CSS layout "
                 "and responsive design, JavaScript, the DOM, JSON and jQuery.",
        "units": [
            ("HTML",
             "Web versus desktop applications; the client\u2013server model; "
             "document structure, elements and attributes; headings, text, "
             "lists, images and multimedia; tables; semantic HTML5; forms and "
             "GET versus POST."),
            ("CSS",
             "Syntax and the three attachment methods; the four combinators; "
             "specificity and the cascade; the box model; colours, borders, "
             "backgrounds, text and fonts; positioning, float, Flexbox and "
             "Grid; pseudo-classes and pseudo-elements; tooltips, galleries, "
             "forms, counters and media queries."),
            ("JavaScript",
             "DHTML; variables and types; operators and coercion; statements "
             "and loops; functions, closures and hoisting; string methods; "
             "Math; arrays and objects; classes; regular expressions; "
             "exception handling."),
            ("Client-Side Scripting",
             "The DOM and the BOM; selecting and changing elements; accessing "
             "form controls; the event model \u2014 bubbling, capturing and "
             "delegation; basic and format validation; inline messages; "
             "windows, dialog boxes and the status bar; keyboard and mouse "
             "events; animation."),
            ("JSON and jQuery",
             "Why data-exchange formats exist; JSON syntax and its "
             "restrictions; JSON versus XML; parsing, stringifying and nested "
             "access; fetch and localStorage; jQuery selectors, filters, DOM "
             "manipulation, events, effects, chaining and AJAX."),
        ],
    },
    {
        "slug": "data-mining",
        "src": "notes/sem-4/course-8-data-mining",
        "number": 8, "year": "II", "sem": "IV",
        "title": "Data Mining",
        "tagline": "Warehousing and OLAP, preprocessing, association rules, "
                   "classification and clustering \u2014 the algorithmic core.",
        "blurb": "5 Units + Lab \u2022 Star schemas and OLAP, preprocessing, "
                 "Apriori and FP-Growth, ID3/C4.5/CART, K-Means and DBSCAN.",
        "units": [
            ("Data Warehousing and OLAP",
             "Inmon\u2019s four characteristics; OLTP versus OLAP; three-tier "
             "architecture and ETL; the multidimensional model; fact and "
             "dimension tables; star, snowflake and fact constellation "
             "schemas; the cube and the five OLAP operations."),
            ("Data Mining and Preprocessing",
             "Definitions and the KDD process; predictive versus descriptive "
             "tasks; cleaning, missing data and noise; the curse of "
             "dimensionality and PCA; feature subset selection; "
             "discretization and binarization; normalisation; similarity and "
             "dissimilarity measures; issues, ethics and applications."),
            ("Association Analysis",
             "Support, confidence and lift; why confidence alone misleads; "
             "the Apriori principle and algorithm; rule generation; "
             "Partition, Pincer-Search and Dynamic Itemset Counting; the "
             "FP-tree and FP-Growth; generalized rules and item constraints."),
            ("Classification",
             "Decision trees and the best split; entropy, information gain, "
             "gain ratio and Gini; ID3, C4.5 and CART; overfitting and "
             "pruning; the confusion matrix, precision, recall, F1, ROC and "
             "AUC; rule-based classifiers; k-nearest neighbour; Na\u00efve "
             "Bayes and Laplace smoothing."),
            ("Clustering Techniques",
             "Clustering paradigms and validity measures; K-Means and its "
             "five weaknesses; K-Medoids and PAM; agglomerative clustering "
             "and linkage criteria; DBSCAN; BIRCH and the CF-tree; "
             "categorical clustering with STIRR, ROCK and CACTUS."),
        ],
    },
    {
        "slug": "python-data-analysis",
        "src": "notes/sem-4/course-9-python-data-analysis",
        "number": 9, "year": "II", "sem": "IV",
        "title": "Python for Data Analysis and Visualization",
        "tagline": "NumPy and Pandas \u2014 the tools you will actually use, "
                   "every day, in any data job you take.",
        "blurb": "5 Units + Lab \u2022 NumPy arrays, Pandas Series and "
                 "DataFrames, cleaning, feature engineering, wrangling and "
                 "three plotting libraries.",
        "units": [
            ("NumPy Essentials",
             "The ndarray against the Python list; creating arrays and dtypes; "
             "arithmetic and broadcasting; basic, boolean and fancy indexing, "
             "and which return views; transposing and swapping axes; universal "
             "functions; statistical functions and the axis parameter; random "
             "number generation."),
            ("Pandas Basics and Data Structures",
             "Series and DataFrame; Index objects; the three accessors and why "
             "\u2018loc\u2019 is inclusive; filtering and boolean indexing; "
             "arithmetic and data alignment; sorting and the five ranking "
             "methods; dropping entries; duplicate indexes."),
            ("Data Input, Output and Cleaning",
             "read_csv and the parameters that matter; JSON and "
             "json_normalize; Excel; detecting, dropping and filling missing "
             "data; replacing sentinel values; renaming axes; removing "
             "duplicates; filtering outliers by z-score and IQR; transforming "
             "with map, apply and transform."),
            ("String Operations and Feature Engineering",
             "The .str accessor; regular expressions with extract, contains "
             "and replace; engineering features from dates, numbers and "
             "categories; dummy and indicator variables and the dummy variable "
             "trap; permutation, stratified sampling and the bootstrap."),
            ("Wrangling, Reshaping and Visualization",
             "Merging and the four join types; concatenation; combining with "
             "overlap; hierarchical indexing; pivot, melt, stack and unstack; "
             "split\u2013apply\u2013combine; recomputing Course 4 in Pandas; "
             "matplotlib, Seaborn and Plotly."),
        ],
    },
    {
        "slug": "document-database",
        "src": "notes/sem-4/course-10-document-database",
        "number": 10, "year": "II", "sem": "IV",
        "title": "Document Oriented Database",
        "tagline": "MongoDB, and the design question behind every document "
                   "database: embed or reference?",
        "blurb": "5 Units + Lab \u2022 NoSQL and CAP, BSON and the document "
                 "model, CRUD and MQL, embedded against normalized models, "
                 "aggregation pipelines, indexing and replication.",
        "units": [
            ("Introduction to NoSQL and the Fundamentals of MongoDB",
             "What NoSQL is and what it is not; the CAP theorem and BASE "
             "against ACID; the four families \u2014 key-value, document, "
             "column and graph; RDBMS against NoSQL, and when NOT to use "
             "NoSQL; Redis, Cassandra, CouchDB and Neo4j compared; JSON and "
             "BSON; installation, the Mongo shell and Compass."),
            ("MongoDB Architecture, Data Modeling and Basics",
             "Database, collection and document; the BSON types and where "
             "each one bites; ObjectId and what its twelve bytes hold; schema "
             "design strategies; embedded against referenced documents; "
             "creating and dropping databases and collections."),
            ("CRUD Operations and Querying",
             "insertOne and insertMany, ordered and unordered; find and the "
             "comparison, logical, element, evaluation and array operators; "
             "updateOne, updateMany and the destructive replaceOne; deleteOne "
             "and deleteMany; regular expression queries; bulk operations; "
             "array update operators and $elemMatch."),
            ("Data Modelling and Aggregation",
             "Embedded against normalized models and the trade-offs of each; "
             "when to normalize; one-to-one, one-to-many and many-to-many; "
             "the 16 MB limit and the unbounded array; the extended reference, "
             "computed and attribute patterns; the aggregation framework, "
             "and $match/$group as WHERE and HAVING."),
            ("Advanced Query Processing and Optimization",
             "Projection, sorting, limiting and skipping, and the order the "
             "server applies them; range pagination against skip; single "
             "field, compound, multikey and text indexes; the prefix rule and "
             "ESR; reading explain(\"executionStats\"); aggregation pipelines "
             "and $lookup; replica sets, failover, write concern, and why an "
             "odd number of members."),
        ],
    },
    {
        "slug": "business-intelligence",
        "src": "notes/sem-5/course-11-business-intelligence",
        "number": 11, "year": "III", "sem": "V",
        "title": "Business Intelligence Tools",
        "tagline": "Power BI and Tableau \u2014 and the modelling decisions "
                   "that decide whether a dashboard is right or merely pretty.",
        "blurb": "5 Units + Lab \u2022 BI and DSS concepts, Power BI and DAX, "
                 "Tableau and LOD expressions, dimensional modelling, "
                 "dashboard design and storytelling.",
        "units": [
            ("Introduction to BI and Decision Support Systems",
             "BI definition, scope and evolution; BI against data analytics "
             "and data science; the BI lifecycle and where projects fail; "
             "applications across finance, HR, marketing, retail, education "
             "and healthcare; maturity models and organizational readiness; "
             "DSS concepts, components and architecture; Power BI and Tableau "
             "compared."),
            ("Data Preparation and Visualization with Power BI",
             "The Desktop / Service / Mobile ecosystem; connecting to Excel, "
             "CSV, SQL Server and Web APIs; Import against DirectQuery; Power "
             "Query as a recorded, replayable recipe; calculated columns "
             "against measures; SUM, COUNT, AVERAGE, IF and CALCULATE; the "
             "average-of-averages trap; sharing through the Service."),
            ("Preparation, Visualization and Storytelling with Tableau",
             "VizQL and the Tableau products; live against extract; shelves, "
             "the marks card and views; blue against green; data preparation "
             "and the filter order of operations; calculated fields; LOD "
             "expressions \u2014 FIXED, INCLUDE and EXCLUDE; joins against "
             "blending and the fan trap; building a story."),
            ("Data Modeling and Relationships in BI Tools",
             "Fact and dimension tables; the grain, and additive, "
             "semi-additive and non-additive measures; star against "
             "snowflake, and why never one flat table; relationships, "
             "cardinality and cross-filter direction; data governance \u2014 "
             "metadata, hierarchies and the six dimensions of quality; model "
             "design best practices."),
            ("Dashboard Design and Business Insights",
             "When a dashboard is and is not the right answer; dashboard "
             "components; the principles of effective visualization and "
             "accessibility; filters, slicers, parameters and drilldowns; "
             "layout, alignment and the F-pattern; publishing to the Power BI "
             "Service and Tableau Public; storytelling and insight "
             "communication."),
        ],
    },
    {
        "slug": "machine-learning",
        "src": "notes/sem-5/course-12a-machine-learning",
        "number": 12, "year": "III", "sem": "V",
        "title": "Machine Learning",
        "tagline": "Track A. The pipeline is the work \u2014 the model is the "
                   "easy part, and knowing whether it is any good is the rest.",
        "blurb": "5 Units + Lab \u2022 ML paradigms, preprocessing and "
                 "evaluation, regression, classification and clustering. All "
                 "12 practicals run under scikit-learn.",
        "units": [
            ("Introduction to Machine Learning",
             "Types of human learning and their machine analogues; Mitchell's "
             "definition; machine learning against traditional programming, "
             "and when not to use it; supervised, unsupervised, "
             "semi-supervised and reinforcement learning; the ML pipeline and "
             "where the effort goes; types of data and how each should be "
             "encoded; the feature matrix and the curse of dimensionality."),
            ("Model Preparation, Evaluation and Feature Engineering",
             "Preprocessing in order, and why splitting comes first; missing "
             "values, outliers, encoding and scaling; the three-way split and "
             "cross-validation; bias and variance; interpretability; why "
             "accuracy lies, the confusion matrix, precision, recall, F1 and "
             "AUC; performance enhancement and class imbalance; feature "
             "engineering, target leakage, subset selection and PCA."),
            ("Supervised Learning \u2014 Regression",
             "What changes when explanation becomes prediction; simple linear "
             "regression and the LINE assumptions; multiple regression, "
             "multicollinearity and adjusted R\u00b2; polynomial regression "
             "and the conditioning trap; logistic regression, the sigmoid and "
             "the odds ratio; maximum likelihood estimation; Ridge, Lasso and "
             "elastic net."),
            ("Supervised Learning \u2014 Classification",
             "The classification pipeline; binary, multi-class and "
             "multi-label; Na\u00efve Bayes, the naive assumption and Laplace "
             "smoothing; k-Nearest Neighbour, distance metrics and choosing "
             "k; decision trees and pruning; support vector machines, the "
             "margin, support vectors and the kernel trick; random forest, "
             "its two sources of randomness and out-of-bag error."),
            ("Unsupervised Learning",
             "Unsupervised against supervised, and why evaluation is the hard "
             "part; clustering types; K-Means, WCSS and the elbow; k-Medoids "
             "and robustness; hierarchical clustering and linkage; DBSCAN, "
             "core, border and noise points; internal against external "
             "validation metrics; case studies in image and speech "
             "recognition, spam filtering and fraud detection."),
        ],
    },
    {
        "slug": "big-data",
        "src": "notes/sem-5/course-12b-big-data",
        "number": 12, "year": "III", "sem": "V",
        "title": "Big Data Technologies",
        "tagline": "Track B. The shuffle is the only step that costs real "
                   "money \u2014 everything else is an attempt to shuffle "
                   "less.",
        "blurb": "5 Units + Lab \u2022 Big data characteristics, HDFS and "
                 "YARN, MapReduce, Hive and Pig, ingestion and "
                 "serialization, HBase, ZooKeeper and Spark. 14 of the 17 "
                 "practicals run, including REAL Apache Spark, Avro and "
                 "Parquet.",
        "units": [
            ("Foundations of Big Data and the Hadoop Ecosystem",
             "What big data means and why a byte count is the wrong "
             "definition; the five Vs and which of them actually drive a "
             "design; big data against a traditional RDBMS; the Hadoop "
             "ecosystem by layer; the four core components including the one "
             "everybody forgets; the two-cluster architecture, data locality "
             "and why the cloud has weakened it; use cases, and when Hadoop "
             "is the wrong answer."),
            ("Hadoop Distributed File System and YARN",
             "The NameNode and DataNode split, and why the NameNode never "
             "touches your data; block arithmetic and why a block is a "
             "maximum rather than an allocation; the small-files problem "
             "measured; replica placement, rack awareness and what "
             "replication 3 really guarantees; the read and write paths, and "
             "why a pipeline; DataNode and NameNode failure; YARN's four "
             "components and the three schedulers, measured."),
            ("MapReduce and High-Level Tools",
             "The map, shuffle and reduce phases, and why the shuffle is the "
             "only expensive step; combiners, their measured saving and when "
             "one silently gives wrong answers; partitioning and skew; the "
             "three Java details that are examined; Hive as a compiler, "
             "partitioning, bucketing and managed against external tables; "
             "Pig as a dataflow language and its two operators with no SQL "
             "equivalent; Crunch, the abstraction ladder, and why Spark "
             "replaced MapReduce."),
            ("Data Ingestion and Serialization",
             "Sqoop's whole trick in two lines of SQL, split columns and what "
             "skew costs; incremental imports and the deletes they never "
             "catch; Flume's source, channel and sink, back-pressure, channel "
             "durability and the defaults that manufacture the small-files "
             "problem; Avro, Parquet and SequenceFile; schema evolution "
             "demonstrated; column projection and predicate pushdown; batch "
             "and streaming joined, the fan trap, and Lambda against Kappa."),
            ("NoSQL and Ecosystem Enhancements",
             "Why HBase exists and what HDFS cannot do; the sparse sorted-map "
             "model, versions, tombstones and compaction; row-key design and "
             "the hotspot-against-scans trade you cannot escape; HBase "
             "against Hive and against MongoDB; CAP and why HBase is CP; "
             "ZooKeeper's ephemeral and sequential znodes, leader election, "
             "distributed locking and quorum arithmetic; Spark's RDDs, "
             "lineage, lazy evaluation, caching and the HBase integration."),
        ],
    },
    {
        "slug": "cloud-computing",
        "src": "notes/sem-5/course-13b-cloud-computing",
        "number": 13, "year": "III", "sem": "V",
        "title": "Cloud Computing for Data Science",
        "tagline": "Track B. Capacity you no longer need can be given back "
                   "\u2014 and nothing you forget to switch off will switch "
                   "itself off.",
        "blurb": "5 Units + Lab \u2022 Service and deployment models, "
                 "virtualization, cloud storage and warehouses, managed ML "
                 "platforms, training, deployment and monitoring. IAM "
                 "evaluation, a real ETL, a real endpoint.",
        "units": [
            ("Introduction to Cloud Computing",
             "The NIST definition and the sentence underneath it; the "
             "evolution from time-sharing through grid and utility "
             "computing; the five essential characteristics, and how to use "
             "them as a test; SOA, web services and why REST replaced SOAP; "
             "the four-part architecture and the control plane; IaaS, PaaS "
             "and SaaS by what the customer manages; continuous delivery, "
             "blue/green and canary."),
            ("Virtualization and Deployment Models",
             "Why virtualization is what makes the cloud possible; "
             "partitioning, isolation and encapsulation; type 1 against type "
             "2 hypervisors, and containers; the six types of virtualization; "
             "overcommitment measured, and why CPU degrades gracefully while "
             "memory falls off a cliff; public, private, community and "
             "hybrid; the role of the cloud in data science, and what it "
             "does not fix."),
            ("Cloud Storage and Data Management",
             "Block, file and object storage compared on access unit, "
             "sharing and cost; why an object store has no directories and no "
             "rename; storage classes, minimum durations and the retrieval "
             "fees that reverse the discount; egress and data gravity; "
             "backup, archiving, DR and content delivery; key-value "
             "databases and their limitations; batch against streaming; "
             "cloud data warehouses, bytes scanned, and the break-even."),
            ("Cloud Platforms for Data Science and ML",
             "What the cloud changes about machine learning and what it does "
             "not; the benefits and the catch attached to each; AIaaS and "
             "GPUaaS as SaaS and IaaS for particular things; managed "
             "platforms compared \u2014 SageMaker, Azure ML, Vertex AI; the "
             "model registry, feature store and experiment tracking; AutoML "
             "run for real, what it costs, and the seven things it cannot "
             "do."),
            ("Training and Deployment of ML on the Cloud",
             "Choosing a platform \u2014 pipeline support, scale-up against "
             "scale-out, framework support, pre-tuned services; the six "
             "steps and the failure mode at each; the container contract and "
             "why /ping must not run the model; real-time, serverless and "
             "batch inference with cost figures; monitoring, alarming on the "
             "tail, and autoscaling measured honestly; drift, retraining and "
             "case studies."),
        ],
    },
    {
        "slug": "artificial-intelligence",
        "src": "notes/sem-5/course-13a-artificial-intelligence",
        "number": 13, "year": "III", "sem": "V",
        "title": "Artificial Intelligence",
        "tagline": "Track A. The other half of AI \u2014 search and logic, "
                   "where nothing is trained and every answer can be "
                   "explained.",
        "blurb": "5 Units + Lab \u2022 Intelligent agents, uninformed and "
                 "informed search, CSPs, propositional and first-order logic, "
                 "expert systems. 19 Prolog experiments, five of them running "
                 "as real logic programs.",
        "units": [
            ("Introduction to AI and Intelligent Agents",
             "Definition and scope of AI; history, the two winters and the "
             "Turing Test; applications; Weak against Strong AI and Narrow "
             "against General AI; the structure of an agent and what "
             "rationality actually requires; the five agent types; PEAS; and "
             "the six environment properties \u2014 observable, "
             "deterministic, episodic, static, discrete and single-agent."),
            ("Problem Solving \u2014 State Space and Uninformed Search",
             "State space representation and its four components; problem "
             "formulation for the 8-puzzle, water jug and vacuum world; the "
             "general search algorithm and the frontier; completeness, "
             "optimality, time and space complexity; Breadth First, Depth "
             "First and Uniform Cost Search measured against each other on "
             "the Romania map; iterative deepening."),
            ("Informed and Advanced Search Strategies",
             "Heuristics, admissibility and consistency; Greedy Best First "
             "Search and why it is short-sighted; A*, its optimality proof "
             "and what an inadmissible heuristic costs; heuristic dominance; "
             "local search, hill climbing and its local maxima; simulated "
             "annealing and the cooling schedule; genetic algorithms; "
             "constraint satisfaction, backtracking, MRV, degree and LCV."),
            ("Knowledge Representation and Reasoning",
             "Knowledge-based agents and the TELL/ASK interface; "
             "representation issues and the four approaches; propositional "
             "logic syntax, semantics, truth tables, validity, "
             "satisfiability, entailment and inference rules; first order "
             "logic, quantifiers, substitution and unification; forward and "
             "backward chaining and when each is right; resolution, CNF and "
             "proof by refutation."),
            ("Expert Systems, Probabilistic and Emerging AI",
             "Expert system architecture \u2014 knowledge base, working "
             "memory, inference engine and explanation facility \u2014 and "
             "why the explanation falls out of the proof; Bayes theorem and "
             "Bayesian belief networks; fuzzy logic and how degree of truth "
             "differs from probability; NLP basics; robotics; AI ethics, "
             "bias, accountability and societal impact."),
        ],
    },
    {
        "slug": "deep-learning",
        "src": "notes/sem-6/course-14a-deep-learning",
        "number": 14, "year": "III", "sem": "VI",
        "title": "Neural Networks and Deep Learning",
        "tagline": "Track A. Where the features are learned rather than "
                   "chosen \u2014 and what that costs.",
        "blurb": "5 Units + Lab \u2022 Perceptrons, activations, "
                 "backpropagation, CNNs, RNNs, LSTM, attention and "
                 "transformers, transfer learning and AI ethics. Ten of "
                 "twelve experiments run against real MNIST, Fashion-MNIST, "
                 "IMDb and real ImageNet weights.",
        "units": [
            ("Foundations of Deep Learning",
             "AI, machine learning and deep learning as nested sets; the "
             "history from McCulloch\u2013Pitts to the Transformer and what "
             "actually changed in 2012; biological against artificial "
             "neurons and the limits of the analogy; the perceptron, its "
             "learning rule, and a four-line proof that it cannot compute "
             "XOR; linear, ReLU, sigmoid, tanh and softmax with their "
             "derivative bounds; why a stack of linear layers is one linear "
             "layer; the dying ReLU and softmax overflow; MSE against "
             "cross-entropy; gradient descent and backpropagation."),
            ("Deep Neural Networks",
             "Forward propagation and getting every shape right; "
             "backpropagation as the chain rule and why dz = a \u2212 y for "
             "softmax with cross-entropy; the symmetry problem and why He "
             "initialisation uses 2/fan_in; the learning rate as the one "
             "hyperparameter that makes training fail, with the two opposite "
             "failures distinguished; SGD, RMSProp and Adam measured; "
             "overfitting against underfitting; dropout, batch "
             "normalisation, early stopping and why both need a train/eval "
             "mode; MSE, cross-entropy and hinge loss; Keras 3 on any "
             "backend."),
            ("Convolutional Neural Networks",
             "Images, pixels and the channel-order trap; the three "
             "properties convolution has that a dense layer lacks; the "
             "output-size formula and where a classical CNN's parameters "
             "actually live; padding and pooling and what each costs; "
             "measuring whether the learned filters are really edge "
             "detectors, and reporting zero when that is the answer; feature "
             "map sparsity and the layer where it goes the wrong way; "
             "LeNet-5, AlexNet and VGG, and why two 3\u00d73 convolutions "
             "beat one 5\u00d75; classification, detection, segmentation "
             "and face embeddings."),
            ("Recurrent Neural Networks and NLP",
             "Why sequences break a feedforward network; the recurrence and "
             "weight sharing along time; the many-to-one, one-to-many and "
             "many-to-many patterns; the vanishing gradient as arithmetic, "
             "stated precisely enough to say that 3e-151 is not zero; LSTM "
             "gates, the additive cell path, and the forget-gate bias of 1; "
             "GRU; RNN against LSTM against GRU measured on both a "
             "constructed dataset and real IMDb, and why the gap narrows; "
             "Word2Vec, GloVe and the biases embeddings inherit; contextual "
             "embeddings and BERT; character-level generation and "
             "temperature."),
            ("Advanced and Emerging Topics",
             "Scaled dot-product attention worked through on checkable "
             "numbers; why the scores are divided by \u221ad_k, measured "
             "against softmax saturation; multi-head attention and the "
             "encoder block; positional encoding and an honest null "
             "ablation; attention weights scored against a known ground "
             "truth, and why 92.5% is not an explanation; the O(T\u00b2) "
             "cost and context length; BERT against GPT; transfer learning "
             "on real ImageNet weights, including the two results that "
             "contradict the usual story; GANs and mode collapse; VAEs; "
             "bias, the three incompatible fairness definitions, privacy, "
             "safety and explainability."),
        ],
    },
    {
        "slug": "time-series",
        "src": "notes/sem-6/course-14b-time-series",
        "number": 14, "year": "III", "sem": "VI",
        "title": "Time Series Analysis and Forecasting",
        "tagline": "Track B. Where the observations are not independent, and "
                   "that single fact breaks almost every method you know.",
        "blurb": "5 Units + Lab \u2022 Stationarity, ACF and PACF, ARMA, "
                 "ARIMA and SARIMA, model selection, prediction intervals, "
                 "VAR and Granger causality, Kalman filtering, spectral "
                 "analysis and forecast evaluation. Every one of the 13 "
                 "experiments runs.",
        "units": [
            ("Fundamentals and Stationary Processes",
             "Why a random split lets a model see the future, and which of "
             "your habits from Courses 4, 8 and 12 A stop being valid; time "
             "series types, components and the forecasting process; "
             "stationarity defined; autocovariance, ACF and PACF, and "
             "reading them together to identify a model; decomposition into "
             "trend, seasonal and residual, classical against STL, checked "
             "against known coefficients."),
            ("ARMA and Forecasting",
             "AR, MA and ARMA(p,q) definitions and their signatures in the "
             "ACF and PACF; estimation, and a 200-draw Monte Carlo showing "
             "the estimator unbiased when a single fit misses; AIC and BIC "
             "against rolling-origin cross-validation, and what to do when "
             "they disagree; Ljung\u2013Box residual diagnostics; "
             "forecasting from an ARMA and where the intervals come from."),
            ("Non-Stationary and Seasonal Models",
             "Differencing, the ADF and KPSS tests, and using the ct "
             "regression to tell a trend-stationary series from a random "
             "walk; over-differencing measured as a variance increase; "
             "ARIMA and SARIMA with seasonal orders; the airline model; "
             "prediction intervals and a measured coverage of 75% against a "
             "nominal 95%."),
            ("Multivariate and State-Space Models",
             "Vector autoregression on a macro system built with known "
             "causality; Granger causality tested in all four directions; "
             "state-space form and the Kalman filter through unobserved "
             "components; what a zero variance estimate means; spectral "
             "analysis and the periodogram, and why detrending first "
             "changes the answer."),
            ("Forecast Evaluation and Comparison",
             "ARIMA against exponential smoothing against machine learning "
             "on the same series; naive and seasonal-naive baselines; RMSE, "
             "MAE, MAPE and MASE, and the cases where they disagree; why "
             "MAPE reaches 75% on a uniform error of 1.0; recursive "
             "forecasting and a measured result that contradicts the "
             "textbook; tree models that cannot extrapolate; testing a "
             "forecast for bias."),
        ],
    },
    {
        "slug": "nlp",
        "src": "notes/sem-6/course-15a-nlp",
        "number": 15, "year": "III", "sem": "VI",
        "title": "Natural Language Processing",
        "tagline": "Track A. Turning text into numbers without throwing away "
                   "what it means.",
        "blurb": "5 Units + Lab \u2022 Ambiguity and regular expressions, "
                 "tokenization, stemming and lemmatization, grammars and "
                 "parsing, named entity recognition, embeddings, "
                 "classification, RNNs and transformers. Eleven of fourteen "
                 "experiments run against real NLTK corpora and real spaCy "
                 "models, every result scored against hand-labelled truth.",
        "units": [
            ("Introduction to NLP and Language Fundamentals",
             "What NLP is and the three properties that make language hard; "
             "the levels of analysis from phonology to discourse; "
             "applications, and why spam detection is adversarial; lexical, "
             "structural and contextual ambiguity told apart, with WordNet "
             "sense counts and actual parse trees; garden-path sentences; "
             "NLTK against spaCy and when to use each; regular expressions "
             "scored against hand-labelled truth, greedy against lazy "
             "quantifiers, and where a regex stops being the right tool."),
            ("Text Preprocessing and Linguistic Analysis",
             "Morphology, lexicon, orthographic rules; inflectional against "
             "derivational morphology; finite state transducers and why "
             "bidirectionality matters; sentence and word tokenization, and "
             "why two trained tokenisers disagree; stopword removal measured "
             "on the Brown corpus, and the sentences it destroys; stemming "
             "against lemmatization on 'ran', 'better' and "
             "'university'/'universal'; context-free grammars and the "
             "Chomsky hierarchy; top-down, bottom-up and chart parsing; why "
             "left recursion kills a top-down parser; CYK and its "
             "O(n\u00b3); semantic analysis and meaning representation."),
            ("Information Extraction and Representation",
             "Named entity recognition, the BIO scheme, and spaCy scored "
             "against thirteen hand-assigned labels \u2014 including the "
             "two Indian state names it gets wrong and the gazetteer that "
             "fixes them; bag of words, TF-IDF and what IDF actually is; "
             "n-grams and the word order unigrams cannot see; the "
             "measurement where counts rank an unrelated document above a "
             "paraphrase; the distributional hypothesis, CBOW against "
             "skip-gram, negative sampling, GloVe; the classification "
             "pipeline and why the vectoriser is fitted on train only; "
             "comparing a model gap against the cross-validation spread; "
             "the ethics of preprocessing."),
            ("Deep Learning for NLP",
             "Why sequences break feedforward networks; RNN against CNN for "
             "text; the vanishing gradient as arithmetic, stated precisely "
             "enough to say that 3e-151 is not zero; LSTM gates and the "
             "additive cell path; GRU; the LSTM-RNN gap measured on both a "
             "constructed dataset and real IMDb, and why it narrows; "
             "perplexity and what value means no better than guessing; "
             "temperature; the O(T\u00b2) cost and why parallelism won; "
             "BERT against GPT; what pre-training buys, measured by "
             "training the small version; subword tokenization and the "
             "Hugging Face ecosystem."),
            ("Transformers and Modern NLP",
             "Self-attention worked on checkable numbers; why the scores "
             "are divided by \u221ad_k, measured against softmax "
             "saturation; multi-head attention, the encoder block, "
             "residuals and layer norm; positional encoding; "
             "encoder-decoder and what cross-attention does; BERT's "
             "pretraining, the full masking recipe including the 10% random "
             "and 10% unchanged, and why NSP was dropped; fine-tuning; GPT "
             "and hallucination; extractive, abstractive and hybrid "
             "summarization, the lead-3 baseline, and why regulated domains "
             "stay extractive; document classification, retrieval against "
             "generative chatbots, and the threshold every retrieval bot "
             "needs."),
        ],
    },
    {
        "slug": "mlops",
        "src": "notes/sem-6/course-15b-mlops",
        "number": 15, "year": "III", "sem": "VI",
        "title": "Data Engineering and MLOps",
        "tagline": "Track B. Every other course ends when the model works. "
                   "This one starts there.",
        "blurb": "5 Units + Lab \u2022 The data engineering lifecycle, "
                 "architecture and distributed systems, MLOps fundamentals, "
                 "deployment and CI/CD, monitoring and governance. Eleven of "
                 "sixteen experiments run against the real tools \u2014 "
                 "MLflow, git and DVC, a Flask server on a real socket, and "
                 "a drift detector scored against injected drift.",
        "units": [
            ("Foundations of Data Engineering",
             "What data engineering is, and why 'systems' and 'maintenance' "
             "are the load-bearing words; the activities from ingestion to "
             "monitoring; the data lifecycle against the data ENGINEERING "
             "lifecycle, with the five undercurrents and why they are drawn "
             "underneath; the evolution of the role; ETL against ELT and why "
             "ELT won; technical against business responsibilities, internal "
             "against external; how data engineering relates to data "
             "science, in both directions; and the measured demonstration "
             "that a pipeline reporting a 1% error is more dangerous than "
             "one that crashes."),
            ("Data Architecture and Distributed Systems",
             "Enterprise, data and solution architecture; the principles of "
             "good architecture and why reversibility deserves your design "
             "effort; availability, reliability, RTO and RPO, with what each "
             "nine actually costs; tiers; monolith against microservices "
             "MEASURED, including the honest admission that microservices "
             "are slower and the one-database-per-service cost; "
             "event-driven architecture and batch against streaming "
             "ingestion measured at a 160x latency difference; dead-letter "
             "queues; hybrid cloud, multicloud and edge; and TCO, where the "
             "licence fee is rarely the largest line."),
            ("MLOps Fundamentals",
             "How MLOps differs from DevOps \u2014 code, data and model "
             "versioned together; training/serving skew and its "
             "architectural fix; data leakage and the three ways it happens; "
             "EDA, feature engineering and recording the base rate first; "
             "experiment tracking with real MLflow, and why the train/test "
             "gap belongs in the table; the four things that must be pinned "
             "for reproducibility, with the split's random_state "
             "demonstrated as the one people forget; model versioning; what "
             "DVC stores in git and what it does not; Responsible AI "
             "controls and what breaks at each scale."),
            ("Model Deployment and CI/CD Pipelines",
             "What production-ready means concretely, and why returning 400 "
             "with a reason matters more than the model; dev, staging and "
             "production, and putting the differences in configuration; "
             "CI/CD for ML including the two stages with no software "
             "equivalent \u2014 data validation and the metric gate; why a "
             "non-deterministic pipeline makes CI meaningless; batch, "
             "online, streaming and embedded deployment; canary, blue-green, "
             "A/B and shadow releases; the seven Docker traps; layer caching "
             "and image size; and Kubernetes readiness against liveness "
             "probes."),
            ("Monitoring, Feedback Loops and Governance",
             "Data, concept and label drift told apart, and the asymmetry "
             "that only one is detectable early; PSI and the KS test scored "
             "against drift injected at a known magnitude \u2014 4 of 5 "
             "batches caught with no false alarms and a one-batch lag; why "
             "statistical significance is not operational significance; "
             "ground truth evaluation and the partial-label feedback trap; "
             "the seven-step retraining loop and the step that must stay "
             "human; metrics against logs, the four Prometheus types, and "
             "why latency needs a histogram; GDPR, CCPA, GxP and the EU AI "
             "Act; why Article 17 breaks trained models; fairness measured "
             "with a control condition; and a model risk management "
             "template."),
        ],
    },
]

EXTRA_PAGES = {
    "practice.md": ("practice", "PRACTICE",
                    "Exam-style questions with fully worked solutions."),
    "lab.md": ("lab", "LAB",
               "Every prescribed lab experiment, with code and expected output."),
    "formula-sheet.md": ("formula-sheet", "REFERENCE",
                         "Every formula from the five units on one page for revision."),
}

TOP_PAGES = [
    ("SYLLABUS-REVIEW.md", "syllabus-review", "Syllabus Review",
     "Thirty-three findings from checking the four official syllabus "
     "documents."),
    ("SYLLABUS-MAP.md", "syllabus-map", "Syllabus Map",
     "Programme structure for Semesters I–VI, elective tracks and unit topics."),
    ("STUDY-PLAN.md", "study-plan", "Study Plan",
     "Week-by-week schedule, revision cycles and a progress checklist."),
    ("data/README.md", "practice-data", "Practice Data",
     "Fifty CSV datasets, one per method, each generated from a known truth."),
    ("data/PRACTICE-QUESTIONS.md", "practice-questions", "Practice Questions",
     "266 questions across those datasets, graded warm-up to stretch, with a "
     "computed answer key."),
]


# --------------------------------------------------------------------------
# Markdown -> HTML
# --------------------------------------------------------------------------

QUESTION_RE = re.compile(
    r"^###\s+(?:(?:Q|Problem\s+)?\d+[.)]?|Q\d+)\b.*$|^###\s+.*\?\s*$")
# the short-answer sections write questions as a wholly bold numbered
# paragraph -- '**3. Define a primary key.**' -- rather than as a heading
BOLD_QUESTION_RE = re.compile(r"^\*\*\d+\.\s.+\*\*\s*$")
SOLUTION_RE = re.compile(r"^\*\*(Solution|Answer)\b[^*]*\*\*[.:]?\s*$", re.I)


def collapse_practice_answers(md_text):
    """On a practice page, hide each answer behind a 'Show answer' toggle.

    A practice question whose answer sits directly beneath it is not practice
    -- the eye reaches the answer before the student has tried anything. Three
    of the nineteen courses wrote their solutions inside <details> by hand;
    this gives the other sixteen the same behaviour without touching the
    markdown, so the files stay readable on GitHub.

    Two source shapes are handled:
      * '### 3. Distinguish slice from dice.' followed straight by the answer
      * '### Problem 1 — ...', the question, then '**Solution.**'
    In the second, the question stays visible and only the solution folds.
    """
    # the three courses that wrote <details> by hand need the same attribute,
    # or their answers render as raw markdown too
    md_text = re.sub(r"<details(?![^>]*markdown=)", '<details markdown="1"',
                     md_text)
    lines = md_text.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        bold_q = BOLD_QUESTION_RE.match(line.strip())
        if not (QUESTION_RE.match(line) or bold_q):
            out.append(line)
            i += 1
            continue

        out.append(line)
        i += 1
        block = []
        while i < len(lines):
            nxt = lines[i]
            if nxt.startswith(("## ", "### ")):
                break
            if bold_q and BOLD_QUESTION_RE.match(nxt.strip()):
                break
            block.append(nxt)
            i += 1

        # already collapsed by hand, or nothing to collapse
        if any("<details" in b for b in block) or not any(b.strip() for b in block):
            out.extend(block)
            continue

        split = next((n for n, b in enumerate(block) if SOLUTION_RE.match(b.strip())),
                     None)
        if split is None:
            question, answer = [], block
        else:
            question, answer = block[:split], block[split + 1:]

        out.extend(question)
        if question and question[-1].strip():
            out.append("")
        # markdown="1" is what makes the md_in_html extension render the
        # markdown INSIDE the element. Without it the answer is emitted
        # verbatim and the reader sees raw pipes and asterisks.
        out.append('<details markdown="1">')
        out.append("<summary>Show answer</summary>")
        out.append("")
        out.extend(answer)
        out.append("")
        out.append("</details>")
        out.append("")
    return "\n".join(out)


def add_anchors_and_toc(body_html, min_sections=4):
    """Give every h2/h3 an id, and prepend an 'On this page' contents list.

    A unit page runs to two and a half thousand words with fifteen sections
    and, until now, one id on the whole document. A student could not see the
    shape of the page, could not jump to the part they were stuck on, and
    could not link a classmate to it. Both problems are the same missing
    attribute.

    The contents list is a <details>, closed by default, so it costs one line
    of vertical space on a phone and expands to the full map on a laptop.
    """
    used = {}

    def slug(text):
        base = re.sub(r"<[^>]+>", "", text)
        base = html.unescape(base)
        base = re.sub(r"[^\w\s-]", "", base).strip().lower()
        base = re.sub(r"[\s_]+", "-", base) or "section"
        used[base] = used.get(base, 0) + 1
        return base if used[base] == 1 else f"{base}-{used[base]}"

    sections = []
    subsections = []

    def tag(m):
        level, attrs, text = m.group(1), m.group(2) or "", m.group(3)
        if "id=" in attrs:
            return m.group(0)
        anchor = slug(text)
        target = sections if level == "2" else subsections
        target.append((anchor, re.sub(r"<[^>]+>", "", text)))
        return f'<h{level}{attrs} id="{anchor}">{text}</h{level}>'

    body_html = re.sub(r"<h([23])([^>]*)>(.*?)</h\1>", tag, body_html,
                       flags=re.S)

    # A practice page is three h2 headings over fifty questions, so a contents
    # list built from h2 alone would say "Section A, Section B, Section C" and
    # help nobody. Where the h2 headings are too few to be a map, list the h3
    # headings instead -- those are the questions, and jumping to question 31
    # is the thing a reader actually wants.
    if len(sections) < min_sections:
        if len(subsections) < 2 * min_sections:
            return body_html
        sections = subsections

    # `t` came out of the rendered HTML, so it is already escaped -- escaping
    # it again turns <!DOCTYPE html> into &amp;lt;!DOCTYPE html&amp;gt; in the
    # contents list. Unescape first, then escape once.
    items = "\n".join(
        f'    <li><a href="#{a}">{html.escape(html.unescape(t))}</a></li>'
        for a, t in sections)
    toc = ('<details class="toc">\n'
           '  <summary>On this page</summary>\n'
           f'  <ol>\n{items}\n  </ol>\n'
           '</details>\n')
    return toc + body_html


def render_markdown(text):
    """Convert Markdown to HTML with the extensions the notes rely on."""
    md = markdown.Markdown(extensions=[
        "tables", "fenced_code", "sane_lists", "attr_list", "md_in_html",
    ])
    return md.convert(text)


def strip_first_heading(text):
    """Remove the leading '# Title' so it is not repeated under the banner."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            return line[2:].strip(), "\n".join(lines[i + 1:])
    return None, text


def unlink(label, target):
    """Drop a link, keeping its text as an inline-code path.

    Used for anything that is not a generated page. A reader following one of
    these on the published site was taken OUT of the study material and into
    a code browser or a raw file download -- the same failure the .md links
    had. The path is still worth naming, so it stays as text; it simply is
    not a link any more.
    """
    text = label.strip()
    if not text:
        text = target
    # `labs/course-7-web/` already reads as a path; a bare word does not
    if not (text.startswith("`") and text.endswith("`")):
        if "/" in text or "." in text.rsplit("/", 1)[-1]:
            text = f"`{text}`"
    return text


def rewrite_links(body, link_map, src_dir, out_dir):
    """Retarget the Markdown's relative links for the generated page.

    Only one case still produces a link: a .md file that becomes a page gets
    its generated .html sibling. Everything else -- a repository directory, a
    lab source file, a .md file with no page -- is UNLINKED and left as text.

    Those used to point at github.com or at the raw file. Both took the
    reader off the site: GitHub Pages serves files rather than directory
    listings, so a relative directory link 404s, and a relative link to a .py
    or .c file hands over source code the browser cannot render. A study page
    should not be a doorway into a code host.
    """
    def repl(m):
        label, target, frag = m.group(1), m.group(2), m.group(3) or ""

        key = pathlib.PurePosixPath(target).name
        if key in link_map:
            return f'[{label}]({link_map[key]}{frag})'

        resolved = (src_dir / target).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            return m.group(0)          # not ours -- leave it alone

        return unlink(label, target)

    return re.sub(r'\[([^\]]*)\]\(([^)#\s]+)(#[^)\s]*)?\)', repl, body)


# --------------------------------------------------------------------------
# Composition: map the notes' recurring structure onto the house style's
# semantic boxes, the way Statistics-Major composes its pages by hand.
# --------------------------------------------------------------------------

HEADING = re.compile(r'^(#{2,6})\s')

# Trigger heading -> (css class, label). The notes use a consistent set of
# marker headings, which is what makes this reliable rather than guesswork.
SECTION_BOXES = [
    (re.compile(r'^###\s*🎯\s*(.*)$'),  "concept", "THE BIG IDEA"),
    (re.compile(r'^###\s*📖\s*(.*)$'),  "tip",     "IN DEPTH"),
    (re.compile(r'^###\s*🔢\s*(.*)$'),  "formula", "FORMULA"),
    (re.compile(r'^###\s*💡\s*(.*)$'),  "tip",     "KEY INSIGHT"),
]

PROBLEM_RE = re.compile(r'^###\s+(Problem\s+\d+|Q\d+)\b(.*)$')
WORKED_RE = re.compile(
    r'^(?:\*\*|\*)(Worked example|Worked solution|Worked examples|Example|Trace)'
    r'([^*]*)(?:\*\*|\*)[.:]?')

# "## Worked example — trace the output" style headings.
WORKED_HEADING_RE = re.compile(
    r'^#{2,4}\s+(Worked example|Example)\b\s*[—-]?\s*(.*)$', re.I)

# "A **linked list** is ..." / "The **control unit** performs ..." -- the
# notes' definition sentences, which Statistics-Major would set as .concept.
DEFINITION_RE = re.compile(
    r'^(?:A|An|The)\s+\*\*([^*]{2,60})\*\*\s+(?:is|are|means|refers to)\b')

# Bolded rhetorical lead-ins that explain rather than define.
INSIGHT_RE = re.compile(
    r'^\*\*(Why|The point|Rule|Remember|Note|Careful|Key)\b[^*]*\*\*')


def _capture(lines, start, stop_levels=(2, 3)):
    """Return (block, next_index): lines until the next qualifying heading."""
    out = []
    i = start
    while i < len(lines):
        line = lines[i]
        m = HEADING.match(line)
        if m and len(m.group(1)) in stop_levels:
            break
        if line.strip() == "---":
            break
        out.append(line)
        i += 1
    return out, i


def _box(cls, label, title, body_lines):
    """Emit a house-style box, matching Statistics-Major's markup.

    The label is a SIBLING of the content, not part of its first paragraph --
    a blank line after it is what keeps Python-Markdown from absorbing the
    following list or paragraph into the same block.

    Blockquote markers are stripped from the body: the box already provides
    the visual container, so a quoted formula inside a .formula section would
    otherwise be boxed twice.
    """
    body = [re.sub(r'^>\s?', '', ln) for ln in body_lines]
    inner = "\n".join(body).strip("\n")

    parts = [f'<div class="{cls}" markdown="1">', f'<span class="label">{label}</span>', '']
    if title:
        parts += [f'#### {title}', '']
    parts += [inner, '</div>', '']
    return parts


def _is_formula_quote(text):
    """A blockquote that states a formula rather than making a remark."""
    if len(text) > 420:
        return False
    mathy = sum(text.count(c) for c in "=Σ∫√±×÷≤≥≠∞µσ²³")
    return "=" in text and mathy >= 1


LIST_START = re.compile(r'^\s{0,3}(?:[-*+]\s+|\d{1,3}[.)]\s+)\S')


def normalise_lists(md_text):
    """Insert the blank line Python-Markdown needs before a list.

    GitHub's renderer accepts a list that starts on the line straight after a
    paragraph; Python-Markdown treats it as lazy continuation and leaves the
    dashes as literal text. The notes are written in the GitHub style, so
    normalise here rather than editing 41 source files.
    """
    lines = md_text.split("\n")
    out = []
    in_fence = False
    for idx, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if (not in_fence and LIST_START.match(line) and out
                and out[-1].strip()
                and not LIST_START.match(out[-1])
                and not out[-1].lstrip().startswith((">", "|", "#"))
                and not out[-1].rstrip().endswith(("|",))):
            out.append("")
        out.append(line)
    return "\n".join(out)


def promote_markdown_boxes(md_text):
    """Wrap recognised sections in .concept / .formula / .example / .tip."""
    md_text = normalise_lists(md_text)
    lines = md_text.split("\n")
    out = []
    i = 0
    in_fence = False

    while i < len(lines):
        line = lines[i]

        # Never rewrite anything inside a fenced code block.
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue
        if in_fence:
            out.append(line)
            i += 1
            continue

        # --- marker headings: 🎯 big idea, 📖 story, 🔢 formula, 💡 insight ---
        matched = False
        for rx, cls, label in SECTION_BOXES:
            m = rx.match(line)
            if m:
                title = m.group(1).strip() or None
                # Drop a redundant title that just repeats the label.
                if title and title.lower().strip(' "') in {
                        "the big idea", "the story", "the formula",
                        'the "aha!" moment'}:
                    title = None
                body, i = _capture(lines, i + 1, stop_levels=(2, 3))
                out += _box(cls, label, title, body)
                matched = True
                break
        if matched:
            continue

        # --- practice problems become worked examples ---
        m = PROBLEM_RE.match(line)
        if m:
            label = m.group(1).upper()
            title = m.group(2).strip(" —-").strip() or None
            body, i = _capture(lines, i + 1, stop_levels=(2, 3))
            out += _box("example", label, title, body)
            continue

        # --- inline "**Worked example.**" paragraphs ---
        wm = WORKED_RE.match(line)
        if wm:
            qualifier = (wm.group(2) or "").strip(" ().:")
            label = "WORKED EXAMPLE"
            if wm.group(1).lower().startswith("trace"):
                label = "TRACE"
            rest = line[wm.end():].strip()
            body, i = _capture(lines, i + 1, stop_levels=(2, 3))
            if rest:
                body = [rest] + body
            out += _box("example", label, qualifier or None, body)
            continue

        # --- "## Worked example — ..." headings ---
        m = WORKED_HEADING_RE.match(line)
        if m:
            title = m.group(2).strip() or None
            body, i = _capture(lines, i + 1, stop_levels=(2, 3))
            out += _box("example", "WORKED EXAMPLE", title, body)
            continue

        # --- definition sentences become .concept, as on Statistics-Major ---
        if DEFINITION_RE.match(line):
            body = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and \
                    not HEADING.match(lines[i]) and \
                    not lines[i].lstrip().startswith(("```", ">", "|", "-", "*", "1.")):
                body.append(lines[i])
                i += 1
            out += _box("concept", "DEFINITION", None, body)
            continue

        # --- explanatory lead-ins become .tip ---
        if INSIGHT_RE.match(line):
            body = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and \
                    not HEADING.match(lines[i]) and \
                    not lines[i].lstrip().startswith(("```", ">", "|")):
                body.append(lines[i])
                i += 1
            out += _box("tip", "WHY IT MATTERS", None, body)
            continue

        # --- blockquotes ---
        if line.startswith(">"):
            block = []
            while i < len(lines) and (lines[i].startswith(">") or
                                      (lines[i].strip() == "" and
                                       i + 1 < len(lines) and
                                       lines[i + 1].startswith(">"))):
                block.append(re.sub(r'^>\s?', '', lines[i]))
                i += 1
            text = "\n".join(block).strip()
            if "examined but" in text.lower():
                cls, label = "warn", "EXAMINED BUT NOT IN THE SYLLABUS"
            elif "⚠" in text:
                # ⚠ marks a trap or a common mistake, which is almost never a
                # syllabus gap -- labelling all of them as one told students
                # that correct, examinable material was off-syllabus
                cls, label = "warn", "WATCH OUT"
            elif _is_formula_quote(text):
                cls, label = "formula", "FORMULA"
            else:
                cls, label = "tip", "NOTE"
            out += _box(cls, label, None, block)
            continue

        # --- "Mistakes that cost marks" list becomes a warning ---
        if re.match(r'^##\s+Mistakes that cost marks\s*$', line):
            out.append(line)
            i += 1
            body, i = _capture(lines, i, stop_levels=(2,))
            out += _box("warn", "COMMON ERRORS", None, body)
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


def promote_boxes(html_text):
    """Map Markdown constructs onto the house style's semantic boxes."""
    # Any blockquote that survived promote_markdown_boxes (e.g. nested inside
    # a list) still gets the house .tip treatment rather than browser default.
    html_text = re.sub(
        r'<blockquote>\s*(.*?)\s*</blockquote>',
        r'<div class="tip"><span class="label">NOTE</span>\n\1\n</div>',
        html_text, flags=re.S)

    # Review-finding references (finding D1, finding **D2**, ...) get a chip.
    html_text = re.sub(
        r'finding\s+(?:<strong>)?\*{0,2}(D\d{1,2})\*{0,2}(?:</strong>)?',
        r'finding <span class="finding">\1</span>', html_text)

    # Left-align the first column of every table -- the house style centres
    # all cells, which suits numeric tables but not topic listings.
    html_text = html_text.replace("<table>", '<table class="main-table">')
    return html_text


def chips_from_headings(body_md, limit=12):
    """Build the .chips topic row from the page's H2 headings."""
    chips = []
    for line in body_md.splitlines():
        if line.startswith("## "):
            t = line[3:].strip()
            # drop numbering prefixes: "1.2 ", "A.1 ", "5.10 "
            t = re.sub(r'^[A-Z]?\d*(\.\d+)*\s+', '', t)
            t = re.sub(r'^(Part\s+[A-Z]\s*[—-]\s*)', '', t)
            t = re.sub(r'[*`]', '', t)
            t = t.split("—")[0].split(" - ")[0].strip()
            if t and t.lower() not in {c.lower() for c in chips}:
                chips.append(t)
    return chips[:limit]


def page(title, banner_title, banner_sub, crumbs, body, css_prefix="",
         mathjax=False, mermaid=False, chips=None, nav=None, footer=""):
    """Assemble one page in the Statistics-Major house layout."""
    head_extra = "\n".join(x for x in
                           [MATHJAX if mathjax else "",
                            ] if x)
    chip_html = ""
    if chips:
        spans = "\n    ".join(f'<span class="chip">{html.escape(c)}</span>'
                              for c in chips)
        chip_html = f'  <h2>Topics Covered</h2>\n  <div class="chips">\n    {spans}\n  </div>\n\n'

    nav_html = ""
    if nav:
        links = "\n    ".join(f'<a href="{href}">{html.escape(label)}</a>'
                              for label, href in nav)
        nav_html = f'  <div class="page-nav">\n    {links}\n  </div>\n\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{css_prefix}css/styles.css">
{head_extra}
</head>
<body>
<div class="wrapper">

  <div class="banner">
    <div class="crumbs">{crumbs}</div>
    <h1>{html.escape(banner_title)}</h1>
    <p>{banner_sub}</p>
  </div>

{chip_html}{body}

{nav_html}  <footer>{footer}</footer>
</div>
{MERMAID if mermaid else ""}
</body>
</html>
"""

# --------------------------------------------------------------------------
# Builders
# --------------------------------------------------------------------------

def build_course(course, link_map):
    """Render one course: its landing page plus every unit and extra page."""
    slug = course["slug"]
    src = ROOT / course["src"]
    out_dir = ROOT / slug
    out_dir.mkdir(exist_ok=True)
    written = []

    unit_files = sorted(src.glob("unit-*.md"),
                        key=lambda p: int(re.search(r'\d+', p.stem).group()))

    # ---- unit pages ----
    for idx, md_path in enumerate(unit_files, start=1):
        raw = md_path.read_text()
        heading, body_md = strip_first_heading(raw)
        unit_title, unit_desc = course["units"][idx - 1]

        body_md = rewrite_links(body_md, link_map, src, out_dir)
        body = add_anchors_and_toc(
            promote_boxes(render_markdown(promote_markdown_boxes(body_md))))

        nav = [("← Course home", f"index_{slug}.html")]
        if idx > 1:
            prev_title = course["units"][idx - 2][0]
            nav.append((f"← Unit {idx - 1}", f"unit{idx - 1}_{slug}.html"))
        if idx < len(unit_files):
            next_title = course["units"][idx][0]
            nav.append((f"Next: Unit {idx + 1} — {next_title} →",
                        f"unit{idx + 1}_{slug}.html"))

        out = out_dir / f"unit{idx}_{slug}.html"
        out.write_text(page(
            title=f"Unit {idx} — {unit_title} | {course['title']}",
            banner_title=f"Unit {idx} — {unit_title}",
            banner_sub=html.escape(unit_desc),
            crumbs=f'<a href="../index.html">Home</a> &raquo; '
                   f'<a href="index_{slug}.html">{html.escape(course["title"])}</a> '
                   f'&raquo; Unit {idx}',
            body=body,
            css_prefix="../",
            mathjax=True,
            mermaid="```mermaid" in raw,
            chips=chips_from_headings(body_md),
            nav=nav,
            footer=f"Unit {idx} — {html.escape(unit_title)} • "
                   f"Course {course['number']}, Semester {course['sem']}",
        ))
        written.append(out)

    # ---- practice / lab / formula-sheet ----
    extras = []
    for fname, (out_slug, tag, desc) in EXTRA_PAGES.items():
        md_path = src / fname
        if not md_path.exists():
            continue
        raw = md_path.read_text()
        heading, body_md = strip_first_heading(raw)
        body_md = rewrite_links(body_md, link_map, src, out_dir)
        if fname == "practice.md":
            body_md = collapse_practice_answers(body_md)
        body = add_anchors_and_toc(
            promote_boxes(render_markdown(promote_markdown_boxes(body_md))))

        out = out_dir / f"{out_slug}_{slug}.html"
        out.write_text(page(
            title=f"{heading or tag} | {course['title']}",
            banner_title=heading or tag.title(),
            banner_sub=html.escape(desc),
            crumbs=f'<a href="../index.html">Home</a> &raquo; '
                   f'<a href="index_{slug}.html">{html.escape(course["title"])}</a> '
                   f'&raquo; {tag.title()}',
            body=body,
            css_prefix="../",
            mathjax=True,
            mermaid="```mermaid" in raw,
            nav=[("← Course home", f"index_{slug}.html")],
            footer=f"{tag.title()} • Course {course['number']} — "
                   f"{html.escape(course['title'])}",
        ))
        written.append(out)
        extras.append((out_slug, tag, desc, out.name))

    # ---- course landing page ----
    readme = src / "README.md"
    intro_html = ""
    if readme.exists():
        raw = readme.read_text()
        _, body_md = strip_first_heading(raw)
        # Keep the prose above the unit table; the cards below replace it.
        body_md = re.split(r'^## Units\b', body_md, flags=re.M)[0]
        body_md = rewrite_links(body_md, link_map, src, out_dir)
        intro_html = promote_boxes(render_markdown(promote_markdown_boxes(body_md)))

    cards = []
    for idx, (unit_title, unit_desc) in enumerate(course["units"], start=1):
        cards.append(
            f'    <a class="unit-card" href="unit{idx}_{slug}.html">\n'
            f'      <span class="tag">UNIT {idx}</span>\n'
            f'      <h3>{html.escape(unit_title)}</h3>\n'
            f'      <p>{html.escape(unit_desc)}</p>\n'
            f'    </a>')
    for out_slug, tag, desc, fname in extras:
        cards.append(
            f'    <a class="unit-card" href="{fname}">\n'
            f'      <span class="tag">{tag}</span>\n'
            f'      <h3>{html.escape(out_slug.replace("-", " ").title())}</h3>\n'
            f'      <p>{html.escape(desc)}</p>\n'
            f'    </a>')

    body = (intro_html
            + '\n  <h2>Units in this Course</h2>\n  <div class="unit-grid">\n\n'
            + "\n\n".join(cards)
            + '\n\n  </div>\n')
    # Course landing pages were short when this site was built. They are not
    # any more -- several now run to nine sections -- so they get the same
    # contents list every other generated page has.
    body = add_anchors_and_toc(body)

    out = out_dir / f"index_{slug}.html"
    out.write_text(page(
        title=f"{course['title']} — Complete Study Material",
        banner_title=course["title"],
        banner_sub=f"B.Sc. (Hons) Data Science — Year {course['year']}, "
                   f"Semester {course['sem']}, Course {course['number']}",
        crumbs='<a href="../index.html">Home</a> &raquo; '
               f'Course {course["number"]}',
        body=body,
        css_prefix="../",
        mathjax=True,
        nav=[("← All courses", "../index.html")],
        footer=f"Course {course['number']} — {html.escape(course['title'])}",
    ))
    written.append(out)
    return written


def build_top_pages(link_map):
    """Render the three repository-level documents."""
    written = []
    for fname, out_slug, title, desc in TOP_PAGES:
        md_path = ROOT / fname
        if not md_path.exists():
            continue
        raw = md_path.read_text()
        heading, body_md = strip_first_heading(raw)
        body_md = rewrite_links(body_md, link_map, ROOT, ROOT)
        body = promote_boxes(render_markdown(promote_markdown_boxes(body_md)))
        # These are the longest documents on the site -- the study plan runs
        # to twelve sections and the question sets to twenty -- and until now
        # they were the only generated pages with no anchors and no contents
        # list, so there was no way to jump or to link a classmate to one.
        body = add_anchors_and_toc(body)

        out = ROOT / f"{out_slug}.html"
        out.write_text(page(
            title=f"{title} | Data Science Major 2025",
            banner_title=heading or title,
            banner_sub=html.escape(desc),
            crumbs='<a href="index.html">Home</a> &raquo; ' + html.escape(title),
            body=body,
            css_prefix="",
            mathjax=True,
            nav=[("← Home", "index.html")],
            footer="Model Syllabus for B.Sc. (Data Science) Major, "
                   "AY&nbsp;2025-26",
        ))
        written.append(out)
    return written


def build_link_map():
    """Map every source .md filename to the page it becomes."""
    link_map = {}
    for course in COURSES:
        slug = course["slug"]
        for idx in range(1, 6):
            link_map[f"unit-{idx}.md"] = f"unit{idx}_{slug}.html"
        for fname, (out_slug, _, _) in EXTRA_PAGES.items():
            link_map[fname] = f"{out_slug}_{slug}.html"
        link_map["README.md"] = f"index_{slug}.html"
    for fname, out_slug, _, _ in TOP_PAGES:
        link_map[fname] = f"{out_slug}.html"
    return link_map


def main():
    written = []

    # Course-local link maps: unit-3.md means a different page in each course,
    # so rebuild the map per course rather than sharing one.
    for course in COURSES:
        slug = course["slug"]
        lm = {}
        for idx in range(1, 6):
            lm[f"unit-{idx}.md"] = f"unit{idx}_{slug}.html"
        for fname, (out_slug, _, _) in EXTRA_PAGES.items():
            lm[fname] = f"{out_slug}_{slug}.html"
        lm["README.md"] = f"index_{slug}.html"
        for fname, out_slug, _, _ in TOP_PAGES:
            lm[fname] = f"../{out_slug}.html"
        written += build_course(course, lm)

    top_lm = {fname: f"{out_slug}.html" for fname, out_slug, _, _ in TOP_PAGES}
    written += build_top_pages(top_lm)

    print(f"{len(written)} pages generated")
    for p in sorted(written):
        print(f"  {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
