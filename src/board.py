from src.terminal import Location, Terminal
from src.utils import generate_sequence


class InvalidCup(Exception):
    pass


class EmptyCup(Exception):
    pass


class Board:
    def __init__(self, side_length):
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

        self._INITIAL_LOCATION = Location(10, 10)
        self._HORIZONTAL_SPACER = Location(0, 4)

        self._TOP_ROW_INDICES_LOCATION = (
            self._INITIAL_LOCATION + self._HORIZONTAL_SPACER
        )
        self._TOP_ROW_LOCATION = self._TOP_ROW_INDICES_LOCATION + Location(1, 0)

        self._PLAYER_1_LOCATION = self._INITIAL_LOCATION + Location(2, 0)
        self._PLAYER_2_LOCATION = self._PLAYER_1_LOCATION + Location(
            0, self._HORIZONTAL_SPACER.column * (self.side_length + 1)
        )

        self._BOTTOM_ROW_LOCATION = (
            self._PLAYER_1_LOCATION + self._HORIZONTAL_SPACER + Location(1, 0)
        )
        self._BOTTOM_ROW_INDICES_LOCATION = self._BOTTOM_ROW_LOCATION + Location(1, 0)

        self._build_index_dicts()

    @property
    def top_row(self):
        return self.cups[1 : self._midpoint]

    @property
    def top_row_indices(self):
        return [i for i in range(1, self._midpoint)]

    @property
    def top_row_cups(self):
        return sorted([self._index_to_cup[idx] for idx in self.top_row_indices])

    @property
    def bottom_row(self):
        return self.cups[self._midpoint + 1 :]

    @property
    def bottom_row_indices(self):
        return [i for i in range(self._midpoint + 1, len(self.cups))]

    @property
    def bottom_row_cups(self):
        return sorted([self._index_to_cup[idx] for idx in self.bottom_row_indices])

    @property
    def player_1_cup(self):
        return self.cups[0]

    @property
    def player_2_cup(self):
        return self.cups[self._midpoint]

    @property
    def _midpoint(self):
        return len(self.cups) // 2

    def _build_index_dicts(self):
        self._cup_to_index = dict()
        letter_sequence = generate_sequence(len(self.cups) - 2)

        for i in range(1, self._midpoint):
            letter = letter_sequence.pop(0)
            self._cup_to_index[letter] = i

        for i in range(len(self.cups) - 1, self._midpoint, -1):
            letter = letter_sequence.pop(0)
            self._cup_to_index[letter] = i

        self._index_to_cup = {v: k for k, v in self._cup_to_index.items()}

    def initialize_cups(self, seeds):
        for i in range(len(self.cups)):
            if i == 0 or i == self._midpoint:
                continue

            self.cups[i] = seeds

    def sow(self, cup):
        if cup not in self._cup_to_index:
            raise InvalidCup(f'Invalid cup. Got {cup}.')

        index = self._cup_to_index[cup]
        seeds = self.cups[index]

        if seeds == 0:
            raise EmptyCup(f"Cup '{cup}' is empty.")

        self.cups[index] = 0
        while seeds:
            index += 1
            self.cups[index % len(self.cups)] += 1
            seeds -= 1

        return index % len(self.cups)

    def _clear_screen(self):
        self.term.clear()

    def _display_cups(self):
        self.term.move(*self._PLAYER_1_LOCATION)
        self.term.display(self.player_1_cup)

        self.term.move(*self._PLAYER_2_LOCATION)
        self.term.display(self.player_2_cup)

        # Draw the top row
        # Draw cup indices
        current_location = self._TOP_ROW_INDICES_LOCATION

        for key in self.top_row_cups:
            self.term.move(*current_location)
            self.term.display(key)
            current_location += self._HORIZONTAL_SPACER

        current_location = self._TOP_ROW_LOCATION

        for val in self.top_row:
            self.term.move(*current_location)
            self.term.display(val)
            current_location += self._HORIZONTAL_SPACER

        # Draw player cups
        # Draw bottom row
        current_location = self._BOTTOM_ROW_LOCATION

        for val in reversed(self.bottom_row):
            self.term.move(*current_location)
            self.term.display(val)
            current_location += self._HORIZONTAL_SPACER

        current_location = self._BOTTOM_ROW_INDICES_LOCATION

        for key in self.bottom_row_cups:
            self.term.move(*current_location)
            self.term.display(key)
            current_location += self._HORIZONTAL_SPACER
