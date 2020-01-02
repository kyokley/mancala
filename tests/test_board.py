import pytest

from src.board import Board


class TestIndexDict:
    def test_seven_cups(self):
        side_length = 7
        board = Board(side_length)

        expected = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
            'g': 7,
            'h': 15,
            'i': 14,
            'j': 13,
            'k': 12,
            'l': 11,
            'm': 10,
            'n': 9,
        }
        assert expected == board._index_dict

    def test_six_cups(self):
        side_length = 6
        board = Board(side_length)

        expected = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
            'g': 13,
            'h': 12,
            'i': 11,
            'j': 10,
            'k': 9,
            'l': 8,
        }
        assert expected == board._index_dict


class TestInitializeCups:
    """
    Indexes and their associated letters:

        a   b   c   d   e   f
        1   2   3   4   5   6
    0                            7
        13  12  11  10  9   8
        g   h   i   j   k   l
    """

    @pytest.fixture(autouse=True)
    def setUp(self):
        self.side_length = 6
        self.board = Board(self.side_length)

    def test_initialize_cups_with_four_seeds(self):
        expected = [
            0,  # Player 1's cup
            4,  # a
            4,  # b
            4,  # c
            4,  # d
            4,  # e
            4,  # f
            0,  # Player 2's cup
            4,  # l
            4,  # k
            4,  # j
            4,  # i
            4,  # h
            4,  # g
        ]
        self.board.initialize_cups(4)
        assert expected == self.board.cups

    def test_initialize_cups_with_three_seeds(self):
        expected = [
            0,  # Player 1's cup
            3,  # a
            3,  # b
            3,  # c
            3,  # d
            3,  # e
            3,  # f
            0,  # Player 2's cup
            3,  # l
            3,  # k
            3,  # j
            3,  # i
            3,  # h
            3,  # g
        ]
        self.board.initialize_cups(3)
        assert expected == self.board.cups


class TestSow:
    """
    Indexes and their associated letters:

        a   b   c   d   e   f
        1   2   3   4   5   6
    0                            7
        13  12  11  10  9   8
        g   h   i   j   k   l
    """

    @pytest.fixture(autouse=True)
    def setUp(self):
        self.side_length = 6
        self.board = Board(self.side_length)
        self.board.initialize_cups(4)

    def test_sow_in_top_row(self):
        expected = [
            0,  # Player 1's cup
            0,  # a
            5,  # b
            5,  # c
            5,  # d
            5,  # e
            4,  # f
            0,  # Player 2's cup
            4,  # l
            4,  # k
            4,  # j
            4,  # i
            4,  # h
            4,  # g
        ]
        last_cup = self.board.sow('a')

        assert expected == self.board.cups
        assert last_cup == 5

    def test_sow_in_bottom_row(self):
        expected = [
            0,  # Player 1's cup
            4,  # a
            4,  # b
            4,  # c
            4,  # d
            4,  # e
            4,  # f
            0,  # Player 2's cup
            4,  # l
            0,  # k
            5,  # j
            5,  # i
            5,  # h
            5,  # g
        ]
        last_cup = self.board.sow('k')

        assert expected == self.board.cups
        assert last_cup == 13

    def test_sow_wraps_around_left(self):
        expected = [
            1,  # Player 1's cup
            5,  # a
            5,  # b
            4,  # c
            4,  # d
            4,  # e
            4,  # f
            0,  # Player 2's cup
            4,  # l
            4,  # k
            4,  # j
            4,  # i
            0,  # h
            5,  # g
        ]
        last_cup = self.board.sow('h')

        assert expected == self.board.cups
        assert last_cup == 2

    def test_sow_wraps_around_right(self):
        expected = [
            0,  # Player 1's cup
            4,  # a
            4,  # b
            4,  # c
            4,  # d
            4,  # e
            0,  # f
            1,  # Player 2's cup
            5,  # l
            5,  # k
            5,  # j
            4,  # i
            4,  # h
            4,  # g
        ]
        last_cup = self.board.sow('f')

        assert expected == self.board.cups
        assert last_cup == 10
