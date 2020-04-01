import pymongo
from bson.json_util import dumps
import json
from datetime import datetime, timezone
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv()

MONGOPASS = os.getenv("MONGOPASS")
MONGODB = os.getenv("MONGODB")
MONGOCOLLECTION3 = os.getenv("MONGOCOLLECTION3")

client = pymongo.MongoClient(f"mongodb+srv://admin:{MONGOPASS}@swap-35noy.mongodb.net/admin?retryWrites=true&w=majority")
db = pymongo.database.Database(client, MONGODB)
colFaucet = pymongo.collection.Collection(db, MONGOCOLLECTION3)

class FaucetTxn:

    time = ""
    add = ""

    def __init__(self, _add):
        self.time = datetime.now()
        self.add = _add

    def getDict(self):
        data = {
            "add": self.add,
            'time': self.time
        }
        return(data)

def isRecent( _add ="" ):

        recCount = 0
        cursor = colFaucet.find({"add": _add}).sort([('time', -1)]).limit(1)

        delta = ""
        for rec in cursor:
             now = datetime.now()
             recTime = rec['time']
             delta = now - recTime

        if (delta.days >= 1):
                return False
        else:
                return True


def insertFaucetTxn(rec):
    try:
        resp = colFaucet.insert_one(rec.getDict())
        return True
    except:
        return False

add ="0x707aC3937A9B31C225D8C240F5917Be97cab9F20"

if (isRecent(add) == False):
        if(insertFaucetTxn(FaucetTxn(add)) == True):
                print("transferring")
        else:
                print("DB Error")
else:
        print("Too Soon")
