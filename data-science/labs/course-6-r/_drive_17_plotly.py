"""Drives 17_plotly.R, and shows the charts it makes.

Run by tools/data-science/capture_lab_outputs.py, with a Python that has Playwright. Rscript
builds each chart and then has nowhere to show it, so this runs the script as Rscript would,
except that each chart it would show is saved as a web page. Each page is then opened in
Chromium for a screenshot, and the hover text of one point is read back, which is the
interactivity the experiment is about.
"""
import pathlib
import subprocess

from playwright.sync_api import sync_playwright

# print.htmlwidget is what shows a chart; this one saves it instead, and says so
SAVE_EACH_CHART = r'''
shown <- 0
save_chart <- function(x, ...) {
  shown <<- shown + 1
  file <- sprintf("chart%d.html", shown)
  htmlwidgets::saveWidget(x, file, selfcontained = TRUE)
  cat(sprintf("[chart %d, which RStudio would show in its Viewer, saved as %s]\n", shown, file))
  invisible(x)
}
registerS3method("print", "htmlwidget", save_chart, envir = asNamespace("htmlwidgets"))
source("17_plotly.R", echo = FALSE, print.eval = TRUE)
'''
r = subprocess.run(["Rscript", "--vanilla", "-e", SAVE_EACH_CHART],
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
print(r.stdout, end="")
assert r.returncode == 0, "the R script failed"

charts = sorted(pathlib.Path(".").glob("chart*.html"), key=lambda p: int(p.stem[5:]))
assert len(charts) == 3, f"expected three charts, got {len(charts)}"

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 760, "height": 460})
    shots = 0

    def screenshot(what):
        global shots
        shots += 1
        page.screenshot(path=f"screens/{shots}.png")
        print(f"  [screenshot {shots}: {what}]")

    for n, chart in enumerate(charts, 1):
        page.goto(chart.resolve().as_uri())
        page.wait_for_selector(".plot-container .main-svg")
        page.wait_for_timeout(500)
        title = page.text_content(".gtitle") if page.query_selector(".gtitle") else "(no title)"
        traces = page.evaluate("document.querySelector('.js-plotly-plot').data.length")
        print(f"\nchart {n}: \"{title}\", {traces} trace(s)")
        screenshot(f"chart {n}")
        if n == 2:                                   # the native scatter, with its hover text
            point = page.query_selector_all(".scatterlayer .point")[0]
            box = point.bounding_box()
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_selector(".hovertext")
            hover = " / ".join(t.text_content() for t in page.query_selector_all(".hovertext text"))
            print(f"  hovering over a point shows: {hover}")
            assert "Name:" in hover and "Marks:" in hover, hover
            screenshot("chart 2, hovering over a point")
    browser.close()
