import pygame
import math


class Tank:
    def __init__(self, body_type, flipped=False):
        self.charging = False
        self.charge_power = 0
        self.min_power = 5
        self.max_power = 25
        self.charge_speed = 0.8  # Prędkość zmiany siły strzału
        self.charge_direction = 1
        self.max_health = 100
        self.health = self.max_health
        # Ścieżka do zasobów
        base_path = "czolgi/PNG/default size/"

        # różne rodzaje czołgów, na przyszłość jak zostanie dodana możliwość wyboru czołgu
        # grafiki czołgów i związane z czołgami typu pociski, wybuchy, stworzone "by Kenney Vleugels"
        self.original_turret = pygame.image.load(f"{base_path}tanks_turret1.png").convert_alpha()
        if body_type == "Desert1":
            self.body = pygame.image.load(f"{base_path}tanks_tankDesert_body1.png").convert_alpha()
            self.tracks = pygame.image.load(f"{base_path}tanks_tankTracks1.png").convert_alpha()
            self.turret = self.original_turret
        elif body_type == "Navy1":
            self.body = pygame.image.load(f"{base_path}tanks_tankNavy_body3.png").convert_alpha()
            self.tracks = pygame.image.load(f"{base_path}tanks_tankTracks3.png").convert_alpha()
            self.turret = pygame.image.load(f"{base_path}tanks_turret2.png").convert_alpha()
            self.original_turret = self.turret
        elif body_type == "Green1":
            self.body = pygame.image.load(f"{base_path}tanks_tankGreen_body1.png").convert_alpha()
            self.tracks = pygame.image.load(f"{base_path}tanks_tankTracks1.png").convert_alpha()
            self.turret = pygame.image.load(f"{base_path}tanks_turret1.png").convert_alpha()
        elif body_type == "Grey1":
            self.body = pygame.image.load(f"{base_path}tanks_tankGrey_body2.png").convert_alpha()
            self.tracks = pygame.image.load(f"{base_path}tanks_tankTracks2.png").convert_alpha()
            self.turret = pygame.image.load(f"{base_path}tanks_turret3.png").convert_alpha()

        # pocisk
        self.bullet = pygame.image.load("czolgi/PNG/default size/tank_bullet5.png").convert_alpha()
        self.bullet_rect = self.bullet.get_rect()
        self.bullet_x = 0
        self.bullet_y = 0
        self.bullet_velocity_x = 0
        self.bullet_velocity_y = 0
        self.bullet_gravity = 0.5
        self.bullet_power = 15
        self.bullet_positions = []
        self.shooting = False

        self.body_type = body_type
        self.body_rect = self.body.get_rect()
        self.tracks_rect = self.tracks.get_rect()
        self.turret_rect = self.turret.get_rect()

        self.total_width = max(self.body_rect.width, self.tracks_rect.width, self.turret_rect.width)
        self.total_height = self.body_rect.height + self.tracks_rect.height + self.turret_rect.height + 100

        self.surface = pygame.Surface((self.total_width, self.total_height), pygame.SRCALPHA)

        center_x = self.total_width // 2

        body_x = center_x - self.body_rect.width // 2
        body_y = 20
        tracks_x = center_x - self.tracks_rect.width // 2
        tracks_y = body_y + 27
        self.turret_angle = 0
        self.flipped = flipped
        if flipped:
            self.body = pygame.transform.flip(self.body, True, False)
            self.tracks = pygame.transform.flip(self.tracks, True, False)
            self.original_turret = pygame.transform.flip(self.original_turret, True, False)
            turret_x = center_x - self.turret_rect.width - 3
        else:
            turret_x = center_x + 3

        if body_type == "Navy1":
            turret_y = 25
        else:
            turret_y = 20

        self.surface.blit(self.tracks, (tracks_x, tracks_y))
        self.surface.blit(self.turret, (turret_x, turret_y))
        self.surface.blit(self.body, (body_x, body_y))

        self.mask = pygame.mask.from_surface(self.surface)

        self.x = 0
        self.y = 0
        self.total_height = self.total_height
        self.total_width = self.total_width

        self.velocity_y = 0
        self.velocity_x = 0
        self.gravity = 0.5
        self.speed = 2
        self.on_ground = False

        self.turret_pivot_x = turret_x + self.turret_rect.width // 2
        self.turret_pivot_y = turret_y + self.turret_rect.height // 2

        # Istniejący kod init...
        self.update_terrain_function = None
        self.terrain_grid = None

        if self.flipped:
            self.turret_angle = 180

    def set_update_terrain_function(self, function):
        self.update_terrain_function = function

    def set_terrain_grid(self, grid):
        self.terrain_grid = grid

    def check_collision_with_terrain(self, terrain_surface):  # Cała klasa napisana samemu
        terrain_mask = pygame.mask.from_surface(terrain_surface)

        offset = (int(self.x), int(self.y))
        overlap = terrain_mask.overlap(self.mask, offset)
        return overlap is not None

    def apply_gravity(self, terrain_surface, terrain_points):  # Klasa napisana samemu
        test_y = self.y + self.velocity_y

        old_y = self.y
        self.y = test_y

        if self.check_collision_with_terrain(terrain_surface):
            while self.check_collision_with_terrain(terrain_surface):
                self.y -= 1
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            self.velocity_y += self.gravity

    def move(self, direction, terrain_surface, terrain_points):
        new_x = self.x + (direction * self.speed)

        screen_width = terrain_surface.get_width()
        if 0 <= new_x <= screen_width - self.total_width:
            old_x = self.x
            self.x = new_x
            if self.check_collision_with_terrain(terrain_surface):
                self.x = old_x
                return False
            return True
        return False

    def update_turret_angle(self, mouse_pos):
        turret_center_x = self.x + self.turret_pivot_x
        turret_center_y = self.y + self.turret_pivot_y

        dx = mouse_pos[0] - turret_center_x
        dy = mouse_pos[1] - turret_center_y
        angle = math.degrees(math.atan2(dy, dx)) * -1

        if self.flipped:
            if angle < 0:
                angle += 360
            min_angle = 150
            max_angle = 190
            angle = min(max(angle, min_angle), max_angle)
        else:
            min_angle = -5
            max_angle = 30
            angle = min(max(angle, min_angle), max_angle)

        self.turret_angle = angle

    def draw(self, screen):
        new_surface = pygame.Surface((self.total_width, self.total_height), pygame.SRCALPHA)

        center_x = self.total_width // 2
        body_x = center_x - self.body_rect.width // 2
        body_y = 20
        tracks_x = center_x - self.tracks_rect.width // 2
        tracks_y = body_y + 27

        if self.flipped:
            turret_x = center_x - self.turret_rect.width - 2
        else:
            turret_x = center_x - 7

        if self.body_type == "Navy1":
            turret_y = 19
        else:
            turret_y = 18

        rotated_turret = pygame.transform.rotate(self.original_turret, self.turret_angle)
        turret_rect = rotated_turret.get_rect(center=(turret_x + self.turret_rect.width // 2,
                                                      turret_y + self.turret_rect.height // 2))

        if self.shooting:
            bullet_rect = self.bullet.get_rect(center=(self.bullet_x, self.bullet_y))
            screen.blit(self.bullet, bullet_rect)

        new_surface.blit(rotated_turret, turret_rect)
        new_surface.blit(self.tracks, (tracks_x, tracks_y))
        new_surface.blit(self.body, (body_x, body_y))

        screen.blit(new_surface, (self.x, self.y))
        self.draw_health_bar(screen)
        self.draw_power_bar(screen)  # Dodaj tę linię

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def shoot(self):
        if not self.shooting and self.charging:
            self.shooting = True
            self.charging = False
            bullet_speed = self.charge_power
            angle_rad = math.radians(self.turret_angle)
            barrel_length = 20

            start_x = self.x + self.turret_pivot_x + math.cos(angle_rad) * barrel_length
            self.bullet_velocity_x = bullet_speed * math.cos(angle_rad)

            start_y = self.y + self.turret_pivot_y - math.sin(angle_rad) * barrel_length
            self.bullet_velocity_y = -bullet_speed * math.sin(angle_rad)

            self.bullet_x = start_x
            self.bullet_y = start_y
            self.bullet_positions = [(self.bullet_x, self.bullet_y)]

    def update_bullet(self, terrain_surface, other_tank=None):
        if self.shooting:
            self.bullet_x += self.bullet_velocity_x
            self.bullet_y += self.bullet_velocity_y
            self.bullet_velocity_y += self.bullet_gravity
            self.bullet_positions.append((self.bullet_x, self.bullet_y))

            bullet_rect = self.bullet.get_rect(center=(self.bullet_x, self.bullet_y))
            bullet_surface = pygame.Surface(bullet_rect.size, pygame.SRCALPHA)
            bullet_surface.blit(self.bullet, (0, 0))
            bullet_mask = pygame.mask.from_surface(bullet_surface)

            # Sprawdzanie kolizji z terenem
            terrain_mask = pygame.mask.from_surface(terrain_surface)
            terrain_offset = (int(bullet_rect.x), int(bullet_rect.y))
            if terrain_mask.overlap(bullet_mask, terrain_offset):
                impact_area = (
                    int(self.bullet_x - 60),
                    int(self.bullet_y - 60),
                    120,
                    120
                )
                
                if self.update_terrain_function and self.terrain_grid:
                    self.update_terrain_function(terrain_surface, self.terrain_grid, impact_area)
                
                self.shooting = False
                self.bullet_positions = []
                return

            if other_tank:
                tank_rect = pygame.Rect(other_tank.x, other_tank.y,
                                        other_tank.total_width, other_tank.total_height)

                if bullet_rect.colliderect(tank_rect):
                    tank_offset = (int(bullet_rect.x - other_tank.x),
                                   int(bullet_rect.y - other_tank.y))

                    if other_tank.mask.overlap(bullet_mask, tank_offset):
                        damage = 25
                        tank_destroyed = other_tank.take_damage(damage)
                        self.shooting = False
                        self.bullet_positions = []
                        return tank_destroyed

            # Sprawdzanie czy pocisk jest poza ekranem
            if (self.bullet_x < 0 or self.bullet_x > terrain_surface.get_width() or
                    self.bullet_y > terrain_surface.get_height()):
                self.shooting = False
                self.bullet_positions = []

    def draw_health_bar(self, screen):
        bar_width = 60
        bar_height = 10
        x = self.x + (self.total_width - bar_width) // 2
        y = self.y - 20
        
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, (0, 255, 0), (x, y, health_width, bar_height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        return self.health <= 0  # Zwraca True jeśli czołg został zniszczony

    def draw_power_bar(self, screen):
        if self.charging:
            bar_width = 60
            bar_height = 10
            x = self.x + (self.total_width - bar_width) // 2
            y = self.y - 35

            pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_width, bar_height))
            power_width = ((self.charge_power - self.min_power) / (self.max_power - self.min_power)) * bar_width
            pygame.draw.rect(screen, (255, 165, 0), (x, y, int(power_width), bar_height))
            power_font = pygame.font.SysFont(None, 20)
            power_text = power_font.render(f"{int(self.charge_power)}", True, (255, 255, 255))
            text_x = x + bar_width + 5
            text_y = y
            screen.blit(power_text, (text_x, text_y))

    def update_charge(self):
        if self.charging:
            self.charge_power += self.charge_speed * self.charge_direction
            if self.charge_power >= self.max_power:
                self.charge_direction = -1
            elif self.charge_power <= self.min_power:
                self.charge_direction = 1