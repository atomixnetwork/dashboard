async function getEthBalance() {
    let promise = new Promise((res, rej) => {
        web3.eth.getBalance(ethereum.selectedAddress, function(error, result) {
            if (!error)
                res(result);
            else
                rej(error);
        });
    });
    let result = await promise;
    return result;
}

async function getTokenBalance() {
    let promise = new Promise((res, rej) => {
        Coin.balanceOf(ethereum.selectedAddress, function(error, result) {
            if (!error)
                res(result);
            else
                rej(error);
        });
    });
    let result = await promise;
    return result;
}

async function tokenSwap() {
    if (await testConnection()){
        let txnHash = document.getElementById("txnHash").value ;

        if (txnHash.length == 71){
            let promise = new Promise((res, rej) => {
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        console.log(this.responseText)
                        res(this.responseText)
                    }
                };
                xhttp.open("POST", endpoint + "/eos-x", true);
                xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                xhttp.send("txnHash=" + txnHash );
            });
        }
        else{
            return {
                'success':false,
                'data':"Invalid Txn Hash"
            }
        }

        let result = await promise;
        return JSON.parse(result);
    }
    else{
        return false;
    }

}
