"""Define la Grid (cuadrícula) para dibujar la ronda"""

from constants import *
import openpyxl as xl
from typing import Optional
from pygame import Rect
from texturedata import TEXTURES

STEPS_PER_ROUND = ((25, 40, 45, 45, 55, 50, 35, 60, 65, 30),  # Fácil 
                   (18, 30, 35, 35, 45, 35, 25, 45, 45, 20),  # Normal
                   (11, 20, 24, 21, 29, 25, 18, 31, 31, 16))  # Difícil


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
    
class Door(Cell):
    def __init__(self, x: int, y: int, value: str | None = None):
        super().__init__(x, y, value)
        self.turns_to_close = 0
        self.door_textures = [
            TEXTURES["door_0"],
            TEXTURES["door_1"],
            TEXTURES["door_2"],
            TEXTURES["door_3"],
            TEXTURES["door_4"]
        ]
        self.texture = self.door_textures[self.turns_to_close]
        self.value = "closed"
    
    def open(self):
        self.turns_to_close = 4
        self.value = None
        self.texture = self.door_textures[self.turns_to_close]

    def pass_turns(self):
        if self.turns_to_close > 0:
            self.turns_to_close -= 1
        if self.turns_to_close == 0:
            self.value = "closed"
        self.texture = self.door_textures[self.turns_to_close]

class Grid():

    def __init__(self):
        self.cells = [[Cell(x, y) for y in range(GRID_SIZE)]
                      for x in range(GRID_SIZE)]
        self._set_defaults()
        self.round_steps = 0
        self.round_count = 10
        self.steps_per_round = STEPS_PER_ROUND

        self.virus_amount = 0

    def _set_defaults(self):
        """Reinicializa la grilla"""
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                self.cells[x][y].value = None

        self.protected_zones = []
        self.doors = []
        self.wandering_virus_lin = {}
        self.wandering_virus_sin = {}
        self.original_virus_pos = {}
        self.firewall_rects = {}
        self.virus_amount = 0
        self.firewall_amount = 0

    def load_round(self, difficulty: int, round: int):
        """Setea contenido del grid desde un documento .xlsx"""

        self._set_defaults()

        self.round_steps = self.steps_per_round[difficulty][round - 1]

        xlsx_path = f"res/maps/level_{round}.xlsx"
        workbook = xl.load_workbook(xlsx_path)
        sheet_data = workbook.active

        self.virus_amount = 0
        self.firewall_amount = 0

        for row in sheet_data.iter_rows():
            for cell in row:
                # las celdas en el documento contienen una string fomateada de la manera
                # que la posición [0] contiene la coordenada "x" y la [3] la "y".
                cell_content = None
                cell_x = int(cell.value[0])
                cell_y = int(cell.value[3])
                if cell.fill.start_color.index == "FFE69138": 
                    cell_content = "wall"
                if cell.fill.start_color.index == "FF980000": 
                    cell_content = "firewall"
                    self.firewall_amount += 1
                    self.firewall_rects[f"firewall{self.firewall_amount}"] = Rect(TILE_SIZE * cell_x + TILE_SIZE, TILE_SIZE * cell_y + TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if cell.fill.start_color.index == "FF00FF00":
                    cell_content = "player"
                if cell.fill.start_color.index == "FFFF0000":
                    cell_content = "virus"
                if cell.fill.start_color.index == "FFFFFF00":
                    self.protected_zones.append([cell_x, cell_y])
                if cell.fill.start_color.index == "FF9900FF":
                    self.virus_amount += 1
                    self.wandering_virus_lin[f"virus{self.virus_amount}"] = [cell_x, cell_y]
                    self.original_virus_pos[f"virus{self.virus_amount}"] = [cell_x, cell_y]
                    cell_content = "wall"
                if cell.fill.start_color.index == "FFFF00FF":
                    self.virus_amount += 1
                    self.wandering_virus_lin[f"virus{self.virus_amount}"] = [cell_x, cell_y]
                    self.original_virus_pos[f"virus{self.virus_amount}"] = [cell_x, cell_y]
                if cell.fill.start_color.index == "FFA64D79":
                    self.virus_amount += 1
                    self.wandering_virus_sin[f"virus{self.virus_amount}"] = [cell_x, cell_y]
                    self.original_virus_pos[f"virus{self.virus_amount}"] = [cell_x, cell_y]
                if cell.fill.start_color.index == "FF46BDC6":
                    self.virus_amount += 1
                    self.wandering_virus_sin[f"virus{self.virus_amount}"] = [cell_x, cell_y]
                    self.original_virus_pos[f"virus{self.virus_amount}"] = [cell_x, cell_y]
                    cell_content = "wall"
                if cell.fill.start_color.index == "FF434343":
                    self.doors.append(Door(cell_x, cell_y, "closed"))
                #434343 door color

                self.cells[cell_x][cell_y].value = cell_content

    def detect(self, x: int, y: int) -> dict:
        """Devuelve qué objetos existen el punto dado."""
        point = [x, y]

        exists_in_point = {"wandering_virus_lin": point in self.wandering_virus_lin.values(),
                           "wandering_virus_sin": point in self.wandering_virus_sin.values(),
                           "protected_zone": self.protected_zones.__contains__(point),
                           }
        return exists_in_point

    def is_there_firewall(self, point: tuple) -> str:
        newpoint = (point[0], point[1])
        for firewall, rect in self.firewall_rects.items():
            if rect.collidepoint(newpoint):
                return firewall
        return ""
    
    def is_there_door(self, point:tuple) -> Door | None:
        for door in self.doors:
            if door.x == point[0] and door.y == point[1]:
                return door
        return None
    
    def move_element(self, cell_from: Cell, x_y_to: tuple):
        """Mueve el valor de cell_from a la celda en la coordenada x_y_to"""
        cell_to = self.cells[x_y_to[0]][x_y_to[1]]
        cell_to.value = cell_from.value
        cell_from.value = None
