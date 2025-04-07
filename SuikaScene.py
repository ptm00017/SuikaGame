from typing import cast

import pygame
import pymunk
import pymunk.pygame_util
from Scene import GameScene
from Fruit import Fruit


class SuikaScene(GameScene):

    def __init__(self, framerate=60):
        super().__init__(framerate)

        # Inicializar espacio de físicas
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)  # Gravedad hacia abajo

        self.draw_options = pymunk.pygame_util.DrawOptions(self.surface)
        self.balls = []

        # Crear bordes del contenedor
        self.create_container()

    def create_container(self):
        static_body = self.space.static_body
        width, height = 750, 670
        thickness = 10

        walls = [
            pymunk.Segment(static_body, (50, height - 50), (width - 50, height - 50), thickness),  # Suelo
            pymunk.Segment(static_body, (50, 50), (50, height - 50), thickness),  # Pared izquierda
            pymunk.Segment(static_body, (width - 50, 50), (width - 50, height - 50), thickness)  # Pared derecha
        ]

        for wall in walls:
            wall.elasticity = 0
            wall.friction = .6
            self.space.add(wall)

    def handleUserInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse button pressed")
                self.create_ball(self._correctMousePos(event.pos))

    def create_ball(self, position):
        if position is None:
            return

        print("Ball created")

        fruit_type = 1
        fruit = Fruit(position, fruit_type)

        self.space.add(fruit.body, fruit)
        self.balls.append(fruit)

    def update(self, deltaTime):
        self.space.step(deltaTime)

    def draw(self):
        self.space.debug_draw(self.draw_options)
        for ball in self.balls:
            ball.draw(self.surface)


    def handlePause(self):
        pass