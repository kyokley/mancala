from src.board import Board


class Game:
    def __init__(self, side_length=6):
        self.board = Board(side_length)
        self.board._clear_screen()
        self.board._display_cups()


if __name__ == '__main__':
    Game()
