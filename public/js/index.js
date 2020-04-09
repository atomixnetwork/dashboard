let CoinContract = undefined;
let Coin = undefined;
let biconomy;

window.addEventListener('load', async () => {
    if (typeof window.ethereum !== 'undefined') {
        ethereum.on('accountsChanged', function (accounts) {
            window.location.reload();
        })

        ethereum.on('chainChanged', function (netId) {
            if(netId != 16110){
                showModal("Warning ⚠", "Please switch to https://betav2.matic.network");
            }
        })
        // window.web3 = new Web3(ethereum);
        // try {
            // 	await ethereum.enable();
            // 	web3.version.getNetwork((err, netId) => {
                // 		if(netId != 16110){
                    // 			alert("Please switch to https://betav2.matic.network");
                    // 		}
                    // 	});
                    // 	CoinContract = web3.eth.contract(coinABI);
                    //  Coin = CoinContract.at(CoinAddress);

                    // } catch (error) {
                        // 	console.log(error);
                        // 	alert("MetaMask Denied");
                        // }

        if (window.Biconomy) {
            let Biconomy = window.Biconomy;
            let options = {
                dappId: '5e8af105f64c16288c945039',
                apiKey: 'rpC-RfNiI.9aa40a94-c6a2-4434-a46c-77e9c60ea239',
                strictMode: false,
                debug: true
            };
            biconomy = new Biconomy(window.ethereum, options);
            console.log(biconomy);
            web3 = new Web3(biconomy);
        }

        biconomy.onEvent(biconomy.READY, async () => {
            await ethereum.enable();
            console.table(biconomy.dappAPIMap);
            if(!biconomy.isLogin) {
                await biconomyLogin();
            }

            web3.version.getNetwork((err, netId) => {
                if(netId != 16110){
                    showModal("Warning ⚠", "Please switch to https://betav2.matic.network");
                }
            });
            CoinContract = web3.eth.contract(coinABI);
            Coin = CoinContract.at(CoinAddress);
            await init();

        }).onEvent(biconomy.ERROR, (error, message) => {
            console.log("Mexa Error", error);
        });

    } else if (window.web3) {
        web3.version.getNetwork((err, netId) => {
            if(netId != 16110){
                showModal("Warning ⚠", "Please switch to https://betav2.matic.network");
            }
          })
        window.web3 = new Web3(web3.currentProvider);
        web3.eth.defaultAccount = web3.eth.accounts[0];
        CoinContract = web3.eth.contract(coinABI);
        Coin = CoinContract.at(CoinAddress);

        init();
    } else {
        showModal("Warning 🚨", "Get a Web3 Compatible Browser");
    }
});

async function biconomyLogin(){

	let promise = new Promise(async (res, rej) => {

		try{

			biconomy.login(await biconomy.getUserAccount(), (error, response) => {
				if(response.transactionHash) {
					console.log("New User");
					res(true);
				} else if(response.userContract) {
					console.log("Existing User Contract: " + response.userContract);
					res(true);
				}
			});

			biconomy.onEvent(biconomy.LOGIN_CONFIRMATION, (log) => {
				console.log(`User contract wallet address: ${log.userContract}`);
			});

		 } catch(error) {
			console.log(`Error Code: ${error.code} Error Message: ${error.message}`);
			rej(false);
		 }

    });
	let result = await promise;
    console.log(result);
    return result;

}

async function getUserContract(){

    if (biconomy){
        return biconomy.getUserContract(await biconomy.getUserAccount())
    }
    else{
        return "0x000000000"
    }
}

document.getElementsByClassName("close-modal")[0].addEventListener("click", closeModal);

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

// if ('serviceWorker' in navigator) {
//     navigator.serviceWorker.register('../serviceworker.js');
// }
