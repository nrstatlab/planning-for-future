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
        "if-elif-else", "while", "for", "nested loop", "break", "continue",
        "pass", "`else` with a loop", "return", "scope", "default",
        "variable-length", "main()", "docstring", "recursive", "lambda",
        "module", "namespace"],
    "notes/sem-2/course-3-python-data-structures/unit-3.md": [
        "slicing", "immutability", "traversal", "formatting", "list",
        "comprehension", "tuple", "tuple assignment", "set", "frozenset",
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
        "uncertainty", "axiom", "conditional probability", "mean", "median",
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
        "building block", "entity set", "attribute classification",
        "degree", "reducing er", "enhanced entity", "generalization",
        "specialization", "is-a", "attribute inheritance",
        "multiple inheritance", "constraint", "advantage"],
    "notes/sem-3/course-5-dbms/unit-3.md": [
        "codd", "relational data model", "key", "integrity",
        "relational algebra", "advantage", "limitation",
        "functional dependenc", "normal form"],
    "notes/sem-3/course-5-dbms/unit-4.md": [
        "command", "data type", "data definition", "selection",
        "projection", "aggregate", "data manipulation", "table modification",
        "join", "set operation", "view", "sub query"],
    "notes/sem-3/course-5-dbms/unit-5.md": [
        "shortcoming", "structure of pl/sql", "language element",
        "data type", "precedence", "control structure", "steps to create",
        "iterative", "procedure", "function", "trigger"],
}


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
        text = path.read_text().lower()
        missing = [k for k in keywords if k.lower() not in text]

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
