from src.mancala.board import Board, EmptyCup, InvalidCup
from src.mancala.player import Result
from src.mancala.terminal import Location, Terminal


class Game:
    def __init__(
        self,
        *,
        player1,
        player2,
        side_length=6,
        initial_seeds=None,
        player_1_color=None,
        player_2_color=None,
        animation_wait=0.1,
    ):
        self.term = Terminal()

        if player_1_color is None and player1.color is None:
            player1.color = self.term.bold + self.term.red
        else:
            player1.color = player_1_color or player1.color

        if player_2_color is None and player2.color is None:
            player2.color = self.term.bold + self.term.blue
        else:
            player2.color = player_2_color or player2.color

        seed_color = self.term.green
        index_color = self.term.yellow

        self.term.clear()
        self.term.move(Location(5, 5))

        self.board = Board(
            side_length,
            seed_color=seed_color,
            index_color=index_color,
            animation_wait=animation_wait,
        )

        self.player1 = player1
        self.player2 = player2

        self.board.assign_player(self.player1)
        self.board.assign_player(self.player2)

        self.current_player = self.player1
        self._players = (self.player1, self.player2)

        seeds = initial_seeds or self._get_initial_seeds()
        self.board.initialize_cups(seeds)
        self.board.clear_board()
        self.board.display_cups()

    def _get_initial_seeds(self):
        seeds = input('Enter the initial number of seeds per cup: ')
        return seeds

    def clear_screen(self):
        self.term.clear()

    def run(self):
        self.clear_screen()
        while not self.board.done():
            self.board.clear_board()
            self.board.display_cups()

            try:
                cup = self.current_player._take_turn()
                last_cup = self.board.sow(cup, color=self.current_player.color)
            except (EmptyCup, InvalidCup):
                continue

            self._determine_next_player(last_cup)
            self.clear_screen()
        self.board.display_cups()

        print()
        print()
        if self.board.player_1_cup > self.board.player_2_cup:
            print(f'{self.player1.name} Wins!')
            self.board.player1.game_over(Result.Win)
            self.board.player2.game_over(Result.Loss)
        elif self.board.player_1_cup < self.board.player_2_cup:
            print(f'{self.player2.name} Wins!')
            self.board.player1.game_over(Result.Loss)
            self.board.player2.game_over(Result.Win)
        else:
            print('Tie game!')
            self.board.player1.game_over(Result.Tie)
            self.board.player2.game_over(Result.Tie)

    def _determine_next_player(self, last_cup):
        if self.current_player == self.player1:
            if last_cup != self.board.player_1_cup_index:
                self.current_player = self.player2
        elif self.current_player == self.player2:
            if last_cup != self.board.player_2_cup_index:
                self.current_player = self.player1
