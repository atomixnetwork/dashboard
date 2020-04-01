import requests
import json
from pprint import pprint

btxnHash = "DA8B948B8F0974D30AD2A611DEF56FDF3ABF7DE3173962D61E9F08DEE19C985F"

r = requests.get(url = f"https://testnet-dex.binance.org/api/v1/tx/{ btxnHash }?format=json")
res = json.loads(r.text)

try:
    if (res['code'] == 0 ):
        print("success")
        if(res['ok'] == True):
            amount = res['tx']['value']['msg'][0]['value']['outputs'][0]['coins'][0]['amount']

    else:
        print("Invalid Hash")
except:
    print(":(")
