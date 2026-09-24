# Unit 3 — Word Processing and Presentations

**Syllabus topics:** Word processing basics — using MS Word/Google Docs:
formatting, styles, tables, mail merge. Presentation tools — using
PowerPoint/Google Slides: slide design, animations, transitions. Applications —
creating resumes, reports, brochures, and presentations. Keyboard shortcuts.

---

This unit is learned at a keyboard. Reading about mail merge teaches you
nothing; doing one mail merge teaches you all of it.

## 3.1 Word processing basics

### Formatting levels

| Level | Controls | Where |
|---|---|---|
| **Character** | Font, size, bold, italic, underline, colour, superscript | Home → Font |
| **Paragraph** | Alignment, indentation, line spacing, spacing before/after, bullets | Home → Paragraph |
| **Page** | Margins, orientation, size, columns, borders | Layout |
| **Section** | Different headers, footers or orientation within one document | Layout → Breaks |
| **Document** | Styles, theme, template | Design |

### Styles — the thing most students skip

A **style** is a named bundle of formatting. Instead of manually making every
heading 16pt bold blue, you apply the "Heading 1" style.

**Why it matters:**

1. **Consistency** — every heading looks identical automatically
2. **One-step global change** — modify the style, and all 40 headings update
3. **Automatic table of contents** — generated from heading styles; without
   them it cannot be built at all
4. **Navigation pane** — jump between sections
5. **Accessibility** — screen readers use heading structure

**This is the single most useful thing in this unit.** Direct formatting on a
long document is slow to apply and painful to change; styles make both trivial.

To generate a table of contents: apply Heading 1/2/3 styles, then
**References → Table of Contents**. Update it with F9.

### Tables

**Insert → Table**, then drag to size or specify rows and columns.

| Task | How |
|---|---|
| Add a row | Tab at the last cell, or right-click → Insert |
| Merge cells | Select → right-click → Merge Cells |
| Split cells | Layout → Split Cells |
| Repeat the header row across pages | Select header → Layout → Repeat Header Rows |
| Sort | Layout → Sort |
| Simple formula | Layout → Formula, e.g. `=SUM(ABOVE)` |
| Convert text to table | Insert → Table → Convert Text to Table |

Word tables support basic formulas, but anything numerical is better done in a
spreadsheet and pasted in.

### Mail merge — the most examined topic in this unit

**The problem it solves:** you must send the same letter to 200 people, each
addressed personally. Typing 200 letters is absurd.

**Mail merge combines a template with a data source** to produce personalised
copies.

**Three components:**

1. **Main document** — the letter, with placeholders
2. **Data source** — a table of recipients (Excel, Access, Outlook contacts, or
   a Word table)
3. **Merged output** — one copy per record

**The six steps** (Mailings tab):

1. **Start Mail Merge** → choose the type (Letters, Envelopes, Labels, Email)
2. **Select Recipients** → Use an Existing List, and pick your Excel file
3. **Edit Recipient List** → filter or sort; untick anyone to exclude
4. **Insert Merge Fields** → place `«FirstName»`, `«Address»` in the letter
5. **Preview Results** → step through records to check
6. **Finish & Merge** → Print, or Edit Individual Documents, or Send Email

**The data source's first row must be the field names**, with no blank rows
above it. This is the commonest cause of a mail merge that will not work.

**Merge rules** for conditional content:
`Mailings → Rules → If...Then...Else` — for example, "Dear Sir" or "Dear Madam"
depending on a Gender column.

### Other useful features

| Feature | Purpose | Where |
|---|---|---|
| **Track Changes** | Record edits for review | Review |
| **Comments** | Margin notes | Review → New Comment |
| **Find & Replace** | Bulk edit — supports wildcards | Home, or Ctrl+H |
| **Headers & Footers** | Repeating top/bottom content | Insert |
| **Page numbers** | Automatic numbering | Insert → Page Number |
| **Footnotes** | References at the page foot | References |
| **Watermark** | Background text such as DRAFT | Design |
| **Columns** | Newspaper-style layout | Layout → Columns |
| **Word Count** | Statistics | Review, or the status bar |
| **Spelling & Grammar** | Proofing | Review, or F7 |

### Creating resumes, reports and brochures

The syllabus names three document types, and each is really a question about
*which feature you reach for*. That is what the examiner is testing.

| Document | The features that matter | The mistake to avoid |
|---|---|---|
| **Resume** | A template; consistent styles; tables (borderless) for alignment; 1–2 pages; PDF export | Aligning with spaces or repeated tabs |
| **Report** | Heading styles; automatic table of contents; captions; page numbers; footnotes; section breaks | Typing the contents page by hand |
| **Brochure** | Columns or a tri-fold template; text boxes; images with text wrapping; landscape orientation | Dragging images so text reflows unpredictably |

**Resume.** Start from a template rather than a blank page. Use a **borderless
table** to line up dates against roles — it holds its alignment when the font
changes, which a row of tabs does not. Keep it to one page for a student, two
at most. **Export to PDF**, always: a `.docx` opened on another machine
repaginates if the fonts differ, and your careful one-page layout becomes one
and a half.

**Report.** This is where **styles** earn their keep, and it is the standard
ten-mark answer:

1. Apply **Heading 1/2/3** styles to section titles — not manual bold and size.
2. Insert → **Table of Contents**, which is built *from* those styles. Change a
   heading later and press F9 to update the whole contents page.
3. Add **captions** to figures and tables (References → Insert Caption), so
   they renumber themselves when you insert one in the middle.
4. Insert **page numbers** in the footer, and use a **section break** if the
   front matter needs Roman numerals and the body Arabic.
5. Use **footnotes** for references.

Every one of those five is automatic. A report formatted by hand has to be
renumbered by hand every time it changes, which is why "I used Heading styles
so the contents page builds itself" is worth more marks than any amount of
description of fonts.

**Brochure.** A tri-fold is three **columns** in **landscape** orientation
(Layout → Orientation, then Layout → Columns → Three). Place images inside
**text boxes** or set their **text wrapping** to Square, so the text flows
around them predictably instead of jumping when you nudge an image.

### 💡 The common thread

Word processors are full of features that do a job *automatically* — styles,
table of contents, captions, mail merge, page numbers — and a manual imitation
of each. The manual version looks identical until something changes, and then
it is wrong everywhere at once. Naming the automatic feature is what
distinguishes a good answer.

## 3.2 Presentation tools

### Building a good deck

| Element | Guidance |
|---|---|
| **Slide layout** | Use the built-in layouts, not manually placed text boxes |
| **Slide master** | Change the design once, applied everywhere |
| **Theme** | A coordinated set of colours, fonts and effects |
| **Transitions** | Between slides — one type, used consistently |
| **Animations** | Within a slide — use sparingly |
| **Speaker notes** | Your script; visible only in Presenter View |

### Transitions vs animations — an exam question

| | Transition | Animation |
|---|---|---|
| Applies to | Moving **between** slides | Objects **within** a slide |
| Tab | Transitions | Animations |
| Example | Fade from slide 3 to slide 4 | A bullet flying in |

### The animation types

| Type | Effect |
|---|---|
| **Entrance** | How an object appears |
| **Emphasis** | Draws attention to something already visible |
| **Exit** | How an object leaves |
| **Motion path** | Moves an object along a path |

### Design principles worth stating in an exam

1. **One idea per slide**
2. **The 6×6 guideline** — at most six bullets, six words each
3. **Large fonts** — 28pt minimum for body text
4. **High contrast** — dark text on light, or the reverse
5. **Images over paragraphs**
6. **Consistency** — the slide master enforces it
7. **Do not read your slides aloud** — the slides support you, they are not the
   talk

**Presenter View** shows your notes and the next slide on your laptop while the
audience sees only the current slide.

### Useful presentation features

| Feature | Purpose |
|---|---|
| **Slide Sorter** | Reorder slides visually |
| **Hyperlinks** | Jump to a slide or a URL |
| **Embedded media** | Audio and video (lab experiment 5 requires this) |
| **Charts** | Insert, or paste linked from Excel |
| **SmartArt** | Diagrams — processes, hierarchies, cycles |
| **Rehearse Timings** | Record how long each slide takes |
| **Export to PDF** | For sharing without the fonts breaking |

## 3.3 Keyboard shortcuts

The syllabus lists these explicitly, so they are examinable — and they make the
lab exam considerably faster.

### Universal

| Shortcut | Action |
|---|---|
| **Ctrl + N** | New |
| **Ctrl + O** | Open |
| **Ctrl + S** | Save |
| **F12** | Save As |
| **Ctrl + P** | Print |
| **Ctrl + W** | Close |
| **Ctrl + Z / Ctrl + Y** | Undo / Redo |
| **Ctrl + C / X / V** | Copy / Cut / Paste |
| **Ctrl + Shift + V** | Paste Special |
| **Ctrl + A** | Select All |
| **Ctrl + F / H** | Find / Replace |

### Formatting

| Shortcut | Action |
|---|---|
| **Ctrl + B / I / U** | Bold / Italic / Underline |
| **Ctrl + L / E / R / J** | Align left / centre / right / justify |
| **Ctrl + Shift + > / <** | Increase / decrease font size |
| **Ctrl + Shift + C / V** | Copy / paste **formatting** |
| **Ctrl + Space** | Remove character formatting |
| **Ctrl + 1 / 2 / 5** | Single / double / 1.5 line spacing |

### Navigation

| Shortcut | Action |
|---|---|
| **Ctrl + Home / End** | Start / end of document |
| **Ctrl + ← / →** | One word left / right |
| **Ctrl + Enter** | Page break |
| **Shift + F3** | Cycle case: lower → Title → UPPER |

### Presentation-specific

| Shortcut | Action |
|---|---|
| **F5** | Start from the beginning |
| **Shift + F5** | Start from the current slide |
| **Ctrl + M** | New slide |
| **B / W** | Blank the screen black / white during a talk |
| **Esc** | End the show |
| **Ctrl + P** *(during a show)* | Pen annotation |

**B and W are genuinely useful** — pressing B blanks the screen so the audience
looks at you rather than the slide.

---

## Exam questions from this unit

**Two marks**

1. What is a style, and why use one?
2. Differentiate a transition from an animation.
3. What are the three components of a mail merge?
4. State any five keyboard shortcuts and their functions.
5. What is a slide master?

**Five marks**

1. Explain the mail merge process step by step.
2. Explain the levels of formatting in a word processor.
3. Explain the features used in preparing a professional report.
4. Explain the design principles for an effective presentation.

**Ten marks**

1. Explain word processing features in detail — formatting, styles, tables and
   mail merge — with the steps for each.
2. Explain how you would prepare a project report with a table of contents,
   headers, footers, page numbers, tables and figures.

## Mistakes that cost marks

- Describing mail merge without naming all three components
- Forgetting that the data source's first row must be the field names
- Confusing transitions (between slides) with animations (within a slide)
- Formatting headings manually instead of using styles — and then being unable
  to generate a table of contents
- Listing shortcuts without saying what they do
