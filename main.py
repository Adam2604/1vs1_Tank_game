import pygame
import sys
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
tank2 = Tank("Navy1", True)
block_size   = 32 # rozmiar jednego kwadratu na mapie
terrain_cols = screen_width  // block_size
terrain_rows = screen_height // block_size

MAX_FUEL = 100  # maksymalna ilość "paliwa" (w pikselach)
current_player = 1  
fuel_remaining = MAX_FUEL  
fuel_remaining_p2 = MAX_FUEL



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
        menu_rect = menu_text.get_rect(center=(768, 150))
        screen.blit(menu_text, menu_rect)

        resume_button = Button(
            image=pygame.transform.scale(pygame.image.load("materialy_graficzne/Play Rect.png"), (500, 120)),
            position=(768, 350),
            label="RESUME",
            font=get_font(75),
            normal_color="#d7fcd4",
            hover_color="White"
        )

        return_to_menu_button = Button(
            image=pygame.transform.scale(pygame.image.load("materialy_graficzne/Quit Rect.png"), (1100, 110)),
            position=(768, 550),
            label="RETURN TO MENU",
            font=get_font(75),
            normal_color="#d7fcd4",
            hover_color="White"
        )

        quit_button = Button(
            image=pygame.image.load("materialy_graficzne/Quit Rect.png"),
            position=(768, 750),
            label="QUIT",
            font=get_font(75),
            normal_color="#d7fcd4",
            hover_color="White"
        )

        resume_button.update_color(menu_mouse_pos)
        resume_button.draw(screen)
        return_to_menu_button.update_color(menu_mouse_pos)
        return_to_menu_button.draw(screen)
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
                if return_to_menu_button.is_clicked(menu_mouse_pos):
                    main_menu()

        pygame.display.update()


terrain_width = 1537
terrain_height = 720
step = 1
scale = 100.0
octaves = 4
persistence = 0.1
lacunarity = 2.0
base = 0


def generate_terrain(map_type="flat"):
    grid = [[0]*terrain_cols for _ in range(terrain_rows)]

    if map_type == "flat":
        base_row = terrain_rows * 3 // 4
        for r in range(base_row, terrain_rows):
            for c in range(terrain_cols):
                grid[r][c] = 1
    else:
        import random
        for c in range(terrain_cols):
            hill_top = random.randint(terrain_rows//3, terrain_rows//2)
            for r in range(hill_top, terrain_rows):
                grid[r][c] = 1

    return grid



def draw_terrain(surface, terrain_grid):
    for r, row in enumerate(terrain_grid):
        for c, cell in enumerate(row):
            if cell:
                x = c * block_size
                y = r * block_size
                rect = pygame.Rect(x, y, block_size, block_size)
                pygame.draw.rect(surface, (18,182,83), rect)    # wypełnienie
                pygame.draw.rect(surface, (10,100,50), rect, 2) # obrys

    for c in range(terrain_cols):
        for r in range(terrain_rows):
            if terrain_grid[r][c]:
                x = c * block_size
                y = r * block_size
                pygame.draw.rect(surface, (100,200,100), (x, y, block_size, 4))
                break




terrain_points = generate_terrain()

def map_selection():
    pygame.display.set_caption("TANKS - WYBÓR MAPY")
    while True:
        screen.fill((30, 30, 30))
        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("Choose Map", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(768, 150))
        screen.blit(menu_text, menu_rect)

        map1_button = Button(
            image=pygame.transform.scale(pygame.image.load("materialy_graficzne/Play Rect.png"), (450, 110)),
            position=(768, 350),
            label="HILLY",
            font=get_font(75),
            normal_color="#d7fcd4",
            hover_color="White"
        )

        map2_button = Button(
            image=pygame.image.load("materialy_graficzne/Play Rect.png"),
            position=(768, 550),
            label="FLAT",
            font=get_font(75),
            normal_color="#d7fcd4",
            hover_color="White"
        )

        back_button = Button(
            image=pygame.transform.scale(pygame.image.load("materialy_graficzne/Quit Rect.png"), (510, 110)),
            position=(768, 750),
            label="RETURN",
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

def game_loop(map_type="flat"):
    global current_player, fuel_remaining, fuel_remaining_p2
    terrain_grid = generate_terrain(map_type)
    terrain_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

    fuel_font = pygame.font.SysFont(None, 36)
    bar_width = 200
    bar_height = 20
    
    def find_height(x_pixel):
        col = x_pixel // block_size
        for r in range(terrain_rows):
            if terrain_grid[r][col]:
                return r * block_size
        return screen_height

    tank1.set_position(100, find_height(100) - tank1.total_height)
    tank2.set_position(screen_width-200, find_height(screen_width-200) - tank2.total_height)
    
    while True:
        # tło i chmury
        terrain_surface.fill((0,0,0,0))
        screen.blit(sky, (0,0))
        screen.blit(cloud1, (1200,50))
        screen.blit(cloud2, (600,200))
        screen.blit(cloud5, (50,50))
        screen.blit(cloud4, (250,175))
        screen.blit(cloud3, (900,190))

        draw_terrain(terrain_surface, terrain_grid)
        screen.blit(terrain_surface, (0,0))

        # Wyświetlanie informacji o turze i paliwie
        current_player_text = fuel_font.render(f"Tura: Gracz {current_player}", True, (255, 255, 255))
        screen.blit(current_player_text, (20, 20))
        
        # Wyświetlanie paliwa dla aktualnego gracza
        if current_player == 1:
            fuel_text = fuel_font.render(f"Paliwo: {int(fuel_remaining)}", True, (255, 255, 255))
            fuel_width = (fuel_remaining / MAX_FUEL) * bar_width
        else:
            fuel_text = fuel_font.render(f"Paliwo: {int(fuel_remaining_p2)}", True, (255, 255, 255))
            fuel_width = (fuel_remaining_p2 / MAX_FUEL) * bar_width
        
        screen.blit(fuel_text, (20, 50))
        
        # Pasek paliwa
        pygame.draw.rect(screen, (100, 100, 100), (20, 80, bar_width, bar_height))  # tło paska
        pygame.draw.rect(screen, (0, 255, 0), (20, 80, int(fuel_width), bar_height))  # pasek paliwa
        
        # Sterowanie czołgami
        keys = pygame.key.get_pressed()
        if current_player == 1:
            if fuel_remaining > 0:
                if keys[pygame.K_a]:
                    if tank1.move(-1, terrain_surface, terrain_grid):
                        fuel_remaining = max(0, fuel_remaining - 1)
                if keys[pygame.K_d]:
                    if tank1.move(1, terrain_surface, terrain_grid):
                        fuel_remaining = max(0, fuel_remaining - 1)
            tank1.update_turret_angle(pygame.mouse.get_pos())
        elif current_player == 2:
            if fuel_remaining_p2 > 0:
                if keys[pygame.K_a]:
                    if tank2.move(-1, terrain_surface, terrain_grid):
                        fuel_remaining_p2 = max(0, fuel_remaining_p2 - 1)
                if keys[pygame.K_d]:
                    if tank2.move(1, terrain_surface, terrain_grid):
                        fuel_remaining_p2 = max(0, fuel_remaining_p2 - 1)
            tank2.update_turret_angle(pygame.mouse.get_pos())

        tank1.apply_gravity(terrain_surface, terrain_grid)
        tank2.apply_gravity(terrain_surface, terrain_grid)

        was_shooting = current_player == 1 and tank1.shooting or current_player == 2 and tank2.shooting

        # Aktualizacja pocisków i sprawdzenie zakończenia strzału
        if current_player == 1:
            tank1.update_bullet(terrain_surface, tank2)
            if was_shooting and not tank1.shooting:
                current_player = 2
                fuel_remaining_p2 = MAX_FUEL
        else:
            tank2.update_bullet(terrain_surface, tank1)
            if was_shooting and not tank2.shooting:
                current_player = 1
                fuel_remaining = MAX_FUEL

        tank1.draw(screen)
        tank2.draw(screen)

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:  # Lewy przycisk myszy
                    if current_player == 1:
                        tank1.shoot()
                    else:
                        tank2.shoot()
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_F11:
                    fullscreen()
                if e.key == pygame.K_ESCAPE:
                    pause_menu()

        pygame.display.update()
        clock.tick(60)


main_menu()