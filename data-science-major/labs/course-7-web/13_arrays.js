/* Experiment 13 — Manipulate arrays and objects: add, delete, sort, search.
 *
 * Every function here is PURE: it takes the list and returns a new one rather
 * than mutating in place. That is why addStudent spreads instead of pushing,
 * and why sortBy copies with [...list] before sorting — Array.prototype.sort
 * mutates, and a sort that silently reorders the caller's array is a bug that
 * surfaces three functions away from its cause.
 */

export const STUDENTS = [
  { roll: 21, name: "Asha",  marks: 72, dept: "DS"    },
  { roll: 22, name: "Ravi",  marks: 45, dept: "DS"    },
  { roll: 23, name: "Meena", marks: 91, dept: "Stats" },
  { roll: 24, name: "Kiran", marks: 66, dept: "DS"    },
  { roll: 25, name: "Bhanu", marks: 38, dept: "Stats" }
];

export function addStudent(list, student) {
  if (list.some(s => s.roll === student.roll))
    throw new Error(`Roll ${student.roll} already exists`);
  return [...list, student];
}

export const removeStudent = (list, roll) => list.filter(s => s.roll !== roll);

export function updateStudent(list, roll, changes) {
  if (!list.some(s => s.roll === roll))
    throw new Error(`Roll ${roll} not found`);
  return list.map(s => (s.roll === roll ? { ...s, ...changes } : s));
}

/** Sort by any key, ascending or descending.
 *
 * The comparator branches on type because sort() with no comparator compares
 * as STRINGS: [10, 9, 100].sort() gives [10, 100, 9]. Numbers need x - y;
 * strings need localeCompare, which also orders accented letters correctly.
 */
export const sortBy = (list, key, desc = false) =>
  [...list].sort((a, b) => {
    const [x, y] = desc ? [b[key], a[key]] : [a[key], b[key]];
    return typeof x === "string" ? x.localeCompare(y) : x - y;
  });

export function search(list, term) {
  const t = String(term).trim().toLowerCase();
  if (t === "") return list;
  return list.filter(s => s.name.toLowerCase().includes(t)
                       || String(s.roll).includes(t)
                       || s.dept.toLowerCase().includes(t));
}

export const findByRoll = (list, roll) => list.find(s => s.roll === roll) ?? null;

/** Group into { dept: [names] } — the JavaScript equivalent of SQL's GROUP BY
 *  and of Course 9's df.groupby("dept"). */
export function groupBy(list, key) {
  const out = {};
  for (const item of list) (out[item[key]] ||= []).push(item);
  return out;
}

export function summary(list) {
  if (list.length === 0) return { count: 0, average: null, top: null, pass: 0 };
  const total = list.reduce((sum, s) => sum + s.marks, 0);
  return {
    count:   list.length,
    average: +(total / list.length).toFixed(2),
    top:     sortBy(list, "marks", true)[0].name,
    pass:    list.filter(s => s.marks >= 50).length
  };
}
