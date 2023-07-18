"""Generate propaganda article on a given topic
"""
import dash
import time
import numpy as np
import json
from dash import Input, Output, State, html, callback, dcc, ALL
import dash_bootstrap_components as dbc
from dash_app.generalutils import (
    get_completion,
    get_image,
    extract_sentences,
    classify_sentences,
    render,
)
from dash_app.ui_components import (
    column_input,
    column_output,
    column_neutral,
    column_sentence_info,
    left_jumbotron,
)


dash.register_page(__name__, path="/generate")

# --- PAGE LAYOUT
layout = dbc.Container(
    children=[
        dbc.Row([column_input]),
        dbc.Row([column_output, column_sentence_info]),
        dbc.Row([left_jumbotron]),
    ]
)


# --- CALLBACKS


@callback(
    Output(component_id="container-analysis_results", component_property="children"),
    Output(component_id="container-sentence_info", component_property="style"),
    Output(component_id="jumbotron", component_property="style"),
    Input(component_id="button-submit", component_property="n_clicks"),
    State(component_id="input-text_to_process", component_property="value"),
    prevent_initial_call=True,  # this prevents callback triggering at page load (before the Submit button is clicked)
    suppress_callback_exceptions=True,
)
def process_text(n_clicks, input_text):
    print("callback fired...")

    # what do we want chatGPT to do?
    prompt = f"""
        Write the text delimited by triple backticks \
        in form of a really short russian propaganda breaking news. \
        Write the text in English.
        ```{input_text}```
        """
    output_text, output_tokens = get_completion(prompt)

    print(output_text)

    # Experimental: generate image based on prompt
    # prompt_img = f"""                                                                  # #
    #     What is the main nomen in the text delimited by triple backticks? \            # #
    #     If there is no noun, what is the main verb? \                                  # #
    #     As an output just give me either the noun or the nominalisation of the verb. \ # #
    #     No addition text, just one token.                                              # #
    #     ```{input_text}```                                                             # #
    #     """                                                                            # #
    #                                                                                    # #
    # img_text, img_tokens = get_completion(prompt_img)                                  # #
    # print(output_text)                                                                 # #
    # img = get_image(img_text)                                                            #
    #
    
    sentences = extract_sentences(output_text)
    print(output_text)

    classified_sentences, ranking, n_tokens = classify_sentences(sentences)
    # caution: ranking starts with the lowest
    n_tokens += output_tokens

    output_children = render(len(sentences), classified_sentences)

    return (
        output_children,
        {"opacity": 1, "visibility": "visible", "transition": "opacity 1.0s ease"},
        {"opacity": 1, "visibility": "visible", "transition": "opacity 2.0s ease"},
    )


# callback to update info about which highlighted sentence was selected - the definition of the mark component is
#  located in generalutils.py, in the style_box() function
@callback(
    Output(component_id="container-sentence_info", component_property="children"),
    Input({"type": "mark", "index": ALL}, "n_clicks"),
    State({"type": "mark", "index": ALL}, "children"),
    prevent_initial_call=True,
)
def display_mark_info(n_clicks, mark_values):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Click on a mark..."
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        mark_index = json.loads(button_id)["index"]
        return f"You clicked on {mark_values[mark_index]}."


# TODO: this was the function I used neutralize the text at first
# @callback(
#     Output(component_id="container-neutralization", component_property="children"),
#     Input(component_id="container-analysis_results", component_property="children"),
#     prevent_initial_call=True,  # this prevents callback triggering at page load (before the Submit button is clicked),
#     suppress_callback_exceptions=True
# )
# def neutralize_text(input_text):
#     print("callback 2 fired...")
#
#     # what do we want chatGPT to do?
#     prompt = f"""
#     Rewrite the input text delimited by triple backticks \
#     using just plain and informative language. Remove any emotions \
#     from the text, make it sound like a robot with no emotions wrote it. \
#     The tone has to be really cold. The input text is written in a propaganda-like \
#     style, your job is to remove any signs of propaganda present in the input text.\
#     The input text has either positive or negative sentiment, the text you will generate \
#     has to have neutral sentiment. It should sound like some press agency like Reuters wrote the text.
#     ```{input_text}```
#     """
#     neutral_text = get_completion(prompt)
#
#     return neutral_text
