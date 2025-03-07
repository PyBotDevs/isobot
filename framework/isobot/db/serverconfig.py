"""The framework module library used for managing server setup configurations."""

# Imports
import json
import os
from typing_extensions import Literal, Union
from framework.isobot.colors import Colors as colors

client_data_dir = f"{os.path.expanduser('~')}/.isobot"

# Functions
class ServerConfig:
    def __init__(self):
        print(f"[framework/db/Automod] {colors.green}ServerConfig db library initialized.{colors.end}")

    def load(self) -> dict:
        """Fetches and returns the latest data from the items database."""
        with open(f"{client_data_dir}/database/serverconfig.json", 'r', encoding="utf8") as f: db = json.load(f)
        return db

    def save(self, data: dict) -> int:
        """Dumps all cached data to your local machine."""
        with open(f"{client_data_dir}/database/serverconfig.json", 'w+', encoding="utf8") as f: json.dump(data, f)
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
                "autoresponder": {

                }
            }
            self.save(serverconf)
        return 0
    
    def fetch_raw(self, server_id: int) -> dict:
        """Fetches the current server configuration data for the specified guild id, and returns it as a `dict`."""
        serverconf = self.load()
        return serverconf[str(server_id)]
    
    # Fetch Functions
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
    
    def fetch_autoresponder_configuration(self, server_id: int, *, autoresponder_name: str = None) -> dict:
        """Fetches a `dict` of the current configuration for autoresponders for the specified guild. Returns an empty `dict` if none are set up."""
        if autoresponder_name is not None:
            return self.fetch_raw(server_id)["autoresponder"][autoresponder_name]
        else:
            return self.fetch_raw(server_id)["autoresponder"]

    # Set Functions
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

    # Autoresponder System Functions
    def add_autoresponder(
        self,
        server_id: Union[int, str],
        autoresponder_name: str,
        autoresponder_trigger: str,
        autoresponder_text: str,
        autoresponder_trigger_condition: str = Literal["MATCH_MESSAGE", "WITHIN_MESSAGE"],
        *,
        channel: list = None,
        match_case: bool = False
    ):
        """Adds a new autoresponder configuration for the specified guild, with the provided configuration data. Returns `0` if successful, returns `1` if configuration with same name already exists.\n\nNotes: \n- `autoreponder_name` can be considered as autoresponder id."""
        serverconf = self.load()
        if autoresponder_name not in serverconf[str(server_id)]["autoresponder"].keys():
            serverconf[str(server_id)]["autoresponder"][autoresponder_name] = {
                "autoresponder_trigger": autoresponder_trigger,
                "autoresponder_text": autoresponder_text,
                "autoresponder_trigger_condition": autoresponder_trigger_condition,
                "active_channel": channel,
                "match_case": match_case
            }
            self.save(serverconf)
            return 0
        else: return 1
    
    def remove_autoresponder(self, server_id: Union[int, str], autoresponder_name: str):
        """Removes an existing autoresponder from the specified guild's serverconfig data. Returns `0` if successful, returns `1` if autoresponder does not exist, returns `2` if no autoresponders set up."""
        serverconf: dict = self.load()
        if autoresponder_name in serverconf[str(server_id)]["autoresponder"].keys():
            del serverconf[str(server_id)]["autoresponder"][autoresponder_name]
            self.save(serverconf)
        else:
            if serverconf[str(server_id)]["autoresponder"].keys() == []:
                return 2
            else: return 1
