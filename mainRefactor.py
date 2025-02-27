import pygame
from CubeScene import CubeScene

pygame.init()
screen = pygame.display.set_mode((800, 600))

scene = CubeScene(screen)  # Cambia a BallScene(screen) para probar la bola
scene.gameLoop()
pygame.quit()