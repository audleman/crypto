import brownie
from brownie import accounts, Lupi
import pytest

#-------------------------------------------------------------------------------
# Fixtures
#-------------------------------------------------------------------------------

@pytest.fixture(scope='module', autouse=True)
def lupi(Lupi, accounts):
    yield Lupi.deploy({'from': accounts[0]})
    
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

@pytest.fixture(scope='module')
def owner():
    return accounts[0]

#-------------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------------

def test_startGame(lupi, accounts, owner):
    assert lupi.getStatus() == 0
    lupi.startGame({'from': owner})
    assert lupi.getStatus() == 1
    assert lupi.getNumPlayers() == 0

def test_submitGuess_game_not_started_reverts(lupi, accounts):
    player1 = accounts[1]
    with brownie.reverts():
        lupi.submitGuess(1, {'from': player1, 'amount': lupi.getBetAmount()})
    
def test_submitGuess_wrong_bet_reverts(lupi, accounts, owner):
    player1 = accounts[1]
    lupi.startGame({'from': owner})
    with brownie.reverts():
        lupi.submitGuess(1, {'from': player1, 'amount': lupi.getBetAmount() - 1})
    
def test_submitGuess__multiple_calls_reverts(lupi, accounts, owner):
    player1 = accounts[1]
    lupi.startGame({'from': owner})
    lupi.submitGuess(1, {'from': player1, 'amount': lupi.getBetAmount()})
    with brownie.reverts():
        lupi.submitGuess(1, {'from': player1, 'amount': lupi.getBetAmount()})

def test_submitGuess__success(lupi, accounts, owner):
    player1 = accounts[1]
    lupi.startGame({'from': owner})
    lupi.submitGuess(1, {'from': player1, 'amount': lupi.getBetAmount()})
    assert lupi.getNumPlayers() == 1
    assert lupi.getMyGuess({'from': player1}) == 1
    assert lupi.balance() == lupi.getBetAmount()
        
def test_updateGuess_called_before_submitGuess_reverts(lupi, accounts, owner):
    player1 = accounts[1]
    lupi.startGame({'from': owner})
    with brownie.reverts():
        lupi.updateGuess(1, {'from': player1})
        
def test_updateGuess_is_not_payable(lupi, accounts, owner):
    player1 = accounts[1]
    lupi.startGame({'from': owner})
    lupi.submitGuess(1, {'from': player1, 'amount': lupi.getBetAmount()})
    with brownie.reverts():
        lupi.updateGuess(1, {'from': player1, 'amount': lupi.getBetAmount()})
        
def test_updateGuess_success(lupi, accounts, owner):
    lupi.startGame({'from': owner})
    player1 = accounts[1]
    lupi.submitGuess(1, {'from': player1, 'amount': lupi.getBetAmount()})
    lupi.updateGuess(2, {'from': player1})
    assert lupi.getMyGuess({'from': player1}) == 2
    
def test_endGame__success(lupi, accounts, owner):
    player1 = accounts[1]
    player2 = accounts[2]
    starting_balance = player1.balance()
    lupi.startGame({'from': owner})
    lupi.submitGuess(1, {'from': player1, 'amount': lupi.getBetAmount()})
    lupi.submitGuess(2, {'from': player2, 'amount': lupi.getBetAmount()})
    assert lupi.balance() == lupi.getBetAmount() * 2
    lupi.endGame({'from': owner})
    assert player1.balance() == starting_balance + 980
    assert player2.balance() == starting_balance - 1000
    assert owner.balance() == starting_balance + 20
    
def test_endGame__foo(lupi, accounts, owner):
    player1 = accounts[1]
    player2 = accounts[2]
    player3 = accounts[3]
    player4 = accounts[4]
    starting_balance = player1.balance()
    lupi.startGame({'from': owner})
    lupi.submitGuess(10, {'from': player1, 'amount': lupi.getBetAmount()})
    lupi.submitGuess(5, {'from': player2, 'amount': lupi.getBetAmount()})
    lupi.submitGuess(20, {'from': player3, 'amount': lupi.getBetAmount()})
    lupi.submitGuess(5, {'from': player4, 'amount': lupi.getBetAmount()})
    gg = lupi.getAllGuesses()
    # print(gg.call_trace())
    # print(gg.return_value)
    # import ipdb; ipdb.set_trace()