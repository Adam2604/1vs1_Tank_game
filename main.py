import pygame
import sys
from noise import pnoise1
from button import Button
from tanks import Tank

pygame.init()
screen_height = 720
screen_width = 1280
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)
sky = pygame.transform.scale(pygame.image.load("materialy_graficzne/background1.png"), (1280, 1280))
cloud1 = pygame.image.load("materialy_graficzne/cloud1.png")
cloud2 = pygame.image.load("materialy_graficzne/cloud2.png")
cloud3 = pygame.transform.scale(pygame.image.load("materialy_graficzne/cloud8.png"), (450, 225))
cloud4 = pygame.transform.scale(pygame.image.load("materialy_graficzne/cloud4.png"), (400, 200))
cloud5 = pygame.transform.scale(pygame.image.load("materialy_graficzne/cloud5.png"), (200, 100))
tank1 = Tank("Desert")

def get_font(size):
    return pygame.font.Font("materialy_graficzne/font.ttf", size)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    rect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, rect)

def main_menu():
    pygame.display.set_caption("TANKS")
    while True:
        screen.fill((30, 30, 30))
        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("Menu główne", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))
        screen.blit(menu_text, menu_rect)

        play_button = Button(
            image=pygame.image.load("materialy_graficzne/Play Rect.png"),
            position=(640, 300),
            label="PLAY",
            font=get_font(75),
            normal_color="#d7fcd4",
            hover_color="White"
        )

        quit_button = Button(
            image=pygame.image.load("materialy_graficzne/Quit Rect.png"),
            position=(640, 500),
            label="QUIT",
            font=get_font(75),
            normal_color="#d7fcd4",
            hover_color="White"
        )

        for button in [play_button, quit_button]:
            button.update_color(menu_mouse_pos)
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(menu_mouse_pos):
                    game_loop()
                if quit_button.is_clicked(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()



# Parametry terenu - funkcje wzięte z dokumentacji, dobrane samemu
terrain_width = 1281
terrain_height = 720
step = 1
scale = 100.0
octaves = 4
persistence = 0.1
lacunarity = 2.0
base = 0

def generate_terrain():
    points = []
    for x in range(0, terrain_width, step):
        y = pnoise1(x / 150.0) * 80 + 500
        points.append((x, int(y)))

    points.append((terrain_width, screen_height))
    points.append((0, screen_height))
    return points

def draw_terrain(screen):
    points = generate_terrain()
    points.append((terrain_width, screen_height))  # domykanie od prawej
    points.append((0, screen_height))              # domykanie od lewej
    pygame.draw.polygon(screen, (18 ,182 ,83), points)  # kolor ziemi

    for i in range(len(points) - 5):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        pygame.draw.line(screen, (100, 200, 100), (x1, y1), (x2, y2), 10)


terrain_points = generate_terrain()

def game_loop():
    terrain_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

    starting_x = 100
    terrain_y = 0
    for i in range(len(terrain_points) - 1):
        x1, y1 = terrain_points[i]
        if x1 <= starting_x <= terrain_points[i + 1][0]:
            terrain_y= y1
            break

    tank1.set_position(starting_x, terrain_y - tank1.total_height)

    while True:
        terrain_surface.fill((0, 0, 0, 0))

        screen.blit(sky, (0,0))
        screen.blit(cloud1, (1000, 50))
        screen.blit(cloud2, (500, 200))
        screen.blit(cloud5, (1, 5))
        screen.blit(cloud4, (125, 175))
        screen.blit(cloud3, (800, 190))

        draw_terrain(terrain_surface)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            tank1.move(-1, terrain_surface, terrain_points)
        if keys[pygame.K_d]:
            tank1.move(1, terrain_surface, terrain_points)

        tank1.apply_gravity(terrain_surface, terrain_points)

        draw_terrain(screen)
        tank1.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

main_menu()