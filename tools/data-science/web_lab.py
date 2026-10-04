"""Open a lab web page in Chromium, as a student would in a browser, for capture_lab_outputs.py.

    python3 web_lab.py 01_formatting.html      # from the page's folder: open it, describe it,
                                               # and take a screenshot of the whole page

A driver beside a page (_drive_10_string_ops.py) uses open_page() to do more: type into it,
press its buttons, and screenshot each state. Either way the page is served over http from a
local server, as the lab notes say to do (a module script or a fetch() does not work from a
file:// address), and:

  - the clock is fixed at CLOCK, in Indian time, so a page that shows the date or the time
    shows the same thing on every run (a driver can open a page without it: jQuery's
    animations time themselves by the clock, and stand still when it does);
  - jQuery, which 16_jquery.html loads from code.jquery.com, is served from npm's copy of the
    same release, as that host cannot be reached from here; the page's integrity attribute
    makes the browser check that the copy is the same file, byte for byte;
  - anything the page writes to the console is printed, and an uncaught error, or a file the
    page asks for and cannot get, fails the run.

Screenshots go to screens/1.png, screens/2.png, ... in the order taken.
"""
import contextlib
import functools
import http.server
import pathlib
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

CLOCK = "2026-10-04T09:00:00+05:30"
TIMEZONE = "Asia/Kolkata"
WIDTH, HEIGHT = 900, 640
JQUERY_CDN = "https://code.jquery.com/jquery-3.7.1.min.js"
JQUERY_NPM = pathlib.Path(__file__).resolve().parent / "node_modules/jquery/dist/jquery.min.js"


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class Page:
    """The open page, and what happened on it."""

    def __init__(self, page):
        self.page = page
        self.problems = []
        self.allowed = []                         # requests a driver means to fail

    def allow_failure(self, url_prefix):
        """A request to this address is meant to fail (a driver blocks it): do not count it."""
        self.allowed.append(url_prefix)

    def __getattr__(self, name):                  # page.click(...), page.fill(...), ...
        return getattr(self.page, name)

    def screenshot(self, what, full_page=False):
        self.page.wait_for_timeout(350)           # let a transition finish
        pathlib.Path("screens").mkdir(exist_ok=True)
        n = len(list(pathlib.Path("screens").glob("*.png"))) + 1    # numbered across pages
        self.page.screenshot(path=f"screens/{n}.png", full_page=full_page)
        print(f"  [screenshot {n}: {what}]")

    def text(self, selector):
        return self.page.inner_text(selector).strip()


@contextlib.contextmanager
def open_page(html, width=WIDTH, height=HEIGHT, clock=CLOCK):
    """Serve this folder, open `html` in Chromium, and yield it as a Page."""
    handler = functools.partial(_Quiet, directory=".")
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as server:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        url = f"http://127.0.0.1:{server.server_address[1]}/{html}"
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            context = browser.new_context(viewport={"width": width, "height": height},
                                          timezone_id=TIMEZONE, locale="en-IN")
            page = context.new_page()
            p = Page(page)
            if clock:                              # None for a page that shows no time
                page.clock.set_fixed_time(clock)
            if JQUERY_NPM.exists():
                page.route(JQUERY_CDN, lambda route: route.fulfill(
                    path=str(JQUERY_NPM), content_type="application/javascript",
                    headers={"Access-Control-Allow-Origin": "*"}))
            page.on("console", lambda m: print(f"  console.{m.type}: {m.text}"))
            page.on("pageerror", lambda e: p.problems.append(f"uncaught error: {e}"))
            page.on("requestfailed", lambda r: any(r.url.startswith(a) for a in p.allowed)
                    or p.problems.append(f"could not load {r.url}"))
            page.on("response", lambda r: r.status >= 400 and p.problems.append(
                f"{r.status} for {r.url}"))
            page.goto(url)
            page.wait_for_load_state("networkidle")
            print(f"opened {html} in Chromium, {width} px wide: \"{page.title()}\"")
            try:
                yield p
            finally:
                browser.close()
                server.shutdown()
    if p.problems:
        sys.exit("the page had problems:\n  " + "\n  ".join(p.problems))


def describe(html):
    """Open a page, list what it shows, and screenshot all of it."""
    with open_page(html) as p:
        heads = p.page.eval_on_selector_all(
            "h1, h2, h3, h4, h5, h6", "hs => hs.map(h => h.tagName + '  ' + h.innerText.trim())")
        for h in heads:
            print(f"  {h}")
        counts = p.page.evaluate("""() => Object.fromEntries(
            ['p', 'li', 'img', 'table', 'form', 'input', 'select', 'button']
              .map(t => [t, document.getElementsByTagName(t).length]).filter(([, n]) => n))""")
        print("  elements: " + ", ".join(f"{n} {t}" for t, n in counts.items()))
        broken = p.page.evaluate("Array.from(document.images).filter(i => !i.naturalWidth).length")
        if broken:
            p.problems.append(f"{broken} image(s) did not load")
        p.screenshot("the whole page", full_page=True)


if __name__ == "__main__":
    describe(sys.argv[1])
