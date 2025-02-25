import pygame
from GameScene import GameScene


class CubeScene(GameScene):
    def __init__(self, screen):
        super().__init__(screen)
        self.running = True
        self.clock = pygame.time.Clock()
        self.cube_x, self.cube_y = 100, 100
        self.speed = 200

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
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.cube_x, self.cube_y, 50, 50))
        pygame.display.flip()

    def gameLoop(self):
        while self.running:
            deltaTime = self.clock.tick(60) / 1000
            self.handleUserInputs()
            self.update(deltaTime)
            self.draw()
