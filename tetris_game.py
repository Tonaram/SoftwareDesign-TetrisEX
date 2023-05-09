# tetris_game.py
import pygame
from tetris.gameplay import ShapeOperations, RowOperations, FallSpeedCalculator, Grid
from tetris.shapes import get_shape
from tetris.music import  MusicPlayer, RandomSongDecorator
from tetris.display import TetrisDisplay
from tetris.constants import S_HEIGHT, S_WIDTH

class TetrisGame:
    def __init__(self):
        pygame.mixer.init()
        pygame.font.init()
        self.win = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.display = TetrisDisplay(self.win)
        self.shape_operations = ShapeOperations()
        self.row_operations = RowOperations()
        self.music_player = RandomSongDecorator(MusicPlayer())

    def main(self, songs):
        global grid
        #init variables
        locked_positions = {}  # (x,y):(255,0,0)
        grid_instance = Grid(locked_positions)
        grid = grid_instance.grid

        hold_piece = None
        hold_switched = False
        change_piece = False
        run = True
        current_piece = get_shape()
        next_piece = get_shape()
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = FallSpeedCalculator.calculate_fall_speed(0)
        score = 0
        current_song = self.music_player.play_random_song()
        #lock delay variables
        ld_time = 0
        ld_limit = 20
        ld_resets = 0
        ld_max_resets = 10
        
        while run:

            grid = grid_instance.create_grid(locked_positions)
            ghost_piece = current_piece.ghost_piece_position(grid, self.shape_operations.valid_space)
            fall_time += clock.get_rawtime()
            clock.tick()

            fps = clock.get_fps()

            current_song = self.music_player.check_music()
                
            # handle piece falling
            keys = pygame.key.get_pressed()  
            if keys[pygame.K_DOWN]:           
                fall_speed_multiplier = 5   
            else:                             
                fall_speed_multiplier = 1     

            if fall_time/1000 >= fall_speed / fall_speed_multiplier:
                fall_time = 0
                current_piece.y += 1
                if not self.shape_operations.valid_space(current_piece, grid) and current_piece.y > 0:
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
                        if not self.shape_operations.valid_space(current_piece, grid):
                            current_piece.x += 1
                        else:
                            ld_time = 0
                            ld_resets += 1


                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not self.shape_operations.valid_space(current_piece, grid):
                            current_piece.x -= 1
                        else:
                            ld_time = 0
                            ld_resets += 1

                    elif event.key == pygame.K_UP:
                        # rotate shape
                        current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                        if not self.shape_operations.valid_space(current_piece, grid):
                            current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                        else:
                            ld_time = 0
                            ld_resets += 1

                    elif event.key == pygame.K_SPACE:
                        while self.shape_operations.valid_space(current_piece, grid):
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
            shape_pos = self.shape_operations.convert_shape_format(current_piece)

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

                cleared_rows = self.row_operations.clear_rows(grid, locked_positions)
                if cleared_rows:
                    score += 10 * cleared_rows
                    fall_speed = FallSpeedCalculator.calculate_fall_speed(score)
            
            # update the window
            self.display.draw_window(ghost_piece, grid, self.shape_operations.convert_shape_format)
            self.display.draw_next_shape(next_piece)
            self.display.draw_score(score)
            self.display.draw_current_song(current_song)
            self.display.draw_fps(fps)
            if hold_piece:
                self.display.draw_hold_shape(hold_piece)
            pygame.display.update()

            # Check if user lost
            if self.shape_operations.check_lost(locked_positions):
                run = False

        # Display "You Lost" message
        self.display.draw_text_middle("You Lost", 40, (255, 255, 255))
        pygame.display.update()
        pygame.time.delay(2000)
    

    def main_menu(self):
        run = True
        songs = self.music_player.load_songs()
        while run:
            self.win.fill((0, 0, 0))
            self.display.draw_text_middle('Press any key to begin', 60, (255, 255, 255))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    self.music_player.play_random_song()
                    self.main(songs)
        pygame.quit()