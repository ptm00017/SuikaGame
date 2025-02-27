import pygame
import pymunk
import pymunk.pygame_util

# Tamaño base del juego
GAME_WIDTH = 800
GAME_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Superficie interna donde se dibuja el juego
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

# Espacio de física Pymunk
space = pymunk.Space()
space.gravity = (0, 900)

# Dibujar opciones para Pymunk
draw_options = pymunk.pygame_util.DrawOptions(game_surface)

# Crear el suelo (segmento estático)
static_body = space.static_body
floor = pymunk.Segment(static_body, (0, GAME_HEIGHT - 20), (GAME_WIDTH, GAME_HEIGHT - 20), 5)
floor.elasticity = 0.9  # Rebote alto
space.add(floor)

def create_ball(position):
    """ Crea una nueva pelota en la posición dada """
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 30))
    body.position = position
    shape = pymunk.Circle(body, 30)
    shape.elasticity = 0.8  # Hace que rebote bastante
    space.add(body, shape)

# Crear una pelota inicial
create_ball((400, 100))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_width, current_height = pygame.display.get_window_size()

            # Hacer que los clicks en la pantalla funcionen independientemente de la resolucion de la ventana
            pos_x = event.pos[0] * GAME_WIDTH / current_width;
            pos_y = event.pos[1] * GAME_HEIGHT/ current_height;
            create_ball((pos_x,pos_y))  # Crear pelota en la posición del clic

        elif event.type == pygame.VIDEORESIZE:
            print("Resolucion = "+str(GAME_WIDTH)+", "+str(GAME_HEIGHT))

    # Limpiar la superficie interna
    game_surface.fill((0, 0, 0))

    # Actualizar la física
    space.step(1 / 60.0)

    # Dibujar en la superficie interna
    space.debug_draw(draw_options)

    # Escalar la superficie interna a la pantalla
    window_size = screen.get_size()
    scaled_surface = pygame.transform.smoothscale(game_surface, window_size)

    # Dibujar la imagen escalada en la pantalla
    screen.blit(scaled_surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
