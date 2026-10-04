"""Drives 04_form_controls.html in Chromium: fills every control, then resets the form.

Run by tools/data-science/capture_lab_outputs.py, through tools/data-science/web_lab.py. The
form is not submitted: it posts to /submit, which there is no server behind.
"""
from web_lab import open_page

with open_page("04_form_controls.html") as p:
    p.fill("#name", "Asha Rao")
    p.fill("#email", "asha@example.com")
    p.fill("#pw", "Passw0rd!")
    p.fill("#age", "19")
    p.fill("#dob", "2007-03-14")
    p.fill("#about", "Second-year data science student.")
    p.check("#gf")
    p.check("#gm")                                # a second radio in the same group
    print(f"checked Female, then Male: Female is now {p.is_checked('#gf')}, Male {p.is_checked('#gm')}"
          " -- one name, so one choice")
    p.check("#s1")
    p.check("#s3")
    p.select_option("#course", index=1)
    sent = p.evaluate("""() => [...new FormData(document.querySelector('form'))]
        .filter(([k, v]) => typeof v === 'string').map(([k, v]) => k + '=' + v)""")
    print("what the form would send, from FormData:")
    for pair in sent:
        print(f"  {pair}")
    assert "gender=M" in sent and sum(s.startswith("subjects=") for s in sent) == 2, sent
    p.screenshot("filled in", full_page=True)
    p.click("button[type=reset]")
    print(f"after Reset: name is {p.input_value('#name')!r}, Male checked {p.is_checked('#gm')}")
    assert p.input_value("#name") == "" and not p.is_checked("#gm")
