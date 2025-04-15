import pygame
from SceneManager import GameState

class Button:
    def __init__(self, x, y, image_path, sceneEnum):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sceneEnum = sceneEnum

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)