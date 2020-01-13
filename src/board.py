import itertools
import time
from collections import namedtuple

from src.terminal import Location, Terminal
from src.utils import generate_sequence

Indicator = namedtuple('Indicator', 'location symbol')


class InvalidCup(Exception):
    pass


class EmptyCup(Exception):
    pass


class TooManyPlayers(Exception):
    pass


class NotEnoughPlayers(Exception):
    pass


class Board:
    def __init__(
        self, side_length, animation_wait=1, seed_color=None, index_color=None,
    ):
        """
        Indexes and their associated letters:

            a   b   c   d   e   f   g
            1   2   3   4   5   6   7
        0                               8
            15  14  13  12  11  10  9
            h   i   j   k   l   m   n
        """
        self.term = Terminal()
        self.side_length = side_length
        self.total_number_of_cups = self.side_length * 2 + 2
        self.cups = [0] * self.total_number_of_cups

        self._SEED_COLOR = seed_color
        self._INDEX_COLOR = index_color

        self._ANIMATION_WAIT = animation_wait

        self._INITIAL_LOCATION = Location(10, 10)
        self._HORIZONTAL_SPACER = Location(0, 4)

        self._TOP_ROW_INDICATOR_LOCATION = (
            self._INITIAL_LOCATION + self._HORIZONTAL_SPACER
        )
        self._TOP_ROW_INDICES_LOCATION = self._TOP_ROW_INDICATOR_LOCATION + Location(
            1, 0
        )
        self._TOP_ROW_LOCATION = self._TOP_ROW_INDICES_LOCATION + Location(1, 0)

        self._PLAYER_1_LOCATION = Location(
            self._TOP_ROW_LOCATION.row + 1, self._INITIAL_LOCATION.column
        )
        self._PLAYER_2_LOCATION = self._PLAYER_1_LOCATION + Location(
            0, self._HORIZONTAL_SPACER.column * (self.side_length + 1)
        )

        self._BOTTOM_ROW_LOCATION = (
            self._PLAYER_1_LOCATION + self._HORIZONTAL_SPACER + Location(1, 0)
        )
        self._BOTTOM_ROW_INDICES_LOCATION = self._BOTTOM_ROW_LOCATION + Location(1, 0)
        self._BOTTOM_ROW_INDICATOR_LOCATION = (
            self._BOTTOM_ROW_INDICES_LOCATION + Location(1, 0)
        )

        self._PLAYER_1_INDICATOR = self._PLAYER_1_LOCATION - self._HORIZONTAL_SPACER
        self._PLAYER_2_INDICATOR = self._PLAYER_2_LOCATION + self._HORIZONTAL_SPACER

        self._build_index_dicts()

        self.players = []

    @property
    def ready_to_play(self):
        return len(self.players) == 2

    def assign_player(self, player):
        if len(self.players) == 2:
            raise TooManyPlayers('Cannot add any more players to this board')

        if not self.players:
            self.player1 = player
            self.player1.assign_board(self)
        elif len(self.players) == 1:
            self.player2 = player
            self.player2.assign_board(self)
        self.players.append(player)

    @property
    def max_row(self):
        return self._BOTTOM_ROW_INDICATOR_LOCATION.row

    @property
    def max_column(self):
        return self._PLAYER_2_INDICATOR.column

    @property
    def min_row(self):
        return self._INITIAL_LOCATION.row

    @property
    def min_column(self):
        return self._INITIAL_LOCATION.column

    @property
    def top_row(self):
        return self.cups[1 : self._midpoint]

    @property
    def top_row_indices(self):
        return [i for i in range(1, self._midpoint)]

    @property
    def top_row_cups(self):
        return sorted([self.index_to_cup[idx] for idx in self.top_row_indices])

    @property
    def bottom_row(self):
        return self.cups[self._midpoint + 1 :]

    @property
    def bottom_row_indices(self):
        return [i for i in range(self._midpoint + 1, len(self.cups))]

    @property
    def bottom_row_cups(self):
        return sorted([self.index_to_cup[idx] for idx in self.bottom_row_indices])

    @property
    def player_1_cup_index(self):
        return 0

    @property
    def player_2_cup_index(self):
        return self._midpoint

    @property
    def player_1_cup(self):
        return self.cups[self.player_1_cup_index]

    @property
    def player_2_cup(self):
        return self.cups[self.player_2_cup_index]

    @property
    def _midpoint(self):
        return len(self.cups) // 2

    def cup_seeds(self, cup):
        return self.cups[self.cup_to_index[cup]]

    def cup_seeds_by_index(self, index):
        return self.cups[index]

    def _build_index_dicts(self):
        self.cup_to_index = dict()
        self._index_to_cup_indicator = dict()

        letter_sequence = generate_sequence(len(self.cups) - 2)

        for i in range(1, self._midpoint):
            letter = letter_sequence.pop(0)
            self.cup_to_index[letter] = i

        for i in range(len(self.cups) - 1, self._midpoint, -1):
            letter = letter_sequence.pop(0)
            self.cup_to_index[letter] = i

        self.index_to_cup = {v: k for k, v in self.cup_to_index.items()}

        for i in range(len(self.cups)):
            if i == 0:  # Player1's cup
                self._index_to_cup_indicator[i] = Indicator(
                    self._PLAYER_1_INDICATOR, '>'
                )
            elif i < self._midpoint:  # Top row
                self._index_to_cup_indicator[i] = Indicator(
                    (i - 1) * self._HORIZONTAL_SPACER
                    + self._TOP_ROW_INDICATOR_LOCATION,
                    'v',
                )
            elif i == self._midpoint:  # Player2's cup
                self._index_to_cup_indicator[i] = Indicator(
                    self._PLAYER_2_INDICATOR, '<'
                )
            else:  # Bottom row cups
                self._index_to_cup_indicator[i] = Indicator(
                    (len(self.cups) - i - 1) * self._HORIZONTAL_SPACER
                    + self._BOTTOM_ROW_INDICATOR_LOCATION,
                    '^',
                )

    def clear_indicators(self):
        for idx, indicator in self._index_to_cup_indicator.items():
            self.term.move(indicator.location)
            self.term.display(' ')

    def done(self):
        return all(val == 0 for val in itertools.chain(self.top_row, self.bottom_row))

    def initialize_cups(self, seeds):
        for i in range(len(self.cups)):
            if i == 0 or i == self._midpoint:
                continue

            self.cups[i] = int(seeds)

    def sow(self, cup, color=None):
        if cup not in self.cup_to_index:
            raise InvalidCup(f'Invalid cup. Got {cup}.')

        self.clear_indicators()
        index = self.cup_to_index[cup]
        seeds = self.cups[index]

        if seeds == 0:
            raise EmptyCup(f"Cup '{cup}' is empty.")

        self._draw_indicator(index, color=color)
        print()
        self.cups[index] = 0
        self.display_cups()
        time.sleep(self._ANIMATION_WAIT)

        while seeds:
            index += 1
            self.cups[index % len(self.cups)] += 1
            seeds -= 1
            self.clear_board()
            self.display_cups()
            self._draw_indicator(index % len(self.cups), color=color)

            print()
            time.sleep(self._ANIMATION_WAIT)

        return index % len(self.cups)

    def _draw_indicator(self, index, color=None):
        indicator = self._index_to_cup_indicator[index]
        self.term.move(indicator.location)
        self.term.display(indicator.symbol, color=color)

    def clear_board(self):
        for row in range(self.min_row, self.max_row):
            # Iterate to max_columns + 1 in case player2's cup has 10 or more seeds
            for column in range(self.min_column, self.max_column + 1):
                self.term.move(row, column)
                self.term.display(' ')

        self.clear_indicators()

    def display_cups(self):
        self.term.move(self._PLAYER_1_LOCATION)
        self.term.display(self.player_1_cup, color=self.player1.color)

        self.term.move(self._PLAYER_2_LOCATION)
        self.term.display(self.player_2_cup, color=self.player2.color)

        # Draw the top row
        # Draw cup indices
        current_location = self._TOP_ROW_INDICES_LOCATION

        for key in self.top_row_cups:
            self.term.move(current_location)
            self.term.display(key, color=self._INDEX_COLOR)
            current_location += self._HORIZONTAL_SPACER

        current_location = self._TOP_ROW_LOCATION

        for val in self.top_row:
            self.term.move(current_location)
            self.term.display(val, color=self._SEED_COLOR)
            current_location += self._HORIZONTAL_SPACER

        # Draw player cups
        # Draw bottom row
        current_location = self._BOTTOM_ROW_LOCATION

        for val in reversed(self.bottom_row):
            self.term.move(current_location)
            self.term.display(val, color=self._SEED_COLOR)
            current_location += self._HORIZONTAL_SPACER

        current_location = self._BOTTOM_ROW_INDICES_LOCATION

        for key in self.bottom_row_cups:
            self.term.move(current_location)
            self.term.display(key, color=self._INDEX_COLOR)
            current_location += self._HORIZONTAL_SPACER
