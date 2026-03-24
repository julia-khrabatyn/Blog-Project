import os
from pathlib import Path

from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env"

load_dotenv(dotenv_path=env_path)

env_name = os.getenv("DJANGO_ENV", "development")

if env_name == "production":
    from .prod_settings import *
else:
    from .dev_settings import *
