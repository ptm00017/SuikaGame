import pygame
from CubeScene import CubeScene

pygame.init()
screen = pygame.display.set_mode((800, 600))

#escena1 = Menu(screen)
escena2 = CubeScene(screen)

currentScene = escena2

while currentScene.isRunning():
    currentScene.gameLoop()
    currentScene = currentScene.getNextScene()
pygame.quit()