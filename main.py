import pygame
import time

pygame.init()

WIDTH = 100
HEIGHT = 100
CELL = 10
RIGHT_MARGIN = 200
MENU_ITEM_HEIGHT = 50

START_GAME = False

life = pygame.display.set_mode(
    size=(WIDTH*CELL + RIGHT_MARGIN, HEIGHT*CELL)
)
pygame.display.set_caption("Conway's Game of Life")

WHITE = (255, 255, 255)
RED = (85, 17, 17)
BLACK = (17, 17, 17)

DEAD = False
ALIVE = True

PRESETS = [
    ("gliders", [
        (1, 5),
        (1, 6),
        (2, 5),
        (2, 6),
        (11, 5),
        (11, 6),
        (11, 7),
        (12, 4),
        (12, 8),
        (13, 3),
        (13, 9),
        (14, 3),
        (14, 9),
        (15, 6),
        (16, 4),
        (16, 9),
        (17, 5),
        (17, 6),
        (17, 7),
        (18, 6),
        (21, 3),
        (21, 4),
        (21, 5),
        (22, 3),
        (22, 4),
        (22, 5),
        (23, 2),
        (23, 6),
        (25, 1),
        (25, 2),
        (25, 6),
        (25, 7),
        (35, 3),
        (35, 4),
        (36, 3),
        (36, 4),
    ]),
    ("clear", []),
]

def displayMenu():

    life.fill(BLACK)
    drawGrid()

    font = pygame.font.SysFont(None, 48)

    text_img = font.render("stop" if START_GAME else "play", True, WHITE)
    life.blit(text_img, (WIDTH*CELL + 10, 0))

    for loc, (text, coords) in enumerate(PRESETS, start=1):
        loc_y = loc * MENU_ITEM_HEIGHT
        text_img = font.render(text, True, WHITE)
        life.blit(text_img, (WIDTH*CELL + 10, loc_y))
        MENU_LOC_TO_ACTION[loc] = presetFactory(coords)

    pygame.display.update()

def startGame(*args):
    global START_GAME
    START_GAME = not START_GAME
    displayMenu()

def presetFactory(coords):

    def setGrid(*args):
        
        for i in range(HEIGHT):
            for j in range(WIDTH):
                grid[i][j] = DEAD

        for x, y in coords:
            grid[y][x] = ALIVE

    return setGrid

MENU_LOC_TO_ACTION = {
    0: startGame,
}

grid = [
    [DEAD for _ in range(WIDTH)]
    for _ in range(HEIGHT)
]

def drawGrid():
    """
        draw the grid
    """
    for i, row in enumerate(grid):
        for j, x in enumerate(row):
            if x is DEAD:
                pygame.draw.rect(
                    life,
                    RED,
                    pygame.Rect(j*CELL, i*CELL, CELL, CELL),
                )
            else:
                pygame.draw.rect(
                    life,
                    WHITE,
                    pygame.Rect(j*CELL, i*CELL, CELL, CELL),
                )
    pygame.display.update()

def click():
    global START_GAME

    m_x, m_y = pygame.mouse.get_pos()
    if m_x >= WIDTH*CELL:
        loc = m_y // MENU_ITEM_HEIGHT
        if loc in MENU_LOC_TO_ACTION:
            MENU_LOC_TO_ACTION[loc]()
        return

    row = m_y // CELL
    col = m_x // CELL

    print(f"{row}, {col}")

    grid[row][col] = not grid[row][col]

def lifeCycle():

    num_grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    def increment(i, j):
        if 0 <= i and i < HEIGHT and 0 <= j and j < WIDTH:
            num_grid[i][j] += 1

    for i, (num_row, life_row) in enumerate(zip(num_grid, grid)):
        for j, (num, life) in enumerate(zip(num_row, life_row)):
            if life:
                increment(i-1, j-1)
                increment(i-1, j)
                increment(i-1, j+1)
                increment(i, j-1)
                increment(i, j+1)
                increment(i+1, j-1)
                increment(i+1, j)
                increment(i+1, j+1)

    for i, (num_row, life_row) in enumerate(zip(num_grid, grid)):
        for j, (num, life) in enumerate(zip(num_row, life_row)):
            if life:
                if num < 2 or 3 < num:
                    grid[i][j] = DEAD
            else:
                if num == 3:
                    grid[i][j] = ALIVE

def main():

    displayMenu()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("got mouse button down")
                click()
                drawGrid()

        if START_GAME: 
            lifeCycle()
            drawGrid()
            time.sleep(0.25)


if __name__ == "__main__":
    main()
