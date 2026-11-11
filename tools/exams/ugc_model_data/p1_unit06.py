# -*- coding: utf-8 -*-
"""UGC NET Paper I, Unit 6: fifty exam-standard model questions."""
from . import AR, Q, ar, match, st

TITLE = "Logical Reasoning"
BLURB = ("Arguments and argument forms, categorical propositions and syllogisms, fallacies, uses of language, "
         "the square of opposition, deduction and induction, analogies, Venn diagrams, and Indian logic: the "
         "pramanas, anumana and the hetvabhasas.")


def sc(statements, conclusions):
    return ("<b>Statements:</b> " + " ".join(statements)
            + '<span class="stmts"><span><b>Conclusions:</b></span>'
            + "".join("<span>(%s) %s</span>" % (r, c) for r, c in zip(["I", "II"], conclusions)) + "</span>"
            + "Which of the conclusions follow?")


FOLLOW = ["Only I follows", "Only II follows", "Neither I nor II follows", "Both I and II follow"]

QUESTIONS = [
 Q("&ldquo;If it rains, the match is cancelled. The match was not cancelled. Therefore it did not rain.&rdquo; "
   "The form of this argument and its status are:",
   ["modus ponens; valid", "modus tollens; valid", "denying the antecedent; invalid",
    "affirming the consequent; invalid"], "B",
   "The pattern is: if P then Q; not Q; therefore not P. This is modus tollens (denying the consequent), a "
   "valid form.", "arguments"),

 Q("&ldquo;If a person is a doctor, the person has a degree. Meera has a degree. Therefore Meera is a "
   "doctor.&rdquo; The argument commits the fallacy of:",
   ["denying the antecedent", "undistributed middle in a hypothetical form", "begging the question",
    "affirming the consequent"], "D",
   "The pattern is: if P then Q; Q; therefore P. Many people with degrees are not doctors: the consequent can "
   "be true for other reasons. Affirming the consequent is a formal fallacy.", "arguments"),

 Q("Consider the statements:"
   + st("A valid argument may have a false conclusion.", "A sound argument always has a true conclusion.",
        "A valid argument with true premises may have a false conclusion.",
        "An argument is properly described as true or false.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "II and IV only", "I, II and IV only"], "A",
   "Validity is a matter of form: a valid argument with a false premise can have a false conclusion (I). A "
   "sound argument is valid with true premises, so its conclusion must be true (II). (III) contradicts the "
   "definition of validity. (IV) is a category mistake: statements are true or false; arguments are valid or "
   "invalid.", "arguments"),

 Q("Match the argument form in List I with its pattern in List II."
   + match(["Modus ponens", "Modus tollens", "Hypothetical syllogism", "Disjunctive syllogism"],
           ["P or Q; not P; therefore Q", "If P then Q; if Q then R; therefore if P then R",
            "If P then Q; P; therefore Q", "If P then Q; not Q; therefore not P"]),
   ["(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(ii), (d)-(i)",
    "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)", "(a)-(iii), (b)-(ii), (c)-(iv), (d)-(i)"], "C",
   "All four are valid forms. Modus ponens affirms the antecedent; modus tollens denies the consequent; the "
   "hypothetical syllogism chains two conditionals; the disjunctive syllogism eliminates one alternative.", "arguments"),

 Q("&ldquo;Either the server is down or the cable is cut. The server is not down. Therefore the cable is "
   "cut.&rdquo; This argument is:",
   ["a hypothetical syllogism", "a disjunctive syllogism", "an instance of modus ponens", "a false dilemma, hence invalid"], "B",
   "P or Q; not P; therefore Q: a disjunctive syllogism, which is valid. Whether the first premise is true "
   "(whether there are really only two possibilities) is a question of soundness, not of validity.", "arguments"),

 Q("In the proposition &ldquo;Some S is not P&rdquo;, which term or terms are distributed?",
   ["The subject only", "Both terms", "Neither term", "The predicate only"], "D",
   "An O proposition says of some members of S that they are excluded from the whole of P, so the predicate "
   "is distributed and the subject is not. A distributes the subject only, E both terms, I neither.", "categorical"),

 Q("Match the proposition in List I with its quality and quantity in List II."
   + match(["A", "E", "I", "O"],
           ["Universal affirmative", "Universal negative", "Particular affirmative", "Particular negative"]),
   ["(a)-(i), (b)-(ii), (c)-(iii), (d)-(iv)", "(a)-(ii), (b)-(i), (c)-(iii), (d)-(iv)",
    "(a)-(i), (b)-(ii), (c)-(iv), (d)-(iii)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)"], "A",
   "A: All S is P. E: No S is P. I: Some S is P. O: Some S is not P. The letters come from the Latin "
   "<em>AffIrmo</em> (I affirm) and <em>nEgO</em> (I deny).", "categorical"),

 Q("&ldquo;All mammals are animals. All dogs are mammals. Therefore all dogs are animals.&rdquo; The mood and "
   "figure of this syllogism are:",
   ["AAA, figure 2", "AAI, figure 1", "AAA, figure 1", "AEA, figure 3"], "C",
   "All three propositions are of type A. The middle term, mammals, is the subject of the major premise and "
   "the predicate of the minor premise (M&ndash;P, S&ndash;M): figure 1. The form is the valid one "
   "traditionally called Barbara.", "categorical"),

 Q("&ldquo;All cats are animals. All dogs are animals. Therefore all dogs are cats.&rdquo; The fallacy "
   "committed is:",
   ["illicit major", "undistributed middle", "illicit minor", "exclusive premises"], "B",
   "The middle term, animals, is the predicate of an A proposition in both premises, and the predicate of an "
   "A proposition is not distributed. A middle term never distributed cannot connect the other two terms.", "categorical"),

 Q("&ldquo;No fish are mammals. No mammals are birds. Therefore no fish are birds.&rdquo; This syllogism is "
   "invalid because it:",
   ["has an undistributed middle term", "has four terms", "commits illicit minor",
    "draws a conclusion from two negative premises"], "D",
   "No conclusion follows from two negative premises (the fallacy of exclusive premises): each premise only "
   "separates a term from the middle term, which tells us nothing about how the two are related to each "
   "other. That the conclusion happens to be true does not make the argument valid.", "categorical"),

 Q("&ldquo;All dogs are animals. No cats are dogs. Therefore no cats are animals.&rdquo; The fallacy "
   "committed is:",
   ["illicit major", "illicit minor", "undistributed middle", "exclusive premises"], "A",
   "The major term, animals, is distributed in the conclusion (an E proposition distributes both terms) but "
   "not in the major premise, where it is the predicate of an A proposition. A term distributed in the "
   "conclusion must be distributed in its premise.", "categorical"),

 Q("In a syllogism the middle term is the predicate of both premises. The syllogism is in the:",
   ["first figure", "third figure", "second figure", "fourth figure"], "C",
   "Figure 1: M&ndash;P, S&ndash;M. Figure 2: P&ndash;M, S&ndash;M (middle term the predicate in both). "
   "Figure 3: M&ndash;P, M&ndash;S (the subject in both). Figure 4: P&ndash;M, M&ndash;S.", "categorical"),

 Q("Match the fallacy in List I with what it appeals to or does in List II."
   + match(["Ad hominem", "Ad populum", "Ad baculum", "Ad misericordiam"],
           ["Appeals to pity", "Attacks the person instead of the argument", "Appeals to force or threat",
            "Appeals to popular belief"]),
   ["(a)-(ii), (b)-(iii), (c)-(iv), (d)-(i)", "(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)",
    "(a)-(iv), (b)-(ii), (c)-(iii), (d)-(i)", "(a)-(ii), (b)-(iv), (c)-(i), (d)-(iii)"], "B",
   "Ad hominem: against the person. Ad populum: many believe it, so it is true. Ad baculum: accept this or "
   "suffer. Ad misericordiam: accept this out of pity.", "fallacies"),

 Q("&ldquo;Our team won the day I wore my blue shirt, so the blue shirt brought us the victory.&rdquo; The "
   "fallacy is:",
   ["hasty generalisation", "equivocation", "red herring", "post hoc ergo propter hoc"], "D",
   "&lsquo;After this, therefore because of this&rsquo;: one event followed another, which does not show "
   "that the first caused the second.", "fallacies"),

 Q("&ldquo;Nobody has ever proved that ghosts do not exist; therefore ghosts exist.&rdquo; The fallacy is:",
   ["argumentum ad ignorantiam", "argumentum ad verecundiam", "petitio principii", "straw man"], "A",
   "The appeal to ignorance treats the absence of disproof as proof (or the absence of proof as disproof). "
   "Lack of evidence against a claim is not evidence for it.", "fallacies"),

 Q("&ldquo;Either you support the new syllabus or you are against progress.&rdquo; The fallacy is:",
   ["slippery slope", "composition", "false dilemma", "ad populum"], "C",
   "Only two options are offered when there are others: one may favour progress and still object to this "
   "particular syllabus.", "fallacies"),

 Q("&ldquo;Every player in this team is excellent; therefore the team is excellent.&rdquo; The fallacy is:",
   ["division", "composition", "equivocation", "begging the question"], "B",
   "Composition argues from what is true of each part to what is true of the whole. A team of fine players "
   "may still play badly together. Division is the reverse: from the whole to each part.", "fallacies"),

 Q("Which of the following lists contains only formal fallacies?",
   ["Straw man, red herring, ad hominem", "Undistributed middle, hasty generalisation, equivocation",
    "Affirming the consequent, slippery slope, illicit major",
    "Undistributed middle, affirming the consequent, denying the antecedent"], "D",
   "Formal fallacies are errors in the form of the argument: undistributed middle, illicit major and minor, "
   "four terms, affirming the consequent, denying the antecedent. Straw man, red herring, ad hominem, hasty "
   "generalisation, slippery slope and equivocation are informal fallacies, errors of content or language.", "fallacies"),

 Q("Match the sentence in List I with the use of language in List II."
   + match(["Water boils at 100&deg;C at sea level.", "Alas, all is lost!", "Close the door.",
            "I promise to return the book tomorrow."],
           ["Informative", "Expressive", "Directive", "Performative"]),
   ["(a)-(i), (b)-(ii), (c)-(iii), (d)-(iv)", "(a)-(ii), (b)-(i), (c)-(iii), (d)-(iv)",
    "(a)-(i), (b)-(iii), (c)-(ii), (d)-(iv)", "(a)-(i), (b)-(ii), (c)-(iv), (d)-(iii)"], "A",
   "Informative language states facts; expressive language voices or arouses feeling; directive language "
   "seeks to cause or prevent action; a performative utterance does the act it names: saying &lsquo;I "
   "promise&rsquo; is promising.", "language"),

 Q("Arrange the following terms in order of increasing connotation: (1) Dog, (2) Animal, (3) Mammal, "
   "(4) Living thing.",
   ["1, 3, 2, 4", "4, 3, 2, 1", "4, 2, 3, 1", "2, 4, 3, 1"], "C",
   "Each step adds attributes: a living thing, an animal, a mammal, a dog. As connotation (intension) "
   "increases, denotation (extension) decreases: there are fewer dogs than mammals.", "language"),

 Q(ar("The term &lsquo;mammal&rsquo; has a wider denotation than the term &lsquo;dog&rsquo;.",
      "The term &lsquo;dog&rsquo; has a richer connotation than the term &lsquo;mammal&rsquo;."),
   AR, "A",
   "Denotation is the class of things a term applies to; connotation the attributes a thing must have for "
   "the term to apply. By the law of inverse variation, the more attributes a term requires, the fewer "
   "things it applies to. Both statements are true and (R) explains (A).", "language"),

 Q("If the proposition &ldquo;All students are present&rdquo; is true, then, on the traditional square of "
   "opposition, the propositions &ldquo;No students are present&rdquo;, &ldquo;Some students are present&rdquo; "
   "and &ldquo;Some students are not present&rdquo; are, respectively:",
   ["false, true, undetermined", "false, true, false", "undetermined, true, false", "false, false, true"], "B",
   "A is true. Its contrary E is false (contraries cannot both be true). Its subaltern I is true. Its "
   "contradictory O is false.", "square"),

 Q("If the proposition &ldquo;Some politicians are honest&rdquo; is false, then the propositions &ldquo;All "
   "politicians are honest&rdquo;, &ldquo;No politicians are honest&rdquo; and &ldquo;Some politicians are not "
   "honest&rdquo; are, respectively:",
   ["false, undetermined, true", "true, false, true", "false, true, undetermined", "false, true, true"], "D",
   "I is false. Its contradictory E is true. A is false (if the particular is false, the universal is "
   "false). O is true, since subcontraries cannot both be false.", "square"),

 Q("Match the pair of propositions in List I with their relation in List II."
   + match(["A and O", "A and E", "I and O", "A and I"],
           ["Subcontraries", "Subalternation", "Contradictories", "Contraries"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "C",
   "Contradictories (A&ndash;O, E&ndash;I): exactly one is true. Contraries (A&ndash;E): not both true. "
   "Subcontraries (I&ndash;O): not both false. Subalternation (A to I, E to O): truth passes down, falsity "
   "passes up.", "square"),

 Q("If the proposition &ldquo;Some students are not present&rdquo; is true, then:",
   ["&ldquo;All students are present&rdquo; is false, and the truth of the other two propositions is undetermined",
    "&ldquo;No students are present&rdquo; is true", "&ldquo;Some students are present&rdquo; is false",
    "&ldquo;All students are present&rdquo; is undetermined"], "A",
   "O is true, so its contradictory A is false. E may be true or false (the truth of a particular does not "
   "fix the universal), and I may be true or false (subcontraries can both be true).", "square"),

 Q("The propositions &ldquo;All swans are white&rdquo; and &ldquo;No swans are white&rdquo; are:",
   ["contradictories: exactly one of them is true", "contraries: they cannot both be true but may both be false",
    "subcontraries: they cannot both be false", "subalterns"], "B",
   "A and E are contraries. If some swans are white and some are not, both are false. The contradictory of "
   "&ldquo;All swans are white&rdquo; is &ldquo;Some swans are not white&rdquo;.", "square"),

 Q("A researcher finds that as the dose of a fertiliser is increased step by step, the yield of the crop "
   "increases step by step. The causal inference drawn uses Mill's method of:",
   ["agreement", "difference", "residues", "concomitant variation"], "D",
   "When one phenomenon varies whenever another varies in a particular manner, the two are causally "
   "connected: the method of concomitant variation.", "deduction"),

 Q("Consider the statements:"
   + st("Adding a new premise cannot make a valid deductive argument invalid.",
        "Inductive arguments are judged as strong or weak.",
        "The conclusion of a valid deductive argument goes beyond what its premises contain.",
        "A sound argument is a valid argument with true premises.")
   + "Which of the statements are correct?",
   ["I and II only", "II, III and IV only", "I, II and IV only", "I, II, III and IV"], "C",
   "(III) is false: a deductive conclusion makes explicit what is already contained in the premises; it is "
   "the inductive conclusion that goes beyond them. That is why new information can weaken an inductive "
   "argument but cannot undo a valid deduction.", "deduction"),

 Q("Several guests fall ill after a dinner. They had eaten different dishes, and the only dish common to all "
   "who fell ill was the salad. Concluding that the salad was the cause uses Mill's method of:",
   ["agreement", "difference", "concomitant variation", "residues"], "A",
   "The method of agreement: if the instances of a phenomenon have only one circumstance in common, that "
   "circumstance is its cause (or effect). The method of difference would compare two cases alike in "
   "everything except one factor.", "deduction"),

 Q("Seismograph : Earthquake :: Anemometer : ?",
   ["Rainfall", "Wind speed", "Humidity", "Atmospheric pressure"], "B",
   "The relation is instrument and what it measures. An anemometer measures wind speed; a rain gauge "
   "measures rainfall, a hygrometer humidity and a barometer atmospheric pressure.", "analogies"),

 Q("Carpenter : Chisel :: Surgeon : ?",
   ["Hospital", "Patient", "Medicine", "Scalpel"], "D",
   "The relation is worker and tool. A carpenter works with a chisel; a surgeon works with a scalpel. The "
   "hospital is the place of work and the patient the person worked on.", "analogies"),

 Q("Flour : Bread :: Clay : ?",
   ["Brick", "Potter", "Soil", "Kiln"], "A",
   "The relation is raw material and product: bread is made from flour, and a brick is made from clay. The "
   "potter is the maker and the kiln the place of firing.", "analogies"),

 Q("Warm : Hot :: Cool : ?",
   ["Warm", "Mild", "Cold", "Humid"], "C",
   "The relation is one of degree: hot is a greater degree of warm, and cold is a greater degree of cool.", "analogies"),

 Q(sc(["All pens are books.", "All books are papers."], ["All pens are papers.", "Some papers are pens."]),
   FOLLOW, "D",
   "From two A propositions in the first figure, &ldquo;All pens are papers&rdquo; follows (Barbara). On the "
   "traditional reading, in which each class has members, &ldquo;All pens are papers&rdquo; gives "
   "&ldquo;Some papers are pens&rdquo; by conversion. Both follow.", "venn"),

 Q(sc(["Some doctors are singers.", "All singers are tall."], ["Some doctors are tall.", "All tall persons are singers."]),
   FOLLOW, "A",
   "The doctors who are singers are all tall, so some doctors are tall: I follows. &ldquo;All singers are "
   "tall&rdquo; cannot be turned round into &ldquo;All tall persons are singers&rdquo;: II does not follow.", "venn"),

 Q(sc(["Some fruits are sweet.", "All sweet things are tasty."], ["All fruits are tasty.", "Some tasty things are fruits."]),
   FOLLOW, "B",
   "The fruits that are sweet are tasty, so some fruits are tasty, and by conversion some tasty things are "
   "fruits: II follows. Nothing is said about the fruits that are not sweet, so &ldquo;All fruits are "
   "tasty&rdquo; does not follow.", "venn"),

 Q(sc(["Some cats are black.", "Some black things are dogs."], ["Some cats are dogs.", "All dogs are black."]),
   FOLLOW, "C",
   "From two particular premises no conclusion follows: the black things that are cats and the black things "
   "that are dogs may be entirely different. Nor does &ldquo;Some black things are dogs&rdquo; say anything "
   "about all dogs. Neither follows.", "venn"),

 Q("To represent the proposition &ldquo;All S is P&rdquo; on a Venn diagram of two overlapping circles, one:",
   ["places an X in the overlap of S and P", "shades the overlap of S and P",
    "places an X in the part of S outside P", "shades the part of S that lies outside P"], "D",
   "A universal proposition says a region is empty, and an empty region is shaded. &ldquo;All S is P&rdquo; "
   "says there is nothing in S outside P. An X marks a region that a particular proposition says is "
   "occupied.", "venn"),

 Q("Which arrangement of circles correctly represents the relation among the classes Dogs, Cats and Animals?",
   ["Three circles, each overlapping the other two", "Two separate circles inside a third, larger circle",
    "Three circles one inside another", "Two overlapping circles inside a third circle"], "B",
   "Every dog and every cat is an animal, so both circles lie inside the circle of animals; no dog is a cat, "
   "so the two inner circles do not overlap.", "venn"),

 Q("Match the school of Indian philosophy in List I with the number of pramanas it accepts in List II."
   + match(["Charvaka", "Vaisheshika", "Sankhya", "Nyaya"], ["One", "Two", "Three", "Four"]),
   ["(a)-(i), (b)-(ii), (c)-(iii), (d)-(iv)", "(a)-(i), (b)-(iii), (c)-(ii), (d)-(iv)",
    "(a)-(ii), (b)-(i), (c)-(iii), (d)-(iv)", "(a)-(i), (b)-(ii), (c)-(iv), (d)-(iii)"], "A",
   "Charvaka accepts perception alone; Vaisheshika (like Buddhism) perception and inference; Sankhya (like "
   "Yoga) adds verbal testimony; Nyaya adds comparison, making four.", "indian-logic"),

 Q("Which pramana is accepted by the Bhatta school of Mimamsa and by Advaita Vedanta but not by the "
   "Prabhakara school of Mimamsa?",
   ["Arthapatti", "Upamana", "Anupalabdhi", "Shabda"], "C",
   "Prabhakara Mimamsa accepts five pramanas: perception, inference, comparison, testimony and postulation "
   "(arthapatti). The Bhatta school and Advaita Vedanta add a sixth, non-apprehension (anupalabdhi).", "indian-logic"),

 Q("Match the term in List I with its meaning in List II."
   + match(["Prama", "Pramana", "Prameya", "Pramata"],
           ["The object of knowledge", "Valid knowledge", "The knower", "The means of valid knowledge"]),
   ["(a)-(ii), (b)-(i), (c)-(iv), (d)-(iii)", "(a)-(ii), (b)-(iv), (c)-(i), (d)-(iii)",
    "(a)-(iv), (b)-(ii), (c)-(i), (d)-(iii)", "(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)"], "B",
   "Prama is valid knowledge; pramana the means by which it is obtained; prameya what is known; pramata the "
   "one who knows. Knowledge that is not valid is aprama.", "indian-logic"),

 Q("Match the pramana in List I with the example in List II."
   + match(["Anumana", "Upamana", "Shabda", "Anupalabdhi"],
           ["Knowing that there is no pot on the floor because none is seen there",
            "Learning the capital of a country from a reliable teacher",
            "Recognising a gavaya in the forest from the description that it resembles a cow",
            "Knowing that there is fire on the hill from the smoke rising from it"]),
   ["(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)",
    "(a)-(iv), (b)-(ii), (c)-(iii), (d)-(i)", "(a)-(iv), (b)-(iii), (c)-(ii), (d)-(i)"], "D",
   "Anumana is inference from a mark invariably connected with the thing; upamana is knowledge from a "
   "described likeness; shabda is the testimony of a trustworthy person or of scripture; anupalabdhi is "
   "knowledge of an absence from non-perception.", "pramanas"),

 Q("A student is known to have passed an examination, and is also known to have been absent from its first "
   "sitting. One concludes that she must have appeared at the second sitting. The pramana at work is:",
   ["arthapatti", "upamana", "pratyaksha", "anupalabdhi"], "A",
   "Arthapatti (postulation) is supposing the one fact that reconciles two otherwise conflicting facts. The "
   "classic example: Devadatta grows fat though he never eats by day, so he must eat at night.", "pramanas"),

 Q("In Nyaya, the bare awareness of an object before it is identified and named, as against the judgement "
   "&ldquo;this is a pot&rdquo;, is called:",
   ["savikalpaka perception", "alaukika perception", "nirvikalpaka perception", "anumana"], "C",
   "Nirvikalpaka perception is indeterminate: awareness without naming or classifying. Savikalpaka perception "
   "is determinate: the object is known as being of a kind. Alaukika is extraordinary, as against ordinary "
   "(laukika), perception.", "pramanas"),

 Q("Shabda as a pramana is valid knowledge obtained from:",
   ["the contact of a sense organ with its object", "the words of a trustworthy person (apta) or of scripture",
    "the perceived likeness between two things", "the absence of an object"], "B",
   "Verbal testimony is a source of knowledge when the speaker is an apta: one who knows the truth and "
   "states it honestly. The first option describes pratyaksha, the third upamana and the fourth anupalabdhi.", "pramanas"),

 Q("In the inference &ldquo;The hill has fire, because it has smoke&rdquo;, the paksha, the sadhya and the "
   "hetu correspond, respectively, to which terms of the Western syllogism?",
   ["Major, minor and middle", "Middle, major and minor", "Minor, middle and major", "Minor, major and middle"], "D",
   "The paksha (the hill) is the subject of the inference: the minor term. The sadhya (fire) is what is to "
   "be proved of it: the major term. The hetu or linga (smoke) is the reason: the middle term.", "anumana"),

 Q("The five members of the Nyaya inference, in the correct order, are:",
   ["pratijna, hetu, udaharana, upanaya, nigamana", "hetu, pratijna, udaharana, nigamana, upanaya",
    "pratijna, udaharana, hetu, upanaya, nigamana", "udaharana, pratijna, hetu, upanaya, nigamana"], "A",
   "Proposition (the hill has fire), reason (because it has smoke), example (whatever has smoke has fire, as "
   "in a kitchen), application (the hill has such smoke), conclusion (therefore the hill has fire).", "anumana"),

 Q("&ldquo;Sound is eternal, because it is produced.&rdquo; Since whatever is produced is non-eternal, the "
   "reason here proves the opposite of what is to be proved. The hetvabhasa is:",
   ["savyabhichara", "asiddha", "viruddha", "badhita"], "C",
   "Viruddha is the contradictory reason: the hetu is invariably connected not with the sadhya but with its "
   "absence. Savyabhichara is the irregular reason, found with and without the sadhya.", "anumana"),

 Q("&ldquo;Fire is cold, because it is a substance.&rdquo; The conclusion is contradicted by perception, "
   "which shows fire to be hot. The hetvabhasa is:",
   ["satpratipaksha", "badhita", "viruddha", "asiddha"], "B",
   "Badhita is the sublated reason: the conclusion is refuted by another, stronger pramana (here "
   "perception). Satpratipaksha is the counter-balanced reason, where a second reason proves the opposite; "
   "asiddha is a reason that is itself unproved.", "anumana"),
]
