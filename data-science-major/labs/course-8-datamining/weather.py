"""The classic 14-record weather dataset, shared by several experiments.

This is the dataset every decision-tree and Naive Bayes example in Unit 4 uses,
and it is WEKA's weather.nominal.arff. Keeping one copy here means the labs
cannot drift from the notes.
"""
import pandas as pd

COLUMNS = ["Outlook", "Temperature", "Humidity", "Wind", "Play"]

ROWS = [
    ("Sunny",    "Hot",  "High",   "Weak",   "No"),
    ("Sunny",    "Hot",  "High",   "Strong", "No"),
    ("Overcast", "Hot",  "High",   "Weak",   "Yes"),
    ("Rain",     "Mild", "High",   "Weak",   "Yes"),
    ("Rain",     "Cool", "Normal", "Weak",   "Yes"),
    ("Rain",     "Cool", "Normal", "Strong", "No"),
    ("Overcast", "Cool", "Normal", "Strong", "Yes"),
    ("Sunny",    "Mild", "High",   "Weak",   "No"),
    ("Sunny",    "Cool", "Normal", "Weak",   "Yes"),
    ("Rain",     "Mild", "Normal", "Weak",   "Yes"),
    ("Sunny",    "Mild", "Normal", "Strong", "Yes"),
    ("Overcast", "Mild", "High",   "Strong", "Yes"),
    ("Overcast", "Hot",  "Normal", "Weak",   "Yes"),
    ("Rain",     "Mild", "High",   "Strong", "No"),
]


def weather_frame():
    return pd.DataFrame(ROWS, columns=COLUMNS)


ARFF = """@relation weather

@attribute outlook     {Sunny, Overcast, Rain}
@attribute temperature {Hot, Mild, Cool}
@attribute humidity    {High, Normal}
@attribute windy       {Weak, Strong}
@attribute play        {Yes, No}

@data
""" + "\n".join(",".join(r) for r in ROWS) + "\n"
