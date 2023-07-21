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
    render_dict,
)
from dash_app.ui_components import (
    column_input_analyse,
    hidden_comp,
    title,
    container_analysis_results,
    call_to_action,
    footer,
)


dash.register_page(__name__, path="/analyse")

# --- PAGE LAYOUT
layout = [
    dbc.Container(
        children=[
            dbc.Row([title]),
            dbc.Row([column_input_analyse]),
            dbc.Row([container_analysis_results]),
            dbc.Row([call_to_action]),
            hidden_comp
        ],
    ),
    dbc.Container([footer]),
]

@callback(
    Output(component_id="analysis_results-container", component_property="children"),
    Output(component_id="container-all_analysis", component_property="style"),
    Output(component_id="footer", component_property="fixed"),
    Output(component_id="call-to-action", component_property="style"),
    Output(component_id="hidden-comp", component_property="data"),
    Input(component_id="button-submit-original", component_property="n_clicks"),
    Input(component_id="button-try-example", component_property="n_clicks"),
    State(component_id="input-text_to_analyze", component_property="value"),
    prevent_initial_call=True,  # this prevents callback triggering at page load (before the Submit button is clicked)
    suppress_callback_exceptions=True,
)
def process_example(n_clicks_1, n_clicks_2, input_text):
    call_to_action_style = {"opacity": 0, "visibility": "hidden", "marginTop": 16}

    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(button_id)

    if n_clicks_1 + n_clicks_2 > 1:
        call_to_action_style = {
            "opacity": 1,
            "visibility": "visible",
            "marginTop": 16,
            "transition": "opacity 1.0s ease",
        }

    if button_id == "button-submit-original":
        sentences = extract_sentences(input_text)

        classified_sentences, ranking, n_tokens = classify_sentences(sentences)
    else:
        classified_sentences = np.load('data/example_0.npy', allow_pickle=True).item()
        ranking = np.load('data/example_0_ranking.npy', allow_pickle=True)
        # sleep some time to show Putin loading
        time.sleep(2)

    # caution: ranking starts with the lowest
    output_text = render_dict(classified_sentences, ranking=ranking)

    return \
        output_text, \
        {
            "opacity": 1,
            "visibility": "visible",
            "transition": "opacity 1.0s ease",
            "min-height": 400,
        }, \
        False,\
        call_to_action_style,\
        classified_sentences

@callback(
    Output(component_id="found-techniques", component_property="children"),
    Output(component_id="explanation", component_property="children"),
    Input(component_id="hidden-comp", component_property="data"),
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
