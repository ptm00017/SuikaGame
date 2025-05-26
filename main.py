import pygame

from SceneManager import SceneManager, GameState
from SuikaScene import SuikaScene
from Menu import Menu

# Iniciar pygame y el mezclador de sonido
pygame.init()
pygame.mixer.init()

# Iniciar sceneManager y rellenarlo con las pantallas del juego
sceneManager = SceneManager()

sceneManager.addScene(GameState.MENU, Menu(60,(1280, 720)))
sceneManager.addScene(GameState.GAME, SuikaScene(60,(1280, 720)))

try:
    while sceneManager.getScene().isRunning():
        sceneManager.getScene().gameLoop()

        # Cuando se termina el bucle de ejecución del juego, este devuelve es la siguiente escena que se debe mostrar
        sceneManager.changeScene(sceneManager.getScene().getNextGameScene())
except Exception as e:
    print(e)

pygame.quit()