# -*- coding: utf-8 -*-
"""UGC NET Paper I, Unit 4: fifty exam-standard model questions."""
from . import AR, Q, ar, match, st

TITLE = "Communication"
BLURB = ("The process, models and types of communication, verbal and non-verbal communication, inter-cultural "
         "and group communication, classroom communication, barriers, and mass media and society.")

QUESTIONS = [
 Q("Arrange the following in the order in which they occur in the process of communication: (1) Decoding, "
   "(2) Feedback, (3) Encoding, (4) Transmission through a channel, (5) Idea in the mind of the sender.",
   ["5, 4, 3, 1, 2", "5, 3, 4, 1, 2", "3, 5, 4, 2, 1", "5, 3, 1, 4, 2"], "B",
   "The sender has an idea, encodes it into symbols, and sends the message through a channel; the receiver "
   "decodes it and responds with feedback, which makes the process two-way.", "meaning"),

 Q("Match the model of communication in List I with its key idea in List II."
   + match(["Lasswell", "Shannon and Weaver", "Berlo", "Schramm"],
           ["Source, message, channel, receiver", "Overlap of the fields of experience of sender and receiver",
            "Who says what, in which channel, to whom, with what effect", "Noise in a linear, mathematical model"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)"], "D",
   "Lasswell (1948) framed communication as five questions; Shannon and Weaver introduced noise; Berlo (1960) "
   "gave the SMCR model; Schramm's circular model says communication works where the fields of experience "
   "overlap.", "meaning"),

 Q("A principal sends a circular to all teachers; the teachers talk about it in the staff room; a rumour "
   "about it then reaches the students. These are examples, respectively, of:",
   ["downward, horizontal and grapevine communication", "upward, horizontal and formal communication",
    "downward, diagonal and formal communication", "horizontal, downward and grapevine communication"], "A",
   "A circular from a superior to subordinates is formal downward communication. Talk among equals is "
   "horizontal (lateral). A rumour travels by the informal channel, the grapevine.", "meaning"),

 Q("Consider the statements about communication:"
   + st("It is a continuous process, not a single act.", "Once made, a communication cannot be taken back.",
        "It is possible for a person in the presence of others to communicate nothing at all.",
        "It is shaped by its context.")
   + "Which of the statements are correct?",
   ["I and II only", "I, III and IV only", "I, II and IV only", "I, II, III and IV"], "C",
   "Communication is a process, irreversible and contextual. (III) is false: one cannot not communicate; "
   "silence, posture and absence also send messages.", "meaning"),

 Q("A lecturer rehearses a difficult explanation silently in her own mind before entering the class. This "
   "is:",
   ["interpersonal communication", "intrapersonal communication", "group communication", "mass communication"], "B",
   "Intrapersonal communication takes place within oneself: thinking, planning, self-talk. Interpersonal "
   "communication is between two persons.", "meaning"),

 Q("Which of the following models describes communication as helical, growing and building on itself over "
   "time?",
   ["Aristotle's", "Berlo's", "Lasswell's", "Dance's"], "D",
   "Frank Dance (1967) pictured communication as a helix: it never returns to the same point but builds on "
   "what went before. Aristotle's, Lasswell's and Berlo's models are linear.", "meaning"),

 Q(ar("Feedback makes communication a two-way process.",
      "Through feedback the sender learns how the message has been received and understood."),
   AR, "A",
   "Without feedback the sender cannot know whether the message was understood as intended; with it, sender "
   "and receiver exchange roles. Both statements are true and (R) explains (A).", "meaning"),

 Q("A junior lecturer of the Statistics department writes directly to the Dean of another faculty about "
   "sharing a laboratory. The direction of this communication is:",
   ["upward", "horizontal", "diagonal", "downward"], "C",
   "Diagonal communication crosses both levels and departments. Upward communication goes to one's own "
   "superior; horizontal is between equals.", "meaning"),

 Q("In Aristotle's model of communication the three main elements are:",
   ["speaker, speech and audience", "source, message and channel", "sender, noise and receiver",
    "encoder, decoder and interpreter"], "A",
   "The classical model, concerned with persuasion, has the speaker, the speech and the audience (with the "
   "occasion and the effect). It is the earliest linear model.", "meaning"),

 Q("The word &lsquo;communication&rsquo; is derived from the Latin <em>communis</em>, which means:",
   ["to speak", "common", "to send", "message"], "B",
   "<em>Communis</em> means &lsquo;common&rsquo;: to communicate is to make an idea common to sender and "
   "receiver, that is, to share meaning.", "meaning"),

 Q("Match the kind of non-verbal communication in List I with what it concerns in List II."
   + match(["Kinesics", "Proxemics", "Haptics", "Chronemics"],
           ["Touch", "The use of time", "Body movement, gesture and posture", "The use of space and distance"]),
   ["(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "A",
   "Kinesics is body language; proxemics (Edward T. Hall) is space; haptics is touch; chronemics is time. "
   "Oculesics is eye contact and paralanguage is how words are said.", "verbal"),

 Q("A speaker conveys sarcasm by the pitch and stress with which the words &ldquo;Very good&rdquo; are said. "
   "The cue lies in:",
   ["kinesics", "artifactics", "proxemics", "paralanguage"], "D",
   "Paralanguage (vocalics) is everything about the voice other than the words: pitch, tone, volume, pace and "
   "pauses. The same words can praise or mock according to it.", "verbal"),

 Q("In Edward T. Hall's classification of distances, a teacher lecturing to a class from the platform, some "
   "four metres or more from the nearest student, is using:",
   ["intimate distance", "personal distance", "public distance", "social distance"], "C",
   "Hall's distances: intimate (up to about 45 cm), personal (about 45 cm to 1.2 m), social (about 1.2 to "
   "3.6 m) and public (beyond about 3.6 m).", "verbal"),

 Q("Which of the following is NOT one of the seven Cs of effective communication as business communication "
   "lists them?",
   ["Concise", "Complex", "Courteous", "Concrete"], "B",
   "The seven Cs are clear, concise, concrete, correct, coherent, complete and courteous. Complexity works "
   "against clarity.", "verbal"),

 Q("Consider the statements about Mehrabian's 7&ndash;38&ndash;55 finding:"
   + st("It concerns messages about feelings and attitudes.",
        "It applies when the words and the tone or face disagree.",
        "It shows that in every kind of communication only 7% of the meaning is carried by words.",
        "The 55% refers to facial expression.")
   + "Which of the statements are correct?",
   ["I and II only", "II and III only", "I, II, III and IV", "I, II and IV only"], "D",
   "Mehrabian studied how listeners judge a speaker's feelings when words and non-verbal cues conflict: about "
   "7% words, 38% tone of voice, 55% face. It is often misquoted as a law of all communication, which it is "
   "not: (III) is false.", "verbal"),

 Q(ar("When a speaker's words and non-verbal signals contradict each other, listeners tend to believe the "
      "non-verbal signals.",
      "Non-verbal signals are harder to control deliberately than words."),
   AR, "A",
   "A teacher who says &ldquo;Take your time&rdquo; while looking at the clock is believed by the clock. "
   "Because gesture, face and voice are less under conscious control, they are taken as the truer guide. Both "
   "statements are true and (R) is the reason.", "verbal"),

 Q("Which of the following best describes active listening?",
   ["Hearing the words while preparing one's reply", "Remaining silent throughout",
    "Attending fully, not interrupting, asking questions and restating what was heard",
    "Listening only to the parts one agrees with"], "C",
   "Hearing is physical; listening is mental. Active listening adds attention, questions and paraphrase, so "
   "that the speaker knows the message has been received.", "verbal"),

 Q("A student chooses to sit in the last row, as far from the teacher as the room allows. The cue is:",
   ["proxemic", "haptic", "chronemic", "paralinguistic"], "A",
   "The student is using distance, which is the subject of proxemics.", "verbal"),

 Q("A candidate arrives twenty minutes late for an interview, and the panel forms an unfavourable impression "
   "before a word is spoken. The non-verbal cue involved is:",
   ["haptics", "chronemics", "oculesics", "kinesics"], "B",
   "Chronemics is communication through the use of time: punctuality, waiting, pauses. Lateness is read as a "
   "message about the person's attitude.", "verbal"),

 Q("In a high-context culture, as Edward T. Hall described it:",
   ["meaning is stated fully and explicitly in words",
    "written contracts matter more than relationships",
    "silence carries no meaning",
    "much of the meaning lies in the setting, the relationship and what is left unsaid"], "D",
   "In high-context cultures the listener is expected to read the situation; in low-context cultures the "
   "speaker is expected to say exactly what is meant.", "intercultural"),

 Q("A host says &ldquo;We will see&rdquo; to a visitor's proposal, meaning a polite refusal; the visitor "
   "takes it as an open question. The misunderstanding arises mainly from a difference between:",
   ["formal and informal channels", "upward and downward communication",
    "high-context and low-context styles of communication", "verbal and written communication"], "C",
   "The host relies on context to convey the refusal; the visitor reads only the literal words. This is the "
   "classic difficulty between high-context and low-context communicators.", "intercultural"),

 Q("Which of the following is NOT one of Hofstede's dimensions of national culture?",
   ["Power distance", "Uncertainty avoidance", "Individualism and collectivism", "High and low context"], "D",
   "Hofstede's dimensions are power distance, individualism&ndash;collectivism, masculinity&ndash;femininity, "
   "uncertainty avoidance, long-term&ndash;short-term orientation and indulgence&ndash;restraint. High and low "
   "context is Hall's distinction.", "intercultural"),

 Q("Arrange Tuckman's stages of group development in the correct order: (1) Norming, (2) Adjourning, "
   "(3) Forming, (4) Performing, (5) Storming.",
   ["3, 5, 1, 4, 2", "3, 1, 5, 4, 2", "5, 3, 1, 4, 2", "3, 5, 4, 1, 2"], "A",
   "Forming, storming, norming, performing (1965), with adjourning added in 1977.", "intercultural"),

 Q("In its second week a new research team quarrels over who should do what; it then agrees on rules and "
   "roles. The team has moved:",
   ["from forming to storming", "from storming to norming", "from norming to performing",
    "from performing to adjourning"], "B",
   "Conflict over roles is the storming stage; settling rules and roles is norming.", "intercultural"),

 Q("Judging the customs of another culture by the standards of one's own, and finding them inferior, is "
   "called:",
   ["stereotyping", "groupthink", "ethnocentrism", "acculturation"], "C",
   "Ethnocentrism treats one's own culture as the measure of others. Stereotyping is attributing a fixed set "
   "of traits to every member of a group.", "intercultural"),

 Q("A close-knit committee approves a risky plan without examining the alternatives, because no member wishes "
   "to disturb the agreement. This is an example of:",
   ["groupthink", "brainstorming", "the grapevine", "the two-step flow"], "A",
   "Groupthink (Irving Janis, 1972) is the tendency of a cohesive group to put agreement above realistic "
   "appraisal of alternatives.", "intercultural"),

 Q("In which communication network of a small group do all messages pass through one central person?",
   ["Circle", "All-channel", "Chain", "Wheel"], "D",
   "The wheel is the most centralised network and is quick for simple tasks. In the all-channel network "
   "everyone communicates with everyone, which suits complex problems and gives the most satisfaction.", "intercultural"),

 Q("In Flanders' Interaction Analysis Categories System, the number of categories and the interval at which "
   "classroom talk is coded are:",
   ["seven categories; every ten seconds", "ten categories; every three seconds",
    "ten categories; every ten seconds", "twelve categories; every three seconds"], "B",
   "Flanders' system has ten categories and the observer records a category every three seconds.", "classroom"),

 Q("Match the group in Flanders' system (List I) with its categories (List II)."
   + match(["Teacher talk: indirect influence", "Teacher talk: direct influence", "Student talk", "Silence or confusion"],
           ["Categories 8 and 9", "Category 10", "Categories 1 to 4", "Categories 5 to 7"]),
   ["(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)"], "C",
   "Indirect influence: accepts feeling, praises, accepts or uses students' ideas, asks questions (1&ndash;4). "
   "Direct influence: lectures, gives directions, criticises or justifies authority (5&ndash;7). Student talk: "
   "response and initiation (8, 9). Silence or confusion: 10.", "classroom"),

 Q("A teacher says: &ldquo;Good point, Asha; let us build on that.&rdquo; In Flanders' system this is:",
   ["category 5, lecturing", "category 7, criticising", "category 9, student initiation",
    "category 3, accepting or using a student's idea"], "D",
   "The teacher takes up a student's idea and develops it: category 3, an indirect influence. (The praise in "
   "&ldquo;good point&rdquo; alone would be category 2.)", "classroom"),

 Q("Research on &lsquo;wait time&rsquo; in classroom questioning is associated with:",
   ["Mary Budd Rowe", "Ned Flanders", "Bruce Tuckman", "Irving Janis"], "A",
   "Mary Budd Rowe showed that pausing a few seconds after a question brings longer and better answers from "
   "more students.", "classroom"),

 Q("Which of the following is a higher-order, open question?",
   ["What is the formula for the mean?", "Why would the median be preferred to the mean for these incomes?",
    "Who introduced the term &lsquo;statistics&rsquo;?", "Is 7 a prime number?"], "B",
   "Open, higher-order questions ask &lsquo;why&rsquo; and &lsquo;what if&rsquo; and admit a reasoned "
   "answer; closed questions have one short answer and check recall.", "classroom"),

 Q("Consider the statements about feedback given by a teacher to students:"
   + st("It should be prompt.", "It should be specific.", "It should be about the work and not the person.",
        "It is most useful when given only at the end of the course.")
   + "Which of the statements are correct?",
   ["I and II only", "II, III and IV only", "I, II and III only", "I, II, III and IV"], "C",
   "Feedback helps learning when it comes while the work is fresh, says exactly what is right or wrong, and "
   "addresses the task. Feedback that arrives only at the end comes too late to be used: (IV) is false.", "classroom"),

 Q(ar("A higher proportion of indirect teacher talk is taken as a sign of a more participative classroom.",
      "Indirect influence, such as accepting feelings and using students' ideas, encourages students to talk."),
   AR, "A",
   "In Flanders' analysis the ratio of indirect to direct teacher talk indicates how far the teacher opens "
   "the floor to students. Both statements are true and (R) explains (A).", "classroom"),

 Q("Classroom communication is most effective when it is:",
   ["one-way, so that no time is lost", "confined to the spoken word",
    "delivered in technical language to raise standards",
    "two-way, clear, suited to the learners and varied in mode"], "D",
   "Effective classroom communication invites questions, uses language the learners follow, and combines "
   "spoken, written and visual modes.", "classroom"),

 Q("Match the example in List I with the kind of barrier to communication in List II."
   + match(["A faulty microphone", "Unexplained technical jargon", "Anxiety of the listener",
            "A long chain of command that filters messages"],
           ["Semantic", "Organisational", "Physical", "Psychological"]),
   ["(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)",
    "(a)-(i), (b)-(iii), (c)-(iv), (d)-(ii)", "(a)-(iii), (b)-(i), (c)-(ii), (d)-(iv)"], "B",
   "Faulty equipment and noise are physical barriers; jargon and ambiguous words are semantic; anxiety, anger "
   "and prejudice are psychological; long hierarchies, filtering and overload are organisational.", "barriers"),

 Q("A lecturer uses the word &lsquo;heteroscedasticity&rsquo; with a first-year class without explaining it. "
   "The barrier created is:",
   ["semantic", "physical", "physiological", "cultural"], "A",
   "The difficulty lies in the meaning of the word: a semantic (language) barrier.", "barriers"),

 Q("A manager reports only the good news from the shop floor to the director. This is called:",
   ["noise", "selective perception", "filtering", "information overload"], "C",
   "Filtering is the deliberate shaping of information by the sender so that it will be seen favourably by "
   "the receiver. It is an organisational barrier, common in upward communication.", "barriers"),

 Q("A listener who dislikes a speaker hears only the points that confirm that dislike. The barrier is:",
   ["physical", "semantic", "organisational", "perceptual"], "D",
   "Selective perception: people notice and remember what fits their existing frame of reference. Together "
   "with stereotypes it makes up the perceptual barriers.", "barriers"),

 Q("Which of the following is a physiological barrier to communication?",
   ["Ambiguous wording", "Hearing difficulty or fatigue", "Rigid hierarchy", "Distance between speaker and listener"], "B",
   "Physiological barriers lie in the body of the communicator or receiver: poor hearing or sight, fatigue, "
   "illness. Distance is a physical barrier.", "barriers"),

 Q("Consider the following ways of overcoming barriers to communication:"
   + st("Using simple and clear language", "Checking understanding through feedback",
        "Listening actively and with empathy", "Sending as much information as possible in every message")
   + "Which of them are effective?",
   ["I, II and III only", "I and II only", "II, III and IV only", "I, II, III and IV"], "A",
   "Too much information in a message causes overload, itself a barrier. Simple language, feedback, the right "
   "channel, active listening and empathy are the remedies.", "barriers"),

 Q(ar("Noise is a barrier to communication.",
      "In communication theory, noise means only loud sound in the physical environment."),
   AR, "C",
   "(A) is true. (R) is false: noise is anything that distorts the message at any stage. It may be physical "
   "(sound), physiological, semantic (misunderstood words) or psychological (prejudice, anxiety).", "barriers"),

 Q("Match the theory of mass communication in List I with its idea in List II."
   + match(["Hypodermic needle", "Two-step flow", "Agenda-setting", "Uses and gratifications"],
           ["An active audience uses media to satisfy its own needs",
            "Media tell people what to think about, not what to think",
            "Media inject messages directly into a passive audience",
            "Media influence passes through opinion leaders"]),
   ["(a)-(iii), (b)-(i), (c)-(ii), (d)-(iv)", "(a)-(iv), (b)-(iii), (c)-(ii), (d)-(i)",
    "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "D",
   "The hypodermic needle (magic bullet) view assumes a passive audience; Lazarsfeld and Katz's two-step flow "
   "brings in opinion leaders; McCombs and Shaw's agenda-setting concerns what people think about; uses and "
   "gratifications starts from an active audience.", "massmedia"),

 Q("During an election a news channel devotes most of its time to unemployment, and voters later name "
   "unemployment as the most important issue. This fits the theory of:",
   ["cultivation", "agenda-setting", "spiral of silence", "uses and gratifications"], "B",
   "Agenda-setting (McCombs and Shaw, 1972): the prominence the media give to an issue shapes how important "
   "the public thinks it is.", "massmedia"),

 Q("The statement &ldquo;the medium is the message&rdquo; and the idea of the &lsquo;global village&rsquo; "
   "are due to:",
   ["Marshall McLuhan", "Harold Lasswell", "Wilbur Schramm", "George Gerbner"], "A",
   "McLuhan (<em>Understanding Media</em>, 1964) argued that the form of a medium shapes society more than "
   "the content it carries.", "massmedia"),

 Q("According to the spiral of silence theory of Elisabeth Noelle-Neumann:",
   ["heavy television viewing shapes beliefs about the real world",
    "audiences choose media to satisfy their needs",
    "people who believe they are in the minority tend to remain silent, which makes the majority view seem stronger",
    "media messages reach people through opinion leaders"], "C",
   "Fear of isolation keeps those who think they are in the minority from speaking, so the apparent majority "
   "grows. Option A is Gerbner's cultivation theory.", "massmedia"),

 Q("Arrange the following in chronological order: (1) Setting up of Prasar Bharati, (2) Hicky's Bengal "
   "Gazette, (3) Beginning of Doordarshan as an experimental service, (4) The name All India Radio adopted, "
   "(5) The Satellite Instructional Television Experiment.",
   ["2, 3, 4, 5, 1", "2, 4, 5, 3, 1", "4, 2, 3, 5, 1", "2, 4, 3, 5, 1"], "D",
   "Hicky's Bengal Gazette, India's first newspaper, 1780; All India Radio so named in 1936; Doordarshan "
   "began on 15 September 1959; SITE ran in 1975&ndash;76; Prasar Bharati was set up in 1997.", "massmedia"),

 Q("Lasswell named three functions of mass communication, to which Charles Wright added a fourth. The "
   "function added by Wright is:",
   ["surveillance of the environment", "entertainment", "correlation of society's response",
    "transmission of culture"], "B",
   "Lasswell: surveillance, correlation and transmission of the cultural heritage. Wright added "
   "entertainment.", "massmedia"),

 Q("The Satellite Instructional Television Experiment (SITE) of 1975&ndash;76 is remembered because it:",
   ["carried educational television programmes to villages by satellite",
    "was India's first private television channel", "introduced colour television in India",
    "started FM radio broadcasting"], "A",
   "SITE used a satellite to bring instructional television to villages, an early large-scale use of "
   "satellite broadcasting for education and development.", "massmedia"),

 Q("Consider the statements:"
   + st("Mass media address large, scattered and heterogeneous audiences.",
        "Feedback in mass communication is generally delayed and limited.",
        "All India Radio and Doordarshan are run by Prasar Bharati.",
        "The hypodermic needle theory assumes an active, selective audience.")
   + "Which of the statements are correct?",
   ["I and II only", "I, III and IV only", "I, II and III only", "I, II, III and IV"], "C",
   "The hypodermic needle theory assumes a <em>passive</em> audience into which messages are injected; the "
   "active audience belongs to the uses and gratifications approach. The other three statements are correct.", "massmedia"),
]
