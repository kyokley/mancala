from src.player import HumanPlayer, RandomPlayer, ImprovedRandomPlayer, DefensivePlayer, PlayerType


class PlayerFactory:
    _player_classes = {}

    @classmethod
    def register(cls, player_type, player_class):
        cls._player_classes[player_type] = player_class

    @classmethod
    def create(cls, player_type, player_name=None):
        if player_type not in cls._player_classes:
            raise KeyError(f'Could not find a Player class of type {player_type}')

        return cls._player_classes[player_type](name=player_name)

    @classmethod
    def all_classes(cls):
        return cls._player_classes.values()


PlayerFactory.register(PlayerType.Human, HumanPlayer)
PlayerFactory.register(PlayerType.Random, RandomPlayer)
PlayerFactory.register(PlayerType.ImprovedRandom, ImprovedRandomPlayer)
PlayerFactory.register(PlayerType.Defensive, DefensivePlayer)
