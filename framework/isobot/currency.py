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
    - reset(user)
    - deposit(user, amount)
    - withdraw(user, amount)"""
    def __init__(self, db_path: str, log_path: str):
        self.db_path = db_path
        self.log_path = log_path
        with open(self.db_path, 'r') as f:
            global currency
            currency = json.load(f)
        print(f"[Framework/Loader] {Colors.green}CurrencyAPI initialized.{Colors.end}")
    
    def get_time(self):
        return datetime.datetime.now().strftime("%H:%M:%S")
    
    def save(self):
        """Saves databases cached on memory."""
        with open(self.db_path, 'w+') as f: json.dump(currency, f, indent=4)

    def add(self, user: discord.User, amount: int):
        """Adds balance to the specified user."""
        currency["wallet"][str(user)] += amount
        self.save()
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency ({user}): Added {amount} coins to wallet\n')
            f.close()

    def remove(self, user: discord.User, amount: int):
        """Removes balance from the specified user."""
        currency["wallet"][str(user)] -= amount
        self.save()
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency ({user}): Removed {amount} coins from wallet\n')
            f.close()

    def reset(self, user: discord.User):
        """Resets the specified user's balance."""
        currency["wallet"][str(user)] = 0
        currency["bank"][str(user)] = 0
        self.save()
        print(f"[Framework/CurrencyAPI] Currency data for \"{user}\" has been wiped")
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency ({user}): Wiped all currency data\n')
            f.close()

    def deposit(self, user: discord.User, amount: int):
        """Moves a specified amount of coins to the user's bank."""
        currency["bank"][str(user)] += amount
        currency["wallet"][str(user)] -= amount
        self.save()
        print(f"[Framework/CurrencyAPI] Moved {amount} coins to bank. User: {user} [{user}]")
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency ({user}): Moved {amount} coins from wallet to bank\n')
            f.close()

    def withdraw(self, user: discord.User, amount: int):
        """Moves a specified amount of coins to the user's wallet."""
        currency["wallet"][str(user)] += amount
        currency["bank"][str(user)] -= amount
        self.save()
        print(f"[Framework/CurrencyAPI] Moved {amount} coins to wallet. User: {user} [{user}]")
        with open(self.log_path, 'a') as f:
            f.write(f'{self.get_time()} framework.isobot.currency ({user}): Moved {amount} coins from bank to wallet\n')
            f.close()

    def wallet(self, user: discord.User):
        """Returns the amount of coins in the user's wallet."""
        return int(currency["wallet"][str(user)])

    def bank(self, user: discord.User):
        """Returns the amount of coins in the user's bank account."""
        return int(currency["bank"][str(user)])