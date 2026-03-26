import os

from .base_settings import *
from .base_settings import env
from .logging_config import get_logging_config

DEBUG = True
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

INSTALLED_APPS += [
    "debug_toolbar",  # "django_extensions",
]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = ["127.0.0.1"]
LOGGING = get_logging_config(DEBUG)
