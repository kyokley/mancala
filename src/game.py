from src.board import Board, EmptyCup, InvalidCup
from src.player import HumanPlayer
from src.terminal import Location, Terminal


class Game:
    def __init__(self, side_length=6):
        self.term = Terminal()

        self.term.clear()
        self.term.move(Location(5, 5))
        seeds = input('Enter the initial number of seeds per cup: ')

        self.board = Board(side_length)
        self.board.initialize_cups(seeds)
        self.board.clear_screen()
        self.board.display_cups()

        self.player1 = HumanPlayer('Player1', self.board)
        self.player2 = HumanPlayer('Player2', self.board)
        self.current_player = self.player1

    def run(self):
        while not self.board.done():
            self.board.clear_screen()
            self.board.display_cups()

            try:
                last_cup = self.current_player.take_turn()
            except (EmptyCup, InvalidCup):
                continue

            if self.current_player == self.player1:
                if last_cup != self.board.player_1_cup_index:
                    self.current_player = self.player2
            elif self.current_player == self.player2:
                if last_cup != self.board.player_2_cup_index:
                    self.current_player = self.player1
        self.board.display_cups()


if __name__ == '__main__':
    game = Game()

    try:
        game.run()
    except KeyboardInterrupt:
        pass
