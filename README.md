# multichainswapAPI2
Ethereum, Binance, Eos Cross Chain Atomic Swapping API

Install Required Dependencies:

```
sudo apt-get install gunicorn3
npm install -g localtunnel
pip3 install python-dotenv web3 apscheduler flask-cors flask bson dnspython pymongo libeospy
```

## Run the server:

### Windows with WSL

Just run the ```startserver.bat```

### Steps to run on Ubuntu/AWS
```ruby {.line-numbers}
gunicorn app:app --workers 1 --bind 0.0.0.0:5000 --log-file app.log --access-logfile access.log --log-level DEBUG
sudo lt --port 80 --subdomain swap
```
