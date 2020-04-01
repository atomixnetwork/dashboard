import requests
import os
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

class Dfuse:

    DFUSE_SERVERKEY = str(os.getenv("DFUSE_SERVERKEY"))

    def updateBearerToken(self):
        endpoint = "https://auth.dfuse.io/v1/auth/issue"
        data = '{"api_key":"'+self.DFUSE_SERVERKEY+'"}'
        headers = {"Content-Type": "application/json"}
        response = requests.post(endpoint, data=data, headers=headers).json()
        return(response['token'])

    def getEosTxn(self, txnHash, bt):
        endpoint = f"https://jungle.eos.dfuse.io/v0/transactions/{txnHash}"
        data = {"json": True}
        # print(bt)
        headers = {"Authorization": f"Bearer {bt}"}
        txnDat = requests.post(endpoint, data=data, headers=headers).json()

        return txnDat
