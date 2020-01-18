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
