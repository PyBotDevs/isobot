"""The isobot module to configure internal user/server settings."""

# Imports
import json
from typing import Union, Literal

# Classes and Functions
class Colors:
    """Contains general stdout colors."""
    cyan = '\033[96m'
    red = '\033[91m'
    green = '\033[92m'
    end = '\033[0m'

# Functions
class Configurator(Colors):
    """The class used to initialize the settings module."""
    def __init__(self):
        print(f"[framework/Configurator] {Colors.green}Module initialized.{Colors.end}")

    def generate(self, user_id: int) -> Literal[0, 1]:
        """Generates a new settings configuration for the specified user.
        Does not do anything if a configuration already exists.\n
        Returns 0 if the request was successful, returns 1 if the configuration already exists."""
        with open("config/settings.json", 'r', encoding="utf-8") as f: db = json.load(f)
        if str(user_id) in db.keys(): return 1
        template = {
            "levelup_messages": True
        }
        db[str(user_id)] = template
        with open("config/settings.json", 'w+', encoding="utf-8") as f: json.dump(db, f, indent=4)
        return 0

    def fetch_setting(self, user_id: int, setting: str) -> Union[int, str, bool]:
        """Fetches the current value of a user setting."""
        with open("config/settings.json", 'r', encoding="utf-8") as f: db = json.load(f)
        return db[str(user_id)][setting]

    def edit_setting(self, user_id: int, setting: str, value) -> Literal[0]:
        """Modifies the value of a user setting."""
        with open("config/settings.json", 'r', encoding="utf-8") as f: db = json.load(f)
        db[str(user_id)][setting] = value
        return 0
    def reset(self, user_id: int):
        """Completely resets the specified user's configuration."""
        with open("config/settings.json", 'r', encoding="utf-8") as f: db = json.load(f)
        template = {
            "levelup_messages": True
        }
        db[str(user_id)] = template
        with open("config/settings.json", 'w+', encoding="utf-8") as f: json.dump(db, f, indent=4)
        return 0
        