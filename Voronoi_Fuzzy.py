# Voronoi diagram simulation fuzzy logic color cells

import pygame, random
import numpy as np

WIDTH, HEIGHT = 320, 240
NUM_SITES = 16

SIGMA = 30.0
RULE_OFFSET = 0.05
RULE_SCALE  = 0.95
COLOR_GAIN  = 1.9

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

sites = []
colors = []
for _ in range(NUM_SITES):
    x = random.randint(0, WIDTH-1)
    y = random.randint(0, HEIGHT-1)
    dx = random.choice([-1,1])
    dy = random.choice([-1,1])
    sites.append([x,y,dx,dy])
    colors.append(np.array([random.randint(50,255),random.randint(50,255),random.randint(50,255)], dtype=np.float32))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for s in sites:
        s[0] += s[2]; s[1] += s[3]
        if s[0] < 0 or s[0] >= WIDTH: s[2]*=-1
        if s[1] < 0 or s[1] >= HEIGHT: s[3]*=-1

    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    weightsum = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

    for i,(sx,sy,_,_) in enumerate(sites):
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
    img = np.clip(img, 0, 255).astype(np.uint8)

    surf = pygame.surfarray.make_surface(np.transpose(img,(1,0,2)))
    screen.blit(surf,(0,0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()