import pygame
from Button import Button
from GameScene import GameScene
from mainRefactor import escena1


class Menu(GameScene):
    def __init__(self, screen):


        self.button = Button(300, 200, 200, 50, (0, 255, 0), "Menu", pygame.font.SysFont("Arial", 36), (0, 0, 0), escena1)