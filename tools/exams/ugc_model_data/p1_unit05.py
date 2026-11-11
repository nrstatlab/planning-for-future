# -*- coding: utf-8 -*-
"""UGC NET Paper I, Unit 5: fifty exam-standard model questions."""
from . import AR, Q, ar, match, st

TITLE = "Mathematical Reasoning and Aptitude"
BLURB = ("Types of reasoning, number and letter series, codes and relationships, and mathematical aptitude: "
         "fractions, time and distance, ratio, proportion and percentage, profit and loss, interest and "
         "discounting, and averages.")

QUESTIONS = [
 Q("Match the type of reasoning in List I with the example in List II."
   + match(["Deductive", "Inductive", "Abductive", "Analogical"],
           ["The grass is wet this morning, so it probably rained in the night",
            "A drug that lowers blood pressure in rats may do so in humans",
            "All metals conduct electricity; copper is a metal; so copper conducts electricity",
            "Every crow seen so far is black, so all crows are black"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)",
    "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "B",
   "Deduction goes from general premises to a particular conclusion; induction from particular observations "
   "to a general statement; abduction from an observation to its most likely explanation; analogy from a "
   "likeness between two cases.", "reasoning"),

 Q("A proof that the sum of the first $n$ odd numbers is $n^2$ shows that it holds for $n=1$ and that, if it "
   "holds for $n$, it holds for $n+1$. The reasoning used is:",
   ["inductive, and the conclusion is only probable", "abductive", "analogical",
    "deductive, and the conclusion is certain"], "D",
   "Mathematical induction, despite its name, is a deductive method of proof: given the two steps, the "
   "conclusion follows with certainty for every $n$.", "reasoning"),

 Q("&ldquo;In a survey of 1,000 voters, 54% favoured the proposal; therefore about 54% of all voters favour "
   "it.&rdquo; This is an example of:",
   ["inductive (statistical) reasoning", "deductive reasoning", "analogical reasoning", "circular reasoning"], "A",
   "The argument goes from a sample to the population. Its conclusion is probable, not certain, and carries a "
   "margin of error: statistical reasoning is inductive.", "reasoning"),

 Q("A doctor notes a patient's fever, rash and recent travel and concludes that the most likely explanation "
   "is a particular infection, to be confirmed by a test. The reasoning is:",
   ["deductive", "inductive generalisation", "abductive", "analogical"], "C",
   "Abduction (C. S. Peirce's term) is inference to the best explanation: it yields a plausible hypothesis "
   "that has still to be tested.", "reasoning"),

 Q("Consider the statements:"
   + st("The conclusion of a valid deductive argument with true premises is certain.",
        "The conclusion of an inductive argument becomes certain when enough cases have been observed.",
        "The conclusion of an argument from analogy is probable.",
        "Statistical reasoning from a sample to a population is inductive.")
   + "Which of the statements are correct?",
   ["I and II only", "I, III and IV only", "II, III and IV only", "I, II, III and IV"], "B",
   "More cases make an inductive conclusion stronger but never certain; a single contrary case can overturn "
   "it. So (II) is false and the other three are correct.", "reasoning"),

 Q(ar("The conclusion of an inductive argument is only probable.",
      "The conclusion of an inductive argument goes beyond what is contained in its premises."),
   AR, "A",
   "The premises report the cases observed; the conclusion speaks of all cases, including those not observed. "
   "Because it says more than the premises, they cannot guarantee it. Both statements are true and (R) is the "
   "reason.", "reasoning"),

 Q("Find the next term of the series: 4, 9, 19, 39, 79, ?",
   ["119", "149", "158", "159"], "D",
   r"Each term is twice the previous term plus one: $4\times2+1=9$, $9\times2+1=19$, and so on. "
   r"$79\times2+1=159$. (The differences 5, 10, 20, 40 double each time, so the next difference is 80.)", "series"),

 Q("Find the next term of the series: 2, 5, 10, 17, 26, ?",
   ["35", "36", "37", "39"], "C",
   r"The terms are $n^2+1$: $1+1$, $4+1$, $9+1$, $16+1$, $25+1$, so the next is $36+1=37$. Equivalently the "
   r"differences are $3,5,7,9$ and the next difference is 11.", "series"),

 Q("Find the next term of the series: 2, 3, 5, 8, 13, 21, ?",
   ["34", "29", "32", "42"], "A",
   r"Each term is the sum of the two before it ($2+3=5$, $3+5=8$, $5+8=13$, $8+13=21$), so the next term is "
   r"$13+21=34$.", "series"),

 Q("Find the next term of the series: 3, 6, 18, 72, 360, ?",
   ["1440", "2160", "1800", "720"], "B",
   r"The multipliers increase by one each time: $\times2,\times3,\times4,\times5$, so the next is "
   r"$360\times6=2160$.", "series"),

 Q("Find the next term of the series: 5, 20, 7, 18, 9, 16, 11, ?",
   ["13", "12", "15", "14"], "D",
   "Two series are interleaved. The terms in odd places are 5, 7, 9, 11 (rising by 2); those in even places "
   "are 20, 18, 16 (falling by 2), so the next is 14.", "series"),

 Q("Which term is wrong in the series: 2, 6, 12, 20, 30, 44, 56?",
   ["20", "30", "44", "56"], "C",
   r"The terms should be $n(n+1)$: $1\times2,\ 2\times3,\ 3\times4,\ 4\times5,\ 5\times6,\ 6\times7=42,\ "
   r"7\times8=56$. So 44 is wrong and should be 42. (The differences should run 4, 6, 8, 10, 12, 14.)", "series"),

 Q("Find the next term of the series: 0, 7, 26, 63, 124, ?",
   ["215", "216", "195", "217"], "A",
   r"The terms are $n^3-1$: $1-1,\ 8-1,\ 27-1,\ 64-1,\ 125-1$, so the next is $216-1=215$.", "series"),

 Q("Find the next term of the series: 4, 9, 25, 49, 121, ?",
   ["144", "169", "196", "225"], "B",
   r"The terms are the squares of the successive primes 2, 3, 5, 7, 11. The next prime is 13 and "
   r"$13^2=169$. (144 is $12^2$, but 12 is not prime.)", "series"),

 Q("Find the next term of the letter series: A, C, F, J, O, ?",
   ["S", "T", "V", "U"], "D",
   "The positions are 1, 3, 6, 10, 15: the steps are +2, +3, +4, +5, so the next step is +6, giving 21, "
   "which is U.", "series"),

 Q("Find the next term of the series: AZ, CX, EV, GT, ?",
   ["IR", "HS", "IQ", "JR"], "A",
   "The first letters go forward two places at a time (A, C, E, G, I); the second letters go back two places "
   "at a time (Z, X, V, T, R). The next pair is IR.", "series"),

 Q("Find the next term of the series: B2, D4, G7, K11, ?",
   ["O15", "P15", "P16", "Q17"], "C",
   "The number is the position of the letter in the alphabet. The positions 2, 4, 7, 11 rise by 2, 3, 4, so "
   "the next rise is 5: position 16, the letter P. The term is P16.", "series"),

 Q("Find the next term of the letter series: Z, W, S, N, ?",
   ["I", "H", "J", "G"], "B",
   "The positions are 26, 23, 19, 14: the steps are $-3,-4,-5$, so the next step is $-6$, giving position 8, "
   "the letter H.", "series"),

 Q("In a certain code MIND is written as NJOE. In the same code BOOK is written as:",
   ["ANNJ", "CPPK", "CQQL", "CPPL"], "D",
   "Each letter is moved one place forward: M to N, I to J, N to O, D to E. So B, O, O, K become C, P, P, L.", "codes"),

 Q("In a certain code RAT is written as IZG. In the same code DOG is written as:",
   ["WLT", "WMT", "VLT", "XLS"], "A",
   "Each letter is replaced by the letter in the same position counted from the end of the alphabet "
   "(position $p$ becomes $27-p$): R (18) to I (9), A to Z, T (20) to G (7). So D (4) becomes W (23), O (15) "
   "becomes L (12) and G (7) becomes T (20).", "codes"),

 Q("If each letter stands for its position in the alphabet and a word is coded by the sum of these numbers, "
   "so that BAD is coded as 7, then FACE is coded as:",
   ["14", "16", "15", "21"], "C",
   r"Check the rule on the given word: B, A, D are in positions 2, 1 and 4, and $2+1+4=7$. F, A, C, E are in "
   r"positions 6, 1, 3 and 5, and $6+1+3+5=15$.", "codes"),

 Q("In a code language &lsquo;sky is blue&rsquo; is written as &lsquo;4 7 2&rsquo;, &lsquo;blue and "
   "green&rsquo; as &lsquo;2 9 5&rsquo; and &lsquo;green is good&rsquo; as &lsquo;5 7 1&rsquo;. The code for "
   "&lsquo;sky&rsquo; is:",
   ["7", "4", "2", "9"], "B",
   "&lsquo;blue&rsquo; is common to the first two sentences, and so is 2: blue is 2. &lsquo;is&rsquo; is "
   "common to the first and third, and so is 7: is is 7. The remaining code in the first sentence, 4, stands "
   "for &lsquo;sky&rsquo;.", "codes"),

 Q("If + means &times;, &minus; means &divide;, &times; means &minus; and &divide; means +, then the value "
   "of 8 + 6 &minus; 3 &times; 4 &divide; 2 is:",
   ["18", "12", "10", "14"], "D",
   r"Replacing the signs: $8\times6\div3-4+2$. Multiplication and division first, from the left: "
   r"$48\div3=16$. Then $16-4+2=14$.", "codes"),

 Q("Pointing to a girl, Ravi says, &ldquo;Her mother is the only daughter of my mother.&rdquo; The girl is "
   "Ravi's:",
   ["niece", "sister", "daughter", "cousin"], "A",
   "The only daughter of Ravi's mother is Ravi's sister. The girl is the daughter of Ravi's sister, that is, "
   "his niece.", "codes"),

 Q("A is the brother of B. B is the sister of C. C is the father of D. How is A related to D?",
   ["Father", "Grandfather", "Uncle", "Brother"], "C",
   "A, B and C are brothers and sisters. C is D's father, so A, a brother of D's father, is D's uncle.", "codes"),

 Q("X is the wife of Y. Y is the brother of Z. Z is the daughter of W, who is a man. How is X related to W?",
   ["Daughter", "Daughter-in-law", "Sister", "Niece"], "B",
   "Z is W's daughter and Y is Z's brother, so Y is W's son. X, the wife of W's son, is W's "
   "daughter-in-law.", "codes"),

 Q("A man walks 10 km towards the south, turns left and walks 6 km, then turns left again and walks 2 km. "
   "How far, and in which direction, is he from the starting point?",
   ["8 km, south", "14 km, south-east", "10 km, south-west", "10 km, south-east"], "D",
   r"Facing south, a left turn faces east; facing east, a left turn faces north. Net movement: $10-2=8$ km "
   r"south and 6 km east. Distance $=\sqrt{8^2+6^2}=10$ km, to the south-east of the start.", "codes"),

 Q("A person facing north turns 90&deg; clockwise, then 180&deg;, and then 90&deg; anticlockwise. The person "
   "is now facing:",
   ["south", "north", "east", "west"], "A",
   "North, 90&deg; clockwise: east. A turn of 180&deg;: west. From west, 90&deg; anticlockwise: south.", "codes"),

 Q("One morning just after sunrise a man standing in an open field finds that his shadow falls exactly to "
   "his right. He is facing:",
   ["north", "east", "south", "west"], "C",
   "In the morning the sun is in the east, so shadows fall towards the west. If west is to his right, he is "
   "facing south (facing south, the right hand points west).", "codes"),

 Q("In a row of 40 students, a student is 15th from the left end. The student's position from the right "
   "end is:",
   ["25th", "26th", "24th", "27th"], "B",
   r"Position from the other end $=$ total $-$ position $+1=40-15+1=26$. There are 25 students to the right, "
   r"so the student is 26th from that end.", "codes"),

 Q(r"The fractions $\dfrac35,\ \dfrac58,\ \dfrac{7}{11},\ \dfrac23$ arranged in ascending order are:",
   [r"$\dfrac58,\ \dfrac35,\ \dfrac{7}{11},\ \dfrac23$", r"$\dfrac35,\ \dfrac{7}{11},\ \dfrac58,\ \dfrac23$",
    r"$\dfrac23,\ \dfrac{7}{11},\ \dfrac58,\ \dfrac35$", r"$\dfrac35,\ \dfrac58,\ \dfrac{7}{11},\ \dfrac23$"], "D",
   r"As decimals: $\tfrac35=0.600$, $\tfrac58=0.625$, $\tfrac7{11}=0.636$, $\tfrac23=0.667$. So the ascending "
   r"order is $\tfrac35,\tfrac58,\tfrac7{11},\tfrac23$.", "aptitude"),

 Q("A train 200 m long, running at 90 km/h, crosses a bridge 300 m long in:",
   ["20 seconds", "12 seconds", "8 seconds", "25 seconds"], "A",
   r"$90$ km/h $=90\times\tfrac{5}{18}=25$ m/s. To cross the bridge the train covers its own length plus the "
   r"bridge: $200+300=500$ m, in $\tfrac{500}{25}=20$ seconds.", "aptitude"),

 Q("A cyclist goes from A to B at 30 km/h and returns over the same road at 60 km/h. The average speed for "
   "the whole journey is:",
   ["45 km/h", "50 km/h", "40 km/h", "42 km/h"], "C",
   r"For two equal distances at speeds $x$ and $y$, the average speed is "
   r"$\dfrac{2xy}{x+y}=\dfrac{2\times30\times60}{90}=40$ km/h. More time is spent at the lower speed, so the "
   r"average is below 45.", "aptitude"),

 Q("Two trains, 120 m and 180 m long, run towards each other on parallel tracks at 54 km/h and 36 km/h. The "
   "time they take to pass each other completely is:",
   ["60 seconds", "12 seconds", "30 seconds", "10 seconds"], "B",
   r"Moving towards each other, the speeds add: $54+36=90$ km/h $=25$ m/s. They must cover the sum of their "
   r"lengths, $300$ m, in $\tfrac{300}{25}=12$ seconds.", "aptitude"),

 Q("If A : B = 3 : 4 and B : C = 6 : 7, then A : B : C is:",
   ["3 : 4 : 7", "18 : 24 : 21", "9 : 12 : 16", "9 : 12 : 14"], "D",
   r"Make B the same in both ratios: its values 4 and 6 have least common multiple 12. $A:B=9:12$ and "
   r"$B:C=12:14$, so $A:B:C=9:12:14$.", "aptitude"),

 Q("The price of an article is raised by 25% and the new price is then reduced by 20%. The net change in "
   "the price is:",
   ["no change", "a rise of 5%", "a fall of 5%", "a rise of 1%"], "A",
   r"Successive changes of $a\%$ and $b\%$ give $a+b+\dfrac{ab}{100}=25-20-\dfrac{500}{100}=0$. Directly: "
   r"$1.25\times0.80=1.00$. The 20% is taken on the larger, raised price, which is why it cancels a rise of "
   r"25%.", "aptitude"),

 Q("A's salary is 60% more than B's. By what percentage is B's salary less than A's?",
   ["60%", "40%", "37.5%", "62.5%"], "C",
   r"If B earns 100, A earns 160. B is less than A by $\dfrac{60}{160}\times100=37.5\%$. The base changes "
   r"from B's salary to A's, so the percentage is not 60.", "aptitude"),

 Q("The population of a town is 20,000. It increases by 10% in the first year and by 20% in the second year. "
   "The population at the end of two years is:",
   ["26,000", "26,400", "24,200", "28,800"], "B",
   r"$20{,}000\times1.10\times1.20=26{,}400$. The second increase is on 22,000, not on 20,000, so the total "
   r"rise is 32% and not 30%.", "aptitude"),

 Q("An article costing ₹500 is marked 40% above cost and sold at a discount of 10% on the marked price. The "
   "profit percentage is:",
   ["30%", "36%", "25%", "26%"], "D",
   r"Marked price $=500\times1.4=700$, that is ₹700. Selling price $=700\times0.9=630$, that is ₹630. Profit $=$ ₹130, which is "
   r"$\dfrac{130}{500}\times100=26\%$ of the cost.", "aptitude"),

 Q("The selling price of 12 articles is equal to the cost price of 15 articles. The profit percentage is:",
   ["25%", "20%", "15%", "30%"], "A",
   r"$12\times SP=15\times CP$, so $\dfrac{SP}{CP}=\dfrac{15}{12}=1.25$: a profit of 25% on cost.", "aptitude"),

 Q("An article is sold at a loss of 10%. Had it been sold for ₹60 more, there would have been a gain of 5%. "
   "The cost price is:",
   ["₹600", "₹450", "₹400", "₹360"], "C",
   r"The difference between a 10% loss and a 5% gain is 15% of the cost price, and this is ₹60. So the cost "
   r"price is $\dfrac{60}{0.15}=400$, that is ₹400.", "aptitude"),

 Q("At what rate of simple interest per annum will a sum of money double itself in 8 years?",
   ["8%", "12.5%", "10%", "16%"], "B",
   r"To double, the interest must equal the principal: $\dfrac{P\times R\times8}{100}=P$, so "
   r"$R=\dfrac{100}{8}=12.5\%$.", "aptitude"),

 Q("The difference between the compound interest and the simple interest on ₹12,000 for 2 years at 5% per "
   "annum is:",
   ["₹60", "₹15", "₹120", "₹30"], "D",
   r"For two years, $CI-SI=P\left(\dfrac{R}{100}\right)^2=12{,}000\times(0.05)^2=30$, that is ₹30. Check: simple interest "
   r"is ₹1,200; compound interest is $12{,}000(1.05^2-1)=1{,}230$, that is ₹1,230.", "aptitude"),

 Q("The compound interest on ₹5,000 for 3 years at 10% per annum, compounded annually, is:",
   ["₹1,655", "₹1,500", "₹1,600", "₹6,655"], "A",
   r"Amount $=5{,}000\times(1.1)^3=5{,}000\times1.331=6{,}655$, that is ₹6,655, so the compound interest is "
   r"$6{,}655-5{,}000=1{,}655$, that is ₹1,655. ₹1,500 is the simple interest.", "aptitude"),

 Q("The present value of ₹12,100 due two years hence, at 10% per annum compound interest, and the true "
   "discount are, respectively:",
   ["₹10,083 and ₹2,017", "₹9,680 and ₹2,420", "₹10,000 and ₹2,100", "₹11,000 and ₹1,100"], "C",
   r"Present value $=\dfrac{12{,}100}{(1.1)^2}=\dfrac{12{,}100}{1.21}=10{,}000$, that is ₹10,000. The true discount is the "
   r"amount less its present value: ₹2,100.", "aptitude"),

 Q("The average of 10 numbers is 15. Later it is found that one number, 14, was wrongly read as 24. The "
   "correct average is:",
   ["16", "14", "14.5", "13"], "B",
   r"The sum taken was $10\times15=150$. The correct sum is $150-24+14=140$, and the correct average is 14.", "aptitude"),

 Q("In a class, 40 students have an average of 50 marks and the other 60 students have an average of 60 "
   "marks. The average for the whole class is:",
   ["55", "54", "58", "56"], "D",
   r"Weighted average $=\dfrac{40\times50+60\times60}{100}=\dfrac{2{,}000+3{,}600}{100}=56$. It is nearer 60 "
   r"because the second group is larger.", "aptitude"),

 Q("The average age of the 5 members of a family is 30 years. A child aged 6 years joins the family. The "
   "new average age is:",
   ["26 years", "24 years", "25 years", "28 years"], "A",
   r"Total age $=5\times30=150$ years. With the child it is 156 years for 6 members: an average of 26 years.", "aptitude"),

 Q("The fourth proportional to 4, 6 and 10 is:",
   ["12", "20", "15", "24"], "C",
   r"The fourth proportional to $a$, $b$, $c$ is the number $x$ for which $a:b=c:x$. If $4:6=10:x$, then the "
   r"product of the extremes equals the product of the means: $4x=60$ and $x=15$.", "aptitude"),

 Q("The pass mark in an examination is 35% of the maximum. A candidate who scores 120 marks fails by 20 "
   "marks. The maximum marks are:",
   ["350", "400", "500", "450"], "B",
   r"The pass mark is $120+20=140$, which is 35% of the maximum. Maximum $=\dfrac{140}{0.35}=400$.", "aptitude"),
]
