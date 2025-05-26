import pygame
import pymunk
import pymunk.pygame_util
import random

from Button import Button
from Scene import GameScene
from Fruit import Fruit
from SceneManager import GameState


class SuikaScene(GameScene):

    def __init__(self, framerate=60):
        super().__init__(framerate)

        # Inicializar espacio de físicas
        self.space = pymunk.Space()
        self.space.gravity = (0, 1300)  # Gravedad hacia abajo

        handler = self.space.add_collision_handler(1, 1)  # Colision de frutas
        handler.begin = self.collision_handler

        self.draw_options = pymunk.pygame_util.DrawOptions(self.surface)
        self.balls = []

        # Crear bordes del contenedor
        self.width, self.height = 750, 670
        self.half_width, self.half_height = (self.surface.get_width() - self.width) / 2, (
                self.surface.get_height() - self.height) / 2
        self.create_container()

        # Puntuacion
        self.score = 0
        self.font = pygame.font.Font(None, 72)
        self.font_pos = (100, 200)

        # Cooldown para la generacion de frutas
        self.generator_cooldown = 500  # En milisegundos
        self.last_generation_time = 0

        # Variables para la cola de frutas a caer
        self.max_fruit_type = 5  # Fruta maxima que puede aparecer de forma aleatoria
        self.queue_img_size = 200  # Resolucion de la imagen de la cola de frutas

        self.next_fruit_images = {}
        for i in range(1, self.max_fruit_type + 1):
            self.next_fruit_images[i] = pygame.image.load(Fruit.fruit_properties[i]["image_path"])

            # Pequeña funcion matemática para escalar la imagen de la fruta
            min_fruit_scale_factor = 0.3  # Establecer el tamaño de la imagen de la fruta más pequeña
            scale_factor = min_fruit_scale_factor + (1 - min_fruit_scale_factor) * (
                        i / self.max_fruit_type)

            # Escalar la imagen al tamaño de queue_img_res
            aspect_ratio = self.next_fruit_images[i].get_width() / self.next_fruit_images[i].get_height()
            fruit_img_res = (self.queue_img_size * aspect_ratio * scale_factor, self.queue_img_size * scale_factor)
            self.next_fruit_images[i] = pygame.transform.smoothscale(self.next_fruit_images[i], fruit_img_res)


        self.current_fruit = random.randint(1, self.max_fruit_type)
        self.next_fruit = random.randint(1, self.max_fruit_type)

        # Variables de eventos
        self.mouse_button_down = False
        self.mouse_pos = None
        self.is_game_over = False

        # Interfaz
        self.back_button = Button(1650, 40, "res/img/button_back.png", GameState.MENU)
        self.restart_button = Button(1650, 280, "res/img/button_restart.png", None)

        # Imagenes
        self.game_over_image = pygame.image.load("res/img/game_over.png")

        # Musica
        self.balls_sound = pygame.mixer.Sound("res/sounds/balls_clash.ogg")

    def handleUserInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_down = True
                self.mouse_pos = self._correctMousePos(event.pos)
            else:
                self.mouse_button_down = False
                self.mouse_pos = None

    def handlePause(self):
        pass

    def update(self, deltaTime):
        if (self.mouse_button_down and self.mouse_pos is not None):
            if not self.is_game_over:
                # Cooldown para la generacion de frutas
                current_time = pygame.time.get_ticks()
                # Si no ha pasado el tiempo de cooldown, no generamos la fruta
                if not (current_time - self.last_generation_time < self.generator_cooldown):
                    self.last_generation_time = current_time
                    was_ball_created = self.generate_new_ball(self.mouse_pos, self.next_fruit)

                    if was_ball_created:
                        # Cambiar la fruta actual a la siguiente
                        self.current_fruit = self.next_fruit
                        self.next_fruit = random.randint(1, self.max_fruit_type)

            if self.back_button.is_clicked(self.mouse_pos):
                self.nextGameScene = self.back_button.sceneEnum
                self.running = False

            if self.restart_button.is_clicked(self.mouse_pos):
                self.__init__(self.framerate)

        if not self.is_game_over:
            self.space.step(deltaTime)

    def draw(self):
        # Dibujar limites del contenedor
        for shape in self.space.shapes:
            if isinstance(shape, pymunk.Segment):  # Verifica si es una pared
                start_pos = (int(shape.a.x), int(shape.a.y))
                end_pos = (int(shape.b.x), int(shape.b.y))
                pygame.draw.line(self.surface, (0, 0, 0), start_pos, end_pos, 2)  # Dibuja una línea negra

        # Dibujar frutas
        for ball in self.balls:
            ball.draw(self.surface)

        # Dibujar la imagen de la siguiente fruta con escala
        next_fruit_image = self.next_fruit_images[self.next_fruit]
        min_fruit_scale_factor = 0.3  # Para cambiar el tamaño de la imagen de la fruta más pequeña
        scale_factor = min_fruit_scale_factor + (1 - min_fruit_scale_factor) * (self.next_fruit / self.max_fruit_type)

        # Calcular dimensiones escaladas manteniendo la relación de aspecto
        #aspect_ratio = next_fruit_image.get_width() / next_fruit_image.get_height()
        #scaled_width = int(self.queue_img_res[0] * aspect_ratio)
        #scaled_height = int(self.queue_img_res[1])

        #scaled_image = pygame.transform.smoothscale(next_fruit_image, (scaled_width, scaled_height))

        next_fruit_x = self.half_width + self.width + 50  # Posición a la derecha del contenedor
        next_fruit_y = self.half_height + self.height // 2 - next_fruit_image.get_height() // 2  # Centrado verticalmente
        self.surface.blit(next_fruit_image, (next_fruit_x, next_fruit_y))

        # Interfaz
        # Dibujar la puntuacion
        texto = self.font.render(str(self.score), True, (0, 0, 0))
        self.surface.blit(texto, (100 - texto.get_width() // 2, 100 - texto.get_height() // 2))

        # Dibujar pantalla de Game Over
        if (self.is_game_over):
            self.surface.blit(self.game_over_image, (400, 0))

        # Botones
        self.restart_button.draw(self.surface)
        self.back_button.draw(self.surface)

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

            # Acutalizar la puntuacion
            self.score += Fruit.fruit_properties[fruit_type]["points"]

            # Crear la nueva bola más grande
            self.create_ball((pos_x, pos_y), fruit_type + 1)

            # Reproducir sonido de colisión
            if self.balls_sound.get_num_channels() == 0:
                previous_volume = pygame.mixer.music.get_volume()
                pygame.mixer_music.set_volume(0.4)

                self.balls_sound.play()

                pygame.mixer_music.set_volume(previous_volume)
            return False  # Evita que pymunk procese la colisión normalmente
        else:
            # Comprueba si las frutas que han chocado han rebasado el contenedor
            if shape_a.body.position.y < self.half_height \
                    or shape_b.body.position.y < self.half_height:
                self.is_game_over = True

            return True  # Retorna True para que pymunk procese la colisión normalmente

    def create_ball(self, position, fruit_type):
        if position is None:
            return

        fruit_type = min(fruit_type, len(Fruit.fruit_properties))
        fruit = Fruit(position, fruit_type)

        self.space.add(fruit.body, fruit)
        self.balls.append(fruit)

    def generate_new_ball(self, position, fruit_type):

        if position is None:
            return False

        x, y = position
        fruit_type = min(fruit_type, len(Fruit.fruit_properties))
        radius = Fruit.fruit_properties[fruit_type]["radius"]

        # Verificar si la posición x está dentro del rango del contenedor
        if x < self.half_width or x > self.half_width + self.width:
            return False

        # Ajustar la posición si está cerca de los bordes del contenedor
        if x - radius < self.half_width:
            x = self.half_width + radius
        elif x + radius > self.half_width + self.width:
            x = self.half_width + self.width - radius

        # Generar la fruta justo encima del contenedor
        y = self.half_height - radius - 10

        fruit = Fruit((x, y), fruit_type)
        self.space.add(fruit.body, fruit)
        self.balls.append(fruit)

        return True
