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

        swapAmount  = (document.getElementById("formSwapAmount").value)*(10**18);

        let promise = new Promise((res, rej) => {
            Coin.burn(swapAmount, function(error, result) {
                if (!error)
                    res(result);
                else
                    rej(error);
            });
        });
        let result = await promise;
        console.log(result);

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                console.log(this.responseText)
            }
        };
        xhttp.open("POST", endpoint + "/eth-x", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("txnHash=" + result + "&redeemAdd=" + document.getElementById("redeemAdd").value );

        return result;
    }
    else{
        return false;
    }

}
