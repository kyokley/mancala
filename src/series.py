import sys

from src.game import Game
from src.player import PlayerType
from src.terminal import Terminal, Location
from src.factory import PlayerFactory
from src.menu import GetUserInput


class Series:
    def __init__(self,
                 initial_seeds=3,
                 number_of_games=10,
                 animation_wait=0.001,
                 player1=None,
                 player2=None,
                 ):
        self.term = Terminal()

        if number_of_games is None:
            number_of_games = GetUserInput('Enter number of games: ').get_response()

        self.number_of_games = number_of_games
        self.initial_seeds = initial_seeds
        self.animation_wait = animation_wait

        player_1_color = self.term.bold + self.term.red
        player_2_color = self.term.bold + self.term.blue

        if not player1:
            player_class = GetUserInput('Enter player type for Player 1:',
                                        PlayerFactory.all_classes()).get_response()
            self.player1 = player_class('Player 1',
                                        color=player_1_color,
                                        wait_time=animation_wait)
        else:
            self.player1 = player1

        if not player2:
            player_class = GetUserInput('Enter player type for Player 2:',
                                        PlayerFactory.all_classes()).get_response()
            self.player2 = player_class('Player 2',
                                        color=player_2_color,
                                        wait_time=animation_wait)
        else:
            self.player2 = player2

    def run_games(self):
        for idx in range(self.number_of_games):
            if idx % 2 == 0:
                game = Game(
                    player1=self.player1,
                    player2=self.player2,
                    initial_seeds=self.initial_seeds,
                    animation_wait=self.animation_wait,
                )
            else:
                game = Game(
                    player1=self.player2,
                    player2=self.player1,
                    initial_seeds=self.initial_seeds,
                    animation_wait=self.animation_wait,
                )

            game.run()

    def final_results(self):
        print()
        print(f'Player 1 ({self.player1.name}):')
        print(f'    Wins: {self.player1.wins}')
        print(f'    Losses: {self.player1.losses}')
        print(f'    Ties: {self.player1.ties}')
        print()
        print(f'Player 2 ({self.player2.name}):')
        print(f'    Wins: {self.player2.wins}')
        print(f'    Losses: {self.player2.losses}')
        print(f'    Ties: {self.player2.ties}')


def main():
    number_of_games = None

    if len(sys.argv) == 2:
        number_of_games = int(sys.argv[1])

    series = Series(number_of_games=number_of_games, animation_wait=0.25,)

    try:
        series.run_games()
        series.final_results()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
