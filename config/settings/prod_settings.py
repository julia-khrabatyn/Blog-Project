import os

from .base_settings import *
from .logging_config import get_logging_config

DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")
# DATABASE will be added later
