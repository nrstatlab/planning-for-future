# Unit 2 — Basic Organization and Networking Fundamentals

**Syllabus topics:** Computer organization — functional components,
input/output devices, storage types, memory hierarchy. Types of computers —
micro, mini, mainframe, and supercomputers. Networking fundamentals —
definition, need for networks, types (LAN, WAN, MAN), topology (star, ring,
bus). Internet basics — IP address, domain name, web browser, email, WWW.

---

## 2.1 Input and output devices

| Input devices | Output devices |
|---|---|
| Keyboard, mouse, trackball | Monitor (LCD, LED, OLED) |
| Scanner, barcode reader, QR reader | Printer (laser, inkjet, dot-matrix) |
| Microphone, webcam | Speakers, headphones |
| Joystick, light pen, graphics tablet | Plotter |
| Touch screen *(also output)* | Projector |
| OMR, OCR, MICR readers | Braille display |
| Biometric scanners | |

**OMR** (Optical Mark Recognition) reads pencil marks — how your answer sheets
are graded. **OCR** (Optical Character Recognition) reads printed text. **MICR**
(Magnetic Ink Character Recognition) reads the numbers along the bottom of a
cheque.

A **touch screen is both an input and an output device**. So is a network
interface card, and a modem. Exams like this question.

## 2.2 Memory and storage

### The memory hierarchy

```
              ▲  faster, smaller, more expensive per byte
              │
     ┌────────────────────┐
     │     Registers      │   < 1 KB      ~1 ns
     ├────────────────────┤
     │   Cache (L1/L2/L3) │   KB–MB       ~10 ns
     ├────────────────────┤
     │   Main memory RAM  │   GB          ~100 ns
     ├────────────────────┤
     │  Secondary: SSD    │   GB–TB       ~100 µs
     ├────────────────────┤
     │  Secondary: HDD    │   TB          ~10 ms
     ├────────────────────┤
     │  Tertiary: tape,   │   TB–PB       seconds
     │  optical, cloud    │
     └────────────────────┘
              │
              ▼  slower, larger, cheaper per byte
```

**The hierarchy exists because of a trade-off.** Fast memory is expensive, so
you can afford only a little; cheap memory is slow, so you cannot work directly
from it. The compromise keeps frequently used data in the fast levels — which
works because programs exhibit **locality of reference**: they tend to reuse the
same data and instructions repeatedly.

### Primary vs secondary memory

| | Primary | Secondary |
|---|---|---|
| Also called | Main memory | Auxiliary / backing store |
| Volatile | RAM yes, ROM no | **No** |
| Speed | Fast | Slow |
| Cost per byte | High | Low |
| CPU access | **Direct** | Only via primary memory |
| Examples | RAM, ROM, cache | HDD, SSD, DVD, tape |

### RAM vs ROM

| | RAM | ROM |
|---|---|---|
| Full name | Random Access Memory | Read Only Memory |
| Volatile | **Yes** — contents lost on power-off | **No** |
| Writable | Yes | No (or with difficulty) |
| Holds | Programs and data in current use | Firmware, BIOS, bootstrap |
| Types | SRAM, DRAM | PROM, EPROM, EEPROM, Flash |

**SRAM vs DRAM:** SRAM uses flip-flops, is fast and expensive, and is used for
cache. DRAM uses capacitors that leak charge and must be **refreshed**
thousands of times a second — slower and cheaper, and used for main memory.

**ROM variants:**
- **PROM** — programmable once
- **EPROM** — erasable with ultraviolet light
- **EEPROM** — erasable electrically; Flash memory is a form of this

### Units of storage

| Unit | Size |
|---|---|
| 1 **nibble** | 4 bits |
| 1 **byte** | 8 bits |
| 1 **KB** | 1024 bytes (2¹⁰) |
| 1 **MB** | 1024 KB (2²⁰) |
| 1 **GB** | 1024 MB (2³⁰) |
| 1 **TB** | 1024 GB (2⁴⁰) |
| 1 **PB** | 1024 TB (2⁵⁰) |

Storage manufacturers use powers of 10 (1 GB = 1,000,000,000 bytes), which is
why a "500 GB" drive shows as about 465 GB in the operating system. The
unambiguous binary units are **KiB, MiB, GiB**.

## 2.3 Types of computers

| Type | Size | Users | Speed | Use | Examples |
|---|---|---|---|---|---|
| **Microcomputer** | Desk | 1 | Lowest | Personal work | PC, laptop, tablet, phone |
| **Minicomputer** | Cabinet | 10s–100s | Medium | Departmental | PDP-11, VAX |
| **Mainframe** | Room | 1000s | High | Banking, airlines, census | IBM z-series |
| **Supercomputer** | Building | Few, large jobs | Highest | Weather, simulation, research | PARAM, Cray, Fugaku |

**India's supercomputers** are worth naming: the **PARAM** series, begun by
C-DAC in 1991 under Dr Vijay Bhatkar, and **PARAM Siddhi-AI**, currently the
fastest in the country.

**Mainframe vs supercomputer** is a standard question. A mainframe handles an
enormous number of **transactions** simultaneously — reliability and throughput
matter most. A supercomputer performs an enormous number of **calculations** on
one problem — raw floating-point speed matters most. A bank needs a mainframe;
a weather forecast needs a supercomputer.

## 2.4 Networking fundamentals

### What a network is, and why

A **computer network** is two or more computers connected to share resources
and communicate.

**Why networks exist:**

1. **Resource sharing** — one printer serving thirty desks
2. **Data sharing** — a shared file store
3. **Communication** — email, messaging, video calls
4. **Reliability** — data replicated across machines
5. **Cost saving** — shared hardware and licences
6. **Scalability** — add machines without redesigning
7. **Centralised administration** — manage many machines from one place

### Types by geographical area

| Type | Full name | Range | Speed | Ownership | Example |
|---|---|---|---|---|---|
| **PAN** | Personal Area Network | ~10 m | Low | Individual | Bluetooth earphones |
| **LAN** | Local Area Network | Building/campus | **High** | Private | College lab |
| **MAN** | Metropolitan Area Network | A city (~50 km) | Medium | Private or public | City cable network |
| **WAN** | Wide Area Network | Country/world | Lower | Usually public | **The Internet** |

**The Internet is the largest WAN.** LANs are fast and privately owned; WANs are
slower per link and usually rely on leased telecommunications infrastructure.

### Network topologies

**Topology** is the arrangement of the connections.

| Topology | Structure | Advantages | Disadvantages |
|---|---|---|---|
| **Bus** | All nodes on one backbone cable | Cheap, simple, little cable | **One cable break kills the whole network**; collisions; hard to fault-find |
| **Star** | All nodes to a central hub/switch | Easy to add nodes; one node failing does not affect others; simple to diagnose | **The hub is a single point of failure**; more cable |
| **Ring** | Each node to the next, forming a loop | No collisions; equal access | One break can stop everything; adding a node disrupts the ring |
| **Mesh** | Every node to every other | Highly reliable; multiple paths | Very expensive; n(n−1)/2 cables |
| **Tree** | Hierarchy of star networks | Scalable; easy to extend | Depends on the root; complex cabling |
| **Hybrid** | Combination | Flexible | Complex and costly |

The syllabus names **star, ring and bus** specifically. Know all three
thoroughly, and be able to draw them.

```
      BUS                      STAR                      RING

 ─┬────┬────┬────┬─          ┌───┐               ┌───┐    ┌───┐
  │    │    │    │        ┌──┤ A │              ┌┤ A ├────┤ B ├┐
 ┌┴┐  ┌┴┐  ┌┴┐  ┌┴┐       │  └───┘              │└───┘    └───┘│
 │A│  │B│  │C│  │D│    ┌──┴──┐  ┌───┐           │              │
 └─┘  └─┘  └─┘  └─┘    │ HUB ├──┤ B │           │┌───┐    ┌───┐│
                       └──┬──┘  └───┘           └┤ D ├────┤ C ├┘
                          │  ┌───┐               └───┘    └───┘
                          └──┤ C │
                             └───┘
```

**Star is the dominant topology today** — every Ethernet network with a switch
is physically a star.

**The mesh cable count** is a common numerical question: a full mesh of n nodes
needs **n(n−1)/2** links. For 6 nodes that is 15.

### Network devices

| Device | Function | OSI layer |
|---|---|---|
| **Repeater** | Amplifies a weakening signal | Physical (1) |
| **Hub** | Broadcasts to every port — "dumb" | Physical (1) |
| **Switch** | Forwards only to the correct port using MAC addresses | Data link (2) |
| **Bridge** | Connects two LAN segments | Data link (2) |
| **Router** | Routes between different networks using IP addresses | Network (3) |
| **Gateway** | Connects networks using different protocols | All |
| **Modem** | Modulates/demodulates for analogue lines | Physical (1) |

**Hub vs switch** is examined constantly: a hub sends every frame to every port,
wasting bandwidth and creating collisions; a switch learns which device is on
which port and sends the frame only there.

### Transmission modes

| Mode | Direction | Example |
|---|---|---|
| **Simplex** | One way only | Keyboard to computer; television broadcast |
| **Half duplex** | Both ways, one at a time | Walkie-talkie |
| **Full duplex** | Both ways simultaneously | Telephone |

## 2.5 Internet basics

### What the Internet is

A global **network of networks** using the **TCP/IP** protocol suite. It began
as **ARPANET** in 1969 (US Department of Defense) and reached India in 1995.

**The Internet is not the Web.** The Internet is the infrastructure; the World
Wide Web is one service running on it, alongside email, FTP and many others.
That distinction is a reliable two-mark question.

### IP address

A unique numeric identifier for a device on a network.

| | IPv4 | IPv6 |
|---|---|---|
| Size | 32 bits | 128 bits |
| Format | Four decimal octets: `192.168.1.1` | Eight hex groups: `2001:0db8::7334` |
| Total addresses | ~4.3 billion | ~3.4 × 10³⁸ |
| Notation | Dotted decimal | Colon hexadecimal |

**IPv6 exists because IPv4 ran out.** 4.3 billion addresses seemed limitless in
1981 and are not remotely enough today.

**IPv4 classes:**

| Class | First octet | Use |
|---|---|---|
| A | 1–126 | Very large networks |
| B | 128–191 | Medium networks |
| C | 192–223 | Small networks |
| D | 224–239 | Multicast |
| E | 240–255 | Experimental |

`127.0.0.1` is **localhost** — the machine itself. Private ranges
(`10.x.x.x`, `172.16–31.x.x`, `192.168.x.x`) are not routable on the public
Internet, which is why your home router hands out `192.168.1.x`.

### Domain names and DNS

Humans remember `google.com`; machines need `142.250.183.14`. The **Domain Name
System** translates between them — effectively the Internet's phone book.

```
www  .  example  .  com
 │        │          │
 │        │          └─ Top-level domain (TLD)
 │        └──────────── Second-level domain
 └───────────────────── Subdomain / host
```

**Top-level domains:** `.com` (commercial), `.org` (organisation), `.edu`
(education), `.gov` (government), `.net` (network), plus country codes such as
`.in`, `.uk`, `.us`. India also has `.ac.in` for academic institutions and
`.gov.in` for government.

### URL structure

```
https://www.example.com:443/folder/page.html?id=42#section
  │           │          │        │            │      │
protocol   domain      port     path        query  fragment
```

### World Wide Web

Invented by **Tim Berners-Lee at CERN in 1989**. Its three foundations:

1. **HTML** — the markup language for pages
2. **HTTP** — the protocol for transferring them
3. **URL** — the addressing scheme

**HTTP vs HTTPS:** HTTPS adds TLS encryption. Anything involving a password or
payment must use HTTPS; the padlock in the address bar indicates it.

### Web browser

Software that requests, interprets and displays web pages: Chrome, Firefox,
Safari, Edge. Its core components are the rendering engine (which draws HTML and
CSS), the JavaScript engine, and the network layer.

### Email

| Protocol | Purpose | Port |
|---|---|---|
| **SMTP** | **Sending** mail | 25, 587 |
| **POP3** | Downloading mail (usually deleting from the server) | 110, 995 |
| **IMAP** | Reading mail while **leaving it on the server** | 143, 993 |

**POP3 vs IMAP:** POP3 downloads and typically deletes, so mail lives on one
device. IMAP synchronises, so the same mailbox appears identically on your
phone and laptop. IMAP is what almost everyone uses now.

**Email address structure:** `username@domain.com` — the local part, `@`, and
the domain.

**Cc vs Bcc:** every recipient sees the Cc list; nobody sees the Bcc list. Using
Cc where Bcc was needed exposes everyone's address to everyone else — a real
privacy failure, and a good exam point.

### Common protocols

| Protocol | Purpose |
|---|---|
| **TCP** | Reliable, connection-oriented delivery |
| **UDP** | Fast, connectionless, no delivery guarantee |
| **IP** | Addressing and routing |
| **HTTP/HTTPS** | Web pages |
| **FTP** | File transfer |
| **SMTP/POP3/IMAP** | Email |
| **DNS** | Name resolution |
| **DHCP** | Automatic IP address assignment |

**TCP vs UDP:** TCP guarantees delivery and order, at the cost of speed — used
for web pages, email and file transfer. UDP does neither, and is used where
speed matters more than perfection: live video, voice calls, online games. A
dropped frame in a video call is better than a stalled one.

---

## Exam questions from this unit

**Two marks**

1. Differentiate RAM and ROM.
2. What is the memory hierarchy, and why does it exist?
3. Differentiate LAN and WAN.
4. Distinguish a hub from a switch.
5. What is the difference between the Internet and the World Wide Web?
6. Differentiate POP3 and IMAP.

**Five marks**

1. Explain the memory hierarchy with a diagram.
2. Explain the network topologies with diagrams, advantages and disadvantages.
3. Explain the types of computers with examples.
4. Explain IP addressing, including IPv4 classes and the need for IPv6.
5. Explain the email protocols.

**Ten marks**

1. Explain computer organization — functional components, I/O devices, storage
   types and the memory hierarchy.
2. Explain networking fundamentals — the need for networks, types, topologies
   and devices — with diagrams.

## Mistakes that cost marks

- Saying RAM is non-volatile — it is volatile; ROM is not
- Placing cache below main memory in the hierarchy
- Confusing a hub (broadcasts to all) with a switch (targets one port)
- Saying the Internet and the WWW are the same thing
- Confusing SMTP (sending) with POP3/IMAP (receiving)
- Drawing a star topology without the central hub
- Forgetting that 1 KB is 1024 bytes, not 1000
