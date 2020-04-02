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
    document.getElementById("formGetTokenSubmit").addEventListener("click", getTokens);
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

async function getTokens(){

    document.getElementById("formGetTokenSubmit").innerHTML = "Processing";

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText)
            let obj =  JSON.parse(this.responseText);
            if(obj['success'] == true){
                messageTitle = "Success"
                messageHTML = "<a href='https://ropsten.etherscan.io/tx/"+obj['data']+"' target='_blank'>View Your Transaction</a>";
                document.getElementById("formGetTokenSubmit").innerHTML = "Thanks";
            }
            else{
                messageTitle = "Hold On";
                messageHTML = obj['data'];
                document.getElementById("formGetTokenSubmit").innerHTML = "Get Tokens";
            }
            showModal(title=messageTitle, body=messageHTML);
        }
    };
    xhttp.open("POST", endpoint + "/faucet", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("add="+ web3.eth.defaultAccount );




}

