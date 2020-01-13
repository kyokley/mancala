import sys

from src.game import Game
from src.player import DefensivePlayer, HumanPlayer, ImprovedRandomPlayer, RandomPlayer
from src.terminal import Location, Terminal


class Series:
    def __init__(self, initial_seeds=3, number_of_games=10, animation_wait=0.01):
        self.term = Terminal()

        self.number_of_games = number_of_games
        self.initial_seeds = initial_seeds
        self.animation_wait = animation_wait

        player_1_color = self.term.bold + self.term.red
        player_2_color = self.term.bold + self.term.blue

        self.games = []

        # self.player1 = ImprovedRandomPlayer(
        # 'Alice', wait_time=self.animation_wait, color=player_1_color
        # )
        self.player1 = DefensivePlayer('Alice', color=player_1_color)
        self.player2 = ImprovedRandomPlayer(
            'Bob', wait_time=self.animation_wait, color=player_2_color
        )

    def run_games(self):
        for idx in range(self.number_of_games):
            if idx % 2:
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
    number_of_games = 0

    if len(sys.argv) == 2:
        number_of_games = int(sys.argv[1])
    else:
        number_of_games = int(input('Enter number of games: '))

    if number_of_games <= 0:
        print('Invalid number of games requested.')
        return

    series = Series(number_of_games=number_of_games, animation_wait=0.1,)

    try:
        series.run_games()
        series.final_results()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
