import pygame

class Tank:
    def __init__(self, body_type):
        # Ścieżka do zasobów
        base_path = "czolgi/PNG/default size/"

        if body_type == "Desert":
            self.body = pygame.image.load(f"{base_path}tanks_tankDesert_body1.png").convert_alpha()
            self.tracks = pygame.image.load(f"{base_path}tanks_tankTracks1.png").convert_alpha()
            self.turret = pygame.image.load(f"{base_path}tanks_turret1.png").convert_alpha()
        else:
            self.body = pygame.image.load(f"{base_path}tanks_tankGreen_body1.png").convert_alpha()
            self.tracks = pygame.image.load(f"{base_path}tanks_tankTracks1.png").convert_alpha()
            self.turret = pygame.image.load(f"{base_path}tanks_turret1.png").convert_alpha()

        # Pobieranie wymiarów wszystkich części
        self.body_rect = self.body.get_rect()
        self.tracks_rect = self.tracks.get_rect()
        self.turret_rect = self.turret.get_rect()

        self.total_width = max(self.body_rect.width, self.tracks_rect.width, self.turret_rect.width) + 60
        self.total_height = self.body_rect.height + self.tracks_rect.height + self.turret_rect.height + 100

        self.surface = pygame.Surface((self.total_width, self.total_height), pygame.SRCALPHA)
        center_x = self.total_width // 2

        turret_x = center_x + 3
        turret_y = 20

        body_x = center_x - self.body_rect.width // 2
        body_y = turret_y

        tracks_x = center_x - self.tracks_rect.width // 2
        tracks_y = body_y + 27

        self.surface.blit(self.tracks, (tracks_x, tracks_y))
        self.surface.blit(self.turret, (turret_x, turret_y))
        self.surface.blit(self.body, (body_x, body_y))

        self.x = 0
        self.y = 0

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def set_position(self, x, y):
        self.x = x
        self.y = y