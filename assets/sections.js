/* NRSTATLAB — collapsible topic sections on long pages.

   Loaded only on long pages (tools/add_site_nav.py decides, at build time:
   four or more topic headings and 1,500 words or more). With scripts off the
   page is exactly as written; this only folds what is already there.

   Each topic heading (<h2 id>) becomes a toggle for everything up to the next
   heading. The first section opens, the rest close, and a bar above them
   offers "Open all" and "Close all". A link to a section -- the contents
   list, a syllabus map's unit3.html#bibd, a search result -- opens it. Closed
   sections use hidden="until-found", so the browser's find-in-page still
   reaches their text (Chrome, Edge); elsewhere they are plainly hidden.

   The page's own navigation and the generated blocks stay outside every
   section: the unit toggle, prev/next, "Next course", "Courses for this exam". */

(function () {
  'use strict';

  var STOP = '.page-nav, .pagination, .progress-toggle, p.next-course, ' +
             'section.exam-courses, footer, .sitefoot';
  var col = document.querySelector('main') ||
            document.querySelector('.wrapper, .container');
  if (!col) return;

  // The topic headings are the h2[id]s that share one parent -- the page's
  // column. Notes put them straight in <main>, in .wrapper, or inside a
  // <section>; the parent holding the most of them is the column.
  var byParent = new Map();
  Array.prototype.forEach.call(col.querySelectorAll('h2[id]'), function (h) {
    if (h.closest('nav, details, header, .exam-courses, .sitenav, .sitefoot')) return;
    var list = byParent.get(h.parentNode) || [];
    list.push(h);
    byParent.set(h.parentNode, list);
  });
  var heads = [];
  byParent.forEach(function (list) { if (list.length > heads.length) heads = list; });
  if (heads.length < 4) return;

  var until = 'onbeforematch' in document.body;   // hidden="until-found" works
  var sections = [];

  heads.forEach(function (h, i) {
    var body = document.createElement('div');
    body.className = 'sec-body';
    body.id = h.id + '--body';
    var n = h.nextSibling;
    while (n && !(n.nodeType === 1 && (n.tagName === 'H2' || n.matches(STOP)))) {
      var next = n.nextSibling;
      body.appendChild(n);
      n = next;
    }
    h.parentNode.insertBefore(body, n);

    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'sec-toggle';
    b.setAttribute('aria-controls', body.id);
    while (h.firstChild) b.appendChild(h.firstChild);
    h.appendChild(b);
    h.classList.add('sec-head');
    b.addEventListener('click', function () { set(i, !open(i)); });
    body.addEventListener('beforematch', function () { set(i, true); });
    sections.push({ head: h, body: body, button: b });
  });

  function open(i) { return sections[i].button.getAttribute('aria-expanded') === 'true'; }
  function set(i, on) {
    var s = sections[i];
    s.button.setAttribute('aria-expanded', on ? 'true' : 'false');
    if (on) s.body.removeAttribute('hidden');
    else s.body.setAttribute('hidden', until ? 'until-found' : '');
  }
  function all(on) { sections.forEach(function (_, i) { set(i, on); }); }

  // The bar: how many sections, and open or close them all.
  var bar = document.createElement('div');
  bar.className = 'sec-bar';
  var count = document.createElement('span');
  count.textContent = sections.length + ' sections';
  bar.appendChild(count);
  [['Open all', true], ['Close all', false]].forEach(function (p) {
    var b = document.createElement('button');
    b.type = 'button';
    b.textContent = p[0];
    b.addEventListener('click', function () { all(p[1]); });
    bar.appendChild(b);
  });
  heads[0].parentNode.insertBefore(bar, heads[0]);

  sections.forEach(function (_, i) { set(i, i === 0); });

  // A link to a heading, or to anything inside a section, opens it.
  function reveal() {
    var id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    var t = document.getElementById(id);
    if (!t) return;
    var hit = false;
    sections.forEach(function (s, i) {
      if (s.head === t || s.body.contains(t)) { set(i, true); hit = true; }
    });
    if (hit) t.scrollIntoView();
  }
  window.addEventListener('hashchange', reveal);
  reveal();

  // Printing prints the whole page, then puts the reader's view back.
  var before = null;
  window.addEventListener('beforeprint', function () {
    before = sections.map(function (_, i) { return open(i); });
    all(true);
  });
  window.addEventListener('afterprint', function () {
    if (before) before.forEach(function (on, i) { set(i, on); });
    before = null;
  });
})();
