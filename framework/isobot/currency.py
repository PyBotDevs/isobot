"""The isobot module for managing the currency db"""

import json
import discord
import datetime

class Colors:
    """Contains general stdout colors."""
    cyan = '\033[96m'
    red = '\033[91m'
    green = '\033[92m'
    end = '\033[0m'

class CurrencyAPI(Colors):
    """The isobot API used for managing currency.
    
    Valid commands:
    - add(user, amount)
    - remove(user, amount)
    - bank_add(user, amount)
    - bank_remove(user, amount)
    - reset(user)
    - deposit(user, amount)
    - withdraw(user, amount)
    - treasury_add(amount)
    - treasury_remove(amount)
    - get_wallet(user)
    - get_bank(user)
    - get_treasury()
    - get_user_networth(user)
    - get_user_count
    - new_wallet(user)
    - new_bank(user)"""

    def __init__(self, db_path: str, log_path: str):
        self.db_path = db_path
        self.log_path = log_path
        print(f"[Framework/Loader] {Colors.green}CurrencyAPI initialized.{Colors.end}")
    
    def get_time(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def add(self, user: discord.User, amount: int) -> int:
        """Adds balance to the specified user."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        currency["wallet"][str(user)] += int(amount)
        with open(self.db_path, 'w+') as f: json.dump(currency, f, indent=4)
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency User({user}): Added {amount} coins to wallet\n')
            f.close()
        return 0
    
    def bank_add(self, user: discord.User, amount: int) -> int:
        """Adds balance to the specified user's bank account."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        currency["bank"][str(user)] += int(amount)
        with open(self.db_path, 'w+') as f: json.dump(currency, f, indent=4)
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency User({user}): Added {amount} coins to bank\n')
            f.close()
        return 0

    def remove(self, user: discord.User, amount: int) -> int:
        """Removes balance from the specified user."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        currency["wallet"][str(user)] -= int(amount)
        with open(self.db_path, 'w+') as f: json.dump(currency, f, indent=4)
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency User({user}): Removed {amount} coins from wallet\n')
            f.close()
        return 0
    
    def bank_remove(self, user: discord.User, amount: int) -> int:
        """Removes balance from the specified user's bank account."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        currency["bank"][str(user)] -= int(amount)
        with open(self.db_path, 'w+') as f: json.dump(currency, f, indent=4)
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency User({user}): Removed {amount} coins from bank\n')
            f.close()
        return 0

    def reset(self, user: discord.User) -> int:
        """Resets the specified user's balance."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        currency["wallet"][str(user)] = 0
        currency["bank"][str(user)] = 0
        with open(self.db_path, 'w+') as f: json.dump(currency, f, indent=4)
        print(f"[Framework/CurrencyAPI] Currency data for \"{user}\" has been wiped")
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency User({user}): Wiped all currency data\n')
            f.close()
        return 0

    def deposit(self, user: discord.User, amount: int) -> int:
        """Moves a specified amount of coins to the user's bank."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        currency["bank"][str(user)] += int(amount)
        currency["wallet"][str(user)] -= int(amount)
        with open(self.db_path, 'w+') as f: json.dump(currency, f, indent=4)
        print(f"[Framework/CurrencyAPI] Moved {amount} coins to bank. User: {user} [{user}]")
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency User({user}): Moved {amount} coins from wallet to bank\n')
            f.close()
        return 0

    def withdraw(self, user: discord.User, amount: int) -> int:
        """Moves a specified amount of coins to the user's wallet."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        currency["wallet"][str(user)] += int(amount)
        currency["bank"][str(user)] -= int(amount)
        with open(self.db_path, 'w+') as f: json.dump(currency, f, indent=4)
        print(f"[Framework/CurrencyAPI] Moved {amount} coins to wallet. User: {user} [{user}]")
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency User({user}): Moved {amount} coins from bank to wallet\n')
            f.close()
        return 0
    
    def treasury_add(self, amount: int) -> int:
        with open(self.db_path, 'r') as f: currency = json.load(f)
        currency["treasury"] += int(amount)
        with open(self.db_path, 'w+') as f: json.dump(currency, f, indent=4)
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency Treasury: Added {amount} coins to treasury\n')
            f.close()
        return 0
    
    def treasury_remove(self, amount: int) -> int:
        with open(self.db_path, 'r') as f: currency = json.load(f)
        currency["treasury"] -= int(amount)
        with open(self.db_path, 'w+') as f: json.dump(currency, f, indent=4)
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency Treasury: Removed {amount} coins from treasury\n')
            f.close()
        return 0

    def get_wallet(self, user: discord.User) -> int:
        """Returns the amount of coins in the user's wallet."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        return int(currency["wallet"][str(user)])

    def get_bank(self, user: discord.User) -> int:
        """Returns the amount of coins in the user's bank account."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        return int(currency["bank"][str(user)])

    def get_treasury(self) -> int:
        """Returns the amount of coins in the treasury."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        return int(currency["treasury"])
    
    def get_user_networth(self, user: discord.User) -> int:
        """Returns the net-worth of the user."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        nw = int(currency["wallet"][str(user)]) + int(currency["bank"][str(user)]) 
        return nw
    
    def get_user_count(self) -> int:
        """Returns the total number of users cached in the currency database."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        users = 0
        for x in currency["wallet"].keys(): users += 1
        return users
    
    def new_wallet(self, user: int) -> int:
        """Makes a new key for a user wallet in the currency database."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        if str(id) not in currency['wallet']:
            currency['wallet'][str(id)] = 5000
            return 0

    def new_bank(self, user: int) -> int:
        """Makes a new key for a user bank account in the currency database."""
        with open(self.db_path, 'r') as f: currency = json.load(f)
        if str(id) not in currency['bank']:
            currency['bank'][str(id)] = 0
            return 0
