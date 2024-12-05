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
       print("\n")


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

   def fill_values(self):
       self.fill_diagonal()

       if not self.fill_remaining(0, self.box_length):
           raise ValueError("Failed to generate a valid Sudoku board.")

   import random

   def fill_remaining(self, row, col, backtrack_count=0):
       if col >= self.row_length and row < self.row_length - 1:
           row += 1
           col = 0
       if row >= self.row_length and col >= self.row_length:
           return True

       if row < self.box_length and col < self.box_length:
           col = self.box_length
       elif row < self.row_length - self.box_length and col == (row // self.box_length) * self.box_length:
           col += self.box_length
       elif row >= self.row_length - self.box_length and col >= self.row_length:
           return True

       numbers = list(range(1, self.row_length + 1))
       random.shuffle(numbers)

       for num in numbers:
           if self.is_valid(row, col, num):
               self.board[row][col] = num
               print(f"Placing {num} at ({row}, {col})")
               if self.fill_remaining(row, col + 1, backtrack_count):
                   return True
               print(f"Backtracking from ({row}, {col})")
               self.board[row][col] = 0

       backtrack_count += 1
       if backtrack_count > 100:
           print(f"Resetting board from row {row}")
           self.reset_partial_board(row)
           return self.fill_remaining(0, 0, 0)

       return False

   def reset_partial_board(self, start_row):
       for row in range(start_row, self.row_length):
           for col in range(self.row_length):
               self.board[row][col] = 0

def generate_sudoku(size, removed):
    for attempt in range(5):
        sudoku = SudokuGenerator(size, removed)
        try:
            sudoku.fill_values()
            sudoku.remove_cells()
            print(f"Sudoku generated successfully on attempt {attempt + 1}")
            return sudoku.get_board()
        except ValueError:
            print(f"Retrying Sudoku generation: Attempt {attempt + 1}")
    raise ValueError("Failed to generate a valid Sudoku puzzle after 5 attempts.")