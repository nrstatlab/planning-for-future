"""Drives 14_json_table.html in Chromium: reads the table it builds from students.json, then
sorts and filters it.

Run by tools/data-science/capture_lab_outputs.py, through tools/data-science/web_lab.py, which
serves the folder over http, so the page's fetch() of students.json works.
"""
from web_lab import open_page

ROWS = "() => [...document.querySelectorAll('#body tr')].map(tr => [...tr.cells].map(td => td.textContent).join(' | '))"


def show(p, what):
    print(f"\n{what}:   status {p.text('#status')!r}")
    for r in p.evaluate(ROWS):
        print(f"  {r}")
    print(f"  {p.text('#summary')}")


with open_page("14_json_table.html") as p:
    p.wait_for_selector("#body tr")
    show(p, "loaded from students.json")
    missing = p.evaluate("document.querySelectorAll('#body td.missing').length")
    print(f"  {missing} cell(s) shown as a dash: a student with no marks")
    p.screenshot("as loaded", full_page=True)
    p.click("th[data-key=total]")
    p.click("th[data-key=total]")
    show(p, "sorted by total, highest first")
    p.fill("#q", "stat")
    show(p, "filtered for 'stat'")
    p.screenshot("filtered", full_page=True)
