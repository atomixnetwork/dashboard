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

    document.getElementById("accAdd").innerText = trimAdd(ethereum.selectedAddress);
    document.getElementById("accEthBal").innerText = parseFloat(web3.fromWei(await getEthBalance())).toFixed(2);
    document.getElementById("accTokenBal").innerText = parseInt(await getTokenBalance());

}

async function swap(){

    document.getElementById("formSwapSubmit").innerHTML = "Processing";
    let obj = await tokenSwap();
    if(obj['success'] == true){
        messageTitle = "Success"

        if(obj['data'].substring(0, 2) == "0x")
            messageHTML = "<a href='https://ropsten.etherscan.io/tx/"+obj['data']+"' target='_blank'>View Your Transaction</a>";
        else
            messageHTML = "<a href='https://jungle.bloks.io/transaction/"+obj['data']+"' target='_blank'>View Your Transaction</a>";
    }
    else{
        messageTitle = "Error"
        messageHTML = obj['data'];
    }

    showModal(title=messageTitle, body=messageHTML);

    document.getElementById("formSwapSubmit").innerHTML = "Swap";
}
