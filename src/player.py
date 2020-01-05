from src.terminal import Location, Terminal


class Player:
    def __init__(self,
                 name):
        self.term = Terminal()
        self.name = name

    def take_turn(self):
        pass


class HumanPlayer(Player):
    def take_turn(self):
        self.term.move(*Location(19, 0))
        print(f"{self.name}'s turn")
        cup = input('Enter cup to sow: ')
        self.board.sow(cup)
