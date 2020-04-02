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

    if(parseFloat(document.getElementById("formSwapAmount").value) < 1){
        showModal(title="Error", body="A Minimum of 1 ANC required.");
    }
    else{
        const res = await tokenSwap();
        if(res == false){
            showModal(title="Error", body="Not Connected to Server");
        }
        else{
            showModal(title="Success", body="Transaction Queued");
        }
    }

    document.getElementById("formSwapSubmit").innerHTML = "Swap";
}

