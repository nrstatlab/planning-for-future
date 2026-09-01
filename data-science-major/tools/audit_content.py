#!/usr/bin/env python3
"""Audit the repository's own claims and markup against what is on disk.

The other tools in this directory check that the LAB CODE is correct. This one
checks that the PROSE is correct -- that the counts the documents state match
the files that exist, that every course has its full set of notes, that no
table is malformed, and that every link resolves.

It exists because those claims drift. A repository that says "24 findings from
three documents" while holding 33 findings from four is wrong in the way that
is hardest to notice: nothing fails, nothing renders badly, and the reader has
no reason to doubt it.

Two markup checks earn their place specifically:

  * UNESCAPED PIPES IN TABLE CELLS. Writing `O(n^3 . |G|)` in a markdown table
    silently splits the cell, and the rendered page shows a truncated value
    with the bold markers left as literal asterisks. Three of those were found
    and fixed the first time this ran.
  * RAGGED ROWS. A row with fewer cells than its header renders short without
    any warning.

Run: python3 tools/audit_content.py
"""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
problems = []


def check(label, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'} {label}"
          f"{'' if ok else '  -- ' + detail}")
    if not ok:
        problems.append(label)


def cells(line):
    """Count table cells, ignoring pipes inside `code` and escaped pipes."""
    line = re.sub(r"`[^`]*`", "X", line)
    line = line.replace("\\|", "")
    return line.strip().strip("|").count("|") + 1


def markdown_files():
    return sorted(
        list(ROOT.glob("*.md"))
        + list(ROOT.glob("notes/**/*.md"))
        + list(ROOT.glob("labs/**/*.md")))


def main():
    pdfs = sorted(ROOT.glob("docs/*.pdf"))
    # Source files only. Counting __pycache__ made this number depend on
    # whether the suites had been run since the last clean, so the hub
    # figure it is checked against drifted every time.
    lab_files = [p for p in (ROOT / "labs").rglob("*")
                 if p.is_file() and "__pycache__" not in p.parts
                 and p.suffix != ".pyc"]
    note_dirs = sorted(p for p in ROOT.glob("notes/sem-*/*") if p.is_dir())
    unit_files = sorted(ROOT.glob("notes/sem-*/*/unit-*.md"))
    pages = sorted(list(ROOT.glob("*.html")) + list(ROOT.glob("*/*.html")))
    review = (ROOT / "SYLLABUS-REVIEW.md").read_text()
    findings = re.findall(r"^### (D\d+)", review, re.M)
    mds = markdown_files()

    print("\nGROUND TRUTH")
    for label, n in (("source PDFs", len(pdfs)),
                     ("course note directories", len(note_dirs)),
                     ("unit files", len(unit_files)),
                     ("lab files", len(lab_files)),
                     ("generated pages", len(pages)),
                     ("markdown files", len(mds)),
                     ("review findings", len(findings))):
        print(f"  {label:<26}{n}")

    # -- 1 -----------------------------------------------------------------
    print("\n1. EVERY COURSE HAS ITS FULL SET OF NOTES")
    required = (["README.md", "practice.md", "lab.md"]
                + [f"unit-{i}.md" for i in range(1, 6)])
    incomplete = []
    for d in note_dirs:
        missing = [f for f in required if not (d / f).exists()]
        if missing:
            incomplete.append(f"{d.name} missing {missing}")
    check(f"{len(note_dirs)} course directories complete", not incomplete,
          "; ".join(incomplete))

    # Six courses had a thinner page than the other thirteen -- no prescribed
    # reading, no objectives, no pointer to the lab code. Nothing was WRONG on
    # them, which is why no check caught it: a reader simply lost the textbook
    # list a third of the way through the programme.
    # "How to study statistics" is Course 4's wording and is right for it, so
    # match the stem rather than the whole heading.
    SECTIONS = ["Course objectives (verbatim)", "Also here", "How to study"]
    thin = []
    for d in note_dirs:
        heads = re.findall(r"^## (.+)$", (d / "README.md").read_text(), re.M)
        for want in SECTIONS:
            if not any(want.lower() in h.lower() for h in heads):
                thin.append(f"{d.name} has no '{want}'")
        # the singular "Textbook" is right where a course prescribes only one
        if not any("textbook" in h.lower() for h in heads):
            thin.append(f"{d.name} lists no prescribed reading")
    check("every course page carries objectives, reading, a lab pointer and "
          "study guidance", not thin, "; ".join(thin[:4]))

    # A practice dataset nobody can find is a file, not a resource. Every
    # course page must name its data directory, and every CSV under data/
    # must be named on some page -- otherwise it exists only for the checker.
    all_md = "\n".join(m.read_text() for m in mds)
    orphans, unlinked = [], []
    for d in note_dirs:
        text = (d / "README.md").read_text()
        if "data/" not in text:
            unlinked.append(d.name)
    for csv_path in sorted((ROOT / "data").rglob("*.csv")):
        rel = csv_path.relative_to(ROOT / "data").as_posix()
        if csv_path.name not in all_md:
            orphans.append(rel)
    check(f"{len(list((ROOT / 'data').rglob('*.csv')))} practice datasets, "
          "each named on a page, each course pointing at its own",
          not orphans and not unlinked,
          f"unreferenced: {orphans[:3]}; courses not pointing at data: "
          f"{unlinked[:3]}")

    # -- 2 -----------------------------------------------------------------
    print("\n2. REVIEW FINDINGS ARE NUMBERED CLEANLY")
    nums = [int(f[1:]) for f in findings]
    dupes = sorted({n for n in nums if nums.count(n) > 1})
    gaps = [n for n in range(1, max(nums) + 1) if n not in nums]
    check("numbers unique", not dupes, str(dupes))
    check("numbers contiguous", not gaps, str(gaps))

    # -- 3 -----------------------------------------------------------------
    print("\n3. STATED COUNTS MATCH THE FILES")
    readme = (ROOT / "README.md").read_text()
    index = (ROOT / "index.html").read_text()
    check(f"README states {len(findings)} findings",
          f"**{len(findings)} findings**" in readme)
    check("README states four source documents",
          "four official documents" in readme)
    check(f"hub states {len(lab_files)} lab files",
          f"{len(lab_files)} lab source files" in index,
          "the hub's file count has drifted")

    # Two counts are DERIVED from the findings list, so both go stale silently
    # whenever a finding is added. They had: the hub said thirteen further
    # findings and the README said twenty, against a real total of 33 with 3
    # of them highlighted on the hub.
    # The README summarises three findings inline and points at the rest. The
    # hub used to repeat that count in its warning box; the box has been
    # removed, so this is a README-only claim now.
    WORDS = {13: "Thirteen", 20: "Twenty", 30: "Thirty", 33: "Thirty-three"}
    highlighted = 3          # D1, D2 and D13 are summarised in the README
    further = len(findings) - highlighted
    word = WORDS.get(further, str(further))
    check(f"README states {further} further findings",
          f"**{word} further findings**" in readme,
          f"expected the word {word!r}")

    # The text-loss pattern is stated in two documents, with the findings named
    # in both. They disagreed: the review counted fourteen INSTANCES and called
    # them findings, and the README carried a second, independently-made
    # classification of fifteen. One list now, checked in both places.
    WORDNUM = {"nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
               "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
               "twenty-four": 24, "thirty-three": 33}
    pattern_claim = re.compile(
        r"\*\*(\w+) of the ([\w-]+) findings are the\s+same\s*defect"
        r"(.*?)(?:\n\n|That is a production|Four documents)", re.S)
    lists, problems_here = {}, []
    for name, text in (("README", readme), ("SYLLABUS-REVIEW", review)):
        mo = pattern_claim.search(text)
        if not mo:
            problems_here.append(f"{name}: the defect-pattern claim is missing")
            continue
        ids = re.findall(r"\bD\d+\b", mo.group(3))
        lists[name] = ids
        if WORDNUM.get(mo.group(1).lower()) != len(ids):
            problems_here.append(f"{name} says {mo.group(1)} but lists "
                                 f"{len(ids)}")
        if WORDNUM.get(mo.group(2).lower()) != len(findings):
            problems_here.append(f"{name} says {mo.group(2)} findings, there "
                                 f"are {len(findings)}")
        absent = [i for i in ids if i not in findings]
        if absent:
            problems_here.append(f"{name} names findings that do not exist: "
                                 f"{absent}")
    if len(lists) == 2 and lists["README"] != lists["SYLLABUS-REVIEW"]:
        problems_here.append("the two documents name different findings")
    n = len(lists.get("README", []))
    check(f"the defect-pattern claim: {n} of {len(findings)}, stated the same "
          "in both documents", not problems_here, "; ".join(problems_here[:3]))

    # -- 3b ----------------------------------------------------------------
    # The hub is hand-maintained while every other page is generated, so it is
    # the one file that can drift away from the courses it advertises. A tile
    # naming a course the generator does not build, or a course with no tile,
    # is invisible until somebody clicks.
    print("\n3b. THE HUB'S TILES MATCH THE COURSES THAT EXIST")
    sys.path.insert(0, str(ROOT / "tools"))
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_bs", ROOT / "tools" / "build_site.py")
    bs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bs)

    tiles = re.findall(
        r'<a class="course[^"]*" href="([^"]+)">\s*'
        r'<span class="num">([^<]+)</span>.*?<h4>(.*?)</h4>',
        index, re.S)
    def plain(t):
        return html.unescape(re.sub(r"<[^>]+>", "", t)).replace("&", "and")

    built = {c["slug"]: c for c in bs.COURSES}
    linked, tile_problems = set(), []
    for href, num, title in tiles:
        slug = href.split("/")[0]
        if slug not in built:
            tile_problems.append(f"tile {num} points at unknown course {slug!r}")
            continue
        linked.add(slug)
        expected = str(built[slug]["number"])
        if not num.replace("Course", "").strip().startswith(expected):
            tile_problems.append(f"tile for {slug} is labelled {num!r}, "
                                 f"course number is {expected}")
        shown, real = plain(title), built[slug]["title"].replace("&", "and")
        if shown.lower() != real.lower():
            tile_problems.append(f"tile for {slug} says {shown!r}, "
                                 f"the course is {real!r}")
    for slug in built:
        if slug not in linked:
            tile_problems.append(f"no tile for course {slug!r}")
    check(f"{len(tiles)} course tiles, one per built course",
          len(tiles) == len(built) and not tile_problems,
          "; ".join(tile_problems[:4]) or
          f"{len(tiles)} tiles against {len(built)} courses")

    # -- 4 -----------------------------------------------------------------
    print("\n4. NO ISSUING-BODY BRANDING")
    # -i matters. This check passed for weeks while six LOWERCASE occurrences
    # sat in the tree: a source URL in the README, a CSS selector example that
    # used the name as its substring, and an Avro namespace carried through
    # two note files and a lab script. A case-sensitive check for a proper
    # noun is not a check.
    hits = subprocess.run(
        ["grep", "-rli", "APSCHE", "--include=*.md", "--include=*.py",
         "--include=*.html", "--include=*.txt", "--include=*.sh", "."],
        cwd=ROOT, capture_output=True, text=True).stdout.split()
    # this file names the string it searches for, so it always matches itself
    hits = [h for h in hits
            if "node_modules" not in h and "audit_content.py" not in h]
    check("no APSCHE reference anywhere", not hits, str(hits))

    # -- 5 -----------------------------------------------------------------
    print("\n5. EVERY DECLARED 'NOT EXECUTED' FILE SAYS SO")
    marker = "*** NOT EXECUTED ***"
    declared = []
    for runner in ROOT.glob("tools/run_*.py"):
        declared += re.findall(r'"([\w./-]+\.(?:md|sql|js|pl|R))":\s*"',
                               runner.read_text())
    silent = [str(h.relative_to(ROOT))
              for name in set(declared)
              for h in ROOT.glob(f"labs/*/{name}")
              if marker not in h.read_text()]
    check(f"{len(set(declared))} declared files carry the marker",
          not silent, str(silent))

    # -- 5b ----------------------------------------------------------------
    # Two lab pages name the courses in which every experiment actually runs.
    # That claim had gone stale in both -- "one of only two such courses" was
    # written before Semester VI existed and only counted the courses that
    # announce the fact, missing 2, 7 and 9, which simply never needed to.
    print("\n5b. THE 'EVERY EXPERIMENT RUNS' COURSES")
    FULLY_RUN = {
        "2":    "labs/course-2-c",
        "7":    "labs/course-7-web",
        "9":    "labs/course-9-python-da",
        "12 A": "labs/course-12a-ml",
        "14 B": "labs/course-14b-timeseries",
    }
    stale = []
    for lab in (ROOT / "notes/sem-6/course-14b-time-series/lab.md",
                ROOT / "notes/sem-5/course-12a-machine-learning/lab.md"):
        text = lab.read_text()
        mo = re.search(r"[Ff]ive courses[^.]*?run every experiment[^.]*\.|"
                       r"[Ff]ive courses in\s+the programme can say that of "
                       r"every experiment(.*?)\.", text, re.S)
        if not mo:
            stale.append(f"{lab.name}: the five-course claim is missing")
            continue
        named = set(re.findall(r"\*\*(\d+(?: [AB])?)\*\*", mo.group(0)))
        # "this one" stands in for the page's own course
        own = "14 B" if "14b" in lab.parent.name else "12 A"
        named.add(own)
        if named != set(FULLY_RUN):
            stale.append(f"{lab.name} names {sorted(named)}, "
                         f"expected {sorted(FULLY_RUN)}")
    for course, labdir in FULLY_RUN.items():
        marked = [f for f in (ROOT / labdir).rglob("*")
                  if f.is_file() and "__pycache__" not in f.parts
                  and f.suffix not in (".pyc", ".png")
                  and marker in f.read_text(errors="ignore")]
        if marked:
            stale.append(f"Course {course} is listed as fully run but "
                         f"{marked[0].name} carries the marker")
    check(f"{len(FULLY_RUN)} courses run every experiment, and both pages "
          "agree", not stale, "; ".join(stale[:3]))

    # -- 6 -----------------------------------------------------------------
    print("\n6. MARKDOWN TABLES ARE WELL FORMED")
    ragged = []
    for m in mds:
        lines = m.read_text().splitlines()
        for i in range(len(lines) - 1):
            head, sep = lines[i].strip(), lines[i + 1].strip()
            if not (head.startswith("|") and sep.startswith("|")):
                continue
            if not set(sep) <= set("|-: "):
                continue
            width, j = cells(head), i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                if cells(lines[j]) != width:
                    ragged.append(f"{m.relative_to(ROOT)}:{j + 1}")
                j += 1
    check(f"no ragged rows across {len(mds)} files", not ragged,
          str(ragged[:6]))

    # -- 7 -----------------------------------------------------------------
    print("\n7. LINKS RESOLVE")
    broken = []
    for p in pages:
        text = p.read_text(errors="replace")
        # href inside a code sample is documentation, not a link
        text = re.sub(r"<code>.*?</code>", "", text, flags=re.S)
        text = re.sub(r"<pre.*?</pre>", "", text, flags=re.S)
        for mo in re.finditer(r'href="([^"#?][^"]*)"', text):
            href = mo.group(1)
            if href.startswith(("http", "mailto:", "#")):
                continue
            if not (p.parent / href.split("#")[0]).resolve().exists():
                broken.append(f"{p.relative_to(ROOT)} -> {href}")
    check(f"{len(pages)} pages, every internal link resolves", not broken,
          str(broken[:5]))

    # a link to a .md file is useless on the published site: the server hands
    # the visitor raw markdown, or the browser downloads it. Every such link
    # was unlinked; this keeps them from creeping back.
    md_links = []
    for p in pages:
        text = p.read_text(errors="replace")
        text = re.sub(r"<code>.*?</code>", "", text, flags=re.S)
        text = re.sub(r"<pre.*?</pre>", "", text, flags=re.S)
        for mo in re.finditer(r'href="([^"]*\.md[^"]*)"', text):
            md_links.append(f"{p.relative_to(ROOT)} -> {mo.group(1)}")
    check("no page links to a .md file", not md_links, str(md_links[:5]))

    # a link to a PDF has the same problem, and worse: it hands the visitor a
    # few hundred kilobytes of binary instead of a page. The syllabus PDFs
    # stay in docs/ because the extractor and verify_all.sh run against them,
    # but nothing the reader can click points at one -- the extracted TEXT is
    # what every claim here is checked against, so that is what is cited.
    pdf_links = []
    for p in pages:
        text = p.read_text(errors="replace")
        text = re.sub(r"<code>.*?</code>", "", text, flags=re.S)
        text = re.sub(r"<pre.*?</pre>", "", text, flags=re.S)
        for mo in re.finditer(r'href="([^"]*\.pdf[^"]*)"', text, re.I):
            pdf_links.append(f"{p.relative_to(ROOT)} -> {mo.group(1)}")
    check("no page links to a PDF", not pdf_links, str(pdf_links[:5]))

    # No page sends the reader into a code host or hands them a raw source
    # file. Both took them out of the study material: a github.com link opens
    # a code browser, and a relative link to a .py or .c file is source the
    # browser cannot render. The paths are still NAMED on the pages -- as
    # inline code -- they are simply not links.
    code_links = []
    source_suffixes = (".py", ".c", ".h", ".pl", ".sh", ".sql", ".java",
                       ".js", ".scala", ".r", ".pig", ".hql", ".conf",
                       ".rb", ".json", ".yml", ".yaml", ".avsc")
    for p in pages:
        text = p.read_text(errors="replace")
        text = re.sub(r"<code>.*?</code>", "", text, flags=re.S)
        text = re.sub(r"<pre.*?</pre>", "", text, flags=re.S)
        for mo in re.finditer(r'href="([^"]+)"', text):
            href = mo.group(1)
            if "github.com" in href or "githubusercontent" in href:
                code_links.append(f"{p.relative_to(ROOT)} -> {href}")
                continue
            if href.startswith(("http", "mailto:", "#")):
                continue
            target = href.split("#")[0].split("?")[0]
            if pathlib.PurePosixPath(target).suffix.lower() in source_suffixes:
                code_links.append(f"{p.relative_to(ROOT)} -> {href}")
    check("no page links to a code host or a source file",
          not code_links, str(code_links[:5]))

    # The administrative metadata was stripped out: which page of the source
    # document a topic sits on, how many credits a course carries, how many
    # hours a week it meets. None of it helps anyone study, all of it dates,
    # and it made the notes read as a transcription rather than a course.
    #
    # The patterns are deliberately narrow. "credits: 4" is a field name in
    # Course 10's MongoDB documents and "page 500" is pagination in the same
    # course -- both are content, and a looser check would delete them.
    admin = []
    patterns = [
        (r"\b\d+\s*credits?\b",            "a credit count"),
        (r"\bcredit (count|hours?|load|weight)\b", "a credit reference"),
        (r"\bhrs?\s*/\s*w(?:k|eek)\b",      "an hours-per-week figure"),
        (r"\bsyllabus\s*\(?pages?\s*\d+",   "a syllabus page number"),
        (r"\bverbatim,\s*pages?\s*\d+",     "a syllabus page number"),
        (r"^Syllabus source: pages?\s*\d+",  "a syllabus page number"),
    ]
    # index.html is hand-maintained, and the first version of this check looked
    # only at markdown -- which is how "listed by title and credits only"
    # survived on the hub while every note file was clean.
    for m in mds + [ROOT / "index.html"]:
        if m.parts[-2].startswith("syllabus-extracted") or \
                m.name.startswith("syllabus-extracted"):
            continue          # the verbatim extraction is the source, not prose
        text = m.read_text()
        for pattern, what in patterns:
            for mo in re.finditer(pattern, text, re.M | re.I):
                line = text.count("\n", 0, mo.start()) + 1
                admin.append(f"{m.relative_to(ROOT)}:{line} {what}"
                             f" -- {mo.group(0)!r}")
    check("no credit, hours or syllabus-page references", not admin,
          str(admin[:5]))

    # a contents entry pointing at a heading that is not on the page is worse
    # than no contents at all -- the click does nothing and the reader assumes
    # the section is missing
    toc_bad, toc_n = [], 0
    for p in pages:
        h = p.read_text(errors="replace")
        if 'class="toc"' not in h:
            continue
        ids = set(re.findall(r'<h[23][^>]*id="([^"]+)"', h))
        for a in re.findall(r'<li><a href="#([^"]+)"', h):
            toc_n += 1
            if a not in ids:
                toc_bad.append(f"{p.relative_to(ROOT)} #{a}")
    check(f"{toc_n} on-page contents anchors resolve", not toc_bad,
          str(toc_bad[:5]))

    md_broken = []
    for name in ("README.md", "SYLLABUS-MAP.md", "SYLLABUS-REVIEW.md",
                 "STUDY-PLAN.md"):
        md = ROOT / name
        body = re.sub(r"```.*?```", "", md.read_text(), flags=re.S)
        for mo in re.finditer(r"\]\(([^)#][^)]*)\)", body):
            href = mo.group(1)
            if href.startswith(("http", "mailto:", "#")):
                continue
            if not (md.parent / href.split("#")[0]).resolve().exists():
                md_broken.append(f"{name} -> {href}")
    check("top-level markdown links resolve", not md_broken,
          str(md_broken[:5]))

    # The notes name lab files constantly. They used to LINK to them, and this
    # check followed the links; now they are plain inline-code paths, so it
    # follows the text instead. Same guarantee either way -- a renamed lab
    # silently breaks every reference to it, and nothing else here would
    # notice -- but it no longer depends on those references being hyperlinks.
    note_broken, n_links = [], 0
    repo_path = re.compile(r"`((?:labs|notes|tools|docs|css)/[\w./-]+)`")
    for md in ROOT.glob("notes/**/*.md"):
        body = re.sub(r"```.*?```", "", md.read_text(), flags=re.S)
        for mo in re.finditer(repo_path, body):
            target = mo.group(1).rstrip("/")
            n_links += 1
            if not (ROOT / target).exists():
                note_broken.append(f"{md.relative_to(ROOT)} -> {mo.group(1)}")
        for mo in re.finditer(r"\]\((\.\./[^)#]*)\)", body):
            href = mo.group(1)
            n_links += 1
            if not (md.parent / href.split("#")[0]).resolve().exists():
                note_broken.append(f"{md.relative_to(ROOT)} -> {href}")
    check(f"{n_links} note-to-lab references resolve", not note_broken,
          str(note_broken[:5]))

    # -- 8 -----------------------------------------------------------------
    print("\n8. WHITESPACE HYGIENE")
    tabs = [str(m.relative_to(ROOT)) for m in mds if "\t" in m.read_text()]
    check("no tabs in markdown", not tabs, str(tabs[:4]))
    trailing = [str(m.relative_to(ROOT)) for m in mds
                if any(ln.rstrip() != ln and ln.strip() and not ln.endswith("  ")
                       for ln in m.read_text().splitlines())]
    check("no stray trailing whitespace", not trailing, str(trailing[:4]))

    print("\n" + "=" * 62)
    print(f"{len(problems)} PROBLEM(S)" if problems else "AUDIT CLEAN")
    print("=" * 62)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
