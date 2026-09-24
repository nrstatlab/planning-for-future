/* Machine Learning — Complete Self-Study Notes
   Two small behaviours: the Python/R tab switch, and a copy button on every
   code pane. Both are progressive — with JS off, the first pane still shows. */

(function () {
  'use strict';

  // ---------- Python / R tabs ----------
  document.addEventListener('click', function (ev) {
    var btn = ev.target.closest('.code-tab');
    if (!btn) return;
    var block = btn.closest('.code-block');
    var pane = document.getElementById(btn.dataset.pane);
    if (!block || !pane) return;

    block.querySelectorAll('.code-tab').forEach(function (b) {
      b.classList.toggle('active', b === btn);
      b.setAttribute('aria-selected', b === btn ? 'true' : 'false');
    });
    block.querySelectorAll('.code-pane').forEach(function (p) {
      p.classList.toggle('active', p === pane);
    });
  });

  // Arrow-key movement between the two tabs, as a tablist should behave.
  document.addEventListener('keydown', function (ev) {
    if (ev.key !== 'ArrowLeft' && ev.key !== 'ArrowRight') return;
    var btn = ev.target.closest && ev.target.closest('.code-tab');
    if (!btn) return;
    var tabs = Array.prototype.slice.call(btn.closest('.code-tabs').querySelectorAll('.code-tab'));
    var next = tabs[(tabs.indexOf(btn) + (ev.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
    next.focus();
    next.click();
    ev.preventDefault();
  });

  // ---------- Copy button ----------
  // The button sits in the pane, never inside <pre>: reading pre.textContent
  // with the button inside it would append the button's own label to the code.
  document.querySelectorAll('.code-pane').forEach(function (pane) {
    var code = pane.querySelector('pre code');
    if (!code) return;

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-btn';
    btn.textContent = 'Copy';
    btn.setAttribute('aria-label', 'Copy code to clipboard');

    btn.addEventListener('click', function () {
      navigator.clipboard.writeText(code.textContent.trimEnd()).then(function () {
        btn.textContent = 'Copied';
        setTimeout(function () { btn.textContent = 'Copy'; }, 2000);
      }, function () {
        btn.textContent = 'Press Ctrl+C';
        setTimeout(function () { btn.textContent = 'Copy'; }, 2500);
      });
    });

    pane.appendChild(btn);
  });
})();
