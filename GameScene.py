import pygame
from abc import ABC, abstractmethod

class GameScene(ABC):
    def __init__(self, screen):
        """
        Inicializa la escena.
        :param screen: Pantalla donde se dibuja el juego.
        """
        self.screen = screen
        self.running = True
        self.nextGameScene = self

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

    @abstractmethod
    def gameLoop(self):
        pass

    def isRunning(self) -> bool:
        return self.running

    def getNextScene(self):
        return self.nextGameScene

