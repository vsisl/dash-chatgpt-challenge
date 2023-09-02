from dash import Input, Output, State, html, callback, dcc, ALL
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

#######################################################################################
#################################### ANALYSIS PART ####################################
#######################################################################################
# title of the analysis part of the project
title_analysis = dmc.Center(
    children=[
        dmc.Space(h="xl"),
        html.H1(
            children=[
                "Analyze propaganda",
                # "Analyze a text with ",
                # html.Br(),
                # html.Span(
                #     "PropagandaBot",
                #     style={
                #         "font-family": "Propaganda",  # custom free font, located in /assets
                #         "background": "linear-gradient(to right, #ff0000, #0600ff)",
                #         "-webkit-background-clip": "text",
                #         "-webkit-text-fill-color": "transparent",
                #     },
                # ),
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

# call to action text that pops up when using the analysis part for longer time
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


# article info that appears when 'Try Example' is clicked
def article_info(label):
    article_information = [
        html.Br(),
        html.Br(),
        dmc.Center(
            children=[
                html.H3(
                    children=[
                            dmc.Tooltip(
                                multiline=True,
                                position="left",
                                withArrow=True,
                                width=420,
                                transition="fade",
                                transitionDuration=200,
                                label=label,
                                children=[dmc.Group([DashIconify(icon="ep:info-filled", width=20, color="#DEDEDE"), dmc.Text("Where does this example come from?", color="gray", size="md")])],
                            ),
                    ],
                    style={"display": "inline-block"},
                ),
            ],
        )
    ]
    return article_information

# column - text input used in the analysis part of the project
column_input_analyse = dmc.Center(
    children=[
        dmc.Container(
            style={"marginBottom": 20, "padding": 10},
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

# big block storing all the components forming the analysis output
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

# used for storing dictionary obtained by classification, then the value is used for different callback
hidden_comp = dcc.Store(id="hidden-comp")

# footer used in landing page and analysis part
footer_analysis = dmc.Container(
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
                                    # "font-family": "Propaganda",  # custom free font, located in /assets
                                    "background": "#858585",
                                    # "background": "#2e2d2d",
                                    "-webkit-background-clip": "text",
                                    "-webkit-text-fill-color": "transparent",
                                },
                            ),
                            href="/"
                        )
                    ]
                ),
                html.Br(),
                dmc.Center(
                    [
                        dmc.Anchor(
                            DashIconify(icon="ion:logo-github", color="gray", width=20),
                            href="https://github.com/vsisl/dash-chatgpt-challenge/",
                        ),
                        dmc.Space(w=25),
                        dmc.Anchor(
                            dmc.Text("Authors", color="gray"),
                            # DashIconify(icon="bi:linkedin", color="gray", width=20),
                            href="/authors",
                        ),
                    ]
                ),
            ]
        )
    ],
    style={"position": "relative", "bottom": 0, "top": 30}
)

#######################################################################################
################################### GENERATIVE PART ###################################
#######################################################################################
# title of the generative part of the project
title_generate = dmc.Center(
    children=[
        dmc.Space(h="xl"),
        html.H1(
            children=[
                "Generate propaganda",
                # "Generate a text with ",
                # html.Br(),
                # html.Span(
                #     "PropagandaBot",
                #     style={
                #         "font-family": "Propaganda",  # custom free font, located in /assets
                #         "background": "linear-gradient(to right, #ff0000, #0600ff)",
                #         "-webkit-background-clip": "text",
                #         "-webkit-text-fill-color": "transparent",
                #     },
                # ),
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

# column - text input used in the analysis part of the project
column_input_generate = dmc.Center(
    children=[
        dmc.Container(
            style={"marginBottom": 20, "padding": 10},
            children=[
                dmc.Group(
                    children=[
                        dmc.Tooltip(
                            multiline=True,
                            withArrow=True,
                            width=320,
                            transition="fade",
                            transitionDuration=200,
                            label="Think of a topic you would like to generate Russian-propaganda-styled text, click "
                                  "'Submit Text' and let the PropagandaBot generate a short example article featuring"
                                  " core techniques typical for propaganda.",
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
                            placeholder="Enter a topic for a propaganda text...",
                            style={"width": 500, "position": "relative"},
                        ),
                        dmc.Button(
                            "Submit Text",
                            id="button-submit-generate",
                            color="red",
                            style={"height": 66},
                            n_clicks=0,
                        ),
                    ]
                )
            ],
        )
    ],
)

# big block storing all the components forming the analysis output in the generative part
container_generation_results = dcc.Loading(
    type="default",
    parent_className="loading_wrapper",  # to apply custom CSS
    children=[
        dmc.Grid(
            id="container-all_generation",
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
                    id="generation_results-container",
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
                            id="found-techniques-generation",
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
                            id="explanation-generation",
                            className="sentence_info-container",
                        ),
                    ],
                ),
            ],
        )
    ],
)

# hidden component used for storing dictionary with classified text, then used as input for different callback
hidden_comp_generation = dcc.Store(id="hidden-comp-generation")

# footer used in the generative part
footer_generation = dmc.Container(
    children=[
        dmc.Footer(
            id="footer-generation",
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
                                    # "font-family": "Propaganda",  # custom free font, located in /assets
                                    "background": "#858585",
                                    # "background": "#2e2d2d",
                                    "-webkit-background-clip": "text",
                                    "-webkit-text-fill-color": "transparent",
                                },
                            ),
                            href="/"
                        )
                    ]
                ),
                html.Br(),
                dmc.Center(
                    [
                        dmc.Anchor(
                            DashIconify(icon="ion:logo-github", color="gray", width=20),
                            href="https://github.com/vsisl/dash-chatgpt-challenge/",
                        ),
                        dmc.Space(w=25),
                        dmc.Anchor(
                            dmc.Text("Authors", color="gray"),
                            # DashIconify(icon="bi:linkedin", color="gray", width=20),
                            href="/authors",
                        ),
                    ]
                ),
            ]
        )
    ],
    style={"position": "relative", "bottom": 0, "top": 30}
)

menu = html.Div(
    [
        dmc.Text(id="menu-text", mb="md",  className="mr-3"),
        dmc.Menu(
            [
                dmc.MenuTarget(dmc.Burger(id="burger-button", opened=False)),
                dmc.MenuDropdown(
                    [
                        dmc.MenuItem("Home", id="button-1", n_clicks=0, href="/"),
                        dmc.MenuItem("About", id="button-2", n_clicks=0, href="/"),
                        dmc.MenuItem(
                            "Project Repository",
                            href="https://github.com/vsisl/dash-chatgpt-challenge/",
                            target="_blank",
                            icon=DashIconify(icon="radix-icons:external-link"),
                        ),
                        dmc.MenuItem(
                            "About the challenge",
                            href="https://community.plotly.com/t/dash-chatgpt-app-challenge/75763",
                            target="_blank",
                            icon=DashIconify(icon="radix-icons:external-link"),
                        ),
                    ]
                ),
            ]
        ),
    ],
    style={"margin-left": "75vw", "margin-right": 0},
)

# global header with dropdown menu
header = dmc.Header(
    height=60,
    fixed=True,
    children=[menu],
    withBorder=False,
)

authors = dmc.Container(
    children=[
        dmc.Space(h=75),
        dmc.Center(dmc.Title(f"Authors of PropagandaBot", order=1),),
        dmc.Space(h=35),
        dmc.Grid(
            children=[
                dmc.Col(
                    children=[
                        dmc.Card(
                            children=[
                                dmc.Group(
                                    [
                                        # dmc.Avatar("VS", color="cyan", radius="xl"),
                                        html.P("Václav Šísl", style={"font-weight": "bold"}),
                                        dmc.Anchor(
                                            DashIconify(icon="bi:linkedin", color="gray", width=20),
                                            href="https://ch.linkedin.com/in/vaclav-sisl",
                                        ),
                                    ],
                                    position="apart",
                                    mt="md",
                                    mb="xs",
                                ),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": 350},
                        )
                    ],
                    span=4
                ),
                dmc.Col(
                    children=[
                        dmc.Card(
                            children=[
                                dmc.Group(
                                    [
                                        # dmc.Avatar("VS", color="cyan", radius="xl"),
                                        html.P("Christian Horvat", style={"font-weight": "bold"}),
                                        dmc.Anchor(
                                            DashIconify(icon="bi:linkedin", color="gray", width=20),
                                            href="https://ch.linkedin.com/in/christian-horvat-466048214",
                                        ),
                                    ],
                                    position="apart",
                                    mt="md",
                                    mb="xs",
                                ),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": 350},
                        )
                    ],
                    span=4
                ),
                dmc.Col(
                    children=[
                        dmc.Card(
                            children=[
                                dmc.Group(
                                    [
                                        # dmc.Avatar("VS", color="cyan", radius="xl"),
                                        html.P("Jan Bureš", style={"font-weight": "bold"}),
                                        dmc.Anchor(
                                            DashIconify(icon="bi:linkedin", color="gray", width=20),
                                            href="https://www.linkedin.com/in/jan-bure%C5%A1-6b2283216/",
                                        ),
                                    ],
                                    position="apart",
                                    mt="md",
                                    mb="xs",
                                ),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": 350},
                        )
                    ],
                    span=4
                ),
            ]
        ),
    ]
)