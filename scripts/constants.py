"""Módulo que contiene constantes globales."""

# medidas
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64
GRID_SIZE = 8

FPS = 60

TEXT_BLOCK_WIDTH = 320
TEXT_BLOCK_HEIGHT = 30

volume_level = 1.0
sensitivity_level = 0.6
MOUSE_MOV_REQ = 100

# colores
WHITE = (255, 255, 255)


# determina el tamaño de la grid en relación a la altura del display
ASPECT_RATIO = (SCREEN_HEIGHT-2*TILE_SIZE)//TILE_SIZE
