from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import requests
import json
from pprint import pprint

burnTxnHashDict= {"0x944a1ae8e1c33fde48cadd43c9d98b1a9cc08519e4b17eb4eaf01a33e1a549b7":"tbnb16uq5gcvg25psr2gqt5y0svn4j53n39lzxkuvl7"}

def checkValidity():
    if(len(burnTxnHashDict)>0):

        for txnHash in burnTxnHashDict.copy():
            print(f"Checking Hash : {txnHash}")
            r = requests.get(url = f"https://ropsten-lvu6lk.blockscout.com/api?module=transaction&action=gettxinfo&txhash={ txnHash }")
            res = json.loads(r.text)
            try:
                if (res['result']['success'] == True):
                    print("Success!")
                    amount = int(res['result']['logs'][0]['data'], 0)
                    token = "ANC-3EF"

                    print(f"Minting and Transferring : { amount } gwei ANC to { burnTxnHashDict[txnHash] }")

                    cmd = f"./tbnbcli token burn --amount { amount } --symbol { token } --from a --chain-id=Binance-Chain-Nile --node=data-seed-pre-2-s1.binance.org:80 --trust-node"
                    result = subprocess.call(cmd.split(" "),stdout=subprocess.PIPE)
                    print("cmd")
                    try:
                        result = result.stdout.decode("utf-8")
                        print(result)
                    except:
                        return ":("

                    burnTxnHashDict.pop(txnHash)
                else:
                    print("Pending")
            except:
                print()


sched = BackgroundScheduler(daemon=True)
sched.add_job(checkValidity,'interval',seconds=5)
sched.start()

app = Flask(__name__)

@app.route("/home")
def home():
    """ Function for test purposes. """
    return "Welcome Home :) !"

if __name__ == "__main__":
    app.run()
