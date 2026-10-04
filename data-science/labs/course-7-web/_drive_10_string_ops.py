"""Drives 10_string_ops.html in Chromium: types two strings, and reads the results.

Run by tools/data-science/capture_lab_outputs.py, through tools/data-science/web_lab.py.
"""
from web_lab import open_page

with open_page("10_string_ops.html") as p:
    for text in ("Data Science", "A man, a plan, a canal: Panama"):
        p.fill("#text", text)
        print(f"\ntyped {text!r}; the page shows:")
        print("\n".join("  " + ln for ln in p.text("#out").split("\n")))
        p.screenshot(f"after typing {text!r}", full_page=True)
    assert "true" in p.text("#out").lower() or "yes" in p.text("#out").lower()
