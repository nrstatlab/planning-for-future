# -*- coding: utf-8 -*-
r"""Data Science using Python (STS-208): the seven prescribed practicals as one ETL pipeline.

Built by build_py_practical.py dsp_data, run with a Python that has NumPy, pandas,
BeautifulSoup and lxml. The programmes are the files in dsp/; each step is marked in the file
by a "# Step i:" comment. The PyMySQL and PyMongo listings need servers and are shown, not run.
"""
PAGE = "statistics/data-science-using-python/practical.html"
SRC = "dsp"
LIBS = [("numpy", "NumPy"), ("pandas", "pandas"), ("bs4", "BeautifulSoup")]
TITLE = "Practical — Data Science using Python (STS-208)"
DESC = ("All seven prescribed practicals of STS-208 as one Extract–Transform–Load pipeline, each stage set "
        "out as Question, Aim, Steps, Programme, and Execution and Results, with the output each one prints.")

PRACTICALS = [
    dict(
        n=1, title="Extract", hid="1-extract-five-formats-one-structure",
        heading="Practical 1: Extract &mdash; Five Formats, One Structure", file="s1_extract.py",
        extra=[dict(file="s1_extract_bs4.py", label="THE SAME HTML TABLE, WITH BeautifulSoup", run=True,
                    intro="The syllabus names BeautifulSoup, and it is what a real scraper uses. The same table, read with it:")],
        question=r"""  <p>Six customer records arrive spread over five sources: a pipe-delimited text file (all six),
  and a CSV file, a JSON document, an XML file and an HTML table (two each). Parse every source into a
  list of dictionaries with the keys <code>id</code>, <code>name</code>, <code>city</code>,
  <code>income</code> and <code>visits</code>, and show why a CSV file must not be split on commas.</p>""",
        aim="Parse the customer records out of five formats and return the same structure from each: a list of dictionaries with the same five keys.",
        steps=[
            r"""<code>str.split("|")</code> on each line, zipped with the field names.""",
            r"""Split on commas, to show what goes wrong; then <code>csv.DictReader</code>, which honours the quotes.""",
            r"""<code>json.loads</code>, then lift <code>address.city</code> up to <code>city</code>: the structure is a tree, and flattening it is the parser's job.""",
            r"""The <code>id</code> is an attribute, read with <code>get</code>; the other fields are child elements, read with <code>findtext</code>.""",
            r"""A subclass of <code>HTMLParser</code> collects the text of each cell, row by row; the first row is the header.""",
            r"""Print how many records each parser returned, and the first of them.""",
            r"""Parse the CSV both ways and print the first record of each.""",
        ],
        method=r"""    <table>
      <tr><th>Format</th><th>Module</th><th>What it costs you if you improvise</th></tr>
      <tr><td>Delimited text</td><td><code>str.split</code></td>
          <td>nothing, <em>if</em> the delimiter cannot occur inside a field</td></tr>
      <tr><td>CSV</td><td><code>csv.DictReader</code></td>
          <td>quoting, embedded commas, embedded newlines &mdash; all of which
          <code>split(",")</code> gets wrong</td></tr>
      <tr><td>JSON</td><td><code>json.loads</code></td>
          <td>nesting; the structure is a tree, not a table, and flattening it is your job</td></tr>
      <tr><td>XML</td><td><code>xml.etree.ElementTree</code></td>
          <td>attributes and child elements are different things and are read differently</td></tr>
      <tr><td>HTML</td><td><code>html.parser</code>, or BeautifulSoup</td>
          <td>real pages are not well-formed XML, so an XML parser rejects them</td></tr>
    </table>
    <p><strong>The point of returning one structure</strong> is that the validation, transform and
    load stages are written once. A pipeline whose second stage has to ask where the data came from
    has not finished its first.</p>""",
        commands=[
            ("<code>csv.DictReader(io.StringIO(text))</code>", "read CSV text as dictionaries keyed by the header, honouring quotes"),
            ("<code>json.loads(text)</code>", "JSON text to nested dictionaries and lists"),
            ("<code>ET.fromstring</code>, <code>findall</code>, <code>get</code>, <code>findtext</code>", "parse XML; find the elements; read an attribute; read a child's text"),
            ("<code>class TableParser(HTMLParser)</code>", "an HTML parser whose <code>handle_starttag</code>, <code>handle_data</code> and <code>handle_endtag</code> collect the cells"),
            ("<code>dict(zip(header, cells))</code>", "pair each field name with its value"),
            ('<code>BeautifulSoup(text, "html.parser")</code>, <code>find</code>, <code>find_all</code>, <code>select</code>', "the same table through BeautifulSoup; the parser named decides how broken markup is repaired"),
        ],
        reading=r"""  <p><strong>Read the last two lines of the first output.</strong> On the record
  <code>1,"Rao, Asha",Vizag,40,7</code> the naive split produces a name of <code>"Rao</code> and
  a city of <code>Asha"</code>, and shifts every later field by one. It raises no error, the row
  count is right, and the damage is only visible if someone looks. <strong>Use the
  <code>csv</code> module even when the file &ldquo;looks simple&rdquo;</strong>, because you
  cannot tell from the first ten rows whether row nine thousand contains a comma.</p>
  <p><strong>And the last two lines of the second.</strong> Given cells whose closing tags are
  missing, BeautifulSoup with <code>"lxml"</code> closes each one and returns the rows intact; with
  <code>"html.parser"</code> it nests each cell inside the one before, and every cell's text runs on
  to the end of the row. The repair belongs to the parser, so name the parser.</p>""",
        notes=[
            r"""<strong>Corrected.</strong> The aim read &ldquo;return an identical list of dictionaries
    from each&rdquo;. What the five parsers return is the same <em>structure</em> &mdash; a list of
    dictionaries with the same five keys &mdash; holding different records (six from the text file, two
    from each of the others), and not yet the same types: JSON gives the numbers as integers, the rest as
    strings. Converting the types is the next stage's work.""",
            r"""<strong>Corrected.</strong> The BeautifulSoup listing was shown as not executed, because
    BeautifulSoup was not installed where this page was first built. It is now installed and the listing
    runs; it has been completed to parse the same table and print what it finds. Its comment said that
    BeautifulSoup repairs broken markup that <code>html.parser</code> will not; Step 3 shows that the
    repair depends on the parser BeautifulSoup is given, and the comment now says so.""",
        ],
        conclusion=r"""    <p>All five parsers return a list of dictionaries with the same five keys &mdash; 6 records from the
    text file and 2 from each of the others &mdash; so the later stages need not know the source, and
    BeautifulSoup returns the same two records from the HTML table as <code>html.parser</code>. Splitting
    the CSV on commas misreads the quoted name <code>"Rao, Asha"</code> as two fields and shifts every
    later column.</p>""",
    ),
    dict(
        n=1, title="Validate", hid="2-validate-the-anomaly-pass",
        heading="Practical 1, continued: Validate &mdash; the Anomaly Pass", file="s2_validate.py",
        question=r"""  <p>&ldquo;Check any anomalies, missing values etc.&rdquo; A batch of seven customer records contains
  a blank city, an income of <code>"n/a"</code>, a record with no <code>visits</code> field, a
  duplicate id and a negative visit count. Accept the clean records, convert their numeric fields, and
  report every rejection with its reason.</p>""",
        aim="Take a batch with five different faults in it, accept the clean records, and report every rejection with its reason.",
        steps=[
            "Seven records as they arrived, every value a string.",
            "The fields that must be present, the ones that must be integers, and the range each number must lie in.",
            r"For each record: list any missing or blank fields; convert the numbers, catching <code>ValueError</code>; range-check what converted; check the id against those already seen. A record with any issue is rejected, with all its issues listed.",
            "Print the counts, and each rejection by row and id.",
            "Print the records that passed, their numbers now integers.",
            "Print the order of the checks, and the reason for it.",
        ],
        method=r"""    <p><strong>Four kinds of fault, and they are not interchangeable.</strong></p>
    <ul>
      <li><strong>Absent</strong> &mdash; the field is not there at all. A <code>KeyError</code>
      waiting to happen.</li>
      <li><strong>Blank</strong> &mdash; the field is there and empty. Different from absent, and
      the two need different treatment: an absent field may mean the source changed shape, a blank
      one usually means the value was not collected.</li>
      <li><strong>Mistyped</strong> &mdash; <code>"n/a"</code> where an integer belongs. Converting
      without catching is how a pipeline dies at three in the morning.</li>
      <li><strong>Impossible</strong> &mdash; a negative visit count. Correctly typed, correctly
      present, and wrong.</li>
    </ul>
    <p>Plus <strong>duplicates</strong>, which are a property of the batch rather than of any one
    record and so must be checked while walking it.</p>""",
        commands=[
            ("<code>f not in r</code>", "an absent field"),
            ('<code>str(r[f]).strip() == ""</code>', "a blank one"),
            ("<code>try: ... except ValueError:</code>", "convert, and record a failure instead of stopping"),
            ("<code>seen = set()</code>", "the ids met so far, for the duplicate check"),
            ("<code>enumerate(rows, 1)</code>", "each record with its row number, counted from 1"),
        ],
        reading=r"""  <p><strong>Two of the seven records survive</strong>, and the report says exactly why the other
  five did not. That report <em>is</em> the deliverable: a load that accepted two of seven rows
  without saying so would look like a success.</p>
  <p><strong>The three checks run in a fixed order</strong> &mdash; presence, then type, then
  range &mdash; because each one depends on the last. Range-checking a string raises; converting
  an absent field raises. Running them in the wrong order turns a report into a crash.</p>""",
        conclusion=r"""    <p>2 of the 7 records are accepted (ids 1 and 2) and 5 are rejected, each with its reason: a blank
    city, a non-integer income, a missing <code>visits</code> field, a second id 2, and visits of
    \(-3\). The report, not the accepted rows alone, is what this stage produces.</p>""",
    ),
    dict(
        n=2, title="Binary Files", hid="3-binary-files", file="s3_binary.py",
        question=r"""  <p>Write three customer records &mdash; an id, a ten-byte name, an income and a visit rate &mdash; to
  a binary file of fixed-width records and read them back; show what reading with the wrong byte order
  does; store a list of incomes as an <code>array</code>; and round-trip a Python object with
  <code>pickle</code>.</p>""",
        aim=r"Write and read fixed-width records with <code>struct</code>, homogeneous numbers with <code>array</code>, and arbitrary objects with <code>pickle</code> &mdash; and know which to use.",
        steps=[
            "Three tuples, each name padded to exactly ten bytes.",
            r"Pack each record with the format <code>'&lt;i10sif'</code> into an in-memory file, then unpack them again at offsets of one record size; compare that size with the native, padded format.",
            "Pack the integer 1 little-endian and unpack the same four bytes big-endian.",
            r"Six incomes as an <code>array('i')</code>, written to bytes and read back.",
            r"A dictionary holding the records, pickled with the protocol pinned, and loaded again.",
        ],
        method=r"""    <table>
      <tr><th>Tool</th><th>Holds</th><th>Readable by</th><th>Use when</th></tr>
      <tr><td><code>struct</code></td><td>a declared layout of C types</td>
          <td>any language, given the layout</td>
          <td>the format is fixed and shared &mdash; instrument output, network frames</td></tr>
      <tr><td><code>array</code></td><td>one numeric type, many values</td>
          <td>any language, given the type and byte order</td>
          <td>a long homogeneous vector; far smaller than a list</td></tr>
      <tr><td><code>pickle</code></td><td>almost any Python object</td>
          <td>Python only</td>
          <td>a cache you wrote and will read yourself &mdash; never across a trust
          boundary</td></tr>
    </table>
    <p><strong>The format string is the whole of <code>struct</code>.</strong> The first character
    sets byte order and alignment: <code>'&lt;'</code> little-endian with no padding,
    <code>'&gt;'</code> big-endian, <code>'@'</code> native with native alignment. The rest names
    the fields &mdash; <code>i</code> a 4-byte signed integer, <code>10s</code> ten raw bytes,
    <code>f</code> a 4-byte float.</p>""",
        commands=[
            ("<code>struct.pack(FMT, *rec)</code>, <code>struct.unpack_from(FMT, raw, off)</code>", "a record to bytes, and bytes at an offset back to a record"),
            ("<code>struct.calcsize(FMT)</code>", "the size of one record in bytes"),
            ("<code>io.BytesIO()</code>", "an in-memory binary file"),
            ("<code>array.array('i', ...)</code>, <code>tobytes</code>, <code>frombytes</code>", "homogeneous integers, to bytes and back"),
            ("<code>pickle.dumps(obj, protocol=4)</code>, <code>pickle.loads</code>", "any object to bytes and back"),
        ],
        reading=r"""  <p><strong>Three things in that output are worth more than the code.</strong></p>
  <ul>
    <li><strong>22 bytes against 24.</strong> The same six fields, packed
    <code>'&lt;i10sif'</code> and <code>'@i10sif'</code>, differ by two bytes of padding the
    native form inserts to align the float. A reader using the wrong one is off by two bytes from
    the second record onward.</li>
    <li><strong>1 read back as 16777216.</strong> Byte order is not a detail. A file written
    little-endian and read big-endian is not corrupt &mdash; it is wrong, with plausible-looking
    numbers, which is far worse.</li>
    <li><strong><code>pickle</code> executes code while loading.</strong> Unpickling a file you
    did not write is running a program you did not read. For anything that crosses a machine
    boundary, use JSON, CSV, or a declared layout like the one above.</li>
  </ul>""",
        conclusion=r"""    <p>The three records are written as 66 bytes, 22 per record, and read back unchanged; the native
    format would have taken 24 bytes a record. The integer 1 read with the wrong byte order becomes
    16,777,216. The <code>array</code> stores six incomes in 24 bytes and the pickle round trip is
    identical &mdash; but only <code>struct</code>, with its byte order fixed, gives a file another
    machine can be trusted to read.</p>""",
    ),
    dict(
        n=3, title="Regular Expressions", hid="4-regular-expressions", file="s4_regex.py",
        question=r"""  <p>From a four-line order log, find the first error, list every order number, and extract the date,
  level, order, customer e-mail and total of every line; then split, substitute and mask with
  patterns, and show the two mistakes that make a pattern wrong without making it fail.</p>""",
        aim="Pull structured fields out of a log file, and meet the two mistakes that make a pattern wrong without making it fail.",
        steps=[
            "The log, as one string.",
            r"<code>re.search</code> returns the first match and where it starts.",
            "<code>re.findall</code> with one group returns the group's text for every match.",
            r"One compiled, commented pattern with named groups; <code>finditer</code> and <code>groupdict</code> turn each line into a record.",
            "Split on a run of whitespace, and on a separator kept in the result.",
            "Mask an e-mail domain with a backreference, recompute every total with a function, and limit the number of replacements.",
            r"<code>(.+)</code> against <code>(.+?)</code> on two table cells.",
            r"<code>\d+\.\d+</code> against <code>\d+\.\d{2}\b</code> on money and a version number.",
            r"Why <code>re.compile</code> is called once, outside the loop.",
        ],
        method=r"""    <table>
      <tr><th>Call</th><th>Returns</th><th>Watch for</th></tr>
      <tr><td><code>re.search</code></td><td>the first match object, or <code>None</code></td>
          <td>test for <code>None</code> before calling <code>.group()</code></td></tr>
      <tr><td><code>re.findall</code></td><td>a list</td>
          <td>with one group it returns the <em>group</em>, with several a list of tuples, and with
          none the whole match &mdash; three different shapes</td></tr>
      <tr><td><code>re.finditer</code></td><td>match objects</td>
          <td>the one to use when you want groups and positions</td></tr>
      <tr><td><code>re.split</code></td><td>a list</td>
          <td>a capturing group puts the separators in the result too</td></tr>
      <tr><td><code>re.sub</code></td><td>a string</td>
          <td>the replacement may be a backreference (<code>\1</code>) or a function</td></tr>
      <tr><td><code>re.compile</code></td><td>a pattern object</td>
          <td>compile once outside the loop, not once per row</td></tr>
    </table>""",
        commands=[
            ("<code>(?P&lt;name&gt;...)</code>, <code>m.groupdict()</code>", "a named group, and all the named groups of a match as a dictionary"),
            ("<code>re.VERBOSE</code>", "allow white space and comments inside the pattern"),
            (r"<code>r'\1@***.\3'</code>", "a replacement that reuses groups 1 and 3"),
            ("<code>lambda m: ...</code> in <code>re.sub</code>", "compute each replacement from its match"),
            ("<code>.+?</code>", "the lazy form: as few characters as will do"),
        ],
        reading=r"""  <p><strong>The greedy match is the classic.</strong> <code>&lt;td&gt;(.+)&lt;/td&gt;</code>
  runs to the <em>last</em> <code>&lt;/td&gt;</code> on the line and returns one wrong string;
  <code>(.+?)</code> stops at the first and returns two right ones. Neither raises.</p>
  <p><strong>And the plausible pattern that is wrong.</strong> <code>\d+\.\d+</code> reads
  <code>3.14159</code> as money. Anchoring to two decimal places and a word boundary fixes it.
  <strong>Test a pattern against what it should <em>not</em> match</strong>, not only against what
  it should.</p>
  <p>Regular expressions applied to whole Pandas columns &mdash; <code>str.extract</code>,
  <code>str.replace</code>, <code>str.contains</code> &mdash; are in
  <a href="../../data-science/python-data-analysis/unit4.html">Python for Data Analysis,
  Unit 4.2</a> and are not repeated.</p>""",
        conclusion=r"""    <p>The first error is at character 176; the four order numbers are A-1043, A-1044, B-2210 and
    B-2211, and all four lines parse into records. The greedy pattern returns one wrong cell where the lazy
    one returns <code>Vizag</code> and <code>Kochi</code>, and the unanchored money pattern takes
    <code>3.14159</code> for an amount where the anchored one does not.</p>""",
    ),
    dict(
        n=4, title="Load", hid="5-load-the-relational-store",
        heading="Practical 4: Load &mdash; the Relational Store", file="s5_sql.py",
        extra=[dict(file="s5_pymysql.py", label="THE SAME SQL, THROUGH PyMySQL (NOT RUN HERE)",
                    intro=r"""The syllabus names PyMySQL, and a MySQL server is what a real pipeline writes to.
  There is no server here, so the listing is shown rather than run &mdash; but every statement in it is
  the one <code>sqlite3</code> executed above.""")],
        question=r"""  <p>Design a normalised schema for cities, customers and their orders; create it, populate it with
  four customers and six orders, and show that its constraints reject three illegal rows; then read
  the orders per customer with a join, update and delete with a <code>WHERE</code>, and show a
  transaction rolled back.</p>""",
        aim="Design a small schema, create it, populate it, and run create, read, update and delete against it &mdash; with the constraints actually enforcing something.",
        steps=[
            r"An in-memory <code>sqlite3</code> database, with foreign keys switched on, which sqlite needs asked for.",
            r"Three tables with primary keys, foreign keys, <code>NOT NULL</code>, <code>UNIQUE</code> and <code>CHECK</code> constraints, and an index on the orders' customer.",
            r"<code>executemany</code> with <code>?</code> placeholders, then <code>commit</code>.",
            r"Three inserts that break a constraint, each caught as an <code>IntegrityError</code>.",
            r"A three-table join with <code>COUNT</code>, <code>SUM</code>, <code>GROUP BY</code> and <code>HAVING</code>.",
            r"An <code>UPDATE</code> and a <code>DELETE</code>, each with a <code>WHERE</code>, and the rows each touched.",
            r"A <code>BEGIN</code>, an update of every row, a failure, and a <code>rollback</code>.",
        ],
        method=r"""    <p><strong>The design, in one line each.</strong> City is separated from customer because the
    city name depends only on the city, not on the customer &mdash; that is third normal form, and
    the practical consequence is that a city renamed once is renamed everywhere. Orders are a
    separate table because a customer has many of them, and repeating the customer's name on every
    order is the anomaly normalisation exists to prevent. The full treatment is in
    <a href="../../data-science/dbms/unit3.html">Database Management Systems, Unit 3</a>.</p>
    <p><strong>The constraints are the design.</strong> A foreign key that is not declared is a
    comment; declared, it is the database refusing to hold a customer in a city that does not
    exist. The listing tries three illegal inserts on purpose and shows all three being rejected.</p>""",
        commands=[
            ("<code>sqlite3.connect(\":memory:\")</code>", "a database that lives only while the program runs"),
            ("<code>cur.executescript(...)</code>", "run several SQL statements at once"),
            ("<code>cur.executemany(sql, rows)</code>", "one parameterised statement for many rows"),
            ("<code>except sqlite3.IntegrityError</code>", "a constraint refused the row"),
            ("<code>cur.rowcount</code>", "the rows the last statement touched"),
            ("<code>con.commit()</code>, <code>con.rollback()</code>", "keep the transaction, or abandon it"),
        ],
        reading=r"""  <p><strong>Read the join.</strong> <code>LEFT JOIN</code> keeps customers with no orders;
  <code>HAVING COUNT(...) &gt; 0</code> then removes them again &mdash; written that way
  deliberately, because <code>HAVING</code> filters <em>after</em> grouping and
  <code>WHERE</code> before, and confusing the two is the commonest SQL error at this level.</p>
  <p><strong>And read the rollback.</strong> The update sets every income to zero and is then
  abandoned; the incomes afterwards are <code>[45, 57, 37, 69]</code>, unchanged. <strong>A load
  that is not in a transaction is a load that can half-succeed</strong>, and a half-loaded table
  is harder to recover from than an empty one.</p>""",
        conclusion=r"""    <p>Three tables are created and loaded with 4 customers and 6 orders, and all three illegal inserts
    are rejected. The join gives each customer's orders and total, largest first (Chitra Das, 15,750.75).
    The update touched 1 row and the delete removed 2 orders, leaving 4; the rolled-back update left
    every income as it was.</p>""",
    ),
    dict(
        n=5, title="Load", hid="6-load-the-document-store",
        heading="Practical 5: Load &mdash; the Document Store", file="s6_documents.py",
        extra=[dict(file="s6_pymongo.py", label="THE SAME OPERATIONS, THROUGH PyMongo (NOT RUN HERE)",
                    intro=r"""The syllabus names PyMongo, which needs a running <code>mongod</code>; these pages are
  not built against one, so this listing is shown, not run. The programme above does in plain Python what
  each of its collection methods does, so that their meaning can be checked without a server.""")],
        question=r"""  <p>Hold the same customers as documents, each with its address, tags and orders inside it; query
  them with a filter and a projection; update, replace and delete documents; total the order value per
  customer with an aggregation pipeline; and count what an index saves.</p>""",
        aim="Load the same data as documents, run the four kinds of operation and an aggregation on them, and see where the document model differs from the relational one.",
        steps=[
            "Four customer documents, with a nested address, an array of tags and an array of orders.",
            r"<code>find</code> with a query (a dotted path, an operator, an array field) and a projection.",
            r"<code>$set</code> one field and <code>$inc</code> another, in one document.",
            r"<code>replace_one</code>, which keeps the <code>_id</code> and nothing else.",
            r"<code>delete_many</code> with an operator.",
            r"<code>$unwind</code> the orders, <code>$group</code> by name with <code>$sum</code>, and <code>$sort</code>.",
            "Count the documents a scan examines against an index lookup.",
        ],
        method=r"""    <table>
      <tr><th></th><th>Relational</th><th>Document</th></tr>
      <tr><td>Shape</td><td>rows of a fixed schema</td>
          <td>documents that need not agree</td></tr>
      <tr><td>A customer's orders</td><td>a second table and a join</td>
          <td>an array inside the customer</td></tr>
      <tr><td>Adding a field</td><td><code>ALTER TABLE</code>, all rows</td>
          <td><code>$set</code> on one document</td></tr>
      <tr><td>Consistency across documents</td><td>the database's job</td>
          <td><strong>yours</strong></td></tr>
      <tr><td>Use when</td><td>the shape is known and relationships matter</td>
          <td>the shape varies, and what you read together you store together</td></tr>
    </table>
    <p><strong>The last row is the decision.</strong> The document model is not &ldquo;SQL without
    the schema&rdquo;; it is a bet that you will read a customer with their orders far more often
    than you will ask a question that crosses customers. When that bet is wrong, the joins you
    avoided reappear in application code, where nothing optimises them.</p>""",
        commands=[
            ("<code>dig(doc, \"address.city\")</code>", "follow a dotted path into a nested document"),
            ("<code>OPS = {\"$gt\": ..., ...}</code>", "the query operators, as a dictionary of functions"),
            ("<code>copy.deepcopy(doc)</code>", "a copy that shares nothing with the original"),
            ("<code>(op, spec), = stage.items()</code>", "unpack a one-key dictionary"),
            ("<code>index = {d[\"_id\"]: d for d in DOCS}</code>", "an index: a dictionary from key to document"),
        ],
        reading=r"""  <p><strong>Three results in that output are the ones to carry away.</strong></p>
  <ul>
    <li><strong><code>$set</code> touched one document</strong> and gave it a field no other
    document has. No schema object changed. That is the whole difference from SQL, and the whole
    cost of it: nothing now guarantees that any two documents agree.</li>
    <li><strong><code>replace_one</code> is not <code>update_one</code>.</strong> It kept the
    <code>_id</code> and discarded the address, the tags and the orders. Collections lose fields
    this way in production.</li>
    <li><strong><code>$unwind</code> drops a document whose array is missing</strong>, which is
    why Devan Iyer vanishes from the aggregation although he is still in the collection. Pass
    <code>preserveNullAndEmptyArrays</code> when that is not what you meant.</li>
  </ul>
  <p>The index demonstration counts what a scan examines against what a lookup examines. A scan
  examines documents until it meets the key, up to every one of them, and the lookup examines one; on
  three documents that is a curiosity, but the scan's count grows with the collection and the
  lookup's does not.</p>""",
        conclusion=r"""    <p>The queries return what their filters say, including a match on any element of an array. After the
    update, the replacement (which lost Devan Iyer's address, tags and orders) and the deletion of Chitra
    Das, 3 documents remain, and the aggregation totals only two customers: Asha Rao 1,795.75 and Biju
    Menon 99.00.</p>""",
    ),
    dict(
        n=6, title="Analyse", hid="7-analyse-numpy",
        heading="Practical 6: Analyse &mdash; NumPy", file="s7_numpy.py",
        question=r"""  <p>Build arrays from a list, a range and a linear spacing; show what a fixed dtype does to an
  assigned value; reshape, transpose and flatten an array; show the difference between writing through
  a slice and through a fancy index; select by condition; and aggregate a two-row array along each
  axis.</p>""",
        aim="Build arrays from several sources, reshape and slice them, index them by position and by condition, and aggregate along an axis.",
        steps=[
            r"<code>np.array</code>, <code>np.arange(...).reshape</code>, <code>np.zeros</code> with a dtype, and <code>np.linspace</code>.",
            "Assign a float into an integer array, and mix two types.",
            r"<code>.T</code>, <code>.ravel()</code>, and <code>.reshape(2, -1)</code>.",
            "Write through a basic slice, then through a fancy index, and look at the original each time.",
            r"A boolean mask, selection by it, <code>np.where</code>, and assignment through the mask.",
            r"Element-wise arithmetic, subtracting the column means by broadcasting, sums along each axis, and the standard deviation with both divisors.",
        ],
        method=r"""    <p>The teaching is in
    <a href="../../data-science/python-data-analysis/unit1.html">Python for Data Analysis,
    Unit 1</a>. What is shown here is the part that goes wrong inside a pipeline: <strong>views
    against copies</strong>, <strong>dtype</strong>, and <strong><code>axis=</code></strong>.</p>""",
        commands=[
            ("<code>a.shape</code>, <code>a.dtype</code>", "the dimensions, and the one type every element shares"),
            ("<code>b[0, :]</code>, <code>b[[0, 2], :]</code>", "a basic slice (a view) and a fancy index (a copy)"),
            ("<code>a[a &gt; 40]</code>, <code>np.where(c, x, y)</code>", "select by condition, and choose element by element"),
            ("<code>m.sum(axis=0)</code>, <code>m.mean(axis=0)</code>", "collapse the rows, leaving one value per column"),
            ("<code>m.std()</code>, <code>m.std(ddof=1)</code>", "the standard deviation with divisor \\(n\\), and with \\(n-1\\)"),
        ],
        reading=r"""  <p><strong>The view and the copy.</strong> A basic slice is a <em>view</em> &mdash; writing to
  it writes to the original. A fancy index is a <em>copy</em> &mdash; writing to it does not. The
  output shows both: after the slice write <code>b[0,0]</code> is 99, and after the fancy-index
  write it is still 99 rather than \(-1\). Nothing warns you either way, and this one distinction
  accounts for most NumPy bugs that survive a code review.</p>
  <p><strong><code>axis=0</code> collapses the rows</strong> and leaves one value per column;
  <code>axis=1</code> collapses the columns. Both return a number, so the wrong one is not an
  error &mdash; it is an answer to a different question.</p>
  <p><strong>And the divisor.</strong> <code>np.std</code> defaults to <code>ddof=0</code> and
  Pandas' <code>.std()</code> to <code>ddof=1</code>. On the same six numbers that is
  \(12.455476\) against \(13.644291\). They are both right; only an unstated convention is
  wrong.</p>""",
        conclusion=r"""    <p>An integer array truncates 3.9 to 3 without a warning; a slice writes through to the original
    and a fancy index does not; the column sums of the two-row array are 109, 93 and 75 and the row sums
    134 and 143; and the six incomes have mean 46.166667, with standard deviation 12.455476 or 13.644291
    according to the divisor.</p>""",
    ),
    dict(
        n=7, title="Analyse", hid="8-analyse-pandas",
        heading="Practical 7: Analyse &mdash; Pandas", file="s8_pandas.py",
        question=r"""  <p>Given five customers (one income missing) and seven orders (one for a customer who does not
  exist): find and handle the missing value; join the tables three ways and count the rows; total the
  orders per customer; total them by month and city with a two-level index; and write the result to CSV
  and read it back.</p>""",
        aim="Complete the pipeline: join the two tables, handle what is missing, aggregate by one key and by two, and write the result back to a file.",
        steps=[
            "Two data frames, customers and orders.",
            r"Count the missing values per column; the mean with and without <code>skipna</code>; fill with the median.",
            r"<code>merge</code> with <code>how=\"inner\"</code>, <code>\"left\"</code> and <code>\"outer\"</code>, counting the rows each keeps.",
            r"<code>groupby(\"name\")</code> with count, sum and mean of the amount.",
            r"<code>groupby([\"month\", \"city\"])</code>, then <code>.loc</code> on the outer level and <code>.unstack()</code>.",
            r"<code>to_csv</code> to an in-memory file, <code>read_csv</code> back, and compare.",
        ],
        method=r"""    <p>Each operation is taught in
    <a href="../../data-science/python-data-analysis/index.html">Python for Data
    Analysis</a> and linked from the table at the top of this page. What follows is the pipeline's
    last stage, with the three places it leaks.</p>""",
        commands=[
            ("<code>df.isna().sum()</code>", "the missing values in each column"),
            ("<code>s.mean(skipna=False)</code>, <code>s.fillna(s.median())</code>", "a mean that will not skip, and a fill that is a decision"),
            ("<code>ORDERS.merge(CUSTOMERS, on=\"cust_id\", how=how)</code>", "a join; <code>how</code> decides which unmatched rows are kept"),
            ("<code>.groupby(...).agg([\"count\", \"sum\", \"mean\"])</code>", "several summaries per group"),
            ("<code>.unstack().fillna(0)</code>", "the inner index level to columns, absent cells set to 0"),
            ("<code>to_csv</code>, <code>read_csv</code>", "write the frame out, and read it back"),
        ],
        reading=r"""  <p><strong>The mean that is not the mean.</strong> One income is missing.
  <code>.mean()</code> skips it and returns \(50.75\) &mdash; the mean of four values reported
  as though it were the mean of five. <code>skipna=False</code> returns <code>nan</code>, which
  is the honest answer to a question that cannot be answered. Filling with the median is a
  decision, and it belongs in the report beside the number.</p>
  <p><strong>The join that loses a row.</strong> Order 107 points at customer 9, who does not
  exist. <code>inner</code> gives 6 rows, <code>left</code> 7, <code>outer</code> 8 &mdash; and
  only the last two make the problem visible. <strong>Count the rows before and after every
  join</strong>, and explain any difference; an unexplained drop is a data fault, not a join
  setting.</p>
  <p><strong>The hierarchical index.</strong> Grouping by month and city gives a two-level index;
  <code>.loc['Feb']</code> selects an outer level and <code>.unstack()</code> turns the inner one
  into columns. The unstacked table has zeros where a city had no orders in a month &mdash; those
  zeros were <em>absent</em> before <code>fillna(0)</code>, and deciding that absent means zero
  is a decision too.</p>
  <p><strong>The write-out.</strong> The frame round-trips through CSV identically. It would not
  if any column held an identifier made of digits: <code>read_csv</code> guesses dtypes from the
  first rows and an account number with leading zeros comes back as an integer, silently
  shortened. Pass <code>dtype={'account': str}</code> whenever the digits are a name rather than
  a quantity.</p>""",
        conclusion=r"""    <p>The mean income is 50.75 over the four known values and undefined over five; the median fill gives
    48.5. The joins keep 6, 7 and 8 rows, the difference being order 107 for a customer who does not
    exist. Chitra Das has the largest total, 15,750.75 from one order, and Asha Rao the most orders, three
    totalling 1,795.75. The summary round-trips through CSV unchanged.</p>""",
    ),
]

HEAD = r"""<div class="wrapper">

  <div class="banner">
    <div class="crumbs"><a href="index.html">Home</a> &raquo; Practical</div>
    <h1>Practical &mdash; Data Science using Python (STS-208)</h1>
    <p>All seven prescribed practicals of STS-208, written as one Extract–Transform–Load pipeline: five formats parsed into one structure, an anomaly pass that reports every rejection, binary files with struct, array and pickle, the re module, a normalised schema with all four CRUD operations in a transaction, the same data as documents with an aggregation pipeline, and NumPy and Pandas to finish. Each practical is set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and Results.</p>
  </div>

  <h2>Topics Covered</h2>
  <div class="chips">
    <span class="chip">ETL Pipeline</span>
    <span class="chip">CSV, JSON, XML, HTML</span>
    <span class="chip">Anomaly Detection</span>
    <span class="chip">Binary Files</span>
    <span class="chip">Regular Expressions</span>
    <span class="chip">SQL &amp; CRUD</span>
    <span class="chip">Transactions</span>
    <span class="chip">MongoDB</span>
    <span class="chip">Aggregation</span>
    <span class="chip">NumPy</span>
    <span class="chip">Pandas</span>
  </div>

<details class="toc">
  <summary>On this page</summary>
  <ol>
{toc}
  </ol>
</details>
  <div class="tip">
    <strong>About this course.</strong> STS-208 is a <strong>practical</strong>, and its
    first stated objective is a pipeline, not a topic: <em>&ldquo;Able to apply to the data set to
    Extract, Transform, Load pipeline which will extract raw data (text files, CSV files, XML
    files, JSON, HTML files, SQL databases, NoSQL databases etc.), clean the data, perform
    transformations on data, load data and visualize the data.&rdquo;</em> So these pages are
    written as one pipeline run end to end, in the order the stages must happen, rather than as
    seven unrelated programs.
  </div>

  <div class="tip">
    <strong>What ran and what did not &mdash; read this before the code.</strong> This page is built by
    running every listing on it that can run here, in Python {version} with {libs}; the block under
    each is the output it printed, unchanged. That covers the standard library,
    <strong>NumPy, Pandas and BeautifulSoup</strong>.
    <p>Two listings cannot run here and say so on their first line, <code>NOT EXECUTED</code>:
    <strong>PyMySQL</strong> and <strong>PyMongo</strong>, which need a MySQL server and a
    <code>mongod</code> that these pages are not built against. The syllabus names both, so both are
    shown &mdash; and each is paired with a listing that <em>did</em> run and produces the same answer:
    <code>sqlite3</code> for PyMySQL (the SQL is standard and identical; only the connect call and the
    placeholder differ), and a plain-Python collection for PyMongo. <strong>Nothing on this page is
    claimed to have run that did not.</strong></p>
  </div>

  <div class="tip">
    <strong>NumPy and Pandas are not taught here.</strong> The two prescribed items that are
    entirely about them &mdash; arrays, and the Pandas data-wrangling list &mdash; are covered unit
    by unit, with worked programs, in
    <a href="../../data-science/python-data-analysis/index.html">Python for Data
    Analysis</a>, and that course is linked at each point instead of being repeated:
    <table>
      <tr><th>Prescribed</th><th>Where it is taught</th></tr>
      <tr><td>NumPy arrays: shapes, sources, reshape, slice, indexes, arithmetic, logic,
          aggregation</td>
          <td><a href="../../data-science/python-data-analysis/unit1.html">Unit 1</a>
          &mdash; the ndarray, creation, dtypes, broadcasting, indexing and slicing, boolean
          indexing</td></tr>
      <tr><td>Series and DataFrame as containers; single-level and hierarchical indexing</td>
          <td><a href="../../data-science/python-data-analysis/unit2.html">Unit 2</a> and
          <a href="../../data-science/python-data-analysis/unit5.html">Unit 5.4</a></td></tr>
      <tr><td>Handling missing data</td>
          <td><a href="../../data-science/python-data-analysis/unit3.html">Unit 3.3</a>,
          with replacement and outlier filtering beside it</td></tr>
      <tr><td>Arithmetic and Boolean operations on whole columns</td>
          <td><a href="../../data-science/python-data-analysis/unit2.html">Unit 2.6</a>
          &mdash; arithmetic and data alignment</td></tr>
      <tr><td>Database-type operations: merging and aggregation</td>
          <td><a href="../../data-science/python-data-analysis/unit5.html">Unit 5.1</a>,
          5.2 and 5.6</td></tr>
      <tr><td>Plotting columns and whole tables</td>
          <td><a href="../../data-science/python-data-analysis/basic-visualizations-with-matplotlib-and-seaborn-plotly.html">Basic
          visualizations with matplotlib, seaborn and plotly</a></td></tr>
      <tr><td>Reading data from files and writing it back</td>
          <td><a href="../../data-science/python-data-analysis/unit3.html">Unit 3.1</a> and
          <a href="../../data-science/python-data-analysis/read-and-write-data-in-csv-txt-json-and-excel-formats.html">CSV,
          TXT, JSON and Excel</a></td></tr>
      <tr><td>Python itself &mdash; files, strings, exceptions, classes</td>
          <td><a href="../../data-science/python-data-structures/index.html">Python
          Programming and Data Structures</a></td></tr>
      <tr><td>Relational design, normalisation and SQL</td>
          <td><a href="../../data-science/dbms/index.html">Database Management Systems</a></td></tr>
      <tr><td>MongoDB: the document model, CRUD, aggregation, indexes</td>
          <td><a href="../../data-science/document-database/index.html">Document
          Databases</a></td></tr>
      <tr><td>NLTK</td>
          <td><a href="../../data-science/nlp/index.html">Natural Language Processing</a></td></tr>
    </table>
    <strong>What is written out below is what that list does not contain</strong>: HTML and XML
    parsing, the anomaly pass, binary files, the <code>re</code> module outside Pandas, and driving
    the two databases from Python &mdash; all held together by the pipeline the course asks for.
  </div>

  <h2 id="the-pipeline-and-why-it-is-an-order">The Pipeline, and Why It Is an Order</h2>

  <div class="concept">
    <span class="label">EXTRACT &rarr; TRANSFORM &rarr; LOAD</span>
    <table>
      <tr><th>Stage</th><th>Job</th><th>The rule</th></tr>
      <tr><td><strong>Extract</strong></td>
          <td>get the bytes out of whatever holds them and into one shape</td>
          <td>every parser returns the <em>same</em> structure, so nothing downstream knows or
          cares what the source was</td></tr>
      <tr><td><strong>Validate</strong></td>
          <td>find what is missing, mistyped, duplicated or impossible</td>
          <td>count and report every rejected record &mdash; a pipeline that silently loses rows
          is worse than one that stops</td></tr>
      <tr><td><strong>Transform</strong></td>
          <td>type, derive, reshape, join</td>
          <td>never before validation: a transformation applied to a bad row propagates the
          fault somewhere harder to find</td></tr>
      <tr><td><strong>Load</strong></td>
          <td>write to the store the consumers read</td>
          <td>in a transaction, so a half-finished load leaves the store as it was</td></tr>
      <tr><td><strong>Analyse</strong></td>
          <td>aggregate, model, plot</td>
          <td>only now &mdash; and the row count at this stage should be explicable from the
          count at the first</td></tr>
    </table>
    <p><strong>The order is the content of the objective.</strong> Any of these stages can be
    written; what makes it a pipeline is that each one may assume the guarantees of the one before
    and must not assume the ones after. The stages below are numbered in that order, and each
    consumes what the last produced.</p>
  </div>

"""

TAIL = r"""  <h2 id="how-marks-are-lost">How Marks Are Lost</h2>

  <div class="tip">
    <span class="label">THE RECURRING ERRORS</span>
    <ul>
      <li><strong>Parsing CSV with <code>split(",")</code>.</strong> It works until a field
      contains a comma, and then it shifts every later column without raising.</li>
      <li><strong>Dropping bad records silently.</strong> Count them, report them, and give the
      reason. Two accepted out of seven is a finding, not a success.</li>
      <li><strong>Transforming before validating.</strong> A derived column computed from a bad row
      carries the fault somewhere harder to find.</li>
      <li><strong>Trusting the native <code>struct</code> format.</strong> Fix the byte order and
      the alignment in the format string, or the file is unreadable on another machine and,
      worse, readable-but-wrong on some.</li>
      <li><strong>Unpickling a file you did not write.</strong> It runs code.</li>
      <li><strong>A greedy <code>.+</code> where <code>.+?</code> belongs</strong>, and a pattern
      never tested against what it should not match.</li>
      <li><strong>String-formatting a SQL query.</strong> <code>"... WHERE id = %s" % value</code>
      is an injection; <code>cur.execute(sql, (value,))</code> is not. The placeholder is not a
      style preference.</li>
      <li><strong>Loading outside a transaction</strong>, so a failure half way leaves a table
      nobody can trust.</li>
      <li><strong>Confusing <code>update_one</code> with <code>replace_one</code></strong>, or
      forgetting that <code>$unwind</code> drops empty arrays.</li>
      <li><strong>Writing through a NumPy slice and expecting a copy</strong>, or reading
      <code>axis=</code> the wrong way round.</li>
      <li><strong>Reporting a Pandas mean over a column with missing values</strong> without saying
      how many were skipped.</li>
      <li><strong>Not counting rows across a join.</strong></li>
    </ul>
  </div>

  <h2 id="what-the-practical-record-should-contain">What the Practical Record Should Contain</h2>

  <div class="concept">
    <span class="label">FOR EACH STAGE OF THE PIPELINE</span>
    <ol>
      <li><strong>Question</strong> &mdash; the task, the stage of Extract&ndash;Transform&ndash;Load it
      belongs to, and the input: its format, its size, and where it came from.</li>
      <li><strong>Aim</strong> &mdash; in one line.</li>
      <li><strong>Steps</strong> &mdash; the method in numbered steps, with the libraries named and the
      version if it matters.</li>
      <li><strong>Programme</strong> &mdash; the program, with each step marked by a comment.</li>
      <li><strong>Execution and Results</strong> &mdash; the output, as it was actually printed;
      <strong>the record counts in and out</strong>, with every difference explained; the faults found,
      counted by kind, and what was done about each; every decision that was a decision &mdash; how
      missing values were filled, which join was used, what was assumed to mean zero; and the
      conclusion, with what the data does not support.</li>
    </ol>
  </div>

  <div class="page-nav">
    <a href="index.html">&larr; Course Home</a>
    <a href="../index.html">All Statistics courses &rarr;</a>
  </div>

  <footer>Data Science using Python &middot; Statistics</footer>
</div>
"""
