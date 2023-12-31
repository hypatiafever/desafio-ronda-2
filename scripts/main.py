"""Equipo: 19014 - THEVECTORS
Institución: 300292400 - ESCUELA DEL CAE D-170
RONDA 2

Crea el juego (mainloop) e inicializa el módulo pygame.

Versión 2.12.3
Estándar de estilo utilizado: PEP8 (https://peps.python.org/pep-0008/)."""

import sys
from math import trunc

import pygame
from audio import AudioHandler
from constants import *
from menus import MovementsMenu, NameMenu, OptionsMenu, PauseMenu, StartMenu
from pygame import Surface
from scene import Scene
from settings import GameSettings
from texturedata import load_textures

SCENE_START_MENU = -3
SCENE_INPUT_NAME = -2
SCENE_INPUT_DIFFICULTY = -1
SCENE_GAME_INTRO = 0


class Game():
    """Contiene la escena y procesa eventos"""

    def __init__(self):

        # definimos el tamaño de la pantalla
        self.screen: Surface = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()  # creamos un reloj para los fps
        load_textures()        
        pygame.display.set_caption("UAIBOT WORLD 2 - OFIRCA 2023 - Ronda 2")

        self.settings: GameSettings = GameSettings()
        self.audio_handler: AudioHandler = AudioHandler(self.settings)
        self.start_menu: StartMenu = StartMenu()
        self.name_menu: NameMenu = NameMenu(self.screen)
        self.options: OptionsMenu = OptionsMenu(self.settings)
        self.mov_amount_ui: MovementsMenu = MovementsMenu()
        self.pause: PauseMenu = PauseMenu()
        self.scene: Scene = Scene(
            self.screen,
            self.audio_handler,
            self.mov_amount_ui,
            self.pause,
            self.name_menu,
            self.start_menu,
            self.options,
            self.settings)

        self.paused = False
        self.running = True
        self.in_rounds = False

        self.data_recorded = False

        self.mouse_moved_amount = 0

    def run(self):
        """Inicia el mainloop del juego."""

        while (self.running):
            self.update()
        self.finish()

    def update(self):
        """Código que se ejecuta en cada frame."""

        # region --- Events ---

        self.in_rounds = self.scene.round > SCENE_GAME_INTRO and self.scene.round <= self.scene.grid.round_count

        # detecta los inputs del usuario
        for event in pygame.event.get():

            if self.scene.round == SCENE_INPUT_NAME:
                self.settings.username = self.name_menu.handle_writing(event)
                if self.settings.username:
                    self.scene.round += 1

            if self.scene.show_options:
                self.options.handle_input(event)

            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and self.in_rounds:  # maneja la activación del estado de pausa
                if event.key == pygame.K_ESCAPE and not self.paused and not self.scene.dead:
                    self.paused = True
                    continue
                elif event.key == pygame.K_ESCAPE and self.paused:
                    if self.scene.show_rules:
                        self.scene.show_rules = False
                    elif self.scene.show_options:
                        self.scene.show_options = False
                    else:
                        self.paused = False
                    continue

            if not self.paused and self.in_rounds:  # maneja el input de las rondas
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.scene.move("right")
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.scene.move("left")
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.scene.move("up")
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.scene.move("down")
                    elif event.key == pygame.K_r:
                        self.scene.restart()
                        self.scene.move_wandering_virus_sin()
                    elif event.key == pygame.K_e:
                        self.scene.change_robot()
                elif event.type == pygame.MOUSEMOTION and not self.scene.dead:
                    self.mouse_moved_amount += 1
                    if self.mouse_moved_amount >= MOUSE_MOV_REQ * self.settings.sensitivity_level:
                        self.scene.move_virus()
                        self.mouse_moved_amount = 0
                elif event.type == pygame.MOUSEBUTTONUP and not self.scene.dead:
                    self.audio_handler.play_sound("res/sounds/click.wav")
                    self.scene.reset_virus_pos(event.pos)
                    self.scene.check_and_break_firewall(event.pos)
                    self.scene.check_and_open_door(event.pos)

            elif event.type == pygame.KEYDOWN and not self.in_rounds:  # maneja el input fuera de las rondas
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and not self.name_menu.active and not self.scene.round == SCENE_START_MENU:
                    self.data_recorded = False
                    self.scene.reset_game()
                # toma cualquier input de tecla durante la intro
                elif self.scene.round == SCENE_GAME_INTRO and self.scene.difficulty_set:
                    self.scene.continue_intro()
                elif self.scene.round == SCENE_START_MENU:
                    self.scene.round += 1

            elif event.type == pygame.MOUSEBUTTONUP:

                # toma la interacción con los botones de la pausa
                if self.paused and not self.scene.show_rules and not self.scene.show_options:
                    result = self.pause.define_button_pressed()
                    if result == 1:
                        self.paused = False
                    elif result == 2:
                        self.running = False
                    elif result == 3:
                        self.scene.show_rules = True
                    elif result == 4:
                        self.scene.show_options = True

                elif self.scene.round == SCENE_INPUT_DIFFICULTY:
                    # toma la interacción con los botones de dificultad
                    result = self.mov_amount_ui.define_button_pressed()
                    if result:
                        self.scene.difficulty = result - 1
                        self.scene.difficulty_set = True
                        self.scene.round += 1

                elif self.scene.round == SCENE_START_MENU:
                    self.scene.round += 1

                elif self.scene.round == SCENE_GAME_INTRO and self.scene.difficulty_set:
                    # toma el paso de la intro
                    self.scene.continue_intro()
        # endregion

        if self.scene.round > self.scene.grid.round_count and not self.data_recorded:
            self.scene.won_game = True
            self.data_recorded = True
            self.write_to_scoreboard()

        self.scene.update(self.in_rounds, self.paused)
        pygame.display.update()
        self.clock.tick(FPS)

    def write_to_scoreboard(self):
        """Guarda la información del usuario en el ranking.txt."""
        pass
        full_string = self.settings.username
        with open("res/ranking.txt", "a") as sb:
            for index in range(self.scene.grid.round_count):
                full_string += f" | n{index + 1}: {self.scene.steps_used_per_round[index] + 1} steps, {trunc(self.scene.time_spent_per_round[index])} seconds"
            full_string += "\n"
            sb.write(full_string)

    def finish(self):
        """Finaliza el programa."""
        self.audio_handler.stop_music()
        pygame.quit()
        sys.exit()


# Inicio del programa
if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
