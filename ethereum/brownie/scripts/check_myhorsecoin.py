from brownie import accounts, config, MyHorseCoin

# Small supply w/ no decimals. Only whole horse coins allowed
initial_supply = 69

def main():
    account = accounts[0]
    # 0xe2145d7e1d4413f24598ae087675f25af5669aed
    amt = MyHorseCoin.balanceOf(account)
    print(f'Total supply of HORSE: {amt}')
    
    