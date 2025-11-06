# 2D Barkley reaction-diffusion model

import numpy as np
import pygame
import random

width, height = 640, 480
Du, Dv = 1.360, 0.435
a, b = 1.145, 0.061
epsilon = 0.05
dt = 0.208
steps_per_frame = 1

U = np.zeros((height, width), dtype=np.float32)
V = np.zeros((height, width), dtype=np.float32)

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def laplacian(Z):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z)

U[:] = 0.0
V[:] = 0.0

num_clusters = random.randint(10, 18)
for _ in range(num_clusters):
    x = random.randint(20, width - 20)
    y = random.randint(20, height - 20)
    radius = random.randint(5, 12)
    yy, xx = np.ogrid[-y:height-y, -x:width-x]
    mask = xx*xx + yy*yy <= radius*radius
    U[mask] = 1.0

V += 0.008 * np.random.rand(height, width)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for _ in range(steps_per_frame):
        Lu = laplacian(U)
        Lv = laplacian(V)

        term = U * (1 - U) * (U - (V + b)/a)
        U += dt * (Du * Lu + term / epsilon)
        V += dt * (Dv * Lv + U - V)

        U = np.clip(U, 0, 1)
        V = np.clip(V, 0, 1)

    img = (255 * U).astype(np.uint8)
    img_transposed = img.T
    rgb_array = np.stack([img_transposed, img_transposed, img_transposed], axis=-1)

    pixels = pygame.surfarray.pixels3d(screen)
    pixels[:] = rgb_array
    del pixels

    pygame.display.flip()
    clock.tick(60)

pygame.quit()