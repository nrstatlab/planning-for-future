/* Experiment 11 — Form validation.
 *
 * The rules are DATA, not a wall of if-statements, so adding a field is one
 * line and the same array drives both submit-time and live validation.
 *
 * IMPORTANT: none of this is security. It runs on the user's machine and can
 * be bypassed by disabling JavaScript, editing the DOM, or sending the request
 * with curl. The server must validate every field again.
 */

export const RULES = {
  name: {
    test: v => v.trim().length >= 3 && v.trim().length <= 50,
    msg:  "Name must be 3 to 50 characters"
  },
  email: {
    // A plausible shape, not an RFC-complete pattern. The only real proof an
    // address exists is sending a confirmation message to it.
    test: v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()),
    msg:  "Enter a valid email address"
  },
  mobile: {
    test: v => /^[6-9]\d{9}$/.test(v.trim()),
    msg:  "Enter a 10-digit Indian mobile number"
  },
  password: {
    // Four lookaheads assert lowercase, uppercase, digit and symbol in any
    // order without consuming anything; .{8,} then does the matching.
    test: v => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/.test(v),
    msg:  "8+ characters with upper, lower, digit and symbol"
  }
};

/** Validate a plain object of values. Returns { field: message } — empty when
 *  everything passed. */
export function validate(values) {
  const errors = {};

  for (const [field, rule] of Object.entries(RULES))
    if (!rule.test(values[field] ?? "")) errors[field] = rule.msg;

  // Rules that compare two fields cannot be expressed as a pattern.
  if (values.password !== values.confirm)
    errors.confirm = "Passwords do not match";

  // A checkbox is read from .checked, never .value.
  if (!values.terms)
    errors.terms = "You must accept the terms";

  return errors;
}

/** A real calendar date. 2026-02-30 matches the shape but does not exist:
 *  new Date(2026, 1, 30) rolls over to 2 March, so comparing the components
 *  back is what proves the date was real. */
export function isRealDate(s) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return false;
  const [y, m, d] = s.split("-").map(Number);
  const dt = new Date(y, m - 1, d);
  return dt.getFullYear() === y && dt.getMonth() === m - 1 && dt.getDate() === d;
}

/** Age in whole years, given an ISO date of birth. */
export function ageOn(dobStr, on = new Date()) {
  const dob = new Date(dobStr);
  let age = on.getFullYear() - dob.getFullYear();
  const m = on.getMonth() - dob.getMonth();
  if (m < 0 || (m === 0 && on.getDate() < dob.getDate())) age--;
  return age;
}
