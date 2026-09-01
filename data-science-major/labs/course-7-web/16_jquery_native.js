/* Experiment 16 — the same behaviour as 16_jquery.html, with no library.
 *
 * jQuery's animation queue depends on timing that jsdom does not reproduce
 * faithfully, so this native version is what tools/run_web_labs.js executes:
 * class toggles can be asserted directly and deterministically.
 *
 * Read it beside the jQuery in 16_jquery.html. Every line has a one-to-one
 * counterpart, which is the real lesson of this experiment — jQuery's ideas
 * succeeded so completely that the library became unnecessary.
 */

/* jQuery: $(el).hide()  /  $(el).show() */
export const hide = el => { el.classList.add("is-hidden"); return el; };
export const show = el => { el.classList.remove("is-hidden"); return el; };

/* jQuery: $(el).toggle() */
export const toggle = el => { el.classList.toggle("is-hidden"); return el; };

/* jQuery: $(el).fadeToggle() — the fade lives in the stylesheet, where the
   browser can run it on the compositor instead of a JavaScript timer. */
export const fadeToggle = el => { el.classList.toggle("is-faded"); return el; };

/* jQuery: $(el).slideToggle() */
export const slideToggle = el => { el.classList.toggle("is-collapsed"); return el; };

/* jQuery: $(el).addClass(a).removeClass(b).text(t) — chaining works here too,
   because each function returns the element. */
export function setMessage(el, text, kind = "success") {
  el.classList.remove("error", "success");
  el.classList.add(kind);
  el.textContent = text;              // textContent, never innerHTML
  return el;
}

/* jQuery: $("#table").on("click", ".delete-btn", fn)
 *
 * Event DELEGATION. One listener on the container, so rows added later — by
 * AJAX, or by the user — work with no extra wiring. Binding directly to
 * ".delete-btn" would only catch the rows that existed at that instant.
 *
 * closest("tr") rather than parentNode.parentNode: wrap the button in a
 * <span> for styling and a parent chain removes the wrong element.
 */
export function wireTable(root) {
  root.addEventListener("click", e => {
    const btn = e.target.closest(".delete-btn");
    if (!btn) return;
    const tr = btn.closest("tr");
    if (!tr) return;
    // Remove after the CSS fade finishes — the native equivalent of jQuery's
    // fadeOut(300, function () { $(this).remove(); }) completion callback.
    tr.addEventListener("transitionend", () => tr.remove(), { once: true });
    tr.classList.add("fading");
  });
  return root;
}

/* jQuery: $(el).animate({ left: "250px" }, 500) */
export function slideTo(el, x) {
  el.style.transform = `translateX(${x}px)`;
  return el;
}

/* jQuery: $("#list").append("<li>…</li>") */
export function appendItem(list, text, doc = document) {
  const li = doc.createElement("li");
  li.textContent = text;
  list.append(li);
  return li;
}

/* jQuery: $("#list").empty() */
export const empty = el => { el.textContent = ""; return el; };
