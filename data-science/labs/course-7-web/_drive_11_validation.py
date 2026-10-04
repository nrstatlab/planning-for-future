"""Drives 11_validation.html in Chromium: submits it empty, wrongly filled, then correctly.

Run by tools/data-science/capture_lab_outputs.py, through tools/data-science/web_lab.py.
"""
from web_lab import open_page

FIELDS = ["name", "email", "mobile", "password", "confirm", "terms"]


def errors(p):
    return {f: p.text(f"#{f}-error") for f in FIELDS if p.text(f"#{f}-error")}


def fill(p, **v):
    for f in FIELDS[:-1]:
        p.fill(f"#{f}", v.get(f, ""))
    p.set_checked("#terms", v.get("terms", False))
    p.click("button[type=submit]")


with open_page("11_validation.html") as p:
    fill(p)
    print("submitted empty:")
    for f, e in errors(p).items():
        print(f"  {f:<9} {e}")
    p.screenshot("submitted empty", full_page=True)

    fill(p, name="Asha Rao", email="asha@", mobile="1234567890", password="password",
         confirm="Password")
    print("\nsubmitted with a bad email, mobile and password, the passwords not matching, "
          "and the terms not accepted:")
    for f, e in errors(p).items():
        print(f"  {f:<9} {e}")
    assert set(errors(p)) == {"email", "mobile", "password", "confirm", "terms"}
    p.screenshot("submitted with mistakes", full_page=True)

    fill(p, name="Asha Rao", email="asha@nri.ac.in", mobile="9876543210", password="Passw0rd!",
         confirm="Passw0rd!", terms=True)
    print(f"\nsubmitted correctly: errors {errors(p)}, status {p.text('#status')!r}")
    assert not errors(p) and p.text("#status") == "All fields valid."
    p.screenshot("submitted correctly", full_page=True)
