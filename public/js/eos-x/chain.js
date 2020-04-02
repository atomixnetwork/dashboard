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
        let txnHash = document.getElementById("txnHash").value ;

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
        let result = await promise;
        return JSON.parse(result);
    }
    else{
        return false;
    }

}
