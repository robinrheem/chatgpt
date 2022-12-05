"""
Settings module
"""
from pathlib import Path

import typer

APP_NAME = "chatgpt"
SETTINGS_PATH = Path(typer.get_app_dir(APP_NAME)) / "settings.json"
SETTINGS_PATH.parent.mkdir(exist_ok=True, parents=True)
