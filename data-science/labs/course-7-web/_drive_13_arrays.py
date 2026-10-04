"""Drives 13_arrays.html in Chromium: adds a student, tries a duplicate, sorts, searches and
deletes, reading the table and the summary after each.

Run by tools/data-science/capture_lab_outputs.py, through tools/data-science/web_lab.py.
"""
from web_lab import open_page

ROWS = "() => [...document.querySelectorAll('#body tr')].map(tr => [...tr.cells].slice(0, 4).map(td => td.textContent).join(' | '))"


def show(p, what):
    print(f"\n{what}:")
    for r in p.evaluate(ROWS):
        print(f"  {r}")
    print(f"  {p.text('#summary')}")


with open_page("13_arrays.html") as p:
    show(p, "as it opens")
    p.fill("#roll", "106")
    p.fill("#name", "Divya")
    p.fill("#marks", "88")
    p.select_option("#dept", "Stats")
    p.click("#add")
    show(p, "after adding Divya, roll 106")
    p.click("#add")
    print(f"\nadding roll 106 again: {p.text('#err')!r}")
    assert "already exists" in p.text("#err")
    p.click("th[data-key=marks]")
    p.click("th[data-key=marks]")
    show(p, "sorted by marks, highest first (the heading clicked twice)")
    p.screenshot("sorted by marks", full_page=True)
    p.fill("#q", "ra")
    show(p, "searching for 'ra'")
    p.fill("#q", "")
    p.click("button.del[data-roll='106']")
    show(p, "after deleting roll 106")
    p.screenshot("after the delete", full_page=True)
