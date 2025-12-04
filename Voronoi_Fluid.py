# Voronoi diagram simulation fluid fuzzy logic color cells

import pygame, random, math
import numpy as np

WIDTH, HEIGHT = 320, 240
NUM_SITES = 20

SIGMA = 35.0
RULE_OFFSET = 0.05
RULE_SCALE  = 0.95
COLOR_GAIN  = 2.5
TURN_GAIN   = 0.1
ALPHA       = 0.8

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

sites = []
colors = []
angles = []
for _ in range(NUM_SITES):
    x = random.randint(0, WIDTH-1)
    y = random.randint(0, HEIGHT-1)
    angle = random.uniform(0, 2*math.pi)
    sites.append([x,y])
    colors.append(np.array([random.randint(50,255),random.randint(50,255),random.randint(50,255)], dtype=np.float32))
    angles.append(angle)

grid = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    weightsum = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

    for i,(sx,sy) in enumerate(sites):
        dx = np.arange(WIDTH) - sx
        dy = np.arange(HEIGHT)[:,None] - sy
        d2 = dx*dx + dy*dy
        weight = np.exp(-d2 / (2*SIGMA*SIGMA))
        weight = RULE_OFFSET + RULE_SCALE * weight
        weightsum += weight
        img += weight[:,:,None] * colors[i]

    img /= weightsum[:,:,None]
    mean = img.mean(axis=2, keepdims=True)
    img = mean + COLOR_GAIN * (img - mean)

    grid = ALPHA * grid + (1-ALPHA) * img
    grid = np.clip(grid, 0, 255)

    for i,(sx,sy) in enumerate(sites):
        ix, iy = int(sx)%WIDTH, int(sy)%HEIGHT
        val = grid[iy, ix].mean()/255.0
        angles[i] += (val-0.5)*2*TURN_GAIN
        dx = math.cos(angles[i])
        dy = math.sin(angles[i])
        sx = (sx + dx) % WIDTH
        sy = (sy + dy) % HEIGHT
        sites[i][0], sites[i][1] = sx, sy

    surf = pygame.surfarray.make_surface(np.transpose(grid.astype(np.uint8),(1,0,2)))
    screen.blit(surf,(0,0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()