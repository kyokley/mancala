from src.utils import generate_sequence
from blessings import Terminal


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

        self._build_index_dict()

    @property
    def _midpoint(self):
        return len(self.cups) // 2

    def _build_index_dict(self):
        self._index_dict = dict()
        letter_sequence = generate_sequence(len(self.cups) - 2)

        for i in range(1, self._midpoint):
            letter = letter_sequence.pop(0)
            self._index_dict[letter] = i

        for i in range(len(self.cups) - 1, self._midpoint, -1):
            letter = letter_sequence.pop(0)
            self._index_dict[letter] = i

    def initialize_cups(self, seeds):
        for i in range(len(self.cups)):
            if i == 0 or i == self._midpoint:
                continue

            self.cups[i] = seeds

    def sow(self, cup):
        if cup not in self._index_dict:
            raise InvalidCup(f'Invalid cup. Got {cup}.')

        index = self._index_dict[cup]
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
        print(self.term.clear())

    def _display_cups(self):
        # Draw the top row
        # Draw cup indices
        print(self.term.move(10, 10), end='')
        for key in self._index_dict:
            print(key, end='')
            print(self.term.move_right, end='')

        # Draw player cups
        # Draw bottom row
        pass
