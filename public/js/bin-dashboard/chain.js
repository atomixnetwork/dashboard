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
