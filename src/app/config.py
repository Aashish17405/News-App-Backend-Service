from dynaconf import Dynaconf

# This loads settings from settings.toml and .env
settings = Dynaconf(
    envvar_prefix="NEWS-APP-BACKEND",
    settings_files=["settings.toml"],
    environments=True,
    load_dotenv=True,
)