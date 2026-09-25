# -*- coding: utf-8 -*-
"""The worked solutions for the APPSC 2025 Paper-II, and where each is taught.

The questions, options and key are NOT here: they are read from the PDF by
pdftext_appsc_paper.py into appsc_paper_2025.json, and appsc_paper.py never
retypes them. This file holds only what the paper does not: for each
question, the syllabus topic it tests, the working, and -- where the paper
itself is loose -- a flag saying how.

TOPICS maps a topic to (syllabus item, the page on this site that teaches
it, a pattern that page's own text must contain). The pattern is checked
when the page is built, so a "Study this" link can never point at a page
that does not teach the thing. A topic whose page is None is one this site
does not teach yet; its questions say so instead of sending the reader
somewhere that would not help, and the page lists them together at the end.

Items are the ten of the Assistant Statistical Officer Paper-II syllabus, as
numbered on exams/appsc/assistant-statistical-officer.html.
"""

ITEMS = {
    1: ("Economic Concepts", "1-economic-concepts"),
    2: ("International Economics", "2-international-economics"),
    3: ("Indian Economics", "3-indian-economics"),
    4: ("Financial Accounting", "4-financial-accounting"),
    5: ("Basics of Computers", "5-basics-of-computers"),
    6: ("Introduction to Statistics", "6-introduction-to-statistics"),
    7: ("Measures of Central Tendency", "7-measures-of-central-tendency"),
    8: ("Measures of Dispersion and Skewness", "8-measures-of-dispersion-and-skewness"),
    9: ("Measure of Relation", "9-measure-of-relation"),
    10: ("Analysis of Time Series and Index Numbers", "10-analysis-of-time-series-and-index-numbers"),
}

# The four parts the page is laid out in, by syllabus item.
GROUPS = [
    ("economics", "Economics", (1, 2, 3)),
    ("accounting", "Financial Accounting", (4,)),
    ("statistics", "Statistics", (6, 7, 8, 9, 10)),
    ("computers", "Computers", (5,)),
]

ECO, FA, DS = "statistics/economics/", "statistics/financial-accounting/", "statistics/descriptive-statistics/"
AS, SM, CF = "statistics/applied-statistics/", "statistics/statistical-methods/", "data-science/computer-fundamentals/"

TOPICS = {
    # 1. Economic concepts
    "demand":      (1, ECO + "unit1.html", r"[Ee]lasticity"),
    "market":      (1, ECO + "unit1.html", r"[Pp]erfect(ly)? compet"),
    "value":       (1, None, None),                      # the labour theory of value
    "natinc":      (1, ECO + "unit2.html", r"[Nn]ational [Ii]ncome"),
    "consumption": (1, None, None),                      # MPC, APC and APS
    "interest":    (1, ECO + "unit1.html", r"[Ii]nterest"),
    "money":       (1, ECO + "unit3.html", r"[Dd]eferred payment"),
    "monetary":    (1, ECO + "unit3.html", r"Cash Reserve Ratio|CRR"),
    "qtm":         (1, ECO + "unit3.html", r"MV"),
    "inflation":   (1, ECO + "unit4.html", r"[Ii]nflation"),
    "budget":      (1, ECO + "unit4.html", r"[Bb]udget"),
    "natural-u":   (1, None, None),                      # the natural rate of unemployment
    # 2. International economics
    "trade":       (2, ECO + "unit5.html", r"[Ff]ree trade"),
    "protection":  (2, ECO + "unit5.html", r"[Pp]rotection"),
    "bop":         (2, ECO + "unit5.html", r"[Bb]alance of [Pp]ayments"),
    "exchange":    (2, ECO + "unit5.html", r"[Ee]xchange rate"),
    "ims":         (2, ECO + "unit5.html", r"Bretton"),
    "wb":          (2, ECO + "unit5.html", r"International Development Association"),
    "growth":      (2, ECO + "unit5.html", r"[Hh]uman capital"),
    # 3. Indian economics
    "population":  (3, AS + "unit4.html", r"[Pp]opulation"),
    "occupation":  (3, None, None),                      # occupational structure, population density
    "poverty":     (3, ECO + "unit6.html", r"[Pp]overty line"),
    "unemploy":    (3, ECO + "unit6.html", r"[Dd]isguised unemployment"),
    "inequality":  (3, ECO + "unit6.html", r"Lorenz"),
    "disparity":   (3, ECO + "unit6.html", r"[Rr]egional"),
    "planning":    (3, ECO + "unit6.html", r"1991"),
    "parallel":    (3, None, None),                      # the parallel economy
    "debt":        (3, ECO + "unit4.html", r"[Ee]xternal debt"),
    "welfare":     (3, None, None),                      # PDS, MSP, the PQLI
    # 4. Financial accounting
    "concepts":    (4, FA + "unit1.html", r"[Bb]usiness [Ee]ntity"),
    "moneymeas":   (4, FA + "unit1.html", r"[Mm]oney [Mm]easurement"),
    "equation":    (4, FA + "unit1.html", r"Assets\s*=\s*Liabilities"),
    "journal":     (4, FA + "unit2.html", r"[Jj]ournal"),
    "subsidiary":  (4, FA + "unit3.html", r"[Ss]ubsidiary"),
    "cashbook":    (4, FA + "unit3.html", r"[Cc]ash [Bb]ook"),
    "brs":         (4, FA + "unit4.html", r"[Pp]ass [Bb]ook"),
    "company":     (4, None, None),                      # the Companies Act, 2013
    # 5. Computers
    "memory":      (5, CF + "unit1.html", r"[Mm]emory"),
    "cache":       (5, CF + "unit2.html", r"[Cc]ache"),
    "binary":      (5, CF + "unit1.html", r"[Bb]inary"),
    "gates":       (5, None, None),                      # logic gates
    "dma":         (5, None, None),                      # direct memory access
    "excel":       (5, CF + "unit4.html", r"[Ff]ormula"),
    "excel-fill":  (5, CF + "unit5.html", r"Flash Fill"),
    "excel-use":   (5, None, None),                      # AutoFit, F2, leading zeros, deleting rows
    # 6. Introduction to statistics
    "data":        (6, DS + "unit1.html", r"[Pp]rimary data"),
    "census":      (6, DS + "unit1.html", r"[Cc]ensus"),
    "schedule":    (6, DS + "unit1.html", r"[Ss]chedule"),
    "frequency":   (6, DS + "unit2.html", r"[Ff]requency distributions?"),
    "diagrams":    (6, DS + "unit2.html", r"[Hh]istogram"),
    "sampling":    (6, "statistics/sampling-techniques/unit1.html", r"[Cc]luster"),
    "probability": (6, "statistics/theory-of-probability/unit1.html", r"[Dd]ice|die"),
    # 7. Central tendency
    "average":     (7, DS + "unit3.html", r"[Aa]rithmetic [Mm]ean"),
    "median":      (7, DS + "unit3.html", r"[Mm]edian"),
    "hm":          (7, DS + "unit3.html", r"[Hh]armonic"),
    "quartile":    (7, DS + "unit3.html", r"[Qq]uartile"),
    # 8. Dispersion, skewness, the normal distribution
    "dispersion":  (8, DS + "unit4.html", r"[Mm]ean [Dd]eviation"),
    "cv":          (8, DS + "unit4.html", r"[Cc]oefficient of [Vv]ariation"),
    "skewness":    (8, DS + "unit5.html", r"Bowley"),
    "normal":      (8, "statistics/theoretical-continuous-distributions/unit4.html", r"[Ss]ymmetric"),
    # 9. Correlation
    "correlation": (9, SM + "unit2.html", r"[Cc]orrelation"),
    "rank":        (9, SM + "unit2.html", r"[Rr]ank"),
    "pe":          (9, SM + "unit3.html", r"[Pp]robable [Ee]rror"),
    # 10. Time series and index numbers
    "ts":          (10, AS + "unit1.html", r"[Ss]ecular"),
    "trend":       (10, AS + "unit1.html", r"[Ll]east [Ss]quares"),
    "seasonal":    (10, AS + "unit2.html", r"[Rr]atio to [Mm]oving"),
    "index":       (10, AS + "unit3.html", r"Laspeyre"),
    "indextests":  (10, AS + "unit3.html", r"[Tt]ime [Rr]eversal"),
    "deflation":   (10, "statistics/applied-statistics-ii/unit2.html", r"[Dd]eflat"),
}

# n: (topic, working, flag or None). The working is HTML; mathematics in $...$.
SOLUTIONS = {
    1: ("monetary", "A higher CRR locks more of every deposit away with the RBI, so banks have less to lend "
        "(I follows). Less lending means less credit creation and so a <em>smaller</em> money supply, "
        "the opposite of II.", None),
    2: ("occupation", "The primary sector draws directly on natural resources &mdash; agriculture, fishing, "
        "forestry, mining. Secondary is manufacturing, tertiary is services, quaternary is knowledge work.", None),
    3: ("monetary", "CRR is the share of deposits banks must keep with the central bank (A-ii); expansionary "
        "policy raises the money supply (B-iii); open market operations are the buying and selling of "
        "government securities (C-i); and the central bank manages monetary policy (D-iv).", None),
    4: ("trade", "Specialisation, the spread of technology and a wider market are the gains from trade "
        "itself. Government spending on infrastructure is a budget decision, not something trade delivers.", None),
    5: ("disparity", "Disparity pulls people <em>from</em> villages to towns &mdash; hence crowded cities, strained "
        "urban services and migration. A move back to rural farm work is the reverse of what it causes.", None),
    6: ("trade", "A free trade area removes restrictions among its members (A), and countries join because "
        "both exporters and importers gain (R) &mdash; which is exactly why such zones exist.", None),
    7: ("poverty", "A is the definition of a poverty line. The headcount index is the share of people "
        "<em>below</em> the line, not above it, so B is false.", None),
    8: ("market", "Under perfect competition the market's demand and supply fix the price and every firm "
        "takes it as given (A). No single firm decides the price, so B is false.", None),
    9: ("growth", "Trade builds specialisation, productivity and market access over time; in an emergency "
        "what is needed is immediate relief, which aid provides and trade cannot.", None),
    10: ("growth", "Capital raises labour productivity and builds transport, communication, industry and "
         "farming. Consumer tastes and preferences are not something capital is needed to change.", None),
    11: ("ims", "An international monetary system is judged on what happens <em>between</em> nations: the flow "
         "of trade and investment and a fair division of the gains. How income is shared inside each "
         "country is a domestic matter, outside its reach.", None),
    12: ("budget", "A budget surplus means revenue exceeds outlays: tax collections are more than government "
         "spending plus transfer payments. The other options describe a deficit and its financing.", None),
    13: ("natinc", "National income counts the factor incomes of India's <em>normal residents</em>. An Australian "
         "citizen employed locally at the Indian embassy in Australia is a resident of Australia, so the "
         "salary is a factor payment to the rest of the world and is left out.", None),
    14: ("market", "Away from the equilibrium price, demand and supply differ: below it there is a shortage, "
         "above it a surplus. Every other option describes equilibrium itself.", None),
    15: ("demand", "Demand is elastic when $|E_d| &gt; 1$ &mdash; quantity responds more than proportionately to "
         "price. $E_d = 1$ is unit elastic, $E_d &lt; 1$ inelastic, $E_d = 0$ perfectly inelastic.", None),
    16: ("bop", "The balance of payments summarises all transactions with the rest of the world (1-B); the "
         "balance of trade is exports minus imports of goods (2-A); autonomous transactions are made for "
         "their own economic reasons, whatever the state of the BoP (3-C).", None),
    17: ("occupation", "Population density is people per unit of area, conventionally persons per square "
         "kilometre.", None),
    18: ("unemploy", "Disguised unemployment is more people on the land than the work needs (A-ii); India's "
         "largest share of workers is in the primary sector (B-i); the informal sector means no job "
         "security and unregulated work (C-iv); migration is labour moving for work (D-iii).", None),
    19: ("growth", "Retained earnings are profits kept instead of paid as dividend (A-ii); human capital is "
         "built by education and skills (B-i); equity financing raises money by selling shares (C-iv); "
         "physical capital is infrastructure and buildings (D-iii).", None),
    20: ("welfare", "The minimum support price guarantees farmers a floor price for their crop. The PDS "
         "serves consumers; globalisation and SEZs are not agricultural policies.", None),
    21: ("budget", "Fiscal policy is the government's taxing and spending. CRR, buying securities and the "
         "discount rate are all tools of the central bank &mdash; monetary policy.", None),
    22: ("planning", "The 1991 reforms followed a crisis of high inflation, a large fiscal deficit and a "
         "balance-of-payments deficit (not surplus), with weak public-sector performance.", None),
    23: ("disparity", "Urban-only industry, poor farm land and natural endowments all widen regional gaps. A "
         "uniform education system across regions would narrow them, not widen them.", None),
    24: ("debt", "Options 1&ndash;3 are uses of external borrowing. Its cost is dependence on foreign lenders, "
         "which can compromise a country's freedom of policy.", None),
    25: ("growth", "Adam Smith's point: a larger market allows finer division of labour, which raises "
         "productivity (A). Producing more with the same labour is what higher productivity means (B).", None),
    26: ("inflation", "Central banks tighten &mdash; contractionary policy &mdash; to curb inflation (A). Inflation is a "
         "rise in the <em>general</em> price level, measured with an index over many goods; one good's price "
         "change is not inflation (B is false).", None),
    27: ("consumption", "MPC is the change in consumption per change in income (A-ii); $APC + APS = 1$ (B-i); gross "
         "investment is net investment plus depreciation (C-iv); which leaves D-iii.", None),
    28: ("demand", "Tea and coffee are substitutes: when coffee's price rises, tea's demand rises (A). For "
         "substitutes the cross-price elasticity is positive (R), which is the reason A holds.", None),
    29: ("growth", "Human capital is the skill and knowledge in the workforce; building it means the same "
         "workers can produce more.", None),
    30: ("wb", "The IDA is the World Bank's arm for the poorest countries, lending on concessional terms to "
         "reduce poverty. Balance-of-payments support is the IMF's role.", None),
    31: ("bop", "Anything that brings foreign exchange in is a credit: exports, and financial inflows. "
         "Imports, outflows and transfers paid abroad are debits.", None),
    32: ("protection", "Protecting infant industries, domestic labour and the balance of payments are classic "
         "arguments for protection. Tariffs raise domestic prices, so controlling inflation is not one.", None),
    33: ("inflation", "By the Fisher relation, inflation is approximately the nominal rate <em>minus</em> the real "
         "rate (option 1 is true); option 2 is the definition. Dividing the nominal rate by the real rate "
         "(option 4) has no meaning.", None),
    34: ("qtm", "In $MV = PY$, with $V$ constant a rise in $M$ must raise $PY$ &mdash; nominal GDP.", None),
    35: ("natural-u", "The natural rate is the unemployment that remains when the economy is at full "
         "employment: frictional plus structural. Cyclical unemployment is what it excludes.", None),
    36: ("planning", "Rapid growth of services supports I. Nothing in the statement says manufacturing and "
         "agriculture no longer matter, so II does not follow.", None),
    37: ("market", "Equilibrium is where market supply meets market demand (A), and it is the interaction of "
         "those two forces that sets the price (R), which explains A.", None),
    38: ("market", "A competitive firm is too small to affect the price; it sells at the price the market "
         "sets &mdash; a price taker.", None),
    39: ("parallel", "Lost tax revenue, corruption and inflationary unrecorded money are the harms of a "
         "parallel economy. Informal jobs are, if anything, a side benefit, not a harm.", None),
    40: ("welfare", "The Public Distribution System supplies food grains to poor households at subsidised "
         "prices; food security is its purpose.", None),
    41: ("inequality", "Inequality often rises in early industrial growth (Kuznets), and the Lorenz curve "
         "measures income distribution &mdash; both true. India has many kinds of inequality, not only "
         "regional, so the third is false: two statements.", None),
    42: ("interest", "The nominal rate is the promised rate on the bond (A-iii); the inflation-adjusted rate "
         "is the real rate (B-iv); profit is the reward of the entrepreneur (C-i); and profit is one "
         "component of income-method GDP (D-ii).", None),
    43: ("welfare", "The PQLI combines life expectancy, infant mortality and literacy. It deliberately leaves "
         "out income, which is exactly what it was built to look past.", None),
    44: ("value", "The labour theory of value (Ricardo, Marx) holds that a good's value is the labour "
         "embodied in it, setting capital aside.", None),
    45: ("ims", "Triffin's diagnosis of Bretton Woods: the linked problems of <em>liquidity</em>, "
         "<em>adjustment</em> and <em>confidence</em>.", None),
    46: ("exchange", "Under a flexible rate a deficit is corrected by the market fall of the currency &mdash; "
         "depreciation. Devaluation is the deliberate cut made under a fixed rate.", None),
    47: ("money", "Repaying a loan over 25 years uses money as the standard of deferred payments &mdash; a unit "
         "for debts settled in the future.", None),
    48: ("natinc", "Consumption of fixed capital is depreciation, the wearing out of capital goods. It is "
         "deducted to go from gross to net; it is not household consumption.", None),
    49: ("consumption", "Income after tax $= 5{,}000 - 10\\% \\times 5{,}000 = 4{,}500$. Spending $= 4{,}500 - 400 = "
         "4{,}100$.", None),
    50: ("company", "Section 128 requires books on the accrual basis and double entry (A-4); Section 129 "
         "requires the Board to lay financial statements before the AGM (B-2); Schedule III's format "
         "applies to companies not governed by special acts (C-3); notified accounting standards are "
         "mandatory (D-1).", None),
    51: ("subsidiary", "Splitting the journal into subsidiary books lets different clerks record different "
         "kinds of transaction at once, faster and more specialised.", None),
    52: ("journal", "The journal is the book of original entry; the ledger is posted from it.", None),
    53: ("concepts", "The business entity concept keeps the business and its owner apart in the accounts; "
         "the owner's capital is a liability of the business.", None),
    54: ("equation", "What the business owns is financed by what it owes to outsiders and to its owner: "
         "Assets = Liabilities + Owner's Equity.", None),
    55: ("brs", "A deposit is a debit in the customer's cash book but a credit in the bank's pass book, "
         "because to the bank it is money owed to the customer.", None),
    56: ("concepts", "The cost concept records assets at what was paid for them: relevant, objective "
         "(evidenced by documents) and feasible to apply.", None),
    57: ("equation", "Liabilities are what the business owes to others.", None),
    58: ("journal", "Journal: first book of original entry (A-2); ledger: the source of the trial balance "
         "(B-4); narration: the brief explanation (C-3); classification: grouping like transactions (D-1).", None),
    59: ("company", "Section 128 of the Companies Act, 2013 requires books of account to be kept at the "
         "registered office (or another place in India the Board decides and notifies).", None),
    60: ("cashbook", "The cash book follows the rule for a cash account: receipts on the debit side, payments "
         "on the credit side.", None),
    61: ("concepts", "A transaction is an event that can be measured in money and changes the business's "
         "position. Every transaction is an event; many events are not transactions.", None),
    62: ("moneymeas", "Money measurement: only what can be expressed in a unit of currency is recorded.", None),
    63: ("dispersion", "Range = largest &minus; smallest $= 12.2 - 5.8 = 6.4$.", None),
    64: ("seasonal", "Ratio to moving average is the most widely used method (A), and it is because it removes "
         "trend and cycle from the seasonal indices (R) that it is preferred.", None),
    65: ("index", "The other options are either false (formulas have no error) or advantages. Index numbers "
         "can be manipulated by choice of base, items and weights &mdash; a real limitation.", None),
    66: ("index", "Fisher's index is the geometric mean of Laspeyres and Paasche: "
         "$\\sqrt{120.69 \\times 120.62} = 120.65$.", None),
    67: ("index", "Consumer price indices are used for wage policy &mdash; dearness allowance is fixed by them. "
         "The other three are genuine limitations.", None),
    68: ("normal", "The normal distribution is symmetric (1-III); its mean equals its mode (2-I); its "
         "quartile deviation is about two-thirds of the standard deviation, $0.6745\\sigma$ (3-IV); and it "
         "is unimodal (4-II).", "The option prints &ldquo;I- III&rdquo; for &ldquo;1-III&rdquo;."),
    69: ("cv", "Standard deviation is an absolute measure of dispersion (1-III); the coefficient of "
         "variation compares consistency, such as two batsmen's scores (2-IV); dispersion is variability "
         "(3-I); range is highest minus lowest (4-II).", "The option prints &ldquo;I- III&rdquo; for &ldquo;1-III&rdquo;."),
    70: ("average", "The mean is pulled by extreme values (A is true) precisely <em>because</em> it uses every "
         "observation, so R, which says it does not, is false.", None),
    71: ("frequency", "All three are standard: a frequency distribution tabulates data by class; an open class "
         "lacks a lower or an upper limit; grouping summarises a large mass of data.", None),
    72: ("data", "Primary data come from surveys or experiments; a questionnaire is pilot-tested first; and "
         "when schedules or questionnaires are administered, enumerators are appointed and trained.", None),
    73: ("correlation", "A family's expenditure rises with its income (positive); newborns' weight rises "
         "strongly with age (high positive); in very old age weight tends to fall with age (negative).", None),
    74: ("cv", "$CV = \\dfrac{\\sigma}{\\bar x} \\times 100 = \\dfrac{3}{12} \\times 100 = 25$.", None),
    75: ("median", "In order: 30, 35, 40, 49, 50, 52, 55, 65, 76, 225. With ten values the median is the mean "
         "of the 5th and 6th: $(50 + 52)/2 = 51$. The outlier 225 does not move it.", None),
    76: ("average", "$\\bar x = \\dfrac{5 \\cdot 3 + 8 \\cdot 2 + 6 \\cdot 4 + 2 \\cdot 1}{3 + 2 + 4 + 1} = \\dfrac{57}{10} = 5.7$.", None),
    77: ("diagrams", "Shares of one total across sectors are shown as the slices of a pie chart.", None),
    78: ("data", "Biographies, newspapers and magazines report what others collected. An autobiography is the "
         "writer's own first-hand account, so it is treated as primary.", None),
    79: ("census", "The census office collects its data directly from every household: for it, census data "
         "are primary. (Anyone else using the published tables is using secondary data.)", None),
    80: ("correlation", "$r = -1$ is perfect <em>negative</em> correlation, so the assertion can hold but the reason "
         "(perfect positive) is wrong.", None),
    81: ("correlation", "$-1 \\le r \\le 1$, so $r$ cannot exceed 1.", None),
    82: ("correlation", "$|r|$ gives the strength and the sign gives the direction of a linear relationship.", None),
    83: ("correlation", "Past 70, weight tends to fall as age rises: a negative correlation.", None),
    84: ("dispersion", "Mean $= 30/5 = 6$; deviations 4, 3, 1, 3, 5 give MD $= 16/5 = 3.2$. Median $= 5$; deviations "
         "3, 2, 0, 4, 6 give MD $= 15/5 = 3$. It is smaller about the median because mean deviation is least "
         "about the median, which is R.", "The options say &ldquo;Both A and B&rdquo;; they mean A and R."),
    85: ("hm", "Equal numbers of each document means equal <em>output</em>, so the right average of rates is the "
         "harmonic mean: $\\dfrac{3}{\\frac{1}{50} + \\frac{1}{40} + \\frac{1}{80}} = \\dfrac{3}{0.0575} \\approx 52$.", None),
    86: ("diagrams", "Bar diagram: rectangles for one-dimensional comparison (A-ii); histogram: grouped data with "
         "continuous classes (B-i); line graph: points and lines over time (C-iv); pie chart: a circle "
         "(D-iii).", None),
    87: ("indextests", "Irving Fisher proposed the time reversal (and factor reversal) tests, so A is true; his "
         "ideal index does satisfy the factor reversal test, so R is true &mdash; but R does not explain who "
         "proposed the test.", "The options say &ldquo;Both A and B&rdquo;; they mean A and R."),
    88: ("deflation", "Real wage $= \\dfrac{138.10}{149.8} \\times 100 = 92.19$.", None),
    89: ("ts", "A time series exists because the value changes over time; a variable that did not change "
         "would have nothing to analyse.", None),
    90: ("frequency", "The class mark is $(\\text{lower} + \\text{upper})/2$ (A), and class boundaries make "
         "classes continuous (R). Both are true, but R is not why the class mark is computed that way.", None),
    91: ("schedule", "Enumerators' work is field-checked, and they explain the enquiry to respondents &mdash; 1 and "
         "2 are true. A questionnaire is filled by the respondent, not by an investigator, so 3 is false.", None),
    92: ("ts", "Planning, forecasting and understanding the past are the uses of time series analysis. It is "
         "by definition about time-dependent data, so option 2 is not a utility.", None),
    93: ("schedule", "Schedules suit illiterate informants, get few non-responses and give more reliable "
         "answers &mdash; but paying trained enumerators makes them costly, not cost-effective.", None),
    94: ("seasonal", "Ratio to trend, ratio to moving average and link relatives measure seasonal variation. "
         "Least squares fits the trend.", None),
    95: ("trend", "That is what &ldquo;least squares&rdquo; means: the fitted line makes the sum of squared "
         "deviations as small as possible.", None),
    96: ("skewness", "Bowley's coefficient lies between $-1$ and $1$ (1-IV); Pearson's measure is built on "
         "mean minus median (2-I); negative skewness has mean &lt; median &lt; mode (3-II); kurtosis is "
         "peakedness (4-III).",
         "Pearson's coefficient is usually written $3(\\text{Mean} - \\text{Median})/\\sigma$ or "
         "$(\\text{Mean} - \\text{Mode})/\\sigma$; the paper drops the 3. The match still holds."),
    97: ("hm", "$n = 11$, sum $= 80$, so the mean is $7.27$ (1-IV). The mode is 9 (2-III). The 6th value in "
         "order is 8, the median (3-II). HM $= 11 / \\sum \\frac{1}{x} = 11/1.909 = 5.76$ (4-I).", None),
    98: ("diagrams", "Multiple bars compare two or more variables (1-IV); a pie shows a total as a circle "
         "(2-III); a line diagram shows time series such as temperature or rainfall (3-II); a frequency "
         "polygon joins the mid-points of a histogram's tops (4-I).", None),
    99: ("quartile", "$Q_2$ is the median by definition. It equals the mean only for a symmetric distribution, "
         "and never equals $Q_1$ in general.", None),
    100: ("normal", "The normal curve is symmetric, so its coefficient of skewness is zero.", None),
    101: ("skewness", "Negative skewness puts the long tail on the left, which pulls the mean below the mode.", None),
    102: ("skewness", "Bowley's $S_k = \\dfrac{Q_3 + Q_1 - 2Q_2}{Q_3 - Q_1} = \\dfrac{168.45 + 160.95 - 329.52}{7.50} "
          "= \\dfrac{-0.12}{7.50} = -0.016$: negative, if only just.", None),
    103: ("average", "A central value represents the data and is where they cluster; variability is what "
          "measures of dispersion describe, not central tendency.", None),
    104: ("census", "India's first (non-synchronous) census was taken in 1872, not 1862; the first synchronous "
          "census was 1881.", None),
    105: ("diagrams", "With equal class widths every rectangle has the same base, so its height is "
          "proportional to its frequency.", None),
    106: ("probability", "There are $6^3 = 216$ equally likely outcomes, of which 6 show the same number on "
          "all three dice: $6/216 = 1/36$.", None),
    107: ("sampling", "Cluster sampling selects whole clusters at random, so each unit has a known chance. "
          "Judgement and convenience sampling are non-probability methods.", None),
    108: ("correlation", "Independence gives zero covariance and so $r = 0$ (I). The converse fails: $r$ "
          "measures only <em>linear</em> association, and $Y = X^2$ with symmetric $X$ has $r = 0$ yet is "
          "fully dependent (II is false).", None),
    109: ("rank", "With $n = 4$: $0.5 = 1 - \\dfrac{6\\sum d^2}{4 \\cdot 15}$ gives $\\sum d^2 = 5$. Correcting "
          "one $d$ from 1 to 2 adds $4 - 1 = 3$, so $\\sum d^2 = 8$ and "
          "$R = 1 - \\dfrac{48}{60} = \\dfrac{1}{5}$.", None),
    110: ("pe", "$PE = 0.6745 \\, \\dfrac{1 - r^2}{\\sqrt n} = 0.6745 \\times \\dfrac{0.36}{4} = 0.061 \\approx 0.06$.", None),
    111: ("correlation", "$r = \\dfrac{\\mathrm{Cov}(X,Y)}{\\sigma_X \\sigma_Y} = \\dfrac{-16.5}{1.7 \\times 10} = -0.97$.", None),
    112: ("correlation", "Correlation is unchanged by a change of origin and by a change of scale with a "
          "positive factor: $r_{UV} = r_{XY}$.",
          "The options are printed as multiples of r(U,V), which would make the question circular; "
          "r(X,Y) is clearly meant, and option 4 is then the answer."),
    113: ("dispersion", "Adding 3 moves every value and the mean alike; multiplying by 2 doubles every "
          "deviation: $MD_Y = 2 \\times 5 = 10$.", None),
    114: ("median", "The median needs only the cumulative frequencies up to its class, and the mode only its "
          "own and neighbouring classes, so both survive open end classes. Both are true, but one does not "
          "explain the other.", None),
    115: ("average", "The mean of 1 to 10 is 5.5 (1 false). Subtracting 3 lowers the mean by 3 (2 false). "
          "Multiplying by a constant multiplies the median too (3 true).", None),
    116: ("quartile", "$N = 40$, so $Q_3$ is the 30th value. Cumulative frequencies: 3, 11, 24, 36, 40 &mdash; the "
          "75&ndash;80 class. $Q_3 = 75 + \\dfrac{30 - 24}{12} \\times 5 = 77.5$.", None),
    117: ("rank", "Completely reversed ranks give $R = -1$ (1 true). Rank correlation is designed for "
          "qualitative, rankable characteristics (2 false). With two individuals $\\sum d^2$ is 0 or 2, so "
          "$R$ is $1$ or $-1$ (3 true).", None),
    118: ("index", "A quantity index measures change in quantities, such as a factory's output (1-III); the "
          "Index of Industrial Production is compiled by the CSO, MoSPI (2-IV); change in total monetary "
          "worth is a value index (3-I); $\\sum p_1 q_1 / \\sum p_1 q_0$ is Paasche's quantity index (4-II).", None),
    119: ("trend", "Moving averages smooth out the short-term swings to reveal the trend. The other three "
          "are methods for seasonal variation.", None),
    120: ("diagrams", "A frequency polygon can be drawn for unequal classes too, once the heights are adjusted "
          "for class width; the other three statements are true.", None),
    121: ("probability", "The addition theorem: $P(A \\cup B) = P(A) + P(B) - P(AB)$, subtracting the overlap "
          "counted twice. Option 1 holds only for mutually exclusive events.", None),
    122: ("schedule", "Short, simple, logical, with sensitive questions last &mdash; all good practice. Open-ended "
          "answers are <em>hard</em> to tabulate and analyse, so option 4 is not true.", None),
    123: ("ts", "Secular trend: the rising trend of population; seasonal: variation within a year; cyclical: "
          "long-period fluctuations; irregular: isolated special occurrences.", None),
    124: ("correlation", "A scatter diagram gives a rough idea of correlation between two variables (i-iii); "
          "a matrix plot does so among several (ii-iv); Pearson's $r$ measures it without ranking (iii-ii); "
          "Spearman's rank correlation cannot be used on a grouped frequency distribution (iv-i).", None),
    125: ("ts", "Seasonal variation repeats within a year (I), and winter demand for woollens is a textbook "
          "example (II).", None),
    126: ("trend", "The annual figure is spread over 12 months, so the constant becomes $30/12 = 2.5$. The "
          "slope is per year of annual sales; per month of monthly sales it is divided by $12 \\times 12$: "
          "$3.6/144 = 0.025$.", None),
    127: ("trend", "Seven years, so take $X = -3, \\dots, 3$ with 1944 as origin; $\\sum X = 0$ and "
          "$\\sum X^2 = 28$. $\\sum XY = -240 - 180 - 92 + 0 + 94 + 198 + 276 = 56$, so the slope "
          "$b = 56/28 = 2$.", None),
    128: ("normal", "The normal distribution is symmetric, so mean, median and mode coincide, every odd-order "
          "central moment vanishes, and the skewness is zero.", None),
    129: ("skewness", "Bowley's measure lies between $-1$ and $1$ (2). Pearson's $3(\\text{Mean} - \\text{Median})/\\sigma$ "
          "lies between $-3$ and $3$ (3). The key counts these two.",
          "Whether statement 1 is false depends on which Pearson coefficient is meant: "
          "$(\\text{Mean} - \\text{Mode})/\\sigma$ has no fixed bound. The key follows the usual textbook "
          "reading, $\\pm 3$."),
    130: ("dispersion", "Mean $= 8457/7 = 1208.14$. Absolute deviations 7.86, 41.14, 23.86, 6.14, 69.86, "
          "67.14, 12.86 sum to 228.86, so MD $= 228.86/7 = 32.69$.", None),
    131: ("average", "Total $= 6 \\times 119 = 714$ kg; the five known bags weigh 584 kg; the sixth is "
          "$714 - 584 = 130$ kg.", None),
    132: ("schedule", "With schedules the enumerator asks the questions and records the answers, so the "
          "quality of the data depends heavily on the enumerator.", None),
    133: ("correlation", "$\\mathrm{Cov}(X, X^2) = E(X^3) - E(X)E(X^2) = 0 - 0 = 0$, since the odd moments of "
          "$N(0,1)$ vanish; so $r = 0$ although $Y$ is a function of $X$.", None),
    134: ("pe", "The usual limits are $r \\pm PE$: $PE = 0.6745 \\times \\dfrac{1 - 0.49}{5} = 0.069$, giving "
          "0.631 and 0.769 &mdash; which is none of the four options.",
          "The Commission withdrew this question: the paper notes &ldquo;discrepancy is found in "
          "question/answer&rdquo; and that it &ldquo;is ignored for all candidates&rdquo;. No option is marked."),
    135: ("correlation", "$\\mathrm{Var}(Z) = \\mathrm{Var}(X) + 4\\mathrm{Var}(Y)$ $+\\, 4\\mathrm{Cov}(X,Y)$, so "
          "$4 = 4 + 12 + 4\\mathrm{Cov}$, so $\\mathrm{Cov} = -3$ and $r = \\dfrac{-3}{2\\sqrt3} = -\\dfrac{\\sqrt3}{2}$.", None),
    136: ("gates", "OR gives 1 if any input is 1; with both inputs 0 it gives 0.", None),
    137: ("gates", "$0 \\text{ OR } 1 = 1$, and NOT 1 $= 0$.", None),
    138: ("gates", "NAND is NOT-AND: AND gives 1 only when both inputs are 1, so NAND gives 0 only then and 1 "
          "otherwise.", None),
    139: ("binary", "In two's complement the most significant bit carries a negative weight, so an MSB of 1 "
          "always means a negative number (I). Subtraction becomes addition of the complement, so the "
          "same adder serves both (II).", None),
    140: ("gates", "NOR is NOT-OR: its output is HIGH only when both inputs are LOW.", None),
    141: ("excel-use", "Double-clicking the column header's right border autofits the column to its widest "
          "entry.", None),
    142: ("excel", "MAX returns the largest number in a range; LARGE needs a rank as well; MIN and AVERAGE do "
          "other jobs.", None),
    143: ("excel", "Inserting a row pushes the rows below down and formulas follow their cells (A). The "
          "reason as worded is taken as false: the $ in an absolute reference exists to stop it changing "
          "when a formula is copied.",
          "In practice Excel does renumber absolute references that point at rows which have moved "
          "(<code>$A$10</code> becomes <code>$A$11</code>), so R is arguably true; the key treats it as false."),
    144: ("excel-use", "F2 opens the cell for editing with the cursor at the end of the existing content; "
          "typing straight into a selected cell replaces it.", None),
    145: ("excel-use", "Select non-adjacent rows with Ctrl-click, then Delete: Excel removes them all at once.", None),
    146: ("cache", "Cache is a small, fast memory between the processor and RAM that holds frequently used "
          "data, cutting the average access time.", None),
    147: ("dma", "DMA frees the CPU during the transfer (I follows). The CPU still sets the transfer up and is "
          "told when it ends, so &ldquo;never involved&rdquo; (II) does not follow.", None),
    148: ("excel-fill", "Flash Fill spots patterns (2-B) and a growth series multiplies by a step (3-C); "
          "option 1 is the only one with both.",
          "Strictly, a linear series is the fixed-step sequence (D) and the fill handle is the tool that "
          "extends any sequence; no option pairs them that way, so option 1 is the intended answer."),
    149: ("excel-use", "A General-format cell treats 00789 as the number 789 and drops the zeros; to keep "
          "them, format the cell as Text or type a leading apostrophe.", None),
    150: ("memory", "ROM is read-only in normal operation; the other three statements about cache, virtual "
          "memory and SRAM are true.", None),
}
