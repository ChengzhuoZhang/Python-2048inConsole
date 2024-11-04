import curses
from collections import defaultdict
from game_functions import GameField, GameRenderer, get_player_input

def main(stdscr):
    # stdscr: The curses screen window object.

    def init():
        game_field.reset()
        return 'Game'

    def not_game(state):
        # Handle the state when the game is not in progress (win or game over).

        renderer.draw(game_field)
        action = get_player_input(stdscr)
        responses = defaultdict(lambda: state)  # Default is current state, loop in current screen
        responses['Restart'], responses['Exit'] = 'Init', 'Exit'  # Map actions to states
        return responses[action]

    def game():

        # Draw current game board
        renderer.draw(game_field)
        # Get user action
        action = get_player_input(stdscr)

        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):  # Move successful
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    # State-action mapping
    state_actions = {
        'Init': init,
        'Win': lambda: not_game('Win'),
        'Gameover': lambda: not_game('Gameover'),
        'Game': game
    }

    curses.use_default_colors()

    # Set max value to win the game
    game_field = GameField(win=2048)
    renderer = GameRenderer(stdscr)

    state = 'Init'

    # State machine loop
    while state != 'Exit':
        state = state_actions[state]()

curses.wrapper(main)