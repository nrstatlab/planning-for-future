#!/usr/bin/env python3
"""Build topics.html -- an A-Z catalogue of everything the site teaches.

The site is filed by syllabus position, so a reader who knows the topic but not
its position has nowhere to start. Every page already carries a hand-written
"Topics Covered" chip row; this collects those into one browsable index.

The chips are the vocabulary, so the index says what the pages actually say --
nothing here is invented, and re-running it keeps the index true to the site.
"""
import html as html_mod
import pathlib
import re
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "topics.html"

CHIP_RE = re.compile(r'<span class="chip">(.*?)</span>', re.S)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)

# Chips that name a page's furniture rather than a topic it teaches.
FURNITURE = {
    "exam questions from this unit", "mistakes that cost marks",
    "practice problems", "not executed", "what to be able to do after this unit",
    "what goes in the lab record", "if you are running this yourself",
    "case study", "concept", "definition", "introductory pages",
    "types of questions", "the link forward", "after the install",
    "scope and coverage", "how to use this page", "summary", "notes",
}
# Above this length a chip is a sentence making a point, not a topic name.
MAX_TOPIC_CHARS = 45

# A chip carrying one of these is making a statement rather than naming a thing
# -- "An EBS volume is in ONE availability zone", "the billing alarm, which
# comes first". An index files things, not claims about them.
PROSE_MARKERS = (", which", ", and ", " that ", " is ", " are ", " was ",
                 " does ", " do ", " you ", " your ", " it ", " not ")
PROSE_OPENERS = ("a note on", "a complete example", "a search", "a second",
                 "an alarm", "read ", "why ", "how ", "what ", "when ")

# Standard index practice: file "The Apriori algorithm" under A, not T.
_ARTICLE_RE = re.compile(r"^(the|a|an)\s+", re.I)


def plain(text):
    return " ".join(html_mod.unescape(re.sub(r"<[^>]+>", " ", text)).split())


def is_topic(chip):
    low = chip.lower().strip(" .:")
    if low in FURNITURE or len(chip) > MAX_TOPIC_CHARS or len(chip) < 2:
        return False
    if not chip[0].isalnum():         # drops emoji-led section markers
        return False
    if any(low.startswith(o) for o in PROSE_OPENERS):
        return False
    if any(m in f" {low} " for m in PROSE_MARKERS):
        return False
    if re.search(r"\bcourse \d", low):   # the site no longer labels by course number
        return False
    return True


def file_under(topic):
    """The form a topic is alphabetised and displayed by."""
    return _ARTICLE_RE.sub("", topic).strip() or topic


def collect():
    """topic -> {page path: page title}"""
    topics = defaultdict(dict)
    for p in sorted(ROOT.rglob("*.html")):
        if ".git" in p.parts or "archive" in p.parts or p.name == "topics.html":
            continue
        text = p.read_text(errors="replace")
        chips = [plain(m.group(1)) for m in CHIP_RE.finditer(text)]
        if not chips:
            continue
        m = TITLE_RE.search(text)
        title = plain(m.group(1)) if m else p.stem
        rel = p.relative_to(ROOT).as_posix()
        for c in chips:
            if is_topic(c):
                topics[file_under(c)][rel] = title
    return topics


def bucket(topic):
    ch = topic[0].upper()
    return ch if ch.isalpha() else "0-9"


def render(topics):
    by_letter = defaultdict(list)
    for t in sorted(topics, key=lambda s: s.lower()):
        by_letter[bucket(t)].append(t)
    letters = [l for l in ["0-9"] + [chr(c) for c in range(65, 91)] if l in by_letter]

    rail = "\n      ".join(
        f'<a href="#{l.lower().replace("-", "")}">{l}</a>' for l in letters)

    blocks = []
    for l in letters:
        rows = []
        for t in by_letter[l]:
            pages = topics[t]
            links = " · ".join(
                f'<a href="{html_mod.escape(path)}">{html_mod.escape(title)}</a>'
                for path, title in sorted(pages.items(), key=lambda kv: kv[1]))
            rows.append(f'      <dt>{html_mod.escape(t)}</dt>\n'
                        f'      <dd>{links}</dd>')
        blocks.append(
            f'  <section class="letter" id="{l.lower().replace("-", "")}">\n'
            f'    <h2>{l}</h2>\n    <dl>\n' + "\n".join(rows) + "\n    </dl>\n  </section>")

    n_topics = len(topics)
    n_pages = len({p for d in topics.values() for p in d})
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>All Topics A–Z — NRSTATLAB</title>
<meta name="description" content="Every topic taught on NRSTATLAB in one A–Z list — {n_topics} topics across {n_pages} pages of statistics, data science and machine learning, each linked to the page that covers it.">
<meta property="og:title" content="All Topics A–Z — NRSTATLAB">
<meta property="og:description" content="Every topic taught on NRSTATLAB in one A–Z list — {n_topics} topics across {n_pages} pages, each linked to the page that covers it.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="NRSTATLAB">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#0f4c81">
<link rel="stylesheet" href="assets/nrstatlab.css">
</head>
<body>

<header class="topics-head">
  <div class="wrap">
    <p class="eyebrow"><a href="index.html">NRSTATLAB</a> &rsaquo; Topics</p>
    <h1>Every topic, A&ndash;Z</h1>
    <p class="lede">{n_topics} topics across {n_pages} pages. If you know what you want to
    read about but not where it sits in a syllabus, start here.</p>
    <nav class="alpha" aria-label="Jump to letter">
      {rail}
    </nav>
  </div>
</header>

<main class="wrap topics">
{chr(10).join(blocks)}
</main>

<footer>
  <div class="wrap">
    <span><b>NRSTATLAB</b> &mdash; study material for statistics and data science</span>
    <span><a href="index.html">Back to the home page</a></span>
  </div>
</footer>

</body>
</html>
"""


def main(apply=False):
    topics = collect()
    n_pages = len({p for d in topics.values() for p in d})
    print(f"{len(topics)} topics from {n_pages} pages")
    if apply:
        OUT.write_text(render(topics))
        print(f"wrote {OUT.relative_to(ROOT)}")
    else:
        print("dry run -- pass --apply to write")
        for t in sorted(topics, key=lambda s: -len(topics[s]))[:8]:
            print(f"   {len(topics[t])} pages  {t}")


if __name__ == "__main__":
    main(apply="--apply" in sys.argv)
