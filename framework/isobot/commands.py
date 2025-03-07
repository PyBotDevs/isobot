# Imports
import json
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

    def save(self, data: dict) -> int:
        """Saves the cached database to local machine storage."""
        with open(f"{client_data_dir}/config/commands.json", 'w+', encoding="utf-8") as f: json.dump(data, f)
        return 0

    def fetch_raw(self) -> dict:
        """Returns the commands database in a raw `json` format."""
        return self.load()

    def list_commands(self) -> list:
        """Returns all the added commands as a `list`."""
        cmds = self.load()
        return cmds.keys()

    def command_disabled_flag(self, command: str, status: bool):
        """Enables or disables the `disabled` flag for a command."""
        cmds = self.load()
        cmds[command]["disabled"] = bool
        self.save(cmds)
        return 0

    def command_bugged_flag(self, command: str, status: bool):
        """Enables or disables the `bugged` flag for a command."""
        cmds = self.load()
        cmds[command]["bugged"] = bool
        self.save(cmds)
        return 0

    def add_command(self, command_name: str, stylized_name: str, description: str, command_type: str, usable_by: str, *, cooldown: int = None):
        """Adds a new command entry into the command registry."""
        cmds = self.load()
        cmds[command_name] = {
            "name": stylized_name,
            "description": description,
            "type": command_type,
            "cooldown": cooldown,
            "args": None,
            "usable_by": usable_by,
            "disabled": False,
            "bugged": False
        }
        self.save(cmds)
        return 0

    def remove_command(self, command):
        """Removes a command permanently from the command registry."""
        cmds = self.load()
        del cmds[command]
        self.save(cmds)
        return 0
