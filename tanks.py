import pygame

class Tank:
    def __init__(self, body_type, flipped=False):
        # Ścieżka do zasobów
        base_path = "czolgi/PNG/default size/"

        if body_type == "Desert1":
            self.body = pygame.image.load(f"{base_path}tanks_tankDesert_body1.png").convert_alpha()
            self.tracks = pygame.image.load(f"{base_path}tanks_tankTracks1.png").convert_alpha()
            self.turret = pygame.image.load(f"{base_path}tanks_turret1.png").convert_alpha()
        elif body_type == "Navy1":
            self.body = pygame.image.load(f"{base_path}tanks_tankNavy_body3.png").convert_alpha()
            self.tracks = pygame.image.load(f"{base_path}tanks_tankTracks3.png").convert_alpha()
            self.turret = pygame.image.load(f"{base_path}tanks_turret2.png").convert_alpha()
        elif body_type == "Green1":
            self.body = pygame.image.load(f"{base_path}tanks_tankGreen_body1.png").convert_alpha()
            self.tracks = pygame.image.load(f"{base_path}tanks_tankTracks1.png").convert_alpha()
            self.turret = pygame.image.load(f"{base_path}tanks_turret1.png").convert_alpha()
        elif body_type == "Grey1":
            self.body = pygame.image.load(f"{base_path}tanks_tankGrey_body2.png").convert_alpha()
            self.tracks = pygame.image.load(f"{base_path}tanks_tankTracks2.png").convert_alpha()
            self.turret = pygame.image.load(f"{base_path}tanks_turret3.png").convert_alpha()

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

        if body_type == "Navy1":
            turret_y = 25
        else:
            turret_y = 20

        if flipped:
            self.body = pygame.transform.flip(self.body, True, False)
            self.tracks = pygame.transform.flip(self.tracks, True, False)
            turret_x = center_x - self.turret_rect.width - 3
        else:
            turret_x = center_x + 3

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

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def set_position(self, x, y):
        self.x = x
        self.y = y