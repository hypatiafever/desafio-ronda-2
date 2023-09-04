"""Define la Grid (cuadrícula) para dibujar la ronda"""

from constants import *
import openpyxl as xl
from typing import Optional

STEPS_PER_ROUND = ((25, 50, 40, 40, 40, 35, 50, 60, 65, 80),  # Fácil
                   (15, 30, 25, 25, 25, 20, 40, 45, 45, 65),  # Normal
                   (10, 19, 15, 19, 12, 11, 29, 22, 27, 34))  # Difícil


class Cell():
    """Celda en la grilla con su posición (x, y) y su valor."""

    value: Optional[str]

    def __init__(self, x: int, y: int, value: Optional[str] = None):
        self.xy = (x, y)
        self.value = value  # None, "virus", "wall", "player", "dead_virus"

    @property
    def x(self) -> int:
        return self.xy[0]

    @property
    def y(self) -> int:
        return self.xy[1]

    def __str__(self) -> str:
        return f"({self.x}, {self.y}) - value: {self.value}"


class Grid():

    def __init__(self):
        self.cells = [[Cell(x, y) for y in range(GRID_SIZE)]
                      for x in range(GRID_SIZE)]
        self._set_defaults()
        self.round_steps = 0
        self.round_count = 2  # tiene que ser +1
        self.steps_per_round = STEPS_PER_ROUND

    def _set_defaults(self):
        """Reinicializa la grilla"""
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                self.cells[x][y].value = None

        self.protected_zones = []
        # self.portal_blue = [None, None]
        # self.portal_orange = [None, None]
        # self.deactivated_protected_zones = []
        # self.batteries = []
        # self.keys = []
        self.wanderer_virus = []
        # self.corrupted_files = []

    def load_round(self, difficulty: int, round: int):
        """Setea contenido del grid desde un documento .xlsx"""

        self._set_defaults()

        self.round_steps = self.steps_per_round[difficulty][round - 1]

        xlsx_path = f"res/maps/level_{round}.xlsx"
        workbook = xl.load_workbook(xlsx_path)
        sheet_data = workbook.active

        for row in sheet_data.iter_rows():
            for cell in row:
                # las celdas en el documento contienen una string fomateada de la manera
                # que la posición [0] contiene la coordenada "x" y la [3] la "y".
                cell_content = None
                cell_x = int(cell.value[0])
                cell_y = int(cell.value[3])
                if cell.fill.start_color.index == "FFE69138":
                    cell_content = "wall"
                if cell.fill.start_color.index == "FF00FF00":
                    cell_content = "player"
                if cell.fill.start_color.index == "FFFF0000":
                    cell_content = "virus"
                if cell.fill.start_color.index == "FFFFFF00":
                    self.protected_zones.append([cell_x, cell_y])
                # if cell.fill.start_color.index == "FF00FFFF":
                #     self.portal_blue = [cell_x, cell_y]
                # if cell.fill.start_color.index == "FFFF9900":
                #     self.portal_orange = [cell_x, cell_y]
                # if cell.fill.start_color.index == "FF0000FF":
                #     self.batteries.append([cell_x, cell_y])
                if cell.fill.start_color.index == "FF9900FF":
                    self.wanderer_virus.append([cell_x, cell_y])
                    cell_content = "wall"
                if cell.fill.start_color.index == "FFFF00FF":
                    self.wanderer_virus.append([cell_x, cell_y])
                # if cell.fill.start_color.index == "FF4A86E8":
                #     self.keys.append([cell_x, cell_y])
                # if cell.fill.start_color.index == "FF434343":
                #     self.deactivated_protected_zones.append([cell_x, cell_y])
                # if cell.fill.start_color.index == "FFFFD966":
                    # self.corrupted_files.append([cell_x, cell_y])

                self.cells[cell_x][cell_y].value = cell_content

    def detect(self, x: int, y: int) -> dict:
        """Devuelve qué objetos existen el punto dado."""
        point = [x, y]
        exists_in_point = {"wandering_virus": self.wanderer_virus.__contains__(point),
                        #    "corrupted_file": self.corrupted_files.__contains__(point),
                           "protected_zone": self.protected_zones.__contains__(point),
                        #    "deactivated_protected_zone": self.deactivated_protected_zones.__contains__(point),
                        #    "battery": self.batteries.__contains__(point),
                        #    "key": self.keys.__contains__(point)}
        }
        return exists_in_point

    def move_element(self, cell_from: Cell, x_y_to: tuple):
        """Mueve el valor de cell_from a la celda en la coordenada x_y_to"""
        cell_to = self.cells[x_y_to[0]][x_y_to[1]]
        cell_to.value = cell_from.value
        cell_from.value = None
