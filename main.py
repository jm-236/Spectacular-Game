import pygame
from settings import *
from scenes.bedroom import Bedroom

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        self.scene = Bedroom(self)

game = Game()

running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.scene.handle_event(event)

    game.scene.update(dt)
    game.scene.draw(screen)

    pygame.display.flip()

pygame.quit()
