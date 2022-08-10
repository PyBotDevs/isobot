import json
import time
import datetime

disabled = False

class IsobankAuth():
    """Use the auth database ONLY."""
    def __init__(self, db_path:str, account_db:str):
        self.db_path = db_path
        self.account_db = account_db
        with open(db_path, 'r') as f:
            global accounts
            accounts = json.load(f)
        with open(account_db, 'r') as f:
            global user_data
            user_data = json.load(f)

    def save(self):
        with open(self.db_path, 'w+') as f: json.dump(accounts, f, indent=4)
        with open(self.db_path, 'w+') as f: json.dump(user_data, f, indent=4)

    def register(self, discord_id:int, auth_id:int):
        if disabled: return "[!] IsoBank is currently disabled."
        if discord_id in accounts: return "[!] That user is already registered!"
        user_count = len(accounts.keys())
        new_id = user_count + 1
        if not str(auth_id).isdigit(): return "\"auth_id\" is not an integer."
        if len(str(auth_id)) != 6: return "\"auth_id\" must be passed as a 6-digit number."
        accounts[str(new_id)] = {"discord_ids": [discord_id], "auth_id": auth_id}
        user_data[str(new_id)] = {"deposited": 0}
        self.save()
        print(f"Discord user ID ({discord_id}) successfully registered as account #{new_id}")
        return accounts[str(new_id)]

    def authorize(self, discord_id:int, account_id:int, auth_id:int):
        if disabled: return "[!] IsoBank is currently disabled."
        wacc = accounts[str(account_id)]
        if wacc["auth_id"] != auth_id: return "Incorrect auth ID"
        if discord_id not in wacc["discord_ids"]:
            wacc["discord_ids"].append(discord_id)
            self.save()
        return wacc
