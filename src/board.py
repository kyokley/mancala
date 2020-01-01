from src.utils import generate_sequence


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
        self.side_length = side_length
        self.total_number_of_cups = self.side_length * 2 + 2
        self.cups = [0] * self.total_number_of_cups

        self._index_dict = dict()

    def _letter_to_index(self, letter):
        letter_sequence = generate_sequence(len(self.cups) - 2)
        for i in range(len(self.cups)):
            if i == 0 or i == self.total_number_of_cups / 2:
                continue

            letter = letter_sequence[i]
            self._index_dict[letter] = i
