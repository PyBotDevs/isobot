# Imports
import json
import os
from framework.isobot.colors import Colors as colors

# Variables
client_data_dir = f"{os.path.expanduser('~')}/.isobot"

# Classes
class Commands():
    """The library used to fetch information about isobot commands, and manage them."""
    def __init__(self):
        print(f"[Framework/Loader] {colors.green}CommandsDB initialized.{colors.end}")

    def load(self) -> dict:
        """Loads the latest content from the commands database onto memory."""
        with open(f"{client_data_dir}/config/commands.json", 'r', encoding="utf-8") as f: data = json.load(f)
        return data

    def fetch_raw(self) -> dict:
        """Returns the commands database in a raw `json` format."""
        return self.load()

    def list_commands(self) -> list:
        """Returns all the added commands as a `list`."""
        cmds = self.load()
        return cmds.keys()
