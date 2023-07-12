"""Home page
"""
import dash
import time
import numpy as np
import json
from dash import Input, Output, State, html, callback, dcc, ALL
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_app.generalutils import get_completion, extract_sentences, classify_sentences, render
from dash_app.ui_components import column_input, column_output, column_neutral, column_sentence_info, left_jumbotron


dash.register_page(__name__, path="/")

# --- PAGE LAYOUT
layout = dmc.Grid([
    dmc.Col(
        span=12,
        children=[
            dmc.Center([
                dmc.Title(children='PropagandaBot', order=1),   # H1 title equivalent
            ])
        ],
    ),

    dmc.Col(
        span=12,
        children=[
            dmc.Center([
                dmc.Group(
                    children=[
                        dmc.Card(
                            children=[
                                # dmc.CardSection(
                                #     dmc.Image(
                                #         src="https://images.unsplash.com/photo-1527004013197-933c4bb611b3?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=720&q=80",
                                #         height=160,
                                #     )
                                # ),
                                dmc.Group(
                                    [
                                        dmc.Text("Analyse", weight=500),
                                        dmc.Badge("Recommended", color="green", variant="light"),
                                    ],
                                    position="apart",
                                    mt="md",
                                    mb="xs",
                                ),
                                dmc.Text(
                                    "Analyse a text to discover if it contains techniques of propaganda.",
                                    size="sm",
                                    color="dimmed",
                                ),

                                dmc.Anchor(
                                    dmc.Button(
                                        "Discover propaganda",
                                        variant="light",
                                        color="blue",
                                        fullWidth=True,
                                        mt="md",
                                        radius="md",

                                    ),
                                    href='/analyse'
                                )
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": 350},
                        ),

                        dmc.Card(
                            children=[
                                dmc.Group(
                                    [
                                        dmc.Text("Generate", weight=500),
                                        dmc.Badge("Advanced", color="orange", variant="light"),
                                    ],
                                    position="apart",
                                    mt="md",
                                    mb="xs",
                                ),
                                dmc.Text(
                                    "Generate propaganda text on a topic of your choice.",
                                    size="sm",
                                    color="dimmed",
                                ),

                                dmc.Anchor(
                                    dmc.Button(
                                        "Create propaganda",
                                        variant="light",
                                        color="blue",
                                        fullWidth=True,
                                        mt="md",
                                        radius="md",
                                    ),
                                    href='/generate'
                                )
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": 350},
                        )
                    ]
                )
            ])
        ]
    )
])


