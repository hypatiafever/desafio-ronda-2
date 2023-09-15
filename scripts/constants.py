"""Módulo que contiene constantes y variables globales."""

class GameVars():
    """Nos permite tener las variables globales juntas en un solo objeto."""
    def __init__(self):
        self.volume_level = 10
        self.sensitivity_level = 6

game_vars = GameVars()

# medidas
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64
GRID_SIZE = 8

FPS = 60

TEXT_BLOCK_WIDTH = 320
TEXT_BLOCK_HEIGHT = 30

MOUSE_MOV_REQ = 10

# colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
