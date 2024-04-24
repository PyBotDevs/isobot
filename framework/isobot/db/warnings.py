"""The framework module library used for managing isobot's warnings database."""

# Imports
import json
from framework.isobot.colors import Colors as colors

# Functions
class Warnings:
    """Used to initialize the warnings database."""
    def __init__(self):
        print(f"[framework/db/Warnings] {colors.green}Warnings db library initialized.{colors.end}")

    def load(self) -> dict:
        """Fetches and returns the latest data from the warnings database."""
        with open("database/warnings.json", 'r', encoding="utf8") as f: db = json.load(f)
        return db

    def save(self, data: dict) -> int:
        """Dumps all cached data to your local machine."""
        with open("database/warnings.json", 'w+', encoding="utf8") as f: json.dump(data, f)
        return 0
    
    def generate(self, guild_id: int, user_id: int) -> int:
        """Generates a new database key for the user in the specified guild.\n\nReturns `0` if generation is successful."""
        data = self.load()
        if str(guild_id) not in data:
            data[str(guild_id)] = {}
        if str(user_id) not in data[str(guild_id)]:
            data[str(guild_id)][str(user_id)] = []
        self.save(data)
        return 0

    def add_warning(self, guild_id: int, user_id: int, moderator_id: int, warning_ts: int, reason: str) -> dict:
        """Adds a new warning entry to the user of the specified guild, in the database.\n\nReturns the warning data as a `dict`."""
        data = self.load()
        # TODO: Add warning ids later. For now, just keep warnings in a list variable.
        warning_data = {
            "moderator_id": moderator_id,
            "warning_ts": warning_ts,
            "reason": reason
        }
        data[str(guild_id)][str(user_id)].append(warning_data)
        self.save(data)
        return warning_data
    
    def clear_all_warnings(self, guild_id: int, user_id: int) -> int:
        """Clears all the warnings for the user in the specified guild."""
        data = self.load()
        data[str(guild_id)][str(user_id)] = []
        self.save(data)
        return 0

    def fetch_all_warnings(self, guild_id: int, user_id: int) -> list:
        """Returns a `list` of all the warnings of the user in a specific guild."""
        data = self.load()
        return data[str(guild_id)][str(user_id)]
