# -*- coding: utf-8 -*-
"""The worked solutions for the APPSC 2022 Paper-II ("ECOSTATS 0411S2"), and
where each is taught.

The same rules as appsc_paper_data.py, which this file builds on: the
paper's words are in appsc_paper_2022_text.py and its key in
appsc_paper_2022.json, and neither is repeated here. This file holds, for
each question, the syllabus topic it tests, the working, and -- where the
paper itself is loose -- a flag saying how.

The syllabus items and the four parts of the page are the 2025 paper's (the
same Paper-II syllabus). The topics are the 2025 paper's plus the ones this
paper adds; each is checked against its page's own text when the page is
built, exactly as before.
"""
from appsc_paper_data import GROUPS, ITEMS, TOPICS as TOPICS_2025  # noqa: F401  (re-exported)

ECO, FA, DS = "statistics/economics/", "statistics/financial-accounting/", "statistics/descriptive-statistics/"
AS, SM, CF = "statistics/applied-statistics/", "statistics/statistical-methods/", "data-science/computer-fundamentals/"
ST, TP = "statistics/sampling-techniques/", "statistics/theory-of-probability/"

TOPICS = dict(TOPICS_2025, **{
    # 1. Economic concepts
    "factors":     (1, ECO + "unit2.html", r"[Ff]actors of production"),
    "goods":       (1, ECO + "unit1.html", r"[Ii]nferior"),
    "deflator":    (1, ECO + "unit2.html", r"GDP deflator"),
    "investment":  (1, None, None),                      # induced and autonomous investment
    "msupply":     (1, ECO + "unit3.html", r"[Nn]arrow money"),
    "multiplier":  (1, ECO + "unit3.html", r"[Cc]redit multiplier|[Mm]oney multiplier"),
    "reserve":     (1, None, None),                      # reserve money
    "fiscal":      (1, ECO + "unit4.html", r"[Ff]iscal deficit"),
    "nontax":      (1, ECO + "unit4.html", r"[Nn]on-tax revenue"),
    "frbm":        (1, None, None),                      # the FRBM Act, 2003
    # 2. International economics
    "accounts-bop": (2, ECO + "unit5.html", r"[Cc]urrent [Aa]ccount"),
    "internal":    (2, None, None),                      # internal and wholesale trade
    # 3. Indian economics
    "plans":       (3, ECO + "unit6.html", r"Five Year Plan"),
    "agri":        (3, None, None),                      # the Green Revolution, agriculture policy
    "industry":    (3, None, None),                      # the Industrial Policy Resolution, 1956
    # 4. Financial accounting
    "conventions": (4, FA + "unit1.html", r"[Cc]onsistency"),
    "gconcern":    (4, FA + "unit1.html", r"[Gg]oing [Cc]oncern"),
    "accounts":    (4, FA + "unit1.html", r"[Rr]eal account"),
    "trial":       (4, FA + "unit5.html", r"[Tt]rial [Bb]alance"),
    "rectify":     (4, FA + "unit5.html", r"[Rr]ectification"),
    "capital-rev": (4, None, None),                      # capital and revenue expenditure
    "depreciation": (4, FA + "unit6.html", r"[Dd]epreciation"),
    "single":      (4, FA + "unit6.html", r"[Ss]ingle [Ee]ntry"),
    # 5. Computers
    "units":       (5, CF + "unit2.html", r"\bKB\b"),
    "excel-fn":    (5, CF + "unit4.html", r"COUNTA"),
    "excel-fin":   (5, None, None),                      # IPMT and PPMT
    # 6. Introduction to statistics
    "scales":      (6, DS + "unit2.html", r"[Tt]rue zero"),
    "likert":      (6, "statistics/statistical-techniques-for-research-methodology/unit2.html", r"Likert"),
    "populations": (6, ST + "unit1.html", r"[Ii]nfinite"),
    "samplesize":  (6, ST + "unit2.html", r"[Ss]ample size"),
    "events":      (6, TP + "unit1.html", r"[Mm]utually exclusive"),
    "bayes":       (6, TP + "unit1.html", r"Bayes"),
    "pie":         (6, DS + "unit2.html", r"[Pp]ie"),
    "ogive":       (7, DS + "unit2.html", r"[Oo]give"),
    # 7. Central tendency
    "gm":          (7, DS + "unit3.html", r"[Gg]eometric"),
    "mode":        (7, DS + "unit3.html", r"[Ee]mpirical"),
    "partition":   (7, DS + "unit3.html", r"[Pp]ercentile"),
    "midrange":    (7, None, None),                      # the midrange
    # 8. Dispersion and skewness
    "range":       (8, DS + "unit4.html", r"[Cc]oefficient of [Rr]ange"),
    "qd":          (8, DS + "unit4.html", r"[Qq]uartile [Dd]eviation"),
    "sd":          (8, DS + "unit4.html", r"[Ss]tandard [Dd]eviation"),
    "moments":     (8, DS + "unit5.html", r"[Mm]oments"),
    "kurtosis":    (8, DS + "unit5.html", r"[Kk]urtosis"),
    # 9. Correlation
    "regression":  (9, SM + "unit3.html", r"[Rr]egression"),
    "cratio":      (9, SM + "unit3.html", r"[Cc]orrelation ratio"),
    "icc":         (9, SM + "unit3.html", r"[Ii]ntra-class"),
    "rdist":       (9, None, None),                      # the sampling distribution of r
    # 10. Time series and index numbers
    "semiavg":     (10, AS + "unit1.html", r"[Ss]emi-average"),
    "ma":          (10, AS + "unit1.html", r"[Mm]oving [Aa]verage"),
    "components":  (10, AS + "unit1.html", r"[Ii]rregular"),
    "deseason":    (10, AS + "unit2.html", r"[Dd]eseasonal"),
    "sindex":      (10, AS + "unit2.html", r"[Ss]easonal [Ii]ndex"),
    "detrend":     (10, "statistics/applied-statistics-ii/unit1.html", r"[Dd]etrend"),
    "stl":         (10, None, None),                      # STL decomposition
    "col":         (10, AS + "unit3.html", r"[Cc]ost of [Ll]iving"),
    "paasche":     (10, AS + "unit3.html", r"Paasche"),
    "circular":    (10, AS + "unit3.html", r"[Cc]ircular"),
})

# What the topics this site does not teach yet are called, for the list at
# the foot of the page (the 2025 paper's names are in appsc_paper.py).
GAP_NAMES = {
    "investment": "Induced and autonomous investment",
    "reserve": "Reserve money (M0)",
    "frbm": "The FRBM Act, 2003",
    "internal": "Internal and wholesale trade",
    "agri": "The Green Revolution and the National Agriculture Policy",
    "industry": "The Industrial Policy Resolution, 1956",
    "capital-rev": "Capital and revenue expenditure (what goes into an asset&rsquo;s cost)",
    "excel-fin": "Excel&rsquo;s financial functions (IPMT, PPMT)",
    "midrange": "The midrange",
    "rdist": "The sampling distribution of the correlation coefficient",
    "stl": "STL decomposition",
}

# Why the Commission withdrew each withdrawn question -- the working for it.
WITHDRAWN = {
    51: "The Commission withdrew this question. As printed, statement (i) describes the occasionally "
        "poor and then calls them &ldquo;the usually poor&rdquo; &mdash; but the usually poor are the "
        "chronic poor, and the occasionally poor are one half of the <em>transient</em> poor. "
        "Statement (ii) gives the transient poor the definition of the <em>churning</em> poor, the "
        "other half. Both statements mix up the textbook&rsquo;s terms, so no option can be marked "
        "safely.",
    81: "The Commission withdrew this question. For two regression coefficients with the same sign as "
        "$r$, $\\tfrac{1}{2}(b_{yx}+b_{xy}) \\ge \\sqrt{b_{yx}b_{xy}} = |r|$ (the AM of two positive "
        "numbers is at least their GM). So the mean of the coefficients is at least $r$ when $r \\gt 0$, "
        "but at most $r$ when $r \\lt 0$: &ldquo;greater than or equal to&rdquo; holds only for the "
        "numerical values, and the question does not say so.",
}

# n: (topic, working, flag or None). The working is HTML; mathematics in $...$.
SOLUTIONS = {
    1: ("factors", "The four factors of production are land, labour, capital and organisation "
        "(enterprise); each earns rent, wages, interest and profit. A service is an output, not a factor.", None),
    2: ("goods", "Complements are used together (car and petrol): a rise in the price of X lowers the "
        "demand for Y. For substitutes the relation runs the other way &mdash; a dearer X raises the "
        "demand for Y.", None),
    3: ("goods", "For an inferior good demand falls as income rises, so its income effect is negative: "
        "(i) is false and (ii) is true.", None),
    4: ("demand", "Perfectly elastic demand has $E_d = \\infty$ (a horizontal demand curve); $E_d = 1$ is "
        "unit elasticity. The other three are stated correctly.", None),
    5: ("market", "Many firms selling close but differentiated products (brands of soap, toothpaste) is "
        "monopolistic competition. Perfect competition has identical products, oligopoly a few firms.", None),
    6: ("deflator", "GDP deflator $= \\dfrac{\\text{nominal GDP}}{\\text{real GDP}} = \\dfrac{18{,}000}{12{,}000} "
        "= 1.5$, or 150%.", None),
    7: ("natinc", "National income is measured by the value added (product), income and expenditure "
        "methods. Cost accounting is a branch of accounting, not a method of measuring it.", None),
    8: ("consumption", "Saving $= 100 - 80 = 20$, so APS $= S/Y = 20/100 = 20\\%$.", None),
    9: ("investment", "Investment that responds to a change in income (or output) is induced investment. "
        "Autonomous investment does not depend on income; gross and net differ only by depreciation.", None),
    10: ("msupply", "Both are items <em>excluded</em> from the money supply: cash held by the banks "
         "themselves is not money with the public, and the monetary gold kept as backing for the "
         "currency is not in circulation. So statement (i), which says the banks&rsquo; cash is included, "
         "is incorrect.",
         "Statement (ii) says the monetary gold reserve <em>is</em> included in the money supply. It is "
         "not &mdash; it is excluded for the same reason as the banks&rsquo; cash &mdash; so by the "
         "question&rsquo;s own heading both statements are incorrect, which is option (1). The paper "
         "marks (4)."),
    11: ("money", "The primary (main) functions are medium of exchange and measure of value. Store of "
         "value and transfer of value (standard of deferred payment) are the secondary functions.", None),
    12: ("msupply", "The RBI&rsquo;s old four measures: $M_1$ as stated in (i); $M_2 = M_1 +$ savings "
         "deposits with post office savings banks; $M_4 = M_3 +$ all post office deposits except National "
         "Savings Certificates. (iii) is wrong: $M_3 = M_1 +$ net time deposits of <em>all</em> banks, "
         "commercial and cooperative, not $M_2$ plus cooperative banks only.", None),
    13: ("multiplier", "Credit multiplier $= 1/\\text{RRR} = 1/0.10 = 10$, so a deposit of ₹1,00,000 "
         "supports $10 \\times 1{,}00{,}000 = \\text{₹}10{,}00{,}000$ of total deposits.", None),
    14: ("reserve", "Reserve money (M0, high-powered money) is currency in circulation plus the banks&rsquo; "
         "deposits with the RBI plus other deposits with the RBI. Deposits with the SBI are ordinary bank "
         "deposits.", None),
    15: ("msupply", "$M_1 =$ currency with the public $+$ demand deposits $+$ other deposits with the RBI "
         "$= 90{,}000 + 2{,}00{,}000 + 2{,}80{,}000 = \\text{₹}5{,}70{,}000$ crores. Time deposits and post office "
         "savings deposits belong to broader measures.", None),
    16: ("budget", "(i) is the definition of the annual financial statement. (ii) is false: James Wilson "
         "presented India&rsquo;s first budget in 1860, not in 1880.", None),
    17: ("brs", "Starting from a debit (favourable) cash-book balance, cheques issued but not yet presented "
         "have been deducted in the cash book but not yet by the bank, so they are added. The other three "
         "are deducted.", None),
    18: ("nontax", "Non-tax revenue is what the government earns without taxing: interest on its loans, "
         "dividends and profits of public enterprises, fees, and grants received. All three qualify.", None),
    19: ("fiscal", "Budget deficit $=$ total expenditure $-$ total receipts $= (30{,}000 + 50{,}000) - "
         "(40{,}000 + 30{,}000) = \\text{₹}10{,}000$ crores.", None),
    20: ("exchange", "A direct quote is the number of units of <em>home</em> currency per unit of foreign "
         "currency (so many rupees to the dollar). Units of foreign currency per unit of home currency is an indirect quote, "
         "so statement 2 is the false one.", None),
    21: ("bop", "Balance of trade $=$ exports $-$ imports, so exports $= 800 + 9{,}000 = \\text{₹}9{,}800$ crores.", None),
    22: ("bop", "Both are the textbook definitions: the balance of payments records all economic "
         "transactions with the rest of the world in a year, and the current account holds goods, "
         "services and unilateral transfers.", None),
    23: ("accounts-bop", "Flows belonging to the current year (trade, income, transfers) go to the current "
         "account; transfers of financial assets and non-produced, non-financial assets go to the capital "
         "account.", None),
    24: ("ims", "The IMF was set up at the Bretton Woods Conference of July 1944.",
         "The conference was in 1944; the IMF formally came into being in December 1945 and began work in "
         "1947. The key rests on reading &ldquo;established&rdquo; as &ldquo;agreed at Bretton "
         "Woods&rdquo;."),
    25: ("wb", "The World Bank Group has five institutions: IBRD, IDA, IFC, MIGA and ICSID.", None),
    26: ("wb", "The International Bank for Reconstruction and Development, founded at Bretton Woods, is "
         "the institution known as the World Bank (with IDA it forms the World Bank proper).", None),
    27: ("internal", "Both are the standard definitions: internal (home) trade is within a country&rsquo;s "
         "borders, and buying and selling in bulk for resale or further use is wholesale trade.", None),
    28: ("growth", "The stock of skill, education and knowledge in people is human capital. Human capital "
         "<em>formation</em> is the process of adding to that stock.", None),
    29: ("binary", "Multiply the fraction by 2 and read off the integer parts: $0.25 \\times 2 = 0.5$ (0), "
         "$0.5 \\times 2 = 1.0$ (1). So $(0.25)_{10} = (0.01)_2$.", None),
    30: ("unemploy", "Unemployment while people move between jobs is frictional. Seasonal follows the "
         "season, cyclical follows the business cycle, and visible (open) unemployment is joblessness "
         "that can be seen and counted.", None),
    31: ("binary", "$1011010_2 = 64 + 16 + 8 + 2 = 90$.", None),
    32: ("binary", "$952 = 3 \\times 256 + 184$ and $184 = 11 \\times 16 + 8$, so the digits are 3, 11 (B), "
         "8: $(3B8)_{16}$.", None),
    33: ("binary", "Each octal digit is three bits: $7 = 111$, $0 = 000$, $5 = 101$, so "
         "$(705)_8 = (111000101)_2$.", None),
    34: ("binary", "$3 \\times 8^3 + 0 \\times 8^2 + 4 \\times 8 + 7 = 1536 + 0 + 32 + 7 = 1575$.", None),
    35: ("binary", "Group in fours from the right: $01\\;1010\\;1100 = 1, A, C$, so $(1AC)_{16}$.", None),
    36: ("units", "Each step is a factor of $2^{10} = 1024$: kilobyte $2^{10}$, megabyte $2^{20}$, gigabyte "
         "$2^{30}$ bytes (and a terabyte $2^{40}$).", None),
    37: ("excel", "A spreadsheet is a grid of rows and columns (i). But columns are lettered A, B, C&hellip; "
         "and rows numbered 1, 2, 3&hellip; &mdash; (ii) and (iii) have them the wrong way round.", None),
    38: ("excel", "Manipulating a cell means working on its contents &mdash; entering, editing, deleting. "
         "Page layout and the clipboard are features of the program, not operations on a cell.", None),
    39: ("excel", "The key takes both as true: formulas combine operators and functions, and a formula is "
         "typed beginning with =.",
         "Both statements are loose. The = sign is not an arithmetic operator, and Excel also accepts a "
         "formula typed beginning with + or &minus; (it adds the = itself)."),
    40: ("excel", "Column 15 is the 15th letter, O, and column 6 is F; the address is column then row: "
         "O4 and F10.", None),
    41: ("excel-fn", "COUNTA counts the cells that are <em>not</em> empty (COUNTBLANK counts the empty "
         "ones), so statement 1 is false. The other three are Excel&rsquo;s own definitions.", None),
    42: ("excel-fn", "All three are Excel&rsquo;s definitions of AVERAGE, CORREL and MIN.", None),
    43: ("excel-fin", "Both are Excel&rsquo;s definitions: for a loan repaid in equal instalments, IPMT gives "
         "the interest part of a period&rsquo;s payment and PPMT the principal part.", None),
    44: ("excel-fn", "SUMIF adds only the cells that meet a criterion (SUM adds them all), and it is NOT, "
         "not OR, that reverses a logical value. Both are false.", None),
    45: ("population", "Census 2011 put India&rsquo;s density at 382 persons per sq. km (up from 325 in "
         "2001).", None),
    46: ("population", "Census 2011 (provisional totals): 623.7 million males and 586.5 million females, "
         "1,210.2 million in all.", None),
    47: ("population", "Census 2011 (provisional totals): 1,210.2 million (121.02 crore). 1,028 million was "
         "the 2001 figure.", None),
    48: ("poverty", "Dadabhai Naoroji, in <em>Poverty and Un-British Rule in India</em>, first estimated a "
         "poverty line for India, from the cost of a subsistence diet.", None),
    49: ("poverty", "Naoroji based his estimate on the cost of the diet given to prisoners &mdash; the "
         "&lsquo;jail cost of living&rsquo;.", None),
    50: ("unemploy", "When more people work on a job than it needs, so that some could leave without output "
         "falling (their marginal product is zero), the unemployment is disguised. It is common on family "
         "farms.", None),
    51: ("poverty", WITHDRAWN[51], None),
    52: ("fiscal", "Fiscal deficit $=$ total expenditure $-$ (revenue receipts $+$ non-debt capital "
         "receipts) $= 1{,}50{,}000 - (1{,}20{,}000 + 10{,}000) = \\text{₹}20{,}000$ crores.", None),
    53: ("frbm", "The Fiscal Responsibility and Budget Management Act was passed in 2003 (it came into force "
         "in 2004).", None),
    54: ("plans", "The First Plan ran from 1951 to 1956 and the Second from 1956 to 1961.", None),
    55: ("plans", "The Second Plan (1956&ndash;61) was built on P.C. Mahalanobis&rsquo;s model, with its "
         "stress on heavy industry.", None),
    56: ("plans", "NITI Aayog, the National Institution for Transforming India, replaced the Planning "
         "Commission on 1 January 2015.", None),
    57: ("agri", "M.S. Swaminathan led the introduction of high-yielding wheat and rice in India and is "
         "called the father of its Green Revolution.", None),
    58: ("agri", "The first National Agricultural Policy was announced in July 2000.", None),
    59: ("industry", "The 1956 Resolution enlarged the public sector (Schedules A, B and C), kept industrial "
         "licensing for the private sector, and gave a special place to small and village industries.", None),
    60: ("gconcern", "Recording on the assumption that the business will continue indefinitely is the going "
         "concern concept; it is why assets are carried at cost less depreciation rather than at sale "
         "value.", None),
    61: ("concepts", "Business entity: the business is separate from its owner, so the owner&rsquo;s "
         "personal expenses paid by the business are drawings, not business expenses.", None),
    62: ("conventions", "Keeping to the same method from year to year, so that one year&rsquo;s accounts "
         "compare with the next, is the convention of consistency.", None),
    63: ("concepts", "The owner&rsquo;s medical bills are personal, and charging them to the firm mixes the "
         "owner with the business: it breaks the business entity concept.", None),
    64: ("moneymeas", "Only what can be measured in money is recorded; qualitative facts (staff morale, a "
         "manager&rsquo;s skill) are left out. That is the money measurement concept.", None),
    65: ("journal", "Pranab&rsquo;s account is closed by debiting the full ₹40,000; the bank pays "
         "₹39,000 and the ₹1,000 he allowed is a gain: Pranab A/c Dr. 40,000, To Bank A/c 39,000, To "
         "Discount received A/c 1,000.", None),
    66: ("capital-rev", "Repairs needed to make a second-hand machine fit for use are part of the cost of "
         "acquiring it, so they are capitalised: debited to the Machinery A/c. Repairs during use would "
         "go to a Repairs A/c.", None),
    67: ("accounts", "The cash account is a real account (an asset). The bank account is a personal "
         "account &mdash; the bank is an artificial person &mdash; so (ii) is false.", None),
    68: ("brs", "Starting from a credit (favourable) pass-book balance, cheques issued but not yet presented "
         "will still reduce the bank balance, so they are deducted. The other three are added.", None),
    69: ("brs", "Both are credits the bank has made that the cash book does not yet show, so the pass book "
         "is higher; starting from its balance, both are deducted.", None),
    70: ("trial", "Assets and expenses are debit balances: cash, sundry debtors, bills receivable and "
         "goodwill. Liabilities and gains are credit balances: rent outstanding, creditors, bank overdraft "
         "and sales.", None),
    71: ("depreciation", "A loss on the sale of a fixed asset is a capital loss charged against the "
         "year&rsquo;s profit: debited to the Profit and Loss Account (the asset account is credited to "
         "close it).", None),
    72: ("rectify", "(i) The purchase was posted as a sale: Ram was debited and Sales credited ₹1,500. "
         "Undo it and post it right: Purchases Dr. 1,500 and Sales Dr. 1,500, To Ram 3,000. (ii) The sale "
         "was posted as a purchase: Purchases debited and Ramesh credited ₹1,200. So Ramesh Dr. 2,400, To "
         "Purchases 1,200, To Sales 1,200.", None),
    73: ("capital-rev", "Everything spent to bring an asset to use is capitalised: $5{,}00{,}000 + 20{,}000 "
         "+ 35{,}000 = \\text{₹}5{,}55{,}000$.", None),
    74: ("depreciation", "At 10% on the diminishing balance: year 1 ₹2,000 (book value 18,000), year 2 "
         "₹1,800 (16,200), year 3 $0.10 \\times 16{,}200 = \\text{₹}1{,}620$.", None),
    75: ("single", "Profit $=$ closing capital $-$ opening capital $+$ drawings $-$ fresh capital "
         "$= 33{,}800 - 30{,}400 + 9{,}600 - 4{,}000 = \\text{₹}9{,}000$.", None),
    76: ("correlation", "$r$ is unchanged by a change of origin and by a change of scale (up to its sign, "
         "if a scale factor is negative), so both statements hold.", None),
    77: ("correlation", "Pearson&rsquo;s $r$ needs interval or ratio data (I). It is a pure number, so "
         "the two variables may well be in entirely different units &mdash; height in cm, weight in kg; "
         "II is false.", None),
    78: ("rank", "Ranks in mathematics 2, 1, 4, 3, 5 and in statistics 4, 1, 3, 2, 5; $d = -2, 0, 1, 1, 0$, "
         "$\\sum d^2 = 6$. $\\rho = 1 - \\dfrac{6 \\times 6}{5(25 - 1)} = 1 - 0.3 = 0.70$.", None),
    79: ("correlation", "$r = \\dfrac{n\\sum xy - \\sum x \\sum y}{\\sqrt{(n\\sum x^2 - (\\sum x)^2)"
         "(n\\sum y^2 - (\\sum y)^2)}} = \\dfrac{4295 - 4290}{\\sqrt{(67650 - 67600)(272.75 - 272.25)}} "
         "= \\dfrac{5}{\\sqrt{50 \\times 0.5}} = 1$.", None),
    80: ("regression", "Taking $Y + X = 5$ as $Y$ on $X$: $b_{yx} = -1$; and $Y + 2X = 3$ as $X$ on $Y$: "
         "$X = (3 - Y)/2$, $b_{xy} = -\\tfrac{1}{2}$. (The other way round the product would be 2, more "
         "than 1, which is impossible.) $r^2 = b_{yx}b_{xy} = 0.5$.",
         "Both regression coefficients are negative, so $r = -\\sqrt{0.5} = -0.707$. The paper&rsquo;s "
         "0.707 is its numerical value; no option carries the sign."),
    81: ("regression", WITHDRAWN[81], None),
    82: ("cratio", "The correlation ratio is $\\eta^2 = $ (dispersion between the categories) $/$ (total "
         "dispersion). With no dispersion within the categories, the two are equal and $\\eta = 1$.", None),
    83: ("icc", "On the usual reading of the intraclass correlation (Koo and Li): below 0.5 poor, 0.5 "
         "to 0.75 moderate, 0.75 to 0.9 good, above 0.9 excellent. 0.782 is good.",
         "The paper says &ldquo;interclass&rdquo;; the reliability of ratings by different raters is "
         "measured by the <em>intraclass</em> correlation, and the bands are a published guideline rather "
         "than a definition."),
    84: ("rdist", "If $\\rho = 0$, $t = \\dfrac{r\\sqrt{n-2}}{\\sqrt{1-r^2}}$ follows Student&rsquo;s $t$ "
         "with $n - 2$ degrees of freedom (two are used up estimating the two means).", None),
    85: ("rdist", "Under $\\rho = 0$ the density of $r$ is $f(r) = \\dfrac{(1-r^2)^{(n-4)/2}}"
         "{B\\left(\\frac{1}{2}, \\frac{n-2}{2}\\right)}$, $-1 \\le r \\le 1$ &mdash; the density that "
         "gives the $t$ result above.", None),
    86: ("index", "Laspeyres uses base-year quantities: $\\dfrac{\\sum p_1q_0}{\\sum p_0q_0} \\times 100 = "
         "\\dfrac{40 + 72 + 100 + 45}{20 + 60 + 80 + 30} \\times 100 = \\dfrac{257}{190} \\times 100 = 135.3$.", None),
    87: ("paasche", "Paasche&rsquo;s quantity index weights by current prices: $\\dfrac{\\sum q_1p_1}{\\sum "
         "q_0p_1} \\times 100 = \\dfrac{110 + 108 + 340}{88 + 54 + 204} \\times 100 = \\dfrac{558}{346} "
         "\\times 100 = 161.27$.", None),
    88: ("circular", "$P_{01} \\times P_{12} \\times P_{20} = 1$ &mdash; going round the cycle of years "
         "brings the index back to where it started &mdash; is the circular test.", None),
    89: ("col", "A cost of living index is built by either the aggregate expenditure method (weights are "
         "base-year quantities) or the family budget method (a weighted mean of price relatives, the "
         "weights being base-year expenditure).", None),
    90: ("quartile", "In order: 23, 25, 29, 34, 47, 52, 57, 62. $Q_3$ is the $\\tfrac{3(n+1)}{4} = 6.75$th "
         "value $= 52 + 0.75(57 - 52) = 55.75$.", None),
    91: ("dispersion", "Range $=$ largest $-$ smallest $= 9\\% - 4\\% = 5\\%$.", None),
    92: ("dispersion", "Mean $= 2{,}00{,}000/4 = 50{,}000$; absolute deviations 10,000, 30,000, 10,000, "
         "30,000; their mean is 20,000.", None),
    93: ("range", "Coefficient of range $= \\dfrac{L - S}{L + S} = \\dfrac{82 - 43}{82 + 43} = "
         "\\dfrac{39}{125} = 0.312$.", None),
    94: ("qd", "$\\dfrac{Q_3 - Q_1}{Q_3 + Q_1} = 0.57$ gives $31 - Q_1 = 0.57(31 + Q_1)$, so $1.57\\,Q_1 = "
         "13.33$ and $Q_1 \\approx 8.5$.", None),
    95: ("cv", "Coefficient of standard deviation $= \\sigma/\\bar{x}$, so $\\sigma = 0.40 \\times 5 = 2$ and "
         "the variance is 4.", None),
    96: ("dispersion", "Coefficient of mean deviation $=$ MD $/$ mean, so mean $= 15{,}000/0.3 = 50{,}000$.", None),
    97: ("qd", "25% earn more than ₹45,000, so $Q_3 = 45{,}000$. QD $= (Q_3 - Q_1)/2 = 13{,}500$ gives "
         "$Q_1 = 18{,}000$, and 75% earn more than $Q_1$.", None),
    98: ("hm", "For two numbers $G^2 = AH$, so $H = G^2/A = 36/12 = 3$.", None),
    99: ("gm", "Mean $14/3$: $2 + a + b = 14$, $a + b = 12$. GM 4: $2ab = 64$, $ab = 32$. So $a, b$ are 4 "
         "and 8.", None),
    100: ("hm", "Write the numbers $6 - d, 6, 6 + d$. $\\dfrac{3}{\\frac{1}{6-d} + \\frac{1}{6} + "
          "\\frac{1}{6+d}} = \\dfrac{54}{11}$ gives $\\dfrac{12}{36 - d^2} = \\dfrac{4}{9}$, so "
          "$36 - d^2 = 27$. GM $= \\big(6(36 - d^2)\\big)^{1/3} = (162)^{1/3}$.", None),
    101: ("median", "$N = 39$, $N/2 = 19.5$; cumulative frequencies 4, 10, 18, 30, so the median class is "
          "48&ndash;52. Median $= 48 + \\dfrac{19.5 - 18}{12} \\times 4 = 48.5$. (The classes are unequal; "
          "the formula uses the median class&rsquo;s own width.)", None),
    102: ("gm", "Product of all five $= 8^5$, of the first three $= 4^3$, so of the last two $= 8^5/4^3 = "
          "512$, and their GM $= \\sqrt{512} = 16\\sqrt{2}$.", None),
    103: ("gm", "The new numbers are the old ones times 12, 48, 192, 768, 3072 &mdash; that is, "
          "$12 \\times 4^k$ with GM $12 \\times 4^2 = 192$. The GM of a product is the product of the GMs: "
          "$8 \\times 192 = 1536$.", None),
    104: ("average", "$\\tfrac{1}{2}\\big(\\log\\tfrac{x}{y} + \\log xy\\big) = \\tfrac{1}{2}(\\log x - \\log y "
          "+ \\log x + \\log y) = \\log x$.", None),
    105: ("dispersion", "Midrange, quartiles and the maximum all locate a point of the distribution. The "
          "range is a spread &mdash; a measure of dispersion.", None),
    106: ("midrange", "Midrange $= \\tfrac{1}{2}(\\text{smallest} + \\text{largest}) = \\tfrac{1}{2}(0 + 10) "
          "= 5$.", None),
    107: ("quartile", "In order: 24, 25, 29, 29, 30, 31. $Q_1$ is the $\\tfrac{n+1}{4} = 1.75$th value "
          "$= 24.75$ and $Q_3$ the 5.25th $= 30.25$; IQR $= 5.5$ days.",
          "The answer depends on the quartile rule: with $(n+1)/4$ it is 5.5, while the medians of the "
          "two halves (25 and 30) give 5.0, which is also an option."),
    108: ("median", "In order: 21, 22, 23, 26, 28, 29. With six values the median is the mean of the "
          "third and fourth: $(23 + 26)/2 = 24.5$.", None),
    109: ("mode", "Empirically, mode $= 3\\,$median $- 2\\,$mean, so $20 = 3M - 28$ and $M = 16$.", None),
    110: ("average", "Modal class 68&ndash;74 ($f_1 = 35$, $f_0 = 25$, $f_2 = 18$, $h = 6$). Mode $= 68 + "
          "\\dfrac{35 - 25}{2(35) - 25 - 18} \\times 6 = 68 + \\dfrac{10}{27} \\times 6 = 70.22$.", None),
    111: ("average", "In order: 15, 17, 18, 18, 18, 19, 19, 19, 19. The median is the 5th value, 18; the "
          "mode is 19 (four times); the mean is $162/9 = 18$.", None),
    112: ("cv", "2, 3, 5, 6 are 1, 2, 4, 5 plus 1: the SD stays $\\sqrt{2.5}$ but the mean rises from 3 to 4. "
          "CV $= \\dfrac{\\sqrt{2.5}}{4} \\times 100 = \\sqrt{\\tfrac{5}{32}} \\times 100$.", None),
    113: ("cv", "CV 20% with mean 20 gives $\\sigma_X = 4$. $\\text{Var}(20 - 3X) = 9\\,\\text{Var}(X) = "
          "9 \\times 16 = 144$.", None),
    114: ("moments", "$\\mu_3 = \\mu_3' - 3\\mu_2'\\mu_1' + 2\\mu_1'^3 = -32 - 3(18)(-2.5) + 2(-2.5)^3 = -32 "
          "+ 135 - 31.25 = 71.75$.", None),
    115: ("kurtosis", "$\\beta_2 = \\mu_4/\\mu_2^2 = 20/25 = 0.8$.", None),
    116: ("skewness", "Bowley&rsquo;s coefficient $= \\dfrac{Q_3 + Q_1 - 2Q_2}{Q_3 - Q_1} = \\dfrac{25.5 + "
          "20.5 - 46}{5} = 0$.", None),
    117: ("sd", "Mean 13; deviations $-4, -2, 1, -1, 4, 2$; squares sum to 42. $\\sigma = \\sqrt{42/6} = "
          "\\sqrt{7}$.", None),
    118: ("sd", "Mean 4 gives $a + b = 7$; variance $\\tfrac{2}{3}$ gives $\\tfrac{25 + a^2 + b^2}{3} - 16 = "
          "\\tfrac{2}{3}$, so $a^2 + b^2 = 25$. Hence 4 and 3.", None),
    119: ("sd", "Adding $\\beta$ moves every value equally and leaves the spread alone; multiplying by "
          "$\\alpha$ multiplies it. So the SD is $\\alpha t$.",
          "Strictly the SD is $|\\alpha|\\,t$ &mdash; an SD is never negative &mdash; so $\\alpha t$ is right "
          "only for $\\alpha \\gt 0$."),
    120: ("partition", "$N = 70$, $3N/10 = 21$; cumulative frequencies 8, 20, 34, so $D_3$ is in 30&ndash;40. "
          "$D_3 = 30 + \\dfrac{21 - 20}{14} \\times 10 = 30.71$.", None),
    121: ("partition", "$N = 80$, $0.9N = 72$; cumulative frequencies 8, 18, 40, 65, 75, so $P_{90}$ is in "
          "60&ndash;80. $P_{90} = 60 + \\dfrac{72 - 65}{10} \\times 20 = 74.0$.", None),
    122: ("components", "A fire is a one-off, unpredictable event: an irregular (random) variation. Trend, "
          "seasonal and cyclical movements are systematic.", None),
    123: ("ts", "The components are trend, seasonal variations, cyclical variations and irregular "
          "variations.",
          "&ldquo;Periodic movements&rdquo; is not a separate component, but it is the usual name for "
          "the seasonal and cyclical components together, so the question tests a label rather than an "
          "idea."),
    124: ("stl", "STL is Seasonal and Trend decomposition using Loess (locally weighted regression), the "
          "method of Cleveland and others (1990).", None),
    125: ("deseason", "Deseasonalising removes the seasonal component (dividing each value by its "
          "seasonal index, or subtracting the seasonal effect), leaving trend, cycle and irregular.", None),
    126: ("detrend", "A trend can be removed either by differencing ($y_t - y_{t-1}$) or by fitting a trend "
          "model and keeping the residuals; both are standard.", None),
    127: ("ma", "A moving average smooths out short-term fluctuations, and in doing so reveals the trend.",
          "A moving average smooths out short-term fluctuations in order to <em>show</em> the long-term "
          "trend; it does not smooth the trend away. On that reading only (I) is correct; the key&rsquo;s "
          "&ldquo;both&rdquo; treats &ldquo;smooth out&rdquo; as &ldquo;bring out&rdquo;."),
    128: ("semiavg", "Split the eight years into halves: $\\bar{y}_1 = (20 + 22 + 20 + 21)/4 = 20.75$ "
          "centred at 2012.5 and $\\bar{y}_2 = (23 + 26 + 28 + 30)/4 = 26.75$ centred at 2016.5. The "
          "trend line joins these two points.", None),
    129: ("frequency", "Tally the 22 values: 41&ndash;49: 42, 45, 47 (3); 50&ndash;58: 51, 51, 53, 58, 54, "
          "52 (6); 59&ndash;67: 61, 64, 63, 67, 59 (5); 68&ndash;76: 76, 68, 74, 72, 70, 75 (6); "
          "77&ndash;85: 83, 79 (2).", None),
    130: ("data", "Material someone else has already collected and published &mdash; government "
          "publications, books, websites, records &mdash; is secondary data.", None),
    131: ("frequency", "A frequency curve is described by its central tendency, dispersion and shape "
          "(skewness, kurtosis). A frequency polygon is another <em>diagram</em>, not a characteristic.", None),
    132: ("scales", "Only the ratio scale has a true (absolute) zero, which is what makes ratios such as "
          "&ldquo;twice as heavy&rdquo; meaningful.", None),
    133: ("likert", "The key follows survey practice, where Likert items, the 0&ndash;10 net promoter "
          "score and bipolar rating grids are all analysed as interval data.",
          "Strictly, a Likert item is ordinal &mdash; the steps are ordered but not known to be equal "
          "&mdash; and treating it as interval is a convention. On a strict reading (I) would not "
          "qualify."),
    134: ("populations", "Germs in a body cannot be counted out one by one; the textbook treats such a "
          "population as infinite.", None),
    135: ("sampling", "Stratified sampling divides the population into <em>homogeneous</em> strata (alike "
          "within, different between). &ldquo;Heterogeneous groups&rdquo; is wrong; the other three "
          "describe their methods.", None),
    136: ("probability", "$P = \\dfrac{\\binom{5}{2} + \\binom{3}{2}}{\\binom{8}{2}} = \\dfrac{10 + 3}{28} = "
          "\\dfrac{13}{28}$.", None),
    137: ("events", "Let $P(X) = p$; then $P(Y) = p/2$ and $P(Z) = p/6$. Exhaustive and exclusive: $p(1 + "
          "\\tfrac{1}{2} + \\tfrac{1}{6}) = 1$, so $p = 0.6$.", None),
    138: ("events", "The key&rsquo;s 0.25 is $P(A)P(B)$ with $P(A) = P(B) = \\tfrac{1}{2}$.",
          "As stated the answer is 1, not 0.25. Exhaustive means $P(A \\cup B) = 1$; with $P(A) = P(B) = p$ "
          "and independence, $2p - p^2 = 1$, so $p = 1$ and $P(A \\cap B) = 1$. Probabilities of "
          "$\\tfrac{1}{2}$ would need $A$ and $B$ to be mutually exclusive, and exclusive events with "
          "positive probability cannot be independent."),
    139: ("samplesize", "$n = \\left(\\dfrac{z\\sigma}{E}\\right)^2 = \\left(\\dfrac{1.96 \\times 5}{0.5}"
          "\\right)^2 = 19.6^2 = 384.16$, rounded up to 385.", None),
    140: ("sampling", "The key takes cluster sampling: the employees concerned are found together in "
          "particular units, which are then studied whole.",
          "Ethnographic work usually uses non-probability sampling &mdash; purposive or snowball &mdash; "
          "which is not offered. Cluster sampling is the key&rsquo;s choice among four probability "
          "methods, and the question gives no reason to prefer it to stratified sampling."),
    141: ("bayes", "$P(W) = \\tfrac{5}{9}$ and then B has 6 red in 10: $P(R \\mid W) = \\tfrac{6}{10}$. "
          "$P(R) = \\tfrac{4}{9}$ and then 7 red in 10. $P(W \\mid \\text{red}) = \\dfrac{\\frac{5}{9} "
          "\\cdot \\frac{6}{10}}{\\frac{5}{9} \\cdot \\frac{6}{10} + \\frac{4}{9} \\cdot \\frac{7}{10}} = "
          "\\dfrac{30}{58} = \\dfrac{15}{29}$.", None),
    142: ("pie", "Angle $= \\dfrac{30}{150} \\times 360° = 72°$.", None),
    143: ("ogive", "The less-than and more-than ogives cross where half the frequency lies on each side: "
          "at the median.", None),
    144: ("average", "AM $= 28/4 = 7$; GM $= (3 \\cdot 4 \\cdot 9 \\cdot 12)^{1/4} = 1296^{1/4} = 6$; HM "
          "$= 4 \\big/ \\left(\\tfrac{1}{3} + \\tfrac{1}{4} + \\tfrac{1}{9} + \\tfrac{1}{12}\\right) = "
          "\\dfrac{144}{28} = 5.14$.", None),
    145: ("qd", "In order: 7, 8, 8, 9, 10. $Q_1$ is the 1.5th value, 7.5, and $Q_3$ the 4.5th, 9.5. "
          "Coefficient $= \\dfrac{9.5 - 7.5}{9.5 + 7.5} = \\dfrac{2}{17}$.", None),
    146: ("skewness", "2, 3, 4, 5, 6 are symmetric about their mean 4, so every odd central moment is zero "
          "and the skewness is 0.", None),
    147: ("correlation", "$\\bar{x} = 5$, $\\bar{y} = 2.5$; $\\sum dx\\,dy = 4$, $\\sum dx^2 = 20$, $\\sum "
          "dy^2 = 5$. $r = \\dfrac{4}{\\sqrt{20 \\times 5}} = 0.40$.", None),
    148: ("pe", "PE $= 0.6745\\,\\dfrac{1 - r^2}{\\sqrt{n}} = 0.6745 \\times \\dfrac{0.36}{5} = 0.0486$.", None),
    149: ("sindex", "By simple averages: the quarter means are 4, 4.667, 6 and 4.333, with grand mean "
          "4.75. The second quarter&rsquo;s index is $4.667/4.75 \\times 100 = 98.3\\%$.", None),
    150: ("index", "$\\dfrac{\\sum p_1q_0}{\\sum p_0q_0} \\times 100 = \\dfrac{300 + 400 + 900}{400 + 350 + "
          "1200} \\times 100 = \\dfrac{1600}{1950} \\times 100 = 82.05\\%$.", None),
}
