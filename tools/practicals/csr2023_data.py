# -*- coding: utf-8 -*-
"""The ten practicals of Computational Statistics and R Programming (2023 syllabus).

build_csr2023_practical.py runs every step's R code in one R session per practical
and writes statistics/computational-statistics-and-r-programming-2023/practical.html,
so each OUTPUT on the page is R's own.

Each practical follows the record-book layout: Question (with its data and parts),
Aim, Formula and R commands, Steps (each with code, then output, then a plot where one
is drawn), Notes, and a Conclusion.

A step is (heading, explanation HTML, R code, options). Options:
  run=False      show the code without running it (installers, CRAN downloads); give
                 the expected output as shown=...
  plot="f.png"   the step draws a plot; it is saved as img/f.png and shown under it
  note=...       a remark printed under the output
"""

MARKS = ("32, 47, 41, 51, 41, 30, 39, 18, 48, 53, 54, 32, 31, 46, 15, 37, 32, 56, 42, 48, "
         "38, 26, 50, 40, 38, 42, 35, 22, 62, 51, 44, 21, 45, 31, 37, 41, 44, 18, 37, 47, "
         "68, 41, 30, 52, 52, 60, 42, 38, 38, 34")
MARKS2 = ("30, 42, 41, 31, 41, 38, 39, 18, 28, 53, 64, 32, 41, 26, 25, 37, 32, 56, 52, 18, "
          "48, 76, 20, 10, 48, 45, 39, 29, 69, 52, 47, 28, 47, 32, 67, 51, 44, 19, 27, 42, "
          "66, 21, 60, 22, 52, 64, 49, 33, 35, 37")


def wrap(values, per=10, indent="  "):
    """The data vector over several lines, ten values a line."""
    v = [x.strip() for x in values.split(",")]
    rows = [", ".join(v[i:i + per]) for i in range(0, len(v), per)]
    return (",\n" + indent).join(rows)


P = []

# ---------------------------------------------------------------- 1
P.append(dict(
    n=1, title="Installing R and RStudio",
    syllabus=[1, 2],
    question="""<p>Install R and RStudio on your computer and confirm that they work. Then create a folder
<code>DS_R</code>, make it the working directory, and display the current working directory.</p>""",
    aim="To install R and RStudio, check the installed version, and set up a working directory for the practicals.",
    commands=[
        ("R", "the language and its engine, from CRAN, cran.r-project.org"),
        ("RStudio Desktop", "a free editor (IDE) that runs R, from posit.co; install R first"),
        ("<code>R.version.string</code>", "the version of R that is running"),
        ("<code>dir.create(path)</code>", "creates a folder"),
        ("<code>setwd(path)</code>", "makes that folder the working directory, where R reads and saves files"),
        ("<code>getwd()</code>", "prints the current working directory"),
    ],
    steps=[
        ("Install R",
         """<p>Open <strong>cran.r-project.org</strong> and choose your system. On Windows: <em>Download R for
Windows &rarr; base &rarr; Download R</em>, run the <code>.exe</code> file, and accept the defaults (64-bit
on a 64-bit machine). On macOS, download the <code>.pkg</code> file for your processor; on Linux, use your
distribution's package (for example <code>sudo apt install r-base</code> on Ubuntu).</p>""",
         None, {}),
        ("Install RStudio Desktop",
         """<p>Open <strong>posit.co/download/rstudio-desktop</strong>, download the installer for your system,
run it, and accept the defaults. RStudio finds the R you installed in Step 1.</p>""",
         None, {}),
        ("Check the installation",
         """<p>Open RStudio. In the <strong>Console</strong> (bottom left), type the command and press Enter.</p>""",
         'R.version.string',
         dict(note="Your version number may be newer; any R 4.x runs every practical on this page.")),
        ("Create the folder DS_R and make it the working directory",
         """<p>The folder is created inside the current working directory (on Windows, usually
<em>Documents</em>). In RStudio the same can be done from <em>Session &rarr; Set Working Directory
&rarr; Choose Directory</em>.</p>""",
         'dir.create("DS_R")\nsetwd("DS_R")\ngetwd()',
         dict(run=False, shown='[1] "C:/Users/Student/Documents/DS_R"',
              note="The path printed is the folder on your own computer, so it will differ from this one.")),
    ],
    notes=[],
    conclusion="""<p>R and RStudio are installed, <code>R.version.string</code> reports the version, and
<code>DS_R</code> is the working directory, so every file the later practicals read or save is kept in one
place.</p>""",
))

# ---------------------------------------------------------------- 2
P.append(dict(
    n=2, title='Installing the Packages "ggplot2", "caTools" and "CART"',
    syllabus=[3],
    question="""<p>Install the packages <code>ggplot2</code>, <code>caTools</code> and CART (classification and
regression trees), and check that each one works.</p>""",
    aim="To install packages from CRAN, confirm that they are installed, and test each with a small example.",
    commands=[
        ("<code>install.packages(\"name\")</code>", "downloads a package from CRAN and installs it; needs the internet, once per computer"),
        ("<code>install.packages(c(\"a\", \"b\"))</code>", "installs several at once"),
        ("<code>library(name)</code>", "loads an installed package into the session; once per session"),
        ("<code>installed.packages()</code>", "the table of installed packages"),
        ("<code>ggplot2</code>", "graphics built in layers"),
        ("<code>caTools</code>", "<code>sample.split()</code>, for splitting data into training and test sets"),
        ("<code>rpart</code>", "classification and regression trees (CART); it comes with R"),
    ],
    steps=[
        ("Install the packages",
         """<p>In the Console, with the internet on:</p>""",
         'install.packages("ggplot2")   # graphics\ninstall.packages("caTools")   # splitting data\n# CART is provided by the rpart package, which is installed with R itself',
         dict(run=False, shown="Installing package into ...\n...\n* DONE (ggplot2)",
              note="Each command prints the download and ends with <code>DONE</code>.")),
        ("Check that they are installed",
         "", 'c("ggplot2", "caTools", "rpart") %in% rownames(installed.packages())', {}),
        ("Test ggplot2: a scatter plot",
         """<p>Using the built-in <code>mtcars</code> data: fuel economy against horsepower.</p>""",
         'library(ggplot2)\nggplot(mtcars, aes(x = mpg, y = hp)) + geom_point()',
         dict(plot="p2-scatter.png")),
        ("Test caTools: split the iris data 70 : 30",
         """<p><code>sample.split()</code> marks each row TRUE (training) or FALSE (test), keeping the share of
each species the same in both. <code>set.seed()</code> makes the split repeatable.</p>""",
         'library(caTools)\nset.seed(123)\nsplit <- sample.split(iris$Species, SplitRatio = 0.7)\ntable(split)',
         {}),
        ("Test rpart: a classification tree",
         "", 'library(rpart)\nfit <- rpart(Species ~ ., data = iris)\nfit', {}),
        ("If an installation fails",
         """<ul><li><strong>"package not available"</strong>: check the spelling (names are case-sensitive)
and the internet, or name a mirror: <code>install.packages("ggplot2", repos = "https://cloud.r-project.org")</code>.</li>
<li><strong>"dependency is not available"</strong>: install with its dependencies:
<code>install.packages("ggplot2", dependencies = TRUE)</code>.</li>
<li><strong>"non-zero exit status"</strong>: update R, restart RStudio, and try again.</li></ul>""",
         None, {}),
    ],
    notes=['There is no package called "CART" on CRAN, so <code>install.packages("CART")</code> fails. '
           'Classification and regression trees in R come from <code>rpart</code>, which is installed with R.',
           'To install dependencies, <code>dependencies = TRUE</code> is an argument: '
           '<code>install.packages("ggplot2", dependencies = TRUE)</code>, not a package name in quotes.'],
    conclusion="""<p>The three packages are installed, and each works: ggplot2 draws, caTools splits 150
iris rows into 105 for training and 45 for testing, and rpart grows a tree.</p>""",
))

# ---------------------------------------------------------------- 3
P.append(dict(
    n=3, title='Loading the Packages "ggplot2" and "caTools"',
    syllabus=[4],
    question="""<p>Load the packages <code>ggplot2</code> and <code>caTools</code>, confirm they are loaded, and use
each once.</p>""",
    aim="To load installed packages into the R session and confirm that they are attached.",
    commands=[
        ("<code>library(name)</code>", "loads the package; stops with an error if it is not installed"),
        ("<code>(.packages())</code>", "the packages attached in this session"),
        ("<code>sample.split(y, SplitRatio)</code>", "TRUE for rows chosen for training"),
        ("<code>subset(data, condition)</code>", "the rows that satisfy a condition"),
    ],
    steps=[
        ("Load the packages", "", 'library(ggplot2)\nlibrary(caTools)', {}),
        ("Confirm they are attached", "", 'c("ggplot2", "caTools") %in% (.packages())', {}),
        ("Use caTools: split mtcars into training and test sets",
         "", 'set.seed(123)\nsplit <- sample.split(mtcars$mpg, SplitRatio = 0.7)\ntrain_set <- subset(mtcars, split == TRUE)\ntest_set  <- subset(mtcars, split == FALSE)\nc(train = nrow(train_set), test = nrow(test_set))', {}),
        ("Use ggplot2: the training set",
         "", 'ggplot(train_set, aes(x = wt, y = mpg)) + geom_point() +\n  labs(title = "mtcars training set", x = "Weight (1000 lb)", y = "Miles per gallon")',
         dict(plot="p3-train.png")),
    ],
    notes=[],
    conclusion="""<p>Both packages load without error and are attached. <code>install.packages()</code> is run once
on a computer; <code>library()</code> is run in every new session.</p>""",
))

# ---------------------------------------------------------------- 4
P.append(dict(
    n=4, title="Basic Operations in R",
    syllabus=[5],
    question="""<p>Carry out the basic operations of R with examples: arithmetic, assignment, logical operations,
vectors, matrices, statistical functions, sequences, conditions, loops and functions.</p>""",
    aim="To learn the basic operations of R through small numerical examples.",
    commands=[
        ("<code>+ - * / ^</code>", "add, subtract, multiply, divide, power"),
        ("<code>%%</code> and <code>%/%</code>", "remainder and integer division"),
        ("<code>&lt;-</code> or <code>=</code>", "assignment"),
        ("<code>&gt; &lt; == != &gt;= &lt;=</code>, <code>&amp; | !</code>", "comparisons, and logical and, or, not"),
        ("<code>c()</code>, <code>matrix()</code>, <code>%*%</code>", "vectors, matrices, matrix product"),
        ("<code>mean() median() sd() var() summary()</code>", "statistics"),
        ("<code>seq() rep()</code>", "sequences and repetition"),
        ("<code>if / else</code>, <code>for</code>, <code>while</code>, <code>function</code>", "control and functions"),
    ],
    steps=[
        ("Arithmetic", "", '5 + 3\n10 - 4\n6 * 7\n20 / 4\n2 ^ 3\n10 %% 3\n10 %/% 3', {}),
        ("Assignment", "", 'a <- 15\nb = 4\nsum_result <- a + b\nprod_result <- a * b\nprint(sum_result)\nprint(prod_result)', {}),
        ("Logical operations", "", 'x <- 10\ny <- 20\nx > y\nx < y\nx == y\nx != y\nx >= y\n(x > 5) & (y < 30)\n(x > 5) | (y > 30)\n!(x > y)', {}),
        ("Vector operations", "", 'vec1 <- c(2, 4, 6)\nvec2 <- c(1, 3, 5)\nvec1 + vec2\nvec1 * vec2\nvec1 / vec2\nvec1 > vec2', {}),
        ("Matrix operations", """<p><code>+</code> adds element by element; <code>%*%</code> is the matrix product.</p>""",
         'mat1 <- matrix(c(1, 2, 3, 4), nrow = 2, ncol = 2)\nmat2 <- matrix(c(5, 6, 7, 8), nrow = 2, ncol = 2)\nmat1 + mat2\nmat1 %*% mat2', {}),
        ("Statistical functions", "", 'nums <- c(10, 20, 30, 40, 50)\nmean(nums)\nmedian(nums)\nsd(nums)\nvar(nums)\nmin(nums)\nmax(nums)\nsummary(nums)', {}),
        ("Sequences and repetition", "", 'seq(1, 10)\nseq(1, 10, by = 2)\nrep(5, times = 4)\nrep(c(1, 2, 3), times = 3)', {}),
        ("Conditional statements", "", 'x <- 15\nif (x > 10) {\n  print("x is greater than 10")\n} else if (x == 10) {\n  print("x is exactly 10")\n} else {\n  print("x is less than 10")\n}', {}),
        ("Loops", "", 'for (i in 1:5) {\n  print(i)\n}\nx <- 1\nwhile (x <= 3) {\n  print(x)\n  x <- x + 1\n}', {}),
        ("Functions", "", 'square <- function(num) {\n  return(num ^ 2)\n}\nsquare(4)\nsquare(5)', {}),
    ],
    notes=['<code>sd()</code> and <code>var()</code> divide by <em>n</em> &minus; 1, the sample formulas: for 10, 20, 30, 40, 50 '
           'they give 15.81 and 250. Dividing by <em>n</em> would give 14.14 and 200.'],
    conclusion="""<p>R works as a calculator, stores values in variables, compares them, and operates on whole
vectors and matrices at once; its statistical functions, sequences, conditions, loops and user-written
functions are the building blocks of every later practical.</p>""",
))

# ---------------------------------------------------------------- 5
P.append(dict(
    n=5, title="Working with Vectors using R",
    syllabus=[6],
    question="""<p>(a) Create a vector <code>v1</code> with elements 1 to 20. (b) Add 2 to every element of
<code>v1</code>. (c) Divide every element of <code>v1</code> by 5. (d) Create a vector <code>v2</code> with
elements 21 to 30, and add <code>v1</code> to <code>v2</code>.</p>""",
    aim="To create vectors and operate on every element at once, and to see how R adds vectors of different lengths.",
    commands=[
        ("<code>a:b</code>", "the whole numbers from a to b"),
        ("<code>v + k</code>, <code>v / k</code>", "applies the operation to every element"),
        ("<code>v1 + v2</code>", "adds element by element; a shorter vector is recycled"),
        ("<code>v[1:10]</code>", "the first ten elements"),
        ("<code>length(v)</code>", "the number of elements"),
    ],
    steps=[
        ("(a) Create v1 with elements 1 to 20", "", 'v1 <- 1:20\nv1', {}),
        ("(b) Add 2 to every element", "", 'v1 + 2', {}),
        ("(c) Divide every element by 5", "", 'v1 / 5', {}),
        ("(d) Create v2 with elements 21 to 30", "", 'v2 <- 21:30\nv2\nlength(v1); length(v2)', {}),
        ("(d) Add v1 to v2",
         """<p><code>v1</code> has 20 elements and <code>v2</code> has 10. R <strong>recycles</strong> the shorter
vector: <code>v2</code> is used twice, so element 11 of <code>v1</code> is added to element 1 of
<code>v2</code> again. Because 20 is a multiple of 10, R gives no warning.</p>""",
         'v1 + v2', {}),
        ("When the lengths do not fit",
         """<p>If the longer length is not a multiple of the shorter, R still recycles but warns.</p>""",
         '1:20 + 1:3', {}),
        ("Adding only the matching elements",
         """<p>To add element by element without recycling, use the first ten elements of <code>v1</code>.</p>""",
         'v1[1:10] + v2', {}),
    ],
    notes=['<code>v1 + v2</code> with 20 and 10 elements gives no warning, because 20 is a multiple of 10; '
           'R recycles <code>v2</code> silently. The warning "longer object length is not a multiple of shorter '
           'object length" appears only when it is not a multiple, as in <code>1:20 + 1:3</code>.'],
    conclusion="""<p>Arithmetic on a vector acts on every element. Adding two vectors works element by element,
recycling the shorter one, which is why <code>v1 + v2</code> has 20 elements: 22, 24, &hellip;, 40 and then
32, 34, &hellip;, 50.</p>""",
))

# ---------------------------------------------------------------- 6
P.append(dict(
    n=6, title="Create the Matrix of the Data using R",
    syllabus=[7],
    question="""<p>Using the distances between five cities in the table below, create a matrix <code>M</code> and find
the pair of cities with the shortest distance.</p>
<table>
<tr><th></th><th>C1</th><th>C2</th><th>C3</th><th>C4</th><th>C5</th></tr>
<tr><th>C1</th><td>0</td><td>12</td><td>13</td><td>8</td><td>20</td></tr>
<tr><th>C2</th><td>12</td><td>0</td><td>15</td><td>28</td><td>88</td></tr>
<tr><th>C3</th><td>13</td><td>15</td><td>0</td><td>6</td><td>9</td></tr>
<tr><th>C4</th><td>8</td><td>28</td><td>6</td><td>0</td><td>33</td></tr>
<tr><th>C5</th><td>20</td><td>88</td><td>9</td><td>33</td><td>0</td></tr>
</table>""",
    aim="To store a table as a matrix with row and column names, and to search it for its smallest off-diagonal value.",
    commands=[
        ("<code>matrix(x, nrow, ncol, byrow = TRUE)</code>", "a matrix filled row by row"),
        ("<code>rownames()</code>, <code>colnames()</code>", "name the rows and columns"),
        ("<code>upper.tri(M)</code>", "TRUE above the diagonal: each pair of cities once"),
        ("<code>min()</code>, <code>which(..., arr.ind = TRUE)</code>", "the smallest value, and its row and column"),
    ],
    steps=[
        ("Create the matrix M", "",
         'M <- matrix(c( 0, 12, 13,  8, 20,\n              12,  0, 15, 28, 88,\n              13, 15,  0,  6,  9,\n               8, 28,  6,  0, 33,\n              20, 88,  9, 33,  0),\n            nrow = 5, ncol = 5, byrow = TRUE)\ncity <- c("C1", "C2", "C3", "C4", "C5")\nrownames(M) <- city\ncolnames(M) <- city\nM', {}),
        ("Check that the matrix is symmetric",
         """<p>The distance from C1 to C2 must equal the distance from C2 to C1.</p>""",
         'isSymmetric(M)', {}),
        ("Find the shortest distance",
         """<p>The diagonal (a city to itself) is 0 and must be left out, and each pair appears twice, above
and below the diagonal. Looking only above the diagonal counts each pair once.</p>""",
         'pairs <- M[upper.tri(M)]\nmin_distance <- min(pairs)\nmin_distance', {}),
        ("Name the pair of cities", "",
         'where <- which(M == min_distance & upper.tri(M), arr.ind = TRUE)\nwhere\ncat("The shortest distance is", min_distance, "between",\n    rownames(M)[where[1, "row"]], "and", colnames(M)[where[1, "col"]], "\\n")', {}),
    ],
    notes=['Searching the whole matrix, as in <code>which(M == min_distance, arr.ind = TRUE)</code> after setting the zeros '
           'to <code>Inf</code>, returns two rows, (C4, C3) and (C3, C4), because the matrix is symmetric; its first row '
           'names the pair as "C4 and C3". Restricting the search to <code>upper.tri(M)</code> gives each pair once.'],
    conclusion="""<p>The shortest distance is <strong>6</strong>, between cities <strong>C3 and C4</strong>.</p>""",
))

# ---------------------------------------------------------------- 7
P.append(dict(
    n=7, title="Create the Data Structures of the Data using R",
    syllabus=[8],
    question="""<p>The marks scored by six students in two sections are:</p>
<table>
<tr><th>Section</th><th>Student</th><th>M1</th><th>M2</th><th>M3</th></tr>
<tr><td>A</td><td>1</td><td>46</td><td>54</td><td>45</td></tr>
<tr><td>A</td><td>2</td><td>34</td><td>55</td><td>55</td></tr>
<tr><td>A</td><td>3</td><td>56</td><td>66</td><td>64</td></tr>
<tr><td>B</td><td>1</td><td>43</td><td>44</td><td>45</td></tr>
<tr><td>B</td><td>2</td><td>67</td><td>76</td><td>78</td></tr>
<tr><td>B</td><td>3</td><td>76</td><td>68</td><td>37</td></tr>
</table>
<p>(a) Create a data structure for the data, with proper names. (b) Display the marks and totals of all
students. (c) Display the highest total in each section. (d) Add a new subject, M4, with marks for both
sections (50, 48, 67 for Section A and 54, 73, 42 for Section B).</p>""",
    aim="To store mixed data in a data frame, add computed and new columns, and summarise by group.",
    commands=[
        ("<code>data.frame()</code>", "a table whose columns may be of different types"),
        ("<code>df$col</code>", "one column; assigning to a new name adds a column"),
        ("<code>rowSums(df[ , cols])</code>", "the total of each row"),
        ("<code>tapply(x, group, max)</code>", "the maximum of x within each group"),
    ],
    steps=[
        ("(a) Create the data frame", "",
         'marks <- data.frame(\n  Section = c("A", "A", "A", "B", "B", "B"),\n  Student = c(1, 2, 3, 1, 2, 3),\n  M1 = c(46, 34, 56, 43, 67, 76),\n  M2 = c(54, 55, 66, 44, 76, 68),\n  M3 = c(45, 55, 64, 45, 78, 37)\n)\nmarks\nstr(marks)', {}),
        ("(b) Marks and totals of all students", "",
         'marks$Total <- rowSums(marks[ , c("M1", "M2", "M3")])\nmarks', {}),
        ("(c) The highest total in each section", "",
         'tapply(marks$Total, marks$Section, max)\nmarks[marks$Total == ave(marks$Total, marks$Section, FUN = max), ]', {}),
        ("(d) Add a new subject M4 and recompute the totals", "",
         'marks$M4 <- c(50, 48, 67, 54, 73, 42)\nmarks$Total <- rowSums(marks[ , c("M1", "M2", "M3", "M4")])\nmarks\ntapply(marks$Total, marks$Section, max)', {}),
    ],
    notes=[],
    conclusion="""<p>With three subjects, the highest totals are <strong>186</strong> in Section A (student 3) and
<strong>221</strong> in Section B (student 2). With M4 added, they become <strong>253</strong> and
<strong>294</strong>, for the same two students.</p>""",
))

# ---------------------------------------------------------------- 8
P.append(dict(
    n=8, title="Create the Matrix of the Data using R with Row and Column Names",
    syllabus=[9],
    question="""<p>Three people, P1, P2 and P3, intend to buy rolls, buns, cakes and bread, in different amounts, from
one of two shops, S1 and S2. The prices (in rupees) and the quantities wanted are:</p>
<table>
<tr><th>Item</th><th>Price at S1</th><th>Price at S2</th></tr>
<tr><td>Roll</td><td>1.5</td><td>1</td></tr>
<tr><td>Bun</td><td>2</td><td>2.5</td></tr>
<tr><td>Cake</td><td>5</td><td>4.5</td></tr>
<tr><td>Bread</td><td>16</td><td>17</td></tr>
</table>
<table>
<tr><th>Person</th><th>Roll</th><th>Bun</th><th>Cake</th><th>Bread</th></tr>
<tr><td>P1</td><td>6</td><td>5</td><td>3</td><td>1</td></tr>
<tr><td>P2</td><td>3</td><td>6</td><td>3</td><td>2</td></tr>
<tr><td>P3</td><td>3</td><td>4</td><td>3</td><td>1</td></tr>
</table>
<p>(a) Create the matrices of this information with row and column names. (b) Display the demand and price
matrices. (c) Find the total amount each person would spend in each shop. (d) Suggest the shop where each
person should buy.</p>""",
    aim="To represent the data as named matrices and use the matrix product to find each person's bill in each shop.",
    commands=[
        ("<code>matrix(..., byrow = TRUE, dimnames = list(rows, cols))</code>", "a named matrix"),
        ("<code>D %*% P</code>", "the matrix product: (3 &times; 4) times (4 &times; 2) gives 3 &times; 2"),
        ("Total cost", "person <em>i</em> at shop <em>j</em> = &Sigma;<sub><em>k</em></sub> quantity<sub><em>ik</em></sub> &times; price<sub><em>kj</em></sub>"),
        ("<code>apply(m, 1, f)</code>", "applies f to each row"),
    ],
    steps=[
        ("(a) Create the price matrix", "",
         'price <- matrix(c(1.5, 1,\n                  2,   2.5,\n                  5,   4.5,\n                  16,  17),\n                nrow = 4, byrow = TRUE,\n                dimnames = list(c("Roll", "Bun", "Cake", "Bread"), c("S1", "S2")))', {}),
        ("(a) Create the demand matrix", "",
         'demand <- matrix(c(6, 5, 3, 1,\n                   3, 6, 3, 2,\n                   3, 4, 3, 1),\n                 nrow = 3, byrow = TRUE,\n                 dimnames = list(c("P1", "P2", "P3"), c("Roll", "Bun", "Cake", "Bread")))', {}),
        ("(b) Display the two matrices", "", 'price\ndemand', {}),
        ("(c) The total amount each person spends in each shop",
         """<p>Each row of <code>demand</code> times each column of <code>price</code> is one bill. For P1 at S1:
6 &times; 1.5 + 5 &times; 2 + 3 &times; 5 + 1 &times; 16 = 9 + 10 + 15 + 16 = 50.</p>""",
         'cost <- demand %*% price\ncost', {}),
        ("(d) The cheaper shop for each person", "",
         'apply(cost, 1, function(r) if (r["S1"] < r["S2"]) "S1" else if (r["S1"] > r["S2"]) "S2" else "either")', {}),
    ],
    notes=['A commonly printed answer to this practical gives totals of 52.5 and 48.5 for P1, 59.0 and 60.0 for P2, '
           'and 52.5 and 50.5 for P3. Those are not the products of these two tables. Multiplying them out, as R does '
           'above, gives 50 and 49, 63.5 and 65.5, and 43.5 and 43.5.'],
    conclusion="""<p>P1 spends ₹50 at S1 and ₹49 at S2, so should buy at <strong>S2</strong>; P2 spends ₹63.50 and
₹65.50, so should buy at <strong>S1</strong>; P3 spends ₹43.50 at either shop.</p>""",
))

# ---------------------------------------------------------------- 9
P.append(dict(
    n=9, title="Applying the Summary of Data using R",
    syllabus=[10, 11],
    question="""<p>The marks in statistics of 50 candidates chosen at random from those appearing in an examination
are:</p>
<p class="data">""" + MARKS + """</p>
<p>(a) Apply <code>summary()</code> to the data. (b) Calculate all the measures of dispersion. (c) Draw
suitable graphs of the data.</p>""",
    aim="To summarise a set of marks with R's built-in functions, measure their spread, and show their distribution in graphs.",
    commands=[
        ("<code>summary(x)</code>", "minimum, first quartile, median, mean, third quartile, maximum"),
        ("Range", "max &minus; min: <code>diff(range(x))</code>"),
        ("Variance", "sample: &Sigma;(x &minus; x&#772;)&sup2; / (n &minus; 1), <code>var(x)</code>; population: &Sigma;(x &minus; x&#772;)&sup2; / n"),
        ("Standard deviation", "the square root of the variance: <code>sd(x)</code> (sample)"),
        ("Quartile deviation", "(Q<sub>3</sub> &minus; Q<sub>1</sub>) / 2, with <code>IQR(x)</code> = Q<sub>3</sub> &minus; Q<sub>1</sub>"),
        ("Mean deviation", "&Sigma;|x &minus; x&#772;| / n"),
        ("Coefficient of variation", "s / x&#772; &times; 100"),
    ],
    steps=[
        ("Enter the data", "", 'marks <- c(' + wrap(MARKS, indent="           ") + ')\nlength(marks)', {}),
        ("(a) Summary of the data",
         """<p>The sorted marks show the order statistics behind the quartiles; <code>table()</code> gives the
frequencies, from which the mode is read.</p>""",
         'summary(marks)\nsort(marks)\nfreq <- table(marks)\nnames(freq)[freq == max(freq)]   # the mode(s)', {}),
        ("(b) Measures of dispersion", "",
         'n <- length(marks)\nc(range = diff(range(marks)),\n  variance_sample = var(marks),\n  variance_population = var(marks) * (n - 1) / n,\n  sd_sample = sd(marks),\n  sd_population = sqrt(var(marks) * (n - 1) / n),\n  IQR = IQR(marks),\n  quartile_deviation = IQR(marks) / 2,\n  mean_deviation = mean(abs(marks - mean(marks))),\n  CV_percent = sd(marks) / mean(marks) * 100)', {}),
        ("(c) Histogram", "",
         'library(ggplot2)\nggplot(data.frame(marks), aes(x = marks)) +\n  geom_histogram(binwidth = 5, boundary = 15, fill = "steelblue", colour = "black") +\n  labs(title = "Histogram of marks", x = "Marks", y = "Frequency")',
         dict(plot="p9-histogram.png")),
        ("(c) Box plot", "",
         'ggplot(data.frame(marks), aes(y = marks)) +\n  geom_boxplot(fill = "tomato", colour = "black") +\n  labs(title = "Box plot of marks", y = "Marks")',
         dict(plot="p9-boxplot.png")),
        ("(c) Density plot", "",
         'ggplot(data.frame(marks), aes(x = marks)) +\n  geom_density(fill = "seagreen", alpha = 0.5) +\n  labs(title = "Density of marks", x = "Marks", y = "Density")',
         dict(plot="p9-density.png")),
    ],
    notes=['Two values, 38 and 41, each occur four times, so the marks have <strong>two modes</strong>, not one.',
           'R\'s <code>var()</code> and <code>sd()</code> divide by <em>n</em> &minus; 1 and give 130.23 and 11.41. '
           'Dividing by <em>n</em> gives 127.62 and 11.30, the population figures that are often printed; the '
           'coefficient of variation is then 28.0% instead of 28.3%. State which divisor you use.',
           'In R, <code>mad()</code> is the <em>median</em> absolute deviation (scaled by 1.4826), not the mean '
           'deviation; the mean deviation about the mean is <code>mean(abs(x - mean(x)))</code> = 8.77.'],
    conclusion="""<p>The marks run from 15 to 68 (range 53), with mean 40.34, median 41 and modes 38 and 41. The
quartiles are 32.5 and 47.75, so the IQR is 15.25. The sample standard deviation is 11.41 and the
coefficient of variation 28.3%. The histogram and density plot show one central peak around 40, slightly
longer on the left; the box plot shows no outliers.</p>""",
))

# ---------------------------------------------------------------- 10
P.append(dict(
    n=10, title="Implementation of Data Visualizations using R",
    syllabus=[11],
    question="""<p>(i) For the 50 marks of Practical 9, draw a histogram, a box plot and a line plot.</p>
<p>(ii) Draw a bar chart of the chlorophyll data, and a multiple bar chart of the production data.</p>
<table>
<tr><th>Chlorophyll type</th><th>Frequency</th></tr>
<tr><td>Albina</td><td>50</td></tr><tr><td>Xantha</td><td>44</td></tr><tr><td>Chloria</td><td>36</td></tr>
<tr><td>Viridis</td><td>30</td></tr><tr><td>Xchloro-viridis</td><td>16</td></tr><tr><td>Chlorotica</td><td>16</td></tr>
<tr><td>Virescent</td><td>8</td></tr>
</table>
<table>
<tr><th>Year</th><th>Wheat</th><th>Maize</th><th>Rice</th></tr>
<tr><td>1984</td><td>0.51</td><td>0.52</td><td>1.38</td></tr>
<tr><td>1985</td><td>0.51</td><td>1.38</td><td>2.02</td></tr>
<tr><td>1986</td><td>0.65</td><td>1.41</td><td>1.91</td></tr>
<tr><td>1987</td><td>0.36</td><td>1.64</td><td>2.26</td></tr>
</table>
<p>(iii) Draw a scatter plot of <code>marks1</code> (the marks of Practical 9) against <code>marks2</code>:</p>
<p class="data">""" + MARKS2 + """</p>""",
    aim="To draw the standard graphs of R, each suited to a different kind of data: bar, multiple bar, histogram, box, line and scatter plots.",
    commands=[
        ("Bar chart", "<code>geom_col()</code> (or <code>geom_bar(stat = \"identity\")</code>): categories against their frequencies"),
        ("Multiple bar chart", "<code>geom_col(position = \"dodge\")</code>: one bar per group within each category"),
        ("Histogram", "<code>geom_histogram()</code>: the distribution of a continuous variable"),
        ("Box plot", "<code>geom_boxplot()</code>: median, quartiles and outliers"),
        ("Line plot", "<code>geom_line()</code>: values in order"),
        ("Scatter plot", "<code>geom_point()</code>: one variable against another; <code>cor()</code> measures the linear relation"),
    ],
    steps=[
        ("The data", "",
         'library(ggplot2)\nmarks1 <- c(' + wrap(MARKS, indent="            ") + ')\nmarks2 <- c(' + wrap(MARKS2, indent="            ") + ')\nchlorophyll <- data.frame(\n  Type = c("Albina", "Xantha", "Chloria", "Viridis", "Xchloro-viridis", "Chlorotica", "Virescent"),\n  Frequency = c(50, 44, 36, 30, 16, 16, 8))\ncrops <- data.frame(\n  Year = rep(c(1984, 1985, 1986, 1987), each = 3),\n  Crop = rep(c("Wheat", "Maize", "Rice"), times = 4),\n  Production = c(0.51, 0.52, 1.38, 0.51, 1.38, 2.02, 0.65, 1.41, 1.91, 0.36, 1.64, 2.26))\nc(length(marks1), length(marks2))', {}),
        ("(ii) Bar chart of the chlorophyll types",
         """<p><code>factor(..., levels = ...)</code> keeps the bars in the table's order, not alphabetical.</p>""",
         'chlorophyll$Type <- factor(chlorophyll$Type, levels = chlorophyll$Type)\nggplot(chlorophyll, aes(x = Type, y = Frequency)) +\n  geom_col(fill = "skyblue", colour = "black") +\n  labs(title = "Chlorophyll types", x = "Type", y = "Frequency")',
         dict(plot="p10-bar.png")),
        ("(ii) Multiple bar chart of crop production", "",
         'ggplot(crops, aes(x = factor(Year), y = Production, fill = Crop)) +\n  geom_col(position = "dodge", colour = "black") +\n  labs(title = "Production of wheat, maize and rice", x = "Year", y = "Production")',
         dict(plot="p10-multibar.png")),
        ("(i) Histogram of the marks", "",
         'ggplot(data.frame(marks1), aes(x = marks1)) +\n  geom_histogram(binwidth = 5, boundary = 15, fill = "steelblue", colour = "black") +\n  labs(title = "Histogram of marks", x = "Marks", y = "Frequency")',
         dict(plot="p10-histogram.png")),
        ("(i) Box plot of the marks", "",
         'ggplot(data.frame(marks1), aes(y = marks1)) +\n  geom_boxplot(fill = "tomato", colour = "black") +\n  labs(title = "Box plot of marks", y = "Marks")',
         dict(plot="p10-boxplot.png")),
        ("(i) Line plot of the marks, in the order given", "",
         'ggplot(data.frame(candidate = seq_along(marks1), marks1), aes(x = candidate, y = marks1)) +\n  geom_line(colour = "steelblue", linewidth = 0.8) +\n  geom_point(colour = "firebrick", size = 2) +\n  labs(title = "Marks of the 50 candidates", x = "Candidate", y = "Marks")',
         dict(plot="p10-line.png")),
        ("(iii) Scatter plot of marks1 against marks2",
         """<p>The two vectors go into one data frame first, so that <code>ggplot()</code> plots these marks and not
another data set.</p>""",
         'pairs <- data.frame(marks1, marks2)\nggplot(pairs, aes(x = marks1, y = marks2)) +\n  geom_point(colour = "steelblue", size = 2.5) +\n  labs(title = "marks1 against marks2", x = "marks1", y = "marks2")\nround(cor(marks1, marks2), 3)',
         dict(plot="p10-scatter.png")),
    ],
    notes=['For the scatter plot, <code>marks1</code> and <code>marks2</code> must be put into a data frame '
           '(<code>pairs &lt;- data.frame(marks1, marks2)</code>) before <code>ggplot()</code>. A version with that line '
           'commented out plots whatever data frame was last called <code>data</code>.',
           'In ggplot2 3.4 and later, the thickness of a line is set with <code>linewidth</code>; '
           '<code>size</code> still works for points but is deprecated for lines.'],
    conclusion="""<p>The bar chart compares the seven chlorophyll types, with Albina the most frequent; the multiple bar
chart shows rice the largest crop in every year. The histogram, box plot and line plot show the marks'
distribution and their variation from candidate to candidate; the scatter plot shows marks2 tending to
rise with marks1, a moderate positive relation (correlation 0.41).</p>""",
))

# The official syllabus's 11 exercises, and the practical that covers each.
SYLLABUS = [
    (1, "Installing R and RStudio"),
    (2, "Create a folder DS_R, make it the working directory, and display the current working directory"),
    (3, 'Installing the "ggplot2", "caTools", "CART" packages'),
    (4, 'Load the packages "ggplot2", "caTools"'),
    (5, "Basic operations in R"),
    (6, "Working with vectors"),
    (7, "A distance matrix and the pair of cities with the shortest distance"),
    (8, "Marks of six students: a data structure, totals, highest per section, a new subject"),
    (9, "Price and demand matrices: total cost per person per shop, and the cheaper shop"),
    (10, "Apply summary() to find the mean, median, standard deviation and other measures"),
    (11, "Implement visualisations: bar, histogram, box, line and scatter plots"),
]
