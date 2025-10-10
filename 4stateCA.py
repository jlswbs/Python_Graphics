import pygame
import numpy as np

# Inicializace Pygame
pygame.init()

# Nastavení okna
width, height = 800, 600
cell_size = 8
rows, cols = height // cell_size, width // cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("4-stavový celulární automat s rekurzivní dynamikou")

# Barvy pro jednotlivé stavy (RGBA)
colors = {
    0: (0, 0, 0),      # Černá (mrtvý)
    1: (255, 0, 0),    # Červená
    2: (0, 255, 0),    # Zelená
    3: (0, 0, 255)     # Modrá
}

# Inicializace mřížky (náhodné stavy 0-3)
grid = np.random.randint(0, 4, size=(rows, cols))

# Funkce pro výpočet sousedů
def count_neighbors(grid, x, y, state):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nx, ny = (x + i) % rows, (y + j) % cols  # Periodické okraje
            if grid[nx, ny] == state:
                count += 1
    return count

# Pravidla automatu pro kontinuální změnu
def update_grid(grid):
    new_grid = grid.copy()
    for i in range(rows):
        for j in range(cols):
            current_state = grid[i, j]
            neighbors = [count_neighbors(grid, i, j, s) for s in range(4)]
            
            # Cyklická pravidla inspirovaná kamenem-nůžkami-papírem:
            # Stav 0 je "prázdný", ostatní stavy se přeměňují cyklicky
            # Pokud má stav X více než 3 sousedy stavu X+1, přemění se na X+1
            # Pokud má málo sousedů, může se vrátit na předchozí stav
            if current_state == 0:
                if neighbors[1] >= 3:  # Prázdný se stane červeným, pokud je dost červených sousedů
                    new_grid[i, j] = 1
            elif current_state == 1:
                if neighbors[2] >= 3:  # Červený se stane zeleným
                    new_grid[i, j] = 2
                elif neighbors[1] < 2:  # Příliš málo červených sousedů -> zpět na prázdný
                    new_grid[i, j] = 0
            elif current_state == 2:
                if neighbors[3] >= 3:  # Zelený se stane modrým
                    new_grid[i, j] = 3
                elif neighbors[2] < 2:  # Příliš málo zelených sousedů -> zpět na červený
                    new_grid[i, j] = 1
            elif current_state == 3:
                if neighbors[0] >= 3:  # Modrý se stane prázdným
                    new_grid[i, j] = 0
                elif neighbors[3] < 2:  # Příliš málo modrých sousedů -> zpět na zelený
                    new_grid[i, j] = 2
    return new_grid

# Hlavní smyčka
running = True
paused = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Mezerník pro pauzu/obnovení
                paused = not paused
            elif event.key == pygame.K_r:  # R pro reset mřížky
                grid = np.random.randint(0, 4, size=(rows, cols))

    if not paused:
        # Rekurzivní předávání: výstup jednoho kroku je vstupem dalšího
        grid = update_grid(grid)

    # Vykreslení mřížky
    screen.fill((255, 255, 255))  # Bílé pozadí
    for i in range(rows):
        for j in range(cols):
            pygame.draw.rect(screen, colors[grid[i, j]],
                            (j * cell_size, i * cell_size, cell_size, cell_size))

    pygame.display.flip()
    clock.tick(10)  # Rychlost simulace (10 FPS)

pygame.quit()