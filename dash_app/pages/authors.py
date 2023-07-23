"""Generate propaganda article on a given topic
"""
import dash
import time
import numpy as np
import json
from dash import Input, Output, State, callback, ALL
import dash_bootstrap_components as dbc
from dash_app.ui_components import (
    authors,
    footer_analysis,
    header,
)

dash.register_page(__name__, path="/authors")

# --- PAGE LAYOUT
layout = [
    # dbc.Container([header]),
    dbc.Container(
        children=[
            dbc.Row([authors]),
        ],
    ),
    dbc.Container([footer_analysis]),
]