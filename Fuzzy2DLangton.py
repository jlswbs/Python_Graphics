# 2D fuzzy langton ant CA

import numpy as np
import pygame

WIDTH, HEIGHT = 320, 240
FPS = 60

TURN_GAIN = np.pi/8
FLIP_ALPHA = 0.499

DRAW_INTERVAL = 100

grid = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

x, y = WIDTH // 2, HEIGHT // 2
angle = np.random.uniform(0, 2*np.pi)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

iteration = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    val = grid[y, x]
    angle += (val - 0.5) * 2 * TURN_GAIN
    grid[y, x] = FLIP_ALPHA * val + (1 - FLIP_ALPHA) * (1 - val)

    dx, dy = int(round(np.cos(angle))), int(round(np.sin(angle)))
    x = (x + dx) % WIDTH
    y = (y + dy) % HEIGHT

    iteration += 1

    if iteration % DRAW_INTERVAL == 0:
        screen.fill((0, 0, 0))
        trail = (grid * 255).astype(np.uint8)
        img = np.stack([trail, trail, trail], axis=-1)
        img = np.transpose(img, (1, 0, 2))
        surf = pygame.surfarray.make_surface(img)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

pygame.quit()