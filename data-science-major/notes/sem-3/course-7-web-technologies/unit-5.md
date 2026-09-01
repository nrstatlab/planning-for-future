# Unit 5 — JSON and jQuery

**Syllabus topics:** Introduction to JSON — need for data exchange formats,
JSON syntax, JSON vs XML, parsing JSON, creating JSON objects and arrays,
accessing nested JSON data, reading/writing JSON in JavaScript. Working with
jQuery — introduction, selectors, filters, DOM manipulation, event handling,
animations, effects, and chaining.

---

## 5.1 Why data exchange formats exist

### 🎯 The big idea

A JavaScript object lives in one program's memory. To send it to another
program — over a network, into a file, into a database — it must become a
**string**. Turning structure into a string is **serialisation**; turning it
back is **parsing**. JSON is a format for doing both.

Three programs that need to agree:

```
Browser (JavaScript)  ──── JSON text ────►  Server (Python)
                      ◄─── JSON text ────
                                            ↓
                                       MongoDB (Course 10)
```

None of them share a memory layout, a type system or even a byte order. They
share a **text format**, and each side converts at its own boundary. That is
the whole idea.

## 5.2 JSON

**JSON** — JavaScript Object Notation. Devised by **Douglas Crockford** around
2001; standardised as ECMA-404 and RFC 8259.

It is a **subset of JavaScript's object literal syntax**, and — despite the
name — it is language-independent. Every serious language has a JSON parser.

### Syntax

```json
{
  "roll": 23,
  "name": "Asha Kumari",
  "cgpa": 8.74,
  "active": true,
  "guardian": null,
  "subjects": ["Data Science", "Statistics", "Python"],
  "address": {
    "city": "Vijayawada",
    "state": "Andhra Pradesh",
    "pin": "520010"
  },
  "marks": [
    { "subject": "Maths", "score": 88 },
    { "subject": "Stats", "score": 91 }
  ]
}
```

**Six value types, and no more:**

| Type | Example |
|---|---|
| string | `"Asha"` — **double quotes only** |
| number | `23`, `8.74`, `-1.2e3` |
| boolean | `true`, `false` — lowercase |
| null | `null` |
| object | `{ "k": v }` |
| array | `[1, 2, 3]` |

### ⚠️ What JSON does **not** allow

This list is the exam question, and every item is a real mistake people make.

| Not allowed | Why |
|---|---|
| Single quotes `'x'` | Strings are double-quoted, always |
| Unquoted keys `{name: 1}` | **Keys must be quoted strings** |
| Trailing comma `[1, 2,]` | Strict — a JavaScript literal permits it, JSON does not |
| Comments `// …` | Deliberately excluded by Crockford |
| `undefined` | Not a JSON value |
| `NaN`, `Infinity` | Not JSON numbers |
| Functions | JSON carries data, never behaviour |
| Dates | No date type — use an ISO 8601 **string** |
| Leading zeros `007`, `+5`, `.5` | Invalid numbers |
| Hex `0xFF` | Invalid |

```json
{
  'name': 'Asha',     ← single quotes
  roll: 23,           ← unquoted key
  cgpa: NaN,          ← not a JSON value
  joined: new Date(), ← not JSON at all
}                     ← trailing comma
```

Five errors in five lines. `JSON.parse` rejects the whole document on the first
one, with a `SyntaxError`.

The absence of comments is deliberate: Crockford removed them because people
were using them to carry parsing directives. If you need a comment, add a
`"_comment"` key.

### 🔢 JSON vs XML

| | JSON | XML |
|---|---|---|
| Syntax | Braces and brackets | Tags |
| Verbosity | Compact | Roughly 2× the bytes |
| Data types | 6 native types | Everything is text |
| Arrays | Native `[…]` | By convention only |
| Parsing in JS | `JSON.parse` — built in, fast | DOM parser — slower, clumsy |
| Attributes | No | Yes |
| Comments | No | Yes |
| Namespaces | No | Yes |
| Schema | JSON Schema (optional) | XSD, DTD (mature) |
| Validation | Weaker | Stronger |
| Mixed content | Poor | Designed for it |
| Typical use | Web APIs, config, NoSQL | Documents, SOAP, RSS, Office files |

The same data, both ways:

```json
{"student": {"roll": 23, "name": "Asha", "subjects": ["DS", "Stats"]}}
```
```xml
<student>
  <roll>23</roll>
  <name>Asha</name>
  <subjects>
    <subject>DS</subject>
    <subject>Stats</subject>
  </subjects>
</student>
```

67 characters against 148. Multiply by a million API calls a day and the
difference is real bandwidth.

**When XML is still the right answer:** documents with mixed content (text
*with* markup inside it, like HTML), where schema validation is contractual, or
where the ecosystem already uses it — SOAP, RSS, SVG, and every `.docx` and
`.xlsx` file. **When JSON is the right answer:** almost every web API written
since 2010.

### ⚠️ JSON is not JavaScript

Every JSON document is valid JavaScript **as an expression**, but the reverse
is false. And a subtle trap:

```js
{"a": 1}          // in a JS statement position this is a BLOCK with a label
JSON.parse('{"a": 1}')   // this is how you get an object
```

Never evaluate JSON with `eval()`. It executes whatever arrives, so a
compromised or malicious endpoint gets to run code in your page. `JSON.parse`
only parses.

## 5.3 Parsing and stringifying

```js
const text = '{"roll":23,"name":"Asha","marks":[88,91]}';

const obj = JSON.parse(text);          // string → object
obj.name;                              // "Asha"
obj.marks[1];                          // 91

const back = JSON.stringify(obj);      // object → string
JSON.stringify(obj, null, 2);          // pretty-printed with 2-space indent
JSON.stringify(obj, ["roll", "name"]); // only these keys
```

### Always wrap `JSON.parse` in `try/catch`

```js
function safeParse(text, fallback = null) {
  try { return JSON.parse(text); }
  catch (e) { console.error("Invalid JSON:", e.message); return fallback; }
}
safeParse('{bad}');            // null, with a logged message
safeParse('{"ok":true}');      // { ok: true }
```

Any input from a network, a file or `localStorage` can be malformed. An
unguarded `JSON.parse` turns that into an uncaught exception that kills the
rest of your script.

### ⚠️ What `stringify` silently drops

```js
JSON.stringify({
  a: undefined,        // key omitted entirely
  b: function () {},   // key omitted entirely
  c: Symbol("s"),      // key omitted entirely
  d: NaN,              // → null
  e: Infinity,         // → null
  f: new Date(),       // → an ISO string
  g: new Map([[1,2]]), // → {}  — Maps and Sets do NOT serialise
  h: 10n               // → TypeError: BigInt not serializable
});
```

`{"d":null,"e":null,"f":"2026-08-26T00:00:00.000Z","g":{}}` — three keys have
vanished without a word and two numbers have become `null`. In an array,
`undefined` becomes `null` instead of disappearing, because array positions
must be preserved:

```js
JSON.stringify([1, undefined, 3]);    // "[1,null,3]"
JSON.stringify({ x: undefined });     // "{}"
```

A **circular reference** throws:

```js
const a = {}; a.self = a;
JSON.stringify(a);                    // TypeError: Converting circular structure to JSON
```

### Replacer and reviver

The optional second argument to each function transforms values as they pass:

```js
// replacer — redact on the way out
JSON.stringify(user, (key, value) => key === "password" ? undefined : value);

// reviver — rebuild real Dates on the way in
const parsed = JSON.parse(text, (key, value) =>
  typeof value === "string" && /^\d{4}-\d{2}-\d{2}T/.test(value)
    ? new Date(value) : value);
```

The reviver is the standard answer to "JSON has no date type": store ISO 8601
strings, and rebuild `Date` objects on parse.

### The deep-copy idiom, and why it is flawed

```js
const copy = JSON.parse(JSON.stringify(original));
```

It works, and it is widely used, but it inherits every limitation above:
functions, `undefined`, `Map`, `Set` and `Symbol` are lost, `Date`s become
strings, and circular references throw. `structuredClone(original)` handles all
of those correctly and is now available everywhere.

## 5.4 Creating and accessing nested JSON

```js
const data = {
  college: "NRI College",
  departments: [
    {
      name: "Data Science",
      hod: { name: "Dr. Rao", email: "rao@nri.ac.in" },
      students: [
        { roll: 23, name: "Asha",  marks: { maths: 88, stats: 91 } },
        { roll: 24, name: "Ravi",  marks: { maths: 65, stats: 58 } }
      ]
    },
    { name: "Statistics", hod: { name: "Dr. Devi" }, students: [] }
  ]
};
```

Every access is a chain of `.` for object keys and `[i]` for array indices:

```js
data.college                                        // "NRI College"
data.departments[0].name                            // "Data Science"
data.departments[0].hod.email                       // "rao@nri.ac.in"
data.departments[0].students[1].marks.stats         // 58
data.departments.length                             // 2
data.departments[1].students.length                 // 0
```

### ⚠️ Guard every level you are not sure about

```js
data.departments[1].hod.email          // TypeError — Statistics has no email
data.departments[1].hod?.email         // undefined — safe
data.departments[5]?.name              // undefined — safe
data.departments[1].hod?.email ?? "not listed"      // a usable default
```

A single missing key three levels down throws and stops the script. Optional
chaining is not decoration here; with data from an API you do not control, it
is the difference between a blank field and a blank page.

For deep, uncertain paths, a helper is clearer than a chain of `?.`:

```js
const get = (obj, path, dflt) =>
  path.split(".").reduce((o, k) => (o == null ? undefined : o[k]), obj) ?? dflt;

get(data, "departments.0.hod.email", "—");   // "rao@nri.ac.in"
get(data, "departments.1.hod.email", "—");   // "—"
```

### Traversing and aggregating

```js
// every student, flattened out of the departments
const all = data.departments.flatMap(d =>
  d.students.map(s => ({ dept: d.name, ...s })));

// class average in statistics
const stats = all.map(s => s.marks.stats);
const avg = stats.reduce((a, b) => a + b, 0) / stats.length;   // 74.5

// group by department
const byDept = {};
for (const s of all) (byDept[s.dept] ||= []).push(s.name);
// { "Data Science": ["Asha", "Ravi"] }

// toppers
const top = [...all].sort((a, b) => b.marks.maths - a.marks.maths)[0].name;  // "Asha"
```

`flatMap` is `map` followed by a one-level `flat`, and it is exactly the right
tool for "an array inside each element of an array".

### 💡 This is what Course 10 stores

A MongoDB document **is** a JSON-shaped object — nested arrays and
sub-documents included. Where Course 5's SQL would need three tables and two
joins to represent this college, MongoDB stores the whole tree in one document.
Unit 5 of this course is, in effect, the data model of Course 10.

## 5.5 Reading and writing JSON in JavaScript

### From a server — `fetch`

```js
async function loadStudents() {
  try {
    const res = await fetch("students.json");
    if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
    const data = await res.json();          // parses the body as JSON
    render(data);
  } catch (err) {
    document.getElementById("status").textContent = "Could not load data: " + err.message;
  }
}
```

### ⚠️ `fetch` does not reject on 404

A 404 or a 500 is a **successful HTTP transaction** that returned an error
status, so the promise resolves. `fetch` only rejects on a *network* failure —
DNS, offline, CORS. **You must check `res.ok` yourself.** Omitting that check
means calling `.json()` on an HTML error page and getting a confusing
`SyntaxError` instead of a clear "not found".

### Sending JSON

```js
const res = await fetch("/api/students", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ roll: 25, name: "Kiran" })
});
```

`body` must be a **string** — `fetch` will not serialise an object for you, and
the `Content-Type` header is what tells the server how to read it.

### Local storage

```js
localStorage.setItem("prefs", JSON.stringify({ theme: "dark", size: 16 }));
const prefs = JSON.parse(localStorage.getItem("prefs") || "{}");
localStorage.removeItem("prefs");
```

`localStorage` stores **strings only**, so JSON is how you keep an object in
it. `|| "{}"` handles the first visit, when `getItem` returns `null` and
`JSON.parse(null)` would give `null` rather than an object. `sessionStorage`
has the same API but is cleared when the tab closes.

Never store passwords, tokens or personal data there: any script on the page
can read it.

### Rendering JSON into a table — lab experiment 14

```js
function renderTable(students) {
  const tbody = document.querySelector("#studentTable tbody");
  tbody.textContent = "";                                  // clear
  const frag = document.createDocumentFragment();
  for (const s of students) {
    const tr = document.createElement("tr");
    for (const v of [s.roll, s.name, s.marks.maths, s.marks.stats]) {
      const td = document.createElement("td");
      td.textContent = v ?? "—";                           // textContent — not innerHTML
      tr.append(td);
    }
    frag.append(tr);
  }
  tbody.append(frag);
}
```

`textContent` again, for the same reason as Unit 4: the data came from
elsewhere, and a `name` of `<img src=x onerror=…>` must render as text.

## 5.6 jQuery

**jQuery** — John Resig, 2006. A library whose purpose was to hide the
differences between browsers behind one small API. At its peak it was on the
majority of websites in existence.

```html
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="js/jquery-3.7.1.min.js"></script>   <!-- or a local copy -->
```

```js
$(document).ready(function () { … });   // classic
$(function () { … });                   // shorthand for the same thing
jQuery.noConflict();                    // release $ if another library wants it
```

`$(…)` is a function that returns a **jQuery object** — an array-like wrapper
around a set of DOM elements, carrying jQuery's methods.

### ⚠️ jQuery objects are not DOM elements

```js
$("#btn").value          // undefined — jQuery objects have no .value
$("#btn").val()          // correct
$("#btn")[0].value       // the raw DOM element, then its property
$("#btn").get(0)         // same thing
$(document.getElementById("btn"))    // DOM element → jQuery object
```

Mixing the two APIs on the same variable is the commonest jQuery bug. The
convention that prevents it is to prefix jQuery variables with `$`:
`const $btn = $("#btn");`

### 🔢 jQuery to plain JavaScript

The syllabus teaches jQuery. Learn the mapping alongside it, because that is
what you will write professionally.

| jQuery | Modern JavaScript |
|---|---|
| `$("#id")` | `document.getElementById("id")` |
| `$(".c")` | `document.querySelectorAll(".c")` |
| `$(el).addClass("x")` | `el.classList.add("x")` |
| `$(el).removeClass("x")` | `el.classList.remove("x")` |
| `$(el).toggleClass("x")` | `el.classList.toggle("x")` |
| `$(el).hasClass("x")` | `el.classList.contains("x")` |
| `$(el).text()` | `el.textContent` |
| `$(el).html()` | `el.innerHTML` |
| `$(el).val()` | `el.value` |
| `$(el).attr("a")` | `el.getAttribute("a")` |
| `$(el).css("color", "red")` | `el.style.color = "red"` |
| `$(el).on("click", f)` | `el.addEventListener("click", f)` |
| `$(el).hide()` | `el.style.display = "none"` |
| `$(el).append(x)` | `el.append(x)` |
| `$(el).remove()` | `el.remove()` |
| `$(el).closest("li")` | `el.closest("li")` |
| `$.each(a, f)` | `a.forEach(f)` |
| `$.ajax(…)` | `fetch(…)` |
| `$(document).ready(f)` | `document.addEventListener("DOMContentLoaded", f)` |

Every entry on the right is now supported by every browser in use. `closest`,
`classList`, `querySelectorAll`, `fetch` and `append` all exist because jQuery
proved they were needed — the library's ideas were absorbed into the platform.

## 5.7 jQuery selectors and filters

Any CSS selector works, plus jQuery's own extensions.

```js
$("p")                    $("#main")                $(".card")
$("ul li")                $("ul > li")              $("h2 + p")
$("input[type='text']")   $("a[href$='.pdf']")
$("p, div, span")         $("*")
```

**Filters** — jQuery-only pseudo-selectors:

| Filter | Selects |
|---|---|
| `:first` / `:last` | The first / last in the whole set |
| `:even` / `:odd` | **0-indexed** — `:even` is the 1st, 3rd, 5th |
| `:eq(n)` / `:gt(n)` / `:lt(n)` | At / after / before index n |
| `:not(sel)` | Excluding |
| `:contains('text')` | Containing that text |
| `:empty` / `:parent` | No children / has children |
| `:has(sel)` | Containing a matching descendant |
| `:hidden` / `:visible` | By rendered visibility |
| `:input`, `:text`, `:checkbox`, `:radio`, `:submit` | Form controls |
| `:checked`, `:selected`, `:disabled` | Form state |

### ⚠️ `:even` and `:nth-child(even)` disagree

`:even` is **0-indexed**, so it matches the 1st, 3rd, 5th rows. CSS's
`:nth-child(even)` is **1-indexed**, so it matches the 2nd, 4th, 6th. Swapping
them inverts your zebra stripes.

`:first`, `:even`, `:contains` and friends are **not CSS**, so they cannot be
used with `querySelectorAll` and jQuery must filter them itself, slowly. Prefer
`.first()` and `.eq(n)`, which are methods rather than selector text.

### Traversal

```js
$(el).parent()      .parents()      .parentsUntil(sel)   .closest(sel)
     .children()    .find(sel)
     .next()        .nextAll()      .prev()   .prevAll()  .siblings()
     .first()       .last()         .eq(n)    .filter(sel)  .not(sel)
     .index()       .length         .each(fn)
```

`.find()` searches **descendants**; `.filter()` narrows the **current set**.
`$("div").find(".x")` gets `.x` inside divs; `$("div").filter(".x")` gets divs
that *are* `.x`.

## 5.8 jQuery DOM manipulation

```js
$("#t").text()                     // get
$("#t").text("New title")          // set — the SAME method does both
$("#t").html("<em>New</em>")
$("#name").val("Asha")

$("#box").attr("title", "hi")      // HTML attribute
$("#cb").prop("checked", true)     // DOM property  ← for checked/disabled/selected
$("#box").removeAttr("title")
$("#box").data("roll")             // reads data-roll

$("#list").append("<li>end</li>")      // inside, last
$("#list").prepend("<li>start</li>")   // inside, first
$("#list").after("<p>after</p>")       // outside, after
$("#list").before("<p>before</p>")     // outside, before
$("#list li").remove()                 // remove elements
$("#list").empty()                     // remove children, keep the element
$("#box").clone()

$("#box").addClass("on").removeClass("off").toggleClass("open");
$("#box").css("color", "red");
$("#box").css({ color: "red", fontSize: "18px" });   // camelCase keys
$("#box").width();  $("#box").height();  $("#box").offset();
```

### ⚠️ `.attr()` vs `.prop()`

```html
<input type="checkbox" id="cb" checked>
```
```js
$("#cb").attr("checked")     // "checked" — the ATTRIBUTE, i.e. the initial value
$("#cb").prop("checked")     // true/false — the PROPERTY, i.e. the CURRENT state
```

The user unticks the box: the attribute still says `checked`, the property is
now `false`. **Use `.prop()` for `checked`, `selected` and `disabled`; use
`.attr()` for everything else.** jQuery 1.6 split them precisely because this
was such a common source of bugs.

### Chaining

Almost every jQuery **setter** returns the same jQuery object, so calls chain:

```js
$("#msg")
  .removeClass("error")
  .addClass("success")
  .text("Saved successfully")
  .css("color", "green")
  .fadeIn(300);
```

That is jQuery's signature feature and a guaranteed exam question. Two rules:

- **Getters break the chain.** `.text()` with no argument returns a *string*,
  and a string has no `.css()`. Only setters return the jQuery object.
- **A chain on an empty set does nothing, silently.** `$("#typo").text("x")`
  with no such element throws no error and shows no warning — the classic "my
  jQuery isn't working" with no message anywhere. Check `.length` when
  debugging.

`.end()` reverts a chain to the previous set:

```js
$("#list").find("li").addClass("item").end().addClass("list-styled");
```

## 5.9 jQuery event handling

```js
$("#btn").on("click", function (e) {
  e.preventDefault();
  $(this).toggleClass("active");         // `this` is the raw DOM element
});

$("#form").on("submit", handler);
$("#f").on("focus blur", handler);       // several events at once
$("#btn").one("click", handler);         // fires at most once
$("#btn").off("click", handler);
$("#btn").trigger("click");              // fire it programmatically

// delegation — the second argument is the selector
$("#table").on("click", "button.delete", function () {
  $(this).closest("tr").remove();
});
```

### ⚠️ `this` inside a jQuery handler is a **DOM element**

```js
$("#btn").on("click", function () {
  this.textContent = "x";       // works — raw DOM
  this.text("x");               // TypeError — DOM elements have no .text()
  $(this).text("x");            // correct — wrap it first
});
```

And, as in Unit 4, an **arrow function** handler gets the enclosing scope's
`this`, so `$(this)` will not be the element. Use `function` handlers with
jQuery, or reach the element through `e.currentTarget`.

### The delegation argument

```js
$(".delete").on("click", handler);              // binds to existing elements ONLY
$("#table").on("click", ".delete", handler);    // works for future rows too
```

The first form binds N listeners now, and rows added afterwards have none. The
second binds one listener on the container. Since AJAX-loaded content is added
after page load, the second form is nearly always what you want — this is the
jQuery version of Unit 4's event delegation.

Shorthand methods — `.click()`, `.hover()`, `.submit()` — still work but are
deprecated in favour of `.on()`, which is the only form that supports
delegation.

## 5.10 jQuery effects and animations

```js
$("#box").hide();          $("#box").show();        $("#box").toggle();
$("#box").hide(400);       $("#box").show("slow");  // "slow"=600ms, "fast"=200ms

$("#box").fadeIn(300);     $("#box").fadeOut(300);
$("#box").fadeToggle();    $("#box").fadeTo(400, 0.5);

$("#panel").slideDown(300); $("#panel").slideUp(300); $("#panel").slideToggle();

$("#box").animate({ left: "250px", opacity: 0.5, width: "300px" }, 500, function () {
  $(this).addClass("done");                    // callback runs when it finishes
});

$("#box").delay(500).fadeIn(300);
$("#box").stop();          $("#box").stop(true, true);   // clear queue, jump to end
```

Effects **queue** per element: each waits for the previous to finish. That is
why they read so naturally chained, and why forgetting `.stop()` on a hover
effect produces the familiar bug where the box keeps animating long after the
pointer has left — every hover queued another animation.

`.animate()` only handles **numeric** properties. It cannot animate colours
(without a plugin) or `display`.

### ⚠️ Prefer CSS transitions

```js
$("#box").fadeIn(300);                              // JavaScript animates every frame
```
```css
.box       { opacity: 0; transition: opacity .3s; }
.box.shown { opacity: 1; }
```
```js
$("#box").addClass("shown");                        // the browser animates it
```

CSS transitions run on the compositor, so they stay smooth when the main thread
is busy, and they respect `prefers-reduced-motion`. jQuery's effects run on
timers in JavaScript.

### AJAX — lab experiments 15 and 16

```js
$.getJSON("students.json", function (data) { render(data); });

$.ajax({
  url: "https://api.openweathermap.org/data/2.5/weather",
  method: "GET",
  data: { q: "Vijayawada", appid: KEY, units: "metric" },
  dataType: "json",
  success: function (d) {
    $("#temp").text(d.main.temp + " °C");
    $("#hum").text(d.main.humidity + " %");
    $("#cond").text(d.weather[0].description);
  },
  error: function (xhr, status, err) {
    $("#status").text("Could not fetch weather: " + err);
  }
});
```

The modern equivalent, with no library at all:

```js
const url = new URL("https://api.openweathermap.org/data/2.5/weather");
url.search = new URLSearchParams({ q: "Vijayawada", appid: KEY, units: "metric" });

try {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const d = await res.json();
  document.getElementById("temp").textContent = `${d.main.temp} °C`;
} catch (e) {
  document.getElementById("status").textContent = "Could not fetch weather: " + e.message;
}
```

**Note on lab 15:** an API key in front-end JavaScript is visible to anyone who
opens dev tools. That is acceptable for a lab exercise with a free key, and
unacceptable in anything real — production code proxies the request through a
server that holds the key. Say so if you are asked; it is the kind of remark
that distinguishes a good answer.

**CORS** is the other thing that will bite you: a browser refuses a
cross-origin response unless the server sends
`Access-Control-Allow-Origin`. It is a *browser* restriction — the same request
from `curl` succeeds — and it cannot be worked around from the client. If a
public API does not permit browser access, it needs a server-side proxy.

### 💡 Should you learn jQuery?

Learn it because it is examined, and because a great deal of existing code uses
it — you will meet it in any codebase older than a few years. But know what
replaced it and why.

jQuery solved a real problem: in 2006, `document.querySelectorAll` did not
exist, and Internet Explorer's event model was incompatible with everyone
else's. **Browsers fixed that.** Every jQuery core feature now has a native
equivalent, and jQuery adds roughly 30 KB and a layer of indirection for no
capability you lack. New projects use plain JavaScript for small work and
React, Vue or Svelte for large work; none of them use jQuery.

The honest summary for an exam: *jQuery's ideas succeeded so completely that
the library became unnecessary.*

---

## Practice problems

### Problem 1

Find every error in this JSON, then write the corrected version.

```
{
  'roll': 23,
  name: "Asha",
  cgpa: 8.74,
  active: True,
  joined: new Date("2024-07-01"),
  marks: [88, 91,],
  // class teacher
  teacher: undefined
}
```

**Solution.** Seven distinct errors:

| # | Error | Fix |
|---|---|---|
| 1 | `'roll'` in single quotes | `"roll"` |
| 2 | `name`, `cgpa`, `active`, … unquoted keys | Quote every key |
| 3 | `True` capitalised | `true` |
| 4 | `new Date(…)` — not a JSON value | An ISO 8601 **string** |
| 5 | Trailing comma in `[88, 91,]` | Remove it |
| 6 | `//` comment | Not permitted at all |
| 7 | `undefined` — not a JSON value | Use `null`, or omit the key |

```json
{
  "roll": 23,
  "name": "Asha",
  "cgpa": 8.74,
  "active": true,
  "joined": "2024-07-01",
  "marks": [88, 91],
  "teacher": null
}
```

### Problem 2

Given the nested `data` object from §5.4, write expressions for: the HOD's
email of the second department (which has none), the number of students across
all departments, and the name of the highest scorer in statistics — each safe
against missing data.

**Solution.**

```js
// 1 — optional chaining plus a default
const email = data.departments[1]?.hod?.email ?? "not listed";      // "not listed"

// 2 — reduce over the departments
const total = data.departments.reduce((n, d) => n + (d.students?.length ?? 0), 0);  // 2

// 3 — flatten, guard, sort, take the first
const topper = data.departments
  .flatMap(d => d.students ?? [])
  .filter(s => typeof s.marks?.stats === "number")
  .sort((a, b) => b.marks.stats - a.marks.stats)[0]?.name ?? "no data";   // "Asha"
```

The `filter` before the `sort` matters: a student with no `marks.stats` gives
`undefined` in the comparator, `b - a` is `NaN`, and the sort order becomes
undefined behaviour rather than an error — a silently wrong answer, which is
worse than a crash.

### Problem 3

Rewrite this jQuery in plain JavaScript, and identify the two bugs in it.

```js
$(".delete-btn").click(function () {
  if (confirm("Delete?")) {
    $(this).parent().parent().fadeOut(300, function () { $(this).remove(); });
  }
});
```

**Solution.**

The two bugs:

1. **No delegation.** `$(".delete-btn")` binds only to buttons that exist at
   that moment. Rows added later — after an AJAX load, or by the user — get no
   handler at all.
2. **`.parent().parent()`** is brittle. Wrap the button in a `<span>` for
   styling and it now removes the `<td>` instead of the `<tr>`. Use
   `.closest("tr")`, which states the intent.

Corrected jQuery, then the plain equivalent:

```js
$("#table").on("click", ".delete-btn", function () {
  if (confirm("Delete?")) $(this).closest("tr").fadeOut(300, function () { $(this).remove(); });
});
```
```js
document.getElementById("table").addEventListener("click", e => {
  const btn = e.target.closest(".delete-btn");
  if (!btn || !confirm("Delete?")) return;
  const tr = btn.closest("tr");
  tr.addEventListener("transitionend", () => tr.remove(), { once: true });
  tr.classList.add("fading");                 // CSS: opacity 0, transition .3s
});
```

The plain version uses `transitionend` with `{ once: true }` so the removal
happens after the CSS fade — the direct equivalent of jQuery's animation
callback, with the animation itself moved into the stylesheet.

---

## Exam questions from this unit

**Two marks**

1. What is JSON, and who devised it?
2. List the JSON data types.
3. Give three things valid in a JavaScript object literal but invalid in JSON.
4. Distinguish `JSON.parse` from `JSON.stringify`.
5. Why must `JSON.parse` be wrapped in `try/catch`?
6. What is method chaining in jQuery?
7. Distinguish `.attr()` from `.prop()`.
8. Why does `fetch` not reject on a 404?

**Five marks**

1. Compare JSON and XML with examples, and state when each is appropriate.
2. Explain JSON syntax exhaustively with a nested example.
3. Explain accessing nested JSON data, with safe handling of missing keys.
4. Explain jQuery selectors and filters with examples.
5. Explain jQuery effects and animations with examples.
6. Explain jQuery event handling and delegation.

**Ten marks**

1. Write a program that fetches JSON data and renders it as a sortable,
   filterable table, and explain it.
2. Explain jQuery completely — selectors, traversal, DOM manipulation, events,
   effects, chaining and AJAX — with examples.
3. Explain JSON, its syntax and its use in JavaScript, comparing it with XML
   throughout.

## Mistakes that cost marks

- Single-quoting JSON strings
- Unquoted JSON keys
- A trailing comma in a JSON array or object
- Writing `//` comments in JSON
- `True` / `False` instead of `true` / `false`
- Claiming JSON has a date type
- Expecting `JSON.stringify` to keep functions or `undefined`
- Using `eval()` instead of `JSON.parse`
- Calling `.json()` without checking `res.ok`
- Treating a jQuery object as a DOM element, or the reverse
- Using `.attr("checked")` for a checkbox's current state
- Binding jQuery handlers without delegation, so new rows are dead
- Using an arrow function and expecting `$(this)` to work
- Confusing jQuery's 0-indexed `:even` with CSS's 1-indexed `:nth-child(even)`
- Continuing a chain after a getter
