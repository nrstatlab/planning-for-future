"""Drives 06_subscribe.html in Chromium: submits it empty, then filled in.

Run by tools/data-science/capture_lab_outputs.py, through tools/data-science/web_lab.py.
"""
from web_lab import open_page

with open_page("06_subscribe.html") as p:
    p.click("button[type=submit]")
    print(f"submitted empty:  email says {p.text('#email-error')!r}")
    print(f"                  consent says {p.text('#consent-error')!r}")
    assert p.text("#email-error") and p.text("#consent-error")
    p.screenshot("submitted empty", full_page=True)

    p.fill("#email", "asha@example.com")
    p.fill("#name", "Asha Rao")
    p.check("#i1")
    p.check("#consent")
    p.click("button[type=submit]")
    print(f"filled in:        status says {p.text('#status')!r}")
    assert p.text("#status") == "Subscribed asha@example.com."
    p.screenshot("filled in and submitted", full_page=True)
