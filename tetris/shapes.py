# tetris\shapes.py
import random

# SHAPE FORMATS
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class ShapeFactory:
    """
    A factory class for creating random tetromino shapes.
    """
    @staticmethod
    def create_piece(column, row):
        """
        Create a random tetromino piece at the specified column and row.

        Args:
            column (int): The starting column for the piece.
            row (int): The starting row for the piece.

        Returns:
            Piece: The randomly created tetromino piece.
        """
        shape = random.choice(SHAPES)
        return Piece(column, row, shape, SHAPE_COLORS[SHAPES.index(shape)])


class Piece:
    """
    Represents a tetromino piece.
    """
    def __init__(self, x, y, shape, color, rotation = 0):
        """
        Initialize a tetromino piece.

        Args:
            x (int): The starting x-coordinate (column) for the piece.
            y (int): The starting y-coordinate (row) for the piece.
            shape (list): The shape matrix of the tetromino piece.
            color (tuple): The RGB color of the piece.
            rotation (int, optional): The initial rotation of the piece. Defaults to 0.
        """
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.rotation = rotation

    def ghost_piece_position(self, grid, valid_space_func):
        """
        Calculate the position of the ghost piece based on the current piece.

        Args:
            grid (list): The game grid.
            valid_space_func (function): A function that checks if the piece is in a valid space.

        Returns:
            Piece: The ghost piece with the calculated position.
        """
        ghost_piece = self.create_ghost_piece()
        while valid_space_func(ghost_piece, grid):
            ghost_piece.y += 1
        ghost_piece.y -= 1
        return ghost_piece

    def create_ghost_piece(self):
        """
        Create a ghost piece based on the current piece.

        Returns:
            Piece: The ghost piece with the same attributes as the current piece.
        """
        return Piece(self.x, self.y, self.shape, self.color, self.rotation)


class Shapes:
    """
    A class to handle shape generation.
    """
    @staticmethod
    def get_shape():
        """
        Get a random shape using the ShapeFactory.

        Returns:
            Piece: A randomly generated tetromino shape.
        """
        return ShapeFactory.create_piece(5, 0)
