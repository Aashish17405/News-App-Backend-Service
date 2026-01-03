@echo off
set ENV_FOR_DYNACONF=development
rem Use 'uv' to run the module inside the project's virtualenv
uv run python -m src.app.main --reload