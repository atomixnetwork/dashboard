async function init(){

    var connectionEle = document.getElementById("connection");
    connectionEle.classList.toggle("col-warning", true);
    connectionEle.innerText = "Testing Connection";
    if(await testConnection()){
        connectionEle.classList.toggle("col-warning", false);
        connectionEle.classList.toggle("col-error", false);
        connectionEle.classList.toggle("col-success", true);
        connectionEle.innerText = "Connected";
    }
    else{
        connectionEle.classList.toggle("col-success", false);
        connectionEle.classList.toggle("col-warning", false);
        connectionEle.classList.toggle("col-error", true);
        connectionEle.innerText = "Not Connected";
        showModal("Error", "Connection Failed");
    }

    await updateDetails();
    document.getElementById("formSwapSubmit").addEventListener("click", swap);
    connectionEle.addEventListener("click", init);
    document.getElementsByClassName("close-modal")[0].addEventListener("click", closeModal);
}

async function updateDetails(){

    document.getElementById("accAdd").innerText = trimAdd(web3.eth.defaultAccount);
    accEthBal = await getEthBalance();
    document.getElementById("accEthBal").innerText = (accEthBal/(10**18)).toFixed(2);
    accTokenBal = await getTokenBalance();
    document.getElementById("accTokenBal").innerText = (accTokenBal/(10**18)).toFixed(2);

}

async function swap(){

    document.getElementById("formSwapSubmit").innerHTML = "Processing";
    let obj = await tokenSwap();
    if(obj['success'] == true){
        messageTitle = "Success"
        messageHTML = obj['data'];
    }
    else{
        messageTitle = "Error"
        messageHTML = obj['data'];
    }

    showModal(title=messageTitle, body=messageHTML);

    document.getElementById("formSwapSubmit").innerHTML = "Swap";
}
