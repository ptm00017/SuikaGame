import math

import pygame
import pymunk

class Fruit(pymunk.Circle):
    # Parametro de cada fruta
    fruit_properties = {
        1: {"radius": 50, "elasticity": 0, "friction": 1, "mass": 20, "image_path": "res/ball_1.png"},
        2: {"radius": 32, "elasticity": 0, "friction": 1, "mass": 20, "image_path": "res/ball_2.png"},
        3: {"radius": 50, "elasticity": 0, "friction": 1, "mass": 20, "image_path": "res/ball_3.png"},
        4: {"radius": 52, "elasticity": 0, "friction": 1, "mass": 20, "image_path": "res/ball_4.png"},
        5: {"radius": 65, "elasticity": 0, "friction": 1, "mass": 20, "image_path": "res/ball_5.png"},
        6: {"radius": 85, "elasticity": 0, "friction": 1, "mass": 20, "image_path": "res/ball_6.png"},
        7: {"radius": 100, "elasticity": 0, "friction": 1, "mass": 20, "image_path": "res/ball_7.png"},
        8: {"radius": 117, "elasticity": 0, "friction": 1, "mass": 20, "image_path": "res/ball_8.png"},
        9: {"radius": 192, "elasticity": 0, "friction": 1, "mass": 20, "image_path": "res/ball_9.png"},
        10: {"radius": 165, "elasticity": 0, "friction": 1, "mass": 20, "image_path": "res/ball_10.png"},
        11: {"radius": 195, "elasticity": 0, "friction": 1, "mass": 20, "image_path": "res/ball_11.png"},
    }

    def __init__(self, position, fruit_type):
        properties = self.fruit_properties[fruit_type]
        mass = properties["mass"]
        radius = properties["radius"]
        inertia = pymunk.moment_for_circle(mass, 0, radius)

        body = pymunk.Body(mass, inertia)
        body.position = position

        super().__init__(body, radius)
        self.elasticity = properties["elasticity"]
        self.friction = properties["friction"]

        self.image = pygame.image.load(properties["image_path"])
        

def draw(self, screen):
    x, y = int(self.body.position.x), int(self.body.position.y)
    radius = self.radius
    image = pygame.transform.scale(pygame.image.load(self.fruit_properties[self.radius]["image_path"]), (radius * 2, radius * 2))

    # Obtener el ángulo de rotación del cuerpo de la fruta
    angle = math.degrees(self.body.angle)  # Convertir de radianes a grados

    # Rotar la imagen
    rotated_image = pygame.transform.rotate(image, -angle)  # Rotar en sentido antihorario

    # Obtener el nuevo rectángulo para la imagen rotada
    rotated_rect = rotated_image.get_rect(center=(x, y))

    # Mantener la transparencia de la imagen rotada
    rotated_image.set_colorkey((0, 0, 0))  # Establecer el color negro (o el color de fondo) como transparente

    # Dibujar la imagen rotada en la pantalla con transparencia
    screen.blit(rotated_image, rotated_rect.topleft)
