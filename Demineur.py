import pygame
import random
import sys

# Initialisation de pygame
pygame.init()

# Définir les dimensions de la fenêtre du jeu
width, height = 600, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Démineur')

# Couleurs
black = (0, 0, 0)
white = (255, 255, 255)
gray = (192, 192, 192)
dark_gray = (160, 160, 160)
red = (255, 0, 0)
number_colors = [
    (0, 0, 255),      # 1 - Bleu
    (0, 128, 0),      # 2 - Vert
    (255, 0, 0),      # 3 - Rouge
    (0, 0, 128),      # 4 - Bleu Foncé
    (128, 0, 0),      # 5 - Marron
    (0, 128, 128),    # 6 - Cyan Foncé
    (0, 0, 0),        # 7 - Noir
    (128, 128, 128)   # 8 - Gris
]

# Dimensions de la grille
cols, rows = 10, 10
cell_size = width // cols

# Variables de jeu
mines_count = 15
grid = []
flags = []
revealed = []
mines = []
game_over = False
bomb_clicked = None

# Police
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

def setup():
    global grid, mines, flags, revealed, game_over, bomb_clicked
    # Réinitialiser les listes
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    mines = []
    flags = []
    revealed = [[False for _ in range(cols)] for _ in range(rows)]
    game_over = False
    bomb_clicked = None
    
    # Placer les mines
    while len(mines) < mines_count:
        x = random.randint(0, cols - 1)
        y = random.randint(0, rows - 1)
        if (x, y) not in mines:
            mines.append((x, y))
            grid[y][x] = -1

    # Calculer les chiffres
    for mine in mines:
        mx, my = mine
        for i in range(-1, 2):
            for j in range(-1, 2):
                nx, ny = mx + i, my + j
                if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] != -1:
                    grid[ny][nx] += 1

def reveal_cell(x, y):
    if revealed[y][x]:
        return
    revealed[y][x] = True
    if grid[y][x] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                nx, ny = x + i, y + j
                if 0 <= nx < cols and 0 <= ny < rows:
                    reveal_cell(nx, ny)

def reveal_all_bombs():
    global revealed
    for (mx, my) in mines:
        revealed[my][mx] = True

def draw_grid():
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if revealed[y][x] or game_over:
                pygame.draw.rect(window, gray, rect)
                if grid[y][x] > 0:
                    color = number_colors[grid[y][x] - 1]
                    text = font.render(str(grid[y][x]), True, color)
                    window.blit(text, (x * cell_size + cell_size // 4, y * cell_size + cell_size // 4))
                elif grid[y][x] == -1:
                    pygame.draw.circle(window, black, rect.center, cell_size // 4)
            else:
                pygame.draw.rect(window, dark_gray, rect)
            pygame.draw.rect(window, black, rect, 2)
            if (x, y) in flags:
                text = font.render('F', True, red)
                window.blit(text, (x * cell_size + cell_size // 4, y * cell_size + cell_size // 4))
    if bomb_clicked:
        bx, by = bomb_clicked
        rect = pygame.Rect(bx * cell_size, by * cell_size, cell_size, cell_size)
        pygame.draw.circle(window, red, rect.center, cell_size // 4)

def show_game_over_window():
    # Créer une nouvelle fenêtre pour le message Game Over
    game_over_window = pygame.display.set_mode((400, 200))
    pygame.display.set_caption('Game Over')

    game_over_font = pygame.font.Font(None, 72)
    small_font = pygame.font.Font(None, 36)
    game_over_message = game_over_font.render('Game Over', True, red)
    retry_message = small_font.render('Cliquez pour rejouer', True, black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                setup()
                return

        game_over_window.fill(white)
        game_over_window.blit(game_over_message, (50, 30))
        game_over_window.blit(retry_message, (90, 120))
        pygame.display.flip()

def reveal_animation(cells, color):
    for alpha in range(0, 255, 15):
        for cell in cells:
            x, y = cell
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            surface = pygame.Surface((cell_size, cell_size))
            surface.set_alpha(alpha)
            surface.fill(color)
            window.blit(surface, (x * cell_size, y * cell_size))
        pygame.display.flip()
        pygame.time.delay(20)

def main():
    global window, game_over
    setup()

    # Boucle principale du jeu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    show_game_over_window()
                    window = pygame.display.set_mode((width, height))
                    pygame.display.set_caption('Démineur')
                else:
                    x, y = event.pos
                    grid_x, grid_y = x // cell_size, y // cell_size
                    if event.button == 1:  # Clique gauche
                        if grid[grid_y][grid_x] == -1:
                            game_over = True
                            bomb_clicked = (grid_x, grid_y)
                            reveal_animation([(grid_x, grid_y)], red)
                            reveal_all_bombs()
                            window.fill(white)
                            draw_grid()
                            pygame.display.flip()
                            pygame.time.delay(5000)  # Pause de 5 secondes
                            show_game_over_window()
                            window = pygame.display.set_mode((width, height))
                            pygame.display.set_caption('Démineur')
                        else:
                            reveal_animation([(grid_x, grid_y)], gray)
                            reveal_cell(grid_x, grid_y)
                    elif event.button == 3:  # Clique droit
                        if (grid_x, grid_y) in flags:
                            flags.remove((grid_x, grid_y))
                        else:
                            flags.append((grid_x, grid_y))

        window.fill(white)
        draw_grid()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
