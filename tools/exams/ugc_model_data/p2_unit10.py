# -*- coding: utf-8 -*-
"""UGC NET Statistics, Unit X: fifty exam-standard model questions.

R code is written inside <code> or <pre>, where MathJax does not look: the
assignment arrow is &lt;- and a dollar sign is &#36;.
"""
from . import AR, Q, ar, match, st

TITLE = "Indian Statistical System and Research Methodology"
BLURB = ("The Ministry of Statistics and Programme Implementation, the National Statistical Commission and "
         "Office, the census and the large sample surveys, the contributions of Indian statisticians, and "
         "computing with R and typesetting with LaTeX.")


def c(s):
    return "<code>%s</code>" % s


def pre(s):
    return "<pre>%s</pre>" % s


QUESTIONS = [
 Q("The Ministry of Statistics and Programme Implementation (MoSPI) came into being as an independent ministry, "
   "by the merger of the Department of Statistics and the Department of Programme Implementation, in:",
   ["1947", "1999", "2005", "2019"], "B",
   "MoSPI was formed in 1999 by merging the Department of Statistics and the Department of Programme "
   "Implementation. 2005 is the year the National Statistical Commission was constituted, and 2019 the year the "
   "National Statistical Office was formed by merging the CSO and the NSSO.", "mospi"),

 Q("Which of the following is NOT monitored by the Programme Implementation Wing of MoSPI?",
   ["The Twenty Point Programme", "Central sector infrastructure projects",
    "The Members of Parliament Local Area Development Scheme (MPLADS)", "The decennial Census of India"], "D",
   "The Programme Implementation Wing monitors the Twenty Point Programme, infrastructure projects and MPLADS. "
   "The Census of India is conducted by the Office of the Registrar General and Census Commissioner, which is "
   "under the Ministry of Home Affairs, not MoSPI.", "mospi"),

 Q("The Annual Survey of Industries (ASI), the principal source of industrial statistics in India, is conducted "
   "under the:",
   ["Collection of Statistics Act, 2008", "Census Act, 1948", "Factories Act, 1948", "Industrial Disputes Act, 1947"], "A",
   "The ASI is conducted under the Collection of Statistics Act, 2008. Its coverage is defined by the Factories "
   "Act, 1948 (factories registered under sections 2(m)(i) and 2(m)(ii)), but that Act is not the authority under "
   "which the survey is taken. The Census Act, 1948 governs the population census.", "mospi"),

 Q("Match the official statistical output in List I with what it measures in List II."
   + match(["Index of Industrial Production (IIP)", "Consumer Price Index (CPI)",
            "Periodic Labour Force Survey (PLFS)", "Annual Survey of Industries (ASI)"],
           ["Employment and unemployment indicators", "Annual data on registered factories",
            "Short-term changes in the volume of industrial output", "Changes in retail prices paid by households"]),
   ["(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)", "(a)-(ii), (b)-(iv), (c)-(i), (d)-(iii)",
    "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)"], "C",
   "The IIP tracks the volume of industrial production month by month; the CPI measures retail price change and "
   "is the measure of inflation; the PLFS gives the labour force participation rate, worker population ratio "
   "and unemployment rate; the ASI gives detailed annual data on registered factories.", "mospi"),

 Q("The National Statistical Commission (NSC) was constituted in 2005 on the recommendation of the commission "
   "chaired by:",
   ["P. C. Mahalanobis", "C. Rangarajan", "Suresh Tendulkar", "C. R. Rao"], "B",
   "The Rangarajan Commission (which reported in 2001) reviewed the Indian statistical system and recommended a "
   "permanent apex body; the NSC was set up in 2005 to evolve policies, priorities and standards for official "
   "statistics.", "nsc"),

 Q("The Secretary (Member-Secretary) of the National Statistical Commission is the:",
   ["Chief Statistician of India", "Chief Executive Officer of NITI Aayog", "Registrar General of India",
    "Governor of the Reserve Bank of India"], "A",
   "The NSC has a Chairperson, four Members, the Chief Executive Officer of NITI Aayog as an ex-officio Member, "
   "and the Chief Statistician of India, who is the Secretary of MoSPI, as its Secretary.", "nsc"),

 Q("Consider the following about the National Statistical Commission:"
   + st("It identifies the core statistics that are of national importance.",
        "It lays down national quality standards for official statistics.",
        "It conducts the decennial population census.",
        "It coordinates the statistical activities of central and state agencies.")
   + "Which of these are functions of the Commission?",
   ["I and II only", "II and III only", "I, II, III and IV", "I, II and IV only"], "D",
   "The NSC is a policy and standards body: it identifies core statistics, sets quality standards, coordinates "
   "agencies and monitors major surveys. It does not collect data itself; the census is conducted by the "
   "Registrar General and Census Commissioner under the Ministry of Home Affairs.", "nsc"),

 Q(ar("The National Statistical Commission advises on matters such as the revision of the base year of the "
      "national accounts and of price indices.",
      "The Commission was set up to evolve policies, priorities and standards for the Indian statistical system."),
   AR, "A",
   "Choosing and revising base years is a question of statistical policy and standards, which is exactly the "
   "Commission's mandate. Both statements are true and (R) explains (A). The compilation itself is done by the "
   "National Statistical Office.", "nsc"),

 Q("The National Statistical Office (NSO) was formed by merging the Central Statistics Office (CSO) and the "
   "National Sample Survey Office (NSSO) in:",
   ["1950", "1999", "2019", "2005"], "C",
   "The CSO and the NSSO were brought together as the NSO in 2019, to streamline the system under MoSPI. 1950 is "
   "the year the National Sample Survey began; 1999 and 2005 are the years of MoSPI and of the NSC.", "nso"),

 Q("Within the National Statistical Office, the estimates of gross domestic product, gross value added, saving "
   "and capital formation are compiled by the:",
   ["Field Operations Division", "National Accounts Division", "Survey Design and Research Division",
    "Social Statistics Division"], "B",
   "The National Accounts Division compiles GDP, GVA, saving and capital formation. The Survey Design and "
   "Research Division plans the sample designs, the Field Operations Division collects the data, and the Social "
   "Statistics Division handles the labour force survey and social indicators.", "nso"),

 Q("The sampling design generally adopted in the household surveys of the National Sample Survey is:",
   ["simple random sampling of households from a national list",
    "systematic sampling of districts only",
    "quota sampling within states",
    "stratified multi-stage sampling, with villages or urban blocks as first-stage units and households as "
    "second-stage units"], "D",
   "The surveys use a stratified multi-stage design: census villages in rural areas and Urban Frame Survey "
   "blocks in urban areas are the first-stage units, and households the ultimate units. No national list of "
   "households exists, which is what makes a multi-stage design necessary.", "nso"),

 Q("In a surveyed population of 1000 persons, 400 are employed and 50 are unemployed (available for and seeking "
   "work). The labour force participation rate and the unemployment rate are, respectively:",
   ["45% and 11.1%", "45% and 5%", "40% and 11.1%", "40% and 12.5%"], "A",
   r"The labour force is the employed plus the unemployed, 450. $\text{LFPR}=\dfrac{450}{1000}=45\%$. The "
   r"unemployment rate is the unemployed as a proportion of the labour force, not of the population: "
   r"$\dfrac{50}{450}=11.1\%$. The worker population ratio is $40\%$.", "nso"),

 Q("The Census of India is conducted under the Census Act of which year, and by an office under which "
   "ministry?",
   ["1948; Ministry of Statistics and Programme Implementation", "1881; Ministry of Home Affairs",
    "1948; Ministry of Home Affairs", "1951; Ministry of Statistics and Programme Implementation"], "C",
   "The Census Act, 1948 provides the legal basis, and the census is conducted by the Office of the Registrar "
   "General and Census Commissioner, India, under the Ministry of Home Affairs. It is a complete enumeration "
   "taken every ten years.", "census"),

 Q("The two phases in which the Census of India is conducted are:",
   ["Sample selection, and Population Enumeration",
    "Houselisting and Housing Census, and Population Enumeration",
    "Population Enumeration, and Economic Census",
    "Pilot survey, and Post-enumeration survey"], "B",
   "In the first phase every building and household is listed and data on housing, amenities and assets are "
   "collected; in the second, each individual is enumerated. The houselisting provides the frame for the "
   "enumeration. The Economic Census is a separate count of establishments.", "census"),

 Q("Match the survey or system in List I with its description in List II."
   + match(["National Sample Survey (NSS)", "National Family Health Survey (NFHS)",
            "Sample Registration System (SRS)", "Agriculture Census"],
           ["Provides birth, death and infant mortality rates",
            "Data on operational holdings, taken every five years",
            "Begun in 1950 at the initiative of P. C. Mahalanobis",
            "Conducted with the International Institute for Population Sciences, Mumbai, as the nodal agency"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(ii), (b)-(iv), (c)-(i), (d)-(iii)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)"], "D",
   "The NSS began in 1950; the NFHS is carried out for the Ministry of Health and Family Welfare with IIPS, "
   "Mumbai, as nodal agency; the SRS gives the vital rates between censuses; the Agriculture Census, every five "
   "years, counts operational holdings.", "census"),

 Q("Consider the statements about the Census of India, 2011:"
   + st("It enumerated about 1.21 billion persons.",
        "The final count put the sex ratio at 943 females per 1000 males.",
        "The literacy rate was about 74%.",
        "It was conducted by the National Statistical Office.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and III only", "II and III only", "I, II, III and IV"], "A",
   "The 2011 census counted about 1.21 billion people, with a sex ratio of 943 (the provisional figure was 940) "
   "and a literacy rate of 74.04%. It was conducted by the Registrar General and Census Commissioner under the "
   "Ministry of Home Affairs, not by the NSO: (IV) is false.", "census"),

 Q("Match the statistician in List I with the contribution in List II."
   + match(["P. C. Mahalanobis", "R. C. Bose", "S. N. Roy", "D. Basu"],
           ["The union&ndash;intersection principle in multivariate analysis",
            r"The $D^2$ statistic, a distance between populations",
            "Independence of a complete sufficient statistic and an ancillary statistic",
            "Disproof of Euler's conjecture on orthogonal Latin squares"]),
   ["(a)-(ii), (b)-(i), (c)-(iv), (d)-(iii)", "(a)-(ii), (b)-(iv), (c)-(i), (d)-(iii)",
    "(a)-(iv), (b)-(ii), (c)-(i), (d)-(iii)", "(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)"], "B",
   r"Mahalanobis introduced $D^2$; Bose, with Shrikhande and Parker, disproved Euler's conjecture; Roy gave the "
   r"union&ndash;intersection principle and the largest root test; Basu's theorem states the independence of a "
   r"complete sufficient statistic and any ancillary statistic.", "statisticians"),

 Q("The Indian Statistical Institute was founded, and the National Sample Survey was started, in the years:",
   ["1931 and 1961", "1950 and 1931", "1931 and 1950", "1947 and 1950"], "C",
   "P. C. Mahalanobis founded the Indian Statistical Institute in Calcutta in 1931 and started the National "
   "Sample Survey in 1950. He also gave the model used for the Second Five Year Plan.", "statisticians"),

 Q("Euler's conjecture that no pair of orthogonal Latin squares exists for orders of the form $4k+2$ was "
   "disproved in 1959 by:",
   ["Mahalanobis, Bose and Roy", "Rao, Mitra and Mathai", "Fisher, Yates and Bose", "Bose, Shrikhande and Parker"], "D",
   "R. C. Bose, S. S. Shrikhande and E. T. Parker showed that pairs of orthogonal Latin squares exist for every "
   "order except 2 and 6 (their first counter-example was of order 22). They came to be called &lsquo;Euler's "
   "spoilers&rsquo;.", "statisticians"),

 Q("Which of the following is NOT a contribution of C. R. Rao?",
   ["The largest root test of multivariate analysis", "A lower bound for the variance of an unbiased estimator",
    "The score test", "Orthogonal arrays"], "A",
   "The largest root test is due to S. N. Roy. C. R. Rao's contributions include the Cram&eacute;r&ndash;Rao "
   "inequality, the Rao&ndash;Blackwell theorem, the score test and orthogonal arrays; he received the "
   "International Prize in Statistics in 2023.", "statisticians"),

 Q("In R, the values of " + c("-7 %/% 2") + " and " + c("-7 %% 2") + " are, respectively:",
   ["-3 and -1", "-3 and 1", "-4 and 1", "-4 and -1"], "C",
   c("%/%") + " is integer division rounding towards minus infinity (the floor), so " + c("-7 %/% 2") + " is "
   r"$\lfloor-3.5\rfloor=-4$. " + c("%%") + r" gives the remainder with the sign of the divisor: "
   r"$-7-2(-4)=1$. The two always satisfy $x=y\times(x\ \%/\%\ y)+(x\ \%\%\ y)$.", "r-basics"),

 Q("In R, " + c("0/0") + " gives " + c("NaN") + ". The value of " + c("is.na(0/0)") + " is:",
   [c("FALSE"), c("TRUE"), c("NA"), "an error"], "B",
   c("NaN") + " (not a number) is treated as a kind of missing value: " + c("is.na(NaN)") + " is " + c("TRUE") + ", "
   "while " + c("is.nan(NA)") + " is " + c("FALSE") + ". Note that " + c("5/0") + " is " + c("Inf") + ", which is "
   "neither.", "r-basics"),

 Q("In R, the result of " + c("c(1, 2, 3, 4) + c(10, 20)") + " is:",
   ["an error, because the lengths differ", c("11 22"), c("11 22 3 4"), c("11 22 13 24")], "D",
   "R recycles the shorter vector: " + c("c(10, 20)") + " is used as " + c("10 20 10 20") + ", giving "
   + c("11 22 13 24") + ". No warning is given here because the longer length is a multiple of the shorter.", "r-basics"),

 Q("After " + c("x &lt;- c(2, 4, 6, 8)") + ", the value of " + c("sum(x[-1])") + " is:",
   ["18", "20", "12", "2"], "A",
   "A negative index drops elements: " + c("x[-1]") + " is " + c("4 6 8") + ", whose sum is 18. (In R, unlike "
   "some languages, " + c("-1") + " does not mean the last element.)", "r-basics"),

 Q("After " + c("m &lt;- matrix(1:6, nrow = 2)") + ", the element " + c("m[2, 3]") + " is:",
   ["5", "6", "4", "3"], "B",
   "By default a matrix is filled column by column, so " + c("m") + " has rows " + c("1 3 5") + " and "
   + c("2 4 6") + ", and " + c("m[2, 3]") + " is 6. With " + c("byrow = TRUE") + " the rows would be "
   + c("1 2 3") + " and " + c("4 5 6") + ".", "r-funcs"),

 Q("After " + c("A &lt;- matrix(c(2, 1, 1, 3), 2)") + ", the values of " + c("(A %*% A)[1, 1]") + " and "
   + c("(A * A)[1, 1]") + " are, respectively:",
   ["4 and 4", "4 and 5", "5 and 5", "5 and 4"], "D",
   c("A") + r" is $\begin{pmatrix}2&1\\1&3\end{pmatrix}$. " + c("%*%") + r" is the matrix product, whose "
   r"$(1,1)$ element is $2\times2+1\times1=5$; " + c("*") + r" multiplies element by element, giving $2\times2=4$.", "r-funcs"),

 Q("After " + c("m &lt;- matrix(1:6, nrow = 2)") + ", the result of " + c("apply(m, 1, sum)") + " is:",
   [c("9 12"), c("3 7 11"), c("21"), c("1 2")], "A",
   "The second argument 1 means &lsquo;over rows&rsquo; (2 would mean over columns). The rows are "
   + c("1 3 5") + " and " + c("2 4 6") + ", with sums 9 and 12. " + c("apply(m, 2, sum)") + " gives "
   + c("3 7 11") + ".", "r-funcs"),

 Q("In R, " + c("mean(c(1, 2, NA, 5))") + " and " + c("mean(c(1, 2, NA, 5), na.rm = TRUE)") + " give, "
   "respectively:",
   ["2 and 2.667", "2.667 and 2.667", c("NA") + " and 2.667", c("NA") + " and 2"], "C",
   "Any arithmetic involving a missing value is missing, so the first is " + c("NA") + ". With "
   + c("na.rm = TRUE") + r" the missing value is removed first and the mean of 1, 2, 5 is $\tfrac83=2.667$.", "r-built"),

 Q("In R, the value of " + c("var(c(2, 4, 6))") + " is:",
   ["2.667", "4", "2", "8"], "B",
   c("var") + r" uses the divisor $n-1$: $\dfrac{(2-4)^2+0+(6-4)^2}{2}=4$, and " + c("sd") + r" gives 2. The "
   r"divisor $n$ would give 2.667.", "r-built"),

 Q("After " + c("x &lt;- c(1, 5, 8, 3)") + ", the value of " + c("sum(x &gt; 2)") + " is:",
   ["16", "17", "4", "3"], "D",
   c("x &gt; 2") + " is the logical vector " + c("FALSE TRUE TRUE TRUE") + ", and in arithmetic " + c("TRUE")
   + " counts as 1 and " + c("FALSE") + " as 0. So the sum is 3, the number of elements greater than 2. "
   + c("sum(x[x &gt; 2])") + " would give 16.", "r-built"),

 Q("Consider the statements about logical values in R:"
   + st(c("NA &amp; FALSE") + " is " + c("FALSE") + ".", c("NA | TRUE") + " is " + c("TRUE") + ".",
        c("NA == NA") + " is " + c("TRUE") + ".", c("is.na(NA)") + " is " + c("TRUE") + ".")
   + "Which of the statements are correct?",
   ["I, II and IV only", "I and II only", "III and IV only", "I, II, III and IV"], "A",
   "A logical operation with " + c("NA") + " gives a definite answer when the answer does not depend on the "
   "missing value: anything AND FALSE is FALSE, anything OR TRUE is TRUE. But a comparison with " + c("NA")
   + " is unknown, so " + c("NA == NA") + " is " + c("NA") + "; missing values are tested with " + c("is.na")
   + ".", "r-built"),

 Q("What is the value of " + c("s") + " after this R code is run?"
   + pre("s &lt;- 0\nfor (i in 1:5) {\n  if (i %% 2 == 0) next\n  s &lt;- s + i\n}"),
   ["15", "6", "9", "5"], "C",
   c("next") + r" skips the rest of the loop body for even $i$, so only the odd values are added: $1+3+5=9$. "
   "With " + c("break") + " in place of " + c("next") + " the loop would stop at $i=2$ and " + c("s") + " would "
   "be 1.", "r-control"),

 Q("What is the value of " + c("n") + " after this R code is run?"
   + pre("x &lt;- 100; n &lt;- 0\nwhile (x &gt; 1) {\n  x &lt;- x / 2\n  n &lt;- n + 1\n}"),
   ["6", "7", "8", "50"], "B",
   "The successive values of " + c("x") + " are 50, 25, 12.5, 6.25, 3.125, 1.5625, 0.78125. The loop stops when "
   + c("x") + r" is no longer greater than 1, after 7 halvings ($2^6=64\lt100\le2^7=128$).", "r-control"),

 Q("In R, the result of " + c('ifelse(c(1, 5, 3) &gt; 2, "H", "L")') + " is:",
   [c('"H"'), c('"L"'), c('"H" "L" "L"'), c('"L" "H" "H"')], "D",
   c("ifelse") + " works element by element on a vector: 1 is not greater than 2, while 5 and 3 are. By contrast "
   + c("if") + " takes a single condition and is not vectorised.", "r-control"),

 Q("In R, the result of " + c("seq(2, 10, by = 3)") + " is:",
   [c("2 5 8"), c("2 5 8 11"), c("2 6 10"), c("2 4 6 8 10")], "A",
   "The sequence starts at 2 and goes up in steps of 3 without passing 10: 2, 5, 8. "
   + c("seq(2, 10, length.out = 3)") + " would give " + c("2 6 10") + ".", "r-data"),

 Q("In R, the results of " + c('rep(c("a", "b"), each = 2)') + " and " + c('rep(c("a", "b"), times = 2)')
   + " are, respectively:",
   [c('"a" "b" "a" "b"') + " and " + c('"a" "a" "b" "b"'), "the same vector in both cases",
    c('"a" "a" "b" "b"') + " and " + c('"a" "b" "a" "b"'), c('"a" "a"') + " and " + c('"b" "b"')], "C",
   c("each") + " repeats every element in turn before moving to the next; " + c("times")
   + " repeats the whole vector.", "r-data"),

 Q("After " + c("x &lt;- c(30, 10, 20)") + ", the results of " + c("order(x)") + " and " + c("rank(x)")
   + " are, respectively:",
   [c("3 1 2") + " and " + c("2 3 1"), c("2 3 1") + " and " + c("3 1 2"), c("10 20 30") + " and " + c("3 1 2"),
    c("2 3 1") + " and " + c("2 3 1")], "B",
   c("order") + " gives the positions of the elements in increasing order: the smallest is in position 2, then "
   "3, then 1. " + c("rank") + " gives the rank of each element: 30 is third, 10 first, 20 second. "
   + c("x[order(x)]") + " is the same as " + c("sort(x)") + ".", "r-data"),

 Q("In R, the value of " + c('substr("statistics", 3, 6)') + " is:",
   [c('"stat"'), c('"tati"'), c('"atist"'), c('"atis"')], "D",
   c("substr(x, start, stop)") + " extracts the characters from position 3 to position 6 inclusive, counting "
   "from 1: s-t-<b>a-t-i-s</b>-t-i-c-s, i.e. " + c('"atis"') + ". " + c('nchar("statistics")') + " is 10.", "r-data"),

 Q("After " + c('f &lt;- factor(c("b", "a", "b", "c"))') + ", the result of " + c("as.integer(f)") + " is:",
   [c("2 1 2 3"), c("1 2 1 3"), c("1 2 3 4"), "an error"], "A",
   "The levels of a factor are the distinct values in sorted order, " + c('"a" "b" "c"') + ", coded 1, 2, 3. "
   "The data b, a, b, c therefore have codes 2, 1, 2, 3. " + c("nlevels(f)") + " is 3 and " + c("table(f)")
   + " gives the counts 1, 2, 1.", "r-list"),

 Q("After " + c('L &lt;- list(a = 1:3, b = "x")') + ", which statement is correct?",
   [c('L["a"]') + " and " + c('L[["a"]]') + " are both integer vectors",
    c('L["a"]') + " is an integer vector and " + c('L[["a"]]') + " is a list",
    c('L["a"]') + " is a list of length 1 and " + c('L[["a"]]') + " is the integer vector " + c("1 2 3"),
    c("length(L)") + " is 4"], "C",
   "Single brackets return a sub-list; double brackets (or " + c("L&#36;a") + ") return the element itself. So "
   + c('L[["a"]][2]') + " is 2. The list has two components, so " + c("length(L)") + " is 2.", "r-list"),

 Q("In R, the values of " + c("round(2.5)") + " and " + c("round(3.5)") + " are, respectively:",
   ["3 and 4", "2 and 4", "2 and 3", "3 and 3"], "B",
   "R follows the IEC 60559 standard and rounds a value exactly half-way to the even digit: 2.5 goes to 2 and "
   "3.5 goes to 4. This avoids the upward bias of always rounding halves up.", "r-list"),

 Q("After " + c('df &lt;- data.frame(x = c(1, 2, 3), y = c("a", "b", "c"))') + ", the results of " + c("dim(df)")
   + " and " + c("nrow(df[df&#36;x &gt; 1, ])") + " are, respectively:",
   [c("2 3") + " and 2", c("3 2") + " and 1", c("6") + " and 2", c("3 2") + " and 2"], "D",
   c("dim") + " gives rows then columns: 3 observations of 2 variables. " + c("df[df&#36;x &gt; 1, ]")
   + " keeps the rows where " + c("x") + " exceeds 1 (the second and third) and all columns, so it has 2 rows. "
   "The comma is essential: without it R would select columns.", "r-frames"),

 Q("In R, the result of " + c('tapply(c(10, 20, 30, 40), c("a", "b", "a", "b"), mean)') + " is:",
   ["a single value, 25", "a = 15, b = 35", "a = 20, b = 30", "a = 40, b = 60"], "C",
   c("tapply") + " applies a function to the values of a vector within the groups defined by a factor. Group a "
   "holds 10 and 30 (mean 20); group b holds 20 and 40 (mean 30). With " + c("sum") + " it would give 40 and "
   "60.", "r-frames"),

 Q("Match the R function in List I with what it does in List II."
   + match([c("hist(x)"), c("boxplot(x)"), c("plot(x, y)"), c("abline(lm(y ~ x))")],
           ["Draws a scatter diagram", "Draws a histogram",
            "Adds the fitted regression line to an existing plot", "Draws a box-and-whisker plot"]),
   ["(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)", "(a)-(ii), (b)-(iv), (c)-(i), (d)-(iii)",
    "(a)-(iv), (b)-(ii), (c)-(i), (d)-(iii)", "(a)-(i), (b)-(iv), (c)-(ii), (d)-(iii)"], "B",
   "The first three are high-level functions that start a new plot; " + c("abline") + " is a low-level function "
   "that adds a line to the current plot, here the least-squares line from " + c("lm") + ". "
   + c("par(mfrow = c(2, 2))") + " would arrange four plots on one page.", "r-graph"),

 Q("After " + c("f &lt;- function(x, y = 2) x^y") + ", the values of " + c("f(3)") + " and " + c("f(y = 3, x = 2)")
   + " are, respectively:",
   ["9 and 8", "9 and 9", "6 and 6", "an error and 8"], "A",
   "When " + c("y") + r" is not supplied its default 2 is used: $3^2=9$. Arguments given by name are matched by "
   r"name whatever their order: $x=2$, $y=3$ gives $2^3=8$.", "r-prog"),

 Q("What does this R code print?"
   + pre("x &lt;- 5\nf &lt;- function() {\n  x &lt;- 10\n  x\n}\nprint(f())\nprint(x)"),
   ["10 and 10", "5 and 5", "10 and 5", "5 and 10"], "C",
   "The assignment inside the function creates a local variable " + c("x") + " that exists only while the "
   "function runs; the function returns 10, and the global " + c("x") + " is still 5. Only the "
   "super-assignment operator " + c("&lt;&lt;-") + " would change the global variable.", "r-prog"),

 Q("In R, " + c("sapply(1:3, function(i) i^2)") + " returns:",
   ["a list of three elements", "the numeric vector " + c("1 4 9"), "the single number 14", "a 3 &times; 3 matrix"], "B",
   c("sapply") + " applies the function to each element and simplifies the result to a vector where it can. "
   + c("lapply") + " does the same but always returns a list. Here the vectorised " + c("(1:3)^2")
   + " gives the same result without any loop.", "r-prog"),

 Q(r"Which LaTeX source produces the formula $\bar x=\dfrac1n\sum_{i=1}^{n}x_i$?",
   [c(r"&#36;\mean{x} = 1/n \sum{i=1}{n} x_i&#36;"), c(r"&#36;\bar{x} = \frac{1}{n} \sum^{i=1}_{n} x_i&#36;"),
    c(r"&#36;\bar{x} = \frac{n}{1} \sum_{i=1}^{n} x_i&#36;"), c(r"&#36;\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i&#36;")], "D",
   c(r"\bar{x}") + " puts a bar over x; " + c(r"\frac{1}{n}") + " takes the numerator first and the denominator "
   "second; the lower limit of a sum follows " + c("_") + " and the upper limit follows " + c("^")
   + ". Option B has the limits interchanged and option C the fraction inverted; "
   + c(r"\mean") + " is not a LaTeX command.", "latex"),

 Q("Match the LaTeX environment in List I with what it produces in List II."
   + match([c("equation"), c("equation*"), c("align"), c("tabular")],
           ["A numbered displayed equation", "An unnumbered displayed equation",
            "Several displayed equations aligned at the &amp; signs", "A table of rows and columns"]),
   ["(a)-(i), (b)-(ii), (c)-(iii), (d)-(iv)", "(a)-(ii), (b)-(i), (c)-(iii), (d)-(iv)",
    "(a)-(i), (b)-(ii), (c)-(iv), (d)-(iii)", "(a)-(iii), (b)-(ii), (c)-(i), (d)-(iv)"], "A",
   "A star after an environment or sectioning command suppresses the number. " + c("align") + " (from the "
   + c("amsmath") + " package) sets several equations aligned at " + c("&amp;") + ", with lines separated by "
   + c(r"\\") + ". " + c("tabular") + " builds a table, its argument (such as " + c("{|c|c|}")
   + ") describing the columns.", "latex"),

 Q("Consider the statements about a LaTeX document:"
   + st(c(r"\usepackage") + " commands are placed in the preamble, before " + c(r"\begin{document}") + ".",
        "The column specification " + c("{lcr}") + " of a " + c("tabular") + " environment declares three "
        "columns.",
        c(r"\includegraphics") + " requires the " + c("graphicx") + " package.",
        c(r"\section*{Introduction}") + " produces a numbered section heading.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "II, III and IV only", "I, II, III and IV"], "B",
   "The preamble, between " + c(r"\documentclass") + " and " + c(r"\begin{document}") + ", is where packages are "
   "loaded. " + c("{lcr}") + " declares a left-aligned, a centred and a right-aligned column. "
   + c(r"\includegraphics") + " is defined by " + c("graphicx") + ". The starred form " + c(r"\section*")
   + " gives an <em>unnumbered</em> heading: (IV) is false.", "latex"),
]
