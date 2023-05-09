# tetris\constants.py

# Constants for the game window dimensions
S_WIDTH = 800  # Screen width
S_HEIGHT = 750  # Screen height
PLAY_WIDTH = 300  # Play area width
PLAY_HEIGHT = 600  # Play area height
BLOCK_SIZE = 30  # Size of each tetromino block

# Coordinates for the top-left corner of the play area
TOP_LEFT_X = (S_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = S_HEIGHT - PLAY_HEIGHT - 50

# Colors used in the game
BG_COLOR = (0, 0, 0)  # Background color
WHITE = (255, 255, 255)  # White color
GRID_COLOR = (112, 112, 112)  # Grid line color
BORDER_COLOR = (255, 0, 0)  # Border color of the play area
GHOST_PIECE_COLOR = (224, 224, 244)  # Ghost piece color

# Positions for the "next shape", "hold shape", and "score" displays
NEXT_SHAPE_POSITION = (TOP_LEFT_X + PLAY_WIDTH + 40, TOP_LEFT_Y + PLAY_HEIGHT // 2 - 100)  # Next shape display position
HOLD_SHAPE_POSITION = (TOP_LEFT_X - PLAY_WIDTH // 2 - 40, TOP_LEFT_Y + PLAY_HEIGHT // 2 - 100)  # Hold shape display position
SCORE_POSITION = (TOP_LEFT_X + PLAY_WIDTH + 60, TOP_LEFT_Y + PLAY_HEIGHT // 2 - 300)  # Score display position
