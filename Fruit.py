import math

import pygame
import pymunk

class Fruit(pymunk.Circle):
    """
    Clase que representa una fruta en el juego, hereda de pymunk.Circle.
    Contiene las propiedades fisicas de una fruta y su imagen asociada.
    """
    fruit_properties = {
        1: {"radius": 25, "elasticity": 0, "friction": 1, "mass": 20, "points": 2, "image_path": "res/img/dulces/ball_1.png"},
        2: {"radius": 32, "elasticity": 0, "friction": 1, "mass": 20, "points": 4, "image_path": "res/img/dulces/ball_2.png"},
        3: {"radius": 50, "elasticity": 0, "friction": 1, "mass": 20, "points": 8, "image_path": "res/img/dulces/ball_3.png"},
        4: {"radius": 52, "elasticity": 0, "friction": 1, "mass": 20, "points": 10, "image_path": "res/img/dulces/ball_4.png"},
        5: {"radius": 65, "elasticity": 0, "friction": 1, "mass": 20, "points": 20, "image_path": "res/img/dulces/ball_5.png"},
        6: {"radius": 85, "elasticity": 0, "friction": 1, "mass": 20, "points": 30, "image_path": "res/img/dulces/ball_6.png"},
        7: {"radius": 100, "elasticity": 0, "friction": 1, "mass": 20, "points": 60, "image_path": "res/img/dulces/ball_7.png"},
        8: {"radius": 117, "elasticity": 0, "friction": 1, "mass": 20, "points": 70, "image_path": "res/img/dulces/ball_8.png"},
        9: {"radius": 192, "elasticity": 0, "friction": 1, "mass": 20, "points": 80, "image_path": "res/img/dulces/ball_9.png"},
        10: {"radius": 165, "elasticity": 0, "friction": 1, "mass": 20, "points": 90, "image_path": "res/img/dulces/ball_10.png"},
        11: {"radius": 195, "elasticity": 0, "friction": 1, "mass": 20, "points": 1000, "image_path": "res/img/dulces/ball_11.png"},
    }

    def __init__(self, position, fruit_type):
        """
        Inicializa una fruta con sus propiedades y posición.
        :param position: Posición inicial de la fruta (pymunk.Vec2d)
        :param fruit_type: Identificador de la fruta (1-11)
        """

        properties = self.fruit_properties[fruit_type]
        mass = properties["mass"]
        radius = properties["radius"]
        inertia = pymunk.moment_for_circle(mass, 0, radius)

        body = pymunk.Body(mass, inertia)
        body.position = position

        super().__init__(body, radius)
        self.elasticity = properties["elasticity"]
        self.friction = properties["friction"]
        self.fruit_type = fruit_type
        self.collision_type = 1 # identificador de colisión de pymunk para las físicas de frutas
        self.image = pygame.image.load(properties["image_path"])
        aspect_ratio = self.image.get_width() / self.image.get_height()
        self.image = pygame.transform.smoothscale(self.image, (2 * radius * aspect_ratio, 2 * radius))

    def draw(self, screen):
        """
        Se encarga de dibujar la fruta en la pantalla.
        :param screen: Superficie de pygame
        """

        # Obtén el ángulo de rotación del cuerpo en grados
        angle = -math.degrees(self.body.angle)  # Convierte de radianes a grados (el signo negativo es para que gire en la dirección correcta)

        # Rota la imagen
        rotated_image = pygame.transform.rotate(self.image, angle)

        # Obtén el rectángulo de la imagen rotada
        rotated_rect = rotated_image.get_rect()

        # Coloca la imagen rotada centrada en la posición del cuerpo
        rotated_rect.center = (int(self.body.position.x), int(self.body.position.y))

        # Dibuja la imagen rotada en la pantalla
        screen.blit(rotated_image, rotated_rect.topleft)
