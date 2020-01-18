import pytest
from pytest_factoryboy import register

from src.game import Game
from src.player import ImprovedRandomPlayer
from tests.factories import PlayerFactory


@pytest.fixture
def basic_game_setup():
    def _basic_game_setup(
        test_instance, player1=None, player2=None,
    ):
        test_instance.player1 = player1 or ImprovedRandomPlayer('Player1', wait_time=0)
        test_instance.player2 = player2 or ImprovedRandomPlayer('Player2', wait_time=0)
        test_instance.game = Game(
            player1=test_instance.player1,
            player2=test_instance.player2,
            animation_wait=0,
            initial_seeds=3,
        )
        test_instance.board = test_instance.game.board

    return _basic_game_setup


register(PlayerFactory)
