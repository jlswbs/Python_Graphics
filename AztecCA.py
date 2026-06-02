# Aztec Cellular Automaton

import pygame
import numpy as np
import sys

WIDTH, HEIGHT = 320, 240
SCALE = 2
FPS = 60

STATES = 8

def generate_initial_grid():
    grid = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
    random_cells = np.random.rand(HEIGHT, WIDTH)
    grid[random_cells > 0.88] = 1
    return grid

def count_alive_neighbors(grid):
    alive = (grid == 1).astype(np.uint8)
    neighbors = sum(
        np.roll(np.roll(alive, dy, axis=0), dx, axis=1)
        for dy in (-1, 0, 1)
        for dx in (-1, 0, 1)
        if not (dx == 0 and dy == 0)
    )
    return neighbors

grid = generate_initial_grid()

pygame.init()
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("Aztec Cellular Automaton")
clock = pygame.time.Clock()

running = True
paused = False
generation = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                grid = generate_initial_grid()
                generation = 0

    if not paused:
        neighbors = count_alive_neighbors(grid)
        new_grid = np.zeros_like(grid)

        birth = (grid == 0) & ((neighbors == 2) | (neighbors == 3) | (neighbors == 1))
        new_grid[birth] = 1

        dying = (grid == 1)
        new_grid[dying] = 2

        fading = (grid >= 2) & (grid < STATES - 1)
        new_grid[fading] = grid[fading] + 1

        grid = new_grid
        generation += 1

    surface_array = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    surface_array[grid == 1] = [255, 230, 160]

    for i in range(2, STATES):
        fade = (STATES - i) / STATES
        r = int(200 * fade + 80)
        g = int(60 * fade + 10)
        b = int(180 * fade + 40)
        surface_array[grid == i] = [r, g, b]

    surface_array = np.repeat(np.repeat(surface_array, SCALE, axis=0), SCALE, axis=1)

    surface = pygame.surfarray.make_surface(np.transpose(surface_array, (1, 0, 2)))
    screen.blit(surface, (0, 0))

    pygame.display.set_caption(f"Aztec CA - Gen: {generation} {'[PAUSED]' if paused else ''}")
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()