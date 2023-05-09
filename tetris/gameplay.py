# tetris\gameplay.py
from abc import ABC, abstractmethod

class Grid:
    def __init__(self, locked_positions={}):
        self.grid = self.create_grid(locked_positions)

    def create_grid(self, locked_positions):
        grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_positions:
                    c = locked_positions[(j, i)]
                    grid[i][j] = c
        return grid


class ShapeOperationStrategy(ABC):
    @abstractmethod
    def execute(self, shape, grid=None):
        pass

class ConvertShapeFormatStrategy(ShapeOperationStrategy):
    def execute(self, shape, grid=None):
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

class ValidSpaceStrategy(ShapeOperationStrategy):
    def execute(self, shape, grid):
        accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
        accepted_positions = [j for sub in accepted_positions for j in sub]
        formatted = ConvertShapeFormatStrategy().execute(shape)

        for pos in formatted:
            if pos not in accepted_positions:
                if pos[1] > -1:
                    return False

        return True

class CheckLostStrategy(ShapeOperationStrategy):
    def execute(self, positions, grid=None):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False

class ShapeOperations:
    def __init__(self):
        self.convert_shape_format_strategy = ConvertShapeFormatStrategy()
        self.valid_space_strategy = ValidSpaceStrategy()
        self.check_lost_strategy = CheckLostStrategy()

    def convert_shape_format(self, shape):
        return self.convert_shape_format_strategy.execute(shape)

    def valid_space(self, shape, grid):
        return self.valid_space_strategy.execute(shape, grid)

    def check_lost(self, positions):
        return self.check_lost_strategy.execute(positions)


class RowOperations:
    def clear_rows(self, grid, locked):
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


class FallSpeedCalculator:
    @staticmethod
    def calculate_fall_speed(score):
        base_speed = 0.27
        speed_increase = 0.01
        milestones = score // 50
        return max(base_speed - milestones * speed_increase, 0.05)