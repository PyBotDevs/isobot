import json
import time
import datetime

class IsoBankManager():
    def __init__(self, db_path:str, auth_db:str):
        self.db_path = db_path
        self.auth_db = auth_db
        with open(db_path, 'r') as f:
            global accounts
            accounts = json.load(f)
        with open(auth_db, 'r') as f:
            global auth
            auth = json.load(f)

    def save(self):
        with open(self.db_path, 'w+') as f: json.dump(accounts, indent=4)

    def deposit(self, account_id:int, discord_id:int, amount:int):
        if discord_id not in auth[str(account_id)]["discord_ids"]: return "Failed to authorize user"
        accounts["deposited"] += amount
        save()
        return f"Deposited {amount} coins to #{account_id} IsoBank account"

    def withdraw(self, account_id:int, discord_id:int, amount:int):
        if discord_id not in auth[str(account_id)]["discord_ids"]: return "Failed to authorize user"
        accounts["deposited"] -= amount
        save()
        return f"Withdrawn {amount} coins from #{account_id} IsoBank account"


