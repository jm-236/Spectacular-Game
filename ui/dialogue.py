import pygame
from state import state

class DialogueBox:
    def __init__(self, text, choices):
        self.text = text
        self.choices = choices
        self.selected = 0
        self.font = pygame.font.SysFont("arial", 20)

    def handle_event(self, event):
        if not self.choices:
            return

        if event.key == pygame.K_UP:
            self.selected = max(0, self.selected - 1)
        elif event.key == pygame.K_DOWN:
            self.selected = min(len(self.choices)-1, self.selected + 1)
        elif event.key == pygame.K_RETURN:
            _, effect = self.choices[self.selected]
            effect()

    def draw(self, screen):
        BOX_HEIGHT = 110
        BOX_Y = 540 - BOX_HEIGHT - 10  # quase fora da tela

        pygame.draw.rect(
            screen,
            (10, 10, 10),
            (50, BOX_Y, 860, BOX_HEIGHT)
        )

        text_surf = self.font.render(self.text, True, (230,230,230))
        screen.blit(text_surf, (70, BOX_Y + 20))

        for i, (txt, _) in enumerate(self.choices):
            color = (255,255,0) if i == self.selected else (200,200,200)
            surf = self.font.render(txt, True, color)
            screen.blit(surf, (80, 410 + i * 25))
