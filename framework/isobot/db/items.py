"""The framework module library used for managing isobot's items database."""
# Imports
import json
import os
from framework.isobot.colors import Colors as colors
from framework.isobot.shop import ShopData

# Variables
client_data_dir = f"{os.path.expanduser('~')}/.isobot"
shop = ShopData(f"{client_data_dir}/config/shop.json")
shopitem = shop.get_item_ids()

# Functions
class Items():
    """Used to initialize the items database."""
    def __init__(self):
        print(f"[framework/db/Levelling] {colors.green}Items db library initialized.{colors.end}")

    def load(self) -> dict:
        """Fetches and returns the latest data from the items database."""
        with open(f"{client_data_dir}/database/items.json", 'r', encoding="utf8") as f: db = json.load(f)
        return db

    def save(self, data: dict) -> int:
        """Dumps all cached data to your local machine."""
        with open(f"{client_data_dir}/database/items.json", 'w+', encoding="utf8") as f: json.dump(data, f)
        return 0

    def generate(self, user_id: int) -> int:
        """Generates a new database key for the specified user id in the items database."""
        items = self.load()
        if str(user_id) not in items: items[str(user_id)] = {}
        for z in shopitem:
            if z not in items[str(user_id)]:
                items[str(user_id)][str(z)] = 0
        self.save(items)
        return 0

    def add_item(self, user_id: int, item: str, *, quantity: int = 1) -> int:
        """Adds an item of choice to a specific user id."""
        items = self.load()
        items[str(user_id)][item] += quantity
        self.save(items)
        return 0

    def remove_item(self, user_id: int, item: str, *, quantity: int = 1) -> int:
        """Removes an item of choice from a specific user id."""
        items = self.load()
        items[str(user_id)][item] -= quantity
        self.save(items)
        return 0

    def fetch_item_count(self, user_id: int, item: str) -> int:
        """Fetches and returns the amount of a specific item owned by the user."""
        items = self.load()
        return items[str(user_id)][item]

    def delete_user(self, user_id: int) -> int:
        """Deletes all user items data for the respective user."""
        items = self.load()
        del items[str(user_id)]
        self.save(items)
        return 0
