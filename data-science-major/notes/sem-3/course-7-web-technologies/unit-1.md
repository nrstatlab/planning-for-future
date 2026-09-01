# Unit 1 — HTML

**Syllabus topics:** Introduction to web designing, difference between web
applications and desktop applications, introduction to HTML, HTML structure,
elements, attributes, headings, paragraphs, images, tables, lists, blocks,
symbols, embedding multi-media components in HTML, HTML forms.

---

## 1.1 Introduction to web design

### 🎯 The big idea

**Web design** is deciding what a page contains, how it is arranged, and how a
visitor moves through it — *before* any of it is written in HTML. Course
Objective 1 says "principles of web design", so the exam expects the
principles, not just the tags.

Five that are worth stating, because each has a concrete consequence:

| Principle | What it means | Consequence if ignored |
|---|---|---|
| **Visual hierarchy** | The most important thing is the most prominent | The reader cannot tell what the page is for |
| **Consistency** | Same navigation, colours and type on every page | Every page feels like a different site |
| **Whitespace** | Space is a design element, not waste | A cramped page is unreadable |
| **Accessibility** | Usable with a screen reader, a keyboard, poor eyesight | You exclude real users, and in many places break the law |
| **Responsiveness** | Works on a phone as well as a desktop | Most of your traffic gets the worst experience |

That last one is not a nicety: more than half of web traffic worldwide is now
from mobile devices, which is why Unit 2's media queries matter more than any
amount of decoration.

### The stages of building a site

```
1. Requirements  →  who is it for, what must it do?
2. Content       →  what actually goes on each page?
3. Wireframe     →  boxes and labels, no colour, no styling
4. Design        →  colour, type, imagery
5. Build         →  HTML, then CSS, then JavaScript
6. Test          →  browsers, screen sizes, keyboard, screen reader
7. Deploy & maintain
```

**Wireframe before you write markup.** Deciding structure while typing tags is
how pages end up with six nested `<div>`s holding one paragraph. The wireframe
also tells you what your HTML *elements* should be, which is where §1.9's
semantic HTML comes from.

### 💡 Static versus dynamic

| | Static | Dynamic |
|---|---|---|
| Page content | Fixed files on disk | Assembled per request |
| Same for everyone? | Yes | No — personalised, database-driven |
| Built with | HTML, CSS, JS | Plus a server language and a database |
| Speed and cost | Fast, cheap, easy to host | Slower, needs a server |
| Example | Documentation, a college prospectus | Gmail, an e-commerce catalogue |

This site — the one you are reading — is **static**: every page was generated
once and is served as a file. That is why it loads instantly and costs nothing
to host, and it is a deliberate choice, not a limitation.

## 1.2 Web applications vs desktop applications

### 🎯 The big idea

A desktop application runs **on your machine**. A web application runs **on a
server**, and your browser only displays the result.

| | Desktop application | Web application |
|---|---|---|
| Installation | Required, per machine | None — just a URL |
| Runs on | The user's computer | A server; the browser renders |
| Updates | Each user must update | Update the server once, everyone has it |
| Platform | Usually OS-specific | Any device with a browser |
| Offline | Works | Usually needs a connection |
| Access to hardware | Full | Limited and permission-gated |
| Performance | Faster — native code | Slower — network latency |
| Data storage | Local disk | Server database |
| Examples | MS Word, Photoshop | Gmail, Google Docs |

**The decisive advantage of web applications is deployment.** Fixing a bug means
updating one server, not persuading a thousand users to install a patch. That
single fact explains most of the industry's shift to the web.

### The client–server model

```
   CLIENT (browser)                          SERVER
   ┌────────────────┐    1. HTTP request    ┌──────────────┐
   │                │  ───────────────────► │  Web server  │
   │  Renders HTML  │                       │              │
   │  Applies CSS   │  ◄─────────────────── │  Application │
   │  Runs JS       │    2. HTTP response   │  Database    │
   └────────────────┘       (HTML/CSS/JS)   └──────────────┘
```

**Client-side vs server-side** — a reliable two-mark question:

| | Client-side | Server-side |
|---|---|---|
| Runs on | The browser | The server |
| Languages | HTML, CSS, JavaScript | Python, PHP, Java, Node.js |
| Sees | Only what was sent to it | The database, files, secrets |
| Speed | Immediate — no round trip | Requires a request |
| Security | **Visible to the user; never trust it** | Controlled |

**Client-side validation is a convenience, never a security control.** Anyone
can open dev tools and disable it. Unit 4 covers validation; the rule to
remember is that the server must validate again, always.

### The three languages, and their division of labour

| Language | Provides | Analogy |
|---|---|---|
| **HTML** | Structure and content | The skeleton |
| **CSS** | Presentation | The clothing |
| **JavaScript** | Behaviour | The muscles |

Keeping them separate is called **separation of concerns**, and it is why
inline `style=` attributes and `onclick=` handlers are discouraged.

## 1.3 HTML basics

**HTML** — HyperText Markup Language. Created by **Tim Berners-Lee** in 1991.
Current version: **HTML5**.

It is a **markup** language, not a programming language: it describes structure,
it has no variables, loops or logic. Saying otherwise in an exam loses a mark.

### Document structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page title — shows in the browser tab</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <h1>Visible content starts here</h1>
  <p>Everything the user sees goes in the body.</p>
  <script src="script.js"></script>
</body>
</html>
```

| Part | Purpose |
|---|---|
| `<!DOCTYPE html>` | Declares HTML5. **Omit it and browsers use "quirks mode"**, where old buggy behaviour is emulated and your CSS breaks in confusing ways. |
| `<html lang="en">` | Root element; `lang` matters for screen readers and search |
| `<head>` | Metadata — **not displayed** |
| `<meta charset="UTF-8">` | Character encoding. Omit it and accented or Indian-language characters show as mojibake |
| `<meta name="viewport">` | **Essential for mobile**; without it phones render a zoomed-out desktop layout |
| `<title>` | Tab text, bookmark name, search result heading |
| `<body>` | Everything visible |

### Elements and attributes

```html
<a href="https://example.com" target="_blank" rel="noopener">Visit</a>
 │   └──────── attributes ─────────────────┘              │
 └─ opening tag                             content    closing tag
```

- **Element** = opening tag + content + closing tag
- **Attribute** = extra information, always in the **opening** tag,
  `name="value"`
- **Void (empty) elements** have no closing tag: `<br>`, `<hr>`, `<img>`,
  `<input>`, `<meta>`, `<link>`

**Global attributes**, usable on any element: `id` (unique per page), `class`
(reusable), `style`, `title`, `data-*`, `hidden`.

**`id` vs `class`** is examined constantly: an `id` must be **unique** in the
document; a `class` may be shared by any number of elements. Use `class` for
styling groups, `id` for a single specific target.

## 1.4 Text elements

```html
<h1>Main heading</h1>        <!-- one per page, ideally -->
<h2>Section</h2>
<h6>Smallest</h6>            <!-- six levels, h1 to h6 -->

<p>A paragraph of text.</p>
<br>                          <!-- line break -->
<hr>                          <!-- horizontal rule -->
<pre>  preserves    spacing
  and line breaks </pre>
```

| Element | Meaning | Renders as |
|---|---|---|
| `<strong>` | **Strong importance** | Bold |
| `<b>` | Stylistically offset | Bold |
| `<em>` | **Emphasis** | Italic |
| `<i>` | Alternate voice | Italic |
| `<mark>` | Highlighted | Yellow background |
| `<small>` | Fine print | Smaller |
| `<del>` / `<ins>` | Deleted / inserted | Struck / underlined |
| `<sub>` / `<sup>` | Subscript / superscript | H<sub>2</sub>O, x<sup>2</sup> |
| `<code>` | Code | Monospace |
| `<blockquote>` | Extended quotation | Indented |
| `<abbr title="...">` | Abbreviation | Dotted underline |

**`<strong>` vs `<b>`** is a standard question. Both look bold. `<strong>`
carries **meaning** — a screen reader emphasises it; `<b>` is purely visual.
Prefer the semantic one. Same for `<em>` over `<i>`.

**Do not use `<br>` to create space between paragraphs.** That is CSS's job
(`margin`). Using `<br><br>` is the mark of someone who has not learned CSS.

## 1.5 Symbols — HTML entities

Certain characters cannot be typed literally because they mean something to the
parser.

| Character | Entity | Why |
|---|---|---|
| `<` | `&lt;` | Would start a tag |
| `>` | `&gt;` | Would end a tag |
| `&` | `&amp;` | Starts an entity |
| `"` | `&quot;` | Ends an attribute value |
| non-breaking space | `&nbsp;` | Prevents a line break |
| © | `&copy;` | |
| ® | `&reg;` | |
| ₹ | `&#8377;` | Indian Rupee |
| — | `&mdash;` | Em dash |

**To display code on a page you must escape `<` and `>`** — otherwise the
browser tries to execute the tags. This is also the first line of defence
against cross-site scripting.

## 1.6 Lists

```html
<ul>                          <!-- Unordered: bullets -->
  <li>First item</li>
  <li>Second item</li>
</ul>

<ol type="1" start="3">       <!-- Ordered: numbers -->
  <li>Third item</li>
</ol>

<dl>                          <!-- Description list -->
  <dt>HTML</dt>
  <dd>HyperText Markup Language</dd>
  <dt>CSS</dt>
  <dd>Cascading Style Sheets</dd>
</dl>

<ul>                          <!-- Nested: note the nesting position -->
  <li>Data Science
    <ul>
      <li>Statistics</li>
      <li>Programming</li>
    </ul>
  </li>
</ul>
```

**A nested list goes *inside* the parent `<li>`, not between `<li>` elements.**
Putting it between them is invalid HTML and a common lab-exam error.

`<ol>` types: `1` (default), `A`, `a`, `I`, `i`. Also `reversed`.

## 1.7 Images and multimedia

```html
<img src="photo.jpg" alt="Students in the data science lab"
     width="600" height="400" loading="lazy">
```

| Attribute | Purpose |
|---|---|
| `src` | Path to the image — **required** |
| `alt` | Text alternative — **required for accessibility** |
| `width` / `height` | Dimensions; setting both prevents layout shift |
| `loading="lazy"` | Defer off-screen images |

**`alt` is not optional.** Screen readers announce it, it displays when the
image fails to load, and search engines index it. An empty `alt=""` is correct
for purely decorative images — but it must be *present*.

```html
<audio controls>
  <source src="lecture.mp3" type="audio/mpeg">
  Your browser does not support audio.
</audio>

<video controls width="640" poster="thumb.jpg">
  <source src="demo.mp4" type="video/mp4">
  <source src="demo.webm" type="video/webm">
  Your browser does not support video.
</video>

<iframe src="https://www.youtube.com/embed/VIDEO_ID"
        width="560" height="315" allowfullscreen title="Demo"></iframe>
```

**The text between the tags is fallback content** shown only when the element is
unsupported. Several `<source>` elements let the browser pick a format it can
play. Lab experiment 5 requires a presentation with text, audio **and** video.

## 1.8 Tables

```html
<table>
  <caption>Semester III marks</caption>
  <thead>
    <tr><th>Roll</th><th>Name</th><th>Marks</th></tr>
  </thead>
  <tbody>
    <tr><td>24001</td><td>Ananya</td><td>85</td></tr>
    <tr><td colspan="2">Total</td><td>85</td></tr>
  </tbody>
  <tfoot>
    <tr><td colspan="3">Provisional</td></tr>
  </tfoot>
</table>
```

| Element | Is |
|---|---|
| `<table>` | The table |
| `<caption>` | Its title — should be the **first** child |
| `<thead>` / `<tbody>` / `<tfoot>` | Row groups |
| `<tr>` | Table row |
| `<th>` | Header cell — bold and centred by default |
| `<td>` | Data cell |
| `colspan` / `rowspan` | Merge across columns / rows |

> **Tables are for tabular data, never for page layout.** Using them to
> position elements was standard practice in the 1990s and is now firmly wrong —
> it breaks screen readers, resists responsive design, and Unit 2's Flexbox and
> Grid exist precisely to replace it. Lab experiment 3 asks you to arrange
> images in a table; do it as instructed for the marks, then note that Flexbox
> is how you would really do it.

## 1.9 Semantic structure

HTML5 added elements that describe *what a region is*, not just how it looks:

```html
<header>   <nav>    <main>   <article>
<section>  <aside>  <footer> <figure> <figcaption>
```

```html
<body>
  <header><h1>Site title</h1><nav>…</nav></header>
  <main>
    <article>
      <h2>Article heading</h2>
      <section>…</section>
    </article>
    <aside>Related links</aside>
  </main>
  <footer>© 2026</footer>
</body>
```

**Why bother, when `<div>` renders identically?** Accessibility — screen readers
navigate by landmark; SEO — search engines identify the main content; and
maintainability — `</section>` tells you what closed, `</div>` does not.

## 1.10 Forms

```html
<form action="/submit" method="post">
  <label for="name">Name:</label>
  <input type="text" id="name" name="name" required
         placeholder="Your full name" maxlength="50">

  <label for="email">Email:</label>
  <input type="email" id="email" name="email" required>

  <label for="age">Age:</label>
  <input type="number" id="age" name="age" min="16" max="99">

  <fieldset>
    <legend>Gender</legend>
    <input type="radio" id="f" name="gender" value="F">
    <label for="f">Female</label>
    <input type="radio" id="m" name="gender" value="M">
    <label for="m">Male</label>
  </fieldset>

  <label for="course">Course:</label>
  <select id="course" name="course">
    <option value="">-- choose --</option>
    <option value="ds">Data Science</option>
    <option value="cs" selected>Computer Science</option>
  </select>

  <input type="checkbox" id="terms" name="terms" required>
  <label for="terms">I accept the terms</label>

  <textarea name="comments" rows="4" cols="40"></textarea>

  <button type="submit">Submit</button>
  <button type="reset">Reset</button>
</form>
```

### Input types

`text` `password` `email` `number` `tel` `url` `date` `time` `color` `range`
`file` `checkbox` `radio` `hidden` `submit` `reset`

HTML5 types matter: `type="email"` gives free format validation and a
mobile keyboard with `@` on it.

### The three attributes that carry marks

**`name`** — without it the field is **not submitted at all**. `id` is for
labels and CSS; `name` is what the server receives. Forgetting `name` is the
most common form bug there is.

**`for` on the `<label>`, matching the input's `id`** — clicking the label then
focuses the input, and screen readers announce them together. A radio button
without a label is nearly unusable on a phone.

**`required`, `min`, `max`, `pattern`, `maxlength`** — free client-side
validation with no JavaScript. Convenience only; see Unit 4.

### GET vs POST

| | GET | POST |
|---|---|---|
| Data goes in | The URL query string | The request body |
| Visible | **Yes, in the address bar** | No |
| Length limit | ~2000 characters | Effectively none |
| Bookmarkable | Yes | No |
| Caching | Cached | Not cached |
| Use for | Searches, filters | Logins, uploads, anything changing state |

**Never send a password by GET** — it would appear in the URL, in browser
history and in server logs.

---

## 📝 Practice problems

### Problem 1

Write HTML for a student registration form with name, email, date of birth,
gender (radio), courses (checkboxes), a state dropdown and a submit button.

**Solution.**

```html
<form action="/register" method="post">
  <fieldset>
    <legend>Personal details</legend>

    <label for="name">Full name:</label>
    <input type="text" id="name" name="name" required maxlength="60">

    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required>

    <label for="dob">Date of birth:</label>
    <input type="date" id="dob" name="dob" required>
  </fieldset>

  <fieldset>
    <legend>Gender</legend>
    <input type="radio" id="g-f" name="gender" value="F" required>
    <label for="g-f">Female</label>
    <input type="radio" id="g-m" name="gender" value="M">
    <label for="g-m">Male</label>
    <input type="radio" id="g-o" name="gender" value="O">
    <label for="g-o">Other</label>
  </fieldset>

  <fieldset>
    <legend>Courses</legend>
    <input type="checkbox" id="c-ds" name="courses" value="ds">
    <label for="c-ds">Data Science</label>
    <input type="checkbox" id="c-st" name="courses" value="stats">
    <label for="c-st">Statistics</label>
  </fieldset>

  <label for="state">State:</label>
  <select id="state" name="state" required>
    <option value="">-- select --</option>
    <option value="AP">Andhra Pradesh</option>
    <option value="TS">Telangana</option>
  </select>

  <button type="submit">Register</button>
</form>
```

**Three details that earn the marks:** every input has a `name` (or it is not
submitted); every `<label for>` matches an `id`; and the radio buttons **share
one `name`**, which is what makes them mutually exclusive. Give them different
names and all three become selectable at once.

The checkboxes deliberately share a name too, so the server receives a list.

### Problem 2

What is wrong with this markup?

```html
<ul>
  <li>Data Science</li>
  <ul>
    <li>Statistics</li>
  </ul>
</ul>
```

**Error:** the nested `<ul>` is a direct child of the outer `<ul>`, which only
permits `<li>` children. It must go **inside** the parent `<li>`.

**Fix:**

```html
<ul>
  <li>Data Science
    <ul>
      <li>Statistics</li>
    </ul>
  </li>
</ul>
```

Browsers render the broken version acceptably, which is exactly why it survives
— but it fails validation and confuses screen readers.

### Problem 3

Distinguish `<strong>` from `<b>`, and `id` from `class`.

**Solution.**

**`<strong>` vs `<b>`** — both render bold. `<strong>` is **semantic**: it means
"this is important", and a screen reader changes its tone for it. `<b>` is
purely **presentational**: "make this bold". Prefer `<strong>` unless you
genuinely mean only visual weight. Same relationship as `<em>` to `<i>`.

**`id` vs `class`** —

| | `id` | `class` |
|---|---|---|
| Uniqueness | **Must be unique** per page | Reusable |
| Per element | One | Many, space-separated |
| CSS selector | `#header` | `.card` |
| JS | `getElementById()` | `getElementsByClassName()`, `querySelectorAll()` |
| Specificity | Higher | Lower |
| Use for | One specific element; anchor targets | Styling groups |

Duplicate `id`s are invalid, and `getElementById()` then returns only the first
— a silent bug.

---

## Exam questions from this unit

**Two marks**

1. Distinguish a web application from a desktop application.
2. What is the purpose of `<!DOCTYPE html>`?
3. Distinguish `<strong>` from `<b>`.
4. Why must an `<img>` have an `alt` attribute?
5. Distinguish `id` from `class`.
6. Why must a form input have a `name`?

**Five marks**

1. Explain the structure of an HTML document with an example.
2. Explain the form elements and input types in HTML.
3. Explain the table elements with `colspan` and `rowspan`.
4. Explain GET and POST with the differences.
5. Explain HTML5 semantic elements and why they matter.

**Ten marks**

1. Design a complete student registration form using all major input types,
   and explain each element.
2. Explain HTML lists, tables and multimedia embedding with examples.

## Mistakes that cost marks

- Omitting `<!DOCTYPE html>` and triggering quirks mode
- Omitting `<meta charset="UTF-8">`
- Nesting a list between `<li>` elements instead of inside one
- Forgetting `name` on form inputs
- `<label>` without a matching `for`
- Giving radio buttons in a group **different** names
- Using `<br><br>` for spacing instead of CSS margins
- Using tables for page layout
- Omitting `alt` on images
- Not closing tags, or closing them in the wrong order
