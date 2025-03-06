import pygame

from SceneManager import SceneManager, GameState
from CubeScene import CubeScene
from Menu import Menu


pygame.init()

sceneManager = SceneManager()

sceneManager.addScene(GameState.MENU,Menu(60))
sceneManager.addScene(GameState.GAME,CubeScene(60))
try:
    while sceneManager.getScene().isRunning():
        sceneManager.getScene().gameLoop()
        sceneManager.changeScene(sceneManager.getScene().getNextGameScene())
except:
    print(" ")
pygame.quit()