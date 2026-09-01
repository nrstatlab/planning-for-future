# Unit 1 — Number Systems, Evolution, Block Diagram and Generations

**Syllabus topics:** Number systems — binary, decimal, octal,
hexadecimal; conversions between number systems. Evolution of computers —
history from early mechanical devices to modern-day systems. Block diagram of a
computer — components like input unit, output unit, memory, CPU (ALU + CU).
Generations of computers — first to fifth generation technologies,
characteristics, examples.

---

## 1.1 Number systems

### Why computers use binary

A transistor is either conducting or not. Two states — so the natural number
system for electronics has two digits, 0 and 1. Every number, letter, image and
instruction inside a computer is ultimately a pattern of these.

| System | Base | Digits used |
|---|:---:|---|
| **Binary** | 2 | 0, 1 |
| **Octal** | 8 | 0–7 |
| **Decimal** | 10 | 0–9 |
| **Hexadecimal** | 16 | 0–9, A(10), B(11), C(12), D(13), E(14), F(15) |

**Why octal and hex exist:** binary is unreadable for humans — `11111111` is
hard to check at a glance, `FF` is easy. One hex digit is exactly four bits and
one octal digit exactly three, so conversion is a matter of grouping, with no
arithmetic at all.

### Conversion: any base → decimal

Multiply each digit by its **positional weight** and add.

**Binary 1011 → decimal**

| Digit | 1 | 0 | 1 | 1 |
|---|---|---|---|---|
| Weight | 2³=8 | 2²=4 | 2¹=2 | 2⁰=1 |
| Product | 8 | 0 | 2 | 1 |

8 + 0 + 2 + 1 = **11**

**Hexadecimal 2AF → decimal**

- 2 × 16² = 2 × 256 = 512
- A(10) × 16¹ = 10 × 16 = 160
- F(15) × 16⁰ = 15 × 1 = 15
- Total = 512 + 160 + 15 = **687**

**Octal 745 → decimal**

7 × 64 + 4 × 8 + 5 × 1 = 448 + 32 + 5 = **485**

### Conversion: decimal → any base

**Divide repeatedly by the base and read the remainders bottom-up.**

**Decimal 45 → binary**

| Division | Quotient | Remainder |
|---|---:|---:|
| 45 ÷ 2 | 22 | **1** |
| 22 ÷ 2 | 11 | **0** |
| 11 ÷ 2 | 5 | **1** |
| 5 ÷ 2 | 2 | **1** |
| 2 ÷ 2 | 1 | **0** |
| 1 ÷ 2 | 0 | **1** |

Reading the remainders **upwards**: **101101**

*Check:* 32 + 8 + 4 + 1 = 45 ✓ — always verify by converting back.

**Decimal 255 → hexadecimal**

- 255 ÷ 16 = 15 remainder **15 (F)**
- 15 ÷ 16 = 0 remainder **15 (F)**

Reading upwards: **FF**

### Conversion: binary ↔ octal (group in 3s)

**Binary 110101 → octal**

Group from the right in threes: `110 | 101` → 6 | 5 → **65**

**Octal 47 → binary**

4 → `100`, 7 → `111` → **100111**

### Conversion: binary ↔ hexadecimal (group in 4s)

**Binary 11010110 → hexadecimal**

Group from the right in fours: `1101 | 0110` → 13(D) | 6 → **D6**

**Hexadecimal 3E → binary**

3 → `0011`, E → `1110` → **00111110**

**Group from the right, always.** `1101101` splits as `110 | 1101` → 6, D →
**6D**. Group it from the *left* instead and you get `1101 | 101` → D, 5 →
**D5**, which is 213 rather than 109. Padding the short leftmost group with
zeros — `0110 | 1101` — changes nothing about the answer; it is a tidiness
habit that makes the direction obvious at a glance, and that is its whole
value.

### Octal ↔ hexadecimal

There is no direct route. **Go via binary**: octal → binary → regroup in fours
→ hex.

Octal 725 → binary `111 010 101` → regroup as `0001 1101 0101` → **1D5**

### Handy reference table

| Decimal | Binary | Octal | Hex |
|---:|---|---:|---|
| 0 | 0000 | 0 | 0 |
| 1 | 0001 | 1 | 1 |
| 2 | 0010 | 2 | 2 |
| 3 | 0011 | 3 | 3 |
| 4 | 0100 | 4 | 4 |
| 5 | 0101 | 5 | 5 |
| 6 | 0110 | 6 | 6 |
| 7 | 0111 | 7 | 7 |
| 8 | 1000 | 10 | 8 |
| 9 | 1001 | 11 | 9 |
| 10 | 1010 | 12 | A |
| 11 | 1011 | 13 | B |
| 12 | 1100 | 14 | C |
| 13 | 1101 | 15 | D |
| 14 | 1110 | 16 | E |
| 15 | 1111 | 17 | F |

**Memorise the 0–15 row.** Every conversion becomes lookup rather than
arithmetic.

### Fractional conversions

For the part after the point, **multiply** by the base and read the integer
parts **downwards**.

**Decimal 0.625 → binary**

| Step | Result | Integer part |
|---|---|---|
| 0.625 × 2 | 1.25 | **1** |
| 0.25 × 2 | 0.5 | **0** |
| 0.5 × 2 | 1.0 | **1** |

Reading **downwards**: **0.101**

*Check:* ½ + 0 + ⅛ = 0.625 ✓

**Note the direction reverses.** Integer conversions read remainders *up*;
fractional conversions read integer parts *down*. Getting this backwards is a
routine error.

Some fractions never terminate in binary — 0.1 decimal is infinite in binary,
which is exactly why `0.1 + 0.2 != 0.3` in Python and in every other language.

### Binary arithmetic

**Addition rules:** 0+0=0 · 0+1=1 · 1+0=1 · **1+1=10** (0 carry 1) ·
**1+1+1=11** (1 carry 1)

```
   1011   (11)
 + 1101   (13)
 ------
  11000   (24)  ✓
```

**Subtraction rules:** 0−0=0 · 1−0=1 · 1−1=0 · **0−1=1 with a borrow**

### Representing negative numbers

| Method | −5 in 8 bits |
|---|---|
| **Sign–magnitude** | `10000101` — leftmost bit is the sign |
| **1's complement** | `11111010` — flip every bit of +5 |
| **2's complement** | `11111011` — 1's complement, then add 1 |

**2's complement is what real computers use**, because addition and subtraction
then use the same circuit, and there is only one representation of zero
(sign–magnitude and 1's complement both have +0 and −0).

**Finding the 2's complement of 5 (`00000101`):**
1. Flip every bit → `11111010`
2. Add 1 → `11111011`

*Check:* 5 + (−5) should be 0. `00000101 + 11111011 = 100000000`; the ninth bit
overflows out of 8 bits, leaving `00000000` ✓

### Codes

| Code | Bits | Represents |
|---|---|---|
| **BCD** (Binary Coded Decimal) | 4 per digit | Each decimal digit separately |
| **ASCII** | 7 (or 8 extended) | 128 characters |
| **EBCDIC** | 8 | IBM mainframe character set |
| **Unicode** | 8–32 | Every writing system in the world |

**ASCII values worth knowing:** `A` = 65, `a` = 97, `0` = 48, space = 32.

The 32 difference between `A` and `a` is a single bit, which is why case
conversion in C can be done with `ch + 32` or a bitwise OR.

## 1.2 Evolution of computers

| Device | Year | Inventor | Significance |
|---|---|---|---|
| **Abacus** | ~3000 BC | China | The first counting device |
| **Napier's Bones** | 1617 | John Napier | Multiplication aid |
| **Slide Rule** | 1622 | William Oughtred | Logarithmic calculation |
| **Pascaline** | 1642 | Blaise Pascal | First mechanical adding machine |
| **Stepped Reckoner** | 1673 | Leibniz | Added multiplication and division |
| **Jacquard Loom** | 1801 | Joseph Jacquard | **Punched cards** — stored instructions |
| **Difference Engine** | 1822 | Charles Babbage | Automatic calculation of tables |
| **Analytical Engine** | 1837 | Charles Babbage | **The first general-purpose design** |
| **First program** | 1843 | **Ada Lovelace** | The first computer programmer |
| **Hollerith Tabulator** | 1890 | Herman Hollerith | US census; his company became IBM |
| **Turing Machine** | 1936 | Alan Turing | The theoretical model of computation |
| **ABC** | 1942 | Atanasoff & Berry | First electronic digital computer |
| **Colossus** | 1943 | Tommy Flowers | Codebreaking at Bletchley Park |
| **ENIAC** | 1946 | Eckert & Mauchly | First general-purpose electronic computer |
| **EDVAC / EDSAC** | 1949 | von Neumann / Wilkes | **Stored-program** concept |
| **UNIVAC I** | 1951 | Eckert & Mauchly | First commercial computer |

**Charles Babbage is the "Father of the Computer"** for the Analytical Engine —
which was never built in his lifetime but contained every logical element of a
modern machine: a store (memory), a mill (processor), input and output.

**Ada Lovelace** wrote an algorithm for it, making her the first programmer.
She also observed that such a machine could manipulate symbols in general, not
only numbers — an insight a century ahead of its time.

### The von Neumann architecture

Proposed by **John von Neumann** in 1945. Its central idea is the
**stored-program concept**: instructions and data live in the **same memory**.

Before this, reprogramming ENIAC meant physically rewiring it — a job that took
days. Storing the program as data made a computer general-purpose in the modern
sense.

Almost every computer today is a von Neumann machine. Its known weakness is the
**von Neumann bottleneck** — instructions and data share one path to memory, so
the CPU waits. The Harvard architecture, which separates them, is used in some
embedded processors.

## 1.3 Block diagram of a computer

```
        ┌───────────────────────────────────────────────┐
        │                    CPU                        │
        │   ┌───────────────┐   ┌───────────────────┐   │
  INPUT─┼──▶│ Control Unit  │   │ Arithmetic Logic  │───┼──▶ OUTPUT
  UNIT  │   │     (CU)      │◀─▶│    Unit (ALU)     │   │    UNIT
        │   └───────┬───────┘   └─────────┬─────────┘   │
        │           │      ┌──────────┐   │             │
        │           └─────▶│ Registers│◀──┘             │
        │                  └──────────┘                 │
        └───────────────────────┬───────────────────────┘
                                │
                    ┌───────────▼────────────┐
                    │     MEMORY UNIT        │
                    │  Primary + Secondary   │
                    └────────────────────────┘

      ────▶  data flow        ◀──▶  control signals
```

| Unit | Function |
|---|---|
| **Input unit** | Accepts data and converts it to machine form |
| **Memory unit** | Stores data, instructions and intermediate results |
| **ALU** | Performs arithmetic (+, −, ×, ÷) and logical (AND, OR, NOT, comparison) operations |
| **Control unit** | Fetches, decodes and coordinates execution; directs the others |
| **Output unit** | Converts results to human-readable form |

**CPU = ALU + CU + Registers.** The CU is often called the "nerve centre" — it
processes no data itself, but tells every other unit what to do and when.

### Registers

Small, extremely fast storage inside the CPU:

| Register | Holds |
|---|---|
| **PC** — Program Counter | Address of the next instruction |
| **IR** — Instruction Register | The instruction currently being executed |
| **MAR** — Memory Address Register | The address being accessed |
| **MDR/MBR** — Memory Data Register | The data being transferred |
| **AC** — Accumulator | Intermediate arithmetic results |

### The machine cycle

**Fetch → Decode → Execute → Store**, repeated billions of times per second.

## 1.4 Generations of computers

| Gen | Years | Technology | Speed | Language | Examples |
|:---:|---|---|---|---|---|
| **1st** | 1940–56 | **Vacuum tubes** | milliseconds | Machine language | ENIAC, UNIVAC, EDVAC |
| **2nd** | 1956–63 | **Transistors** | microseconds | Assembly, FORTRAN, COBOL | IBM 1401, IBM 7094 |
| **3rd** | 1964–71 | **Integrated Circuits (SSI/MSI)** | nanoseconds | C, PASCAL, BASIC | IBM System/360, PDP-8 |
| **4th** | 1971–present | **VLSI / Microprocessors** | picoseconds | C++, Java, Python | IBM PC, Apple Macintosh |
| **5th** | Present onward | **ULSI, AI, parallel processing** | — | Prolog, LISP, AI systems | Modern AI systems, quantum research |

### Characteristics by generation

**First (vacuum tubes)** — enormous, consumed huge power, generated great heat,
very unreliable (tubes burned out constantly), used punched cards, magnetic drum
memory. ENIAC filled a room and weighed 30 tonnes.

**Second (transistors)** — the transistor, invented at Bell Labs in 1947,
replaced the vacuum tube: smaller, cheaper, far more reliable, much less heat.
Magnetic core memory. Assembly and the first high-level languages appeared.

**Third (integrated circuits)** — many transistors on a single silicon chip.
Keyboards and monitors replaced punched cards. **Operating systems** appeared,
enabling multiprogramming and time-sharing.

**Fourth (microprocessors)** — VLSI put an entire CPU on one chip. The Intel
4004 (1971) was the first. This generation brought the personal computer, the
GUI, networks and the Internet.

**Fifth (AI)** — parallel processing, ULSI, natural language processing,
machine learning, quantum computing. Defined by capability rather than by
component technology, which is why its boundary is fuzzy.

**The trend across all five generations:** smaller, faster, cheaper, more
reliable, and using less power. That single sentence answers "compare the
generations" questions.

---

## 📝 Worked practice

### Problem 1 — Convert (1101101)₂ to decimal, octal and hexadecimal

**Decimal:** 64 + 32 + 0 + 8 + 4 + 0 + 1 = **109**

**Octal:** group in threes from the right: `001 | 101 | 101` → 1, 5, 5 →
**(155)₈**

**Hexadecimal:** group in fours from the right: `0110 | 1101` → 6, D →
**(6D)₁₆**

*Check:* 6 × 16 + 13 = 96 + 13 = 109 ✓

### Problem 2 — Convert (378)₁₀ to binary and hexadecimal

**Binary** — divide by 2:

378→189 r**0**, 189→94 r**1**, 94→47 r**0**, 47→23 r**1**, 23→11 r**1**,
11→5 r**1**, 5→2 r**1**, 2→1 r**0**, 1→0 r**1**

Reading upwards: **(101111010)₂**

**Hexadecimal** — group the binary in fours: `0001 | 0111 | 1010` → 1, 7, A →
**(17A)₁₆**

*Check:* 1 × 256 + 7 × 16 + 10 = 256 + 112 + 10 = 378 ✓

### Problem 3 — Add (10110)₂ and (1101)₂, and verify in decimal

```
   10110      (22)
 + 01101      (13)
 -------
  100011      (35)
```

Working right to left: 0+1=1 · 1+0=1 · 1+1=0 carry 1 · 0+1+1=0 carry 1 ·
1+0+1=0 carry 1 · carry 1

*Check:* 22 + 13 = 35, and 100011 = 32 + 2 + 1 = 35 ✓

### Problem 4 — Find the 2's complement of (00101100)₂ and verify

The number is 32 + 8 + 4 = **44**, so we expect −44.

1. **1's complement** — flip every bit: `11010011`
2. **Add 1**: `11010011 + 1 = ` **`11010100`**

*Check:* add it to the original. `00101100 + 11010100 = 100000000`. The ninth
bit overflows out of 8 bits, leaving `00000000` = 0 ✓

---

## Exam questions from this unit

**Two marks**

1. Why do computers use the binary system?
2. Convert (1010)₂ to decimal.
3. What is the 2's complement, and why is it preferred?
4. Who is the Father of the Computer, and why?
5. Expand ALU and CU.

**Five marks**

1. Convert a given number between all four bases, showing every step.
2. Explain the stored-program concept and the von Neumann architecture.
3. Explain the block diagram of a computer with a diagram.
4. Explain binary addition and subtraction with examples.

**Ten marks**

1. Explain the generations of computers with technology, characteristics,
   languages and examples for each.
2. Explain number systems and all the conversions between them, with examples.

## Mistakes that cost marks

- Reading remainders downwards instead of upwards (integer conversions)
- Reading fractional multiplications upwards instead of downwards
- Grouping binary from the left instead of the **right**
- Forgetting to pad the leftmost group with zeros
- Forgetting that A = 10 and F = 15 in hexadecimal
- Trying to convert octal to hex directly instead of going via binary
- Confusing the ALU (does the work) with the CU (directs the work)
- Not verifying by converting back — it takes ten seconds and catches most
  errors
