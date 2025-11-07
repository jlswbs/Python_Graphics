# Gray-Scott reaction-diffusion model

import numpy as np
import pygame

Du = 0.18
Dv = 0.09
f  = 0.04
k  = 0.06

width, height = 640, 480
steps_per_frame = 8

U = np.ones((height, width), dtype=np.float32)
V = np.zeros((height, width), dtype=np.float32)

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def laplacian(Z):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z)

U[:] = 1.0
V[:] = 0.0

for _ in range(10):
    x = np.random.randint(30, width - 30)
    y = np.random.randint(30, height - 30)
    radius = np.random.randint(5, 14)
    yy, xx = np.ogrid[-y:height-y, -x:width-x]
    mask = xx*xx + yy*yy <= radius*radius
    V[mask] = 1.0
    U[mask] = 0.5

U += 0.02 * np.random.rand(height, width)
V += 0.02 * np.random.rand(height, width)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for _ in range(steps_per_frame):
        Lu = laplacian(U)
        Lv = laplacian(V)
        uv2 = U * V * V
        U += Du * Lu - uv2 + f * (1 - U)
        V += Dv * Lv + uv2 - (f + k) * V
        U = np.clip(U, 0, 1)
        V = np.clip(V, 0, 1)

    img = (255 * V).astype(np.uint8)
    img_transposed = img.T
    rgb_array = np.stack([img_transposed, img_transposed, img_transposed], axis=-1)
    pixels = pygame.surfarray.pixels3d(screen)
    pixels[:] = rgb_array
    del pixels

    pygame.display.flip()
    clock.tick(60)

pygame.quit()