"""The isobot module for managing the currency database"""

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
    - new_bank(user)
    - delete_user(user)
    - fetch_all_cached_user_ids()"""

    def __init__(self, db_path: str, log_path: str):
        self.db_path = db_path
        self.log_path = log_path
        print(f"[Framework/Loader] {Colors.green}CurrencyAPI initialized.{Colors.end}")

    def save(self, data: dict) -> int:
        """Dumps all cached data to your local machine."""
        with open(self.db_path, 'w+', encoding="utf8") as f: json.dump(data, f)
        return 0

    def load(self) -> dict:
        """Loads the database from your local machine onto memory."""
        with open(self.db_path, 'r', encoding="utf-8") as f: data = json.load(f)
        return data

    def get_time(self) -> str:
        """Returns the current time in a formatted state."""
        return datetime.datetime.now().strftime("%H:%M:%S")

    def log(self, data: str):
        """Logs new information to the currency log."""
        with open(self.log_path, 'a', encoding="utf-8") as f:
            f.write(f'{self.get_time()} framework.isobot.currency {data}\n')
            f.close()
        return 0

    def add(self, user: discord.User, amount: int) -> int:
        """Adds balance to the specified user."""
        currency = self.load()
        currency["wallet"][str(user)] += int(amount)
        self.save(currency)
        self.log(f"User({user}): Added {amount} coins to wallet")
        return 0

    def bank_add(self, user: discord.User, amount: int) -> int:
        """Adds balance to the specified user's bank account."""
        currency = self.load()
        currency["bank"][str(user)] += int(amount)
        self.save(currency)
        self.log(f"User({user}): Added {amount} coins to bank")
        return 0

    def remove(self, user: discord.User, amount: int) -> int:
        """Removes balance from the specified user."""
        currency = self.load()
        currency["wallet"][str(user)] -= int(amount)
        self.save(currency)
        self.log(f"User({user}): Removed {amount} coins from wallet")
        return 0

    def bank_remove(self, user: discord.User, amount: int) -> int:
        """Removes balance from the specified user's bank account."""
        currency = self.load()
        currency["bank"][str(user)] -= int(amount)
        self.save(currency)
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency User({user}): Removed {amount} coins from bank\n')
            f.close()
        self.log(f"")
        return 0

    def reset(self, user: discord.User) -> int:
        """Resets the specified user's balance."""
        currency = self.load()
        currency["wallet"][str(user)] = 0
        currency["bank"][str(user)] = 0
        self.save(currency)
        print(f"[Framework/CurrencyAPI] Currency data for \"{user}\" has been wiped")
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency User({user}): Wiped all currency data\n')
            f.close()
        self.log(f"")
        return 0

    def deposit(self, user: discord.User, amount: int) -> int:
        """Moves a specified amount of coins to the user's bank."""
        currency = self.load()
        currency["bank"][str(user)] += int(amount)
        currency["wallet"][str(user)] -= int(amount)
        self.save(currency)
        print(f"[Framework/CurrencyAPI] Moved {amount} coins to bank. User: {user} [{user}]")
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency User({user}): Moved {amount} coins from wallet to bank\n')
            f.close()
        self.log(f"")
        return 0

    def withdraw(self, user: discord.User, amount: int) -> int:
        """Moves a specified amount of coins to the user's wallet."""
        currency = self.load()
        currency["wallet"][str(user)] += int(amount)
        currency["bank"][str(user)] -= int(amount)
        self.save(currency)
        print(f"[Framework/CurrencyAPI] Moved {amount} coins to wallet. User: {user} [{user}]")
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency User({user}): Moved {amount} coins from bank to wallet\n')
            f.close()
        self.log(f"")
        return 0

    def treasury_add(self, amount: int) -> int:
        """Adds a specified amount of coins to the treasury."""
        currency = self.load()
        currency["treasury"] += int(amount)
        self.save(currency)
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency Treasury: Added {amount} coins to treasury\n')
            f.close()
        self.log(f"")
        return 0

    def treasury_remove(self, amount: int) -> int:
        """Removes a specified amount of coins from the treasury."""
        currency = self.load()
        currency["treasury"] -= int(amount)
        self.save(currency)
        self.log(f"Treasury: Removed {amount} coins from treasury")
        return 0

    def get_wallet(self, user: discord.User) -> int:
        """Returns the amount of coins in the user's wallet."""
        currency = self.load()
        return int(currency["wallet"][str(user)])

    def get_bank(self, user: discord.User) -> int:
        """Returns the amount of coins in the user's bank account."""
        currency = self.load()
        return int(currency["bank"][str(user)])

    def get_treasury(self) -> int:
        """Returns the amount of coins in the treasury."""
        currency = self.load()
        return int(currency["treasury"])

    def get_user_networth(self, user: discord.User) -> int:
        """Returns the net-worth of the user."""
        currency = self.load()
        nw = int(currency["wallet"][str(user)]) + int(currency["bank"][str(user)])
        return nw

    def get_user_count(self) -> int:
        """Returns the total number of users cached in the currency database."""
        currency = self.load()
        users = 0
        for x in currency["wallet"].keys(): users += 1
        return users

    def new_wallet(self, user: int) -> int:
        """Makes a new key for a user wallet in the currency database."""
        currency = self.load()
        if str(user) not in currency['wallet']:
            currency['wallet'][str(user)] = 5000
            self.save(currency)
            return 0

    def new_bank(self, user: int) -> int:
        """Makes a new key for a user bank account in the currency database."""
        currency = self.load()
        if str(user) not in currency['bank']:
            currency['bank'][str(user)] = 0
            self.save(currency)
            return 0

    def delete_user(self, user: int) -> int:
        """Permanently deletes all user data for the respective user."""
        currency = self.load()
        if str(user) in currency['wallet']: del currency['wallet'][str(user)]
        if str(user) in currency['bank']: del currency['bank'][str(user)]
        self.save(currency)
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency User({user}): Successfully deleted all user data from currency database.\n')
            f.close()
        return 0
    
    def fetch_all_cached_user_ids(self) -> list:
        """Fetches the ids of all cached users in the currency database, and returns it as a `list`.\n\n(uses database's `wallet` property to fetch ids)"""
        currency = self.load()
        all_user_ids = list()
        for uid in currency["wallet"]:
            all_user_ids.append(str(uid))
        return all_user_ids
