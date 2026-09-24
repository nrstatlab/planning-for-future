# -*- coding: utf-8 -*-
"""The APPSC syllabus, split into gradeable lines and pointed at the notes.

Two notifications, both dated 15/09/2026, and one syllabus body between them:
the Assistant Director splits ten subject items across Paper-2 and Paper-3 at
P.G. standard; the Assistant Statistical Officer takes the same ten items, in
the same words, as a single Paper-II at degree standard.  So SUBJECT below is
written once and both posts' pages are built from it.

Each row is (syllabus line, destination, grade), the destination being None,
one html path, or a tuple when the line spans two pages.  Paths are relative
to statistics-papers/appsc/.
"""
S = "../../statistics-major/"
D = "../../data-science-major/"
X = "../../exam-subjects/"
ISS = "../iss/"
EC = X + "economics/"
FA = X + "financial-accounting/"


def bsc(folder, unit):
    return f"{S}{folder}/unit{unit}_{folder}.html"


XL = S + "statistical data analysis using ms excel/"
CF = D + "computer-fundamentals/"

# --------------------------------------------------------------- the documents
DOCS = {
    "AD": {
        "post": "Assistant Director",
        "service": "A.P. Economics and Statistical Service",
        "notice": "Brief Notification No.&nbsp;09/2026, dated 15/09/2026",
        "scheme_src": ("Annexure VII of G.O. Ms. No.201 Finance (HR-I, Plg &amp; Policy) "
                       "Dept., Dt.21/12/2017"),
        "standard": "Papers 2 and 3 at P.G. standard; Paper 1 at degree standard",
        "papers": [("PAPER-1", "General Studies and Mental Ability (Degree standard)", 150, 150, 150),
                   ("PAPER-2", "Paper-2 (P. G. Standard)", 150, 150, 150),
                   ("PAPER-3", "Paper-3 (P. G. Standard)", 150, 150, 150)],
        "total": 450,
        "eligibility": ("Must possess Post Graduate Degree in one of the Subjects of "
                        "Mathematics, Pure Mathematics, Statistics, Economics, Applied "
                        "Economics, Applied Statistics, Applied Mathematics, Econometrics "
                        "or Computer Science from a recognized University or Institution "
                        "recognized by the University Grants Commission or any other "
                        "recognized equivalent qualification."),
        "slug": "assistant-director",
    },
    "ASO": {
        "post": "Assistant Statistical Officer",
        "service": "A.P. Economics &amp; Statistical Subordinate Service",
        "notice": "Brief Notification No.&nbsp;20/2026, dated 15/09/2026",
        "scheme_src": ("Annexure-V of G.O.Ms.No.201, Finance (HR-I Plg, &amp; Policy) "
                       "Dept., Dt: 21/12/2017"),
        "standard": "Both papers at degree standard",
        "papers": [("PAPER-I", "General Studies &amp; Mental Ability", 150, 150, 150),
                   ("PAPER-II", "Subject", 150, 150, 150)],
        "total": 300,
        "eligibility": ("Bachelor&rsquo;s Degree with Statistics as one of the main "
                        "subjects; or a Bachelor&rsquo;s Degree with Mathematics, "
                        "Economics, Commerce or Computer Science as one of the main "
                        "subjects, with Statistics as a paper in one, two or all three "
                        "years as the case may be."),
        "slug": "assistant-statistical-officer",
    },
}

NEGATIVE = ("As per G.O. Ms. No.235 Finance (HR-I, Plg &amp; Policy) Dept., Dt.06/12/2016, "
            "for each wrong answer will be penalized with 1/3rd of the marks prescribed "
            "for the question.")

# ------------------------------------------------- the ten shared subject items
# (item number, item title, AD paper it sits in, rows)
SUBJECT = [
 (1, "Economic Concepts", "PAPER-2", [
  ("Concepts of production, consumption and demand; concept of elasticity",
   bsc("applied statistics ii", 3), "brief"),
  ("Market structures and equilibrium; price determination", EC + "unit1.html", "deep"),
  ("National income: concepts and determinants &mdash; employment, consumption, savings and investment",
   EC + "unit2.html", "deep"),
  ("Rate of interest and profit", EC + "unit1.html", "brief"),
  ("Concepts of money and measures of money supply, velocity", EC + "unit3.html", "deep"),
  ("Banks and credit creation; banks and portfolio management; central bank and control over supply of money",
   EC + "unit3.html", "deep"),
  ("Determination of price level; inflation &mdash; meaning, measurement and control",
   bsc("applied statistics", 3), "brief"),
  ("Public finance: budgets, taxes and non-tax revenues, budget deficits", EC + "unit4.html", "deep"),
 ]),
 (2, "International Economics", "PAPER-2", [
  ("Free trade and protection", EC + "unit5.html", "deep"),
  ("Balance of payments accounts and adjustment; exchange rate under the exchange markets",
   EC + "unit5.html", "deep"),
  ("International Monetary System and World Trading order &mdash; Brettonwoods system. IMF and the World Bank and their associates",
   EC + "unit5.html", "brief"),
  ("Sources of growth &mdash; capital, human capital, productivity, trade and aid, non-economic factors",
   EC + "unit5.html", "brief"),
 ]),
 (3, "Indian Economics", "PAPER-2", [
  ("Population: size, composition, quality and growth trend; occupational distribution; effects of births and deaths",
   (bsc("applied statistics", 4), bsc("applied statistics", 5)), "deep"),
  ("Mass poverty; unemployment and its types; inequality and types thereof; rural&ndash;urban disparities",
   EC + "unit6.html", "deep"),
  ("Foreign trade: balance of payments and external debt", EC + "unit5.html", "brief"),
  ("Inflation and the parallel economy and its effects; fiscal deficit", EC + "unit4.html", "deep"),
  ("Sectoral trends and regional disparities", EC + "unit6.html", "brief"),
  ("Economic Planning in India: Major controversies on planning in India, NITI Ayog",
   EC + "unit6.html", "brief"),
  ("Broad fiscal, monetary, industry, trade and agricultural policies", EC + "unit6.html", "brief"),
 ]),
 (4, "Financial Accounting", "PAPER-2", [
  ("Introduction to accounting; accounting concepts and conventions", FA + "unit1.html", "deep"),
  ("Accounting process &mdash; journalizing, posting to ledger accounts", FA + "unit2.html", "deep"),
  ("Subsidiary books including cash book", FA + "unit3.html", "deep"),
  ("Bank reconciliation statement", FA + "unit4.html", "deep"),
  ("Preparation of trial balance and final accounts; errors and rectification", FA + "unit5.html", "deep"),
  ("Depreciation and reserves; single entry and non-trading concerns", FA + "unit6.html", "deep"),
 ]),
 (5, "Basics of Computers", "PAPER-2", [
  ("Binary system, octal and hexadecimal systems; conversion to and from decimal systems; codes, bits, bytes and words",
   CF + "unit1_computer-fundamentals.html", "deep"),
  ("Memory of a computer; arithmetic and logical operations on numbers",
   (CF + "unit1_computer-fundamentals.html", CF + "unit2_computer-fundamentals.html"), "deep"),
  ("Algorithms and flow charts",
   (D + "problem-solving-c/unit1_problem-solving-c.html",
    D + "problem-solving-c/unit2_problem-solving-c.html"), "deep"),
  ("Using Spread Sheet: Basics of Spreadsheet; Manipulation of cells; Formulas and Functions; Editing of Spread Sheet, printing of Spread Sheet",
   (CF + "unit4_computer-fundamentals.html",
    XL + "unit1_statistical data analysis using ms excel.html"), "deep"),
 ]),
 (6, "Introduction to Statistics", "PAPER-3", [
  ("Collection of data: primary and secondary data",
   bsc("descriptive statistics", 1), "deep"),
  ("Methods of sampling (random, non-random)",
   (bsc("sampling techniques", 1), bsc("sampling techniques", 2)), "deep"),
  ("Definition of probability", bsc("theory of probability", 1), "deep"),
  ("Census; schedule and questionnaire",
   (bsc("descriptive statistics", 1), bsc("sampling techniques", 1)), "deep"),
  ("Frequency distribution; tabulation",
   (bsc("descriptive statistics", 1), bsc("descriptive statistics", 2)), "deep"),
  ("Diagrammatic and graphic presentation of data",
   bsc("descriptive statistics", 2), "deep"),
 ]),
 (7, "Measures of Central Tendency", "PAPER-3", [
  ("Meaning, objectives and characteristics of measures of central tendency",
   bsc("descriptive statistics", 3), "deep"),
  ("Arithmetic mean, geometric mean, harmonic mean",
   bsc("descriptive statistics", 3), "deep"),
  ("Median and mode", bsc("descriptive statistics", 3), "deep"),
  ("Quartiles, deciles, percentiles", bsc("descriptive statistics", 3), "deep"),
  ("Properties of averages and their applications",
   bsc("descriptive statistics", 3), "deep"),
 ]),
 (8, "Measures of Dispersion and Skewness", "PAPER-3", [
  ("Dispersion: meaning and properties", bsc("descriptive statistics", 4), "deep"),
  ("Range, quartile deviation, mean deviation, standard deviation, coefficient of variation",
   bsc("descriptive statistics", 4), "deep"),
  ("Skewness: Meaning &mdash; Karl Pearson and Bowley's measures of skewness",
   bsc("descriptive statistics", 5), "deep"),
  ("Concept of kurtosis", bsc("descriptive statistics", 5), "deep"),
  ("Normal distribution",
   S + "theoretical continuous distributions/unit4_theoretical continuous distributions.html",
   "deep"),
 ]),
 (9, "Measure of Relation", "PAPER-3", [
  ("Correlation: meaning, uses and types of correlation",
   bsc("statistical methods", 2), "deep"),
  ("Karl Pearson's correlation coefficient", bsc("statistical methods", 2), "deep"),
  ("Spearman's rank correlation", bsc("statistical methods", 2), "deep"),
  ("Probable error", bsc("statistical methods", 3), "deep"),
 ]),
 (10, "Analysis of Time Series and Index Numbers", "PAPER-3", [
  ("Time series analysis: meaning and uses; components of time series",
   bsc("applied statistics", 1), "deep"),
  ("Measurement of trend and seasonal variations",
   (bsc("applied statistics", 1), bsc("applied statistics", 2)), "deep"),
  ("Utility of decomposition of time series; decentralization of data",
   bsc("applied statistics", 2), "deep"),
  ("Index numbers: meaning and importance", bsc("applied statistics", 3), "deep"),
  ("Methods of construction of index numbers: price index numbers, quantity index numbers",
   bsc("applied statistics", 3), "deep"),
  ("Tests of adequacy of index numbers", bsc("applied statistics", 3), "deep"),
  ("Base shifting and deflation of index numbers",
   bsc("applied statistics ii", 2), "deep"),
  ("Cost of living index numbers; limitations of index numbers",
   (bsc("applied statistics", 3), bsc("applied statistics ii", 2)), "deep"),
 ]),
]

# A note printed under a particular item's table.
ITEM_NOTES = {
 8: ("<strong>Two spellings corrected.</strong> Both notifications print "
     "&ldquo;Coefficient of Veriation&rdquo; and &ldquo;Karl Pearson and Bowl&rsquo;s measures "
     "of skewness&rdquo;. The lines above print <em>variation</em> and <em>Bowley&rsquo;s</em>, "
     "because reproducing the first would read as this site&rsquo;s own typo and the second "
     "would send you looking up the wrong statistician. Every other line on this page is the "
     "notification&rsquo;s own wording, with &hellip; marking where a long line has been "
     "shortened."),
}

# --------------------------------------------- General Studies, one graded line
GS_TITLES = [
 "Major current events and issues pertaining to International, National and State of Andhra Pradesh",
 "General science and its applications to day to day life; contemporary developments in science &amp; technology and information technology",
 "History of India, with a focus on Andhra Pradesh and the Indian National Movement",
 "Geography of India with focus on Andhra Pradesh",
 "Indian polity and governance: constitutional issues, public policy, reforms and e-Governance initiatives",
 "Indian economy and planning",
 "Sustainable development and environmental protection",
 "Disaster management: vulnerability profile, prevention and mitigation strategies, application of remote sensing and GIS",
 "Logical reasoning, analytical ability and logical interpretation",
]

GS_GRADED = [
 ("Data analysis: tabulation of data, visual representation of data, basic data analysis (summary statistics such as mean, median, mode and variance) and interpretation",
  (bsc("descriptive statistics", 2), bsc("descriptive statistics", 3),
   bsc("descriptive statistics", 4)), "deep"),
]

# ------------------------------------------------ Computer Proficiency Test
CPT = [
 ("A", "Part A &mdash; computing, systems and the internet", [
  ("Introduction to Computers &mdash; Components and their classification &mdash; Peripheral devices and their purpose. Input Devices &mdash; Keyboard, Mouse, Scanner &hellip; Output Devices: Display devices, Printers, Monitor, Speaker, Plotter, Secondary Storage Devices &hellip; Random-Access Memory (RAM) &mdash; Read-Only Memory (ROM) &mdash; Control Unit &mdash; Memory Unit &mdash; Arithmetic Logic Unit (ALU)",
   CF + "unit1_computer-fundamentals.html", "deep"),
  ("System Software, Application Software, Embedded software, Proprietary Software, Open source software (their purpose and characteristics only)",
   D + "problem-solving-c/unit1_problem-solving-c.html", "brief"),
  ("Purpose of operating system, Single User and Multi User Operating Systems with Examples",
   CF + "unit2_computer-fundamentals.html", "brief"),
  ("Interfacing Graphical User Interface (GUI), Differences between Character User Interface (CUI) and Graphical User Interface (GUI) &mdash; working With Files and Folders &hellip; Running An Application Through the File Manager &hellip; Setting up of Printer, Webcam, Scanner and other peripheral devices",
   CF + "unit2_computer-fundamentals.html", "brief"),
  ("Introduction to Linux &mdash; Features and advantages of Linux, File handling commands, directory handling commands &mdash; User Management &mdash; File permissions &hellip; Macintosh Apple Computer (MAC) OS &hellip; Basics commands",
   CF + "unit2_computer-fundamentals.html", "brief"),
  ("Minimum Hardware and Software Requirements for a system to use internet, Communication Protocols and Facilities &mdash; Various browsers &mdash; What is Internet Protocol (IP) Address &mdash; Steps required in connecting system to network &mdash; Uploading and Downloading Files from Internet",
   CF + "unit2_computer-fundamentals.html", "brief"),
  ("Sending and receiving mails, Basic E-Mail Functions, Using your word processor for E-mail, Finding E-Mail Address, Mailing Lists and lists Servers",
   CF + "unit2_computer-fundamentals.html", "brief"),
  ("WWW advantages of the Web &mdash; how to navigate with the Web &mdash; Web Searching",
   CF + "unit2_computer-fundamentals.html", "brief"),
 ]),
 ("B", "Part B &mdash; the office suite, practical", [
  ("MSOFFICE or any open source office like Libre Office / Apache Open Office / Neo office for Windows/Linux/Macintosh Apple Computer (MAC) OS",
   CF + "unit3_computer-fundamentals.html", "brief"),
  ("Introduction to Office Software &mdash; Starting and Exiting the Office Applications &mdash; Introducing the Office Shortcut Bar &mdash; Customizing Office Shortcut Bar",
   CF + "unit3_computer-fundamentals.html", "brief"),
  ("Common Office Tools and Techniques &mdash; Opening An Application &mdash; Creating Files &mdash; Entering And Editing Text &mdash; Saving Files &hellip; Managing Your files With the Office Applications",
   CF + "unit3_computer-fundamentals.html", "brief"),
  ("Key Combinations &mdash; Cut, Copy and Paste &mdash; Drag And Drop Editing &mdash; Menu Bars And Toolbars &mdash; Undo and Redo &mdash; Spell Checking &mdash; Auto Correct &mdash; Find and Replace &mdash; Help And The Office Assistants &mdash; Templates and Wizards",
   CF + "unit3_computer-fundamentals.html", "brief"),
  ("Starting Word &hellip; Designing Your Document &mdash; Typing Text &hellip; Formatting text and document &hellip; Saving Document &mdash; Page Setup &hellip; Printing &hellip; Page Break &mdash; Header and Footer &hellip; Table and Sorting &mdash; Working With Graphics &hellip; Word Art &hellip; Mail Merge",
   CF + "unit3_computer-fundamentals.html", "deep"),
  ("Features Of Excel &mdash; Excel worksheet &mdash; Selecting Cell &hellip; Entering And Editing Formulas &mdash; Referencing Cells &hellip; Excel Functions &hellip; Saving A Worksheet &mdash; Printing A Worksheet &hellip; Function Wizard &hellip; Organizing Your Data &mdash; Excel's Chart Features &hellip; Creating Trend Lines &hellip; Sorting Excel Data &mdash; Adding Subtotals To Databases &hellip; Comma Separated Value (CSV) File format &mdash; Using Worksheet As Databases",
   (CF + "unit4_computer-fundamentals.html",
    XL + "unit1_statistical data analysis using ms excel.html",
    XL + "unit2_statistical data analysis using ms excel.html",
    CF + "unit5_computer-fundamentals.html"), "deep"),
  ("Introduction &mdash; Starting Presentation Software &mdash; Views in Presentation Software &mdash; Slides &hellip; Color Schemes &mdash; Formatting Slides &mdash; Creating a Presentation &hellip; Using a Template &hellip; Working with Text in Power Point &hellip; Inserting A Picture &mdash; Working With Graphics &hellip; Assigning Transitions And Timings &mdash; Setting The Master Slide &mdash; Setting Up The Slide Show &mdash; Running The Slide Show",
   CF + "unit3_computer-fundamentals.html", "deep"),
 ]),
]

CPT_SCHEME = ("Proficiency in Office Automation with usage of Computers and Associated "
              "Software &mdash; practical, 60 minutes, 100 marks, with minimum qualifying "
              "marks of 30 (SC/ST/PBD), 35 (B.C.&rsquo;s) and 40 (O.C.&rsquo;s)")
CPT_SRC = "G.O.Ms.No.26, G.A. (Ser.B) Dept., dt: 24.02.2023"
