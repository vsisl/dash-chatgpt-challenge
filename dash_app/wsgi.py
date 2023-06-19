"""This is na entrypoint for Gunicorn (production server for the Dash app).

To run the app in production, execute the following command from the repository root folder:
    $ gunicorn dash_app.wsgi:application ----bind=0.0.0.0:80 --workers=2*n_cpu+1 --timeout=300 --log-level=info
"""
from dash_app.app import app

application = app.server

if __name__ == "__main__":
    application.run()
