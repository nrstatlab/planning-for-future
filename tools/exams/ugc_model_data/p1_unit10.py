# -*- coding: utf-8 -*-
"""UGC NET Paper I, Unit 10: fifty exam-standard model questions.

Only settled facts are used (founders, years, Acts, constitutional entries);
nothing that depends on the latest ranking or a proposal not yet in force.
"""
from . import AR, Q, ar, match, st

TITLE = "Higher Education System"
BLURB = ("Institutions of higher learning in ancient India, higher education since Independence, oriental, "
         "conventional and non-conventional programmes, professional, technical and skill-based education, "
         "value and environmental education, and policies, governance and administration.")

QUESTIONS = [
 Q("Match the ancient centre of learning in List I with the ruler or dynasty under whom it was founded in "
   "List II."
   + match(["Nalanda", "Vikramashila", "Odantapuri", "Valabhi"],
           ["Gopala (Pala)", "The Maitraka kings", "Kumaragupta I (Gupta)", "Dharmapala (Pala)"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)",
    "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "B",
   "Nalanda was founded in the 5th century under Kumaragupta I; Vikramashila by Dharmapala and Odantapuri by "
   "Gopala, both Pala kings, in the 8th century; Valabhi flourished under the Maitrakas of Gujarat.", "ancient"),

 Q("Which of the following ancient centres of learning lies outside the present-day territory of India?",
   ["Nalanda", "Vikramashila", "Valabhi", "Takshashila"], "D",
   "Takshashila (Taxila) is near Rawalpindi in present-day Pakistan. Nalanda, Vikramashila and Odantapuri are "
   "in Bihar and Valabhi in Gujarat.", "ancient"),

 Q("Consider the statements about Nalanda:"
   + st("It was a great residential Buddhist university.", "The Chinese pilgrim Xuanzang studied there.",
        "Its ruins are a UNESCO World Heritage Site.", "It was founded by the Pala king Dharmapala.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and II only", "II, III and IV only", "I, II, III and IV"], "A",
   "Nalanda was founded under the Gupta king Kumaragupta I; it was Vikramashila that Dharmapala founded. So "
   "(IV) is false. The ruins of Nalanda were inscribed as a World Heritage Site in 2016.", "ancient"),

 Q("Chanakya, the grammarian Panini and the physician Jivaka are associated with the ancient centre of "
   "learning at:",
   ["Nalanda", "Valabhi", "Takshashila", "Odantapuri"], "C",
   "Takshashila, which flourished from about the 6th century BCE, was known for medicine, law, military "
   "science and grammar.", "ancient"),

 Q("Arrange the following in the chronological order of their beginning: (1) Vikramashila, (2) Takshashila, "
   "(3) Nalanda.",
   ["3, 2, 1", "2, 3, 1", "2, 1, 3", "1, 2, 3"], "B",
   "Takshashila flourished from about the 6th century BCE; Nalanda was founded in the 5th century CE; "
   "Vikramashila in the late 8th century CE.", "ancient"),

 Q("Which of the following was NOT a feature of the gurukula system?",
   ["Students lived in the household of the teacher", "Learning was largely oral",
    "The course ended with a gift to the teacher", "Fixed fees were charged at the time of admission"], "D",
   "In the gurukula the student lived with the teacher, served the household and learnt orally, without "
   "fees; the gurudakshina, a gift at the end, closed the course.", "ancient"),

 Q("The scholar Atisha and the study of Tantric Buddhism are associated with:",
   ["Vikramashila", "Takshashila", "Valabhi", "Nalanda"], "A",
   "Vikramashila, in Bihar, founded by Dharmapala in the late 8th century, was the great centre of Tantric "
   "Buddhism, and Atisha was its most famous scholar.", "ancient"),

 Q("Which ancient centre in Gujarat was known for Hinayana Buddhism and also for secular subjects such as "
   "law and economics?",
   ["Odantapuri", "Nalanda", "Valabhi", "Vikramashila"], "C",
   "Valabhi, under the Maitraka kings from the 6th century, rivalled Nalanda and taught secular subjects "
   "beside Buddhist learning.", "ancient"),

 Q("Match the commission in List I with its chairman in List II."
   + match(["University Education Commission (1948&ndash;49)", "Secondary Education Commission (1952&ndash;53)",
            "Education Commission (1964&ndash;66)", "Committee that drafted the National Education Policy 2020"],
           ["D. S. Kothari", "K. Kasturirangan", "S. Radhakrishnan", "A. L. Mudaliar"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)"], "D",
   "Radhakrishnan chaired the first commission of independent India, on university education; Mudaliar the "
   "one on secondary education; Kothari the Education Commission; Kasturirangan the committee for the 2020 "
   "policy.", "post-independence"),

 Q("Arrange the following in chronological order: (1) National Policy on Education, 1986, (2) Kothari "
   "Commission, (3) National Education Policy 2020, (4) Radhakrishnan Commission, (5) First National Policy "
   "on Education.",
   ["4, 2, 5, 1, 3", "2, 4, 5, 1, 3", "4, 5, 2, 1, 3", "4, 2, 1, 5, 3"], "A",
   "Radhakrishnan Commission 1948&ndash;49; Kothari Commission 1964&ndash;66; the first National Policy on "
   "Education 1968, based on the Kothari report; the second policy 1986 (revised 1992); the National "
   "Education Policy 2020.", "post-independence"),

 Q("The University Grants Commission was inaugurated, and became a statutory body, in the years:",
   ["1948 and 1953", "1953 and 1956", "1956 and 1968", "1945 and 1987"], "B",
   "The UGC was inaugurated in 1953, as the Radhakrishnan Commission had recommended, and was made statutory "
   "by the UGC Act, 1956. (1945 and 1987 are the corresponding years for AICTE.)", "post-independence"),

 Q("The 10+2+3 pattern of education and a common school system were proposed by:",
   ["the Radhakrishnan Commission", "the Mudaliar Commission", "the Kothari Commission",
    "the National Policy on Education, 1986"], "C",
   "The Education Commission of 1964&ndash;66, chaired by D. S. Kothari, in its report <em>Education and "
   "National Development</em>.", "post-independence"),

 Q("A body grades a college A++ after a visit by a peer team; another body places the same college 40th in "
   "an annual national list. The two bodies are, respectively:",
   ["NIRF and NAAC", "UGC and AICTE", "AICTE and NIRF", "NAAC and NIRF"], "D",
   "The National Assessment and Accreditation Council assesses and accredits institutions with grades; the "
   "National Institutional Ranking Framework ranks them each year.", "post-independence"),

 Q("Consider the statements about the National Education Policy 2020:"
   + st("It aims at a gross enrolment ratio of 50% in higher education by 2035.",
        "It provides for four-year undergraduate degrees with multiple entry and exit.",
        "It provides for an Academic Bank of Credits.",
        "It recommends that vocational education be kept as a stream separate from mainstream education.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and II only", "II, III and IV only", "I, II, III and IV"], "A",
   "The policy asks for vocational education to be <em>integrated</em> into mainstream schooling and higher "
   "education, not kept apart. So (IV) is false.", "post-independence"),

 Q("The National Assessment and Accreditation Council (NAAC) was set up by the UGC in 1994, with its "
   "headquarters at:",
   ["New Delhi", "Bengaluru", "Hyderabad", "Pune"], "B",
   "NAAC, established in 1994 following the National Policy on Education of 1986 and its Programme of "
   "Action of 1992, is at Bengaluru.", "post-independence"),

 Q("Match the body or scheme in List I with the year in List II."
   + match(["IGNOU founded", "AICTE made statutory", "RUSA launched", "NIRF approved"],
           ["2015", "1985", "2013", "1987"]),
   ["(a)-(ii), (b)-(iv), (c)-(i), (d)-(iii)", "(a)-(iv), (b)-(ii), (c)-(iii), (d)-(i)",
    "(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)", "(a)-(ii), (b)-(iii), (c)-(iv), (d)-(i)"], "C",
   "The Indira Gandhi National Open University was founded in 1985; the All India Council for Technical "
   "Education gained statutory powers in 1987; the Rashtriya Uchchatar Shiksha Abhiyan began in 2013; the "
   "National Institutional Ranking Framework dates from 2015, with its first rankings in 2016.", "post-independence"),

 Q("The Rashtriya Uchchatar Shiksha Abhiyan (RUSA) is a scheme for:",
   ["ranking of universities", "accreditation of colleges", "recruitment of teachers",
    "central funding of state higher-education institutions"], "D",
   "RUSA, launched in 2013, channels central funds to state universities and colleges on the basis of state "
   "plans.", "post-independence"),

 Q(ar("The University Grants Commission was set up after Independence.",
      "The University Education Commission chaired by S. Radhakrishnan recommended such a body."),
   AR, "A",
   "The Radhakrishnan Commission (1948&ndash;49) recommended a University Grants Commission; it was "
   "inaugurated in 1953 and made statutory in 1956. Both statements are true and (R) explains (A).", "post-independence"),

 Q("The first National Policy on Education (1968) was based on the report of:",
   ["the Radhakrishnan Commission", "the Kothari Commission", "the Mudaliar Commission",
    "the Kasturirangan Committee"], "B",
   "The Kothari Commission reported in 1966 and the first National Policy on Education followed in 1968.", "post-independence"),

 Q("The Programme of Action that accompanied the revision of the National Policy on Education, 1986, was "
   "adopted in:",
   ["1988", "1990", "1992", "1994"], "C",
   "The 1986 policy was revised in 1992, with a Programme of Action. NAAC was set up two years later, in "
   "1994.", "post-independence"),

 Q("A student takes the degree of Acharya in Vyakarana at a Sanskrit university. This is an example of:",
   ["oriental learning", "non-conventional education", "technical education", "skill-based education"], "A",
   "Oriental learning keeps the classical traditions (Sanskrit, Pali, Prakrit, Persian, Arabic) in Sanskrit "
   "universities, pathshalas and madrasas, with degrees such as Shastri and Acharya.", "programmes"),

 Q("A working clerk studies for a degree from study material sent by an open university and attends "
   "counselling sessions at weekends. The programme is:",
   ["conventional", "oriental", "professional", "non-conventional"], "D",
   "Conventional programmes are regular, full-time and campus-based. Open and distance learning, "
   "correspondence courses, online degrees, and part-time and evening courses are non-conventional.", "programmes"),

 Q("The first state open university in India, founded in 1982, was in:",
   ["Maharashtra", "Andhra Pradesh", "Tamil Nadu", "Rajasthan"], "B",
   "It is now Dr B. R. Ambedkar Open University, at Hyderabad. IGNOU, the national open university, followed "
   "in 1985.", "programmes"),

 Q("Correspondence courses at the university level in India were first started in 1962 by:",
   ["the University of Madras", "IGNOU", "the University of Delhi", "the University of Mumbai"], "C",
   "The University of Delhi began correspondence courses in 1962, the beginning of distance education at "
   "the university level in India.", "programmes"),

 Q("Consider the statements about open and distance learning:"
   + st("Its strengths are reach, flexibility and low cost.",
        "Its weaknesses include low completion rates and uneven learner support.",
        "In India it is regulated by the UGC.",
        "It requires the learner to attend classes on the campus every day.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and II only", "II, III and IV only", "I, II, III and IV"], "A",
   "Daily attendance on a campus is the mark of conventional education; distance learning exists to remove "
   "that condition. So (IV) is false.", "programmes"),

 Q("Match the kind of programme in List I with the example in List II."
   + match(["Oriental", "Conventional", "Non-conventional"],
           ["A full-time B.Sc. in a college", "A degree through an open university", "A Shastri degree in Sanskrit"]),
   ["(a)-(i), (b)-(iii), (c)-(ii)", "(a)-(iii), (b)-(ii), (c)-(i)", "(a)-(ii), (b)-(i), (c)-(iii)",
    "(a)-(iii), (b)-(i), (c)-(ii)"], "D",
   "The Shastri degree belongs to oriental learning; the full-time college degree is conventional; the open "
   "university degree is non-conventional.", "programmes"),

 Q("Match the field in List I with its regulatory body in List II."
   + match(["Technical education", "Teacher education", "Legal education", "Medical education"],
           ["National Medical Commission", "Bar Council of India", "AICTE", "NCTE"]),
   ["(a)-(iii), (b)-(i), (c)-(ii), (d)-(iv)", "(a)-(iv), (b)-(iii), (c)-(ii), (d)-(i)",
    "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)"], "C",
   "The All India Council for Technical Education, the National Council for Teacher Education, the Bar "
   "Council of India and the National Medical Commission regulate the four fields.", "professional"),

 Q("The National Medical Commission replaced the Medical Council of India in:",
   ["2014", "2020", "2017", "2010"], "B",
   "The National Medical Commission took the place of the Medical Council of India in 2020 as the regulator "
   "of medical education and practice.", "professional"),

 Q("The National Skills Qualifications Framework (NSQF) arranges qualifications:",
   ["by the fees charged for them", "by the age of the learner", "alphabetically by trade",
    "in levels according to competence, so that skills can be recognised and built upon"], "D",
   "The NSQF (2013) is a competence-based framework of levels, which lets a learner move between vocational "
   "and general education and have skills recognised however they were gained.", "professional"),

 Q("Arrange the following in chronological order: (1) Launch of the Skill India mission, (2) AICTE set up "
   "as an advisory body, (3) National Skills Qualifications Framework, (4) AICTE given statutory status.",
   ["2, 4, 3, 1", "4, 2, 3, 1", "2, 3, 4, 1", "2, 4, 1, 3"], "A",
   "AICTE was set up as an advisory body in 1945 and given statutory powers in 1987; the NSQF was notified "
   "in 2013; Skill India was launched in 2015.", "professional"),

 Q("Which of the following lists contains only institutions of skill-based (vocational) training?",
   ["IITs and NITs", "Medical colleges and law colleges", "Industrial Training Institutes and apprenticeships",
    "Sanskrit universities and madrasas"], "C",
   "Industrial Training Institutes, apprenticeships and short courses train for a trade. The IITs and NITs "
   "give technical education at degree level; medical and law colleges give professional education.", "professional"),

 Q("A B.Voc. student spends a semester as an intern in the medical-records office of a hospital and earns "
   "credits for it. This illustrates:",
   ["oriental learning", "skill-based education integrated into a degree programme",
    "distance education", "value education"], "B",
   "The National Education Policy 2020 asks for vocational education to be part of mainstream higher "
   "education; credit for an internship within a degree is an instance of it.", "professional"),

 Q("Consider the statements:"
   + st("Professional education prepares for a regulated profession such as medicine, law or teaching.",
        "Polytechnics award diplomas in technical subjects.",
        "The National Council for Teacher Education regulates teacher education.",
        "AICTE regulates medical education.")
   + "Which of the statements are correct?",
   ["I and II only", "II, III and IV only", "I, II, III and IV", "I, II and III only"], "D",
   "AICTE regulates technical education; medical education is regulated by the National Medical Commission. "
   "So (IV) is false.", "professional"),

 Q("Which body regulates the education of architects in India?",
   ["The Council of Architecture", "AICTE alone", "The Bar Council of India", "The Pharmacy Council of India"], "A",
   "Each regulated profession has its council: the Council of Architecture for architects, the Pharmacy "
   "Council for pharmacists, the Bar Council for lawyers.", "professional"),

 Q("Which of the following are the values named in the Preamble to the Constitution of India that value "
   "education is expected to foster?",
   ["Liberty, equality and prosperity", "Justice, liberty, equality and fraternity",
    "Truth, non-violence and discipline", "Unity, faith and discipline"], "B",
   "The Preamble secures to all citizens justice, liberty and equality, and promotes among them fraternity. "
   "Value education also covers personal values such as truthfulness, respect and responsibility.", "value"),

 Q("The aims of environmental education usually listed, following the Tbilisi Declaration of 1977, are:",
   ["reading, writing and arithmetic", "liberty, equality and fraternity",
    "awareness, knowledge, attitudes, skills and participation", "reduce, reuse and recycle"], "C",
   "The Tbilisi Declaration of UNESCO and UNEP set out awareness, knowledge, attitudes, skills and "
   "participation as the objectives of environmental education.", "value"),

 Q("Environmental studies became a compulsory part of education in India following the directions of the "
   "Supreme Court in:",
   ["Kesavananda Bharati v. State of Kerala", "Unni Krishnan v. State of Andhra Pradesh",
    "Vishaka v. State of Rajasthan", "M. C. Mehta v. Union of India"], "D",
   "On the Court's directions in M. C. Mehta v. Union of India, environmental studies was made compulsory, "
   "and the UGC framed a compulsory undergraduate course in it.", "value"),

 Q(ar("Value education works better through example, discussion of dilemmas and service than through "
      "lectures alone.",
      "Values are formed by what learners see practised and do themselves, not merely by what they are told."),
   AR, "A",
   "A learner can repeat a lecture on honesty without becoming honest; values are absorbed from the conduct "
   "of teachers, the culture of the institution and the learner's own practice. Both statements are true and "
   "(R) is the reason.", "value"),

 Q("Students audit the use of water on their campus and present proposals for saving it to the "
   "administration. This is environmental education mainly through:",
   ["awareness", "participation", "recall", "indoctrination"], "B",
   "The students act on a real problem and take part in its solution: participation, the fifth of the "
   "Tbilisi objectives.", "value"),

 Q("Education was transferred from the State List to the Concurrent List by the:",
   ["42nd Amendment, 1976", "44th Amendment, 1978", "73rd Amendment, 1992", "86th Amendment, 2002"], "A",
   "Since the 42nd Amendment both the Union and the states can legislate on education. The 86th Amendment "
   "made elementary education a fundamental right.", "policies"),

 Q("&lsquo;Coordination and determination of standards in institutions for higher education or "
   "research&rsquo; is a subject under:",
   ["Entry 25 of the Concurrent List", "Entry 11 of the State List", "Entry 66 of the Union List",
    "the Directive Principles"], "C",
   "Entry 66 of the Union List gives the Union this power, which is the constitutional basis of bodies such "
   "as the UGC. Education in general is Entry 25 of the Concurrent List.", "policies"),

 Q("Match the kind of institution in List I with the way it is established in List II."
   + match(["Central university", "State university", "Deemed-to-be university", "Institution of National Importance"],
           ["Declared under Section 3 of the UGC Act", "By an Act of Parliament, as a university",
            "By an Act of Parliament, with that special status, as for the IITs", "By an Act of a state legislature"]),
   ["(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)", "(a)-(iv), (b)-(ii), (c)-(i), (d)-(iii)",
    "(a)-(ii), (b)-(i), (c)-(iv), (d)-(iii)", "(a)-(ii), (b)-(iv), (c)-(i), (d)-(iii)"], "D",
   "Central universities and Institutions of National Importance are created by Parliament, state "
   "universities by state legislatures, and deemed-to-be universities by a declaration under Section 3 of "
   "the UGC Act, 1956.", "policies"),

 Q("In a university, a proposal to introduce a new syllabus is approved by:",
   ["the Executive Council", "the Academic Council", "the Finance Committee", "the Court"], "B",
   "The Academic Council is responsible for courses, examinations and academic standards. The Executive "
   "Council (or Syndicate) deals with administration and finance.", "policies"),

 Q("The Chancellor of a state university is usually:",
   ["the Governor of the state", "the Chief Minister", "the Education Minister", "the Chairman of the UGC"], "A",
   "In most state universities the Governor is the Chancellor by virtue of office; the Vice-Chancellor is "
   "the chief executive and academic officer.", "policies"),

 Q("An autonomous college is one that:",
   ["awards its own degrees", "is not affiliated to any university",
    "frames its own syllabus and conducts its own examinations, while the university awards the degree",
    "receives no grants from the government"], "C",
   "Autonomy covers the curriculum, teaching and evaluation; the degree is still awarded by the university "
   "to which the college is affiliated.", "policies"),

 Q("Consider the statements:"
   + st("The UGC is concerned with standards and grants in university education.",
        "NAAC accredits institutions.",
        "The National Board of Accreditation accredits programmes, chiefly technical ones.",
        "NIRF is a regulatory body that grants recognition to universities.")
   + "Which of the statements are correct?",
   ["I and II only", "I, III and IV only", "II, III and IV only", "I, II and III only"], "D",
   "NIRF is a ranking framework, not a regulator; it neither recognises nor accredits. So (IV) is false.", "policies"),

 Q("Under which provision is an institution declared a deemed-to-be university?",
   ["Section 12B of the UGC Act", "Section 3 of the UGC Act", "Article 30 of the Constitution",
    "Section 2(f) of the UGC Act"], "B",
   "Section 3 of the UGC Act, 1956 empowers the Central Government, on the advice of the UGC, to declare an "
   "institution of higher education to be deemed a university.", "policies"),

 Q("Match the university body or officer in List I with the function in List II."
   + match(["Vice-Chancellor", "Academic Council", "Executive Council", "Chancellor"],
           ["Head of the university, usually by virtue of another office", "Administration and finance",
            "Chief executive and academic officer", "Courses, examinations and academic standards"]),
   ["(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)", "(a)-(iv), (b)-(iii), (c)-(ii), (d)-(i)",
    "(a)-(iii), (b)-(ii), (c)-(iv), (d)-(i)", "(a)-(i), (b)-(iv), (c)-(ii), (d)-(iii)"], "A",
   "The Vice-Chancellor runs the university; the Academic Council decides academic matters; the Executive "
   "Council (Syndicate) manages administration and finance; the Chancellor is the formal head.", "policies"),

 Q(ar("Both Parliament and the state legislatures can make laws on education.",
      "Education is a subject in the Concurrent List of the Seventh Schedule."),
   AR, "A",
   "Subjects in the Concurrent List are open to both the Union and the states, and education has been there "
   "since the 42nd Amendment of 1976. Both statements are true and (R) explains (A).", "policies"),

 Q("The Indian Institutes of Technology are:",
   ["deemed-to-be universities", "state universities", "Institutions of National Importance, created by Act of Parliament",
    "autonomous colleges affiliated to central universities"], "C",
   "The IITs, like AIIMS and some other institutes, are Institutions of National Importance established by "
   "Acts of Parliament, with the power to award their own degrees.", "policies"),
]
