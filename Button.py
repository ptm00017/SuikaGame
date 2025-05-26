import pygame
from SceneManager import GameState

class Button:
    def __init__(self, x, y, image_path, sceneEnum):
        """
        Constructor de la clase Button, se encarga de inicializar el botón con su imagen y su posición.
        :param x:
        :param y:
        :param image_path: Ruta de la imagen del botón.
        :param sceneEnum: Enum para guardar la escena a la que se dirige el botón.
        """

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sceneEnum = sceneEnum


    def draw(self, screen):
        """
        Se encarga de dibujar el botón en la pantalla
        :param screen: Superficie de pygame donde se dibuja el botón.
        """

        screen.blit(self.image, self.rect)


    def is_clicked(self, pos):
        """
            Se encarga de detectar si el botón ha sido pulsado por el ratón.
            Se usa junto con el evento MOUSEBUTTONDOWN de pygame y la posicion del ratón.
            Args:
                pos: Posicion de evento de pygame, event.pos

            """
        return self.rect.collidepoint(pos)