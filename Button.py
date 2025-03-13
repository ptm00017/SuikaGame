import pygame
from SceneManager import GameState

class Button:
    def __init__(self, x, y, width, height, color, text, font, text_color, sceneEnum):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.sceneEnum = sceneEnum

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=20)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        hasBeenClicked = self.rect.collidepoint(pos)

        return hasBeenClicked

