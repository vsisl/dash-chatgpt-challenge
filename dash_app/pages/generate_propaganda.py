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
            hidden_comp_generation
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
    prompt = f"""
        Write the text delimited by triple backticks \
        in form of a really short russian propaganda breaking news. \
        Write the text in English.
        ```{input_text}```
        """
    output_text, output_tokens = get_completion(prompt)

    sentences = extract_sentences(output_text)

    classified_sentences, ranking, n_tokens = classify_sentences(sentences)
    # caution: ranking starts with the lowest
    n_tokens += output_tokens

    output_children = render(classified_sentences, ranking=ranking)

    return \
        output_children, \
        {
            "opacity": 1,
            "visibility": "visible",
            "transition": "opacity 1.0s ease",
            "min-height": 400,
        }, \
        False,\
        classified_sentences


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
    ctx = dash.callback_context
    if not ctx.triggered:
        return "", ""
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        mark_index = json.loads(button_id)["index"]

        if content[str(mark_index)]["classes"] == ['']:
            return " ", " "
        techniques = content[str(mark_index)]["classes"]

        techniques_children = []
        for i, technique in enumerate(techniques):
            techniques_children.append(style_technique(technique))

        explanation = content[str(mark_index)]["explain"]

        explanation_children = [
            style_explanation(expl, technique)
            for expl, technique in zip(explanation, techniques)
        ]

        return techniques_children, explanation_children