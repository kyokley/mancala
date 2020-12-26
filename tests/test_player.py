import pytest

from src.player import DefensivePlayer


class TestDefensiveMove:
    @pytest.fixture(autouse=True)
    def setUp(self, basic_game_setup):
        self.player = DefensivePlayer('Player1')
        basic_game_setup(self, player1=self.player)

        self.board.initialize_cups(0)

    def test_move1(self):
        """
            a   b   c   d   e   f
            0   3   3   0   1   1
        0                           0
            0   0   0   0   0   0
            g   h   i   j   k   l
        """
        self.board.cups[1] = 0
        self.board.cups[2] = 3
        self.board.cups[3] = 3
        self.board.cups[4] = 0
        self.board.cups[5] = 1
        self.board.cups[6] = 1

        move = self.player._defensive_move()
        assert move == 'e'

    def test_move2(self):
        """
            a   b   c   d   e   f
            0   2   4   3   1   1
        0                           0
            0   0   0   0   0   0
            g   h   i   j   k   l
        """
        self.board.cups[1] = 0
        self.board.cups[2] = 2
        self.board.cups[3] = 4
        self.board.cups[4] = 3
        self.board.cups[5] = 1
        self.board.cups[6] = 1

        move = self.player._defensive_move()
        assert move == 'b'


class TestScoreMoves:
    @pytest.fixture(autouse=True)
    def setUp(self, basic_game_setup):
        self.player = DefensivePlayer('Player1')
        basic_game_setup(self, player1=self.player)

        self.board.initialize_cups(0)

    def test_move1(self):
        """
            a   b   c   d   e   f
            1   2   3   0   1   0
        0                           0
            7   1   2   3   1   7
            g   h   i   j   k   l
        """
        # Top Rows
        self.board.cups[1] = 1
        self.board.cups[2] = 2
        self.board.cups[3] = 3
        self.board.cups[4] = 0
        self.board.cups[5] = 1
        self.board.cups[6] = 0

        # Bottom Rows
        self.board.cups[8] = 7
        self.board.cups[9] = 1
        self.board.cups[10] = 3
        self.board.cups[11] = 2
        self.board.cups[12] = 1
        self.board.cups[13] = 7

        scored_moves = self.player._score_moves()
        expected = [
            {'cup': 'a', 'score': 0},
            {'cup': 'b', 'score': -1},
            {'cup': 'c', 'score': -1},
            {'cup': 'e', 'score': 0},
            {'cup': 'g', 'score': 4.0},
            {'cup': 'h', 'score': 5.0},
            {'cup': 'i', 'score': 6.0},
            {'cup': 'j', 'score': 7.0},
            {'cup': 'k', 'score': 7.0},
            {'cup': 'l', 'score': 8.0},
        ]
        assert scored_moves == expected
