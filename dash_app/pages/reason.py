"""Reason page
"""
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from dash_app.ui_components import (
    header,
    footer_analysis
)


dash.register_page(__name__, path="/reason")

# --- PAGE LAYOUT
layout = dmc.Container([
        dmc.Space(h=75),
        dmc.Center(dmc.Title(f"Why we built PropagandaBot", order=1),),
        dmc.Space(h=35),

        # TODO: add reason here

        dbc.Container([footer_analysis]),
])