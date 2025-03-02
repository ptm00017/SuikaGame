import pygame
from Button import Button
from GameScene import GameScene
from SceneManager import GameState

class CubeScene(GameScene):
    def __init__(self, framerate):
        super().__init__(framerate)
        self.clock = pygame.time.Clock()
        self.cube_x, self.cube_y = 100, 100
        self.speed = 200

        self.button = Button(300, 200, 200, 50, (0, 255, 0), "Menu", pygame.font.SysFont("Arial", 36), (0, 0, 0), GameState.MENU)

    def handleUserInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


    def handlePause(self):
        pass

    def update(self, deltaTime):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.cube_x -= self.speed * deltaTime
        if keys[pygame.K_RIGHT]:
            self.cube_x += self.speed * deltaTime
        if keys[pygame.K_UP]:
            self.cube_y -= self.speed * deltaTime
        if keys[pygame.K_DOWN]:
            self.cube_y += self.speed * deltaTime

    def draw(self):
        self.surface.fill((255, 255, 255))
        pygame.draw.rect(self.surface, (0, 255, 0), (self.cube_x, self.cube_y, 50, 50))
        self.button.draw(self.surface)

        self._drawScaledGame()

    def getNextGameScene(self):
        return self.nextGameScene