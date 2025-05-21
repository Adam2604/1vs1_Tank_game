import pygame
import math


class Tank:
    def __init__(self, body_type, flipped=False):
        # Ścieżka do zasobów
        base_path = "czolgi/PNG/default size/"

        # różne rodzaje czołgów
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
            max_angle = 185
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
            turret_x = center_x - self.turret_rect.width - 3
        else:
            turret_x = center_x - 7

        turret_y = 25 if hasattr(self, 'navy') else 18

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

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def shoot(self):
        if not self.shooting:
            self.shooting = True
            bullet_speed = self.bullet_power  # Stała prędkość pocisku
            angle_rad = math.radians(self.turret_angle)
            barrel_length = 20  # Długość lufy

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

            # Sprawdzanie kolizji z drugim czołgiem
            if other_tank:
                tank_rect = pygame.Rect(other_tank.x, other_tank.y,
                                        other_tank.total_width, other_tank.total_height)

                if bullet_rect.colliderect(tank_rect):
                    tank_offset = (int(bullet_rect.x - other_tank.x),
                                   int(bullet_rect.y - other_tank.y))

                    if other_tank.mask.overlap(bullet_mask, tank_offset):
                        self.shooting = False
                        self.bullet_positions = []
                        return

            # Sprawdzanie czy pocisk jest poza ekranem
            if (self.bullet_x < 0 or self.bullet_x > terrain_surface.get_width() or
                    self.bullet_y > terrain_surface.get_height()):
                self.shooting = False
                self.bullet_positions = []