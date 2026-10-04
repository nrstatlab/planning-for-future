"""Drives 15_weather.html in Chromium: shows the saved sample, then tries a real fetch.

Run by tools/data-science/capture_lab_outputs.py, through tools/data-science/web_lab.py. A real
fetch needs an OpenWeatherMap key, and api.openweathermap.org cannot be reached from where
these labs are checked, so the driver shows what the page does then: it reports the failure
in its status line. The sample is the page's own offline path, through the same summarise().
"""
from web_lab import open_page

with open_page("15_weather.html", height=760) as p:
    p.click("#demo")
    p.wait_for_selector("#out:not([hidden])")
    print("the sample response, through summarise():")
    for f in ("place", "temp", "cond", "feels", "hum", "press", "wind", "cloud"):
        print(f"  {f:<6} {p.text('#' + f)}")
    p.screenshot("the saved sample", full_page=True)

    p.fill("#city", "Hyderabad")
    p.fill("#key", "no-key-here")
    p.allow_failure("https://api.openweathermap.org/")      # stopped, as it could not be reached
    p.page.route("https://api.openweathermap.org/**", lambda route: route.abort("internetdisconnected"))
    p.click("#wxform button[type=submit]")
    p.wait_for_function("document.getElementById('status').textContent !== 'Fetching…'")
    print(f"\na real fetch, which cannot reach the API from here: status {p.text('#status')!r}")
    p.screenshot("a fetch that failed", full_page=True)
