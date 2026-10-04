# Practical Lab

**16 experiments**, each set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and
Results.

Code lives in `labs/course-7-web/`.

> **These run, twice over.** Every page is opened in Chromium, served over http from a local
> server as a page should be, and what it shows is under **5. Execution and Results**: the
> page's headings, or what a driver typed, clicked and read back, with screenshots. The
> interactive pages each have a driver beside them, `_drive_10_string_ops.py` and so on, run by
> `tools/data-science/capture_lab_outputs.py`. Separately, every JavaScript function is executed
> by `tools/data-science/run_web_labs.js` under Node 22 with jsdom, and its result asserted, and
> every HTML file is structurally checked — balanced tags, every `<label for>` resolving to a
> real id, every `<img>` carrying `alt`.

```bash
npm --prefix tools/data-science install       # jsdom and jQuery, once
node tools/data-science/run_web_labs.js       # from the repository root
```

Two things cannot be reached from where these pages are checked. jQuery's CDN,
`code.jquery.com`, is served instead from npm's copy of the same release, 3.7.1, and the page's
`integrity` attribute makes the browser check that it is the same file, byte for byte. The
weather API needs a key and a network, so Experiment 15 shows the page's own offline path. The
clock is fixed at 09:00 on 4 October 2026, Indian time, so the calendar and the greeting show
the same thing on every run.

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

### 1. Question

Write a page that uses the HTML formatting options: bold, italics, underline, headings H1–H6, font type, size and colour, a coloured or image background, paragraphs, line breaks, a horizontal rule and `<pre>`.

### 2. Aim

Use HTML's formatting elements, and know which are obsolete and which carry meaning.

### 3. Steps

1. **Set up the head: charset, viewport, title and styles.**
2. **Show the six heading levels.**
3. **Bold, italics and underline.**
4. **Paragraphs, line breaks and a horizontal rule.**
5. **Set the font type, size and colour.**
6. **Give a background colour and a background image.**
7. **Keep the spacing with pre.**
8. **Show the other inline formatting.**

<div class="formula" markdown="1">
<span class="label">THE EXAM POINT</span>

The syllabus asks for the `<font>` tag, which is
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
</div>


### 4. Programme

{{programme: course-7-web/01_formatting.html}}

### 5. Execution and Results

{{output: course-7-web/01_formatting.html}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Every option renders: the six heading levels, the semantic and presentational bold and italic, the CSS fonts, the patterned background, and the `<pre>` block with its spacing kept.
</div>


## Experiment 2 — Lists and an image

### 1. Question

Write a page with ordered, unordered and nested lists, and an image.

### 2. Aim

Use HTML's three list types, nest them correctly, and add an image with alt text.

### 3. Steps

1. **Set up the head: charset, viewport, title and styles.**
2. **An ordered list, and its type and start.**
3. **An unordered list.**
4. **A nested list, inside an li.**
5. **A description list.**
6. **An image, with alt text and a caption.**

<div class="formula" markdown="1">
<span class="label">THE MISTAKE EVERYONE MAKES</span>

A nested list goes **inside** an `<li>`, not
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
</div>


### 4. Programme

{{programme: course-7-web/02_lists.html}}

### 5. Execution and Results

{{output: course-7-web/02_lists.html}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The ordered list continues from III in Roman numerals, the nested list reaches three levels, and the image loads with its caption.
</div>


## Experiment 3 — Ten images aligned with a table

### 1. Question

Align ten images using a table.

### 2. Aim

Lay images out in a table as asked, and then the way HTML5 intends, with CSS Grid.

### 3. Steps

1. **Set up the head: charset, viewport, title and styles.**
2. **Arrange ten images in a table.**
3. **Say why a table is the wrong tool for layout.**
4. **Lay out the same gallery with CSS Grid.**

<div class="formula" markdown="1">
<span class="label">STATE THE CAVEAT</span>

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
</div>


### 4. Programme

{{programme: course-7-web/03_image_table.html}}

### 5. Execution and Results

{{output: course-7-web/03_image_table.html}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The ten images sit in the table's grid, and again in the CSS Grid gallery below it.
</div>


## Experiment 4 — A form with every control type

### 1. Question

Create a form with text boxes, radio buttons, check boxes, and reset and submit buttons.

### 2. Aim

Build a form from every kind of control, each labelled and named.

### 3. Steps

1. **Set up the head: charset, viewport, title and styles.**
2. **Open the form.**
3. **Text boxes, each with a label.**
4. **Radio buttons, sharing one name.**
5. **Check boxes.**
6. **A select list and a file picker.**
7. **Reset and submit buttons.**

<div class="formula" markdown="1">
<span class="label">RADIO VS CHECKBOX, AND THE RULE BEHIND IT</span>

Radio buttons in one group
must share the **same `name`** — that is what makes them mutually exclusive,
and different names give you three independent buttons that can all be on at
once. Checkboxes sharing a name submit as multiple values under that key.

Every input needs a `name`, or it is **not submitted at all**. Every input
needs a `<label for>` matching its `id`, or clicking the text does not focus
the field and a screen reader has nothing to announce.
</div>


### 4. Programme

{{programme: course-7-web/04_form_controls.html}}

### 5. Execution and Results

{{output: course-7-web/04_form_controls.html}}

The driver fills the form but does not submit it: it posts to `/submit`, and no server is
behind that address. `FormData` shows what would be sent — one `gender`, two `subjects`.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Checking Male clears Female, as one shared name makes them; the two subjects submit under one key; and Reset empties the form.
</div>


## Experiment 5 — Embed a calendar

### 1. Question

Embed a calendar object in a web page.

### 2. Aim

Show a calendar three ways: the native date picker, an embedded calendar, and a month grid generated in JavaScript.

### 3. Steps

**In HTML**, `05_calendar.html`:

1. **Set up the head: charset, viewport, title and styles.**
2. **The native date picker.**
3. **An embedded external calendar.**
4. **Controls for a generated month grid.**
5. **Fill the month list, and start at today's month.**
6. **Draw the month, and move between months.**

**In JavaScript**, `05_calendar.js`:

1. **Name the months and days.**
2. **Count the days in a month.**
3. **Find the first weekday, and lay the month out in weeks.**
4. **Test for a leap year.**
5. **Draw the month into a table.**

<div class="formula" markdown="1">
<span class="label">THREE MODERN ANSWERS</span>

The syllabus says "embed a calendar object", which in 2004 meant an ActiveX
control. Three modern answers, in increasing order of effort: the native date picker (one
line), an embedded external calendar (an `<iframe>`), and a month grid you generate yourself,
which is the version worth learning because it is pure logic.

**The trick worth remembering:** `new Date(y, m, 0)` is day zero of month `m`,
which is the **last day of month m − 1** — so it gives you the number of days
in a month, leap years included, with no table and no arithmetic.
</div>


### 4. Programme

**In HTML**, `05_calendar.html`:

{{programme: course-7-web/05_calendar.html}}

**In JavaScript**, `05_calendar.js`:

{{programme: course-7-web/05_calendar.js}}

### 5. Execution and Results

{{output: course-7-web/05_calendar.html}}

Verified: February 2024 has 29 days, February 2025 has 28, and 1 August 2026
falls on a Saturday. The first and third are shown above; all three are asserted by the runner.

Note that JavaScript months are **0-indexed** in the `Date` constructor
(January is 0) but 1-indexed in an ISO string. Mixing the two is the classic
date bug.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The page opens on October 2026 with the 4th marked as today; it moves between months, and February 2024 has 29 days.
</div>


## Experiment 6 — Mailing-list subscription form

### 1. Question

Create a form to subscribe to a mailing list.

### 2. Aim

Build a subscription form that asks for consent, and check it before it is sent.

### 3. Steps

1. **Set up the head, and link the stylesheet.**
2. **Ask for the email and name.**
3. **Ask for the topics.**
4. **Ask for the frequency, format and consent.**
5. **Check the email and the consent on submit.**

<div class="formula" markdown="1">
<span class="label">CONSENT</span>

An explicit **consent** checkbox, unticked by default, is not decoration —
pre-ticked consent is unlawful under most data-protection regimes and is the
kind of detail that separates a good answer from a complete one.
</div>


### 4. Programme

{{programme: course-7-web/06_subscribe.html}}

### 5. Execution and Results

{{output: course-7-web/06_subscribe.html}}

The page borrows its look from `07_styled_form.css`, so its styling is Experiment 7's.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Submitted empty, the form asks for a valid email and for consent; filled in, it reports "Subscribed asha@example.com."
</div>


## Experiment 7 — Style a registration form with CSS

### 1. Question

Style a registration form with CSS: different selectors, colours, borders and spacing.

### 2. Aim

Style a form with CSS, using every kind of selector.

### 3. Steps

**In HTML**, `07_styled_form.html`:

1. **Set up the head, and link the stylesheet.**
2. **Personal details.**
3. **Account.**
4. **Programme.**

**In CSS**, `07_styled_form.css`:

1. **Define the colours once, as custom properties.**
2. **Lay out the page, the form and its fieldsets.**
3. **Style the labels and the text-like controls.**
4. **Show state with pseudo-classes.**
5. **Style the error messages and the buttons.**
6. **Respect the user's settings.**

<div class="formula" markdown="1">
<span class="label">SELECTORS, AND TWO DETAILS</span>

Selector types demonstrated: element (`form`), class, id, **attribute**
(`input[type="text"]`), **pseudo-class** (`:focus`, `:invalid`), descendant,
and a custom-property `:root` block.

Two details the examiner looks for. **`font: inherit`** — form controls use
the operating system font unless told otherwise, so an unstyled input looks
alien beside your text. And **`:not(:placeholder-shown)`** — without it,
`:invalid` fires on an empty required field the moment the page loads, and the
form is red before the user has typed anything.
</div>


### 4. Programme

**In HTML**, `07_styled_form.html`:

{{programme: course-7-web/07_styled_form.html}}

**In CSS**, `07_styled_form.css`:

{{programme: course-7-web/07_styled_form.css}}

### 5. Execution and Results

{{output: course-7-web/07_styled_form.html}}

**Corrected:** the `.is-invalid` rule lost to `input:valid:not(:placeholder-shown)`, which is
more specific, so a field the script had rejected kept a green border while showing its error —
in Experiment 11, a mobile number of 1234567890 looked accepted. The rule now repeats those
pseudo-classes, and the stylesheet says why.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The form is drawn with the stylesheet's colours, borders and spacing, and no field is red before anything has been typed.
</div>


## Experiment 8 — Responsive page with Flexbox and Grid

### 1. Question

Create a responsive page with Flexbox and Grid.

### 2. Aim

Lay a page out with Flexbox and Grid so that it adapts to the screen's width.

### 3. Steps

**In HTML**, `08_responsive.html`:

1. **Set up the head: the viewport meta, and the stylesheet.**
2. **A navigation bar.**
3. **The page header.**
4. **A sidebar.**
5. **The main content: cards, and a media object.**
6. **The footer.**

**In CSS**, `08_responsive.css`:

1. **Define the colours and the gap.**
2. **A navigation bar with Flexbox.**
3. **A page layout with named Grid areas.**
4. **A card grid that needs no media query.**
5. **A media object with Flexbox.**
6. **Change the layout at the breakpoints, for print and for reduced motion.**

<div class="formula" markdown="1">
<span class="label">THE VIEWPORT, AND THE RULE</span>

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

**Without that meta tag the page is not responsive**, whatever the CSS says: a
phone pretends to be 980px wide and renders your desktop layout shrunk to
illegibility.

**Flexbox for one dimension, Grid for two** — that is the whole rule.

The `repeat(auto-fit, minmax(240px, 1fr))` line is worth memorising: it fits
as many columns as will hold 240px each and stretches them to fill the row,
reflowing at every width with **no media queries at all**. It is a complete
responsive grid in one declaration.
</div>


### 4. Programme

**In HTML**, `08_responsive.html`:

{{programme: course-7-web/08_responsive.html}}

**In CSS**, `08_responsive.css`:

{{programme: course-7-web/08_responsive.css}}

### 5. Execution and Results

{{output: course-7-web/08_responsive.html}}

Note that the mobile layout puts `main` **above** `side`, so a phone user
reads the content before the sidebar. Named grid areas make that reordering a
one-line change. At 1200 px the cards still come two to a row: their box is 734 px wide, and
three cards of 240 px, with the two 24 px gaps used above 1100 px, need 768.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

At 390 px there is one column, with the sidebar under the content; at 800 and 1200 px the sidebar sits beside it, and the cards reflow on their own.
</div>


## Experiment 9 — Hover effects and transitions

### 1. Question

Add hover effects and transitions to a page with CSS.

### 2. Aim

Animate elements on hover with CSS transitions, cheaply and considerately.

### 3. Steps

**In HTML**, `09_hover.html`:

1. **Set up the head, and link the stylesheet.**
2. **Buttons.**
3. **Images that zoom.**
4. **Cards whose caption slides up.**
5. **A growing underline.**
6. **A tooltip.**
7. **A keyframe animation.**

**In CSS**, `09_hover.css`:

1. **Buttons: background, lift and shadow.**
2. **Image zoom, cropped by the wrapper.**
3. **A caption that slides up on hover.**
4. **An underline that grows from the centre.**
5. **A CSS-only tooltip.**
6. **Keyframe animations.**
7. **Respect the user's motion preference.**

<div class="formula" markdown="1">
<span class="label">THREE POINTS EARN THE MARKS</span>

**Animate `transform` and `opacity`, not `width`, `top` or `margin`.** The
browser can composite transform and opacity changes on the GPU without
recalculating layout; the others force a reflow on every frame and stutter.

**`overflow: hidden` on the wrapper** is what makes the zoom crop cleanly
instead of the enlarged image spilling over its neighbours.

**The `prefers-reduced-motion` block** respects users who get motion sickness
from animation. It is two lines and it is the difference between a page that
is merely pretty and one that is considerate.
</div>


### 4. Programme

**In HTML**, `09_hover.html`:

{{programme: course-7-web/09_hover.html}}

**In CSS**, `09_hover.css`:

{{programme: course-7-web/09_hover.css}}

### 5. Execution and Results

{{output: course-7-web/09_hover.html}}

Note that `rgba()` fades only the caption's background; `opacity` there would
fade the white text too.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

On hover the button lifts 2 px, the image loses its grey and scales by 1.1, the caption slides up into view, and the tooltip appears.
</div>


## Experiment 10 — JavaScript string operations

### 1. Question

Write JavaScript string operations: reverse a string, take a substring, and count the vowels.

### 2. Aim

Operate on strings in JavaScript, and show the results live on a page.

### 3. Steps

**In HTML**, `10_string_ops.html`:

1. **Set up the head, and link the stylesheet.**
2. **A text box for the string.**
3. **Show every result for what is typed.**
4. **Update on every keystroke.**

**In JavaScript**, `10_string_ops.js`:

1. **Reverse a string.**
2. **Count the vowels, consonants and words.**
3. **Test for a palindrome, title-case, and count each character.**
4. **Find the longest word.**
5. **Put everything together.**

<div class="formula" markdown="1">
<span class="label">THREE THINGS TO NOTICE</span>

`[...s]` splits by **code point**, while `s.split("")` splits by UTF-16 code
unit. For plain ASCII they agree; for an emoji or an accented character
`split("")` tears the character in half and the reversal produces garbage.

`(s.match(…) || [])` is not optional. `match` returns **`null`** when nothing
matches, not an empty array, and `null.length` throws.

`s.trim().split(/\s+/)` on an empty string gives `[""]`, whose length is 1 —
so a word count needs the explicit empty check, or every blank input reports
one word.
</div>


### 4. Programme

**In HTML**, `10_string_ops.html`:

{{programme: course-7-web/10_string_ops.html}}

**In JavaScript**, `10_string_ops.js`:

{{programme: course-7-web/10_string_ops.js}}

### 5. Execution and Results

{{output: course-7-web/10_string_ops.html}}

Asserted by the runner: `reverse("Data Science") === "ecneicS ataD"`,
`countVowels("Data Science") === 5`, `isPalindrome("A man, a plan, a canal: Panama")
=== true`, and `stats("").words === 0`. The longest word of the second string is
"canal:", colon and all: words are split on spaces only.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

"Data Science" has 12 characters, 2 words and 5 vowels, and reverses to "ecneicS ataD"; "A man, a plan, a canal: Panama" is a palindrome.
</div>


## Experiment 11 — Form validation

### 1. Question

Validate a form in JavaScript: the email's format, the password's length and the required fields.

### 2. Aim

Check a form's fields in JavaScript before it is sent, and show each error beside its field.

### 3. Steps

**In HTML**, `11_validation.html`:

1. **Set up the head, and link the stylesheet.**
2. **The registration form, with a place for each error.**
3. **Load the code that checks it.**

**In JavaScript**, `11_validation.js`:

1. **Write a rule for each field.**
2. **Check every rule, and the two that compare fields.**
3. **Check that a date is real, and find an age.**

**In JavaScript**, `11_validation_wire.js`:

1. **Show or clear a field's error.**
2. **Read the form's values.**
3. **Check everything on submit.**
4. **Check a field again once it has been left.**

<div class="formula" markdown="1">
<span class="label">THE DETAIL MOST OFTEN MISSED</span>

The HTML half wires it up, and its `submit` handler is the part that matters:

```js
form.addEventListener("submit", e => {
  const errors = validate(readValues());
  for (const id of [...Object.keys(RULES), "confirm", "terms"])
    setFieldError(form.elements[id], errors[id] || "");
  if (Object.keys(errors).length) {
    e.preventDefault();                          // THIS is what cancels submit
    form.querySelector(".is-invalid")?.focus();  // move focus to the first problem
  }
});
```

**`FormData` omits unchecked checkboxes entirely** — the key is simply absent,
not `false` — so the `terms` value has to be read from `.checked` separately.
That one line is the most commonly missed detail in this experiment.

And say it in the viva: this is a convenience, not a control. The server
validates again.
</div>


### 4. Programme

**In HTML**, `11_validation.html`:

{{programme: course-7-web/11_validation.html}}

**In JavaScript**, `11_validation.js`:

{{programme: course-7-web/11_validation.js}}

**In JavaScript**, `11_validation_wire.js`:

{{programme: course-7-web/11_validation_wire.js}}

### 5. Execution and Results

{{output: course-7-web/11_validation.html}}

The runner asserts that `asha@` is rejected and `asha@nri.ac.in` accepted;
that `9876543210` passes and `1234567890` fails (an Indian mobile starts 6–9);
that `Passw0rd!` passes and `password` fails; and that mismatched passwords
produce exactly the `confirm` error. The driver tries the same values in the page.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Each wrong field gets its message and a red border; with every field right, the page reports "All fields valid."
</div>


## Experiment 12 — Time-based greeting

### 1. Question

Show a greeting that changes with the time of day.

### 2. Aim

Greet by the hour in JavaScript, in a way that can be tested at every hour.

### 3. Steps

**In HTML**, `12_greeting.html`:

1. **Set up the head: charset, viewport, title and styles.**
2. **A card for the greeting and the clock.**
3. **Greet by the hour, with the name.**
4. **Tick the clock every second.**

**In JavaScript**, `12_greeting.js`:

1. **Choose the greeting from the hour.**
2. **Give a class for each period of the day.**
3. **Add the name.**
4. **Format the time.**

<div class="formula" markdown="1">
<span class="label">THE WHOLE TRICK</span>

**Taking `hour` as a parameter with a default is the whole trick.** A function
that reads the clock internally can only be tested by waiting until 9 am; this
one is asserted at every boundary — 0, 11, 12, 16, 17, 20, 21, 23 — in a
fraction of a second, and still behaves identically when called with no
arguments in the page.

That is a general lesson, not a JavaScript one: **push the unpredictable input
to the edge of the function**, and the logic inside becomes testable. The same
idea makes Python for Data Analysis and Visualization's data pipelines testable.
</div>


### 4. Programme

**In HTML**, `12_greeting.html`:

{{programme: course-7-web/12_greeting.html}}

**In JavaScript**, `12_greeting.js`:

{{programme: course-7-web/12_greeting.js}}

### 5. Execution and Results

{{output: course-7-web/12_greeting.html}}

The page's own "Pretend the hour is" list does in the browser what the parameter does in
the runner.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

At 09:00 the page says "Good morning!"; with a name and the hour set to 14, 19 and 22, it says good afternoon, evening and night, and restyles itself for each.
</div>


## Experiment 13 — Array and object manipulation

### 1. Question

Manipulate an array of objects in JavaScript: add, delete, sort and search.

### 2. Aim

Keep a list of students in an array, and change it only through pure functions.

### 3. Steps

**In HTML**, `13_arrays.html`:

1. **Set up the head, and link the stylesheet.**
2. **A form to add a student, a search box and a table.**
3. **Draw the table and the summary.**
4. **Add a student.**
5. **Delete a student.**
6. **Search, and sort by a column.**

**In JavaScript**, `13_arrays.js`:

1. **Start with five students.**
2. **Add, remove and update, each returning a new array.**
3. **Sort by any key.**
4. **Search, find and group.**
5. **Summarise.**

<div class="formula" markdown="1">
<span class="label">PURE FUNCTIONS, AND THE COMPARATOR</span>

Every function is **pure**: it takes the list and returns a new one rather
than mutating in place. That is why `addStudent` spreads instead of pushing,
and why `sortBy` copies with `[...list]` before sorting — `sort` mutates, and
a sort that silently reorders the caller's array is a bug that surfaces three
functions away.

The comparator branches on type because **`sort()` with no comparator compares
as strings**, so `[10, 9, 100]` sorts to `[10, 100, 9]`. Numbers need `x - y`;
strings need `localeCompare`, which also handles accents correctly.
</div>


### 4. Programme

**In HTML**, `13_arrays.html`:

{{programme: course-7-web/13_arrays.html}}

**In JavaScript**, `13_arrays.js`:

{{programme: course-7-web/13_arrays.js}}

### 5. Execution and Results

{{output: course-7-web/13_arrays.html}}

Asserted by the runner against a five-student fixture: the average is 62.4,
the top scorer is Meena, adding a duplicate roll throws, and `summary([])`
returns nulls rather than `NaN`. The page shows the same.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The five students average 62.4, with Meena top; a sixth is added, a duplicate roll is refused, the table sorts by marks and filters by name, and a delete restores the five.
</div>


## Experiment 14 — Render JSON as a table

### 1. Question

Fetch student information held in a JSON file, and display it as a table.

### 2. Aim

Load JSON with `fetch()`, and draw it into a table safely and efficiently.

### 3. Steps

**In HTML**, `14_json_table.html`:

1. **Set up the head, and link the stylesheet.**
2. **A search box, a status line and the table.**
3. **Draw the rows that match, in order.**
4. **Filter, and sort by a column.**

**In JavaScript**, `14_json_table.js`:

1. **Turn the JSON into rows.**
2. **Sort and filter the rows.**
3. **Summarise them.**
4. **Draw them, as text.**
5. **Load the file, checking the response.**

<div class="formula" markdown="1">
<span class="label">THREE DELIBERATE CHOICES</span>

**`textContent`, not `innerHTML`.** The data came from a file or an API, so a
`name` of `<img src=x onerror=alert(1)>` must render as text. This is the XSS
rule from Unit 4, in the one place students most often break it.

**A `DocumentFragment`.** Rows are built off-document and inserted once, so
the browser reflows once rather than once per row.

**Optional chaining on `s.marks?.maths`.** One student in the fixture has no
`marks` object at all; without the `?.` the whole render throws and the page
goes blank instead of showing a dash.
</div>


### 4. Programme

**In HTML**, `14_json_table.html`:

{{programme: course-7-web/14_json_table.html}}

**In JavaScript**, `14_json_table.js`:

{{programme: course-7-web/14_json_table.js}}

### 5. Execution and Results

{{output: course-7-web/14_json_table.html}}

The `doc` parameter defaults to `document` but can be passed jsdom's document,
which is how the runner tests this without a browser. Bhanu Prakash, the student with no
marks, shows two dashes and a total of 0, and is left out of the average.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The five students load from `students.json`, with an average total of 155.5 and Meena Devi top; the table sorts by total and filters to the Statistics students.
</div>


## Experiment 15 — Fetch weather data from an open API

### 1. Question

Fetch real-time weather data from an open API, and display it.

### 2. Aim

Call a web API with `fetch()`, check the response, and show its data.

### 3. Steps

**In HTML**, `15_weather.html`:

1. **Set up the head, and link the stylesheet.**
2. **A form for the city and the API key.**
3. **A card for the weather.**
4. **Show a summary on the card.**
5. **Fetch the weather on submit.**
6. **Or show the saved sample.**

**In JavaScript**, `15_weather.js`:

1. **Pick the fields to show from the response.**
2. **Convert to Fahrenheit.**
3. **Build the request, and fetch it.**

<div class="formula" markdown="1">
<span class="label">THE POINT OF THE EXPERIMENT</span>

The runner has no network access and no API key, so it tests `summarise`
against a **saved sample response**, and tests `fetchWeather` with a stub
`fetchFn` that returns `{ ok: false, status: 404 }` — asserting that it throws
rather than returning undefined.

That split is the point of the experiment. **Separating the network call from
the parsing makes the parsing testable**, and the parsing is where the bugs
actually are.
</div>


### 4. Programme

**In HTML**, `15_weather.html`:

{{programme: course-7-web/15_weather.html}}

**In JavaScript**, `15_weather.js`:

{{programme: course-7-web/15_weather.js}}

### 5. Execution and Results

{{output: course-7-web/15_weather.html}}

The page has the same split: **Use saved sample** puts the saved response through the same
`summarise()`. The driver presses it, then tries a real fetch, which it stops, as the API cannot
be reached from here; the page says so in its status line rather than going blank.

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

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The sample shows Vijayawada at 30 °C, feeling like 34 °C (93.2 °F), in moderate rain; a fetch that cannot reach the API is reported as "Failed to fetch".
</div>


## Experiment 16 — jQuery DOM manipulation

### 1. Question

Use jQuery to hide, show, fade, slide and toggle elements.

### 2. Aim

Change a page with jQuery's effects, chaining and event delegation.

### 3. Steps

**In HTML**, `16_jquery.html`:

1. **Set up the head, and link the stylesheet.**
2. **A panel to hide, show, fade, slide and toggle.**
3. **A box to animate.**
4. **A message to change by chaining.**
5. **A table whose rows can be added and deleted.**
6. **Load jQuery.**
7. **Wire every button with jQuery.**
8. **Or, where jQuery did not load, with plain JavaScript.**

**In CSS**, `16_jquery.css`:

1. **Style the page and the buttons.**
2. **The panel's states, for the library-free version.**
3. **The box, the table, and the message.**

**In JavaScript**, `16_jquery_native.js`:

1. **Hide, show and toggle.**
2. **Fade and slide.**
3. **Set a message.**
4. **Delete rows by delegation.**
5. **Move, append and empty.**

<div class="formula" markdown="1">
<span class="label">FOUR EXAM POINTS</span>

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
</div>


### 4. Programme

**In HTML**, `16_jquery.html`:

{{programme: course-7-web/16_jquery.html}}

**In CSS**, `16_jquery.css`:

{{programme: course-7-web/16_jquery.css}}

**In JavaScript**, `16_jquery_native.js`:

{{programme: course-7-web/16_jquery_native.js}}

### 5. Execution and Results

{{output: course-7-web/16_jquery.html}}

**`16_jquery_native.js` is the same behaviour with no library**, and it is
what the runner executes under jsdom — jQuery's animation queue depends on
timing that jsdom does not reproduce faithfully, while the native version's
class toggles can be asserted directly. Asserted: clicking a `.delete-btn` adds `fading`
to the correct `<tr>`, and a click elsewhere in the table does nothing.

In Chromium, jQuery loads, so the jQuery version is the one that runs, and its animations play
out in real time; the clock is not fixed for this page, as jQuery times its animations by it.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

jQuery 3.7.1 loads; each effect hides or shows the panel, `animate()` moves the box to 250 px, the chained message reads "Saved successfully", and a row added after the page loaded can be deleted.
</div>


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
