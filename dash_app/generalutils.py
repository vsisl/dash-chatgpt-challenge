"""
Utilities & other helper functions.
"""
import re
import ast
import random
import numpy as np
import pandas as pd
from dash import html
from dash_app.gptutils import (
    get_completion,
    get_classification,
    get_classification_cheaper,
    get_classification_christian,
)
import dash_mantine_components as dmc

DEFAULT_LABEL_COLORS = {
    "AtA": "#7aecec",
    "AtFP": "#bfeeb7",
    "BRaH": "#feca74",
    "BaWF": "#ff9561",
    "CO": "#aa9cfc",
    "D": "#c887fb",
    "EM": "#9cc9cc",
    "FW": "#ffeb80",
    "LL": "#ff8197",
    "NCL": "#ff8197",
    "R": "#f0d0ff",
    "S": "#bfe1d9",
    "TtC": "#bfe1d9",
    "WSMRH": "#e4e7d2",
}


# Dictionary: technique name to abbreviation
term_to_abbreviation = {
    "Appeal to Authority": "AtA",
    "Appeal to Fear Prejudice": "AtFP",
    "Bandwagon, Reductio ad hitlerum": "BRaH",
    "Black and White Fallacy": "BaWF",
    "Causal Oversimplification": "CO",
    "Doubt": "D",
    "Exaggeration, Minimisation": "EM",
    "Flag-Waving": "FW",
    "Loaded Language": "LL",
    "Name Calling, Labeling": "NCL",
    "Repetition": "R",
    "Slogans": "S",
    "Thought-terminating Cliches": "TtC",
    "Whataboutism, Straw Man, Red Herring": "WSMRH",
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
    "Name Calling, Labeling": "Labeling the object of the propaganda campaign as either something the target audience "
    "fears, hates, finds undesirable or loves, praises.",
    "Repetition": "Repeating the same message over and over again so that the audience will eventually accept it.",
    "Slogans": "A brief and striking phrase that may include labeling and stereotyping.",
    "Thought-terminating Cliches": " Words or phrases that discourage critical thought and meaningful discussion about "
    "a given topic. They are typically short, generic sentences that offer seemingly "
    "simple answers to complex questions or that distract attention away from other "
    "lines of thought.",
    "Whataboutism, Straw Man, Red Herring": "A technique that attempts to discredit an opponent's position by "
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
        idx = str(i)  # stringified integer
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


def style_name(name):
    """
    Stylize a given name (used for techniques abbreviations) for improved visual presentation purposes.

    This function returns a stylized representation of a technique abbreviation. The technique is
    enclosed in a `html.Span` element and stylized using CSS styles for font size,
    font weight, line-height, text transformation, and more.

    Parameters:
    - name (str): The name that needs to be stylized.

    Returns:
    html.Span: A Dash `html.Span` component containing the stylized name.

    Note:
    The corresponding CSS style "hover-box" located in assets/custom.css
    """
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
    """
    Style a set of children elements inside a visually distinct box with a specified title.

    This function wraps the provided children elements inside a styled `html.Mark` element,
    which serves as a distinct box. The `title` attribute provides additional information
    when hovered over. The box is given a unique ID based on the provided `idx`, which
    can be used for interaction and reference in callback scenarios.

    Parameters:
    - children (list): A list of elements that need to be wrapped inside the styled box.
    - title (str): A descriptive title for the box which appears on hover.
    - idx (int): Index or identifier used to generate a unique ID for the box.

    Returns:
    html.Mark: A styled Dash `html.Mark` component containing the children with the
               specified title and unique ID.
    """
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
    """
    Stylize a given propaganda technique with a Tooltip for enhanced presentation.

    This function returns a stylized representation of a given technique wrapped inside
    a Tooltip. When hovered over, the Tooltip displays the definition of the technique.
    The background color of the technique label is determined based on its abbreviation
    using a default color mapping.

    Parameters:
    - technique (str): The propaganda technique that needs to be stylized.

    Returns:
    dmc.Tooltip: A Dash Tooltip component containing the stylized technique and its definition
                 when hovered over.
    """
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
                    "background-color": DEFAULT_LABEL_COLORS[
                        term_to_abbreviation[technique]
                    ],
                    "transition": "background-color 0.3s ease",
                    "cursor": "default",
                },
            )
        ],
    )


def style_explanation(explanation, technique):
    """
    Style a given explanation text based on the associated technique.

    The function stylizes an explanation text by underlining it. The underline color is
    determined by the technique's abbreviation using a default color mapping.

    Parameters:
    - explanation (str): The text content that needs to be stylized.
    - technique (str): Technique associated with the explanation which determines the underline color.

    Returns:
    html.Span: A Dash html.Span component containing the stylized explanation text.
    """
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
    """
    Style and process an entity (the term is used from text analysis - basically in our case it is a sentence with
    identified techniques) with its associated techniques for display.

    Given the children (text content) of an entity and its associated propaganda techniques,
    this function constructs a stylized representation with a title and abbreviated name
    derived from the techniques. The entity is then wrapped inside a styled box for
    better visual distinction.

    Parameters:
    - children (str or list): The text content of the entity. Can be a string or a list of strings.
    - techniques (list): List of propaganda techniques associated with the entity.
    - idx (int): Index or identifier for the entity.

    Returns:
    obj: A styled box containing the entity text along with its associated techniques.
    """
    # Initialize name and title strings
    name = ""
    title = ""

    # Iterate through each technique and construct the title and name strings
    for technique_label in techniques:
        title += technique_label + ", "
        name += term_to_abbreviation[technique_label] + ", "

    # Remove the trailing comma and space from the title and name
    title = title[:-2]
    name = name[:-2]

    # Convert children to a list if it is a string
    if type(children) is str:
        children = [children]

    # Append the stylized name to the children list
    children.append(style_name(name))

    # TODO: fix a bug - function is highlighting also sentences that do not contain any propaganda techniques
    # NOTE: hopefully the above to do is fixed

    return style_box(children, title, idx)


def render(input_dictionary, ranking=None):
    # TODO: add docstring
    children = []

    for idx, values in input_dictionary.items():
        # if sentence does not contain any propaganda techniques, simply render it as is
        if values["classes"] is None or values["classes"] == []:
            children.append(values["sentence"] + ' ')
        elif ranking is not None:
            last_five_elements = ranking[-5:]
            is_in_last_five = np.isin(int(idx), last_five_elements)
            if not is_in_last_five:
                children.append(values["sentence"] + ' ')
            else:
                labels = values["classes"]
                children.append(
                    entity(children=values["sentence"], techniques=labels, idx=int(idx))
                )
        # if sentence contains propaganda techniques, apply special styling and add labels
        else:
            labels = values["classes"]
            children.append(
                entity(children=values["sentence"], techniques=labels, idx=int(idx))
            )

    return children


def load_random_article():
    """
    Generate random filenames for an article and its associated ranking based on a random number.

    This function generates a random number between 1 and 9, which is then used to
    construct filenames for a corresponding article and its ranking. This is useful
    when there are a set of pre-defined articles and rankings saved with a specific
    naming convention, and one needs to randomly select one of them.

    Returns:
    tuple:
    - str: Filename of the randomly selected article.
    - str: Filename of the ranking associated with the randomly selected article.

    Note:
    It is assumed that the files are saved with a naming convention "article_X.npy"
    and "article_X_ranking.npy" where X is a number between 1 and 9.
    """
    # Generate a random number between 1 and 9
    random_num = random.randint(1, 9)

    # Construct the filename
    article_name = f"article_{random_num}.npy"
    ranking_name = f"article_{random_num}_ranking.npy"

    return article_name, ranking_name
