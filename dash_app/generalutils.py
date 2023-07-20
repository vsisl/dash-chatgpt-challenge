"""
Utilities & other helper functions.
"""
import re
import ast
import numpy as np
import pandas as pd
from dash import html
from gptutils import get_completion, get_classification, get_classification_cheaper
import dash_mantine_components as dmc

# TODO: probably remove this - my initial thought was to use different colors for different techniques, but generally
#       there are multiple techniques present in a sentence
DEFAULT_LABEL_COLORS = {
    "AtA": "#7aecec",
    "AtFP": "#bfeeb7",
    "BoRaH": "#feca74",
    "BaWF": "#ff9561",
    "CO": "#aa9cfc",
    "D": "#c887fb",
    "EoM": "#9cc9cc",
    "FW": "#ffeb80",
    "LL": "#ff8197",
    "NCoL": "#ff8197",
    "R": "#f0d0ff",
    "S": "#bfe1d9",
    "TtC": "#bfe1d9",
    "WoSMoRH": "#e4e7d2",
}


# Dictionary: technique name to abbreviation
term_to_abbreviation = {
    "Appeal to Authority": "AtA",
    "Appeal to Fear Prejudice": "AtFP",
    "Bandwagon, Reductio ad hitlerum": "BoRaH",
    "Black and White Fallacy": "BaWF",
    "Causal Oversimplification": "CO",
    "Doubt": "D",
    "Exaggeration, Minimisation": "EoM",
    "Flag-Waving": "FW",
    "Loaded Language": "LL",
    "Name Calling or Labeling": "NCoL",
    "Repetition": "R",
    "Slogans": "S",
    "Thought-terminating Cliches": "TtC",
    "Whataboutism or Straw Man or Red Herring": "WoSMoRH",
}

# Dictionary: abbreviation to technique name
abbreviation_to_term = {v: k for k, v in term_to_abbreviation.items()}

term_to_defintion = {
    "Appeal to Authority": "Stating that a claim is true simply because a valid authority or expert on the issue said "
                           "it was true, without any other supporting evidence offered.",
    "Appeal to Fear Prejudice": "Seeking to build support for an idea by instilling anxiety and/or panic in the "
                                "population towards an alternative.",
    "Bandwagon, Reductio ad hitlerum": "Attempting to persuade the target audience to join in and take the course of "
                                       "action because 'everyone else is taking the same action'",
    "Black and White Fallacy": "Presenting two alternative options as the only possibilities, when in fact more "
                               "possibilities exist. As an the extreme case, tell the audience exactly what actions"
                               " to take, eliminating any other possible choices.",
    "Causal Oversimplification": "Assuming a single cause or reason when there are actually multiple causes for an "
                                 "issue.",
    "Doubt": "Questioning the credibility of someone or something.",
    "Exaggeration, Minimisation": "Either representing something in an excessive manner: making things larger, better, "
                                  "worse (e.g., 'the best of the best', 'quality guaranteed') or making something seem"
                                  " less important or smaller than it really is (e.g., saying that an insult was just "
                                  "a joke). ",
    "Flag-Waving": "Playing on strong national feeling (or to any group; e.g., race, gender, political preference) to"
                   " justify or promote an action or idea.",
    "Loaded Language": "Using specific words and phrases with strong emotional implications (either positive "
                       "or negative) to influence an audience.",
    "Name Calling or Labeling": "Labeling the object of the propaganda campaign as either something the target audience "
                                "fears, hates, finds undesirable or loves, praises.",
    "Repetition": "Repeating the same message over and over again so that the audience will eventually accept it.",
    "Slogans": "A brief and striking phrase that may include labeling and stereotyping.",
    "Thought-terminating Cliches": " Words or phrases that discourage critical thought and meaningful discussion about "
                                   "a given topic. They are typically short, generic sentences that offer seemingly "
                                   "simple answers to complex questions or that distract attention away from other "
                                   "lines of thought.",
    "Whataboutism or Straw Man or Red Herring": "A technique that attempts to discredit an opponent's position by "
                                                "charging them with hypocrisy without directly disproving their "
                                                "argument, when an opponent's proposition is substituted with a similar "
                                                "one which is then refuted in place of the original proposition or "
                                                "introducing irrelevant material to the issue being discussed, so "
                                                "that everyone's attention is diverted away from the points made.",
}

def extract_sentences(text):
    """
    Extracts sentences from the given text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of strings representing the extracted sentences.
    """

    # Split the text into sentences using regular expressions
    sentences = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))

    # Remove leading and trailing whitespaces from each sentence
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    return sentences


def classify_sentences(sentences):
    # Create an empty ndarray to store the sentences and their numbers
    ary = np.empty((len(sentences), 2), dtype=object)

    # Iterate through the sentences and assign numbers
    for i, sentence in enumerate(sentences):
        what = ast.literal_eval(get_classification_cheaper(sentence))
        print(what)
        ary[i][0] = sentence
        # ary[i][1] = ast.literal_eval(get_classification(sentence))
        ary[i][1] = what
        print(ary[i][0], ary[i][1])

    return ary


# corresponding style "hover-box" located in assets/custom.css
def style_name(name):
    return html.Span(
        name,
        style={
            "font-size": "0.8em",
            "font-weight": "bold",
            "line-height": "1",
            "border-radius": "0.35em",
            "text-transform": "uppercase",
            "vertical-align": "middle",
            "margin-left": "0.5rem",
        },
        className="hover-box",
    )


# corresponding style "hover-text" located in assets/custom.css
def style_box(children, title, idx):
    return html.Mark(
        children,
        id={"type": "mark", "index": idx},
        title=title,
        style={
            "padding": "0.45em 0.6em",
            "margin": "0 0.25em",
            "line-height": "1",
            "border-radius": "0.35em",
            "background-color": f"rgba(#fffdc9, 0)",
            "transition": "background-color 0.3s ease",
            "cursor": "default",
        },
        className="hover-box",
    )


def style_technique(technique):
    return dmc.Tooltip(
        multiline=True,
        withArrow=True,
        width=320,
        transition="fade",
        transitionDuration=200,
        label=term_to_defintion[technique],
        children=[
            html.Mark(
                technique,
                style={
                    "padding": "7px",
                    "margin": "7px",
                    "line-height": "1",
                    "border-radius": "0.35em",
                    "background-color": DEFAULT_LABEL_COLORS[term_to_abbreviation[technique]],
                    "transition": "background-color 0.3s ease",
                    "cursor": "default",
                },
            )
        ]
    )


def style_explanation(explanation, technique):
    return html.Span(
        explanation,
        style={
            "text-decoration": "underline",
            "text-decoration-style": "solid",
            "text-decoration-color": DEFAULT_LABEL_COLORS[
                term_to_abbreviation[technique]
            ],
            "text-decoration-thickness": 3,
        },
    )


def entity(children, techniques, idx):
    name = ""
    title = ""
    for technique_label in techniques:
        title += technique_label + ", "
        name += term_to_abbreviation[technique_label] + ", "
    title = title[:-2]
    name = name[:-2]

    if type(children) is str:
        children = [children]

    children.append(style_name(name))

    return style_box(children, title, idx)


def render(length, ary):
    children = []
    idx = 0
    for i in range(length):
        if ary[i][1] is None:
            children.append(ary[i][0])
        else:
            labels = ary[i][1]
            # children.append(entity(ary[i][0], term_to_abbreviation[labels[0]], idx))
            children.append(entity(ary[i][0], labels, idx))
            idx += 1

    return children


# TODO: make this the only render function
# TODO: change this to work with dictionaries, NOT PANDAS DATAFRAME!!
# used in the analysis part to generate highlighted and not highlighted text
def render_new_dataformat(df):
    children = []
    idx = 0
    for i, row in df.iterrows():
        if pd.isna(row["classes"]):
            children.append(row["sentence"])
        else:
            labels = ast.literal_eval(row["classes"])
            children.append(entity(row["sentence"], labels, idx))
            idx += 1

    print(children)

    return children
