import pygame
import sys
from TBoard_Cell_Classes import Board
from TSudokuGenerator_Class import generate_sudoku

def main():
    pygame.init()

    screen = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("Sudoku Game")

    title_font = pygame.font.SysFont(None, 60)
    option_font = pygame.font.SysFont(None, 40)
    difficulty_font = pygame.font.SysFont(None, 30)

    game_state = "START"
    board = None

    def show_start_screen():
        screen.fill((255, 255, 255))
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
        screen.fill((255, 255, 255))
        option = option_font.render("Select a difficulty:", True, (0, 0, 0))
        screen.blit(option, (150, 180))

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

    def show_game_in_progress():
        screen.fill((255, 255, 255))
        if board:
            board.draw()

        reset_button = pygame.Rect(50, 460, 100, 50)
        restart_button = pygame.Rect(200, 460, 100, 50)
        exit_button = pygame.Rect(350, 460, 100, 50)

        pygame.draw.rect(screen, (0, 255, 0), reset_button)
        pygame.draw.rect(screen, (255, 255, 0), restart_button)
        pygame.draw.rect(screen, (255, 0, 0), exit_button)

        reset_text = option_font.render("Reset", True, (255, 255, 255))
        restart_text = option_font.render("Restart", True, (255, 255, 255))
        exit_text = option_font.render("Exit", True, (255, 255, 255))

        screen.blit(reset_text, (60, 475))
        screen.blit(restart_text, (215, 475))
        screen.blit(exit_text, (365, 475))

        pygame.display.flip()

    running = True
    while running:
        if game_state == "START":
            show_start_screen()
        elif game_state == "DIFFICULTY":
            show_difficulty_screen()
        elif game_state == "IN_PROGRESS":
            show_game_in_progress()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
                        try:
                            board_array = generate_sudoku(9, 30)  # Easy difficulty
                            board = Board(540, 540, screen, difficulty="easy")
                            board.initialize_from_array(board_array)
                            game_state = "IN_PROGRESS"
                        except ValueError:
                            print("Failed to generate a puzzle. Please try again.")
                            game_state = "START"

                    elif medium_button.collidepoint(event.pos):
                        try:
                            board_array = generate_sudoku(9, 40)  # Medium difficulty
                            board = Board(540, 540, screen, difficulty="medium")
                            board.initialize_from_array(board_array)
                            game_state = "IN_PROGRESS"
                        except ValueError:
                            print("Failed to generate a puzzle. Please try again.")
                            game_state = "START"

                    elif hard_button.collidepoint(event.pos):
                        try:
                            board_array = generate_sudoku(9, 50)  # Hard difficulty
                            board = Board(540, 540, screen, difficulty="hard")
                            board.initialize_from_array(board_array)
                            game_state = "IN_PROGRESS"
                        except ValueError:
                            print("Failed to generate a puzzle. Please try again.")
                            game_state = "START"

                elif game_state == "IN_PROGRESS":
                    reset_button = pygame.Rect(50, 460, 100, 50)
                    restart_button = pygame.Rect(200, 460, 100, 50)
                    exit_button = pygame.Rect(350, 460, 100, 50)

                    if reset_button.collidepoint(event.pos):
                        if board:
                            board.reset_to_original()
                    elif restart_button.collidepoint(event.pos):
                        game_state = "START"
                    elif exit_button.collidepoint(event.pos):
                        running = False
                    else:
                        if board:
                            row, col = board.click(event.pos[0], event.pos[1])
                            if row is not None and col is not None:
                                board.select(row, col)

            if event.type == pygame.KEYDOWN:
                if game_state == "IN_PROGRESS" and board:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        board.sketch(event.key - pygame.K_1 + 1)
                    elif event.key == pygame.K_RETURN:
                        if board.selected_cell:
                            board.place_number(board.selected_cell.sketched_value)
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        board.clear()

                    if board.is_full():
                        if board.check_board():
                            game_state = "WIN"
                        else:
                            game_state = "GAME_OVER"

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
