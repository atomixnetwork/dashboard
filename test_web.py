from web3 import Web3, HTTPProvider
from pprint import pprint
import os
from ancDetails import ANC_ABI, ANC_CONTRACT_ADDRESS
from dotenv import load_dotenv

load_dotenv()

userAddress = Web3.toChecksumAddress("0x707ac3937a9b31c225d8c240f5917be97cab9f20")
swapAmount = 20000000

w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/c66eb274af774bcc913c47eb60888a20"))

private_key= os.getenv("PRIVATEKEY")
acct = w3.eth.account.privateKeyToAccount(private_key)
ownerAddress = acct.address
ancContractAddress = Web3.toChecksumAddress(ANC_CONTRACT_ADDRESS)

ancContract = w3.eth.contract(address=ancContractAddress,abi=ANC_ABI)

gas_estimate = ancContract.functions.mint(userAddress, swapAmount).estimateGas({'from': acct.address})
print(f"Gas estimate to transact with mint: { gas_estimate }")

print(f"Minting : {swapAmount} ANC")

txn = ancContract.functions.mint(userAddress, swapAmount).buildTransaction(
    {
        'nonce': w3.eth.getTransactionCount(acct.address),
        'from': acct.address,
        'gas': 65000,
        'gasPrice': 1000000000,
        'value': 0,
        'chainId': 3
    }
)

signed_txn = w3.eth.account.signTransaction(txn, private_key)
tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print("Transaction receipt mined: \n")
pprint(receipt)
