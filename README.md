# Mancala: The Game ![Test](https://github.com/kyokley/mancala/workflows/Test/badge.svg)

![Screenshot](/../screenshot/screenshots/game.gif?raw=true)

[Mancala](https://en.wikipedia.org/wiki/Mancala) is a two player game where players take turns moving stones or seeds around a board. The objective is for the player to capture more seeds or stones than their opponent.

## Installation

Currently, this package is not available on PYPI so the easiest way to install it is to use pip and install from git

From inside a virtualenv, run the following:
```
pip install git+https://github.com/kyokley/mancala/
```

Alternatively, if you are running docker, and have make installed, you may simply run `make build`.

## Playing the Game

### Single Game

#### Getting Started
After installing, a new game can be started by entering `mancala` (or `mancala-series` to run multiple games) at the prompt. You will then be asked for the number of seeds per cup to begin the game with. Once this value has been provided, the game begins.

#### Objective
Player 1 will attempt to collect seeds in the leftmost cup while Player 2 will attempt the same in the rightmost cup. The player with the most seeds in their cup at the end of the game is the winner. The game is over when all seeds have been moved to either Player 1 or Player 2's cups.

#### Taking Turns
Players take turns selecting indices (a, b, c, ...), removing all "seeds" from that "cup", and placing them one-by-one in subsequent "cups" in a clockwise direction. If the last seed falls in the player's cup, the player gets to take another turn.
