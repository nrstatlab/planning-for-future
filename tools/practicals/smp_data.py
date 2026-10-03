# -*- coding: utf-8 -*-
r"""Statistical Methods using Python (STS-105): the twelve prescribed programs, and tails.py.

Built by build_py_practical.py smp_data. The programmes are the files in smp/; each step is
marked in the file by a "# Step i:" comment, and the page shows what each one prints.
"""
PAGE = "statistics/statistical-methods-using-python/practical.html"
SRC = "smp"
TITLE = "Practical — Statistical Methods using Python (STS-105)"
DESC = ("All twelve prescribed programs of STS-105, written in pure Python with no statistical packages, "
        "each set out as Question, Aim, Steps, Programme, and Execution and Results, with the output "
        "each one prints.")

HEAD = r"""<div class="wrapper">

  <div class="banner">
    <div class="crumbs"><a href="index.html">Home</a> &raquo; Practical</div>
    <h1>Practical &mdash; Statistical Methods using Python (STS-105)</h1>
    <p>All twelve prescribed programs of STS-105, written in pure Python with no statistical packages: matrices, sorting and searching, the summary measures, moments and shape, random number generation, fitting six distributions with goodness-of-fit tests, correlation and regression, seven tests of hypotheses, and both analyses of variance. Each program is set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and Results.</p>
  </div>

  <h2>Topics Covered</h2>
  <div class="chips">
    <span class="chip">Matrices</span>
    <span class="chip">Sorting &amp; Searching</span>
    <span class="chip">Frequency Tables</span>
    <span class="chip">Moments</span>
    <span class="chip">Random Generation</span>
    <span class="chip">Distribution Fitting</span>
    <span class="chip">Goodness of Fit</span>
    <span class="chip">Correlation</span>
    <span class="chip">Regression</span>
    <span class="chip">Tests of Hypotheses</span>
    <span class="chip">ANOVA</span>
  </div>

<details class="toc">
  <summary>On this page</summary>
  <ol>
{toc}
  </ol>
</details>
  <div class="tip">
    <strong>About this course.</strong> STS-105 is a <strong>practical</strong>. Its own
    note is the constraint that shapes every program below:
    <em>&ldquo;Must able to write Programs with all possibilities like usage of functions, Loops,
    OOP concepts, methods, built in functions etc. wherever it is possible. Without usage of Python
    Packages for statistical tools.&rdquo;</em>
    So nothing here imports <code>numpy</code>, <code>scipy</code>, <code>pandas</code> or
    <code>statistics</code>. Only <code>math</code> and <code>fractions</code> from the standard
    library appear, and every distribution, every tail area and every algorithm is written out.
  </div>

  <div class="tip">
    <strong>The Python itself is not taught here.</strong> Variables, input and output, the
    decision and repetition structures, functions and arguments, modules, exception handling,
    lists, tuples, dictionaries, sets, strings, classes and file input and output are all covered,
    with worked programs, in
    <a href="../../data-science/python-data-structures/index.html">Python Programming
    and Data Structures</a> &mdash;
    <a href="../../data-science/python-data-structures/unit1.html">Unit 1</a> for the
    language basics and control flow,
    <a href="../../data-science/python-data-structures/unit2.html">Unit 2</a> for
    functions and modules,
    <a href="../../data-science/python-data-structures/unit3.html">Unit 3</a> for lists,
    tuples, dictionaries and sets,
    <a href="../../data-science/python-data-structures/unit4.html">Unit 4</a> for classes
    and exception handling, and
    <a href="../../data-science/python-data-structures/unit5.html">Unit 5</a> for files.
    <strong>None of it is repeated below.</strong> What is written out here is the
    <em>statistics</em>: which formula, why that one, and what the output means.
  </div>

  <h2 id="the-twelve-programs">The Twelve Programs</h2>
  <div class="concept">
    <span class="label">WHAT EACH ONE IS FOR</span>
    <table>
      <tr><th>#</th><th>Program</th><th>The statistical point</th></tr>
      <tr><td>0</td><td>The tail areas (<code>tails.py</code>)</td>
          <td>\(t\), \(F\), \(\chi^{2}\) and normal \(p\) values with no table, for programs 8, 9, 11 and 12</td></tr>
      <tr><td>1</td><td>Sum and product of two matrices</td>
          <td>shape conditions; multiplication does not commute</td></tr>
      <tr><td>2</td><td>Determinant and inverse</td>
          <td>cofactor expansion; the transpose inside the adjoint; detecting singularity</td></tr>
      <tr><td>3</td><td>Four sorts, two searches</td>
          <td>comparison counts, and why binary search needs sorted input</td></tr>
      <tr><td>4</td><td>Median and mode</td>
          <td>the even-\(n\) case; several modes; no mode at all</td></tr>
      <tr><td>5</td><td>Frequency table and five summaries</td>
          <td>the grouped formulae, and the grouping error they carry</td></tr>
      <tr><td>6</td><td>Four moments, skewness, kurtosis</td>
          <td>raw to central conversion, checked a second way</td></tr>
      <tr><td>7</td><td>Random numbers from five distributions</td>
          <td>inverse transform, Box&ndash;Muller, Knuth's Poisson &mdash; and verifying them</td></tr>
      <tr><td>8</td><td>Binomial, Poisson, negative binomial fits</td>
          <td>over-dispersion; pooling classes; degrees of freedom after estimation</td></tr>
      <tr><td>9</td><td>Normal, exponential, Cauchy fits</td>
          <td>expected frequencies from the c.d.f.; fitting a distribution with no moments</td></tr>
      <tr><td>10</td><td>Correlation and both regression lines</td>
          <td>\(b_{yx}b_{xy} = r^{2}\); why there are two lines</td></tr>
      <tr><td>11</td><td>Tests for means, variances, correlations</td>
          <td>seven tests, the tail areas computed, and the order to run them in</td></tr>
      <tr><td>12</td><td>One-way and two-way analysis of variance</td>
          <td>the correction factor route, and error by subtraction as a check</td></tr>
    </table>
    <p><strong>Every output shown below is the output these programs actually produce.</strong>
    This page is built by running each programme, as listed, in Python {version}; the text under
    each is what it printed, unchanged. Save <code>tails.py</code> in the same folder as the
    others, since programs 8, 9, 11 and 12 import it.</p>
  </div>

"""

PRACTICALS = [
    dict(
        n=0, title="The Tail Areas, Written Once", file="tails.py",
        question=r"""  <p>Without a statistical package or a printed table, write a module <code>tails.py</code>
  that returns \(P(|T_\nu| &gt; t)\), \(P(F_{d_1,d_2} &gt; f)\), \(P(\chi^{2}_\nu &gt; q)\) and
  \(P(|Z| &gt; z)\), and check it at the published 5% points \(t_{10} = 2.228\),
  \(F_{5,10} = 3.326\), \(\chi^{2}_{8} = 15.507\) and \(z = 1.959964\).</p>""",
        aim=r"""Compute the four tail areas that programs 8, 9, 11 and 12 need, once, so that each of
        them can import them. <strong>Write this file first and keep it beside the others</strong>;
        in the examination it is the single piece of code worth having memorised in outline.""",
        steps=[
            r"""Evaluate the continued fraction for the incomplete beta function by Lentz's method,
            stopping when a term changes the value by less than \(3\times10^{-16}\).""",
            r"""Multiply it by the front factor \(x^{a}(1-x)^{b}/\{a\,B(a,b)\}\), using
            \(I_x(a,b) = 1 - I_{1-x}(b,a)\) when \(x\) is past \((a+1)/(a+b+2)\), where the
            fraction converges fastest.""",
            r"""Both are one incomplete beta, by the two identities in the method box.""",
            r"""The \(\chi^{2}\) tail is the upper incomplete gamma function at \(\nu/2\) and
            \(q/2\): by the series for the lower part when \(q/2 &lt; \nu/2 + 1\), and by the
            continued fraction for the upper part when \(q/2\) is larger, so that a very small
            tail is computed directly.""",
            r"""\(P(|Z| &gt; z) = \operatorname{erfc}\!\left(|z|/\sqrt2\right)\), from the standard
            library.""",
            r"""Print each function at a published 5% point. Every line must show 0.0500.""",
        ],
        method=r"""    <p>Four programs need \(P(|T| &gt; t)\), \(P(F &gt; f)\), \(P(\chi^{2} &gt; q)\) or
    \(P(|Z| &gt; z)\), and no package may supply them. Two facts make it possible at all:</p>
    \[ P\!\left(|T_\nu| &gt; t\right) = I_{\frac{\nu}{\nu+t^{2}}}\!\left(\frac{\nu}{2},
       \frac{1}{2}\right), \qquad
       P\!\left(F_{d_1,d_2} &gt; f\right)
       = I_{\frac{d_2}{d_2+d_1f}}\!\left(\frac{d_2}{2}, \frac{d_1}{2}\right), \]
    <p>so a single incomplete beta function \(I_x(a,b)\) delivers both the \(t\) and the \(F\)
    tail; and the \(\chi^{2}\) tail is the incomplete gamma function, which its own series and
    continued fraction supply.</p>""",
        commands=[
            ("<code>math.lgamma(x)</code>", r"\(\ln\Gamma(x)\), for the front factors without overflow"),
            ("<code>math.exp</code>, <code>math.log</code>", "the front factors, built on the log scale"),
            ("<code>math.erfc(x)</code>", r"the complementary error function, \(1 - \operatorname{erf}(x)\)"),
            ("<code>for m in range(1, 300): ... break</code>", "iterate the continued fraction until it has converged"),
            ('<code>if __name__ == "__main__":</code>', "run the check only when the file is run, not when another program imports it"),
        ],
        notes=[
            r"""<strong>Corrected.</strong> The first version of <code>chi2_upper</code> computed every
    tail as 1 minus the series for the lower part. Below about \(10^{-13}\) that subtraction
    loses all its digits: it printed \(p = 1.332\times10^{-15}\) for the exponential fit in
    Practical 9, where the true value is \(3.99\times10^{-56}\), and \(5.773\times10^{-15}\) for
    the Poisson fit in Practical 8, where it is \(7.889\times10^{-15}\). Step 4 now uses the
    continued fraction for the upper tail. Rechecked against SciPy for \(\nu\) from 1 to 100,
    all four functions agree to a relative error below \(2\times10^{-13}\). No decision changes:
    both fits are rejected either way.""",
        ],
        conclusion=r"""    <p>All four functions return 0.0500 at the published 5% points, so programs 8, 9, 11 and
    12 take their \(p\) values from this module instead of a table.</p>""",
    ),
    dict(
        n=1, title="Sum and Product of Two Matrices", file="p1.py",
        question=r"""  <p>Without packages, write a program to find \(A + B\), \(AB\) and \(BA\) for</p>
  \[ A = \begin{pmatrix}2 &amp; 1 &amp; 1\\ 1 &amp; 3 &amp; 2\\ 1 &amp; 0 &amp; 4\end{pmatrix}, \qquad
     B = \begin{pmatrix}1 &amp; 0 &amp; 2\\ 2 &amp; 1 &amp; 0\\ 0 &amp; 3 &amp; 1\end{pmatrix}, \]
  <p>and decide whether \(AB = BA\).</p>""",
        aim="Add and multiply two matrices, and show that matrix multiplication does not commute.",
        steps=[
            "A matrix is stored as a list of rows: the rows are <code>len(M)</code>, the columns <code>len(M[0])</code>.",
            "Refuse unless the two shapes agree, then add entry by entry.",
            r"Refuse unless the columns of \(A\) equal the rows of \(B\); each entry of the product is the inner product of a row of \(A\) with a column of \(B\).",
            "Print each row with its entries in fixed-width columns.",
            r"Store \(A\) and \(B\) as lists of rows.",
            r"Print \(A + B\), \(AB\) and \(BA\), and compare the two products.",
        ],
        method=r"""    <p><strong>What has to be written out.</strong> Addition is elementwise and needs the two
    matrices to have the same shape. Multiplication needs the columns of \(A\) to equal the rows of
    \(B\), and each entry is an inner product:</p>
    \[ (AB)_{ij} = \sum_{k=1}^{c}A_{ik}B_{kj}. \]
    <p>Both shape conditions are checked before any arithmetic, because a silent shape mismatch in
    Python produces a wrong answer rather than an error.</p>""",
        commands=[
            ("<code>[[... for j in ...] for i in ...]</code>", "a list comprehension that builds the matrix row by row"),
            ("<code>sum(A[i][k] * B[k][j] for k in range(ca))</code>", "the inner product for one entry"),
            ("<code>raise ValueError(...)</code>", "stop with a message when the shapes do not fit"),
            ('<code>f"{v:6.2f}"</code>', "print a number in 6 columns with 2 decimals"),
            ("<code>==</code> on two lists", "true only if every entry agrees"),
        ],
        conclusion=r"""    <p>\(A + B\), \(AB\) and \(BA\) are printed above. The program prints <code>False</code> for
    \(AB = BA\): the \((1,3)\) entry, for one, is 5 in \(AB\) and 9 in \(BA\). Matrix
    multiplication does not commute, even for two square matrices of the same order.</p>""",
    ),
    dict(
        n=2, title="Determinant and Inverse of a Matrix", file="p2.py",
        question=r"""  <p>For the matrix \(A\) of Practical 1, find \(\det(A)\) by cofactor expansion and
  \(A^{-1}\) by the adjoint, in exact fractions, and check that \(AA^{-1} = I\). Then show that</p>
  \[ S = \begin{pmatrix}1 &amp; 2 &amp; 3\\ 2 &amp; 4 &amp; 6\\ 1 &amp; 0 &amp; 1\end{pmatrix} \]
  <p>has no inverse.</p>""",
        aim="Compute a determinant by cofactor expansion and an inverse by the adjoint, in exact arithmetic, and detect a singular matrix.",
        steps=[
            r"The minor \(M_{ij}\) is the matrix with row \(i\) and column \(j\) deleted.",
            r"Expand along the first row, recursively, down to the \(2\times2\) case.",
            r"Refuse if \(\det = 0\). Otherwise form the cofactors, <strong>transpose</strong> them to get the adjoint, and divide by the determinant as a <code>Fraction</code>.",
            "Print each entry right-aligned, as a fraction.",
            r"Print \(\det(A)\) and \(A^{-1}\).",
            r"Multiply \(A\) by \(A^{-1}\); the product must be the identity exactly.",
            r"Find \(\det(S)\), which is 0.",
        ],
        method=r"""    <p><strong>The two formulae.</strong> Expanding along the first row,</p>
    \[ \det(A) = \sum_{j=1}^{n}(-1)^{1+j}a_{1j}\det\!\left(M_{1j}\right), \]
    <p>where \(M_{1j}\) is \(A\) with row 1 and column \(j\) deleted; and</p>
    \[ A^{-1} = \frac{1}{\det(A)}\operatorname{adj}(A), \qquad
       \operatorname{adj}(A) = \left[(-1)^{i+j}\det\!\left(M_{ij}\right)\right]^{\mathsf T}. \]
    <p><strong>The transpose in the adjoint is the step that is most often dropped</strong>, and
    for a symmetric matrix dropping it makes no difference &mdash; which is exactly why the test
    matrix below is <em>not</em> symmetric.</p>
    <p>Using <code>Fraction</code> rather than <code>float</code> makes the check
    \(AA^{-1} = I\) come out exactly, with no rounding to interpret.</p>""",
        commands=[
            ("<code>from fractions import Fraction</code>", "exact rational arithmetic"),
            ("<code>Fraction(cof[j][i], d)</code>", r"the \((i,j)\) entry of the inverse: note the swapped indices, which is the transpose"),
            ("<code>det(minor(M, 0, j))</code>", "a function that calls itself on a smaller matrix (recursion)"),
            ("<code>(-1) ** (i + j)</code>", "the sign of a cofactor"),
        ],
        conclusion=r"""    <p>\(\det(A) = 19\), and every entry of \(A^{-1}\) is a multiple of \(1/19\); the product
    \(AA^{-1}\) is the identity exactly. \(\det(S) = 0\) because its second row is twice its
    first, so \(S\) is singular and has no inverse.</p>""",
    ),
    dict(
        n=3, title="Four Sorts and Two Searches", file="p3.py",
        question=r"""  <p>Sort the ten numbers 42, 17, 93, 8, 55, 23, 71, 4, 66, 30 by bubble, insertion, merge
  and quick sort, counting the comparisons where the method allows it; then search the sorted
  list for 66 and for 50 by linear and by binary search, and compare the work each one does.</p>""",
        aim="Implement bubble, insertion, merge and quick sort, and linear and binary search, and count the comparisons each one uses.",
        steps=[
            "Swap adjacent out-of-order pairs, pass after pass; stop early if a pass makes no swap.",
            "Grow a sorted prefix, sliding each new key back to its place.",
            "Split the list in two, sort each half, and merge the two sorted halves.",
            "Partition about the middle element into smaller, equal and larger, and sort each side.",
            "Linear search scans from the start; binary search halves the interval each time, and returns the position and the comparisons used.",
            "Run all four sorts on the same data and check that they agree.",
            "Search the sorted list for a value that is there (66) and one that is not (50).",
        ],
        method=r"""    <table>
      <tr><th>Method</th><th>Idea</th><th>Comparisons</th></tr>
      <tr><td>Bubble</td><td>repeatedly swap adjacent out-of-order pairs</td>
          <td>\(O(n^{2})\); \(O(n)\) if already sorted, using the early exit</td></tr>
      <tr><td>Insertion</td><td>grow a sorted prefix, sliding each new key back into it</td>
          <td>\(O(n^{2})\) worst, \(O(n)\) best &mdash; usually beats bubble</td></tr>
      <tr><td>Merge</td><td>split, sort each half, merge</td>
          <td>\(O(n\log n)\) always; needs extra space</td></tr>
      <tr><td>Quick</td><td>partition about a pivot, recurse on each side</td>
          <td>\(O(n\log n)\) expected, \(O(n^{2})\) on a bad pivot</td></tr>
      <tr><td>Linear search</td><td>scan</td><td>\(O(n)\); works on unsorted data</td></tr>
      <tr><td>Binary search</td><td>halve the interval</td>
          <td>\(O(\log n)\); <strong>requires sorted data</strong></td></tr>
    </table>""",
        commands=[
            ("<code>a = a[:]</code>", "work on a copy, so the caller's list is not changed"),
            ("<code>a[j], a[j + 1] = a[j + 1], a[j]</code>", "swap two entries in one statement"),
            ("<code>return a, comps</code>", "return two values, as a tuple"),
            ("<code>(lo + hi) // 2</code>", "the middle position, by integer division"),
            ("<code>enumerate(a)</code>", "each position together with its value"),
        ],
        reading=r"""  <p>The comparison counts in the output are the point of the exercise: on the same ten numbers
  bubble sort used 44 comparisons and insertion sort 29, and binary search found the target in
  2 comparisons where linear search needed 8. The search for 50 returns position \(-1\): it is
  not in the list, and binary search established that in 4 comparisons.</p>""",
        conclusion=r"""    <p>All four sorts give 4, 8, 17, 23, 30, 42, 55, 66, 71, 93. Insertion sort used fewer
    comparisons than bubble sort (29 against 44), and binary search found 66 at position 7 in 2
    comparisons against linear search's 8 &mdash; but only because the list had been sorted
    first.</p>""",
    ),
    dict(
        n=4, title="Median and Mode of an Array", file="p4.py",
        question=r"""  <p>Find the median of 7, 3, 9, 3, 5, 8, 3, 9, 4 (odd \(n\)) and of 12, 4, 9, 4, 15, 7
  (even \(n\)); find the mode of the first, of 2, 5, 2, 7, 5, 9, and of 4, 6, 9, 11.</p>""",
        aim="Compute the median and the mode from first principles, and handle the two cases a library routine hides.",
        steps=[
            r"Sort; take the middle value if \(n\) is odd, and the mean of the two middle values if \(n\) is even.",
            "Count each value in a dictionary in one pass, find the largest count, and keep every value that reaches it.",
            "Enter an odd-length array, an even-length one, a bimodal one and one with no repeats.",
            "Print both medians.",
            "Print the modes, and say what each result means.",
        ],
        method=r"""    <p><strong>Median.</strong> Sort, then take the middle value if \(n\) is odd and the mean of
    the two middle values if \(n\) is even. Note the indices: for even \(n\) they are
    \(n/2 - 1\) and \(n/2\) in Python's zero-based numbering, not \(n/2\) and \(n/2 + 1\).</p>
    <p><strong>Mode.</strong> Build a frequency dictionary in one pass, then take every value
    attaining the maximum count. Two cases matter and both appear in the output:</p>
    <ul>
      <li><strong>Several modes.</strong> The data can be bimodal, and the honest answer is the
      list, not the first one found.</li>
      <li><strong>No repeats.</strong> Every value occurs once. The mode is then
      <em>undefined</em>; reporting all four values as modes is wrong, because the mode is meant
      to be the most frequent value and no value is more frequent than another.</li>
    </ul>""",
        commands=[
            ("<code>sorted(a)</code>", "a sorted copy of the list"),
            ("<code>n // 2</code>, <code>n % 2</code>", "the middle position, and whether \\(n\\) is odd"),
            ("<code>freq.get(v, 0) + 1</code>", "add one to a value's count, starting from 0"),
            ("<code>max(freq.values())</code>", "the largest count"),
        ],
        reading=r"""  <p>The last line prints the four values, but the program's own message says what they
  mean: each occurs once, so the data has no mode.</p>""",
        conclusion=r"""    <p>The medians are 5 (odd \(n = 9\)) and 8.0 (even \(n = 6\), the mean of 7 and 9). The
    mode of the first array is 3, occurring 3 times. The second set is bimodal, with modes 2 and 5;
    in the last set no value repeats, so the mode is undefined.</p>""",
    ),
    dict(
        n=5, title="Frequency Table, and the Five Summaries From It", file="p5.py",
        question=r"""  <p>Group the forty values below into the classes 10&ndash;20, 20&ndash;30, &hellip;,
  50&ndash;60. From the table, find the mean, median, mode, variance and standard deviation; find
  the same from the raw values, and the grouping error in the mean.</p>
  <p>23, 45, 12, 37, 52, 28, 41, 19, 33, 47, 55, 26, 38, 44, 31, 17, 49, 35, 22, 40,
  29, 51, 36, 43, 25, 48, 32, 39, 27, 46, 34, 21, 42, 30, 53, 24, 37, 45, 33, 41</p>""",
        aim="Build a grouped frequency table and compute the mean, median, mode, variance and standard deviation from it &mdash; then compute the same quantities from the raw values and measure the grouping error.",
        steps=[
            "Store the forty values as a list.",
            "Count the values into five classes of width 10 from 10; a value on the top edge goes in the last class.",
            r"Mid-points, then \(\sum f_im_i/n\).",
            "Find the class that holds the \\(n/2\\)th value, and interpolate within it.",
            "The modal class and its two neighbours, in the mode formula.",
            "Print the table, then the five grouped summaries.",
            "Compute the mean, median and variance from the raw values, and the grouping error in the mean.",
            "The two middle classes tie at 12, so apply the formula to the other of them too.",
        ],
        method=r"""    <p><strong>The grouped formulae.</strong> With class mid-points \(m_i\), frequencies
    \(f_i\) and \(n = \sum f_i\),</p>
    \[ \bar x = \frac{\sum f_im_i}{n}, \qquad
       s^{2} = \frac{\sum f_i\left(m_i - \bar x\right)^{2}}{n}, \]
    \[ \text{median} = L + \frac{n/2 - c}{f}\,h, \qquad
       \text{mode} = L + \frac{f_1 - f_0}{2f_1 - f_0 - f_2}\,h, \]
    <p>where \(L\) is the lower boundary of the class containing the item, \(c\) the cumulative
    frequency before it, \(f\) its frequency, \(h\) the width, and \(f_0, f_1, f_2\) the
    frequencies of the class before the modal class, the modal class and the class after.</p>""",
        commands=[
            ("<code>int((v - low) // width)</code>", "the class a value falls in"),
            ("<code>[0] * k</code>", "a list of \\(k\\) zero counts"),
            ("<code>zip(mids, counts)</code>", "pair each mid-point with its frequency"),
            ("<code>counts.index(max(counts))</code>", "the first class with the largest frequency"),
            ("<code>math.sqrt</code>", "the standard deviation from the variance"),
        ],
        reading=r"""  <p><strong>Two things the output shows that a formula sheet does not.</strong> First, the
  grouped mean is \(36.25\) against a raw mean of \(35.75\): grouping replaces every value by
  its class mid-point and the error does not vanish. Second, the two middle classes tie at
  12 observations, so the modal class is not unique &mdash; and applying the formula to either
  of them returns the same number, \(40\), the boundary they share.</p>""",
        conclusion=r"""    <p>From the table: mean 36.25, median 36.67, mode 40, variance 120.94, standard deviation
    11.00. From the raw values: mean 35.75, median 36.5, variance 113.24, standard deviation 10.64.
    Grouping has moved the mean by \(+0.50\) and inflated the variance; the mode is 40 whichever of
    the two tied classes is used.</p>""",
    ),
    dict(
        n=6, title="Four Moments, Skewness and Kurtosis", file="p6.py",
        question=r"""  <p>For 12, 15, 11, 18, 22, 14, 16, 19, 13, 25, 17, 20, 14, 16, 21, find the first four
  raw moments, convert them to central moments, check the conversion by computing the central
  moments directly, and find \(\beta_1\), \(\gamma_1\), \(\beta_2\) and \(\gamma_2\).</p>""",
        aim="Compute the first four raw moments, convert them to central moments, and from those the two shape coefficients.",
        steps=[
            r"\(m_r' = \frac{1}{n}\sum x_i^{r}\) for \(r = 1, \dots, 4\).",
            "Convert by the three formulae in the method box.",
            "Compute the same central moments from the deviations about the mean.",
            "Print both sets and confirm that they agree.",
            "Compute the four coefficients and say what the signs mean.",
        ],
        method=r"""    <p><strong>The conversion, which is the examinable part.</strong> Writing
    \(m_r' = \frac{1}{n}\sum x_i^{r}\) for the raw moments about the origin,</p>
    \[ \mu_2 = m_2' - m_1'^{2}, \qquad
       \mu_3 = m_3' - 3m_1'm_2' + 2m_1'^{3}, \]
    \[ \mu_4 = m_4' - 4m_1'm_3' + 6m_1'^{2}m_2' - 3m_1'^{4}, \]
    <p>and then</p>
    \[ \beta_1 = \frac{\mu_3^{2}}{\mu_2^{3}}, \quad \gamma_1 = \frac{\mu_3}{\mu_2^{3/2}},
       \qquad \beta_2 = \frac{\mu_4}{\mu_2^{2}}, \quad \gamma_2 = \beta_2 - 3. \]
    <p>The program computes the central moments <em>both</em> ways &mdash; through the conversion
    and directly from the deviations &mdash; and reports that they agree. That is the check worth
    writing into the record, because the conversion formulae are easy to mis-copy and a
    mis-copied \(\mu_3\) changes the sign of the skewness without changing anything that looks
    wrong.</p>
    <p>Note also why \(\gamma_1\) is preferred to \(\beta_1\): squaring throws the sign away, so
    \(\beta_1\) says how skew the data is but not which way.</p>""",
        commands=[
            ("<code>sum(v ** r for v in x) / n</code>", "the \\(r\\)th raw moment"),
            ("<code>m1, m2, m3, m4 = m</code>", "unpack a list into four names"),
            ("<code>max(abs(a - b) ...) &lt; 1e-8</code>", "the two routes agree, allowing for rounding"),
            ('<code>... if g1 &gt; 0 else ...</code>', "choose the message by the sign"),
        ],
        conclusion=r"""    <p>The central moments are \(\mu_2 = 14.6489\), \(\mu_3 = 23.7286\) and
    \(\mu_4 = 506.5591\) by both routes. \(\gamma_1 = +0.4232\), so the data is positively skewed,
    with the long tail to the right; \(\beta_2 = 2.3606 &lt; 3\) (\(\gamma_2 = -0.6394\)), so it is
    platykurtic, flatter than the normal.</p>""",
    ),
    dict(
        n=7, title="Random Numbers from Five Distributions", file="p7.py",
        question=r"""  <p>Starting from a uniform generator written out in full, generate 20,000 values from each
  of \(U(2,8)\), Bin\((10, 0.3)\), Poisson\((4)\), \(N(5, 2^{2})\) and Exp\((0.5)\), and compare
  each sample's mean and variance with the theoretical ones.</p>""",
        aim="Generate samples from the uniform, binomial, Poisson, normal and exponential distributions using the algorithms, not a library.",
        steps=[
            r"Lehmer's generator \(x_{k+1} = 16807x_k \bmod (2^{31}-1)\), divided by the modulus, as a class that keeps its own state.",
            r"\(a + (b-a)U\); a Bernoulli is \(1\) if \(U &lt; p\); a binomial is the sum of \(n\) Bernoullis.",
            r"Multiply uniforms until the product falls to \(e^{-\lambda}\) or below; the number of factors before that is the value.",
            r"\(\mu + \sigma\sqrt{-2\ln U_1}\cos(2\pi U_2)\), keeping one of the pair.",
            r"\(-\ln(U)/\lambda\).",
            "Print the sample mean and variance beside the theoretical ones.",
            "Draw 20,000 values from each distribution and compare.",
        ],
        method=r"""    <p><strong>The base generator.</strong> Everything rests on a stream of \(U(0,1)\) values,
    here Lehmer's minimal standard generator \(x_{k+1} = 16807x_k \bmod (2^{31}-1)\), whose output
    divided by the modulus is uniform on \((0,1)\). It is <em>deterministic</em>: the same seed
    gives the same stream, which is what makes the output below reproducible.</p>
    <table>
      <tr><th>Distribution</th><th>Algorithm</th><th>Why it works</th></tr>
      <tr><td>\(U(a,b)\)</td><td>\(a + (b-a)U\)</td><td>inverse transform, the c.d.f. being linear</td></tr>
      <tr><td>Bernoulli\((p)\)</td><td>\(1\) if \(U &lt; p\)</td><td>\(P(U &lt; p) = p\)</td></tr>
      <tr><td>Bin\((n,p)\)</td><td>sum \(n\) Bernoullis</td><td>the definition of the binomial</td></tr>
      <tr><td>Poisson\((\lambda)\)</td><td>multiply uniforms until the product falls below
          \(e^{-\lambda}\)</td>
          <td>equivalent to counting exponential inter-arrivals inside one unit of time</td></tr>
      <tr><td>\(N(\mu,\sigma^{2})\)</td>
          <td>\(\mu + \sigma\sqrt{-2\ln U_1}\cos(2\pi U_2)\)</td>
          <td>Box&ndash;Muller: the polar form of a bivariate standard normal</td></tr>
      <tr><td>Exp\((\lambda)\)</td><td>\(-\ln(U)/\lambda\)</td>
          <td>inverse transform on \(F(x) = 1 - e^{-\lambda x}\)</td></tr>
    </table>""",
        commands=[
            ("<code>class LCG:</code> &hellip; <code>self.x</code>", "a class whose object remembers where the stream has got to"),
            ("<code>(16807 * self.x) % 2147483647</code>", r"the next value, modulo \(2^{31}-1\)"),
            ("<code>while True:</code> &hellip; <code>return k</code>", "loop until the condition is met, then leave the function"),
            ("<code>math.log</code>, <code>math.cos</code>, <code>math.pi</code>", "Box&ndash;Muller and the inverse transforms"),
            ("<code>[uniform(2, 8) for _ in range(N)]</code>", "a sample of \\(N\\) values"),
        ],
        reading=r"""  <p><strong>The verification is the exercise.</strong> Generating numbers is easy; showing they
  come from the right distribution is the work. Each sample's mean and variance are printed
  beside the theoretical values, and all five agree to about two decimal places at
  \(n = 20{,}000\) &mdash; which is the accuracy a Monte Carlo standard error of
  \(\sigma/\sqrt{n}\) predicts. Here \(\sigma/\sqrt{n}\) is between 0.010 and 0.014, and the
  largest gap in a mean, the Poisson's 0.0315, is about two standard errors.</p>""",
        conclusion=r"""    <p>All five samples have means and variances close to the theory: for example
    Bin\((10, 0.3)\) gives mean 3.0009 and variance 2.0996 against 3 and 2.1. The algorithms
    generate the distributions they claim to, within sampling error.</p>""",
    ),
    dict(
        n=8, title="Fitting Binomial, Poisson and Negative Binomial", file="p8.py",
        question=r"""  <p>Fit a binomial, a Poisson and a negative binomial distribution to the frequency
  distribution below, test each fit by \(\chi^{2}\), and say which describes the data.</p>
  <table>
    <tr><th>\(x\)</th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr>
    <tr><th>\(f\)</th><td>447</td><td>132</td><td>42</td><td>21</td><td>3</td><td>2</td></tr>
  </table>""",
        aim="Fit all three discrete distributions to one data set, test each fit, and let the test choose.",
        steps=[
            "Store the counts and frequencies; print \\(n\\), the mean, the variance and the variance-to-mean ratio.",
            "The three probability functions, the binomial coefficient written out.",
            "Estimate each distribution's parameters by the method of moments.",
            r"Multiply each probability by \(n\); for the two unbounded fits the last class takes the whole upper tail.",
            "Pool the upper classes until every expected frequency is at least 5, then compute \\(\\chi^{2}\\) and its degrees of freedom.",
            "Print each \\(\\chi^{2}\\), its degrees of freedom and its \\(p\\) value from <code>tails.py</code>.",
            "Draw the observed frequencies against the negative binomial fit in characters.",
        ],
        method=r"""    <p><strong>Read the data before fitting anything.</strong> The variance-to-mean ratio is
    \(1.4849\). For a Poisson it should be 1; for a binomial it must be
    <em>below</em> 1, since \(npq &lt; np\); above 1 means <strong>over-dispersion</strong>, which
    is the negative binomial's territory. The answer is visible before a single expected frequency
    is computed, and the tests below only confirm it.</p>
    <table>
      <tr><th>Fit</th><th>Estimates</th><th>Constraint on the variance</th></tr>
      <tr><td>Binomial \((N, p)\)</td><td>\(N\) fixed by the largest possible count,
          \(\hat p = \bar x/N\)</td><td>\(\sigma^{2} &lt; \mu\)</td></tr>
      <tr><td>Poisson \((\lambda)\)</td><td>\(\hat\lambda = \bar x\)</td>
          <td>\(\sigma^{2} = \mu\)</td></tr>
      <tr><td>Negative binomial \((r, p)\)</td>
          <td>\(\hat p = \bar x/s^{2}\), \(\hat r = \bar x^{2}/(s^{2}-\bar x)\)</td>
          <td>\(\sigma^{2} &gt; \mu\)</td></tr>
    </table>
    <p><strong>The goodness-of-fit test.</strong>
    \(\chi^{2} = \sum (O_i - E_i)^{2}/E_i\) on
    \(k - 1 - (\text{parameters estimated})\) degrees of freedom, after pooling the upper tail
    until every expected frequency reaches 5. <strong>Both adjustments matter</strong>: without
    pooling, a class with \(E = 0.08\) contributes a huge term that is pure noise; without
    subtracting the estimated parameters the degrees of freedom are too many and every fit looks
    better than it is.</p>""",
        commands=[
            ("<code>from tails import chi2_upper</code>", "the \\(\\chi^{2}\\) tail area from Practical 0"),
            ("<code>math.factorial</code>", "the factorials in the binomial coefficient and the Poisson"),
            ("<code>fits = {...}</code>", "a dictionary of the three lists of expected frequencies, keyed by name"),
            ("<code>e.pop()</code>, then <code>e[-1] += ...</code>", "pool the last class into the one before it (pop first, then add)"),
            ('<code>"#" * k</code>', "a bar of \\(k\\) characters, since no plotting package is permitted"),
        ],
        reading=r"""  <p>The negative binomial pays two degrees of freedom and still wins comfortably. The last
  block draws the comparison with characters, since no plotting package is permitted &mdash; and
  it is enough to see that the fit tracks the observed counts.</p>""",
        conclusion=r"""    <p>The variance-to-mean ratio is 1.4849, so the data is over-dispersed. The binomial
    (\(\chi^{2} = 41.67\) on 1 df) and the Poisson (\(\chi^{2} = 64.95\) on 2 df) are both
    rejected, with \(p\) values below \(10^{-9}\). The negative binomial, with \(\hat r = 0.9593\)
    and \(\hat p = 0.6734\), gives \(\chi^{2} = 4.13\) on 2 df, \(p = 0.127\): it fits, and it is
    the distribution that describes these data.</p>""",
    ),
    dict(
        n=9, title="Fitting Normal, Exponential and Cauchy", file="p9.py",
        question=r"""  <p>Fit a normal, an exponential and a Cauchy distribution to the grouped data below, test
  each fit by \(\chi^{2}\), and say which describes the data.</p>
  <table>
    <tr><th>Class</th><td>10&ndash;20</td><td>20&ndash;30</td><td>30&ndash;40</td><td>40&ndash;50</td><td>50&ndash;60</td><td>60&ndash;70</td><td>70&ndash;80</td></tr>
    <tr><th>\(f\)</th><td>9</td><td>15</td><td>37</td><td>55</td><td>36</td><td>17</td><td>6</td></tr>
  </table>""",
        aim="Fit three continuous distributions to one grouped data set and test each.",
        steps=[
            "Store the class edges and frequencies; compute the mean and standard deviation from the mid-points.",
            "The median and the quartiles by interpolation in the grouped distribution, and half the interquartile range.",
            "The normal, exponential and Cauchy distribution functions.",
            r"\(\bar x\) and \(s\) for the normal, \(1/\bar x\) for the exponential, the median and half the interquartile range for the Cauchy.",
            r"\(n[F(b) - F(a)]\) for each class, the two outer classes opened to \(\pm\infty\), printed beside the observed.",
            "\\(\\chi^{2}\\) for each fit, its degrees of freedom and its \\(p\\) value from <code>tails.py</code>.",
        ],
        method=r"""    <p><strong>Expected frequencies come from the c.d.f., not the density.</strong> For a class
    \((a, b]\),</p>
    \[ E = n\left[F(b) - F(a)\right], \]
    <p>and the two outer classes are opened to \(\pm\infty\) so that the probabilities sum to
    exactly 1. Using \(n\,h\,f(m)\) with the density at the mid-point is an approximation that
    leaves the expected frequencies not quite summing to \(n\), and the resulting \(\chi^{2}\) is
    not the one the test assumes.</p>
    <table>
      <tr><th>Distribution</th><th>\(F(x)\)</th><th>Fitted by</th></tr>
      <tr><td>Normal</td><td>\(\tfrac12\left[1 + \operatorname{erf}\!\left(
          \frac{x-\mu}{\sigma\sqrt2}\right)\right]\)</td><td>\(\bar x\) and \(s\)</td></tr>
      <tr><td>Exponential</td><td>\(1 - e^{-\lambda x}\)</td><td>\(\hat\lambda = 1/\bar x\)</td></tr>
      <tr><td>Cauchy</td><td>\(\tfrac12 + \tfrac1\pi\arctan\!\left(\frac{x-x_0}{\gamma}\right)\)</td>
          <td>the median and half the interquartile range</td></tr>
    </table>
    <p><strong>Why the Cauchy is fitted differently.</strong> It has no mean and no variance
    &mdash; the defining integrals diverge &mdash; so the method of moments does not merely
    perform badly, it does not exist. The median estimates the location \(x_0\) and half the
    interquartile range estimates the scale \(\gamma\), because for a Cauchy the quartiles are
    exactly \(x_0 \pm \gamma\).</p>""",
        commands=[
            ("<code>math.erf</code>", "the error function, for the normal c.d.f."),
            ("<code>math.atan</code>", "the arctangent, for the Cauchy c.d.f."),
            ("<code>def expected(cdf, *args)</code>", "one function for all three fits: the c.d.f. is passed in as an argument"),
            ("<code>from tails import chi2_upper</code>", "the \\(\\chi^{2}\\) tail area from Practical 0"),
        ],
        reading=r"""  <p>The output rejects the exponential outright, rejects the Cauchy at \(p = 0.00007\) because
  its tails are far too heavy for this data, and accepts the normal at \(p = 0.637\).</p>""",
        notes=[r"""<strong>Corrected.</strong> The exponential's \(p\) value was printed as
    \(1.332\times10^{-15}\), the floor of the old <code>chi2_upper</code>; the true value is
    \(3.99\times10^{-56}\) (see the note in Practical 0). The decision is the same."""],
        conclusion=r"""    <p>The normal with \(\mu = 44.66\) and \(\sigma = 13.85\) fits: \(\chi^{2} = 2.54\) on 4 df,
    \(p = 0.637\). The exponential (\(\chi^{2} = 269.28\) on 5 df) and the Cauchy
    (\(\chi^{2} = 24.28\) on 4 df, \(p = 0.00007\)) are rejected. The data is described by the
    normal distribution.</p>""",
    ),
    dict(
        n=10, title="Correlation and Both Regression Lines", file="p10.py",
        question=r"""  <p>For the ten pairs below, find the correlation coefficient and both regression lines,
  verify that \(b_{yx}b_{xy} = r^{2}\) and that both lines pass through \((\bar x, \bar y)\), find
  the angle between the lines, and predict \(y\) at \(x = 69\).</p>
  <table>
    <tr><th>\(x\)</th><td>65</td><td>63</td><td>67</td><td>64</td><td>68</td><td>62</td><td>70</td><td>66</td><td>68</td><td>67</td></tr>
    <tr><th>\(y\)</th><td>68</td><td>66</td><td>68</td><td>65</td><td>69</td><td>66</td><td>68</td><td>65</td><td>71</td><td>67</td></tr>
  </table>""",
        aim="Compute the correlation coefficient and <em>both</em> regression lines, and verify the three relations between them.",
        steps=[
            r"Store \(x\) and \(y\); compute the means, \(S_{xx}\), \(S_{yy}\) and \(S_{xy}\).",
            r"\(r = S_{xy}/\sqrt{S_{xx}S_{yy}}\).",
            r"The two slopes and intercepts; check \(b_{yx}b_{xy} = r^{2}\), and evaluate each line at the other's mean.",
            r"\(\tan\theta = \left|\frac{m_2 - m_1}{1 + m_1m_2}\right|\) with \(m_1 = b_{yx}\) and \(m_2 = 1/b_{xy}\), the slopes of the two lines in the \((x, y)\) plane.",
            r"\(\sqrt{(S_{yy} - b_{yx}S_{xy})/(n-2)}\), and the line \(y\) on \(x\) at \(x = 69\).",
        ],
        method=r"""    \[ r = \frac{S_{xy}}{\sqrt{S_{xx}S_{yy}}}, \qquad
       b_{yx} = \frac{S_{xy}}{S_{xx}}, \qquad b_{xy} = \frac{S_{xy}}{S_{yy}}, \]
    <p>and the three facts the program checks:</p>
    <ol>
      <li><strong>\(b_{yx}b_{xy} = r^{2}\)</strong>, so the correlation is the geometric mean of
      the two regression coefficients.</li>
      <li><strong>Both lines pass through \(\left(\bar x, \bar y\right)\)</strong>, which the
      output confirms by evaluating each at the other's mean.</li>
      <li><strong>The angle between them measures the correlation.</strong> It is zero when
      \(|r| = 1\) &mdash; the two lines coincide &mdash; and a right angle when \(r = 0\).</li>
    </ol>""",
        commands=[
            ("<code>zip(x, y)</code>", "pair each \\(x\\) with its \\(y\\)"),
            ("<code>math.sqrt</code>", "the square roots in \\(r\\) and the residual sd"),
            ("<code>math.atan</code>, <code>math.degrees</code>", "the angle between the lines, in degrees"),
        ],
        reading=r"""  <p>\(b_{yx}b_{xy}\) and \(r^{2}\) both come out to \(0.405541\), and the angle between the
  lines is \(24.19^{\circ}\).</p>
  <p><strong>The two lines are not the same line, and neither is "the" line.</strong>
  \(y\) on \(x\) minimises vertical deviations and is the one to use for predicting \(y\);
  \(x\) on \(y\) minimises horizontal deviations. Predicting \(x\) from the first by rearranging
  it is a standard and serious error.</p>""",
        conclusion=r"""    <p>\(r = 0.6368\), a moderate positive correlation. The line of \(y\) on \(x\) is
    \(y = 35.4786 + 0.4821x\) and of \(x\) on \(y\) is \(x = 9.3925 + 0.8411y\); they meet at
    \((66, 67.3)\) at an angle of \(24.19^{\circ}\). The predicted \(y\) at \(x = 69\) is 68.75.</p>""",
    ),
    dict(
        n=11, title="Testing Means, Variances and Correlations", file="p11.py",
        question=r"""  <p>Carry out, at the 5% level:</p>
  <ol>
    <li>a test of \(\mu = 50\) for 48, 52, 55, 49, 53, 51, 47, 54, 50, 52, 56, 50;</li>
    <li>a test of equal means for A: 23, 27, 25, 29, 24, 26, 28 and B: 31, 28, 33, 30, 35, 29;</li>
    <li>a paired test for eight subjects measured before (72, 68, 75, 70, 66, 74, 69, 71) and
    after (70, 65, 71, 68, 65, 70, 67, 69);</li>
    <li>a test of \(\sigma^{2} = 6\) for the sample in (1);</li>
    <li>a test of equal variances for A and B;</li>
    <li>a test of \(\rho = 0\), and</li>
    <li>a test of \(\rho = 0.8\), for the ten pairs of Practical 10.</li>
  </ol>""",
        aim="Carry out seven tests, with every tail area computed rather than read from a table.",
        steps=[
            r"A function that returns \(n\), \(\bar x\) and \(s^{2}\) with divisor \(n - 1\).",
            r"\(t = (\bar x - \mu_0)/(s/\sqrt n)\) on \(n - 1\) df.",
            r"The pooled variance, then \(t\) on \(n_1 + n_2 - 2\) df.",
            r"The differences \(d\), then \(t = \bar d/(s_d/\sqrt n)\) on \(n - 1\) df.",
            r"\(\chi^{2} = (n-1)s^{2}/\sigma_0^{2}\) on \(n - 1\) df, two-sided.",
            r"\(F\), the larger variance over the smaller, two-sided.",
            r"\(t = r\sqrt{(n-2)/(1-r^{2})}\) on \(n - 2\) df.",
            r"Fisher's \(z\) for \(r\) and for \(\rho_0\), and \((z - z_0)\sqrt{n-3}\) against \(N(0,1)\).",
        ],
        method=r"""    <table>
      <tr><th>Test</th><th>Statistic</th><th>Null distribution</th></tr>
      <tr><td>One mean</td><td>\(\dfrac{\bar x - \mu_0}{s/\sqrt n}\)</td><td>\(t_{n-1}\)</td></tr>
      <tr><td>Two means, independent</td>
          <td>\(\dfrac{\bar x_1 - \bar x_2}{\sqrt{s_p^{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}}\)</td>
          <td>\(t_{n_1+n_2-2}\)</td></tr>
      <tr><td>Two means, paired</td><td>\(\dfrac{\bar d}{s_d/\sqrt n}\)</td><td>\(t_{n-1}\)</td></tr>
      <tr><td>One variance</td><td>\((n-1)s^{2}/\sigma_0^{2}\)</td><td>\(\chi^{2}_{n-1}\)</td></tr>
      <tr><td>Two variances</td><td>\(s_1^{2}/s_2^{2}\), larger over smaller</td>
          <td>\(F_{n_1-1,\,n_2-1}\)</td></tr>
      <tr><td>\(\rho = 0\)</td><td>\(r\sqrt{\dfrac{n-2}{1-r^{2}}}\)</td><td>\(t_{n-2}\)</td></tr>
      <tr><td>\(\rho = \rho_0 \ne 0\)</td>
          <td>\(\left(z - z_0\right)\sqrt{n-3}\), \(z = \tfrac12\ln\frac{1+r}{1-r}\)</td>
          <td>\(N(0,1)\)</td></tr>
    </table>""",
        commands=[
            ("<code>from tails import t_two_sided, F_upper, chi2_upper, normal_two_sided</code>", "the four tail areas from Practical 0"),
            ("<code>[b - a for b, a in zip(before, after)]</code>", "the paired differences"),
            ("<code>max(s2a, s2b) / min(s2a, s2b)</code>", "the larger variance over the smaller"),
            ("<code>2 * min(p_lo, p_hi)</code>", "a two-sided \\(p\\) value from the two tails of \\(\\chi^{2}\\)"),
            ("<code>math.log</code>", "Fisher's \\(z\\) transformation"),
        ],
        reading=r"""  <p><strong>Three points that decide marks.</strong></p>
  <ul>
    <li><strong>The order of the tests.</strong> The two-variance \(F\) comes out at
    \(p = 0.654\), so the variances may be treated as equal and the pooled two-sample \(t\) is
    legitimate. Running the pooled \(t\) without that check is the commonest omission.</li>
    <li><strong>Paired means paired.</strong> The same eight subjects are measured twice, so the
    differences are analysed, not the two samples. The paired \(t\) is \(6.61\) with
    \(p = 0.0003\); treating the two columns as independent samples would throw away exactly the
    pairing that makes the effect visible.</li>
    <li><strong>\(\rho = 0\) and \(\rho = \rho_0\) are different tests.</strong> The \(t\)
    statistic is valid only against zero, because only then is the sampling distribution of
    \(r\) symmetric. Against \(\rho_0 = 0.8\) Fisher's \(z\) transformation is needed, and here
    it gives \(p = 0.36\) &mdash; the same \(r\) that is significantly different from 0 is
    <em>not</em> significantly different from 0.8, which is not a contradiction but a statement
    about how little ten observations settle.</li>
  </ul>""",
        conclusion=r"""    <ol>
      <li>\(t = 1.766\) on 11 df, \(p = 0.105\): \(\mu = 50\) is not rejected.</li>
      <li>\(t = -3.786\) on 11 df, \(p = 0.003\): the means of A and B differ.</li>
      <li>\(t = 6.614\) on 7 df, \(p = 0.0003\): the mean fell, by 2.5.</li>
      <li>\(\chi^{2} = 14.15\) on 11 df, \(p = 0.449\): \(\sigma^{2} = 6\) is not rejected.</li>
      <li>\(F = 1.457\) on (5, 6) df, \(p = 0.654\): the variances may be taken as equal, which
      justifies the pooled test in (2).</li>
      <li>\(r = 0.637\), \(t = 2.336\) on 8 df, \(p = 0.048\): \(\rho = 0\) is rejected, just.</li>
      <li>Fisher's \(z\) statistic \(-0.915\), \(p = 0.360\): \(\rho = 0.8\) is not rejected.</li>
    </ol>""",
    ),
    dict(
        n=12, title="One-Way and Two-Way Analysis of Variance", file="p12.py",
        question=r"""  <p>(a) Three treatments gave the yields A: 20, 22, 19, 24, 25; B: 27, 25, 30, 28, 26;
  C: 23, 21, 24, 22, 25. Test whether the treatment means differ.</p>
  <p>(b) Three varieties were grown in four blocks, one plot each:</p>
  <table>
    <tr><th></th><th>Block 1</th><th>Block 2</th><th>Block 3</th><th>Block 4</th></tr>
    <tr><th>Variety 1</th><td>18</td><td>22</td><td>20</td><td>16</td></tr>
    <tr><th>Variety 2</th><td>23</td><td>25</td><td>26</td><td>21</td></tr>
    <tr><th>Variety 3</th><td>15</td><td>19</td><td>18</td><td>14</td></tr>
  </table>
  <p>Test whether the varieties differ and whether the blocks differ.</p>""",
        aim="Produce both analysis of variance tables from the correction factor upward.",
        steps=[
            r"A function that prints the table: for each source the SS, df, MS, \(F\) against the error mean square, and its \(p\) value from <code>tails.py</code>.",
            r"\(G\), \(CF = G^{2}/N\), the total and treatment sums of squares, and the error by subtraction.",
            r"The row and column totals, their sums of squares, and the error by subtraction on \((r-1)(c-1)\) df.",
            "Print the sum of the parts beside the total.",
        ],
        method=r"""    \[ CF = \frac{G^{2}}{N}, \qquad SS_{\text{total}} = \sum x^{2} - CF, \]
    \[ SS_{\text{treatments}} = \sum_i \frac{T_i^{2}}{n_i} - CF, \qquad
       SS_{\text{error}} = SS_{\text{total}} - SS_{\text{treatments}}, \]
    <p>and for the two-way layout with one observation per cell,</p>
    \[ SS_{\text{rows}} = \frac{\sum_i R_i^{2}}{c} - CF, \qquad
       SS_{\text{columns}} = \frac{\sum_j C_j^{2}}{r} - CF, \]
    \[ SS_{\text{error}} = SS_{\text{total}} - SS_{\text{rows}} - SS_{\text{columns}}
       \quad\text{on } (r-1)(c-1) \text{ degrees of freedom.} \]
    <p><strong>Error is obtained by subtraction, always.</strong> Computing it directly is
    possible but slower and gives no check; obtaining it by subtraction and then confirming that
    the components add back to the total &mdash; which the program prints &mdash; catches an
    arithmetic slip anywhere in the table.</p>""",
        commands=[
            ("<code>from tails import F_upper</code>", "the \\(F\\) tail area from Practical 0"),
            ("<code>groups = {\"A\": [...], ...}</code>", "the treatments, as a dictionary of lists"),
            ("<code>[v for g in groups.values() for v in g]</code>", "all the observations in one list"),
            ("<code>sum(tab[i][j] for i in range(r))</code>", "a column total"),
            ("<code>f\"{name:&lt;14}{ss:12.4f}\"</code>", "line the table up in columns"),
        ],
        reading=r"""  <p><strong>What the two-way layout can and cannot do.</strong> With one observation per cell
  there is nothing left over to estimate an interaction, so the model
  \(y_{ij} = \mu + \alpha_i + \beta_j + e_{ij}\) is an assumption, not a finding. The moment a
  cell holds two observations, a pure error term appears and the interaction becomes testable
  &mdash; which is where
  <a href="../design-and-analysis-of-experiments-advanced/unit1.html">Design and Analysis of Experiments,
  Unit 1</a> picks the subject up.</p>""",
        conclusion=r"""    <p>(a) \(F = 8.99\) on (2, 12) df, \(p = 0.004\): the treatment means differ.
    (b) Varieties \(F = 114.88\) on (2, 6) df, \(p = 0.00002\), and blocks \(F = 34.53\) on
    (3, 6) df, \(p = 0.0004\): both differ. The parts add back to the total, 160.25.</p>""",
    ),
]

TAIL = r"""  <h2 id="how-marks-are-lost">How Marks Are Lost</h2>
  <div class="tip">
    <span class="label">THE RECURRING ERRORS</span>
    <ul>
      <li><strong>Importing a package.</strong> The course's own note forbids it. A program that
      calls <code>statistics.mean</code> or <code>numpy.linalg.inv</code> answers a different
      question from the one asked.</li>
      <li><strong>Dropping the transpose in the adjoint.</strong> It makes no difference for a
      symmetric matrix, so the error survives every symmetric test case and fails the
      examination's.</li>
      <li><strong>Mutating a list while indexing it from the end.</strong>
      <code>e[-2] += e.pop()</code> does not do what it reads as: the index \(-2\) is resolved
      <em>after</em> the pop, so the value lands in the wrong cell. Pop first, then add.</li>
      <li><strong>Not pooling before a \(\chi^{2}\) goodness-of-fit test</strong>, and not
      subtracting the estimated parameters from the degrees of freedom. Either one alone
      invalidates the test.</li>
      <li><strong>Fitting a Cauchy by its mean.</strong> It has none. Use the median and the
      half-interquartile range.</li>
      <li><strong>Using \(n\) where \(n-1\) belongs.</strong> Divide by \(n\) for a descriptive
      variance and by \(n-1\) for the one that goes into a \(t\) or an \(F\). State which you
      are using.</li>
      <li><strong>Printing a number without saying what it is.</strong> Every program above
      labels its output; an unlabelled column of figures earns nothing.</li>
    </ul>
  </div>

  <h2 id="what-the-practical-record-should-contain">What the Practical Record Should Contain</h2>
  <div class="concept">
    <span class="label">FOR EACH PROGRAM</span>
    <ol>
      <li><strong>Question</strong> &mdash; the problem as set, with its input data.</li>
      <li><strong>Aim</strong> &mdash; in one line.</li>
      <li><strong>Steps</strong> &mdash; the formula or algorithm, written out before any code, in
      numbered steps.</li>
      <li><strong>Programme</strong> &mdash; the program, with the functions named for what they do
      and each step marked by a comment.</li>
      <li><strong>Execution and Results</strong> &mdash; the output, as it was actually printed
      (not as it should have been); the check, a second route to the same number or an identity
      that must hold; and the conclusion in words.</li>
    </ol>
  </div>

  <div class="page-nav">
    <a href="index.html">&larr; Course Home</a>
    <a href="../index.html">All Statistics courses &rarr;</a>
  </div>

  <footer>Statistical Methods using Python &middot; Statistics</footer>
</div>
"""
