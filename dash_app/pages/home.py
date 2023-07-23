"""Home page
"""
import dash
import time
import numpy as np
import json
from dash import Input, Output, State, html, callback, dcc, ALL
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from dash_app.ui_components import (
    header,
    footer_analysis
)


dash.register_page(__name__, path="/")

# --- PAGE LAYOUT
layout = dmc.Grid(
    [
        # dbc.Container([header]),
        dmc.Col(
            span=12,
            children=[
                dmc.Space(h=70),
                dmc.Center(
                    [
                        # TODO: replace this logo with different one, use the vectorized version of the logo (available)
                        dmc.Image(
                            # src=r"/assets/putin.png",
                            src=r"/assets/logo-inverse-small.png",
                            alt="PropagandaBot",
                            style={"width": "375px"},
                        ),
                    ]
                ),
                dmc.Space(h=60),
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
                                                html.H4("Analyse",
                                                        style={"weight": 800}),
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
                                            # size="sm",
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
                                            href="/analyze",
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
                                                html.H4("Generate",
                                                        style={"weight": 800}),
                                                # dmc.Badge(
                                                #     "Advanced",
                                                #     color="orange",
                                                #     variant="light",
                                                # ),
                                            ],
                                            position="apart",
                                            mt="md",
                                            mb="xs",
                                        ),
                                        dmc.Text(
                                            "Generate propaganda text on a topic of your choice.",
                                            # size="sm",
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
                ),
                dmc.Space(h=105),
            ],
        ),
        footer_analysis
    ]
)
