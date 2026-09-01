#!/usr/bin/env python3
"""Structural checks for the Machine Learning notes.

The notes are hand-authored HTML with no build step, so these checks stand in
for a compiler. They guard the classes of defect that have actually bitten this
material: unescaped `<` or `&` inside code panes, unbalanced MathJax
delimiters, stray `$` used as a delimiter, broken links between pages, code
tabs pointing at panes that do not exist, Python panes that no longer parse,
and the algorithm inventory drifting away from what the pages claim.

Run from anywhere:  python scripts/check_notes.py
Exit code 0 = clean, 1 = at least one failure.
"""
import ast
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = sorted(p for p in ROOT.glob("*.html") if p.name != "ml_self_study_notes.html")

TOPIC_PAGES = [p for p in PAGES if re.match(r"unit\d-", p.name)]
UNIT_PAGES = [p for p in PAGES if re.match(r"unit\d\.html$", p.name)]

EXPECTED_ALGORITHMS = 23
EXPECTED_EXAMPLES = EXPECTED_ALGORITHMS * 3

failures: list[str] = []
notes: list[str] = []


def check(ok: bool, label: str, detail: str = "") -> None:
    (notes if ok else failures).append(
        f"  {'ok  ' if ok else 'FAIL'}  {label}" + ("" if ok or not detail else f": {detail}")
    )


def code_panes(src: str):
    return re.findall(
        r'<div class="code-pane[^"]*" id="([^"]+)">'
        r'<pre class="language-(\w+)"><code>(.*?)</code></pre></div>',
        src, re.S)


def strip_code(src: str) -> str:
    """Body text with <pre> blocks and <script>/<style> removed."""
    return re.sub(r"<pre.*?</pre>|<script.*?</script>|<style.*?</style>", "", src, flags=re.S)


# ── per-page checks ───────────────────────────────────────────────────────
bad_delims, stray_dollar, raw_lt, bare_amp, bad_py = [], [], [], [], []
total_panes = total_algos = total_examples = 0

for page in PAGES:
    src = page.read_text(encoding="utf-8")
    prose = strip_code(src)

    # MathJax delimiters must balance, and `$` must never be one.
    for op, cl in ((r"\(", r"\)"), (r"\[", r"\]")):
        if prose.count(op) != prose.count(cl):
            bad_delims.append(f"{page.name} {op}={prose.count(op)} {cl}={prose.count(cl)}")
    for m in re.finditer(r"\$(?=\S)([^$\n]{1,300}?)(?<=\S)\$", prose):
        if re.search(r"\\[a-zA-Z]|\^|_\{", m.group(1)):        # looks like TeX
            stray_dollar.append(f"{page.name}: {m.group(0)[:44]}")

    # Code panes must be escaped and must parse.
    panes = code_panes(src)
    total_panes += len(panes)
    for pid, lang, body in panes:
        if re.search(r"<(?!/?(?:code|pre)\b)", body):
            raw_lt.append(f"{page.name}#{pid}")
        if re.search(r"&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9a-fA-F]+;)", body):
            bare_amp.append(f"{page.name}#{pid}")
        if lang == "python":
            try:
                ast.parse(html.unescape(body))
            except SyntaxError as exc:
                bad_py.append(f"{page.name}#{pid} line {exc.lineno}")

    total_algos += len(re.findall(r'<div class="algo-head" id="', src))
    total_examples += len(re.findall(r'<div class="ex ex-\w+">', src))

check(not bad_delims, "MathJax delimiters balance on every page", "; ".join(bad_delims))
check(not stray_dollar, "no `$` used as a math delimiter", "; ".join(stray_dollar))
check(not raw_lt, "no raw '<' inside code panes", ", ".join(raw_lt))
check(not bare_amp, "no bare '&' inside code panes", ", ".join(bare_amp))
check(not bad_py, "every Python pane parses", ", ".join(bad_py))

# ── inventory ─────────────────────────────────────────────────────────────
check(total_algos == EXPECTED_ALGORITHMS,
      f"{EXPECTED_ALGORITHMS} algorithms across the topic pages", f"found {total_algos}")
check(total_examples == EXPECTED_EXAMPLES,
      "3 worked examples per algorithm", f"found {total_examples}")
check(total_panes == EXPECTED_ALGORITHMS * 2,
      "a Python and an R pane for every algorithm", f"found {total_panes}")
check(len(TOPIC_PAGES) == 9, "9 topic pages", f"found {len(TOPIC_PAGES)}")
check(len(UNIT_PAGES) == 4, "4 unit pages", f"found {len(UNIT_PAGES)}")

# ── links ─────────────────────────────────────────────────────────────────
anchors: dict[str, set[str]] = {p.name: set(re.findall(r'\bid="([^"]+)"', p.read_text(encoding="utf-8")))
                                for p in PAGES}
broken, missing_tabs = [], []
for page in PAGES:
    src = page.read_text(encoding="utf-8")
    for href in re.findall(r'href="([^"#][^"]*?)(?:#([^"]*))?"', src):
        target, frag = href
        if target.startswith(("http:", "https:", "mailto:")):
            continue
        dest = (ROOT / target).resolve()
        if not dest.exists():
            broken.append(f"{page.name} -> {target}")
        elif frag and frag not in anchors.get(target, set()):
            broken.append(f"{page.name} -> {target}#{frag}")
    for frag in re.findall(r'href="#([^"]+)"', src):
        if frag not in anchors[page.name]:
            broken.append(f"{page.name} -> #{frag}")
    for pane_id in re.findall(r'data-pane="([^"]+)"', src):
        if pane_id not in anchors[page.name]:
            missing_tabs.append(f"{page.name}#{pane_id}")

check(not broken, "every internal link and anchor resolves", "; ".join(broken[:6]))
check(not missing_tabs, "every code tab points at a real pane", ", ".join(missing_tabs))

# ── shared assets ─────────────────────────────────────────────────────────
check((ROOT / "css" / "styles.css").exists(), "css/styles.css present")
check((ROOT / "js" / "notes.js").exists(), "js/notes.js present")
no_css = [p.name for p in PAGES if 'href="css/styles.css"' not in p.read_text(encoding="utf-8")]
check(not no_css, "every page links the shared stylesheet", ", ".join(no_css))
no_js = [p.name for p in TOPIC_PAGES if 'src="js/notes.js"' not in p.read_text(encoding="utf-8")]
check(not no_js, "every topic page loads the tab script", ", ".join(no_js))

# ── report ────────────────────────────────────────────────────────────────
print("\n".join(notes))
if failures:
    print("\n".join(failures))
    print(f"\n{len(failures)} check(s) failed.")
    sys.exit(1)
print(f"\nAll {len(notes)} checks passed across {len(PAGES)} pages.")
