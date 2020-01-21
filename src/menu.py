from src.terminal import Location, Terminal

INITIAL_MENU_LOCATION = Location(5, 5)


class GetUserInput:
    def __init__(
        self, prompt, choices=None,
    ):
        self.term = Terminal()
        self.prompt = prompt
        self.choices = list(choices) if choices else None

        self._inital_location = INITIAL_MENU_LOCATION

    def get_response(self):
        self.term.clear()
        self.term.move(self._inital_location)

        if self.choices:
            print(self.prompt)
            for idx, choice in enumerate(self.choices):
                print(f'     ({idx + 1})  {str(choice)}')

        done = False
        while not done:
            if self.choices:
                user_resp = input(f'Enter [1-{len(self.choices)}]: ')
            else:
                user_resp = input(self.prompt)

            try:
                val = int(user_resp)

                if self.choices:
                    choice = self.choices[val - 1]
                else:
                    choice = val

                done = True
            except ValueError:
                continue

        return choice
