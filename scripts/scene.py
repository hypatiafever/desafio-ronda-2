"""Scene controla todos los elementos del juego.

Se encarga de los eventos, renderizado y lógica general del juego."""

import random as rng
import pygame
from audio import AudioHandler
from constants import *
from grid import Grid
from gui import Menu, Pause
from pygame import Surface
from texturedata import TEXTURES


class Scene(object):

    def __init__(self, screen: Surface, menu: Menu, pause: Pause):

        # define los tamaños de las fuentes para la gui
        pygame.font.init()
        self.small_font = pygame.font.Font("res/font/PixelOperator.ttf", 38)
        self.large_font = pygame.font.Font("res/font/PixelOperator.ttf", 48)

        self.screen = screen
        self.menu = menu
        self.pause = pause
        self.audio_player: AudioHandler = AudioHandler()
        self.used_steps = 0
        self.robots = [
            "UAIBOT",
            "UAIBOTA",
            "UAIBOTINO",
        ]

        self.grid = Grid()
        # dibuja fondo verde en pantalla
        self.grid_background: Surface = Surface(
            (TILE_SIZE * 8, TILE_SIZE * 8))
        self.grid_background.fill("darkgreen")

        self.round = 0
        self.intro_finished = False
        self.difficulty_set = False
        self.difficulty = 0

        self.player_cell = None
        self.dead = False
        self.intro_frame_num = 2
        # define la textura de los virus al azar
        self.virus_index = rng.randint(1, 5)
        self.show_rules = False

    def update(self, in_rounds: bool, paused: bool):
        """Actualiza el comportamiento de la escena."""
        self.draw(in_rounds, paused)
        self.check_finished()
        self.dead_state()

    # region --- Draws ---

    def draw(self, in_rounds: bool, paused: bool):
        """Se encarga del renderizado general."""

        grid: Grid = self.grid
        screen: Surface = self.screen
        screen.fill("white")
        screen.blit(TEXTURES["background"], (0, 0))

        # si se está en una ronda del juego, la dibuja
        if (in_rounds and self.difficulty_set and not paused):
            screen.blit(self.grid_background, (TILE_SIZE, TILE_SIZE))
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):

                    tile_position = (TILE_SIZE*x + TILE_SIZE,
                                     TILE_SIZE*y + TILE_SIZE)
                    # "+ TILESIZE" compensa por los márgenes
                    content_dict = grid.detect(x, y)

                    if content_dict["protected_zone"]:
                        screen.blit(
                            TEXTURES["protected_zone"], tile_position)
                    # if content_dict["deactivated_protected_zone"]:
                    #     screen.blit(
                    #         TEXTURES["deactivated_protected_zone"], tile_position)
                    # if content_dict["key"]:
                    #     screen.blit(
                    #         TEXTURES["key"], tile_position)
                    # if grid.portal_blue == [x, y]:
                    #     screen.blit(
                    #         TEXTURES["portal_blue"], tile_position)
                    # if grid.portal_orange == [x, y]:
                    #     screen.blit(
                    #         TEXTURES["portal_orange"], tile_position)
                    # if content_dict["battery"]:
                    #     screen.blit(
                    #         TEXTURES["battery"], tile_position)
                    if grid.cells[x][y].value == "player":
                        screen.blit(
                            TEXTURES[self.robots[0]], tile_position)
                        self.player_cell = grid.cells[x][y]
                    if grid.cells[x][y].value == "wall":
                        screen.blit(
                            TEXTURES["wall"], tile_position)
                    if grid.cells[x][y].value == "virus":
                        screen.blit(TEXTURES[f"virus{self.virus_index}"],
                                    tile_position)
                    if grid.cells[x][y].value == "dead_virus":
                        screen.blit(
                            TEXTURES[f"virus{self.virus_index}_dead"], tile_position)
                    if content_dict["wandering_virus"]:
                        screen.blit(
                            TEXTURES["wandering_virus"], tile_position)
                    # if content_dict["corrupted_file"]:
                    #     screen.blit(
                    #         TEXTURES["corrupted_file"], tile_position)

            # region --- GUI ---

            grid_end_area = (GRID_SIZE * TILE_SIZE + TILE_SIZE, GRID_SIZE * TILE_SIZE + TILE_SIZE)
            mouse_pos = pygame.mouse.get_pos()
            mouse_above_grid_end = mouse_pos[0] < grid_end_area[0] and mouse_pos[1] < grid_end_area[1]
            mouse_below_grid_start = mouse_pos[0] > TILE_SIZE and mouse_pos[1] > TILE_SIZE
            if mouse_above_grid_end and mouse_below_grid_start:
                pygame.mouse.set_visible(False)
                screen.blit(TEXTURES["mouse_crosshair"], (mouse_pos[0] - TILE_SIZE // 2, mouse_pos[1] - TILE_SIZE // 2))
            else:
                pygame.mouse.set_visible(True)

            x = 672

            self.screen.blit(
                TEXTURES["text_background_2"], (x, 128, 156, 46))
            step_text = self.small_font.render(
                f"Ronda {self.round}", False, WHITE)
            self.screen.blit(
                step_text, (677, 128, TEXT_BLOCK_WIDTH, TEXT_BLOCK_HEIGHT))

            self.screen.blit(
                TEXTURES["text_background_1"], (x, 320, 400, 46))
            step_text = self.small_font.render(
                f"Movimientos utilizados: {self.used_steps}", False, WHITE)
            self.screen.blit(
                step_text, (677, 320, TEXT_BLOCK_WIDTH, TEXT_BLOCK_HEIGHT))

            self.screen.blit(
                TEXTURES["text_background_1"], (x, 384, 400, 46))
            remaining_steps_text = self.small_font.render(
                f"Movimientos restantes: {self.grid.round_steps - self.used_steps}", False, WHITE)
            self.screen.blit(
                remaining_steps_text, (677, 384, TEXT_BLOCK_WIDTH, TEXT_BLOCK_HEIGHT))

            # if self.round == 2:
            #     self.screen.blit(
            #         TEXTURES["safe_zones_rules"], (x, 450, 600, 80))
            # if self.round == 3:
            #     self.screen.blit(
            #         TEXTURES["portal_rules"], (x, 450, 600, 90))
            # if self.round == 4:
            #     self.screen.blit(
            #         TEXTURES["battery_rules"], (x, 450, 600, 90))
            # if self.round == 5:
            #     self.screen.blit(
            #         TEXTURES["wandering_virus_rules"], (x, 450, 600, 90))
            # if self.round == 6:
            #     self.screen.blit(
            #         TEXTURES["key_rules"], (x, 450, 600, 90))
            # if self.round == 7:
            #     self.screen.blit(
            #         TEXTURES["corrupted_folder_rules"], (x, 450, 600, 90))

            # endregion

        # Dibuja el menu y reproduce la musica correspondiente
        if not self.difficulty_set:
            self.menu.draw(self.screen)
            self.audio_player.play_music("res/sounds/menu-theme.mp3")
        else:
            self.audio_player.play_music("res/sounds/main-theme.mp3")

        # Dibuja la pausa y controla el volumen de la musica
        if paused:
            if not self.show_rules:
                self.pause.draw(self.screen)
                self.audio_player.lower_music_vol()
        else:
            self.audio_player.reset_music_vol()

        if self.round < 1 and self.difficulty_set:
            self.draw_intro()

        if self.round > grid.round_count:
            self.draw_win()

        if self.show_rules:
            self.screen.blit(
                TEXTURES["game_rules"], (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw_intro(self):
        """Renderiza la introducción en pantalla."""
        if self.intro_frame_num < 7:
            self.screen.blit(
                TEXTURES[f"intro_frame{self.intro_frame_num}"], (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(
                TEXTURES["press_any_black"], (SCREEN_WIDTH - 450, SCREEN_HEIGHT - 45, 450, 50))
        elif self.intro_frame_num == 7:
            self.screen.blit(
                TEXTURES["game_rules"], (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(
                TEXTURES["press_any_white"], (SCREEN_WIDTH - 450, SCREEN_HEIGHT - 45, 450, 50))

    def draw_win(self):
        """Renderiza en pantalla el mensaje de haber ganado."""
        self.screen.blit(
            TEXTURES["win"], (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    # endregion

    # region --- Checks ---

    def check_finished(self) -> bool:
        """True si todos los virus fueron atrapados y pasa a la siguiente ronda"""
        protected_zones_count = len(self.grid.protected_zones)
            # len(self.grid.deactivated_protected_zones)

        if self.intro_finished:

            done_virus = 0

            for pos in self.grid.protected_zones:
                x = pos[0]
                y = pos[1]
                if self.grid.cells[x][y].value == "dead_virus":
                    done_virus += 1
                if self.grid.cells[x][y].value == "virus":
                    done_virus += 1
                    self.grid.cells[x][y].value = "dead_virus"
                    self.audio_player.play_sound(
                        "res/sounds/kill-virus.wav")

            if done_virus == protected_zones_count:
                self.round += 1

                if self.round < self.grid.round_count:
                    self.virus_index = rng.randint(1, 5)
                    self.grid.load_round(self.difficulty, self.round)
                    self.used_steps = 0
                return True

        return False

    # def check_kill_player(self):
    #     """Determina si el jugador es atacado por el virus y activa la condición de muerto del jugador."""
    #     for virus in self.grid.wanderer_virus:
    #         if virus[0] != None:
    #             if self.grid.cells[virus[0]][virus[1]].value == "player":
    #                 self.audio_player.interrupt_music(
    #                     "res/sounds/main-theme.mp3", "res/sounds/lost.wav")
    #                 self.dead = True

    # def check_batteries(self):
    #     """Determina si las baterías son obtenidas por el jugador."""
    #     if self.intro_finished:
    #         for pos in self.grid.batteries:
    #             x = pos[0]
    #             y = pos[1]
    #             if self.grid.cells[x][y] == self.player_cell:
    #                 # una vez obtenidas las baterías son eliminadas
    #                 self.audio_player.play_sound("res/sounds/battery.wav")
    #                 self.grid.batteries.remove(pos)
    #                 self.grid.round_steps += 10

    # def check_corrupted_file(self):
    #     """Determina si las carpetas corruptas son tocadas por el jugador."""
    #     if self.intro_finished:
    #         for pos in self.grid.corrupted_files:
    #             x = pos[0]
    #             y = pos[1]
    #             if self.grid.cells[x][y] == self.player_cell:
    #                 # una vez obtenidas las carpetas corruptas son eliminadas
    #                 self.audio_player.play_sound(
    #                     "res/sounds/corrupted-file.wav")

    #                 self.grid.corrupted_files.remove(pos)
    #                 self.update_steps(5)

    # def check_keys(self):
    #     """Determina si se han conseguido todas las keys (pendrive), eliminándolas a medida que se consiguen."""
    #     got_all_keys = False

    #     if self.intro_finished:
    #         for pos in self.grid.keys:
    #             x = pos[0]
    #             y = pos[1]
    #             if self.grid.cells[x][y].value == "player":
    #                 self.grid.keys.remove(pos)
    #                 if len(self.grid.keys) == 0:
    #                     got_all_keys = True

    #     if got_all_keys:
    #         self.grid.protected_zones = self.grid.deactivated_protected_zones
    #         self.grid.deactivated_protected_zones = []

    # endregion

    def move_wandering_virus(self):
        """Controla el movimiento del virus que ataca al jugador."""
        for virus in self.grid.wanderer_virus:
            if virus[0] != None:
                if virus[0] != 0:
                    virus[0] -= 1
                else:
                    virus[0] = 7

    # def teleport_blue_orange(self):
    #     """Mueve el player desde el portal azul hasta el naranja."""
    #     if self.grid.portal_blue[0] != None:
    #         if self.grid.cells[self.grid.portal_blue[0]][self.grid.portal_blue[1]].value == "player":
    #             self.audio_player.play_sound(
    #                 "res/sounds/enter-portal.wav")
    #             self.grid.move_element(
    #                 self.player_cell, self.grid.portal_orange)

    # def teleport_orange_blue(self):
    #     """Mueve el player desde el portal naranja hasta el azul."""
    #     if self.grid.portal_orange[0] != None:
    #         if self.grid.cells[self.grid.portal_orange[0]][self.grid.portal_orange[1]].value == "player":

    #             self.audio_player.play_sound(
    #                 "res/sounds/enter-portal.wav")
    #             self.grid.move_element(
    #                 self.player_cell, self.grid.portal_blue)

    # region --- Event Handling ---

    def move(self, direction: str):
        """Maneja el movimiento del jugador, realiza las computaciones
        relacionadas con este y sus consecuencias y activa el avance del turno."""
        if not self.dead:
            offset_x = 0
            offset_y = 0
            if direction == "right":
                offset_x = 1
            elif direction == "left":
                offset_x = -1
            elif direction == "up":
                offset_y = -1
            elif direction == "down":
                offset_y = 1

            farther_offset_x = offset_x * 2
            farther_offset_y = offset_y * 2

            map_values = self.grid.cells

            moved = False

            # celda siguiente a la dirección del movimiento
            next_cell = map_values[self.player_cell.x +
                                   offset_x][self.player_cell.y+offset_y]
            # celda anterior a la dirección del movimiento
            prev_cell = map_values[self.player_cell.x -
                                   offset_x][self.player_cell.y-offset_y]

            if next_cell.x != 7 and next_cell.y != 7:  # evita un chequeo mas allá del borde
                # celda dos bloques mas allá en la dirección del movimiento
                farther_cell = map_values[self.player_cell.x +
                                          farther_offset_x][self.player_cell.y+farther_offset_y]
            else:
                farther_cell = next_cell

            if self.robots[0] == "UAIBOT":

                if next_cell.value is None:
                    self.grid.move_element(
                        self.player_cell, next_cell.xy)
                    self.audio_player.play_sound("res/sounds/move.wav")
                    moved = True

                if next_cell.value == "virus" and not farther_cell.value in {"wall", "virus", "dead_virus"}:
                    self.grid.move_element(next_cell, farther_cell.xy)
                    self.grid.move_element(
                        self.player_cell, next_cell.xy)
                    self.audio_player.play_sound("res/sounds/move.wav")
                    moved = True

            if self.robots[0] == "UAIBOTA":

                if next_cell.value is None:
                    self.grid.move_element(
                        self.player_cell, next_cell.xy)
                    self.audio_player.play_sound("res/sounds/move.wav")
                    moved = True
                    if prev_cell.value == "virus":
                        self.grid.move_element(
                            prev_cell, self.player_cell.xy)

            if self.robots[0] == "UAIBOTINO":
                if next_cell.value is None:
                    self.grid.move_element(
                        self.player_cell, next_cell.xy)
                    moved = True
                    self.audio_player.play_sound("res/sounds/move.wav")

                if next_cell.value == "virus" and not farther_cell.value in {"wall", "virus", "dead_virus"}:
                    self.grid.move_element(
                        self.player_cell, farther_cell.xy)
                    self.audio_player.play_sound("res/sounds/jump.wav")

                    # como UAIBOTINO se mueve dos celdas en vez de una en este caso, la celda próxima a la que se
                    # actualizará su posición corresponde a la celda siguiente a esta
                    next_cell = farther_cell
                    moved = True

            if moved:
                # actualiza la posición del player con el movimiento realizado
                self.player_cell = next_cell

                self.move_wandering_virus()
                # self.check_keys()
                # self.teleport_blue_orange()
                # self.teleport_orange_blue()
                # self.check_batteries()
                # self.check_corrupted_file()
                passed_round = self.check_finished()
                # self.check_kill_player()
                if not passed_round:  # esto hace que el contador de turnos no llegue a cero si se gana con el último movimiento
                    self.update_steps(1)

    def restart(self):
        """Devuelve todo al estado inicial de la ronda."""
        if self.round > 0:
            self.grid.load_round(self.difficulty, self.round)

            self.used_steps = 0
            self.robots = [
                "UAIBOT",
                "UAIBOTA",
                "UAIBOTINO",
            ]
            self.dead = False

    def reset_game(self):
        """Reinicia el juego desde el principio."""
        self.round = 0
        self.intro_finished = False
        self.difficulty_set = False
        self.difficulty = 0
        self.audio_player.stop_music()

    def update_steps(self, steps_delta: int):
        """Maneja el sistema de turnos, haciendo el avance y el reseteo en caso de que se terminen los movimientos habilitados."""
        self.used_steps += steps_delta

        if self.used_steps >= self.grid.round_steps:
            self.restart()
            self.audio_player.interrupt_music(
                "res/sounds/main-theme.mp3",
                "res/sounds/lost.wav")

    def change_robot(self):
        """Ejecuta la rotación entre los robots."""
        self.robots.append(self.robots[0])
        self.robots.pop(0)

    def dead_state(self):
        """Cuando el jugador muere notifica al usuario con un mensaje en pantalla."""
        if self.dead:
            self.screen.blit(
                TEXTURES["text_background_3"], (SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2 - 50, 600, 100))

    # endregion
