# -*- coding: utf-8 -*-
"""The working of every Paper I model MCQ whose key can be computed.

recheck_ugc_paper1.py evaluates each entry and requires the result to equal
the keyed option and no other option. The working is written here afresh, as
arithmetic, not copied from the explanation on the page, so a slip in either
shows up as a disagreement.

    (unit, question): (python expression, how to read the options)

"number"  the options are numbers; the result must equal the keyed one (to
          1e-9, or to the option's own last decimal place) and no other
"""


def h_index(citations):
    c = sorted(citations, reverse=True)
    return sum(1 for i, x in enumerate(c, 1) if x >= i)


COMPUTED = {
    # Unit I Q20: SGPA, credit-weighted
    (1, 20): ("(4*8 + 3*6 + 3*10) / (4 + 3 + 3)", "number"),
    # Unit II Q16: h-index of six papers
    (2, 16): ("h_index([12, 10, 7, 5, 3, 1])", "number"),
}
