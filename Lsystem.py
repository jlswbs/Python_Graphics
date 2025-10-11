import pygame
import numpy as np
import math

# Nastavení displeje
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamický L-systém")

# Parametry L-systému
axiom = "X"
rules = {"X": "F[+X][-X]FX", "F": "FF"}
iterations = 7
length = 2.0
base_angle = 25.0

# Generování L-systému
def generate_lsystem():
    current = axiom
    for _ in range(iterations):
        next_gen = ""
        for char in current:
            next_gen += rules.get(char, char)
        current = next_gen
    return current

# Vykreslení L-systému do frame bufferu
def draw_lsystem(surface, lsystem, dynamic_angle):
    x, y = WIDTH / 2, HEIGHT - 50
    angle = -90
    stack = []
    surface.fill((0, 0, 0))  # Černé pozadí

    for char in lsystem:
        if char == 'F':
            rad = math.radians(angle)
            new_x = x + length * math.cos(rad)
            new_y = y + length * math.sin(rad)
            pygame.draw.line(surface, (255, 255, 255), (int(x), int(y)), (int(new_x), int(new_y)), 1)
            x, y = new_x, new_y
        elif char == '+':
            angle += dynamic_angle
        elif char == '-':
            angle -= dynamic_angle
        elif char == '[':
            stack.append((x, y, angle))
        elif char == ']':
            x, y, angle = stack.pop()

# Hlavní smyčka
def main():
    lsystem = generate_lsystem()
    clock = pygame.time.Clock()
    running = True
    start_time = pygame.time.get_ticks() / 1000.0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dynamický úhel podle času
        t = pygame.time.get_ticks() / 1000.0 - start_time
        dynamic_angle = base_angle + 10 * math.sin(t)

        # Vykreslení
        draw_lsystem(screen, lsystem, dynamic_angle)
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()