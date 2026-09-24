#!/usr/bin/env node
/* Verify the Course 7 (Web Technologies) labs.
 *
 * Two kinds of check:
 *
 *   1. LOGIC — every exported function from the .js modules is executed and
 *      its result asserted. These genuinely run; nothing here is desk-checked.
 *
 *   2. STRUCTURE — every .html file is parsed with jsdom and checked for the
 *      things that cost marks: a doctype, a charset, a viewport meta, a title,
 *      every <img> carrying alt, every <label for> resolving to a real id,
 *      every form control carrying a name, and radio groups sharing a name.
 *
 * What is NOT automated is visual appearance. Open the pages in a browser.
 *
 * Usage:  npm --prefix tools install     (once)
 *         node tools/run_web_labs.js
 */

import { readFileSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import assert from "node:assert/strict";
import { JSDOM } from "jsdom";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const LABS = path.join(ROOT, "labs", "course-7-web");

let passed = 0;
let failed = 0;

function check(name, fn) {
  try {
    fn();
    passed++;
    console.log(`  ok    ${name}`);
  } catch (err) {
    failed++;
    console.log(`  FAIL  ${name}\n        ${err.message}`);
  }
}

async function acheck(name, fn) {
  try {
    await fn();
    passed++;
    console.log(`  ok    ${name}`);
  } catch (err) {
    failed++;
    console.log(`  FAIL  ${name}\n        ${err.message}`);
  }
}

function banner(t) {
  console.log(`\n${"=".repeat(62)}\n${t}\n${"=".repeat(62)}`);
}

const mod = f => import(path.join(LABS, f));
const readLab = f => readFileSync(path.join(LABS, f), "utf8");

/* ==================================================================
   Experiment 5 — calendar
   ================================================================== */
banner("Experiment 5 — calendar");
{
  const { monthMatrix, daysInMonth, firstWeekday, isLeapYear, renderCalendar,
          MONTH_NAMES, DAY_NAMES } = await mod("05_calendar.js");

  check("daysInMonth handles leap years", () => {
    assert.equal(daysInMonth(2024, 2), 29, "2024 is a leap year");
    assert.equal(daysInMonth(2025, 2), 28);
    assert.equal(daysInMonth(2000, 2), 29, "2000 is divisible by 400");
    assert.equal(daysInMonth(1900, 2), 28, "1900 is divisible by 100 but not 400");
    assert.equal(isLeapYear(2000), true);
    assert.equal(isLeapYear(1900), false);
  });

  check("daysInMonth for every month of 2026", () => {
    const expected = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    for (let m = 1; m <= 12; m++) assert.equal(daysInMonth(2026, m), expected[m - 1]);
  });

  check("1 August 2026 is a Saturday", () => {
    assert.equal(DAY_NAMES[firstWeekday(2026, 8)], "Sat");
  });

  check("monthMatrix rows are always 7 wide and cover every day", () => {
    for (let m = 1; m <= 12; m++) {
      const weeks = monthMatrix(2026, m);
      for (const w of weeks) assert.equal(w.length, 7);
      const days = weeks.flat().filter(d => d !== null);
      assert.deepEqual(days, Array.from({ length: daysInMonth(2026, m) }, (_, i) => i + 1));
    }
  });

  check("monthMatrix rejects an out-of-range month", () => {
    assert.throws(() => monthMatrix(2026, 13), RangeError);
    assert.throws(() => monthMatrix(2026, 0), RangeError);
  });

  check("renderCalendar builds a table with a caption and 7 headers", () => {
    const dom = new JSDOM("<table id='c'></table>");
    const doc = dom.window.document;
    const table = renderCalendar(2026, 8, doc.getElementById("c"), doc);
    assert.equal(table.querySelector("caption").textContent, "August 2026");
    assert.equal(table.querySelectorAll("thead th").length, 7);
    assert.equal(table.querySelectorAll("tbody td:not(.empty)").length, 31);
    assert.equal(MONTH_NAMES.length, 12);
  });
}

/* ==================================================================
   Experiment 10 — string operations
   ================================================================== */
banner("Experiment 10 — string operations");
{
  const { reverse, countVowels, countWords, isPalindrome, titleCase,
          charFrequency, longestWord, stats } = await mod("10_string_ops.js");

  check("reverse", () => {
    assert.equal(reverse("Data Science"), "ecneicS ataD");
    assert.equal(reverse(""), "");
    assert.equal(reverse("a"), "a");
  });

  check("countVowels", () => {
    assert.equal(countVowels("Data Science"), 5);   // a, a, i, e, e
    assert.equal(countVowels("rhythm"), 0);
    assert.equal(countVowels("AEIOU"), 5, "must be case-insensitive");
  });

  check("countWords handles blank and multi-space input", () => {
    assert.equal(countWords("Data Science"), 2);
    assert.equal(countWords(""), 0, "empty string is zero words, not one");
    assert.equal(countWords("   "), 0);
    assert.equal(countWords("a   b\t\nc"), 3);
  });

  check("isPalindrome ignores case and punctuation", () => {
    assert.equal(isPalindrome("A man, a plan, a canal: Panama"), true);
    assert.equal(isPalindrome("Madam"), true);
    assert.equal(isPalindrome("Data Science"), false);
    assert.equal(isPalindrome(""), false, "an empty string is not a palindrome here");
  });

  check("titleCase", () => {
    assert.equal(titleCase("data science major"), "Data Science Major");
    assert.equal(titleCase("HTML AND CSS"), "Html And Css");
  });

  check("charFrequency skips whitespace and folds case", () => {
    const f = charFrequency("Data Science");
    assert.equal(f.a, 2);
    assert.equal(f.e, 2);
    assert.equal(f.c, 2);
    assert.equal(f[" "], undefined, "whitespace must be skipped");
    assert.equal(Object.values(f).reduce((a, b) => a + b, 0), 11,
                 "12 characters minus one space");
  });

  check("longestWord", () => {
    assert.equal(longestWord("Data Science Major"), "Science");
    assert.equal(longestWord(""), "");
  });

  check("stats on 'Data Science'", () => {
    const s = stats("Data Science");
    assert.equal(s.length, 12);
    assert.equal(s.words, 2);
    assert.equal(s.vowels, 5);
    assert.equal(s.consonants, 6, "D,t,S,c,n,c");
    assert.equal(s.digits, 0);
    assert.equal(s.reversed, "ecneicS ataD");
    assert.equal(s.firstFour, "Data");
    assert.equal(s.lastSeven, "Science");
    assert.equal(s.isPalindrome, false);
  });

  check("stats never throws on empty input", () => {
    const s = stats("");
    assert.equal(s.length, 0);
    assert.equal(s.words, 0);
    assert.equal(s.vowels, 0);
    assert.equal(s.consonants, 0);
  });
}

/* ==================================================================
   Experiment 11 — form validation
   ================================================================== */
banner("Experiment 11 — form validation");
{
  const { RULES, validate, isRealDate, ageOn } = await mod("11_validation.js");

  const good = { name: "Asha Kumari", email: "asha@nri.ac.in",
                 mobile: "9876543210", password: "Passw0rd!",
                 confirm: "Passw0rd!", terms: true };

  check("a fully valid submission produces no errors", () => {
    assert.deepEqual(validate(good), {});
  });

  check("email rule", () => {
    const t = RULES.email.test;
    for (const ok of ["asha@nri.ac.in", "a.b+c@example.co.uk", "x@y.io"])
      assert.equal(t(ok), true, `${ok} should pass`);
    for (const bad of ["asha@", "@nri.ac.in", "asha", "a@b", "a b@c.in", ""])
      assert.equal(t(bad), false, `${bad} should fail`);
  });

  check("Indian mobile rule — must start 6 to 9", () => {
    const t = RULES.mobile.test;
    assert.equal(t("9876543210"), true);
    assert.equal(t("6000000000"), true);
    assert.equal(t("1234567890"), false, "must not start below 6");
    assert.equal(t("98765432101"), false, "11 digits");
    assert.equal(t("987654321"), false, "9 digits");
  });

  check("password rule needs all four character classes", () => {
    const t = RULES.password.test;
    assert.equal(t("Passw0rd!"), true);
    assert.equal(t("password"), false, "no upper, digit or symbol");
    assert.equal(t("PASSW0RD!"), false, "no lowercase");
    assert.equal(t("Password!"), false, "no digit");
    assert.equal(t("Passw0rd"), false, "no symbol");
    assert.equal(t("Pw0rd!"), false, "too short");
  });

  check("name rule", () => {
    assert.equal(RULES.name.test("Asha"), true);
    assert.equal(RULES.name.test("Al"), false);
    assert.equal(RULES.name.test("   "), false, "must trim before measuring");
    assert.equal(RULES.name.test("x".repeat(51)), false);
  });

  check("mismatched passwords produce exactly the confirm error", () => {
    const e = validate({ ...good, confirm: "Different1!" });
    assert.deepEqual(Object.keys(e), ["confirm"]);
    assert.equal(e.confirm, "Passwords do not match");
  });

  check("unaccepted terms produce exactly the terms error", () => {
    const e = validate({ ...good, terms: false });
    assert.deepEqual(Object.keys(e), ["terms"]);
  });

  check("missing fields are reported, not crashed on", () => {
    const e = validate({});
    assert.deepEqual(Object.keys(e).sort(),
                     ["email", "mobile", "name", "password", "terms"]);
  });

  check("isRealDate rejects a date that matches the shape but does not exist", () => {
    assert.equal(isRealDate("2026-08-26"), true);
    assert.equal(isRealDate("2024-02-29"), true, "2024 is a leap year");
    assert.equal(isRealDate("2025-02-29"), false, "2025 is not");
    assert.equal(isRealDate("2026-02-30"), false);
    assert.equal(isRealDate("2026-13-01"), false);
    assert.equal(isRealDate("26-08-2026"), false, "wrong shape");
  });

  check("ageOn counts whole years, allowing for the birthday", () => {
    assert.equal(ageOn("2000-08-26", new Date(2026, 7, 26)), 26, "on the birthday");
    assert.equal(ageOn("2000-08-27", new Date(2026, 7, 26)), 25, "day before");
    assert.equal(ageOn("2000-09-01", new Date(2026, 7, 26)), 25, "month not reached");
    assert.equal(ageOn("2000-01-01", new Date(2026, 7, 26)), 26);
  });
}

/* ==================================================================
   Experiment 12 — time-based greeting
   ================================================================== */
banner("Experiment 12 — time-based greeting");
{
  const { greeting, periodClass, personalGreeting, formatTime } =
    await mod("12_greeting.js");

  check("every boundary hour", () => {
    const expected = [
      [0,  "Good morning"],  [11, "Good morning"],
      [12, "Good afternoon"],[16, "Good afternoon"],
      [17, "Good evening"],  [20, "Good evening"],
      [21, "Good night"],    [23, "Good night"]
    ];
    for (const [h, want] of expected)
      assert.equal(greeting(h), want, `hour ${h}`);
  });

  check("all 24 hours return one of the four greetings", () => {
    const seen = new Set();
    for (let h = 0; h < 24; h++) seen.add(greeting(h));
    assert.deepEqual([...seen].sort(),
      ["Good afternoon", "Good evening", "Good morning", "Good night"]);
  });

  check("out-of-range hours throw", () => {
    assert.throws(() => greeting(24), RangeError);
    assert.throws(() => greeting(-1), RangeError);
    assert.throws(() => greeting(9.5), RangeError);
  });

  check("greeting() with no argument uses the real clock", () => {
    const now = new Date().getHours();
    assert.equal(greeting(), greeting(now));
  });

  check("periodClass", () => {
    assert.equal(periodClass(9), "morning");
    assert.equal(periodClass(14), "afternoon");
    assert.equal(periodClass(19), "evening");
    assert.equal(periodClass(22), "night");
  });

  check("personalGreeting trims and falls back", () => {
    assert.equal(personalGreeting("Asha", 9), "Good morning, Asha!");
    assert.equal(personalGreeting("  Asha  ", 9), "Good morning, Asha!");
    assert.equal(personalGreeting("", 9), "Good morning!");
    assert.equal(personalGreeting(null, 9), "Good morning!");
  });

  check("formatTime pads to two digits", () => {
    assert.equal(formatTime(new Date(2026, 7, 26, 9, 5, 3)), "09:05:03");
    assert.equal(formatTime(new Date(2026, 7, 26, 23, 59, 59)), "23:59:59");
  });
}

/* ==================================================================
   Experiment 13 — arrays and objects
   ================================================================== */
banner("Experiment 13 — arrays and objects");
{
  const { STUDENTS, addStudent, removeStudent, updateStudent, sortBy,
          search, findByRoll, groupBy, summary } = await mod("13_arrays.js");

  check("summary of the fixture", () => {
    const s = summary(STUDENTS);
    assert.equal(s.count, 5);
    assert.equal(s.average, 62.4);       // (72+45+91+66+38)/5 = 312/5
    assert.equal(s.top, "Meena");
    assert.equal(s.pass, 3);             // 72, 91, 66
  });

  check("summary of an empty list returns nulls, not NaN", () => {
    assert.deepEqual(summary([]), { count: 0, average: null, top: null, pass: 0 });
  });

  check("sortBy numbers numerically, not lexicographically", () => {
    const nums = [{ n: 10 }, { n: 9 }, { n: 100 }, { n: 1 }];
    assert.deepEqual(sortBy(nums, "n").map(x => x.n), [1, 9, 10, 100]);
  });

  check("sortBy strings alphabetically, ascending and descending", () => {
    assert.deepEqual(sortBy(STUDENTS, "name").map(s => s.name),
                     ["Asha", "Bhanu", "Kiran", "Meena", "Ravi"]);
    assert.deepEqual(sortBy(STUDENTS, "marks", true).map(s => s.marks),
                     [91, 72, 66, 45, 38]);
  });

  check("sortBy does NOT mutate the original", () => {
    const before = STUDENTS.map(s => s.roll);
    sortBy(STUDENTS, "marks", true);
    assert.deepEqual(STUDENTS.map(s => s.roll), before);
  });

  check("addStudent returns a new array and rejects a duplicate roll", () => {
    const out = addStudent(STUDENTS, { roll: 26, name: "New", marks: 50, dept: "DS" });
    assert.equal(out.length, 6);
    assert.equal(STUDENTS.length, 5, "original untouched");
    assert.throws(() => addStudent(STUDENTS, { roll: 21, name: "X", marks: 1, dept: "DS" }),
                  /already exists/);
  });

  check("removeStudent", () => {
    assert.equal(removeStudent(STUDENTS, 23).length, 4);
    assert.equal(removeStudent(STUDENTS, 999).length, 5, "a missing roll is a no-op");
    assert.equal(STUDENTS.length, 5, "original untouched");
  });

  check("updateStudent copies rather than mutating", () => {
    const out = updateStudent(STUDENTS, 21, { marks: 99 });
    assert.equal(out.find(s => s.roll === 21).marks, 99);
    assert.equal(STUDENTS.find(s => s.roll === 21).marks, 72, "original untouched");
    assert.throws(() => updateStudent(STUDENTS, 999, {}), /not found/);
  });

  check("search across name, roll and department", () => {
    assert.equal(search(STUDENTS, "ash").length, 1);
    assert.equal(search(STUDENTS, "DS").length, 3);
    assert.equal(search(STUDENTS, "23").length, 1);
    assert.equal(search(STUDENTS, "").length, 5, "blank term returns everything");
    assert.equal(search(STUDENTS, "zzz").length, 0);
  });

  check("findByRoll returns null rather than undefined", () => {
    assert.equal(findByRoll(STUDENTS, 23).name, "Meena");
    assert.equal(findByRoll(STUDENTS, 999), null);
  });

  check("groupBy", () => {
    const g = groupBy(STUDENTS, "dept");
    assert.deepEqual(Object.keys(g).sort(), ["DS", "Stats"]);
    assert.equal(g.DS.length, 3);
    assert.equal(g.Stats.length, 2);
  });
}

/* ==================================================================
   Experiment 14 — JSON into a table
   ================================================================== */
banner("Experiment 14 — JSON into a table");
{
  const { toRows, sortRows, filterRows, summarise, renderTable, loadStudents,
          COLUMNS } = await mod("14_json_table.js");
  const data = JSON.parse(readLab("students.json"));

  check("students.json is valid JSON with the expected shape", () => {
    assert.equal(data.students.length, 5);
    assert.equal(typeof data.college, "string");
  });

  check("toRows flattens nested marks", () => {
    const rows = toRows(data);
    assert.equal(rows[0].name, "Asha Kumari");
    assert.equal(rows[0].maths, 88);
    assert.equal(rows[0].total, 179);
  });

  check("a student with no marks object yields nulls, not a TypeError", () => {
    const rows = toRows(data);
    const bhanu = rows.find(r => r.roll === 25);
    assert.equal(bhanu.maths, null);
    assert.equal(bhanu.stats, null);
    assert.equal(bhanu.total, 0);
  });

  check("summarise ignores rows without marks", () => {
    const s = summarise(toRows(data));
    assert.equal(s.count, 5);
    assert.equal(s.scored, 4);
    assert.equal(s.avgTotal, 155.5);     // (179+123+183+137)/4 = 622/4
    assert.equal(s.top, "Meena Devi");
  });

  check("sortRows sinks nulls to the bottom", () => {
    const sorted = sortRows(toRows(data), "maths");
    assert.equal(sorted.at(-1).roll, 25, "the row with no marks sorts last");
    assert.equal(sorted[0].maths, 65);
  });

  check("filterRows searches every column", () => {
    const rows = toRows(data);
    assert.equal(filterRows(rows, "Statistics").length, 2);
    assert.equal(filterRows(rows, "meena").length, 1, "must be case-insensitive");
    assert.equal(filterRows(rows, "").length, 5);
  });

  check("renderTable escapes markup instead of executing it", () => {
    const dom = new JSDOM("<table><tbody id='b'></tbody></table>");
    const doc = dom.window.document;
    const evil = [{ roll: 1, name: '<img src=x onerror="alert(1)">',
                    dept: "DS", maths: 1, stats: 2, total: 3 }];
    renderTable(evil, doc.getElementById("b"), doc);
    const cell = doc.querySelectorAll("td")[1];
    assert.equal(cell.querySelector("img"), null, "must NOT create an element");
    assert.equal(cell.textContent, '<img src=x onerror="alert(1)">');
  });

  check("renderTable emits one row per record and clears between renders", () => {
    const dom = new JSDOM("<table><tbody id='b'></tbody></table>");
    const doc = dom.window.document;
    const tbody = doc.getElementById("b");
    const rows = toRows(data);
    renderTable(rows, tbody, doc);
    assert.equal(tbody.querySelectorAll("tr").length, 5);
    assert.equal(tbody.querySelectorAll("tr")[0].children.length, COLUMNS.length);
    renderTable(rows.slice(0, 2), tbody, doc);
    assert.equal(tbody.querySelectorAll("tr").length, 2, "must clear first");
  });

  check("a null cell renders as a dash", () => {
    const dom = new JSDOM("<table><tbody id='b'></tbody></table>");
    const doc = dom.window.document;
    renderTable(toRows(data), doc.getElementById("b"), doc);
    const last = doc.querySelectorAll("tr")[4];
    assert.equal(last.children[3].textContent, "—");
    assert.equal(last.children[3].className, "missing");
  });

  await acheck("loadStudents throws on a 404 instead of parsing an error page", async () => {
    const stub = async () => ({ ok: false, status: 404, statusText: "Not Found" });
    await assert.rejects(() => loadStudents("x", stub), /HTTP 404/);
  });

  await acheck("loadStudents parses a successful response", async () => {
    const stub = async () => ({ ok: true, json: async () => data });
    const rows = await loadStudents("students.json", stub);
    assert.equal(rows.length, 5);
  });
}

/* ==================================================================
   Experiment 15 — weather API
   ================================================================== */
banner("Experiment 15 — weather API");
{
  const { summarise, toF, buildUrl, fetchWeather } = await mod("15_weather.js");
  const sample = JSON.parse(readLab("weather-sample.json"));

  check("summarise a real saved OpenWeatherMap response", () => {
    const w = summarise(sample);
    assert.equal(w.place, "Vijayawada");
    assert.equal(w.country, "IN");
    assert.equal(w.tempC, 30, "29.86 rounds to 30");
    assert.equal(w.feelsC, 34, "34.21 rounds to 34");
    assert.equal(w.humidity, 78);
    assert.equal(w.pressure, 1004);
    assert.equal(w.condition, "moderate rain");
    assert.equal(w.windMs, 4.63);
    assert.equal(w.cloudPct, 90);
  });

  check("summarise survives missing optional sections", () => {
    const w = summarise({ name: "X", main: { temp: 20, feels_like: 20, humidity: 50, pressure: 1000 } });
    assert.equal(w.condition, "unknown");
    assert.equal(w.windMs, null);
    assert.equal(w.cloudPct, null);
    assert.equal(w.country, "");
  });

  check("toF", () => {
    assert.equal(toF(0), 32);
    assert.equal(toF(100), 212);
    assert.equal(toF(30), 86);
    assert.equal(toF(-40), -40, "the one temperature where the scales meet");
  });

  check("buildUrl escapes a city name with a space", () => {
    const u = buildUrl("New Delhi", "KEY");
    assert.equal(u.searchParams.get("q"), "New Delhi");
    assert.equal(u.searchParams.get("units"), "metric");
    assert.ok(u.toString().includes("New+Delhi"), "must be escaped in the query string");
  });

  await acheck("fetchWeather maps HTTP statuses to useful messages", async () => {
    const stub = s => async () => ({ ok: false, status: s, statusText: "x" });
    await assert.rejects(() => fetchWeather("X", "k", stub(401)), /Invalid API key/);
    await assert.rejects(() => fetchWeather("X", "k", stub(404)), /not found/);
    await assert.rejects(() => fetchWeather("X", "k", stub(500)), /HTTP 500/);
    await assert.rejects(() => fetchWeather("X", ""), /API key is required/);
  });

  await acheck("fetchWeather returns the summary on success", async () => {
    const stub = async () => ({ ok: true, json: async () => sample });
    const w = await fetchWeather("Vijayawada", "k", stub);
    assert.equal(w.place, "Vijayawada");
    assert.equal(w.tempC, 30);
  });
}

/* ==================================================================
   Experiment 16 — DOM manipulation without jQuery
   ================================================================== */
banner("Experiment 16 — DOM manipulation");
{
  const { hide, show, toggle, fadeToggle, slideToggle, setMessage,
          wireTable, slideTo, appendItem, empty } = await mod("16_jquery_native.js");

  const makeDom = () => new JSDOM(`
    <div id="panel"></div>
    <p id="msg"></p>
    <div id="box"></div>
    <ul id="list"></ul>
    <table id="table"><tbody>
      <tr id="r1"><td>21</td><td>Asha</td>
        <td><button class="delete-btn"><span>Delete</span></button></td></tr>
      <tr id="r2"><td>22</td><td>Ravi</td>
        <td><button class="delete-btn">Delete</button></td></tr>
    </tbody></table>`);

  check("hide, show and toggle", () => {
    const doc = makeDom().window.document;
    const p = doc.getElementById("panel");
    hide(p);
    assert.ok(p.classList.contains("is-hidden"));
    show(p);
    assert.ok(!p.classList.contains("is-hidden"));
    toggle(p);
    assert.ok(p.classList.contains("is-hidden"));
    toggle(p);
    assert.ok(!p.classList.contains("is-hidden"));
  });

  check("fadeToggle and slideToggle are independent", () => {
    const doc = makeDom().window.document;
    const p = doc.getElementById("panel");
    fadeToggle(p);
    assert.ok(p.classList.contains("is-faded"));
    slideToggle(p);
    assert.ok(p.classList.contains("is-collapsed"));
    assert.ok(p.classList.contains("is-faded"), "the fade must survive");
  });

  check("setMessage swaps the class rather than accumulating classes", () => {
    const doc = makeDom().window.document;
    const m = doc.getElementById("msg");
    setMessage(m, "Saved successfully", "success");
    assert.equal(m.textContent, "Saved successfully");
    assert.ok(m.classList.contains("success"));
    setMessage(m, "Could not save", "error");
    assert.ok(m.classList.contains("error"));
    assert.ok(!m.classList.contains("success"), "the old class must be removed");
  });

  check("setMessage escapes markup", () => {
    const doc = makeDom().window.document;
    const m = doc.getElementById("msg");
    setMessage(m, "<b>bold</b>");
    assert.equal(m.querySelector("b"), null);
    assert.equal(m.textContent, "<b>bold</b>");
  });

  check("delegation: clicking a delete button marks the right row", () => {
    const dom = makeDom();
    const doc = dom.window.document;
    wireTable(doc.getElementById("table"));
    doc.querySelector("#r1 .delete-btn").click();
    assert.ok(doc.getElementById("r1").classList.contains("fading"));
    assert.ok(!doc.getElementById("r2").classList.contains("fading"),
              "only the clicked row");
  });

  check("delegation works when the click lands on a child of the button", () => {
    const dom = makeDom();
    const doc = dom.window.document;
    wireTable(doc.getElementById("table"));
    doc.querySelector("#r1 .delete-btn span").click();   // e.target is the SPAN
    assert.ok(doc.getElementById("r1").classList.contains("fading"),
              "closest() must walk up from the target to the button");
  });

  check("a click elsewhere in the table does nothing", () => {
    const dom = makeDom();
    const doc = dom.window.document;
    wireTable(doc.getElementById("table"));
    doc.querySelector("#r1 td").click();
    assert.ok(!doc.getElementById("r1").classList.contains("fading"));
  });

  check("delegation catches rows added AFTER wiring", () => {
    const dom = makeDom();
    const doc = dom.window.document;
    wireTable(doc.getElementById("table"));
    const tr = doc.createElement("tr");
    tr.id = "r3";
    tr.innerHTML = '<td>24</td><td>New</td><td><button class="delete-btn">Delete</button></td>';
    doc.querySelector("tbody").append(tr);
    doc.querySelector("#r3 .delete-btn").click();
    assert.ok(doc.getElementById("r3").classList.contains("fading"),
              "this is the whole point of delegation");
  });

  check("slideTo sets a transform", () => {
    const doc = makeDom().window.document;
    const b = doc.getElementById("box");
    slideTo(b, 250);
    assert.equal(b.style.transform, "translateX(250px)");
    slideTo(b, 0);
    assert.equal(b.style.transform, "translateX(0px)");
  });

  check("appendItem and empty", () => {
    const doc = makeDom().window.document;
    const list = doc.getElementById("list");
    appendItem(list, "One", doc);
    appendItem(list, "<b>Two</b>", doc);
    assert.equal(list.children.length, 2);
    assert.equal(list.children[1].textContent, "<b>Two</b>");
    assert.equal(list.querySelector("b"), null, "must be escaped");
    empty(list);
    assert.equal(list.children.length, 0);
  });
}

/* ==================================================================
   Structural checks on every HTML file
   ================================================================== */
banner("HTML structure — all pages");
{
  const pages = readdirSync(LABS).filter(f => f.endsWith(".html")).sort();

  check(`all ${pages.length} pages present`, () => {
    assert.equal(pages.length, 16, "one page per experiment, 11 having a separate .js");
  });

  for (const page of pages) {
    const src = readLab(page);
    const dom = new JSDOM(src);
    const doc = dom.window.document;

    check(`${page} — head essentials`, () => {
      assert.ok(/^<!DOCTYPE html>/i.test(src.trim()), "missing <!DOCTYPE html>");
      assert.ok(doc.querySelector("meta[charset]"), "missing <meta charset>");
      assert.ok(doc.querySelector('meta[name="viewport"]'), "missing viewport meta");
      assert.ok(doc.querySelector("title")?.textContent.trim(), "missing <title>");
      assert.equal(doc.documentElement.getAttribute("lang"), "en", "missing lang on <html>");
    });

    check(`${page} — every <img> has alt`, () => {
      for (const img of doc.querySelectorAll("img"))
        assert.ok(img.hasAttribute("alt"),
                  `<img src="${img.getAttribute("src")}"> has no alt`);
    });

    check(`${page} — every <label for> resolves`, () => {
      for (const label of doc.querySelectorAll("label[for]")) {
        const id = label.getAttribute("for");
        assert.ok(doc.getElementById(id),
                  `<label for="${id}"> points at no element`);
      }
    });

    check(`${page} — ids are unique`, () => {
      const ids = [...doc.querySelectorAll("[id]")].map(e => e.id);
      const dupes = ids.filter((v, i) => ids.indexOf(v) !== i);
      assert.deepEqual(dupes, [], `duplicate ids: ${dupes.join(", ")}`);
    });

    check(`${page} — every submitting control has a name`, () => {
      for (const form of doc.querySelectorAll("form")) {
        for (const el of form.querySelectorAll("input, select, textarea")) {
          if (["submit", "reset", "button"].includes(el.type)) continue;
          assert.ok(el.getAttribute("name"),
                    `<${el.tagName.toLowerCase()} id="${el.id}"> has no name`);
        }
      }
    });

    check(`${page} — radio groups share a name`, () => {
      const byName = {};
      for (const r of doc.querySelectorAll('input[type="radio"]'))
        (byName[r.name] ??= []).push(r);
      for (const [name, group] of Object.entries(byName))
        assert.ok(group.length >= 2 || name === "",
                  `radio group "${name}" has only one button — check the names`);
    });

    check(`${page} — every referenced local file exists`, () => {
      const refs = [
        ...[...doc.querySelectorAll("link[href]")].map(e => e.getAttribute("href")),
        ...[...doc.querySelectorAll("script[src]")].map(e => e.getAttribute("src")),
        ...[...doc.querySelectorAll("img[src]")].map(e => e.getAttribute("src"))
      ].filter(u => u && !/^(https?:)?\/\//.test(u));

      for (const ref of refs) {
        const p = path.join(LABS, ref.replace(/^\.\//, ""));
        assert.ok(readdirSync(path.dirname(p)).includes(path.basename(p)),
                  `${ref} does not exist`);
      }
    });
  }

  check("no page uses innerHTML with unescaped interpolation", () => {
    // A crude but effective guard: flag `innerHTML = ` followed by a template
    // literal containing ${, which is the XSS shape this course warns about.
    for (const page of pages) {
      const src = readLab(page);
      assert.ok(!/innerHTML\s*=\s*`[^`]*\$\{/.test(src),
                `${page} interpolates into innerHTML`);
    }
    for (const f of readdirSync(LABS).filter(f => f.endsWith(".js"))) {
      const src = readLab(f);
      assert.ok(!/innerHTML\s*=\s*`[^`]*\$\{/.test(src),
                `${f} interpolates into innerHTML`);
    }
  });
}

/* ================================================================== */
banner("Summary");
console.log(`${passed} passed, ${failed} failed`);
process.exit(failed === 0 ? 0 : 1);
