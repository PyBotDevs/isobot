"""The IsoCard payments web server."""
# Imports
import json
import random
import logging
import isocardtxn
from api import auth
from flask import Flask
from flask import request
from framework.isobot import currency
from threading import Thread

# TODO: Add log file write commands to ALL EXISTING FUNCTIONS.

# Configuration
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask('')
currency = currency.CurrencyAPI("database/currency.json", "logs/currency.log")

def call_isocards_database() -> dict:
    """Calls all of the latest information from the IsoCards database."""
    with open("database/isocard.json", 'r') as f: isocards = json.load(f)
    return isocards

def save(data):
    """Dumps all cached databases to the local machine."""
    with open("database/isocard_transactions.json", 'w+') as f: json.dump(data, f, indent=4)

# Functions
def generate_verification_code() -> int:
    """Generates a random 6 digit verification code."""
    int_1 = str(random.randint(1, 9))
    int_2 = str(random.randint(0, 9))
    int_3 = str(random.randint(0, 9))
    int_4 = str(random.randint(0, 9))
    int_5 = str(random.randint(0, 9))
    int_6 = str(random.randint(0, 9))
    code: str = int_1 + int_2 + int_3 + int_4 + int_5 + int_6
    return int(code)

def generate_txn_id() -> str:
    """Generates a randomized transaction id, which is three *CAPITAL* letters followed by 6 numbers."""
    txn_id = str()
    for _ in range(3):
        txn_id += str(random.choice(('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', )))
    for _ in range(6):
        txn_id += str(random.randint(0, 9))
    return txn_id

# API Commands
@app.route('/', methods=["GET"])
def main():
    return "Server is online."

@app.route('/requestpayment', methods=["GET"])
def requestpayment():
    try:
        isocards = call_isocards_database()
        with open("database/isocard_transactions.json", 'r') as f: transactions_db = json.load(f)
        args = request.args
        card_number = args.get("cardnumber")
        ssc = args.get("ssc")
        amount = args.get("amount")
        merchant_id = args.get("merchantid")
        if str(isocards[str(card_number)]["ssc"]) == ssc:
            verification_code = generate_verification_code()
            txn_id = generate_txn_id()
            user_id = isocards[str(card_number)]["cardholder_user_id"]
            transactions_db[str(verification_code)] = {
                "txn_id": txn_id,
                "payer_id": user_id,
                "merchant_id": merchant_id,
                "card_number": card_number,
                "user_id": user_id,
                "amount": int(amount),
                "status": "in_progress"
            }
            save(transactions_db)
            isocardtxn.write_transaction(txn_id, user_id, merchant_id, card_number, user_id, int(amount), "In Progress")
            request_data = {
                "code": 200,
                "message": f"Payment requested to IsoCard number: {card_number}. Payment will be complete once user accepts this.",
                "txn_id": txn_id,
                "verification_code": verification_code
            }
            return request_data, 200
        else: return {
            "code": 401,
            "message": "Unable to authorize transaction."
        }, 401
    except Exception as e: return {
        "code": 500,
        "message": f"Failed to process payment: {e}",
        "exception": type(e).__name__
    }, 500

@app.route('/checkpayment', methods=["GET"])
def checkpayment():
    try:
        with open("database/isocard_transactions.json", 'r') as f: transactions_db = json.load(f)
        args = request.args
        verification_code = args.get("verificationcode")
        txn_id: str = transactions_db[str(verification_code)]["txn_id"]
        if transactions_db[str(verification_code)]["status"] == "complete":
            if currency.get_bank(transactions_db[str(verification_code)]["payer_id"]) < transactions_db[str(verification_code)]["amount"]:
                del transactions_db[str(verification_code)]
                isocardtxn.update_transaction_status(txn_id, "Terminated (insufficient balance)")
                return {
                    "code": 403,
                    "txn_id": txn_id,
                    "message": "Transaction terminated: Insufficient payer balance.",
                    "exception": "InsufficientFunds"
                }, 403
            currency.bank_remove(transactions_db[str(verification_code)]["payer_id"], transactions_db[str(verification_code)]["amount"])
            currency.bank_add(transactions_db[str(verification_code)]["merchant_id"], transactions_db[str(verification_code)]["amount"])
            del transactions_db[str(verification_code)]
            save(transactions_db)
            isocardtxn.update_transaction_status(txn_id, "Successful")
            return {
                "code": 200,
                "txn_id": txn_id,
                "message": "Transaction complete."
            }, 200
        else: return {
            "code": 202,
            "txn_id": txn_id,
            "message": "Transaction still not approved."
        }, 202
    except KeyError: return {
        "code": 404,
        "message": "Verification code does not point to an active transaction.",
        "exception": "TransactionNotFound"
    }, 404
    except Exception as e:
        isocardtxn.update_transaction_status(txn_id, "Failed (unable to process payment)")
        return {
        "code": 500,
        "message": f"Failed to process payment due to an unhandled server error: {e}",
        "exception": type(e).__name__
    }, 500

@app.route('/account', methods=["GET"])
def account():
    try:
        isocards = call_isocards_database()
        args = request.args
        isocard_number = args.get("cardnumber")
        ssc = args.get("ssc")
        if isocards[str(isocard_number)]["ssc"] == ssc:
            card_data = isocards[str(isocard_number)]
            del card_data["config"]
            del card_data["ssc"]
            card_data["account_balance"] = currency.get_wallet(card_data["user_id"])
            return {
                "code": 200,
                "card_info": card_data
            }, 200
        else: return {
            "code": 403,
            "message": "Incorrect IsoCard SSC.",
            "exception": "InvalidSSC"
        }
    except KeyError: return {
        "code": 404,
        "message": "Card number is invalid.",
        "exception": "InvalidIsoCard"
    }, 404
    except Exception as e: return {
        "code": 500,
        "message": f"Failed to fetch account info: {e}",
        "exception": type(e).__name__
    }

# Initialization
def run(): app.run(host="0.0.0.0", port=4800)

def deploy_server():
    """Deploys the IsoCard Payments Server. (if the option is enabled in the runtimeconfig file)\n\nRuntimeconfig Option: `isocard_server_enabled`"""
    if auth.get_runtime_options()["isocard_server_enabled"]:  # Run server ONLY if its runtime option is enabled
        print("[isocard/server] Starting IsoCard payments server...")
        t = Thread(target=run)
        t.daemon = True
        t.start()


#btw i use arch
