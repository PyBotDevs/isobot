"""The framework module library used for managing server automod configurations."""

# Imports
import json

# Functions
class Automod():
    """Initializes the Automod database system."""
    def __init__(self):
        print("[framework/db/Automod] Automod db library initialized.")

    def load(self) -> dict:
        """Fetches and returns the latest data from the items database."""
        with open("database/automod.json", 'r', encoding="utf8") as f: db = json.load(f)
        return db

    def save(self, data: dict) -> int:
        """Dumps all cached data to your local machine."""
        with open("database/automod.json", 'w+', encoding="utf8") as f: json.dump(data, f)
        return 0

    def generate(self, server_id: int) -> int:
        """Generates a new database key for the specified server/guild id in the automod database."""
        automod_config = self.load()
        if str(server_id) not in automod_config:
            automod_config[str(server_id)] = {
                "swear_filter": {
                    "enabled": False,
                    "keywords": {
                        "use_default": True,
                        "default": ["fuck", "shit", "pussy", "penis", "cock", "vagina", "sex", "moan", "bitch", "hoe", "nigga", "nigger", "xxx", "porn"],
                        "custom": []
                    }
                }
            }
        self.save(automod_config)

    def fetch_config(self, server_id: int) -> dict:
        """Fetches and returns the specified server's automod configuration.\n\nReturns in raw `dict` format."""
        automod_config = self.load()
        return automod_config[str(server_id)]

    def swearfilter_enabled(self, server_id: int, value: bool) -> int:
        """Sets a `bool` value to define whether the server's swear-filter is enabled or not."""
        automod_config = self.load()
        automod_config[str(server_id)]["swear_filter"]["enabled"] = value
        self.save(automod_config)
        return 0

    def swearfilter_usedefaultkeywords(self, server_id: int, enabled: bool) -> int:
        """Sets a `bool` value to define whether the server's swear-filter will use default keywords."""
        automod_config = self.load()
        automod_config[str(server_id)]["swear_filter"]["keywords"]["use_default"] = enabled
        self.save(automod_config)
        return 0

    def swearfilter_addkeyword(self, server_id: int, keyword: str) -> int:
        """Adds a new custom keyword for the server's automod configuration."""
        automod_config = self.load()
        automod_config[str(server_id)]["swear_filter"]["keywords"]["custom"].append(keyword)
        self.save(automod_config)
        return 0

    def swearfilter_removekeyword(self, server_id: int, keyword_id: int) -> int:
        """Removes a keyword (using id) from the server's automod configuration."""
        automod_config = self.load()
        data = automod_config[str(server_id)]["swear_filter"]["keywords"]["custom"]
        data.pop(id-1)
        self.save(automod_config)
        return 0
