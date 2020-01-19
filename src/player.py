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


RANDOM_PLAYER_WAIT_TIME = 0.5
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
        print(f"{self.color or ''}{self.name}{self.term.normal}'s turn")
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
        opp_free_moves = []

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
                opp_free_moves.append(
                    {'cup': self.board.index_to_cup[index], 'seeds': seeds}
                )

        if opp_free_moves:
            opp_free_moves.sort(key=lambda x: x['seeds'], reverse=True)

            for opp_free_move in opp_free_moves:
                opp_free_move_cup = opp_free_move['cup']

                for check_cup in self._legal_moves_in_reverse(
                    starting_with=opp_free_move_cup
                ):
                    check_cup_seeds = self.board.cup_seeds(check_cup)

                    if check_cup_seeds >= self._distance(check_cup, opp_free_move_cup):
                        return check_cup
        return None

    def _distance(self, first_cup, second_cup):
        first_index = self.board.cup_to_index[first_cup]
        second_index = self.board.cup_to_index[second_cup]

        number_of_cups = len(self.board.cups)
        return (second_index - first_index) % number_of_cups

    def _legal_moves_in_reverse(self, starting_with=None):
        moves = []

        if not starting_with:
            starting_with = self._legal_cups[0]
        starting_index = self.board.cup_to_index[starting_with]
        number_of_playable_cups = len(self.board.top_row_cups) * 2

        for idx in range(number_of_playable_cups):
            test_index = (starting_index - (idx + 1)) % number_of_playable_cups

            if test_index in (
                self.board.player_1_cup_index,
                self.board.player_2_cup_index,
            ):
                continue

            ref_cup = self.board.index_to_cup[test_index]
            seeds = self.board.cup_seeds(ref_cup)

            if seeds > 0:
                moves.append(ref_cup)

        return moves

    @property
    def _my_cup_index(self):
        return (
            self.board.player_1_cup_index
            if self.is_player1
            else self.board.player_2_cup_index
        )

    @property
    def _opp_cup_index(self):
        return (
            self.board.player_1_cup_index
            if self.is_player2
            else self.board.player_2_cup_index
        )

    def _score_moves(self):
        legal_cups = self._legal_cups

        possible_moves = []

        for legal_cup in legal_cups:
            fake_board_cups = self._fake_sow(legal_cup)
            board_score = 0

            for cup_index in range(len(fake_board_cups)):
                if self._is_player_cup(cup_index):
                    continue

                cup = self.board.index_to_cup[cup_index]
                if self._will_finish_in_my_cup(cup, fake_board_cups=fake_board_cups):
                    board_score += 1

                if self._will_finish_in_opp_cup(cup, fake_board_cups=fake_board_cups):
                    board_score -= 1

            possible_moves.append({'cup': legal_cup, 'score': board_score})

        return possible_moves

    def _is_player_cup(self, cup_index):
        return cup_index in (
            self.board.player_1_cup_index,
            self.board.player_2_cup_index,
        )

    def _fake_sow(self, cup):
        board_cups = self.board.cups.copy()

        index = self.board.cup_to_index[cup]
        seeds = self.board.cup_seeds(cup)

        if seeds == 0:
            return board_cups

        board_cups[index] = 0
        while seeds:
            index += 1
            board_cups[index % len(board_cups)] += 1
            seeds -= 1
        return board_cups

    def _will_finish_in_my_cup(self, cup, fake_board_cups=None):
        board_cups = fake_board_cups or self.board.cups

        cup_index = self.board.cup_to_index[cup]

        if self._is_player_cup(cup_index):
            return False

        seeds = board_cups[cup_index]

        if seeds == 0:
            return False

        if (cup_index + seeds) % len(board_cups) == self._my_cup_index:
            return True

        return False

    def _will_finish_in_opp_cup(self, cup, fake_board_cups=None):
        board_cups = fake_board_cups or self.board.cups

        cup_index = self.board.cup_to_index[cup]

        if self._is_player_cup(cup_index):
            return False

        seeds = board_cups[cup_index]

        if seeds == 0:
            return False

        if (cup_index + seeds) % len(board_cups) == self._opp_cup_index:
            return True

        return False

    def take_turn(self):
        free_play_moves = self._free_play_moves()

        if free_play_moves:
            next_move = free_play_moves[0]['cup']
        else:
            defensive_move = self._defensive_move()

            if defensive_move:
                next_move = defensive_move
            else:
                possible_moves = self._score_moves()
                possible_moves.sort(key=lambda x: x['score'], reverse=True)
                max_score = possible_moves[0]['score']

                next_move = rand.choice(
                    [
                        move['cup']
                        for move in possible_moves
                        if move['score'] == max_score
                    ]
                )

        print(f'{self.color}{self.name}{self.term.normal} chooses {next_move}')
        time.sleep(self.wait_time)
        return next_move
