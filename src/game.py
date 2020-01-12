from src.board import Board, EmptyCup, InvalidCup
from src.player import RandomPlayer
from src.terminal import Location, Terminal


class Game:
    def __init__(self, side_length=6):
        self.term = Terminal()

        self.term.clear()
        self.term.move(Location(5, 5))

        self.board = Board(side_length)

        seeds = self._get_initial_seeds()
        self.board.initialize_cups(seeds)
        self.board.clear_board()
        self.board.display_cups()

        self.player1 = RandomPlayer('Player1', self.board, wait_time=0.5, color=self.term.bold + self.term.red)
        self.player2 = RandomPlayer('Player2', self.board, wait_time=0.5, color=self.term.bold + self.term.blue)
        self.current_player = self.player1
        self._players = (self.player1, self.player2)

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
                cup = self.current_player.take_turn()
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
        elif self.board.player_1_cup < self.board.player_2_cup:
            print(f'{self.player2.name} Wins!')
        else:
            print('Tie game!')

    def _determine_next_player(self, last_cup):
        if self.current_player == self.player1:
            if last_cup != self.board.player_1_cup_index:
                self.current_player = self.player2
        elif self.current_player == self.player2:
            if last_cup != self.board.player_2_cup_index:
                self.current_player = self.player1


def main():
    game = Game()

    try:
        game.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
