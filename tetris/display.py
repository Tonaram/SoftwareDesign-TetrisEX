# tetris\display.py
import pygame
import os

from .constants import *

class Text:
    def __init__(self, text, size, color, font_name='forte'):
        self.font = pygame.font.SysFont(font_name, size)
        self.label = self.font.render(text, 1, color)

    def draw(self, surface, position):
        surface.blit(self.label, position)

class TetrisDisplay:
    def __init__(self, surface):
        self.surface = surface

    def draw_text_middle(self, text, size, color):
        label = Text(text, size, color)
        position = (TOP_LEFT_X + PLAY_WIDTH/2 - (label.label.get_width() / 2),
                    TOP_LEFT_Y + PLAY_HEIGHT/2 - label.label.get_height()/2)
        label.draw(self.surface, position)

    def draw_grid(self, row, col, grid):
        sx = TOP_LEFT_X
        sy = TOP_LEFT_Y
        for i in range(row):
            pygame.draw.line(self.surface, GRID_COLOR, (sx, sy + i * BLOCK_SIZE),
                             (sx + PLAY_WIDTH, sy + i * BLOCK_SIZE))  # horizontal lines
            for j in range(col):
                pygame.draw.line(self.surface, GRID_COLOR, (sx + j * BLOCK_SIZE, sy),
                                 (sx + j * BLOCK_SIZE, sy + PLAY_HEIGHT))  # vertical lines
                if grid[i][j] == (0, 0, 0):  # Draw shape lines only for empty cells
                    pygame.draw.rect(self.surface, GRID_COLOR, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_window(self, ghost_piece, grid, convert_shape_format_func):
        self.surface.fill(BG_COLOR)

        title = Text('TETRIS', 50, WHITE)
        title.draw(self.surface, (TOP_LEFT_X + PLAY_WIDTH / 2 - (title.label.get_width() / 2), BLOCK_SIZE))

        self.draw_pieces(grid, ghost_piece, convert_shape_format_func)
        self.draw_grid(20, 10, grid)
        pygame.draw.rect(self.surface, BORDER_COLOR, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)

    def draw_pieces(self, grid, ghost_piece, convert_shape_format_func):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(self.surface, grid[i][j], (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        ghost_piece_positions = convert_shape_format_func(ghost_piece)
        for i in range(len(ghost_piece_positions)):
            x, y = ghost_piece_positions[i]
            if y > -1:
                pygame.draw.rect(self.surface, GHOST_PIECE_COLOR, (TOP_LEFT_X + x * BLOCK_SIZE + 1, TOP_LEFT_Y + y * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2), 1)

    def draw_next_shape(self, shape):
        label = Text('Next Shape', 30, WHITE)
        label.draw(self.surface, (NEXT_SHAPE_POSITION[0] + 10, NEXT_SHAPE_POSITION[1] - 30))

        self.draw_shape(shape, NEXT_SHAPE_POSITION)

    def draw_hold_shape(self, shape):
        label = Text('Hold', 30, WHITE)
        label.draw(self.surface, (HOLD_SHAPE_POSITION[0] + 10, HOLD_SHAPE_POSITION[1] - 30))
        self.draw_shape(shape, HOLD_SHAPE_POSITION)

    def draw_shape(self, shape, position):
        sx, sy = position
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(self.surface, shape.color, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    def draw_score(self, score):
        label = Text(f'Score: {score}', 30, WHITE)
        label.draw(self.surface, (SCORE_POSITION[0], SCORE_POSITION[1]))

    def draw_current_song(self, current_song):
        song_name, _ = os.path.splitext(current_song)
        label = Text(f'Now Playing: {song_name}', 20, WHITE)
        label.draw(self.surface, (S_WIDTH // 2 - label.label.get_width() // 2, S_HEIGHT - 40))

    def draw_fps(self, fps):
        label = Text(f"FPS: {int(fps)}", 30, WHITE)
        label.draw(self.surface, (10, 10))

