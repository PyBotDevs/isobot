"""The framework database module for handling IsoCard data."""

# Imports
import json
import time
from framework.isobot.colors import Colors as colors

# Functions
class IsoCard:
    def __init__(self):
        print(f"[framework/db/IsoCard] {colors.green}IsoCard db library initialized.{colors.end}")
    
    def load(self) -> dict:
        """Loads the latest IsoCard database content from local storage."""
        with open("database/isocard.json", "r", encoding="utf-8") as f: data = json.load(f)
        return data
    
    def save(self, data: dict) -> int:
        """Saves the latest cached database to local storage."""
        with open("database/isocard.json", 'w+', encoding="utf-8") as f: json.dump(data, f, indent=4)
        return 0
    
    def fetch_all_cards(self):
        """Fetches a `dict_keys` list of all registered IsoCard numbers in the IsoCard database.\n\n***WARNING:*** This function must **ONLY** be used for validation of IsoCard ownership, and nothing else."""
        isocard_db = self.load()
        return isocard_db.keys()

    def fetch_card_data(self, card_id: int) -> dict:
        """Fetches the raw `dict` data related to the given IsoCard id.\n\nReturns data as `dict` if successful, returns `KeyError` if card id does not exist."""
        isocard_db = self.load()
        return isocard_db[str(card_id)]
    
    def generate(self, new_card_id: int, user_id: int, user_name: str, ssc: int) -> dict:
        """Generates a new IsoCard with the given data, and returns that IsoCard data as a `dict` through the function."""
        isocard_db = self.load()
        isocard_db[str(new_card_id)] = {
            "cardholder_user_id": user_id,
            "cardholder_name": user_name,
            "ssc": ssc, # Special Security Code
            "card_registration_timestamp": round(time.time()),
            "type": "standard",  # Card type
            "config" : {
                "spend_limit": 100000,  # Daily spending limit for IsoCard
                "shared_cardholder_ids": [],  # Other users who can use this card
                "card_label": None
            }
        }
        self.save(isocard_db)
        return isocard_db[str(new_card_id)]
    
    def set_card_label(self, card_id: int, label: str) -> int:
        """Changes the display label for a specific IsoCard."""
        isocard_db = self.load()
        isocard_db[str(card_id)]["config"]["card_label"] = label
        self.save()
        return 0
