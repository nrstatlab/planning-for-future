# -*- coding: utf-8 -*-
"""UGC NET Paper I, Unit 1: fifty exam-standard model questions."""
from . import AR, Q, ar, match, st

TITLE = "Teaching Aptitude"
BLURB = ("Teaching and its levels, learners and their differences, the factors that affect teaching, methods "
         "off-line and on-line, teaching support systems, and evaluation, including the Choice Based Credit "
         "System and computer-based testing.")

QUESTIONS = [
 Q("Consider the statements about teaching:"
   + st("It is a tripolar process joining the teacher, the learner and the content.",
        "Its test is the learning that results, not the talk that was given.",
        "In Jackson's scheme, the pre-active phase is the phase of evaluating and revising.",
        "It is both an art and a science.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and IV only", "II, III and IV only", "I, II, III and IV"], "B",
   "(I), (II) and (IV) are the standard ideas about teaching. (III) is false: the pre-active phase is planning "
   "(objectives, content, method); the interactive phase is the class itself; evaluating and revising belong "
   "to the post-active phase.", "concept"),

 Q("Match the item in List I with its entry in List II."
   + match(["Highest level of the cognitive domain in the 2001 revision", "Levels of the affective domain",
            "Levels of the psychomotor domain (Dave)", "Highest level of the cognitive domain in Bloom (1956)"],
           ["Evaluation", "Create", "Receiving, responding, valuing", "Imitation, manipulation, precision"]),
   ["(a)-(i), (b)-(iii), (c)-(iv), (d)-(ii)", "(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)",
    "(a)-(iii), (b)-(ii), (c)-(iv), (d)-(i)", "(a)-(ii), (b)-(iii), (c)-(iv), (d)-(i)"], "D",
   "Bloom's original cognitive domain ended with evaluation; the revision by Anderson and Krathwohl renamed "
   "the levels as verbs and placed create (the old synthesis) above evaluate. The affective domain runs from "
   "receiving to characterisation; Dave's psychomotor levels begin with imitation, manipulation and precision.", "concept"),

 Q("Arrange the levels of the revised taxonomy of the cognitive domain from the lowest to the highest: "
   "(1) Analyse, (2) Remember, (3) Create, (4) Understand, (5) Evaluate, (6) Apply.",
   ["2, 4, 6, 1, 5, 3", "2, 4, 1, 6, 5, 3", "2, 6, 4, 1, 3, 5", "4, 2, 6, 1, 5, 3"], "A",
   "Remember, understand, apply, analyse, evaluate, create. Each level builds on the ones below it, and "
   "<em>create</em> is at the top, above <em>evaluate</em>.", "concept"),

 Q("A teacher writes the objective: &ldquo;Students will compare two sampling methods and judge which of them "
   "suits a given survey, giving reasons.&rdquo; In the revised taxonomy this objective is mainly at the level:",
   ["Apply", "Understand", "Evaluate", "Remember"], "C",
   "Judging between alternatives against criteria, with reasons, is <em>evaluate</em>. Listing the methods "
   "would be remember, explaining them understand, and using one in a new survey apply. The verb of the "
   "objective tells the level.", "concept"),

 Q("The maxim of teaching &ldquo;from the psychological to the logical&rdquo; means that a teacher should:",
   ["explain the psychology of learning before the logic of the subject",
    "begin from the learner's interest and experience and arrive at the logical order of the subject",
    "teach abstract rules first and examples afterwards",
    "arrange content strictly as the textbook does"], "B",
   "The psychological order is the order in which the learner can take the matter in, starting from what "
   "interests them; the logical order is the systematic order of the subject itself. Good teaching starts with "
   "the first and ends with the second.", "concept"),

 Q("Morrison's teaching model for the understanding level has five steps. Their correct sequence is:",
   ["preparation, presentation, comparison, generalisation, application",
    "exploration, assimilation, presentation, recitation, organisation",
    "presentation, exploration, organisation, assimilation, recitation",
    "exploration, presentation, assimilation, organisation, recitation"], "D",
   "Morrison: exploration, presentation, assimilation, organisation, recitation. The first option is the "
   "Herbartian sequence for the memory level, not Morrison's.", "levels"),

 Q(ar("The reflective level is the highest level of teaching.",
      "It requires the learner to solve problems by critical and original thinking, which presupposes memory "
      "and understanding."),
   AR, "A",
   "Each level of teaching assumes the one below it. Reflective teaching (Hunt) puts the learner before a "
   "problem to be defined, hypothesised about and tested, which cannot be done without facts and understanding. "
   "Both statements are true and (R) is the reason.", "levels"),

 Q("After a lesson on the five-year plans, the learners can explain why the emphasis of planning moved from "
   "agriculture to industry. The lesson has reached the:",
   ["memory level", "reflective level", "understanding level", "autonomous development level"], "C",
   "Explaining a relation or reason is grasp of meaning: the understanding level (Morrison), &lsquo;memory "
   "plus insight&rsquo;. Reciting the dates of the plans would be the memory level; arguing, with evidence, what "
   "the next plan should give priority to would be the reflective level.", "levels"),

 Q("The Herbartian steps of a memory-level lesson, in the correct order, are:",
   ["presentation, preparation, comparison, application, generalisation",
    "preparation, presentation, comparison, generalisation, application",
    "preparation, comparison, presentation, generalisation, application",
    "exploration, presentation, assimilation, organisation, recitation"], "B",
   "Preparation, presentation, comparison (association), generalisation, application: set out by Herbart's "
   "followers from his teaching. The last option is Morrison's model for the understanding level.", "levels"),

 Q("Consider the statements about the levels of teaching:"
   + st("At the memory level the teacher is dominant and the learner passive.",
        "The understanding level may be described as memory plus insight.",
        "The reflective level is the most teacher-centred of the three.",
        "Each level assumes the level below it.")
   + "Which of the statements are correct?",
   ["I, II and IV only", "I and II only", "II, III and IV only", "I, II, III and IV"], "A",
   "(III) is false: the reflective level is the most learner-centred; the teacher only creates the problem "
   "situation. The memory level is the most teacher-centred. The other three statements are correct.", "levels"),

 Q("From the answers to a short quiz a teacher notices that half the class confuses the mean with the median, "
   "and teaches the idea again with a new example. This shows that teaching is:",
   ["a one-way process", "summative", "authoritarian", "diagnostic and remedial"], "D",
   "Finding what learners have not yet understood (diagnosis) and acting on it (remedy) is a characteristic of "
   "good teaching. It also shows teaching as two-way: the quiz is feedback from learners to the teacher.", "characteristics"),

 Q("A teacher with full command of the subject gives a brilliant lecture that hardly any student can follow. "
   "The basic requirement of teaching that has not been met is:",
   ["subject knowledge of the teacher", "availability of content", "readiness of the learners",
    "a way of evaluating"], "C",
   "Teaching needs learners who are ready: the teacher must start from what they already know. A teacher and "
   "content were present; the lecture failed because it did not begin where the learners were.", "characteristics"),

 Q("Consider the statements about the characteristics of good teaching:"
   + st("It is interactive, with feedback in both directions.", "It is purposeful and planned.",
        "It is democratic, inviting questions and allowing disagreement.",
        "It can be called successful even if it brings about no change in the learner.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "II, III and IV only", "I, II, III and IV"], "B",
   "Teaching ends in learning: teaching that changes nothing in the learner has not succeeded, so (IV) is "
   "false. The first three are the characteristics the paper asks about.", "characteristics"),

 Q("Match the thinker in List I with the idea in List II."
   + match(["Jean Piaget", "Erik Erikson", "Malcolm Knowles", "Howard Gardner"],
           ["Andragogy", "Multiple intelligences", "Formal operational stage", "Identity versus role confusion"]),
   ["(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)", "(a)-(i), (b)-(iv), (c)-(iii), (d)-(ii)"], "A",
   "Piaget: abstract thought develops in the formal operational stage, from about eleven. Erikson: adolescence "
   "is the stage of identity versus role confusion. Knowles popularised andragogy, the art and science of "
   "helping adults learn. Gardner (1983) proposed multiple intelligences.", "learners"),

 Q("Consider the following about adult learners, according to Knowles:"
   + st("They are self-directed.", "Their orientation to learning is problem-centred.",
        "They need to know why they are learning something.",
        "They prefer subject-centred learning to be stored for use in the distant future.")
   + "Which of these are among his assumptions?",
   ["I and II only", "II and III only", "I, II and III only", "I, II, III and IV"], "C",
   "Adults want learning they can use now, organised around the problems of their life roles, so (IV) is the "
   "opposite of Knowles's view. His other assumptions: experience is a resource, readiness comes from life "
   "roles, and motivation is mainly internal.", "learners"),

 Q("A course on data handling for working nurses begins with a real problem from the wards that the nurses "
   "themselves bring, and not with definitions. The course design follows:",
   ["pedagogy, because the teacher decides the content", "programmed instruction",
    "the memory level of teaching", "andragogy, because it is problem-centred and uses the learners' experience"], "D",
   "Andragogy treats the adults' experience as a resource and organises learning around problems they need to "
   "solve. Pedagogy, for children, is subject-centred and teacher-directed.", "learners"),

 Q("A first-year undergraduate class is found to work better in small groups with clear tasks and early, "
   "private feedback. The best explanation is that adolescent learners:",
   ["are self-directed and need no guidance", "are peer-oriented and sensitive to public criticism",
    "are motivated only by internal satisfaction", "reason mainly from long experience"], "B",
   "For adolescents the peer group matters greatly, identity is still forming and public correction hurts. "
   "They need structure and guidance. Self-direction, internal motivation and reasoning from experience are "
   "the marks of adult learners.", "learners"),

 Q(ar("Adult learners resist being treated like children.",
      "Adults have a self-concept of being responsible for their own decisions."),
   AR, "A",
   "One of Knowles's assumptions is that adults see themselves as responsible for their own lives; being "
   "directed at every step conflicts with that self-concept, and they resist it. Both statements are true and "
   "(R) explains (A).", "learners"),

 Q("Which of the following is NOT one of the intelligences in Howard Gardner's theory of multiple "
   "intelligences?",
   ["Bodily-kinaesthetic", "Intrapersonal", "Naturalistic", "Fluid"], "D",
   "Gardner's list: linguistic, logical-mathematical, spatial, musical, bodily-kinaesthetic, interpersonal, "
   "intrapersonal and (added later) naturalistic. Fluid intelligence belongs to Cattell's distinction between "
   "fluid and crystallised intelligence, a different theory.", "differences"),

 Q(ar("A teacher should use varied modes of presentation for the whole class and not label learners by "
      "a preferred learning style.",
      "Research has not shown that matching teaching to a learner's preferred style improves learning."),
   AR, "A",
   "Learning-style schemes such as Fleming's VARK (visual, aural, read/write, kinaesthetic) describe "
   "preferences, but the evidence does not show that teaching each learner in the preferred style helps. Varied "
   "modes help everyone. Both statements are true and (R) is the reason.", "differences"),

 Q("In a class some students solve a problem at once while others need a worked example. The teacher gives the "
   "first group an extension task and the second a guided one. This practice is:",
   ["streaming by ability into separate classes", "programmed instruction", "differentiated instruction",
    "summative evaluation"], "C",
   "Differentiated instruction adjusts tasks to learners' readiness inside one class: enrichment for the fast, "
   "support for the slow. It is how a teacher answers individual differences without separating the learners "
   "permanently.", "differences"),

 Q("Match the classroom situation in List I with the factor affecting teaching in List II."
   + match(["A class of 150 students in one section", "No microphone in the lecture hall",
            "Students afraid to ask questions", "An outdated textbook"],
           ["Learning environment", "Institution", "Support material", "Instructional facilities"]),
   ["(a)-(ii), (b)-(iii), (c)-(i), (d)-(iv)", "(a)-(ii), (b)-(iv), (c)-(i), (d)-(iii)",
    "(a)-(iv), (b)-(ii), (c)-(i), (d)-(iii)", "(a)-(i), (b)-(iv), (c)-(ii), (d)-(iii)"], "B",
   "Class size is decided by the institution's policies and resources. A microphone is an instructional "
   "facility. Fear of asking is a matter of classroom climate, the learning environment. A textbook is support "
   "material.", "factors"),

 Q("Which of the following pairs of a factor and an example is NOT correctly matched?",
   ["Learner &mdash; prior knowledge", "Teacher &mdash; enthusiasm", "Institution &mdash; time-table",
    "Support material &mdash; projector and internet connection"], "D",
   "Projectors, internet, laboratories, the library and seating are <em>instructional facilities</em>. Support "
   "material is what carries the content: textbooks, notes, models, charts, audio-visual aids and e-content.", "factors"),

 Q("Which of the following factors affecting teaching can an individual teacher change most directly?",
   ["The classroom climate", "The class size", "The policies of the institution", "The family background of learners"], "A",
   "The learning environment (classroom climate, teacher&ndash;student relations, freedom to ask) is largely "
   "of the teacher's own making. Class size and policies are institutional, and family background is a learner "
   "factor outside the teacher's control.", "factors"),

 Q("Consider the statements:"
   + st("Readiness to learn is a learner-related factor.", "E-content is a support material.",
        "The library is an instructional facility.", "Classroom discipline is an institutional factor.")
   + "Which of the statements are correct?",
   ["I and II only", "I and III only", "I, II and III only", "I, II, III and IV"], "C",
   "Discipline, classroom climate and relations among teacher and students make up the <em>learning "
   "environment</em>; institutional factors are policies, time-table, class size, leadership and resources. So "
   "(IV) is false.", "factors"),

 Q("Match the method in List I with the person associated with it in List II."
   + match(["Project method", "Heuristic method", "Dalton plan", "Personalised System of Instruction"],
           ["Helen Parkhurst", "Fred Keller", "W. H. Kilpatrick", "H. E. Armstrong"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)",
    "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "B",
   "Kilpatrick (1918) developed the project method from Dewey's ideas; Armstrong the heuristic method, in which "
   "the learner finds out for themselves; Parkhurst the Dalton plan of assignments done at the learner's pace; "
   "Keller the Personalised System of Instruction, with mastery of each unit before the next.", "methods"),

 Q("Students watch a recorded lecture and read a chapter at home; class time is then used for solving "
   "problems and discussion with the teacher's help. This arrangement is called:",
   ["programmed instruction", "the Dalton plan", "team teaching", "the flipped classroom"], "D",
   "In a flipped classroom the first meeting with the content happens before class, and class time, the "
   "scarce resource, is given to the harder work of applying it. It is a learner-centred arrangement.", "methods"),

 Q("Which of the following is NOT a feature of linear programmed instruction as developed by B. F. Skinner?",
   ["Learners compete in groups for the fastest answer", "Content is presented in small steps",
    "The learner gets immediate feedback on each response", "The learner proceeds at their own pace"], "A",
   "Programmed instruction is individual: small frames, an active response to each, immediate knowledge of "
   "results (reinforcement) and self-pacing. Group competition is no part of it.", "methods"),

 Q(ar("In brainstorming, criticism of the ideas offered is postponed.",
      "The purpose of brainstorming is to arrive quickly at the single correct idea."),
   AR, "C",
   "(A) is true: Osborn's rule is many ideas first, judgement later, because early criticism stops people "
   "from offering ideas. (R) is false: the aim is a large number and variety of ideas, from which the useful "
   "ones are sifted afterwards.", "methods"),

 Q("Which of the following lists contains only learner-centred methods?",
   ["Lecture, seminar, project", "Demonstration, discussion, case study", "Seminar, project, role play",
    "Recitation, brainstorming, lecture"], "C",
   "Lecture, demonstration and recitation are teacher-centred: the teacher presents and learners receive. "
   "Seminar, project, role play, discussion, case study and brainstorming make the learners active while the "
   "teacher guides.", "methods"),

 Q("A teacher-centred method such as the lecture is most suitable when:",
   ["the aim is to develop skills and attitudes", "a large class must be given new information in limited time",
    "learners are to be trained in problem-solving", "the lesson is at the reflective level"], "B",
   "The lecture is economical: one teacher, many learners, much information, little time. Skills, attitudes, "
   "problem-solving and reflective aims are better served by learner-centred methods.", "methods"),

 Q("Consider the statements about SWAYAM:"
   + st("It stands for Study Webs of Active-Learning for Young Aspiring Minds.", "It was launched in 2017.",
        "It offers courses at the postgraduate level only.", "Its courses follow a four-quadrant approach.")
   + "Which of the statements are correct?",
   ["I and II only", "II and IV only", "I, II, III and IV", "I, II and IV only"], "D",
   "SWAYAM is the Government of India's MOOC platform, launched in July 2017, with courses from school to "
   "postgraduate level, so (III) is false. The four quadrants are e-tutorial, e-content, self-assessment and "
   "a discussion forum.", "online"),

 Q("Match the quadrant of a SWAYAM course in List I with what it contains in List II."
   + match(["e-Tutorial", "e-Content", "Self-assessment", "Discussion forum"],
           ["Quizzes and assignments", "Video lectures", "Clearing of doubts among learners and teachers",
            "Material to read"]),
   ["(a)-(ii), (b)-(iv), (c)-(i), (d)-(iii)", "(a)-(iv), (b)-(ii), (c)-(i), (d)-(iii)",
    "(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)", "(a)-(i), (b)-(iv), (c)-(ii), (d)-(iii)"], "A",
   "The e-tutorial is the video lecture; the e-content is the material to read; self-assessment is the "
   "quizzes and assignments; the discussion forum is where doubts are raised and answered.", "online"),

 Q("Under the UGC's credit framework for online learning, the share of the courses of a semester that a "
   "university may allow a student to take through SWAYAM was raised in 2021:",
   ["from 10% to 20%", "from 20% to 30%", "from 20% to 40%", "from 40% to 50%"], "C",
   "The limit on credits earned through SWAYAM courses was raised from 20% to 40% of the courses in a "
   "semester by the 2021 regulations.", "online"),

 Q("Which statement about SWAYAM Prabha is correct?",
   ["It is a platform of interactive online courses that needs a broadband connection",
    "It is a group of direct-to-home educational television channels broadcasting round the clock",
    "It is a digital library of theses", "It is a credit bank for transferring credits between institutions"], "B",
   "SWAYAM Prabha is a group of DTH channels, begun in 2017, that carry educational programmes 24 hours a day "
   "by satellite, for learners without good internet. The theses repository is Shodhganga and the credit bank "
   "is the Academic Bank of Credits.", "online"),

 Q("Consider the following modes of online teaching:"
   + st("A live webinar", "A recorded lecture", "A discussion forum", "A live online class with chat")
   + "Which of them are synchronous?",
   ["I and II only", "II and III only", "I, II and IV only", "I and IV only"], "D",
   "Synchronous means that teacher and learners are present at the same time: the live webinar and the live "
   "class. A recorded lecture and a forum can be used at any time: they are asynchronous. Blended learning "
   "mixes face-to-face and online work.", "online"),

 Q("The term MOOC (Massive Open Online Course) was coined in 2008 for an open online course run by:",
   ["George Siemens and Stephen Downes", "Salman Khan", "Benjamin Bloom and David Krathwohl",
    "Sebastian Thrun and Peter Norvig"], "A",
   "The name was given to the open course taught by George Siemens and Stephen Downes in 2008. A MOOC is "
   "open to anyone, usually free to join, for very large numbers, and delivered online.", "online"),

 Q("Arrange the following from the most concrete to the most abstract in Edgar Dale's Cone of Experience: "
   "(1) Verbal symbols, (2) Demonstrations, (3) Direct purposeful experiences, (4) Television and films, "
   "(5) Visual symbols.",
   ["3, 4, 2, 5, 1", "2, 3, 4, 1, 5", "3, 2, 4, 5, 1", "3, 2, 5, 4, 1"], "C",
   "Direct purposeful experience is the base of the cone; then come contrived experiences, demonstrations, "
   "field trips, exhibits, television and film, recordings and pictures, visual symbols, and at the top verbal "
   "symbols, which depend on words alone.", "support"),

 Q("Which of the following lists contains only ICT-based teaching support?",
   ["Chalkboard, flannel board, charts", "Interactive board, learning management system, virtual laboratory",
    "Overhead projector, slide projector, models", "Radio lessons, maps, specimens"], "B",
   "Interactive (smart) boards, learning management systems such as Moodle, MOOCs, simulations and virtual "
   "labs are ICT-based. The chalkboard, charts, maps, models and specimens are traditional aids; overhead and "
   "slide projectors, recordings and broadcast lessons are the &lsquo;modern&rsquo; (pre-digital) group.", "support"),

 Q(ar("A field visit lies nearer the base of Dale's Cone of Experience than a lecture on the same topic.",
      "The cone arranges learning experiences from the concrete at its base to the abstract at its top."),
   AR, "A",
   "A field visit is close to direct experience; a lecture uses verbal symbols, the most abstract of all, at "
   "the top of the cone. Both statements are true and (R) explains (A).", "support"),

 Q("Which of the following lists contains only visual aids?",
   ["Radio, chart, model", "Film, slide, recording", "Television, chart, map", "Chart, slide, model"], "D",
   "Aids are grouped by the sense they address: audio (radio, recordings), visual (charts, slides, models, "
   "maps) and audio-visual (film, television, video). Each of the other lists contains an audio or an "
   "audio-visual aid.", "support"),

 Q("Match the type of evaluation in List I with its timing and purpose in List II."
   + match(["Placement", "Formative", "Diagnostic", "Summative"],
           ["At the end, to judge and certify achievement", "Before teaching, to decide where a learner should start",
            "During teaching, to give feedback that improves learning",
            "When difficulties persist, to find their causes"]),
   ["(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)", "(a)-(iii), (b)-(ii), (c)-(iv), (d)-(i)",
    "(a)-(ii), (b)-(iii), (c)-(iv), (d)-(i)", "(a)-(i), (b)-(iii), (c)-(iv), (d)-(ii)"], "C",
   "Placement comes before teaching, formative during it, diagnostic when a difficulty does not go away, and "
   "summative at the end. The terms formative and summative are Michael Scriven's (1967).", "evaluation"),

 Q("An examination rule says: &ldquo;The top 6% of the candidates who appear will qualify.&rdquo; This is an "
   "example of:",
   ["norm-referenced evaluation", "criterion-referenced evaluation", "formative evaluation", "diagnostic evaluation"], "A",
   "Norm-referenced evaluation compares a candidate with the others (rank, percentile). &ldquo;Everyone who "
   "scores 40% or more qualifies&rdquo; would be criterion-referenced: comparison with a fixed standard. "
   "Robert Glaser made the distinction in 1963.", "evaluation"),

 Q("A weekly ungraded quiz whose results decide what is taught again next week, and the end-of-semester "
   "examination, are examples respectively of:",
   ["summative and formative evaluation", "formative and summative evaluation",
    "diagnostic and placement evaluation", "placement and summative evaluation"], "B",
   "Evaluation used while teaching is going on, to improve it, is formative. Evaluation at the end, to judge "
   "and grade what was achieved, is summative.", "evaluation"),

 Q("A test gives almost the same scores when repeated on the same students, but its questions call only for "
   "recall although the course aimed at application. The test is:",
   ["valid but not reliable", "neither valid nor reliable", "both valid and reliable", "reliable but not valid"], "D",
   "Reliability is consistency of scores; validity is measuring what the test claims to measure. This test is "
   "consistent, hence reliable, but it does not measure application, the intended outcome, so it is not valid. "
   "A test can be reliable without being valid, but not valid without being reliable.", "evaluation"),

 Q("Which statement about measurement, assessment and evaluation is correct?",
   ["Measurement is the widest of the three terms",
    "Evaluation only assigns numbers to performance",
    "Evaluation is the widest: it adds a value judgement to the evidence collected",
    "Assessment and evaluation exclude qualitative evidence"], "C",
   "Measurement assigns numbers; assessment collects evidence, quantitative and qualitative; evaluation judges, "
   "against the objectives, how good the performance is. Evaluation is tied to the objectives and the learning "
   "experiences in a triangle.", "evaluation"),

 Q("Under the ten-point grading scale of the Choice Based Credit System, a student earns grades A+ (9), "
   "B+ (7) and O (10) in three courses of 4, 3 and 3 credits. The SGPA is:",
   ["8.67", "8.7", "8.5", "9.0"], "B",
   r"SGPA is the credit-weighted mean of the grade points: "
   r"$\dfrac{4(9)+3(7)+3(10)}{4+3+3}=\dfrac{36+21+30}{10}=8.7$. The simple average of 9, 7 and 10 is 8.67, which "
   r"ignores the credits.", "cbcs"),

 Q("A student has SGPA 7.5 in the first semester (20 credits) and SGPA 8.5 in the second semester "
   "(30 credits). The CGPA after two semesters is:",
   ["8.1", "8.0", "7.9", "8.25"], "A",
   r"CGPA is weighted by credits: $\dfrac{20(7.5)+30(8.5)}{20+30}=\dfrac{150+255}{50}=8.1$. It is not the simple "
   r"average 8.0, because the second semester carries more credits.", "cbcs"),

 Q("In the Choice Based Credit System, one credit stands for one hour of lecture or tutorial, or two hours of "
   "practical work, a week. A course with 3 lectures and 4 hours of practical work every week carries:",
   ["7 credits", "3 credits", "4 credits", "5 credits"], "D",
   r"Lectures: $3\times1=3$ credits. Practical: $4\div2=2$ credits. Total 5 credits.", "cbcs"),

 Q("Consider the statements about innovations in evaluation:"
   + st("In computer adaptive testing a harder question follows a right answer and an easier one a wrong answer.",
        "In an adaptive test two candidates may see different questions and still be scored on the same scale.",
        "Computer-based testing suits long essay-type answers better than objective questions.",
        "The Academic Bank of Credits stores the credits a student earns so that they can be carried between "
        "institutions.")
   + "Which of the statements are correct?",
   ["I and II only", "I, III and IV only", "I, II and IV only", "I, II, III and IV"], "C",
   "(I) and (II) describe adaptive testing: each next question is chosen from the answers so far, and since "
   "the difficulty of every question is known in advance, different sets give comparable scores. (IV) is the "
   "purpose of the Academic Bank of Credits. (III) is false: computer-based testing suits objective questions "
   "better than long answers.", "cbt"),
]
