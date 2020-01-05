import pytest

from src.game import Game


class TestDetermineNextPlayer:
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        mocker.patch('src.game.Game._get_initial_seeds', lambda x: 3)
        self.game = Game()
        self.board = self.game.board
        self._player_cups = {
            self.game.player1: self.board.player_1_cup_index,
            self.game.player2: self.board.player_2_cup_index,
        }

    @pytest.mark.parametrize('current_player_index,last_cup', [(0, 5), (1, 5)])
    def test_no_extra_turn(self, current_player_index, last_cup):
        player = self.game._players[current_player_index]
        self.game.current_player = player

        self.game._determine_next_player(last_cup)
        assert self.game.current_player != player

    @pytest.mark.parametrize('current_player_index', [0, 1])
    def test_extra_turn(self, current_player_index):
        player = self.game._players[current_player_index]
        self.game.current_player = player

        last_cup = self._player_cups[player]

        self.game._determine_next_player(last_cup)
        assert self.game.current_player == player
