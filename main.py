import pygame
import sys
from noise import pnoise1
from button import Button
from tanks import Tank

pygame.init()
screen_height = 864
screen_width = 1546
window_size = (screen_width, screen_height)
is_fullscreen = False
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

# grafiki nieba oraz chmur zostały pobrane ze strony https://szadiart.itch.io/background-desert-mountains
sky = pygame.transform.scale(pygame.image.load("materialy_graficzne/background1.png"), (1536, 1536))
cloud1 = pygame.image.load("materialy_graficzne/cloud1.png")
cloud2 = pygame.image.load("materialy_graficzne/cloud2.png")
cloud3 = pygame.transform.scale(pygame.image.load("materialy_graficzne/cloud8.png"), (450, 225))
cloud4 = pygame.transform.scale(pygame.image.load("materialy_graficzne/cloud4.png"), (400, 200))
cloud5 = pygame.transform.scale(pygame.image.load("materialy_graficzne/cloud5.png"), (200, 100))
tank1 = Tank("Desert1")


def get_font(size):
    return pygame.font.Font("materialy_graficzne/font.ttf", size)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    rect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, rect)


def fullscreen():
    global screen, is_fullscreen
    is_fullscreen = not is_fullscreen
    if is_fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(window_size)


def main_menu():
    pygame.display.set_caption("TANKS")
    while True:
        screen.fill((30, 30, 30))
        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("Main Menu", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(768, 150))
        screen.blit(menu_text, menu_rect)

        play_button = Button(
            image=pygame.image.load("materialy_graficzne/Play Rect.png"),
            position=(768, 350),
            label="PLAY",
            font=get_font(75),
            normal_color="#d7fcd4",
            hover_color="White"
        )

        quit_button = Button(
            image=pygame.image.load("materialy_graficzne/Quit Rect.png"),
            position=(768, 550),
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(menu_mouse_pos):
                    map_selection()
                if quit_button.is_clicked(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def pause_menu():
    pygame.display.set_caption("TANKS - PAUSE")
    while True:
        screen.fill((30, 30, 30))
        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("PAUSE", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(768, 150))  # Zmienione z 960 na 768
        screen.blit(menu_text, menu_rect)

        resume_button = Button(
            image=pygame.transform.scale(pygame.image.load("materialy_graficzne/Play Rect.png"), (500, 120)),
            position=(768, 350),  # Zmienione z 960 na 768 i z 450 na 350
            label="RESUME",
            font=get_font(75),
            normal_color="#d7fcd4",
            hover_color="White"
        )

        quit_button = Button(
            image=pygame.image.load("materialy_graficzne/Quit Rect.png"),
            position=(768, 550),  # Zmienione z 960 na 768 i z 650 na 550
            label="QUIT",
            font=get_font(75),
            normal_color="#d7fcd4",
            hover_color="White"
        )

        resume_button.update_color(menu_mouse_pos)
        resume_button.draw(screen)
        quit_button.update_color(menu_mouse_pos)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    fullscreen()
                if event.key == pygame.K_ESCAPE:
                    return  # Powrót do gry
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.is_clicked(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
                if resume_button.is_clicked(menu_mouse_pos):
                    return

        pygame.display.update()


terrain_width = 1537
terrain_height = 720
step = 1
scale = 100.0
octaves = 4
persistence = 0.1
lacunarity = 2.0
base = 0


def generate_terrain(map_type="hilly"):
    points = []
    if map_type == "flat":
        base_height = 600
        for x in range(0, terrain_width, step):
            y = base_height
            points.append((x, int(y)))
    else:  # hilly
        for x in range(0, terrain_width, step):
            y = pnoise1(x / 150.0) * 80 + 500
            points.append((x, int(y)))

    points.append((terrain_width, screen_height))
    points.append((0, screen_height))
    return points


def draw_terrain(screen, map_type="hilly"):
    points = generate_terrain(map_type)
    points.append((terrain_width, screen_height))
    points.append((0, screen_height))
    pygame.draw.polygon(screen, (18, 182, 83), points)  # kolor ziemi

    for i in range(len(points) - 5):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        pygame.draw.line(screen, (100, 200, 100), (x1, y1), (x2, y2), 10)
    
    return points


terrain_points = generate_terrain()


def game_loop(map_type="hilly"):
    global terrain_points
    terrain_points = generate_terrain(map_type)
    terrain_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

    starting_x = 100
    terrain_y = 0
    for i in range(len(terrain_points) - 1):
        x1, y1 = terrain_points[i]
        if x1 <= starting_x <= terrain_points[i + 1][0]:
            terrain_y = y1
            break

    tank1.set_position(starting_x, terrain_y - tank1.total_height)

    while True:
        terrain_surface.fill((0, 0, 0, 0))

        screen.blit(sky, (0, 0))
        # Aktualizacja pozycji chmur
        screen.blit(cloud1, (1200, 50))
        screen.blit(cloud2, (600, 200))
        screen.blit(cloud5, (50, 50))
        screen.blit(cloud4, (250, 175))
        screen.blit(cloud3, (900, 190))

        draw_terrain(terrain_surface, map_type)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            tank1.move(-1, terrain_surface, terrain_points)
        if keys[pygame.K_d]:
            tank1.move(1, terrain_surface, terrain_points)

        tank1.apply_gravity(terrain_surface, terrain_points)

        draw_terrain(screen, map_type)
        tank1.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.K_F11:
                fullscreen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()

        pygame.display.update()
        clock.tick(60)


def map_selection():
    pygame.display.set_caption("TANKS - WYBÓR MAPY")
    while True:
        screen.fill((30, 30, 30))
        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("Wybierz Mapę", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(768, 150))
        screen.blit(menu_text, menu_rect)

        map1_button = Button(
            image=pygame.image.load("materialy_graficzne/Play Rect.png"),
            position=(768, 300),
            label="Mapa Pagórkowata",
            font=get_font(75),
            normal_color="#d7fcd4",
            hover_color="White"
        )

        map2_button = Button(
            image=pygame.image.load("materialy_graficzne/Play Rect.png"),
            position=(768, 450),
            label="Mapa Płaska",
            font=get_font(75),
            normal_color="#d7fcd4",
            hover_color="White"
        )

        back_button = Button(
            image=pygame.image.load("materialy_graficzne/Quit Rect.png"),
            position=(768, 600),
            label="POWRÓT",
            font=get_font(75),
            normal_color="#d7fcd4",
            hover_color="White"
        )

        for button in [map1_button, map2_button, back_button]:
            button.update_color(menu_mouse_pos)
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if map1_button.is_clicked(menu_mouse_pos):
                    game_loop(map_type="hilly")
                if map2_button.is_clicked(menu_mouse_pos):
                    game_loop(map_type="flat")
                if back_button.is_clicked(menu_mouse_pos):
                    main_menu()

        pygame.display.update()


main_menu()