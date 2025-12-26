import pygame
from scenes.base_scene import Scene
from ui.dialogue import DialogueBox
from ui.phone import Phone
from player import Player

class Bedroom(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player()
        self.phone = Phone()
        self.show_phone = False

        self.background = pygame.image.load(
            "assets/images/bedroom.png"
        ).convert()
        self.background = pygame.transform.scale(
            self.background, (960, 540)
        )


        self.dialogue = DialogueBox(
            "07:10 AM - Mais um dia...",
            []
        )

        self.interaction_text = None

        # zonas de interação
        self.bed = pygame.Rect(150, 320, 120, 60)
        self.desk = pygame.Rect(400, 330, 100, 60)
        self.door = pygame.Rect(850, 280, 60, 120)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.show_phone = not self.show_phone

            if event.key == pygame.K_e:
                self.check_interaction()

    def check_interaction(self):
        if self.player.rect.colliderect(self.bed):
            self.dialogue.text = "A cama ainda tá quente.\nNão dá pra voltar."
        elif self.player.rect.colliderect(self.desk):
            self.dialogue.text = "Livros, mochila...\nEscola."
        elif self.player.rect.colliderect(self.door):
            self.dialogue.text = "Hora de ir."
            # futuramente: trocar cena

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if not self.show_phone:
            self.player.update(dt, keys)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        # quarto escuro

        # objetos
        pygame.draw.rect(screen, (60, 60, 80), self.bed)
        pygame.draw.rect(screen, (80, 60, 40), self.desk)
        pygame.draw.rect(screen, (40, 40, 40), self.door)

        self.player.draw(screen)

        if self.show_phone:
            self.phone.draw(screen)
        else:
            self.dialogue.draw(screen)
