import os
from pathlib import Path

from .base_settings import env


current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env"


env_name = env("DJANGO_ENV", default="development")

if env_name == "production":
    from .prod_settings import *
else:
    from .dev_settings import *
