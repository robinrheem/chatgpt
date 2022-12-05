"""
Settings module
"""
import json
from json.decoder import JSONDecodeError
from pathlib import Path

import typer


def extract_setting(key: str) -> str:
    with open(SETTINGS_PATH) as s:
        try:
            return json.load(s)[key]
        except JSONDecodeError:
            pass
    return ""


APP_NAME = "chatgpt"
SETTINGS_PATH = Path(typer.get_app_dir(APP_NAME)) / "settings.json"
SETTINGS_PATH.parent.mkdir(exist_ok=True, parents=True)
SETTINGS_PATH.touch(exist_ok=True)
SESSION_TOKEN = extract_setting("sessionToken")
PARENT_ID = extract_setting("parentId")
CONVERSATION_ID = extract_setting("conversationId")
