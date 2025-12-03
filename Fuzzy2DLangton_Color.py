# 2D fuzzy langton ant CA color

import numpy as np
import pygame
import random

WIDTH, HEIGHT = 320, 240
FPS = 60

TURN_GAIN = np.pi/8
FLIP_ALPHA = 0.5
DRAW_INTERVAL = 50
N = 6

grid = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
color_buffer = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

ants = []
for i in range(N):
    x = random.randint(0, WIDTH-1)
    y = random.randint(0, HEIGHT-1)
    angle = random.random() * 2*np.pi
    color = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
    ants.append({"x":x, "y":y, "angle":angle, "color":color})

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

iteration = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for ant in ants:
        x, y, angle = ant["x"], ant["y"], ant["angle"]
        val = grid[y, x]
        angle += (val - 0.5) * 2 * TURN_GAIN
        grid[y, x] = FLIP_ALPHA * val + (1 - FLIP_ALPHA) * (1 - val)
        dx, dy = int(round(np.cos(angle))), int(round(np.sin(angle)))
        x = (x + dx) % WIDTH
        y = (y + dy) % HEIGHT
        ant["x"], ant["y"], ant["angle"] = x, y, angle
        color_buffer[y, x] = ant["color"]

    iteration += 1

    if iteration % DRAW_INTERVAL == 0:
        img = np.transpose(color_buffer, (1, 0, 2))
        surf = pygame.surfarray.make_surface(img)
        screen.blit(surf, (0, 0))
        for ant in ants:
            pygame.draw.rect(screen, ant["color"], (ant["x"], ant["y"], 1, 1))
        pygame.display.update()
        clock.tick(FPS)

pygame.quit()