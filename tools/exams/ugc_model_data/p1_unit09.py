# -*- coding: utf-8 -*-
"""UGC NET Paper I, Unit 9: fifty exam-standard model questions.

Only settled facts are used (acts, years, conventions, definitions); no
figure that changes from year to year.
"""
from . import AR, Q, ar, match, st

TITLE = "People, Development and Environment"
BLURB = ("The Millennium and Sustainable Development Goals, human and environment interaction, environmental "
         "issues, pollution and waste, climate change, the effects of pollutants on health, energy resources, "
         "natural hazards, the Environment (Protection) Act, the National Action Plan on Climate Change and "
         "international agreements.")

QUESTIONS = [
 Q("Consider the statements:"
   + st("The Millennium Development Goals were eight in number and ran from 2000 to 2015.",
        "The Sustainable Development Goals are 17 goals with 169 targets, for 2015 to 2030.",
        "The Sustainable Development Goals apply only to developing countries.",
        "The Sustainable Development Goals were adopted in the 2030 Agenda, in September 2015.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and IV only", "II, III and IV only", "I, II, III and IV"], "B",
   "The MDGs were addressed mainly to developing countries; the SDGs apply to all countries. So (III) is "
   "false and the other three are correct.", "goals"),

 Q("Match the Sustainable Development Goal in List I with its subject in List II."
   + match(["SDG 4", "SDG 7", "SDG 13", "SDG 14"],
           ["Climate action", "Life below water", "Quality education", "Affordable and clean energy"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)"], "D",
   "SDG 4 is quality education, SDG 7 affordable and clean energy, SDG 13 climate action and SDG 14 life "
   "below water (SDG 15 is life on land).", "goals"),

 Q("&ldquo;Development that meets the needs of the present without compromising the ability of future "
   "generations to meet their own needs&rdquo; is the definition of sustainable development given in:",
   ["the Brundtland Report, Our Common Future (1987)", "Agenda 21 (1992)", "the Kyoto Protocol (1997)",
    "the Millennium Declaration (2000)"], "A",
   "The definition comes from the report of the World Commission on Environment and Development, chaired by "
   "Gro Harlem Brundtland, published in 1987.", "goals"),

 Q("Which of the following was NOT one of the eight Millennium Development Goals?",
   ["To achieve universal primary education", "To reduce child mortality",
    "To provide affordable and clean energy", "To improve maternal health"], "C",
   "Affordable and clean energy is SDG 7; energy had no goal of its own among the MDGs. The eight MDGs "
   "covered poverty and hunger, primary education, gender equality, child mortality, maternal health, "
   "HIV/AIDS and malaria, environmental sustainability and a global partnership.", "goals"),

 Q("In India, the SDG India Index, which scores the states and union territories on their progress towards "
   "the goals, is published by:",
   ["the Reserve Bank of India", "NITI Aayog", "the Central Pollution Control Board",
    "the National Statistical Commission"], "B",
   "NITI Aayog brings out the SDG India Index, an example of turning the global goals into measures that "
   "can be tracked nationally and by state.", "goals"),

 Q("In the IPAT identity, the environmental impact I is expressed as the product of:",
   ["production, agriculture and trade", "pollution, area and time",
    "people, attitude and tools", "population, affluence and technology"], "D",
   "Impact = Population &times; Affluence (consumption per person) &times; Technology (impact per unit of "
   "consumption).", "interaction"),

 Q("The population of a city is unchanged, but every household doubles its use of electricity generated "
   "from coal. In terms of the IPAT identity, the impact rises through:",
   ["affluence", "population", "technology", "none of the three"], "A",
   "Consumption per person has risen while the number of people and the technology (coal-based power) are "
   "the same: the change is in A.", "interaction"),

 Q("Match the human activity in List I with a characteristic environmental impact in List II."
   + match(["Agriculture", "Mining", "Urbanisation", "Transport"],
           ["Heat islands and loss of wetlands", "Vehicle emissions and fragmentation of habitats",
            "Fertiliser run-off and falling water tables", "Land degradation and acid drainage"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "C",
   "Each activity has its typical impacts: agriculture on soil and water, mining on land, urbanisation on "
   "land use and local climate, transport on air and on the continuity of habitats.", "interaction"),

 Q("Smoke from the burning of crop residue in Punjab and Haryana adds to the winter air pollution of Delhi. "
   "By its scale, this environmental issue is:",
   ["local", "regional", "global", "indoor"], "B",
   "The cause and the effect lie in different states, hundreds of kilometres apart, but within one region. "
   "A city's garbage dump is local; climate change and ozone depletion are global.", "issues"),

 Q("Which of the following lists contains only global environmental issues?",
   ["Noise near a highway, acid rain, ozone depletion", "A polluted lake, desertification, climate change",
    "River pollution along a basin, plastic in the oceans, a city's garbage dump",
    "Climate change, ozone depletion, loss of biodiversity"], "D",
   "Global issues affect the whole planet whatever their source: climate change, ozone depletion, loss of "
   "biodiversity, plastic in the oceans. Noise, a lake and a dump are local; acid rain, river-basin pollution "
   "and desertification are regional.", "issues"),

 Q(ar("The depletion of the ozone layer had to be dealt with by a global treaty.",
      "Ozone-depleting substances released in any country thin the ozone layer for all."),
   AR, "A",
   "Because the harm does not stay where the gases are released, no country can protect itself alone; hence "
   "the Vienna Convention and the Montreal Protocol. Both statements are true and (R) is the reason.", "issues"),

 Q("A stretch of river below a town's sewage outfall has a high biochemical oxygen demand (BOD). This "
   "indicates:",
   ["a high level of dissolved oxygen", "contamination by heavy metals only",
    "a heavy load of organic pollution", "very clean water"], "C",
   "BOD is the oxygen micro-organisms need to break down the organic matter in water. A high BOD means much "
   "organic matter, such as sewage, and the dissolved oxygen falls as it is used up.", "pollution"),

 Q("Arrange the following in the order of the waste hierarchy, from the most preferred to the least "
   "preferred: (1) Recycle, (2) Dispose, (3) Reduce, (4) Recover energy, (5) Reuse.",
   ["3, 1, 5, 4, 2", "3, 5, 1, 4, 2", "5, 3, 1, 4, 2", "3, 5, 4, 1, 2"], "B",
   "Reduce, reuse, recycle, recover, dispose. It is best not to create waste at all, and disposal is the "
   "last resort.", "pollution"),

 Q("Match the kind of waste in List I with the rules that govern it in India in List II."
   + match(["Household garbage", "Hospital waste", "Discarded phones and computers", "Sewage and effluent"],
           ["E-Waste (Management) Rules, 2022", "Water (Prevention and Control of Pollution) Act, 1974",
            "Solid Waste Management Rules, 2016", "Bio-Medical Waste Management Rules, 2016"]),
   ["(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)"], "A",
   "Solid waste is to be segregated at source into wet, dry and domestic hazardous; biomedical waste goes "
   "into colour-coded bags; e-waste rules rest on extended producer responsibility; liquid waste falls under "
   "the Water Act.", "pollution"),

 Q("Under the principle of extended producer responsibility in the E-Waste (Management) Rules:",
   ["consumers must repair their own devices", "municipalities alone must collect electronic waste",
    "electronic waste may be exported freely",
    "the producer of a product must arrange for the collection and recycling of a share of it at the end of its life"], "D",
   "Extended producer responsibility puts the duty of taking back and recycling end-of-life products on "
   "those who make and sell them.", "pollution"),

 Q("Noise is measured in decibels on a logarithmic scale. A sound of 70 dB has how many times the intensity "
   "of a sound of 50 dB?",
   ["1.4 times", "20 times", "100 times", "2 times"], "C",
   r"Every 10 dB is a tenfold increase in intensity. A difference of 20 dB is $10\times10=100$ times.", "pollution"),

 Q("Consider the statements:"
   + st("PM2.5 refers to particles less than 2.5 micrometres in diameter.",
        "India's National Air Quality Index reports air quality in six categories.",
        "Eutrophication is caused by excess nutrients such as nitrates and phosphates in water.",
        "Under the noise rules, silence zones have the most relaxed limits.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "II, III and IV only", "I, II, III and IV"], "B",
   "Silence zones, around hospitals, schools and courts, have the <em>strictest</em> noise limits, so (IV) is "
   "false. The Air Quality Index (2014) runs from good to severe and is based on eight pollutants.", "pollution"),

 Q("In a lake that receives run-off rich in fertiliser, algae multiply rapidly, the dissolved oxygen falls "
   "and fish die. The process is called:",
   ["eutrophication", "biomagnification", "salinisation", "desertification"], "A",
   "Nutrients feed algal blooms; when the algae die and decay, oxygen is used up. Biomagnification is the "
   "build-up of a persistent pollutant along the food chain.", "pollution"),

 Q("Which of the following is NOT one of the six greenhouse gases covered by the Kyoto Protocol?",
   ["Methane", "Nitrous oxide", "Sulphur hexafluoride", "Chlorofluorocarbons"], "D",
   "The Kyoto gases are carbon dioxide, methane, nitrous oxide, hydrofluorocarbons, perfluorocarbons and "
   "sulphur hexafluoride. Chlorofluorocarbons, though they also trap heat, are controlled as ozone-depleting "
   "substances under the Montreal Protocol.", "climate"),

 Q("The Intergovernmental Panel on Climate Change (IPCC) was set up in 1988 by:",
   ["the World Bank and the International Monetary Fund", "the UN General Assembly and UNESCO",
    "the World Meteorological Organization and the United Nations Environment Programme",
    "the World Health Organization and the Food and Agriculture Organization"], "C",
   "The IPCC was established by the WMO and UNEP to assess the science of climate change; it does not itself "
   "do research.", "climate"),

 Q("Planting mangroves along a coast stores carbon and also protects the shore against storm surges. In the "
   "language of climate policy these are, respectively:",
   ["adaptation and mitigation", "mitigation and adaptation", "mitigation and compensation",
    "adaptation and remediation"], "B",
   "Mitigation reduces the cause (emissions, or carbon in the atmosphere); adaptation copes with the effects "
   "already happening. Mangroves do both.", "climate"),

 Q("The principle that all countries must act on climate change, but that developed countries, which have "
   "emitted most, should take the lead, is called:",
   ["common but differentiated responsibilities", "the polluter pays principle",
    "the precautionary principle", "extended producer responsibility"], "A",
   "Common but differentiated responsibilities was set out at Rio in 1992. Climate justice and the fund for "
   "loss and damage follow from the same idea.", "climate"),

 Q(ar("Per tonne emitted, methane warms the atmosphere far more than carbon dioxide, yet carbon dioxide "
      "contributes most to global warming.",
      "Carbon dioxide is emitted in far greater quantity and stays in the atmosphere much longer."),
   AR, "A",
   "The contribution of a gas depends on its strength, the amount emitted and how long it lasts. Methane is "
   "strong but short-lived and emitted in smaller amounts. Both statements are true and (R) explains (A).", "climate"),

 Q("Which of the following is an adaptation measure and not a mitigation measure?",
   ["Replacing coal-fired power by solar power", "Improving the fuel efficiency of vehicles",
    "Planting forests to absorb carbon dioxide", "Developing drought-resistant varieties of crops"], "D",
   "Drought-resistant crops help people live with a changed climate: adaptation. The other three reduce "
   "emissions or remove carbon dioxide: mitigation.", "climate"),

 Q("Match the pollutant in List I with the disease or condition in List II."
   + match(["Mercury", "Cadmium", "Fluoride in excess", "Nitrate in drinking water"],
           ["Itai-itai disease", "Blue baby syndrome", "Minamata disease", "Mottled teeth and stiff joints"]),
   ["(a)-(iii), (b)-(i), (c)-(ii), (d)-(iv)", "(a)-(i), (b)-(iii), (c)-(iv), (d)-(ii)",
    "(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)"], "C",
   "Mercury causes Minamata disease; cadmium causes itai-itai; excess fluoride causes dental and skeletal "
   "fluorosis; nitrate causes methaemoglobinaemia (blue baby syndrome) in infants.", "health"),

 Q("The gas that leaked in the Bhopal disaster of December 1984 was:",
   ["carbon monoxide", "methyl isocyanate", "sulphur dioxide", "chlorine"], "B",
   "Methyl isocyanate escaped from a pesticide plant. The disaster led to the Environment (Protection) Act, "
   "1986.", "health"),

 Q("Long-term drinking of groundwater contaminated with arsenic, as in parts of the Ganga basin, causes:",
   ["skin lesions and cancers", "softening of the bones", "mottling of the teeth", "blue baby syndrome"], "A",
   "Arsenicosis shows first as lesions and darkening of the skin and raises the risk of cancers. Softening "
   "of bones is the effect of cadmium, mottled teeth of fluoride, blue baby syndrome of nitrate.", "health"),

 Q("Which pollutant is particularly harmful to the developing nervous system of children?",
   ["Ozone", "Carbon dioxide", "Nitrogen", "Lead"], "D",
   "Lead damages the nervous system and impairs children's mental development, which is why leaded petrol "
   "was phased out.", "health"),

 Q("Consider the following effects on health:"
   + st("Hearing loss", "Sleep disturbance", "High blood pressure", "Dental fluorosis")
   + "Which of them are caused by prolonged exposure to noise?",
   ["I and II only", "I, III and IV only", "I, II and III only", "I, II, III and IV"], "C",
   "Noise causes hearing loss, stress, disturbed sleep and raised blood pressure. Dental fluorosis comes from "
   "excess fluoride in drinking water.", "health"),

 Q("Which of the following sources of energy is renewable but confined to particular places, and draws on "
   "the internal heat of the Earth?",
   ["Biomass", "Geothermal", "Nuclear", "Natural gas"], "B",
   "Geothermal energy is the Earth's own heat, available where hot rock or water lies near the surface; the "
   "best-known Indian site is the Puga valley in Ladakh.", "energy"),

 Q("Which of the following lists contains only non-renewable sources of energy?",
   ["Coal, petroleum and natural gas", "Coal, wind and biomass", "Solar, hydro and geothermal",
    "Petroleum, solar and nuclear"], "A",
   "The fossil fuels are non-renewable and are the main source of carbon dioxide. Wind, biomass, solar, "
   "hydro and geothermal energy are renewable.", "energy"),

 Q("Biogas, produced from cattle dung in a village digester, is obtained by:",
   ["combustion in excess air", "distillation", "nuclear fission", "anaerobic digestion"], "D",
   "Micro-organisms break the organic matter down in the absence of air and release a gas, mostly methane; "
   "the slurry left over is a good manure. It is a form of biomass energy.", "energy"),

 Q("Consider the statements:"
   + st("Nuclear power is a low-carbon source of energy that uses a non-renewable fuel.",
        "India's three-stage nuclear programme aims at using its reserves of thorium.",
        "Soil is renewed only very slowly and can be lost quickly by erosion.",
        "Large hydroelectric projects have no social or ecological costs.")
   + "Which of the statements are correct?",
   ["I and II only", "II and III only", "I, II and III only", "I, II, III and IV"], "C",
   "Large dams displace people and alter rivers and forests, so (IV) is false. The other three are correct.", "energy"),

 Q("India has announced the goal of reaching net-zero emissions by the year:",
   ["2050", "2070", "2060", "2100"], "B",
   "India has announced net zero by 2070. Its updated Nationally Determined Contribution (2022) also commits "
   "it to cutting the emissions intensity of GDP by 45% by 2030 from the 2005 level.", "energy"),

 Q("A hazard becomes a disaster when:",
   ["it overwhelms the capacity of the affected community to cope", "it is forecast in advance",
    "it occurs in an uninhabited area", "it is of natural origin"], "A",
   "A hazard is a threatening event; a disaster is its outcome when the people exposed are vulnerable and "
   "cannot cope with their own resources.", "hazards"),

 Q("A municipality forbids the building of new houses on the flood plain of a river. This is an example of:",
   ["structural mitigation", "response", "recovery", "non-structural mitigation"], "D",
   "Non-structural mitigation works through rules and knowledge: land-use zoning, building codes, insurance, "
   "early warning and awareness. Structural mitigation is physical: embankments, shelters, resistant "
   "buildings.", "hazards"),

 Q("Arrange the following phases of the disaster management cycle in order, beginning before the event: "
   "(1) Response, (2) Recovery and reconstruction, (3) Mitigation and preparedness.",
   ["1, 3, 2", "3, 2, 1", "3, 1, 2", "2, 3, 1"], "C",
   "Mitigation and preparedness come before the event, response during and just after it, recovery and "
   "reconstruction afterwards.", "hazards"),

 Q("Consider the statements about the Disaster Management Act, 2005:"
   + st("It created the National Disaster Management Authority.",
        "It provides for disaster management authorities at the state and district levels.",
        "The National Disaster Response Force is the specialised force for responding to disasters.",
        "The National Disaster Management Authority is headed by the Union Home Minister.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and III only", "II, III and IV only", "I, II, III and IV"], "B",
   "The National Disaster Management Authority is chaired by the Prime Minister, not the Home Minister, so "
   "(IV) is false. The Act sets up authorities at the national, state and district levels, and the National "
   "Disaster Response Force is the specialised response force.", "hazards"),

 Q("The international framework for disaster risk reduction that the Sendai Framework replaced in 2015 "
   "was the:",
   ["Hyogo Framework for Action", "Kyoto Protocol", "Agenda 21", "Montreal Protocol"], "A",
   "The Hyogo Framework for Action covered 2005 to 2015; the Sendai Framework for Disaster Risk Reduction "
   "covers 2015 to 2030. The Kyoto and Montreal Protocols concern greenhouse gases and the ozone layer.", "hazards"),

 Q("Consider the statements about the Environment (Protection) Act, 1986:"
   + st("It was enacted after the Bhopal gas tragedy.",
        "It gives effect to the decisions of the Stockholm Conference of 1972.",
        "It is an umbrella law that empowers the Central Government to protect and improve the environment.",
        "The Environment Impact Assessment notification is issued under it.")
   + "Which of the statements are correct?",
   ["I and III only", "I, II and III only", "II, III and IV only", "I, II, III and IV"], "D",
   "All four are correct. The Act was passed under Article 253 of the Constitution to implement the "
   "Stockholm decisions, and many rules, including the EIA notification of 2006 and the waste rules, are "
   "made under it.", "epa"),

 Q("Arrange the following laws in chronological order: (1) Air (Prevention and Control of Pollution) Act, "
   "(2) Wild Life (Protection) Act, (3) Environment (Protection) Act, (4) Water (Prevention and Control of "
   "Pollution) Act, (5) Forest (Conservation) Act.",
   ["2, 4, 1, 5, 3", "4, 2, 5, 1, 3", "2, 4, 5, 1, 3", "2, 5, 4, 1, 3"], "C",
   "Wild Life Act 1972, Water Act 1974, Forest (Conservation) Act 1980, Air Act 1981, Environment "
   "(Protection) Act 1986.", "epa"),

 Q("The requirement that a new highway or mining project must have its environmental impact assessed before "
   "it is cleared comes from:",
   ["the Environment Impact Assessment notification under the Environment (Protection) Act", "the Factories Act",
    "the Biological Diversity Act", "the Disaster Management Act"], "A",
   "The EIA notification of 2006 was issued under the Environment (Protection) Act, 1986, and lists the "
   "projects that need prior environmental clearance.", "epa"),

 Q("The National Green Tribunal, a specialised body for the speedy disposal of environmental cases, was "
   "established under an Act of:",
   ["1986", "2010", "2002", "1974"], "B",
   "The National Green Tribunal Act was passed in 2010. 2002 is the year of the Biological Diversity Act.", "epa"),

 Q("The National Action Plan on Climate Change was released in 2008. The number of national missions under "
   "it is:",
   ["six", "ten", "twelve", "eight"], "D",
   "The eight missions are on solar energy, enhanced energy efficiency, sustainable habitat, water, the "
   "Himalayan ecosystem, a green India, sustainable agriculture and strategic knowledge for climate change.", "napcc"),

 Q("Which of the following is NOT one of the national missions under the National Action Plan on Climate "
   "Change?",
   ["National Solar Mission", "National Water Mission", "National Nuclear Energy Mission",
    "National Mission for a Green India"], "C",
   "There is no nuclear mission among the eight. Rooftop solar targets fall under the Solar Mission and the "
   "afforestation of degraded land under the Green India Mission.", "napcc"),

 Q("Match the activity in List I with the mission of the National Action Plan on Climate Change in List II."
   + match(["Afforestation of degraded land", "Rating appliances for efficient use of electricity",
            "Climate-resilient cropping", "Protection of glaciers and mountain ecosystems"],
           ["Mission for Sustaining the Himalayan Ecosystem", "Mission for a Green India",
            "Mission for Enhanced Energy Efficiency", "Mission for Sustainable Agriculture"]),
   ["(a)-(ii), (b)-(iii), (c)-(iv), (d)-(i)", "(a)-(iii), (b)-(ii), (c)-(iv), (d)-(i)",
    "(a)-(ii), (b)-(iv), (c)-(iii), (d)-(i)", "(a)-(i), (b)-(iii), (c)-(iv), (d)-(ii)"], "A",
   "Each activity belongs to the mission whose name describes it: Green India for forests, Enhanced Energy "
   "Efficiency for appliances and industry, Sustainable Agriculture for cropping, and the Himalayan mission "
   "for glaciers and mountain ecosystems.", "napcc"),

 Q("Arrange the following in chronological order: (1) Montreal Protocol, (2) Stockholm Conference, "
   "(3) Paris Agreement, (4) Rio Earth Summit, (5) Kyoto Protocol.",
   ["2, 4, 1, 5, 3", "2, 1, 4, 5, 3", "1, 2, 4, 5, 3", "2, 1, 5, 4, 3"], "B",
   "The Stockholm Conference was held in 1972, the Montreal Protocol was adopted in 1987, the Rio Earth "
   "Summit met in 1992, the Kyoto Protocol was adopted in 1997 and the Paris Agreement in 2015.", "agreements"),

 Q("Match the agreement in List I with its subject in List II."
   + match(["Montreal Protocol", "Kyoto Protocol", "Cartagena Protocol", "Nagoya Protocol"],
           ["Biosafety", "Access to genetic resources and sharing of benefits",
            "Substances that deplete the ozone layer", "Emissions of greenhouse gases"]),
   ["(a)-(iii), (b)-(i), (c)-(iv), (d)-(ii)", "(a)-(iv), (b)-(iii), (c)-(i), (d)-(ii)",
    "(a)-(iii), (b)-(iv), (c)-(ii), (d)-(i)", "(a)-(iii), (b)-(iv), (c)-(i), (d)-(ii)"], "D",
   "The Montreal Protocol (1987) phases out ozone-depleting substances; the Kyoto Protocol (1997) set "
   "emission targets; the Cartagena (2000) and Nagoya (2010) Protocols belong to the Convention on Biological "
   "Diversity.", "agreements"),

 Q("The International Solar Alliance was launched in 2015 by India and France. Its headquarters are at:",
   ["Gurugram, India", "Paris, France", "Geneva, Switzerland", "Nairobi, Kenya"], "A",
   "The Alliance, launched at the Paris climate conference to promote solar energy, has its headquarters at "
   "Gurugram in India.", "agreements"),

 Q("Consider the statements about the Rio Earth Summit of 1992:"
   + st("It produced the Rio Declaration and Agenda 21.",
        "The UN Framework Convention on Climate Change was opened for signature there.",
        "The Convention on Biological Diversity was opened for signature there.",
        "It adopted the Montreal Protocol.")
   + "Which of the statements are correct?",
   ["I and II only", "II and III only", "I, II and III only", "I, II, III and IV"], "C",
   "The Montreal Protocol dates from 1987, five years before Rio, so (IV) is false. Rio produced the Rio "
   "Declaration, Agenda 21 and the Forest Principles, and opened the two conventions for signature.", "agreements"),
]
