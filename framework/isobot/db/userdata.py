"""The framework module library used for managing general user data."""

# Imports
import json
import os
from framework.isobot.colors import Colors as colors

client_data_dir = f"{os.path.expanduser('~')}/.isobot"

# Functions
class UserData():
    """Used to initialize the UserData system."""
    def __init__(self):
        print(f"[framework/db/UserData] {colors.green}UserData library initialized.{colors.end}")

    def load(self) -> dict:
        """Fetches and returns the latest data from the levelling database."""
        with open(f"{client_data_dir}/database/user_data.json", 'r', encoding="utf8") as f: db = json.load(f)
        return db

    def save(self, data: dict) -> int:
        """Dumps all cached data to your local machine."""
        with open(f"{client_data_dir}/database/user_data.json", 'w+', encoding="utf8") as f: json.dump(data, f)
        return 0

    def generate(self, user_id: int) -> int:
        """Generates a new data key for the specified user.\n
        Returns `0` if the request was successful, returns `1` if the data key already exists."""
        userdat = self.load()
        if str(user_id) not in userdat.keys():
            userdat[str(user_id)] = {"work_job": None}
            self.save(userdat)
            return 0
        else: return 1

    def fetch(self, user_id: int, key: str) -> str:
        """Fetches the vakue of a data key, from a specific user."""
        userdat = self.load()
        return userdat[str(user_id)][key]

    def set(self, user_id: int, key: str, value) -> int:
        """Sets a new value for a data key, for a specific user."""
        userdat = self.load()
        userdat[str(user_id)][key] = value
        self.save(userdat)
        return 0

    def delete_user(self, user_id: int) -> int:
        """Deletes all user data for the respective user."""
        userdat = self.load()
        del userdat[str(user_id)]
        self.save(userdat)
        return 0
