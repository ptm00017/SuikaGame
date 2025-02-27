import pygame
from CubeScene import CubeScene

pygame.init()

#escena1 = Menu(screen)
escena2 = CubeScene()

currentScene = escena2

while currentScene.isRunning():
    currentScene.gameLoop()
    currentScene = currentScene.getNextScene()
pygame.quit()