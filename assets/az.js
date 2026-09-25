/* NRSTATLAB — the home page's A–Z column.

   Each letter is a plain link to its section of topics.html, so with scripts
   off, or if the data cannot be fetched, it still goes somewhere. With them
   on, a letter lists its topics in the column itself -- each topic with the
   pages that teach it -- from assets/topics-index.json, which
   tools/build_topic_index.py writes from the same grouping as topics.html.
   The file is fetched the first time a letter is picked, never before.

   Search results (assets/search.js, data-inline) take the column's place
   while the box has words in it; picking a letter clears the box. */

(function () {
  'use strict';

  var rail = document.querySelector('.az-letters');
  var panel = document.getElementById('az-panel');
  if (!rail || !panel) return;

  var src = document.currentScript && document.currentScript.src;
  var dataUrl = new URL('topics-index.json', src || window.location.href).href;
  var data = null, pending = null;

  function load() {
    if (data) return Promise.resolve(data);
    if (!pending) {
      pending = fetch(dataUrl)
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (d) { data = d; return d; });
      pending.catch(function () { pending = null; });
    }
    return pending;
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }

  function show(letter, d) {
    var row = null;
    for (var i = 0; i < d.letters.length; i++) {
      if (d.letters[i][0] === letter) { row = d.letters[i]; break; }
    }
    panel.textContent = '';
    if (!row) {
      panel.appendChild(el('p', 'az-hint', 'No topics under ' + letter + ' yet.'));
      return;
    }
    var n = row[1].length;
    var head = el('h3', 'az-head', (letter === 'Symbols' ? 'Symbols and Greek' : letter) +
                  ' — ' + n + ' topic' + (n === 1 ? '' : 's'));
    head.tabIndex = -1;
    panel.appendChild(head);
    var dl = el('dl', 'az-list');
    row[1].forEach(function (entry) {
      dl.appendChild(el('dt', null, entry[0]));
      var dd = el('dd');
      entry[1].forEach(function (pi, j) {
        if (j) dd.appendChild(document.createTextNode(' · '));
        var a = el('a', null, d.pages[pi][1]);
        a.href = new URL('../' + d.pages[pi][0], dataUrl).href;
        dd.appendChild(a);
      });
      dl.appendChild(dd);
    });
    panel.appendChild(dl);
    var all = el('a', 'azlink', 'All ' + d.n.toLocaleString('en-IN') + ' topics on one page');
    all.href = new URL('../topics.html', dataUrl).href;
    panel.appendChild(all);
    head.focus({ preventScroll: true });
  }

  rail.addEventListener('click', function (ev) {
    var a = ev.target.closest('a[data-letter]');
    if (!a || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.button) return;
    ev.preventDefault();
    var letter = a.getAttribute('data-letter');
    // A letter replaces any search in progress: clear the box, and let
    // search.js close its list the way it always does, on input.
    var box = document.querySelector('.col-az .search input');
    if (box && box.value) {
      box.value = '';
      box.dispatchEvent(new Event('input', { bubbles: true }));
    }
    Array.prototype.forEach.call(rail.querySelectorAll('a'), function (x) {
      if (x === a) x.setAttribute('aria-current', 'true');
      else x.removeAttribute('aria-current');
    });
    load().then(function (d) { show(letter, d); },
                function () { window.location.href = a.href; });
  });
})();
