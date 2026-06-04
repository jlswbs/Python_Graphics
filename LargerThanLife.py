# Larger Than Life Cellular Automaton

import pygame
import numpy as np
import sys

WIDTH, HEIGHT = 320, 240
SCALE = 2
FPS = 60

RADIUS = 5
STATES = 32

def generate_initial_grid():
    grid = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
    rnd = np.random.rand(HEIGHT, WIDTH)
    grid[rnd > 0.8] = 1
    return grid

def count_neighbors(grid):
    active = (grid == 1).astype(np.uint8)

    neighbors = np.zeros_like(active, dtype=np.uint16)

    for dy in range(-RADIUS, RADIUS + 1):
        for dx in range(-RADIUS, RADIUS + 1):
            if dx == 0 and dy == 0:
                continue

            neighbors += np.roll(
                np.roll(active, dy, axis=0),
                dx,
                axis=1
            )

    return neighbors

grid = generate_initial_grid()

pygame.init()
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("Larger Than Life CA")
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
        neighbors = count_neighbors(grid)

        new_grid = np.zeros_like(grid)

        birth = (grid == 0) & (neighbors >= 10) & (neighbors <= 12)
        new_grid[birth] = 1

        active = (grid == 1)
        new_grid[active] = 2

        fading = (grid >= 2) & (grid < STATES - 1)
        new_grid[fading] = grid[fading] + 1

        grid = new_grid
        generation += 1

    surface_array = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    surface_array[grid == 1] = [255, 255, 255]

    fading = (grid >= 2)

    if np.any(fading):
        t = (grid[fading] - 2) / (STATES - 2)

        surface_array[fading, 0] = (50 * (1 - t)).astype(np.uint8)
        surface_array[fading, 1] = (255 * (1 - t)).astype(np.uint8)
        surface_array[fading, 2] = (255 * (1 - t)).astype(np.uint8)

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
        f"Larger Than Life CA - Gen: {generation} {'[PAUSED]' if paused else ''}"
    )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()