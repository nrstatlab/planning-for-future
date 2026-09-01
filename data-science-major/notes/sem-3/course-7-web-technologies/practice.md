# Course 7 — Practice Questions with Solutions

Worked answers for the questions listed at the end of each unit, plus the
kinds of applied problems the lab examiner asks. Attempt each one before
reading the solution — recognising an answer is not the same as producing it.

---

## Section A — Two-mark questions

### 1. Distinguish a web application from a desktop application.

A desktop application is installed on and runs on the user's own machine; a
web application runs on a server and is delivered to a browser over HTTP.

The decisive practical difference is **deployment**: fixing a bug in a web
application means updating one server, while fixing it in a desktop
application means persuading every user to install a patch. Desktop
applications are faster and work offline with full hardware access; web
applications are platform-independent, need no installation, and centralise
data.

### 2. What does `<!DOCTYPE html>` do?

It tells the browser to render in **standards mode**. Omitting it triggers
**quirks mode**, in which the browser emulates 1990s bugs — most visibly, the
box model computes `width` as including padding and border. It is not an HTML
tag and has no closing form.

### 3. Distinguish `<strong>` from `<b>`.

Both render bold by default. `<strong>` is **semantic** — it means "this
content is important", and a screen reader may change its tone for it. `<b>`
is **presentational** — it means "draw this bold" with no meaning attached.
Prefer `<strong>` unless you genuinely mean only visual weight. The same
relationship holds between `<em>` (emphasis) and `<i>` (italic).

### 4. Why must an `<img>` carry an `alt` attribute?

Three reasons: a screen reader announces it, so blind users learn what the
image shows; it displays if the image fails to load; and search engines index
it. It is required by the HTML specification. For a purely decorative image
write `alt=""` — an *empty* alt, which tells assistive technology to skip it.
Omitting the attribute entirely makes the screen reader read the filename
aloud instead.

### 5. Distinguish `id` from `class`.

An `id` must be **unique** in the document and an element may have only one;
a `class` is reusable and an element may carry many, space-separated. In CSS
`id` is `#name` and class is `.name`, and `id` has higher specificity. Use
`id` for one specific element or as a link anchor; use `class` for styling
groups.

### 6. What does "cascading" mean in Cascading Style Sheets?

Several rules can target the same element and set the same property. The
cascade is the defined order that decides which wins: `!important`
declarations first, then **specificity**, then **source order** — the rule
written last. Rules cascade down through this order rather than conflicting.

### 7. Distinguish padding from margin.

Padding is the space **inside** the border, between the border and the
content; margin is the space **outside** the border, between this element and
its neighbours. Padding is covered by the element's background; margin is
always transparent. Vertical margins **collapse** with adjacent margins;
padding never does.

### 8. Distinguish a pseudo-class from a pseudo-element.

A **pseudo-class** (one colon, `:hover`) selects a whole element that is in a
particular **state**. A **pseudo-element** (two colons, `::before`) selects a
**part** of an element or inserts generated content. A pseudo-class targets
something in the DOM; a pseudo-element targets something that is not.

### 9. Distinguish `opacity` from `rgba()`.

`opacity: 0.5` fades the **entire element and all its children**, text
included, and a child cannot undo it. `rgba(0,0,0,0.5)` fades **only the
colour it is applied to**. For a translucent overlay with crisp text, `rgba()`
is the only correct choice.

### 10. What is `border-collapse`?

A table property. With the default `separate`, every cell draws its own
border, so adjacent cells show a doubled line. With `collapse`, adjacent
borders merge into one. `border-spacing` works only under `separate`.

### 11. Distinguish `em` from `rem`.

`em` is relative to the **parent element's** font size and therefore
**compounds** through nesting — three nested elements at `1.2em` give
1.2³ = 1.728× the base. `rem` is relative to the **root** `<html>` font size
and never compounds. Use `rem` for type, and `em` for spacing that should
scale with its own element's text.

### 12. What is DHTML?

Dynamic HTML — not a language, but a **name for the combination** of HTML,
CSS, JavaScript and the DOM used to change a page after it has loaded. The
term is historical; it is no longer used in industry.

### 13. Distinguish JavaScript from Java.

Unrelated languages that share four letters for marketing reasons.
JavaScript is dynamically and weakly typed, interpreted or JIT-compiled, runs
in a browser or Node.js, and uses **prototypal** inheritance. Java is
statically and strongly typed, compiled to bytecode, runs on the JVM, and uses
**class-based** inheritance.

### 14. Distinguish `==` from `===`.

`==` performs type coercion before comparing, so `5 == "5"` is `true`.
`===` compares type **and** value with no coercion, so `5 === "5"` is
`false`. Always use `===`; the one accepted exception is `x == null`, which
tests for `null` or `undefined` together.

### 15. Distinguish `let`, `const` and `var`.

| | `var` | `let` | `const` |
|---|---|---|---|
| Scope | Function | Block | Block |
| Reassign | Yes | Yes | **No** |
| Redeclare | Yes | No | No |
| Hoisting | To `undefined` | Temporal dead zone | Temporal dead zone |

`const` prevents **rebinding**, not mutation: a `const` array can still be
pushed to. Use `const` by default, `let` when the value must change, `var`
never.

### 16. What is a closure?

A function that retains access to the variables of the scope in which it was
created, even after that scope has returned. It is how JavaScript provided
private state before class fields existed.

```js
function counter() {
  let n = 0;                      // private
  return () => ++n;
}
const next = counter();
next();  next();                  // 2 — n survived
```

### 17. Distinguish `for…in` from `for…of`.

`for…in` iterates **keys** (and includes inherited enumerable properties);
`for…of` iterates **values** of an iterable. On an array, `for…in` gives
index **strings** in no guaranteed order, so `i + 1` produces `"01"`. Use
`for…of` on arrays and `for…in` on plain objects.

### 18. Why does `[10, 9, 100].sort()` give the wrong order?

`sort()` with no comparator converts every element to a string and compares
lexicographically, so `"100" < "9"` and the result is `[10, 100, 9]`. Pass a
comparator: `.sort((a, b) => a - b)`. Note also that `sort` **mutates** the
original array.

### 19. What is the DOM?

The Document Object Model — the tree of objects the browser builds in memory
from an HTML document. JavaScript changes the page by changing that tree, and
the browser re-renders. The HTML file is not the page; the DOM is.

### 20. Distinguish the DOM from the BOM.

The **DOM** models the *document* — the element tree, rooted at `document`.
The **BOM**, Browser Object Model, models the *browser* — `window`,
`navigator`, `location`, `history`, `screen`. `document` is a property of
`window` and is the bridge between them.

### 21. Distinguish `innerHTML` from `textContent`.

`innerHTML` gets or sets content as **parsed HTML**; `textContent` treats it
as **plain text**, escaping any tags. Setting `innerHTML` from user input is a
**cross-site scripting (XSS)** vulnerability. `innerHTML` also destroys and
rebuilds the subtree, losing event listeners and typed form values.

### 22. Name the three JavaScript dialog boxes and say what each returns.

`alert(msg)` shows a message and returns `undefined`; `confirm(msg)` returns
`true` or `false`; `prompt(msg, default)` returns the typed **string**, or
`null` if cancelled. All three are modal, blocking and unstylable.

### 23. What does `preventDefault()` do?

Cancels the browser's default action for that event — submitting a form,
following a link, scrolling on an arrow key, showing the context menu. It does
**not** stop the event bubbling; that is `stopPropagation()`.

### 24. Distinguish `e.target` from `e.currentTarget`.

`e.target` is the element the event **originated on**; `e.currentTarget` is
the element the **listener is attached to**. Click a `<span>` inside a
`<button>` carrying the handler and `target` is the span, `currentTarget` the
button. Event delegation relies on the difference.

### 25. Why is client-side validation not security?

Because it runs on the attacker's machine. Anyone can disable JavaScript, edit
the DOM in dev tools, or send the HTTP request directly with `curl` and never
load your page at all. It is a **convenience for honest users**; the server
must validate every field again.

### 26. What is JSON, and who devised it?

JavaScript Object Notation — a lightweight, text-based data-interchange
format, a subset of JavaScript's object literal syntax but language
independent. Devised by **Douglas Crockford** around 2001; standardised as
ECMA-404 and RFC 8259.

### 27. List the JSON data types.

Six: **string** (double-quoted only), **number**, **boolean** (`true` /
`false`), **null**, **object**, **array**. There is no date type, no
`undefined`, and no function.

### 28. Give three things valid in a JavaScript object literal but invalid in JSON.

Unquoted keys (`{name: 1}`); single-quoted strings (`'text'`); a trailing
comma (`[1, 2,]`). Also acceptable: comments, `undefined`, `NaN`, `Infinity`,
functions, and hex or leading-zero numbers.

### 29. Why must `JSON.parse` be wrapped in `try/catch`?

It throws a `SyntaxError` on malformed input, and input from a network, a
file or `localStorage` can always be malformed. An unguarded call turns bad
data into an uncaught exception that kills the rest of the script.

### 30. Distinguish `.attr()` from `.prop()` in jQuery.

`.attr()` reads the HTML **attribute** — the value written in the markup,
which is the *initial* state. `.prop()` reads the DOM **property** — the
*current* state. After the user unticks a checkbox, `attr("checked")` still
returns `"checked"` while `prop("checked")` returns `false`. Use `.prop()` for
`checked`, `selected` and `disabled`.

### 31. What is method chaining in jQuery?

Almost every jQuery **setter** returns the same jQuery object, so calls can be
strung together: `$("#m").addClass("ok").text("Saved").fadeIn(300);`.
**Getters break the chain** — `.text()` with no argument returns a string, and
a string has no `.css()`.

### 32. Why does `fetch` not reject on a 404?

Because a 404 is a **successful HTTP transaction** that returned an error
status. `fetch` rejects only on a *network* failure — DNS, offline, CORS. You
must check `res.ok` yourself before calling `.json()`.

---

## Section B — Five-mark questions

### 1. Explain the structure of an HTML document with an example.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Student Profile</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header><h1>Asha Kumari</h1></header>
  <main>
    <p>B.Sc. Data Science, Semester III.</p>
  </main>
  <footer><p>&copy; 2026</p></footer>
  <script src="app.js" defer></script>
</body>
</html>
```

| Part | Purpose |
|---|---|
| `<!DOCTYPE html>` | Standards mode — not a tag |
| `<html lang="en">` | Root; `lang` helps screen readers and translation |
| `<head>` | Metadata — **not rendered** |
| `<meta charset="UTF-8">` | Character encoding; **must come first** in `<head>` |
| `<meta name="viewport">` | Required for responsive layout on phones |
| `<title>` | Tab caption, bookmark name, search result heading |
| `<body>` | Everything the user sees |
| `<script defer>` | Loads in parallel, runs after parsing |

The `charset` meta must be within the first 1024 bytes; otherwise the browser
may have already begun decoding with the wrong encoding and mis-render
non-ASCII text.

### 2. Explain the four CSS combinators with examples.

| Combinator | Symbol | Selects |
|---|:---:|---|
| Descendant | space | Any depth inside |
| Child | `>` | **Direct** children only |
| Adjacent sibling | `+` | The **immediately** following sibling |
| General sibling | `~` | **All** following siblings |

```html
<div>
  <p>A</p>
  <section><p>B</p></section>
</div>
<h1>Title</h1>
<p>C</p>
<p>D</p>
```

| Selector | Matches | Why |
|---|---|---|
| `div p` | A, B | Any `p` inside the div |
| `div > p` | A | B's parent is `section` |
| `h1 + p` | C | The next sibling |
| `h1 ~ p` | C, D | All later siblings |

Siblings must share a parent, and `+` and `~` look only **forwards** — there
is no "previous sibling" combinator.

### 3. Explain the CSS box model and compute a total width.

Every element is four nested rectangles: **content**, **padding**, **border**,
**margin**. Padding sits inside the background; margin is transparent and
outside it.

```css
div { width: 300px; padding: 20px; border: 5px solid; margin: 10px; }
```

Under the default `box-sizing: content-box`:

```
border-box width = 5 + 20 + 300 + 20 + 5 = 350px
space occupied   = 10 + 350 + 10        = 370px
```

Under `box-sizing: border-box`, `width: 300px` means the **border box** is
300px, so the content shrinks to 300 − 20 − 20 − 5 − 5 = **250px** and the
space occupied is 320px. Because content-box arithmetic is so error-prone,
virtually every real stylesheet begins:

```css
*, *::before, *::after { box-sizing: border-box; }
```

Note also that adjacent **vertical margins collapse** to the larger of the
two, not their sum: a 30px bottom margin above a 20px top margin gives a 30px
gap.

### 4. Explain CSS positioning with all five values.

| Value | Positioned relative to | Space reserved in flow |
|---|---|---|
| `static` | Nothing — default | Yes |
| `relative` | Its **own** normal position | **Yes** |
| `absolute` | Nearest **positioned ancestor** | **No** |
| `fixed` | The **viewport** | No |
| `sticky` | Flow, then viewport past a threshold | Yes |

`top`, `right`, `bottom`, `left` and `z-index` apply only to non-`static`
elements — setting `left: 20px` on a static element does nothing.

The pattern to memorise is the relative/absolute pairing:

```css
.card      { position: relative; }               /* the anchor */
.card .tag { position: absolute; top: 8px; right: 8px; }
```

Without `position: relative` on `.card`, the tag positions itself against the
page, and every "why is my badge in the corner of the screen" bug is this.

`z-index` stacks positioned elements, but only compares elements within the
same **stacking context**, which is why a `z-index: 9999` sometimes still
loses to a lower value elsewhere.

### 5. Explain specificity and resolve this conflict.

```html
<p id="intro" class="lead">Hello</p>
```
```css
p      { color: black; }
.lead  { color: blue;  }
#intro { color: green; }
p.lead { color: red;   }
```

Count each selector as `(a, b, c)` — IDs, then classes/attributes/pseudo-
classes, then elements/pseudo-elements — and compare **left to right**:

| Selector | (a, b, c) |
|---|---|
| `p` | (0, 0, 1) |
| `.lead` | (0, 1, 0) |
| `#intro` | **(1, 0, 0)** |
| `p.lead` | (0, 1, 1) |

`#intro` is the only selector with an ID, and `a` is compared first, so the
text is **green**. Source order is irrelevant here because there is no tie.

The full cascade order is `!important` first, then specificity, then source
order. The common exam shorthand of "IDs = 100, classes = 10, elements = 1" is
a useful approximation but technically wrong: eleven class selectors do not
beat one ID.

Inline `style=` behaves as if higher than any ID selector, which is why
inline styles are so hard to override and are best avoided.

### 6. Explain float, the collapsing-parent problem, and `clear`.

`float: left | right` pulls an element to one side of its container and lets
subsequent inline content wrap around it. It was designed for images in text.

```css
img.left { float: left; margin: 0 15px 10px 0; }
```

A floated element is taken out of normal flow, so **its parent computes a
height of zero** and any background or border on the parent collapses to
nothing. Three fixes:

```css
.parent { overflow: auto; }                  /* old side-effect hack */
.parent { display: flow-root; }              /* modern and explicit */
.parent::after { content: ""; display: block; clear: both; }  /* clearfix */
```

`clear: left | right | both` on a **later** element pushes it below the
floats rather than beside them.

For page layout, use **Flexbox** (one dimension) or **Grid** (two). Float was
used for layout for fifteen years only because nothing better existed.

### 7. Explain string manipulation methods with examples.

Strings are **immutable** — every method returns a new string.

```js
const s = "Data Science";
s.length              // 12
s.toUpperCase()       // "DATA SCIENCE"
s.indexOf("Science")  // 5      (-1 when absent)
s.includes("Sci")     // true
s.slice(0, 4)         // "Data"
s.slice(-7)           // "Science"    — negative counts from the end
s.replace("Data","Web")   // "Web Science"  — FIRST match only
s.replaceAll("a","@")     // "D@t@ Science"
s.split(" ")          // ["Data", "Science"]
"  hi ".trim()        // "hi"
"5".padStart(3,"0")   // "005"
[...s].reverse().join("")   // "ecneicS ataD"
```

`slice` accepts negative indices; `substring` clamps them to 0 and silently
**swaps** its arguments if `start > end`, which hides bugs. Use `slice`.
`substr` is deprecated.

Template literals are preferred to `+` concatenation:

```js
`${name} scored ${marks}%`
```

### 8. Explain array methods, distinguishing mutating from non-mutating.

**Mutating** — they change the original: `push`, `pop`, `shift`, `unshift`,
`splice`, `sort`, `reverse`, `fill`.

**Non-mutating** — they return something new: `slice`, `concat`, `join`,
`map`, `filter`, `reduce`, `find`, `some`, `every`, `flat`, `flatMap`, `at`.

```js
const marks = [72, 45, 91, 66, 38];
marks.map(m => m + 5)              // [77, 50, 96, 71, 43]
marks.filter(m => m >= 50)         // [72, 91, 66]
marks.reduce((s, m) => s + m, 0)   // 312
marks.find(m => m < 50)            // 45
marks.some(m => m > 90)            // true
marks.every(m => m > 30)           // true
[...marks].sort((a, b) => b - a)   // [91,72,66,45,38] — copy first
```

`reduce` needs an initial value; without one it uses the first element as the
seed and throws on an empty array.

The chain `filter → sort → map` is the shape of most real array code, and is
exactly what Course 9's Pandas expresses as `df[df.mark >= 50]`.

### 9. Explain exception handling in JavaScript.

```js
try {
  const data = JSON.parse(input);
  if (!data.name) throw new Error("name is required");
  process(data);
} catch (err) {
  console.error(err.name, err.message);
} finally {
  cleanup();               // runs whether or not an exception occurred
}
```

Built-in types: `Error`, `SyntaxError`, `TypeError`, `ReferenceError`,
`RangeError`, `URIError`. Custom errors extend `Error`:

```js
class ValidationError extends Error {
  constructor(field, msg) { super(msg); this.name = "ValidationError"; this.field = field; }
}
```

Three points that earn marks:

- **Re-throw what you cannot handle.** A `catch` that swallows everything turns
  a crash into a silently wrong answer.
- **Never `return` from `finally`** — it discards the `try`'s return value and
  any pending exception.
- **`try/catch` does not catch asynchronous callbacks.** The `try` block has
  already finished by the time a `setTimeout` callback runs; put the `try`
  inside the callback, or use `async/await`.

### 10. Explain event bubbling, capturing and delegation.

An event travels **down** from `window` to the target (capture phase), then
back **up** (bubble phase). Handlers run in the bubble phase unless registered
with `{ capture: true }`.

```
capture ↓   window → document → body → div → button
target  ●                                     button
bubble  ↑   button → div → body → document → window
```

**Delegation** exploits bubbling: attach one listener to a parent and identify
the real target inside it.

```js
document.getElementById("table").addEventListener("click", e => {
  const btn = e.target.closest("button.delete");
  if (!btn) return;
  btn.closest("tr").remove();
});
```

Two advantages: one listener instead of hundreds, and **elements added later
work with no extra wiring** — which matters because AJAX-loaded rows are added
after page load. `e.stopPropagation()` halts the journey; `e.preventDefault()`
cancels the browser's default action instead.

### 11. Explain the three dialog boxes and their limitations.

```js
alert("Saved");                            // → undefined
if (confirm("Delete?")) remove();          // → true / false
const n = prompt("Name?", "Student");      // → string, or null on Cancel
```

`prompt` returns `null` for **Cancel** and `""` for **OK with nothing typed** —
both falsy, so `if (!n)` cannot distinguish them; test `n === null`. It always
returns a **string**, so wrap in `Number()` for numeric input.

All three are **modal and blocking** — they freeze the page including timers
and animations — **cannot be styled**, and are suppressed by browsers after
repeated use or in background tabs. HTML5's `<dialog>` replaces them: stylable,
non-blocking, closes on Escape, and traps focus correctly.

```js
dlg.showModal();
dlg.addEventListener("close", () => { if (dlg.returnValue === "ok") remove(); },
                     { once: true });
```

The `{ once: true }` matters — without it each call adds another listener and
the second deletion fires twice.

### 12. Compare JSON and XML with examples.

```json
{"student": {"roll": 23, "name": "Asha", "subjects": ["DS", "Stats"]}}
```
```xml
<student>
  <roll>23</roll><name>Asha</name>
  <subjects><subject>DS</subject><subject>Stats</subject></subjects>
</student>
```

67 characters against 148.

| | JSON | XML |
|---|---|---|
| Verbosity | Compact | ~2× the bytes |
| Data types | 6 native | Everything is text |
| Arrays | Native | By convention only |
| Parsing in JS | Built in, fast | Slow, clumsy DOM API |
| Attributes, comments, namespaces | No | Yes |
| Schema validation | JSON Schema, optional | XSD/DTD, mature |
| Mixed content | Poor | Designed for it |

**XML remains right** for documents with mixed content, where schema
validation is contractual, and in established ecosystems — SOAP, RSS, SVG,
`.docx`, `.xlsx`. **JSON is right** for essentially every web API written
since 2010, for configuration, and for document databases (Course 10).

### 13. Explain jQuery selectors and filters.

Any CSS selector works, plus jQuery's own filters:

```js
$("p")  $("#main")  $(".card")  $("ul > li")  $("input[type='text']")
$("tr:even")  $("li:first")  $("p:contains('marks')")  $("input:checked")
```

| Filter | Selects |
|---|---|
| `:first` / `:last` | First / last of the whole set |
| `:even` / `:odd` | **0-indexed** |
| `:eq(n)` / `:gt(n)` / `:lt(n)` | By index |
| `:contains('x')` | Containing that text |
| `:has(sel)` | Containing a matching descendant |
| `:hidden` / `:visible` | By rendered visibility |
| `:input`, `:checkbox`, `:checked`, `:disabled` | Form controls and state |

**`:even` is 0-indexed and matches the 1st, 3rd, 5th** rows; CSS's
`:nth-child(even)` is 1-indexed and matches the 2nd, 4th, 6th. Swapping them
inverts your zebra stripes.

jQuery's filters are **not CSS**, so `querySelectorAll` cannot use them and
jQuery must filter them itself, slowly. Prefer `.first()` and `.eq(n)`.

Traversal: `.parent()`, `.children()`, `.find()`, `.closest()`, `.siblings()`,
`.next()`, `.prev()`, `.filter()`, `.not()`, `.eq()`. Note `.find()` searches
**descendants** while `.filter()` narrows the **current set**.

### 14. Explain jQuery effects and animations.

```js
$("#b").hide(400);   $("#b").show("slow");    $("#b").toggle();
$("#b").fadeIn(300); $("#b").fadeOut(300);    $("#b").fadeTo(400, 0.5);
$("#p").slideDown(300); $("#p").slideUp(300); $("#p").slideToggle();
$("#b").animate({ left: "250px", opacity: 0.5 }, 500, function () {
  $(this).addClass("done");            // callback on completion
});
$("#b").delay(500).fadeIn(300);
$("#b").stop(true, true);              // clear the queue, jump to the end
```

Durations: a number in milliseconds, or `"slow"` (600 ms) / `"fast"` (200 ms).

Effects **queue per element**, each waiting for the previous to finish. That
is why they chain so readably — and why a hover effect without `.stop()`
keeps animating long after the pointer has left, because every hover queued
another animation.

`.animate()` handles **numeric** properties only; it cannot animate colours
without a plugin, nor `display`.

For anything a stylesheet can express, a CSS transition is better: it runs on
the compositor rather than a JavaScript timer, so it stays smooth when the
main thread is busy, and it respects `prefers-reduced-motion`.

---

## Section C — Ten-mark questions

### 1. Design a complete student registration form and explain each element.

```html
<form id="reg" action="/register" method="post" novalidate>
  <fieldset>
    <legend>Personal details</legend>

    <label for="name">Full name *</label>
    <input type="text" id="name" name="name" required minlength="3" maxlength="50"
           autocomplete="name" aria-describedby="name-error">
    <span id="name-error" class="error" role="alert"></span>

    <label for="email">Email *</label>
    <input type="email" id="email" name="email" required
           autocomplete="email" aria-describedby="email-error">
    <span id="email-error" class="error" role="alert"></span>

    <label for="mobile">Mobile *</label>
    <input type="tel" id="mobile" name="mobile" required
           pattern="[6-9][0-9]{9}" title="10-digit Indian mobile number">

    <label for="dob">Date of birth</label>
    <input type="date" id="dob" name="dob" max="2010-12-31">

    <fieldset>
      <legend>Gender</legend>
      <input type="radio" id="gf" name="gender" value="F" required>
      <label for="gf">Female</label>
      <input type="radio" id="gm" name="gender" value="M">
      <label for="gm">Male</label>
      <input type="radio" id="go" name="gender" value="O">
      <label for="go">Other</label>
    </fieldset>
  </fieldset>

  <fieldset>
    <legend>Course</legend>

    <label for="course">Programme *</label>
    <select id="course" name="course" required>
      <option value="">— select —</option>
      <optgroup label="Science">
        <option value="ds">B.Sc. Data Science</option>
        <option value="st">B.Sc. Statistics</option>
      </optgroup>
    </select>

    <fieldset>
      <legend>Electives</legend>
      <input type="checkbox" id="e1" name="electives" value="ml">
      <label for="e1">Machine Learning</label>
      <input type="checkbox" id="e2" name="electives" value="viz">
      <label for="e2">Data Visualization</label>
    </fieldset>

    <label for="photo">Photograph</label>
    <input type="file" id="photo" name="photo" accept="image/*">

    <label for="about">About yourself</label>
    <textarea id="about" name="about" rows="4" maxlength="200"></textarea>
  </fieldset>

  <input type="checkbox" id="terms" name="terms" required>
  <label for="terms">I accept the terms *</label>

  <button type="submit">Register</button>
  <button type="reset">Clear</button>
</form>
```

| Element | Why it is there |
|---|---|
| `action` | Where the data is sent |
| `method="post"` | Data goes in the body, not the URL — required for files and passwords |
| `novalidate` | Suppresses the browser's own messages so JavaScript can show its own |
| `<fieldset>`/`<legend>` | Groups related controls; screen readers announce the legend with each field |
| `<label for>` | Ties the label to the input by **id**; clicking the label focuses the field |
| `name` | The key the server receives — **without it the field is not submitted** |
| `required`, `minlength`, `pattern` | Free constraint validation |
| `autocomplete` | Lets the browser fill known values |
| `aria-describedby` | Links the field to its error message for screen readers |
| `<optgroup>` | Groups options within a select |
| Same `name` on radios | What makes them **mutually exclusive** — different names give three independent buttons |
| `type="file"` | Also requires `enctype="multipart/form-data"` on the form for a real upload |

**GET vs POST.** GET appends data to the URL as a query string — visible,
bookmarkable, length-limited, cached, and therefore only for **safe, idempotent
retrieval** such as a search. POST puts data in the request body — not visible
in the URL, no practical length limit, not cached, and required for file
uploads and for anything that **changes server state**.

Two closing points that earn the last marks. Every field marked `required`
must **also** be checked on the server, since client-side validation is a
convenience, not a control. And every input needs a `<label>`: a placeholder
is not a label — it disappears when the user types, and screen readers treat
it inconsistently.

### 2. Explain the JavaScript event model exhaustively.

**Three ways to attach a handler:**

```html
<button onclick="save()">HTML attribute — avoid</button>
```
```js
btn.onclick = handler;                     // property: only ONE handler
btn.addEventListener("click", handler);    // preferred
btn.addEventListener("click", handler, { once: true, capture: false, passive: true });
btn.removeEventListener("click", handler); // needs the SAME function reference
```

`addEventListener` wins on three counts: multiple handlers on one element,
options, and behaviour kept out of the markup. `removeEventListener` fails
silently if given a different function object, so an inline arrow handler can
never be removed.

**The event object:**

| Property | Meaning |
|---|---|
| `type` | `"click"` |
| `target` | Where it originated |
| `currentTarget` | Where the listener is attached |
| `clientX/Y`, `pageX/Y`, `offsetX/Y` | Coordinates — viewport, document, element |
| `key`, `code`, `repeat` | Keyboard |
| `ctrlKey`, `shiftKey`, `altKey`, `metaKey` | Modifiers |
| `preventDefault()` | Cancel the default action |
| `stopPropagation()` | Stop the journey through the tree |

**Three phases** — capture down, target, bubble up — as diagrammed in
Section B question 10, with delegation as the practical payoff.

**`this` in handlers:** a `function` handler gets the element; an **arrow**
handler gets the enclosing scope's `this`, so it must use `e.currentTarget`.

**Event categories:** mouse (`click`, `dblclick`, `mousedown/up/move`,
`mouseenter/leave`, `mouseover/out`, `contextmenu`), keyboard (`keydown`,
`keyup`), form (`submit`, `change`, `input`, `focus`, `blur`), window
(`DOMContentLoaded`, `load`, `resize`, `scroll`), touch and clipboard.

Four pairs worth distinguishing:

| Pair | Difference |
|---|---|
| `mouseenter` / `mouseover` | `mouseover` bubbles and re-fires on children |
| `input` / `change` | `input` on every keystroke; `change` when committed |
| `DOMContentLoaded` / `load` | HTML parsed vs. images and stylesheets also loaded |
| `keydown` / `keyup` | Repeats while held and is cancellable vs. fires once, after |

Finally, listen for **`submit` on the form**, not `click` on the button:
pressing Enter in a text field submits without any click, and a `click`
handler misses it entirely.

### 3. Write a complete form-validation program and explain it.

```js
const CHECKS = [
  { id: "name",  test: v => v.trim().length >= 3,
    msg: "Name must be at least 3 characters" },
  { id: "email", test: v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()),
    msg: "Enter a valid email address" },
  { id: "mobile", test: v => /^[6-9]\d{9}$/.test(v.trim()),
    msg: "Enter a 10-digit Indian mobile number" },
  { id: "password", test: v => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/.test(v),
    msg: "8+ characters with upper, lower, digit and symbol" }
];

function validate(form) {
  const errors = {};
  for (const c of CHECKS) {
    const value = form.elements[c.id].value;
    if (!c.test(value)) errors[c.id] = c.msg;
  }
  if (form.elements.password.value !== form.elements.confirm.value)
    errors.confirm = "Passwords do not match";
  if (!form.elements.terms.checked)
    errors.terms = "You must accept the terms";
  return errors;
}

function setFieldError(input, message) {
  const box = document.getElementById(input.id + "-error");
  input.classList.toggle("is-invalid", Boolean(message));
  input.setAttribute("aria-invalid", message ? "true" : "false");
  if (box) box.textContent = message || "";      // textContent, never innerHTML
}

const form = document.getElementById("reg");

form.addEventListener("submit", function (e) {
  const errors = validate(this);
  for (const id of [...CHECKS.map(c => c.id), "confirm", "terms"])
    setFieldError(this.elements[id], errors[id] || "");
  if (Object.keys(errors).length) {
    e.preventDefault();
    this.querySelector(".is-invalid")?.focus();
  }
});

// live feedback, but only after the user has left the field once
for (const c of CHECKS) {
  const input = form.elements[c.id];
  let touched = false;
  const run = () => setFieldError(input, c.test(input.value) ? "" : c.msg);
  input.addEventListener("blur",  () => { touched = true; run(); });
  input.addEventListener("input", () => { if (touched) run(); });
}
```

**Why it is written this way.**

The checks are **data, not a wall of `if` statements**, so adding a field is
one line and the same array drives both submit-time and live validation.

Two rules cannot be expressed as a regex and so are written separately: the
password confirmation compares two fields, and the terms checkbox reads
`.checked`, not `.value`.

`e.preventDefault()` is what actually cancels the submission — returning
`false` works only for the obsolete `onsubmit=` attribute form.

Focus moves to the **first** invalid field, which is what makes the form
usable from the keyboard, and `role="alert"` on the error spans makes screen
readers announce the messages.

Validation runs on **blur first, then on every keystroke**. Validating from
the first character shows "invalid email" while the user is still typing the
first letter, which is hostile; once they have left the field and got it
wrong, live feedback helps them fix it.

The messages are written with `textContent`, so a value containing
`<img src=x onerror=…>` renders as text rather than executing.

And the closing point, which is worth marks in itself: **none of this is
security**. It is a convenience for honest users. Every one of these rules
must be enforced again on the server, because an attacker never runs your
JavaScript at all.
