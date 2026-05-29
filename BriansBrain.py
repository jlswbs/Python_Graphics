# Brian's Brain Cellular Automaton

import pygame
import numpy as np
import sys

WIDTH, HEIGHT = 320, 240
SCALE = 2
FPS = 60

OFF = 0
ON = 1
DYING = 2

def generate_initial_grid():
    grid = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)

    random_cells = np.random.rand(HEIGHT, WIDTH)

    grid[random_cells > 0.90] = ON

    return grid

def count_on_neighbors(grid):
    on_cells = (grid == ON).astype(np.uint8)

    neighbors = sum(
        np.roll(np.roll(on_cells, dy, axis=0), dx, axis=1)
        for dy in (-1, 0, 1)
        for dx in (-1, 0, 1)
        if not (dx == 0 and dy == 0)
    )

    return neighbors

grid = generate_initial_grid()

pygame.init()

screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("Brian's Brain")

clock = pygame.time.Clock()

running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

            elif event.key == pygame.K_r:
                grid = generate_initial_grid()

    if not paused:
        neighbors = count_on_neighbors(grid)

        new_grid = np.zeros_like(grid)

        birth = (grid == OFF) & (neighbors == 2)

        new_grid[birth] = ON
        new_grid[grid == ON] = DYING
        new_grid[grid == DYING] = OFF

        grid = new_grid

    surface_array = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    surface_array[grid == ON] = [255, 255, 255]
    surface_array[grid == DYING] = [80, 80, 80]

    surface_array = np.repeat(
        np.repeat(surface_array, SCALE, axis=0),
        SCALE,
        axis=1
    )

    surface = pygame.surfarray.make_surface(
        np.transpose(surface_array, (1, 0, 2))
    )

    screen.blit(surface, (0, 0))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()