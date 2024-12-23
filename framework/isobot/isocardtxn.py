# Imports
import json
import time
import datetime
from typing_extensions import Union

# Variables
log_file_path = "logs/isocard_transactions.log"

# Initialization
with open("database/isocard_transaction_history.json", 'r', encoding="utf-8") as f:
    txn_db = json.load(f)

# Pre-defined Methods
def save() -> int:
    """
    # `save()` Command
    ## Command Information
    Dumps the latest transaction data from memory to local machine storage.

    ## Status Return Codes
    ### If successful:
    - Returns `0`
    ### If not successful:
    - Returns the respective exception class
    """
    with open("database/isocard_transaction_history.json", 'r', encoding="utf-8") as f:
        json.dump(txn_db, f, indent=4)
    return 0

def write_to_log(txn_id: str, payer_id: Union[str, int], reciever_id: Union[str, int], data: str) -> int:
    """
    # `write_to_log()` Command
    ## Command Information
    Writes a new transaction update to the specified log path.

    ## Status Return Codes
    ### If successful:
    - Returns `0`
    ### If not successful:
    - Returns the respective exception class

    ## Log Format
    Each log update is written to the log file at `logs/isocard_transactions.log`, whenever the command is fired during runtime.

    The log format is provided as follows:

    ```log
    [current time] (payer id -> receiver id) transaction id: status update data
    ```
    """
    current_time = datetime.time().strftime("%d-%m-%Y %H:%M:%S")
    with open(log_file_path, 'a') as f:
        f.write(f"[{current_time}] ({str(payer_id)} -> {str(reciever_id)}) {txn_id}: {data}\n")
    return 0

# Functions
def read_transaction(txn_id: str) -> dict:
    """
    # `read_transactions()` Command
    ## Command Information
    Reads and returns the data of a transaction from the history log with the given transaction id.
    
    ## Exception Handling
    ### Transaction does not exist in the transactions database:
    - Returns error response code`1`

    ## Response Format
    All successful responses will be provided in the following `dict` format:

    ```json
    txn_id: {
        "payer_id": user id of the payer,
        "merchant_id": user id of the merchant (reciever),
        "card_number": IsoCard number of the payer,
        "user_id": the id of the user paying,
        "amount": amount of coins requested by merchant,
        "status": current status of the transaction,
        "timestamp": time at which the transaction was logged
    }
    ```
    """
    try:
        return txn_db[str(txn_id)]
    except KeyError:
        return 1

def write_transaction(txn_id: str, payer_id: str, merchant_id: str, card_number: str, user_id: str, amount: int, status: str) -> int:
    """
    # `write_transaction()` Command
    ## Command Information
    Writes a new transaction to the transaction history log.

    ## Status Return Codes
    ### If successful:
    - Returns `0`
    ### If not successful:
    - Returns the respective exception class

    ## Log Database Format
    Each transaction in the transaction history database is stored in the following format:

    ```json
    txn_id: {
        "payer_id": user id of the payer,
        "merchant_id": user id of the merchant (reciever),
        "card_number": IsoCard number of the payer,
        "user_id": the id of the user paying,
        "amount": amount of coins requested by merchant,
        "status": current status of the transaction,
        "timestamp": time at which the transaction was logged
    }
    ```

    - Note: This format can be refered to, while working with the output from the `read_transaction()` command.
    """
    txn_db[str(txn_id)] = {
        "payer_id": payer_id,
        "merchant_id": merchant_id,
        "card_number": card_number,
        "user_id": user_id,
        "amount": amount,
        "status": status,
        "timestamp": round(time.time()),
    }
    save()
    return 0

def update_transaction_status(txn_id: str, new_status: str) -> int:
    """
    # `update_transaction_status()` Command
    ## Command Information
    Updates the status field of a transaction in transaction history.
    
    ## Status Return Codes
    ### If successful:
    - Returns `0` 
    ### If transaction does not exist:
    - Returns `1`
    """
    try:
        txn_db[str(txn_id)]["status"] = new_status
        save()
        return 0
    except KeyError:
        return 1
