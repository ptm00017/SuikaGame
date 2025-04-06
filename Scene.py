import pygame
from abc import ABC, abstractmethod

class GameScene(ABC):
    prueba = False

    def __init__(self, framerate):
        """
        Inicializa la escena.
        :param screen: Pantalla donde se dibuja el juego.
        """
        self.screen = pygame.display.set_mode((1280, 720),  pygame.RESIZABLE)
        self.surface = pygame.Surface((1920, 1080))

        self.clock = pygame.time.Clock()
        self.framerate = framerate

        self.running = True
        self.nextGameScene = None

    @abstractmethod
    def handleUserInputs(self):
        pass

    @abstractmethod
    def handlePause(self):
        pass

    @abstractmethod
    def update(self, deltaTime):
        pass

    @abstractmethod
    def draw(self):
        pass

    def gameLoop(self):
        while self.running:
            deltaTime = self.clock.tick(self.framerate) / 1000
            self.handleUserInputs()
            if deltaTime < 2 * 1 / self.framerate:
                self.update(deltaTime)
            self.surface.fill((255, 255, 255))
            self.draw()
            self._drawScaledGame()
            pygame.display.flip()

    def isRunning(self) -> bool:
        return self.running

    def getNextGameScene(self):
        if(self.nextGameScene is not None):
            prueba = True
            print("GameScene::getNextGameScene()\t"+str(self.nextGameScene))
        return self.nextGameScene

    def _correctMousePos(self, event):
        window_size = self.screen.get_size()
        surface_size = self.surface.get_size()

        return (pygame.mouse.get_pos()[0] * surface_size[0] / window_size[0],
                pygame.mouse.get_pos()[1] * surface_size[1] / window_size[1])


    def _drawScaledGame(self):

        # Obtener tamaños de la ventana y la superficie base
        window_width, window_height = self.screen.get_size()
        base_width, base_height = self.surface.get_size()

        # Calcular la escala máxima manteniendo la relación de aspecto
        scale = min(window_width / base_width, window_height / base_height)
        new_width = int(base_width * scale)
        new_height = int(base_height * scale)

        # Escalar la superficie y centrarla en la pantalla
        scaled_surface = pygame.transform.smoothscale(self.surface, (new_width, new_height))
        x_offset = (window_width - new_width) // 2
        y_offset = (window_height - new_height) // 2

        self.screen.fill((0, 0, 0))  # Llenar el fondo para evitar residuos
        self.screen.blit(scaled_surface, (x_offset, y_offset))