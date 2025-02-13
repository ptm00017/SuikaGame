import pygame
import pymunk
import pymunk.pygame_util
import math
import random

pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 670, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
bowl = pymunk.Space()
bowl.gravity = (0, 900)

ball_properties = {
    25 : pygame.image.load("res/ball_1.png"),
    32 : pygame.image.load("res/ball_2.png"),
    50 : pygame.image.load("res/ball_3.png"),
    52 : pygame.image.load("res/ball_4.png"),
    65 : pygame.image.load("res/ball_5.png"),
    85 : pygame.image.load("res/ball_6.png"),
    100 : pygame.image.load("res/ball_7.png"),
    117 : pygame.image.load("res/ball_8.png"),
    192 : pygame.image.load("res/ball_9.png"),
    165 : pygame.image.load("res/ball_10.png"),
    195 : pygame.image.load("res/ball_11.png"),

}

# Cargar imágenes de las bolas y escalarlas
ball_sizes = [25,32,50,52,65,85,100,117,192,165,195]  # Tamaños de las bolas
ball_images = {
    size: pygame.transform.scale(pygame.image.load("ball.png"), (size * 2, size * 2))
    for size in ball_sizes
}

# Lista de bolas en el espacio
balls = []


def create_ball(position, radius, space):
    """Crea una nueva bola con imagen en la posición dada"""

    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, radius))
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0
    shape.friction = 1
    shape.collision_type = radius  # Usamos el radio como tipo de colisión
    space.add(body, shape)
    balls.append(shape)
    return shape


def collision_handler(arbiter, space, data):
    """Maneja colisiones entre bolas del mismo tamaño"""
    shape_a, shape_b = arbiter.shapes
    radius = shape_a.radius  # Ambas bolas tienen el mismo radio

    if radius in ball_sizes and ball_sizes.index(radius) < len(ball_sizes) - 1:
        new_radius = ball_sizes[ball_sizes.index(radius) + 1]

        # Posición media entre las dos bolas
        pos_x = (shape_a.body.position.x + shape_b.body.position.x) / 2
        pos_y = (shape_a.body.position.y + shape_b.body.position.y) / 2

        # Eliminar las bolas antiguas
        space.remove(shape_a, shape_a.body, shape_b, shape_b.body)
        balls.remove(shape_a)
        balls.remove(shape_b)

        # Crear la nueva bola más grande
        create_ball((pos_x, pos_y), new_radius,space)

    return False  # Evita que pymunk procese la colisión normalmente


# Crear manejadores de colisión para cada tamaño de bola
for size in ball_sizes:
    handler = bowl.add_collision_handler(size, size)
    handler.begin = collision_handler


# Crear bordes de la pantalla
def create_walls(space):
    static_body = space.static_body
    walls = [
        pymunk.Segment(static_body, (0, HEIGHT), (WIDTH, HEIGHT), 5),
        pymunk.Segment(static_body, (0, 0), (0, HEIGHT), 5),
        pymunk.Segment(static_body, (WIDTH, 0), (WIDTH, HEIGHT), 5)
    ]
    for wall in walls:
        wall.elasticity = 0
        wall.friction = 1
        bowl.add(wall)


create_walls(bowl)

# Bucle principal
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            create_ball(pygame.mouse.get_pos(), ball_sizes[random.randint(0, 3)],bowl)

    bowl.step(1 / 60)

    # Dibujar las bolas con sus imágenes
    for ball in balls:
        x, y = int(ball.body.position.x), int(ball.body.position.y)
        radius = ball.radius
        image = pygame.transform.scale(ball_properties[radius], (radius*2,radius*2))

        # Obtener el ángulo de rotación del cuerpo de la bola
        angle = math.degrees(ball.body.angle)  # Convertir de radianes a grados

        # Rotar la imagen
        rotated_image = pygame.transform.rotate(image, -angle)  # Rotar en sentido antihorario

        # Obtener el nuevo rectángulo para la imagen rotada
        rotated_rect = rotated_image.get_rect(center=(x, y))

        # Mantener la transparencia de la imagen rotada
        rotated_image.set_colorkey((0, 0, 0))  # Establecer el color negro (o el color de fondo) como transparente

        # Dibujar la imagen rotada en la pantalla con transparencia
        screen.blit(rotated_image, rotated_rect.topleft)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()