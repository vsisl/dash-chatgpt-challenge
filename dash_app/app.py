"""This is the entrypoint for the Dash app.

To run the app (development environment only), execute the following command from the repository root folder:
    $ python dash_app/app.py

"""
import dash
from dash import Dash, html, dcc, DiskcacheManager, CeleryManager
import dash_bootstrap_components as dbc
from celery_app.app import celery_app

# MAIN APP LAYOUT

# logo and title for navigation bar
navbar_logo_and_title = html.A(
    # Use row and col to control vertical alignment of logo / brand
    dbc.Row(
        [
            # TODO: we can put a logo for our app here (probably some open-source icon?)
            # dbc.Col(html.Img(src='assets/favicon.ico', height='50px')),
            dbc.Col(
                [
                    dbc.NavbarBrand(
                        "Amazing dash/chatGPT app",
                        className="ms-2",
                        # style={'fontSize': '2.0rem', 'color': '#36738a', 'fontWeight': '200'}
                    )
                ]
            ),
        ],
        align="end",
        className="g-0",
    ),
    href="/",
    style={"textDecoration": "none"},
)

# items for navigation bar
navbar_options = dbc.Row(
    [
        dbc.Nav(
            [
                dbc.NavItem(
                    dbc.NavLink(
                        "Project repo on GitHub",
                        href="https://github.com/vsisl/dash-chatgpt-challenge",
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        "Challenge description",
                        href="https://community.plotly.com/t/dash-chatgpt-app-challenge/75763",
                    )
                ),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("PLACEHOLDER", href="", disabled=True)
                        # TODO: we can put more links here if needed
                    ],
                    nav=True,
                    in_navbar=True,
                    label="More",
                    align_end=True,
                ),
            ]
        )
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

# navigation bar
navbar = dbc.Navbar(
    dbc.Container(
        [
            navbar_logo_and_title,
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                navbar_options,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ],
        fluid=True,
    ),  # fluid=True makes the navbar expand to the full width of the screen
    color="dark",
    dark=True,
    expand="lg",  # specify screen size at which to expand the menu bar, e.g. sm, md, lg etc.
)

background_callback_manager = CeleryManager(celery_app)
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], background_callback_manager=background_callback_manager)
app.title = "Amazing Dash app"

# main app layout
app.layout = dbc.Container(
    [
        # navbar,
        dash.page_container,
    ]
)


if __name__ == "__main__":
    app.run_server(debug=False)
