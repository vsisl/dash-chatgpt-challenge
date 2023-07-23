"""Generate propaganda article on a given topic
"""
import dash
import time
import numpy as np
import json
from dash import Input, Output, State, callback, ALL
import dash_bootstrap_components as dbc
from dash_app.generalutils import (
    load_random_article,
    extract_sentences,
    classify_sentences,
    style_technique,
    style_explanation,
    render,
)
from dash_app.ui_components import (
    column_input_analyse,
    hidden_comp,
    title_analysis,
    container_analysis_results,
    call_to_action,
    footer_analysis,
    header,
    article_info,
)


dash.register_page(__name__, path="/analyze")

# --- PAGE LAYOUT
layout = [
    # dbc.Container([header]),
    dbc.Container(
        children=[
            dbc.Row([title_analysis]),
            dbc.Row([column_input_analyse]),
            dbc.Row([container_analysis_results]),
            dbc.Row([call_to_action]),
            hidden_comp,
        ],
    ),
    dbc.Container([footer_analysis]),
]

# --- CALLBACKS


@callback(
    Output(component_id="analysis_results-container", component_property="children"),
    Output(component_id="container-all_analysis", component_property="style"),
    Output(component_id="footer", component_property="fixed"),
    Output(component_id="call-to-action", component_property="style"),
    Output(component_id="hidden-comp", component_property="data"),
    Input(component_id="button-submit-original", component_property="n_clicks"),
    Input(component_id="button-try-example", component_property="n_clicks"),
    State(component_id="input-text_to_analyze", component_property="value"),
    background=True,
    running=[
        (Output("button-submit-original", "disabled"), True, False),
        (Output("button-try-example", "disabled"), True, False),
    ],
    prevent_initial_call=True,  # this prevents callback triggering at page load (before the Submit button is clicked)
    suppress_callback_exceptions=True,
)
def process_input(n_clicks_1, n_clicks_2, input_text):
    """
    Callback function to process the input text, either from a user submission or from a sample example.

    This function handles the response when either the "Submit Original Text" button or the "Try Example" button
    is clicked. It processes the given input text by extracting sentences, classifying them, and generating
    the output text. It also modifies several components on the page such as displaying analysis results, showing of
    call-to-action, and updating the footer in a way that it has relative position.

    Parameters:
    - n_clicks_1 (int): Number of clicks on the "Submit Original Text" button.
    - n_clicks_2 (int): Number of clicks on the "Try Example" button.
    - input_text (str): Text entered by the user in the input field.

    Returns:
    tuple:
    - list: Output text containing the processed analysis results. This "text" is formed both by plain string sentence
           and highlighted sentences that are html.Mark objects.
    - dict: Style properties for the "all_analysis" container - initially it is hidden and only after this callback is
            executed, it appears.
    - bool: Whether the footer should be fixed.
    - dict: Style properties for the "call-to-action" component -  initially it is hidden and only after the buttons are
            clicked more than once in total, it appears.
    - dict: Data for the "hidden-comp" component to use in the following callback
    """
    # initially the call to action is hidden
    call_to_action_style = {"opacity": 0, "visibility": "hidden", "marginTop": 16}

    # check which button was pushed to decide what action to take
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if n_clicks_1 + n_clicks_2 > 1:
        # if the buttons are clicked more than once in total, the call to action appears
        call_to_action_style = {
            "opacity": 1,
            "visibility": "visible",
            "marginTop": 16,
            "transition": "opacity 1.0s ease",
        }

    if button_id == "button-submit-original":
        # an original text was submitted, so it has to be fully analyzed
        sentences = extract_sentences(input_text)

        classified_sentences, ranking, n_tokens = classify_sentences(sentences)
    else:
        # example was chosen, a random article has to be loaded
        article_name, ranking_name, label_name = load_random_article()
        classified_sentences = np.load(
            "data/example_articles/" + article_name, allow_pickle=True
        ).item()
        ranking = np.load("data/example_articles/" + ranking_name, allow_pickle=True)
        with open("data/example_articles/" + label_name, "r") as file:
            label = file.read()
        # sleep some time to show Putin loading - otherwise the text would be loaded right away
        time.sleep(2)

    output_text = render(classified_sentences, ranking=ranking)

    if button_id == "button-try-example":
        output_text.extend(article_info(label))

    return (
        output_text,
        {
            "opacity": 1,
            "visibility": "visible",
            "transition": "opacity 1.0s ease",
            "min-height": 400,
        },
        False,
        call_to_action_style,
        classified_sentences,
    )


@callback(
    Output(component_id="found-techniques", component_property="children"),
    Output(component_id="explanation", component_property="children"),
    Input(component_id="hidden-comp", component_property="data"),
    Input({"type": "mark", "index": ALL}, "n_clicks"),
    State({"type": "mark", "index": ALL}, "children"),
    prevent_initial_call=True,
)
def display_mark_info(content, n_clicks, mark_values):
    """
    Callback function to display information related to a selected sentence (represented by a html.Mark object).

    When a sentence is clicked, this function retrieves and displays the corresponding techniques and explanations
    associated with that sentence. The techniques are styled and placed in colored boxes, and the explanations are
    styled with underlines that match the color of the technique boxes.

    Parameters:
    - content (dict): A dictionary containing details about each sentence, including its classes (techniques) and
                      explanations.
    - n_clicks (int): Number of times a sentence (html.Mark object) has been clicked. (not needed, just in case)
    - mark_values: All information associated with the selected html.Mark object. (not needed, just in case)

    Returns:
    tuple:
    - list: A list of styled techniques related to the selected sentence.
    - list: A list of styled explanations corresponding to each technique for the selected sentence.
    """
    # wait for a sentence to be clicked, if no sentence is clicked, there are no 'techniques' or 'explanation', so empty
    # strings can be returned
    ctx = dash.callback_context
    if not ctx.triggered:
        return "", ""
    else:
        # a sentence, or more precisely a html.Mark object, was clicked, check the index of this html.Mark and display
        # corresponding information about the techniques and explanation
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        mark_index = json.loads(button_id)["index"]

        # TODO: this could be removed as these type of checks now happen during the creation of the dicitonary
        if content[str(mark_index)]["classes"] == [""]:
            return " ", " "
        techniques = content[str(mark_index)]["classes"]

        techniques_children = []
        for i, technique in enumerate(techniques):
            # each technique that was found is put into a colored box to make it look prettier
            techniques_children.append(style_technique(technique))

        explanation = content[str(mark_index)]["explain"]

        # the explanations are styled in a way that the underlining has the same color as the box around the technique
        explanation_children = [
            style_explanation(expl, technique)
            for expl, technique in zip(explanation, techniques)
        ]

        return techniques_children, explanation_children
