from brownie import accounts, config, MyHorseCoin

# Small supply w/ no decimals. Only whole horse coins allowed
initial_supply = 69

def main():
    account = accounts[0]
    coin = MyHorseCoin.deploy(initial_supply, {'from': account})
    
    