import pygame
import numpy as np

pygame.init()

width, height = 800, 600
cell_size = 8
rows, cols = height // cell_size, width // cell_size
screen = pygame.display.set_mode((width, height))

colors = {
    0: (0, 0, 0),
    1: (255, 255, 255)
}

grid = np.random.randint(0, 2, size=(rows, cols))

def count_neighbors(grid, x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nx, ny = (x + i) % rows, (y + j) % cols
            count += grid[nx, ny]
    return count

def update_grid(grid):
    new_grid = grid.copy()
    for i in range(rows):
        for j in range(cols):
            neighbors = count_neighbors(grid, i, j)
            if grid[i, j] == 0:
                if neighbors == 3:
                    new_grid[i, j] = 1
            else:  # Živá buňka
                if neighbors < 2 or neighbors > 3:
                    new_grid[i, j] = 0
                else:
                    new_grid[i, j] = 1
    return new_grid

running = True
paused = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                grid = np.random.randint(0, 2, size=(rows, cols))

    if not paused:
        grid = update_grid(grid)

    screen.fill((255, 255, 255))
    for i in range(rows):
        for j in range(cols):
            pygame.draw.rect(screen, colors[grid[i, j]],
                            (j * cell_size, i * cell_size, cell_size, cell_size))

    pygame.display.flip()

pygame.quit()