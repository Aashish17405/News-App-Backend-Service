import os
from pathlib import Path
from dotenv import load_dotenv
from dynaconf import Dynaconf

# This helps the app find files like '.env' and 'settings.toml'
ROOT_DIR = Path(__file__).parent.parent.parent

load_dotenv(ROOT_DIR / ".env")

settings = Dynaconf(
    settings_files=["settings.toml"], 
    root_path=ROOT_DIR,
    environments=True,
    load_dotenv=True,
)

db_url = os.getenv("DATABASE_URL")
if db_url:
    settings.set("DATABASE_URL", db_url)