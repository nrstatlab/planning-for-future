/* Experiment 5 — Embed a calendar object in a web page.
 *
 * The syllabus phrase "calendar object" dates from an era of ActiveX
 * controls. Three modern answers, in the HTML: the native <input type="date">
 * picker, an <iframe> embed, and a month grid generated here.
 *
 * This module is pure: it takes a year and month and returns data, with no
 * reference to `document`. That is what makes it testable — see
 * tools/run_web_labs.js.
 */

export const MONTH_NAMES = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

export const DAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

/** Number of days in a month. `month` is 1-12.
 *
 * new Date(y, m, 0) is "day zero" of month m, which the Date constructor
 * normalises to the LAST day of month m-1. Because `month` here is 1-based
 * and the constructor is 0-based, passing `month` straight through lands on
 * the last day of the month we asked about — leap years included, with no
 * table and no arithmetic of our own.
 */
export function daysInMonth(year, month) {
  return new Date(year, month, 0).getDate();
}

/** Weekday index (0 = Sunday) of the first of the month. */
export function firstWeekday(year, month) {
  return new Date(year, month - 1, 1).getDay();
}

/** A month as an array of 7-element week rows.
 *  Cells before the 1st and after the last are null. */
export function monthMatrix(year, month) {
  if (!Number.isInteger(month) || month < 1 || month > 12)
    throw new RangeError("month must be an integer from 1 to 12");

  const cells = Array(firstWeekday(year, month)).fill(null);
  for (let d = 1; d <= daysInMonth(year, month); d++) cells.push(d);
  while (cells.length % 7 !== 0) cells.push(null);

  const weeks = [];
  for (let i = 0; i < cells.length; i += 7) weeks.push(cells.slice(i, i + 7));
  return weeks;
}

export function isLeapYear(y) {
  return (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;
}

/** Render a month into a <table>. `doc` is injectable so jsdom can pass its
 *  own document; in a browser it defaults to the real one. */
export function renderCalendar(year, month, table, doc = document) {
  table.textContent = "";

  const caption = doc.createElement("caption");
  caption.textContent = `${MONTH_NAMES[month - 1]} ${year}`;
  table.append(caption);

  const thead = doc.createElement("thead");
  const hrow = doc.createElement("tr");
  for (const d of DAY_NAMES) {
    const th = doc.createElement("th");
    th.scope = "col";
    th.textContent = d;
    hrow.append(th);
  }
  thead.append(hrow);
  table.append(thead);

  const today = new Date();
  const isThisMonth = today.getFullYear() === year && today.getMonth() === month - 1;

  const tbody = doc.createElement("tbody");
  for (const week of monthMatrix(year, month)) {
    const tr = doc.createElement("tr");
    for (const day of week) {
      const td = doc.createElement("td");
      if (day === null) {
        td.className = "empty";
      } else {
        td.textContent = String(day);
        if (isThisMonth && day === today.getDate()) td.className = "today";
      }
      tr.append(td);
    }
    tbody.append(tr);
  }
  table.append(tbody);
  return table;
}
