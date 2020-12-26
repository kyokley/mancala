from src.game import Game
from src.player import DefensivePlayer, HumanPlayer


def main():
    player1 = DefensivePlayer(
        'Player1',
    )
    player2 = HumanPlayer(
        'Player2',
    )
    game = Game(player1=player1, player2=player2)

    try:
        game.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
