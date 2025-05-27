from enum import Enum

import pygame


class GameState(Enum):
    MENU = 1
    GAME = 2

class SceneManager:
    def __init__(self):
        self.scenes = dict()
        self.currentScene = GameState.MENU

    def changeScene(self, sceneEnum):
        self.currentScene = sceneEnum
        self.scenes[self.currentScene].restart()

    def addScene(self, sceneEnum, scene):
        self.scenes.update({sceneEnum: scene})

    def getScene(self):
        return self.scenes[self.currentScene]