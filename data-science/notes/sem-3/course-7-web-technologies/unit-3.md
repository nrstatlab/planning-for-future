# Unit 3 — JavaScript

**Syllabus topics:** What is DHTML, JavaScript, basics, variables, operators,
statements, string manipulations, mathematical functions, arrays, functions,
objects, regular expressions, exception handling.

---

## 3.1 DHTML

### 🎯 The big idea

**DHTML** — Dynamic HTML — is not a language. It is a *name for the combination*
of HTML, CSS, JavaScript and the DOM used to change a page after it has loaded.

| Component | Role in DHTML |
|---|---|
| HTML | The initial structure |
| CSS | The presentation to be changed |
| JavaScript | The code that changes it |
| **DOM** | The interface through which JavaScript reaches HTML and CSS |

The term dates from around 1997 and is largely historical; nobody says "DHTML"
in industry now. It is examined, so know the definition — and know that
answering "DHTML is a scripting language" loses the mark.

## 3.2 What JavaScript is

Created by **Brendan Eich at Netscape in 1995**, reportedly in ten days.
Standardised as **ECMAScript**; ES6 (2015) is the version that modernised it,
and everything since is named by year (ES2016, ES2017, …).

### ⚠️ JavaScript is not Java

| | JavaScript | Java |
|---|---|---|
| Typing | Dynamic, weak | Static, strong |
| Runs in | Browser / Node.js | JVM |
| Compilation | Interpreted / JIT | Compiled to bytecode |
| Inheritance | Prototypal | Class-based |
| Origin | Netscape, 1995 | Sun, 1995 |

The name was a marketing decision. The languages are unrelated. This *is* an
exam question.

### Where the code goes

```html
<script>
  console.log("inline");
</script>

<script src="app.js"></script>          <!-- blocks parsing -->
<script src="app.js" defer></script>    <!-- downloads now, runs after parse -->
<script src="app.js" async></script>    <!-- downloads now, runs whenever ready -->
```

| Attribute | Downloads | Executes | Order preserved |
|---|---|---|---|
| none | Immediately, **blocking** | Immediately | Yes |
| `defer` | In parallel | After HTML is parsed | **Yes** |
| `async` | In parallel | As soon as it arrives | **No** |

**Use `defer` in the `<head>`.** It gets the download started early and still
guarantees the DOM exists when the code runs. A plain `<script>` in the head
that touches the DOM will fail, because the elements do not exist yet — which
is why the old advice was "put scripts at the end of `<body>`".

## 3.3 Variables

| Keyword | Scope | Re-assign | Re-declare | Hoisted as |
|---|---|---|---|---|
| `var` | **Function** | Yes | Yes | `undefined` |
| `let` | **Block** | Yes | No | Temporal dead zone |
| `const` | **Block** | **No** | No | Temporal dead zone |

**Rule: `const` by default, `let` when it must change, `var` never.**

```js
if (true) {
  var  a = 1;
  let  b = 2;
}
console.log(a);   // 1  — var leaked out of the block
console.log(b);   // ReferenceError — let did not
```

### ⚠️ `const` does not mean immutable

It means the **binding** cannot be reassigned. The object it points at can
still be changed.

```js
const arr = [1, 2, 3];
arr.push(4);        // fine — arr still points at the same array
arr = [9];          // TypeError: Assignment to constant variable
```

Use `Object.freeze(obj)` if you actually need the contents locked.

### The eight types

Seven primitives plus objects:

`number`, `string`, `boolean`, `undefined`, `null`, `symbol`, `bigint`, and
`object` (which covers arrays, functions and dates).

```js
typeof 42            // "number"
typeof "hi"          // "string"
typeof true          // "boolean"
typeof undefined     // "undefined"
typeof null          // "object"   ← a famous bug, kept for compatibility
typeof [1,2]         // "object"
typeof function(){}  // "function"
```

`typeof null === "object"` is wrong and has been since 1995. It cannot be fixed
without breaking the web. Use `Array.isArray(x)` to test for arrays, since
`typeof` will not tell you.

**`undefined` vs `null`** — `undefined` means "no value has been assigned"
(the language's doing); `null` means "deliberately empty" (the programmer's
doing).

## 3.4 Operators

| Category | Operators |
|---|---|
| Arithmetic | `+ - * / % ** ++ --` |
| Assignment | `= += -= *= /= %= **=` |
| Comparison | `== != === !== > < >= <=` |
| Logical | `&& \|\| !` |
| Ternary | `cond ? a : b` |
| Nullish | `??`, `??=` |
| Optional chain | `?.` |
| Spread / rest | `...` |
| String | `+` concatenation |

### 🔢 `==` vs `===`

`==` converts types before comparing. `===` does not.

```js
5 == "5"          // true   — string converted to number
5 === "5"         // false  — different types
0 == false        // true
0 === false       // false
null == undefined // true
null === undefined// false
NaN == NaN        // false  — NaN equals nothing, itself included
[] == false       // true   — [] → "" → 0
```

**Always use `===`.** The coercion rules of `==` are genuinely surprising and
no real program benefits from them. The one accepted exception is
`x == null`, which tests for `null` **or** `undefined` in one go.

To test for `NaN`, use `Number.isNaN(x)` — never `x === NaN`.

### Truthy and falsy

Exactly **eight** falsy values; everything else is truthy.

```
false, 0, -0, 0n, "", null, undefined, NaN
```

Note what is **truthy**: `"0"`, `"false"`, `[]`, `{}`. An empty array being
truthy catches people constantly — use `arr.length === 0` to test emptiness.

### `??` vs `||`

```js
const a = 0 || 10;    // 10  — 0 is falsy, so the fallback fires
const b = 0 ?? 10;    // 0   — 0 is not null/undefined, so it is kept
```

`||` falls back on any falsy value; `??` falls back only on `null` and
`undefined`. When 0 or `""` are legitimate values — a count, a search box — `??`
is the correct operator.

### Optional chaining

```js
const city = user?.address?.city;        // undefined instead of TypeError
const n    = list?.length ?? 0;
obj.method?.();                          // call only if it exists
```

Without `?.`, reading `.city` of an undefined `address` throws.

## 3.5 Statements

```js
// conditionals
if (x > 0) { … } else if (x < 0) { … } else { … }

switch (day) {
  case "Sat":
  case "Sun": type = "weekend"; break;
  default:    type = "weekday";
}

// loops
for (let i = 0; i < n; i++)      { … }
for (const v of array)           { … }   // values     — arrays, strings, sets
for (const k in object)          { … }   // keys       — objects
while (cond)   { … }
do { … } while (cond);
```

### ⚠️ `for…in` vs `for…of`

| | `for…in` | `for…of` |
|---|---|---|
| Iterates | **Keys / indices** | **Values** |
| Works on | Objects (and arrays, badly) | Arrays, strings, Maps, Sets |
| Array order | Not guaranteed | Guaranteed |
| Inherited keys | **Included** | N/A |

```js
const a = ["x", "y"];
for (const i of a) console.log(i);   // x, y
for (const i in a) console.log(i);   // "0", "1"  ← strings, not numbers
```

Using `for…in` on an array is a bug waiting to happen: the indices are strings,
so `i + 1` gives `"01"`.

`switch` compares with `===`, and a missing `break` falls through to the next
case — occasionally deliberate, usually a bug.

## 3.6 Functions

```js
// declaration — hoisted, callable before its definition
function add(a, b) { return a + b; }

// expression — not hoisted
const sub = function (a, b) { return a - b; };

// arrow — not hoisted, no own `this`
const mul = (a, b) => a * b;
const sq  = x => x * x;
const mk  = () => ({ ok: true });      // parenthesise a returned object literal

// default and rest parameters
function greet(name = "student", ...rest) {
  return `Hello, ${name}! (${rest.length} extra)`;
}
```

### Arrow functions vs regular functions

| | Regular | Arrow |
|---|---|---|
| `this` | Depends on **how it is called** | Inherited from enclosing scope |
| `arguments` object | Yes | No |
| Usable as constructor | Yes | **No** |
| Hoisted (declaration form) | Yes | No |
| Implicit return | No | Yes, with no braces |

The `this` difference is the one that matters, and Unit 4 shows why: inside an
event handler written as a regular function, `this` is the element; inside an
arrow function it is not.

### Closures

A **closure** is a function that keeps access to the variables of the scope it
was created in, even after that scope has returned.

```js
function counter() {
  let count = 0;                 // private — nothing outside can touch it
  return {
    increment: () => ++count,
    value:     () => count
  };
}
const c = counter();
c.increment();  c.increment();
console.log(c.value());          // 2
```

`count` survives because the returned functions still reference it. This is how
JavaScript did private state for twenty years, and it is a standard exam
question.

**The classic closure bug:**

```js
for (var i = 0; i < 3; i++) setTimeout(() => console.log(i), 0);  // 3 3 3
for (let i = 0; i < 3; i++) setTimeout(() => console.log(i), 0);  // 0 1 2
```

`var` has one function-scoped binding shared by all three callbacks, and by the
time they run the loop has finished. `let` creates a fresh binding per
iteration. This exact example appears in interviews and exams alike.

### 💡 Hoisting

Declarations are processed before any code runs.

```js
console.log(f());    // "works"  — function declarations hoist entirely
function f() { return "works"; }

console.log(v);      // undefined — the var declaration hoisted, not the value
var v = 5;

console.log(l);      // ReferenceError — let is in the temporal dead zone
let l = 5;
```

## 3.7 String manipulation

Strings are **immutable**: every method returns a new string.

```js
const s = "Data Science";

s.length                 // 12
s.toUpperCase()          // "DATA SCIENCE"
s.toLowerCase()          // "data science"
s.charAt(0)              // "D"
s[0]                     // "D"
s.indexOf("Science")     // 5      (-1 if absent)
s.lastIndexOf("a")       // 3
s.includes("Sci")        // true
s.startsWith("Data")     // true
s.endsWith("ce")         // true
s.slice(0, 4)            // "Data"
s.slice(-7)              // "Science"     ← negative counts from the end
s.substring(0, 4)        // "Data"        ← negatives clamp to 0
s.replace("Data", "Web") // "Web Science" ← first match only
s.replaceAll("a", "@")   // "D@t@ Science"
s.split(" ")             // ["Data", "Science"]
"  hi  ".trim()          // "hi"
"5".padStart(3, "0")     // "005"
"ab".repeat(3)           // "ababab"
s.concat("!")            // "Data Science!"
[...s].reverse().join("")// "ecneicS ataD"
```

### ⚠️ `slice` vs `substring` vs `substr`

| | Negative indices | Swaps arguments if start > end |
|---|---|---|
| `slice(a, b)` | **Counts from the end** | No — returns `""` |
| `substring(a, b)` | Treated as 0 | **Yes** |
| `substr(a, len)` | Deprecated | — |

Use `slice`. `substring`'s silent argument-swapping hides bugs, and `substr` is
deprecated.

### Template literals

```js
const name = "Priya", marks = 87;
const msg = `${name} scored ${marks}%, which is ${marks >= 75 ? "a distinction" : "a pass"}.`;
const multi = `line one
line two`;
```

Backticks, `${}` for interpolation, real newlines allowed. Prefer them to `+`
concatenation.

**Worked example.** Count the vowels in a string, three ways.

```js
function countVowels(s) {
  let n = 0;
  for (const ch of s.toLowerCase()) if ("aeiou".includes(ch)) n++;
  return n;
}
const countVowels2 = s => (s.match(/[aeiou]/gi) || []).length;
const countVowels3 = s => [...s].filter(c => "aeiouAEIOU".includes(c)).length;

countVowels("Data Science");   // 5  — a, a, i, e, e
```

The `|| []` in the second version matters: `match` returns `null`, not an empty
array, when nothing matches, and `null.length` throws. This is lab experiment 10.

## 3.8 Mathematical functions

```js
Math.PI            // 3.141592653589793
Math.E             // 2.718281828459045

Math.abs(-5)       // 5
Math.round(4.5)    // 5      — .5 always rounds UP, so -4.5 → -4
Math.floor(4.9)    // 4      — toward -∞
Math.ceil(4.1)     // 5      — toward +∞
Math.trunc(-4.9)   // -4     — toward zero
Math.sign(-3)      // -1
Math.pow(2, 10)    // 1024   — or 2 ** 10
Math.sqrt(144)     // 12
Math.cbrt(27)      // 3
Math.min(3, 1, 2)  // 1
Math.max(3, 1, 2)  // 3
Math.min(...[3,1,2])  // 1   — spread, since min takes arguments not an array
Math.random()      // [0, 1)
Math.log(Math.E)   // 1      — NATURAL log
Math.log10(1000)   // 3
Math.log2(8)       // 3
Math.exp(1)        // 2.718…
Math.hypot(3, 4)   // 5
Math.sin(Math.PI/2)// 1      — radians, not degrees
```

### ⚠️ `Math.round(-4.5)` is `-4`

JavaScript rounds half **up** (toward +∞), not away from zero. So
`Math.round(4.5) === 5` but `Math.round(-4.5) === -4`. Note also that
`Math.log` is the natural logarithm, not base 10 — a frequent error when
porting formulas.

### Random integers

```js
// integer in [min, max] inclusive
const randInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
randInt(1, 6);   // a die roll
```

The `+ 1` is essential. `Math.random()` never returns 1, so without it the
maximum is unreachable — an off-by-one that is easy to miss because it only
shows up in the distribution.

### Number formatting and floating point

```js
(3.14159).toFixed(2)          // "3.14"   ← a STRING
(1234.5678).toFixed(0)        // "1235"
parseInt("42px")              // 42
parseInt("08")                // 8
parseFloat("3.14abc")         // 3.14
Number("42")                  // 42
Number("42px")                // NaN      ← stricter than parseInt
Number.isInteger(5.0)         // true
(1234567.891).toLocaleString("en-IN")   // "12,34,567.891"

0.1 + 0.2                     // 0.30000000000000004
0.1 + 0.2 === 0.3             // false
Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON   // true — the correct test
```

Floating-point binary cannot represent 0.1 exactly, exactly as in C (Course 2)
and Python (Course 3). **Never compare floats with `===`.** For money, work in
paise as integers.

## 3.9 Arrays

```js
const a = [10, 20, 30];
const b = new Array(3);       // length 3, all empty — rarely what you want
const c = Array.of(3);        // [3]
const d = Array.from("abc");  // ["a","b","c"]
```

### Mutating methods — they change the original

| Method | Effect | Returns |
|---|---|---|
| `push(x)` | Add to **end** | New length |
| `pop()` | Remove from end | The element |
| `unshift(x)` | Add to **front** | New length |
| `shift()` | Remove from front | The element |
| `splice(i, n, ...items)` | Remove `n` at `i`, insert items | Removed elements |
| `sort(cmp)` | Sort **in place** | The array |
| `reverse()` | Reverse in place | The array |
| `fill(v)` | Overwrite | The array |

### Non-mutating methods — they return something new

| Method | Returns |
|---|---|
| `slice(a, b)` | A shallow copy of a range |
| `concat(arr)` | Joined array |
| `join(sep)` | A string |
| `indexOf(x)` / `includes(x)` | Index / boolean |
| `map(fn)` | New array, same length |
| `filter(fn)` | New array, ≤ length |
| `reduce(fn, init)` | A single value |
| `find(fn)` / `findIndex(fn)` | First match / its index |
| `some(fn)` / `every(fn)` | Boolean |
| `flat(d)` / `flatMap(fn)` | Flattened |
| `at(i)` | Element, **negatives allowed** |

```js
const marks = [72, 45, 91, 66, 38];

marks.map(m => m + 5)                    // [77, 50, 96, 71, 43]
marks.filter(m => m >= 50)               // [72, 91, 66]
marks.reduce((s, m) => s + m, 0)         // 312
marks.reduce((s, m) => s + m, 0) / marks.length   // 62.4
marks.find(m => m < 50)                  // 45
marks.some(m => m > 90)                  // true
marks.every(m => m > 30)                 // true
marks.at(-1)                             // 38
[...marks].sort((x, y) => y - x)         // [91,72,66,45,38] — copy first
```

### ⚠️ `sort()` sorts as strings by default

```js
[10, 9, 100, 1].sort()                   // [1, 10, 100, 9]   ← wrong
[10, 9, 100, 1].sort((a, b) => a - b)    // [1, 9, 10, 100]   ← right
```

The default converts every element to a string and compares lexicographically,
so `"100" < "9"`. **Always pass a comparator for numbers.** And remember `sort`
mutates — spread into a copy first if the original matters.

For strings with accents or non-English text, use
`arr.sort((a, b) => a.localeCompare(b))`.

**Worked example.** From an array of student objects, get the names of those
who passed, sorted by descending mark.

```js
const students = [
  { name: "Asha",   mark: 72 },
  { name: "Ravi",   mark: 45 },
  { name: "Meena",  mark: 91 },
  { name: "Kiran",  mark: 66 }
];

const passers = students
  .filter(s => s.mark >= 50)
  .sort((a, b) => b.mark - a.mark)
  .map(s => s.name);
// ["Meena", "Asha", "Kiran"]
```

That chain — filter, sort, map — is the shape of most real array code, and it
is exactly what Course 9's Pandas does with `df[df.mark >= 50]`.

### Destructuring and spread

```js
const [first, second, ...rest] = [1, 2, 3, 4, 5];   // 1, 2, [3,4,5]
const { name, mark = 0 } = students[0];
const copy   = [...marks];                          // shallow copy
const merged = [...a, ...b];
const maxOf  = Math.max(...marks);                  // 91
[x, y] = [y, x];                                    // swap
```

## 3.10 Objects

```js
const student = {
  name: "Asha",
  roll: 23,
  marks: { maths: 88, stats: 91 },
  greet() { return `Hi, ${this.name}`; }             // shorthand method
};

student.name             // dot notation
student["name"]          // bracket — needed for dynamic or odd keys
student.marks.stats      // 91
student.email = "a@x.in" // add
delete student.roll      // remove
"name" in student        // true
Object.keys(student)     // ["name","marks","greet","email"]
Object.values(student)
Object.entries(student)  // [[k, v], …]
Object.assign({}, student, { roll: 24 })
{ ...student, roll: 24 } // spread — the modern equivalent
Object.freeze(student)   // shallow immutability
```

### 💡 `this`

`this` is decided by **how a function is called**, not where it is written.

| Call form | `this` |
|---|---|
| `obj.method()` | `obj` |
| `plainFunction()` | `undefined` in strict mode, `window` otherwise |
| `new Ctor()` | The new object |
| `fn.call(o)` / `.apply(o)` / `.bind(o)` | `o` |
| Arrow function | The enclosing scope's `this` — cannot be changed |

```js
const o = {
  name: "obj",
  bad() { setTimeout(function () { console.log(this.name); }, 0); }, // undefined
  good(){ setTimeout(() => console.log(this.name), 0); }             // "obj"
};
```

The arrow function has no `this` of its own, so it uses `good`'s — which is
`o`. This is the single most useful thing arrows do.

### Classes

ES6 syntax over the same prototype machinery.

```js
class Student {
  #private = "hidden";                 // truly private field
  static count = 0;

  constructor(name, marks) {
    this.name = name;
    this.marks = marks;
    Student.count++;
  }
  get average() {                      // accessed as s.average, no parentheses
    return this.marks.reduce((a, b) => a + b, 0) / this.marks.length;
  }
  toString() { return `${this.name} (${this.average.toFixed(1)})`; }
}

class Topper extends Student {
  constructor(name, marks, prize) {
    super(name, marks);                // MUST come before any use of `this`
    this.prize = prize;
  }
  toString() { return super.toString() + ` 🏆 ${this.prize}`; }
}

const t = new Topper("Meena", [91, 88, 95], "Gold");
console.log(String(t));                // "Meena (91.3) 🏆 Gold"
```

Forgetting `super()` in a derived constructor is a `ReferenceError`, not a
silent failure.

## 3.11 Regular expressions

```js
const re1 = /\d{3}-\d{4}/;              // literal
const re2 = new RegExp("\\d{3}", "g");  // from a string — note doubled backslashes
```

| Flag | Meaning |
|---|---|
| `g` | Global — all matches |
| `i` | Case-insensitive |
| `m` | `^`/`$` match line boundaries |
| `s` | `.` also matches newline |
| `u` | Unicode |

| Pattern | Matches |
|---|---|
| `.` | Any character except newline |
| `\d` `\D` | Digit / non-digit |
| `\w` `\W` | `[A-Za-z0-9_]` / not |
| `\s` `\S` | Whitespace / not |
| `\b` | Word boundary |
| `[abc]` `[^abc]` | Set / negated set |
| `[a-z]` | Range |
| `^` `$` | Start / end of string (or line with `m`) |
| `*` `+` `?` | 0+, 1+, 0 or 1 |
| `{n}` `{n,}` `{n,m}` | Exactly / at least / between |
| `*?` `+?` | **Lazy** — as few as possible |
| `(…)` | Capture group |
| `(?:…)` | Non-capturing group |
| `(?<name>…)` | Named group |
| `a\|b` | Alternation |

```js
const s = "Roll 23, marks 88 and 91";

/\d+/.test(s)                    // true
s.match(/\d+/g)                  // ["23", "88", "91"]
s.replace(/\d+/g, "#")           // "Roll #, marks # and #"
s.search(/marks/)                // 10
"a1b2".split(/\d/)               // ["a", "b", ""]

const m = "2026-08-26".match(/(?<y>\d{4})-(?<mo>\d{2})-(?<d>\d{2})/);
m.groups.y                       // "2026"
```

### Common validation patterns

```js
const patterns = {
  email:  /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/,
  phoneIN:/^[6-9]\d{9}$/,
  pin:    /^[1-9]\d{5}$/,
  strong: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/,
  date:   /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/
};
patterns.email.test("asha@nrstat.in")   // true
```

The password pattern uses **lookaheads** — `(?=…)` asserts that something can
be matched from here without consuming it. Four lookaheads mean "must contain a
lowercase, an uppercase, a digit and a symbol", in any order, and `.{8,}` then
does the actual matching.

### ⚠️ Two regex traps

**The `g` flag makes `test()` stateful.** A regex with `g` remembers
`lastIndex` between calls:

```js
const re = /\d/g;
re.test("a1");   // true
re.test("a1");   // false  ← resumed from lastIndex
```

Do not use `g` with `test()`, or reset `re.lastIndex = 0`.

**Never validate email with a "perfect" regex.** The fully RFC-compliant
pattern is thousands of characters long and still cannot tell you the address
exists. Check for a plausible shape, then send a confirmation mail. The
simplest sound check is `/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/`.

**Worked example.** Extract every mark from a report line and average them.

```js
const line = "Maths 88, Stats 91, CS 79";
const marks = line.match(/\d+/g).map(Number);          // [88, 91, 79]
const avg   = marks.reduce((a, b) => a + b, 0) / marks.length;  // 86
```

`.map(Number)` is essential — `match` returns **strings**, and without it
`"88" + "91"` is `"8891"`.

## 3.12 Exception handling

```js
try {
  const data = JSON.parse(input);
  if (!data.name) throw new Error("name is required");
  process(data);
} catch (err) {
  console.error(err.name, err.message);
} finally {
  cleanup();                 // runs whether or not an exception occurred
}
```

`catch` may omit its binding (`catch { … }`) if you do not need the error.

### Built-in error types

| Type | Thrown when |
|---|---|
| `Error` | Generic base |
| `SyntaxError` | Bad syntax — including `JSON.parse` of invalid text |
| `TypeError` | Wrong type — `null.foo`, calling a non-function |
| `ReferenceError` | Undeclared variable, or TDZ access |
| `RangeError` | Out of range — bad array length, deep recursion |
| `URIError` | Malformed URI |

### Custom errors

```js
class ValidationError extends Error {
  constructor(field, message) {
    super(message);
    this.name  = "ValidationError";
    this.field = field;
  }
}

function validate(age) {
  if (typeof age !== "number" || Number.isNaN(age))
    throw new ValidationError("age", "age must be a number");
  if (age < 0 || age > 130)
    throw new RangeError("age out of range");
  return age;
}

try { validate("x"); }
catch (e) {
  if (e instanceof ValidationError) console.log(`Field ${e.field}: ${e.message}`);
  else if (e instanceof RangeError) console.log("Range:", e.message);
  else throw e;                        // not ours — re-throw
}
```

**Re-throwing what you cannot handle is the discipline that matters.** A
`catch` that swallows every error turns a crash into a silent wrong answer,
which is far worse.

### ⚠️ `finally` overrides `return`

```js
function f() {
  try    { return 1; }
  finally{ return 2; }      // returns 2 — the try's return is discarded
}
```

Never `return` from `finally`. It also silently discards a pending exception.

`try/catch` does **not** catch errors from asynchronous callbacks:

```js
try { setTimeout(() => { throw new Error("boom"); }, 0); }
catch { /* never runs — the callback fires long after try/catch has exited */ }
```

The `try` block finished before the callback ran. Put the `try` *inside* the
callback, or use `async/await` where `try/catch` works normally.

---

## Practice problems

### Problem 1

Predict the output and justify each line.

```js
console.log(1 + "2");
console.log("3" - 1);
console.log([] + {});
console.log(typeof NaN);
console.log(0.1 + 0.2 === 0.3);
console.log([1,2,3] === [1,2,3]);
```

**Solution.**

| Expression | Result | Why |
|---|---|---|
| `1 + "2"` | `"12"` | `+` prefers string concatenation if either side is a string |
| `"3" - 1` | `2` | `-` has no string meaning, so both convert to numbers |
| `[] + {}` | `"[object Object]"` | `[]` → `""`, `{}` → `"[object Object]"` |
| `typeof NaN` | `"number"` | NaN is a numeric value meaning "not representable" |
| `0.1+0.2===0.3` | `false` | Binary floating point |
| `[1,2,3]===[1,2,3]` | `false` | Objects compare by **reference**, not contents |

### Problem 2

Write a function `wordFrequency(text)` returning an object of word counts,
case-insensitive and ignoring punctuation. Then print the top three.

**Solution.**

```js
function wordFrequency(text) {
  const words = text.toLowerCase().match(/\b[a-z']+\b/g) || [];
  const freq  = {};
  for (const w of words) freq[w] = (freq[w] || 0) + 1;
  return freq;
}

const f = wordFrequency("The data is the data we need, and the data is here.");
// { the: 3, data: 3, is: 2, we: 1, need: 1, and: 1, here: 1 }

const top3 = Object.entries(f)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 3);
// [["the",3], ["data",3], ["is",2]]
```

`(freq[w] || 0) + 1` handles the first occurrence, where `freq[w]` is
`undefined` and `undefined + 1` would be `NaN`.

### Problem 3

`safeDivide(a, b)` must return the quotient, throw a `TypeError` if either
argument is not a finite number, and throw a `RangeError` on division by zero.
Write it and a test harness.

**Solution.**

```js
function safeDivide(a, b) {
  if (!Number.isFinite(a) || !Number.isFinite(b))
    throw new TypeError("both arguments must be finite numbers");
  if (b === 0) throw new RangeError("division by zero");
  return a / b;
}

for (const [a, b] of [[10, 2], [1, 0], ["x", 2], [1, Infinity]]) {
  try { console.log(`${a}/${b} =`, safeDivide(a, b)); }
  catch (e) { console.log(`${a}/${b} → ${e.name}: ${e.message}`); }
}
// 10/2 = 5
// 1/0 → RangeError: division by zero
// x/2 → TypeError: both arguments must be finite numbers
// 1/Infinity → TypeError: both arguments must be finite numbers
```

`Number.isFinite` rejects `NaN`, `Infinity` **and** non-numbers in one test —
unlike the global `isFinite()`, which coerces `"5"` to 5 and accepts it.

---

## Exam questions from this unit

**Two marks**

1. What is DHTML?
2. Distinguish JavaScript from Java.
3. Distinguish `==` from `===`.
4. Distinguish `let`, `const` and `var`.
5. What is a closure?
6. Distinguish `for…in` from `for…of`.
7. Why does `[10,9,100].sort()` give the wrong order?
8. Distinguish `null` from `undefined`.

**Five marks**

1. Explain JavaScript data types and `typeof`, including its anomalies.
2. Explain the string manipulation methods with examples.
3. Explain array methods, distinguishing mutating from non-mutating.
4. Explain exception handling with `try`, `catch`, `finally` and `throw`.
5. Explain regular expressions and write patterns for email and phone.
6. Explain `this` and how arrow functions differ.

**Ten marks**

1. Explain JavaScript functions completely — declarations, expressions, arrows,
   parameters, closures and hoisting — with examples.
2. Explain objects, classes, inheritance and prototypes with a worked example.
3. Write a program using arrays and objects to compute student statistics, and
   explain every method used.

## Mistakes that cost marks

- Calling JavaScript a version of Java
- Using `==` and being surprised by the coercion
- `sort()` on numbers with no comparator
- Forgetting that `sort` and `reverse` mutate the original
- Using `for…in` on an array
- Assuming `const` makes an object immutable
- Comparing floats with `===`
- `x === NaN` instead of `Number.isNaN(x)`
- Forgetting `.map(Number)` after `match()`
- Using `g` with `.test()` and getting alternating results
- Forgetting `super()` in a derived class constructor
- `return` inside `finally`
- Wrapping `setTimeout` in `try/catch` and expecting it to catch
- Treating client-side validation as security
