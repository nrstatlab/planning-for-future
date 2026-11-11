# -*- coding: utf-8 -*-
"""UGC NET Paper I, Unit 2: fifty exam-standard model questions."""
from . import AR, Q, ar, match, st

TITLE = "Research Aptitude"
BLURB = ("The meaning and types of research, positivism and post-positivism, experimental, descriptive and "
         "historical methods, qualitative and quantitative approaches, the steps of research, thesis writing "
         "and referencing, ICT in research, and research ethics.")

QUESTIONS = [
 Q("A college teacher finds that her students interpret graphs badly, introduces a weekly exercise, measures "
   "the change at the end of the term and revises the exercise for the next term. This is:",
   ["fundamental research", "action research", "historical research", "ex post facto research"], "B",
   "Action research is done by a practitioner to improve their own practice, in cycles of plan, act, observe "
   "and reflect. It is credited to Kurt Lewin; Stephen Corey took it into education. It does not aim at theory "
   "or at generalising beyond the classroom.", "meaning"),

 Q("Match the type of research in List I with its description in List II."
   + match(["Fundamental", "Applied", "Exploratory", "Longitudinal"],
           ["Studies the same units over a period of time", "Seeks to find out what the problem is",
            "Aims to extend knowledge or build theory", "Aims to solve a practical problem"]),
   ["(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(ii), (d)-(i)",
    "(a)-(iii), (b)-(ii), (c)-(iv), (d)-(i)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "D",
   "Fundamental (pure, basic) research extends knowledge with no application in view; applied research solves "
   "a practical problem; exploratory research clarifies a problem not yet well understood; longitudinal "
   "research follows the same units over time, unlike a cross-sectional study at one point.", "meaning"),

 Q("Consider the statements about the characteristics of research:"
   + st("It is systematic: it follows a planned sequence of steps.",
        "It is empirical: it rests on evidence.",
        "It is replicable: another researcher following the same method should reach the same result.",
        "Its findings depend on the personal preferences of the researcher.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and II only", "II, III and IV only", "I, II, III and IV"], "A",
   "Research is systematic, empirical, logical, replicable, critical and cumulative, and it is "
   "<em>objective</em>: its findings should not depend on who did it. So (IV) is false.", "meaning"),

 Q("A study measures reading ability in a sample of Class V, Class VIII and Class X students in the same "
   "month and compares the three groups. By its time dimension the study is:",
   ["longitudinal", "experimental", "cross-sectional", "a panel study"], "C",
   "It observes different groups at one point in time: cross-sectional. A longitudinal (or panel) study would "
   "follow the same students from Class V to Class X. Nothing is manipulated, so it is not experimental.", "meaning"),

 Q(ar("Action research does not aim at generalisations that hold for all settings.",
      "Its purpose is to improve the practitioner's own practice in a particular setting."),
   AR, "A",
   "Action research is local and practical by design: the practitioner studies and improves what happens in "
   "her own classroom or institution. Both statements are true and (R) is the reason for (A).", "meaning"),

 Q("A study examines whether a new theory of consumer choice holds, with no application in view; another "
   "study tries to reduce the waiting time at the outpatient desk of one hospital. These are, respectively:",
   ["applied and fundamental research", "fundamental and applied research",
    "action and fundamental research", "descriptive and historical research"], "B",
   "Testing or building theory for its own sake is fundamental research; solving a particular practical "
   "problem is applied research.", "meaning"),

 Q("Match the name in List I with the idea in List II."
   + match(["Auguste Comte", "Karl Popper", "Max Weber", "Glaser and Strauss"],
           ["Verstehen (interpretive understanding)", "Grounded theory", "Positivism", "Falsification"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "C",
   "Comte is the founder of positivism. Popper held that a scientific statement must be falsifiable. Weber's "
   "Verstehen is the understanding of the meanings people give to their actions, the root of interpretivism. "
   "Glaser and Strauss (1967) proposed grounded theory.", "positivism"),

 Q("According to Karl Popper, the statement &ldquo;All swans are white&rdquo; is scientific because:",
   ["a large number of white swans have been observed", "it has been proved by induction",
    "it is accepted by most scientists", "it can be shown false by a single observation of a black swan"], "D",
   "Popper's criterion is falsifiability: a scientific statement must forbid something, so that an observation "
   "could refute it. No number of white swans proves the statement; one black swan refutes it. A theory is "
   "never proved, only not yet refuted.", "positivism"),

 Q("Consider the statements:"
   + st("Positivism holds that reality exists independently and can be known directly by observation and "
        "measurement.",
        "Post-positivism holds that knowledge is provisional and that a theory can never be finally proved.",
        "Interpretivism holds that social reality is constructed by people and seeks their meanings.",
        "Post-positivism rejects the use of quantitative methods altogether.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and II only", "I, III and IV only", "I, II, III and IV"], "A",
   "Post-positivism keeps the scientific method and quantitative measurement but admits error: it uses several "
   "measures and methods (triangulation) and treats findings as the best current estimate. It does not reject "
   "quantitative methods, so (IV) is false.", "positivism"),

 Q("A researcher starts from a theory, derives a hypothesis from it and then collects data to test the "
   "hypothesis. The reasoning followed is:",
   ["inductive", "abductive", "deductive", "analogical"], "C",
   "Deduction goes from the general (theory) to the particular (a hypothesis tested on data); it is the logic "
   "of the positivist, quantitative tradition. Induction goes the other way, from observations to a general "
   "statement, as in much qualitative research.", "positivism"),

 Q("A researcher lives for a year in a village and interviews women at length about what &ldquo;a good "
   "school&rdquo; means to them. The approach is:",
   ["positivist", "interpretivist", "experimental", "post-positivist"], "B",
   "The study seeks the participants' own meanings, not a measured effect or a law: interpretivism "
   "(constructivism), usually pursued by qualitative methods.", "positivism"),

 Q("Sixty students are divided at random into two groups. One group is taught with simulations and the other "
   "without, and both take the same test. The design is:",
   ["pre-experimental", "quasi-experimental", "ex post facto", "true experimental"], "D",
   "Random assignment together with a control group makes a true experimental design (Campbell and Stanley). "
   "If two existing sections had been used without random assignment it would be quasi-experimental; with one "
   "group and no control, pre-experimental.", "methods"),

 Q("In an experiment one group of students is taught with simulations and another without, and both groups "
   "take the same test. The independent and the dependent variables are, respectively:",
   ["the test score and the method of teaching", "the method of teaching and the test score",
    "the students and the teacher", "random assignment and the control group"], "B",
   "The independent variable is the one the researcher manipulates, the presumed cause: the method of "
   "teaching. The dependent variable is the effect that is observed: the test score.", "methods"),

 Q(ar("Only the experimental method can establish a cause-and-effect relation directly.",
      "In an experiment the researcher manipulates the independent variable while controlling other variables."),
   AR, "A",
   "Because the researcher changes one thing and holds the rest alike (by control and random assignment), a "
   "difference in the outcome can be put down to the treatment. Descriptive and correlational studies show "
   "association only. Both statements are true and (R) is the reason.", "methods"),

 Q("In a study of a new teaching method, the students simply grow older and more mature during the year, and "
   "this by itself improves their scores. This threat to internal validity is called:",
   ["history", "instrumentation", "maturation", "attrition"], "C",
   "Maturation is change in the subjects themselves with the passage of time. History is an outside event "
   "during the study; instrumentation a change in the measuring instrument; attrition the loss of subjects.", "methods"),

 Q("Consider the statements:"
   + st("Internal validity concerns whether the observed effect is really due to the treatment.",
        "External validity concerns whether the result holds beyond the subjects and setting of the study.",
        "Random assignment mainly strengthens internal validity.",
        "A descriptive survey can by itself establish causation.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and IV only", "II, III and IV only", "I, II and III only"], "D",
   "Random assignment makes the groups alike in everything but the treatment, which protects internal "
   "validity; random <em>selection</em> from the population is what helps external validity. A survey shows "
   "things as they are and can show association, not cause: (IV) is false.", "methods"),

 Q("A historian finds a letter said to have been written in 1857 and examines its paper, ink and handwriting "
   "to decide whether it is genuine. She is carrying out:",
   ["external criticism", "internal criticism", "content analysis", "triangulation"], "A",
   "External criticism asks whether the document is authentic: is it what it claims to be, from the time it "
   "claims? Internal criticism comes next and asks whether what it says is credible and accurate.", "methods"),

 Q("Which of the following is a primary source for a historical study of a university?",
   ["A textbook of the history of education", "A newspaper article written last year about its early days",
    "The minutes of the meetings of its governing body", "An encyclopaedia entry on the university"], "C",
   "Primary sources are first-hand records made at the time: original documents, minutes, letters, "
   "eyewitness accounts. Textbooks, later articles and encyclopaedias report or interpret such records and are "
   "secondary sources.", "methods"),

 Q("Which of the following is NOT a descriptive method of research?",
   ["Survey", "Case study", "Correlational study", "Randomised controlled trial"], "D",
   "Descriptive research describes things as they are without manipulating anything: surveys, case studies, "
   "correlational, developmental and observational studies. A randomised controlled trial manipulates a "
   "treatment and is experimental.", "methods"),

 Q("Match the qualitative approach in List I with its focus in List II."
   + match(["Ethnography", "Phenomenology", "Grounded theory", "Case study"],
           ["Building a theory from the data", "An intensive study of a single unit",
            "A culture or group studied from the inside", "The lived experience of a phenomenon"]),
   ["(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)",
    "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)", "(a)-(i), (b)-(iv), (c)-(iii), (d)-(ii)"], "B",
   "Ethnography studies a culture from within, often by long participant observation; phenomenology asks what "
   "an experience is like for those who live it; grounded theory builds theory from data; a case study "
   "examines one person, group or institution in depth.", "qualquant"),

 Q("Consider the statements about quantitative and qualitative research:"
   + st("Quantitative research is mainly deductive; qualitative research is mainly inductive.",
        "Quantitative research usually uses large probability samples; qualitative research small purposive ones.",
        "Thematic analysis is a technique of quantitative research.",
        "Mixed-methods research uses both kinds of data.")
   + "Which of the statements are correct?",
   ["I, II and IV only", "I and II only", "I, III and IV only", "I, II, III and IV"], "A",
   "Thematic, content and narrative analysis are ways of analysing words and meanings: qualitative. "
   "Quantitative analysis is statistical. The other three statements are correct.", "qualquant"),

 Q("A study of people recovering from drug addiction recruits each participant through an earlier "
   "participant, because no list of such people exists. The sampling method is:",
   ["quota sampling", "systematic sampling", "snowball sampling", "stratified sampling"], "C",
   "In snowball sampling each participant names or brings others. It is a non-probability method suited to "
   "hidden or hard-to-reach populations for which there is no sampling frame.", "qualquant"),

 Q("Which of the following lists contains only probability sampling methods?",
   ["Simple random, quota, cluster", "Stratified, purposive, systematic", "Convenience, snowball, quota",
    "Simple random, stratified, systematic, cluster"], "D",
   "In probability sampling every unit has a known, non-zero chance of selection: simple random, stratified, "
   "systematic and cluster sampling. Convenience, purposive, quota and snowball sampling are non-probability "
   "methods.", "qualquant"),

 Q("An interviewer is told to interview 30 men and 30 women, choosing whoever is convenient until the numbers "
   "are complete. This is:",
   ["stratified random sampling", "quota sampling", "cluster sampling", "systematic sampling"], "B",
   "Quota sampling fixes the number wanted in each category but leaves the choice of individuals to the "
   "interviewer, so it is not a probability method. In stratified random sampling the units within each "
   "stratum are chosen at random.", "qualquant"),

 Q("To understand why students have stopped using the college library, the most suitable tool is:",
   ["in-depth interviews with a small number of students", "a count of the books issued each month",
    "a standardised achievement test", "a census of all the books in the library"], "A",
   "A &lsquo;why&rsquo; question about reasons and meanings calls for qualitative tools: in-depth interviews "
   "or focus groups. The count of books issued would show <em>that</em> use has fallen, not why.", "qualquant"),

 Q(ar("Findings of qualitative research are usually not generalised statistically to a population.",
      "Qualitative studies generally use small samples chosen purposively and not at random."),
   AR, "A",
   "Statistical generalisation needs a probability sample of adequate size. Qualitative work chooses a few "
   "information-rich cases on purpose and aims at depth of understanding, so its findings are transferred to "
   "similar settings by judgement, not by statistical inference. Both statements are true and (R) explains (A).", "qualquant"),

 Q("Arrange the following steps of research in the correct order: (1) Collection of data, (2) Formulation of "
   "hypotheses, (3) Identification of the problem, (4) Review of literature, (5) Preparation of the research "
   "design, (6) Analysis of data.",
   ["3, 2, 4, 5, 1, 6", "4, 3, 2, 5, 1, 6", "3, 4, 2, 5, 1, 6", "3, 4, 5, 2, 6, 1"], "C",
   "Problem, review of literature, objectives and hypotheses, research design, sampling and collection of "
   "data, analysis, then testing of hypotheses, interpretation and the report. The review comes before the "
   "hypotheses because it shows what is known and where the gap is.", "steps"),

 Q("&ldquo;Students taught through simulations will score higher in statistics than students taught without "
   "them.&rdquo; This hypothesis is:",
   ["a null hypothesis", "a non-directional hypothesis", "a research question", "a directional hypothesis"], "D",
   "It states that there is a difference and in which direction. The null hypothesis would say there is no "
   "difference; a non-directional hypothesis would say only that the two groups differ.", "steps"),

 Q("In a study of the effect of hours of study on marks, the previous ability of the students also affects "
   "the marks and has to be held constant. Previous ability is:",
   ["the independent variable", "an extraneous variable", "the dependent variable", "a criterion variable"], "B",
   "An extraneous variable affects the dependent variable but is not what the study is about; it must be "
   "controlled, for instance by matching or by random assignment, or it will be confused with the effect of "
   "the independent variable.", "steps"),

 Q("Consider the statements about a good hypothesis:"
   + st("It is testable.", "It is specific.", "It is stated before the data are seen.",
        "It must always be proved true by the study.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and II only", "II, III and IV only", "I, II, III and IV"], "A",
   "A hypothesis is a testable, specific statement, consistent with known facts and set down in advance. It "
   "may be supported or rejected by the data; a rejected hypothesis is still a result. So (IV) is false.", "steps"),

 Q("Training improves the knowledge of workers, and the improved knowledge in turn raises their output. In "
   "this chain, knowledge is:",
   ["an extraneous variable", "the independent variable", "an intervening (mediating) variable",
    "the dependent variable"], "C",
   "An intervening or mediating variable carries the effect from the independent variable (training) to the "
   "dependent variable (output).", "steps"),

 Q("The main purpose of the review of literature in research is to:",
   ["increase the length of the thesis", "collect the primary data", "test the hypothesis",
    "find out what is already known and where the gap lies"], "D",
   "The review shows what has been done, with which methods and results, and what remains unanswered. It lets "
   "the researcher define the problem precisely, avoid repeating work, and choose a design.", "steps"),

 Q("Which of the following is decided at the stage of the research design?",
   ["The conclusions of the study", "The method, the variables, the sample and the tools",
    "The title of the published paper", "The style of referencing only"], "B",
   "The research design is the plan of the study: which method, which variables and how they are measured, "
   "what sample and what tools. It is made after the problem and hypotheses are fixed and before data are "
   "collected.", "steps"),

 Q("The usual structure of a research article, abbreviated IMRaD, stands for:",
   ["Introduction, Methods, Results and Discussion", "Index, Methods, References and Data",
    "Introduction, Materials, Review and Discussion", "Idea, Method, Review and Decision"], "A",
   "A research article has a title, abstract and keywords, then Introduction, Methods, Results and Discussion, "
   "followed by the references.", "writing"),

 Q("Match the style of referencing in List I with the form of its in-text citation in List II."
   + match(["APA", "MLA", "Vancouver", "IEEE"],
           ["Numbers in square brackets, as [1]", "Author and year, as (Rao, 2019)",
            "Author and page, as (Rao 45)", "Numbers in the order of first citation, used in medicine"]),
   ["(a)-(ii), (b)-(iii), (c)-(i), (d)-(iv)", "(a)-(iii), (b)-(ii), (c)-(iv), (d)-(i)",
    "(a)-(ii), (b)-(iii), (c)-(iv), (d)-(i)", "(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)"], "C",
   "APA (psychology, education, social sciences) is author&ndash;date; MLA (languages and literature) is "
   "author&ndash;page; Vancouver (medicine) numbers sources in the order cited; IEEE (engineering) uses "
   "numbers in square brackets.", "writing"),

 Q("A researcher has six papers, cited 25, 18, 9, 6, 4 and 2 times. Her h-index and i10-index are, "
   "respectively:",
   ["6 and 2", "4 and 3", "5 and 2", "4 and 2"], "D",
   "The h-index is the largest $h$ such that $h$ papers have at least $h$ citations each. Four papers have at "
   "least 4 citations (25, 18, 9, 6), but there are not five with at least 5, so $h=4$. The i10-index counts "
   "papers with at least 10 citations: two (25 and 18).", "writing"),

 Q("Match the abbreviation in List I with its meaning in List II."
   + match(["ibid.", "et al.", "sic", "cf."],
           ["And others", "Compare", "In the same source as the one just cited", "Thus, as in the original"]),
   ["(a)-(i), (b)-(iii), (c)-(iv), (d)-(ii)", "(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)",
    "(a)-(iii), (b)-(i), (c)-(ii), (d)-(iv)", "(a)-(iv), (b)-(i), (c)-(iii), (d)-(ii)"], "B",
   "<em>ibid.</em> refers to the source cited immediately before; <em>et al.</em> means &lsquo;and "
   "others&rsquo;; <em>sic</em> marks that a quotation is reproduced exactly, mistakes included; <em>cf.</em> "
   "means &lsquo;compare&rsquo;.", "writing"),

 Q("Which of the following belongs to the reference material placed after the text of a thesis?",
   ["Appendices", "Abstract", "Acknowledgements", "Certificate"], "A",
   "A thesis has preliminary pages (title, declaration, certificate, acknowledgements, contents, abstract), the "
   "text (introduction to conclusions) and reference material (references or bibliography, and appendices such "
   "as questionnaires and raw tables).", "writing"),

 Q("Consider the statements:"
   + st("A list of references contains only the works cited in the text.",
        "A bibliography may also include works consulted but not cited.",
        "The impact factor of journals is associated with Eugene Garfield.",
        "The h-index was proposed by Jorge Hirsch.")
   + "Which of the statements are correct?",
   ["I and II only", "III and IV only", "I, II and III only", "I, II, III and IV"], "D",
   "All four are correct. References list what is cited; a bibliography can be wider. Garfield devised the "
   "journal impact factor, and Hirsch proposed the h-index in 2005.", "writing"),

 Q("An abstract of a research paper should contain:",
   ["a detailed review of all earlier studies", "the list of references",
    "the problem, the method, the main result and the conclusion, in brief", "the questionnaire used"], "C",
   "The abstract is a short paragraph that lets a reader decide whether to read the paper: what was asked, how "
   "it was studied, what was found and what it means.", "writing"),

 Q("A student wishes to see the doctoral theses already submitted to Indian universities on rural credit "
   "before choosing a topic. The service to consult is:",
   ["Shodh Shuddhi", "Shodhganga", "Vidwan", "ORCID"], "B",
   "Shodhganga, run by INFLIBNET, is the repository of Indian theses. Shodhgangotri holds synopses of research "
   "in progress, Shodh Shuddhi is the plagiarism-detection service given to universities, Vidwan is a database "
   "of experts, and ORCID is an identifier for researchers.", "ict"),

 Q("A database search uses the expression: sampling AND agriculture NOT forestry. Compared with a search "
   "for sampling alone, this search will return:",
   ["fewer records, each containing both of the first two terms and not the third", "more records",
    "exactly the same records", "records containing any one of the three terms"], "A",
   "AND requires both terms and NOT excludes a term, so both narrow the search. OR is the operator that "
   "widens it, returning records with either term.", "ict"),

 Q("Match the tool in List I with its use in research in List II."
   + match(["Zotero", "NVivo", "SPSS", "DOI"],
           ["Statistical analysis of quantitative data", "A persistent identifier of a published paper",
            "Managing references and citations", "Analysis of qualitative data"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)"], "D",
   "Zotero (like Mendeley and EndNote) manages references; NVivo (like ATLAS.ti) analyses qualitative data; "
   "SPSS (like R, SAS and Stata) is statistical software; the Digital Object Identifier permanently "
   "identifies a paper, as ORCID identifies a researcher.", "ict"),

 Q("Which of the following is a consortium that gives universities access to e-journals and databases?",
   ["Shodhgangotri", "Vidwan", "e-ShodhSindhu", "Shodh Shuddhi"], "C",
   "e-ShodhSindhu is the INFLIBNET consortium for e-resources. Shodhgangotri holds synopses, Vidwan profiles "
   "of experts, and Shodh Shuddhi provides plagiarism-detection software.", "ict"),

 Q("A researcher leaves out three survey responses because they weaken her result, and does not mention it in "
   "the report. This is:",
   ["plagiarism", "falsification", "fabrication", "duplicate publication"], "B",
   "Falsification is changing or omitting data or results so that the research is not accurately represented; "
   "nothing need be invented. Fabrication is making up data; plagiarism is using another's words or ideas "
   "without credit.", "ethics"),

 Q("A thesis shows 35% similarity after the exclusions permitted by the UGC regulations of 2018 on academic "
   "integrity. The level of plagiarism and the consequence for the student are:",
   ["Level 1; a revised script to be submitted within the stipulated period",
    "Level 0; no penalty", "Level 2; debarred from submitting a revised script for one year",
    "Level 3; registration cancelled"], "A",
   "Level 0 is similarity up to 10% (no penalty); Level 1 above 10% to 40% (revised script within the set time, "
   "up to six months); Level 2 above 40% to 60% (debarred from resubmitting for a year); Level 3 above 60% "
   "(registration cancelled).", "ethics"),

 Q("The three basic ethical principles of the Belmont Report (1979) are:",
   ["honesty, objectivity and openness", "consent, confidentiality and anonymity",
    "fabrication, falsification and plagiarism", "respect for persons, beneficence and justice"], "D",
   "The Belmont Report rests on respect for persons (from which informed consent follows), beneficence (do no "
   "harm, maximise benefit) and justice (fair sharing of burdens and benefits). Fabrication, falsification and "
   "plagiarism are the three kinds of misconduct.", "ethics"),

 Q("Arrange the following in chronological order: (1) the Belmont Report, (2) the Nuremberg Code, (3) the "
   "Declaration of Helsinki.",
   ["1, 2, 3", "2, 1, 3", "2, 3, 1", "3, 2, 1"], "C",
   "The Nuremberg Code came in 1947, the World Medical Association's Declaration of Helsinki in 1964 and the "
   "Belmont Report in 1979.", "ethics"),

 Q("Consider the statements about informed consent in research:"
   + st("Participants must be told the purpose, the procedure and the risks.",
        "Participants may withdraw from the study at any time.",
        "Consent must be given freely, without pressure.",
        "Once consent is given, participants may be identified by name in the report.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "II, III and IV only", "I, II, III and IV"], "B",
   "Consent covers taking part; it does not remove the duty of confidentiality and anonymity. Participants "
   "should not be identifiable in the report unless they have separately and expressly agreed. So (IV) is "
   "false.", "ethics"),

 Q(ar("A researcher should avoid publishing in predatory journals.",
      "Predatory journals charge fees for publication without genuine peer review."),
   AR, "A",
   "Work published without real review has not been checked and carries no credit; such journals exist to "
   "collect fees. Both statements are true and (R) is the reason for (A).", "ethics"),
]
