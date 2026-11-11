# -*- coding: utf-8 -*-
"""UGC NET Paper I, Unit 3: fifty exam-standard model questions on ten passages.

The passages were written for this page; none is taken from a past paper or a
published source.
"""
from . import Q, st

TITLE = "Comprehension"
BLURB = ("Ten passages, each followed by five questions of the kinds the paper sets: the main idea, a stated "
         "detail, an inference, the meaning of a word in its context, the author's attitude and the best "
         "title.")


def P(n, text):
    a = 5 * n - 4
    return ("PASSAGE", "Passage %d (Questions %d&ndash;%d)" % (n, a, a + 4),
            "".join("<p>%s</p>" % p for p in text))


QUESTIONS = [
 P(1, ["A census counts everyone; a sample survey counts a few and reasons to the rest. It is tempting to "
       "think that the census must be the more accurate of the two, since it leaves no one out. In practice "
       "the opposite is often true. A census needs an army of temporary enumerators, hurriedly trained and "
       "thinly supervised, and the errors they make in asking and recording do not shrink as the count grows; "
       "they accumulate. A survey of a few thousand households can employ a small, well-trained staff, revisit "
       "doubtful cases and check its own work.",
       "The survey pays for this with sampling error, the error that arises because only a part was observed. "
       "But sampling error has a virtue that the other kind lacks: when the sample is drawn by chance, its size "
       "can be calculated from the sample itself. The careful surveyor therefore knows roughly how wrong the "
       "estimate may be. The census-taker, whose errors are of the unmeasured kind, often does not."]),

 Q("The main point of the passage is that:",
   ["a census is always less accurate than a sample survey",
    "a well-conducted sample survey can be more accurate than a census, and its error can be assessed",
    "sampling error is larger than every other kind of error", "enumerators should be better paid"], "B",
   "The passage argues that non-sampling errors can make a census less accurate, while a survey can control "
   "them and also measure its sampling error. Option A overstates (&lsquo;often&rsquo;, not "
   "&lsquo;always&rsquo;); C contradicts the passage; D is not discussed.", "kinds"),

 Q("According to the passage, the errors made by enumerators in a census:",
   ["cancel one another as the count grows", "can be calculated from the census itself",
    "arise because only a part of the population is observed", "accumulate as the count grows"], "D",
   "The first paragraph says these errors &lsquo;do not shrink as the count grows; they accumulate&rsquo;. "
   "Options B and C describe sampling error, not enumerators' errors.", "kinds"),

 Q("The &lsquo;virtue&rsquo; of sampling error mentioned in the second paragraph is that it:",
   ["can be estimated from the sample when the sample is drawn by chance", "is always very small",
    "disappears when enumerators are well trained", "does not affect the estimate"], "A",
   "&lsquo;When the sample is drawn by chance, its size can be calculated from the sample itself.&rsquo; The "
   "passage does not say it is small or absent, only that it is measurable.", "kinds"),

 Q("It can be inferred from the passage that the author would agree that:",
   ["a census should never be taken", "the size of an operation is no guarantee of its accuracy",
    "sample surveys have no errors other than sampling error", "temporary staff work better than permanent staff"], "B",
   "The whole argument is that counting everyone does not by itself make a result accurate. The author does "
   "not reject the census altogether (A), admits surveys need care with doubtful cases (C), and blames "
   "hurried training of temporary staff (D).", "kinds"),

 Q("In the passage, the word &lsquo;thinly&rsquo; in &lsquo;thinly supervised&rsquo; most nearly means:",
   ["cheaply", "strictly", "inadequately", "secretly"], "C",
   "Supervision spread too thin is insufficient supervision. The context, hurried training and accumulating "
   "errors, points to inadequacy, not to cost, strictness or secrecy.", "kinds"),

 P(2, ["When a teacher asks a question and a hand goes up at once, the class learns something the teacher did "
       "not intend: that questions are answered by the quick. Studies of classrooms have found that teachers "
       "typically wait less than a second after asking before they call on someone or answer themselves. When "
       "the pause is lengthened to three seconds or more, the changes are striking. Answers become longer; "
       "more students offer them; students begin to respond to one another and not only to the teacher; and "
       "those who seldom spoke begin to speak.",
       "The pause costs nothing and needs no equipment, yet it is hard to keep. Silence in a classroom feels "
       "like failure, and a teacher's instinct is to fill it. What the longer wait asks of the teacher is not "
       "a new technique so much as a different belief: that thinking takes time, and that a question worth "
       "asking is worth waiting for."]),

 Q("The passage is mainly about:",
   ["the difficulty of maintaining discipline", "the effect of waiting longer after asking a question",
    "the need for equipment in classrooms", "why quick students should be rewarded"], "B",
   "Both paragraphs concern the pause after a question: what a longer pause changes, and why teachers find "
   "it hard to keep.", "kinds"),

 Q("Which of the following is NOT mentioned as a result of a longer pause?",
   ["Answers become longer", "More students answer", "Students respond to one another",
    "Students score higher in the final examination"], "D",
   "The passage lists longer answers, more students answering, students responding to one another and quiet "
   "students speaking. Examination scores are not mentioned; choosing D needs no outside knowledge, only a "
   "check against the list.", "eliminate"),

 Q("According to the passage, teachers find the longer pause hard to keep because:",
   ["silence feels like failure and they want to fill it", "it requires expensive equipment",
    "students object to it", "the syllabus leaves no time"], "A",
   "&lsquo;Silence in a classroom feels like failure, and a teacher's instinct is to fill it.&rsquo; The "
   "passage says the pause costs nothing and needs no equipment.", "kinds"),

 Q("The opening sentence suggests that calling on the first hand raised teaches the class that:",
   ["the teacher is well prepared", "only correct answers matter", "speed is valued above thought",
    "questions have no answers"], "C",
   "&lsquo;Questions are answered by the quick&rsquo; is an unintended lesson: that being fast is what "
   "counts. The rest of the passage contrasts this with the belief that thinking takes time.", "kinds"),

 Q("The author's attitude to the longer pause is best described as:",
   ["sceptical", "approving", "indifferent", "mocking"], "B",
   "The author reports its benefits as &lsquo;striking&rsquo; and ends by recommending the belief behind it. "
   "There is no doubt, indifference or ridicule in the tone.", "kinds"),

 P(3, ["Rivers were once described as the veins of a country, and the comparison is more exact than it "
       "sounds. A river is not a pipe that carries water from one place to another; it is a living system "
       "that carries silt, nutrients, fish and seeds, floods its plain in one season and shrinks in another, "
       "and in doing so builds the very land that people farm. When a river is straightened, walled and "
       "dammed so that it behaves like a pipe, it delivers water more reliably, but it stops doing the other "
       "things. The delta that received its silt begins to sink and the sea advances; the fish that travelled "
       "upstream to breed find a wall in their way.",
       "None of this is an argument against dams, which have fed and lit millions of homes. It is an argument "
       "against a habit of mind that counts only what a river is made to do and never what it had been doing "
       "all along, unasked and unpaid."]),

 Q("The central idea of the passage is that:",
   ["dams should not be built", "rivers are best understood as pipes that deliver water",
    "a river does much more than carry water, and this is forgotten when it is engineered",
    "deltas are sinking all over the world"], "C",
   "The passage contrasts the river as a living system with the river treated as a pipe, and objects to "
   "ignoring what the natural river does. It expressly says it is not an argument against dams.", "kinds"),

 Q("According to the passage, when a river is engineered to behave like a pipe:",
   ["it delivers water less reliably", "its delta receives more silt", "fish find it easier to travel upstream",
    "it delivers water more reliably but ceases to perform its other functions"], "D",
   "&lsquo;It delivers water more reliably, but it stops doing the other things.&rsquo; The delta loses silt "
   "and the fish meet a wall, the reverse of options B and C.", "kinds"),

 Q("The phrase &lsquo;unasked and unpaid&rsquo; refers to:",
   ["the services a river provides naturally", "the labourers who build dams",
    "farmers who use river water", "engineers who design canals"], "A",
   "The phrase describes &lsquo;what it had been doing all along&rsquo;: building land, carrying silt and "
   "nutrients, sustaining fish. Nobody ordered these services or paid for them.", "kinds"),

 Q("The author's attitude towards dams is:",
   ["wholly hostile", "balanced: aware of their benefits and of their costs", "uncritically admiring",
    "uninterested"], "B",
   "The author grants that dams &lsquo;have fed and lit millions of homes&rsquo; and objects only to a way of "
   "thinking that overlooks what is lost.", "kinds"),

 Q("The most suitable title for the passage is:",
   ["How Dams Are Built", "The History of Irrigation", "More Than a Pipe: What Rivers Do",
    "Fishing in Rivers"], "C",
   "A title should cover the whole passage and its point: that a river is more than a carrier of water. The "
   "other titles fit a detail or a topic the passage does not treat.", "kinds"),

 P(4, ["A translation is often judged by how little of itself it shows. The ideal, on this view, is a pane of "
       "glass: the reader should look through it at the original and forget that anyone stood between. The "
       "ideal is attractive and impossible. Languages do not divide the world in the same places. One has a "
       "single word where another needs a sentence; one marks respect in every verb, another cannot mark it "
       "at all. The translator must therefore choose, at every line, what to keep and what to let go, and a "
       "choice is a kind of authorship.",
       "This does not mean that anything goes. A translator is like a musician playing a written score: free "
       "in phrasing and bound in notes. The good ones know which is which. What it does mean is that readers "
       "should stop asking whether a translation is faithful, as though faithfulness were one thing, and ask "
       "what it has chosen to be faithful to."]),

 Q("The &lsquo;pane of glass&rsquo; stands for a translation that:",
   ["is full of the translator's opinions", "is so transparent that the reader forgets the translator",
    "is difficult to read", "changes the meaning of the original"], "B",
   "The image is of looking through the translation at the original, forgetting &lsquo;that anyone stood "
   "between&rsquo;.", "kinds"),

 Q("The author calls the ideal of the invisible translator &lsquo;impossible&rsquo; because:",
   ["translators are poorly trained", "readers dislike translations", "publishers interfere with the text",
    "languages differ in how they divide the world, so the translator must make choices"], "D",
   "&lsquo;Languages do not divide the world in the same places&rsquo;; hence the translator must choose "
   "what to keep, and &lsquo;a choice is a kind of authorship&rsquo;.", "kinds"),

 Q("The comparison with a musician is used to show that a translator:",
   ["has freedom within limits", "has no freedom at all", "may change the original at will",
    "needs musical training"], "A",
   "&lsquo;Free in phrasing and bound in notes&rsquo;: some things may be varied, others must be kept. This "
   "guards against reading the first paragraph as &lsquo;anything goes&rsquo;.", "kinds"),

 Q("Which of the following statements would the author most probably accept?",
   ["There is exactly one faithful translation of any text",
    "A translation should be judged without reference to the original",
    "Two good translations of the same work may differ because they are faithful to different things",
    "Translation is a mechanical activity"], "C",
   "The closing sentence asks readers to consider &lsquo;what it has chosen to be faithful to&rsquo;, which "
   "implies that faithfulness is not one thing and that good translations can differ.", "kinds"),

 Q("In the passage, the word &lsquo;bound&rsquo; in &lsquo;bound in notes&rsquo; most nearly means:",
   ["heading towards", "obliged to follow", "tied with rope", "leaping"], "B",
   "The musician is free in one respect and constrained in another: &lsquo;bound&rsquo; here means obliged, "
   "restricted. The other meanings of the word do not fit the contrast with &lsquo;free&rsquo;.", "kinds"),

 P(5, ["An average is a useful servant and a poor master. To say that the average income of a village has "
       "risen is to say something true and to conceal something that may be more important: who gained. If "
       "one family's income rises tenfold and the rest stand still, the average rises, and a report that "
       "stops at the average will describe a village that no one lives in.",
       "The remedy is not to distrust averages but to ask for their companions. The median tells where the "
       "middle household stands and is unmoved by a fortune at the top. A measure of spread tells how far the "
       "households lie from one another. A table by groups tells whether the landless shared in the gain. "
       "Each of these costs a line in a report. Their absence should make a reader curious, for a figure that "
       "travels alone has usually left something behind."]),

 Q("The main argument of the passage is that:",
   ["averages are false and should not be used", "the median is always better than the mean",
    "an average should be read along with other measures that show how the values are distributed",
    "village incomes have not risen"], "C",
   "The author says the remedy &lsquo;is not to distrust averages but to ask for their companions&rsquo;: "
   "the median, a measure of spread, a table by groups.", "kinds"),

 Q("&lsquo;A village that no one lives in&rsquo; means:",
   ["a village that has been abandoned", "a village with a very small population",
    "a village that exists only on paper for tax purposes",
    "a picture given by the average that matches the condition of no actual household"], "D",
   "If one family gains hugely and the rest do not, the &lsquo;average household&rsquo; described by the "
   "report corresponds to nobody: it is a statistical fiction.", "kinds"),

 Q("According to the passage, the median is useful because it:",
   ["is not affected by a very large value at the top", "is always larger than the mean",
    "is easier to calculate than the mean", "measures the spread of incomes"], "A",
   "The median &lsquo;is unmoved by a fortune at the top&rsquo;. The passage says nothing about its size "
   "relative to the mean or its ease of calculation, and spread is a separate measure.", "kinds"),

 Q("The last sentence implies that when a report gives only an average, the reader should:",
   ["accept it, since averages are true", "suspect that relevant information has been omitted",
    "reject the report altogether", "calculate the average again"], "B",
   "&lsquo;A figure that travels alone has usually left something behind&rsquo;: the missing companions "
   "should make the reader curious about what is not shown, not dismiss the report.", "kinds"),

 Q("The expression &lsquo;a useful servant and a poor master&rsquo; suggests that an average:",
   ["should never be used", "is expensive to compute", "is helpful as an aid but misleading if relied on alone",
    "is used mainly by servants and masters"], "C",
   "The proverb-like phrase means the thing serves well when kept in its place and badly when allowed to "
   "rule: the average helps, but should not be the only guide.", "kinds"),

 P(6, ["The first printed books were made to look like manuscripts. Their letters copied the hands of "
       "scribes; spaces were left for initials to be painted in by hand; some were even printed on vellum. "
       "The printers were not timid. They were selling to buyers who knew what a book looked like, and a book "
       "looked like a manuscript. It took about two generations for print to discover what it could do that "
       "the pen could not: title pages, page numbers, indexes that sent every reader to the same place, "
       "identical copies that could be cited and corrected.",
       "Every new medium seems to begin this way, by imitating the one it will displace. Early films were "
       "plays photographed from a seat in the stalls; early web pages were brochures. The imitation is not a "
       "failure of imagination. It is how a new thing earns the trust that later allows it to become itself."]),

 Q("The passage is chiefly concerned with:",
   ["the superiority of manuscripts over printed books", "the invention of the index",
    "how a new medium at first imitates the old one before finding its own possibilities",
    "the decline of the theatre"], "C",
   "The first paragraph gives the case of print, the second generalises it to film and the web: imitation "
   "first, then discovery of what the new medium can do.", "kinds"),

 Q("According to the passage, early printers made books resemble manuscripts because:",
   ["they lacked the skill to do otherwise", "buyers expected a book to look like a manuscript",
    "the law required it", "vellum was cheaper than paper"], "B",
   "&lsquo;They were selling to buyers who knew what a book looked like, and a book looked like a "
   "manuscript.&rsquo; The author expressly denies that the printers were timid.", "kinds"),

 Q("Which of the following is mentioned as something print could do that the pen could not?",
   ["Painted initials", "The use of vellum", "The copying of scribes' handwriting",
    "Identical copies that could be cited and corrected"], "D",
   "The list of what print discovered includes title pages, page numbers, indexes and identical copies. The "
   "other three options are features of the early imitation of manuscripts.", "kinds"),

 Q("The author regards the early imitation of an older medium as:",
   ["a necessary stage that earns trust", "a failure of imagination", "a commercial fraud", "an accident"], "A",
   "&lsquo;The imitation is not a failure of imagination. It is how a new thing earns the trust that later "
   "allows it to become itself.&rsquo;", "kinds"),

 Q("The examples of early films and early web pages are given in order to:",
   ["show that films are inferior to plays", "show that the pattern seen in printing is a general one",
    "criticise the internet", "prove that printing was unimportant"], "B",
   "They follow the sentence &lsquo;Every new medium seems to begin this way&rsquo; and serve as further "
   "instances of the same pattern.", "kinds"),

 P(7, ["It is a commonplace that correlation is not causation, and like most commonplaces it is repeated "
       "more often than it is used. Towns with more police have more crime; countries that eat more chocolate "
       "win more scientific prizes. Few are deceived by examples like these, because the absurdity is on the "
       "surface. The danger lies in the cases where a causal story is ready to hand. Children who have "
       "breakfast do better at school: of course, we say, a fed child attends. But households that give "
       "breakfast differ from those that do not in income, in routine, in the time adults have; and any of "
       "these might do the work that we have credited to the meal.",
       "The cure is not to stop looking for causes, which would be to stop thinking. It is to ask, of every "
       "pleasing explanation, what else would have to be true if it were right, and then to go and look."]),

 Q("According to the author, people are most likely to mistake a correlation for a cause when:",
   ["the correlation is obviously absurd", "the data come from many countries",
    "the numbers are very large", "a plausible causal explanation is readily available"], "D",
   "&lsquo;The danger lies in the cases where a causal story is ready to hand.&rsquo; Absurd examples deceive "
   "few, because their absurdity is on the surface.", "kinds"),

 Q("The example of breakfast and school performance is used to show that:",
   ["breakfast has no effect on learning", "schools should provide meals",
    "other differences between households may explain the association",
    "children who skip breakfast are punished"], "C",
   "The author points to income, routine and adults' time as things that differ between the two kinds of "
   "household and &lsquo;might do the work that we have credited to the meal&rsquo;. The author does not say the meal "
   "has no effect.", "kinds"),

 Q("The statement that the commonplace is &lsquo;repeated more often than it is used&rsquo; means that people:",
   ["say it readily but seldom apply it in their own reasoning", "do not know it", "disagree with it",
    "use it too strictly"], "A",
   "To repeat a maxim is easy; to use it is to check one's own favourite explanations. The author's point is "
   "that the second is rarer than the first.", "kinds"),

 Q("What does the author recommend?",
   ["Giving up the search for causes", "Testing an explanation by working out its other consequences and "
    "checking them", "Trusting explanations that seem natural", "Collecting no further data"], "B",
   "&lsquo;To ask, of every pleasing explanation, what else would have to be true if it were right, and then "
   "to go and look.&rsquo; Giving up the search &lsquo;would be to stop thinking&rsquo;.", "kinds"),

 Q("The tone of the passage is best described as:",
   ["cautionary and reasoned", "angry", "humorous throughout", "despairing"], "A",
   "The author warns against a common error and offers a remedy, in a measured way. The light examples at the "
   "start serve the argument; the passage is neither comic throughout nor angry or hopeless.", "kinds"),

 P(8, ["Antibiotics are unlike other medicines in one respect that is easy to state and hard to take in: "
       "every use of them makes them a little less useful to everyone. A tablet for blood pressure works as "
       "well on its millionth patient as on its first. An antibiotic, each time it is used, kills the "
       "susceptible bacteria and spares the few that happen to resist it, and it is those few that multiply. "
       "Used carelessly, for colds that it cannot cure or in courses abandoned half-way, it hastens the day "
       "when it will cure nothing.",
       "This makes the effectiveness of antibiotics a common resource, like a pasture or a fishing ground, "
       "and it shares their weakness. The benefit of each use goes to one patient; the cost is spread, thinly "
       "and invisibly, over all. No individual has a reason to hold back. Only rules made in common, and "
       "kept, can protect what no one owns and everyone needs."]),

 Q("In what respect, according to the passage, do antibiotics differ from a medicine for blood pressure?",
   ["They are more expensive", "Each use of them reduces their future usefulness for everyone",
    "They act more slowly", "They have more side effects"], "B",
   "&lsquo;Every use of them makes them a little less useful to everyone&rsquo;, whereas the blood-pressure "
   "tablet &lsquo;works as well on its millionth patient as on its first&rsquo;.", "kinds"),

 Q("Resistance spreads, according to the passage, because an antibiotic:",
   ["strengthens every bacterium it touches", "is usually given in too small a dose",
    "kills susceptible bacteria and leaves the resistant ones to multiply", "is destroyed by the body"], "C",
   "The drug &lsquo;kills the susceptible bacteria and spares the few that happen to resist it, and it is "
   "those few that multiply&rsquo;: selection, not strengthening.", "kinds"),

 Q("The comparison with a pasture or a fishing ground is made to show that:",
   ["antibiotics are used in farming", "bacteria live in fields and water",
    "antibiotics should be free of cost",
    "the effectiveness of antibiotics is a shared resource that each user has reason to over-use"], "D",
   "As with a common pasture, the gain from each use is private and the cost is spread over all, so &lsquo;no "
   "individual has a reason to hold back&rsquo;.", "kinds"),

 Q("Which of the following is given in the passage as a careless use of antibiotics?",
   ["Taking them for colds, which they cannot cure", "Taking them with food",
    "Taking them only on a doctor's advice", "Storing them in a cool place"], "A",
   "The passage names two careless uses: &lsquo;for colds that it cannot cure&rsquo; and &lsquo;in courses "
   "abandoned half-way&rsquo;.", "kinds"),

 Q("The solution proposed by the author is:",
   ["leaving the decision to each patient", "inventing new antibiotics every year",
    "collective rules that are actually observed", "banning antibiotics"], "C",
   "&lsquo;Only rules made in common, and kept, can protect what no one owns and everyone needs.&rsquo; "
   "Individual choice is exactly what fails with a common resource.", "kinds"),

 P(9, ["When the question is asked why some regions grew rich in handicrafts and others did not, the "
       "answers given are usually about skill or enterprise. A humbler answer deserves a hearing: roads. A "
       "weaver's cloth is worth what it will fetch in the market he can reach. Where a cart could travel in "
       "all seasons, a village could specialise, sell what it made best and buy the rest; where the monsoon "
       "closed the track for four months, every household had to grow its own food and make its own goods, "
       "and did both badly.",
       "Specialisation, in other words, is not a habit of mind that some peoples have and others lack. It is "
       "a response to the size of the market, and the size of the market is set by the cost of carrying "
       "things. The historian who wishes to explain skill would do well to begin by looking at a map."]),

 Q("The passage explains differences in the growth of handicrafts mainly by differences in:",
   ["the natural talent of the people", "the fertility of the soil", "religious beliefs",
    "transport and access to markets"], "D",
   "The &lsquo;humbler answer&rsquo; is roads: the market a producer can reach, set by the cost of carrying "
   "goods, determines whether a village can specialise.", "kinds"),

 Q("According to the passage, a village cut off for four months in the monsoon:",
   ["had to produce everything for itself, and did so inefficiently", "specialised in weaving",
    "grew rich by trade", "imported its food"], "A",
   "&lsquo;Every household had to grow its own food and make its own goods, and did both badly.&rsquo;", "kinds"),

 Q("&lsquo;A response to the size of the market&rsquo; means that people specialise:",
   ["because they are naturally enterprising", "when they can sell to enough buyers to make it worthwhile",
    "only when the government orders it", "when markets are small"], "B",
   "Specialisation pays only if what one makes can be sold widely and the rest bought. It follows the extent "
   "of the market; it is not an inborn habit.", "kinds"),

 Q("The advice to &lsquo;begin by looking at a map&rsquo; implies that:",
   ["historians cannot read documents", "geography and communications help to explain economic differences",
    "maps are more accurate than records", "skill cannot be explained"], "B",
   "A map shows roads, rivers and distances, which fix the cost of carriage and so the size of markets: the "
   "author's proposed explanation of where skill developed.", "kinds"),

 Q("Which of the following views does the author reject?",
   ["That the cost of transport affects the size of the market",
    "That a weaver's cloth is worth what it fetches in the market he can reach",
    "That specialisation is a habit of mind which some peoples possess and others lack",
    "That all-season roads allowed villages to specialise"], "C",
   "The second paragraph begins by denying exactly this. The other three are the author's own statements.", "eliminate"),

 P(10, ["A university library used to be judged by the number of its volumes, and the habit of counting "
        "dies hard. Yet the reader who walks in today does not lack material; she is drowning in it. A "
        "search that once returned a shelf now returns a hundred thousand records, ordered by a rule she "
        "cannot see. What she needs is not more but less: a way of telling the article that has been checked "
        "from the one that merely looks like it, the data set that is documented from the one that is "
        "orphaned, the journal that reviews from the journal that only charges.",
        "The librarian who can teach this is doing something older than the catalogue and more durable than "
        "any database. Collections age, formats die, subscriptions lapse. The ability to judge a source, once "
        "learnt, goes with the reader for life, and it is the one holding of a library that cannot be "
        "cancelled when the budget is cut."]),

 Q("The main contention of the passage is that a library's most important contribution today is:",
   ["owning the largest number of volumes", "teaching readers to judge the quality of sources",
    "subscribing to more databases", "preserving old formats"], "B",
   "The reader needs &lsquo;not more but less&rsquo;: the ability to tell reliable sources from unreliable "
   "ones, which the passage calls the library's most durable holding.", "kinds"),

 Q("&lsquo;She is drowning in it&rsquo; conveys that the reader:",
   ["has too little material", "cannot enter the library", "dislikes reading",
    "is overwhelmed by the quantity of material available"], "D",
   "The metaphor is of excess: a search returns &lsquo;a hundred thousand records&rsquo;. The problem is "
   "abundance, not scarcity.", "kinds"),

 Q("&lsquo;The journal that only charges&rsquo; refers to a journal that:",
   ["takes a fee for publishing without genuinely reviewing the work", "is sold at a high price",
    "pays its authors", "is published by a university"], "A",
   "It is set against &lsquo;the journal that reviews&rsquo;: a journal that collects fees but does not carry "
   "out real peer review.", "kinds"),

 Q("Which of the following is NOT stated or implied in the passage?",
   ["Search results are ordered by rules the reader cannot see", "Library budgets may be cut",
    "Printed books will soon disappear altogether", "The skill of judging sources lasts a lifetime"], "C",
   "The passage says that collections age and formats die, but nowhere that printed books will vanish. The "
   "other three are stated: the unseen ordering rule, budget cuts, and a skill that &lsquo;goes with the "
   "reader for life&rsquo;.", "eliminate"),

 Q("&lsquo;The one holding of a library that cannot be cancelled&rsquo; is:",
   ["its oldest manuscript", "its building", "the reader's learnt ability to judge sources", "its catalogue"], "C",
   "A &lsquo;holding&rsquo; is normally an item in a collection; the author uses the word figuratively for "
   "the skill the library has given its readers, which no budget cut can take back.", "kinds"),
]
