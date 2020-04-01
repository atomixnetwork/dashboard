import pymongo
from bson.json_util import dumps
import json
from datetime import datetime, timezone, timedelta
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv()

MONGOPASS = os.getenv("MONGOPASS")
MONGODB = os.getenv("MONGODB")
MONGOCOLLECTION1 = os.getenv("MONGOCOLLECTION1")
MONGOCOLLECTION2 = os.getenv("MONGOCOLLECTION2")
MONGOCOLLECTION3 = os.getenv("MONGOCOLLECTION3")

client = pymongo.MongoClient(f"mongodb+srv://admin:{MONGOPASS}@cluster-b647v.mongodb.net/admin?retryWrites=true&w=majority")
db = pymongo.database.Database(client, MONGODB)
colBinance = pymongo.collection.Collection(db, MONGOCOLLECTION1)
colEos = pymongo.collection.Collection(db, MONGOCOLLECTION2)
colFaucet = pymongo.collection.Collection(db, MONGOCOLLECTION3)

def getPrettyTime():
    """Get user's pretty current time"""
    rightnow = datetime.today()
    prettytime = rightnow.ctime()
    return prettytime

class TxnObject:

    time = ""
    TxnHash = ""
    TxnRedeemer = ""

    def __init__(self, _txnHash, _txnRedeemer):
        self.time = getPrettyTime()
        self.TxnHash = _txnHash
        self.TxnRedeemer = _txnRedeemer

    def getDict(self):
        data = {
            "_id": self.TxnHash,
            'time': self.time ,
            'txnRedeemer': self.TxnRedeemer
        }
        return(data)

def doesBinanceHashExist( _binanceTxnHash ="" ):

    try:
        recCount = 0
        records = colBinance.find({"_id": _binanceTxnHash})
        for x in records:
            recCount+=1

        if (recCount >= 1):
            return True
        else:
            return False
    except:
        return False

def doesEosHashExist( _eosTxnHash ="" ):

    try:
        recCount = 0
        records = colEos.find({"_id": _eosTxnHash})
        for x in records:
            recCount+=1

        if (recCount >= 1):
            return True
        else:
            return False
    except:
        return False

def insertBinanceRecord(rec):

    try:
        resp = colBinance.insert_one(rec.getDict())
        return True
    except pymongo.errors.DuplicateKeyError:
        return False
    except:
        return False

def insertEosRecord(rec):

    try:
        resp = colEos.insert_one(rec.getDict())
        return True
    except pymongo.errors.DuplicateKeyError:
        return False
    except:
        return False


class FaucetTxn:

    time = ""
    add = ""

    def __init__(self, _add):
        self.time = datetime.now()
        self.add = _add.lower();

    def getDict(self):
        data = {
            "add": self.add,
            'time': self.time
        }
        return(data)

def insertFaucetTxn(rec):
    try:
        resp = colFaucet.insert_one(rec.getDict())
        return True
    except:
        return False

def isRecent( _add ="" ):

    _add = _add.lower();
    recCount = 0
    cursor = colFaucet.find({"add": _add}).sort([('time', -1)]).limit(1)

    delta = timedelta()
    for rec in cursor:
        now = datetime.now()
        recTime = rec['time']
        delta = now - recTime
    print(delta)
    if (delta.days >= 1):
        return False
    elif (delta.seconds == 0 and delta.days == 0):
        return False
    else:
        return True

# print(isRecent("0x707ac3937a9b31c225d8c240f5917be97cab9f20"))

# print(doesHashExist("F73F496A0278445333193EC348C14A50371272EB79E142AF6E4D0DB4E59ADA8B"))

# print(records)
# record = BinanceToEthereumTxn(
#     "B04E2714A61872FA25D9E7A669B11FCCA7907D5373DC8412AE5D44AA98C1A442",
#     "0x707aC3937A9B31C225D8C240F5917Be97cab9F20")

# if(doesHashExist(record.binanceTxnHash) == False):
#     if (insertRecord(record)):
#         print("Txn Info Backed Up to DB")
#     else:
#         print("Error in Backing up info")
# else:
#     print("Hash Already redeemed")

#col_results = json.loads(dumps(col.find().limit(5).sort("time", -1)))
#     print(col_results)


