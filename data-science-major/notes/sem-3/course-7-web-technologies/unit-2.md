# Unit 2 — CSS

**Syllabus topics:** CSS home, introduction, syntax, CSS combinators, colors,
background, borders, margins, padding, height/width, text, fonts, tables, lists,
position, overflow, float, pseudo class, pseudo elements, opacity, tool tips,
image gallery, CSS forms, CSS counters.

---

## 2.1 What CSS is and why it exists

### 🎯 The big idea

HTML says *what* something is. CSS says *what it should look like*. Separating
the two means one stylesheet can restyle a thousand pages.

Before CSS, presentation lived in HTML itself — `<font color="red">`,
`<center>`, `bgcolor` attributes. Changing a site's colour scheme meant editing
every page. **CSS** (Cascading Style Sheets, 1996) moved presentation into its
own file, and the `<font>` tag is now obsolete.

### The three ways to attach CSS

| Method | Syntax | Scope | Use |
|---|---|---|---|
| **Inline** | `<p style="color:red">` | That one element | Almost never |
| **Internal** | `<style>` in `<head>` | That one page | Single-page demos |
| **External** | `<link rel="stylesheet" href="styles.css">` | Every page that links it | **Always, in real work** |

```html
<head>
  <link rel="stylesheet" href="styles.css">
  <style>
    p { color: navy; }
  </style>
</head>
<body>
  <p style="color: red;">This paragraph is red.</p>
</body>
```

The red wins. That is the cascade at work, and §2.4 explains why.

### 💡 Why "cascading"?

Because several rules can target the same element, and the browser must decide
which wins. Rules "cascade" down through a defined order of precedence rather
than fighting. Understanding that order is the single most useful CSS skill —
it is the difference between fixing a style and adding `!important` until
something moves.

## 2.2 Syntax

```css
selector {
  property: value;
  property: value;
}
```

```css
h1 {
  color: #2b4c7e;
  font-size: 32px;
  text-align: center;
}
```

- **Selector** — which elements the rule applies to (`h1`)
- **Declaration block** — the braces
- **Declaration** — one `property: value` pair
- Declarations end in `;`. The last one's semicolon is optional but **always
  write it** — you will add another declaration later and forget.
- Comments are `/* … */` only. `//` is **not** a CSS comment; it silently
  breaks the rest of the rule in some parsers.

## 2.3 Selectors

| Selector | Example | Matches |
|---|---|---|
| Universal | `*` | Every element |
| Type | `p` | All `<p>` |
| Class | `.note` | `class="note"` |
| ID | `#header` | `id="header"` |
| Grouping | `h1, h2, h3` | All three |
| Attribute | `input[type="text"]` | Text inputs |
| Attribute prefix | `a[href^="https"]` | Links starting with https |
| Attribute suffix | `a[href$=".pdf"]` | Links ending in .pdf |
| Attribute contains | `a[href*="syllabus"]` | Substring match |

### 🔢 CSS combinators

The syllabus names these explicitly. There are exactly **four**, and the exam
question is almost always "distinguish them".

| Combinator | Symbol | Meaning | Example |
|---|:---:|---|---|
| Descendant | space | Anywhere inside | `div p` |
| Child | `>` | **Direct** child only | `div > p` |
| Adjacent sibling | `+` | The **next** sibling | `h1 + p` |
| General sibling | `~` | **All** later siblings | `h1 ~ p` |

Given this markup:

```html
<div>
  <p>A</p>
  <section><p>B</p></section>
</div>
<h1>Title</h1>
<p>C</p>
<p>D</p>
```

| Selector | Matches |
|---|---|
| `div p` | A **and** B — descendant, any depth |
| `div > p` | A only — B's parent is `<section>`, not `<div>` |
| `h1 + p` | C only — the immediately following sibling |
| `h1 ~ p` | C **and** D — all following siblings |

**Worked example.** Style only the first paragraph after each heading, in grey.

```css
h2 + p { color: #666; font-style: italic; }
```

This is the standard "lede paragraph" pattern, and it needs no extra class in
the HTML at all.

## 2.4 Specificity and the cascade

### 🔢 The formula

When two rules set the same property on the same element, the winner is decided
in this order:

1. **`!important`** declarations beat everything (avoid them)
2. **Specificity** — count `(a, b, c)`:
   - `a` = number of **ID** selectors
   - `b` = number of **class**, attribute and pseudo-class selectors
   - `c` = number of **element** and pseudo-element selectors
   Compare left to right; the first difference decides.
3. **Source order** — on an exact tie, the rule written **last** wins.

Inline `style=` behaves as if it had specificity `(1,0,0,0)` — higher than any
ID selector.

| Selector | (a, b, c) | Value |
|---|---|---|
| `p` | (0, 0, 1) | 1 |
| `.note` | (0, 1, 0) | 10 |
| `p.note` | (0, 1, 1) | 11 |
| `#main p` | (1, 0, 1) | 101 |
| `#main .note` | (1, 1, 0) | 110 |
| `style="…"` | inline | wins over all above |

The "value" column is the common shorthand taught in exams (units, tens,
hundreds). It is a useful approximation but technically wrong — 11 class
selectors do **not** beat one ID. Compare column by column instead.

**Worked example.** Which colour wins?

```html
<p id="intro" class="lead">Hello</p>
```
```css
p          { color: black; }   /* (0,0,1) */
.lead      { color: blue;  }   /* (0,1,0) */
#intro     { color: green; }   /* (1,0,0) */
p.lead     { color: red;   }   /* (0,1,1) */
```

**Solution.** Green. `#intro` is (1,0,0); nothing else has an ID, and `a` is
compared first.

### ⚠️ On `!important`

It exists, and using it is almost always a mistake. It wins, so the next
developer must write `!important` too, and then you have two rules that both
win and no way to resolve them but source order. Fix specificity instead.

## 2.5 Colours

| Notation | Example | Notes |
|---|---|---|
| Keyword | `red`, `rebeccapurple` | 140 named colours |
| Hex | `#ff0000` | `#RRGGBB`, 00–ff each |
| Short hex | `#f00` | Each digit doubled |
| RGB | `rgb(255, 0, 0)` | 0–255 |
| RGBA | `rgba(255, 0, 0, 0.5)` | Alpha 0–1 |
| HSL | `hsl(0, 100%, 50%)` | Hue 0–360, sat %, light % |
| HSLA | `hsla(0, 100%, 50%, 0.5)` | With alpha |

**HSL is the one worth knowing.** To make a colour lighter, raise the third
number; to make a colour scheme, hold hue and vary the rest. Doing the same in
hex requires arithmetic.

```css
.btn         { background: hsl(210, 70%, 45%); }
.btn:hover   { background: hsl(210, 70%, 35%); }  /* just darker */
.btn:disabled{ background: hsl(210, 10%, 60%); }  /* just greyer */
```

## 2.6 The box model

### 🎯 The big idea

Every element is a rectangle made of four nested layers: content, padding,
border, margin. Almost every layout bug is a misunderstanding of this diagram.

```
        ┌─────────────── margin ───────────────┐
        │  ┌──────────── border ────────────┐  │
        │  │  ┌───────── padding ────────┐  │  │
        │  │  │                          │  │  │
        │  │  │        CONTENT           │  │  │
        │  │  │      width × height      │  │  │
        │  │  └──────────────────────────┘  │  │
        │  └────────────────────────────────┘  │
        └──────────────────────────────────────┘
```

| Layer | Property | Background? | Collapses? |
|---|---|---|---|
| Content | `width`, `height` | Yes | — |
| Padding | `padding` | **Yes** | No |
| Border | `border` | It *is* the border | No |
| Margin | `margin` | **No — transparent** | **Yes, vertically** |

**Padding is inside the background; margin is outside it.** That is the
practical difference and the standard two-mark answer.

### 🔢 Computing total width

By default (`box-sizing: content-box`):

```
total width = margin-left + border-left + padding-left
            + width
            + padding-right + border-right + margin-right
```

**Worked example.**

```css
div { width: 300px; padding: 20px; border: 5px solid; margin: 10px; }
```

Rendered width of the border box = 5 + 20 + 300 + 20 + 5 = **350px**.
Horizontal space occupied including margins = 10 + 350 + 10 = **370px**.

This surprises everyone, which is why virtually every real stylesheet starts:

```css
*, *::before, *::after { box-sizing: border-box; }
```

With `border-box`, `width: 300px` means the border box is 300px and padding
eats into it. Content becomes 300 − 20 − 20 − 5 − 5 = **250px**. Set it once
and stop doing arithmetic.

### Shorthand order

`margin` and `padding` take one to four values, clockwise from the top:

| Values | Meaning |
|---|---|
| `margin: 10px` | All four sides |
| `margin: 10px 20px` | top/bottom, left/right |
| `margin: 10px 20px 30px` | top, left/right, bottom |
| `margin: 10px 20px 30px 40px` | top, right, bottom, left |

Remember **TRouBLe** — Top, Right, Bottom, Left.

### ⚠️ Margin collapse

Adjacent **vertical** margins collapse to the larger of the two, not their sum.

```css
h2 { margin-bottom: 30px; }
p  { margin-top: 20px; }
```

The gap between them is **30px**, not 50px. Horizontal margins never collapse.
Padding never collapses. This is asked in exams and it catches everyone once.

## 2.7 Borders

```css
border: 2px solid #333;              /* width style colour */
border-width: 1px 2px;
border-style: dashed;
border-color: red;
border-radius: 8px;                  /* rounded corners */
border-radius: 50%;                  /* a circle, if width == height */
```

Border styles: `none`, `solid`, `dashed`, `dotted`, `double`, `groove`,
`ridge`, `inset`, `outset`, `hidden`.

**`border-style` is required.** `border: 2px red` renders nothing, because the
default style is `none`. That is the single most common CSS beginner bug.

## 2.8 Background

```css
.hero {
  background-color: #eef;
  background-image: url("banner.jpg");
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
  background-attachment: fixed;
}
/* shorthand */
.hero { background: #eef url("banner.jpg") no-repeat center/cover fixed; }
```

| Property | Useful values |
|---|---|
| `background-repeat` | `repeat`, `repeat-x`, `repeat-y`, `no-repeat` |
| `background-position` | `left/center/right top/center/bottom`, `50% 20%`, `10px 20px` |
| `background-size` | `auto`, `cover`, `contain`, `100% 200px` |
| `background-attachment` | `scroll`, `fixed`, `local` |

`cover` fills the box and may crop; `contain` fits entirely and may leave gaps.

**Always set `background-color` as well as an image.** If the image fails to
load, the text must still be readable.

Gradients count as images:

```css
.card { background: linear-gradient(to bottom, #fff, #e8eef6); }
```

## 2.9 Text and fonts

| Property | Values |
|---|---|
| `color` | Any colour notation |
| `text-align` | `left`, `right`, `center`, `justify` |
| `text-decoration` | `none`, `underline`, `overline`, `line-through` |
| `text-transform` | `uppercase`, `lowercase`, `capitalize` |
| `text-indent` | Length — first-line indent |
| `letter-spacing`, `word-spacing` | Length |
| `line-height` | **Unitless number preferred**: `1.6` |
| `text-shadow` | `2px 2px 4px #999` |
| `white-space` | `normal`, `nowrap`, `pre`, `pre-wrap` |

| Font property | Values |
|---|---|
| `font-family` | Stack, generic last |
| `font-size` | `16px`, `1rem`, `1.2em`, `120%` |
| `font-weight` | `normal`, `bold`, `100`–`900` |
| `font-style` | `normal`, `italic`, `oblique` |
| `font-variant` | `small-caps` |
| `font` | `italic bold 16px/1.5 Georgia, serif` |

### Font stacks

```css
body { font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
```

The browser tries each in turn. **Always end with a generic family** —
`serif`, `sans-serif`, `monospace`, `cursive`, `fantasy` — so there is a
guaranteed fallback. Quote names containing spaces.

### 💡 px vs em vs rem

| Unit | Relative to | Compounds? |
|---|---|---|
| `px` | Nothing — absolute | No |
| `em` | The **parent's** font size | **Yes** |
| `rem` | The **root** `<html>` font size | No |
| `%` | Parent (context-dependent) | Yes |
| `vw` / `vh` | 1% of viewport width / height | No |

`em` compounding bites: nest three elements each at `font-size: 1.2em` and the
innermost is 1.2³ = **1.728×** the base. `rem` avoids this entirely, which is
why modern stylesheets use `rem` for type and `em` only for spacing that should
scale with its own text.

**Worked example.** With `html { font-size: 16px; }`, what is `1.5rem`?
**Solution.** 1.5 × 16 = **24px**, regardless of nesting depth.

## 2.10 height, width and overflow

```css
.box {
  width: 60%;
  max-width: 800px;      /* never wider than this */
  min-width: 320px;      /* never narrower */
  height: auto;
  min-height: 200px;
}
```

**`max-width` is the responsive design workhorse.** `width: 800px` breaks on a
phone; `width: 100%; max-width: 800px` does not.

### overflow

What happens when content is bigger than its box:

| Value | Behaviour |
|---|---|
| `visible` | Spills out (default) |
| `hidden` | Clipped, no scrollbar |
| `scroll` | Scrollbars always shown |
| `auto` | Scrollbars only when needed — **usually what you want** |

`overflow-x` and `overflow-y` set the axes separately. A wide table inside
`overflow-x: auto` scrolls itself instead of forcing the whole page sideways.

## 2.11 Positioning

### 🔢 The five position values

| Value | Positioned relative to | In normal flow? |
|---|---|---|
| `static` | Nothing — default | Yes |
| `relative` | **Its own normal position** | **Yes** — space reserved |
| `absolute` | Nearest positioned **ancestor** | **No** — removed |
| `fixed` | The **viewport** | No |
| `sticky` | Flow, then viewport past a threshold | Yes |

`top`, `right`, `bottom`, `left` and `z-index` only apply to non-`static`
elements. Setting `left: 20px` on a static element does nothing at all.

**The relative/absolute pairing** is the pattern to memorise:

```css
.card     { position: relative; }              /* the anchor */
.card .tag{ position: absolute; top: 8px; right: 8px; }
```

Without `position: relative` on `.card`, the tag positions itself against the
page, not the card. Nearly every "why is my badge in the corner of the screen"
question is this.

`z-index` stacks positioned elements; higher is nearer the viewer. It only
compares elements within the same **stacking context**, which is why a
`z-index: 9999` sometimes still loses.

## 2.12 float

`float` pulls an element to one side and lets text wrap around it. It was
invented for images in text and then abused for page layout for fifteen years.

```css
img.left { float: left; margin: 0 15px 10px 0; }
```

**The collapsing-parent problem.** A floated child is out of normal flow, so
its parent computes a height of zero. Three fixes, in order of modernity:

```css
.parent { overflow: auto; }                    /* the old hack */
.parent { display: flow-root; }                /* the modern, explicit fix */
.parent::after { content: ""; display: block; clear: both; }  /* clearfix */
```

`clear: left | right | both` on a later element pushes it below the floats.

### ⚠️ Do not use float for layout

Use **Flexbox** for one dimension and **Grid** for two. The syllabus does not
name them in the unit list, but the prescribed practical activity explicitly
says "Flexbox/Grid", and lab experiment 8 requires them.

```css
/* one row, spaced out, wrapping on small screens */
.row { display: flex; gap: 1rem; flex-wrap: wrap; justify-content: space-between; }
.row > * { flex: 1 1 250px; }

/* a responsive card grid with no media queries at all */
.grid { display: grid; gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }
```

That second rule is worth memorising: `auto-fit` + `minmax` fits as many
columns as will hold 240px and stretches them to fill. It is a complete
responsive grid in three lines.

## 2.13 Pseudo-classes

A **pseudo-class** selects an element in a particular **state**. One colon.

| Pseudo-class | Matches |
|---|---|
| `:link` | Unvisited link |
| `:visited` | Visited link |
| `:hover` | Pointer over it |
| `:active` | Being clicked |
| `:focus` | Has keyboard focus |
| `:focus-visible` | Focused **via keyboard** — no ring on mouse click |
| `:first-child` | First child of its parent |
| `:last-child` | Last child |
| `:nth-child(n)` | The nth; also `odd`, `even`, `3n+1` |
| `:nth-of-type(n)` | The nth of that element type |
| `:not(sel)` | Everything except |
| `:checked` | Checked checkbox/radio |
| `:disabled`, `:enabled` | Form state |
| `:required`, `:valid`, `:invalid` | Validation state |

### ⚠️ LVHA — link pseudo-class order

`:link`, `:visited`, `:hover`, `:active` must be written **in that order**.
They have equal specificity, so a `:hover` rule written before `:visited` will
be overridden on visited links and the hover will appear broken. Mnemonic:
**Lo**Ve **HA**te.

```css
a:link    { color: #06c; }
a:visited { color: #639; }
a:hover   { color: #04a; text-decoration: underline; }
a:active  { color: #c00; }
```

**Worked example.** Zebra-stripe a table without adding any classes.

```css
tbody tr:nth-child(even) { background: #f4f6f9; }
tbody tr:hover           { background: #e8eef6; }
```

`:nth-child()` counts from 1, so `even` is rows 2, 4, 6…

**Never remove focus outlines.** `:focus { outline: none; }` makes a page
unusable by keyboard. Replace the ring, do not delete it:

```css
:focus-visible { outline: 3px solid #2b8a3e; outline-offset: 2px; }
```

## 2.14 Pseudo-elements

A **pseudo-element** styles a *part* of an element, or inserts content. Two
colons in CSS3 (`::before`), though one still works for the original four.

| Pseudo-element | Styles |
|---|---|
| `::before` | Generated content before the content |
| `::after` | Generated content after |
| `::first-line` | The first rendered line |
| `::first-letter` | The first letter — drop caps |
| `::selection` | Text the user has highlighted |
| `::placeholder` | Placeholder text in an input |
| `::marker` | The bullet or number of a list item |

**`content` is mandatory** for `::before` and `::after`. Omit it and nothing
renders, even with a width and a background.

```css
.external::after   { content: " ↗"; }
a[href$=".pdf"]::after { content: " (PDF)"; font-size: 0.85em; color: #666; }
blockquote::before { content: "\201C"; font-size: 3rem; color: #ccd; }
p::first-letter    { font-size: 3rem; float: left; line-height: 1; }
```

Generated content is **not in the DOM** and is generally not read aloud or
copied. Never put meaningful text in it.

### 🎯 Pseudo-class vs pseudo-element

This distinction is a guaranteed two-mark question.

| | Pseudo-class | Pseudo-element |
|---|---|---|
| Colons | One — `:hover` | Two — `::before` |
| Selects | A **whole element** in a state | A **part** of an element, or inserted content |
| Exists in DOM | Yes | No |
| Example | `a:hover` | `p::first-letter` |
| Count per selector | Many | One (traditionally) |

## 2.15 Styling tables

```css
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #d6dbe4; padding: 8px 10px; text-align: left; }
th { background: #eef2f7; font-weight: 600; }
tbody tr:nth-child(even) { background: #fafbfd; }
caption { caption-side: bottom; font-size: .9em; color: #666; }
```

**`border-collapse`** is the property that matters:

| Value | Effect |
|---|---|
| `separate` (default) | Each cell has its own border — doubled lines |
| `collapse` | Adjacent borders merge into one |

With `separate`, `border-spacing: 4px` controls the gap. With `collapse`,
`border-spacing` is ignored.

## 2.16 Styling lists

```css
ul { list-style-type: square; }
ol { list-style-type: upper-roman; }
ul.plain { list-style: none; padding-left: 0; }
li { margin-bottom: .4rem; }
ul.icons { list-style: none; }
ul.icons li::before { content: "✔ "; color: #2b8a3e; }
```

| Property | Values |
|---|---|
| `list-style-type` | `disc`, `circle`, `square`, `decimal`, `lower-alpha`, `upper-roman`, `none` |
| `list-style-position` | `outside` (default), `inside` |
| `list-style-image` | `url(bullet.png)` |
| `list-style` | Shorthand for all three |

Removing bullets with `list-style: none` leaves the indent behind — you almost
always want `padding-left: 0` too.

## 2.17 Opacity

```css
.faded  { opacity: 0.5; }                    /* the whole element, children too */
.bg     { background: rgba(0, 0, 0, 0.5); }  /* only the background */
```

### ⚠️ `opacity` vs `rgba()`

`opacity` fades the element **and everything inside it**, text included, and it
cannot be undone by a child. `rgba()` (or `hsla()`) fades only the colour it is
applied to. For a translucent overlay with crisp white text, `rgba()` is the
only correct choice.

```css
/* WRONG — the caption text goes half-transparent too */
.overlay { background: black; opacity: .5; }
/* RIGHT — background fades, text stays solid */
.overlay { background: rgba(0, 0, 0, .5); color: #fff; }
```

`opacity: 0` also keeps the element clickable and in the layout, unlike
`visibility: hidden` (unclickable, still occupies space) and `display: none`
(gone entirely).

## 2.18 Tooltips

A pure-CSS tooltip, which the syllabus names explicitly, is the
relative/absolute pattern plus a `:hover` and a pseudo-element.

```html
<span class="tip" data-tip="Coefficient of determination">R²</span>
```
```css
.tip { position: relative; border-bottom: 1px dotted #888; cursor: help; }

.tip::after {
  content: attr(data-tip);          /* pull the text from the attribute */
  position: absolute;
  bottom: 125%; left: 50%;
  transform: translateX(-50%);
  background: #333; color: #fff;
  padding: 6px 10px; border-radius: 4px;
  white-space: nowrap;
  opacity: 0; visibility: hidden;
  transition: opacity .25s;
}
.tip:hover::after,
.tip:focus::after { opacity: 1; visibility: visible; }
```

Three ideas do all the work: `attr()` reads an HTML attribute into `content`;
`transform: translateX(-50%)` centres the box on its anchor whatever its width;
and `visibility` toggles alongside `opacity` so the hidden tooltip cannot be
clicked.

## 2.19 Image gallery

```html
<div class="gallery">
  <figure><img src="1.jpg" alt="Sunrise"><figcaption>Sunrise</figcaption></figure>
  <figure><img src="2.jpg" alt="Harbour"><figcaption>Harbour</figcaption></figure>
</div>
```
```css
.gallery { display: grid; gap: 12px;
           grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
.gallery figure { margin: 0; border: 1px solid #ddd; padding: 6px;
                  background: #fff; overflow: hidden; }
.gallery img { width: 100%; height: 160px; object-fit: cover; display: block;
               transition: transform .3s; }
.gallery figure:hover img { transform: scale(1.08); }
.gallery figcaption { font-size: .85rem; text-align: center; padding-top: 6px; }
```

`object-fit: cover` is the important one: it makes images of different aspect
ratios fill an identical box by cropping, instead of stretching. `display:
block` on the image removes the mysterious few pixels of space underneath it
(inline elements sit on the text baseline, which leaves room for descenders).

## 2.20 CSS forms

```css
input[type="text"], input[type="email"], input[type="password"], select, textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccd3dd;
  border-radius: 6px;
  font: inherit;               /* forms do NOT inherit fonts by default */
  background: #fff;
}
input:focus, select:focus, textarea:focus {
  border-color: #2b4c7e;
  outline: 3px solid rgba(43, 76, 126, .25);
  outline-offset: 0;
}
input:invalid:not(:placeholder-shown) { border-color: #c92a2a; }
input:valid:not(:placeholder-shown)   { border-color: #2b8a3e; }
label { display: block; margin-bottom: 4px; font-weight: 600; }
button { padding: 10px 18px; border: 0; border-radius: 6px;
         background: #2b4c7e; color: #fff; cursor: pointer; }
button:hover { background: #1f3a63; }
button:disabled { background: #aab; cursor: not-allowed; }
```

Two things students consistently miss. **`font: inherit`** — form controls use
the operating system's font unless you say otherwise, so an unstyled input
looks alien next to your text. And **`:not(:placeholder-shown)`** — without it,
`:invalid` fires on an empty required field the instant the page loads, and the
form is red before the user has typed anything.

## 2.21 CSS counters

Counters let CSS number things automatically — sections, figures, nested lists
— without touching the HTML.

```css
body    { counter-reset: section; }         /* create and zero it */
h2::before {
  counter-increment: section;               /* add 1 */
  content: "Section " counter(section) ". "; /* display it */
}
```

Nested numbering (1.1, 1.2, 2.1) uses `counters()` — plural — with a separator:

```css
ol.outline { counter-reset: item; list-style: none; }
ol.outline li::before {
  counter-increment: item;
  content: counters(item, ".") " ";
  font-weight: bold;
}
```

| Property / function | Purpose |
|---|---|
| `counter-reset: name [n]` | Create or reset (default 0) |
| `counter-increment: name [n]` | Add (default 1) |
| `counter(name[, style])` | Value of the innermost |
| `counters(name, sep[, style])` | All nested values joined |

`counter-reset` on the wrong element is the usual bug: reset on the **common
ancestor**, increment on the item. Resetting on the item itself zeroes it every
time and every number comes out 1.

## 2.22 Responsive design and media queries

```css
/* mobile first: base rules are the small-screen rules */
.container { padding: 1rem; }

@media (min-width: 768px) {
  .container { padding: 2rem; max-width: 720px; margin: 0 auto; }
}
@media (min-width: 1100px) {
  .container { max-width: 1040px; }
}
@media print {
  nav, .no-print { display: none; }
}
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
```

**Mobile-first** means writing the small-screen layout as the default and
adding complexity with `min-width`. It produces less CSS than the reverse, and
it degrades safely on devices you did not anticipate.

None of it works without this in the HTML `<head>`:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

Without it a phone pretends to be 980px wide and renders your desktop layout
shrunk to illegibility. Omitting it is the number-one reason a "responsive"
page is not.

## 2.23 Transitions and simple animation

The syllabus puts animation in Unit 4 with events, but the CSS half belongs
here.

```css
.btn { background: #2b4c7e; transition: background .25s ease, transform .25s ease; }
.btn:hover { background: #1f3a63; transform: translateY(-2px); }

@keyframes fade-in {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: none; }
}
.card { animation: fade-in .4s ease-out both; }
```

`transition: property duration timing-function delay`. Animate `transform` and
`opacity` where you can — the browser can do those on the GPU without
recalculating layout. Animating `width`, `height`, `top` or `margin` forces a
reflow on every frame and stutters.

---

## Practice problems

### Problem 1

Given:

```html
<div class="wrap">
  <p class="intro">One</p>
  <p>Two</p>
  <span>Three</span>
  <p>Four</p>
</div>
```

Which elements do these select?
(a) `.wrap p` (b) `.wrap > p` (c) `.intro + p` (d) `.intro ~ p` (e) `p:last-child`

**Solution.**

(a) One, Two, Four — all `<p>` descendants.
(b) One, Two, Four — they are all direct children, so the same set here.
(c) Two — the immediately following sibling `<p>`.
(d) Two and Four — all later `<p>` siblings.
(e) Four — it is the last child of `.wrap` **and** a `<p>`. Note `p:last-child`
means "a `p` that is its parent's last child", not "the last `p`". If a
`<span>` came last, this would match nothing.

### Problem 2

```css
div { width: 200px; padding: 15px; border: 3px solid; margin: 12px; }
```

Give the rendered border-box width under `content-box` and under `border-box`,
and the total horizontal space consumed in each case.

**Solution.**

`content-box` (default): border box = 3 + 15 + 200 + 15 + 3 = **236px**;
with margins, 12 + 236 + 12 = **260px**.

`border-box`: border box = **200px** exactly; content shrinks to
200 − 15 − 15 − 3 − 3 = **164px**; with margins, 12 + 200 + 12 = **224px**.

### Problem 3

Write CSS that produces a badge in the top-right corner of every `.card`,
without changing the HTML, given `<div class="card" data-badge="NEW">…</div>`.

**Solution.**

```css
.card { position: relative; }
.card[data-badge]::after {
  content: attr(data-badge);
  position: absolute; top: 8px; right: 8px;
  background: #2b8a3e; color: #fff;
  font-size: .7rem; font-weight: 700; letter-spacing: .04em;
  padding: 3px 7px; border-radius: 999px;
}
```

The attribute selector means cards without a `data-badge` get nothing, so no
empty green pill appears on them.

---

## Exam questions from this unit

**Two marks**

1. What does "cascading" mean in Cascading Style Sheets?
2. Distinguish inline, internal and external CSS.
3. Distinguish padding from margin.
4. Distinguish a pseudo-class from a pseudo-element.
5. Distinguish `opacity` from `rgba()`.
6. What is `border-collapse`?
7. What is margin collapse?
8. Distinguish `em` from `rem`.

**Five marks**

1. Explain the four CSS combinators with examples.
2. Explain the CSS box model and compute the total width of a given element.
3. Explain CSS positioning — all five values — with examples.
4. Explain specificity and resolve a given conflict.
5. Explain CSS counters with an example.
6. Explain float, the collapsing-parent problem, and `clear`.

**Ten marks**

1. Design a responsive student registration form with CSS, explaining every
   selector used.
2. Explain pseudo-classes and pseudo-elements exhaustively with examples, and
   build a CSS-only tooltip.
3. Explain media queries and mobile-first responsive design, with an image
   gallery as the example.

## Mistakes that cost marks

- `border: 2px red` with no style — renders nothing
- Writing `//` comments in CSS
- Expecting `top`/`left` to work on a `static` element
- Forgetting `position: relative` on the parent of an absolute child
- Writing the link pseudo-classes out of LVHA order
- Omitting `content` on `::before` / `::after`
- Adding vertical margins and expecting them to sum
- Using `opacity` where `rgba()` was needed
- Omitting the viewport `<meta>` and calling the page responsive
- `outline: none` on `:focus`, destroying keyboard accessibility
- Using `float` for whole-page layout instead of Flexbox or Grid
- Forgetting `font: inherit` on form controls
- Resetting a counter on the item being counted, so every number is 1
