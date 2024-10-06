"""The framework module library used for managing server setup configurations."""

# Imports
import json
from framework.isobot.colors import Colors as colors

# Functions
class ServerConfig:
    def __init__(self):
        print(f"[framework/db/Automod] {colors.green}ServerConfig db library initialized.{colors.end}")

    def load(self) -> dict:
        """Fetches and returns the latest data from the items database."""
        with open("database/serverconfig.json", 'r', encoding="utf8") as f: db = json.load(f)
        return db

    def save(self, data: dict) -> int:
        """Dumps all cached data to your local machine."""
        with open("database/serverconfig.json", 'w+', encoding="utf8") as f: json.dump(data, f)
        return 0

    def generate(self, server_id: int) -> int:
        """Generates a new database key for the specified server/guild id in the automod database."""
        serverconf = self.load()
        if str(server_id) not in serverconf:
            serverconf[str(server_id)] = {
                "autorole": None,
                "welcome_message": {
                    "channel": None,
                    "message": None
                },
                "goodbye_message": {
                    "channel": None,
                    "message": None
                },
                "level_up_override_channel": None,
                "verification_role": None,
                "autoresponder": [
                    
                ]
            }
            self.save(serverconf)
        return 0
    
    def fetch_raw(self, server_id: int) -> dict:
        """Fetches the current server configuration data for the specified guild id, and returns it as a `dict`."""
        serverconf = self.load()
        return serverconf[str(server_id)]
    
    def fetch_autorole(self, server_id: int) -> str:
        """Fetches the specified autorole for the server. Returns `None` if not set."""
        return self.fetch_raw(server_id)["autorole"]
    
    def fetch_welcome_message(self, server_id: int) -> dict:
        """Fetches the welcome message and set channel for the server as `dict`.\n\nReturns `None` for `channel` and `message` values if not set."""
        return self.fetch_raw(server_id)["welcome_message"]
    
    def fetch_goodbye_message(self, server_id: int) -> dict:
        """Fetches the goodbye message and set channel for the server as `dict`.\n\nReturns `None` for `channel` and `message` values if not set."""
        return self.fetch_raw(server_id)["goodbye_message"]
    
    def fetch_levelup_override_channel(self, server_id: int) -> str:
        """Fetches the level-up override channel for the specified guild. Returns `None` if not set."""
        return self.fetch_raw(server_id)["level_up_override_channel"]
    
    def fetch_verification_role(self, server_id: int) -> str:
        """Fetches the verified member role for the specified guild. Returns `None` if server verification system is disabled."""
        return self.fetch_raw(server_id)["verification_role"]

    def set_autorole(self, server_id: int, role_id: int) -> int:
        """Sets a role id to use as autorole for the specified guild. Returns `0` if successful."""
        serverconf = self.load()
        serverconf[str(server_id)]["autorole"] = role_id
        self.save(serverconf)
    
    def set_welcome_message(self, server_id: int, channel_id: int, message: str) -> int:
        """Sets a channel id to send a custom welcome message to, for the specified guild. Returns `0` if successful."""
        serverconf = self.load()
        serverconf[str(server_id)]["welcome_message"]["channel"] = channel_id
        serverconf[str(server_id)]["welcome_message"]["message"] = message
        self.save(serverconf)
    
    def set_goodbye_message(self, server_id: int, channel_id: int, message: str) -> int:
        """Sets a channel id to send a custom goodbye message to, for the specified guild. Returns `0` if successful."""
        serverconf = self.load()
        serverconf[str(server_id)]["goodbye_message"]["channel"] = channel_id
        serverconf[str(server_id)]["goodbye_message"]["message"] = message
        self.save(serverconf)
    
    def set_levelup_override_channel(self, server_id: int, channel_id: int) -> int:
        """Sets a level-up override channel id for the specified guild. Returns `0` if successful."""
        serverconf = self.load()
        serverconf[str(server_id)]["level_up_override_channel"] = channel_id
        self.save(serverconf)
    
    def set_verification_role(self, server_id: int, role_id: int) -> int:
        """Sets a verified member role id for the specified guild for the specified guild, and enables server member verification. Returns `0` if successful."""
        serverconf = self.load()
        serverconf[str(server_id)]["verification_role"] = role_id
        self.save(serverconf)
