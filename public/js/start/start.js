window.addEventListener('load', async () => {
    document.getElementById("getStarted").addEventListener("click", gotoSwapPage);
});

function gotoSwapPage(){
    var chain1 = document.getElementById("chain1");
    var chain1Value = chain1.options[chain1.selectedIndex].value;
    var chain2 = document.getElementById("chain2");
    var chain2Value = chain2.options[chain2.selectedIndex].value;
    console.log(chain1Value);
    console.log(chain2Value);
    if(chain1Value == chain2Value){
        console.log("Cannot swap between same chains");
    }
    else if(chain1Value == "Binance"){
        window.location.href = '/bin-x';
    }
    else if(chain1Value == "Ethereum"){
        window.location.href = '/eth-x';
    }
    else if(chain1Value == "EOS"){
        window.location.href = '/eos-x';
    }
}
