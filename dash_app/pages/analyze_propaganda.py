"""Generate propaganda article on a given topic
"""
import ast

import dash
import time
import numpy as np
import pandas as pd
import json
from dash import Input, Output, State, html, callback, dcc, ALL
import dash_bootstrap_components as dbc
from dash_app.generalutils import (
    get_completion,
    extract_sentences,
    classify_sentences,
    render,
    render_new_dataformat,
    style_technique,
    style_explanation,
)
from dash_app.ui_components import (
    column_input_analyse,
    column_output,
    column_neutral,
    column_sentence_info,
    left_jumbotron,
    title,
    container_analysis_results,
    call_to_action,
    footer,
)


dash.register_page(__name__, path="/analyse")

# TODO / NOTE: so far the only example of cached data, this is the data Christian provided, but it is manually edited so
#  it only contains a few highlighted sentences...
# TODO: change this to work with dictionaries, NOT PANDAS DATAFRAME!! - my mistake...
df = pd.read_csv("data_chris_edited.csv")

# --- PAGE LAYOUT
layout = [
    dbc.Container(
        children=[
            dbc.Row([title]),
            dbc.Row([column_input_analyse]),
            dbc.Row([container_analysis_results]),
            dbc.Row([call_to_action]),
        ],
    ),
    dbc.Container([footer]),
]


@callback(
    Output(component_id="analysis_results-container", component_property="children"),
    Output(component_id="container-all_analysis", component_property="style"),
    Output(component_id="call-to-action", component_property="style"),
    Input(component_id="button-try-example", component_property="n_clicks"),
    prevent_initial_call=True,  # this prevents callback triggering at page load (before the Submit button is clicked)
    suppress_callback_exceptions=True,
)
def process_example(n_clicks):
    call_to_action_style = {"opacity": 0, "visibility": "hidden", "marginTop": 16}
    if n_clicks > 1:
        call_to_action_style = {
            "opacity": 1,
            "visibility": "visible",
            "marginTop": 16,
            "transition": "opacity 1.0s ease",
        }
    # TODO: distinguish between Try Example and Submit Text - only the second one works now and it works incorrectly, it
    #  always loads a polished
    output_text = render_new_dataformat(df)
    # sleep some time to show Putin loading
    time.sleep(1)
    return output_text, {
        "opacity": 1,
        "visibility": "visible",
        "transition": "opacity 1.0s ease",
        "min-height": 400,
    }, call_to_action_style


@callback(
    Output(component_id="analysis_results-container", component_property="children"),
    Output(component_id="container-all_analysis", component_property="style"),
    Output(component_id="call-to-action", component_property="style"),
    Input(component_id="button-submit-original", component_property="n_clicks"),
    State(component_id="input-text_to_analyze", component_property="value"),
    prevent_initial_call=True,  # this prevents callback triggering at page load (before the Submit button is clicked)
    suppress_callback_exceptions=True,
)
def process_original(n_clicks, input_text):
    call_to_action_style = {"opacity": 0, "visibility": "hidden", "marginTop": 16}
    if n_clicks > 1:
        call_to_action_style = {
            "opacity": 1,
            "visibility": "visible",
            "marginTop": 16,
            "transition": "opacity 1.0s ease",
        }
    # TODO: distinguish between Try Example and Submit Text - only the second one works now and it works incorrectly, it
    #  always loads a polished
    output_text = render_new_dataformat(df)
    # sleep some time to show Putin loading
    time.sleep(1)
    return output_text, {
        "opacity": 1,
        "visibility": "visible",
        "transition": "opacity 1.0s ease",
        "min-height": 400,
    }, call_to_action_style


@callback(
    Output(component_id="found-techniques", component_property="children"),
    Output(component_id="explanation", component_property="children"),
    Input({"type": "mark", "index": ALL}, "n_clicks"),
    State({"type": "mark", "index": ALL}, "children"),
    prevent_initial_call=True,
)
def display_mark_info(n_clicks, mark_values):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "", ""
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        mark_index = json.loads(button_id)["index"]
        out = df.loc[df["sentence"] == mark_values[mark_index][0]]

        string_with_techniques = out["classes"].values[0]
        list_of_techniques = ast.literal_eval(string_with_techniques)

        # techniques_children = [style_technique(technique) for technique in list_of_techniques]
        techniques_children = []
        for i, technique in enumerate(list_of_techniques):
            techniques_children.append(style_technique(technique))
            if i != len(list_of_techniques) - 1:
                techniques_children.append(html.Br())

        string_with_explanation = out["explain"].values[0]
        explanation = ast.literal_eval(string_with_explanation)

        explanation_children = [
            style_explanation(expl, technique)
            for expl, technique in zip(explanation, list_of_techniques)
        ]

        return techniques_children, explanation_children
