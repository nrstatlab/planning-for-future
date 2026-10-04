"""Drives 05_calendar.html in Chromium: reads the month it opens on, then moves to others.

Run by tools/data-science/capture_lab_outputs.py, through tools/data-science/web_lab.py, with
the clock fixed at 4 October 2026, so the page opens on October 2026 with the 4th marked.
"""
from web_lab import open_page

GRID = """() => [...document.querySelectorAll('#cal tbody tr')]
    .map(tr => [...tr.cells].map(td => td.textContent.padStart(3)).join(''))"""


def show(p, what):
    print(f"\n{p.text('#cal caption')}   ({what})")
    print("  " + "".join(d.rjust(3) for d in p.evaluate(
        "() => [...document.querySelectorAll('#cal thead th')].map(th => th.textContent)")))
    for row in p.evaluate(GRID):
        print("  " + row)


with open_page("05_calendar.html") as p:
    show(p, "today's month")
    print(f"  today, marked: {p.text('#cal td.today')}")
    assert p.text("#cal caption") == "October 2026" and p.text("#cal td.today") == "4"
    p.screenshot("October 2026, the month it opens on", full_page=True)

    p.click("#prev")
    p.click("#prev")
    show(p, "after Previous twice")
    first = p.evaluate("() => [...document.querySelectorAll('#cal tbody tr')[0].cells]"
                       ".findIndex(td => td.textContent === '1')")
    print(f"  1 August 2026 is in column {first}, a Saturday")
    assert first == 6

    p.select_option("#month", "2")
    p.fill("#year", "2024")
    p.dispatch_event("#year", "change")
    show(p, "February 2024, chosen from the list")
    days = p.evaluate("() => document.querySelectorAll('#cal tbody td:not(.empty)').length")
    print(f"  {days} days: 2024 is a leap year")
    assert days == 29
    p.screenshot("February 2024", full_page=True)
