# 2D Barkley reaction-diffusion model - color

import numpy as np
import pygame
import random

width, height = 640, 480
Du, Dv = 1.360, 0.435
a, b = 1.145, 0.061
epsilon = 0.05
dt = 0.208
steps_per_frame = 8

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

def colorize(U, V):
    phase = (U - V + 1.0) * 0.5
    hue = (phase * 360) % 360
    saturation = np.clip(U * 2.0, 0.0, 1.0)
    value = np.clip(1.0 - V * 0.8, 0.3, 1.0)

    h = hue / 60.0
    i = np.floor(h).astype(int)
    f = h - i
    p = value * (1 - saturation)
    q = value * (1 - saturation * f)
    t = value * (1 - saturation * (1 - f))

    r = np.zeros_like(h)
    g = np.zeros_like(h)
    b = np.zeros_like(h)

    mask = i == 0
    r[mask], g[mask], b[mask] = value[mask], t[mask], p[mask]
    mask = i == 1
    r[mask], g[mask], b[mask] = q[mask], value[mask], p[mask]
    mask = i == 2
    r[mask], g[mask], b[mask] = p[mask], value[mask], t[mask]
    mask = i == 3
    r[mask], g[mask], b[mask] = p[mask], q[mask], value[mask]
    mask = i == 4
    r[mask], g[mask], b[mask] = t[mask], p[mask], value[mask]
    mask = i == 5
    r[mask], g[mask], b[mask] = value[mask], p[mask], q[mask]

    return np.stack([r, g, b], axis=-1)

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

    color_image = colorize(U, V)  # (height, width, 3)
    img = (255 * color_image).astype(np.uint8)
    img_transposed = img.transpose(1, 0, 2)  # (width, height, 3)

    pixels = pygame.surfarray.pixels3d(screen)
    pixels[:] = img_transposed
    del pixels

    pygame.display.flip()
    clock.tick(60)

pygame.quit()