"""This is the entrypoint for the Dash app.

To run the app (development environment only), execute the following command from the repository root folder:
    $ python dash_app/app.py

"""
import dash
from dash import Dash, html, dcc, DiskcacheManager, CeleryManager
import dash_bootstrap_components as dbc
from celery_app.app import celery_app

background_callback_manager = CeleryManager(celery_app)
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], background_callback_manager=background_callback_manager)
app.title = "PropagandaBot"

# --- MAIN APP LAYOUT

# main app layout
app.layout = dbc.Container(
    [
        dash.page_container,
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8000)
