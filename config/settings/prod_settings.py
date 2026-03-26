import os

from .base_settings import *
from .base_settings import env
from .logging_config import get_logging_config

DEBUG = False
SECRET_KEY = env("SECRET_KEY")
# DATABASE will be added later
