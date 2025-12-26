from dynaconf import Dynaconf

# This loads settings from settings.toml and .env
settings = Dynaconf(
    envvar_prefix="NEWSAPP", 
    settings_files=["settings.toml"],
    environments=True,
    load_dotenv=True,
)