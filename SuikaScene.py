import pygame
import pymunk
import pymunk.pygame_util
import random
from Scene import GameScene
from Fruit import Fruit


class SuikaScene(GameScene):

    def __init__(self, framerate=60):
        super().__init__(framerate)

        # Inicializar espacio de físicas
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)  # Gravedad hacia abajo

        handler = self.space.add_collision_handler(1, 1)  # Colision de frutas
        handler.begin = self.collision_handler

        self.draw_options = pymunk.pygame_util.DrawOptions(self.surface)
        self.balls = []

        # Crear bordes del contenedor
        self.width, self.height = 750, 670
        self.half_width, self.half_height = (self.surface.get_width() - self.width) / 2, (
                    self.surface.get_height() - self.height) / 2
        self.create_container()


    def create_container(self):
        static_body = self.space.static_body
        thickness = 1

        walls = [
            pymunk.Segment(static_body, (self.half_width, self.half_height + self.height),
                           (self.half_width + self.width, self.half_height + self.height), thickness),  # Suelo
            pymunk.Segment(static_body, (self.half_width, self.half_height),
                           (self.half_width, self.half_height + self.height), thickness),  # Pared izquierda
            pymunk.Segment(static_body, (self.half_width + self.width, self.half_height),
                           (self.half_width + self.width, self.half_height + self.height), thickness)  # Pared derecha
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
                self.create_ball(self._correctMousePos(event.pos), random.randint(1, 5))

    def collision_handler(self, arbiter, space, data):

        shape_a, shape_b = arbiter.shapes

        if shape_a.fruit_type == shape_b.fruit_type:
            # Posicion intermedia entre bolas
            pos_x = (shape_a.body.position.x + shape_b.body.position.x) / 2
            pos_y = (shape_a.body.position.y + shape_b.body.position.y) / 2

            fruit_type = shape_a.fruit_type

            if shape_a in self.balls:
                self.balls.remove(shape_a)
                space.remove(shape_a, shape_a.body)
            if shape_b in self.balls:
                self.balls.remove(shape_b)
                space.remove(shape_b, shape_b.body)

            # Crear la nueva bola más grande
            self.create_ball((pos_x, pos_y), fruit_type + 1)
            return False  # Evita que pymunk procese la colisión normalmente
        else:
            # TODO: Condicion de parada del juego
            # if shape_a.body.position.y > self.half_height + self.height or shape_b.body.position.y > self.half_height + self.height:

            return True  # Retorna True para que pymunk procese la colisión normalmente

    def create_ball(self, position, fruit_type):
        if position is None:
            return

        fruit_type = min(fruit_type, len(Fruit.fruit_properties))
        fruit = Fruit(position, fruit_type)

        self.space.add(fruit.body, fruit)
        self.balls.append(fruit)

    def update(self, deltaTime):
        self.space.step(deltaTime)

    def draw(self):
        for shape in self.space.shapes:
            if isinstance(shape, pymunk.Segment):  # Verifica si es una pared
                start_pos = (int(shape.a.x), int(shape.a.y))
                end_pos = (int(shape.b.x), int(shape.b.y))
                pygame.draw.line(self.surface, (0, 0, 0), start_pos, end_pos, 2)  # Dibuja una línea negra

        for ball in self.balls:
            ball.draw(self.surface)

    def handlePause(self):
        pass
