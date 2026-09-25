# -*- coding: utf-8 -*-
"""The words of the APPSC 2022 Paper-II ("ECOSTATS 0411S2"), transcribed.

In this PDF every question and every option is a picture (English over
Telugu), and the text layer holds only headers and option IDs, so the
English here was typed from the pictures, question by question. Nothing
else about the paper is typed: its numbering, option IDs, withdrawn
questions and key come from the PDF itself, through pdftext_appsc_2022.py
into appsc_paper_2022.json. recheck_appsc_2022.py holds these words to an
OCR reading of the same pictures.

The transcription is kept in the form it was typed in, one line per line of
the paper:

    Qn     a question
    S:     a line of its stem
    L:     a bulleted line of its stem
    T:     a row of a table in the stem, cells separated by " | "
    O:     an option
    OL:    a further line of the option above
    OT:    an option that is a table: rows separated by " // ", cells by " | "

Mathematics is in $...$; the paper's own spelling and punctuation are kept.
"""
import re

TRANSCRIPTION = r"""
Q1
S: “Production is the outcome of the combined activity of the four factors of production”.
S: With reference to the above statement, which of the following is/are NOT considered as factors of production?
S: (i) Land
S: (ii) Labour
S: (iii) Capital
S: (iv) Organisation
S: (v) Service
O: (i) only
O: (ii) only
O: (i), (ii) and (iii) only
O: (v) only
Q2
S: Two goods X and Y are said to be ______ if the price of good X is inversely related to the demand of good Y.
O: substitutes
O: complementary
O: Giffen goods
O: necessities
Q3
S: Which of the following statements are true/false?
S: (i) Inferior goods have positive income effect.
S: (ii) Inferior goods have negative income effect.
O: Both statements (i) and (ii) are true
O: Statement (i) is true and statement (ii) is false
O: Both statements (i) and (ii) are false
O: Statement (i) is false and statement (ii) is true
Q4
S: Which of the following statements is FALSE regarding degree of price elasticity of demand?
O: Perfectly Elastic Demand: ($E_d = 1$)
O: Perfectly Inelastic Demand: ($E_d = 0$)
O: Less than Unit Elastic: ($E_d < 1$)
O: More than Unit Elastic: ($E_d > 1$)
Q5
S: A ______ competition is a market situation, in which many firms compete with each other to sell their closely-related differentiated products.
O: perfect
O: monopoly
O: monopolistic
O: oligopoly
Q6
S: If the nominal GDP = ₹18,000 crores and the real GDP = ₹12,000 crores, calculate the GDP deflator.
O: 0.66 or 66%
O: 1.5 or 150%
O: 1 or 100%
O: 0.60 or 60%
Q7
S: Which of the following is NOT a method of measurement of National Income?
O: Value Added Method
O: Income Method
O: Expenditure Method
O: Cost Accounting Method
Q8
S: If the disposable income is ₹100 and consumption expenditure is ₹80, calculate the Average Propensity to Save (APS)?
O: 20%
O: 30%
O: 40%
O: 10%
Q9
S: The part of investment (increase or decrease) which takes place due to a change in the level of national income is termed as ______.
O: gross investment
O: net investment
O: induced investment
O: autonomous investment
Q10
S: Which of the following statements are correct/incorrect regarding items excluded from money supply of a country?
S: (i) The cash held by commercial banks is included in money supply.
S: (ii) The stock of monetary gold held in reserves as a backing to paper currency is included in money supply.
O: Both statements (i) and (ii) are incorrect.
O: Both statements (i) and (ii) are correct.
O: Statement (i) is correct and statement (ii) is incorrect.
O: Statement (i) is incorrect and statement (ii) is correct.
Q11
S: Which of the following is/are considered as primary function(s) of money?
S: (i) Medium of exchange
S: (ii) Measure of value
S: (iii) Store of value
S: (iv) Transfer of value
O: (i) only
O: (i) and (ii) only
O: (i), (ii), (iii) and (iv)
O: (i), (ii) and (iii) only
Q12
S: Which of the following are correct regarding measures of money supply?
S: (i) $M_1$ = Currency-notes and coins with the public (excluding cash in hand of all commercial banks) + Demand deposits (excluding inter-bank deposits) of all commercial banks and cooperative banks + Other deposits held with the RBI
S: (ii) $M_2$ = $M_1$ + Savings deposits with post office savings banks
S: (iii) $M_3$ = $M_2$ + Time deposits of all cooperative banks only
S: (iv) $M_4$ = $M_3$ + Total deposits with the post office savings banks excluding National Savings Certificates.
O: (i), (ii) and (iv) only
O: (i), (ii) and (iii) only
O: (iii) and (iv) only
O: (i), (ii), (iii) and (iv)
Q13
S: Compute credit multiplier and total credit money created by the banking system, if the required reserve ratio is 10% for every ₹1,00,000 deposited in the banking system.
O: 10 and ₹10,00,000
O: 10 and ₹1,00,000
O: 0 and ₹10,00,000
O: 10 and ₹1,00,00,000
Q14
S: Which of the following is correct with regard to Reserve Money?
O: Reserve Money = Currency in circulation + Bankers’ deposits with RBI + Other deposits with RBI
O: Reserve Money = Currency in circulation + Bankers’ deposits with RBI + Other deposits with SBI
O: Reserve Money = Bankers’ deposits with RBI + Other deposits with RBI
O: Reserve Money = Currency in circulation + Bankers’ deposits with RBI
Q15
S: Calculate narrow money ($M_1$) from the following data.
T: Particulars | In ₹ crores
T: Currency with public | 90,000
T: Demand deposits with banking system | 2,00,000
T: Time deposits with banking system | 2,20,000
T: Other deposits with RBI | 2,80,000
T: Saving deposits of post office saving banks | 60,000
O: ₹5,70,000 crores
O: ₹5,00,000 crores
O: ₹8,50,000 crores
O: ₹8,00,000 crores
Q16
S: Which of the following statements are true/false?
S: (i) A government budget is an annual statement showing item wise estimates of receipts and expenditures during a fiscal year.
S: (ii) James Wilson presented India’s first budget on 18 February 1880.
O: Statement (i) is true and statement (ii) is false
O: Both statements (i) and (ii) are true
O: Both statements (i) and (ii) are false
O: Statement (i) is false and statement (ii) is true
Q17
S: Which of the following transactions will be added when the starting point is debit, i.e. favourable balance as per cash book.
O: Cheques issued but not presented for payment
O: Cheques deposited but not collected or credited by the bank
O: Cheques deposited but dishonoured
O: Cheques recorded but not deposited
Q18
S: Which of the following is/are considered as source(s) of non-tax revenue of the central government?
S: (i) Interest received on loans given by the government to the state.
S: (ii) Profits or dividends received by public enterprises like BHEL, LIC etc.
S: (iii) Grants or donations received by the government from international organizations.
O: (i), (ii) and (iii)
O: (ii) and (iii) only
O: (i) and (iii) only
O: (i) only
Q19
S: Calculate budget deficit from the following data:
T: Items | In ₹ crores
T: Revenue receipts | 40,000
T: Revenue expenditure | 30,000
T: Capital receipts | 30,000
T: Capital expenditure | 50,000
O: ₹50,000 crores
O: ₹30,000 crores
O: ₹10,000 crores
O: Nil
Q20
S: Which of the following statements is FALSE?
O: Exchange rate is the rate at which the currency of one country exchanges for the currency of another country.
O: A direct quote is the number of units of a foreign currency exchangeable for one unit of home currency.
O: An exchange rate regime is the system by which a country manages its currency with respect to foreign currencies.
O: There are two major types of exchange rate regimes: floating exchange rate and fixed exchange rate.
Q21
S: The balance of trade surplus of a country is ₹800 crores. If the value of imports is ₹9,000 crores, find the value of exports.
O: ₹9,800 crores
O: ₹9,000 crores
O: ₹8,900 crores
O: ₹8,200 crores
Q22
S: Which of the following statements are true/false?
S: (i) The balance of payment of a country is a systematic record of all economic transactions between the residents of a country and rest of the world, during a year.
S: (ii) The current account records exports and imports of goods and services and unilateral transfers.
O: Both statements (i) and (ii) are true
O: Statement (i) is false and statement (ii) is true
O: Statement (i) is true and statement (ii) is false
O: Both statements (i) and (ii) are false
Q23
S: The ______ account includes all international economic transactions with income or payment flows occurring within the current year and the ______ account is made up of transfers of financial assets and the acquisition and disposal of non-produced or non-financial assets.
O: current; capital
O: capital; capital
O: current; current
O: capital; current
Q24
S: The International Monetary Fund was established in ______ at the Bretton Woods Conference.
O: 1945
O: 1944
O: 1940
O: 1947
Q25
S: The World Bank Group includes which of the following?
S: (i) International Bank for Reconstruction and Development (IBRD)
S: (ii) International Development Association (IDA)
S: (iii) International Finance Corporation (IFC)
S: (iv) Multilateral Investment Guarantee Agency (MIGA)
S: (v) International Centre for Settlement of Investment Disputes (ICSID)
O: (i) and (ii) only
O: (i), (ii) and (iii) only
O: (i), (ii), (iii) and (iv) only
O: (i), (ii), (iii), (iv) and (v)
Q26
S: Which of the following institutions was renamed as the World Bank?
O: International Bank for Reconstruction and Development
O: International Development Association
O: International Finance Corporation
O: Multilateral Investment Guarantee Agency
Q27
S: Which of the following statements are true/false regarding trade?
S: (i) Internal trade refers to buying and selling of goods and services within the boundaries of a nation.
S: (ii) The buying and selling of goods and services in large quantities for the purpose of resale or intermediate use is known as wholesale trade.
O: Both statements (i) and (ii) are true
O: Statement (i) is false and statement (ii) is true
O: Both statements (i) and (ii) are false
O: Statement (i) is true and statement (ii) is false
Q28
S: The stock of skill, ability, expertise, education and knowledge embodied in the people of a country is called ______.
O: capital
O: human capital
O: human capital formation
O: financial capital
Q29
S: Convert $(0.25)_{10}$ to binary.
O: $(0.01)_2$
O: $(0.10)_2$
O: $(1.01)_2$
O: $(0.25)_1$
Q30
S: ______ unemployment exists in an economy due to movement of people from one job to another and in the process, they remain unemployment for some times.
O: Visible
O: Seasonal
O: Cyclical
O: Frictional
Q31
S: Convert the following binary to decimal.
S: $(1011010)_2 = (?)_{10}$
O: $(90)_{10}$
O: $(64)_{10}$
O: $(80)_{10}$
O: $(88)_{10}$
Q32
S: Convert the following decimal to hexadecimal.
S: $(952)_{10} = (?)_{16}$
O: $(3B8)_{16}$
O: $(3A8)_{16}$
O: $(3C8)_{16}$
O: $(3D8)_{16}$
Q33
S: Convert $(705)_8$ to binary number.
O: $(111000101)_2$
O: $(11000101)_2$
O: $(110000101)_2$
O: $(111000111)_2$
Q34
S: Convert the following octal to decimal.
S: $(3047)_8 = (?)_{10}$
O: $(1575)_{10}$
O: $(1557)_{10}$
O: $(1536)_{10}$
O: $(1563)_{10}$
Q35
S: Convert $(0110101100)_2$ to hexadecimal number.
O: $(1AC)_{16}$
O: $(1BC)_{16}$
O: $(1AD)_{16}$
O: $(1DC)_{16}$
Q36
S: Which of the following options is correct?
O: A kilobyte = $2^{10}$ bytes, a megabyte = $2^{20}$ bytes, and a gigabyte = $2^{40}$ bytes
O: A kilobyte = $2^{10}$ bytes, a megabyte = $2^{20}$ bytes, and a gigabyte = $2^{30}$ bytes
O: A kilobyte = $2^{10}$ bytes, a megabyte = $2^{30}$ bytes, and a gigabyte = $2^{40}$ bytes
O: A kilobyte = $2^{20}$ bytes, a megabyte = $2^{30}$ bytes, and a gigabyte = $2^{40}$ bytes
Q37
S: Which of the following statements is/are considered as feature(s) of a spreadsheet?
S: (i) A spreadsheet is described as a grid that is structured by several rows and column.
S: (ii) Every column in a spreadsheet is identified by a number assigned sequentially as 1, 2 and 3 and so on.
S: (iii) Every row in a spreadsheet is assigned a letter or letters for identification.
O: (i) only
O: (ii) only
O: (i), (ii) and (iii)
O: (i) and (ii) only
Q38
S: Manipulation of a cell in a spreadsheet means which of the following?
S: (i) Modify or editing cell contents
S: (ii) Page layout
S: (iii) Clipboard
O: (i) only
O: (i) and (iii) only
O: (i), (ii) and (iii)
O: (i) and (ii) only
Q39
S: Which of the following statements are true/false?
S: (i) Formulas are made up of arithmetic operators such as = + − and other functions
S: (ii) A formula in Excel always has to start with =
O: Statement (i) is false and statement (ii) is true
O: Both statements (i) and (ii) are false
O: Both statements (i) and (ii) are true
O: Statement (i) is true and statement (ii) is false
Q40
S: Find the cell address of the following cells.
S: (i) $4^{\text{th}}$ row and $15^{\text{th}}$ column
S: (ii) $10^{\text{th}}$ row and $6^{\text{th}}$ column
O: O4 and F10
O: O5 and F10
O: O4 and F11
O: O43 and F10
Q41
S: Which of the following statements are FALSE?
O: The COUNTA function counts the number of cells that are empty in a range.
O: The COUNT function counts the number of cells that contain numerical value within the lists of arguments.
O: The COUNTIF function counts the number of cells within a range that meet a single criterion that you specify.
O: The DEVSQ function returns the sum of squares of deviations of data points from their sample mean.
Q42
S: Which of the following statements are true/false with regard to Excel functions?
S: (i) The AVERAGE function returns the average (arithmetic mean) of the arguments.
S: (ii) The CORREL function returns the correlation coefficient of the array1 and array2 cell ranges.
S: (iii) The MIN function returns the smallest number in a set of values.
O: All statements (i), (ii) and (iii) are true.
O: Statements (i) and (iii) are true, statement (ii) is false.
O: Statements (i) and (ii) are true, statement (iii) is false.
O: Statements (ii) and (iii) are true, statement (i) is false.
Q43
S: Which of the following statements are true/false?
S: (i) The IPMT financial function returns the interest payment for a given period based on period, constant payment and a constant interest rate.
S: (ii) The PPMT financial function returns the payment on the principal for a given period for an investment based on periodic, constant payments and a constant interest rate.
O: Statement (i) is true and statement (ii) is false
O: Both statements (i) and (ii) are true
O: Statement (i) is false and statement (ii) is true
O: Both statements (i) and (ii) are false
Q44
S: Which of the following statements are true/false?
S: (i) The SUMIF function adds all the numbers in a range of cells.
S: (ii) The OR logical function reverses the value of its argument.
O: Both statements (i) and (ii) are true
O: Statement (i) is true and statement (ii) is false
O: Both statements (i) and (ii) are false
O: Statement (i) is false and statement (ii) is true
Q45
S: As per the 2011 Census, the density of population in India is ___ persons per sq. km.
O: 382
O: 328
O: 823
O: 380
Q46
S: As per the 2011 Census, the number of males was pegged at ______ million and the population of females stood at ______ million.
O: 623.7; 586.5
O: 632.7; 586.5
O: 623.7; 568.5
O: 623.7; 486.5
Q47
S: India’s population as per the 2011 Census is:
O: 1210.2 million
O: 1201.2 million
O: 1028.2 million
O: 1008.2 million
Q48
S: ______ gave the concept of the poverty line in pre-independent India.
O: Dr. Amartya Sen
O: Dadabhai Naoroji
O: Dr. VKRV Rao
O: RC Desai
Q49
S: For the estimation of the poverty line, who among the following coined the term ‘jail cost of living’?
O: Dr. VKRV Rao
O: Mahatma Gandhi
O: Dadabhai Naoroji
O: Dr. Amartya Sen
Q50
S: ______ unemployment refers to a situation wherein more people are engaged in any economic activity than required.
O: Disguised
O: Seasonal
O: Structural
O: Cyclical
Q51
S: Which of the following statements are true/false?
S: (i) Occasionally poor are those who are rich most of the time but may sometimes have a patch of bad luck; may remain below the poverty line. They are called the usually poor.
S: (ii) Transient poor are those who regularly move in and out of poverty.
O: Both statements (i) and (ii) are true.
O: Statement (i) is false and statement (ii) is true.
O: Statement (i) is true and statement (ii) is false.
O: Both statements (i) and (ii) are false.
Q52
S: Calculate fiscal deficit from the following particulars.
T: Items | In ₹ crores
T: Estimated total expenditure of the government | 1,50,000
T: Revenue receipts of the government | 1,20,000
T: Non-debt capital receipt of the government | 10,000
O: ₹20,000 crores
O: ₹30,000 crores
O: ₹10,000 crores
O: ₹40,000 crores
Q53
S: The Fiscal Responsibility and Budget Management Act to correct fiscal imbalances was passed in:
O: 2000
O: 2003
O: 2008
O: 2010
Q54
S: Which of the following options is correct regarding the First and Second Five-Year Plans?
OT: First Five-Year Plan | 1951-56 // Second Five-Year Plan | 1956-61
OT: First Five-Year Plan | 1950-55 // Second Five-Year Plan | 1955-60
OT: First Five-Year Plan | 1948-53 // Second Five-Year Plan | 1953-58
OT: First Five-Year Plan | 1949-54 // Second Five-Year Plan | 1954-59
Q55
S: The Nehru-Mahalanobis model was started in the ______ Five-Year Plan.
O: First
O: Second
O: Third
O: Fourth
Q56
S: The Government of India constituted the NITI Aayog in ______. NITI stands for ______.
O: 2015; National Institution for Transforming India
O: 2016; National Institution for Transforming India
O: 2015; National Institution for Transmuting India
O: 2016; National Institution for Transmuting India
Q57
S: Who among the following is considered as the ‘Indian Father of the Green Revolution’?
O: Dr. Manmohan Singh
O: Dr. Amartya Sen
O: Dr. MS Swaminathan
O: Prof. Mani Shankar Aiyar
Q58
S: The first ever National Agriculture Policy was announced in:
O: August 1947
O: July 1982
O: July 2000
O: September 2020
Q59
S: Which of the following are major provisions of the Industrial Policy Resolution, 1956?
S: (i) Provision of Licensing
S: (ii) Expansion of Public Sector
S: (iii) Emphasis on Small Industries
O: (i), (ii) and (iii)
O: (ii) and (iii) only
O: (i) and (ii) only
O: (i) and (iii) only
Q60
S: Which of the following concepts states that the transactions of business are recorded in the books of the business on the assumption that it is a continuing enterprise?
O: Business Entity
O: Going Concern
O: Accounting Period
O: Revenue Recognition
Q61
S: The ______ accounting concept state that personal expenses of a proprietor or partners should be debited to the Drawing Account.
O: Separate Business Entity
O: Money Measurement
O: Accounting Period
O: Going Concern
Q62
S: ABC Ltd. follows the diminishing balance method of depreciation for depreciating machinery year after year due to the ______ convention.
O: Conservatism
O: Disclosure
O: Consistency
O: Materiality
Q63
S: ‘The owner of a firm records his daily medical expenses in the firm’s Income Statement.’
S: With reference to the above statement, indicate which of the following accounting principles has the owner violated?
O: Separate Business Entity
O: Matching
O: Accrual
O: Cost
Q64
S: Under which accounting concept are qualitative transactions NOT recorded in the books of account?
O: Money Measurement
O: Accounting Period
O: Going Concern
O: Business Entity
Q65
S: Pass the necessary journal entry for the following transaction.
S: Issued cheque of ₹39,000 to Pranab, a creditor, in settlement of his account of ₹40,000.
O: Pranab A/c Dr. ₹40,000
OL: To Bank A/c ₹39,000
OL: To Discount received A/c ₹1,000
O: Bank A/c Dr. ₹40,000
OL: To Bank A/c ₹39,000
OL: To Discount received A/c ₹1,000
O: Pranab A/c Dr. ₹40,000
OL: To Bank A/c ₹39,000
OL: To Pranab A/c ₹1,000
O: Pranab A/c Dr. ₹40,000
OL: To Bank A/c ₹40,000
Q66
S: Repair expenses paid on the repair of an old machine purchased should be ______.
O: debited to the Machinery A/c
O: credited to the Machinery A/c
O: debited to the Repair A/c
O: credited to the Repair A/c
Q67
S: Which of the following statements are true/false?
S: (i) Cash account is a real account.
S: (ii) Bank account is a real account.
O: Statement (i) is false and statement (ii) is true.
O: Both statements (i) and (ii) are true.
O: Both statements (i) and (ii) are false.
O: Statement (i) is true and statement (ii) is false.
Q68
S: Which of the following transactions will be deducted when the starting point is credit, i.e. favourable balance as per the bank statement or pass book?
O: Cheques deposited but not collected by the bank.
O: Cheques issued but not presented for payment.
O: Cheques deposited but dishonoured.
O: Cheques recorded but not deposited.
Q69
S: The Bank Reconciliation Statement is prepared as on 31 March 2021 starting with credit balance as per the bank pass book. State whether the following transactions will be shown in the Bank Reconciliation Statement by adding or deducting it from the given balance.
S: (i) Bank had collected interest and credited the account with ₹1,000.
S: (ii) Bill of exchange for ₹10,000 realized by the bank was not recorded in the cash book.
O: Both transactions (i) and (ii) will be deducted from the bank pass book.
O: Transaction (i) will be added to the bank pass book and transaction (ii) will be deducted from the bank pass book.
O: Transaction (i) will be deducted from the bank pass book and transaction (ii) will be added to the bank pass book.
O: Both transactions (i) and (ii) will be added to the bank pass book.
Q70
S: Identify which of the following transactions are shown as a Debit or Credit balance in a Trial Balance.
S: (i) Cash in hand
S: (ii) Rent outstanding
S: (iii) Creditors
S: (iv) Bank overdraft
S: (v) Sundry debtors
S: (vi) Bills receivable
S: (vii) Goodwill
S: (viii) Sales
O: Debit balance: (i), (iv), (vi) and (vii)
OL: Credit balance: (ii), (iii), (v) and (viii)
O: Debit balance: (i), (v), (vi) and (vii)
OL: Credit balance: (ii), (iii), (iv) and (viii)
O: Debit balance: (ii), (v), (vi) and (vii)
OL: Credit balance: (i), (iii), (iv) and (viii)
O: Debit balance: (i), (v), (vi) and (viii)
OL: Credit balance: (ii), (iii), (iv) and (vii)
Q71
S: Loss on sale of an old car used for business is ______.
O: debited to the Profit and Loss Account
O: credited to the Profit and Loss Account
O: debited to the Car Account
O: debited to the Trading Account
Q72
S: Rectify the following two journal entries.
S: (i) A purchase of goods from Ram amounting to ₹1,500 has been wrongly passed through the sales book.
S: (ii) A credit sale of goods of ₹1,200 to Ramesh has been wrongly passed through the purchase book.
O: (i) Purchases A/c Dr. ₹1,500
OL: Sales A/c Dr. ₹1,500
OL: To Ram A/c ₹3,000
OL: (ii) Ramesh A/c Dr. ₹2,400
OL: To Purchases A/c ₹1,200
OL: To Sales A/c ₹1,200
O: (i) Ram A/c Dr. ₹1,500
OL: Sales A/c Dr. ₹1,500
OL: To Purchases A/c ₹3,000
OL: (ii) Ramesh A/c Dr. ₹2,400
OL: To Purchases A/c ₹1,200
OL: To Sales A/c ₹1,200
O: (i) Purchases A/c Dr. ₹1,500
OL: Sales A/c Dr. ₹1,500
OL: To Ram A/c ₹3,000
OL: (ii) Purchases A/c Dr. ₹2,400
OL: To Ramesh A/c ₹1,200
OL: To Sales A/c ₹1,200
O: (i) Purchases A/c Dr. ₹1,500
OL: Sales A/c Dr. ₹1,500
OL: To Ram A/c ₹3,000
OL: (ii) Sales A/c Dr. ₹2,400
OL: To Purchases A/c ₹1,200
OL: To Ramesh A/c ₹1,200
Q73
S: Mr. Mehra purchased a machine on 1 December 2021 for ₹5,00,000. He paid ₹20,000 for loading and carriage expenses to bring the machine to the factory. He further incurred ₹35,000 for installing the machine in the factory. Calculate the amount that will be debited to the Machinery Account.
O: ₹5,00,000
O: ₹5,20,000
O: ₹5,35,000
O: ₹5,55,000
Q74
S: The cost of a machine is ₹20,000 and the rate of depreciation is 10%. The company follows the diminishing balance method of depreciation. The useful life of the machine is 5 years. Calculate the amount of depreciation that will be charged to the Profit and Loss Account in the 3rd year.
O: ₹1,800
O: ₹1,620
O: ₹1,458
O: Nil
Q75
S: Garima maintains books on the single entry system. She presented the following information.
L: Capital on 1 April 2021 = ₹30,400
L: Capital on 1 April 2022 = ₹33,800
L: Drawings made during the period April 2021 to March 2022 = ₹9,600
L: Capital introduced on 1 August 2021 = ₹4,000
S: Calculate the profit or loss made by Garima during the period.
O: Profit made during the period = ₹9,000
O: Loss during the period = ₹9,000
O: Profit made during the period = ₹9,400
O: Loss during the period = ₹9,400
Q76
S: Karl Pearson’s correlation coefficient is independent of:
S: Statement I: change of scale
S: Statement II: change of origin
S: Which option is correct?
O: Only statement I is correct.
O: Only statement II is correct.
O: Both statements I and II are correct.
O: Neither statement I nor statement II is correct.
Q77
S: For the computation of Karl Pearson’s correlation coefficient:
S: Statement I: the two variables have to be measured on either an interval or ratio scale
S: Statement II: the two variables cannot be measured in entirely different units
S: Which option is correct?
O: Only statement I is correct.
O: Only statement II is correct.
O: Both statement I and II are correct.
O: Neither statement I nor statement II is correct.
Q78
S: The Spearman’s correlation coefficient between marks of two subjects for five students for the following data is:
T: Roll No. | 1 | 2 | 3 | 4 | 5
T: Mathematics | 56 | 45 | 61 | 58 | 76
T: Statistics | 66 | 40 | 65 | 59 | 67
O: 0.67
O: 0.70
O: 0.73
O: 0.81
Q79
S: The Pearson’s correlation coefficient of the given data having following calculations is:
S: $n = 5, \sum x = 260, \sum y = 16.5, \sum xy = 859, \sum x^2 = 13530, \sum y^2 = 54.55$
O: 0.70
O: 0.80
O: 0.90
O: 1.00
Q80
S: The correlation coefficient from two lines of regression $Y + X = 5$ and $Y + 2X = 3$ is:
O: 0.25
O: 0.303
O: 0.5
O: 0.707
Q81
S: The arithmetic mean of both regression coefficients is:
O: greater than and equal to correlation coefficient
O: less than and equal to correlation coefficient
O: equal to correlation coefficient
O: square root to correlation coefficient
Q82
S: When the overall sample dispersion is purely due to dispersion among the categories and not at all due to dispersion within the individual categories, then the value of the correlation ratio is:
O: $-1$
O: 0
O: 1
O: $\infty$
Q83
S: If the interclass correlation coefficient is 0.782, then the exams can be rated with ______ reliability by different raters.
O: poor
O: moderate
O: good
O: excellent
Q84
S: For $n$ pairs from an uncorrelated bivariate normal distribution, the sampling distribution of the studentised Pearson's correlation coefficient follows:
O: student $t$ -distribution with degree of freedom $n - 1$
O: student $t$ -distribution with degree of freedom $n - 2$
O: $\chi^2$ distribution with degree of freedom $n - 1$
O: $\chi^2$ distribution with degree of freedom $n - 2$
Q85
S: For data (size $n$ ) that follow a bivariate normal distribution with zero population correlation ( $\rho = 0$ ), the exact density function $f(r)$ for the sample correlation coefficient $r$ of a normal bivariate is:
O: $f(r) = \dfrac{(1-r^2)^{\frac{n-1}{2}}}{B\left(\frac{1}{2},\frac{1}{2}(n-2)\right)}$; $B$ is beta function
O: $f(r) = \dfrac{(1-r^2)^{\frac{n-2}{2}}}{B\left(\frac{1}{2},\frac{1}{2}(n-2)\right)}$; $B$ is beta function
O: $f(r) = \dfrac{(1-r^2)^{\frac{n-3}{2}}}{B\left(\frac{1}{2},\frac{1}{2}(n-2)\right)}$; $B$ is beta function
O: $f(r) = \dfrac{(1-r^2)^{\frac{n-4}{2}}}{B\left(\frac{1}{2},\frac{1}{2}(n-2)\right)}$; $B$ is beta function
Q86
S: The Laspeyre’s price index from the following data is:
T: Commodity | Base period | | Current period |
T: | Price | Quantity | Price | Quantity
T: Sugar | 2 | 10 | 4 | 5
T: Salt | 5 | 12 | 6 | 10
T: Tea | 4 | 20 | 5 | 15
T: Snack | 2 | 15 | 3 | 10
O: 132.3
O: 135.3
O: 138.3
O: 141.3
Q87
S: The Paasche’s quantity index from the following data is:
T: Commodity | Base period | | Current period |
T: | Price | Quantity | Price | Quantity
T: Sugar | 10 | 8 | 11 | 10
T: Salt | 15 | 6 | 9 | 12
T: Tea | 8 | 12 | 17 | 20
O: 141.27
O: 151.27
O: 161.27
O: 171.27
Q88
S: If the price index number satisfies $P_{01} \times P_{12} \times P_{20} = 1$ , then the index number follows the:
O: time reversal test
O: factor reversal test
O: circular test
O: unit test
Q89
S: The cost of living index number is constructed by the:
S: (I) Aggregate expenditure method
S: (II) Family Budget method
S: Which option is correct?
O: Only (I)
O: Only (II)
O: Both (I) and (II)
O: Neither (I) nor (II)
Q90
S: The value of third quartile $Q_3$ for the following marks 25, 47, 34, 52, 23, 62, 29, 57 of 8 students in Statistics is:
O: 53.75
O: 54.75
O: 55.75
O: 56.75
Q91
S: The yearly earnings of investment manager for the past 6 years are 4%, 6%, 7%, 8%, 8.2%, 9%. The range is:
O: 0.8%
O: 5%
O: 7.03%
O: 7.5%
Q92
S: The profit for 4-quarters of a year are 40,000, 20,000, 60,000, and 80,000, respectively. The mean absolute deviation is:
O: 15,000
O: 18,500
O: 20,000
O: 20,200
Q93
S: The coefficient of range for the following data is:
S: 43, 53, 61, 74, 65, 82, 73, 46, 60, 63
O: 0.112
O: 0.212
O: 0.312
O: 0.412
Q94
S: If the coefficient of quartile deviation of the students’ marks is 0.57 and the third quartile $Q_3$ is 31, then the first quartile $Q_1$ is:
O: 6.5
O: 7.5
O: 8.5
O: 9.5
Q95
S: If the coefficient of standard deviation is 0.40 and the mean is 5 for the given data, then the variance is equal to:
O: 2.5
O: 3.6
O: 4.0
O: 4.9
Q96
S: For the data of 50 employees' earnings, the coefficient of mean deviation and mean deviation are 0.3 and 15,000, respectively, the mean earning is:
O: 40,000
O: 48,000
O: 50,000
O: 52,500
Q97
S: In a town, 25% of the persons earned more than ₹45,000. If the quartile deviation is 13500, then the 75% of the persons earned is more than ______.
O: 12000
O: 14000
O: 16000
O: 18000
Q98
S: If the arithmetic mean and the geometric mean of two numbers are 12 and 6, then the harmonic mean is:
O: 2
O: 3
O: 4
O: 6
Q99
S: For the three numbers 2, $a$ , $b$ , the arithmetic mean is $\frac{14}{3}$ and the geometric mean is 4. The value of $a$ and $b$ respectively are:
O: (4, 8)
O: (6, 6)
O: (9, 3)
O: (10, 2)
Q100
S: If the harmonic mean and arithmetic mean respectively of three numbers in arithmetic progression are 54/11 and 6, then the geometric mean of those numbers is:
O: $(27)^{\frac{1}{3}}$
O: $(81)^{\frac{1}{3}}$
O: $(162)^{\frac{1}{3}}$
O: $(243)^{\frac{1}{3}}$
Q101
S: The median of the following data is:
T: Class | 40-44 | 44-46 | 46-48 | 48-52 | 52-58 | 58-60
T: Frequency | 4 | 6 | 8 | 12 | 7 | 2
O: 48.5
O: 49
O: 48
O: 47.5
Q102
S: The geometric mean of five numbers is 8 and the geometric mean of the first three numbers is 4. The geometric mean of the last two numbers is:
O: 16
O: $16\sqrt{2}$
O: 32
O: $32\sqrt{32}$
Q103
S: If the geometric mean of 2, 4, 8, 16, 32 is 8, then the geometric mean of 24, 192, 1536, 12288, 98304 is:
O: 512
O: 1024
O: 1536
O: 2048
Q104
S: If $g(x) = \log x$, then the arithmetic mean of $g\left(\frac{x}{y}\right)$ and $g(xy)$ is:
O: $\log x$
O: $\log y$
O: $x \log y$
O: $y \log x$
Q105
S: Which of the following is not a measure of location?
O: Midrange
O: Quartile
O: Range
O: Maximum
Q106
S: The midrange of the following data is:
S: 9, 1, 0, 1, 5, 1, 9, 0, 10, 9
O: 5
O: 5.5
O: 5.8
O: 6
Q107
S: Interquartile range of corona incubation in days for the following data is:
S: 29, 31, 24, 29, 30, 25
O: 4.5 days
O: 5.0 days
O: 5.5 days
O: 6.0 days
Q108
S: The median of the data set 26, 23, 28, 22, 29, 21 is:
O: 24.5
O: 23
O: 26
O: 25.5
Q109
S: For the arbitrary data set, the mean and mode are 14 and 20 respectively. The median by empirical relation is:
O: 11.5
O: 15.3
O: 26
O: 16
Q110
S: The mode of marks obtained by the students of Mathematics class given in the following data is:
T: Marks | 50-56 | 56-62 | 62-68 | 68-74 | 74-80 | 80-86 | 86-92
T: Frequency | 6 | 11 | 25 | 35 | 18 | 12 | 6
O: 68.22
O: 69.22
O: 70.22
O: 71.22
Q111
S: The median, mode, and mean of 19, 15, 18, 19, 19, 17, 18, 19, 18, respectively, are:
O: 19, 19, 19
O: 19, 18, 19
O: 18, 19, 18
O: 18, 19, 19
Q112
S: If the coefficient of variation of 1, 2, 4, 5 is $\sqrt{\frac{5}{18}} \times 100$, then the coefficient of 2, 3, 5, 6 is:
O: $\sqrt{\frac{5}{32}} \times 100$
O: $\sqrt{\frac{5}{16}} \times 100$
O: $\sqrt{\frac{5}{8}} \times 100$
O: $\sqrt{\frac{5}{4}} \times 100$
Q113
S: If the mean and coefficient of variation of $X$ are 20 and 20, respectively, then the variance of $Y = 20 - 3X$ is:
O: 100
O: 64
O: 36
O: 144
Q114
S: If the first four moments about the origin are $-2.5, 18, -32, 110$ , then the third moment about the mean is:
O: 70.75
O: 71.75
O: 72.75
O: 73.75
Q115
S: The second and fourth moment about mean for a distribution are 5 and 20, respectively. The value of Pearson’s coefficient of kurtosis $\beta_2$ is:
O: 4
O: 2
O: 1
O: 0.8
Q116
S: For the unequal class intervals, the first, second, and third quartiles are 20.5, 23, and 25.5, respectively. The Bowley’s coefficient of skewness is:
O: $-1.5$
O: $-1$
O: 0
O: 1.5
Q117
S: The standard deviation of the data set 9, 11, 14, 12, 17, 15 is:
O: $\sqrt{5}$
O: $\sqrt{6}$
O: $\sqrt{7}$
O: $\sqrt{8}$
Q118
S: If the mean and standard deviation of 5, $a, b$ are 4 and $\sqrt{\frac{2}{3}}$ respectively, then the values of $a$ and $b$ respectively are:
O: (4, 3)
O: (4, 4)
O: (3, 3)
O: (4, 2)
Q119
S: If the standard deviation of $p, q, r$ is $t$ , then the standard deviation of $\alpha p + \beta, \alpha q + \beta, \alpha r + \beta$ is:
O: $\alpha t$
O: $\alpha^2 t^2$
O: $\alpha^2 t^2 + 3\beta^2$
O: $\alpha t + 3\beta$
Q120
S: The third decile $D_3$ for the following frequency table is:
T: Range | 10-20 | 20-30 | 30-40 | 40-50 | 50-60 | 60-70 | 70-80
T: Frequency | 8 | 12 | 14 | 10 | 6 | 16 | 4
O: 30.41
O: 30.51
O: 30.61
O: 30.71
Q121
S: For the frequency table of marks obtained by the students, the ninetieth percentile $P_{90}$ is:
T: Marks | 0-10 | 10-20 | 20-40 | 40-60 | 60-80 | 80-100
T: Frequency | 8 | 10 | 22 | 25 | 10 | 5
O: 72.6
O: 73.8
O: 74.0
O: 75.2
Q122
S: A fire in a production unit delaying manufacturing for some time is a/an:
O: cyclical trend
O: irregular trend
O: seasonal trend
O: secular trend
Q123
S: Which of the following is NOT a component of the time series?
O: Trend
O: Seasonal variations
O: Cyclic variations
O: Periodic movements
Q124
S: The STL decomposition is an acronym for:
O: Seasonal and Trend decomposition using Loess
O: Seasonal and Trend decomposition using Loss
O: Seasonal and Trend decomposition using Lorentz
O: Seasonal and Trend decomposition using Lipschitz
Q125
S: Deseasonalisation is a statistical method for removing the ______ of a time series.
O: errors in seasonal component
O: irregular components
O: outlier trends
O: seasonal component
Q126
S: To remove an underlying trend in the time series data, the method of detrend are:
S: (I) Detrend by differencing
S: (II) Detrend by model fitting
S: Which option is correct?
O: Only (I) is correct.
O: Only (II) is correct.
O: Both (I) and (II) are correct.
O: Neither (I) nor (II) is correct.
Q127
S: The moving average method is used with time-series data to smooth out:
S: (I) Short term fluctuations
S: (II) Long term trends
S: Which option is correct?
O: Only (I) is correct.
O: Only (II) is correct.
O: Both (I) and (II) are correct.
O: Neither (I) nor (II) is correct.
Q128
S: By method of semi-average, the linear trend is observed from the plot between which points for the following time series data?
T: Year | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018
T: Production | 20 | 22 | 20 | 21 | 23 | 26 | 28 | 30
O: (2011, 20) and (2018, 30)
O: (2012.5, 22.75) and (2016.5, 24.75)
O: (2012.5, 20.75) and (2016.5, 26.75)
O: (2014, 21) and (2015, 23)
Q129
S: Which frequency table is correct for the following data set?
S: 76, 51, 68, 83, 74, 61, 42, 72, 51, 64, 53, 70, 45, 63, 47, 75, 67, 58, 54, 59, 52, 79
OT: Marks | 41-49 | 50-58 | 59-67 | 68-76 | 77-85 // Frequency | 3 | 5 | 6 | 6 | 2
OT: Marks | 41-49 | 50-58 | 59-67 | 68-76 | 77-85 // Frequency | 3 | 6 | 6 | 5 | 2
OT: Marks | 41-49 | 50-58 | 59-67 | 68-76 | 77-85 // Frequency | 3 | 6 | 6 | 6 | 2
OT: Marks | 41-49 | 50-58 | 59-67 | 68-76 | 77-85 // Frequency | 3 | 6 | 5 | 6 | 2
Q130
S: Government publications, websites, books, journal articles, internal records etc. are appropriate for:
S: (I) primary data
S: (II) secondary data
S: Which option is correct?
O: Only (I) is correct.
O: Only (II) is correct.
O: Both (I) and (II) are correct.
O: Neither (I) nor (II) is correct.
Q131
S: Which of the following is NOT a characteristics of frequency curve?
O: Measure of central tendency
O: Measure of dispersion
O: Frequency polygon
O: Shape of the frequency curve
Q132
S: The feature of absolute zero is a characteristic of:
O: nominal scale
O: ordinal scale
O: interval scale
O: ratio scale
Q133
S: Questions that can be measured on the interval scale is:
S: (I) Likert scale
S: (II) Net promoter score
S: (III) Bipolar matrix table
S: Which option is correct?
O: Only (I) is correct.
O: Both (I) and (II) are correct.
O: Both (I) and (III) are correct.
O: All (I), (II), and (III) are correct.
Q134
S: ‘The number of germs in the patient’s body’ is an example of the:
O: finite population
O: infinite population
O: existent population
O: hypothetical population
Q135
S: Which of the following is NOT correct?
O: Convenience sampling: sample is taken from a group of people easy to contact
O: Quota sampling: sample involving individuals that represent a population
O: Snowball sampling: recruitment technique
O: Stratified random sampling: population is divided into heterogeneous groups
Q136
S: A box contains 5 red and 3 white marbles. Two marbles are chosen at random. What is the probability that both are of the same colour?
O: 15/28
O: 1/2
O: 13/28
O: 28/30
Q137
S: Let $X, Y,$ and $Z$ be mutually exclusive and exhaustive events such that $P(X) = 2P(Y) = 6P(Z)$ . The value of $P(X)$ is:
O: 0.3
O: 0.4
O: 0.5
O: 0.6
Q138
S: Let $A$ and $B$ be exhaustive and equally likely, and independent events. The value of $P(A \cap B)$ is:
O: 0
O: 0.25
O: 0.50
O: 1
Q139
S: Assuming the marks in Statistics are normally distributed with a standard deviation = 5. The minimum size required to construct a 95% confidence interval for mean with a maximum error = 0.5 is:
O: 370
O: 375
O: 380
O: 385
Q140
S: An officer conducts an ethnographic investigation into the complications confronted by extremely-backwards employees. Which method of sampling will be the most appropriate?
O: Random sampling
O: Stratified sampling
O: Cluster sampling
O: Systematic sampling
Q141
S: Suppose bag A consists of 4 red and 5 white marbles and bag B consists of 6 red and 3 white marbles. A marble is selected at random from bag A and kept in bag B. Finally, a marble is selected at random from bag B. What is the probability that white marble was kept from bag A to bag B given that the marble chosen from bag B is red?
O: 12/29
O: 13/29
O: 14/29
O: 15/29
Q142
S: The number of men, women, and children in society is 30, 70, and 50, respectively. The angle corresponding to men, if the distribution is represented in a pie chart, is:
O: 36°
O: 72°
O: 120°
O: 168°
Q143
S: The $x$ -coordinate of the point of intersection of the ‘less than ogive’ and ‘more than ogive’ represents which central tendency among the following options.
O: Mean
O: Median
O: Mode
O: First quartile
Q144
S: The arithmetic mean, geometric mean, and harmonic mean of data set 3, 4, 9, 12, respectively, are:
O: $(7, 36, 6.14)$
O: $(7, 36, 5.14)$
O: $(7, 6, 5.14)$
O: $(7, 6, 6.14)$
Q145
S: The coefficient of quartile deviation for data set 8, 9, 7, 10, 8 is:
O: $\frac{1}{17}$
O: $\frac{2}{17}$
O: $\frac{3}{17}$
O: $\frac{4}{17}$
Q146
S: The population skewness from the following data is:
S: 3, 5, 2, 6, 4
O: 0
O: 0.533
O: 1.533
O: 2.533
Q147
S: The Pearson correlation coefficient from the following data is:
T: $X$ | 2 | 4 | 6 | 8
T: $Y$ | 1 | 4 | 2 | 3
O: 0.30
O: 0.36
O: 0.40
O: 0.44
Q148
S: The probable error by Pearson’s product-moment method if the correlation coefficient is 0.8 for 25 pair of samples is:
O: 0.0186
O: 0.0286
O: 0.0386
O: 0.0486
Q149
S: For the particular commodity, the quarter-wise average price for three years is as follows.
T: Year | Quarter1 | Quarter2 | Quarter3 | Quarter4
T: 2020 | 4 | 2 | 5 | 6
T: 2021 | 4 | 7 | 6 | 3
T: 2022 | 4 | 5 | 7 | 4
S: The quarterly seasonal index for the second quarter is:
O: 84.2%
O: 98.3%
O: 126.3%
O: 91.2%
Q150
S: Following is the price table for different fabrics.
T: | Base Year | | Current Year
T: Fabric | Price | Quantity | Price
T: Cotton | 200 | 2 | 150
T: Silk | 350 | 1 | 400
T: Woollen | 400 | 3 | 300
S: The Laspeyre’s price index is:
O: 72.05%
O: 82.05%
O: 92.05%
O: 102.05%
"""


def parse(src=TRANSCRIPTION):
    """{n: {"stem": [block], "options": [option]}}, where a block is
    {"p": text}, {"list": [text]} or {"table": [[cell]]}, and an option is
    {"lines": [text]} or {"table": [[cell]]}."""
    out, cur = {}, None
    for raw in src.strip("\n").split("\n"):
        m = re.match(r"^Q(\d+)$", raw)
        if m:
            cur = out[int(m.group(1))] = {"stem": [], "options": []}
            continue
        kind, _, t = raw.partition(": ")
        if cur is None or not t:
            raise ValueError("cannot read line %r" % raw)
        stem = cur["stem"]
        if kind == "S":
            stem.append({"p": t})
        elif kind == "L":
            if not (stem and "list" in stem[-1]):
                stem.append({"list": []})
            stem[-1]["list"].append(t)
        elif kind == "T":
            if not (stem and "table" in stem[-1]):
                stem.append({"table": []})
            stem[-1]["table"].append([c.strip() for c in t.split("|")])
        elif kind == "O":
            cur["options"].append({"lines": [t]})
        elif kind == "OL":
            cur["options"][-1]["lines"].append(t)
        elif kind == "OT":
            cur["options"].append({"table": [[c.strip() for c in r.split("|")] for r in t.split(" // ")]})
        else:
            raise ValueError("unknown line kind %r" % raw)
    return out


TEXT = parse()
