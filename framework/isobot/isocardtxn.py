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
    """Dumps the latest transaction data to local machine storage."""
    with open("database/isocard_transaction_history.json", 'r', encoding="utf-8") as f:
        json.dump(txn_db, f, indent=4)
    return 0

def write_to_log(payer_id: Union[str, int], reciever_id: Union[str, int], data: str) -> int:
    """Writes a new transaction update to the specified log path."""
    current_time = datetime.time().strftime("%d-%m-%Y %H:%M:%S")
    with open(log_file_path, 'a') as f:
        f.write(f"[{current_time}] ({str(payer_id)} -> {str(reciever_id)}) {data}\n")
    return 0

# Functions
def write_transaction(txn_id: str, payer_id: str, merchant_id: str, card_number: str, user_id: str, amount: int, status: str):
    """Writes a new transaction to the transaction history log."""
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

def update_transaction_status(txn_id: str, new_status: str) -> int:
    """Updates the status field of a transaction in transaction history.\n\nReturns `0` if successful, returns `1` if transactions does not exist."""
    try:
        txn_db[str(txn_id)]["status"] = new_status
        save()
        return 0
    except KeyError:
        return 1
