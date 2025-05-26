import pygame
from Button import Button
from Scene import GameScene
from SceneManager import GameState

class Menu(GameScene):
    def __init__(self, framerate, window_resolution):
        super().__init__(framerate, window_resolution)
        self.clock = pygame.time.Clock()

        self.button_play = Button(700, 620, "res/img/button_play.png", GameState.GAME)
        self.button_exit = Button(700, 780, "res/img/button_exit.png", None)

        self.title_image = pygame.image.load("res/img/title.png")


        self.mouse_pos = None

        # Si la canción no se estaba reproduciéndose antes, reproducir
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("res/sounds/loop.ogg")
            pygame.mixer.music.set_volume(0.8)  # Ajusta el volumen de la música
            pygame.mixer.music.play(-1)  # Reproduce en loop infinito (-1)



    def handleUserInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = self._correctMousePos(event.pos)
                        

    def handlePause(self):
        pass

    def update(self, deltaTime):
        if self.mouse_pos is not None:
            # Terminar la ejecucion del menú y establece la siguiente escena como la escena del juego.
            if self.button_play.is_clicked(self.mouse_pos):
                self.nextGameScene = self.button_play.sceneEnum
                self.running = False
            # Cerrar el juego por completo
            if self.button_exit.is_clicked(self.mouse_pos):
                pygame.quit()

    def draw(self):
        # Dibujar fondo del juego
        self.surface.fill((255, 255, 255))

        self.button_play.draw(self.surface)
        self.button_exit.draw(self.surface)
        self.surface.blit(self.title_image, (340, 50))