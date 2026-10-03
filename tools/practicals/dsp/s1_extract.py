# Stage 1a -- EXTRACT: the same six records from five formats, with the
# standard library only.  Each parser returns the same list of dictionaries,
# so the rest of the pipeline never learns where the data came from.
import csv
import io
import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

FIELDS = ["id", "name", "city", "income", "visits"]

# Step 1: Delimited text, split on the delimiter
RAW_TXT = """\
1|Asha Rao|Vizag|40|7
2|Biju Menon|Kochi|57|5
3|Chitra Das|Kolkata|37|8
4|Devan Iyer|Madurai|69|10
5|Esha Khan|Bhopal|36|6
6|Farid Ali|Patna|38|5
"""

def from_txt(text):
    rows = []
    for line in text.strip().splitlines():
        rows.append(dict(zip(FIELDS, line.split("|"))))
    return rows

# Step 2: CSV, naively and with csv.DictReader
# note the quoted field containing a comma -- this is why split(",") is wrong
RAW_CSV = '''\
id,name,city,income,visits
1,"Rao, Asha",Vizag,40,7
2,"Menon, Biju",Kochi,57,5
'''

def from_csv_naive(text):
    rows = []
    lines = text.strip().splitlines()
    header = lines[0].split(",")
    for line in lines[1:]:
        rows.append(dict(zip(header, line.split(","))))
    return rows

def from_csv(text):
    return [dict(r) for r in csv.DictReader(io.StringIO(text))]

# Step 3: JSON, flattening the nested address
RAW_JSON = """
{"customers": [
  {"id": 3, "name": "Chitra Das", "address": {"city": "Kolkata"},
   "income": 37, "visits": 8},
  {"id": 4, "name": "Devan Iyer", "address": {"city": "Madurai"},
   "income": 69, "visits": 10}
]}
"""

def from_json(text):
    doc = json.loads(text)
    return [{"id": c["id"], "name": c["name"], "city": c["address"]["city"],
             "income": c["income"], "visits": c["visits"]}
            for c in doc["customers"]]

# Step 4: XML: an attribute and child elements
RAW_XML = """
<customers>
  <customer id="5"><name>Esha Khan</name><city>Bhopal</city>
    <income>36</income><visits>6</visits></customer>
  <customer id="6"><name>Farid Ali</name><city>Patna</city>
    <income>38</income><visits>5</visits></customer>
</customers>
"""

def from_xml(text):
    root = ET.fromstring(text)
    rows = []
    for c in root.findall("customer"):
        rows.append({"id": c.get("id"),                       # attribute
                     "name": c.findtext("name"),              # child text
                     "city": c.findtext("city"),
                     "income": c.findtext("income"),
                     "visits": c.findtext("visits")})
    return rows

# Step 5: HTML, with html.parser
RAW_HTML = """
<table id="customers">
  <tr><th>id</th><th>name</th><th>city</th><th>income</th><th>visits</th></tr>
  <tr><td>1</td><td>Asha Rao</td><td>Vizag</td><td>40</td><td>7</td></tr>
  <tr><td>2</td><td>Biju Menon</td><td>Kochi</td><td>57</td><td>5</td></tr>
</table>
"""

class TableParser(HTMLParser):
    """Collect the cells of every row of the first table."""
    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell, self.grab = [], [], [], False

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.grab, self.cell = True, []

    def handle_data(self, data):
        if self.grab:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("td", "th"):
            self.row.append("".join(self.cell).strip())
            self.grab = False
        elif tag == "tr":
            self.rows.append(self.row)

def from_html(text):
    p = TableParser()
    p.feed(text)
    header, *body = p.rows
    return [dict(zip(header, r)) for r in body]

# Step 6: Parse all five, and print the count and first record of each
for name, rows in (("delimited text", from_txt(RAW_TXT)),
                   ("csv.DictReader", from_csv(RAW_CSV)),
                   ("json", from_json(RAW_JSON)),
                   ("xml.etree", from_xml(RAW_XML)),
                   ("html.parser", from_html(RAW_HTML))):
    print(f"{name:16s} {len(rows)} record(s); first = {rows[0]}")

# Step 7: Why csv.DictReader and not split(',')
print()
print("why csv.DictReader and not split(','):")
print("  naive :", from_csv_naive(RAW_CSV)[0])
print("  proper:", from_csv(RAW_CSV)[0])
