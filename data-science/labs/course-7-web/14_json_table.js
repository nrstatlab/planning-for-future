/* Experiment 14 — Fetch and display student information held in JSON.
 *
 * Three deliberate choices in renderTable, each worth a mark in the viva:
 *
 *   1. textContent, NOT innerHTML. The data came from a file or an API, so a
 *      name of "<img src=x onerror=alert(1)>" must render as text. This is
 *      the XSS rule from Unit 4, in the one place students most often break it.
 *
 *   2. A DocumentFragment. Rows are built off-document and inserted once, so
 *      the browser reflows once instead of once per row.
 *
 *   3. Optional chaining on s.marks?.maths. One student in students.json has
 *      no marks object at all; without the ?. the whole render throws and the
 *      page goes blank instead of showing a dash.
 */

export const COLUMNS = ["roll", "name", "dept", "maths", "stats", "total"];

export function toRows(data) {
  return data.students.map(s => ({
    roll:  s.roll,
    name:  s.name,
    dept:  s.dept,
    maths: s.marks?.maths ?? null,
    stats: s.marks?.stats ?? null,
    total: (s.marks?.maths ?? 0) + (s.marks?.stats ?? 0)
  }));
}

export function sortRows(rows, key, desc = false) {
  return [...rows].sort((a, b) => {
    const [x, y] = desc ? [b[key], a[key]] : [a[key], b[key]];
    if (x === null) return 1;              // nulls always sink to the bottom
    if (y === null) return -1;
    return typeof x === "string" ? x.localeCompare(y) : x - y;
  });
}

export function filterRows(rows, term) {
  const t = String(term).trim().toLowerCase();
  if (t === "") return rows;
  return rows.filter(r =>
    Object.values(r).some(v => String(v ?? "").toLowerCase().includes(t)));
}

export function summarise(rows) {
  const scored = rows.filter(r => r.maths !== null && r.stats !== null);
  if (scored.length === 0) return { count: rows.length, avgTotal: null, top: null };
  const sum = scored.reduce((a, r) => a + r.total, 0);
  return {
    count:    rows.length,
    scored:   scored.length,
    avgTotal: +(sum / scored.length).toFixed(2),
    top:      sortRows(scored, "total", true)[0].name
  };
}

export function renderTable(rows, tbody, doc = document) {
  tbody.textContent = "";
  const frag = doc.createDocumentFragment();

  for (const r of rows) {
    const tr = doc.createElement("tr");
    for (const col of COLUMNS) {
      const td = doc.createElement("td");
      td.textContent = r[col] ?? "—";
      if (r[col] === null) td.className = "missing";
      tr.append(td);
    }
    frag.append(tr);
  }

  tbody.append(frag);                       // ONE insertion into the document
  return tbody;
}

/** Load and parse, with the two guards that matter.
 *  fetchFn is injectable so the runner can test the failure path offline. */
export async function loadStudents(url = "students.json", fetchFn = fetch) {
  const res = await fetchFn(url);
  // fetch does NOT reject on 404 — an error status is still a successful HTTP
  // transaction. Skip this check and you call .json() on an HTML error page.
  if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
  return toRows(await res.json());
}
