"""The framework module library used for managing user presence and AFK data."""

# Imports
import json
import time
import os
from framework.isobot.colors import Colors as colors

client_data_dir = f"{os.path.expanduser('~')}/.isobot"

# Functions
class Presence():
    """Used to initialize the User Presence system."""
    def __init__(self):
        print(f"[framework/db/UserData] {colors.green}Presence database initialized.{colors.end}")

    def load(self) -> dict:
        """Fetches and returns the latest data from the presence database."""
        with open(f"{client_data_dir}/database/presence.json", 'r', encoding="utf8") as f: db = json.load(f)
        return db

    def save(self, data: dict) -> int:
        """Dumps all cached data to your local machine."""
        with open(f"{client_data_dir}/database/presence.json", 'w+', encoding="utf8") as f: json.dump(data, f)
        return 0

    def add_afk(self, guild_id: int, user_id: int, response: str) -> int:
        """Generates a new afk data request in the guild for the specified user."""
        presence = self.load()
        exctime = time.time()
        if str(guild_id) not in presence: presence[str(guild_id)] = {}
        presence[str(guild_id)][str(user_id)] = {"type": "afk", "time": exctime, "response": response}
        self.save(presence)
        return 0

    def remove_afk(self, guild_id: int, user_id: int) -> int:
        """Clears the specified user's AFK data.\n\nReturns `0` if the request was successful, returns 1 if the user's AFK is not present in the database (equivalent to `KeyError`)."""
        presence = self.load()
        try:
            del presence[str(guild_id)][str(user_id)]
            self.save(presence)
            return 0
        except KeyError: return 1

    def get_presence(self, guild_id: int, user_id: int) -> dict:
        """Returns a `dict` of the specified user's current AFK status in the guild. Returns `1` if the user is not in the presence database."""
        presence = self.load()
        if str(guild_id) not in presence:
            presence[str(guild_id)] = {}
            self.save(presence)
        if str(user_id) in presence[str(guild_id)]:
            return {
                "afk": True,
                "response": presence[str(guild_id)][str(user_id)]['response'],
                "time": presence[str(guild_id)][str(user_id)]['time']
            }
        else: return 1

    def get_raw(self) -> dict:
        """Returns the entire raw presence database. Can be useful for complex data operations on the database."""
        presence = self.load()
        return presence
