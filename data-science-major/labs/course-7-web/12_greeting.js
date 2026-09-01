/* Experiment 12 — A greeting that changes with the time of day.
 *
 * The whole trick is the default parameter. A function that reads the clock
 * internally can only be tested by waiting until 9 a.m.; this one is asserted
 * at every boundary in a fraction of a second, and still behaves identically
 * when called with no arguments in the page.
 *
 * The general lesson: push the unpredictable input to the EDGE of the
 * function, and the logic inside becomes testable.
 */

export function greeting(hour = new Date().getHours()) {
  if (!Number.isInteger(hour) || hour < 0 || hour > 23)
    throw new RangeError("hour must be an integer from 0 to 23");

  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  if (hour < 21) return "Good evening";
  return "Good night";
}

/** A CSS class per period, so the page can restyle itself too. */
export function periodClass(hour = new Date().getHours()) {
  return { "Good morning": "morning", "Good afternoon": "afternoon",
           "Good evening": "evening", "Good night": "night" }[greeting(hour)];
}

/** "Good morning, Asha!" — with a sensible fallback for an empty name. */
export function personalGreeting(name, hour = new Date().getHours()) {
  const who = (name ?? "").trim();
  return who === "" ? `${greeting(hour)}!` : `${greeting(hour)}, ${who}!`;
}

/** 24-hour clock formatted as "09:05:03". padStart is why this never shows
 *  "9:5:3". */
export function formatTime(d = new Date()) {
  const p = n => String(n).padStart(2, "0");
  return `${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
}
