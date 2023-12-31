"""Scene controla todos los elementos del juego.

Se encarga de los eventos, renderizado y lógica general del juego."""


from math import sin, trunc
from random import randint
from time import time

import pygame
from audio import AudioHandler
from constants import *
from grid import Grid
from menus import MovementsMenu, NameMenu, OptionsMenu, PauseMenu, StartMenu
from pygame import Surface
from texturedata import TEXTURES
from settings import GameSettings


class Scene(object):

    def __init__(self, screen: Surface, audio_handler: AudioHandler,
                 movement_menu: MovementsMenu,
                 pause_menu: PauseMenu,
                 name_menu: NameMenu,
                 start_menu: StartMenu,
                 options_menu: OptionsMenu,
                 settings: GameSettings):

        # define los tamaños de las fuentes para la gui
        pygame.font.init()
        self.small_font = pygame.font.Font("res/font/PixelOperator.ttf", 38)
        self.large_font = pygame.font.Font("res/font/PixelOperator.ttf", 48)

        self.screen = screen
        self.audio_handler = audio_handler

        self.start_menu = start_menu
        self.name_menu = name_menu
        self.movement_menu = movement_menu
        self.pause_menu = pause_menu
        self.options_menu = options_menu
        self.settings = settings

        self.used_steps = 0
        self.steps_used_per_round = []
        self.time_spent_per_round = []

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

        self.round = -3
        self.intro_finished = False
        self.difficulty_set = False
        self.difficulty = 0

        self.player_cell = None
        self.dead = False
        self.intro_frame_num = 2
        # define la textura de los virus al azar
        self.virus_index = randint(1, 4)
        self.show_rules = False
        self.show_options = False
        self.won_game = False

        self.start_time = 0
        self.current_time = 0
        self.elapsed_time = 0
        self.time_limit = 55
        self.timer = self.time_limit

        self.door_turns = 0

    def update(self, in_rounds: bool, paused: bool):
        """Actualiza el comportamiento de la escena."""
        self.draw(in_rounds, paused)
        self.check_finished()
        self.check_kill_player()
        if in_rounds:
            self.run_timer(paused)
        if self.dead:
            self.dead_state()

    def run_timer(self, paused):
        """Maneja el funcionamiento del timer del juego"""
        if self.start_time == 0:
            self.start_time = time()

        # delta_time nos permite que tanto el tiempo de comienzo y el tiempo
        # actual avancen a la vez para simular una pausa
        delta_time = time() - self.current_time
        self.current_time = time()
        if paused:
            self.start_time += delta_time
        if not self.dead and not paused:
            self.elapsed_time = self.current_time - self.start_time
            self.timer = self.time_limit - self.elapsed_time

        if self.timer <= 0:
            self.dead_state()

    def update_timer_bar(self) -> list:
        """Maneja la barra de progreso del timer y devuelve los elementos para dibujarla."""
        timer_full_w = 400
        bg_rect = pygame.Rect(SCREEN_WIDTH // 2 - 416 // 2, 12, 416, 40)
        fg_rect = pygame.Rect(SCREEN_WIDTH // 2 -
                              timer_full_w // 2, 20, timer_full_w, 24)

        time_left = (self.time_limit - self.elapsed_time) / self.time_limit
        fg_rect.w *= time_left

        time_percentage = trunc(time_left * 100)
        percentage_text = self.small_font.render(
            f"{time_percentage}%", False, WHITE)
        percentage_rect = percentage_text.get_rect()
        percentage_rect.center = bg_rect.center

        return bg_rect, (172, 89, 106), fg_rect, (102, 41, 53), percentage_text, percentage_rect

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
                    door = grid.is_there_door((x, y))
                    if door:
                        screen.blit(door.texture, tile_position)
                    if content_dict["protected_zone"]:
                        screen.blit(
                            TEXTURES["protected_zone"], tile_position)
                    if grid.cells[x][y].value == "player":
                        screen.blit(
                            TEXTURES[self.robots[0]], tile_position)
                        self.player_cell = grid.cells[x][y]
                    if grid.cells[x][y].value == "wall":
                        screen.blit(
                            TEXTURES["wall"], tile_position)
                    if grid.cells[x][y].value == "firewall":
                        screen.blit(
                            TEXTURES["firewall"], tile_position)
                    if grid.cells[x][y].value == "virus":
                        screen.blit(TEXTURES[f"virus{self.virus_index}"],
                                    tile_position)
                    if grid.cells[x][y].value == "dead_virus":
                        screen.blit(
                            TEXTURES[f"virus{self.virus_index}_dead"], tile_position)
                    if content_dict["wandering_virus_lin"]:
                        screen.blit(
                            TEXTURES["wandering_virus_lin"], tile_position)
                    if content_dict["wandering_virus_sin"]:
                        screen.blit(
                            TEXTURES["wandering_virus_sin"], tile_position)
                timer_bar = self.update_timer_bar()
                pygame.draw.rect(screen, timer_bar[1], timer_bar[0])
                pygame.draw.rect(screen, timer_bar[3], timer_bar[2])
                screen.blit(timer_bar[4], timer_bar[5])

            # region --- GUI ---

            if self.round == 1:
                self.screen.blit(
                    TEXTURES["sin_virus_rules"], (672, 450))
            if self.round == 2:
                self.screen.blit(
                    TEXTURES["click_virus"], (672, 450))
            if self.round == 3:
                self.screen.blit(
                    TEXTURES["firewall_rules"], (672, 450))
            if self.round == 6:
                self.screen.blit(
                    TEXTURES["door_rules"], (672, 450))
                
            if in_rounds:
                self.screen.blit(
                    TEXTURES["pause_rules"], (672, TILE_SIZE))

            grid_end_area = (GRID_SIZE * TILE_SIZE + TILE_SIZE,
                             GRID_SIZE * TILE_SIZE + TILE_SIZE)
            mouse_pos = pygame.mouse.get_pos()
            mouse_above_grid_end = mouse_pos[0] < grid_end_area[0] and mouse_pos[1] < grid_end_area[1]
            mouse_below_grid_start = mouse_pos[0] > TILE_SIZE and mouse_pos[1] > TILE_SIZE
            if mouse_above_grid_end and mouse_below_grid_start:
                pygame.mouse.set_visible(False)
                screen.blit(TEXTURES["mouse_crosshair"], (mouse_pos[0] -
                            TILE_SIZE // 2, mouse_pos[1] - TILE_SIZE // 2))
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

            timer_text = self.small_font.render(
                f"Tiempo restante: {trunc(self.timer)}", False, WHITE
            )
            self.screen.blit(
                timer_text, (0, 0, TEXT_BLOCK_WIDTH, TEXT_BLOCK_HEIGHT))

            # endregion

        if self.round == -3:  # start menu
            self.start_menu.draw(screen)
            self.audio_handler.play_music("res/sounds/menu-theme.mp3")

        if self.round == -2:  # menú de definición del nombre del jugador
            self.name_menu.draw()

        if self.round == -1:  # menú de elección de movimientos
            self.movement_menu.draw(self.screen)

        # Dibuja la pausa y controla el volumen de la musica
        if paused:
            pygame.mouse.set_visible(True)
            if not self.show_rules and not self.show_options:
                self.pause_menu.draw(self.screen)
        
        if paused or self.show_options or self.show_rules:
            self.audio_handler.lower_music_vol()
        else:
            self.audio_handler.reset_music_vol()

        if self.round < 1 and self.difficulty_set:
            self.draw_intro()
        if self.won_game:
            self.draw_win()

        if self.show_rules:
            self.screen.blit(
                TEXTURES["game_rules"], (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        if self.show_options:
            self.options_menu.draw(self.screen)

    def draw_intro(self):
        """Renderiza la introducción en pantalla."""
        if self.intro_frame_num < 6:
            self.screen.blit(
                TEXTURES[f"intro_frame{self.intro_frame_num}"], (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(
                TEXTURES["press_any_black"], (SCREEN_WIDTH - 450, SCREEN_HEIGHT - 45, 450, 50))
        elif self.intro_frame_num == 6:
            self.screen.blit(
                TEXTURES["game_rules"], (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(
                TEXTURES["press_any_white"], (SCREEN_WIDTH - 450, SCREEN_HEIGHT - 45, 450, 50))

    def continue_intro(self):
        """Maneja el pasar de los frames de la intro."""
        if self.intro_frame_num < 6:  # pasa al siguiente frame o termina la animaciòn
            self.intro_frame_num += 1
        else:
            self.intro_finished = True
            self.audio_handler.stop_music()
            self.audio_handler.play_music("res/sounds/main-theme.mp3")

    def draw_win(self):
        pygame.mouse.set_visible(True)
        """Renderiza en pantalla el mensaje de haber ganado."""
        self.screen.blit(
            TEXTURES["win"], (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(
            TEXTURES["r_return"], (SCREEN_WIDTH // 2 - 590 // 2, SCREEN_HEIGHT //
                                   2 + 300 - sin(pygame.time.get_ticks() / 100) * 10)
        )
        congrats_text = self.large_font.render(
            "Felicidades, has ganado", False, WHITE)
        congrats_rect = congrats_text.get_rect(
            centerx=SCREEN_WIDTH // 2, centery=70)
        player_name_text = self.large_font.render(
            self.settings.username, False, WHITE)
        player_name_rect = player_name_text.get_rect(
            centerx=SCREEN_WIDTH // 2, centery=player_name_text.get_rect().h + 80)

        self.screen.blit(congrats_text, congrats_rect)
        self.screen.blit(player_name_text, player_name_rect)

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
                    self.audio_handler.play_sound(
                        "res/sounds/kill-virus.wav")

            if done_virus == protected_zones_count and self.round <= self.grid.round_count:

                if self.round >= 1:
                    self.steps_used_per_round.append(self.used_steps)
                    self.time_spent_per_round.append(self.elapsed_time)

                self.round += 1

                if self.round <= self.grid.round_count:
                    self.virus_index = randint(1, 4)
                    self.grid.load_round(self.difficulty, self.round)
                    self.start_time = 0
                    self.current_time = 0
                    self.elapsed_time = 0
                    self.timer = self.time_limit
                    self.used_steps = 0
                return True

        return False

    def check_kill_player(self):
        """Determina si el jugador es atacado por el virus y activa la condición de muerto del jugador."""
        all_moving_virus = {}
        all_moving_virus.update(self.grid.wandering_virus_lin)
        all_moving_virus.update(self.grid.wandering_virus_sin)
        for virus in all_moving_virus.values():
            if virus[0] != None:
                if self.grid.cells[virus[0]][virus[1]].value == "player" and not self.dead:
                    self.dead = True
                    self.audio_handler.interrupt_music(
                        "res/sounds/main-theme.mp3", "res/sounds/lost.wav")

    def check_and_break_firewall(self, pos: tuple):
        """Rompe la pared que coincide con la posición que se da."""
        firewall_to_break = self.grid.is_there_firewall(pos)
        if firewall_to_break:
            self.grid.cells[pos[0] // TILE_SIZE -
                            1][pos[1] // TILE_SIZE - 1].value = None
            self.grid.firewall_rects.pop(firewall_to_break)
            self.update_steps(1)

    def check_and_open_door(self, pos: tuple):
        """Abre la puerta que coincide con la posición que se da."""
        for door in self.grid.doors:
            if pos[0] // TILE_SIZE - 1 == door.x and pos[1] // TILE_SIZE - 1 == door.y:
                door.open()

    # endregion

    def move_virus(self):
        """Mueve ambos virus al mismo tiempo."""
        self.move_wandering_virus_lin()
        self.move_wandering_virus_sin()

    def move_wandering_virus_lin(self):
        """Controla el movimiento del virus que se mueve de manera lineal."""
        for virus in self.grid.wandering_virus_lin.values():
            if virus[0] != None:
                if virus[0] != 0:
                    virus[0] -= 1
                else:
                    virus[0] = 7

    def move_wandering_virus_sin(self):
        """Controla el movimiento del virus que se mueve de manera sinusoidal."""
        y_delta = 0
        for virus in self.grid.wandering_virus_sin.values():
            if virus[0] != None:
                y_delta = 1 if virus[0] % 2 else -1

                if virus[0] != 0:
                    virus[0] -= 1
                else:
                    virus[0] = 7
                    if virus[1] < 7:
                        virus[1] += 1
                    if virus[1] == 7:
                        virus[1] = 1

                virus[1] += y_delta

    def reset_virus_pos(self, mouse_pos: tuple):
        """Vuelve los virus a sus lugares originales."""
        all_moving_virus = {}
        all_moving_virus.update(self.grid.wandering_virus_lin)
        all_moving_virus.update(self.grid.wandering_virus_sin)

        for virus_id, cell in all_moving_virus.items():
            # "- TILE_SIZE" ajusta por el offset de la grid
            if (mouse_pos[0] - TILE_SIZE) // TILE_SIZE == cell[0] and (mouse_pos[1] - TILE_SIZE) // TILE_SIZE == cell[1]:
                if virus_id in self.grid.wandering_virus_lin.keys():
                    self.grid.wandering_virus_lin[virus_id] = list(
                        self.grid.original_virus_pos[virus_id])
                elif virus_id in self.grid.wandering_virus_sin.keys():
                    self.grid.wandering_virus_sin[virus_id] = list(
                        self.grid.original_virus_pos[virus_id])

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

            next_cell_door = self.grid.is_there_door(next_cell.xy)
            next_cell_empty = True if next_cell.value is None else False
            if next_cell_door:
                if next_cell_door.value is not None:
                    next_cell_empty = False

            farther_cell_door = self.grid.is_there_door(farther_cell.xy)
            farther_cell_empty = True if farther_cell.value is None else False
            if farther_cell_door:
                if farther_cell_door.value is not None:
                    farther_cell_empty = False

            if self.robots[0] == "UAIBOT":

                if next_cell_empty:
                    self.grid.move_element(
                        self.player_cell, next_cell.xy)
                    self.audio_handler.play_sound("res/sounds/move.wav")
                    moved = True

                if next_cell.value == "virus" and farther_cell_empty:
                    self.grid.move_element(next_cell, farther_cell.xy)
                    self.grid.move_element(
                        self.player_cell, next_cell.xy)
                    self.audio_handler.play_sound("res/sounds/move.wav")
                    moved = True

            if self.robots[0] == "UAIBOTA":  # UAIBOTA

                if next_cell_empty:
                    self.grid.move_element(
                        self.player_cell, next_cell.xy)
                    self.audio_handler.play_sound("res/sounds/move.wav")
                    moved = True
                    if prev_cell.value == "virus":
                        self.grid.move_element(
                            prev_cell, self.player_cell.xy)

            if self.robots[0] == "UAIBOTINO":  # UAIBOTINO
                if next_cell_empty:
                    self.grid.move_element(
                        self.player_cell, next_cell.xy)
                    moved = True
                    self.audio_handler.play_sound("res/sounds/move.wav")

                if next_cell.value == "virus" and farther_cell_empty:
                    self.grid.move_element(
                        self.player_cell, farther_cell.xy)
                    self.audio_handler.play_sound("res/sounds/jump.wav")

                    # como UAIBOTINO se mueve dos celdas en vez de una en este caso, la celda próxima a la que se
                    # actualizará su posición corresponde a la celda siguiente a esta
                    next_cell = farther_cell
                    moved = True

            if moved:
                # actualiza la posición del player con el movimiento realizado
                self.player_cell = next_cell

                self.move_virus()
                passed_round = self.check_finished()
                if not passed_round:  # esto hace que el contador de turnos no llegue a cero si se gana con el último movimiento
                    self.update_steps(1)

    def restart(self):
        """Devuelve todo al estado inicial de la ronda."""
        if self.round > 0:
            stay_still_virus = self.grid.wandering_virus_sin
            self.grid.load_round(self.difficulty, self.round)
            self.grid.wandering_virus_sin = stay_still_virus
            self.used_steps = 0
            self.start_time = 0
            self.current_time = 0
            self.elapsed_time = 0
            self.timer = self.time_limit
            self.dead = False

    def reset_game(self):
        """Reinicia el juego desde el principio."""
        self.round = -3
        self.won_game = False
        self.intro_finished = False
        self.difficulty_set = False
        self.steps_used_per_round = []
        self.time_spent_per_round = []
        self.difficulty = 0
        self.start_time = 0
        self.current_time = 0
        self.elapsed_time = 0
        self.audio_handler.stop_music()

    def update_steps(self, steps_delta: int):
        """Maneja el sistema de turnos, haciendo el avance y el reseteo en caso de que se terminen los movimientos habilitados."""
        self.used_steps += steps_delta
        for door in self.grid.doors:
            door.pass_turns()
        if self.used_steps >= self.grid.round_steps:
            self.restart()
            self.audio_handler.interrupt_music(
                "res/sounds/main-theme.mp3",
                "res/sounds/lost.wav")

    def change_robot(self):
        """Ejecuta la rotación entre los robots."""
        self.robots.append(self.robots[0])
        self.robots.pop(0)

    def dead_state(self):
        """Cuando el jugador muere notifica al usuario con un mensaje en pantalla."""
        self.dead = True
        self.screen.blit(
            TEXTURES["text_background_3"], (SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2 - 50, 600, 100))

    # endregion
