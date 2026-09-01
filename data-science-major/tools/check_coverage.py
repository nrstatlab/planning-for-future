#!/usr/bin/env python3
"""Check that every syllabus unit topic has corresponding notes.

Cross-checks the unit topic lists extracted from the PDF against the notes
tree, so no topic in the source document goes unaccounted for.

Usage: python3 tools/check_coverage.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Representative keywords per unit, taken from the syllabus topic lists.
# Each must appear somewhere in that unit's notes file.
COVERAGE = {
    "notes/sem-1/course-1-computer-fundamentals/unit-1.md": [
        "binary", "octal", "hexadecimal", "conversion", "evolution",
        "block diagram", "generation", "ALU", "control unit"],
    "notes/sem-1/course-1-computer-fundamentals/unit-2.md": [
        "memory hierarchy", "storage", "microcomputer", "mainframe",
        "supercomputer", "LAN", "WAN", "MAN", "star", "ring", "bus",
        "IP address", "domain name", "browser", "email", "WWW"],
    "notes/sem-1/course-1-computer-fundamentals/unit-3.md": [
        "formatting", "styles", "table", "mail merge", "animation",
        "transition", "resume", "shortcut"],
    "notes/sem-1/course-1-computer-fundamentals/unit-4.md": [
        "cell referencing", "SUM", "AVERAGE", "IF", "COUNT", "chart",
        "sorting", "filtering", "conditional formatting", "LEFT", "RIGHT",
        "MID", "LEN", "TRIM", "CONCAT", "TEXTJOIN", "AND", "OR", "IFERROR",
        "VLOOKUP", "HLOOKUP", "XLOOKUP", "INDEX", "MATCH"],
    "notes/sem-1/course-1-computer-fundamentals/unit-5.md": [
        "conditional formatting", "colour scale", "icon set", "data bar",
        "pivot table", "pivot chart", "data validation", "Goal Seek",
        "Scenario Manager", "data table", "dashboard", "slicer",
        "combo chart", "sparkline", "named range", "freeze panes", "split"],

    "notes/sem-1/course-2-problem-solving-c/unit-1.md": [
        "software", "compiler", "interpreter", "assembly", "flowchart",
        "algorithm", "token", "keyword", "identifier",
        "constant", "data type", "operator", "structure of a c program",
        "history and features",
        "formatted", "unformatted"],
    "notes/sem-1/course-2-problem-solving-c/unit-2.md": [
        "if", "else if", "switch", "while", "for", "do-while", "break",
        "continue", "goto"],
    "notes/sem-1/course-2-problem-solving-c/unit-3.md": [
        "one-dimensional", "two-dimensional", "initialization",
        "memory representation", "string", "string handling",
        "character handling"],
    "notes/sem-1/course-2-problem-solving-c/unit-4.md": [
        "pointer", "pointer arithmetic", "prototype", "return", "nesting",
        "recursion", "by value", "by address", "local", "global",
        "automatic", "extern", "static", "register"],
    "notes/sem-1/course-2-problem-solving-c/unit-5.md": [
        "malloc", "calloc", "realloc", "free", "structure", "nested",
        "array of structures", "union", "text file", "opening", "reading",
        "writing", "closing"],

    "notes/sem-2/course-3-python-data-structures/unit-1.md": [
        "interactive mode", "script mode", "identifier", "keyword",
        "literal", "variable", "operator", "expression", "indentation",
        "bitwise", "identity", "precedence"],
    "notes/sem-2/course-3-python-data-structures/unit-2.md": [
        "elif", "while", "for", "nested loop", "break", "continue",
        "pass", "`else` with a loop", "return", "scope", "default",
        "variable-length", "main()", "docstring", "recursive", "lambda",
        "module", "namespace"],
    "notes/sem-2/course-3-python-data-structures/unit-3.md": [
        "slicing", "immutability", "traversal", "formatting", "list",
        "comprehension", "tuple", "unpacking", "set", "frozenset",
        "dictionar"],
    "notes/sem-2/course-3-python-data-structures/unit-4.md": [
        "file handling", "csv", "pathlib", "syntax error", "exception",
        "try-except", "raise", "user-defined exception", "assertion",
        "class", "object", "constructor", "destructor", "encapsulation",
        "inheritance", "multilevel", "multiple", "overriding"],
    "notes/sem-2/course-3-python-data-structures/unit-5.md": [
        "abstract data", "linked list", "singly", "doubly", "circular",
        "node", "insertion", "deletion", "traversal", "stack", "lifo",
        "queue", "fifo", "priority queue", "tkinter", "widget",
        "event handling"],

    "notes/sem-2/course-4-statistical-foundations/unit-1.md": [
        "uncertain", "axiom", "conditional probability", "mean", "median",
        "mode", "range", "interquartile", "variance", "standard deviation",
        "correlation", "covariance", "histogram", "bar chart",
        "scatter plot", "bayes"],
    "notes/sem-2/course-4-statistical-foundations/unit-2.md": [
        "random variable", "discrete", "continuous", "probability mass",
        "probability density", "cumulative distribution", "expectation",
        "variance", "moment", "moment-generating"],
    "notes/sem-2/course-4-statistical-foundations/unit-3.md": [
        "binomial", "poisson", "geometric", "negative binomial", "uniform",
        "normal", "exponential", "gamma", "joint", "marginal",
        "conditional", "central limit"],
    "notes/sem-2/course-4-statistical-foundations/unit-4.md": [
        "bivariate", "scatter", "pearson", "spearman", "linear regression",
        "estimation", "analysis of variance", "multiple linear",
        "residual", "goodness of fit"],
    "notes/sem-2/course-4-statistical-foundations/unit-5.md": [
        "population", "sample", "parameter", "statistic",
        "sampling distribution", "point", "interval estimation",
        "confidence interval", "z-test", "t-test", "chi-square", "f-test",
        "p-value", "type i", "type ii", "power"],

    "notes/sem-3/course-5-dbms/unit-1.md": [
        "data", "information", "file-based", "drawback", "classification",
        "advantage", "data model", "component", "three-schema", "cost",
        "risk"],
    "notes/sem-3/course-5-dbms/unit-2.md": [
        "building block", "entity set", "classification of attribute",
        "degree", "reducing an er", "enhanced er", "generalization",
        "specialization", "is-a", "attribute inheritance",
        "multiple inheritance", "constraint", "advantage"],
    "notes/sem-3/course-5-dbms/unit-3.md": [
        "codd", "relational data model", "key", "integrity",
        "relational algebra", "advantage", "limitation",
        "functional dependenc", "normal form"],
    "notes/sem-3/course-5-dbms/unit-4.md": [
        "command", "data type", "data definition", "selection",
        "projection", "aggregate", "data manipulation", "alter table",
        "join", "set operation", "view", "subquer"],
    "notes/sem-3/course-5-dbms/unit-5.md": [
        "shortcoming", "structure of a pl/sql", "language element",
        "data type", "precedence", "control structure", "steps to create",
        "iterative", "procedure", "function", "trigger"],

    # ---- Semester III, Course 6: Data Science with R
    "notes/sem-3/course-6-data-science-r/unit-1.md": [
        "what data science is", "application", "life cycle",
        "toolkit", "team", "exploratory data analysis", "feature engineering",
        "data transformation"],
    "notes/sem-3/course-6-data-science-r/unit-2.md": [
        "rstudio", "data type", "vector", "matrix", "list", "data frame",
        "factor", "operator", "control structure", "apply", "function",
        "package", "csv", "excel", "json", "xml"],
    "notes/sem-3/course-6-data-science-r/unit-3.md": [
        "dplyr", "filter", "select", "mutate", "arrange", "summarise",
        "tidyr", "missing", "date", "ggplot2", "grammar of graphics",
        "geometr", "scale", "facet"],
    "notes/sem-3/course-6-data-science-r/unit-4.md": [
        "linear regression", "multiple regression", "confusion matrix",
        "precision", "recall", "roc", "auc", "k-means", "text mining",
        "tf-idf", "recommender", "ethic"],
    "notes/sem-3/course-6-data-science-r/unit-5.md": [
        "time series", "decomposition", "stationar", "differencing", "acf",
        "pacf", "arima", "forecast", "plotly", "shiny"],

    # ---- Semester III, Course 7: Web Technologies
    "notes/sem-3/course-7-web-technologies/unit-1.md": [
        "web design", "desktop application", "document structure", "element",
        "attribute", "heading", "paragraph", "image", "table", "list",
        "block", "symbol", "multi", "form"],
    "notes/sem-3/course-7-web-technologies/unit-2.md": [
        "syntax", "combinator", "color", "background", "border", "margin",
        "padding", "height", "width", "text", "font", "table", "list",
        "position", "overflow", "float", "pseudo-class", "pseudo-element",
        "opacity", "tooltip", "image gallery", "css form", "counter"],
    "notes/sem-3/course-7-web-technologies/unit-3.md": [
        "dhtml", "variable", "operator", "statement", "string manipulation",
        "mathematical function", "array", "function", "object",
        "regular expression", "exception handling"],
    "notes/sem-3/course-7-web-technologies/unit-4.md": [
        "form element", "object model", "data validation", "data format",
        "responsive message", "opening window", "dialog box", "status bar",
        "animat", "keyboard", "mouse event"],
    "notes/sem-3/course-7-web-technologies/unit-5.md": [
        "data exchange", "json syntax", "json vs xml", "parsing and stringifying",
        "creating and accessing nested json", "nested", "reading", "writing", "jquery", "selector",
        "filter", "dom manipulation", "event handling", "animation",
        "effect", "chaining"],

    # ---- Semester IV, Course 8: Data Mining
    "notes/sem-4/course-8-data-mining/unit-1.md": [
        "data warehouse", "database systems", "characteristic",
        "architecture", "component", "data modeling", "star schema",
        "star", "snow", "fact constellation", "fact table", "olap cube",
        "olap operation"],
    "notes/sem-4/course-8-data-mining/unit-2.md": [
        "what data mining is", "kdd", "data mining task", "data cleaning",
        "missing data", "dimensionality reduction", "feature subset selection",
        "discretization", "binarization", "data transformation",
        "similarity", "dissimilarity", "issues", "challenge", "application",
        "case stud"],
    "notes/sem-4/course-8-data-mining/unit-3.md": [
        "association rule", "two-step process", "apriori", "partition",
        "pincer", "dynamic itemset counting", "fp-tree", "growth",
        "generalized association", "item constraint"],
    "notes/sem-4/course-8-data-mining/unit-4.md": [
        "decision tree", "tree construction", "best split", "splitting indices",
        "splitting criterion", "cart", "id3", "c4.5", "comparing classifiers",
        "rule-based", "nearest neighbour", "bayesian"],
    "notes/sem-4/course-8-data-mining/unit-5.md": [
        "clustering paradigm", "partitioning", "k-means", "k-medoid",
        "hierarchical", "dbscan", "birch", "categorical clustering",
        "stirr", "rock", "cactus"],

    # ---- Semester IV, Course 9: Python for Data Analysis
    "notes/sem-4/course-9-python-data-analysis/unit-1.md": [
        "ndarray", "multidimensional", "creating ndarray", "data types",
        "arithmetic", "indexing and slicing", "boolean indexing",
        "fancy indexing", "transpos", "swapping axes", "universal function",
        "element-wise", "statistical function", "random number"],
    "notes/sem-4/course-9-python-data-analysis/unit-2.md": [
        "series", "dataframe", "index object", "indexing and selection",
        "filtering", "boolean indexing", "arithmetic", "data alignment",
        "sorting", "ranking", "dropping entries", "duplicate index"],
    "notes/sem-4/course-9-python-data-analysis/unit-3.md": [
        "reading and writing text data", "csv", "json", "excel", "missing data",
        "dropping", "filling", "replacing values", "renaming",
        "removing duplicates", "filtering outliers", "mapping"],
    "notes/sem-4/course-9-python-data-analysis/unit-4.md": [
        "string method", "regular expression", "vectorized string",
        "dummy", "indicator variable", "permutation", "random sampling"],
    "notes/sem-4/course-9-python-data-analysis/unit-5.md": [
        "merging", "joining", "concatenating", "combining data with overlap",
        "pivot", "stack", "unstack", "hierarchical indexing",
        "summary statistics", "matplotlib", "customisation", "plt.style",
        "seaborn", "plotly", "interactive"],

    # ---- Semester IV, Course 10: Document Oriented Database
    "notes/sem-4/course-10-document-database/unit-1.md": [
        "nosql", "history", "features of nosql", "cap theorem", "base",
        "key-value", "document", "column", "graph", "rdbms",
        "when to use nosql", "misconception", "use case",
        "redis", "cassandra", "couchdb", "neo4j", "json", "bson",
        "installation", "mongo shell", "compass"],
    "notes/sem-4/course-10-document-database/unit-2.md": [
        "architecture", "database", "collection", "document", "bson format",
        # These five follow the NOTES' wording, not the syllabus's: the notes
        # use British spelling ("modelling"), spell out "versus", and write
        # the shell commands themselves. The topic is the same.
        "advantages of mongodb over rdbms", "data type", "objectid",
        "embedded document", "null", "modelling", "schema design",
        "embedded versus referenced", "createcollection",
        "dropdatabase", "drop one collection"],
    "notes/sem-4/course-10-document-database/unit-3.md": [
        "crud", "insertone", "insertmany", "find", "updateone", "updatemany",
        "replaceone", "deleteone", "deletemany", "$gt", "$lt", "$in", "$nin",
        "$and", "$or", "$not", "regular expression", "bulk", "array"],
    "notes/sem-4/course-10-document-database/unit-4.md": [
        "embedded", "normalized", "trade-off", "benefit", "limitation",
        "reference", "when to normalize", "relationship",
        "one-to-one", "one-to-many", "many-to-many",
        "aggregation framework", "pipeline", "operator"],
    "notes/sem-4/course-10-document-database/unit-5.md": [
        "projection", "limiting", "skipping", "sorting", "indexing",
        "single field", "compound", "multikey", "text index",
        "pipeline", "stage", "replication", "replica set", "failover",
        "consistency"],

    # ---- Semester V, Course 11: Business Intelligence Tools
    "notes/sem-5/course-11-business-intelligence/unit-1.md": [
        "definition", "scope", "evolution", "data analytics", "data science",
        "bi lifecycle", "finance", "hr", "marketing", "retail", "education",
        "healthcare", "maturity model", "readiness",
        "decision support system", "component", "architecture",
        "power bi", "tableau", "comparison", "suitability", "case study"],
    "notes/sem-5/course-11-business-intelligence/unit-2.md": [
        "power bi", "ecosystem", "desktop", "service", "mobile", "interface",
        "data source", "excel", "csv", "sql server", "web api",
        "power query", "cleaning", "transformation", "dax",
        "sum", "count", "average", "calculate", "if",
        "chart", "table", "card", "sharing"],
    "notes/sem-5/course-11-business-intelligence/unit-3.md": [
        "tableau", "characteristic", "architecture", "tableau public",
        "desktop", "reader", "online", "server", "shelves", "marks card",
        "view", "extension", "data connection", "cleaning", "pivot",
        "filtering", "calculated field", "lod", "bar", "line", "tree",
        "geo map", "scatter", "storytelling", "story"],
    "notes/sem-5/course-11-business-intelligence/unit-4.md": [
        "dimensional modeling", "dimension table", "fact table", "schema",
        "star", "snowflake", "relationship", "cardinality", "cross-filter",
        "join", "inner", "left", "full", "blending",
        "governance", "metadata", "hierarchies", "quality",
        "best practice"],
    "notes/sem-5/course-11-business-intelligence/unit-5.md": [
        "dashboard", "when to use", "component", "principles",
        "parameter", "slicer", "filter", "drilldown", "graph", "map",
        "layout", "alignment", "accessibility", "publishing",
        "power bi service", "tableau public", "storytelling",
        "insight communication"],

    # ---- Semester V, Course 12 A: Machine Learning, Track A
    "notes/sem-5/course-12a-machine-learning/unit-1.md": [
        "types of human learning", "what is machine learning", "supervised",
        "unsupervised", "semi-supervised", "reinforcement",
        "machine learning activities", "application",
        "types of data", "structure of data"],
    "notes/sem-5/course-12a-machine-learning/unit-2.md": [
        "pre-processing", "model selection", "training",
        "model representation", "interpretability", "evaluating",
        "performance enhancement", "feature engineering",
        "feature transformation", "feature subset selection",
        "principal component analysis"],
    "notes/sem-5/course-12a-machine-learning/unit-3.md": [
        "regression", "simple linear regression", "multiple linear regression",
        "polynomial regression", "logistic regression",
        "maximum likelihood estimation"],
    "notes/sem-5/course-12a-machine-learning/unit-4.md": [
        "supervised learning", "classification model", "learning steps",
        "naive bayes", "k-nearest neighbour", "decision tree",
        "support vector machine", "random forest"],
    "notes/sem-5/course-12a-machine-learning/unit-5.md": [
        "unsupervised learning", "clustering", "partitioning method",
        "k-means", "k-medoid", "hierarchical clustering",
        "density-based", "dbscan", "image recognition",
        "speech recognition", "email spam filtering", "fraud detection"],

    # ---- Semester V, Course 12 B: Big Data Technologies, Track B
    "notes/sem-5/course-12b-big-data/unit-1.md": [
        "introduction to big data", "volume", "variety", "velocity",
        "veracity", "value", "hadoop ecosystem", "hdfs", "mapreduce",
        "yarn", "hadoop common", "hadoop architecture", "use cases"],
    "notes/sem-5/course-12b-big-data/unit-2.md": [
        "hdfs architecture", "blocks", "namenode", "datanode",
        "hdfs file operations", "fault tolerance", "replication",
        "yarn architecture", "resourcemanager", "nodemanager",
        "application scheduling"],
    "notes/sem-5/course-12b-big-data/unit-3.md": [
        "mapreduce programming model", "map", "shuffle", "reduce",
        "writing mapreduce applications", "hive", "pig", "crunch",
        "spark integration"],
    "notes/sem-5/course-12b-big-data/unit-4.md": [
        "data ingestion", "sqoop", "flume", "serialization", "avro",
        "parquet", "sequencefile", "batch", "streaming"],
    "notes/sem-5/course-12b-big-data/unit-5.md": [
        "nosql", "hbase", "zookeeper", "coordination",
        "hadoop integration with spark"],

    # ---- Semester V, Course 13 B: Cloud Computing, Track B
    "notes/sem-5/course-13b-cloud-computing/unit-1.md": [
        "definition", "evolution of cloud computing",
        "service-oriented architecture", "web services", "utility",
        "grid computing", "characteristics of cloud computing",
        "cloud computing architecture", "front-end", "back-end",
        "networking", "delivery models", "saas", "paas", "iaas",
        "continuous delivery"],
    "notes/sem-5/course-13b-cloud-computing/unit-2.md": [
        "virtualization", "application", "network", "desktop", "storage",
        "server", "data virtualization", "deployment models", "public",
        "private", "community", "hybrid", "role of cloud computing in data science",
        "advantages of cloud in machine learning"],
    "notes/sem-5/course-13b-cloud-computing/unit-3.md": [
        "cloud storage", "benefits", "backup", "archiving",
        "content delivery", "block-based", "file-based", "object-based",
        "key-value databases", "batch", "streaming", "cloud data warehouse",
        "redshift", "bigquery"],
    "notes/sem-5/course-13b-cloud-computing/unit-4.md": [
        "machine learning in the cloud", "limitations", "aiaas", "gpuaas",
        "managed ml platforms", "sagemaker", "azure ml", "automl"],
    "notes/sem-5/course-13b-cloud-computing/unit-5.md": [
        "selecting cloud ml platforms", "etl", "scale-up", "scale-out",
        "ml frameworks", "pre-tuned services", "data source identification",
        "feature engineering", "training", "validation", "deployment",
        "monitoring", "case studies"],

    # ---- Semester V, Course 13 A: Artificial Intelligence, Track A
    "notes/sem-5/course-13a-artificial-intelligence/unit-1.md": [
        "definition and scope of ai", "history", "turing test",
        "applications of ai", "weak ai", "strong ai", "narrow ai",
        "general ai", "intelligent agents", "structure of agents",
        "rationality", "agent types", "deterministic", "stochastic",
        "static", "dynamic", "discrete", "continuous", "peas"],
    "notes/sem-5/course-13a-artificial-intelligence/unit-2.md": [
        "state space representation", "goal test", "path cost",
        "problem formulation", "8-puzzle", "water jug", "vacuum",
        "uninformed search", "breadth first search", "depth first search",
        "uniform cost search", "completeness", "optimality",
        "space complexity"],
    "notes/sem-5/course-13a-artificial-intelligence/unit-3.md": [
        "informed search", "heuristic", "admissibility", "consistency",
        "greedy best first search", "a* algorithm", "local search",
        "hill climbing", "simulated annealing", "genetic algorithm",
        "constraint satisfaction", "backtracking search"],
    "notes/sem-5/course-13a-artificial-intelligence/unit-4.md": [
        "knowledge representation", "propositional logic", "syntax",
        "semantics", "truth table", "inference rules", "first order logic",
        "quantifier", "substitution", "unification", "forward chaining",
        "backward chaining", "resolution", "knowledge-based agents"],
    "notes/sem-5/course-13a-artificial-intelligence/unit-5.md": [
        "expert systems", "architecture", "knowledge base",
        "inference engine", "explanation facility", "probabilistic reasoning",
        "bayes' theorem", "bayesian belief network", "fuzzy logic",
        "uncertainty", "nlp", "robotics", "ai ethics", "societal impact"],

    "notes/sem-6/course-14a-deep-learning/unit-1.md": [
        "artificial intelligence", "machine learning", "deep learning",
        "history", "biological", "artificial neuron", "perceptron",
        "activation function", "relu", "sigmoid", "tanh", "softmax",
        "shallow", "feedforward", "recurrent", "gradient descent",
        "backpropagation", "loss function", "cross-entropy"],
    "notes/sem-6/course-14a-deep-learning/unit-2.md": [
        "forward propagation", "backward propagation",
        "weight initialization", "learning rate", "sgd", "adam", "rmsprop",
        "overfitting", "underfitting", "regularization", "dropout",
        "batch normalization", "hinge loss", "keras", "tensorflow"],
    "notes/sem-6/course-14a-deep-learning/unit-3.md": [
        "pixel", "filter", "kernel", "padding", "pooling", "convolution",
        "fully connected", "softmax", "lenet", "alexnet", "vgg",
        "image classification", "object detection", "facial recognition"],
    "notes/sem-6/course-14a-deep-learning/unit-4.md": [
        "sequence", "time series", "recurrent neural network",
        "vanishing", "exploding gradient", "lstm", "gru",
        "word embedding", "word2vec", "glove", "contextual", "bert",
        "sentiment analysis", "text generation", "forecasting"],
    "notes/sem-6/course-14a-deep-learning/unit-5.md": [
        "generative", "gan", "generator", "discriminator", "vae",
        "transformer", "attention", "bert", "gpt", "transfer learning",
        "fine-tuning", "bias", "fairness", "privacy", "safety",
        "explainability"],

    "notes/sem-6/course-14b-time-series/unit-1.md": [
        "time series", "components", "forecasting process", "stationary",
        "autocovariance", "autocorrelation", "acf", "pacf",
        "evaluation metrics"],
    "notes/sem-6/course-14b-time-series/unit-2.md": [
        "arma", "estimation", "forecasting", "model selection", "aic",
        "diagnostic", "residual", "prediction interval"],
    "notes/sem-6/course-14b-time-series/unit-3.md": [
        "non-stationary", "differencing", "arima", "sarima", "seasonal",
        "dickey-fuller", "kpss"],
    "notes/sem-6/course-14b-time-series/unit-4.md": [
        "multivariate", "vector autoregression", "var", "granger",
        "state space", "kalman filter"],
    "notes/sem-6/course-14b-time-series/unit-5.md": [
        "exponential smoothing", "holt-winters", "machine learning",
        "rmse", "mae", "mape", "mase", "baseline", "spectral analysis",
        "periodogram"],

    "notes/sem-6/course-15a-nlp/unit-1.md": [
        "definition", "goals", "scope of nlp", "applications", "chatbot",
        "translation", "summarization", "spam detection",
        "language processing", "lexical", "structural", "contextual",
        "nltk", "spacy", "regular expression", "findall", "split", "sub"],
    "notes/sem-6/course-15a-nlp/unit-2.md": [
        "morphology", "lexicon", "orthographic", "finite state transducer",
        "tokenization", "stopword", "stemming", "lemmatization", "grammar",
        "context-free grammar", "top-down", "bottom-up", "cyk",
        "semantic analysis", "meaning representation"],
    "notes/sem-6/course-15a-nlp/unit-3.md": [
        "named entity recognition", "ner", "spacy", "word embedding",
        "word2vec", "skip-gram", "cbow", "bag of words", "n-gram",
        "text classification", "sentiment analysis", "ethical"],
    "notes/sem-6/course-15a-nlp/unit-4.md": [
        "recurrent neural network", "rnn", "cnn", "feedforward", "lstm",
        "gru", "sequence modeling", "transformer", "pretrained", "bert",
        "gpt", "hugging face"],
    "notes/sem-6/course-15b-mlops/unit-1.md": [
        "data engineering", "lifecycle", "skills", "activities",
        "evolution", "roles", "technical", "business", "internal",
        "external", "data science", "data lifecycle"],
    "notes/sem-6/course-15b-mlops/unit-2.md": [
        "enterprise", "data architecture", "principles", "scalability",
        "failure", "tiers", "microservices", "monolith", "modular",
        "event-driven", "hybrid cloud", "multicloud", "edge computing",
        "team size", "interoperability", "cost", "tco"],
    "notes/sem-6/course-15b-mlops/unit-3.md": [
        "mlops", "challenges", "risk", "responsible ai", "scaling",
        "eda", "feature engineering", "model training", "evaluation",
        "reproducibility", "deployment requirements", "monitoring",
        "model versioning", "experimentation tracking"],
    "notes/sem-6/course-15b-mlops/unit-4.md": [
        "production", "runtime environments", "ci/cd", "artifact",
        "testing", "batch", "online", "a/b testing", "canary",
        "containerization", "docker", "kubernetes", "scaling"],
    "notes/sem-6/course-15b-mlops/unit-5.md": [
        "drift detection", "ground truth", "feedback loop", "retraining",
        "online evaluation", "logging", "monitoring", "governance",
        "gdpr", "ccpa", "gxp", "responsible ai", "compliance",
        "model risk management"],

    "notes/sem-6/course-15a-nlp/unit-5.md": [
        "transformer architecture", "self-attention", "encoder-decoder",
        "bert", "pretraining", "fine-tuning", "gpt", "generative",
        "hugging face", "extractive", "abstractive", "hybrid",
        "document classification", "chatbot", "virtual assistant"],
}


def body_of(path):
    """The note's prose, lowercased, with the syllabus header stripped off.

    Every unit file opens by quoting its syllabus line verbatim, so searching
    the whole file would let a keyword match that quotation rather than any
    material actually written. Stripping everything up to the first horizontal
    rule makes the check mean what it claims: the TOPIC IS TAUGHT, not merely
    listed. Without this, 19 of the keywords passed vacuously.
    """
    text = path.read_text()
    parts = re.split(r"^---$", text, maxsplit=1, flags=re.M)
    return normalise((parts[1] if len(parts) > 1 else text))


def normalise(text):
    """Lowercase, and fold the two spelling differences that are not gaps.

    The notes are written in British English; several syllabus lines use
    American spellings. 'Regularisation' and 'regularization' are the same
    topic, and a coverage checker that reports one as missing is measuring
    orthography rather than content. Likewise an en-dash in a name such as
    Dickey-Fuller.

    This folds ONLY -ise/-isation to -ize/-ization and the dash characters.
    It does not loosen matching in any other way, so a keyword that fails
    still means the topic is genuinely absent.
    """
    text = text.lower()
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    # collapse every run of whitespace to one space, so a keyword broken
    # across a line wrap still matches. Without this the check reports a
    # false gap whenever a phrase happens to straddle the margin.
    text = " ".join(text.split())
    text = re.sub(r"is(ation|ations|ing|ed|es|e)\b", lambda m: "iz" + m.group(1),
                  text)
    return text


def main():
    missing_total = 0
    files_checked = 0

    for rel_path, keywords in COVERAGE.items():
        path = ROOT / rel_path
        if not path.exists():
            print(f"MISSING FILE  {rel_path}")
            missing_total += len(keywords)
            continue

        files_checked += 1
        body = body_of(path)
        # the keywords go through the same fold, so the two sides always
        # agree even where the fold is crude
        missing = [k for k in keywords if normalise(k) not in body]

        if missing:
            print(f"GAPS  {rel_path}")
            for k in missing:
                print(f"        not found: {k!r}")
            missing_total += len(missing)
        else:
            print(f"ok    {rel_path}  ({len(keywords)} topics)")

    total = sum(len(v) for v in COVERAGE.values())
    print()
    print(f"{files_checked} unit files checked, "
          f"{total - missing_total}/{total} syllabus topics covered")

    # Every course folder should also have README, practice and lab notes.
    print()
    for course_dir in sorted((ROOT / "notes").glob("*/*")):
        for required in ("README.md", "practice.md", "lab.md"):
            if not (course_dir / required).exists():
                print(f"MISSING  {course_dir.relative_to(ROOT)}/{required}")
                missing_total += 1

    return 1 if missing_total else 0


if __name__ == "__main__":
    sys.exit(main())
