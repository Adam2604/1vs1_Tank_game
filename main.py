import pygame
import sys
from noise import pnoise1

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Parametry terenu - funkcje wzięte z dokumentacji, dobrane samemu
terrain_width = 800
terrain_height = 600
step = 2
scale = 100.0
octaves = 4
persistence = 0.5
lacunarity = 2.0
base = 0

def generate_terrain():
    points = []
    for x in range(0, terrain_width, step):
        y = pnoise1(x / 100.0) * 100 + 400
        points.append((x, y))
    return points

def draw_terrain(points):
    polygon = points.copy()
    polygon.append((terrain_width, terrain_height))
    polygon.append((0, terrain_height))
    pygame.draw.polygon(screen, (34, 139, 34), polygon)

terrain_points = generate_terrain()

while True:
    screen.fill((135, 206, 235))  # niebo
    draw_terrain(terrain_points)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
