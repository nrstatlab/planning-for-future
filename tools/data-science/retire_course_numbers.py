#!/usr/bin/env python3
"""Take the programme's numbering, semesters and elective tracks out of the Data Science notes.

    python3 tools/data-science/retire_course_numbers.py            # dry run
    python3 tools/data-science/retire_course_numbers.py --diff     # ... and show every change
    python3 tools/data-science/retire_course_numbers.py --apply    # write the markdown

One-shot, like tools/retire_programme_labels.py. The notes were written for
a six-semester programme and refer to one another as "Course 5" or
"Course 12 A", place themselves in "Semester IV", and explain the Track A /
Track B elective choice. The site is studied course by course now, in any
order, so a number tells a reader nothing: every "Course N" becomes the
course's name, taken from build_site.py's COURSES so it cannot drift, and
the semester and track sentences are reworded to say the same thing without
a timetable.

Only data-science/notes/ is touched -- the markdown is the source and
build_site.py regenerates the pages from it. The programme documents at the
top of data-science/ (study plan, syllabus map, syllabus review, extracted
syllabi) describe the programme as its documents do and are left alone.

Code is protected: fenced blocks and `inline code` are never rewritten, so a
data set with a `semester` column, or HTML that prints "Semester III marks",
stays exactly as it was.
"""
import argparse
import difflib
import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
NOTES = ROOT / "data-science" / "notes"

spec = importlib.util.spec_from_file_location("_bs", ROOT / "tools" / "data-science" / "build_site.py")
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)


def names():
    """'12 A' -> 'Machine Learning', from each course's source folder name."""
    out = {}
    for c in bs.COURSES:
        m = re.search(r"course-(\d+)([ab])?-", c["src"])
        key = m.group(1) + (" " + m.group(2).upper() if m.group(2) else "")
        out[key] = c["title"]
    return out


NAME = names()
ML_PATH = "Machine Learning, Artificial Intelligence, Neural Networks and Deep Learning and Natural Language Processing"
DATA_PATH = ("Big Data Technologies, Cloud Computing for Data Science, Time Series Analysis and "
             "Forecasting and Data Engineering and MLOps")

# The opening paragraph of each elective course, which explained the track.
# The pairing is real and useful; only the timetable goes.
INTROS = {
    "course-11-business-intelligence": (
        "**This course comes before either specialisation.** After it the material divides into a "
        "machine-learning path (%s) and a data-platform path (%s); this one belongs to neither."
        % (ML_PATH, DATA_PATH)),
    **{k: "**Part of the machine-learning path:** %s." % ML_PATH
       for k in ("course-12a-machine-learning", "course-13a-artificial-intelligence",
                 "course-14a-deep-learning", "course-15a-nlp")},
    **{k: "**Part of the data-platform path:** %s." % DATA_PATH
       for k in ("course-12b-big-data", "course-13b-cloud-computing",
                 "course-14b-time-series", "course-15b-mlops")},
}

# Sentence by sentence, each checked in context. \s+ because the markdown wraps.
SENTENCES = [
    (r"Semester\s+V's\s+Business\s+Intelligence\s+course", "the Business Intelligence Tools course"),
    (r"This\s+is\s+also\s+the\s+course\s+with\s+the\s+highest\s+marks-per-hour\s+ratio\s+in\s+the\s+semester\.",
     "This is also the course with the highest marks-per-hour ratio of any."),
    (r"If\s+you\s+have\s+limited\s+time\s+in\s+Semester\s+II,\s+spend\s+it\s+on\s+this\s+course\.",
     "If you have limited time, spend it on this course."),
    (r"—\s+Data\s+Mining\s+in\s+Semester\s+IV,\s+Machine\s+Learning\s+or\s+Time\s+Series\s+in\s+Year\s+III\s+—",
     "— Data Mining, Machine Learning, Time Series —"),
    (r"even\s+though\s+you\s+are\s+learning\s+Python\s+in\s+Course\s+3\s+the\s+same\s+semester\.",
     "even though Python Programming and Data Structures teaches the language."),
    (r"even\s+though\s+you\s+are\s+learning\s+Python\s+in\s+Course\s+3\s+the\s+same\s+semester;\s+Python-based\s+analysis\s+waits\s+until\s+Semester\s+IV\.",
     "even though Python Programming and Data Structures teaches the language; Python-based analysis is "
     "taught in Python for Data Analysis and Visualization."),
    (r"that\s+is\s+what\s+the\s+degree\s+is\s+for\.", "that is what the course is for."),
    (r"\(You\s+meet\s+the\s+document\s+model\s+again\s+in\s+Semester\s+IV,\s+Course\s+10\.\)",
     "(You meet the document model again in Document Oriented Database.)"),
    (r"which\s+you\s+meet\s+in\s+Semester\s+V's\s+Business\s+Intelligence\s+course\.",
     "which you meet in the Business Intelligence Tools course."),
    (r"it\s+feeds\s+the\s+Semester\s+VI\s*\n>\s*elective\.", "it feeds the\n> Time Series Analysis and Forecasting course."),
    (r"After\s+a\s+semester\s+of\s+Python\s+and\s+C", "After Python and C"),
    (r"it\s+feeds\s+directly\s+into\s*\n>\s*the\s+Semester\s+VI\s+elective\s+\*Time\s+Series\s+Analysis\s+and\s+Forecasting\*\.",
     "it feeds directly into\n> *Time Series Analysis and Forecasting*."),
    (r"Semester\s+VI's\s+MLOps\s+elective\s+is", "The Data Engineering and MLOps course is"),
    (r"This\s+is\s+the\s+one\s+Semester\s+IV\s+course\s+whose\s+prescribed",
     "This is one of the few courses whose prescribed"),
    (r"with\s+the\s+other\s*\n>\s*Semester\s+V\s+text\s+defects\.", "with the other\n> text defects."),
    (r"This\s+is\s+Course\s+13\s+A's\s+territory\s+too;\s+if\s+you\s+are\s+on\s+Track\s+A\s+you\s+will\s+meet\s+agents\s+and\s+environments\s+again\s+in\s+its\s+Unit\s+1\.",
     "This is Artificial Intelligence's territory too: its Unit 1 takes agents and environments further."),
    (r"The\s+Track\s+B\s+course\s+measures\s+this\s+directly:",
     "The Time Series Analysis and Forecasting course measures this directly:"),
    (r"Both\s+labs\s+in\s+this\s+semester\s+do\s+it\s+in\s+one\s+line\.",
     "Both this course's lab and Neural Networks and Deep Learning's do it in one line."),
    (r"Course\s+15\s+B\s+is\s+the\s+only\s+Semester\s+VI\s+course\s+whose\s+students\s+cannot",
     "This is the only course of the later ones whose students cannot"),
    # These two describe the syllabus document, not the site.
    (r"while\s+every\s+other\s+course\s*\n>\s*in\s+the\s+programme\s+writes",
     "while every other course's\n> syllabus writes"),
    (r"Every\s+other\s+course\s+in\s*\n>\s*the\s+programme\s+has\s+five\s+of\s+each\.",
     "Every other course's syllabus\n> has five of each."),
    # plurals, before the singular rule
    (r"\bCourses\s+12\s+and\s+13\b", "the elective courses"),
    (r"\bCourses\s+2\s+and\s+3\b", "Problem Solving Using C and Python Programming and Data Structures"),
    (r"\bCourses\s+3\s+and\s+9\b", "Python Programming and Data Structures and Python for Data Analysis and Visualization"),
    (r"\bCourses\s+4,\s+8\s+and\s+12\s+A\b", "Statistical Foundations for Data Science, Data Mining and Machine Learning"),
    (r"\bCourses\s+6,\s+8,\s+10,\s+11\s+and\b", "Data Science with R, Data Mining, Document Oriented Database, Business Intelligence Tools and"),
]

H1 = re.compile(r"^# Course \d+(?: [AB])? — ", re.M)
COURSE = re.compile(r"\bCourse\s+(\d+)(?:\s?([AB])\b)?")
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)


def one_course(m):
    key = m.group(1) + (" " + m.group(2) if m.group(2) else "")
    if key not in NAME:           # "Course 12" with no A/B names the pair
        return m.group(0)
    return NAME[key]


def rewrite(text, folder, is_readme):
    kept = []

    def hold(m):
        kept.append(m.group(0))
        return "\x00%d\x00" % (len(kept) - 1)

    out = CODE.sub(hold, text)
    if is_readme and folder in INTROS:
        # The intro is the paragraph between the H1 and the first rule.
        out = re.sub(r"(\A# [^\n]*\n\n)(.*?)(\n\n---)", lambda m: m.group(1) + INTROS[folder] + m.group(3),
                     out, count=1, flags=re.S)
    out = H1.sub("# ", out)
    for pat, rep in SENTENCES:
        out = re.sub(pat, rep, out)
    out = COURSE.sub(one_course, out)
    # "Course 13 B (Cloud Computing)" came out as "Cloud Computing for Data
    # Science (Cloud Computing)": a parenthesis that only repeats the name goes.
    for name in NAME.values():
        words = set(re.findall(r"\w+", name.lower()))
        out = re.sub(re.escape(name) + r"\s+\(([^)\n]*(?:\n[^)\n]*)?)\)",
                     lambda m: name if set(re.findall(r"\w+", m.group(1).lower())) <= words else m.group(0),
                     out)
        # A name ending in s takes the bare apostrophe.
        if name.endswith("s"):
            out = out.replace(name + "'s", name + "'")
    # "this programme" was the six-semester programme; the site's word is catalogue.
    out = re.sub(r"\b(this|the|whole)(\s+)programme\b(?!\s+VARCHAR)", r"\1\2catalogue", out)
    out = re.sub(r"\bThe(\s+)rest(\s+)of(\s+)the(\s+)programme\b", r"The\1rest\2of\3the\4catalogue", out)
    return re.sub(r"\x00(\d+)\x00", lambda m: kept[int(m.group(1))], out)


def main(apply_changes, show):
    changed = 0
    for p in sorted(NOTES.rglob("*.md")):
        folder = p.parent.name
        text = p.read_text()
        out = rewrite(text, folder, p.name == "README.md")
        if out != text:
            changed += 1
            if show:
                sys.stdout.writelines(difflib.unified_diff(
                    text.splitlines(True), out.splitlines(True),
                    str(p.relative_to(ROOT)), str(p.relative_to(ROOT)), n=0))
            if apply_changes:
                p.write_text(out)
    left = []
    for p in sorted(NOTES.rglob("*.md")):
        t = CODE.sub("", p.read_text() if apply_changes else rewrite(p.read_text(), p.parent.name, p.name == "README.md"))
        for m in re.finditer(r"[^\n]*\b(Semester|Track [AB]|Course \d+)\b[^\n]*", t):
            left.append("%s: %s" % (p.relative_to(NOTES), m.group(0).strip()[:140]))
    print("%d file(s) %s; %d line(s) still name a semester, track or course number"
          % (changed, "written" if apply_changes else "would change", len(left)))
    for l in left:
        print("   ", l)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--diff", action="store_true")
    a = ap.parse_args()
    main(a.apply, a.diff)
