# Python-2048inConsole
A python project implemented 2048 game in console. 

- **`main.py`**: Controls the main game loop, user interaction, and state management.
- **`game_functions.py`**: Contains core game logic, utility functions, and classes

Inside main.py:

- **Main Flow**:
    - The `main()` function is responsible for initializing the game and managing the game state.
    - **State Management**: Different functions handle various game states such as `Init`, `Game`, `Win`, and `Gameover`.
- **State Machine Loop**:
    - The program uses a state-action mapping and loop to keep the game running until the player exits.
- **Curses Library**: Render the game in a terminal interface.

Inside game_functions.py: 
- **GameField Class**: Manages the game field, controls tile movement, score tracking, and win/gameover conditions.
- **GameRenderer Class**: Responsible for rendering the game state on the screen using `curses`.
- **Utility Functions** (`transpose()`, `reverse_rows()`, etc.): Helper functions for matrix operations to manage tile movements.

Structures as a Finite State Machine:
![Image_20241104015408](https://github.com/user-attachments/assets/33f9181b-9937-4255-b761-f6ac18f81cc1)
