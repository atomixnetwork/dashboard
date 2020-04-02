var CoinContract;
var Coin;

window.addEventListener('load', async () => {
    if (window.ethereum) {
        window.web3 = new Web3(ethereum);
        try {
                await ethereum.enable();
                web3.version.getNetwork((err, netId) => {
                    if(netId != 3){
                        showModal(title="Error", body="Please switch to the Ropsten Testnet");
                    }
                  })
                init();
                web3.eth.defaultAccount = web3.eth.accounts[0];
                CoinContract = web3.eth.contract(coinABI);
                Coin = CoinContract.at(CoinAddress);

        } catch (error) {
                console.log(error);
                showModal(title="Error", body="MetaMask Denied");
        }

    } else if (window.web3 || window.web3.currentProvider.isTrust || window.web3.currentProvider.isToshi) {
        web3.version.getNetwork((err, netId) => {
            if(netId != 3){
                showModal(title="Error", body="Please switch to the Ropsten Testnet");
            }
          })
        window.web3 = new Web3(web3.currentProvider);
        web3.eth.defaultAccount = web3.eth.accounts[0];
        CoinContract = web3.eth.contract(coinABI);
        Coin = CoinContract.at(CoinAddress);

        init();
    }else{
        // window.web3  = new Web3(window.web3.currentProvider);
        // web3 = new Web3(new Web3.providers.HttpProvider("https://kovan.infura.io/v3/8f68025ea6a8425cb75ae44591a8b1b3"));
        // web3.eth.defaultAccount = web3.eth.accounts[0];
        // init();
        showModal(title="Error", body="Install a Browser which supports Web3");

    }
});

document.getElementsByClassName("close-modal")[0].addEventListener("click", closeModal);
// var CoinContract = web3.eth.contract(coinABI);

async function testConnection() {
    try{
        let response = await fetch(endpoint + "/test");
        let result = await response.json();
        if(result['success'])
            return true;
        else
            return false;
    }
    catch(error){
        console.log(error);
        return false;
    }
}

function trimAdd(add){
    return add.slice(0,5)+".."+add.slice(add.length-3,add.length);
}
function trimTxnHash(add){
    return add.slice(0,4)+".."+add.slice(add.length-4,add.length);
}
function trimTxnHashl(add=""){
    if (add == null)
        add=""
    return add.slice(0,5)+".."+add.slice(add.length-5,add.length);
}


function b2e() {
    window.location.href = '/b2e';
}
function e2b() {
    window.location.href = '/e2b';
}

async function validateBinanceAdress(bAdd = "tbnb16uq5gcvg25psr2gqt5y0svn4j53n39lzxkuvl7") {
    if (bAdd == "" || bAdd ==" ")
        return false;
    let response = await fetch("https://testnet-dex.binance.org/api/v1/account/"+bAdd);
    let result = await response.json();
    if(!result['code'])
        return true;
    else{
        console.log(result);
        return false;
    }
}

function closeModal(){

    let overlayEle = document.getElementsByClassName("modal-overlay");
    let modalEle = document.getElementsByClassName("modal");
    overlayEle[0].classList.toggle("active", false);
    modalEle[0].classList.toggle("active", false);

}

function showModal(title="", body=""){

    var overlayEle = document.getElementsByClassName("modal-overlay");
    var modalEle = document.getElementsByClassName("modal");
    overlayEle[0].classList.toggle("active", true);
    modalEle[0].classList.toggle("active", true);

    document.getElementById("modalHeading").innerText = title;
    document.getElementById("modalBody").innerHTML = body;

    console.log("MODAL || title:"+title+" body : "+body);
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('serviceworker.js');
}
