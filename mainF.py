import pygame
from sudoku_generator import SudokuGenerator
from cell import Board
import sys
def main():
    pygame.init()
    screen = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku Game")

    background = pygame.image.load("istockphoto-636267114-612x612.jpg").convert()
    screen.blit(pygame.transform.scale(background, (540, 540)), (0, 0))
    win_screen = pygame.image.load("istockphoto-1339034513-612x612.jpg").convert()
    lose_screen = pygame.image.load("sadface.jpeg").convert()


    # Font
    title_font = pygame.font.SysFont("None", 60)
    option_font = pygame.font.SysFont("None", 40)
    difficulty_font = pygame.font.SysFont("None", 30)

    game_state = "START"
    board = None
    original_board = None
    clock = pygame.time.Clock()
    def show_start_screen():
        # screen.fill((255, 255, 255))
        title = title_font.render("Sudoku Game", True, (0, 0, 0))
        screen.blit(title, (130, 40))
        start_button = pygame.Rect(170, 250, 200, 50)
        quit_button = pygame.Rect(170, 320, 200, 50)
        pygame.draw.rect(screen, (0, 255, 0), start_button)
        pygame.draw.rect(screen, (225, 0, 0), quit_button)
        start_text = option_font.render("Start", True, (255, 255, 255))
        quit_text = option_font.render("Quit", True, (255, 255, 255))
        screen.blit(start_text, (240, 265))
        screen.blit(quit_text, (240, 335))
        pygame.display.flip()
    def show_difficulty_screen():
        # screen.fill((255, 255, 255))
        option = option_font.render("Select a difficulty:", True, (0, 0, 0))
        screen.blit(option, (150, 180))
        # Difficulty buttons
        easy_button = pygame.Rect(170, 250, 200, 50)
        medium_button = pygame.Rect(170, 320, 200, 50)
        hard_button = pygame.Rect(170, 390, 200, 50)
        pygame.draw.rect(screen, (0, 255, 0), easy_button)
        pygame.draw.rect(screen, (0, 255, 0), medium_button)
        pygame.draw.rect(screen, (0, 255, 0), hard_button)
        easy_text = difficulty_font.render("Easy", True, (255, 255, 255))
        medium_text = difficulty_font.render("Medium", True, (255, 255, 255))
        hard_text = difficulty_font.render("Hard", True, (255, 255, 255))
        screen.blit(easy_text, (240, 265))
        screen.blit(medium_text, (230, 335))
        screen.blit(hard_text, (230, 405))
        pygame.display.flip()
    def show_game_over():
        screen.blit(pygame.transform.scale(lose_screen, (540, 540)), (0, 0))
        game_over_text = option_font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (220, 200))
        pygame.display.flip()
    def show_win():
        screen.blit(pygame.transform.scale(win_screen, (540, 540)), (0, 0))
        win_text = option_font.render("You Win!", True, (0, 255, 0))
        screen.blit(win_text, (220, 200))
        pygame.display.flip()
    def show_game_in_progress():
        screen.fill((255, 255, 255))
        board.draw()
        reset_button = pygame.Rect(50, 550, 100, 40)
        restart_button = pygame.Rect(200, 550, 100, 40)
        exit_button = pygame.Rect(350, 550, 100, 40)
        pygame.draw.rect(screen, (0, 255, 0), reset_button)
        pygame.draw.rect(screen, (255, 170, 51), restart_button)
        pygame.draw.rect(screen, (255, 0, 0), exit_button)
        reset_text = option_font.render("Reset", True, (255, 255, 255))
        restart_text = option_font.render("Restart", True, (255, 255, 255))
        exit_text = option_font.render("Exit", True, (255, 255, 255))
        screen.blit(reset_text, (60, 560))
        screen.blit(restart_text, (200, 560))
        screen.blit(exit_text, (365, 560))
        pygame.display.flip()
    running = True
    while running:
        if game_state == "START":
            show_start_screen()
        elif game_state == "DIFFICULTY":
            show_difficulty_screen()
        elif game_state == "IN_PROGRESS":
            show_game_in_progress()
        elif game_state == "GAME_OVER":
            show_game_over()
        elif game_state == "WIN":
            show_win()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "START":
                    start_button = pygame.Rect(170, 250, 200, 50)
                    quit_button = pygame.Rect(170, 320, 200, 50)
                    if start_button.collidepoint(event.pos):
                        game_state = "DIFFICULTY"
                    elif quit_button.collidepoint(event.pos):
                        running = False
                elif game_state == "DIFFICULTY":
                    easy_button = pygame.Rect(170, 250, 200, 50)
                    medium_button = pygame.Rect(170, 320, 200, 50)
                    hard_button = pygame.Rect(170, 390, 200, 50)
                    if easy_button.collidepoint(event.pos):
                        game_state = "IN_PROGRESS"
                        difficulty = 30  # Easy
                    elif medium_button.collidepoint(event.pos):
                        game_state = "IN_PROGRESS"
                        difficulty = 40  # Medium
                    elif hard_button.collidepoint(event.pos):
                        game_state = "IN_PROGRESS"
                        difficulty = 50  # Hard
                    sudoku_generator = SudokuGenerator(9, difficulty)
                    sudoku_generator.fill_values()
                    sudoku_generator.remove_cells()
                    board = Board(540, 540, screen, sudoku_generator.get_board())
                    original_board = [row[:] for row in sudoku_generator.get_board()]
                elif game_state == "IN_PROGRESS":
                    reset_button = pygame.Rect(50, 550, 100, 40)
                    restart_button = pygame.Rect(200, 550, 100, 40)
                    exit_button = pygame.Rect(350, 550, 100, 40)
                    if reset_button.collidepoint(event.pos):
                        board.reset_to_original(original_board)
                        board.clear_sketched_values()
                        board.draw()
                    elif restart_button.collidepoint(event.pos):
                        game_state = "START"
                        background = pygame.image.load("istockphoto-636267114-612x612.jpg").convert()
                        screen.blit(pygame.transform.scale(background, (540, 540)), (0, 0))
                        show_start_screen()
                    elif exit_button.collidepoint(event.pos)    :
                        running = False
                    else:
                        x, y = event.pos
                        row, col = board.click(x, y)
                        if row is not None and col is not None:
                            board.select(row, col)
            elif event.type == pygame.KEYDOWN:
                if game_state == "IN_PROGRESS":
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        if board.selected_cell:
                            board.sketch(event.key - pygame.K_1 + 1)
                    elif event.key == pygame.K_RETURN:
                        if board.selected_cell:
                            board.place_number(board.selected_cell.sketched_value)
                            if board.is_full() and board.check_board():
                                game_state = "WIN"
                                show_win()
                    elif event.key == pygame.K_BACKSPACE:
                        if board.selected_cell:
                            if board.selected_cell.value != 0:
                                board.clear_selected_cell_value()
                            else:
                                board.clear_selected_cell_sketch()
                    # if board.is_full() and board.check_board():
                    #     game_state = "WIN"
                    elif board.is_full():
                        game_state = "GAME_OVER"
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
if __name__ == "__main__":
    main()