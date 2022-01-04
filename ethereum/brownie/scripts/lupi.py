from brownie import accounts, config, Lupi

# Small supply w/ no decimals. Only whole horse coins allowed
initial_supply = 69

def main():
    owner = accounts[0]
    lupi = Lupi.deploy({'from': owner})
    print(f'Game status: {lupi.getStatus()}')
    lupi.startGame({'from': owner})
    print(f'Game status after starting game: {lupi.getStatus()}')
    player1 = accounts[1]
    player2 = accounts[2]
    lupi.submitGuess(30, {'from': player1, 'value': 1000})
    lupi.submitGuess(20, {'from': player2, 'value': 1000})
    print(f'Number of players: {lupi.getNumPlayers()}')
    
    
    
    