/* NRSTATLAB — your progress, kept in this browser and nowhere else.

   Nothing here is sent anywhere. Progress is one localStorage entry on this
   device; clear the site's data, or press "Clear my progress" on the About
   page, and it is gone. It does not follow the reader to another device --
   that would need an account, and this site has none.

   Progressive, like search.js: the HTML ships without any of this, and a
   reader with scripts off, or with storage blocked (private windows, some
   browsers' strict modes), sees every page exactly as it is.

   The page says what it is. tools/add_site_nav.py writes data-progress on
   this script's tag: "unit" pages get the mark-done toggle and are remembered
   as the last page read; "summary" pages (hubs, course homes, exam hubs, the
   home page, About) show totals, and only they fetch the list of units,
   assets/progress-index.json. Page ids are paths from the site root, e.g.
   statistics/sampling-theory/unit2.html. */

(function () {
  'use strict';

  var me = document.currentScript;
  if (!me) return;
  var role = me.getAttribute('data-progress');
  var KEY = 'nrstatlab.progress.v1';

  // ---- storage: every access guarded ---------------------------------------
  function load() {
    try {
      var s = JSON.parse(window.localStorage.getItem(KEY) || 'null');
      if (s && s.v === 1 && s.done && typeof s.done === 'object') return s;
    } catch (e) { /* unreadable or blocked */ }
    return { v: 1, done: {}, last: null };
  }
  function save(s) {
    try { window.localStorage.setItem(KEY, JSON.stringify(s)); return true; }
    catch (e) { return false; }
  }
  function storageWorks() {
    try {
      var t = KEY + '.test';
      window.localStorage.setItem(t, '1');
      window.localStorage.removeItem(t);
      return true;
    } catch (e) { return false; }
  }
  if (!storageWorks()) return;

  // ---- where the site root is, from this script's own address --------------
  var root = new URL('..', me.src);                 // assets/progress.js -> root
  function idOf(href) {
    var u = new URL(href, window.location.href);
    if (u.origin !== root.origin || u.pathname.indexOf(root.pathname) !== 0) return null;
    var p = decodeURIComponent(u.pathname.slice(root.pathname.length));
    if (p === '' || p.slice(-1) === '/') p += 'index.html';
    return p;
  }
  var here = idOf(window.location.href);

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function pageTitle() {
    var h = document.querySelector('h1');
    return (h ? h.textContent : document.title).replace(/\s+/g, ' ').trim();
  }

  // ---- unit pages -------------------------------------------------------------
  if (role === 'unit') {
    var state = load();
    state.last = { path: here, title: pageTitle(), at: new Date().toISOString() };
    save(state);

    var toggles = [];
    function paint() {
      var done = !!load().done[here];
      toggles.forEach(function (b) {
        b.setAttribute('aria-pressed', done ? 'true' : 'false');
        b.textContent = done ? 'Done ✓ (undo)' : 'Mark this unit done';
      });
    }
    function flip() {
      var s = load();
      if (s.done[here]) delete s.done[here];
      else s.done[here] = new Date().toISOString().slice(0, 10);
      save(s);
      paint();
    }
    function toggle() {
      var wrap = el('div', 'progress-toggle');
      var b = el('button');
      b.type = 'button';
      b.addEventListener('click', flip);
      wrap.appendChild(b);
      toggles.push(b);
      return wrap;
    }
    // Under the page's header, and again at the end of its main column, so a
    // reader who has just finished the unit does not have to scroll back up.
    var head = document.querySelector('.banner, .site-header');
    var col = head && head.nextElementSibling;
    // UGC NET's header spans the page and its column is the <main> after it;
    // everywhere else the header card sits inside the column already.
    if (col && col.tagName === 'MAIN') col.insertBefore(toggle(), col.firstChild);
    else if (head) head.parentNode.insertBefore(toggle(), head.nextSibling);
    var foot = document.querySelector('.page-nav, .pagination');
    if (foot) foot.parentNode.insertBefore(toggle(), foot);
    paint();
    return;
  }

  if (role !== 'summary') return;

  // ---- summary pages ------------------------------------------------------------
  var state = load();
  var done = state.done;

  function counts(index, course) {
    var units = index.courses[course];
    if (!units) return null;
    var n = 0;
    units.forEach(function (u) { if (done[course + '/' + u]) n += 1; });
    return { done: n, total: units.length };
  }
  function badge(c) {
    var b = el('span', 'progress-badge' + (c.done === c.total ? ' is-complete' : ''),
               c.done === c.total ? 'Complete' : c.done + '/' + c.total);
    b.setAttribute('aria-label', c.done + ' of ' + c.total + ' done');
    return b;
  }
  function courseOf(href) {
    var id = idOf(href);
    if (!id || !/\/index\.html$/.test(id)) return null;
    return id.replace(/\/index\.html$/, '');
  }
  function contentLinks(selector) {
    // The menu and the site footer link everything from everywhere; progress
    // belongs on the page's own content only.
    return Array.prototype.filter.call(document.querySelectorAll(selector), function (a) {
      return !a.closest('.sitenav, .sitefoot, header.sitebar, nav');
    });
  }

  function aboutPage() {
    var box = document.getElementById('progress-controls');
    if (!box) return;
    var n = Object.keys(done).length;
    var p = el('p', null, n ? 'This browser has ' + n + ' unit' + (n === 1 ? '' : 's') +
                              ' marked done.' : 'Nothing is marked done in this browser yet.');
    box.appendChild(p);
    if (!n && !state.last) return;
    var b = el('button', 'progress-clear', 'Clear my progress');
    b.type = 'button';
    b.addEventListener('click', function () {
      if (!window.confirm('Clear every unit marked done, and the last page read, from this browser?')) return;
      try { window.localStorage.removeItem(KEY); } catch (e) { /* nothing to clear */ }
      p.textContent = 'Cleared. Nothing is marked done in this browser now.';
      b.remove();
    });
    box.appendChild(b);
    box.hidden = false;
  }

  function homePage(index) {
    var main = document.querySelector('main');
    if (!main || !state.last) return;
    var total = 0;
    Object.keys(index.courses).forEach(function (c) { total += counts(index, c).done; });
    var strip = el('p', 'progress-continue');
    strip.appendChild(el('b', null, 'Continue where you left off: '));
    var a = el('a', null, state.last.title || state.last.path);
    a.href = new URL(state.last.path, root).href;
    strip.appendChild(a);
    if (total) strip.appendChild(document.createTextNode(' · ' + total + ' unit' +
                                                          (total === 1 ? '' : 's') + ' done'));
    main.insertBefore(strip, main.firstChild);
  }

  function courseHome(index, course) {
    var c = counts(index, course);
    if (!c) return;
    var line = el('p', 'progress-line', c.done + ' of ' + c.total + ' done in this browser');
    var head = document.querySelector('.banner, .site-header');
    var after = document.querySelector('.useful-for');
    var col = head && head.nextElementSibling;
    if (after) after.parentNode.insertBefore(line, after.nextSibling);
    else if (col && col.tagName === 'MAIN') col.insertBefore(line, col.firstChild);
    else if (head) head.parentNode.insertBefore(line, head.nextSibling);
    // A tick on each unit card that is done. A link to a section (#anchor) is
    // not a unit card: the UGC NET map links unit sections a hundred times.
    contentLinks('a[href]').forEach(function (a) {
      if (a.getAttribute('href').indexOf('#') !== -1) return;
      var id = idOf(a.getAttribute('href'));
      if (id && done[id] && id.indexOf(course + '/') === 0 && !a.querySelector('.progress-tick')) {
        var t = el('span', 'progress-tick', '✓');
        t.setAttribute('aria-label', 'done');
        a.appendChild(t);
      }
    });
  }

  function courseLists(index) {
    // Hub cards, and the exam hubs' "Courses for this exam" rows.
    contentLinks('a.course[href], .exam-courses a[href]').forEach(function (a) {
      var course = courseOf(a.getAttribute('href'));
      var c = course && counts(index, course);
      if (!c || !c.done) return;
      var slot = a.querySelector('.status') || a;
      slot.appendChild(document.createTextNode(' '));
      slot.appendChild(badge(c));
    });
  }

  if (here === 'about.html') { aboutPage(); return; }
  if (!Object.keys(done).length && !state.last) return;     // nothing to show yet

  fetch(new URL('assets/progress-index.json', root).href)
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (index) {
      if (!index || !index.courses) return;
      if (here === 'index.html') { homePage(index); return; }
      var course = here.replace(/\/index\.html$/, '');
      if (index.courses[course]) courseHome(index, course);
      courseLists(index);
    })
    .catch(function () { /* offline or blocked: the page is complete without it */ });
})();
