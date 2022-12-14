# Imports
import json, os

# Config
wdir = os.getcwd()

# Setup
with open(f'{wdir}/api/runtimeconfig.json', 'r') as f:
    global config
    config = json.load(f)

# Commands
def get_token():
    """Returns the token in `runtimeconfig.json`, if it exists.\nIf there is no token provided in the config, it will manually ask the user for input and it will autosave it."""
    if config["token"] == "":
        print("[!] Looks like you didn't input a token. Would you like to import one?")
        arg1 = input("[Yes/No/y/n] > ")
        if arg1.lower() == "y":
            arg2 = input("Enter your custom token: ")
            config["token"] = str(arg2)
            with open(f'{wdir}/api/runtimeconfig.json', 'w+') as f: json.dump(config, f, indent=4)
            print("[✅] Setup successful!")
        elif arg1.lower() == "n": return
    return str(config["token"])

def get_secret():
    """Returns the bot client secret in `runtimeconfig.json`, if it exists."""
    if config["secret"] != "": return config["secret"]
    else: return "Secret has not been set."

def get_public_key():
    """Returns the bot's public key in `runtimeconfig.json`, if it exists."""
    if config["public_key"]: return config["public_key"]
    else: return "Public key has not been set."
