"""
# Isobot Configuration Updater Assistant
## Overview
This module is responsible for the smooth web-based updation of any configuration files in the Isobot client.

## How Does it Work?
Every time the bot is started, this module sends a request to the main server to check for any new updates in the general configuration files.

If there are updates, the module downloads the new files and replaces the old ones, before starting.

If there are no updates available, this is skipped and the bot is directly started.
"""

# Imports
import requests
import os
import json
from typing_extensions import Literal

# Variables
client_data_dir = f"{os.path.expanduser('~')}/.isobot"

# Configuration
class UpdaterConfig:
    """This class contains the full configuration for the updater."""
    update_server_target = "https://raw.githubusercontent.com/PyBotDevs/resources/refs/heads/base/isobot-config-data"
    use_raw_file_data = False
    config_files_path = f"{client_data_dir}/config/"
    config_files_list = ("commands.json", "shop.json", "words.json")

# Functions
def download_file(config_file_name: str) -> tuple:
    """Downloads the requested file from the update server.\n\nReturns a `tuple` containing the status of the request, along with the data from the request."""
    download_request = requests.get(UpdaterConfig.update_server_target + "/" + config_file_name + ("?raw=true" if UpdaterConfig.use_raw_file_data else ""))
    if download_request.status_code == 200:
        return (True, dict(json.loads(download_request.text)))
    else:
        return (False, download_request.status_code)

def check_for_updates() -> Literal[True]:
    """
    Sends a request to the update server to check for any updates to the configuration files.

    Returns `True` if client-side process is successful.
    """
    # Check if all config files exist, and download them if they don't
    if not os.path.isdir(f"{client_data_dir}/config"):
        os.mkdir(f"{client_data_dir}/config")

    for _file in UpdaterConfig.config_files_list:
        if not os.path.exists(UpdaterConfig.config_files_path + _file):
            print(f"[!] A required configuration file appears to be missing. Downloading file from server...")
            downloaded_config_file = download_file(_file)
            if downloaded_config_file[0] == False:
                print(f"[❌] (code: {downloaded_config_file[1]}) An error occured while trying to download the configuration file. Skipping...")
                continue
            else:
                with open(UpdaterConfig.config_files_path + _file, "x") as config_file:
                    json.dump(downloaded_config_file[1], config_file, indent=4)
                    config_file.close()
                print(f"[✅] Successfully downloaded the configuration file.")
        
    # Check for any updates with existing config files, and update them if any updates are available
    for _file in UpdaterConfig.config_files_list:
        check_file = download_file(_file)
        if check_file[0] == False:
            print(f"[❌] (code: {check_file[1]}) An error occured while trying to check for updates to the configuration file. Skipping...")
            continue
        else:
            with open(UpdaterConfig.config_files_path + _file, "r") as config_file:
                if dict(check_file[1]) != dict(json.load(config_file)):
                    print(f"[!] An update is available for the {_file} configuration file. Updating...")
                    with open(UpdaterConfig.config_files_path + "/" + _file, "w+") as config_file:
                        json.dump(check_file[1], config_file, indent=4)
                        config_file.close()
                    print(f"[✅] Successfully updated the configuration file.")
    return True
