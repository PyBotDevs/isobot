"""The framework module library used for managing isobot's levelling database."""
# Imports
import json
import os
from framework.isobot.colors import Colors as colors

client_data_dir = f"{os.path.expanduser('~')}/.isobot"

# Functions
class Levelling():
    """Used to initialize the levelling database."""
    def __init__(self):
        print(f"[framework/db/Levelling] {colors.green}Levelling db library initialized.{colors.end}")

    def load(self) -> dict:
        """Fetches and returns the latest data from the levelling database."""
        with open(f"{client_data_dir}/database/levels.json", 'r', encoding="utf8") as f: db = json.load(f)
        return db

    def save(self, data: dict) -> int:
        """Dumps all cached data to your local machine."""
        with open(f"{client_data_dir}/database/levels.json", 'w+', encoding="utf8") as f: json.dump(data, f)
        return 0

    def generate(self, user_id: int) -> int:
        """Generates a new data key for the specified user.\n
        Returns `0` if the request was successful, returns `1` if the data key already exists."""
        levels = self.load()
        if str(user_id) not in levels:
            levels[str(user_id)] = {"xp": 0, "level": 0}
            self.save(levels)
            return 0
        return 1

    def set_level(self, user_id: int, count: int) -> int:
        """Sets a new level for the specified user."""
        levels = self.load()
        levels[str(user_id)]["level"] = count
        self.save(levels)
        return 0

    def set_xp(self, user_id: int, count: int) -> int:
        """Sets a new xp count for the specified user."""
        levels = self.load()
        levels[str(user_id)]["xp"] = count
        self.save(levels)
        return 0

    def add_levels(self, user_id: int, count: int) -> int:
        """Adds a specified amount of levels to the specified user."""
        levels = self.load()
        levels[str(user_id)]["level"] += count
        self.save(levels)
        return 0

    def remove_levels(self, user_id: int, count: int) -> int:
        """Removes a specified amount of levels from the specified user."""
        levels = self.load()
        levels[str(user_id)]["level"] -= count
        self.save(levels)
        return 0

    def add_xp(self, user_id: int, count: int) -> int:
        """Adds a specified amount of xp to the specified user."""
        levels = self.load()
        levels[str(user_id)]["xp"] += count
        self.save(levels)
        return 0

    def remove_xp(self, user_id: int, count: int) -> int:
        """Removes a specified amount of xp from the specified user."""
        levels = self.load()
        levels[str(user_id)]["xp"] -= count
        self.save(levels)
        return 0

    def get_level(self, user_id: int) -> int:
        """Fetches a user's current level."""
        levels = self.load()
        return levels[str(user_id)]["level"]

    def get_xp(self, user_id: int) -> int:
        """Fetches a user's current xp."""
        levels = self.load()
        return levels[str(user_id)]["xp"]

    def get_raw(self):
        """Fetches and returns the raw json data in the levelling database."""
        levels = self.load()
        return levels

    def delete_user(self, user_id: int) -> int:
        """Deletes all user levelling data for the respective user."""
        levels = self.load()
        del levels[str(user_id)]
        self.save(levels)
        return 0
