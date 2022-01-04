// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

error InvalidBetAmount(uint256 bet, uint256 expected_bet);

contract Lupi is Ownable {

    enum GameStatus { 
        Unititialized, 
        Started,
        Finished 
    }

    struct Player {
        address payable addr;
        uint8 guess;
    }

    GameStatus public status;

    uint256 public gameId;

    // Fixed bet (for now)
    uint256 bet = 1000;
    
    Player[] private players;

    // constructor() { }

    function startGame() public onlyOwner {
        delete players;
        gameId = gameId + 1;
        status = GameStatus.Started;
    }

    function endGame() public onlyOwner {
        assert(status == GameStatus.Started);
        status = GameStatus.Finished;
        Player memory winner = _getWinner();
        uint256 playerShare = (address(this).balance / 100) * 99;
        uint256 contractShare = (address(this).balance / 100);
        winner.addr.transfer(playerShare);
        payable(owner()).transfer(contractShare);
    }

    function _getWinner(Player[] memory sortedPlayers) internal view returns(Player memory) {
        Player memory player = players[0];
        return player;
    }

    function getBetAmount() public view returns (uint256) {
        return bet;
    }

    function getStatus() public view returns (GameStatus) {
        return status;
    }

    function getNumPlayers() public view returns (uint8) {
        return uint8(players.length);
    }

    function playerExists(address addr) internal view returns (bool) {
        for(uint256 i = 0; i < players.length; i++) {
            if (players[i].addr == addr) {
                return true;
            }
        }
        return false;
    }

    function _getPlayerIndex(address addr) internal view returns(uint256) {
        for(uint256 i = 0; i < players.length; i++) {
            if (players[i].addr == addr) {
                return i;
            }
        }
        assert(false);
    }

    function getAllGuesses() public view returns(uint8[] memory) {
        // Copy players into memory array. Sorting costs 20x less gas
        Player[] memory p = new Player[](players.length);
        for(uint256 i = 0; i < players.length; i++) {
            p[i] = players[i];
        }
        _sortPlayers(p, 0, int(players.length - 1));
        uint8[] memory guesses = new uint8[](players.length);
        for(uint256 i = 0; i < p.length; i++) {
            guesses[i] = p[i].guess;
        }
        return guesses;
    }
 
    function getMyGuess() public view returns (uint8) {
        return players[_getPlayerIndex(msg.sender)].guess;
    }

    function submitGuess(uint8 guess) public payable {
        // TODO: implement maxGuesses? Something large enough to not impact
        // gameplay while preventing DDOS
        require(status == GameStatus.Started, "Game has not started");
        if (msg.value != bet) {
            revert InvalidBetAmount(msg.value, bet);
        }
        if (playerExists(msg.sender)) {
            revert("Player is already in game, use updateGuess");
        } 
        Player memory p = Player(payable(msg.sender), guess);
        players.push(p);
    }

    function updateGuess(uint8 guess) public {
        Player storage player = players[_getPlayerIndex(msg.sender)];
        player.guess = guess;
    }

    function _sortPlayers(Player[] memory p, int left, int right) pure internal {
        /*
        In-memory sort of players. This cuts gas cost by ~20x
        */
        int i = left;
        int j = right;
        if(i==j) return;
        uint pivot = p[uint(left + (right - left) / 2)].guess;
        while (i <= j) {
            while (p[uint(i)].guess < pivot) i++;
            while (pivot < p[uint(j)].guess) j--;
            if (i <= j) {
                Player memory tmp = p[uint(i)];
                p[uint(i)] = p[uint(j)];
                p[uint(j)] = tmp;
                i++;
                j--;
            }
        }
        if (left < j)
            _sortPlayers(p, left, j);
        if (i < right)
            _sortPlayers(p, i, right);
    }

}