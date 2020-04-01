bin_add = "tbnb16uq5gcvg25psr2gqt5y0svn4j53n39lzxkuvl7"
eth_add = "0x707aC3937A9B31C225D8C240F5917Be97cab9F20"
eos_add = "antestacc111"

def isBinanceAdd(add = ""):
    if(len(add) == 43 and (add[:4]).lower() == "tbnb"):
        return True
    else:
        return False

def isEthereumAdd(add = ""):
    if(len(add) == 42 and (add[:2]).lower() == "0x"):
        return True
    else:
        return False

def isEosAdd(add = ""):
    if(len(add) == 12):
        return True
    else:
        return False

# print(isEthereumAdd("0x707aC3937A9B31C225D8C240F5917Be97cab9F20"))
# print(isBinanceAdd("tbnb16uq5gcvg25psr2gqt5y0svn4j53n39lzxkuvl7"))
