"""Framework module used to fetch information on isobot's item shop."""

# Imports
import json

# Functions
class ShopData:
    """Initializes the isobot shop."""
    def __init__(self, db_path: str):
        self.db_path = db_path
        with open(db_path, 'r') as f: self.db = json.load(f)

    def get_item_ids(self) -> list:
        """Fetches and returns all of the shop item ids."""
        json_list = list()
        for h in self.db: json_list.append(str(h))
        return json_list

    def get_item_names(self) -> list:
        """Fetches and returns all of the shop item names."""
        json_list = list()
        for h in self.db: json_list.append(str(h["stylized name"]))
        return json_list

    def get_raw_data(self) -> dict:
        """Fetches the entire raw shop data, in a `dict` format."""
        return self.db
