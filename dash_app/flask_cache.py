"""Module for initialising a flask cache for the dash app. Using Redis as the cache DB."""
import os

from flask_caching import Cache

from dash import get_app

app = get_app()
redis_url = os.getenv(
    "REDISTOGO_URL", default="redis://localhost:6379"   # REDISTOGO_URL var from docker-compose file
)
cache = Cache(
    app.server, config={"CACHE_TYPE": "redis", "CACHE_REDIS_URL": redis_url + "/0"}
)
