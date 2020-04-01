import requests
txnHash = "0x237183f03afd3a2d7cd97dc37edeb618579b9e15280f35580d100ff11e22e489"

ropstenEndpoint = "https://ropsten.infura.io/v3/c66eb274af774bcc913c47eb60888a20"
data = '{"jsonrpc":"2.0","method":"eth_getTransactionReceipt","params": ["'+txnHash +'"],"id":1}'


headers = {"Content-Type": "application/json"}
response = requests.post(ropstenEndpoint, data=data, headers=headers).json()
print(int(response["result"]["logs"][0]["data"], 0)/(10**18))
print(bool(int(response['result']['status'], 0)))
