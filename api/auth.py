# Imports
import json, os, os.path

# Config
wdir = os.getcwd()

# Setup
with open(f'{wdir}/api/runtimeconfig.json', 'r') as f:
    global config
    config = json.load(f)

# Commands
def get_token():
    """Returns the token in `runtimeconfig.json`, if it exists.\n\nIf there is no token provided in the config, it will try accessing the alternate token location.\n\nIf no alternate token exists, it will manually ask the user for input and it will autosave it to `runtimeconfig.json`."""
    if config["token"] == "":
        if config["alt_token_path"] != "":
            tkn = str()
            with open(config["alt_token_path"], 'r', encoding="utf-8") as f:
                tkn = f.read()
                f.close()
            return str(tkn)
        else:
            print("[!] Looks like you didn't input a token. Would you like to import one?")
            arg1 = input("[Yes/No/y/n] > ")
            if arg1.lower() == "y" or arg1.lower() == "yes":
                arg2 = input("Enter your custom token: ")
                config["token"] = str(arg2)
                with open(f'{wdir}/api/runtimeconfig.json', 'w+') as f: json.dump(config, f, indent=4)
                print("[✅] Setup successful!")
            elif arg1.lower() == "n" or arg1.lower() == "no": return
    return str(config["token"])

def get_secret():
    """Returns the bot client secret in `runtimeconfig.json`, if it exists."""
    if config["secret"] != "": return config["secret"]
    else: return "Secret has not been set."

def get_public_key():
    """Returns the bot's public key in `runtimeconfig.json`, if it exists."""
    if config["public_key"] != "": return config["public_key"]
    else: return "Public key has not been set."

def get_mode() -> bool:
    """Returns a boolean of the current runtime mode.\n\nReturns `True` if replit mode is active, returns `False` if replit mode is inactive."""
    return config["replit"]

def ext_token(token_name: str) -> str:
    """Returns an external extra authorization token from `runtimeconfig.json`, if it exists."""
    return str(config["other_keys"][token_name])
    #except KeyError: return "This external authorization key does not exist."

def get_runtime_options() -> dict:
    """Returns a dict of all the client's runtime configuration options, as well as their respective values."""
    return dict(config["runtime_options"])
