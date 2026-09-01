"""Shared data for the Course 15 A practicals.

TWO KINDS OF DATA, DELIBERATELY.

The REAL corpora -- Brown, Reuters, the Penn Treebank, movie_reviews,
Gutenberg, WordNet -- come from NLTK and are what the syllabus names. They
tell you how a method performs on language people actually wrote.

The CONSTRUCTED text below exists for a different job. Every ambiguous
sentence here is ambiguous in a way that is documented, every entity in the
news paragraph is labelled by hand, and every FAQ question has a known answer.
That makes the labs CHECKABLE: you can ask whether the parser found the two
readings that are there, not merely whether it produced a tree.

The Indian-context text is not decoration. spaCy's English model was trained
mostly on American news, and running it on Indian place names and
organisations exposes failures that a lab on Reuters would hide -- which is
the more useful thing for these students to see.
"""
import re

SEED = 42


# ------------------------------------------------------- experiment 2: regex
#
# One text carrying every pattern the syllabus asks for, plus the near-misses
# that break a naive pattern. The near-misses are the point.

CONTACT_TEXT = """
From: asha.reddy@nrigroup.ac.in
To: ravi_kumar99@gmail.com, admin@nri.edu

Ravi, the workshop is on 14/03/2025 and the follow-up on 2025-04-02.
An older batch met on March 3, 2024. Call me on +91 98765 43210 or
040-2345-6789; the office line is (040) 2345 6789.

Tag your posts #DataScience #NLP2025 and #ai -- not # alone, and not
C#, which is a language.

Not an email: asha at nrigroup dot ac dot in. Also not one: @nri_official
is a handle. And 91-98765 is too short to be a phone number.
"""

# hand-labelled truth, so the regexes can be SCORED rather than eyeballed
CONTACT_TRUTH = {
    "emails": ["asha.reddy@nrigroup.ac.in", "ravi_kumar99@gmail.com",
               "admin@nri.edu"],
    "hashtags": ["#DataScience", "#NLP2025", "#ai"],
    "dates": ["14/03/2025", "2025-04-02", "March 3, 2024"],
    "phones": ["+91 98765 43210", "040-2345-6789", "(040) 2345 6789"],
}


# ------------------------------------------ experiment 3: ambiguity, labelled

AMBIGUOUS = [
    ("I saw the man with the telescope.",
     "structural",
     "Attachment: 'with the telescope' can modify 'saw' (I used it) or "
     "'the man' (he had it). Two parse trees, both grammatical."),
    ("The bank was closed.",
     "lexical",
     "'bank' is a financial institution or a river edge. WordNet lists "
     "18 synsets for it."),
    ("Visiting relatives can be boring.",
     "structural",
     "'Visiting' is a gerund (the act of visiting) or a participle "
     "(relatives who are visiting)."),
    ("She saw her duck.",
     "lexical + structural",
     "'duck' is a noun (the bird) or a verb (to lower the head), which "
     "also changes the structure."),
    ("Time flies like an arrow.",
     "structural",
     "The classic: 'time' as noun or imperative verb, 'flies' as verb or "
     "noun, 'like' as preposition or verb."),
    ("The old man the boats.",
     "structural",
     "A garden path: 'man' is the VERB and 'the old' is the subject. "
     "Almost everyone misreads it once."),
]


# ------------------------------------------------- experiment 7: two grammars

TOY_GRAMMAR = """
S   -> NP VP
NP  -> Det N | Det N PP | 'I' | 'she'
VP  -> V NP | VP PP
PP  -> P NP
Det -> 'the' | 'a' | 'an'
N   -> 'man' | 'telescope' | 'park' | 'dog'
V   -> 'saw' | 'walked'
P   -> 'with' | 'in'
"""

AMBIGUOUS_SENTENCE = "I saw the man with the telescope".split()


# --------------------------------------------------- experiment 8: NER truth
#
# Hand-labelled, so spaCy's output can be SCORED. The Indian entities are
# here on purpose -- see the module docstring.

NEWS_TEXT = (
    "Infosys announced on 12 January 2024 that it will open a development "
    "centre in Hyderabad, investing 2,400 crore rupees over three years. "
    "Chief Executive Salil Parekh said the centre will employ 15,000 people "
    "by 2027. The announcement was made in Bengaluru alongside Karnataka "
    "Chief Minister Siddaramaiah. Microsoft and Google have made similar "
    "commitments in Andhra Pradesh and Tamil Nadu."
)

# (text, the label a careful human would assign)
NEWS_TRUTH = [
    ("Infosys", "ORG"),
    ("12 January 2024", "DATE"),
    ("Hyderabad", "GPE"),
    ("Salil Parekh", "PERSON"),
    ("15,000", "CARDINAL"),
    ("2027", "DATE"),
    ("Bengaluru", "GPE"),
    ("Karnataka", "GPE"),
    ("Siddaramaiah", "PERSON"),
    ("Microsoft", "ORG"),
    ("Google", "ORG"),
    ("Andhra Pradesh", "GPE"),
    ("Tamil Nadu", "GPE"),
]


# ------------------------------------- experiment 9: documents with known ties
#
# Built so the similarity ranking is known in advance: DOCS[0] and DOCS[1]
# share a topic and much vocabulary; DOCS[2] shares the topic and almost no
# vocabulary; DOCS[3] is unrelated. A good representation should rank
# 0-1 highest, and the 0-2 pair is where bag-of-words and n-grams differ.

DOCS = [
    "The model learns weights from the training data by gradient descent.",
    "Gradient descent updates the model weights using the training data.",
    "Parameters are fitted to observations by iteratively minimising a loss.",
    "The monsoon arrived early this year and the reservoirs are full.",
]

DOC_TRUTH = {
    "most_similar_to_0": 1,
    "same_topic_different_words": 2,
    "unrelated": 3,
}


# ------------------------------------------- experiment 14: FAQ with answers

FAQ = [
    ("How do I reset my password?",
     "Use the 'Forgot password' link on the sign-in page; a reset email "
     "arrives within five minutes."),
    ("What are the library opening hours?",
     "The library is open 08:00 to 20:00 on weekdays and 09:00 to 13:00 on "
     "Saturday."),
    ("How do I apply for a bonafide certificate?",
     "Submit the request form at the academic section; it is issued in two "
     "working days."),
    ("When does the semester examination begin?",
     "End-semester examinations begin in the third week of April."),
    ("How much is the hostel fee?",
     "The hostel fee is 45,000 rupees per year, payable in two instalments."),
    ("Where do I collect my marks memo?",
     "Marks memos are collected from the examination branch with your ID."),
]

# questions a student would actually type, with the FAQ index that answers
# them. NONE of these is a copy of the FAQ question -- that is the test.
FAQ_QUERIES = [
    ("i forgot my password what do i do", 0),
    ("library timings on saturday", 1),
    ("bonafide certificate procedure", 2),
    ("when are the exams", 3),
    ("cost of staying in the hostel", 4),
    ("how to get marks memo", 5),
]


def tokens(text):
    """Lowercased word tokens, punctuation dropped. Deliberately naive.

    Experiment 4 replaces this with NLTK and spaCy and measures how they
    differ -- so this exists to be the thing they are compared against.
    """
    return re.findall(r"[a-z0-9']+", text.lower())
