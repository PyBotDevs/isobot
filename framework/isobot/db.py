"""A module to manage the databases in isobot."""

# Imports
import json
import discord
import datetime

def get_time(self):
    return datetime.datetime.now().strftime("%H:%M:%S")

class Colors:
    """Contains general stdout colors."""
    cyan = '\033[96m'
    red = '\033[91m'
    green = '\033[92m'
    end = '\033[0m'

class Items(Colors):
    def __init__(self, db_path: str, log_path: str):
        self.db_path = db_path
        self.log_path = log_path
        print(f"[Framework/Loader] {Colors.green}Items database initialized.{Colors.end}")
    
    def new(self, user_id: discord.User) -> int:
        with open(self.db_path, 'r') as f: items = json.load(f)
        if str(user_id) not in items: items[str(user_id)] = {}
        with open("config/shop.json", 'r') as f: shopitem = json.load(f)
        for z in shopitem.keys():
            if z in items[str(user_id)]: pass
            else: items[str(user_id)][str(z)] = 0
        with open(self.db_path, 'w+') as f: json.dump(items, f, indent=4)
        return 0
    
    def add_item(self, user_id: discord.User, item: str, quantity: int) -> int:
        with open(self.db_path, 'r') as f: items = json.load(f)
        items[str(user_id)][item] += quantity
        with open(self.db_path, 'w+') as f: json.dump(items, f, indent=4)
        return 0

    def remove_item(self, user_id: discord.User, item: str, quantity: int) -> int:
        with open(self.db_path, 'r') as f: items = json.load(f)
        items[str(user_id)][item] -= quantity
        with open(self.db_path, 'w+') as f: json.dump(items, f, indent=4)
        return 0
    
class Levels(Colors):
    def __init__(self, db_path: str, log_path: str):
        self.db_path = db_path
        self.log_path = log_path
        print(f"[Framework/Loader] {Colors.green}Levels database initialized.{Colors.end}")
    
    def new(self, user_id: discord.User) -> int:
        with open(self.db_path, 'r') as f: levels = json.load(f)
        if str(user_id) not in levels: levels[str(user_id)] = {
            "xp": 0, 
            "level": 0
        }
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0

    def get_level(self, user_id: discord.User) -> int:
        with open(self.db_path, 'r') as f: levels = json.load(f)
        return levels[str(user_id)]["level"]
    
    def get_xp(self, user_id: discord.User) -> int:
        with open(self.db_path, 'r') as f: levels = json.load(f)
        return levels[str(user_id)]["xp"]
    
    def add_levels(self, user_id: discord.User, level: int):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["level"] += level
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def remove_levels(self, user_id: discord.User, level: int):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["level"] += level
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def reset_level(self, user_id: discord.User):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["level"] = 0
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def add_xp(self, user_id: discord.User, xp: int):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["xp"] += xp
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def remove_xp(self, user_id: discord.User, xp: int):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["xp"] += xp
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def reset_xp(self, user_id: discord.User):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["xp"] = 0
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def edit_level(self, user_id: discord.User, level: int):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["level"] = level
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def edit_xp(self, user_id: discord.User, xp: int):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["xp"] = xp
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0

class Weather(Colors):
    """Class to manage the weather db"""
    def __init__(self, db_path: str, log_path: str):
        self.db_path = db_path
        self.log_path = log_path
        print(f"[Framework/Loader] {Colors.green}Weather database initialized.{Colors.end}")
        
    def new(self, user_id: discord.User):
        with open("database/weather.json", 'r', encoding="utf-8") as f: user_db = json.load(f)
        if str(user_id) not in user_db: user_db[str(user_id)] = {"location": None, "scale": "Celsius"}
        with open("database/weather.json", 'w+', encoding="utf-8") as f: json.dump(user_db, f, indent=4)
        return 0
    
    def set_scale(self, user_id: discord.User, scale: str) -> int:
        with open("database/weather.json", 'r', encoding="utf-8") as f: user_db = json.load(f)
        user_db[str(user_id)]["scale"] = scale
        with open("database/weather.json", 'w+', encoding="utf-8") as f: json.dump(user_db, f, indent=4)
        return 0

    def set_default_location(self, user_id: discord.User, location: str) -> int:
        with open("database/weather.json", 'r', encoding="utf-8") as f: user_db = json.load(f)
        user_db[str(user_id)]["location"] = location
        with open("database/weather.json", 'w+', encoding="utf-8") as f: json.dump(user_db, f, indent=4)
        return 0

    def get_scale(self, user_id: discord.User):
        with open("database/weather.json", 'r', encoding="utf-8") as f: user_db = json.load(f)
        return user_db[str(user_id)]["scale"]

    def get_default_location(self, user_id: discord.User):
        with open("database/weather.json", 'r', encoding="utf-8") as f: user_db = json.load(f)
        return user_db[str(user_id)]["location"]
