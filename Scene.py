import pygame
from abc import ABC, abstractmethod


class GameScene(ABC):

    """
    Clase abstracta que representa una escena del juego.
    Contiene el bucle de ejecución del juego
    """


    def __init__(self, framerate):
        """
        Inicializa la escena.
        :param screen: Pantalla donde se dibuja el juego.
        """
        # La ventana del juego, se puede redimensionar
        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

        # Pantalla interna del juego, internamente se dibuja cualquier cosa a esta superficie y se renderiza a esa resolucion,
        # despues es reescalado según las dimensiones de la ventana.
        self.surface = pygame.Surface((1920, 1080))

        self.clock = pygame.time.Clock()
        self.framerate = framerate

        self.running = True

        # Variable que almacena la escena siguiente a mostrar tras terminar el bucle de ejecución del juego.
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
        """
        Bucle de ejecución del juego, se encarga de manejar los eventos, actualizar el estado del juego y dibujar en pantalla.
        :return:
        """
        while self.running:
            deltaTime = self.clock.tick(self.framerate) / 1000
            self.handleUserInputs()
            # Si pasa mucho tiempo entre frames, no actualizar el juego para evitar problemas de logica.
            if deltaTime < 2 * 1 / self.framerate:
                self.update(deltaTime)
            self.surface.fill((255, 255, 255))
            self.draw()
            self._drawScaledGame()
            pygame.display.flip()

    def isRunning(self) -> bool:
        return self.running

    def restart(self):
        """
        Reinicia la escena por completo, llama de nuevo al contructor de la escena.
        :return:
        """
        self.__init__(self.framerate)

    def getNextGameScene(self):
        if (self.nextGameScene is not None):
            print("GameScene::getNextGameScene()\t" + str(self.nextGameScene))
        return self.nextGameScene

    def _correctMousePos(self, event):
        """
        Corrige la posición del ratón para que corresponda con las coordenadas de la superficie del juego escalada.
        :param event:
        :return:
        """

        window_width, window_height = self.screen.get_size()
        base_width, base_height = self.surface.get_size()

        # Calcular la escala máxima manteniendo la relación de aspecto,
        # es decir, hasta cuando se puede escalar la superficie sin que se salga de los bordes de la ventana.
        scale = min(window_width / base_width, window_height / base_height)
        new_width = int(base_width * scale)
        new_height = int(base_height * scale)

        # Tamaño de los bordes negros en pixeles
        x_offset = (window_width - new_width) // 2
        y_offset = (window_height - new_height) // 2

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Verificar si el ratón está dentro de los bordes negros
        if mouse_x < x_offset or mouse_x > x_offset + new_width or mouse_y < y_offset or mouse_y > y_offset + new_height:
            return None

        # Ajustar la posición del ratón
        corrected_x = (mouse_x - x_offset) * base_width / new_width
        corrected_y = (mouse_y - y_offset) * base_height / new_height

        return corrected_x, corrected_y

    def _drawScaledGame(self):
        """
        Dibujar el contenido del juego con
        :return:
        """
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

        self.screen.fill((0, 0, 0))  # Llenar la pantalla de negro para evitar residuos
        self.screen.blit(scaled_surface, (x_offset, y_offset))