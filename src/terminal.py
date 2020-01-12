from blessings import Terminal as BlessingsTerm


class Location:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __repr__(self):
        return f'<Location ({self.row}, {self.column})>'

    def __eq__(self, other):
        return (other.row, other.column) == (self.row, self.column)

    def __add__(self, other):
        new_x = self.row + other.row
        new_y = self.column + other.column

        return self.__class__(new_x, new_y)

    def __sub__(self, other):
        new_x = self.row - other.row
        new_y = self.column - other.column

        return self.__class__(new_x, new_y)

    def __rmul__(self, other):
        if isinstance(other, int):
            new_x = other * self.row
            new_y = other * self.column
        else:
            raise ValueError('Multiplication not supported for {type(other)}({other}).')

        return self.__class__(new_x, new_y)

    def __getitem__(self, index):
        return (self.row, self.column)[index]


class Terminal:
    def __init__(self):
        self._term = BlessingsTerm()

    def __getattribute__(self, name):
        if name in (
            'black',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
            'bold',
            'reverse',
            'underline',
            'no_underline',
            'blink',
            'normal'
        ):
            return getattr(self._term, name)
        else:
            return super().__getattribute__(name)

    def display(self, val, color=None):
        if color:
            print(color, end='')

        print(val, end='')

        if color:
            print(self._term.normal, end='')

    def clear(self):
        self.display(self._term.clear())

    def move(self, row_or_location, column=None):
        if isinstance(row_or_location, Location):
            if column is not None:
                raise ValueError('column cannot be provided with a Location')

            self.display(self._term.move(*row_or_location))
        elif column is None:
            raise ValueError('column must be provided when used without a Location')
        else:
            self.display(self._term.move(row_or_location, column))

    def move_right(self):
        self.display(self._term.move_right)

    def move_left(self):
        self.display(self._term.move_left)

    def move_up(self):
        self.display(self._term.move_up)

    def move_down(self):
        self.display(self._term.move_down)
