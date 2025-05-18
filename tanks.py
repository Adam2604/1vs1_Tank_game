import pygame
import math

class Tank:
    def __init__(self, body_type, flipped=False):
        # Ścieżka do zasobów
        base_path = "czolgi/PNG/default size/"

        #różne rodzaje czołgów
        # Zachowaj oryginalną grafikę lufy przed jakimkolwiek przekształceniem
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

        #pocisk
        self.bullet = pygame.image.load("czolgi/PNG/default size/tank_bullet5.png").convert_alpha()
        self.bullet_rect = self.bullet.get_rect()
        self.is_shooting = False
        self.bullet_x = 0
        self.bullet_y = 0

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

    def check_collision_with_terrain(self, terrain_surface): #Cała klasa napisana samemu
        terrain_mask = pygame.mask.from_surface(terrain_surface)

        offset = (int(self.x), int(self.y))
        overlap = terrain_mask.overlap(self.mask, offset)
        return overlap is not None

    def apply_gravity(self, terrain_surface, terrain_points): #Klasa napisana samemu
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

        if 0 <= new_x <= 1280 - self.total_width:
            old_x = self.x
            self.x = new_x
            if self.check_collision_with_terrain(terrain_surface):
                self.x = old_x

    def update_turret_angle(self, mouse_pos):
        turret_center_x = self.x + self.turret_pivot_x
        turret_center_y = self.y + self.turret_pivot_y

        dx = mouse_pos[0] - turret_center_x
        dy = mouse_pos[1] - turret_center_y
        angle = math.degrees(math.atan2(dy, dx)) * -1

        if self.flipped:
            min_angle = 175
            max_angle = 200
            angle = max(min_angle, min(max_angle, angle))
        else:
            min_angle = -5
            max_angle = 30
            angle = max(min_angle, min(max_angle, angle))

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
        new_surface.blit(rotated_turret, turret_rect)
        new_surface.blit(self.tracks, (tracks_x, tracks_y))
        new_surface.blit(self.body, (body_x, body_y))
        
        screen.blit(new_surface, (self.x, self.y))
        
    def set_position(self, x, y):
        self.x = x
        self.y = y