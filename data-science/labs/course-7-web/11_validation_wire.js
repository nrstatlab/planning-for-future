/* Experiment 11 — the DOM half. Wires 11_validation.js to the form in
 * 07_styled_form.html. Kept separate so the rules stay testable. */

import { RULES, validate } from "./11_validation.js";

const form = document.getElementById("reg");

function setFieldError(input, message) {
  if (!input) return;
  const box = document.getElementById(input.id + "-error");
  input.classList.toggle("is-invalid", Boolean(message));
  input.setAttribute("aria-invalid", message ? "true" : "false");
  if (box) box.textContent = message || "";      // textContent, never innerHTML
}

function readValues() {
  const values = Object.fromEntries(new FormData(form));
  // FormData OMITS unchecked checkboxes entirely — the key is absent, not
  // false — so the checkbox has to be read from .checked separately.
  values.terms = form.elements.terms.checked;
  return values;
}

form.addEventListener("submit", e => {
  const errors = validate(readValues());
  for (const id of [...Object.keys(RULES), "confirm", "terms"])
    setFieldError(form.elements[id], errors[id] || "");

  if (Object.keys(errors).length) {
    e.preventDefault();                          // THIS is what cancels submit
    form.querySelector(".is-invalid")?.focus();  // move focus to the first problem
    document.getElementById("status").textContent = "";
  } else {
    e.preventDefault();                          // demo only: nothing to POST to
    document.getElementById("status").textContent = "All fields valid.";
  }
});

// Live feedback, but only after the user has left the field once. Validating
// from the first character shows "invalid email" while they are still typing
// the first letter, which is hostile.
for (const [field, rule] of Object.entries(RULES)) {
  const input = form.elements[field];
  if (!input) continue;
  let touched = false;
  const run = () => setFieldError(input, rule.test(input.value) ? "" : rule.msg);
  input.addEventListener("blur",  () => { touched = true; run(); });
  input.addEventListener("input", () => { if (touched) run(); });
}
