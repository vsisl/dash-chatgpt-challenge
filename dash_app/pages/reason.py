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

        dbc.Container(
            [
                dcc.Markdown(["""
                We created PropagandaBot for a couple of key reasons:

                  - **Easy-to-use tool for discovering propaganda**: We wanted everyone to have a simple way to check if a piece of text, like a news article, is using propaganda techniques. Just [feed the text into PropagandaBot](/analyze) and see if your text contains techniques of propaganda.
                    
                  - **Education on propaganda methods**: We also wanted to educate about different propaganda methods. Knowing these can help you spot when someone is trying to sway your opinion using sneaky tactics.
                    
                  - **Showing the risks of AI in spreading propaganda and fake news**: It's important to understand how AI can be used to create manipulative content. We built PropagandaBot to show just how easily this can happen.
                    
                  - **Learning & fun**: Most importantly, we created this project to learn something new and to have fun. You, as the user of PropagandaBot, can have fun too - just think of a hillarious topic for a propaganda article and [let PropagandaBot generate it for you](/generate).
                    
                Finally, we want to express that our goal was not to create a tool that could be misused by bad actors. We believe that PropagandaBot, by itself, isn't more dangerous than any other AI tool out there. Instead, we hope it's a helpful resource for understanding and learning about propaganda in our world today.
                """]),

                html.P([
                    "PropagandaBot was created to participate in the ",
                    html.A(
                        children="Dash-ChatGPT App Challenge",
                        href="https://community.plotly.com/t/dash-chatgpt-app-challenge/75763",
                    ),
                    ".",
                ]),

                footer_analysis
            ]
        ),
])