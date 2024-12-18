
import pygame

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0
        self.selected = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        font = pygame.font.Font(None, 40)
        if self.value != 0:
            text = font.render(str(self.value), True, pygame.Color('black'))
            self.screen.blit(text, (self.col * 60 + 20, self.row * 60 + 10))
        elif self.sketched_value != 0:
            text = font.render(str(self.sketched_value), True, pygame.Color('gray'))
            self.screen.blit(text, (self.col * 60 + 5, self.row * 60 + 5))

        color = pygame.Color('red') if self.selected else pygame.Color('black')
        pygame.draw.rect(self.screen, color, (self.col * 60, self.row * 60, 60, 60), 2)


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = [[Cell(0, r, c, screen) for c in range(9)] for r in range(9)]
        self.selected_cell = None

    def draw(self):
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, pygame.Color('black'), (0, i * 60), (540, i * 60), line_width)
            pygame.draw.line(self.screen, pygame.Color('black'), (i * 60, 0), (i * 60, 540), line_width)

        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        if 0 <= x < 540 and 0 <= y < 540:
            return y // 60, x // 60
        return None

    def clear(self):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.sketched_value = 0

    def sketch(self, value):
        if self.selected_cell:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            self.selected_cell.set_cell_value(value)
            self.selected_cell.sketched_value = 0

    def reset_to_original(self):
        for row in self.cells:
            for cell in row:
                cell.set_cell_value(0)
                cell.set_sketched_value(0)

    def is_full(self):
        return all(cell.value != 0 for row in self.cells for cell in row)

    def update_board(self):
        self.board = [[cell.value for cell in row] for row in self.cells]

    def find_empty(self):
        for r, row in enumerate(self.cells):
            for c, cell in enumerate(row):
                if cell.value == 0:
                    return r, c
        return None

    def check_board(self):
        def is_valid_group(group):
            values = [cell.value for cell in group if cell.value != 0]
            return len(values) == len(set(values))

        for row in self.cells:
            if not is_valid_group(row):
                return False

        for col in range(9):
            if not is_valid_group([self.cells[row][col] for row in range(9)]):
                return False

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = [
                    self.cells[r][c]
                    for r in range(box_row, box_row + 3)
                    for c in range(box_col, box_col + 3)
                ]
                if not is_valid_group(box):
                    return False

        return True