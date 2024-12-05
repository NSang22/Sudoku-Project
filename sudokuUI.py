pip install pygame
import pygame
import sys

pygame.init()

def startScreen(screen):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 74)
    text = font.render("Sudoku", True, (0, 0, 0))
    screen.blit(text, (150, 50))


    buttons = {
        "Easy": pygame.Rect(100, 200, 200, 50),
        "Medium": pygame.Rect(100, 300, 200, 50),
        "Hard": pygame.Rect(100, 400, 200, 50)
    }
    for label, rect in buttons.items():
        pygame.draw.rect(screen, (0, 128, 0), rect)
        text = font.render(label, True, (255, 255, 255))
        screen.blit(text, (rect.x + 10, rect.y + 10))

    pygame.display.flip()
    return buttons



def draw_grid(screen):
    for x in range(0, 450, 50):
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, 450), 1)
        pygame.draw.line(screen, (0, 0, 0), (0, x), (450, x), 1)

    for x in range(0, 450, 150):
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, 450), 3)
        pygame.draw.line(screen, (0, 0, 0), (0, x), (450, x), 3)

def end_screen(screen, success):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 74)
    message = "Congratulations!" if success else "Game Over!"
    text = font.render(message, True, (0, 128, 0) if success else (255, 0, 0))
    screen.blit(text, (50, 200))
    pygame.display.flip()


def handle_input(event, board):
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos

        row, col = y // 50, x // 50
        board.select(row, col)

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            board.place_number()
        elif pygame.K_1 <= event.key <= pygame.K_9:
            board.sketch(event.key - pygame.K_0)

#if button = easy:
    #generate 30 cells

#if button = medium:
    #generate 40 cells

#if button = hard:
    #generate 50 cells