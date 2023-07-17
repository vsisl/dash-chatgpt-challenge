"""Home page
"""
import dash
import time
import numpy as np
import json
from dash import Input, Output, State, html, callback, dcc, ALL
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_app.generalutils import (
    get_completion,
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


dash.register_page(__name__, path="/")

# --- PAGE LAYOUT
layout = dmc.Grid(
    [
        dmc.Col(
            span=12,
            children=[
                dmc.Space(h=50),
                dmc.Center(
                    [
                        # TODO: replace this logo with different one, use the vectorized version of the logo (available)
                        dmc.Image(
                            src=r"/assets/putin.png",
                            alt="PropagandaBot",
                            style={"width": "375px"},
                        ),
                    ]
                ),
                dmc.Space(h=30),
            ],
        ),
        dmc.Col(
            span=12,
            children=[
                dmc.Center(
                    [
                        dmc.Group(
                            children=[
                                dmc.Card(
                                    children=[
                                        dmc.Group(
                                            [
                                                dmc.Text("Analyse", weight=500),
                                                dmc.Badge(
                                                    "Recommended",
                                                    color="green",
                                                    variant="light",
                                                ),
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
                                            href="/analyse",
                                        ),
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
                                                dmc.Badge(
                                                    "Advanced",
                                                    color="orange",
                                                    variant="light",
                                                ),
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
                                            href="/generate",
                                        ),
                                    ],
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={"width": 350},
                                ),
                            ]
                        )
                    ]
                )
            ],
        ),
    ]
)
