# Hybrid Continuous Cellular Automaton

import pygame
import numpy as np
import sys

WIDTH, HEIGHT = 320, 240
SCALE = 2
FPS = 60

STATES = 7

def generate_initial_grid():
    grid = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
    random_cells = np.random.rand(HEIGHT, WIDTH)
    grid[random_cells > 0.88] = 1
    return grid

def count_weighted_neighbors(grid):
    h, w = grid.shape
    weighted = np.zeros((h, w), dtype=np.float32)

    weighted[grid == 1] = 1.0
    weighted[grid == 2] = 0.09
    weighted[grid == 3] = 0.07
    weighted[grid == 4] = 0.05
    weighted[grid == 5] = 0.03
    weighted[grid == 6] = 0.01

    neighbors = np.zeros((h, w), dtype=np.float32)

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            neighbors += np.roll(np.roll(weighted, dy, axis=0), dx, axis=1)

    return neighbors

grid = generate_initial_grid()

pygame.init()
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("Hybrid Continuous Cellular Automaton")
clock = pygame.time.Clock()

running = True
paused = False
generation = 0

COLORS = {
    0: [0, 0, 0],
    1: [140, 255, 120],
    2: [0, 255, 180],
    3: [0, 180, 255],
    4: [120, 80, 255],
    5: [220, 60, 255],
    6: [40, 10, 60],
}

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

        neighbors = count_weighted_neighbors(grid)

        new_grid = np.zeros_like(grid)

        birth = (grid == 0) & (neighbors >= 1.8) & (neighbors <= 2.8)
        new_grid[birth] = 1

        survive = (grid == 1) & (neighbors >= 2.8) & (neighbors <= 5.8)
        new_grid[survive] = 1

        dying = (grid == 1) & ~survive
        new_grid[dying] = 2

        fading = (grid >= 2) & (grid < STATES - 1)
        new_grid[fading] = grid[fading] + 1

        reverberate = (
            (grid >= 3)
            & (grid <= 5)
            & (neighbors >= 2.2)
            & (neighbors <= 2.8)
        )
        new_grid[reverberate] = 1

        grid = new_grid
        generation += 1

    surface_array = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    for state, color in COLORS.items():
        surface_array[grid == state] = color

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
        f"Hybrid CCA - Gen: {generation} "
        f"{'[PAUSED]' if paused else ''}"
    )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()