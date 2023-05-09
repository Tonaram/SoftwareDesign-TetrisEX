# run.py

# Import the TetrisGame class from tetris_game
from tetris_game import TetrisGame

# Check if the script is being executed directly, rather than being imported as a module
if __name__ == "__main__":
    # Create an instance of the TetrisGame class
    game = TetrisGame()
    # Start the main menu of the game
    game.main_menu()
