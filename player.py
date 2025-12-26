import pygame

class Player:
    def __init__(self):
        self.rect = pygame.Rect(200, 300, 40, 80)
        self.speed = 200
        self.floor_y = 460
        self.image = pygame.image.load("assets/images/peter.png").convert_alpha()
        scale = 4
        w, h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (w*scale, h*scale))

        self.rect = self.image.get_rect()
        self.rect.bottom = self.floor_y


    def update(self, dt, keys):

        LIMITE_ESQUERDO = 0 # Onde a cama começa
        LIMITE_DIREITO = 860  # Onde a porta termina

        if keys[pygame.K_a] and self.rect.x > LIMITE_ESQUERDO:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_d] and self.rect.x < LIMITE_DIREITO:
            self.rect.x += self.speed * dt

    def draw(self, screen):
        screen.blit(self.image, self.rect)

