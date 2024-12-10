

import math, random
class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]
        self.box_length = int(math.sqrt(row_length))
    def get_board(self):
        return self.board
    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) if num != 0 else "." for num in row))
    def valid_in_row(self, row, num):
        return num not in self.board[row]
    def valid_in_col(self, col, num):
        return num not in [self.board[row][col] for row in range(self.row_length)]
    def valid_in_box(self, row_start, col_start, num):
        for row in range(row_start, row_start + self.box_length):
            for col in range(col_start, col_start + self.box_length):
                if self.board[row][col] == num:
                    return False
        return True
    def is_valid(self, row, col, num):
        box_start_row = row - row % self.box_length
        box_start_col = col - col % self.box_length
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(box_start_row, box_start_col, num))
    def fill_values(self):
        def solve():
            for row in range(self.row_length):
                for col in range(self.row_length):
                    if self.board[row][col] == 0:
                        for num in random.sample(range(1, self.row_length + 1), self.row_length):
                            if self.is_valid(row, col, num):
                                self.board[row][col] = num
                                if solve():
                                    return True
                                self.board[row][col] = 0
                        return False
            return True
        solve()
    def fill_box(self, row_start, col_start):
        nums = list(range(1, self.row_length + 1))
        random.shuffle(nums)
        for row in range(row_start, row_start + self.box_length):
            for col in range(col_start, col_start + self.box_length):
                self.board[row][col] = nums.pop()
    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)
    def remove_cells(self):
        removed = 0
        while removed < self.removed_cells:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    sudoku.remove_cells()
    return sudoku.get_board()
generate_sudoku(9, 30)