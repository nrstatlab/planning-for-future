"""Drives 12_greeting.html in Chromium: reads the greeting at the fixed clock, then at
four other hours chosen from the page's own list, with a name typed in.

Run by tools/data-science/capture_lab_outputs.py, through tools/data-science/web_lab.py, with
the clock fixed at 09:00 on 4 October 2026, Indian time.
"""
from web_lab import open_page

with open_page("12_greeting.html") as p:
    p.wait_for_timeout(1200)                       # let the clock tick once
    print(f"at the real (fixed) clock: {p.text('#greet')!r}, the clock shows {p.text('#clock')}")
    assert p.text("#greet") == "Good morning!" and p.text("#clock") == "09:00:00"
    p.fill("#name", "Asha")
    for hour in ("9", "14", "19", "22"):
        p.select_option("#hour", hour)
        cls = p.evaluate("document.body.className")
        print(f"  hour {hour.rjust(2)}:00 -> {p.text('#greet')!r}  (body class {cls!r})")
        p.screenshot(f"pretending the hour is {hour}:00")
