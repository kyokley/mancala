import itertools
import random
import time
from enum import IntEnum

from src.terminal import Location, Terminal


class NoGameInProgress(Exception):
    pass


class Result(IntEnum):
    Tie = 0
    Loss = 1
    Win = 2


RANDOM_PLAYER_WAIT_TIME = 1
rand = random.SystemRandom()


class Player:
    def __init__(self, name, board=None, color=None):
        self.term = Terminal()
        self.name = f'{name} ({self.__class__.__name__})'
        self.board = board
        self.color = color

        self.wins = 0
        self.losses = 0
        self.ties = 0

    def _take_turn(self):
        if self.board is None:
            raise NoGameInProgress('No board has been assigned to this player')

        self.term.move(*Location(19, 0))
        print(f"{self.color}{self.name}{self.term.normal}'s turn")
        cup = self.take_turn()

        if cup is None:
            raise Exception('A cup must be returned by the user')
        return cup

    def take_turn(self):
        raise NotImplementedError('take_turn must be implemented by subclasses')

    def assign_board(self, board):
        self.board = board

    def game_over(self, result):
        if result == Result.Win:
            self.wins += 1
        elif result == Result.Loss:
            self.losses += 1
        elif result == Result.Tie:
            self.ties += 1
        else:
            raise ValueError('Result not recognized. Got {result}')

        self.board = None

    @property
    def games_player(self):
        return self.wins + self.losses + self.ties

    @property
    def is_player1(self):
        return self.board.player1 == self

    @property
    def is_player2(self):
        return self.board.player2 == self

    @property
    def cup_index(self):
        return (
            self.board.player_1_cup_index
            if self.is_player1
            else self.board.player_2_cup_index
        )


class HumanPlayer(Player):
    def take_turn(self):
        cup = input('Enter cup to sow: ')
        return cup


class RandomPlayer(Player):
    def __init__(self, name, board=None, wait_time=RANDOM_PLAYER_WAIT_TIME, **kwargs):
        super().__init__(name, board=board, **kwargs)
        self.wait_time = wait_time

    @property
    def _legal_cups(self):
        return [
            cup
            for cup in itertools.chain(
                self.board.top_row_cups, self.board.bottom_row_cups
            )
            if self.board.cup_seeds(cup) > 0
        ]

    def take_turn(self):
        time.sleep(self.wait_time)

        cup = rand.choice(self._legal_cups)
        print(f'{self.color}{self.name}{self.term.normal} chooses {cup}')
        time.sleep(self.wait_time)
        return cup


class ImprovedRandomPlayer(RandomPlayer):
    def _free_play_moves(self):
        moves = []

        for index in itertools.chain(
            self.board.top_row_indices, self.board.bottom_row_indices
        ):
            seeds = self.board.cup_seeds_by_index(index)

            if seeds == 0:
                continue

            if (index + seeds) % len(self.board.cups) == (
                self.board.player_1_cup_index
                if self.is_player1
                else self.board.player_2_cup_index
            ):
                moves.append({'cup': self.board.index_to_cup[index], 'seeds': seeds})

        moves.sort(key=lambda x: x['seeds'])
        return moves

    def take_turn(self):
        time.sleep(self.wait_time)
        free_play_moves = self._free_play_moves()
        if free_play_moves:
            next_move = free_play_moves[0]['cup']
        else:
            next_move = rand.choice(self._legal_cups)

        print(f'{self.color}{self.name}{self.term.normal} chooses {next_move}')
        time.sleep(self.wait_time)
        return next_move


class DefensivePlayer(ImprovedRandomPlayer):
    def _defensive_move(self):
        moves = []

        for index in itertools.chain(
            self.board.top_row_indices, self.board.bottom_row_indices
        ):
            seeds = self.board.cup_seeds_by_index(index)

            if seeds == 0:
                continue

            if (index + seeds) % len(self.board.cups) == (
                self.board.player_2_cup_index
                if self.is_player1
                else self.board.player_1_cup_index
            ):
                moves.append({'cup': self.board.index_to_cup[index], 'seeds': seeds})

        moves.sort(key=lambda x: x['seeds'], reverse=True)

        if moves:
            opp_free_move_cup = moves[0]['cup']

            legal_moves = self._legal_cups
            index = self._legal_cups.index(opp_free_move_cup)

            if opp_free_move_cup in self.board.top_row_cups:
                move = legal_moves.pop((index - 1) % len(legal_moves))
            else:
                move = legal_moves.pop((index + 1) % len(legal_moves))

            return move
        return None

    def take_turn(self):
        free_play_moves = self._free_play_moves()

        if free_play_moves:
            next_move = free_play_moves[0]['cup']
        else:
            defensive_move = self._defensive_move()

            if defensive_move:
                next_move = defensive_move
            else:
                next_move = rand.choice(self._legal_cups)

        print(f'{self.color}{self.name}{self.term.normal} chooses {next_move}')
        time.sleep(self.wait_time)
        return next_move
