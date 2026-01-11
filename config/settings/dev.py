from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

MIDDLEWARE.insert(
    0,
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)
