# Unit 4 — Client-Side Scripting

**Syllabus topics:** Accessing HTML form elements using JavaScript object
model, basic data validations, data format validations, generating responsive
messages, opening windows using JavaScript, different kinds of dialog boxes,
accessing status bar using JavaScript, embedding basic animative features using
different keyboard and mouse events.

---

## 4.1 The DOM

### 🎯 The big idea

When a browser loads HTML it builds a **tree of objects** in memory. That tree
is the **DOM** — Document Object Model. JavaScript changes the page by changing
the tree; the browser re-renders automatically.

The HTML file is not the page. The DOM is the page. Editing the DOM in dev
tools does not change the file, and re-loading discards every change.

```html
<html>
  <body>
    <h1 id="t">Marks</h1>
    <p class="note">Semester III</p>
  </body>
</html>
```

```
document
└── html
    └── body
        ├── h1#t
        │   └── "Marks"                 (text node)
        └── p.note
            └── "Semester III"
```

### The browser object model

`window` is the global object. Everything else hangs off it.

| Object | Provides |
|---|---|
| `window` | The browser window; the global scope |
| `document` | The DOM tree — **part of the DOM, not the BOM** |
| `navigator` | Browser and platform information |
| `location` | The current URL |
| `history` | Session history — `back()`, `forward()`, `go(n)` |
| `screen` | Screen dimensions |

**DOM vs BOM** is an exam question: the **DOM** models the *document*; the
**BOM** models the *browser* — `window`, `navigator`, `location`, `history`,
`screen`. `document` is the bridge between them.

```js
location.href                 // full URL
location.hostname             // "nrstatlab.github.io"
location.search               // "?id=23"
location.reload();
location.href = "next.html";  // navigate

new URLSearchParams(location.search).get("id");   // "23"
```

## 4.2 Selecting elements

| Method | Returns | Live? |
|---|---|---|
| `getElementById(id)` | One element or `null` | — |
| `getElementsByTagName(t)` | HTMLCollection | **Live** |
| `getElementsByClassName(c)` | HTMLCollection | **Live** |
| `getElementsByName(n)` | NodeList | Live |
| `querySelector(sel)` | **First** match or `null` | — |
| `querySelectorAll(sel)` | NodeList | **Static** |

```js
document.getElementById("email");
document.querySelector("#email");
document.querySelector(".card .title");
document.querySelectorAll("input[type=checkbox]");
document.querySelectorAll("tbody tr:nth-child(even)");
```

### ⚠️ Live vs static collections

```js
const live   = document.getElementsByTagName("li");   // live
const static_= document.querySelectorAll("li");       // static snapshot
document.querySelector("ul").append(document.createElement("li"));
live.length;      // grew
static_.length;   // unchanged
```

A live collection updates itself as the DOM changes. Deleting from one while
looping over it skips elements — the classic bug:

```js
// WRONG — the collection shrinks under the loop
const items = document.getElementsByClassName("row");
for (let i = 0; i < items.length; i++) items[i].remove();

// RIGHT — take a static snapshot
document.querySelectorAll(".row").forEach(el => el.remove());
```

`querySelectorAll` returns a NodeList, which **has `forEach`** but not `map`,
`filter` or `reduce`. Spread it if you need those: `[...document.querySelectorAll("li")].map(…)`.

Use `querySelector`/`querySelectorAll` by default; use `getElementById` when you
have an id, because it is marginally faster and reads clearly.

## 4.3 Reading and changing elements

| Property | Gets/sets |
|---|---|
| `textContent` | All text, **tags escaped** — safe |
| `innerText` | Rendered text — respects CSS, slower |
| `innerHTML` | HTML markup — **parsed** |
| `outerHTML` | Including the element itself |
| `value` | Form control value |
| `className` / `classList` | Classes |
| `style` | Inline styles |
| `dataset` | `data-*` attributes |

```js
const h = document.getElementById("t");
h.textContent = "Semester III Marks";
h.style.color = "navy";
h.style.backgroundColor = "#eef";      // camelCase, not background-color
h.classList.add("highlight");
h.classList.remove("dim");
h.classList.toggle("open");
h.classList.contains("open");          // boolean
h.setAttribute("title", "click me");
h.getAttribute("title");
h.dataset.rollNo = "23";               // sets data-roll-no
```

### ⚠️ `innerHTML` and XSS

```js
const name = getUserInput();                 // e.g. "<img src=x onerror=alert(1)>"
el.innerHTML   = `Hello ${name}`;            // ← executes the attacker's code
el.textContent = `Hello ${name}`;            // ← displays it literally. Safe.
```

**Use `textContent` for text. Use `innerHTML` only for markup you wrote
yourself.** Inserting user input through `innerHTML` is **cross-site
scripting** (XSS), the most common web vulnerability there is.

`innerHTML` also destroys and rebuilds everything inside, losing event listeners
and any typed-in form values. `el.innerHTML += "x"` re-parses the entire subtree
and is both slow and destructive.

### Creating and moving nodes

```js
const li = document.createElement("li");
li.textContent = "New row";
li.className = "row";

list.append(li);                   // last child   (accepts text and multiple nodes)
list.prepend(li);                  // first child
li.before(other);  li.after(other);
list.appendChild(li);              // older API, nodes only
list.insertBefore(li, list.firstChild);
li.remove();                       // modern
li.replaceWith(newLi);
const clone = li.cloneNode(true);  // true = deep copy
```

### 💡 Batch DOM writes

Every insertion can force the browser to recalculate layout. Building 1000 rows
one at a time is measurably slow. Build them off-screen first:

```js
const frag = document.createDocumentFragment();
for (const s of students) {
  const tr = document.createElement("tr");
  tr.innerHTML = `<td>${s.roll}</td><td>${s.name}</td>`;
  frag.append(tr);
}
tbody.append(frag);                // ONE insertion into the live document
```

A `DocumentFragment` is a lightweight container that is not part of the
document, so nothing reflows until the single final `append`.

## 4.4 Accessing form elements

There are four routes, and the syllabus's phrase "JavaScript object model"
refers to the second.

```html
<form id="reg" name="reg">
  <input type="text"  name="username" id="username">
  <input type="email" name="email">
  <select name="course">
    <option value="ds">Data Science</option>
    <option value="st" selected>Statistics</option>
  </select>
  <input type="checkbox" name="terms">
  <input type="radio" name="gender" value="F">
  <input type="radio" name="gender" value="M">
</form>
```

```js
// 1. by id
document.getElementById("username").value;

// 2. the forms collection — the classic "JavaScript object model" route
document.forms["reg"].username.value;
document.forms[0].elements["email"].value;

// 3. the form's elements collection
const f = document.getElementById("reg");
f.elements.username.value;

// 4. querySelector
document.querySelector("#reg [name=email]").value;
```

### Reading each control type

| Control | Read with |
|---|---|
| text, email, password, number, date | `.value` (**always a string**) |
| textarea | `.value` |
| checkbox | `.checked` — boolean |
| radio group | `f.elements.gender.value` — the checked one |
| select (single) | `.value`, or `.options[.selectedIndex].text` for the label |
| select (multiple) | `[...sel.selectedOptions].map(o => o.value)` |
| file | `.files` — a FileList |

```js
f.elements.terms.checked;                       // true / false
f.elements.gender.value;                        // "F", or "" if none checked
f.elements.course.value;                        // "st"
f.elements.course.options[f.elements.course.selectedIndex].text;  // "Statistics"
Number(f.elements.age.value);                   // convert! .value is a string
Object.fromEntries(new FormData(f));            // every field as an object
```

### ⚠️ `.value` is always a string

```js
const age = document.getElementById("age").value;   // "25", not 25
age + 1        // "251"   ← string concatenation
Number(age) + 1// 26
```

Even `<input type="number">` gives a string. This is the most common form bug
there is. `valueAsNumber` exists for number and date inputs and gives `NaN`
when empty, which is often more convenient than `Number("")` giving 0.

Radio buttons need `f.elements.name.value`, not `.value` on an individual
button — a single radio's `.value` is its `value` attribute whether or not it
is checked.

## 4.5 Events

### Three ways to attach a handler

```html
<button onclick="save()">HTML attribute — avoid</button>
```
```js
btn.onclick = handler;                     // property — only ONE handler
btn.addEventListener("click", handler);    // ← use this
btn.addEventListener("click", handler2);   // both run
btn.removeEventListener("click", handler); // needs the SAME function reference
```

`addEventListener` is correct because it allows multiple handlers, supports
options (`once`, `capture`, `passive`), and keeps behaviour out of the markup.

`removeEventListener` fails silently if you pass a different function object —
an inline arrow can never be removed:

```js
btn.addEventListener("click", () => f());   // impossible to remove
btn.addEventListener("click", f);           // removable
btn.addEventListener("click", f, { once: true });  // auto-removes after one fire
```

### Common events

| Category | Events |
|---|---|
| Mouse | `click`, `dblclick`, `mousedown`, `mouseup`, `mousemove`, `mouseenter`, `mouseleave`, `mouseover`, `mouseout`, `contextmenu` |
| Keyboard | `keydown`, `keyup`, (`keypress` — deprecated) |
| Form | `submit`, `reset`, `change`, `input`, `focus`, `blur`, `invalid` |
| Window | `load`, `DOMContentLoaded`, `resize`, `scroll`, `beforeunload` |
| Touch | `touchstart`, `touchmove`, `touchend` |
| Clipboard | `copy`, `cut`, `paste` |

### ⚠️ Four pairs students confuse

| Pair | Difference |
|---|---|
| `mouseenter` / `mouseover` | `mouseover` **bubbles** and re-fires when moving onto a child; `mouseenter` does not |
| `change` / `input` | `input` fires on **every keystroke**; `change` fires when the value is committed (blur, or selection) |
| `load` / `DOMContentLoaded` | `DOMContentLoaded` fires when HTML is parsed; `load` waits for images, stylesheets and fonts |
| `keydown` / `keyup` | `keydown` repeats while held and can be prevented; `keyup` fires once, after the change |

For live search and character counters, use `input`. For "validate when they
leave the field", use `change` or `blur`.

### The event object

```js
el.addEventListener("click", function (e) {
  e.type            // "click"
  e.target          // what was actually clicked (may be a descendant)
  e.currentTarget   // what the listener is attached to  — same as `this` here
  e.clientX, e.clientY   // viewport coordinates
  e.pageX,   e.pageY     // document coordinates, including scroll
  e.offsetX, e.offsetY   // relative to the target
  e.button          // 0 left, 1 middle, 2 right
  e.shiftKey, e.ctrlKey, e.altKey, e.metaKey
  e.preventDefault();    // cancel the browser's default action
  e.stopPropagation();   // stop bubbling to ancestors
});
```

**`target` vs `currentTarget`** is a five-mark answer. Click a `<span>` inside a
`<button>` that carries the listener: `target` is the span, `currentTarget` is
the button.

### Bubbling, capturing and delegation

An event travels **down** from `window` to the target (capture phase), then
**up** again (bubble phase). Handlers run in the bubble phase unless you pass
`{ capture: true }`.

```
capture ↓   window → document → body → div → button
target  ●                                     button
bubble  ↑   button → div → body → document → window
```

**Event delegation** exploits bubbling: one listener on a parent handles all its
children, including ones added later.

```js
document.getElementById("marks-table").addEventListener("click", e => {
  const btn = e.target.closest("button.delete");
  if (!btn) return;                       // click was somewhere else
  btn.closest("tr").remove();
});
```

One listener instead of a hundred, and rows added after page load work with no
extra wiring. `closest(selector)` walks up from the target to the nearest
matching ancestor — the standard delegation idiom.

### `this` in handlers

```js
btn.addEventListener("click", function () { this.classList.add("on"); });  // this = btn
btn.addEventListener("click", () => { this.classList.add("on"); });        // this = OUTER scope — breaks
btn.addEventListener("click", e => { e.currentTarget.classList.add("on"); });// correct with arrows
```

If you use arrow handlers — and you should, for consistency — reach the element
through `e.currentTarget`, never `this`.

## 4.6 Basic data validation

**Basic validation** asks "is anything there, and is it in range?" Format
validation (§4.7) asks "does it look right?"

```js
function validateBasic(form) {
  const errors = [];
  const name = form.elements.username.value.trim();
  const age  = form.elements.age.valueAsNumber;

  if (name === "")                errors.push(["username", "Name is required"]);
  else if (name.length < 3)       errors.push(["username", "At least 3 characters"]);
  else if (name.length > 50)      errors.push(["username", "At most 50 characters"]);

  if (Number.isNaN(age))          errors.push(["age", "Age is required"]);
  else if (!Number.isInteger(age))errors.push(["age", "Age must be a whole number"]);
  else if (age < 16 || age > 100) errors.push(["age", "Age must be between 16 and 100"]);

  if (!form.elements.terms.checked) errors.push(["terms", "You must accept the terms"]);
  if (form.elements.gender.value === "") errors.push(["gender", "Select a gender"]);
  return errors;
}
```

### ⚠️ Always `.trim()` before testing emptiness

`"   "` is not `""`, so `value === ""` passes a field containing only spaces.
`value.trim() === ""` catches it. Store the trimmed value too.

### Wiring it to the form

```js
document.getElementById("reg").addEventListener("submit", function (e) {
  const errors = validateBasic(this);
  if (errors.length) {
    e.preventDefault();                 // ← stop the submission
    showErrors(errors);
  }
});
```

Listen for **`submit` on the form**, not `click` on the button. Pressing Enter
in a text field submits without any click, and a `click` handler would miss it
entirely. `e.preventDefault()` is what actually cancels the submission.

## 4.7 Data format validation

```js
const RULES = {
  email:    { re: /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/, msg: "Enter a valid email address" },
  phone:    { re: /^[6-9]\d{9}$/,                  msg: "Enter a 10-digit Indian mobile number" },
  pincode:  { re: /^[1-9]\d{5}$/,                  msg: "Enter a valid 6-digit PIN code" },
  rollno:   { re: /^\d{2}[A-Z]{3}\d{4}$/,          msg: "Format: 23DSC0145" },
  password: { re: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/,
              msg: "8+ chars with upper, lower, digit and symbol" },
  date:     { re: /^\d{4}-\d{2}-\d{2}$/,           msg: "Use YYYY-MM-DD" }
};

function checkFormat(kind, value) {
  const r = RULES[kind];
  return r.re.test(value) ? null : r.msg;
}
```

### Validation a regex cannot do

A pattern checks **shape**, not **meaning**. These need code:

```js
// 1. Confirm password matches
if (pw.value !== pw2.value) errors.push(["pw2", "Passwords do not match"]);

// 2. A real calendar date — 2026-02-30 matches the regex but does not exist
function isRealDate(s) {
  const [y, m, d] = s.split("-").map(Number);
  const dt = new Date(y, m - 1, d);
  return dt.getFullYear() === y && dt.getMonth() === m - 1 && dt.getDate() === d;
}

// 3. Age derived from a date of birth
function ageOn(dobStr, on = new Date()) {
  const dob = new Date(dobStr);
  let a = on.getFullYear() - dob.getFullYear();
  const m = on.getMonth() - dob.getMonth();
  if (m < 0 || (m === 0 && on.getDate() < dob.getDate())) a--;
  return a;
}

// 4. End after start
if (new Date(end.value) <= new Date(start.value))
  errors.push(["end", "End date must be after the start date"]);
```

The date check works because `new Date(2026, 1, 30)` silently rolls over to
2 March — so comparing the components back tells you whether the date was real.

### HTML5 built-in validation

The browser will do a great deal for free:

```html
<input type="email" required>
<input type="text" required minlength="3" maxlength="50">
<input type="number" min="16" max="100" step="1" required>
<input type="text" pattern="[6-9][0-9]{9}" title="10-digit mobile number">
<input type="url"> <input type="tel"> <input type="date">
<form novalidate>   <!-- disables it, so your JS can take over messaging -->
```

The Constraint Validation API exposes it to JavaScript:

```js
input.checkValidity();          // boolean, fires an `invalid` event if false
input.validity.valueMissing;    // which constraint failed
input.validity.typeMismatch;
input.validity.patternMismatch;
input.validity.rangeUnderflow;
input.validationMessage;        // the browser's own localised message
input.setCustomValidity("Roll number already registered");  // "" clears it
```

Use HTML5 attributes **and** JavaScript: the attributes give free accessible
behaviour, and JavaScript gives you control over the messages.

### ⚠️ Client-side validation is never security

Everything in this section is a **convenience for honest users**. It is
trivially bypassed — disable JavaScript, edit the DOM, or send the request
with `curl` and never load the page at all.

**The server must validate every field again.** Anything else means a database
full of whatever an attacker chose to send. This point is worth marks and is
worth far more than marks.

## 4.8 Generating responsive messages

"Responsive" here means *the page responds to what the user does* — inline,
immediate, next to the field.

```js
function setFieldError(input, message) {
  const box = document.getElementById(input.id + "-error");
  input.classList.toggle("is-invalid", Boolean(message));
  input.setAttribute("aria-invalid", message ? "true" : "false");
  box.textContent = message || "";       // textContent, not innerHTML
}
```
```html
<label for="email">Email</label>
<input id="email" name="email" type="email" aria-describedby="email-error" required>
<span id="email-error" class="error" role="alert"></span>
```
```css
.error       { color: #c92a2a; font-size: .85rem; display: block; min-height: 1.2em; }
.is-invalid  { border-color: #c92a2a; }
```

Four details separate a good implementation from a bad one:

- **`min-height` on the error span** so the layout does not jump when a message
  appears
- **`role="alert"`** so screen readers announce it
- **`aria-describedby`** linking the field to its message
- **`textContent`**, not `innerHTML` — the message may contain user input

### Live feedback, without nagging

```js
const email = document.getElementById("email");
let touched = false;

email.addEventListener("blur",  () => { touched = true; validateEmail(); });
email.addEventListener("input", () => { if (touched) validateEmail(); });

function validateEmail() {
  setFieldError(email, checkFormat("email", email.value.trim()));
}
```

Validate on **blur first, then on every keystroke**. Validating from the first
character shows "invalid email" while the user is still typing the first
letter, which is hostile. Once they have left the field and got it wrong,
live feedback helps them fix it.

### A live character counter

```js
const bio = document.getElementById("bio"), out = document.getElementById("bio-count");
const MAX = 200;
bio.addEventListener("input", () => {
  const left = MAX - bio.value.length;
  out.textContent = `${left} characters remaining`;
  out.classList.toggle("warn", left < 20);
});
```

## 4.9 Opening windows

```js
const w = window.open(
  "report.html",                     // URL ("" = blank)
  "reportWin",                       // window name — reused if it exists
  "width=600,height=400,left=100,top=100,resizable=yes,scrollbars=yes"
);

if (!w) alert("Please allow pop-ups for this site.");   // ALWAYS check

w.document.write("<h1>Generated</h1>");   // only for same-origin
w.focus();
w.resizeTo(800, 600);
w.moveTo(50, 50);
w.print();
w.close();                                 // only closes what you opened

window.opener                              // the child's reference to the parent
```

Two rules. **`window.open` returns `null` when blocked**, so dereferencing it
without checking throws. And **pop-up blockers only allow it during a user
gesture** — inside a click handler it works; inside `setTimeout` or on page
load it is blocked.

```js
window.open("x.html");                                   // blocked at load
btn.onclick = () => window.open("x.html");               // allowed
setTimeout(() => window.open("x.html"), 2000);           // blocked
```

Also add `rel="noopener"` to `target="_blank"` links, or open with
`window.open(url, "_blank", "noopener")` — otherwise the opened page can
manipulate `window.opener.location` and redirect your page to a phishing site.

Modern practice avoids pop-ups almost entirely: use a modal `<dialog>` in the
page instead. The syllabus examines them; industry does not use them.

## 4.10 Dialog boxes

The syllabus's "different kinds of dialog boxes" means these three.

| Dialog | Call | Returns | Buttons |
|---|---|---|---|
| **Alert** | `alert(msg)` | `undefined` | OK |
| **Confirm** | `confirm(msg)` | `true` / `false` | OK, Cancel |
| **Prompt** | `prompt(msg, default)` | **string**, or `null` on cancel | OK, Cancel |

```js
alert("Registration successful");

if (confirm("Delete this record permanently?")) deleteRecord();

const name = prompt("Enter your name:", "Student");
if (name === null)        console.log("cancelled");
else if (name.trim() === "") console.log("submitted empty");
else                      console.log(`Hello, ${name}`);
```

### ⚠️ Distinguish cancel from empty

`prompt` returns `null` for **Cancel** and `""` for **OK with nothing typed**.
Both are falsy, so `if (!name)` cannot tell them apart. Test `name === null`
explicitly when it matters.

`prompt` also always returns a **string**: `Number(prompt("Age?"))`.

### The three limitations

All three dialogs are **modal and blocking** — they freeze the page, including
timers and animations, until dismissed. They **cannot be styled**. And browsers
suppress them after repeated use, or in background tabs.

That is why real applications build their own, and why HTML5 added `<dialog>`:

```html
<dialog id="confirmBox">
  <form method="dialog">
    <p>Delete this record permanently?</p>
    <button value="cancel">Cancel</button>
    <button value="ok">Delete</button>
  </form>
</dialog>
```
```js
const dlg = document.getElementById("confirmBox");
dlg.showModal();                                    // .show() for non-modal
dlg.addEventListener("close", () => {
  if (dlg.returnValue === "ok") deleteRecord();
});
```

`<dialog>` is stylable, non-blocking, closes on Escape, and traps focus
correctly for keyboard and screen-reader users. `method="dialog"` on the inner
form closes it and sets `returnValue` to the clicked button's `value`.

## 4.11 The status bar

The syllabus asks for "accessing status bar using JavaScript". The honest
answer has two halves, and giving both earns the mark.

**What was taught:**

```js
window.status = "Loading data…";                 // the classic technique
window.defaultStatus = "Ready";
link.onmouseover = function () { window.status = "Go to results"; return true; };
```

**What actually happens now:** nothing. `window.status` is a settable property
that every modern browser **ignores**. It was disabled because it was used for
phishing — a link to `evil.com` could display "https://yourbank.com" in the
status bar. Firefox removed it in 2010; Chrome, Edge and Safari followed.
It remains in the HTML specification only as a no-op, kept so old pages do not
break.

```js
window.status = "anything";
console.log(window.status);    // "" in a modern browser — the write was discarded
```

**What to do instead** — a status area you control inside the page:

```html
<div id="status" role="status" aria-live="polite"></div>
```
```js
const setStatus = msg => { document.getElementById("status").textContent = msg; };
setStatus("Loading student records…");
```

`aria-live="polite"` makes a screen reader announce changes without
interrupting, so this is more accessible than the status bar ever was.

## 4.12 Keyboard events

```js
document.addEventListener("keydown", e => {
  e.key        // "a", "A", "Enter", "Escape", "ArrowLeft", " "   ← use this
  e.code       // "KeyA"  — physical key, layout-independent
  e.repeat     // true while held down
  e.ctrlKey, e.shiftKey, e.altKey, e.metaKey

  if (e.key === "Escape") closeModal();
  if (e.key === "Enter" && e.ctrlKey) submitForm();
  if (e.key === "s" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); save(); }
});
```

**Use `e.key`.** `e.keyCode` and `e.which` are deprecated, and `e.charCode`
even more so. `e.key` gives the character or a descriptive name and handles
non-English layouts.

Note `e.key` for the space bar is `" "` — a single space, not `"Space"`. That
is `e.code`.

Restricting an input to digits:

```js
input.addEventListener("keydown", e => {
  const allowed = ["Backspace","Delete","Tab","Escape","Enter","ArrowLeft","ArrowRight","Home","End"];
  if (allowed.includes(e.key) || e.ctrlKey || e.metaKey) return;
  if (!/^\d$/.test(e.key)) e.preventDefault();
});
```

The `allowed` list is not optional. Blocking everything non-numeric without it
blocks Backspace and Ctrl+V, and the field becomes unusable. Even then, paste
by right-click bypasses `keydown` — so **also handle `input`**, and validate on
submit regardless.

Arrow-key navigation, which lab experiment 16 uses:

```js
const box = document.getElementById("player");
let x = 0, y = 0;
const STEP = 10;
document.addEventListener("keydown", e => {
  const moves = { ArrowUp: [0,-1], ArrowDown: [0,1], ArrowLeft: [-1,0], ArrowRight: [1,0] };
  const m = moves[e.key];
  if (!m) return;
  e.preventDefault();                       // stop the page scrolling
  x += m[0] * STEP;  y += m[1] * STEP;
  box.style.transform = `translate(${x}px, ${y}px)`;
});
```

`e.preventDefault()` on the arrow keys is what stops the page scrolling under
your animation.

## 4.13 Mouse events and animation

### 💡 Prefer CSS classes to inline style changes

```js
// verbose, and mixes presentation into the script
el.onmouseover = () => { el.style.transform = "scale(1.1)"; el.style.boxShadow = "0 4px 12px #0003"; };
el.onmouseout  = () => { el.style.transform = "";           el.style.boxShadow = ""; };

// one line, and the design lives in the stylesheet where it belongs
el.addEventListener("mouseenter", () => el.classList.add("lifted"));
el.addEventListener("mouseleave", () => el.classList.remove("lifted"));
```
```css
.card    { transition: transform .25s ease, box-shadow .25s ease; }
.lifted  { transform: scale(1.1); box-shadow: 0 4px 12px #0003; }
```

Better still, a pure hover effect needs no JavaScript at all —
`.card:hover { … }`. Use JavaScript when the state must **persist** past the
pointer leaving.

### Drag with mouse events

```js
const el = document.getElementById("draggable");
let dragging = false, ox = 0, oy = 0;

el.addEventListener("mousedown", e => {
  dragging = true;
  ox = e.clientX - el.offsetLeft;
  oy = e.clientY - el.offsetTop;
  el.classList.add("dragging");
  e.preventDefault();                       // stop text selection
});
document.addEventListener("mousemove", e => {   // on DOCUMENT, not the element
  if (!dragging) return;
  el.style.left = (e.clientX - ox) + "px";
  el.style.top  = (e.clientY - oy) + "px";
});
document.addEventListener("mouseup", () => {
  dragging = false;
  el.classList.remove("dragging");
});
```

`mousemove` and `mouseup` go on `document`, not the element. Move the pointer
faster than the element follows and it leaves the element's box — an
element-bound `mousemove` then stops firing and the drag sticks.

### 🔢 Animation: `setInterval` vs `requestAnimationFrame`

```js
// timer-driven — fixed rate, keeps running in background tabs
let pos = 0;
const id = setInterval(() => {
  pos += 2;
  box.style.left = pos + "px";
  if (pos >= 300) clearInterval(id);         // ALWAYS clear it
}, 16);

// frame-driven — synchronised to the display, pauses in background tabs
function step() {
  pos += 2;
  box.style.left = pos + "px";
  if (pos < 300) requestAnimationFrame(step);
}
requestAnimationFrame(step);
```

| | `setInterval` | `requestAnimationFrame` |
|---|---|---|
| Rate | Whatever you ask for | The display refresh rate |
| Background tabs | Keeps running, wasting battery | Paused |
| Smoothness | Can tear or stutter | Synchronised to repaint |
| Cancel with | `clearInterval(id)` | `cancelAnimationFrame(id)` |

Use `requestAnimationFrame` for animation and `setInterval` for clocks and
polling. And for anything a stylesheet can express — a fade, a slide, a
transform — use a CSS transition, which the browser can run off the main
thread entirely.

**Forgetting `clearInterval` is a real bug**, not a style point: the callback
keeps firing forever, and if it references DOM nodes they can never be garbage
collected.

**Worked example.** A greeting that changes with the time of day — lab
experiment 12.

```js
function greeting(hour = new Date().getHours()) {
  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  if (hour < 21) return "Good evening";
  return "Good night";
}
document.getElementById("greet").textContent = greeting();
```

Taking `hour` as a parameter with a default is what makes this **testable** —
you can assert `greeting(9) === "Good morning"` without waiting until 9 am.
The lab version does exactly that.

---

## Practice problems

### Problem 1

Explain why this deletes only every other row, and fix it.

```js
const rows = document.getElementsByClassName("row");
for (let i = 0; i < rows.length; i++) rows[i].remove();
```

**Solution.**

`getElementsByClassName` returns a **live** HTMLCollection. Removing `rows[0]`
makes the old `rows[1]` become `rows[0]`, but `i` has already advanced to 1 —
so the loop skips it. Each iteration removes one and skips one.

Three correct fixes:

```js
document.querySelectorAll(".row").forEach(el => el.remove());   // static snapshot
[...rows].forEach(el => el.remove());                           // snapshot the live one
while (rows.length) rows[0].remove();                           // always take the first
```

### Problem 2

Write a complete validator for a registration form with username (3–20
alphanumeric), email, password (8+ with mixed case, digit and symbol), confirm
password, and an accepted-terms checkbox. Show errors inline and block
submission.

**Solution.**

```js
const CHECKS = [
  { id: "username", test: v => /^[A-Za-z0-9_]{3,20}$/.test(v.trim()),
    msg: "3–20 letters, digits or underscore" },
  { id: "email",    test: v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()),
    msg: "Enter a valid email address" },
  { id: "password", test: v => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/.test(v),
    msg: "8+ chars with upper, lower, digit and symbol" }
];

function validate(form) {
  const errors = {};
  for (const c of CHECKS) {
    const v = form.elements[c.id].value;
    if (!c.test(v)) errors[c.id] = c.msg;
  }
  if (form.elements.password.value !== form.elements.confirm.value)
    errors.confirm = "Passwords do not match";
  if (!form.elements.terms.checked)
    errors.terms = "You must accept the terms";
  return errors;
}

document.getElementById("reg").addEventListener("submit", function (e) {
  const errors = validate(this);
  for (const c of [...CHECKS.map(c => c.id), "confirm", "terms"])
    setFieldError(this.elements[c], errors[c] || "");
  if (Object.keys(errors).length) {
    e.preventDefault();
    this.querySelector(".is-invalid")?.focus();     // move focus to the first problem
  }
});
```

Two things earn the extra marks: the checks are **data**, not a wall of `if`
statements, so adding a field is one line; and focus moves to the first invalid
field, which is what makes the form usable by keyboard.

### Problem 3

Distinguish `alert`, `confirm` and `prompt`, then rewrite a `confirm`-based
delete using `<dialog>` and explain the advantages.

**Solution.**

`alert` shows a message and returns `undefined`; `confirm` returns a boolean;
`prompt` returns the typed string or `null` on cancel. All three are modal,
blocking and unstylable.

```js
// before
if (confirm("Delete record " + id + "?")) doDelete(id);

// after
const dlg = document.getElementById("confirmBox");
function askDelete(id) {
  dlg.querySelector("p").textContent = `Delete record ${id}?`;
  dlg.returnValue = "";
  dlg.showModal();
  dlg.addEventListener("close", () => {
    if (dlg.returnValue === "ok") doDelete(id);
  }, { once: true });
}
```

Advantages: it can be styled to match the site; it does not freeze the page,
so animations and timers continue; Escape closes it and focus is trapped inside
it; and the message can contain markup. The `{ once: true }` matters — without
it, every call to `askDelete` adds another `close` listener and the second
deletion fires twice.

---

## Exam questions from this unit

**Two marks**

1. What is the DOM?
2. Distinguish the DOM from the BOM.
3. Distinguish `innerHTML` from `textContent`.
4. Distinguish `getElementById` from `querySelector`.
5. Name the three JavaScript dialog boxes and what each returns.
6. What does `preventDefault()` do?
7. Distinguish `e.target` from `e.currentTarget`.
8. Why is client-side validation not security?

**Five marks**

1. Explain the DOM methods for selecting, creating and removing elements.
2. Explain how to access every kind of form control from JavaScript.
3. Explain event bubbling, capturing and delegation with an example.
4. Explain the three dialog boxes with examples and their limitations.
5. Explain `window.open` and its parameters, including pop-up blocking.
6. Explain keyboard and mouse events with an animation example.

**Ten marks**

1. Write a complete form validation program covering required fields, format
   validation and inline messages, and explain it.
2. Explain the JavaScript event model exhaustively — attachment methods, the
   event object, phases and delegation.
3. Explain client-side scripting for dialogs, windows, status messages and
   event-driven animation, with code.

## Mistakes that cost marks

- Treating `.value` as a number
- Using `innerHTML` with user input — an XSS vulnerability
- Testing `value === ""` without `.trim()`
- Handling `click` on the submit button instead of `submit` on the form
- Forgetting `e.preventDefault()`, so the form submits anyway
- Looping over a live HTMLCollection while removing from it
- Using an arrow function and then expecting `this` to be the element
- `removeEventListener` with a different function reference
- Not checking `window.open` for `null`
- Confusing `prompt`'s `null` (cancel) with `""` (empty)
- Claiming `window.status` still works — it does not
- Forgetting `clearInterval`
- Binding `mousemove` to the dragged element instead of the document
- Using `e.keyCode` instead of `e.key`
