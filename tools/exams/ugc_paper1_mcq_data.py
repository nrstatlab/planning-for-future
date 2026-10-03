# -*- coding: utf-8 -*-
"""The model MCQs of UGC NET Paper I, from which ugc_paper1_mcqs.py writes
exams/ugc-net/paper-1/mcqs.html.

Each question is (stem, [A, B, C, D], key, explanation), in HTML. Unit 3 is
four passages of five questions; a ("PASSAGE", label, html) entry precedes the
five questions it serves.

Written by Claude and checked by recheck_ugc_paper1.py; a unit is scored in the
web application only once the owner has approved it, and APPROVED records the
date of that approval (the page carries it as data-approved on the unit's
heading). A unit is added to UNITS in the batch that writes its notes.
"""

APPROVED = {}

U1 = [
 ("Who proposed the memory level of teaching?", ["J. F. Herbart", "H. C. Morrison", "H. Hunt", "B. S. Bloom"], "A",
  "The memory level, the lowest and most teacher-centred, is Herbart's; the understanding level is Morrison's and the reflective level Hunt's."),
 ("The reflective level of teaching is associated with:", ["Herbart", "Morrison", "Hunt", "Skinner"], "C",
  "Hunt's reflective level is the highest: learner-centred, built on problem-solving and critical thinking."),
 ("In the revised taxonomy of Anderson and Krathwohl (2001), the highest level of the cognitive domain is:", ["Evaluate", "Synthesis", "Analyse", "Create"], "D",
  "The revision renamed the levels as verbs and put <em>create</em> (once synthesis) above <em>evaluate</em>. Synthesis is the old name, not a level of the revision."),
 ("\"Valuing\" is a level of which domain of educational objectives?", ["Affective", "Cognitive", "Psychomotor", "Conative"], "A",
  "The affective domain (Krathwohl, Bloom and Masia, 1964) runs receiving, responding, valuing, organisation, characterisation."),
 ("The phase of teaching in which the teacher decides objectives, content and method is the:", ["Interactive phase", "Post-active phase", "Pre-active phase", "Evaluative phase"], "C",
  "Planning comes before the class: the pre-active phase. The interactive phase is the class itself; the post-active phase is evaluation afterwards."),
 ("A teacher starts with the scores of a real cricket match before defining the arithmetic mean. Which maxim is being followed?", ["Abstract to concrete", "Concrete to abstract", "General to particular", "Logical to psychological"], "B",
  "Real scores are concrete; the definition is abstract. The maxim is concrete to abstract (and particular to general, not general to particular)."),
 ("Andragogy, the art and science of helping adults learn, was popularised by:", ["Malcolm Knowles", "Jean Piaget", "Erik Erikson", "Edgar Dale"], "A",
  "Knowles set andragogy against pedagogy. Piaget described cognitive stages, Erikson psychosocial stages, Dale the cone of experience."),
 ("In Piaget's theory, abstract and hypothetical reasoning develops from about the age of eleven, in the:", ["Sensorimotor stage", "Pre-operational stage", "Concrete operational stage", "Formal operational stage"], "D",
  "Formal operations begin around eleven or twelve, which is why adolescents can handle abstract ideas that younger children cannot."),
 ("Which is NOT one of Knowles' assumptions about adult learners?", ["They are self-directed", "Their orientation is problem-centred", "Their motivation is mainly external", "Their experience is a resource for learning"], "C",
  "Knowles held that adults' motivation is mainly internal (self-esteem, satisfaction, quality of life). The other three are among his assumptions."),
 ("A class of 150 students taught together in one hall is a factor affecting teaching related mainly to:", ["The learner", "Support material", "The teacher's personality", "The institution"], "D",
  "Class size is set by the institution's policies and resources, so it is an institutional factor."),
 ("Which of these is a learner-centred method?", ["Lecture", "Demonstration", "Project method", "Recitation"], "C",
  "In the project method learners plan and carry out a purposeful task; the teacher guides. Lecture, demonstration and recitation are teacher-centred."),
 ("The project method of teaching was developed by:", ["W. H. Kilpatrick", "H. E. Armstrong", "Helen Parkhurst", "B. F. Skinner"], "A",
  "Kilpatrick set it out in 1918, drawing on Dewey. Armstrong is known for the heuristic method, Parkhurst for the Dalton plan, Skinner for programmed instruction."),
 ("Programmed instruction, in small steps with immediate feedback, is associated with:", ["Fred Keller", "B. F. Skinner", "Alex Osborn", "Ned Flanders"], "B",
  "Skinner's linear programming grew from his work on reinforcement. Keller devised the Personalised System of Instruction, Osborn brainstorming, Flanders interaction analysis."),
 ("In a flipped classroom:", ["Learners meet the content before class and use class time for problems and discussion", "The teacher lectures in class and sets exercises as homework", "All teaching is online and there are no classes", "There is no assessment"], "A",
  "The usual order is flipped: first contact with the content is at home (video, reading), and class time is for active work."),
 ("SWAYAM stands for:", ["System for Web-based Advanced Youth Academic Modules", "Study Without Age Yet Aiming at Mastery", "Study Webs of Active-Learning for Young Aspiring Minds", "Scheme for Web Access for Young Academic Minds"], "C",
  "SWAYAM, launched in 2017, is the Government of India's MOOC platform: Study Webs of Active-Learning for Young Aspiring Minds."),
 ("Which is NOT one of the four quadrants of a SWAYAM course?", ["E-tutorial", "E-content", "Discussion forum", "Classroom attendance"], "D",
  "The four quadrants are e-tutorial, e-content, self-assessment and a discussion forum. Attendance in a classroom is not part of a MOOC."),
 ("In Edgar Dale's Cone of Experience, the most abstract experiences, at the top of the cone, are:", ["Direct, purposeful experiences", "Verbal symbols", "Demonstrations", "Field trips"], "B",
  "Direct, purposeful experiences form the base; verbal symbols, which depend on words alone, sit at the top."),
 ("Evaluation carried out during teaching, to give feedback that improves learning while it is going on, is:", ["Summative", "Formative", "Placement", "Norm-referenced"], "B",
  "Formative evaluation happens during teaching and shapes it; summative evaluation judges at the end. Scriven introduced the two terms in 1967."),
 ("A test that compares each candidate's performance with a fixed standard of mastery, not with other candidates, is:", ["Norm-referenced", "Diagnostic", "Placement", "Criterion-referenced"], "D",
  "Criterion-referenced tests measure against a standard; norm-referenced tests rank candidates against one another (Glaser, 1963)."),
 ("Under CBCS a student earns grade points 8, 6 and 10 in courses of 4, 3 and 3 credits. The SGPA is:", ["8.0", "7.9", "8.2", "8.4"], "A",
  "SGPA = (4&times;8 + 3&times;6 + 3&times;10) / (4 + 3 + 3) = (32 + 18 + 30) / 10 = 8.0. Here the simple mean of the grade points is also 8.0, but only by chance: always weight by credits."),
]

U2 = [
 ("Action research, in which practitioners study and improve their own practice, was introduced by:", ["Kurt Lewin", "Karl Popper", "Auguste Comte", "Max Weber"], "A",
  "Lewin introduced action research in the 1940s; Stephen Corey took it into education. Popper is known for falsification, Comte for positivism, Weber for Verstehen."),
 ("Research carried out to solve an immediate practical problem is called:", ["Fundamental research", "Applied research", "Conceptual research", "Historical research"], "B",
  "Applied research aims at a practical solution; fundamental (pure) research aims to extend knowledge or theory."),
 ("Positivism as a philosophy of knowledge is associated with:", ["Karl Popper", "Max Weber", "Barney Glaser", "Auguste Comte"], "D",
  "Comte founded positivism. Popper's falsification underlies post-positivism; Weber's Verstehen, interpretivism; Glaser, grounded theory."),
 ("The principle that a scientific statement must be capable of being shown false is:", ["Verification", "Falsification", "Triangulation", "Replication"], "B",
  "Popper's falsification: one black swan refutes \"all swans are white\", but no number of white swans proves it."),
 ("Which method of research can directly establish a cause-and-effect relationship?", ["Survey", "Case study", "Experimental", "Historical"], "C",
  "Only the experimental method manipulates the presumed cause while controlling other variables. Surveys and case studies can show association, not cause."),
 ("A design with an experimental and a control group, but without random assignment to them, is:", ["True experimental", "Pre-experimental", "Ex post facto", "Quasi-experimental"], "D",
  "Random assignment is what makes a design truly experimental. A control group without it is quasi-experimental; one group without a control is pre-experimental."),
 ("In historical research, the process of checking whether a document is genuine is called:", ["Internal criticism", "External criticism", "Content analysis", "Triangulation"], "B",
  "External criticism tests authenticity (is it what it claims to be?); internal criticism tests the credibility of its content."),
 ("Grounded theory, which builds theory from the data rather than testing it, was developed by:", ["Campbell and Stanley", "Lazarsfeld and Katz", "Glaser and Strauss", "McCombs and Shaw"], "C",
  "Barney Glaser and Anselm Strauss, <em>The Discovery of Grounded Theory</em> (1967). Campbell and Stanley classified experimental designs."),
 ("A researcher studying a hidden population with no list of its members asks each participant to name others. This is:", ["Systematic sampling", "Stratified sampling", "Snowball sampling", "Cluster sampling"], "C",
  "Snowball sampling grows through referrals and suits hidden populations. The other three are probability methods that need a list or frame."),
 ("Which of the following is a probability sampling method?", ["Quota sampling", "Purposive sampling", "Convenience sampling", "Stratified random sampling"], "D",
  "In stratified random sampling every unit has a known chance of selection. Quota, purposive and convenience sampling are non-probability methods."),
 ("Arrange in the usual order: (i) review of literature (ii) data collection (iii) identifying the problem (iv) formulating hypotheses.", ["iii, i, iv, ii", "i, iii, iv, ii", "iii, iv, i, ii", "iv, iii, i, ii"], "A",
  "The problem comes first; the literature review shows what is known; hypotheses follow from both; data are collected to test them."),
 ("In a study of the effect of a teaching method on achievement, achievement is the:", ["Independent variable", "Dependent variable", "Extraneous variable", "Intervening variable"], "B",
  "The teaching method is the presumed cause (independent); achievement is the outcome measured (dependent)."),
 ("A hypothesis stating that there is no difference between two groups is the:", ["Alternative hypothesis", "Directional hypothesis", "Null hypothesis", "Research hypothesis"], "C",
  "The null hypothesis states no difference or no relation; it is the one tested statistically."),
 ("The referencing style that cites author and page in the text, as in (Rao 45), is:", ["MLA", "APA", "Vancouver", "IEEE"], "A",
  "MLA uses author&ndash;page. APA uses author&ndash;date (Rao, 2019); Vancouver and IEEE number their references."),
 ("In footnotes, \"ibid.\" means:", ["The same source as the previous note", "The work already cited, at another place", "Compare", "And others"], "A",
  "<em>Ibid.</em> (ibidem, in the same place) refers to the source cited immediately before. <em>Op. cit.</em> is the work already cited; <em>cf.</em> is compare; <em>et al.</em> is and others."),
 ("A researcher's six papers are cited 12, 10, 7, 5, 3 and 1 times. The researcher's h-index is:", ["3", "4", "5", "6"], "B",
  "Four papers have at least 4 citations (12, 10, 7, 5), but there are not five papers with at least 5 (the fifth has 3). So h = 4."),
 ("Shodhganga, maintained by INFLIBNET, is:", ["Plagiarism-detection software", "A MOOC platform", "A list of approved journals", "A repository of Indian PhD theses"], "D",
  "Shodhganga holds theses submitted to Indian universities. Plagiarism-detection software is provided through Shodh Shuddhi; SWAYAM is the MOOC platform."),
 ("Under the UGC plagiarism regulations of 2018, similarity of up to 10% is:", ["Level 0", "Level 1", "Level 2", "Level 3"], "A",
  "Level 0, up to 10%, is minor similarity and carries no penalty. Level 1 is above 10% to 40%, Level 2 above 40% to 60%, Level 3 above 60%."),
 ("In research misconduct, fabrication means:", ["Copying another's work without credit", "Changing data to fit the hypothesis", "Publishing the same work twice", "Making up data or results"], "D",
  "Fabrication is inventing data; falsification is changing them; plagiarism is copying without credit. Together they are the three serious forms of misconduct."),
 ("The three ethical principles of the Belmont Report (1979) are:", ["Consent, confidentiality and anonymity", "Validity, reliability and objectivity", "Respect for persons, beneficence and justice", "Honesty, openness and accountability"], "C",
  "The Belmont Report's principles are respect for persons, beneficence and justice; informed consent is how respect for persons is applied."),
]

P1 = """<p>For most of the twentieth century, India's farms drew their water from canals and tanks; today the larger share of irrigated land is watered from wells. The change brought great gains. A farmer with a tube well need not wait for a canal's turn; she can water when the crop needs it, and yields have risen accordingly. But groundwater is a bank account that is refilled only by the rain that soaks into the soil, and in many districts more is withdrawn each year than the monsoon returns. Water tables have fallen so far in places that wells must be deepened every few years, at a cost the poorest farmers cannot meet.</p>
<p>The difficulty is that no single farmer gains by holding back: water she leaves in the ground may simply be pumped by a neighbour. Free or cheap electricity for pumps, introduced to help farmers, has made the problem worse by removing the one cost that might have encouraged restraint. Some villages have shown another way. By agreeing among themselves which crops to grow and how much to pump, and by building small structures that slow run-off and let rain soak in, they have stabilised their water tables. Their experience suggests that the answer lies less in new technology than in new rules, made by those who share the resource.</p>"""

P2 = """<p>Before a scientific paper is published in a reputable journal, it is usually sent to two or three experts in the field who are not its authors. These reviewers judge whether the question is worth asking, whether the methods can answer it, and whether the conclusions follow from the results. They may recommend that the paper be accepted, revised or rejected. The system, called peer review, is often described as the gatekeeper of science.</p>
<p>Gatekeeper is too strong a word. Reviewers rarely see the raw data and almost never repeat the experiment; they judge the paper as it is written. They can miss honest errors, and a determined fraud may pass them altogether. Their judgement can also be coloured by the authors' reputation, which is why many journals now hide the authors' names from reviewers. None of this means that peer review is worthless: it catches many weak arguments and improves most of the papers that pass through it. But a reader should treat publication as a sign that a paper has been checked for sense, not as a guarantee that its findings are true. That guarantee, as far as science offers one, comes only when other researchers, working independently, find the same result.</p>"""

P3 = """<p>Children who begin school in a language they do not speak at home face two tasks at once: learning to read, and learning the language in which reading is taught. Many manage both, but many fall behind in the first years and never catch up. Studies in several countries have found that children taught first in their mother tongue learn to read sooner, and later learn a second language at least as well as children taught in it from the start. The skills of reading, it seems, transfer from one language to another; what does not transfer is the understanding of words never heard before.</p>
<p>Why, then, do many parents prefer that their children be taught from the first day in a language of wider use, such as English? Their reasons are not foolish. That language opens doors to higher education and to jobs, and parents fear that a child taught first at home will be left behind. The research suggests that their aim and the mother-tongue approach need not conflict: a strong start in the home language, with the second language introduced gradually and taught well, may be the surest route to the very fluency parents want. The difficulty is practical. It needs teachers and books in many languages, which poorer school systems find hard to provide.</p>"""

P4 = """<p>Every winter, thousands of volunteers in many countries spend a few hours counting the birds they see and send their tallies to a central database. No single count is precise: volunteers differ in skill, some days are cloudy, and a rare bird may be recorded twice or missed altogether. Yet taken together, over decades, such counts have revealed changes that no team of professionals could have measured alone, such as the slow northward shift of many species' winter ranges.</p>
<p>The value of such citizen science depends on its design. Volunteers must follow the same simple method, count for a fixed time in a fixed place, and record not only what they saw but how long they looked. With these details, statisticians can correct for differences in effort and skill. Without them, a rise in the number of birds recorded might mean only a rise in the number of people looking. The lesson reaches beyond birds: large amounts of imperfect data can answer questions that small amounts of perfect data cannot, provided the way the data were gathered is known.</p>"""

U3 = [
 ("PASSAGE", "Passage 1 (Questions 1&ndash;5)", P1),
 ("The passage is mainly about:", ["How tube wells have raised crop yields in India", "The gains of groundwater irrigation, its overuse, and how shared rules may help", "Why free electricity for farmers should be abolished", "Why canals are better than wells"], "B",
  "The first paragraph gives the gains and the overuse; the second, why it happens and what some villages did. (A) is one detail; (C) goes beyond the passage, which says cheap power worsened the problem but proposes no abolition; (D) is never argued."),
 ("According to the passage, why does no single farmer gain by pumping less?", ["The water she leaves may be pumped by a neighbour", "Her pump costs too much to run", "The monsoon refills her well every year", "Canals supply her instead"], "A",
  "The passage says so directly: \"water she leaves in the ground may simply be pumped by a neighbour\". (C) contradicts it: more is withdrawn than the monsoon returns."),
 ("In the passage, \"stabilised\" most nearly means:", ["Raised sharply", "Measured accurately", "Stopped from falling further", "Sold to neighbours"], "C",
  "The villages stopped the decline of their water tables. Nothing says the tables rose sharply, so (A) claims too much."),
 ("The author would most likely agree that:", ["New pumping technology will solve the problem", "Groundwater can never be replenished", "Poor farmers pump the most water", "Cooperation among those who share a resource can protect it"], "D",
  "The last sentence: the answer lies \"in new rules, made by those who share the resource\". (A) is what the author plays down; (B) contradicts \"refilled only by the rain\"."),
 ("The comparison of groundwater to \"a bank account\" is used to:", ["Explain that withdrawing more than is deposited runs the resource down", "Show that farmers have become wealthy", "Suggest that banks should pay for wells", "Describe how canals were run"], "A",
  "Rain is the deposit, pumping the withdrawal; when withdrawals exceed deposits, the balance (the water table) falls."),
 ("PASSAGE", "Passage 2 (Questions 6&ndash;10)", P2),
 ("The passage is mainly concerned with:", ["How to write a scientific paper", "The role and the limits of peer review", "Fraud in science", "Why journals hide authors' names"], "B",
  "It describes what peer review does and then what it cannot do. Fraud and hidden names are single points within that."),
 ("According to the passage, reviewers usually:", ["Repeat the experiment", "Examine the raw data", "Judge the paper as it is written", "Decide whether the authors are promoted"], "C",
  "\"Reviewers rarely see the raw data and almost never repeat the experiment; they judge the paper as it is written.\""),
 ("Why do many journals now hide the authors' names from reviewers?", ["Because reviewers' judgement can be coloured by the authors' reputation", "To save space in the journal", "To prevent fraud altogether", "Because authors ask them to"], "A",
  "The passage links the practice to reputation. It does not claim that hiding names prevents fraud; it says fraud may pass review."),
 ("It can be inferred that, in the author's view, the strongest evidence that a finding is true is:", ["Publication in a reputable journal", "Independent replication by other researchers", "Approval by three reviewers", "The reputation of the authors"], "B",
  "\"That guarantee &hellip; comes only when other researchers, working independently, find the same result.\" Publication is only \"a sign that a paper has been checked for sense\"."),
 ("The author regards the phrase \"gatekeeper of science\" as:", ["Exactly right", "An insult to reviewers", "Irrelevant", "An overstatement"], "D",
  "\"Gatekeeper is too strong a word.\" The author still values peer review, so (B) is wrong."),
 ("PASSAGE", "Passage 3 (Questions 11&ndash;15)", P3),
 ("Which best states the main idea of the passage?", ["Children should never be taught in English", "Parents who prefer English are foolish", "Starting school in the mother tongue can help both reading and later second-language learning, though it is hard to provide", "Reading skills cannot pass from one language to another"], "C",
  "The passage gives the evidence for a mother-tongue start, reconciles it with parents' aims, and names the practical difficulty. (B) contradicts \"their reasons are not foolish\"; (D) contradicts \"the skills of reading &hellip; transfer\"."),
 ("According to the passage, what does NOT transfer from one language to another?", ["The skills of reading", "Confidence in class", "The ability to write", "Understanding of words never heard before"], "D",
  "\"What does not transfer is the understanding of words never heard before.\" Reading skills, by contrast, do transfer."),
 ("The author's attitude to parents who prefer English from the first day is:", ["Understanding", "Contemptuous", "Indifferent", "Hostile"], "A",
  "The author explains their reasons (\"not foolish\": higher education, jobs) and argues their aim can be met another way."),
 ("The passage implies that a mother-tongue start:", ["Guarantees a good job", "May be the surest route to the fluency in a second language that parents want", "Should replace all teaching of a second language", "Costs nothing to provide"], "B",
  "The second paragraph says so. (C) contradicts \"the second language introduced gradually\"; (D) contradicts the last two sentences."),
 ("\"The difficulty is practical\" refers to:", ["The methods of teaching reading", "Parents' attitudes", "Providing teachers and books in many languages", "Children's ability to learn"], "C",
  "The next sentence explains it: the approach \"needs teachers and books in many languages\"."),
 ("PASSAGE", "Passage 4 (Questions 16&ndash;20)", P4),
 ("The best title for the passage is:", ["Many Imperfect Counts, Well Designed", "Why Volunteers Make Mistakes", "The Northward Shift of Birds", "Careers in Ornithology"], "A",
  "The passage is about how many imprecise counts, gathered by a known method, become valuable. (B) and (C) are single points."),
 ("Volunteers must record how long they looked so that:", ["They can be paid for their time", "Rare birds are not missed", "Each count becomes precise", "Statisticians can correct for differences in effort"], "D",
  "\"With these details, statisticians can correct for differences in effort and skill.\" Recording time does not make a single count precise."),
 ("\"A rise in the number of birds recorded might mean only a rise in the number of people looking.\" This sentence illustrates:", ["That birds are increasing", "Why the effort behind each count must be recorded", "That volunteers are dishonest", "That such counts are useless"], "B",
  "Without a record of effort, more observers would look like more birds. The passage does not say the counts are useless."),
 ("The author's tone towards citizen science is:", ["Dismissive", "Alarmed", "Balanced and appreciative", "Sarcastic"], "C",
  "The author admits each count's imprecision and praises what the counts reveal together."),
 ("Which statement is NOT supported by the passage?", ["A single count is imprecise", "Counts over decades revealed shifts in winter ranges", "Details of method let statisticians correct for effort", "Professionals could have measured these changes more easily on their own"], "D",
  "The passage says the opposite: the counts \"revealed changes that no team of professionals could have measured alone\"."),
]

U4 = [
 ("\"Who says what, in which channel, to whom, with what effect?\" is the model of communication given by:", ["Shannon and Weaver", "David Berlo", "Harold Lasswell", "Wilbur Schramm"], "C",
  "Lasswell's verbal model (1948) names the five questions."),
 ("The concept of \"noise\" in a model of communication was introduced by:", ["Aristotle", "Harold Lasswell", "Frank Dance", "Shannon and Weaver"], "D",
  "Shannon and Weaver's mathematical model (1948&ndash;49) added noise, anything that distorts the signal between transmitter and receiver."),
 ("In Berlo's SMCR model, the letters stand for:", ["Source, Message, Channel, Receiver", "Sender, Medium, Code, Response", "Signal, Message, Context, Reply", "Source, Meaning, Communication, Result"], "A",
  "Berlo (1960): Source, Message, Channel, Receiver, each with its own elements (skills, attitudes, knowledge, culture)."),
 ("Schramm's model of communication emphasises:", ["The overlap of the sender's and receiver's fields of experience", "A one-way flow from sender to receiver", "The capacity of the channel", "Communication growing like a helix"], "A",
  "Schramm (1954): communication works where the fields of experience overlap; his model is circular and interactive. The helix is Dance's."),
 ("A report sent by a subordinate to a superior is an example of:", ["Downward communication", "Horizontal communication", "Diagonal communication", "Upward communication"], "D",
  "Upward communication runs from subordinate to superior; downward, the other way; horizontal, between equals."),
 ("The grapevine in an organisation is an example of:", ["Formal communication", "Mass communication", "Informal communication", "Intrapersonal communication"], "C",
  "The grapevine runs outside official channels: informal communication."),
 ("The study of the use of space and distance in communication is called:", ["Kinesics", "Haptics", "Proxemics", "Chronemics"], "C",
  "Proxemics (Edward T. Hall). Kinesics is body movement, haptics touch, chronemics time."),
 ("Chronemics is the study of the use of:", ["Touch", "Eye contact", "Voice", "Time"], "D",
  "Chronemics covers punctuality, waiting and pauses: how time communicates."),
 ("Paralanguage refers to:", ["How words are said: pitch, tone, volume and pace", "Sign language", "Body posture", "Written symbols"], "A",
  "Paralanguage (vocalics) is the vocal part of speech other than the words themselves."),
 ("In Edward T. Hall's proxemics, the social distance zone is about:", ["Up to 45 cm", "45 cm to 1.2 m", "1.2 m to 3.6 m", "Beyond 3.6 m"], "C",
  "Intimate up to about 45 cm, personal about 45 cm to 1.2 m, social about 1.2 to 3.6 m, public beyond about 3.6 m."),
 ("Mehrabian's \"7&ndash;38&ndash;55\" finding applies to:", ["All communication", "Written communication", "Communication of feelings and attitudes when words and tone disagree", "Mass media"], "C",
  "The finding concerned messages about feelings and attitudes with inconsistent cues. Applying it to all communication is a common misquotation."),
 ("The distinction between high-context and low-context cultures was made by:", ["Geert Hofstede", "Bruce Tuckman", "Irving Janis", "Edward T. Hall"], "D",
  "Hall, in <em>Beyond Culture</em> (1976). Hofstede gave the dimensions of national culture; Tuckman the stages of groups; Janis groupthink."),
 ("Which is NOT one of Hofstede's dimensions of culture?", ["Power distance", "Uncertainty avoidance", "Individualism and collectivism", "High context and low context"], "D",
  "High and low context is Hall's distinction, not one of Hofstede's dimensions."),
 ("The correct order of Tuckman's stages of group development is:", ["Forming, norming, storming, performing", "Forming, storming, norming, performing", "Storming, forming, norming, performing", "Norming, forming, storming, performing"], "B",
  "Forming, storming, norming, performing (1965); adjourning was added in 1977."),
 ("In Flanders' Interaction Analysis Categories System, category 4 is:", ["Praises or encourages", "Asks questions", "Lectures", "Criticises or justifies authority"], "B",
  "Categories 1&ndash;4 are indirect teacher talk: 1 accepts feeling, 2 praises, 3 accepts or uses ideas, 4 asks questions. Lecturing is 5; criticising is 7."),
 ("How many categories does Flanders' Interaction Analysis Categories System have?", ["7", "10", "8", "12"], "B",
  "Ten: seven of teacher talk, two of student talk, and one for silence or confusion."),
 ("A lecturer uses technical terms with first-year students without explaining them. This is:", ["A physical barrier", "A semantic barrier", "A physiological barrier", "An organisational barrier"], "B",
  "Semantic barriers arise from language: jargon, ambiguity, unfamiliar words."),
 ("\"The medium is the message\" was said by:", ["Marshall McLuhan", "Wilbur Schramm", "Harold Lasswell", "Paul Lazarsfeld"], "A",
  "McLuhan, <em>Understanding Media</em> (1964), who also gave us the \"global village\"."),
 ("According to the agenda-setting theory of McCombs and Shaw, the mass media:", ["Tell people what to think", "Tell people what to think about", "Have no effect on public opinion", "Inject messages into a passive audience"], "B",
  "The media decide which issues people consider important, not their opinions on them. (D) describes the hypodermic needle theory."),
 ("India's first newspaper, Hicky's Bengal Gazette, began in:", ["1780", "1822", "1857", "1936"], "A",
  "James Augustus Hicky started it in Calcutta in 1780. 1936 is the year the name All India Radio was adopted."),
]

UNITS = [
 (1, "Teaching Aptitude", "Levels and objectives of teaching, learners, methods, SWAYAM, support systems, evaluation, CBCS.", U1),
 (2, "Research Aptitude", "Types and methods of research, positivism, steps, sampling, referencing, ICT, ethics.", U2),
 (3, "Comprehension", "Four passages, five questions each: main idea, detail, inference, vocabulary, tone.", U3),
 (4, "Communication", "Models, types, non-verbal cues, culture and groups, classroom talk, barriers, mass media.", U4),
]
