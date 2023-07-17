from dash import Input, Output, State, html, callback, dcc, ALL
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

# column - text input (outdated - currently used in the generative part of the project)
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

# column - analysis results (outdated - currently used in the generative part of the project)
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
)

# TODO: remove this or move it to different place, maybe CSS file
# useful style definition used across multiple components
style = {
    "height": 100,
    "marginBottom": 20,
    "padding": 10,
    'display': 'flex',
}

# title of the analysis part of the project
title = dmc.Center(
    children=[
        dmc.Space(h='xl'),
        html.H1(
            children=[
                "Analyze a text with ",
                html.Br(),
                html.Span(
                    "PropagandaBot",
                    style={
                        "font-family": "Propaganda",  # custom free font, located in /assets
                        "background": "linear-gradient(to right, #ff0000, #0600ff)",
                        "-webkit-background-clip": "text",
                        "-webkit-text-fill-color": "transparent",
                    },
                ),
            ],
            style={"display": "inline-block"},
        )],
    style={
        "marginTop": 70,
        "marginBottom": 20,
        'display': 'flex',
    },
)


# column - text input used in the analysis part of the project
column_input_analyse = dmc.Center(
    children=[
        dmc.Container(
            style=style,
            children=[
                dmc.Group(
                    children=[
                        dbc.Textarea(
                                    id="input-text_to_analyze",
                                    placeholder="Type or paste text here...",
                                    style={"width": 550},
                                ),
                        dmc.Button(
                            "Submit Text",
                            id="button-submit-original",
                            color="red",
                            style={"height": 66}
                        ),
                        dmc.Text(
                            "or",
                            color="dimmed",
                        ),
                        dmc.Button(
                            "Try Example",
                            id="button-try-example",
                            color="blue",
                            style={"height": 66}
                        ),
                    ]
                )
            ]
        )
    ],
)


container_analysis_results = dcc.Loading(
            type="default",
            parent_className="loading_wrapper",  # to apply custom CSS
            children=[
                dmc.Grid(
                    id="container-all_analysis",
                    gutter="xl",
                    style={'opacity': 0, 'visibility': 'hidden', "min-height": 100},
                    children=[
                        dmc.Col(
                            id="analysis_results-container",
                            className="analysis_results-container",
                            span=7,
                            children="PLACEHOLDER",
                        ),
                        dmc.Col(
                            span=4,
                            offset=0.2,
                            className="sentence_info-container",  # the same style as above column
                            children=[
                                dmc.Group(
                                    [
                                        dmc.Text("Found techniques", weight=900),
                                        dmc.Badge("PLACEHOLDER", color="red", variant="light"),
                                    ],
                                    position="apart",
                                ),
                                dmc.Text(
                                    children="",
                                    id='found-techniques',
                                    className="sentence_info-container",
                                ),
                                dmc.Group(
                                    [
                                        dmc.Text("Explanation", weight=900),
                                        dmc.Badge("PLACEHOLDER", color="red", variant="light"),
                                    ],
                                    position="apart",
                                ),
                                dmc.Text(
                                    children="",
                                    id='explanation',
                                    className="sentence_info-container",
                                ),

                            ],
                        )
                    ],
                )
            ]
)

# column - information about the sentences
column_sentence_info = dbc.Col(
    [
                dbc.Container(
                    id="container-sentence_info",
                    children="PLACEHOLDER: analysis results will appear here...",
                    style={'opacity': 0, 'visibility': 'hidden'}
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
                    style={'opacity': 0, 'visibility': 'hidden'}
                )

    ],
    className="w-25 m-2 p-3 bg-light border rounded-3",
    width=6,
)

hidden_div = html.Div(id='hidden-div', style={'display': 'none'})

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
        id='jumbotron',
        style={'opacity': 0, 'visibility': 'hidden'}
    ),
    width=12,
)