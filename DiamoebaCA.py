# Diamoeba Cellular Automaton

import pygame
import numpy as np
import sys

WIDTH, HEIGHT = 320, 240
SCALE = 2
FPS = 60

def generate_initial_grid():
    grid = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
    random_cells = np.random.rand(HEIGHT, WIDTH)
    grid[random_cells > 0.55] = 1
    return grid

def count_alive_neighbors(grid):
    neighbors = sum(
        np.roll(np.roll(grid, dy, axis=0), dx, axis=1)
        for dy in (-1, 0, 1)
        for dx in (-1, 0, 1)
        if not (dx == 0 and dy == 0)
    )
    return neighbors

grid = generate_initial_grid()

pygame.init()
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("Diamoeba Cellular Automaton")
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

        birth = (grid == 0) & (
            (neighbors == 3) |
            (neighbors == 5) |
            (neighbors == 6) |
            (neighbors == 7) |
            (neighbors == 8)
        )

        survive = (grid == 1) & (
            (neighbors == 5) |
            (neighbors == 6) |
            (neighbors == 7) |
            (neighbors == 8)
        )

        new_grid = np.zeros_like(grid)
        new_grid[birth | survive] = 1

        grid = new_grid
        generation += 1

    surface_array = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    surface_array[grid == 1] = [120, 255, 120]
    surface_array[grid == 0] = [5, 10, 15]

    surface_array = np.repeat(
        np.repeat(surface_array, SCALE, axis=0),
        SCALE,
        axis=1
    )

    surface = pygame.surfarray.make_surface(
        np.transpose(surface_array, (1, 0, 2))
    )

    screen.blit(surface, (0, 0))

    pygame.display.set_caption(
        f"Diamoeba CA - Gen: {generation} {'[PAUSED]' if paused else ''}"
    )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()