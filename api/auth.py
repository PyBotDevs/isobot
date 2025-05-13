# Imports
import json, os, os.path
from typing_extensions import Literal

# Config
wdir = f"{os.path.expanduser('~')}/.isobot"

# Setup
def load_config() -> dict:
    """Loads the runtimeconfig file and returns the contents as a `dict`."""
    with open(f'{wdir}/runtimeconfig.json', 'r') as f:
        return json.load(f)

def initial_setup() -> Literal[0]:
    # Building runtimeconfig files and directory IF missing:
    """Checks whether the required runtimeconfig files are present in the bot runtime directory.\n\nReturns `0` if successful."""
    if not os.path.isfile(f"{wdir}/runtimeconfig.json"):
        print(f"[!] Runtimeconfig not found. Building runtime configuration files...")
        print("   > Creating runtimeconfig file...")
        with open(f'{wdir}/runtimeconfig.json', 'x') as f:  # Create a new file for runtimeconfig
            json.dump({}, f)
            f.close()

    # Check whether any keys are missing in runtimeconfig file, and add them accordingly:
    with open(f'{wdir}/runtimeconfig.json', 'r') as f: runtimeconfig_db = json.load(f)
    required_keys = ("token", "alt_token_path", "secret", "public_key", "runtime_options", "replit", "other_keys")
    for key in required_keys:
        if key not in runtimeconfig_db:
            print(f"[!] Update available for runtimeconfig. Updating configuration...")
            if key == "runtime_options":
                runtimeconfig_db[key] = {}
            elif key == "other_keys":
                runtimeconfig_db[key] = {}
            elif key == "replit":
                runtimeconfig_db[key] = False
            else:
                runtimeconfig_db[key] = ""
    with open(f'{wdir}/runtimeconfig.json', 'w+') as f: json.dump(runtimeconfig_db, f, indent=4)

    default_runtime_option_values = {
        "themes": False,
        "log_messages": False,
        "guild_log_blacklist": {},
        "only_log_whitelist": False,
        "guild_log_whitelist": {},
        "ping_server_override": False,
        "debug_mode": False,
        "show_ping_on_startup": True,
        "isocard_server_enabled": True,
        "superusers": []
    }
    for key in default_runtime_option_values:
        if key not in runtimeconfig_db["runtime_options"]:
            print(f"[!] Update available for runtimeconfig. Updating configuration...")
            runtimeconfig_db["runtime_options"][key] = default_runtime_option_values[key]

    other_api_keys_list = ("openweathermap", "reddit", "ossapi", "chatgpt")
    for key in other_api_keys_list:
        if key not in runtimeconfig_db["other_keys"]:
            print(f"[!] Update available for runtimeconfig. Updating configuration...")
            runtimeconfig_db["other_keys"][key] = ""
    
    with open(f'{wdir}/runtimeconfig.json', 'w+') as f: json.dump(runtimeconfig_db, f, indent=4)
    return 0

# Commands
def get_token():
    """Returns the token in `runtimeconfig.json`, if it exists.\n\nIf there is no token provided in the config, it will try accessing the alternate token location.\n\nIf no alternate token exists, it will manually ask the user for input and it will autosave it to `runtimeconfig.json`."""
    initial_setup()
    config = load_config()
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
                with open(f'{wdir}/runtimeconfig.json', 'w+') as f: json.dump(config, f, indent=4)
                print("[✅] Setup successful!")
            elif arg1.lower() == "n" or arg1.lower() == "no": return
    return str(config["token"])

def get_secret():
    """Returns the bot client secret in `runtimeconfig.json`, if it exists."""
    initial_setup()
    config = load_config()
    if config["secret"] != "": return config["secret"]
    else: return "Secret has not been set."

def get_public_key():
    """Returns the bot's public key in `runtimeconfig.json`, if it exists."""
    initial_setup()
    config = load_config()
    if config["public_key"] != "": return config["public_key"]
    else: return "Public key has not been set."

def get_mode() -> bool:
    """Returns a boolean of the current runtime mode.\n\nReturns `True` if replit mode is active, returns `False` if replit mode is inactive."""
    initial_setup()
    config = load_config()
    return config["replit"]

def ext_token(token_name: str) -> str:
    """Returns an external extra authorization token from `runtimeconfig.json`, if it exists."""
    initial_setup()
    config = load_config()
    return str(config["other_keys"][token_name])
    #except KeyError: return "This external authorization key does not exist."

def get_runtime_options() -> dict:
    """Returns a dict of all the client's runtime configuration options, as well as their respective values."""
    initial_setup()
    config = load_config()
    return dict(config["runtime_options"])
