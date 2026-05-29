# SmoothLife Cellular Automaton Simulation

import pygame
import numpy as np
from scipy.fft import fft2, ifft2
import sys

WIDTH, HEIGHT = 320, 240
SCALE = 1
FPS = 60

R_INNER = 3.0
R_OUTER = 9.0

B1, B2 = 0.278, 0.365
S1, S2 = 0.267, 0.445
SIGMA_1 = 0.028
SIGMA_2 = 0.015

def sigma_1(x, a, alpha):
    return 1.0 / (1.0 + np.exp(-4.0 * (x - a) / alpha))

def sigma_2(x, a, b, alpha):
    return sigma_1(x, a, alpha) * (1.0 - sigma_1(x, b, alpha))

def transition_func(m, n):
    s_val = sigma_2(n, S1, S2, SIGMA_2)
    b_val = sigma_2(n, B1, B2, SIGMA_2)
    s_m = sigma_1(m, 0.5, SIGMA_1)
    return s_m * s_val + (1.0 - s_m) * b_val

y, x = np.ogrid[-HEIGHT//2:HEIGHT//2, -WIDTH//2:WIDTH//2]
dist = np.sqrt(x**2 + y**2)

mask_M = dist < R_INNER
mask_N = (dist >= R_INNER) & (dist <= R_OUTER)

mask_M = mask_M / np.sum(mask_M)
mask_N = mask_N / np.sum(mask_N)

mask_M = np.fft.ifftshift(mask_M)
mask_N = np.fft.ifftshift(mask_N)

FFT_M = fft2(mask_M)
FFT_N = fft2(mask_N)

def generate_initial_grid():
    raw_grid = np.random.rand(HEIGHT, WIDTH)

    init_blur = np.fft.ifftshift(dist < R_OUTER)
    init_blur = init_blur / np.sum(init_blur)

    blurred = np.real(ifft2(fft2(raw_grid) * fft2(init_blur)))

    normalized = (blurred - blurred.min()) / (blurred.max() - blurred.min())
    return normalized

grid = generate_initial_grid()

pygame.init()

screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("SmoothLife")

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
        grid_fft = fft2(grid)

        M = np.real(ifft2(grid_fft * FFT_M))
        N = np.real(ifft2(grid_fft * FFT_N))

        dt = 1.0

        grid_target = transition_func(M, N)

        grid = grid + dt * (grid_target - grid)
        grid = np.clip(grid, 0.0, 1.0)

    view_grid = (grid * 255).astype(np.uint8)

    surface_array = np.stack(
        [view_grid, view_grid, view_grid],
        axis=-1
    )

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
