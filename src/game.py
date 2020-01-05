from src.board import Board
from src.terminal import Location, Terminal


class Game:
    def __init__(self, side_length=6):
        self.term = Terminal()

        self.board = Board(side_length)
        self.board.initialize_cups(3)
        self.board._clear_screen()
        self.board._display_cups()

    def prompt(self):
        self.term.move(*Location(20, 0))
        cup = input('Enter cup to sow: ')
        self.board.sow(cup)

    def run(self):
        while True:
            self.board._clear_screen()
            self.board._display_cups()
            self.prompt()


if __name__ == '__main__':
    game = Game()

    try:
        game.run()
    except KeyboardInterrupt:
        pass
