import pygame
import random
import os

pygame.mixer.init()
pygame.font.init()

# Constants
S_WIDTH = 800
S_HEIGHT = 750
PLAY_WIDTH = 300  # meaning 300 // 10 = 30 width per block
PLAY_HEIGHT = 600  # meaning 600 // 20 = 20 height per block
BLOCK_SIZE = 30
TOP_LEFT_X = (S_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = S_HEIGHT - PLAY_HEIGHT - 50

current_song = ""
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

class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0  # number from 0-3
    
    def ghost_piece_position(self, grid):
        ghost_piece = Piece(self.x, self.y, self.shape)
        ghost_piece.rotation = self.rotation
        while valid_space(ghost_piece, grid):
            ghost_piece.y += 1
        ghost_piece.y -= 1
        return ghost_piece

def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    global SHAPES, SHAPE_COLORS

    return Piece(5, 0, random.choice(SHAPES))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('forte', size)
    label = font.render(text, 1, color)

    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width() / 2), TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2))


def draw_grid(surface, row, col):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i * BLOCK_SIZE), (sx + PLAY_WIDTH, sy + i * BLOCK_SIZE))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * BLOCK_SIZE, sy), (sx + j * BLOCK_SIZE, sy + PLAY_HEIGHT))  # vertical lines


def clear_rows(grid, locked):
    inc = 0
    full_rows = []

    # Find full rows
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            full_rows.append(i)
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    # shift rows
    for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
        x, y = key
        rows_to_shift_down = sum(row_index > y for row_index in full_rows)
        if rows_to_shift_down > 0:
            newKey = (x, y + rows_to_shift_down)
            locked[newKey] = locked.pop(key)
    return inc



def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('forte', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = TOP_LEFT_X + PLAY_WIDTH + 40
    sy = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 100)

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface, ghost_piece):
    surface.fill((0,0,0))
    # Tetris Title
    font = pygame.font.SysFont('forte', 50)
    label = font.render('TETRIS', 1, (255,255,255))

    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), BLOCK_SIZE))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Draw ghost piece
    ghost_piece_positions = convert_shape_format(ghost_piece)
    for i in range(len(ghost_piece_positions)):
        x, y = ghost_piece_positions[i]
        if y > -1:
            pygame.draw.rect(surface, (224, 224, 244), (TOP_LEFT_X + x * BLOCK_SIZE + 1, TOP_LEFT_Y + y * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2), 1)

    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)


def draw_score(surface, score):
    font = pygame.font.SysFont('forte', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = TOP_LEFT_X + PLAY_WIDTH + 60
    sy = TOP_LEFT_Y + PLAY_HEIGHT / 2 - 300

    surface.blit(label, (sx , sy))

def calculate_fall_speed(score):
    base_speed = 0.27
    speed_increase = 0.01
    milestones = score // 50
    return max(base_speed - milestones * speed_increase, 0.05)

def load_songs():
    songs = []
    music_path = "music"
    for song in os.listdir(music_path):
        if song.endswith('.mp3') or song.endswith('.ogg'):
            songs.append(os.path.join(music_path, song))
    return songs

def play_random_song(songs):
    global current_song
    current_song = random.choice(songs)
    pygame.mixer.music.load(current_song)
    pygame.mixer.music.play(0)
    return os.path.basename(current_song)

def draw_current_song(surface, current_song):
    font = pygame.font.SysFont('forte', 20)
    song_name, _ = os.path.splitext(current_song)
    label = font.render('Now Playing: ' + song_name, 1, (255,255,255))

    surface.blit(label, (S_WIDTH // 2 - label.get_width() // 2, S_HEIGHT - 40))

def check_music(songs):
    global current_song
    if not pygame.mixer.music.get_busy():
        current_song = play_random_song(songs)
    return os.path.basename(current_song)

def draw_fps(surface, fps):
    font = pygame.font.SysFont('forte', 30)
    label = font.render(f"FPS: {int(fps)}", 1, (255, 255, 255))
    surface.blit(label, (10, 10))

def draw_hold_shape(shape, surface):
    font = pygame.font.SysFont('forte', 30)
    label = font.render('Hold', 1, (255,255,255))

    sx = TOP_LEFT_X - PLAY_WIDTH // 2 - 60
    sy = TOP_LEFT_Y + PLAY_HEIGHT // 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    surface.blit(label, (sx + 10, sy - 30))

def main(songs):
    global grid
    #init variables
    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    hold_piece = None
    hold_switched = False
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = calculate_fall_speed(0)
    score = 0
    current_song = play_random_song(songs)
    #lock delay variables
    ld_time = 0
    ld_limit = 20
    ld_resets = 0
    ld_max_resets = 10
    
    while run:

        grid = create_grid(locked_positions)
        ghost_piece = current_piece.ghost_piece_position(grid)
        fall_time += clock.get_rawtime()
        clock.tick()

        fps = clock.get_fps()

        current_song = check_music(songs)
            
        # handle piece falling
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_DOWN]:           
            fall_speed_multiplier = 5   
        else:                             
            fall_speed_multiplier = 1     

        if fall_time/1000 >= fall_speed / fall_speed_multiplier:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                if ld_time >= ld_limit or ld_resets >= ld_max_resets:
                    change_piece = True
                else:
                    ld_time += clock.get_rawtime()
            else:
                ld_time = 0
                ld_resets = 0

        # handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                    else:
                        ld_time = 0
                        ld_resets += 1


                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                    else:
                        ld_time = 0
                        ld_resets += 1

                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                    else:
                        ld_time = 0
                        ld_resets += 1

                elif event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True
                
                elif event.key == pygame.K_c:
                    if not hold_switched:
                        if hold_piece is None:
                            hold_piece = current_piece
                            current_piece = next_piece
                            next_piece = get_shape()
                        else:
                            hold_piece, current_piece = current_piece, hold_piece
                            current_piece.x = 5
                            current_piece.y = 0
                        hold_switched = True

        # update shape position on grid
        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # check if piece hit the ground
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            hold_switched = False

            cleared_rows = clear_rows(grid, locked_positions)
            if cleared_rows:
                score += 10 * cleared_rows
                fall_speed = calculate_fall_speed(score)
        
        # update the window
        draw_window(win, ghost_piece)
        draw_next_shape(next_piece, win)
        draw_score(win, score)
        draw_current_song(win, current_song)
        draw_fps(win, fps)
        if hold_piece:
            draw_hold_shape(hold_piece, win)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

    # Display "You Lost" message
    draw_text_middle("You Lost", 40, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    songs = load_songs()
    while run:
        win.fill((0,0,0))
        draw_text_middle('Press any key to begin', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                play_random_song(songs)
                main(songs)
    pygame.quit()


win = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption('Tetris')

main_menu()  # start game