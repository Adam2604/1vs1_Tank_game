import pygame
import sys
import random
from button import Button
from tanks import Tank

pygame.init()
screen_height = 864
screen_width = 1546
window_size = (screen_width, screen_height)
is_fullscreen = False
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

# grafiki nieba oraz chmur zostały pobrane ze strony https://szadiart.itch.io/background-desert-mountains
sky = pygame.transform.scale(pygame.image.load("materialy_graficzne/background1.png"), (1536, 1536))
cloud1 = pygame.image.load("materialy_graficzne/cloud1.png")
cloud2 = pygame.image.load("materialy_graficzne/cloud2.png")
cloud3 = pygame.transform.scale(pygame.image.load("materialy_graficzne/cloud8.png"), (450, 225))
cloud4 = pygame.transform.scale(pygame.image.load("materialy_graficzne/cloud4.png"), (400, 200))
cloud5 = pygame.transform.scale(pygame.image.load("materialy_graficzne/cloud5.png"), (200, 100))

tank1 = Tank("Desert1")
tank2 = Tank("Navy1", True)
block_size = 10  # rozmiar jednego kwadratu na mapie
terrain_cols = screen_width // block_size
terrain_rows = screen_height // block_size

MAX_FUEL = 100  # maksymalna ilość paliwa (w pikselach)
current_player = 1
fuel_remaining = MAX_FUEL
fuel_remaining_p2 = MAX_FUEL

def find_height(x_pixel, terrain_grid):
    col = x_pixel // block_size
    col = max(0, min(col, terrain_cols - 1))
    
    for r in range(terrain_rows):
        if terrain_grid[r][col]:
            return (r * block_size) - 5
    return screen_height

def get_font(size):
    return pygame.font.Font("materialy_graficzne/font.ttf", size)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    rect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, rect)

def generate_terrain(map_type="flat"):
    grid = [[0] * terrain_cols for _ in range(terrain_rows)]

    if map_type == "flat":
        base_row = terrain_rows * 3 // 4
        for r in range(base_row, terrain_rows):
            for c in range(terrain_cols):
                grid[r][c] = 1
    else:
        random.seed(20)
        base_height = terrain_rows * 3 // 4
        current_height = base_height
        max_height_change = 2
        change_frequency = 0.3
        max_deviation = 20
        
        heights = []
        for c in range(terrain_cols):
            if random.random() < change_frequency:
                height_change = random.randint(-max_height_change, max_height_change)
                current_height = min(base_height + max_deviation, 
                                   max(base_height - max_deviation, 
                                       current_height + height_change))
            heights.append(current_height)

        for c in range(terrain_cols):
            for r in range(heights[c], terrain_rows):
                grid[r][c] = 1
        random.seed()
    return grid

def draw_terrain(surface, terrain_grid):
    for r, row in enumerate(terrain_grid):
        for c, cell in enumerate(row):
            if cell:
                x = c * block_size
                y = r * block_size
                rect = pygame.Rect(x, y, block_size, block_size)
                pygame.draw.rect(surface, (18, 182, 83), rect)

    for c in range(terrain_cols):
        for r in range(terrain_rows):
            if terrain_grid[r][c]:
                x = c * block_size
                y = r * block_size
                pygame.draw.rect(surface, (100, 200, 100), (x, y, block_size, 4))
                break

def update_terrain(static_surface, terrain_grid, modified_area):
    x, y, width, height = modified_area
    explosion_radius = 60
    destroy_terrain(terrain_grid, (x + width//2, y + height//2), explosion_radius)

    margin = block_size * 4
    clear_area = (
        x - margin,
        y - margin,
        width + margin * 2,
        height + margin * 2
    )
    static_surface.fill((0, 0, 0, 0), clear_area)

    start_col = max(0, (x - margin) // block_size)
    end_col = min(terrain_cols, (x + width + margin) // block_size + 1)
    start_row = max(0, (y - margin) // block_size)
    end_row = min(terrain_rows, (y + height + margin) // block_size + 1)

    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if terrain_grid[r][c]:
                draw_x = c * block_size
                draw_y = r * block_size
                rect = pygame.Rect(draw_x, draw_y, block_size, block_size)
                pygame.draw.rect(static_surface, (18, 182, 83), rect)

def destroy_terrain(terrain_grid, impact_point, radius):
    impact_x, impact_y = impact_point
    destruction_radius = 3  # Liczba bloków do zniszczenia
    
    center_col = int(impact_x // block_size)
    center_row = int(impact_y // block_size)

    for row in range(center_row - destruction_radius, center_row + destruction_radius + 1):
        for col in range(center_col - destruction_radius, center_col + destruction_radius + 1):
            if 0 <= row < len(terrain_grid) and 0 <= col < len(terrain_grid[0]):
                dx = col - center_col
                dy = row - center_row
                distance = (dx * dx + dy * dy) ** 0.5

                if distance <= destruction_radius:
                    terrain_grid[row][col] = 0

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

def game_loop(map_type):
    global current_player, fuel_remaining, fuel_remaining_p2

    tank1.reset()
    tank2.reset()
    tank1.can_shoot = True
    tank2.can_shoot = True

    current_player = 1
    fuel_remaining = MAX_FUEL
    fuel_remaining_p2 = MAX_FUEL

    terrain_grid = generate_terrain(map_type)
    static_terrain_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    draw_terrain(static_terrain_surface, terrain_grid)

    # Pozycje początkowe czołgów
    tank1_x = 100
    tank2_x = screen_width - 200

    # Znajdowanie wysokości terenu dla czołgów
    def get_terrain_height(x):
        col = x // block_size
        col = max(0, min(col, terrain_cols - 1))
        for r in range(terrain_rows):
            if terrain_grid[r][col]:
                return (r * block_size) - 5
        return screen_height

    tank1_y = get_terrain_height(tank1_x)
    tank2_y = get_terrain_height(tank2_x)

    tank1.set_position(tank1_x, tank1_y - tank1.total_height)
    tank2.set_position(tank2_x, tank2_y - tank2.total_height)
    dynamic_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

    fuel_font = pygame.font.SysFont(None, 36)
    bar_width = 200
    bar_height = 20

    def find_height(x_pixel):
        col = x_pixel // block_size
        for r in range(terrain_rows):
            if terrain_grid[r][col]:
                return r * block_size
        return screen_height

    tank1.set_update_terrain_function(update_terrain)
    tank2.set_update_terrain_function(update_terrain)
    tank1.set_terrain_grid(terrain_grid)
    tank2.set_terrain_grid(terrain_grid)

    while True:
        dynamic_surface.fill((0, 0, 0, 0))

        screen.blit(sky, (0, 0))
        screen.blit(cloud1, (1200, 50))
        screen.blit(cloud2, (600, 200))
        screen.blit(cloud5, (50, 50))
        screen.blit(cloud4, (250, 175))
        screen.blit(cloud3, (900, 190))
        screen.blit(static_terrain_surface, (0, 0))


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
        pygame.draw.rect(screen, (100, 100, 100), (20, 80, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (20, 80, int(fuel_width), bar_height))

        # Sterowanie czołgami
        keys = pygame.key.get_pressed()
        if current_player == 1:
            if fuel_remaining > 0:
                if keys[pygame.K_a]:
                    if tank1.move(-1, static_terrain_surface, terrain_grid):
                        fuel_remaining = max(0, fuel_remaining - 1)
                if keys[pygame.K_d]:
                    if tank1.move(1, static_terrain_surface, terrain_grid):
                        fuel_remaining = max(0, fuel_remaining - 1)
            tank1.update_turret_angle(pygame.mouse.get_pos())
        elif current_player == 2:
            if fuel_remaining_p2 > 0:
                if keys[pygame.K_a]:
                    if tank2.move(-1, static_terrain_surface, terrain_grid):
                        fuel_remaining_p2 = max(0, fuel_remaining_p2 - 1)
                if keys[pygame.K_d]:
                    if tank2.move(1, static_terrain_surface, terrain_grid):
                        fuel_remaining_p2 = max(0, fuel_remaining_p2 - 1)
            tank2.update_turret_angle(pygame.mouse.get_pos())

        tank1.apply_gravity(static_terrain_surface, terrain_grid)
        tank2.apply_gravity(static_terrain_surface, terrain_grid)

        was_shooting = current_player == 1 and tank1.shooting or current_player == 2 and tank2.shooting

        if current_player == 1:
            tank_destroyed = tank1.update_bullet(static_terrain_surface, tank2)
            if tank_destroyed:
                victory_screen(1)
            elif was_shooting and not tank1.shooting:
                current_player = 2
                fuel_remaining_p2 = MAX_FUEL
                tank2.can_shoot = True
        else:
            tank_destroyed = tank2.update_bullet(static_terrain_surface, tank1)
            if tank_destroyed:
                victory_screen(2)
            elif was_shooting and not tank2.shooting:
                current_player = 1
                fuel_remaining = MAX_FUEL
                tank1.can_shoot = True

        tank1.draw(screen)
        tank2.draw(screen)

        # Aktualizacja siły strzału
        if current_player == 1:
            tank1.update_charge()
        else:
            tank2.update_charge()

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:  # Wciśnięcie lewego przycisku
                    if current_player == 1 and tank1.can_shoot:
                        tank1.charging = True
                        tank1.charge_power = tank1.min_power
                    elif current_player == 2 and tank2.can_shoot:
                        tank2.charging = True
                        tank2.charge_power = tank2.min_power
            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:  # Puszczenie lewego przycisku
                    if current_player == 1:
                        tank1.shoot()
                    else:
                        tank2.shoot()

            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_F11:
                    fullscreen()
                if e.key == pygame.K_ESCAPE:
                    pause_menu()

        pygame.display.update()
        clock.tick(60)

def victory_screen(winner):
    victory_font = get_font(90)
    return_font = get_font(30)
    
    fade_alpha = 0
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((30, 30, 30))
    
    start_time = pygame.time.get_ticks()
    
    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        
        # Stopniowe przyciemnianie ekranu - wzięte od chata GPT
        if fade_alpha < 180:
            fade_alpha = min(180, elapsed_time // 20)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_menu()
                if event.key == pygame.K_F11:
                    fullscreen()
                    
        # Przyciemnienie tła
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        
        victory_text = victory_font.render(f"Player {winner} won!", True, "#b68f40")
        victory_rect = victory_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(victory_text, victory_rect)
        return_text = return_font.render("Press ENTER to back to menu", True, "#FFFFFF")
        return_rect = return_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(return_text, return_rect)
        
        pygame.display.update()

terrain_points = generate_terrain()
main_menu()