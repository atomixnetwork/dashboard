from subprocess import Popen, PIPE, STDOUT
import os
from dotenv import load_dotenv
load_dotenv()
amount = 1010*(10**8)

cmd = f"tbnbcli token mint --amount { amount } --symbol ANC-3EF --from anudittest --chain-id=Binance-Chain-Nile --node=data-seed-pre-2-s1.binance.org:80 --trust-node"

p = Popen(cmd.split(" "), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
grep_stdout = p.communicate(input=bytes(os.getenv("KEYPASS").encode('UTF-8')))[0]
print(grep_stdout.decode())
