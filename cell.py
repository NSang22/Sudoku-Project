import pygame
class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0
        self.selected = False
        self.is_prefilled = value != 0
    def set_cell_value(self, value):
        if 0 <= value <= 9:
            self.value = value
        else:
            print("Invalid value!")
    def set_sketched_value(self, value):
        if 0 <= value <= 9:
            self.sketched_value = value
        else:
            print("Invalid value!")
    def draw(self):
        font = pygame.font.Font(None, 40)
        if self.value != 0:
            text = font.render(str(self.value), True, pygame.Color('black'))
            text_rect = text.get_rect(center=(self.col * 60 + 30, self.row * 60 + 30))
            self.screen.blit(text, text_rect)
        elif self.sketched_value != 0:
            text = font.render(str(self.sketched_value), True, pygame.Color('red'))  # Changed to red
            text_rect = text.get_rect(center=(self.col * 60 + 30, self.row * 60 + 30))
            self.screen.blit(text, text_rect)

        color = pygame.Color('red') if self.selected else pygame.Color('black')
        pygame.draw.rect(self.screen, color, (self.col * 60, self.row * 60, 60, 60), 2)
class Board:
    def __init__(self, width, height, screen, board_data):
        self.width = width
        self.height = height
        self.screen = screen
        self.board_data = board_data
        self.board = board
        self.cells = [[Cell(value, r, c, screen) for c, value in enumerate(row)] for r, row in enumerate(board_data)]
        self.selected_cell = None
    def draw(self):
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 1
            color = (0, 0, 0) if i % 3 == 0 else (128, 128, 128)
            pygame.draw.line(self.screen, color,
                             (i * 60, 0),
                             (i * 60, 540),
                             line_width)

            # Draw horizontal lines
            pygame.draw.line(self.screen, color,
                             (0, i * 60),
                             (540, i * 60),
                             line_width)
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
    def reset_to_original(self, original_board):
        for r in range(9):
            for c in range(9):
                original_value = original_board[r][c]
                cell = self.cells[r][c]
                if cell.value != original_value:
                    cell.set_cell_value(original_value)
    def clear_sketched_values(self):
        for row in self.cells:
            for cell in row:
                cell.set_sketched_value(0)
    def is_full(self):
        return all(cell.value != 0 for row in self.cells for cell in row)
    def check_board(self):
        for row in self.cells:
            values = [cell.value for cell in row if cell.value != 0]
            if len(values) != len(set(values)):
                return False
        for col in range(9):
            values = [self.cells[row][col].value for row in range(9) if self.cells[row][col].value != 0]
            if len(values) != len(set(values)):
                return False
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                values = [
                    self.cells[r][c].value
                    for r in range(box_row, box_row + 3)
                    for c in range(box_col, box_col + 3)
                    if self.cells[r][c].value != 0
                ]
                if len(values) != len(set(values)):
                    return False
        return True
class Board:
    def __init__(self, width, height, screen, board_data):
        self.width = width
        self.height = height
        self.screen = screen
        self.board_data = board_data
        self.cells = [[Cell(value, r, c, screen) for c, value in enumerate(row)] for r, row in enumerate(board_data)]
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
        if not self.cells[row][col].is_prefilled:
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
    def reset_to_original(self, original_board):
        for r in range(9):
            for c in range(9):
                original_value = original_board[r][c]
                cell = self.cells[r][c]
                if cell.value != original_value:
                    cell.set_cell_value(original_value)
    def clear_sketched_values(self):
        for row in self.cells:
            for cell in row:
                cell.set_sketched_value(0)
    def clear_selected_cell_sketch(self):
        if self.selected_cell:
            self.selected_cell.sketched_value = 0
            self.draw()

    def clear_selected_cell_value(self):
        if self.selected_cell:
            self.selected_cell.value = 0
            self.selected_cell.sketched_value = 0
    def is_full(self):
        return all(cell.value != 0 for row in self.cells for cell in row)
    def check_board(self):
        for row in self.cells:
            values = [cell.value for cell in row if cell.value != 0]
            if len(values) != len(set(values)):
                return False
        for col in range(9):
            values = [self.cells[row][col].value for row in range(9) if self.cells[row][col].value != 0]
            if len(values) != len(set(values)):
                return False
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                values = [
                    self.cells[r][c].value
                    for r in range(box_row, box_row + 3)
                    for c in range(box_col, box_col + 3)
                    if self.cells[r][c].value != 0
                ]
                if len(values) != len(set(values)):
                    return False
        return True