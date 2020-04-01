import requests
import json
import os
import time
import logging

from flask import Flask, request, jsonify
from subprocess import Popen, PIPE, STDOUT
from pprint import pprint
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from web3 import Web3, HTTPProvider
from flask_cors import CORS

from tokenDetails import TOKEN_ABI, TOKEN_CONTRACT_ADDRESS
from db import client, insertBinanceRecord, insertEosRecord, doesBinanceHashExist, doesEosHashExist, TxnObject
from db import FaucetTxn, isRecent, insertFaucetTxn
from eoslib import eos_issue, eos_transfer, eos_retire, eos_getBalance
from checkadd import isBinanceAdd, isEthereumAdd, isEosAdd
from dfuse import Dfuse

load_dotenv()

erc20Name = os.getenv("ERC20NAME")
bep2Name = os.getenv("BEP2NAME")
B2E_BGP = float(os.getenv("B2E_BGP"))
B2E_EGP = float(os.getenv("B2E_EGP"))
E2B_BGP = float(os.getenv("E2B_BGP"))
GENGASPRICE1 = float(os.getenv("GENGASPRICE1"))
GENGASPRICE2 = float(os.getenv("GENGASPRICE2"))
EXTRACLI = str(os.getenv("EXTRACLI"))
OWNER_ACCOUNT = str(os.getenv("OWNER_ACCOUNT"))
LOG_KEY = str(os.getenv("LOG_KEY"))

app = Flask(__name__)
CORS(app)

app.logger.info(f"ERC-20 : {erc20Name}")
app.logger.info(f"BEP-2 : {bep2Name}")

client.server_info() # would fail if the DB doesn't connect

df = Dfuse()

ethTxnHashDict = {}

def pollEthX():

    ethTxnHashRem = []

    for txnHash in ethTxnHashDict:
        app.logger.info(f"Checking Hash : {txnHash}")

        ropstenEndpoint = "https://ropsten.infura.io/v3/9f34d0bf5e1b4b36914fd5bc66c50b05"
        data = '{"jsonrpc":"2.0","method":"eth_getTransactionReceipt","params": ["'+txnHash +'"],"id":1}'
        headers = {"Content-Type": "application/json"}
        res = requests.post(ropstenEndpoint, data=data, headers=headers).json()
        # print(res)
        try:
            # if type(res['result']) != type(None) and bool(int(res['result']['status'], 16)) == True:
            if type(res['result']) != type(None):
                amount = 0

                try:
                    amount = int(res["result"]["logs"][0]["data"], 0)
                    print(amount)
                except:
                    ethTxnHashRem.append(txnHash)

                if(isBinanceAdd(ethTxnHashDict[txnHash])):
                    app.logger.info(f"[ETH-BIN SWAP] ==> Binance Swap Detected")

                    amount = int(amount / (10 ** 10))

                    cmd = f"{EXTRACLI}tbnbcli token mint --amount { amount } --symbol {bep2Name} --from anudittest --chain-id=Binance-Chain-Nile --node=data-seed-pre-2-s1.binance.org:80 --trust-node"
                    p = Popen(cmd.split(" "), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                    grep_stdout = p.communicate(
                        input=bytes(os.getenv("KEYPASS").encode("UTF-8"))
                    )[0]
                    # app.logger.info(grep_stdout)
                    # app.logger.info(f"[ETH-BIN SWAP] ==> {bep2Name} Minted")
                    btxhash = grep_stdout.decode().split("\"hash\": \"")[1][:64]
                    app.logger.info(f"[ETH-BIN SWAP] ==> {bep2Name} Minted {btxhash}")

                    # time.sleep(1)

                    amount = int(amount - E2B_BGP)

                    cmd = f"{EXTRACLI}tbnbcli send --from anudittest --to { ethTxnHashDict[txnHash] } --amount {amount}:{bep2Name} --chain-id=Binance-Chain-Nile --node=data-seed-pre-2-s1.binance.org:80 --json --memo AtomixSwap"
                    p = Popen(cmd.split(" "), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                    grep_stdout = p.communicate(
                        input=bytes(os.getenv("KEYPASS").encode("UTF-8"))
                    )[0]
                    # app.logger.info(grep_stdout)
                    # app.logger.info(f"[ETH-BIN SWAP] ==> {bep2Name} Transferred")
                    data = grep_stdout.decode().split("\"hash\": \"")[1][:64]
                    app.logger.info(f"[ETH-BIN SWAP] ==> {bep2Name} Transferred {data}")

                    ethTxnHashRem.append(txnHash)

                elif(isEosAdd(ethTxnHashDict[txnHash])):
                    app.logger.info(f"[ETH-EOS SWAP] ==> EOS Swap Detected")
                    try:
                        redeemAdd = ethTxnHashDict[txnHash]
                        amount = str(format((amount/(10**18) - GENGASPRICE1), '.4f'))
                        amountString = f"{amount} ANT"
                        app.logger.info(f"[BIN-EOS SWAP] ==> Redeem Add : {redeemAdd}  and Amount : {amountString}")
                        txnH = eos_issue(amountString)
                        txnH2 = eos_transfer(redeemAdd, amountString)

                        app.logger.info(f"[ETH-EOS SWAP] ==> EOS Swap DONE {txnH2}")
                        ethTxnHashRem.append(txnHash)

                    except Exception as e:
                        app.logger.info(str(e))
                        ethTxnHashRem.append(txnHash)


        except Exception as e:
            app.logger.info(str(e))
            continue

    if (len(ethTxnHashRem) > 0):
        app.logger.info(f"[ETH-BIN SWAP] ==> DELETING REDEEMED TXNS")
        for x in ethTxnHashRem:
            del ethTxnHashDict[x]
        ethTxnHashRem = []

eosTxnHashDict = {}

def pollEosX():

    bearerToken = "kk"
    eosTxnHashRem = []

    for txnHash in eosTxnHashDict:
        app.logger.info(f"[EOS-x SWAP] ==> Checking {txnHash}")

        txnDat = df.getEosTxn(txnHash, bearerToken)
        # app.logger.info(txnDat)

        if(('code' in txnDat) and (txnDat['code'] == 'auth_invalid_token_error')):

            app.logger.info(f"[EOS-x SWAP] ==> Updating Bearer Token as {txnDat['code']}")
            bearerToken = df.updateBearerToken()
            txnDat = df.getEosTxn(txnHash, bearerToken)

        if(('code' in txnDat) and txnDat['code'] == 'data_trx_not_found_error'):

            app.logger.info(f"[EOS-x SWAP] ==> INVALID HASH {txnHash}")
            # del eosTxnHashDict[txnHash]
            eosTxnHashRem.append(txnHash)

        elif('code' in txnDat):

            app.logger.info(f"[EOS-x SWAP] ==> UNKNOWN CODE {txnDat['code']}")
            # del eosTxnHashDict[txnHash]

            eosTxnHashRem.append(txnHash)

        elif (txnDat['execution_irreversible'] == False):

            app.logger.info(f"[EOS-x SWAP] ==> NOT YET IRREVERSIBLE {txnHash}")

        elif (txnDat['execution_irreversible'] == True):

            # pprint(txnDat)

            txnDetails = txnDat['execution_trace']['action_traces'][0]['act']['data']
            fromAccount = txnDetails['from']
            toAccount = txnDetails['to']
            redeemAdd = txnDetails['memo']
            redeemAmount = float(txnDetails['quantity'].split(" ")[0])

            # pprint(txnDetails)

            if((toAccount).lower() == (OWNER_ACCOUNT).lower()):

                if(isBinanceAdd(redeemAdd) == True):

                    amount = int(redeemAmount * (10 ** 8))

                    cmd = f"{EXTRACLI}tbnbcli token mint --amount { amount } --symbol {bep2Name} --from anudittest --chain-id=Binance-Chain-Nile --node=data-seed-pre-2-s1.binance.org:80 --trust-node"
                    p = Popen(cmd.split(" "), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                    grep_stdout = p.communicate(
                        input=bytes(os.getenv("KEYPASS").encode("UTF-8"))
                    )[0]
                    # app.logger.info(grep_stdout)
                    # app.logger.info(f"[ETH-BIN SWAP] ==> {bep2Name} Minted")
                    btxhash = str(grep_stdout.decode()).split("tx hash: ")[1][:64]
                    app.logger.info(f"[EOS-BIN SWAP] ==> {bep2Name} Minted {btxhash}")

                    # time.sleep(1)

                    amount = int(amount)

                    cmd = f"{EXTRACLI}tbnbcli send --from anudittest --to { redeemAdd } --amount {amount}:{bep2Name} --chain-id=Binance-Chain-Nile --node=data-seed-pre-2-s1.binance.org:80 --json --memo AtomixSwap"
                    p = Popen(cmd.split(" "), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                    grep_stdout = p.communicate(
                        input=bytes(os.getenv("KEYPASS").encode("UTF-8"))
                    )[0]
                    # app.logger.info(grep_stdout)
                    # app.logger.info(f"[ETH-BIN SWAP] ==> {bep2Name} Transferred")
                    data = json.loads(grep_stdout.decode("utf8"))
                    app.logger.info(f"[EOS-BIN SWAP] ==> {bep2Name} Transferred {data['TxHash']}")

                    eosTxnHashRem.append(txnHash)

                    app.logger.info(f"[EOS-x SWAP] ==> UPDATING DB")
                    record = TxnObject(txnHash,redeemAdd)
                    insertEosRecord(record)

                    app.logger.info(f"[EOS-BIN SWAP] Burning EOS")
                    eos_retire(txnDetails['quantity'])


                elif(isEthereumAdd(redeemAdd) == True):

                    userAddress = Web3.toChecksumAddress(redeemAdd)

                    w3 = Web3(
                        HTTPProvider(
                            "https://ropsten.infura.io/v3/9f34d0bf5e1b4b36914fd5bc66c50b05"
                        )
                    )

                    private_key = os.getenv("PRIVATEKEY")
                    acct = w3.eth.account.privateKeyToAccount(private_key)
                    ownerAddress = acct.address
                    tokenContractAddress = Web3.toChecksumAddress(TOKEN_CONTRACT_ADDRESS)

                    tokenContract = w3.eth.contract(address=tokenContractAddress, abi=TOKEN_ABI)

                    swapAmount = redeemAmount * (10 ** 18)
                    swapAmount = int(swapAmount)

                    app.logger.info(f"[EOS-ETH SWAP] ==> Minting {swapAmount} {erc20Name}")

                    txn = tokenContract.functions.mint(
                        userAddress, int(swapAmount)
                    ).buildTransaction(
                        {
                            "nonce": w3.eth.getTransactionCount(acct.address),
                            "from": acct.address,
                            "gas": 65000,
                            "gasPrice": 1000000000,
                            "value": 0,
                            "chainId": 3,
                        }
                    )

                    signed_txn = w3.eth.account.signTransaction(txn, private_key)
                    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
                    tx_hash = str(tx_hash.hex())
                    app.logger.info(f"[EOS-ETH SWAP] ==> {erc20Name} Minted {tx_hash}")

                    eosTxnHashRem.append(txnHash)

                    app.logger.info(f"[EOS-x SWAP] ==> UPDATING DB")
                    record = TxnObject(txnHash,redeemAdd)
                    insertEosRecord(record)

                    app.logger.info(f"[EOS-ETH SWAP] Burning EOS")
                    eos_retire(txnDetails['quantity'])


                else:
                    continue

    if (len(eosTxnHashRem) > 0):
        app.logger.info(f"[EOS-x SWAP] ==> DELETING REDEEMED TXNS")
        for x in eosTxnHashRem:
            del eosTxnHashDict[x]
        eosTxnHashRem = []

sched = BackgroundScheduler(daemon=True)
sched.add_job(pollEthX, "interval", seconds=10)
sched.add_job(pollEosX, "interval", seconds=5)
sched.start()


@app.errorhandler(404)
def not_found(error):
    app.logger.error(str(error))
    return jsonify({'error': 'Not found'}), 404

@app.route("/")
def start():
    return "<p style='margin: 20px;font-family: monospace;'>👋 from the AtomiX Swap Server</p>"

@app.route("/test")
def test():
    app.logger.info("Test Endpoint Invoked")
    response = app.response_class(
        response=json.dumps({"success": True, "data": "Connected."}),
        status=200,
        mimetype="application/json",
    )
    return response

@app.route('/applog')
def applog():
    if(request.args.get("accesskey") != None and request.args.get("accesskey") == LOG_KEY):
        if(os.path.exists('app.log') != True):
            response = app.response_class(
                response=json.dumps({"error": "Log file not found"}),
                status=404,
                mimetype="application/json",
            )
            return response
        else:
            f = open("app.log", "r")
            response = app.response_class(
                response=f.read(),
                status=200,
                mimetype='text/plain',
            )
            return response
    else:
        response = app.response_class(
            response=json.dumps({"error": "Invalid Access Key"}),
            status=403,
            mimetype="application/json",
        )
        return response

@app.route('/accesslog')
def accesslog():
    if(request.args.get("accesskey") != None and request.args.get("accesskey") == LOG_KEY):
        if(os.path.exists('app.log') != True):
            response = app.response_class(
                response=json.dumps({"error": "Log file not found"}),
                status=404,
                mimetype="application/json",
            )
            return response
        else:
            f = open("access.log", "r")
            response = app.response_class(
                response=f.read(),
                status=200,
                mimetype='text/plain',
            )
            return response
    else:
        response = app.response_class(
            response=json.dumps({"error": "Invalid Access Key"}),
            status=403,
            mimetype="application/json",
        )
        return response

@app.route("/faucet", methods=["POST"])
def faucet():
    add = request.form.get("add")

    app.logger.info(f"[FAUCET] ==> add : {add}")

    if (type(add) != str):
        response = app.response_class(
            response=json.dumps({"success": False, "data": "No Address Sent"}),
            status=200,
            mimetype="application/json",
        )
        return response

    if (isEthereumAdd(add) != True):
        response = app.response_class(
            response=json.dumps({"success": False, "data": "Invalid Address"}),
            status=200,
            mimetype="application/json",
        )
        return response


    if (isRecent(add) == False):
        if(insertFaucetTxn(FaucetTxn(add)) == True):

            userAddress = Web3.toChecksumAddress(add)

            w3 = Web3(
                HTTPProvider(
                    "https://ropsten.infura.io/v3/9f34d0bf5e1b4b36914fd5bc66c50b05"
                )
            )

            private_key = os.getenv("PRIVATEKEY")
            acct = w3.eth.account.privateKeyToAccount(private_key)
            ownerAddress = acct.address
            tokenContractAddress = Web3.toChecksumAddress(TOKEN_CONTRACT_ADDRESS)

            tokenContract = w3.eth.contract(address=tokenContractAddress, abi=TOKEN_ABI)

            amt = 100 * (10 ** 18)

            app.logger.info(f"[FAUCET] ==> Transferring {amt} {erc20Name}")

            txn = tokenContract.functions.transfer(
                userAddress, int(amt)
            ).buildTransaction(
                {
                    "nonce": w3.eth.getTransactionCount(acct.address),
                    "from": acct.address,
                    "gas": 65000,
                    "gasPrice": 1000000000,
                    "value": 0,
                    "chainId": 3,
                }
            )

            signed_txn = w3.eth.account.signTransaction(txn, private_key)
            tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_hash = str(tx_hash.hex())
            app.logger.info(f"[FAUCET] ==> {erc20Name} TRANSFERRED {tx_hash}")

            response = app.response_class(
                response=json.dumps({"success": True, "data": tx_hash}),
                status=200,
                mimetype="application/json",
            )
            return response
        else:
            response = app.response_class(
                response=json.dumps({"success": False, "data": "DB Error"}),
                status=200,
                mimetype="application/json",
            )
            return response
    else:
        response = app.response_class(
            response=json.dumps({"success": False, "data": "Too Soon"}),
            status=200,
            mimetype="application/json",
        )
        return response

@app.route("/eth-x", methods=["POST"])
def eth_x():
    try:
        txnHash = request.form.get("txnHash")
        redeemAdd = request.form.get("redeemAdd")
        if (type(redeemAdd) != str):
            response = app.response_class(
                response=json.dumps({"success": False, "data": "No Transaction Redeemer"}),
                status=200,
                mimetype="application/json",
            )
            return response

        ethTxnHashDict[txnHash] = redeemAdd
        app.logger.info(f"[ETH-X SWAP] ==>  txnHash : {txnHash} and redeemAdd : {redeemAdd}")
        response = app.response_class(
            response=json.dumps({"success": True, "data": "Transaction Queued"}),
            status=200,
            mimetype="application/json",
        )
        return response

    except:
        response = app.response_class(
            response=json.dumps(
                {"success": False, "data": "Error"}
            ),
            status=200,
            mimetype="application/json",
        )
        return response

@app.route("/eos-x", methods=["POST"])
def eos_x():
    try:
        txnHash = request.form.get("txnHash")
        if (txnHash in eosTxnHashDict):
            response = app.response_class(
                response=json.dumps(
                    {"success": False, "data": f"TxnHash Already Queued"}
                ),
                status=200,
                mimetype="application/json",
            )
            return response
        else:
            if (doesEosHashExist(txnHash) == True):
                response = app.response_class(
                    response=json.dumps(
                        {"success": True, "data": f"TxnHash Already Redeemed"}
                    ),
                    status=200,
                    mimetype="application/json",
                )
                return response
            else:
                eosTxnHashDict[txnHash] = "something"
                app.logger.info(f"[EOS-X SWAP] ==>  txnHash : {txnHash}")

                response = app.response_class(
                    response=json.dumps(
                        {"success": True, "data": f"TxnHash Queued"}
                    ),
                    status=200,
                    mimetype="application/json",
                )
                return response
    except:
        return ":("


@app.route("/bin-x", methods=["POST"])
def bin_x():

    ethAdd = request.form.get("ethAdd")
    btxnHash = request.form.get("btxnHash")

    app.logger.info(f"[BIN-X SWAP] ==> btxnHash : { btxnHash } and ethAdd : { ethAdd }")

    if (doesBinanceHashExist(btxnHash) == True):
        response = app.response_class(
            response=json.dumps(
                {"success": False, "data": "Transaction Already Redeemed"}
            ),
            status=200,
            mimetype="application/json",
        )
        return response


    r = requests.get(url=f"https://testnet-dex.binance.org/api/v1/tx/{ btxnHash }?format=json")
    res = json.loads(r.text)
    # pprint(res)

    swapAmount = ""
    redeemAdd = ""

    try:
        if res["code"] == 0:
            if (res["ok"] == True
                and res["tx"]["value"]["msg"][0]["value"]["outputs"][0]["coins"][0]["denom"]== bep2Name
                and res["tx"]["value"]["msg"][0]["value"]["outputs"][0]["address"] == "tbnb16uq5gcvg25psr2gqt5y0svn4j53n39lzxkuvl7"):

                # if str(redeemAdd).lower() == str(res["tx"]["value"]["memo"]).lower():

                # else:
                #     response = app.response_class(
                #         response=json.dumps(
                #             {"success": False, "data": "Incorrect Redeemer Address"}
                #         ),
                #         status=200,
                #         mimetype="application/json",
                #     )
                #     return response

                redeemAdd = str(res["tx"]["value"]["memo"]).lower()

                swapAmount = int(
                    res["tx"]["value"]["msg"][0]["value"]["outputs"][0]["coins"][0]["amount"]
                )

                swapAmount = int((swapAmount - B2E_BGP))

                app.logger.info(f"[BIN-X SWAP] ==> Amount Locked { swapAmount }")

                cmd2 = f"{EXTRACLI}tbnbcli token burn --amount { swapAmount } --symbol { bep2Name } --from anudittest --chain-id=Binance-Chain-Nile --node=data-seed-pre-2-s1.binance.org:80 --trust-node"
                p = Popen(cmd2.split(" "), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                grep_stdout = p.communicate(input=bytes(os.getenv("KEYPASS").encode("UTF-8")))[0]
                btxhash = str(grep_stdout.decode()).split("tx hash: ")[1][:64]
                app.logger.info(f"[BIN-X SWAP] ==> {bep2Name} Burnt {btxhash}")

            else:
                response = app.response_class(
                    response=json.dumps(
                        {"success": False, "data": "Incorrect Transaction Details"}
                    ),
                    status=200,
                    mimetype="application/json",
                )
                return response
        else:
            response = app.response_class(
                response=json.dumps({"success": False, "data": "Invalid Hash"}),
                status=200,
                mimetype="application/json",
            )
            return response
    except:
        response = app.response_class(
            response=json.dumps({"success": False, "data": "EXP Invalid Hash"}),
            status=200,
            mimetype="application/json",
        )
        return response


    if(isEthereumAdd(redeemAdd) == True):
        app.logger.info(f"[BIN-ETH SWAP] ==> Ethereum Swap Detected")

        if (redeemAdd != str(ethAdd).lower()):
            response = app.response_class(
                response=json.dumps({"success": False, "data": "Incorrect Redeemer"}),
                status=200,
                mimetype="application/json",
            )
            return response

        userAddress = Web3.toChecksumAddress(redeemAdd)

        w3 = Web3(
            HTTPProvider(
                "https://ropsten.infura.io/v3/9f34d0bf5e1b4b36914fd5bc66c50b05"
            )
        )

        private_key = os.getenv("PRIVATEKEY")
        acct = w3.eth.account.privateKeyToAccount(private_key)
        ownerAddress = acct.address
        tokenContractAddress = Web3.toChecksumAddress(TOKEN_CONTRACT_ADDRESS)

        tokenContract = w3.eth.contract(address=tokenContractAddress, abi=TOKEN_ABI)

        swapAmount = swapAmount * (10 ** 10)
        swapAmount = int(swapAmount - B2E_EGP)

        app.logger.info(f"[BIN-ETH SWAP] ==> Minting {swapAmount} {erc20Name}")

        txn = tokenContract.functions.mint(
            userAddress, int(swapAmount)
        ).buildTransaction(
            {
                "nonce": w3.eth.getTransactionCount(acct.address),
                "from": acct.address,
                "gas": 65000,
                "gasPrice": 1000000000,
                "value": 0,
                "chainId": 3,
            }
        )

        signed_txn = w3.eth.account.signTransaction(txn, private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_hash = str(tx_hash.hex())
        app.logger.info(f"[BIN-ETH SWAP] ==> {erc20Name} Minted {tx_hash}")

        record = TxnObject(btxnHash,redeemAdd)
        insertBinanceRecord(record)

        response = app.response_class(
            response=json.dumps({"success": True, "data": tx_hash}),
            status=200,
            mimetype="application/json",
        )
        return response

    elif(isEosAdd(redeemAdd) == True):
        app.logger.info(f"[BIN-EOS SWAP] ==> EOS Swap Detected")
        try:
            amount = str(format((swapAmount/(10**8)), '.4f'))
            amountString = f"{amount} ANT"
            app.logger.info(f"[BIN-EOS SWAP] ==> Redeem Add : {redeemAdd}  and Amount : {amountString}")
            txnH = eos_issue(amountString)
            txnH2 = eos_transfer(redeemAdd, amountString)

            record = TxnObject(btxnHash,redeemAdd)
            insertBinanceRecord(record)

            response = app.response_class(
                response=json.dumps({"success": True, "data": txnH2}),
                status=200,
                mimetype="application/json",
            )
            return response
        except:
            response = app.response_class(
                response=json.dumps({"success": False, "data": f"Invalid EOS Address"}),
                status=200,
                mimetype="application/json",
            )
            return response
    else:
        response = app.response_class(
            response=json.dumps(
                {"success": False, "data": f"Invalid Address"}
            ),
            status=200,
            mimetype="application/json",
        )
        return response

if __name__ != "__main__":
    # conditions for gunicorn
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == "__main__":
    # conditions for normal Execution
    app.run(host="127.0.0.1", port="5000", debug=True, use_reloader=False, threaded=True)
