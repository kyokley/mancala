import itertools
import random
import time

from src.terminal import Location, Terminal

RANDOM_PLAYER_WAIT_TIME = 1
rand = random.SystemRandom()


class Player:
    def __init__(self, name, board):
        self.term = Terminal()
        self.name = name
        self.board = board

    def take_turn(self):
        self.term.move(*Location(19, 0))
        print(f"{self.name}'s turn")


class HumanPlayer(Player):
    def take_turn(self):
        super().take_turn()
        cup = input('Enter cup to sow: ')
        return cup


class RandomPlayer(Player):
    def __init__(self, name, board, wait_time=RANDOM_PLAYER_WAIT_TIME):
        super().__init__(name, board)
        self.wait_time = wait_time

    def take_turn(self):
        super().take_turn()
        time.sleep(self.wait_time)
        legal_cups = [
            cup
            for cup in itertools.chain(
                self.board.top_row_cups, self.board.bottom_row_cups
            )
            if self.board.cup_seeds(cup) > 0
        ]
        cup = rand.choice(legal_cups)
        print(f'{self.name} chooses {cup}')
        time.sleep(self.wait_time)
        return cup
