import json
import discord

class Colors():
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
    def __init__(self, db_path:str):
        self.db_path = db_path
        print(f"[Framework/Loader] {Colors.green}CurrencyAPI initialized.{Colors.end}")
    def save(self):
        """Saves databases cached on memory."""
        with open(self.db_path, 'w+') as f: json.dump(currency, f, indent=4)
    def add(self, user:discord.User, amount:int):
        """Adds balance to the specified user."""
        currency["wallet"][str(user.id)] += amount
        self.save()
    def remove(self, user:discord.User, amount:int):
        """Removes balance from the specified user."""
        currency["wallet"][str(user.id)] -= amount
        self.save()
    def reset(self, user:discord.User):
        """Resets the specified user's balance."""
        currency["wallet"][str(user.id)] = 0
        currency["bank"][str(user.id)] = 0
        self.save()
        print(f"[Framework/CurrencyAPI] Currency data for \"{user.id}\" has been wiped.")
    def deposit(self, user:discord.User, amount:int):
        """Moves a specified amount of coins to the user's bank."""
        currency["bank"][str(user.id)] += amount
        currency["wallet"][str(user.id)] -= amount
        save()
        print(f"[Framework/CurrencyAPI] Moved {amount} coins to bank. User: {user} [{user.id}]")
    def withdraw(self, user:discord.User, amount:int):
        """Moves a specified amount of coins to the user's wallet."""
        currency["wallet"][str(user.id)] += amount
        currency["bank"][str(user.id)] -= amount
        save()
        print(f"[Framework/CurrencyAPI] Moved {amount} coins to wallet. User: {user} [{user.id}]")
