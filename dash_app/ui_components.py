from dash import Input, Output, State, html, callback, dcc, ALL
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

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
    width=6
    # className="w-75 m-2 h-100 p-3 bg-light border rounded-3",
)

# TODO: remove this or move it to different place, maybe CSS file
# useful style definition used across multiple components
style = {
    # "height": 100,
    "marginBottom": 20,
    "padding": 10,
    # "display": "flex",
}

# title of the analysis part of the project
title = dmc.Center(
    children=[
        dmc.Space(h="xl"),
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
        ),
    ],
    style={
        "marginTop": 70,
        "marginBottom": 20,
        "display": "flex",
    },
)

# title of the analysis part of the project
call_to_action = dmc.Center(
    children=[
        html.H3(
            children=[
                dmc.Anchor(
                    dmc.Button(
                        id="go-to-generate",
                        children="Try generating and analyzing a new propaganda text",
                        variant="subtle",
                        leftIcon=DashIconify(icon="emojione-monotone:hammer-and-pick"),
                        color="gray",
                    ),
                    href="/generate",
                ),
            ],
            style={"display": "inline-block"},
        ),
    ],
    id="call-to-action",
    style={"opacity": 0, "visibility": "hidden", "marginTop": 16},
)


# column - text input used in the analysis part of the project
column_input_analyse = dmc.Center(
    children=[
        dmc.Container(
            style=style,
            children=[
                dmc.Group(
                    children=[
                        dmc.Tooltip(
                            multiline=True,
                            withArrow=True,
                            width=320,
                            transition="fade",
                            transitionDuration=200,
                            label="Paste a text, click 'Submit Text' and let the PropagandaBot identify whether it "
                                  "contains any techniques typical for propaganda. At first, you can try playing "
                                  "around with some examples by clicking 'Try Example'.",
                            children=[DashIconify(
                                icon="heroicons:question-mark-circle-20-solid",
                                color="#DEDEDE",
                                width=25,
                                style={"position": "relative", "marginLeft": 0}
                            )],
                        ),
                        dbc.Textarea(
                                id="input-text_to_analyze",
                            maxlength=1300,
                            valid=False,
                            placeholder="Type or paste text here...",
                            style={"width": 500, "position": "relative"},
                        ),
                        dmc.Button(
                            "Submit Text",
                            id="button-submit-original",
                            color="red",
                            style={"height": 66},
                            n_clicks=0,
                        ),
                        dmc.Text(
                            "or",
                            color="dimmed",
                        ),
                        dmc.Button(
                            "Try Example",
                            id="button-try-example",
                            color="blue",
                            style={"height": 66},
                            n_clicks=0,
                        ),
                    ]
                )
            ],
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
            # style={"opacity": 0, "visibility": "hidden", "height": "50vh"},
            style={"opacity": 0, "visibility": "hidden"},
            children=[
                dmc.Tooltip(
                    multiline=True,
                    withArrow=True,
                    width=320,
                    transition="fade",
                    transitionDuration=200,
                    label="The highlighted sentences represent the sentences with the highest confidence score of"
                          " propaganda techniques identification. You can click these sentences and see in the"
                          " right panel which propaganda techniques were found in a sentence and why were they"
                          " identified as a part of the sentence.",
                    children=[DashIconify(
                        icon="heroicons:question-mark-circle-20-solid",
                        color="#DEDEDE",
                        width=25,
                        style={"position": "absolute", "marginLeft": 0}
                    )],
                ),
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
                                dmc.Tooltip(
                                    multiline=True,
                                    withArrow=True,
                                    width=220,
                                    transition="fade",
                                    transitionDuration=200,
                                    label="Find out the techniques identified in a given sentence. Hover over these"
                                          " techniques to see their definitions.",
                                    children=[DashIconify(
                                        icon="heroicons:question-mark-circle-20-solid",
                                        # color="red",
                                        color="#DEDEDE",
                                        width=25,
                                    )],
                                ),
                            ],
                            position="apart",
                        ),
                        dmc.Text(
                            children="",
                            id="found-techniques",
                            className="sentence_techniques-container",
                        ),
                        dmc.Group(
                            [
                                dmc.Text("Explanation", weight=900),
                                dmc.Tooltip(
                                            multiline=True,
                                            withArrow=True,
                                            width=220,
                                            transition="fade",
                                            transitionDuration=200,
                                            label="Find out the explanations of why the above techniques"
                                            " were identified in the sentence. The explanations are underlined"
                                            " with color matching the color of the technique.",
                                            children=[DashIconify(
                                                        icon="heroicons:question-mark-circle-20-solid",
                                                        # color="red",
                                                        color="#DEDEDE",
                                                        width=25,
                                            )],
                                ),
                            ],
                            position="apart",
                        ),
                        dmc.Text(
                            children="",
                            id="explanation",
                            className="sentence_info-container",
                        ),
                    ],
                ),
            ],
        )
    ],
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
    # width=6,
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

hidden_comp = dcc.Store(id="hidden-comp")

left_jumbotron = dbc.Col(
    html.Div(
        [
            html.H4("Wonder how a neutral version would look like?"),
            html.Hr(className="my-2"),
            dbc.Button("Neutralize and compare", color="secondary", outline=True),
        ],
        className="p-5 m-2  bg-light border rounded-3",
        id="jumbotron",
        style={"opacity": 0, "visibility": "hidden"},
    ),
    width=12,
)

footer = dmc.Container(
    children=[
        dmc.Footer(
        id="footer",
        height=110,
        fixed=True,
        withBorder=False,
        children=[
                dmc.Center(
                    children=[
                        dmc.Anchor(
                            html.H4(
                                "PropagandaBot",
                                style={
                                    "font-family": "Propaganda",  # custom free font, located in /assets
                                    "background": "#858585",
                                    # "background": "#2e2d2d",
                                    "-webkit-background-clip": "text",
                                    "-webkit-text-fill-color": "transparent",
                                },
                            ),
                            # TODO: add home address
                            href="http://127.0.0.1:8050/"
                        )
                    ]
                ),
                html.Br(),
                dmc.Center(
                    [
                        DashIconify(icon="ion:logo-github", color="gray", width=20,),
                        dmc.Space(w=25),
                        # dmc.Text(
                        #     "2023",
                        #     color="dimmed",
                        # ),
                        DashIconify(icon="bi:linkedin", color="gray", width=20),
                    ]
                ),
            ]
        )
    ],
    style={"position": "relative", "bottom": 0, "top": 30}
)