import eospy.cleos
import os
import pytz
import eospy.keys
from pprint import pprint
import json
import datetime as dt
from dotenv import load_dotenv
load_dotenv()

OWNER_ACCOUNT = str(os.getenv("OWNER_ACCOUNT"))
OWNER_ACCOUNT_KEY = str(os.getenv("OWNER_ACCOUNT_KEY"))

ENDPOINT = "http://jungle2.cryptolions.io:80"

OWNER_ACCOUNT_KEY = eospy.keys.EOSKey(OWNER_ACCOUNT_KEY)
ce = eospy.cleos.Cleos(url=ENDPOINT)

def eos_transfer(acct = "antestacc111", amt="0.0000 ANT", memo = "AtomixSwap"):

    arguments = {
                "from": OWNER_ACCOUNT,  # sender
                "to": acct,  # receiver
                "quantity": amt,
                "memo": memo,
            }
    payload = {
            "account": "antestacc111",
            "name": "transfer",
            "authorization": [{
                "actor": OWNER_ACCOUNT,
                "permission": "active",
            }],
        }

    #Converting payload to binary
    data=ce.abi_json_to_bin(payload['account'],payload['name'],arguments)
    payload['data']=data['binargs']
    trx = {"actions": [payload]}
    trx['expiration'] = str((dt.datetime.utcnow() + dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))

    resp = ce.push_transaction(trx, OWNER_ACCOUNT_KEY, broadcast=True)
    return(resp['transaction_id'])

def eos_issue(amt="0.0000 ANT"):

    arguments = {
                "to": OWNER_ACCOUNT,  # receiver
                "quantity": amt,
                "memo": "AtomixSwap Swap Issue",
            }
    payload = {
            "account": OWNER_ACCOUNT,
            "name": "issue",
            "authorization": [{
                "actor": OWNER_ACCOUNT,
                "permission": "active",
            }],
        }

    #Converting payload to binary
    data=ce.abi_json_to_bin(payload['account'],payload['name'],arguments)
    payload['data']=data['binargs']
    trx = {"actions": [payload]}
    trx['expiration'] = str((dt.datetime.utcnow() + dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))

    resp = ce.push_transaction(trx, OWNER_ACCOUNT_KEY, broadcast=True)
    return(resp['transaction_id'])

def eos_retire(amt="0.0000 ANT"):

    arguments = {
                "quantity": amt,
                "memo": "AtomixSwap Swap Retire",
            }
    payload = {
            "account": OWNER_ACCOUNT,
            "name": "retire",
            "authorization": [{
                "actor": OWNER_ACCOUNT,
                "permission": "active",
            }],
        }

    #Converting payload to binary
    data=ce.abi_json_to_bin(payload['account'],payload['name'],arguments)
    payload['data']=data['binargs']
    trx = {"actions": [payload]}
    trx['expiration'] = str((dt.datetime.utcnow() + dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))

    resp = ce.push_transaction(trx, OWNER_ACCOUNT_KEY, broadcast=True)
    # pprint(resp)
    return(resp['transaction_id'])

def eos_getBalance(acct = "antestacc111"):
    resp = ce.get_table(OWNER_ACCOUNT, acct, "accounts")
    balance = resp['rows'][0]['balance']
    # print(balance)
    return(balance)

# print(eos_transfer("antestacc111", "30.0000 ANT", "TBNB16UQ5GCVG25PSR2GQT5Y0SVN4J53N39LZXKUVL7"))


# pprint(ce.get_transaction("a56d744250e3744bb20f311a56cb7a6a1129a8202751d2245b677763924f5bab"))

# getBalance("antestacc111")
# transfer("anuditnagar2", "100.0000 ANT")
# print(eos_transfer("anuditnagar2", "18.0000 ANT"))
# retire( "100.0000 ANT" )
