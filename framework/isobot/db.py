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
    
    def new(user_id: discord.User) -> int:
        with open(self.db_path, 'r') as f: items = json.load(f)
        if str(user_id) not in items: items[str(user_id)] = {}
        with open("config/shop.json", "r") as f: 
            all_shopitems = json.load(f)
            shopitem = list()
            for x in all_shopitems: shopitem.append(x)
        for z in shopitem.keys():
            if z in items[str(user_id)]: pass
            else: items[str(user_id)][str(z)] = 0
        with open(self.db_path, 'w+') as f: json.dump(items, f, indent=4)
        return 0
    
    def add_item(user_id: discord.User, item: str, quantity: int) -> int:
        with open(self.db_path, 'r') as f: items = json.load(f)
        items[str(user_id)][item] += quantity
        with open(self.db_path, 'w+') as f: json.dump(items, f, indent=4)
        return 0

    def remove_item(user_id: discord.User, item: str, quantity: int) -> int:
        with open(self.db_path, 'r') as f: items = json.load(f)
        items[str(user_id)][item] -= quantity
        with open(self.db_path, 'w+') as f: json.dump(items, f, indent=4)
        return 0
    
class Levels(Colors):
    def __init__(self, db_path: str, log_path: str):
        self.db_path = db_path
        self.log_path = log_path
        print(f"[Framework/Loader] {Colors.green}Levels database initialized.{Colors.end}")
    
    def new(user_id: discord.User) -> int:
        with open(self.db_path, 'r') as f: levels = json.load(f)
        if str(user_id) not in levels: levels[str(user_id)] = {
            "xp": 0, 
            "level": 0
        }
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0

    def get_level(user_id: discord.User) -> int:
        with open(self.db_path, 'r') as f: levels = json.load(f)
        return levels[str(user_id)]["level"]
    
    def get_xp(user_id: discord.User) -> int:
        with open(self.db_path, 'r') as f: levels = json.load(f)
        return levels[str(user_id)]["xp"]
    
    def add_levels(user_id: discord.User, level: int):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["level"] += level
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def remove_levels(user_id: discord.User, level: int):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["level"] += level
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def reset_level(user_id: discord.User):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["level"] = 0
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def add_xp(user_id: discord.User, xp: int):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["xp"] += xp
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def remove_xp(user_id: discord.User, xp: int):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["xp"] += xp
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def reset_xp(user_id: discord.User):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["xp"] = 0
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def edit_level(user_id: discord.User, level: int):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["level"] = level
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
    def edit_xp(user_id: discord.User, xp: int):
        with open(self.db_path, 'r') as f: levels = json.load(f)
        levels[str(user_id)]["xp"] = xp
        with open(self.db_path, 'w+') as f: json.dump(levels, f, indent=4)
        return 0
    
