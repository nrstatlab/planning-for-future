# -*- coding: utf-8 -*-
"""UGC NET Paper I, Unit 8: fifty exam-standard model questions."""
from . import AR, Q, ar, match, st

TITLE = "Information and Communication Technology"
BLURB = ("Abbreviations and terminology, bits and bytes, the internet and the web, intranet and extranet, "
         "e-mail, audio and video conferencing, digital initiatives in higher education, and ICT in "
         "governance.")

QUESTIONS = [
 Q("Match the abbreviation in List I with what it does in List II."
   + match(["DNS", "SMTP", "FTP", "HTTPS"],
           ["Transfers files between computers", "Carries web pages over an encrypted connection",
            "Translates domain names into IP addresses", "Sends e-mail"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)",
    "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "B",
   "The Domain Name System turns a name such as ugc.gov.in into an IP address; the Simple Mail Transfer "
   "Protocol sends mail; the File Transfer Protocol moves files; HTTPS is HTTP made secure by encryption.", "terms"),

 Q("The number of bits in 2 KB, taking 1 KB as 1,024 bytes, is:",
   ["2,048", "8,192", "16,000", "16,384"], "D",
   r"$2\times1{,}024$ bytes $=2{,}048$ bytes, and each byte is 8 bits: $2{,}048\times8=16{,}384$ bits. "
   r"(2,048 is the number of bytes; 16,000 takes a kilobyte as 1,000 bytes.)", "terms"),

 Q("The decimal equivalent of the binary number 11010 is:",
   ["26", "22", "25", "52"], "A",
   r"The places of a binary number, from the right, are worth 1, 2, 4, 8, 16. So 11010 is "
   r"$1\times16+1\times8+0\times4+1\times2+0\times1=26$.", "terms"),

 Q("The binary equivalent of the decimal number 45 is:",
   ["101011", "110101", "101101", "100101"], "C",
   r"$45=32+8+4+1$, so the digits for $32,16,8,4,2,1$ are $1,0,1,1,0,1$: 101101. Check: "
   r"$32+0+8+4+0+1=45$.", "terms"),

 Q("Arrange the following units of storage in increasing order of size: (1) Gigabyte, (2) Kilobyte, "
   "(3) Terabyte, (4) Megabyte, (5) Byte.",
   ["5, 2, 1, 4, 3", "5, 2, 4, 1, 3", "2, 5, 4, 1, 3", "5, 4, 2, 1, 3"], "B",
   "Byte, kilobyte, megabyte, gigabyte, terabyte: each is 1,024 times the one before it in computing usage.", "terms"),

 Q("A file of 50 MB is downloaded over a connection whose speed is 100 Mbps. Ignoring overheads, the "
   "download takes about:",
   ["0.5 second", "2 seconds", "8 seconds", "4 seconds"], "D",
   r"Speeds are quoted in bits per second and file sizes in bytes. $100$ Mbps $=\dfrac{100}{8}=12.5$ MB per "
   r"second, so 50 MB takes $\dfrac{50}{12.5}=4$ seconds. Forgetting the factor 8 gives half a second.", "terms"),

 Q("Consider the statements:"
   + st("RAM is volatile: its contents are lost when the power is switched off.",
        "ROM holds its contents permanently.",
        "The CPU is the processor of the computer.",
        "A byte consists of ten bits.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and II only", "II, III and IV only", "I, II, III and IV"], "A",
   "A byte is 8 bits, so (IV) is false. RAM is working memory and is volatile; ROM is permanent; the Central "
   "Processing Unit carries out the instructions.", "terms"),

 Q("Match the type of network in List I with its usual extent in List II."
   + match(["LAN", "MAN", "WAN", "Wi-Fi"],
           ["A country or the world", "Wireless local networking", "A building or campus", "A city"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "C",
   "Local, Metropolitan and Wide Area Networks differ in the area they cover. Wi-Fi is a trade name for "
   "wireless local area networking under the IEEE 802.11 standards.", "terms"),

 Q("In cloud computing, a service that lets a user work with an application, such as e-mail or a word "
   "processor, through a browser without installing it is called:",
   ["Infrastructure as a Service", "Software as a Service", "Platform as a Service", "Internet of Things"], "B",
   "SaaS delivers ready software over the internet; PaaS gives developers a platform on which to build; "
   "IaaS rents out computing infrastructure such as servers and storage.", "terms"),

 Q("In the address https://www.ugc.gov.in/page.html, the parts &lsquo;https&rsquo;, "
   "&lsquo;www.ugc.gov.in&rsquo; and &lsquo;page.html&rsquo; are, respectively:",
   ["the domain name, the protocol and the file", "the file, the domain name and the protocol",
    "the protocol, the file and the domain name", "the protocol, the domain name and the file"], "D",
   "A URL (Uniform Resource Locator) names the protocol, then the domain name, which DNS turns into an IP "
   "address, and then the path of the file on that server.", "terms"),

 Q("Which of the following lists contains only file formats for images?",
   ["JPEG and GIF", "MP3 and JPEG", "PDF and MP4", "GIF and MP3"], "A",
   "JPEG and GIF are image formats. MP3 is an audio format, MP4 a video format and PDF a document format.", "terms"),

 Q("VoIP is a technology for:",
   ["sending e-mail", "storing files in the cloud", "making voice calls over the internet",
    "translating domain names"], "C",
   "Voice over Internet Protocol carries telephone calls as data over the internet instead of over the "
   "telephone network.", "terms"),

 Q("Consider the statements:"
   + st("The internet grew out of ARPANET, first connected in 1969.",
        "The World Wide Web was proposed by Tim Berners-Lee at CERN in 1989.",
        "The World Wide Web and the internet are the same thing.",
        "Public internet access in India began in 1995.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and IV only", "II, III and IV only", "I, II, III and IV"], "B",
   "The web is one service that runs on the internet, as e-mail and file transfer are others; the internet "
   "is the network of networks itself. So (III) is false. Public access in India began on 15 August 1995 "
   "through VSNL.", "internet"),

 Q("An e-mail that appears to come from a bank asks the receiver to &lsquo;verify the account&rsquo; by "
   "entering the password on a linked page. This is an example of:",
   ["spam", "a firewall", "ransomware", "phishing"], "D",
   "Phishing uses fake messages and look-alike sites to steal passwords and account details. Ransomware "
   "locks the victim's files and demands payment; spam is unwanted bulk mail.", "internet"),

 Q("Software that displays web pages, and a service that finds web pages matching given words, are "
   "respectively:",
   ["a web browser and a search engine", "a search engine and a web browser",
    "an operating system and a browser", "a server and a client"], "A",
   "Chrome, Firefox, Edge and Safari are browsers; Google and Bing are search engines. The search engine is "
   "itself a website, opened in a browser.", "internet"),

 Q("Which of the following is malicious software that encrypts the victim's files and demands payment for "
   "restoring them?",
   ["Worm", "Spyware", "Ransomware", "Adware"], "C",
   "Ransomware holds data to ransom. A worm spreads itself across networks; spyware secretly gathers "
   "information; adware shows unwanted advertisements.", "internet"),

 Q("Consider the following measures:"
   + st("Strong passwords", "Two-factor authentication", "Regular software updates",
        "Sharing a one-time password with a caller who claims to be from the bank")
   + "Which of them improve cyber security?",
   ["I and II only", "I, II and III only", "I, III and IV only", "I, II, III and IV"], "B",
   "A one-time password is the second factor that protects an account; giving it to anyone defeats the "
   "protection, and no bank asks for it. The first three are standard defences, along with firewalls and "
   "antivirus software.", "internet"),

 Q("The set of rules by which data are addressed, routed and delivered reliably across the internet is:",
   ["HTML", "HTTP", "FTP", "TCP/IP"], "D",
   "The Internet Protocol addresses and routes packets; the Transmission Control Protocol delivers them "
   "reliably and in order. HTML is the language in which web pages are written.", "internet"),

 Q(ar("A firewall protects a network.",
      "A firewall monitors the traffic entering and leaving a network and blocks what its rules do not allow."),
   AR, "A",
   "The firewall stands between a trusted network and the outside and filters traffic by rules. Both "
   "statements are true and (R) explains (A).", "internet"),

 Q("A university's library catalogue can be opened only on computers of the campus network. The catalogue "
   "is on the university's:",
   ["extranet", "internet", "intranet", "cloud"], "C",
   "An intranet uses the same protocols as the internet but is open only to members of one organisation.", "intranet"),

 Q("A university gives its affiliated colleges login accounts through which they upload examination marks "
   "to its server. This is an example of:",
   ["an intranet", "an extranet", "the public internet", "a peer-to-peer network"], "B",
   "An extranet is a private network opened, in a controlled way, to selected outside users such as "
   "suppliers or partner institutions.", "intranet"),

 Q("Match the network in List I with its users in List II."
   + match(["Internet", "Intranet", "Extranet"],
           ["Members of one organisation only", "The organisation and selected outsiders", "Anyone"]),
   ["(a)-(iii), (b)-(i), (c)-(ii)", "(a)-(i), (b)-(iii), (c)-(ii)", "(a)-(iii), (b)-(ii), (c)-(i)",
    "(a)-(ii), (b)-(i), (c)-(iii)"], "A",
   "The internet is public; an intranet is private to one organisation; an extranet extends a private "
   "network to chosen outside users.", "intranet"),

 Q("Which statement about an intranet is correct?",
   ["It cannot use web browsers", "It must be connected to the internet at all times",
    "It is open to the general public", "It uses TCP/IP and web protocols on a private network"], "D",
   "The technology of an intranet is the same as the internet's: TCP/IP, web servers and browsers. What "
   "differs is who is allowed in.", "intranet"),

 Q("A teacher writes one e-mail to 60 parents and does not want any parent to see the addresses of the "
   "others. The addresses should be entered in the field:",
   ["To", "CC", "BCC", "Subject"], "C",
   "Addresses in BCC (blind carbon copy) are hidden from all the other recipients. Everyone can see the "
   "addresses in To and CC.", "email"),

 Q("Which e-mail protocol keeps messages on the server and synchronised across a phone and a laptop?",
   ["SMTP", "IMAP", "POP3", "FTP"], "B",
   "IMAP leaves mail on the server and keeps every device in step. POP3 usually downloads mail to one device "
   "and removes it from the server. SMTP is used for sending.", "email"),

 Q("A message is sent with A in the To field, B in CC and C in BCC. If A chooses &lsquo;Reply all&rsquo;, "
   "the reply goes to:",
   ["the sender and B", "the sender only", "the sender, B and C", "B and C only"], "A",
   "Reply all answers the sender and everyone in To and CC. A cannot see that C received a blind copy, so C "
   "is not included.", "email"),

 Q("In the e-mail address registrar@university.ac.in, the part &lsquo;university.ac.in&rsquo; is the:",
   ["user name", "protocol", "password", "domain name"], "D",
   "An address has a user name, the @ sign and the domain name of the mail server.", "email"),

 Q("The first e-mail between computers on a network was sent in 1971, and the @ sign was chosen for "
   "addresses, by:",
   ["Tim Berners-Lee", "Vint Cerf", "Ray Tomlinson", "Bill Gates"], "C",
   "Ray Tomlinson sent the first network e-mail in 1971. Berners-Lee proposed the World Wide Web; Cerf is "
   "one of the designers of TCP/IP.", "email"),

 Q("Consider the statements about e-mail:"
   + st("An attachment is a file sent along with a message.", "Spam is unwanted bulk mail.",
        "Forward sends a received message on to a new recipient.",
        "Addresses placed in CC are hidden from the other recipients.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "II, III and IV only", "I, II, III and IV"], "B",
   "Addresses in CC are visible to all recipients; it is BCC that hides them. So (IV) is false.", "email"),

 Q("A lecture is streamed live to 500 registered teachers, who can send questions only through the chat box. "
   "This is best described as:",
   ["a webinar", "an audio conference", "a chat room", "an intranet"], "A",
   "A webinar is a seminar on the web: one or a few speakers to a large audience who listen and ask "
   "questions in writing. In a video meeting all participants can normally speak and be seen.", "conferencing"),

 Q("In video conferencing, the delay between a participant's speaking and being heard at the other end is "
   "called:",
   ["bandwidth", "resolution", "bit rate", "latency"], "D",
   "Latency is delay. Bandwidth is the amount of data the connection can carry per second; too little of it "
   "makes the picture break up.", "conferencing"),

 Q("Consider the following:"
   + st("A camera and a microphone", "Conferencing software or a browser", "Adequate bandwidth",
        "A printed copy of the agenda for each participant")
   + "Which of them are necessary for a video conference?",
   ["I and II only", "I, III and IV only", "I, II and III only", "I, II, III and IV"], "C",
   "Video conferencing needs devices to capture sound and picture, software to connect the participants and "
   "enough bandwidth. Printed papers are not a technical requirement.", "conferencing"),

 Q("An external examiner at another university takes part in a doctoral viva through a live two-way picture "
   "and sound link. The technology used is:",
   ["audio conferencing", "video conferencing", "e-mail", "a discussion forum"], "B",
   "Live two-way video and sound is video conferencing; it usually adds screen-sharing and chat. Audio "
   "conferencing carries voice only.", "conferencing"),

 Q("Match the initiative in List I with the institution that runs it in List II."
   + match(["National Digital Library of India", "NPTEL", "e-PG Pathshala", "Shodhganga"],
           ["The IITs and IISc", "INFLIBNET, as a repository of theses", "IIT Kharagpur",
            "UGC, through INFLIBNET, as postgraduate e-content"]),
   ["(a)-(iii), (b)-(i), (c)-(ii), (d)-(iv)", "(a)-(i), (b)-(iii), (c)-(iv), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)"], "D",
   "NDLI is run by IIT Kharagpur; NPTEL (the National Programme on Technology Enhanced Learning) by the IITs "
   "and IISc; e-PG Pathshala is the UGC's postgraduate e-content through INFLIBNET; Shodhganga is INFLIBNET's "
   "repository of theses.", "initiatives"),

 Q("The National Mission on Education through Information and Communication Technology (NMEICT), the "
   "umbrella for many digital platforms in higher education, was begun in:",
   ["2009", "2015", "2017", "2021"], "A",
   "NMEICT was begun in 2009. SWAYAM was launched in 2017, Digital India in 2015, and the Academic Bank of "
   "Credits in 2021.", "initiatives"),

 Q("A student who has lost her degree certificate obtains a verified digital copy that her university had "
   "deposited. The system that makes this possible is the:",
   ["National Digital Library of India", "Academic Bank of Credits",
    "National Academic Depository, through DigiLocker", "e-ShodhSindhu"], "C",
   "The National Academic Depository keeps degrees and mark sheets in digital form, deposited by "
   "institutions and available to students through DigiLocker.", "initiatives"),

 Q("Which platform provides a single search across millions of learning resources of many kinds and "
   "levels?",
   ["Shodhgangotri", "National Digital Library of India", "Virtual Labs", "Vidwan"], "B",
   "NDLI is a digital library with one search window over resources from many sources. Shodhgangotri holds "
   "research synopses, Virtual Labs offers online experiments, and Vidwan is a database of experts.", "initiatives"),

 Q("The Academic Bank of Credits:",
   ["lends money to students for fees", "is a consortium for e-journals",
    "is a group of educational television channels",
    "stores the credits a student earns so that they can be carried from one institution to another"], "D",
   "Introduced in 2021, it keeps a digital account of a student's credits, which makes multiple entry and "
   "exit and transfer between institutions possible.", "initiatives"),

 Q("Consider the statements:"
   + st("SWAYAM offers MOOCs from school level to postgraduate level.",
        "SWAYAM Prabha is a group of educational DTH television channels.",
        "Virtual Labs lets students perform laboratory experiments online.",
        "e-ShodhSindhu is a repository of doctoral theses.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and II only", "II, III and IV only", "I, II, III and IV"], "A",
   "e-ShodhSindhu is the consortium that gives institutions access to e-journals and databases; the "
   "repository of theses is Shodhganga. So (IV) is false.", "initiatives"),

 Q("A college with a small library wishes to give its students access to subscribed scholarly journals. "
   "The service meant for this purpose is:",
   ["Shodhganga", "SWAYAM Prabha", "e-ShodhSindhu", "DigiLocker"], "C",
   "e-ShodhSindhu, run by INFLIBNET, negotiates access to e-journals and databases for member institutions.", "initiatives"),

 Q("NPTEL, a joint initiative of the IITs and IISc, mainly offers:",
   ["school-level television lessons", "online courses in engineering and the sciences",
    "plagiarism-detection software", "digital copies of degree certificates"], "B",
   "The National Programme on Technology Enhanced Learning provides courses in engineering and science, and "
   "is one of the national coordinators of SWAYAM.", "initiatives"),

 Q("Arrange the following in chronological order: (1) Launch of Digital India, (2) National e-Governance "
   "Plan, (3) Launch of SWAYAM, (4) NMEICT, (5) Digital Personal Data Protection Act.",
   ["2, 4, 1, 3, 5", "4, 2, 1, 3, 5", "2, 4, 3, 1, 5", "2, 1, 4, 3, 5"], "A",
   "The National e-Governance Plan was approved in 2006; NMEICT began in 2009; Digital India was launched on "
   "1 July 2015; SWAYAM in 2017; the Digital Personal Data Protection Act was passed in 2023.", "initiatives"),

 Q("Match the model of e-governance in List I with the example in List II."
   + match(["G2C", "G2B", "G2G", "G2E"],
           ["Online submission of tenders by firms", "Pay slips and service records of government staff",
            "A citizen obtaining a birth certificate online", "Exchange of data between two departments"]),
   ["(a)-(iii), (b)-(i), (c)-(ii), (d)-(iv)", "(a)-(i), (b)-(iii), (c)-(iv), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)"], "D",
   "Government to Citizen, to Business, to Government and to Employee: the names say who is served.", "egovernance"),

 Q("Digital India was launched on:",
   ["15 August 1995", "1 July 2017", "1 July 2015", "26 January 2006"], "C",
   "Digital India was launched on 1 July 2015, aiming at digital infrastructure for every citizen, services "
   "on demand and digital literacy. 15 August 1995 is the date public internet access began in India.", "egovernance"),

 Q("A farmer applies at a village Common Service Centre for a copy of a land record and receives it the same "
   "day. This service is an example of:",
   ["G2B", "G2C", "G2G", "G2E"], "B",
   "A government service delivered to a citizen is G2C. Common Service Centres are the village-level access "
   "points for such online services.", "egovernance"),

 Q("Match the platform in List I with its purpose in List II."
   + match(["DigiLocker", "UMANG", "UPI", "Aadhaar"],
           ["Instant payments between bank accounts", "A unique digital identity",
            "Official documents kept in digital form", "A single mobile app for many government services"]),
   ["(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "A",
   "DigiLocker holds documents; UMANG (Unified Mobile Application for New-age Governance) gathers many "
   "services in one app; the Unified Payments Interface, from the National Payments Corporation of India, "
   "makes instant payments; Aadhaar is the identity.", "egovernance"),

 Q(ar("Online tendering reduces corruption in public procurement.",
      "When bids are submitted and opened on a public portal, there is less room for discretion and more "
      "transparency."),
   AR, "A",
   "Corruption thrives on discretion and secrecy; a portal on which every bid is recorded and opened removes "
   "both. Both statements are true and (R) is the reason.", "egovernance"),

 Q("Which of the following is a challenge, and not a benefit, of e-governance?",
   ["Services available at any hour", "Greater transparency", "Faster delivery", "The digital divide"], "D",
   "The digital divide is the gap between those who have access to devices, connectivity and digital skills "
   "and those who do not. Privacy, data protection and cyber security are the other main challenges.", "egovernance"),

 Q("The National e-Governance Plan (NeGP), which set up mission-mode projects for services such as passports "
   "and income tax, was approved in:",
   ["2000", "2012", "2006", "2015"], "C",
   "The NeGP was approved in 2006. Digital India (2015) later brought e-governance under a wider "
   "programme.", "egovernance"),

 Q("Consider the statements about e-governance:"
   + st("It uses ICT to deliver government services.", "It aims to make administration more transparent.",
        "It removes the need for any protection of personal data.",
        "Common Service Centres extend its reach to villages.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and IV only", "II, III and IV only", "I, II, III and IV"], "B",
   "E-governance handles large amounts of personal data, which makes its protection more necessary, not "
   "less; the Digital Personal Data Protection Act, 2023 addresses this. So (III) is false.", "egovernance"),
]
