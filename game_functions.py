from random import randrange, choice

letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
actions_dict = dict(zip(letter_codes, actions * 2))

def get_player_input(keyboard):
    # Get the user's action from the keyboard input.

    char = ''
    while char not in actions_dict:
        # Return the ASCII code of the pressed key
        try:
            char = keyboard.getch()
        except ValueError:
            continue  # Handle non-character inputs

    return actions_dict[char]

def transpose(field):
    # Transpose the game field (swap rows and columns).
    return [list(row) for row in zip(*field)]

def reverse_rows(field):
    # Reverse each row of the game field.
    return [row[::-1] for row in field]

class GameField:
    def __init__(self, height=4, width=4, win=2048):

        self.height = height
        self.width = width
        self.win_value = win
        self.reset()

    def reset(self):
        """
        Reset the game field to the initial state.
        """
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.add_new_tile()
        self.add_new_tile()

    def move(self, direction):
        # Move tiles in the given direction and spawn a new tile if the move is successful.

        def move_row_left(row):
            # Move a single row to the left, combining tiles where possible.

            def tighten(row):  # Squeeze non-zero elements together
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row

            return tighten(merge(tighten(row)))

        # Define the moves for each direction
        moves = {
            'Left': lambda field: [move_row_left(row) for row in field],
            'Right': lambda field: reverse_rows(moves['Left'](reverse_rows(field))),
            'Up': lambda field: transpose(moves['Left'](transpose(field))),
            'Down': lambda field: transpose(moves['Right'](transpose(field))),
        }

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.add_new_tile()
                return True
            else:
                return False

    def is_win(self):

        return any(any(i >= self.win_value for i in row) for row in self.field)

    def is_gameover(self):

        return not any(self.move_is_possible(move) for move in actions)

    def add_new_tile(self):

        new_element = 2
        (i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def move_is_possible(self, direction):
        def row_is_left_movable(row):
            def change(i):  # True if there'll be change in i-th tile
                if row[i] == 0 and row[i + 1] != 0:  # Move
                    return True
                if row[i] != 0 and row[i + 1] == row[i]:  # Merge
                    return True
                return False

            return any(change(i) for i in range(len(row) - 1))

        # Define checks for each direction
        check = {
            'Left': lambda field: any(row_is_left_movable(row) for row in field),
            'Right': lambda field: check['Left'](reverse_rows(field)),
            'Up': lambda field: check['Left'](transpose(field)),
            'Down': lambda field: check['Right'](transpose(field)),
        }

        if direction in check:
            return check[direction](self.field)
        else:
            return False

class GameRenderer:

    def __init__(self, screen):
        self.screen = screen

    def draw(self, game_field):
        # Draw the game field on the screen.

        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart (Q)Exit'
        gameover_string = '           GAME OVER'
        win_string = '          YOU WIN!'

        def cast(string):
            # Print a string to the screen.

            self.screen.addstr(string + '\n')

        def draw_hor_separator():
            # Draw a horizontal separator line.

            line = '+' + ('+------' * game_field.width + '+')[1:]
            cast(line)

        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        # Clear the screen and draw the game field
        self.screen.clear()
        for row in game_field.field:
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()
        if game_field.is_win():
            cast(win_string)
        elif game_field.is_gameover():
            cast(gameover_string)
        else:
            cast(help_string1)
        cast(help_string2)