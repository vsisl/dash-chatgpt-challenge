"""Home page
"""

import dash
from dash import Input, Output, State, html, callback, dcc
import dash_bootstrap_components as dbc
from dash_app.utilities import get_completion


dash.register_page(__name__, path="/")


### LAYOUTS

# column - text input
column_input = dbc.Col(
    [
        dbc.Textarea(
            id="input-text_to_process",
            placeholder="Type or paste text here...",
            # type="text",      # can be used with dbc.Input
            size="lg",
            minlength=50,
            maxlength=5000,  # can be used to limit nr. of characters
        ),
        dbc.Button(
            id="button-submit",
            children="Submit",
        ),
    ],
    width=6,
)

# column - analysis results
column_output = dbc.Col(
    [
        dcc.Loading(
            type="default",
            parent_className="loading_wrapper",  # to apply custom CSS
            children=[
                dbc.Container(
                    id="container-analysis_results",
                    children="PLACEHOLDER: analysis results with appear here...",
                )
            ],
        )
    ],
    width=6,
)

# page layout
layout = dbc.Container(children=[dbc.Row([column_input, column_output])])

### CALLBACKS


@callback(
    Output(component_id="container-analysis_results", component_property="children"),
    Input(component_id="button-submit", component_property="n_clicks"),
    State(component_id="input-text_to_process", component_property="value"),
    prevent_initial_call=True,  # this prevents callback triggering at page load (before the Submit button is clicked)
)
def process_text(n_clicks, input_text):
    """This is an example callback function.

    Callback functions are used to dynamically populate the content of the app.
    You can think of them as of the "backend" of the app.
    Read more here: https://dash.plotly.com/basic-callbacks

    :param n_clicks: int
    :param input_text: str
    :return: str
    """
    # TODO: make some machine learning magic here
    print("callback fired...")
    # create output - e.g. analysis results or modified input text

    # what do we want chatGPT to do?
    prompt = f"""
    Write the text delimited by triple backticks \
    in form of a russian propaganda breaking news.
    ```{input_text}```
    """
    output_text = get_completion(prompt)

    return output_text
