"""
Utilities & other helper functions.
"""
import re
import ast
import numpy as np
import pandas as pd
from dash import html
from dash_app.gptutils import (
    get_completion,
    get_classification,
    get_classification_cheaper,
    get_classification_christian,
)

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
    """Classifies given sentences for presence of propaganda techniques.

    :param sentences: list of str; list of sentences to be classified;
                        e.g. ['BREAKING NEWS: Russian Propaganda Exposed!',
                              "In a shocking revelation, evidence has emerged exposing the Russian government's ..."]
    :return: out_dict: dict;
                        e.g.
                            {
                                '0': {
                                    'sentence': 'BREAKING NEWS: Russian Propaganda Exposed!',
                                    'classes': ['Flag-Waving'],
                                    'confidence': [0.2],
                                    'explain': ['The sentence uses loaded language and exclamation marks to create a sense of urgency and patriotism, indicating a flag-waving technique.']
                                },
                                '1': {
                                    'sentence': "In a shocking revelation, evidence has emerged exposing the Russian government's ...",
                                    'classes': ['Appeal to Fear Prejudice', 'Appeal to Authority'],
                                    'confidence': [0.5, 0.8],
                                    'explain': ['The sentence uses loaded language ("shocking revelation") and appeals to fear by exposing the Russian government.']
                                }
                            }
             best: numpy.ndarray; array of indices of sentences from variable 'out_dict';
                                    indices are ordered based on propaganda scores (highest to lowest) of individual
                                    sentences
                                e.g.
                                    [1, 0]
             total_tokens: int; total API tokens used by this function call
    """
    out_dict = {}

    confidence_ranking = np.zeros(len(sentences))
    # Iterate through the sentences and assign numbers
    total_tokens = 0
    for i, sentence in enumerate(sentences):
        # TODO: refactor
        idx = str(i)  # strigified integer
        out_dict[idx] = {}

        # TODO: possibly add a boolean switch to be able to choose between
        #  get_classification_christian() and
        #  get_classification_cheaper()
        classification_dict, tokens = get_classification_christian(sentence)
        total_tokens += tokens

        out_dict[idx] = {
            "sentence": sentence,
            "classes": classification_dict["classes"],
            "confidence": classification_dict["confidence"],
            "explain": classification_dict["explain"],
        }

        # find the highest propaganda score among all propaganda techniques for each sentence
        confidence_ranking[i] = np.max(classification_dict["confidence"])

    # find the highest propaganda score among all sentences
    best = np.argsort(confidence_ranking)

    return out_dict, best, total_tokens


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


def entity(children, techniques, idx):
    # TODO: add docstring
    name = ""
    title = ""

    # if there are propaganda techniques in the given sentence, apply special styling
    if techniques is not None:
        for technique_label in techniques:
            title += technique_label + ","
            name += term_to_abbreviation[technique_label] + ","

    if type(children) is str:
        children = [children]

    children.append(style_name(name))

    # TODO: fix a bug - function is highlighting also sentences that do not contain any propaganda techniques

    return style_box(children, title, idx)


def render(classified_sentences):
    # TODO: add docstring
    children = []

    for i, sentence_dict in classified_sentences.items():
        # if sentence does not contain any propaganda techniques, simply render it as is
        if sentence_dict["classes"] is None:
            children.append(sentence_dict["sentence"])

        # if sentence contains propaganda techniques, apply special styling and add labels
        else:
            labels = sentence_dict["classes"]
            # children.append(entity(ary[i][0], term_to_abbreviation[labels[0]], idx))
            children.append(
                entity(
                    children=sentence_dict["sentence"], techniques=labels, idx=int(i)
                )
            )

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
