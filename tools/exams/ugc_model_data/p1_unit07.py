# -*- coding: utf-8 -*-
"""UGC NET Paper I, Unit 7: fifty exam-standard model questions.

Twenty questions on data and their presentation, then six data sets with five
questions each. The data sets are invented for practice; DATA holds their
figures so that ugc_model_verify.py can recompute every answer from them.
"""
from . import AR, Q, ar, match, st

TITLE = "Data Interpretation"
BLURB = ("Sources and classification of data, scales of measurement, graphical representation, data and "
         "governance, and six data sets (tables, a pie chart given as percentages, and time series) with "
         "five questions on each.")

DATA = {
    "rice": {"years": [2021, 2022, 2023, 2024, 2025],
             "P": [40, 44, 50, 48, 60], "Q": [30, 36, 33, 45, 54], "R": [50, 55, 60, 66, 72], "S": [20, 25, 30, 36, 45]},
    "budget": {"total": 360, "Salaries": 40, "Research": 15, "Library": 10, "Infrastructure": 20,
               "Scholarships": 10, "Others": 5},
    "depts": {"Mathematics": (200, 40), "Physics": (150, 60), "Chemistry": (250, 52), "Statistics": (100, 45),
              "Economics": (300, 50)},
    "trade": {"years": [2020, 2021, 2022, 2023, 2024], "exports": [200, 240, 300, 360, 450],
              "imports": [250, 300, 330, 400, 420]},
    "marks": {"subjects": ["English", "Mathematics", "Science", "Social Science"],
              "A": [70, 80, 60, 90], "B": [60, 90, 75, 55], "C": [85, 65, 70, 80], "D": [50, 70, 90, 60],
              "E": [75, 85, 80, 70]},
    "sales": {"months": ["January", "February", "March", "April", "May", "June"],
              "X": [30, 36, 45, 40, 50, 54], "Y": [25, 30, 40, 44, 55, 66]},
}


def table(head, rows):
    return ('<div class="table-scroll"><table><tr>' + "".join("<th>%s</th>" % h for h in head) + "</tr>"
            + "".join("<tr>" + "".join("<td>%s</td>" % v for v in r) + "</tr>" for r in rows) + "</table></div>")


def S(n, first, intro, tab):
    return ("PASSAGE", "Data set %d (Questions %d&ndash;%d)" % (n, first, first + 4), "<p>%s</p>%s" % (intro, tab))


_r, _b, _d, _t, _m, _s = (DATA[k] for k in ("rice", "budget", "depts", "trade", "marks", "sales"))

QUESTIONS = [
 Q("A researcher interviews 300 shopkeepers about digital payments and also uses the monthly figures of "
   "digital transactions published by a bank. The two sets of data are, respectively:",
   ["secondary and primary", "primary and secondary", "both primary", "both secondary"], "B",
   "Data the investigator collects for the present purpose are primary; data collected by someone else for "
   "another purpose, such as published figures, are secondary.", "data"),

 Q("The difference between a questionnaire and a schedule is that:",
   ["a questionnaire has open questions and a schedule closed ones",
    "a questionnaire is used in a census and a schedule in a sample survey",
    "a questionnaire collects qualitative data and a schedule quantitative data",
    "a questionnaire is filled in by the respondent, and a schedule by the enumerator who asks the questions"], "D",
   "Both are lists of questions. The questionnaire is completed by the respondent, often by post or online; "
   "the schedule is completed by an enumerator in an interview, which suits respondents who cannot read or "
   "write.", "data"),

 Q("Match the table in List I with the basis of its classification in List II."
   + match(["Students by state of origin", "Enrolment in each year from 2015 to 2025",
            "Workers by religion", "Households by monthly income class"],
           ["Geographical", "Chronological", "Qualitative", "Quantitative"]),
   ["(a)-(i), (b)-(ii), (c)-(iii), (d)-(iv)", "(a)-(ii), (b)-(i), (c)-(iii), (d)-(iv)",
    "(a)-(i), (b)-(ii), (c)-(iv), (d)-(iii)", "(a)-(iii), (b)-(ii), (c)-(i), (d)-(iv)"], "A",
   "Classification by place is geographical, by time chronological, by an attribute (religion, sex) "
   "qualitative, and by the size of a variable (income classes) quantitative.", "data"),

 Q("Consider the statements:"
   + st("A census covers every unit of the population.",
        "A sample survey covers a part of the population chosen to represent it.",
        "Secondary data are always more accurate than primary data.",
        "Primary data are generally costlier and slower to collect than secondary data.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "I, II and IV only", "I, II, III and IV"], "C",
   "(III) is false: secondary data may not fit the purpose, and their definitions, coverage and accuracy "
   "have to be checked before use. The other three are correct.", "data"),

 Q(ar("Secondary data should be scrutinised before they are used.",
      "They were collected by another agency, for a different purpose, with its own definitions and methods."),
   AR, "A",
   "Because the user did not design the collection, the definitions, the coverage, the period and the "
   "accuracy may not suit the new purpose. Both statements are true and (R) is the reason.", "data"),

 Q("Which of the following is NOT a method of collecting primary data?",
   ["Direct personal interview", "Observation", "Mailed questionnaire",
    "Use of tables from a published census report"], "D",
   "Interview, observation, questionnaire, schedule and experiment produce primary data. Published reports, "
   "census tables, journals and administrative records are sources of secondary data.", "data"),

 Q("Match the scale of measurement in List I with the example in List II."
   + match(["Nominal", "Ordinal", "Interval", "Ratio"],
           ["Temperature in degrees Celsius", "Monthly income", "Blood group", "Rank in class"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "C",
   "Nominal: names without order. Ordinal: order without equal differences. Interval: equal differences but "
   "no true zero. Ratio: equal differences and a true zero.", "types"),

 Q("The statement &ldquo;40&deg;C is twice as hot as 20&deg;C&rdquo; is not meaningful because the Celsius "
   "scale is:",
   ["a nominal scale", "an interval scale, whose zero is arbitrary", "an ordinal scale",
    "a ratio scale"], "B",
   "Ratios make sense only on a ratio scale, which has a true zero. Zero on the Celsius scale is not an "
   "absence of heat, so differences are meaningful (40 is 20 degrees warmer) but ratios are not.", "types"),

 Q("Responses to an item are recorded as strongly disagree, disagree, neutral, agree, strongly agree. The "
   "most appropriate measure of central tendency is the:",
   ["median", "arithmetic mean", "geometric mean", "harmonic mean"], "A",
   "The responses are ordered, but the steps between them are not known to be equal: an ordinal scale. The "
   "median (and the mode) are meaningful; a mean of such codes is at best a convention.", "types"),

 Q("Consider the following variables:"
   + st("Number of children in a family", "Height of a student", "Number of road accidents in a month",
        "Time taken to finish a test")
   + "Which of them are discrete?",
   ["I and II only", "II and IV only", "I, II and III only", "I and III only"], "D",
   "Discrete variables are counts that take separate values: children, accidents. Height and time are "
   "measurements that can take any value in a range: continuous.", "types"),

 Q("Consider the statements about scales of measurement:"
   + st("The four scales were set out by S. S. Stevens.", "A ratio scale has a true zero.",
        "The mean is an appropriate average for nominal data.",
        "The mode can be found for data on any of the four scales.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "I, II and IV only", "I, II, III and IV"], "C",
   "Nominal data are categories without order or size, so they cannot be averaged by the mean; only the mode "
   "applies: (III) is false. The mode, the commonest value, can be found on every scale.", "types"),

 Q("Which statement about a histogram is correct?",
   ["Its bars are separated by gaps, and only their heights matter",
    "Its bars touch, and the area of each bar represents the frequency of its class",
    "It is used to compare categories such as states", "It shows the shares of a whole as sectors"], "B",
   "A histogram shows the distribution of a continuous variable: the bars touch, and area represents "
   "frequency, so classes of unequal width need adjusted heights. Separate bars for categories make a bar "
   "chart; sectors make a pie chart.", "graphs"),

 Q("In a pie chart, an item that accounts for 35% of the total is represented by a sector whose central "
   "angle is:",
   ["35&deg;", "63&deg;", "105&deg;", "126&deg;"], "D",
   r"The whole circle of $360^\circ$ stands for 100%, so each 1% takes $3.6^\circ$ and 35% takes "
   r"$35\times3.6=126^\circ$. The first option confuses the percentage with the angle.", "graphs"),

 Q("Match the purpose in List I with the most suitable chart in List II."
   + match(["Comparing categories", "Showing the distribution of a continuous variable",
            "Showing the shares of one whole", "Showing change over time"],
           ["Bar chart", "Histogram", "Pie chart", "Line chart"]),
   ["(a)-(i), (b)-(ii), (c)-(iii), (d)-(iv)", "(a)-(ii), (b)-(i), (c)-(iii), (d)-(iv)",
    "(a)-(i), (b)-(ii), (c)-(iv), (d)-(iii)", "(a)-(iv), (b)-(ii), (c)-(iii), (d)-(i)"], "A",
   "Bars compare categories; a histogram shows a distribution; a pie shows parts of a whole; a line chart "
   "shows a trend, its slope giving the rate of change.", "graphs"),

 Q("Which of the following graphs is used to locate the median and the quartiles of a frequency "
   "distribution?",
   ["Pie chart", "Bar chart", "Ogive", "Choropleth map"], "C",
   "An ogive is a cumulative frequency curve. Reading across from half (or a quarter, or three quarters) of "
   "the total frequency to the curve and down to the axis gives the median (or the quartiles).", "graphs"),

 Q("A map on which each district is shaded according to its literacy rate is called a:",
   ["dot map", "choropleth map", "proportional symbol map", "flow map"], "B",
   "A choropleth map shades areas by the value of a variable. A dot map places one dot for a fixed number of "
   "cases, and a proportional symbol map draws a circle whose size depends on the value.", "graphs"),

 Q("The National Data Sharing and Accessibility Policy (NDSAP), which provides for the open sharing of "
   "non-sensitive government data, was notified in:",
   ["2005", "2008", "2012", "2023"], "C",
   "The NDSAP was notified in 2012. 2008 is the year of the Collection of Statistics Act and 2023 that of the "
   "Digital Personal Data Protection Act.", "governance"),

 Q("The Open Government Data Platform India, data.gov.in, is run by the:",
   ["National Informatics Centre", "National Statistical Commission", "Reserve Bank of India",
    "Unique Identification Authority of India"], "A",
   "data.gov.in publishes the datasets that ministries and departments release under the NDSAP, and it is "
   "run by the National Informatics Centre.", "governance"),

 Q("Match the Act in List I with what it deals with in List II."
   + match(["Collection of Statistics Act, 2008", "Digital Personal Data Protection Act, 2023",
            "Aadhaar Act, 2016", "Census Act, 1948"],
           ["The decennial population census", "Collection of statistics by government and confidentiality of the information",
            "Processing of digital personal data, with consent", "A unique identity for the delivery of subsidies and benefits"]),
   ["(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)", "(a)-(iii), (b)-(ii), (c)-(iv), (d)-(i)",
    "(a)-(ii), (b)-(iii), (c)-(i), (d)-(iv)", "(a)-(ii), (b)-(iii), (c)-(iv), (d)-(i)"], "D",
   "The Collection of Statistics Act governs statistical collection and protects confidentiality; the DPDP "
   "Act governs digital personal data (consent, data fiduciaries, data principals, a Data Protection Board); "
   "the Aadhaar Act gives the identity used for Direct Benefit Transfer; the Census Act governs the census.", "governance"),

 Q("Consider the following as elements of good data governance:"
   + st("Data that are accurate, timely and consistent", "Protection of privacy and security",
        "Clear responsibility for each dataset",
        "Open publication of all data, including personal data, without restriction")
   + "Which of them are correct?",
   ["I and II only", "I, II and III only", "II, III and IV only", "I, II, III and IV"], "B",
   "Good governance of data means quality, access where it can be open, privacy and security where data must "
   "be protected, and accountability. Personal data are not to be published without restriction: (IV) is "
   "false.", "governance"),

 S(1, 21, "Production of rice (in lakh tonnes) in four states, P, Q, R and S, in five years.",
   table(["State"] + _r["years"], [[s] + _r[s] for s in "PQRS"])),

 Q("The total production of rice of the four states in 2023 was:",
   ["163 lakh tonnes", "170 lakh tonnes", "173 lakh tonnes", "183 lakh tonnes"], "C",
   r"Read down the column for 2023: P 50, Q 33, R 60 and S 30. Their sum is $50+33+60+30=173$ lakh tonnes.", "interpretation"),

 Q("The percentage increase in the production of State Q from 2024 to 2025 was:",
   ["20%", "16.7%", "25%", "9%"], "A",
   r"$\dfrac{54-45}{45}\times100=20\%$. The base is the earlier year, 45; dividing by 54 gives 16.7%, which is "
   r"wrong.", "interpretation"),

 Q("The average annual production of State R over the five years was:",
   ["60 lakh tonnes", "61.2 lakh tonnes", "59.4 lakh tonnes", "60.6 lakh tonnes"], "D",
   r"$\dfrac{50+55+60+66+72}{5}=\dfrac{303}{5}=60.6$ lakh tonnes.", "interpretation"),

 Q("The ratio of the production of State P in 2021 to that of State S in 2025 was:",
   ["2 : 1", "8 : 9", "9 : 8", "4 : 5"], "B",
   r"P produced 40 in 2021 and S produced 45 in 2025. The ratio $40:45$ reduces to $8:9$ on dividing both "
   r"terms by 5. The order matters: $9:8$ is the ratio the other way round.", "interpretation"),

 Q("The share of State S in the total production of the four states in 2025 was about:",
   ["18.2%", "23.4%", "19.5%", "22.5%"], "C",
   r"Total in 2025 $=60+54+72+45=231$. Share of S $=\dfrac{45}{231}\times100\approx19.5\%$.", "interpretation"),

 S(2, 26, "The expenditure of a university in a year was ₹360 crore. A pie chart shows its distribution "
          "under six heads, as the following percentages of the total.",
   table(["Head", "Share of expenditure"],
         [[h, "%d%%" % _b[h]] for h in ("Salaries", "Research", "Library", "Infrastructure", "Scholarships", "Others")])),

 Q("The central angle of the sector representing Research is:",
   ["15&deg;", "54&deg;", "36&deg;", "60&deg;"], "B",
   r"The whole circle is $360^\circ$, so each 1% is $3.6^\circ$ and Research, with 15%, takes "
   r"$15\times3.6=54^\circ$. The angle depends only on the percentage, not on the amount in rupees.", "graphs"),

 Q("The expenditure on Salaries was:",
   ["₹40 crore", "₹120 crore", "₹160 crore", "₹144 crore"], "D",
   r"Salaries take 40% of the total of ₹360 crore: $0.40\times360=144$, that is ₹144 crore. (₹40 crore would "
   r"be the answer only if the total were ₹100 crore.)", "interpretation"),

 Q("The expenditure on Infrastructure exceeded the expenditure on Library by:",
   ["₹36 crore", "₹10 crore", "₹72 crore", "₹18 crore"], "A",
   r"The difference of the shares is $20\%-10\%=10\%$ of ₹360 crore, which is ₹36 crore.", "interpretation"),

 Q("The ratio of the combined expenditure on Scholarships and Library to the expenditure on Salaries was:",
   ["1 : 4", "2 : 1", "1 : 2", "1 : 3"], "C",
   r"Since all are shares of the same total, compare the percentages: $(10+10):40=20:40=1:2$.", "interpretation"),

 Q("If the expenditure on Research is increased by 20% next year, it will become:",
   ["₹56.4 crore", "₹64.8 crore", "₹72 crore", "₹74 crore"], "B",
   r"Research now: $15\%$ of 360 $=54$ crore. Increased by 20%: $54\times1.2=64.8$, that is ₹64.8 crore. "
   r"(The increase is 20% of the research expenditure, not 20 percentage points of the budget.)", "interpretation"),

 S(3, 31, "The number of students enrolled in five departments of a college, and the percentage of them who "
          "are women.",
   table(["Department", "Students enrolled", "Women (% of enrolled)"],
         [[d, _d[d][0], "%d%%" % _d[d][1]] for d in _d])),

 Q("The number of women students in the Department of Chemistry is:",
   ["120", "125", "52", "130"], "D",
   r"Chemistry has 250 students, of whom 52% are women: $0.52\times250=130$. The remaining 120 are men.", "interpretation"),

 Q("The total number of men students in the five departments is:",
   ["505", "495", "500", "515"], "A",
   r"Women: $80+90+130+45+150=495$. Total enrolled: $200+150+250+100+300=1000$. Men: $1000-495=505$.", "interpretation"),

 Q("The percentage of women among all the students of the five departments is:",
   ["49.4%", "49.5%", "50%", "50.5%"], "B",
   r"$\dfrac{495}{1000}\times100=49.5\%$. It is not the simple average of the five percentages (49.4%), "
   r"because the departments differ in size.", "interpretation"),

 Q("The ratio of the number of men in Mathematics to the number of women in Physics is:",
   ["2 : 3", "3 : 4", "4 : 3", "8 : 9"], "C",
   r"Men in Mathematics: $60\%$ of 200 $=120$. Women in Physics: $60\%$ of 150 $=90$. Ratio $120:90=4:3$.", "interpretation"),

 Q("Which department has the largest number of men students?",
   ["Mathematics", "Chemistry", "Physics", "Economics"], "D",
   "Men: Mathematics 120, Physics 60, Chemistry 120, Statistics 55, Economics 150. Economics has the most, "
   "although its percentage of men (50%) is lower than that of Mathematics (60%).", "interpretation"),

 S(4, 36, "Exports and imports of a country (in thousand crore rupees) in five years.",
   table(["Year"] + _t["years"], [["Exports"] + _t["exports"], ["Imports"] + _t["imports"]])),

 Q("In which year was the trade deficit (imports minus exports) the largest?",
   ["2021", "2020", "2023", "2022"], "A",
   "The deficits are 50, 60, 30, 40 and &minus;30 (a surplus in 2024). The largest, 60, was in 2021.", "interpretation"),

 Q("The percentage increase in exports from 2020 to 2024 was:",
   ["225%", "55.6%", "125%", "250%"], "C",
   r"$\dfrac{450-200}{200}\times100=125\%$. Exports became 225% of their 2020 value, which is an increase of "
   r"125%, not of 225%.", "interpretation"),

 Q("The average annual value of imports over the five years was:",
   ["330 thousand crore rupees", "340 thousand crore rupees", "350 thousand crore rupees", "310 thousand crore rupees"], "B",
   r"$\dfrac{250+300+330+400+420}{5}=\dfrac{1700}{5}=340$.", "interpretation"),

 Q("The ratio of exports to imports in 2022 was:",
   ["11 : 10", "9 : 10", "5 : 6", "10 : 11"], "D",
   r"In 2022 exports were 300 and imports 330. The ratio $300:330$ reduces to $10:11$ on dividing both terms "
   r"by 30. Exports were smaller, so the first term of the ratio is the smaller one.", "interpretation"),

 Q("In how many of the five years were exports more than 85% of imports?",
   ["3", "2", "4", "5"], "A",
   r"Exports as a percentage of imports: 2020, 80%; 2021, 80%; 2022, 90.9%; 2023, 90%; 2024, 107.1%. The "
   r"figure exceeds 85% in three years: 2022, 2023 and 2024.", "interpretation"),

 S(5, 41, "Marks (out of 100 in each subject) obtained by five students, A to E, in four subjects.",
   table(["Student"] + _m["subjects"], [[s] + _m[s] for s in "ABCDE"])),

 Q("Which student obtained the highest total?",
   ["A", "C", "E", "B"], "C",
   "Totals: A 300, B 280, C 300, D 270, E 310. E has the highest total.", "interpretation"),

 Q("The average of the marks obtained by the five students in Mathematics is:",
   ["76", "80", "77", "78"], "D",
   r"$\dfrac{80+90+65+70+85}{5}=\dfrac{390}{5}=78$.", "interpretation"),

 Q("The percentage of marks obtained by student B in the four subjects taken together is:",
   ["75%", "70%", "72%", "68%"], "B",
   r"B's total is $60+90+75+55=280$. The maximum for four subjects is 400, so the percentage is "
   r"$\dfrac{280}{400}\times100=70\%$.", "interpretation"),

 Q("How many students scored more than 70 marks in Science?",
   ["3", "4", "2", "5"], "A",
   "The Science marks are 60, 75, 70, 90 and 80. Three of them (75, 90, 80) are more than 70; a score of "
   "exactly 70 is not &lsquo;more than 70&rsquo;.", "interpretation"),

 Q("The total of the marks of the five students in Social Science exceeds their total in English by:",
   ["10", "20", "15", "25"], "C",
   r"English: $70+60+85+50+75=340$. Social Science: $90+55+80+60+70=355$. Difference $=15$.", "interpretation"),

 S(6, 46, "Monthly sales (in thousands) of two-wheelers by two companies, X and Y, in the first six months of "
          "a year, as plotted on a line chart.",
   table(["Company"] + _s["months"], [["X"] + _s["X"], ["Y"] + _s["Y"]])),

 Q("The total sales of Company X in the six months were:",
   ["250 thousand", "255 thousand", "260 thousand", "265 thousand"], "B",
   r"Add the six monthly figures of Company X: $30+36+45+40+50+54=255$ thousand. (Company Y sold 260 thousand "
   r"in the same period.)", "interpretation"),

 Q("In which month did the sales of Company Y exceed those of Company X for the first time?",
   ["March", "May", "June", "April"], "D",
   "Y is below X in January (25 against 30), February (30 against 36) and March (40 against 45). In April Y "
   "sells 44 against X's 40: on the line chart the two lines cross between March and April.", "graphs"),

 Q("By what percentage did the sales of Company Y in June exceed those of Company X in June?",
   ["22.2%", "18.2%", "12%", "20%"], "A",
   r"$\dfrac{66-54}{54}\times100=22.2\%$. The base is X's sales, 54; dividing by 66 would give 18.2%, the "
   r"percentage by which X fell short of Y.", "interpretation"),

 Q("The average monthly sales of Company Y over the six months were about:",
   ["42.5 thousand", "44.0 thousand", "43.3 thousand", "45.0 thousand"], "C",
   r"$\dfrac{25+30+40+44+55+66}{6}=\dfrac{260}{6}\approx43.3$ thousand.", "interpretation"),

 Q("The ratio of the total sales of Company X to the total sales of Company Y in the six months was:",
   ["52 : 51", "51 : 52", "5 : 6", "17 : 18"], "B",
   r"The totals are 255 thousand for X and 260 thousand for Y. The ratio $255:260$ reduces to $51:52$ on "
   r"dividing both terms by 5.", "interpretation"),
]
