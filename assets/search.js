/* NRSTATLAB — site-wide search.

   The index is fetched only when the reader first asks to search, so a page
   that is merely read costs nothing for this. Until then the box is inert.

   Progressive, like everything else here: the box ships in the HTML with the
   `hidden` attribute and this script removes it. With JS off nobody is shown a
   search box that cannot work — they get the A–Z index link that is already
   on the page. */

(function () {
  'use strict';

  var box = document.querySelector('.search input[type="search"]');
  if (!box) return;

  var wrap = box.closest('.search');
  var list = wrap.querySelector('.results');
  var status = wrap.querySelector('.sstatus');
  wrap.hidden = false;               // JS is running, so the box can work

  // Every path in the index is relative to the site root, so a page deeper
  // than the root prefixes them. It states its own depth rather than this
  // script guessing at one.
  var base = box.getAttribute('data-base') || '';

  var index = null;                  // the loaded records
  var pending = null;                // the in-flight fetch, so we ask once
  var active = -1;                   // highlighted result, for the arrow keys
  var shown = [];

  /* Statistics is written in Greek here — the site says "χ² Test for Goodness
     of Fit", and a reader types "chi square". Without this they never meet.
     "²" expands to both "square" and "squared" so either spelling of the
     query is a whole-word hit; the folded text is only ever tokenised, never
     shown, so emitting two words costs nothing. */
  var GREEK = {
    'χ': 'chi', 'σ': 'sigma', 'μ': 'mu', 'α': 'alpha', 'β': 'beta',
    'λ': 'lambda', 'ρ': 'rho', 'θ': 'theta', 'π': 'pi', 'τ': 'tau',
    'Σ': 'sigma', 'Χ': 'chi', '²': ' square squared ', '³': ' cube cubed '
  };

  function fold(s) {
    var out = '';
    for (var i = 0; i < s.length; i++) {
      var c = s[i];
      out += Object.prototype.hasOwnProperty.call(GREEK, c) ? GREEK[c] : c;
    }
    return out.toLowerCase();
  }

  function words(s) {
    return fold(s).split(/[^a-z0-9]+/).filter(Boolean);
  }

  /* One searchable bag of words per field, built once when the index loads.
     Keeping the fields apart is what lets a title hit outrank a passing
     mention in a description. */
  function prep(r) {
    r._t = words(r.t);
    r._k = words((r.k || []).join(' '));
    r._h = words((r.h || []).join(' '));
    r._d = words(r.d || '');
    return r;
  }

  function load() {
    if (pending) return pending;
    var url = box.getAttribute('data-index');
    say('Loading the index…');
    pending = fetch(url)
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      })
      .then(function (recs) {
        index = recs.map(prep);
        say('');
        return index;
      })
      .catch(function () {
        pending = null;              // a failed load should be retryable
        say('Search could not load. The A–Z index still works.');
        return null;
      });
    return pending;
  }

  /* Where a word appears decides its weight: what a page claims to be about
     beats what it mentions in passing, and a whole-word hit beats a prefix of
     a longer word. */
  var FIELDS = [['_t', 12], ['_k', 7], ['_h', 4], ['_d', 1]];

  /* Matching *every* word was the first rule here, and it was wrong: a reader
     who types a question — "which test for two groups" — got nothing at all,
     because no page carries all five words. So a page needs one word, and
     pages matching more words rank first regardless of weight. Covering the
     question is a stronger signal than scoring well on part of it. */
  function score(rec, terms) {
    var total = 0, matched = 0;
    for (var i = 0; i < terms.length; i++) {
      var term = terms[i], best = 0;
      for (var f = 0; f < FIELDS.length; f++) {
        var bag = rec[FIELDS[f][0]], weight = FIELDS[f][1];
        for (var w = 0; w < bag.length; w++) {
          if (bag[w] === term) { best = Math.max(best, weight * 2); break; }
          if (bag[w].indexOf(term) === 0) best = Math.max(best, weight);
        }
      }
      if (best) { matched++; total += best; }
    }
    return matched ? [matched, total] : null;
  }

  function search(q) {
    var terms = words(q);
    if (!terms.length || !index) return [];
    var hits = [];
    for (var i = 0; i < index.length; i++) {
      var s = score(index[i], terms);
      if (s) hits.push([s[0], s[1], index[i]]);
    }
    hits.sort(function (a, b) {
      return b[0] - a[0]            // covered more of the question
          || b[1] - a[1]            // then matched in more important places
          || a[2].t.length - b[2].t.length;   // then the more specific title
    });
    return hits.slice(0, 8).map(function (h) { return h[2]; });
  }

  function esc(s) {
    return s.replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  /* Show why a page matched — the first of its own topics that the reader's
     words touch, falling back to its description. A result nobody can explain
     is a result nobody trusts. */
  function why(rec, terms) {
    var pool = (rec.k || []).concat(rec.h || []);
    for (var i = 0; i < pool.length; i++) {
      var w = words(pool[i]);
      for (var t = 0; t < terms.length; t++) {
        for (var j = 0; j < w.length; j++) {
          if (w[j].indexOf(terms[t]) === 0) return pool[i];
        }
      }
    }
    return rec.d || '';
  }

  function say(msg) {
    if (status) status.textContent = msg;
  }

  function render(q) {
    var terms = words(q);
    shown = search(q);
    active = -1;
    if (!q.trim()) {
      close();
      return;
    }
    if (!shown.length) {
      list.innerHTML = '<li class="none">Nothing matches those words. ' +
        'Try fewer, or browse the <a href="' + esc(base) +
        'topics.html">A–Z index</a>.</li>';
      open();
      say('No results.');
      return;
    }
    list.innerHTML = shown.map(function (r, i) {
      return '<li role="option" id="sr' + i + '" aria-selected="false">' +
        '<a href="' + esc(base + r.u) + '">' +
        '<span class="rt">' + esc(r.t) + '</span>' +
        '<span class="rs">' + esc(r.s) + '</span>' +
        '<span class="rw">' + esc(why(r, terms)) + '</span></a></li>';
    }).join('');
    open();
    say(shown.length + (shown.length === 1 ? ' result.' : ' results.'));
  }

  function open() {
    list.hidden = false;
    box.setAttribute('aria-expanded', 'true');
  }

  function close() {
    list.hidden = true;
    list.innerHTML = '';
    box.setAttribute('aria-expanded', 'false');
    box.removeAttribute('aria-activedescendant');
    active = -1;
    say('');
  }

  function move(step) {
    var items = list.querySelectorAll('li[role="option"]');
    if (!items.length) return;
    if (active >= 0) items[active].setAttribute('aria-selected', 'false');
    // Cycle over n+1 positions: the input itself (-1) and each result.
    var n = items.length;
    active = ((active + 1) + step + (n + 1)) % (n + 1) - 1;
    if (active < 0) {
      box.removeAttribute('aria-activedescendant');
      return;
    }
    items[active].setAttribute('aria-selected', 'true');
    box.setAttribute('aria-activedescendant', items[active].id);
    items[active].scrollIntoView({ block: 'nearest' });
  }

  box.addEventListener('focus', load);

  box.addEventListener('input', function () {
    var q = box.value;
    if (index) { render(q); return; }
    load().then(function (ok) { if (ok) render(box.value); });
  });

  box.addEventListener('keydown', function (ev) {
    if (ev.key === 'ArrowDown') { move(1); ev.preventDefault(); }
    else if (ev.key === 'ArrowUp') { move(-1); ev.preventDefault(); }
    else if (ev.key === 'Enter' && active >= 0 && shown[active]) {
      window.location.href = base + shown[active].u;
      ev.preventDefault();
    } else if (ev.key === 'Escape') {
      if (list.hidden) box.blur(); else close();
    }
  });

  // Clicking away closes the list; clicking a result must still navigate, so
  // this listens on the document rather than blurring the input.
  document.addEventListener('click', function (ev) {
    if (!wrap.contains(ev.target)) close();
  });

  // "/" jumps to the box, the convention on documentation sites — but not
  // while the reader is typing somewhere else.
  document.addEventListener('keydown', function (ev) {
    if (ev.key !== '/' || ev.metaKey || ev.ctrlKey || ev.altKey) return;
    var el = document.activeElement;
    if (el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' ||
               el.isContentEditable)) return;
    box.focus();
    box.select();
    ev.preventDefault();
  });
}());
