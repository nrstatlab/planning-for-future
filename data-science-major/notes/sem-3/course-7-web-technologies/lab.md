# Course 7 — Practical Lab

**16 experiments**

Code lives in `labs/course-7-web/`.

> **These run.** Unlike the Course 6 R scripts, every JavaScript experiment
> here is executed by `tools/run_web_labs.js`
> under Node 22 with jsdom, and its result asserted. The HTML and CSS files are
> structurally checked — balanced tags, every `<label for>` resolving to a real
> id, every `<img>` carrying `alt`. What is **not** automated is visual
> appearance: open the pages in a browser for that.

```bash
cd tools && npm install          # jsdom, once
node tools/run_web_labs.js       # from the repository root
```

## How the files are organised

Each experiment that has logic is split in two:

```
labs/course-7-web/
    10_string_ops.js        ← pure functions, exported — testable
    10_string_ops.html      ← the browser page that uses them
```

That split is what makes the labs verifiable. A function that takes its input
as a parameter and returns a value can be asserted; one that reads
`document.getElementById(…)` and writes to the page cannot be, without a
browser. The `.js` file holds the logic, the `.html` file holds the wiring.

The examiner will ask you to demonstrate in a browser, so know both halves.

---

## Experiment 1 — HTML formatting options

**File:** `01_formatting.html`

Required: bold, italics, underline, headings H1–H6, font type/size/colour,
coloured or image background, paragraph, line break, horizontal rule, `<pre>`.

```html
<body style="background-color:#f4f6f9">
  <h1>Heading level 1</h1>
  <h2>Heading level 2</h2>
  <!-- … through h6 -->

  <p><strong>Bold</strong>, <em>italic</em>, <u>underlined</u>.</p>
  <p>Line one<br>Line two after a break.</p>
  <hr>
  <p style="font-family: Georgia, serif; font-size: 20px; color: #2b4c7e;">
    Georgia, 20px, navy.
  </p>
  <pre>
    Text in a pre tag
        keeps   its    spacing
    and its line breaks.
  </pre>
</body>
```

**The exam point.** The syllabus asks for the `<font>` tag, which is
**obsolete** — removed in HTML5. Show that you know it existed and that CSS
replaced it:

```html
<font face="Georgia" size="5" color="blue">Obsolete since HTML5</font>
<span style="font-family:Georgia; font-size:20px; color:blue">The modern way</span>
```

Likewise `<b>`, `<i>` and `<u>` still render, but `<strong>`, `<em>` and a CSS
underline carry meaning. Saying so is worth a mark.

`<pre>` is the only element that preserves whitespace and newlines. Everything
else collapses runs of spaces to one.

---

## Experiment 2 — Lists and an image

**File:** `02_lists.html`

Ordered, unordered, nested, plus an image.

```html
<ol type="I" start="1">
  <li>Semester I</li>
  <li>Semester II</li>
</ol>

<ul>
  <li>Data Science
    <ul>
      <li>Statistics</li>
      <li>Python
        <ol type="a"><li>NumPy</li><li>Pandas</li></ol>
      </li>
    </ul>
  </li>
</ul>

<dl>
  <dt>DOM</dt><dd>Document Object Model</dd>
  <dt>JSON</dt><dd>JavaScript Object Notation</dd>
</dl>

<img src="images/campus.jpg" alt="The college campus at sunrise"
     width="400" height="250">
```

**The mistake everyone makes:** a nested list goes **inside** an `<li>`, not
between two of them.

```html
<ul>
  <li>Parent
    <ul><li>Child</li></ul>          <!-- correct: inside the li -->
  </li>
</ul>

<ul>
  <li>Parent</li>
  <ul><li>Child</li></ul>            <!-- WRONG: a ul directly inside a ul -->
</ul>
```

Both render similarly in a forgiving browser, but only the first validates,
and only the first is announced correctly by a screen reader.

There are three list types: `<ol>` ordered, `<ul>` unordered, `<dl>`
description. `type` on `<ol>` gives `1`, `A`, `a`, `I`, `i`.

---

## Experiment 3 — Ten images aligned with a table

**File:** `03_image_table.html`

```html
<table>
  <caption>Gallery — arranged in a 2 × 5 grid</caption>
  <tr>
    <td><img src="images/1.jpg" alt="Sunrise over the river"></td>
    <td colspan="2"><img src="images/2.jpg" alt="The library building"></td>
    <!-- … -->
  </tr>
</table>
```
```css
table { border-collapse: collapse; }
td    { padding: 4px; }
td img{ width: 150px; height: 110px; object-fit: cover; display: block; }
```

**State the caveat, because the examiner is listening for it.** This
experiment asks you to use a table for **layout**, which HTML5 forbids: tables
are for tabular data, and a screen reader announces "table, 2 rows, 5 columns"
to someone who cannot see the images. Do it as asked — then add the modern
equivalent, which is three lines and also responsive:

```css
.gallery { display: grid; gap: 8px;
           grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); }
```

`object-fit: cover` makes images of different aspect ratios fill an identical
box by cropping, rather than stretching. `display: block` removes the few
pixels of space under an inline image.

---

## Experiment 4 — A form with every control type

**File:** `04_form_controls.html`

Text box, radio buttons, check boxes, reset and submit.

```html
<form action="/submit" method="post">
  <label for="name">Name</label>
  <input type="text" id="name" name="name">

  <fieldset>
    <legend>Gender</legend>
    <input type="radio" id="f" name="gender" value="F"><label for="f">Female</label>
    <input type="radio" id="m" name="gender" value="M"><label for="m">Male</label>
  </fieldset>

  <fieldset>
    <legend>Subjects</legend>
    <input type="checkbox" id="s1" name="subjects" value="ds"><label for="s1">Data Science</label>
    <input type="checkbox" id="s2" name="subjects" value="st"><label for="s2">Statistics</label>
  </fieldset>

  <button type="submit">Submit</button>
  <button type="reset">Reset</button>
</form>
```

**Radio vs checkbox, and the rule behind it.** Radio buttons in one group
must share the **same `name`** — that is what makes them mutually exclusive,
and different names give you three independent buttons that can all be on at
once. Checkboxes sharing a name submit as multiple values under that key.

Every input needs a `name`, or it is **not submitted at all**. Every input
needs a `<label for>` matching its `id`, or clicking the text does not focus
the field and a screen reader has nothing to announce.

---

## Experiment 5 — Embed a calendar

**File:** `05_calendar.html`, `05_calendar.js`

The syllabus says "embed a calendar object", which in 2004 meant an ActiveX
control. Three modern answers, in increasing order of effort:

```html
<!-- 1. the native date picker — one line -->
<label for="dob">Date of birth</label>
<input type="date" id="dob" name="dob" min="1990-01-01" max="2010-12-31">

<!-- 2. an embedded external calendar -->
<iframe src="https://calendar.google.com/calendar/embed?src=…"
        width="600" height="400" style="border:0" title="Academic calendar"
        loading="lazy"></iframe>
```

The third is to generate a month grid yourself, which is the version worth
learning because it is pure logic:

```js
// 05_calendar.js
export function monthMatrix(year, month) {      // month: 1–12
  const first = new Date(year, month - 1, 1);
  const lead  = first.getDay();                 // 0 = Sunday
  const days  = new Date(year, month, 0).getDate();   // day 0 of next month
  const cells = Array(lead).fill(null);
  for (let d = 1; d <= days; d++) cells.push(d);
  while (cells.length % 7) cells.push(null);
  const weeks = [];
  for (let i = 0; i < cells.length; i += 7) weeks.push(cells.slice(i, i + 7));
  return weeks;
}
```

**The trick worth remembering:** `new Date(y, m, 0)` is day zero of month `m`,
which is the **last day of month m − 1** — so it gives you the number of days
in a month, leap years included, with no table and no arithmetic.

Verified: February 2024 has 29 days, February 2025 has 28, and 1 August 2026
falls on a Saturday.

Note that JavaScript months are **0-indexed** in the `Date` constructor
(January is 0) but 1-indexed in an ISO string. Mixing the two is the classic
date bug.

---

## Experiment 6 — Mailing-list subscription form

**File:** `06_subscribe.html`

```html
<form id="subscribe" action="/subscribe" method="post">
  <label for="email">Email address *</label>
  <input type="email" id="email" name="email" required
         autocomplete="email" aria-describedby="email-error">
  <span id="email-error" class="error" role="alert"></span>

  <label for="name">Name</label>
  <input type="text" id="name" name="name" autocomplete="name">

  <fieldset>
    <legend>Interests</legend>
    <input type="checkbox" id="i1" name="topics" value="ds"><label for="i1">Data Science</label>
    <input type="checkbox" id="i2" name="topics" value="ml"><label for="i2">Machine Learning</label>
  </fieldset>

  <label for="freq">Frequency</label>
  <select id="freq" name="freq">
    <option value="d">Daily</option>
    <option value="w" selected>Weekly</option>
    <option value="m">Monthly</option>
  </select>

  <input type="checkbox" id="consent" name="consent" required>
  <label for="consent">I consent to receiving email *</label>

  <button type="submit">Subscribe</button>
</form>
```

An explicit **consent** checkbox, unticked by default, is not decoration —
pre-ticked consent is unlawful under most data-protection regimes and is the
kind of detail that separates a good answer from a complete one.

---

## Experiment 7 — Style a registration form with CSS

**Files:** `07_styled_form.html`, `07_styled_form.css`

Required: different selectors, colours, borders, spacing.

```css
:root {                                   /* custom properties */
  --brand:  #2b4c7e;
  --danger: #c92a2a;
  --line:   #ccd3dd;
}

*, *::before, *::after { box-sizing: border-box; }

form { max-width: 520px; margin: 2rem auto; padding: 1.5rem;
       background: #fff; border: 1px solid var(--line); border-radius: 10px; }

fieldset { border: 1px solid var(--line); border-radius: 8px;
           padding: 1rem; margin-bottom: 1rem; }
legend   { font-weight: 700; padding: 0 .4rem; color: var(--brand); }

label { display: block; margin-bottom: .3rem; font-weight: 600; }

input[type="text"], input[type="email"], input[type="tel"], select, textarea {
  width: 100%; padding: 10px 12px; margin-bottom: 1rem;
  border: 1px solid var(--line); border-radius: 6px;
  font: inherit;                          /* forms do NOT inherit fonts */
}

input:focus, select:focus, textarea:focus {
  border-color: var(--brand);
  outline: 3px solid rgba(43, 76, 126, .25);
}

input:invalid:not(:placeholder-shown) { border-color: var(--danger); }

label[for="terms"] { display: inline; font-weight: 400; }

button { padding: 10px 18px; border: 0; border-radius: 6px;
         background: var(--brand); color: #fff; cursor: pointer;
         transition: background .2s; }
button:hover    { background: #1f3a63; }
button:disabled { background: #aab; cursor: not-allowed; }
```

Selector types demonstrated: element (`form`), class, id, **attribute**
(`input[type="text"]`), **pseudo-class** (`:focus`, `:invalid`), descendant,
and a custom-property `:root` block.

Two details the examiner looks for. **`font: inherit`** — form controls use
the operating system font unless told otherwise, so an unstyled input looks
alien beside your text. And **`:not(:placeholder-shown)`** — without it,
`:invalid` fires on an empty required field the moment the page loads, and the
form is red before the user has typed anything.

---

## Experiment 8 — Responsive page with Flexbox and Grid

**Files:** `08_responsive.html`, `08_responsive.css`

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

**Without that meta tag the page is not responsive**, whatever the CSS says: a
phone pretends to be 980px wide and renders your desktop layout shrunk to
illegibility.

```css
/* Flexbox — one dimension: a navigation bar */
.nav { display: flex; gap: 1rem; align-items: center;
       justify-content: space-between; flex-wrap: wrap; }
.nav ul { display: flex; gap: 1rem; list-style: none; margin: 0; padding: 0; }

/* Grid — two dimensions: a card layout that needs no media query at all */
.cards { display: grid; gap: 1rem;
         grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }

/* Grid — a named page layout */
.page {
  display: grid;
  grid-template-areas: "head head" "side main" "foot foot";
  grid-template-columns: 220px 1fr;
  gap: 1rem;
}
.page > header { grid-area: head; }
.page > aside  { grid-area: side; }
.page > main   { grid-area: main; }
.page > footer { grid-area: foot; }

@media (max-width: 700px) {
  .page { grid-template-areas: "head" "main" "side" "foot";
          grid-template-columns: 1fr; }
}
```

**Flexbox for one dimension, Grid for two** — that is the whole rule.

The `repeat(auto-fit, minmax(240px, 1fr))` line is worth memorising: it fits
as many columns as will hold 240px each and stretches them to fill the row,
reflowing at every width with **no media queries at all**. It is a complete
responsive grid in one declaration.

Note that the mobile layout puts `main` **above** `side`, so a phone user
reads the content before the sidebar. Named grid areas make that reordering a
one-line change.

---

## Experiment 9 — Hover effects and transitions

**Files:** `09_hover.html`, `09_hover.css`

```css
.btn {
  background: #2b4c7e; color: #fff; padding: 10px 18px; border-radius: 6px;
  transition: background .25s ease, transform .25s ease, box-shadow .25s ease;
}
.btn:hover { background: #1f3a63; transform: translateY(-2px);
             box-shadow: 0 4px 12px rgba(0,0,0,.2); }
.btn:active{ transform: translateY(0); }

.thumb { overflow: hidden; border-radius: 8px; }
.thumb img { display: block; width: 100%;
             transition: transform .4s ease, filter .4s ease;
             filter: grayscale(60%); }
.thumb:hover img { transform: scale(1.1); filter: grayscale(0); }

.card { position: relative; }
.card .caption {
  position: absolute; inset: auto 0 0 0;
  background: rgba(0,0,0,.65); color: #fff; padding: .6rem;
  transform: translateY(100%); transition: transform .3s ease;
}
.card:hover .caption { transform: translateY(0); }

@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
```

Three points earn the marks.

**Animate `transform` and `opacity`, not `width`, `top` or `margin`.** The
browser can composite transform and opacity changes on the GPU without
recalculating layout; the others force a reflow on every frame and stutter.

**`overflow: hidden` on the wrapper** is what makes the zoom crop cleanly
instead of the enlarged image spilling over its neighbours.

**The `prefers-reduced-motion` block** respects users who get motion sickness
from animation. It is two lines and it is the difference between a page that
is merely pretty and one that is considerate.

Note that `rgba()` fades only the caption's background; `opacity` there would
fade the white text too.

---

## Experiment 10 — JavaScript string operations

**Files:** `10_string_ops.js`, `10_string_ops.html`

Reverse, substring, count vowels.

```js
export function reverse(s) {
  return [...s].reverse().join("");
}

export function countVowels(s) {
  return [...s.toLowerCase()].filter(c => "aeiou".includes(c)).length;
}

export function stats(s) {
  return {
    length:     s.length,
    words:      s.trim() === "" ? 0 : s.trim().split(/\s+/).length,
    vowels:     countVowels(s),
    consonants: (s.match(/[b-df-hj-np-tv-z]/gi) || []).length,
    digits:     (s.match(/\d/g) || []).length,
    reversed:   reverse(s),
    isPalindrome: (() => {
      const c = s.toLowerCase().replace(/[^a-z0-9]/g, "");
      return c.length > 0 && c === reverse(c);
    })()
  };
}
```

Asserted by the runner: `reverse("Data Science") === "ecneicS ataD"`,
`countVowels("Data Science") === 5`, `stats("A man, a plan, a canal: Panama")
.isPalindrome === true`, and `stats("").words === 0`.

**Three things to notice.**

`[...s]` splits by **code point**, while `s.split("")` splits by UTF-16 code
unit. For plain ASCII they agree; for an emoji or an accented character
`split("")` tears the character in half and the reversal produces garbage.

`(s.match(…) || [])` is not optional. `match` returns **`null`** when nothing
matches, not an empty array, and `null.length` throws.

`s.trim().split(/\s+/)` on an empty string gives `[""]`, whose length is 1 —
so a word count needs the explicit empty check, or every blank input reports
one word.

---

## Experiment 11 — Form validation

**Files:** `11_validation.js`, `11_validation.html`

Email format, password length, required fields.

```js
export const RULES = {
  name:     { test: v => v.trim().length >= 3,
              msg: "Name must be at least 3 characters" },
  email:    { test: v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()),
              msg: "Enter a valid email address" },
  mobile:   { test: v => /^[6-9]\d{9}$/.test(v.trim()),
              msg: "Enter a 10-digit Indian mobile number" },
  password: { test: v => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/.test(v),
              msg: "8+ characters with upper, lower, digit and symbol" }
};

export function validate(values) {
  const errors = {};
  for (const [field, rule] of Object.entries(RULES))
    if (!rule.test(values[field] ?? "")) errors[field] = rule.msg;
  if (values.password !== values.confirm) errors.confirm = "Passwords do not match";
  if (!values.terms) errors.terms = "You must accept the terms";
  return errors;
}
```

The runner asserts that `asha@` is rejected and `asha@nri.ac.in` accepted;
that `9876543210` passes and `1234567890` fails (an Indian mobile starts 6–9);
that `Passw0rd!` passes and `password` fails; and that mismatched passwords
produce exactly the `confirm` error.

The HTML half wires it up, and its `submit` handler is the part that matters:

```js
form.addEventListener("submit", e => {
  const values = Object.fromEntries(new FormData(form));
  values.terms = form.elements.terms.checked;      // FormData omits unchecked boxes
  const errors = validate(values);
  Object.keys(RULES).forEach(f => setFieldError(form.elements[f], errors[f] || ""));
  if (Object.keys(errors).length) {
    e.preventDefault();
    form.querySelector(".is-invalid")?.focus();
  }
});
```

**`FormData` omits unchecked checkboxes entirely** — the key is simply absent,
not `false` — so the `terms` value has to be read from `.checked` separately.
That one line is the most commonly missed detail in this experiment.

And say it in the viva: this is a convenience, not a control. The server
validates again.

---

## Experiment 12 — Time-based greeting

**Files:** `12_greeting.js`, `12_greeting.html`

```js
export function greeting(hour = new Date().getHours()) {
  if (hour < 0 || hour > 23 || !Number.isInteger(hour))
    throw new RangeError("hour must be an integer from 0 to 23");
  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  if (hour < 21) return "Good evening";
  return "Good night";
}
```

**Taking `hour` as a parameter with a default is the whole trick.** A function
that reads the clock internally can only be tested by waiting until 9 am; this
one is asserted at every boundary — 0, 11, 12, 16, 17, 20, 21, 23 — in a
fraction of a second, and still behaves identically when called with no
arguments in the page.

That is a general lesson, not a JavaScript one: **push the unpredictable input
to the edge of the function**, and the logic inside becomes testable. The same
idea makes Course 9's data pipelines testable.

---

## Experiment 13 — Array and object manipulation

**Files:** `13_arrays.js`, `13_arrays.html`

Add, delete, sort, search.

```js
export function addStudent(list, student) {
  if (list.some(s => s.roll === student.roll))
    throw new Error(`Roll ${student.roll} already exists`);
  return [...list, student];                   // returns a NEW array
}

export const removeStudent = (list, roll) => list.filter(s => s.roll !== roll);

export const sortBy = (list, key, desc = false) =>
  [...list].sort((a, b) => {
    const [x, y] = desc ? [b[key], a[key]] : [a[key], b[key]];
    return typeof x === "string" ? x.localeCompare(y) : x - y;
  });

export const search = (list, term) => {
  const t = term.trim().toLowerCase();
  return t === "" ? list
                  : list.filter(s => s.name.toLowerCase().includes(t)
                                  || String(s.roll).includes(t));
};

export function summary(list) {
  if (list.length === 0) return { count: 0, average: null, top: null };
  const total = list.reduce((s, x) => s + x.marks, 0);
  return {
    count:   list.length,
    average: +(total / list.length).toFixed(2),
    top:     sortBy(list, "marks", true)[0].name
  };
}
```

Every function is **pure**: it takes the list and returns a new one rather
than mutating in place. That is why `addStudent` spreads instead of pushing,
and why `sortBy` copies with `[...list]` before sorting — `sort` mutates, and
a sort that silently reorders the caller's array is a bug that surfaces three
functions away.

The comparator branches on type because **`sort()` with no comparator compares
as strings**, so `[10, 9, 100]` sorts to `[10, 100, 9]`. Numbers need `x - y`;
strings need `localeCompare`, which also handles accents correctly.

Asserted by the runner against a five-student fixture: the average is 62.4,
the top scorer is Meena, adding a duplicate roll throws, and `summary([])`
returns nulls rather than `NaN`.

---

## Experiment 14 — Render JSON as a table

**Files:** `14_json_table.js`, `14_json_table.html`, `students.json`

```js
export function toRows(data) {
  return data.students.map(s => ({
    roll:  s.roll,
    name:  s.name,
    maths: s.marks?.maths ?? null,
    stats: s.marks?.stats ?? null,
    total: (s.marks?.maths ?? 0) + (s.marks?.stats ?? 0)
  }));
}

export function renderTable(rows, tbody, doc = document) {
  tbody.textContent = "";                       // clear
  const frag = doc.createDocumentFragment();
  for (const r of rows) {
    const tr = doc.createElement("tr");
    for (const v of Object.values(r)) {
      const td = doc.createElement("td");
      td.textContent = v ?? "—";                // textContent, NOT innerHTML
      tr.append(td);
    }
    frag.append(tr);
  }
  tbody.append(frag);                           // ONE insertion
}
```

Three deliberate choices.

**`textContent`, not `innerHTML`.** The data came from a file or an API, so a
`name` of `<img src=x onerror=alert(1)>` must render as text. This is the XSS
rule from Unit 4, in the one place students most often break it.

**A `DocumentFragment`.** Rows are built off-document and inserted once, so
the browser reflows once rather than once per row.

**Optional chaining on `s.marks?.maths`.** One student in the fixture has no
`marks` object at all; without the `?.` the whole render throws and the page
goes blank instead of showing a dash.

The `doc` parameter defaults to `document` but can be passed jsdom's document,
which is how the runner tests this without a browser.

---

## Experiment 15 — Fetch weather data from an open API

**Files:** `15_weather.js`, `15_weather.html`

```js
export function summarise(json) {              // pure — testable offline
  return {
    place:     json.name,
    tempC:     Math.round(json.main.temp),
    feelsC:    Math.round(json.main.feels_like),
    humidity:  json.main.humidity,
    condition: json.weather?.[0]?.description ?? "unknown",
    wind:      json.wind?.speed ?? null
  };
}

export async function fetchWeather(city, key, fetchFn = fetch) {
  const url = new URL("https://api.openweathermap.org/data/2.5/weather");
  url.search = new URLSearchParams({ q: city, appid: key, units: "metric" });
  const res = await fetchFn(url);
  if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
  return summarise(await res.json());
}
```

The runner has no network access and no API key, so it tests `summarise`
against a **saved sample response**, and tests `fetchWeather` with a stub
`fetchFn` that returns `{ ok: false, status: 404 }` — asserting that it throws
rather than returning undefined.

That split is the point of the experiment. **Separating the network call from
the parsing makes the parsing testable**, and the parsing is where the bugs
actually are.

**Three things to say in the viva.**

`fetch` does **not reject on a 404** — an error status is still a successful
HTTP transaction, so `res.ok` must be checked explicitly. Skip it and you call
`.json()` on an HTML error page and get a confusing `SyntaxError`.

**An API key in front-end JavaScript is visible to anyone** who opens dev
tools. Acceptable for a lab with a free key; in production the request goes
through a server that holds the key.

**CORS** may block the request entirely. It is a browser restriction — the
same request from `curl` succeeds — and it cannot be worked around from the
client. If an API does not permit browser access, it needs a server-side proxy.

---

## Experiment 16 — jQuery DOM manipulation

**Files:** `16_jquery.html`, `16_jquery_native.js`

Hide, show, fade, slide, toggle.

```js
$(function () {
  $("#hide").on("click",   () => $("#panel").hide(400));
  $("#show").on("click",   () => $("#panel").show(400));
  $("#fade").on("click",   () => $("#panel").fadeToggle(300));
  $("#slide").on("click",  () => $("#panel").slideToggle(300));
  $("#toggle").on("click", () => $("#panel").toggle(300));

  $("#animate").on("click", function () {
    $("#box").stop(true).animate({ left: "250px", opacity: .5 }, 500, function () {
      $(this).addClass("done");
    });
  });

  // delegation — works for rows added later
  $("#table").on("click", ".delete-btn", function () {
    $(this).closest("tr").fadeOut(300, function () { $(this).remove(); });
  });

  $("#msg").removeClass("error").addClass("success")
           .text("Saved successfully").fadeIn(300);        // chaining
});
```

**`16_jquery_native.js` is the same behaviour with no library**, and it is
what the runner executes under jsdom — jQuery's animation queue depends on
timing that jsdom does not reproduce faithfully, while the native version's
class toggles can be asserted directly:

```js
export function wireTable(root) {
  root.addEventListener("click", e => {
    const btn = e.target.closest(".delete-btn");
    if (!btn) return;
    const tr = btn.closest("tr");
    tr.addEventListener("transitionend", () => tr.remove(), { once: true });
    tr.classList.add("fading");
  });
}
```

Asserted: clicking a `.delete-btn` adds `fading` to the correct `<tr>`, and a
click elsewhere in the table does nothing.

**Four exam points from this experiment.**

**Delegation.** `$("#table").on("click", ".delete-btn", …)` binds one listener
to the table, so rows added by AJAX afterwards work. `$(".delete-btn").on(…)`
binds only to rows that exist at that instant.

**`.closest("tr")`, not `.parent().parent()`.** Wrap the button in a `<span>`
for styling and the parent chain now removes the wrong element.

**`this` inside a jQuery handler is a raw DOM element** — wrap it as `$(this)`
to use jQuery methods on it. And an **arrow function** handler gets the
enclosing scope's `this`, so `$(this)` will not be the element; use `function`
handlers with jQuery.

**`.stop(true)`** before an animation clears the queue. Without it, five
rapid clicks queue five animations and the box keeps moving long after you
stopped clicking.

---

## Lab examination

The lab exam gives you one experiment, a browser and a text editor, roughly an
hour, and then a viva.

**What actually costs marks:**

- Forgetting `name` on form inputs, so nothing submits
- A `<label>` whose `for` does not match any `id`
- Radio buttons in one group given different `name` values
- Omitting `<!DOCTYPE html>` or `<meta charset="UTF-8">`
- Omitting the viewport meta and calling the page responsive
- `border: 2px red` with no style keyword — it renders nothing
- Treating `input.value` as a number
- Handling `click` on the submit button instead of `submit` on the form
- Forgetting `e.preventDefault()`, so the page reloads and your output vanishes
- `sort()` on numbers with no comparator
- Using `innerHTML` with data from a file or an API

**What earns them:**

- Open dev tools (F12) when something does not work. The Console shows the
  error, the Elements tab shows the live DOM, and Network shows what was
  fetched. Debugging without them is guesswork, and examiners notice.
- Validate at validator.w3.org before you submit. Browsers silently forgive
  broken markup; validators do not.
- Say the security sentence out loud in the viva: *client-side validation is a
  convenience for honest users, and the server must validate again.*
- When the syllabus asks for something obsolete — `<font>`, a table used for
  layout, `window.status` — do it as asked, then name the modern replacement
  and why it replaced it. That is the difference between a pass and a
  distinction.
