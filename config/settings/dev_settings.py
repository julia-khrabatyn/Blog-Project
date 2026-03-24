import os

from .base_settings import *  # REFAC: i read that it is appropriate to use import * in situations like this
from .logging_config import get_logging_config

DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY")
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

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
