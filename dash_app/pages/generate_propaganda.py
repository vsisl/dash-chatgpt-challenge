"""Generate propaganda article on a given topic
"""
import dash
import time
import numpy as np
import json
from dash import Input, Output, State, callback, ALL
import dash_bootstrap_components as dbc
from dash_app.generalutils import (
    get_completion,
    extract_sentences,
    classify_sentences,
    style_technique,
    style_explanation,
    render,
)
from dash_app.ui_components import (
    column_input_generate,
    hidden_comp_generation,
    title_generate,
    container_generation_results,
    footer_generation,
    header,
)

dash.register_page(__name__, path="/generate")

# --- PAGE LAYOUT
layout = [
    dbc.Container([header]),
    dbc.Container(
        children=[
            dbc.Row([title_generate]),
            dbc.Row([column_input_generate]),
            dbc.Row([container_generation_results]),
            hidden_comp_generation,
        ],
    ),
    dbc.Container([footer_generation]),
]


# --- CALLBACKS


@callback(
    Output(component_id="generation_results-container", component_property="children"),
    Output(component_id="container-all_generation", component_property="style"),
    Output(component_id="footer-generation", component_property="fixed"),
    Output(component_id="hidden-comp-generation", component_property="data"),
    Input(component_id="button-submit-generate", component_property="n_clicks"),
    State(component_id="input-text_to_analyze", component_property="value"),
    prevent_initial_call=True,  # this prevents callback triggering at page load (before the Submit button is clicked)
    suppress_callback_exceptions=True,
)
def process_text(n_clicks, input_text):
    """
    Callback function to generate and process the text based on user's input.

    This function handles the response when the "Submit Text" button is clicked. It processes the given prompt and
    generates Russian-styled propaganda text that is then analyzed by extracting sentences, classifying them, and
    generating the output content. It also modifies several components on the page such as displaying analysis results
    and updating the footer in a way that it has relative position.

    Parameters:
    - n_clicks (int): Number of clicks on the "Submit Text" button.
    - input_text (str): Prompt to generate Russian-styled propaganda from.

    Returns:
    tuple:
    - list: Output content containing the processed analysis results. This content is formed both by plain string sentence
           and highlighted sentences that are html.Mark objects.
    - dict: Style properties for the "all_analysis" container - initially it is hidden and only after this callback is
            executed, it appears.
    - bool: Whether the footer should be fixed.
    - dict: Data for the "hidden-comp" component to use in the following callback
    """

    # Construct the prompt by embedding the input text within triple backticks and
    # providing additional instructions to be used for generating completions.
    prompt = f"""
        Write the text delimited by triple backticks \
        in form of a really short russian propaganda breaking news. \
        Write the text in English.
        ```{input_text}```
        """

    # Use the constructed prompt to get a generated completion text
    # along with the number of tokens used in the completion.
    output_text, output_tokens = get_completion(prompt)

    # Extract individual sentences from the generated completion text.
    sentences = extract_sentences(output_text)

    # Classify the extracted sentences and obtain their ranking
    # and the number of tokens in each classified sentence.
    classified_sentences, ranking, n_tokens = classify_sentences(sentences)

    # Update the total token count by adding the tokens from the output completion.
    n_tokens += output_tokens

    # Render the classified sentences for display, using the obtained ranking.
    output_children = render(classified_sentences, ranking=ranking)

    return (
        output_children,
        {
            "opacity": 1,
            "visibility": "visible",
            "transition": "opacity 1.0s ease",
            "min-height": 400,
        },
        False,
        classified_sentences,
    )


# callback to update info about which highlighted sentence was selected - the definition of the mark component is
#  located in generalutils.py, in the style_box() function
@callback(
    Output(component_id="found-techniques-generation", component_property="children"),
    Output(component_id="explanation-generation", component_property="children"),
    Input(component_id="hidden-comp-generation", component_property="data"),
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
