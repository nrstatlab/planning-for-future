"""Drives 18_shiny_app.R the way a student would use it, and checks what it shows.

Run by tools/data-science/capture_lab_outputs.py, with a Python that has Playwright. It starts
the app with shiny::runApp(), as its header says to, opens it in Chromium, uploads a CSV of
the ten students the other experiments use, and goes through the three tabs: the data, the
summary, and the histogram, first of hours and then of marks with fewer bins. Each step is
checked against what the page shows, and screenshotted.
"""
import socket
import subprocess
import time
import urllib.request

from playwright.sync_api import sync_playwright

CSV = """name,section,hours,marks
Ananya,A,9,85
Bhavana,A,5,62
Charan,B,11,91
Divya,B,4,55
Eshwar,A,7,74
Fiona,C,8,79
Gopal,C,3,48
Harika,B,10,88
Ismail,A,6,68
Jyothi,C,2,41
"""
with open("students.csv", "w") as fh:
    fh.write(CSV)

with socket.socket() as s:                     # a free port
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
app = subprocess.Popen(["Rscript", "--vanilla", "-e",
                        f"shiny::runApp('18_shiny_app.R', port = {port}, launch.browser = FALSE)"],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
url = f"http://127.0.0.1:{port}/"
for _ in range(120):
    try:
        urllib.request.urlopen(url, timeout=1)
        break
    except OSError:
        if app.poll() is not None:
            raise SystemExit("the app stopped:\n" + app.stdout.read())
        time.sleep(0.5)
else:
    raise SystemExit("the app did not start")
print("started the app with shiny::runApp('18_shiny_app.R')")

shots = 0
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1000, "height": 640})

        def screenshot(what):
            global shots
            page.wait_for_timeout(400)
            shots += 1
            page.screenshot(path=f"screens/{shots}.png")
            print(f"  [screenshot {shots}: {what}]")

        page.goto(url)
        page.wait_for_selector("text=CSV Explorer")
        print(f"page title: {page.text_content('h2')}")
        print(f"before an upload, the Data tab shows {len(page.query_selector_all('#preview table'))} table(s)")

        page.set_input_files("input#file", "students.csv")
        page.wait_for_selector("#preview table")
        header = [th.inner_text() for th in page.query_selector_all("#preview th")]
        rows = page.query_selector_all("#preview tbody tr")
        print(f"\nuploaded students.csv; the Data tab shows the columns {header}, {len(rows)} rows")
        print(f"  first row: {[td.inner_text() for td in rows[0].query_selector_all('td')]}")
        assert header == ["name", "section", "hours", "marks"] and len(rows) == 10
        choices = sorted(page.evaluate("Object.keys($('#column')[0].selectize.options)"))
        print(f"  the column picker offers the numeric columns: {choices}")
        assert set(choices) == {"hours", "marks"}
        screenshot("the Data tab, after the upload")

        page.click("a[data-value='Summary']")
        page.wait_for_selector("#summary:not(:empty)")
        summary = page.inner_text("#summary")
        print("\nthe Summary tab shows summary(data()):")
        print("\n".join("  " + ln for ln in summary.rstrip().split("\n")))
        assert "Mean   : 6.5" in summary and "Mean   :69.1" in summary
        screenshot("the Summary tab")

        page.click("a[data-value='Plot']")
        page.wait_for_selector("#histogram img")
        column = page.evaluate("$('#column').val()")
        print(f"\nthe Plot tab draws a histogram of {column}")
        screenshot("the Plot tab, hours")

        page.evaluate("$('#column')[0].selectize.setValue('marks')")
        page.evaluate("$('#bins').data('ionRangeSlider').update({from: 8})")
        page.evaluate("$('#bins').trigger('change')")
        page.wait_for_function("$('#column').val() === 'marks'")
        page.wait_for_timeout(1500)
        column = page.evaluate("$('#column').val()")
        print(f"chose the column {column} and {page.input_value('#bins')} bins; the histogram is redrawn")
        assert page.input_value("#bins") == "8"
        screenshot("the Plot tab, marks in 8 bins")
        browser.close()
finally:
    app.terminate()
    app.wait(timeout=20)
print("\nstopped the app")
