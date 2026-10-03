# Stage 1a, again -- the same HTML table read with BeautifulSoup, which the
# syllabus names.  It is not in the standard library: pip install beautifulsoup4.
from bs4 import BeautifulSoup

# Step 1: Find the table, its header and its rows

def from_html_bs4(text):
    soup = BeautifulSoup(text, "html.parser")        # or "lxml", if installed
    table = soup.find("table", id="customers")
    header = [th.get_text(strip=True) for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr")[1:]:              # skip the header row
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cells:
            rows.append(dict(zip(header, cells)))
    return rows

# the three selectors worth knowing, and what each returns
# soup.find("a")                     -> the first <a>, or None
# soup.find_all("a", class_="nav")   -> a list, possibly empty
# soup.select("table#customers td")  -> a list, by CSS selector
#
# note class_ with the underscore: "class" is a Python keyword.
#
# BeautifulSoup builds a tree from broken markup, but HOW it repairs it is
# decided by the parser it is given: "lxml" closes an unclosed cell, while
# "html.parser" nests the next one inside it (Step 3).  It does NOT run
# JavaScript, so a page whose table is built in the browser yields nothing --
# fetch the API the page calls instead of scraping what it renders.

# Step 2: Read the same table as Stage 1a, and use the selectors
RAW_HTML = """
<table id="customers">
  <tr><th>id</th><th>name</th><th>city</th><th>income</th><th>visits</th></tr>
  <tr><td>1</td><td>Asha Rao</td><td>Vizag</td><td>40</td><td>7</td></tr>
  <tr><td>2</td><td>Biju Menon</td><td>Kochi</td><td>57</td><td>5</td></tr>
</table>
"""
rows = from_html_bs4(RAW_HTML)
print(f"BeautifulSoup    {len(rows)} record(s); first = {rows[0]}")
soup = BeautifulSoup(RAW_HTML, "html.parser")
print("find('a')                        ->", soup.find("a"))
print("select('table#customers td')[:5] ->", [td.get_text() for td in soup.select("table#customers td")][:5])

# Step 3: Broken markup: the repair belongs to the parser
BROKEN = '<table id="customers"><tr><th>id<th>name<tr><td>1<td>Asha Rao<tr><td>2<td>Biju</table>'
for parser in ("html.parser", "lxml"):
    soup = BeautifulSoup(BROKEN, parser)
    cells = [[c.get_text(strip=True) for c in tr.find_all(["th", "td"])] for tr in soup.find_all("tr")]
    print(f"unclosed cells, {parser:11s} ->", cells)
