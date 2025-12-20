# 2D Sandpile like CA

import pygame
import random
import numpy as np

WIDTH = 160
HEIGHT = 120

pygame.init()
CELL_SIZE = 2
screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
clock = pygame.time.Clock()

grid = np.zeros((HEIGHT, WIDTH), dtype=np.int32)
threshold = random.randint(3, 8)

def rndrule():
    global threshold
    threshold = random.randint(3, 8)
    grid[:, :] = np.random.randint(0, threshold * 4, size=(HEIGHT, WIDTH))

def step():
    global grid
    new_grid = np.copy(grid)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y, x] >= threshold:
                share = grid[y, x] // 4
                new_grid[y, x] -= share * 4
                if share > 0:
                    new_grid[(y - 1) % HEIGHT, x] += share
                    new_grid[(y + 1) % HEIGHT, x] += share
                    new_grid[y, (x - 1) % WIDTH] += share
                    new_grid[y, (x + 1) % WIDTH] += share
    grid = new_grid

def draw():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            val = grid[y, x]
            if val == 0:
                color = (0, 0, 0)
            elif val < threshold:
                color = (255, 255, 255)
            elif val < threshold * 2:
                color = (255, 255, 0)
            elif val < threshold * 3:
                color = (255, 0, 0)
            else:
                color = (0, 0, 255)
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    rndrule()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    rndrule()
                elif event.key == pygame.K_ESCAPE:
                    running = False
        step()
        draw()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()