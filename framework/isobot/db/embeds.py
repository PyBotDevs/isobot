# Imports
import json
from framework.isobot.colors import Colors as colors

# Functions
class Embeds():
    """Initializes the Embed database system."""
    def __init__(self):
        print(f"[framework/db/Embeds] {colors.green}Embeds db library initialized.{colors.end}")

    def load(self) -> dict:
        """Fetches and returns the latest data from the embeds database."""
        with open("database/embeds.json", 'r', encoding="utf8") as f: db = json.load(f)
        return db

    def save(self, data: dict) -> int:
        """Dumps all cached data to your local machine."""
        with open("database/embeds.json", 'w+', encoding="utf8") as f: json.dump(data, f)
        return 0
