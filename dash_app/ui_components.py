from dash import Input, Output, State, html, callback, dcc, ALL
import dash_bootstrap_components as dbc

# column - text input
column_input = dbc.Col(
    [
        dbc.Textarea(
            id="input-text_to_process",
            placeholder="Type or paste text here...",
            className="analysis_results-container",
            # type="text",      # can be used with dbc.Input
            size="md",
            minlength=50,
            maxlength=5000,  # can be used to limit nr. of characters
        ),
        dbc.Button(
            id="button-submit",
            children="Submit",
        ),
    ],
    width=12,
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
                    className="analysis_results-container",
                    children="PLACEHOLDER: analysis results will appear here...",
                )
            ],
        )
    ],
    className="w-75 m-2 h-100 p-3 bg-light border rounded-3",
    # width=6,
)


# column - information about the sentences
column_sentence_info = dbc.Col(
    [
        dbc.Container(
            id="container-sentence_info",
            children="PLACEHOLDER: analysis results will appear here...",
            style={"opacity": 0, "visibility": "hidden"},
        )
    ],
    className="w-25 m-2 p-3 bg-light border rounded-3",
    width=6,
)


# column - neutralization results
column_neutral = dbc.Col(
    [
        dbc.Container(
            id="container-neutralization",
            children="PLACEHOLDER: analysis results will appear here...",
            style={"opacity": 0, "visibility": "hidden"},
        )
    ],
    className="w-25 m-2 p-3 bg-light border rounded-3",
    width=6,
)

hidden_div = html.Div(id="hidden-div", style={"display": "none"})

left_jumbotron = dbc.Col(
    html.Div(
        [
            html.H4("Wonder how a neutral version would look like?"),
            html.Hr(className="my-2"),
            # html.P(
            #     "Or, keep it light and add a border for some added definition "
            #     "to the boundaries of your content."
            # ),
            dbc.Button("Neutralize and compare", color="secondary", outline=True),
        ],
        className="p-5 m-2  bg-light border rounded-3",
        id="jumbotron",
        style={"opacity": 0, "visibility": "hidden"},
    ),
    width=12,
)
