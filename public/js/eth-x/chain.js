let t_accEthBal = 0;
let t_accAncBal = 0;

async function getEthBalance() {
    let promise = new Promise((res, rej) => {
        web3.eth.getBalance(web3.eth.defaultAccount, function(error, result) {
            if (!error)
                res(result);
            else
                rej(error);
        });
    });
    let result = await promise;
    t_accEthBal = result;
    return t_accEthBal;
}

async function getTokenBalance() {
    let promise = new Promise((res, rej) => {
        Coin.balanceOf(web3.eth.defaultAccount, function(error, result) {
            if (!error)
                res(result);
            else
                rej(error);
        });
    });
    let result = await promise;
    t_accAncBal = result;
    return t_accAncBal;
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
